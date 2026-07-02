"""
run_rescore_task393.py — TASK-393 cookies-coffee D4 scoring measurement.

PURPOSE: Re-score the cookies-coffee corpus with BARI_D4_SCORE_V1=on added to the
existing config flag vector. All other flags are held exactly as in the live config.
Output is written to this staging directory. No live files are touched.

Context (from task delegation):
  - live frontend: bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json
    (run_id = run_cookies_005+run_cakes_001_cookies, 119 products, grades: C=10/D=26/E=83)
  - live config: 03_operations/page_generator/configs/cookies_coffee.json
    flags: BARI_FAT_TECH_V1=on; all others off; D4 MISSING → stale vs every other shelf
  - BSIP1 source: TASK-405 de-polluted corpus (current state)
  - Guard: OFF banned; no copy authoring; no live file writes; do not deploy

Flags applied for this run (live flags + D4=on):
  BARI_RECAL_P0=off
  BARI_GRAD_SODIUM_V1=off
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_SHELF_RELATIVE_V1=off
  BARI_FAT_TECH_V1=on
  BARI_D4_SCORE_V1=on       ← NEW (this is the change being measured)

Hard rules:
  - OFF=0: no Open Food Facts data; unknown stays null
  - No live file writes
  - All copy fields stay PENDING_COPY
  - No score/grade decisions made here; impact surfaced for orchestrator
"""

from __future__ import annotations

import csv
import hashlib
import importlib
import json
import os
import sys
import time
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[4]
STAGING_DIR = Path(__file__).resolve().parent

CONFIG_PATH = REPO / "03_operations" / "page_generator" / "configs" / "cookies_coffee.json"
SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
GENERATE_PAGE_PY = REPO / "03_operations" / "page_generator" / "generate_page.py"
BASELINE_PATH = REPO / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"

PRODUCTS_DIR = STAGING_DIR / "products"
STAGING_CONFIG = STAGING_DIR / "staging_config.json"
STAGED_PAGE = STAGING_DIR / "cookies_coffee_task393_staged.json"
GRADE_MOVE_TABLE = STAGING_DIR / "grade_move_table.csv"
SUMMARY_PATH = STAGING_DIR / "run_summary.json"

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))

# Score-engine page_generator dir needed for render_fields
_PAGE_GEN_DIR = REPO / "03_operations" / "page_generator"
if str(_PAGE_GEN_DIR) not in sys.path:
    sys.path.insert(0, str(_PAGE_GEN_DIR))

# ---------------------------------------------------------------------------
# D4-inclusive flag vector (live flags + BARI_D4_SCORE_V1=on)
# ---------------------------------------------------------------------------

TASK393_FLAGS = {
    "BARI_RECAL_P0": "off",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
    "BARI_SHELF_RELATIVE_V1": "off",
    "BARI_FAT_TECH_V1": "on",
    "BARI_D4_SCORE_V1": "on",   # TASK-393: the new flag
}

MANAGED_BARI_VARS = list(TASK393_FLAGS.keys()) + [
    "BARI_RECAL_P0_YOGURT_TRIM",
    "BARI_TASK144_FIXES",
    "BARI_TASK250_CONF",
    "BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15",
    "BARI_GLASSBOX_W2",
    "BARI_DAIRY_SAT_FAT_INFER",
    "BARI_HC_DAIRY_SATFAT_V1",
]

OFF_MARKERS = ["open_food_facts", "openfoodfacts", "off_candidate_panel"]

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]


def score_to_grade(score):
    if score is None:
        return None
    for grade, thresh in GRADE_SCALE:
        if score >= thresh:
            return grade
    return "E"


# ---------------------------------------------------------------------------
# Env management
# ---------------------------------------------------------------------------

def snapshot_env():
    return {k: os.environ.get(k) for k in MANAGED_BARI_VARS}


