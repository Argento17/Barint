"""
provenance_gate.py — Bari C0 Provenance Enforcement Gate
=========================================================
A deterministic gate that proves a served frontend score JSON was produced by
the canonical pipeline (configs/*.json -> rescore_all.py -> generate_page.py)
with a fully recorded, version-controlled origin.

WHY THIS EXISTS
---------------
The canonical pipeline records provenance (generate_page.py stamps
config_sha256, generator_version, source_paths). The failure was that NOTHING
ENFORCED it: some live scores were produced by ad-hoc scripts OUTSIDE the
pipeline with null _meta.run_id, null scoring.bsip1_dir, and — most dangerous —
UNTRACKED source corpora (the corpus that produced the live numbers is not in
version control, so the scores are unreproducible and unauditable).

This gate makes the provenance MANDATORY. A served file PASSES only if it can
be traced back to a committed origin through a binding config.

PASS REQUIRES ALL FIVE:
  R1  _meta exists AND carries a provenance identity:
        a non-null run_id  OR  a config_sha256.
  R2  The COMPLETE scoring flag vector (the BARI_* flags used) is recorded —
        in _meta (scoring_flags / flags) OR in the bound config (scoring.flags).
  R3  generator_version (or equivalent engine/generator stamp) is present —
        in _meta OR in the bound config.
  R4  The backing source corpus (run_products_dir / corpus_dirs) is COMMITTED
        IN GIT. Determined read-only via `git ls-files`. An untracked source
        dir = FAIL ("origin not in version control").
  R5  A config in configs/*.json binds this served file (resolved by category
        or by served-file / baseline_json name), AND the bound corpus dirs
        exist on disk.

Each failure names exactly what is missing.

SEVERITY
--------
Failures are classified so the table separates real, unauditable defects from
the cosmetic stamp gap:
  HARD   R1 (no provenance identity), R4 (origin not in version control),
         R5 (no binding config) — the served numbers are unreproducible or
         their origin is untraceable. THESE are the real forensic defects.
  SOFT   R3 (missing generator/engine stamp) — provenance is otherwise intact;
         the file simply predates generate_page self-stamping. Deliverable 3
         (generate_page emits generator_version into _meta) closes this.
  R2 is HARD when the flag vector is absent entirely.
A file PASSES only with zero failures of any severity. `--all` annotates each
FAIL row with [HARD] or [SOFT-ONLY] so reviewers can see the off-spine files
fail on HARD defects while the legacy-canonical files fail only on the cosmetic
stamp that Deliverable 3 fixes.

USAGE
-----
  Single file:
    python provenance_gate.py <served_file.json>
  Scan every config-bound live served file and print a PASS/FAIL table:
    python provenance_gate.py --all

  Options:
    --configs-dir <dir>   directory of configs/*.json (default: ../configs
                          relative to this script — the canonical location)
    --repo-root <dir>     git repo root used for `git ls-files` tracking checks
                          (default: auto-detected from --configs-dir upward)
    --json                machine-readable JSON output

NOTE ON READ-ONLY OPERATION
---------------------------
This gate ONLY reads. It runs `git ls-files` / `git status` against the repo
(read-only git). It never writes, moves, or commits anything.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Path / repo helpers
# ---------------------------------------------------------------------------

def _here() -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__)))


def default_configs_dir() -> Path:
    # gates/ -> page_generator/ -> configs/
    return (_here().parent / "configs").resolve()


def find_repo_root(start: Path) -> Path:
    """Walk upward from `start` until a directory containing .git is found."""
    p = start.resolve()
    for cand in [p] + list(p.parents):
        if (cand / ".git").exists():
            return cand
    # Fallback: assume C:\Bari layout (configs is 3 levels under root)
    return start.resolve()


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def norm_path(raw, repo_root: Path):
    """
    Normalize a config-declared path (often Windows-style 'C:\\Bari\\...') to:
      (abs_path: Path, rel_to_repo: str or None)
    rel_to_repo is the POSIX path relative to repo_root if the path is inside
    the repo, used for `git ls-files`.
    """
    if not raw:
        return None, None
    s = str(raw).replace("\\", "/")
    abs_path = Path(s)
    if not abs_path.is_absolute():
        abs_path = (repo_root / s).resolve()
    else:
        abs_path = abs_path.resolve()
    try:
        rel = abs_path.relative_to(repo_root.resolve())
        rel_posix = rel.as_posix()
    except ValueError:
        rel_posix = None
    return abs_path, rel_posix


# ---------------------------------------------------------------------------
# Git tracking (read-only)
# ---------------------------------------------------------------------------

def git_tracked_count(rel_posix, repo_root: Path):
    """
    Return the number of files git tracks under rel_posix (read-only).
    rel_posix must be repo-relative POSIX. Returns -1 on git error.
    """
    if rel_posix is None:
        return None  # cannot evaluate — path outside repo
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", rel_posix],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return -1
        lines = [ln for ln in result.stdout.splitlines() if ln.strip()]
        return len(lines)
    except Exception:
        return -1


# ---------------------------------------------------------------------------
# Config index: build served-file -> config binding
# ---------------------------------------------------------------------------

def build_config_index(configs_dir: Path):
    """
    Scan configs/*.json (skipping _generated_* scratch configs) and build:
      by_baseline_name[basename(baseline_json)] = (config_path, config_dict)
      by_category[category]                       = (config_path, config_dict)
    """
    by_baseline = {}
    by_category = {}
    if not configs_dir.is_dir():
        return by_baseline, by_category
    for fname in sorted(os.listdir(configs_dir)):
        if not fname.endswith(".json"):
            continue
        if fname.startswith("_generated_"):
            continue  # scratch / regenerated configs, not the binding source
        fpath = configs_dir / fname
        try:
            cfg = load_json(fpath)
        except Exception:
            continue
        baseline = cfg.get("baseline_json")
        if baseline:
            by_baseline[os.path.basename(str(baseline).replace("\\", "/"))] = (fpath, cfg)
        cat = cfg.get("category")
        if cat:
            by_category.setdefault(cat, (fpath, cfg))
    return by_baseline, by_category


def resolve_config_for_served(served_path: Path, served_meta, by_baseline, by_category):
    """
    Resolve the binding config for a served file.
    Priority:
      1. by served-file basename matching a config baseline_json basename
      2. by _meta.category matching a config category
    Returns (config_path, config_dict) or (None, None).
    """
    base = served_path.name
    if base in by_baseline:
        return by_baseline[base]
    cat = (served_meta or {}).get("category")
    if cat and cat in by_category:
        return by_category[cat]
    return None, None


# ---------------------------------------------------------------------------
# Flag-vector extraction
# ---------------------------------------------------------------------------

def extract_flag_vector(meta, config):
    """
    Return (flags_dict_or_None, source_str).
    Looks in _meta first (scoring_flags / flags / scoring.flags), then config.
    A flag vector must be a non-empty dict to count.
    """
    if isinstance(meta, dict):
        for key in ("scoring_flags", "flags"):
            v = meta.get(key)
            if isinstance(v, dict) and v:
                return v, f"_meta.{key}"
        sc = meta.get("scoring")
        if isinstance(sc, dict) and isinstance(sc.get("flags"), dict) and sc["flags"]:
            return sc["flags"], "_meta.scoring.flags"
    if isinstance(config, dict):
        sc = config.get("scoring")
        if isinstance(sc, dict) and isinstance(sc.get("flags"), dict) and sc["flags"]:
            return sc["flags"], "config.scoring.flags"
    return None, None


def extract_generator_stamp(meta, config):
    """Return (value_or_None, source_str) for the generator/engine version stamp."""
    candidates = ("generator_version", "generator", "engine_version",
                  "engine", "schema_version")
    if isinstance(meta, dict):
        for k in candidates:
            v = meta.get(k)
            if v:
                return v, f"_meta.{k}"
    if isinstance(config, dict):
        sc = config.get("scoring", {})
        # configs don't normally carry generator_version, but check _source as a
        # weak engine stamp ONLY if it names a generator (not an ad-hoc script).
        gv = config.get("generator_version")
        if gv:
            return gv, "config.generator_version"
    return None, None


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def evaluate(served_path: Path, configs_dir: Path, repo_root: Path):
    """
    Evaluate one served file against R1..R5.
    Returns a dict: {file, category, passed (bool), failures [str], detail {...}}
    """
    failures = []
    detail = {}

    try:
        served = load_json(served_path)
    except Exception as e:
        return {
            "file": served_path.name,
            "category": None,
            "passed": False,
            "failures": [f"unreadable_served_file: {e}"],
            "detail": {},
        }

    meta = served.get("_meta") if isinstance(served, dict) else None
    by_baseline, by_category = build_config_index(configs_dir)
    config_path, config = resolve_config_for_served(served_path, meta, by_baseline, by_category)
    category = (meta or {}).get("category") if isinstance(meta, dict) else None

    # ---- R1: _meta + provenance identity ---------------------------------
    if not isinstance(meta, dict) or not meta:
        failures.append("R1 missing: no _meta block")
    else:
        run_id = meta.get("run_id")
        config_sha = meta.get("config_sha256")
        has_identity = (run_id is not None and str(run_id).strip() != "") or \
                       (config_sha is not None and str(config_sha).strip() != "")
        detail["run_id"] = run_id
        detail["config_sha256"] = config_sha
        if not has_identity:
            failures.append("R1 missing: _meta has neither a non-null run_id nor a config_sha256 (no provenance identity)")

    # ---- R5 (resolve config first; R2/R3/R4 may depend on it) ------------
    if config is None:
        failures.append("R5 missing: no config in configs/*.json binds this served file (resolved by served-file name or category)")
    else:
        detail["bound_config"] = config_path.name
        # corpus dirs must exist
        corpus_dirs = config.get("corpus_dirs", [])
        if isinstance(corpus_dirs, str):
            corpus_dirs = [corpus_dirs]
        run_dir_raw = config.get("run_products_dir")
        run_dirs = run_dir_raw if isinstance(run_dir_raw, list) else ([run_dir_raw] if run_dir_raw else [])
        missing_exist = []
        all_source = list(corpus_dirs) + list(run_dirs)
        for d in all_source:
            ap, _ = norm_path(d, repo_root)
            if ap is None or not ap.exists():
                missing_exist.append(str(d))
        if missing_exist:
            failures.append(f"R5 missing: bound config corpus/run dir(s) do not exist on disk: {missing_exist}")

    # ---- R2: complete scoring flag vector --------------------------------
    flags, flags_src = extract_flag_vector(meta, config)
    detail["flag_vector_source"] = flags_src
    detail["flag_count"] = len(flags) if flags else 0
    if not flags:
        failures.append("R2 missing: no scoring flag vector (BARI_* flags) recorded in _meta or bound config")

    # ---- R3: generator / engine version stamp ----------------------------
    gv, gv_src = extract_generator_stamp(meta, config)
    detail["generator_stamp"] = gv
    detail["generator_stamp_source"] = gv_src
    if not gv:
        failures.append("R3 missing: no generator_version / engine version stamp in _meta or bound config")

    # ---- R4: backing source corpus committed in git ----------------------
    # Use the bound config's source dirs if available; else _meta.source_paths.
    src_dirs = []
    if config is not None:
        cd = config.get("corpus_dirs", [])
        if isinstance(cd, str):
            cd = [cd]
        rd = config.get("run_products_dir")
        rd = rd if isinstance(rd, list) else ([rd] if rd else [])
        src_dirs = list(cd) + list(rd)
    elif isinstance(meta, dict):
        sp = meta.get("source_paths", {}) or {}
        cd = sp.get("corpus_dirs", []) or []
        rd = sp.get("run_products_dir", []) or []
        if isinstance(cd, str):
            cd = [cd]
        if isinstance(rd, str):
            rd = [rd]
        src_dirs = list(cd) + list(rd)

    if not src_dirs:
        failures.append("R4 missing: no source corpus dirs declared (cannot verify version control)")
    else:
        untracked = []
        tracked_summary = {}
        for d in src_dirs:
            ap, rel = norm_path(d, repo_root)
            if rel is None:
                untracked.append(f"{d} (outside repo — cannot be version-controlled here)")
                continue
            n = git_tracked_count(rel, repo_root)
            tracked_summary[rel] = n
            if n is None:
                untracked.append(f"{d} (path outside repo)")
            elif n == -1:
                untracked.append(f"{d} (git error checking tracking)")
            elif n == 0:
                untracked.append(f"{d} (0 tracked files — origin not in version control)")
        detail["git_tracked"] = tracked_summary
        if untracked:
            failures.append(f"R4 FAIL: backing source corpus not committed in git: {untracked}")

    # Classify severity: any failure whose code is not R3 is HARD.
    # (R3 is the cosmetic generator-stamp gap that Deliverable 3 closes.)
    def is_hard(msg):
        return not msg.startswith("R3 ")
    hard = [f for f in failures if is_hard(f)]
    soft = [f for f in failures if not is_hard(f)]
    if not failures:
        severity = "PASS"
    elif hard:
        severity = "HARD"
    else:
        severity = "SOFT-ONLY"

    return {
        "file": served_path.name,
        "category": category,
        "passed": len(failures) == 0,
        "severity": severity,
        "hard_failures": hard,
        "soft_failures": soft,
        "failures": failures,
        "detail": detail,
    }


# ---------------------------------------------------------------------------
# --all: enumerate config-bound live served files
# ---------------------------------------------------------------------------

def enumerate_served_files(configs_dir: Path, repo_root: Path):
    """
    Every live served file = the baseline_json of every non-scratch config.
    Returns sorted list of Path. Missing files are still returned (they will
    FAIL R1 as unreadable, which is correct).
    """
    by_baseline, _ = build_config_index(configs_dir)
    paths = []
    seen = set()
    for fname in sorted(os.listdir(configs_dir)):
        if not fname.endswith(".json") or fname.startswith("_generated_"):
            continue
        try:
            cfg = load_json(configs_dir / fname)
        except Exception:
            continue
        b = cfg.get("baseline_json")
        if not b:
            continue
        ap, _ = norm_path(b, repo_root)
        if ap and str(ap) not in seen:
            seen.add(str(ap))
            paths.append(ap)
    return sorted(paths, key=lambda p: p.name)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Bari C0 provenance gate")
    ap.add_argument("served_file", nargs="?", help="Path to a served frontend JSON")
    ap.add_argument("--all", action="store_true",
                    help="Scan every config-bound live served file")
    ap.add_argument("--configs-dir", default=None,
                    help="Configs directory (default: ../configs next to this script)")
    ap.add_argument("--repo-root", default=None,
                    help="Git repo root for tracking checks (default: auto)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    configs_dir = Path(args.configs_dir).resolve() if args.configs_dir else default_configs_dir()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else find_repo_root(configs_dir)

    if args.all:
        served_files = enumerate_served_files(configs_dir, repo_root)
        results = [evaluate(p, configs_dir, repo_root) for p in served_files]

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            n_pass = sum(1 for r in results if r["passed"])
            n_fail = len(results) - n_pass
            print(f"PROVENANCE GATE — {len(results)} served files  "
                  f"({n_pass} PASS / {n_fail} FAIL)")
            print(f"  configs: {configs_dir}")
            print(f"  repo:    {repo_root}")
            print("-" * 78)
            n_hard = sum(1 for r in results if r["severity"] == "HARD")
            n_soft = sum(1 for r in results if r["severity"] == "SOFT-ONLY")
            print(f"{'RESULT':<11} {'CATEGORY':<18} {'SERVED FILE':<40}")
            print("-" * 78)
            for r in results:
                if r["passed"]:
                    tag = "PASS"
                elif r["severity"] == "HARD":
                    tag = "FAIL[HARD]"
                else:
                    tag = "FAIL[SOFT]"
                cat = (r["category"] or "-")[:18]
                print(f"{tag:<11} {cat:<18} {r['file']:<40}")
                if not r["passed"]:
                    for f in r["failures"]:
                        print(f"            - {f}")
            print("-" * 78)
            print(f"TOTAL: {n_pass} PASS / {n_fail} FAIL "
                  f"({n_hard} HARD = real provenance defects, "
                  f"{n_soft} SOFT-ONLY = cosmetic stamp gap closed by Deliverable 3)")
        sys.exit(0 if all(r["passed"] for r in results) else 1)

    if not args.served_file:
        ap.error("provide a served_file or use --all")

    served_path = Path(args.served_file).resolve()
    r = evaluate(served_path, configs_dir, repo_root)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        tag = "PASS" if r["passed"] else "FAIL"
        print(f"{tag}: {r['file']} (category={r['category']})")
        for f in r["failures"]:
            print(f"  - {f}")
    sys.exit(0 if r["passed"] else 1)


if __name__ == "__main__":
    main()
