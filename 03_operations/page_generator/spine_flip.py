#!/usr/bin/env python3
"""
spine_flip.py — Spine step 4: orchestration command (P169 / TASK-319).

Chains the existing verified pieces (orchestration ONLY):
  affected_set.py --set ...  → affected shelves + FROZEN GATE (exit 2 on breach, never proceed)
  rescore_all.py --shelf <s> (with flag overrides via env for the what-if)
  copy_stage.py --staging <rescored> --live <config.baseline_json> --shelf <s>
  gates/run_gates.py <post-copy page> --config <shelf.json> --baseline <live> [--schema ... --corpus ... --run ...]

Staging-only under _rescore_staging/. NO engine/scoring changes. NO bari-web edits.
NO git push, NO PR, NO deploy — produce bundle + report; owner performs merge/deploy.
OFF-ban absolute (TASK-238): never source, never substitute, never reference in code paths.

CLI:
  python spine_flip.py --set BARI_X=on [--set BARI_Y=off ...] [--note "..."] [--out-dir _rescore_staging/_spine_runs/<ts>]

Exit:
  2 = frozen breach (hard block)
  1 = movement processed (with per-shelf errors recorded)
  0 = no movement

Final line (always):
  "DEPLOY-READY: N shelves, M products need copy authoring, gates <PASS/REVIEW>, frozen breach <none|...>. No push performed."

Produces in --out-dir:
  - spine_run_report.json + .md (full aggregate + per-shelf)
  - consolidated_author_set.json
  - per affected shelf/ subdir with copy-applied <s>_rescored.json + author_set.json + *_gates_report.md
  - copy of affected_set.json for the run

Graceful: shelf error recorded (not fatal to run). All integrity surface honestly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
PAGE_GEN = REPO / "03_operations" / "page_generator"
CONFIGS_DIR = PAGE_GEN / "configs"
STAGING_ROOT = REPO / "_rescore_staging"
SPINE_RUNS = STAGING_ROOT / "_spine_runs"

AFFECTED_PY = PAGE_GEN / "affected_set.py"
RESCORE_PY = PAGE_GEN / "rescore_all.py"
COPY_PY = PAGE_GEN / "copy_stage.py"
GATES_PY = PAGE_GEN / "gates" / "run_gates.py"
SCHEMA_V3 = PAGE_GEN / "contract" / "page_output_schema_v3.json"


def load_json(p: Path) -> dict[str, Any]:
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json(p: Path, data: dict[str, Any]) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    p.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_path(p: Path) -> str:
    if not p.is_file():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_subprocess(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    description: str = "",
) -> tuple[int, str, str]:
    """Run cmd, capture stdout/stderr, return (exit, stdout, stderr). Prints header + tail of output."""
    print(f"\n>>> {description or ' '.join(cmd)}")
    t0 = time.perf_counter()
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed = time.perf_counter() - t0
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    # Print a bounded amount for visibility (head + tail if long)
    combined = (stdout + "\n" + stderr).strip()
    if combined:
        lines = combined.splitlines()
        if len(lines) > 60:
            print("\n".join(lines[:30]))
            print(f"  ... [{len(lines)-60} lines elided] ...")
            print("\n".join(lines[-30:]))
        else:
            print(combined)
    print(f"<<< exit={result.returncode} ({elapsed:.1f}s)")
    return result.returncode, stdout, stderr


def parse_flag_sets(sets: list[str] | None) -> dict[str, str]:
    overrides: dict[str, str] = {}
    if not sets:
        return overrides
    for item in sets:
        if "=" not in item:
            print(f"ERROR: invalid --set '{item}', expected KEY=VAL", file=sys.stderr)
            sys.exit(3)
        k, v = item.split("=", 1)
        overrides[k.strip()] = v.strip()
    return overrides


def get_shelf_config(shelf: str) -> tuple[Path, dict[str, Any]]:
    cfg_path = CONFIGS_DIR / f"{shelf}.json"
    if not cfg_path.is_file():
        raise FileNotFoundError(f"no config for shelf {shelf}: {cfg_path}")
    cfg = load_json(cfg_path)
    return cfg_path, cfg


def get_baseline(cfg: dict[str, Any]) -> Path:
    b = cfg.get("baseline_json")
    if not b:
        raise ValueError("config missing baseline_json")
    bp = Path(b)
    if not bp.is_file():
        raise FileNotFoundError(f"baseline not found: {bp}")
    return bp


def derive_corpus_run_for_gates(cfg: dict[str, Any], shelf: str) -> tuple[str | None, str | None]:
    """Return (corpus_dir, run_products_dir) best effort from config + staging layout."""
    corpus: str | None = None
    corpus_dirs = cfg.get("corpus_dirs") or []
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    for d in corpus_dirs:
        if d and Path(d).is_dir():
            corpus = str(d)
            break
    if not corpus:
        scoring = cfg.get("scoring") or {}
        bs = scoring.get("bsip1_dir")
        if bs and Path(bs).is_dir():
            corpus = str(bs)

    run_dir = str(STAGING_ROOT / shelf / "products")
    if not Path(run_dir).is_dir():
        # fallback to config run_products_dir (pre-rescore)
        rp = cfg.get("run_products_dir")
        if rp:
            if isinstance(rp, list):
                rp = next((x for x in rp if x and Path(x).is_dir()), None)
            if rp and Path(rp).is_dir():
                run_dir = str(rp)
            else:
                run_dir = None
        else:
            run_dir = None
    return corpus, run_dir


def count_off_in_page(page: dict[str, Any]) -> int:
    import re
    OFF_RE = re.compile(r"open_food_facts|openfoodfacts\.org|images\.openfoodfacts|off_candidate_panel", re.IGNORECASE)
    return len(OFF_RE.findall(json.dumps(page.get("products", []), ensure_ascii=False)))


def build_consolidated_author( per_shelf_authors: list[dict[str, Any]] ) -> dict[str, Any]:
    all_needed: list[dict[str, Any]] = []
    total = 0
    by_shelf: dict[str, Any] = {}
    for entry in per_shelf_authors:
        shelf = entry["shelf"]
        data = entry["author_set"]
        needed = data.get("authored_needed", [])
        total += len(needed)
        by_shelf[shelf] = {
            "author_needed": len(needed),
            "carried": data.get("carried", 0),
            "pending_carried": data.get("pending_carried", 0),
        }
        for item in needed:
            item2 = dict(item)
            item2["shelf"] = shelf
            all_needed.append(item2)
    return {
        "total_author_needed": total,
        "by_shelf": by_shelf,
        "authored_needed": all_needed,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Spine orchestrator: flag what-if → affected + frozen gate → rescore + copy + gate → deploy-ready bundle (staging only)."
    )
    parser.add_argument(
        "--set",
        action="append",
        metavar="FLAG=VAL",
        help="scoring flag override for the what-if (repeatable). Passed to affected_set and to rescore env.",
    )
    parser.add_argument("--note", default="", help="free text note for the spine run report")
    parser.add_argument(
        "--out-dir",
        default=None,
        help="explicit output dir for the deploy bundle (default: _rescore_staging/_spine_runs/<utc-ts>)",
    )
    args = parser.parse_args()

    t_start = time.perf_counter()
    commands_run: list[dict[str, Any]] = []

    overrides = parse_flag_sets(args.set)
    if not overrides:
        print("ERROR: at least one --set FLAG=VAL is required", file=sys.stderr)
        return 3

    flag_str = " ".join(f"{k}={v}" for k, v in overrides.items())
    print(f"SPINE FLIP start  flags={flag_str}  note={args.note or '(none)'}")

    # --- 1. Affected set + FROZEN GATE ---
    affected_path = REPO / "affected_set_spine.json"  # temp working name; will be copied to bundle
    affected_cmd = [
        sys.executable,
        str(AFFECTED_PY),
    ]
    for k, v in overrides.items():
        affected_cmd.extend(["--set", f"{k}={v}"])
    affected_cmd.extend(["--out", str(affected_path)])

    exit_a, out_a, err_a = run_subprocess(
        affected_cmd, cwd=REPO, description="affected_set.py (shadow diff + shelf map + frozen gate)"
    )
    commands_run.append({"cmd": " ".join(affected_cmd), "exit_code": exit_a})

    if not affected_path.is_file():
        print("ERROR: affected_set.py did not produce output", file=sys.stderr)
        return 3
    affected = load_json(affected_path)
    frozen_touched = bool(affected.get("frozen_touched"))
    affected_shelves: list[str] = list(affected.get("affected_shelves") or [])
    frozen_breaches: list[str] = list(affected.get("frozen_breaches") or [])

    # Prepare out_dir early so block reports still land somewhere
    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = SPINE_RUNS / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    # Always copy the affected manifest for the run into bundle
    bundle_affected = out_dir / "affected_set.json"
    shutil.copy2(affected_path, bundle_affected)

    if frozen_touched:
        # HARD BLOCK — write report, exit 2, no further scoring/copy/gates
        block_report = {
            "spine": "flip",
            "flag_overrides": overrides,
            "note": args.note,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "frozen_touched": True,
            "frozen_breaches": frozen_breaches,
            "affected_shelves": affected_shelves,
            "verdict": "FROZEN_BREACH_BLOCK",
            "affected_set_sha": sha256_path(bundle_affected),
        }
        write_json(out_dir / "spine_run_report.json", block_report)
        md = [
            f"# Spine Flip — FROZEN BREACH BLOCK",
            "",
            f"flags: {flag_str}",
            f"note: {args.note}",
            f"generated: {block_report['generated_at']}",
            "",
            f"**FROZEN BREACH** — {', '.join(frozen_breaches) or 'unknown'}",
            "This is a hard stop. No rescore, no copy, no gates, no bundle of staged pages.",
            "Owner must resolve the invariant violation before any further spine action on these flags.",
            "",
            "See affected_set.json for full shadow details.",
        ]
        (out_dir / "spine_run_report.md").write_text("\n".join(md), encoding="utf-8")
        print("\n=== FROZEN BREACH — HARD BLOCK (exit 2) ===")
        print(f"frozen_breaches: {', '.join(frozen_breaches)}")
        print(f"Report bundle: {out_dir}")
        print(f"DEPLOY-READY: 0 shelves, 0 products need copy authoring, gates N/A, frozen breach {','.join(frozen_breaches) or 'yes'}. No push performed.")
        elapsed = time.perf_counter() - t_start
        print(f"Total wall time: {elapsed:.1f}s")
        return 2

    if not affected_shelves:
        # No movement — clean exit 0, still emit minimal report + affected
        empty_report = {
            "spine": "flip",
            "flag_overrides": overrides,
            "note": args.note,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "frozen_touched": False,
            "frozen_breaches": [],
            "affected_shelves": [],
            "verdict": "NO_MOVEMENT",
            "affected_set_sha": sha256_path(bundle_affected),
        }
        write_json(out_dir / "spine_run_report.json", empty_report)
        (out_dir / "spine_run_report.md").write_text(
            "# Spine Flip — NO MOVEMENT\n\n" + json.dumps(overrides) + "\n\nNo shelves required re-score.",
            encoding="utf-8",
        )
        print("\n=== NO MOVEMENT (exit 0) ===")
        print(f"DEPLOY-READY: 0 shelves, 0 products need copy authoring, gates N/A, frozen breach none. No push performed.")
        elapsed = time.perf_counter() - t_start
        print(f"Total wall time: {elapsed:.1f}s")
        return 0

    print(f"Affected shelves ({len(affected_shelves)}): {', '.join(affected_shelves)}")

    # --- Process each shelf ---
    per_shelf: list[dict[str, Any]] = []
    per_shelf_authors: list[dict[str, Any]] = []
    all_commands: list[dict[str, Any]] = list(commands_run)

    for shelf in affected_shelves:
        print(f"\n========== SHELF: {shelf} ==========")
        shelf_rec: dict[str, Any] = {
            "shelf": shelf,
            "rescore_exit": None,
            "copy_exit": None,
            "gate_exit": None,
            "score_moves": 0,
            "grade_moves": 0,
            "carried": 0,
            "author_needed": 0,
            "off_count": 0,
            "gate_overall": "UNKNOWN",
            "gate_report": None,
            "error": None,
            "staged_page_in_bundle": None,
        }
        try:
            cfg_path, cfg = get_shelf_config(shelf)
            baseline_path = get_baseline(cfg)

            # 2. RESCORE (with flag overrides in env)
            run_env = os.environ.copy()
            for k, v in overrides.items():
                run_env[k] = v
            rescore_cmd = [sys.executable, str(RESCORE_PY), "--shelf", shelf]
            rexit, rout, rerr = run_subprocess(
                rescore_cmd, cwd=REPO, env=run_env, description=f"rescore_all.py --shelf {shelf} (flags={flag_str})"
            )
            all_commands.append({"cmd": " ".join(rescore_cmd), "exit_code": rexit})
            shelf_rec["rescore_exit"] = rexit

            staged = STAGING_ROOT / shelf / f"{shelf}_rescored.json"
            if not staged.is_file():
                shelf_rec["error"] = "rescore did not produce _rescored.json"
                per_shelf.append(shelf_rec)
                continue

            # Capture moves/off from the single-shelf run_summary (rescore_all writes it)
            moves = {"score_moves": 0, "grade_moves": 0, "off_count": 0}
            rsumm = STAGING_ROOT / "run_summary.json"
            if rsumm.is_file():
                try:
                    summ = load_json(rsumm)
                    for ent in summ.get("shelves", []):
                        if ent.get("shelf") == shelf:
                            moves["score_moves"] = int(ent.get("score_moves") or 0)
                            moves["grade_moves"] = int(ent.get("grade_moves") or 0)
                            moves["off_count"] = int(ent.get("off_count") or 0)
                            break
                except Exception:
                    pass
            shelf_rec["score_moves"] = moves["score_moves"]
            shelf_rec["grade_moves"] = moves["grade_moves"]
            shelf_rec["off_count"] = moves["off_count"]

            # 3. COPY STAGE
            copy_cmd = [
                sys.executable, str(COPY_PY),
                "--staging", str(staged),
                "--live", str(baseline_path),
                "--shelf", shelf,
            ]
            cexit, cout, cerr = run_subprocess(
                copy_cmd, cwd=REPO, description=f"copy_stage.py for {shelf}"
            )
            all_commands.append({"cmd": " ".join(copy_cmd), "exit_code": cexit})
            shelf_rec["copy_exit"] = cexit

            author_p = STAGING_ROOT / shelf / "author_set.json"
            if author_p.is_file():
                try:
                    adata = load_json(author_p)
                    shelf_rec["carried"] = int(adata.get("carried", 0))
                    shelf_rec["author_needed"] = len(adata.get("authored_needed", []))
                    per_shelf_authors.append({"shelf": shelf, "author_set": adata})
                except Exception as e:
                    shelf_rec["error"] = (shelf_rec.get("error") or "") + f"; author_set load: {e}"

            # 4. GATES (post-copy; pass config+baseline per spec; add corpus/run/schema for integrity gates)
            corpus_arg, run_arg = derive_corpus_run_for_gates(cfg, shelf)
            gate_cmd = [
                sys.executable, str(GATES_PY),
                str(staged),
                "--config", str(cfg_path),
                "--baseline", str(baseline_path),
            ]
            if SCHEMA_V3.is_file():
                gate_cmd += ["--schema", str(SCHEMA_V3)]
            if corpus_arg:
                gate_cmd += ["--corpus", corpus_arg]
            if run_arg:
                gate_cmd += ["--run", run_arg]

            gexit, gout, gerr = run_subprocess(
                gate_cmd, cwd=REPO, description=f"run_gates.py for {shelf} (post-copy)"
            )
            all_commands.append({"cmd": " ".join(gate_cmd), "exit_code": gexit})
            shelf_rec["gate_exit"] = gexit
            shelf_rec["gate_overall"] = "PASS" if gexit == 0 else "FAIL"

            gate_rp = STAGING_ROOT / shelf / f"{shelf}_rescored_gates_report.md"
            if gate_rp.is_file():
                shelf_rec["gate_report"] = str(gate_rp)

            # Note OFF count: prefer the one captured at rescore time (pre-copy; copy does not touch OFF)
            # If copy somehow affected, re-count but OFF ban means we expect 0 anyway.
            try:
                page_now = load_json(staged)
                shelf_rec["off_count"] = count_off_in_page(page_now)
            except Exception:
                pass

        except Exception as exc:
            shelf_rec["error"] = str(exc)
            print(f"  SHELF ERROR [{shelf}]: {exc}", file=sys.stderr)

        per_shelf.append(shelf_rec)

    # --- Aggregate report + bundle ---
    consolidated = build_consolidated_author(per_shelf_authors)
    total_author = consolidated["total_author_needed"]

    # Compute gate summary
    gate_fails = [s["shelf"] for s in per_shelf if s.get("gate_overall") == "FAIL"]
    integrity_flags: list[str] = []
    INTEGRITY_GATES = ["G4 OFF", "G5 GRADE-INTEGRITY", "G7 PARITY", "G8 DATA-SANITY"]
    for srec in per_shelf:
        if srec.get("error"):
            continue
        # Parse the captured gate stdout (gout) for honest FAILs on integrity gates
        # (the gate_res was run just before; we re-capture? Use report file as authoritative.)
        gr = srec.get("gate_report")
        gout_for_parse = ""
        if gr and Path(gr).is_file():
            try:
                gout_for_parse = Path(gr).read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
        for gname in INTEGRITY_GATES:
            # Look for the header line containing FAIL for that gate
            if gname in gout_for_parse:
                # crude but sufficient: if a FAIL appears in the section before next gate header
                sec_start = gout_for_parse.find(gname)
                sec_end = len(gout_for_parse)
                for ng in ["[PASS]", "[FAIL]", "[WARN]", "[SKIP]", "### "]:
                    nxt = gout_for_parse.find(ng, sec_start + 1)
                    if 0 < nxt < sec_end:
                        sec_end = nxt
                section = gout_for_parse[sec_start:sec_end]
                if "FAIL:" in section or "\n  FAIL " in section:
                    integrity_flags.append(f"{srec['shelf']}:{gname}")
    gates_summary = "PASS" if not gate_fails else "REVIEW"
    if integrity_flags:
        gates_summary = "REVIEW (integrity)"

    overall_verdict = "READY" if (not gate_fails and not any(s.get("error") for s in per_shelf)) else "REVIEW"

    spine_report = {
        "spine": "flip",
        "flag_overrides": overrides,
        "note": args.note,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "frozen_touched": False,
        "frozen_breaches": [],
        "affected_shelves": affected_shelves,
        "per_shelf": per_shelf,
        "consolidated_author": {
            "total_author_needed": total_author,
            "by_shelf": consolidated["by_shelf"],
        },
        "gates_summary": gates_summary,
        "integrity_flags": integrity_flags,
        "overall_verdict": overall_verdict,
        "affected_set_sha": sha256_path(bundle_affected),
        "commands_run": all_commands,
    }
    report_sha = write_json(out_dir / "spine_run_report.json", spine_report)

    # Human .md
    md_lines = [
        "# Spine Flip Run Report",
        "",
        f"**flags:** {flag_str}",
        f"**note:** {args.note}",
        f"**generated:** {spine_report['generated_at']}",
        f"**verdict:** {overall_verdict}",
        "",
        "## Summary",
        f"- Shelves processed: {len(affected_shelves)}",
        f"- Products needing copy authoring (consolidated): {total_author}",
        f"- Gates: {gates_summary}",
        f"- Frozen breach: none",
        "",
        "## Per-shelf",
    ]
    for s in per_shelf:
        err = f" ERROR: {s['error']}" if s.get("error") else ""
        md_lines.append(
            f"- {s['shelf']}: score_moves={s['score_moves']} grade_moves={s['grade_moves']} "
            f"carried={s['carried']} author_needed={s['author_needed']} off={s['off_count']} "
            f"gate={s['gate_overall']} {err}"
        )
    if integrity_flags:
        md_lines.append("")
        md_lines.append("**Integrity flags (G4/G5/G7/G8 FAILs):**")
        for f in integrity_flags:
            md_lines.append(f"  - {f}")
    md_lines += [
        "",
        "See spine_run_report.json for full machine details.",
        "Bundle contains staged pages (post copy) + per-shelf author_set + gate reports.",
        "No push performed. Owner action required for deploy.",
    ]
    (out_dir / "spine_run_report.md").write_text("\n".join(md_lines), encoding="utf-8")

    # Consolidated author_set
    cons_path = out_dir / "consolidated_author_set.json"
    cons_data = {
        "spine_run_dir": str(out_dir),
        "flag_overrides": overrides,
        "note": args.note,
        "generated_at": spine_report["generated_at"],
        "total_author_needed": total_author,
        "by_shelf": consolidated["by_shelf"],
        "authored_needed": consolidated["authored_needed"],
    }
    write_json(cons_path, cons_data)

    # Deploy-ready bundle: copy key artifacts per shelf
    for srec in per_shelf:
        shelf = srec["shelf"]
        bdir = out_dir / shelf
        bdir.mkdir(parents=True, exist_ok=True)
        src_page = STAGING_ROOT / shelf / f"{shelf}_rescored.json"
        if src_page.is_file():
            dst = bdir / f"{shelf}_rescored.json"
            shutil.copy2(src_page, dst)
            srec["staged_page_in_bundle"] = str(dst.relative_to(out_dir))
        src_auth = STAGING_ROOT / shelf / "author_set.json"
        if src_auth.is_file():
            shutil.copy2(src_auth, bdir / "author_set.json")
        src_gr = STAGING_ROOT / shelf / f"{shelf}_rescored_gates_report.md"
        if src_gr.is_file():
            shutil.copy2(src_gr, bdir / f"{shelf}_rescored_gates_report.md")

    # Copy the spine reports into root of bundle (already written there)

    elapsed = time.perf_counter() - t_start

    # Final DEPLOY-READY line (exact per spec)
    n_shelves = len(affected_shelves)
    print("\n" + "=" * 70)
    print(
        f"DEPLOY-READY: {n_shelves} shelves, {total_author} products need copy authoring, "
        f"gates {gates_summary}, frozen breach none. No push performed."
    )
    print(f"Bundle: {out_dir}")
    print(f"Report: {out_dir / 'spine_run_report.json'} + .md")
    print(f"Consolidated author: {cons_path}")
    print(f"Total wall time: {elapsed:.1f}s")
    print("=" * 70)

    # Persist final commands for return block visibility
    spine_report["commands_run"] = all_commands
    write_json(out_dir / "spine_run_report.json", spine_report)

    # Non-zero if any shelf had error or gate fail (but still produced bundle)
    any_error = any(bool(s.get("error")) for s in per_shelf)
    any_gate_fail = bool(gate_fails)
    return 1 if (any_error or any_gate_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
