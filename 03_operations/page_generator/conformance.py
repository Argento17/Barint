#!/usr/bin/env python3
"""
conformance.py — Spine-conformance gate / auditor (TASK new-category onboarding).

Answers ONE question per live category: "When the owner flips a scoring switch
(`spine_flip.py --set BARI_X=on`), will this category actually re-flow and serve the
new scores — or will it silently keep OLD scores while the rest of the shelf moves?"

The owner's feared failure (verbatim): ship a new category, be happy, then discover
DAYS LATER it doesn't conform to the spine. This tool makes that detectable in one
command — and `onboard_category.py` calls it as a hard final gate so a new category
can never go live non-conforming in the first place.

WHY THESE CHECKS (verified against source, reviewed by C3 / P215):
  `spine_flip.py:391` loops ONLY `affected_shelves` and rescores each via
  `rescore_all.py --shelf <stem>`, then propagates via
  `copy_stage.py --live <config.baseline_json>`. `affected_shelves` comes from
  `affected_set.build_corpus_to_shelves_map()`, which maps a corpus to a shelf ONLY
  if the corpus is registered in shadow_registry_v1.json AND resolves to a config.

  UPDATE 2026-06-18 (spine re-flow fix, parallel-chat finding): spine_flip.py now
  rescores EVERY live config unconditionally — it NO LONGER gates the rescore on the
  shadow diff / registry mapping (that gate keyed off a stored baseline which drifted
  from the live shelves and silently skipped live categories). So re-flow is guaranteed
  by HARD-1 + HARD-3 alone; registry reachability is demoted to SOFT-2 (advisory, governs
  only the shadow-diff PREVIEW). Two things must be true for a real flip to re-flow + serve:

  HARD-1  config exists and its corpus dirs resolve (the shelf can be scored at all).
  HARD-3  config.baseline_json is set AND equals the frontend JSON the live route
          serves (per live_manifest.json). Fail = the flip may rescore correctly but
          `copy_stage` writes nowhere / to a stale file -> the page still serves old
          data. (C3 P215: "rescored but frontend kept serving old JSON" is the worst,
          days-later drift — false confidence is the bigger danger than false alarms.)
  SOFT-2  ADVISORY: whether a registered corpus maps to this shelf (shadow-diff PREVIEW
          visibility only). No longer a re-flow blocker — the flip rescores every live
          config regardless.

  SOFT (deploy/live hygiene, reported but do NOT block — C3 classified these as
  non-re-flow):
    SOFT-4  listed in live_manifest.json (tracked as live).
    SOFT-5  frontend JSON is the standard {_meta, products} shape (juices uses a
            bespoke FLAT schema -> needs a manual loader override; flagged, not failed).
    SOFT-6  registry class diagnostic (frozen/candidate/published). Class is NOT
            load-bearing for re-flow: affected_set does not filter by class; frozen
            corpora ARE included and trip the exit-2 frozen gate. Reported for context.

  INTEGRITY:
    HARD-7  OFF (Open Food Facts) string count == 0 in the served frontend JSON.
            Project-wide hard ban; any OFF dependency is a launch blocker.

Usage:
  python 03_operations/page_generator/conformance.py --all
  python 03_operations/page_generator/conformance.py --slug cakes
  python 03_operations/page_generator/conformance.py --slug breakfast-cereals --json

Exit code: 0 = every checked category conforms (no HARD failure).
           1 = at least one HARD check failed somewhere.
           3 = usage / load error.

ASCII-only output (Windows cp1252 stdout safe).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent          # .../page_generator
REPO = THIS_DIR.parents[1]                           # C:\Bari
CONFIGS_DIR = THIS_DIR / "configs"
SHADOW_REGISTRY = REPO / "03_operations" / "shadow" / "shadow_registry_v1.json"
LIVE_MANIFEST = REPO / "03_operations" / "spine" / "live_manifest.json"
WEB_DATA_DIR = REPO / "bari-web" / "src" / "data" / "comparisons"

OFF_MARKERS = ("openfoodfacts", "open_food_facts", "off.net", "world.off",
               "off_api", "open_food_facts_fallback")


def norm(s: str | None) -> str:
    """Normalize a category identifier: lower, unify - and _."""
    return (s or "").strip().lower().replace("-", "_")


def norm_path(p: str | None) -> str:
    if not p:
        return ""
    return str(Path(p)).lower().replace("\\", "/").rstrip("/")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Load the three sources of truth
# ---------------------------------------------------------------------------

def load_configs() -> dict[str, dict]:
    """Return {stem: config_dict} for non-_generated configs."""
    out: dict[str, dict] = {}
    for p in sorted(CONFIGS_DIR.glob("*.json")):
        if p.name.startswith("_generated_"):
            continue
        try:
            out[p.stem] = load_json(p)
        except Exception as exc:  # noqa: BLE001
            out[p.stem] = {"_load_error": str(exc)}
    return out


def load_manifest_entries() -> list[dict]:
    if not LIVE_MANIFEST.is_file():
        return []
    return load_json(LIVE_MANIFEST).get("files", [])


def load_registry() -> dict:
    if not SHADOW_REGISTRY.is_file():
        return {"corpora": [], "deferred": []}
    return load_json(SHADOW_REGISTRY)


def real_stem_to_corpora() -> dict[str, list[str]]:
    """Invert affected_set.build_corpus_to_shelves_map() -> {stem: [corpus,...]}.

    Imports and calls the REAL function the flip path uses. This is HARD-2's
    load-bearing oracle: a stem present here is reachable by a score-flip.
    """
    if str(THIS_DIR) not in sys.path:
        sys.path.insert(0, str(THIS_DIR))
    from affected_set import build_corpus_to_shelves_map  # noqa: WPS433

    corpus_to_shelves = build_corpus_to_shelves_map()
    inv: dict[str, list[str]] = {}
    for corpus, stems in corpus_to_shelves.items():
        for stem in stems:
            inv.setdefault(stem, [])
            if corpus not in inv[stem]:
                inv[stem].append(corpus)
    return inv


# ---------------------------------------------------------------------------
# Per-category resolution
# ---------------------------------------------------------------------------

def manifest_for_category(cat_norm: str, entries: list[dict]) -> list[dict]:
    return [e for e in entries if norm(e.get("category")) == cat_norm]


def manifest_for_path(baseline_json: str | None, entries: list[dict]) -> dict | None:
    if not baseline_json:
        return None
    target = norm_path(baseline_json)
    for e in entries:
        if norm_path(e.get("path")) == target:
            return e
    return None


def registry_class(cat_norm: str, registry: dict) -> tuple[str | None, bool]:
    """Return (class, is_deferred). Best-effort name match on the corpus list.

    Deferred matching tolerates a prefix relationship (e.g. category 'bread'
    matches deferred entry 'bread_retail_003') so a documented, accepted Shadow-v1
    limitation reads as DEFERRED rather than a fixable failure (avoids false-alarm
    fatigue — C3 P215). Corpus matches stay exact.
    """
    for c in registry.get("corpora", []):
        if norm(c.get("name")) == cat_norm:
            return c.get("class"), False
    for d in registry.get("deferred", []):
        dn = norm(d.get("name"))
        if dn == cat_norm or dn.startswith(cat_norm) or cat_norm.startswith(dn):
            return "deferred", True
    return None, False


def corpus_dirs_resolve(cfg: dict) -> tuple[bool, list[str]]:
    """Check corpus_dirs / run_products_dir point at existing directories."""
    missing: list[str] = []
    found_any = False
    for key in ("corpus_dirs", "run_products_dir"):
        val = cfg.get(key)
        items = val if isinstance(val, list) else ([val] if val else [])
        for item in items:
            if not item:
                continue
            p = Path(item)
            if p.is_dir():
                found_any = True
            else:
                missing.append(str(item))
    return (found_any and not missing), missing


def detect_shape(frontend_path: Path) -> str:
    """standard ({_meta, products}) | flat | missing | unreadable."""
    if not frontend_path.is_file():
        return "missing"
    try:
        data = load_json(frontend_path)
    except Exception:  # noqa: BLE001
        return "unreadable"
    if isinstance(data, dict) and "products" in data and "_meta" in data:
        return "standard"
    return "flat"


def off_count(frontend_path: Path) -> int:
    """Count OFF markers in the SERVED product data only.

    Deliberately scans the `products` array, NOT the whole file: an OFF marker
    inside a `_meta`/exclusions `reason` string is AUDIT TEXT documenting that a
    product was REMOVED because it was OFF-sourced (a good thing), not OFF data on
    the page. Scanning the whole file flags those as contamination -> false alarm
    (C3 P215: false alarms train the owner to ignore the gate). Real contamination
    lives in a served product record, which this still catches.
    """
    if not frontend_path.is_file():
        return 0
    try:
        data = load_json(frontend_path)
    except Exception:  # noqa: BLE001
        blob = frontend_path.read_text(encoding="utf-8", errors="replace").lower()
        return sum(blob.count(m) for m in OFF_MARKERS)
    if isinstance(data, dict) and "products" in data:
        payload = data["products"]
    else:
        payload = data  # flat schema: the whole doc is the served data
    blob = json.dumps(payload, ensure_ascii=False).lower()
    return sum(blob.count(m) for m in OFF_MARKERS)


ALLOWED_OFF_CONTEXT_KEYS = frozenset({"reason", "note", "_comment", "exclusions"})


def _off_disallowed_outside_products(data: Any) -> list[str]:
    """Find OFF markers outside products[] and outside allowed audit-key contexts."""
    hits: list[str] = []

    def walk(obj: Any, key_path: list[str]) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "products":
                    continue
                walk(v, key_path + [str(k)])
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, key_path + [f"[{i}]"])
        elif isinstance(obj, str):
            lower = obj.lower()
            if any(m in lower for m in OFF_MARKERS):
                if not any(k in ALLOWED_OFF_CONTEXT_KEYS for k in key_path):
                    hits.append(".".join(key_path) or "(root)")

    if isinstance(data, dict):
        walk(data, [])
    return hits


def config_corpus_source_paths(cfg: dict) -> set[str]:
    """Normalized corpus/scoring source dirs declared by the shelf config."""
    paths: set[str] = set()
    for key in ("corpus_dirs", "run_products_dir"):
        val = cfg.get(key)
        items = val if isinstance(val, list) else ([val] if val else [])
        for item in items:
            if item:
                paths.add(norm_path(item))
    scoring = cfg.get("scoring") or {}
    bsip1 = scoring.get("bsip1_dir")
    if isinstance(bsip1, str) and bsip1:
        paths.add(norm_path(bsip1))
    return paths


def count_corpus_products(cfg: dict) -> int | None:
    scoring = cfg.get('scoring') or {}
    glob_pat = scoring.get('bsip1_glob', 'bsip1_*.json')
    dirs = []
    for key in ('corpus_dirs', 'run_products_dir'):
        val = cfg.get(key)
        items = val if isinstance(val, list) else ([val] if val else [])
        dirs.extend(str(item) for item in items if item)
    bsip1 = scoring.get('bsip1_dir')
    if isinstance(bsip1, str) and bsip1:
        dirs.append(bsip1)
    if not dirs:
        return None
    count = 0
    for d in dirs:
        pdir = Path(d)
        if not pdir.is_dir():
            continue
        count += len([f for f in pdir.glob(glob_pat) if 'audit' not in f.name])
    return count if count > 0 else None


def unmapped_registered_corpora(registry: dict,
                                stem_corpora: dict[str, list[str]]) -> list[dict]:
    """Registered scored corpora that map to NO config stem (no live page).

    These are correctly NOT conformance-checked (there is no page to go stale), but
    leaving them implicit means "is this category covered?" has no visible answer.
    This surfaces them explicitly so the silent gap can't recur (red-team MEDIUM
    2026-06-18). Returns [{name, class, note_head}] for each unmapped corpus.
    """
    mapped: set[str] = set()
    for corpora in stem_corpora.values():
        mapped.update(corpora)
    out: list[dict] = []
    for c in registry.get("corpora", []):
        name = c.get("name", "")
        if name and name not in mapped:
            note = (c.get("note") or "").strip()
            head = note.split(".")[0][:90] if note else ""
            out.append({"name": name, "class": c.get("class"), "note_head": head})
    return out


def registry_source_map(registry: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for c in registry.get('corpora', []):
        src = c.get('source')
        name = c.get('name', '')
        if isinstance(src, list):
            out[name] = [norm_path(s) for s in src if s]
        elif src:
            out[name] = [norm_path(src)]
        else:
            out[name] = []
    return out


# ---------------------------------------------------------------------------
# Evaluate one config stem
# ---------------------------------------------------------------------------

def evaluate(stem: str, cfg: dict, *, entries: list[dict], registry: dict,
             stem_corpora: dict[str, list[str]],
             all_config_sources: set[str] | None = None) -> dict:
    checks: list[dict] = []

    def add(check_id: str, hard: bool, ok: bool, detail: str) -> None:
        checks.append({"id": check_id, "hard": hard, "ok": ok, "detail": detail})

    if "_load_error" in cfg:
        add("HARD-1-config", True, False, f"config unreadable: {cfg['_load_error']}")
        return _finalize(stem, None, checks)

    cat = cfg.get("category")
    cat_norm = norm(cat)
    cls, deferred = registry_class(cat_norm, registry)

    # HARD-1: config + corpus dirs resolve
    dirs_ok, missing = corpus_dirs_resolve(cfg)
    add("HARD-1-corpus_dirs", True, dirs_ok,
        "all corpus dirs exist" if dirs_ok
        else f"missing/empty corpus dirs: {missing or '(none declared)'}")

    # SOFT-2: shadow-diff PREVIEW visibility (ADVISORY since the 2026-06-18 spine re-flow
    # fix). spine_flip.py now rescores EVERY live config unconditionally — it no longer
    # gates the rescore on the shadow diff / registry mapping. So a live config re-flows
    # because it IS a live config (guaranteed by HARD-1 corpus + HARD-3 baseline_served),
    # NOT because a registered corpus maps to it. Registry mapping now only governs whether
    # the (advisory) shadow-diff PREVIEW shows this shelf. We report it for that diagnostic
    # value but it is NOT a re-flow blocker. (Was HARD-2; demoted after the parallel-chat
    # finding that the shadow baseline drifts from the live shelves.)
    corpora = stem_corpora.get(stem, [])
    add("SOFT-2-shadow_preview", False, True,
        f"shadow-diff preview will show this shelf (registered corpus/corpora: {corpora})"
        if corpora
        else "re-flows via unconditional live-config rescore; shadow-diff preview is BLIND "
             "to it (no registered corpus maps -> not a blocker, just advisory drift)")

    # HARD-3: baseline_json set + equals served frontend JSON
    baseline = cfg.get("baseline_json")
    served = manifest_for_path(baseline, entries)
    if not baseline:
        add("HARD-3-baseline_served", True, False,
            "config.baseline_json is null -> copy_stage has no live file to write; "
            "flip cannot propagate scores to the served page")
    elif not Path(baseline).is_file():
        add("HARD-3-baseline_served", True, False,
            f"baseline_json does not exist on disk: {baseline}")
    elif served is None:
        # baseline exists but is not the file live_manifest says is served
        cat_entries = [norm_path(e.get("path")) for e in manifest_for_category(cat_norm, entries)]
        add("HARD-3-baseline_served", True, False,
            f"baseline_json ({Path(baseline).name}) is NOT the file live_manifest serves "
            f"for category '{cat}' (manifest serves: {[Path(p).name for p in cat_entries] or 'NOTHING'})")
    else:
        add("HARD-3-baseline_served", True, True,
            f"baseline_json == served file ({served.get('data_file')}, "
            f"{served.get('product_count')} products)")

    # SOFT-4: in live_manifest at all
    in_manifest = bool(served or manifest_for_category(cat_norm, entries))
    add("SOFT-4-in_manifest", False, in_manifest,
        "tracked in live_manifest" if in_manifest else "not in live_manifest")

    # SOFT-5: frontend JSON shape
    # Resolve the served file for shape/OFF even when baseline_json is null:
    # fall back to the served entry, then to a category-matched manifest entry.
    frontend_path = Path(baseline) if baseline else None
    if frontend_path is None and served:
        frontend_path = Path(served.get("path", ""))
    if frontend_path is None:
        cat_entries = manifest_for_category(cat_norm, entries)
        if cat_entries:
            frontend_path = Path(cat_entries[0].get("path", ""))
    shape = detect_shape(frontend_path) if frontend_path else "missing"
    add("SOFT-5-shape", False, shape == "standard",
        f"frontend JSON shape = {shape}"
        + (" (FLAT: needs manual loader override, e.g. juices)" if shape == "flat" else ""))

    # SOFT-6: registry class diagnostic (cls/deferred computed at top)
    add("SOFT-6-registry_class", False, True,
        f"registry class = {cls or 'NOT REGISTERED'}"
        + (" (deferred: bespoke/out-of-scope)" if deferred else ""))

    # HARD-7: OFF ban
    n_off = off_count(frontend_path) if frontend_path else 0
    add("HARD-7-off_zero", True, n_off == 0,
        "OFF markers = 0" if n_off == 0 else f"OFF markers found: {n_off} (LAUNCH BLOCKER)")

    # SOFT-8 (RT-4): OFF markers outside products[] in disallowed context
    off_outside_ok = True
    off_outside_detail = "no OFF markers outside products[]"
    if frontend_path and frontend_path.is_file() and n_off == 0:
        try:
            data = load_json(frontend_path)
            disallowed = _off_disallowed_outside_products(data)
            if disallowed:
                off_outside_ok = False
                off_outside_detail = (
                    f"OFF marker(s) outside products[] in disallowed context: "
                    f"{', '.join(disallowed[:3])}"
                    + (" ..." if len(disallowed) > 3 else "")
                )
        except Exception as exc:  # noqa: BLE001
            off_outside_detail = f"OFF outside-products scan skipped: {exc}"
    add("SOFT-8-off_misplaced", False, off_outside_ok, off_outside_detail)

    # SOFT-9 (RT-8): registry shadow source not referenced by config corpus dirs
    reg_sources = registry_source_map(registry)
    cfg_sources = config_corpus_source_paths(cfg)
    # A registry source counts as "drifted" only if NO config anywhere references it
    # (a true orphan). Checking against THIS stem's config alone false-alarms on corpora
    # that legitimately SHARE a dir with another category — e.g. the cookies_coffee corpus
    # shares run_cakes_001 with the cakes stem, so when --all evaluates the cakes stem,
    # cookies' OTHER source (run_cookies_001) is not in cakes' config but IS valid. Use the
    # repo-wide union of all config sources to avoid that (this is why --slug and --all
    # disagreed before the fix).
    known_sources = all_config_sources if all_config_sources is not None else cfg_sources
    shadow_hits: list[str] = []
    for corpus_name in corpora:
        for src in reg_sources.get(corpus_name, []):
            if src and src not in known_sources:
                shadow_hits.append(f"{corpus_name}:{src}")
    add(
        "SOFT-9-registry_source",
        False,
        not shadow_hits,
        "all registry sources referenced by config corpus_dirs"
        if not shadow_hits
        else "; ".join(
            f"shadow source {hit} not referenced by config corpus_dirs — "
            f"shadow may validate a stale/partial corpus."
            for hit in shadow_hits
        ),
    )

    # SOFT-10 (RT-9): MALFORMED shelf_rel calibration (declared but incomplete).
    # NOTE: we do NOT warn on "flag on + shelf_rel null". BARI_SHELF_RELATIVE_V1 is a
    # GLOBAL DEFAULT flag; actual shelf-relative enrollment is by category scope
    # (constants.py SUGAR/FATSAT_SHELF_REL_SCOPE), not the flag — so a null shelf_rel
    # is correct for non-enrolled categories (e.g. milk). Flagging flag-on-without-block
    # false-alarms on every such category. We only flag a shelf_rel that IS declared
    # but is missing median/scale (a real, reliably-detectable misconfiguration).
    scoring = cfg.get("scoring") or {}
    shelf_rel = scoring.get("shelf_rel")
    shelf_rel_ok = True
    shelf_rel_detail = "shelf_rel calibration present or category not shelf-relative"
    if isinstance(shelf_rel, dict):
        missing = [k for k in ("median", "scale") if shelf_rel.get(k) is None]
        if missing:
            shelf_rel_ok = False
            shelf_rel_detail = (
                f"shelf_rel declared but missing {missing} — incomplete calibration; "
                "shelf-relative scores will be wrong."
            )
    add("SOFT-10-shelf_rel", False, shelf_rel_ok, shelf_rel_detail)

    # SOFT-11 (RT-11): live_manifest product_count vs served JSON products length
    manifest_count_ok = True
    manifest_count_detail = "product_count not comparable (no served manifest entry)"
    if frontend_path and frontend_path.is_file() and served is not None:
        try:
            data = load_json(frontend_path)
            file_count = len(data.get("products", [])) if isinstance(data, dict) else 0
            manifest_count = served.get("product_count")
            if manifest_count is not None and file_count != manifest_count:
                manifest_count_ok = False
                manifest_count_detail = (
                    f"live_manifest product_count={manifest_count} != "
                    f"served file products={file_count} (manifest stale?)"
                )
            else:
                manifest_count_detail = f"product_count matches ({file_count})"
        except Exception as exc:  # noqa: BLE001
            manifest_count_detail = f"manifest product_count check skipped: {exc}"
    add('SOFT-11-manifest_count', False, manifest_count_ok, manifest_count_detail)

    cal_ok = True
    cal_detail = 'calibration_n not set — drift check skipped'
    if isinstance(shelf_rel, dict):
        cal_n = shelf_rel.get('calibration_n')
        if cal_n is not None:
            current_n = count_corpus_products(cfg)
            if current_n is None:
                cal_detail = f'calibration_n={cal_n} but corpus dirs unreadable'
            elif cal_n <= 0:
                cal_detail = f'calibration_n={cal_n} invalid — drift check skipped'
            else:
                drift = abs(current_n - cal_n) / cal_n
                cal_ok = drift <= 0.25
                cal_detail = f'calibration_n={cal_n}, current_corpus={current_n}, drift={drift:.1%}' + (' — within 25% threshold' if cal_ok else ' — exceeds 25% threshold')
    add('SOFT-12-calibration_drift', False, cal_ok, cal_detail)

    return _finalize(stem, cat, checks, deferred=deferred)


def _finalize(stem: str, cat: str | None, checks: list[dict], *, deferred: bool = False) -> dict:
    hard_fail = [c for c in checks if c["hard"] and not c["ok"]]
    soft_fail = [c for c in checks if not c["hard"] and not c["ok"]]
    return {
        "stem": stem,
        "category": cat,
        "conforms": not hard_fail,
        "deferred": deferred,
        "hard_failures": [c["id"] for c in hard_fail],
        "soft_warnings": [c["id"] for c in soft_fail],
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def resolve_stem(slug: str, configs: dict[str, dict]) -> str | None:
    """Resolve a user-supplied slug/category/stem to a config stem."""
    if slug in configs:
        return slug
    target = norm(slug)
    for stem, cfg in configs.items():
        if norm(stem) == target or norm(cfg.get("category")) == target:
            return stem
    return None


def print_report(results: list[dict], registry_unmapped: list[dict] | None = None) -> None:
    for r in results:
        if not r["conforms"]:
            status = "NON-CONFORMING"
        elif r.get("deferred"):
            status = "DEFERRED"
        else:
            status = "CONFORMS"
        print(f"\n[{status}] {r['stem']}  (category: {r['category']})")
        for c in r["checks"]:
            mark = "PASS" if c["ok"] else ("FAIL" if c["hard"] else "warn")
            tier = "HARD" if c["hard"] else "soft"
            print(f"    {mark:4s} {tier} {c['id']:24s} {c['detail']}")

    bad = [r for r in results if not r["conforms"]]
    deferred = [r for r in results if r["conforms"] and r.get("deferred")]
    ok = [r for r in results if r["conforms"] and not r.get("deferred")]
    print("\n" + "=" * 72)
    print(f"SUMMARY: {len(ok)} conform, {len(deferred)} deferred (accepted), "
          f"{len(bad)} non-conforming  (of {len(results)}).")
    if deferred:
        print("\nDEFERRED (documented Shadow-v1 limitation; won't re-flow until a Shadow-v2 "
              "custom loader exists — accepted, not a bug):")
        for r in deferred:
            print(f"  - {r['stem']}")
    if bad:
        print("\nNON-CONFORMING (a score-flip would leave these stale / mis-served):")
        for r in bad:
            print(f"  - {r['stem']:20s} HARD failures: {', '.join(r['hard_failures'])}")
        print("\nA targeted spine_flip would re-flow every OTHER shelf and leave the above "
              "at OLD scores. Fix before the next score switch.")
    else:
        print("\nAll non-deferred categories will re-flow correctly on a score-flip.")

    if registry_unmapped:
        print("\n" + "-" * 72)
        print("REGISTERED CORPORA WITH NO LIVE PAGE (not conformance-checked, by design):")
        print("  These are scored in the shadow backtest but map to NO config/route, so")
        print("  there is no live page to go stale. Listed for visibility — if one SHOULD")
        print("  be live it needs a config + route; if it is a retired/expansion corpus the")
        print("  note says so.")
        for u in registry_unmapped:
            head = f" — {u['note_head']}" if u.get("note_head") else ""
            print(f"  - {u['name']:24s} [class={u.get('class')}]{head}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Spine-conformance gate / auditor.")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="check every configured shelf")
    g.add_argument("--slug", help="check one category (route slug, category name, or config stem)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of human report")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

    configs = load_configs()
    if not configs:
        print("ERROR: no configs found in " + str(CONFIGS_DIR), file=sys.stderr)
        return 3
    entries = load_manifest_entries()
    registry = load_registry()
    stem_corpora = real_stem_to_corpora()

    if args.all:
        stems = sorted(configs)
    else:
        stem = resolve_stem(args.slug, configs)
        if stem is None:
            print(f"ERROR: no config matches slug '{args.slug}'. Known stems: "
                  f"{', '.join(sorted(configs))}", file=sys.stderr)
            return 3
        stems = [stem]

    # Repo-wide union of every config's declared source paths (for SOFT-9 orphan check).
    all_config_sources: set[str] = set()
    for c in configs.values():
        all_config_sources |= config_corpus_source_paths(c)

    results = [
        evaluate(stem, configs[stem], entries=entries, registry=registry,
                 stem_corpora=stem_corpora, all_config_sources=all_config_sources)
        for stem in stems
    ]

    # In --all mode, surface registered corpora that map to no config (no live page).
    registry_unmapped = unmapped_registered_corpora(registry, stem_corpora) if args.all else None

    if args.json:
        out = {"results": results}
        if registry_unmapped is not None:
            out["registry_unmapped"] = registry_unmapped
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_report(results, registry_unmapped)

    return 0 if all(r["conforms"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