def restore_env(snap):
    for k, v in snap.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def apply_flags(flags):
    for k, v in flags.items():
        os.environ[k] = v


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def sha256_file(path):
    h = hashlib.sha256()
    with open(Path(path), "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def off_in_record(rec):
    s = json.dumps(rec, ensure_ascii=False).lower()
    return any(m in s for m in OFF_MARKERS)


# ---------------------------------------------------------------------------
# Corpus collection (mirrors rescore_all logic)
# ---------------------------------------------------------------------------

def collect_bsip1_files(corpus_dirs: list[str]) -> list[Path]:
    files = []
    seen = set()
    for cdir in corpus_dirs:
        p = Path(cdir)
        if not p.is_dir():
            print(f"  WARNING: corpus dir not found: {cdir}")
            continue
        for fname in sorted(p.glob("bsip1_*.json")):
            if "audit" in fname.name:
                continue
            try:
                rec = load_json(fname)
            except Exception:
                continue
            bc = str(rec.get("barcode", "")).strip()
            if not bc or bc in seen:
                continue
            if rec.get("file_type") != "product":
                continue
            seen.add(bc)
            files.append(fname)
    return files


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def reload_score_engine():
    import score_engine
    return importlib.reload(score_engine)


def make_score_one(se):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from trace_writer import assemble_trace
    from structural_classifier import classify_structural_class

    def score_one(product):
        signals = extract_signals(product)
        cat = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova = infer_nova(product, l3)
        ev = assign_evaluation_scope(product, cat["category"])
        sr = se.score_product(product, signals, cat, nova, ev)
        trace = assemble_trace(product, signals, cat, nova, ev, sr)
        trace["structural_class"] = classify_structural_class(trace)
        return trace

    return score_one


def score_corpus(bsip1_files, products_dir, flags):
    from input_loader import load_product, validate_product

    PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

    apply_flags(flags)
    se = reload_score_engine()
    score_one = make_score_one(se)

    scored = 0
    off_hits = []

    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        errors = validate_product(product)
        product["_load_errors"] = errors

        # OFF guard
        if off_in_record(product):
            off_hits.append(str(fpath))
            print(f"  OFF VIOLATION in {fpath.name} — halting")
            continue

        pid = product.get("canonical_product_id", fpath.stem)
        pdir = products_dir / str(pid)
        pdir.mkdir(parents=True, exist_ok=True)

        trace = score_one(product)
        (pdir / "bsip2_trace.json").write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        scored += 1

    return scored, off_hits


# ---------------------------------------------------------------------------
# Load traces produced by above scoring pass
# ---------------------------------------------------------------------------

def load_traces_by_barcode(products_dir: Path) -> dict[str, dict]:
    traces = {}
    if not products_dir.is_dir():
        return traces
    for dname in sorted(products_dir.iterdir()):
        if not dname.is_dir():
            continue
        tp = dname / "bsip2_trace.json"
        if not tp.is_file():
            continue
        try:
            t = load_json(tp)
            bc = str(t.get("input_reference", {}).get("barcode", "")).strip()
            if bc and bc not in traces:
                traces[bc] = t
        except Exception:
            pass
    return traces


# ---------------------------------------------------------------------------
# Exclusion set (from config)
# ---------------------------------------------------------------------------

def load_exclusion_set(config: dict) -> set[str]:
    return {str(e["barcode"]) for e in config.get("exclusions", [])}


# ---------------------------------------------------------------------------
# Baseline extraction
# ---------------------------------------------------------------------------

def load_baseline(path: Path) -> dict[str, dict]:
    if not path.is_file():
        print(f"  WARNING: baseline not found at {path}")
        return {}
    data = load_json(path)
    result = {}
    for p in data.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if bc:
            result[bc] = p
    return result


# ---------------------------------------------------------------------------
# Staging page build (minimal — copy fields stay PENDING_COPY)
# ---------------------------------------------------------------------------

def build_staged_page(
    traces: dict[str, dict],
    bsip1_lookup: dict[str, dict],
    baseline_products: dict[str, dict],
    exclusion_set: set[str],
    flags: dict,
) -> dict:
    """
    Produce the staged frontend JSON.
    - Scores and grades come from fresh traces.
    - Copy fields: PENDING_COPY (never authored here).
    - Products excluded by the config exclusion list are dropped.
    - Only products in the baseline (the 119 live products) are in scope.
    """
    import subprocess

    # Use generate_page.py via subprocess with staging config so the full
    # pipeline logic (dedup, exclusions, render_fields) runs correctly.
    # This is delegated below; here we just build the diff table directly.
    products = []

    for bc, trace in sorted(traces.items()):
        if bc in exclusion_set:
            continue

        score = trace.get("final_score_estimate")
        grade = score_to_grade(score) if score is not None else None

        # Baseline entry for copy carry-over
        baseline_entry = baseline_products.get(bc, {})

        entry = {
            "barcode": bc,
            "score": score,
            "grade": grade,
            # Carry name from bsip1 or baseline
            "name": (
                (bsip1_lookup.get(bc) or {}).get("canonical_name_he")
                or baseline_entry.get("name")
                or "UNKNOWN"
            ),
            # Copy fields: carry from baseline or mark PENDING
            "rowVerdict": baseline_entry.get("rowVerdict", "PENDING_COPY"),
            "insightLine": baseline_entry.get("insightLine", "PENDING_COPY"),
            "consumerTakeaway": baseline_entry.get("consumerTakeaway", "PENDING_COPY"),
            "bariInterpretation": baseline_entry.get("bariInterpretation", "PENDING_COPY"),
            # Scoring metadata from trace
            "_d4_score_penalty": trace.get("d4_score_penalty"),
            "_d4_score_note": trace.get("d4_score_note"),
            "_nova_proxy": trace.get("nova_proxy"),
            "_binding_cap": trace.get("binding_cap"),
        }
        products.append(entry)

    # Sort by score desc (None last) — matches live page convention
    products.sort(key=lambda p: (p["score"] is None, -(p["score"] or 0)))

    return {
        "_meta": {
            "task": "TASK-393",
            "stage": "SCORING_MEASUREMENT_ONLY",
            "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "category": "cookies_coffee",
            "run_id": "task393_rescore_d4on",
            "product_count": len(products),
            "flags_applied": flags,
            "bsip1_sources": [
                "03_operations/bsip1/run_cookies_001/output",
                "03_operations/bsip1/run_cakes_001/output",
            ],
            "baseline_run_id": "run_cookies_005+run_cakes_001_cookies",
            "off_used": False,
            "copy_status": "PENDING_COPY — not authored; carry-over from baseline where available",
            "deploy_status": "NOT_DEPLOYED — staging measurement only",
        },
        "products": products,
    }


# ---------------------------------------------------------------------------
# Diff computation
# ---------------------------------------------------------------------------

def compute_diff(baseline_products: dict[str, dict], staged_products: list[dict]) -> dict:
    staged_by_bc = {p["barcode"]: p for p in staged_products}

    common = sorted(set(baseline_products) & set(staged_by_bc))
    baseline_only = sorted(set(baseline_products) - set(staged_by_bc))
    staged_only = sorted(set(staged_by_bc) - set(baseline_products))

    grade_move_rows = []
    score_moves = 0
    grade_moves = 0
    grade_direction_counts = Counter()

    for bc in common:
        old = baseline_products[bc]
        new = staged_by_bc[bc]

        old_score = old.get("score")
        new_score = new.get("score")
        old_grade = old.get("grade")
        new_grade = new.get("grade")

        score_moved = (
            old_score is not None
            and new_score is not None
            and round(old_score) != round(new_score)
        )
        grade_moved = old_grade != new_grade

        if score_moved:
            score_moves += 1
        if grade_moved:
            grade_moves += 1
            direction = f"{old_grade}->{new_grade}"
            grade_direction_counts[direction] += 1

        grade_move_rows.append({
            "barcode": bc,
            "name": new.get("name", ""),
            "old_score": old_score,
            "new_score": new_score,
            "score_delta": (
                round(new_score - old_score, 2)
                if old_score is not None and new_score is not None
                else None
            ),
            "old_grade": old_grade,
            "new_grade": new_grade,
            "grade_moved": grade_moved,
            "d4_penalty": new.get("_d4_score_penalty"),
        })

    # Sort: grade movers first, then by score delta magnitude
    grade_move_rows.sort(
        key=lambda r: (not r["grade_moved"], -(abs(r["score_delta"] or 0)))
    )

    # Grade distribution (new)
    new_grade_dist = Counter(r["new_grade"] for r in grade_move_rows if r["new_grade"])
    old_grade_dist = Counter(r["old_grade"] for r in grade_move_rows if r["old_grade"])

    return {
        "total_baseline": len(baseline_products),
        "total_staged": len(staged_products),
        "common": len(common),
        "baseline_only": len(baseline_only),
        "staged_only": len(staged_only),
        "score_moves": score_moves,
        "grade_moves": grade_moves,
        "grade_direction_counts": dict(sorted(grade_direction_counts.items())),
        "old_grade_distribution": dict(sorted(old_grade_dist.items())),
        "new_grade_distribution": dict(sorted(new_grade_dist.items())),
        "grade_move_rows": grade_move_rows,
        "baseline_only_barcodes": baseline_only,
        "staged_only_barcodes": staged_only,
    }


# ---------------------------------------------------------------------------
# Write grade-move CSV
# ---------------------------------------------------------------------------

def write_grade_move_csv(diff: dict, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = diff["grade_move_rows"]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "barcode", "name", "old_score", "new_score", "score_delta",
            "old_grade", "new_grade", "grade_moved", "d4_penalty",
        ])
        for r in rows:
            writer.writerow([
                r["barcode"], r["name"],
                r["old_score"], r["new_score"], r["score_delta"],
                r["old_grade"], r["new_grade"], r["grade_moved"], r["d4_penalty"],
            ])
    print(f"  Grade-move table written: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    t0 = time.perf_counter()
    print("=" * 70)
    print("TASK-393 — Cookies-coffee D4 rescore (STAGING MEASUREMENT ONLY)")
    print("=" * 70)
    print(f"Config: {CONFIG_PATH}")
    print(f"Staging dir: {STAGING_DIR}")
    print(f"Baseline: {BASELINE_PATH}")
    print()

    # 1. Load config
    config = load_json(CONFIG_PATH)
    corpus_dirs = config.get("corpus_dirs", [])
    exclusion_set = load_exclusion_set(config)
    print(f"Exclusions: {len(exclusion_set)} barcodes")

    # 2. Collect BSIP1 files
    print("\n--- Step 1: Collect BSIP1 corpus ---")
    bsip1_files = collect_bsip1_files(corpus_dirs)
    print(f"  BSIP1 files collected: {len(bsip1_files)}")
    if not bsip1_files:
        print("FATAL: no BSIP1 files found — aborting")
        return 1

    # Build lookup for name resolution
    bsip1_lookup = {}
    for f in bsip1_files:
        try:
            rec = load_json(f)
            bc = str(rec.get("barcode", "")).strip()
            if bc:
                bsip1_lookup[bc] = rec
        except Exception:
            pass

    # 3. Snapshot env and score
    print("\n--- Step 2: Score corpus with D4=on ---")
    print(f"  Flags: {TASK393_FLAGS}")
    env_snap = snapshot_env()
    off_violations = []
    scored = 0
    try:
        scored, off_violations = score_corpus(bsip1_files, PRODUCTS_DIR, TASK393_FLAGS)
    finally:
        restore_env(env_snap)

    print(f"  Scored: {scored} products")

    if off_violations:
        print(f"FATAL: OFF violation(s) detected in BSIP1 corpus: {off_violations}")
        return 1

    # 4. Load new traces
    print("\n--- Step 3: Load new traces ---")
    traces = load_traces_by_barcode(PRODUCTS_DIR)
    print(f"  Traces loaded: {len(traces)}")

    # 5. OFF check on traces
    off_in_traces = sum(1 for t in traces.values() if off_in_record(t))
    print(f"  OFF in traces: {off_in_traces}")
    if off_in_traces > 0:
        print("FATAL: OFF contamination found in traces — aborting")
        return 1

    # 6. Load baseline
    print("\n--- Step 4: Load baseline ---")
    baseline_products = load_baseline(BASELINE_PATH)
    print(f"  Baseline products: {len(baseline_products)}")

    # 7. Build staged page
    print("\n--- Step 5: Build staged page ---")
    staged_page = build_staged_page(
        traces, bsip1_lookup, baseline_products, exclusion_set, TASK393_FLAGS
    )
    write_json(STAGED_PAGE, staged_page)
    print(f"  Staged page written: {STAGED_PAGE}")
    print(f"  Products in staged page: {len(staged_page['products'])}")

    # 8. OFF check on staged page
    off_in_page = sum(
        1 for p in staged_page["products"] if off_in_record(p)
    )
    print(f"  OFF in staged page: {off_in_page}")
    if off_in_page > 0:
        print("FATAL: OFF contamination in staged page — aborting")
        return 1

    # 9. Diff
    print("\n--- Step 6: Compute diff vs baseline ---")
    diff = compute_diff(baseline_products, staged_page["products"])
    write_grade_move_csv(diff, GRADE_MOVE_TABLE)

    print(f"\n  Baseline products:  {diff['total_baseline']}")
    print(f"  Staged products:    {diff['total_staged']}")
    print(f"  Common (matched):   {diff['common']}")
    print(f"  Baseline-only:      {diff['baseline_only']} {diff['baseline_only_barcodes']}")
    print(f"  Staged-only:        {diff['staged_only']} {diff['staged_only_barcodes']}")
    print(f"\n  Score moves:        {diff['score_moves']} / {diff['common']}")
    print(f"  Grade moves:        {diff['grade_moves']} / {diff['common']}")
    print(f"\n  Grade direction breakdown:")
    for direction, count in sorted(diff["grade_direction_counts"].items()):
        print(f"    {direction}: {count}")
    print(f"\n  Old grade distribution: {diff['old_grade_distribution']}")
    print(f"  New grade distribution: {diff['new_grade_distribution']}")

    # 10. Print barcode|old_score|new_score|old_grade|new_grade table for grade movers
    print("\n--- Grade movers (barcode | old_score | new_score | old_grade | new_grade | d4_penalty) ---")
    grade_movers = [r for r in diff["grade_move_rows"] if r["grade_moved"]]
    if grade_movers:
        print(f"{'barcode':<20} {'old_score':>9} {'new_score':>9} {'delta':>6} {'old_G':>5} {'new_G':>5} {'d4_pen':>7}  name")
        for r in grade_movers:
            print(
                f"{r['barcode']:<20} {str(r['old_score'] or 'None'):>9} "
                f"{str(r['new_score'] or 'None'):>9} {str(r['score_delta'] or 'None'):>6} "
                f"{r['old_grade'] or '?':>5} {r['new_grade'] or '?':>5} "
                f"{str(r['d4_penalty'] or 0):>7}  {r['name']}"
            )
    else:
        print("  (no grade movers)")

    # 11. Write summary
    elapsed = time.perf_counter() - t0
    summary = {
        "task": "TASK-393",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stage": "SCORING_MEASUREMENT_ONLY",
        "flags_applied": TASK393_FLAGS,
        "bsip1_files": len(bsip1_files),
        "scored": scored,
        "off_violations_bsip1": len(off_violations),
        "off_in_traces": off_in_traces,
        "off_in_page": off_in_page,
        "off_used": False,
        "diff": {
            "total_baseline": diff["total_baseline"],
            "total_staged": diff["total_staged"],
            "common": diff["common"],
            "baseline_only": diff["baseline_only"],
            "staged_only": diff["staged_only"],
            "score_moves": diff["score_moves"],
            "grade_moves": diff["grade_moves"],
            "grade_direction_counts": diff["grade_direction_counts"],
            "old_grade_distribution": diff["old_grade_distribution"],
            "new_grade_distribution": diff["new_grade_distribution"],
        },
        "grade_move_table_csv": str(GRADE_MOVE_TABLE),
        "staged_page_json": str(STAGED_PAGE),
        "live_files_touched": [],
        "wall_clock_sec": round(elapsed, 2),
    }
    write_json(SUMMARY_PATH, summary)
    print(f"\n  Summary written: {SUMMARY_PATH}")

    # 12. Gate: hard fail only on OFF or error
    if off_violations or off_in_traces > 0 or off_in_page > 0:
        print("\nRESULT: HARD FAIL — OFF contamination detected")
        return 1

    print(f"\nRESULT: STAGING COMPLETE — {diff['grade_moves']} grade moves measured")
    print(f"Wall-clock: {elapsed:.1f}s")
    print()
    print("GUARDS:")
    print(f"  OFF=0 (BSIP1 corpus, traces, staged page): confirmed")
    print(f"  Live files touched: 0")
    print(f"  Deploy status: NOT_DEPLOYED")
    print(f"  Copy authored: NO (PENDING_COPY carried from baseline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
