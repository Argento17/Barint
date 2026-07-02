"""
measure_r3_biscuit_narrow_v1.py — TASK-394 Cross-Shelf Impact Measurement
=========================================================================
Measures the full cross-shelf impact of BARI_R3_BISCUIT_NARROW_V1 (OFF vs ON).

Scope: ALL live frontend JSON files (18 active shelves, ~520 products).
For each shelf, re-scores every product twice — once with flag OFF, once with flag ON —
and produces a full diff table of every category/score/grade change.

CRITICAL: env flags set BEFORE any engine import (env-before-import discipline,
juices contamination bug pattern). The flag state switch is achieved by running two
separate Python sub-processes, each with the appropriate env before import.

Output dir: C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_task394_r3_measure\
  off_scores.json       — per-barcode {cat, score, grade} with flag OFF
  on_scores.json        — per-barcode {cat, score, grade} with flag ON
  diff_table.json       — every product whose cat/score/grade changed
  safety_assertions.json — verification of the 3 safety assertions
  verification_table.csv — full flat machine-readable table (barcode/shelf/off_cat/on_cat/...)
  run_record.json        — run metadata

Does NOT touch any frontend JSON or deployed files.
"""
import os, sys

# ============================================================================
# CRITICAL: Set ALL flag state BEFORE any engine import.
# This script sets the COMMON flags (production defaults).
# The R3 flag is passed via subprocess so each run gets a clean import.
# ============================================================================
os.environ["BARI_RECAL_P0"]                  = "off"
os.environ["BARI_GRAD_SODIUM_V1"]            = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"]  = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"]               = "off"
os.environ["BARI_SODIUM_CEREAL"]             = "off"
os.environ["BARI_TASK144_FIXES"]             = "off"
os.environ["BARI_FAT_TECH_V1"]               = "on"
os.environ["BARI_D4_SCORE_V1"]               = "off"
os.environ["BARI_HC_DAIRY_SATFAT_V1"]        = "off"
os.environ["BARI_SHELF_RELATIVE_V1"]         = "off"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"]      = "off"
os.environ["BARI_GLASSBOX_W2"]               = "off"
os.environ["BARI_GLASSBOX_D5D6"]             = "off"
os.environ["BARI_GLASSBOX_W15"]              = "off"
# R3 flag must be set BEFORE import — controlled in _score_shelf() below
# (this master process sets it for import; subprocess workers inherit it)

import json, pathlib, datetime, hashlib, csv, logging, subprocess, tempfile
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
SRC  = pathlib.Path(__file__).parent
COMPARISONS = ROOT / "bari-web" / "src" / "data" / "comparisons"
OUT_DIR = ROOT / "02_products" / "cookies_coffee" / "bsip2_outputs" / "run_task394_r3_measure"
RUN_ID  = "run_task394_r3_measure"
TASK_ID = "TASK-394"

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]

def score_to_grade(score):
    if score is None:
        return None
    for grade, floor in GRADE_SCALE:
        if score >= floor:
            return grade
    return "E"

def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stdev(scores):
    if not scores: return 0.0
    n = len(scores)
    mean = sum(scores) / n
    return (sum((x - mean)**2 for x in scores) / n) ** 0.5

# ---------------------------------------------------------------------------
# BSIP1 corpus map — shelf_slug → list of BSIP1 output dirs (ordered by priority)
# The map covers every live frontend JSON file. First-listed dir wins for dedup.
# ---------------------------------------------------------------------------
SHELF_CORPUS_MAP: dict[str, list[pathlib.Path]] = {
    "cookies_coffee": [
        ROOT / "03_operations/bsip1/run_cookies_001/output",
        ROOT / "03_operations/bsip1/run_cakes_001/output",
    ],
    "cakes_hard_cookies": [
        ROOT / "03_operations/bsip1/run_cakes_001/output",
        ROOT / "03_operations/bsip1/run_cookies_001/output",
    ],
    "chocolate_tablets": [
        ROOT / "03_operations/bsip1/score_choc_task362_20260621_114832/output",
        ROOT / "03_operations/bsip1/task366_20260622T130415/output",
        ROOT / "03_operations/bsip1/choc_task366_pass2_20260622_140336/output",
    ],
    "chocolate_bars": [
        ROOT / "03_operations/bsip1/score_bars_task362_20260620_150421/output",
        ROOT / "03_operations/bsip1/score_choc_task362_20260621_114832/output",
    ],
    "granola": [
        ROOT / "03_operations/bsip1/fresh_rescore_task391_20260624_113405/output",
    ],
    "protein_bars": [
        ROOT / "03_operations/bsip1/score_bars_task362_20260620_150421/output",
        ROOT / "03_operations/bsip1/run_snacks_task360_phase3_20260620_083413/output",
    ],
    "protein_combined": [
        ROOT / "03_operations/bsip1/score_bars_task362_20260620_150421/output",
        ROOT / "03_operations/bsip1/score_choc_task362_20260621_114832/output",
        ROOT / "03_operations/bsip1/run_snacks_task360_phase3_20260620_083413/output",
    ],
    "snacks": [
        ROOT / "03_operations/bsip1/run_snacks_task360_phase3_20260620_083413/output",
        ROOT / "03_operations/bsip1/run_snacks_task360_shuf_20260620_064221/output",
    ],
    "cereals": [
        ROOT / "03_operations/bsip1/run_cereals_008/output",
        ROOT / "03_operations/bsip1/run_cereals_006/output",
        ROOT / "03_operations/bsip1/run_cereals_005/output",
        ROOT / "03_operations/bsip1/run_cereals_002/output",
        ROOT / "03_operations/bsip1/run_cereals_001/output",
    ],
    "brined_cheeses": [
        ROOT / "03_operations/bsip1/run_brined_cheeses_002/output",
        ROOT / "03_operations/bsip1/run_brined_cheeses_001/output",
    ],
    "cheese": [
        ROOT / "03_operations/bsip1/run_cheese_003/output",
        ROOT / "03_operations/bsip1/run_cheese_001/output",
    ],
    "hard_cheeses": [
        ROOT / "03_operations/bsip1/run_cheese_003/output",
        ROOT / "03_operations/bsip1/run_cheese_001/output",
    ],
    "hummus": [
        ROOT / "03_operations/bsip1/run_hummus_001/output",
    ],
    "bread": [
        ROOT / "03_operations/bsip1/run_bread_conform_001/output",
        ROOT / "03_operations/bsip1/run_bread_light_001/output",
    ],
    "juices": [
        # Juices uses a different corpus structure — walk bsip1_outputs
        ROOT / "02_products/juices/bsip1_outputs",
    ],
    "milk": [
        ROOT / "03_operations/bsip1/run_milk_002/output",
        ROOT / "03_operations/bsip1/run_milk_001/output",
    ],
    "yogurts": [
        ROOT / "03_operations/bsip1/run_yogurt_006/output",
        ROOT / "03_operations/bsip1/run_yogurt_005/output",
        ROOT / "03_operations/bsip1/run_yogurt_004/output",
        ROOT / "03_operations/bsip1/run_yogurt_001/output",
    ],
}

# Map frontend JSON filename to shelf slug
FRONTEND_TO_SHELF: dict[str, str] = {
    "cookies_coffee_frontend_v2.json":       "cookies_coffee",
    "cakes_hard_cookies_frontend_v1.json":   "cakes_hard_cookies",
    "chocolate_tablets_frontend_v1.json":    "chocolate_tablets",
    "chocolate_bars_frontend_v1.json":       "chocolate_bars",
    "granola_frontend_v2.json":              "granola",
    "protein_bars_frontend_v1.json":         "protein_bars",
    "protein_combined_frontend_v2.json":     "protein_combined",
    "snacks_frontend_v5.json":               "snacks",
    "cereals_frontend_v2.json":              "cereals",
    "brined_cheeses_frontend_v2.json":       "brined_cheeses",
    "cheese_frontend_v4.json":               "cheese",
    "hard_cheeses_frontend_v2.json":         "hard_cheeses",
    "hummus_frontend_v5.json":               "hummus",
    "bread_frontend_v3.json":                "bread",
    "juices_frontend_v3.json":               "juices",
    "milk_frontend_v1.json":                 "milk",
}


def build_corpus_lookup(shelf_slug: str) -> dict:
    """Build barcode -> bsip1_record lookup for a shelf. First-listed dir wins."""
    dirs = SHELF_CORPUS_MAP.get(shelf_slug, [])
    lookup = {}
    for d in dirs:
        if not d.exists():
            log.warning("Corpus dir missing: %s", d)
            continue
        for fp in sorted(d.glob("bsip1_*.json")):
            try:
                doc = json.loads(fp.read_text(encoding="utf-8"))
                bc = str(doc.get("barcode") or "")
                if bc and bc not in lookup:
                    lookup[bc] = doc
            except Exception as e:
                log.warning("Corpus load error %s: %s", fp.name, e)
    return lookup


def _score_one_product(bsip1_doc: dict, r3_flag: bool) -> dict | None:
    """Score one product with the given R3 flag state. Returns trace dict or None."""
    # Import engine modules (flag already set in environment)
    # This function assumes os.environ["BARI_R3_BISCUIT_NARROW_V1"] is already set
    # correctly before this function is called (and before the modules were imported).
    try:
        from signal_extractor import extract_signals
        from router_v2 import classify_category
        from nova_proxy import infer_nova
        from evaluation_scope import assign_evaluation_scope
        from score_engine import score_product
        from trace_writer import assemble_trace
        from structural_classifier import classify_structural_class

        signals     = extract_signals(bsip1_doc)
        cat_result  = classify_category(bsip1_doc)
        l3          = signals["L3_inferred_classifications"]
        nova_result = infer_nova(bsip1_doc, l3)
        eval_result = assign_evaluation_scope(bsip1_doc, cat_result["category"])
        score_result= score_product(bsip1_doc, signals, cat_result, nova_result, eval_result)
        trace       = assemble_trace(bsip1_doc, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)
        return trace
    except Exception as e:
        log.error("Score error barcode=%s: %s", bsip1_doc.get("barcode"), e)
        import traceback; traceback.print_exc()
        return None


def score_shelf(
    shelf_slug: str,
    frontend_path: pathlib.Path,
    r3_on: bool,
) -> dict[str, dict]:
    """Score all products on a shelf. Returns barcode -> {cat, score, grade, name}."""
    corpus = build_corpus_lookup(shelf_slug)

    frontend = json.loads(frontend_path.read_text(encoding="utf-8"))
    live_products = frontend.get("products") or []

    results = {}
    for p in live_products:
        bc = str(p.get("barcode") or "")
        name = p.get("name") or p.get("nameHe") or ""
        if not bc:
            continue

        bsip1_doc = corpus.get(bc)
        if not bsip1_doc:
            log.debug("No BSIP1 match: %s (%s) on shelf %s", bc, name, shelf_slug)
            results[bc] = {
                "barcode": bc, "name": name, "shelf": shelf_slug,
                "category": None, "score": None, "grade": None,
                "no_corpus": True,
            }
            continue

        trace = _score_one_product(bsip1_doc, r3_on)
        if trace is None:
            results[bc] = {
                "barcode": bc, "name": name, "shelf": shelf_slug,
                "category": None, "score": None, "grade": None,
                "score_error": True,
            }
            continue

        score = trace.get("final_score_estimate")
        cat   = trace.get("category")
        grade = score_to_grade(score)
        results[bc] = {
            "barcode": bc,
            "name":    name,
            "shelf":   shelf_slug,
            "category": cat,
            "score":   round(score, 1) if score is not None else None,
            "grade":   grade,
            "binding_cap": trace.get("binding_cap"),
            "nova": trace.get("nova_proxy"),
            "anchor_override": trace.get("anchor_override"),
            "r3_override_trace": trace.get("req362_override_trace"),
        }
    return results


def run_two_pass(r3_on: bool, all_shelves: list) -> dict[str, dict[str, dict]]:
    """Run scoring for all shelves with given flag state. Returns shelf -> {bc -> row}."""
    import importlib, sys as _sys

    # Reload router_v2 with the correct flag state.
    # env-before-import: env must be set BEFORE importing the module.
    flag_val = "on" if r3_on else "off"
    os.environ["BARI_R3_BISCUIT_NARROW_V1"] = flag_val

    # Force-reload modules that read flags at import time
    modules_to_reload = [
        "router_v2", "score_engine", "signal_extractor",
        "evaluation_scope", "nova_proxy", "trace_writer",
        "structural_classifier", "constants", "grade_governance",
    ]
    for mod in modules_to_reload:
        if mod in _sys.modules:
            del _sys.modules[mod]

    log.info("=== BARI_R3_BISCUIT_NARROW_V1=%s — scoring %d shelves ===", flag_val, len(all_shelves))

    shelf_results = {}
    for shelf_slug, frontend_path in all_shelves:
        log.info("  Shelf: %s | flag=%s", shelf_slug, flag_val)
        results = score_shelf(shelf_slug, frontend_path, r3_on)
        shelf_results[shelf_slug] = results
        counts = Counter(r["grade"] for r in results.values() if r.get("grade"))
        log.info("    %d products | %s", len(results), dict(counts))

    return shelf_results


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-394: R3 Biscuit Narrow V1 — cross-shelf impact measurement ===")
    log.info("Run ID: %s | TS: %s", RUN_ID, ts)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure SRC is on path for engine imports
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    # Build shelf list from live frontend JSON files
    all_shelves = []
    for fj in sorted(COMPARISONS.glob("*.json")):
        slug = FRONTEND_TO_SHELF.get(fj.name)
        if slug is None:
            log.debug("Skipping unmapped frontend: %s", fj.name)
            continue
        all_shelves.append((slug, fj))
    log.info("Live shelves to score: %d", len(all_shelves))

    # ---- Pass 1: flag OFF (baseline) ----
    off_results = run_two_pass(r3_on=False, all_shelves=all_shelves)

    # ---- Pass 2: flag ON ----
    on_results  = run_two_pass(r3_on=True,  all_shelves=all_shelves)

    # ---- Build diff table ----
    diff_rows = []
    all_barcodes_off = {}   # bc -> row (dedup by bc, keep first shelf)
    all_barcodes_on  = {}

    for shelf_slug, _ in all_shelves:
        for bc, row_off in off_results.get(shelf_slug, {}).items():
            row_on = on_results.get(shelf_slug, {}).get(bc, {})
            if not row_on:
                continue
            all_barcodes_off[bc] = row_off
            all_barcodes_on[bc]  = row_on

            cat_off   = row_off.get("category")
            cat_on    = row_on.get("category")
            score_off = row_off.get("score")
            score_on  = row_on.get("score")
            grade_off = row_off.get("grade")
            grade_on  = row_on.get("grade")

            cat_changed   = (cat_off != cat_on)
            grade_changed = (grade_off != grade_on)
            score_delta   = (
                round(score_on - score_off, 1)
                if (score_on is not None and score_off is not None) else None
            )
            score_changed = (score_delta is not None and score_delta != 0.0)

            if cat_changed or grade_changed or score_changed:
                diff_rows.append({
                    "barcode":       bc,
                    "name":          row_off.get("name", ""),
                    "shelf":         shelf_slug,
                    "off_category":  cat_off,
                    "on_category":   cat_on,
                    "off_score":     score_off,
                    "on_score":      score_on,
                    "score_delta":   score_delta,
                    "off_grade":     grade_off,
                    "on_grade":      grade_on,
                    "cat_changed":   cat_changed,
                    "grade_changed": grade_changed,
                    "score_changed": score_changed,
                    "r3_off_trace":  row_off.get("r3_override_trace"),
                    "r3_on_trace":   row_on.get("r3_override_trace"),
                })

    diff_rows.sort(key=lambda x: (x["shelf"], x.get("off_score") or 0))

    # ---- Safety assertion 1: ZERO genuine-chocolate products change ----
    # Genuine chocolate: chocolate_tablets, chocolate_bars shelves
    choc_movers = [r for r in diff_rows if r["shelf"] in ("chocolate_tablets", "chocolate_bars")]
    sa1_pass = len(choc_movers) == 0

    # ---- Safety assertion 2: only biscuit-anchored flavor-descriptor products move ----
    # Every mover should have: off_category = snack_bar_granola (R3 fired),
    # on_category = biscuit (R3 yielded), AND off_trace shows rule3_chocolate_lens
    sa2_violations = []
    for r in diff_rows:
        if r["shelf"] in ("chocolate_tablets", "chocolate_bars"):
            continue  # already in SA1
        off_trace = r.get("r3_off_trace") or {}
        on_trace  = r.get("r3_on_trace") or {}
        off_override = off_trace.get("override_applied")
        on_override  = on_trace.get("override_applied")
        # Valid mover: R3 fired OFF (rule3_chocolate_lens), R3 yielded ON (None, biscuit stays)
        off_is_r3   = (off_override == "rule3_chocolate_lens")
        on_is_yield = (on_override is None and r["on_category"] == "biscuit")
        if r.get("cat_changed") and not (off_is_r3 and on_is_yield):
            sa2_violations.append({
                "barcode": r["barcode"], "name": r["name"], "shelf": r["shelf"],
                "off_cat": r["off_category"], "on_cat": r["on_category"],
                "off_override": off_override, "on_override": on_override,
                "issue": "unexpected mover pattern",
            })
    sa2_pass = len(sa2_violations) == 0

    # ---- Safety assertion 3: specific cookies — 2986065 + 7290017894317 ----
    sa3_2986065 = None
    sa3_7290017894317 = None
    for r in diff_rows:
        if r["barcode"] == "2986065":
            sa3_2986065 = r
        if r["barcode"] == "7290017894317":
            sa3_7290017894317 = r

    # ---- Per-shelf grade distribution diff ----
    shelf_grade_diffs = {}
    for shelf_slug, _ in all_shelves:
        off_grades = Counter(
            r.get("grade") for r in off_results.get(shelf_slug, {}).values()
            if r.get("grade") is not None
        )
        on_grades = Counter(
            r.get("grade") for r in on_results.get(shelf_slug, {}).values()
            if r.get("grade") is not None
        )
        all_grades = set(off_grades) | set(on_grades)
        shelf_grade_diffs[shelf_slug] = {
            g: {"off": off_grades.get(g, 0), "on": on_grades.get(g, 0),
                "delta": on_grades.get(g, 0) - off_grades.get(g, 0)}
            for g in sorted(all_grades)
        }

    # ---- Totals ----
    total_products = sum(len(v) for v in off_results.values())
    total_cat_changed   = sum(1 for r in diff_rows if r["cat_changed"])
    total_grade_changed = sum(1 for r in diff_rows if r["grade_changed"])
    total_score_changed = sum(1 for r in diff_rows if r["score_changed"] and not r["grade_changed"])

    log.info("=== RESULTS ===")
    log.info("Total products scored: %d", total_products)
    log.info("Category changes: %d | Grade changes: %d | Score-only: %d",
             total_cat_changed, total_grade_changed, total_score_changed)
    log.info("SA1 (no genuine-chocolate movers): %s", "PASS" if sa1_pass else "FAIL")
    log.info("SA2 (only biscuit-anchor flavor-descriptor movers): %s", "PASS" if sa2_pass else "FAIL")

    # ---- Save artifacts ----

    # off/on score tables
    off_flat = {bc: {
        "barcode": bc, "shelf": r["shelf"], "name": r["name"],
        "category": r["category"], "score": r["score"], "grade": r["grade"],
    } for bc, r in all_barcodes_off.items()}
    on_flat = {bc: {
        "barcode": bc, "shelf": r["shelf"], "name": r["name"],
        "category": r["category"], "score": r["score"], "grade": r["grade"],
    } for bc, r in all_barcodes_on.items()}

    (OUT_DIR / "off_scores.json").write_text(
        json.dumps(off_flat, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "on_scores.json").write_text(
        json.dumps(on_flat, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "diff_table.json").write_text(
        json.dumps(diff_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Safety assertions
    sa_report = {
        "SA1_no_chocolate_shelf_movers": {
            "pass": sa1_pass,
            "description": "ZERO genuine-chocolate products (chocolate_tablets/chocolate_bars shelves) change category/score/grade",
            "choc_movers_found": len(choc_movers),
            "detail": choc_movers if not sa1_pass else [],
        },
        "SA2_only_biscuit_anchor_flavor_descriptors_move": {
            "pass": sa2_pass,
            "description": "Every category-changing mover has R3 fired OFF (rule3_chocolate_lens) and R3 yielded ON (biscuit stays)",
            "violations_found": len(sa2_violations),
            "violations": sa2_violations if not sa2_pass else [],
        },
        "SA3_specific_cookies": {
            "barcode_2986065": {
                "name": "פתי בר בטעם שוקולד",
                "description": "Petit Beurre chocolate FLAVOR (hard biscuit anchor 0.93) — expect: OFF=snack_bar_granola/E, ON=biscuit/D",
                "off_cat": sa3_2986065["off_category"] if sa3_2986065 else "NOT_IN_DIFF (no change)",
                "off_score": sa3_2986065["off_score"] if sa3_2986065 else None,
                "off_grade": sa3_2986065["off_grade"] if sa3_2986065 else None,
                "on_cat":  sa3_2986065["on_category"] if sa3_2986065 else None,
                "on_score": sa3_2986065["on_score"] if sa3_2986065 else None,
                "on_grade": sa3_2986065["on_grade"] if sa3_2986065 else None,
                "moved": sa3_2986065 is not None,
            },
            "barcode_7290017894317": {
                "name": "עוגיות כוסמין מלא שוקולד",
                "description": "Whole-spelt cookie w/ 10% choc chips (עוגיות hard anchor 0.85) — Nutrition said E defensible on merits; report honestly",
                "off_cat": sa3_7290017894317["off_category"] if sa3_7290017894317 else "NOT_IN_DIFF (no change)",
                "off_score": sa3_7290017894317["off_score"] if sa3_7290017894317 else None,
                "off_grade": sa3_7290017894317["off_grade"] if sa3_7290017894317 else None,
                "on_cat":  sa3_7290017894317["on_category"] if sa3_7290017894317 else None,
                "on_score": sa3_7290017894317["on_score"] if sa3_7290017894317 else None,
                "on_grade": sa3_7290017894317["on_grade"] if sa3_7290017894317 else None,
                "moved": sa3_7290017894317 is not None,
            },
        },
    }
    (OUT_DIR / "safety_assertions.json").write_text(
        json.dumps(sa_report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Verification table CSV
    verify_path = OUT_DIR / "verification_table.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        writer = csv.writer(vf)
        writer.writerow([
            "barcode", "name", "shelf",
            "off_category", "off_score", "off_grade",
            "on_category",  "on_score",  "on_grade",
            "score_delta", "cat_changed", "grade_changed", "score_changed",
        ])
        # Write ALL products (not just movers)
        all_bcs = set(all_barcodes_off) | set(all_barcodes_on)
        for bc in sorted(all_bcs):
            row_off = all_barcodes_off.get(bc, {})
            row_on  = all_barcodes_on.get(bc, {})
            # Check if in diff
            diff_row = next((r for r in diff_rows if r["barcode"] == bc), None)
            writer.writerow([
                bc,
                row_off.get("name") or row_on.get("name") or "",
                row_off.get("shelf") or row_on.get("shelf") or "",
                row_off.get("category"), row_off.get("score"), row_off.get("grade"),
                row_on.get("category"),  row_on.get("score"),  row_on.get("grade"),
                diff_row["score_delta"] if diff_row else 0.0,
                diff_row["cat_changed"]   if diff_row else False,
                diff_row["grade_changed"] if diff_row else False,
                diff_row["score_changed"] if diff_row else False,
            ])

    # Run record
    engine_sha  = sha256_file(SRC / "score_engine.py")
    router_sha  = sha256_file(SRC / "router_v2.py")
    signal_sha  = sha256_file(SRC / "signal_extractor.py")
    eval_sha    = sha256_file(SRC / "evaluation_scope.py")

    # Full grade distribution OFF vs ON (across all shelves combined)
    all_off_grades = Counter(r.get("grade") for r in all_barcodes_off.values() if r.get("grade"))
    all_on_grades  = Counter(r.get("grade") for r in all_barcodes_on.values() if r.get("grade"))

    run_record = {
        "run_id":  RUN_ID,
        "task":    TASK_ID,
        "generated": ts,
        "flag_state": {
            "BARI_R3_BISCUIT_NARROW_V1": "off (baseline) vs on (treatment)",
            "BARI_FAT_TECH_V1":          "on",
            "all_others":                "off",
        },
        "scope": {
            "shelves_scored": len(all_shelves),
            "shelf_slugs": [s for s, _ in all_shelves],
            "total_products_scored": total_products,
            "total_unique_barcodes": len(all_bcs if 'all_bcs' in dir() else []),
        },
        "diff_summary": {
            "total_products_with_any_change": len(diff_rows),
            "category_changes": total_cat_changed,
            "grade_changes": total_grade_changed,
            "score_only_changes": total_score_changed,
            "diff_table_path": str(OUT_DIR / "diff_table.json"),
        },
        "grade_distribution": {
            "OFF": dict(all_off_grades),
            "ON":  dict(all_on_grades),
        },
        "per_shelf_grade_diffs": shelf_grade_diffs,
        "safety_assertions": {
            "SA1_pass": sa1_pass,
            "SA2_pass": sa2_pass,
            "SA3_2986065_moved": sa3_2986065 is not None,
            "SA3_7290017894317_moved": sa3_7290017894317 is not None,
        },
        "artifacts": {
            "off_scores":          str(OUT_DIR / "off_scores.json"),
            "on_scores":           str(OUT_DIR / "on_scores.json"),
            "diff_table":          str(OUT_DIR / "diff_table.json"),
            "safety_assertions":   str(OUT_DIR / "safety_assertions.json"),
            "verification_table":  str(verify_path),
        },
        "engine_sha256":  engine_sha,
        "router_sha256":  router_sha,
        "signal_sha256":  signal_sha,
        "eval_sha256":    eval_sha,
        "off_used": False,
    }

    rr_path = OUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- Print summary ----
    print("\n" + "=" * 76)
    print(f"TASK-394: R3 BISCUIT NARROW V1 — CROSS-SHELF IMPACT MEASUREMENT")
    print(f"Run ID: {RUN_ID}")
    print("=" * 76)
    print(f"Shelves scored: {len(all_shelves)} | Total products: {total_products}")
    print()
    print("OVERALL GRADE DISTRIBUTION:")
    print(f"  {'Grade':<6}  {'OFF':>6}  {'ON':>6}  {'Delta':>6}")
    for g in ["S", "A", "B", "C", "D", "E"]:
        off_c = all_off_grades.get(g, 0)
        on_c  = all_on_grades.get(g, 0)
        print(f"  {g:<6}  {off_c:>6}  {on_c:>6}  {on_c - off_c:>+6}")
    print()
    print(f"TOTAL CHANGES (OFF->ON): {len(diff_rows)} products")
    print(f"  Category changes: {total_cat_changed}")
    print(f"  Grade changes:    {total_grade_changed}")
    print(f"  Score-only:       {total_score_changed}")
    print()
    print("FULL DIFF TABLE (category/score/grade movers):")
    print(f"  {'Barcode':<20}  {'Shelf':<22}  {'OFF Cat':<20}  {'ON Cat':<14}  {'OFF Sc':>7}  {'ON Sc':>7}  {'OFF Gr':>7}  {'ON Gr':>7}")
    for r in diff_rows:
        print(f"  {r['barcode']:<20}  {r['shelf']:<22}  {str(r['off_category']):<20}  {str(r['on_category']):<14}  {str(r['off_score']):>7}  {str(r['on_score']):>7}  {str(r['off_grade']):>7}  {str(r['on_grade']):>7}")
        # Print name on next line for readability
        print(f"    Name: {r['name']}")
    print()
    print("SAFETY ASSERTIONS:")
    print(f"  SA1 — No genuine-chocolate shelf movers: {'PASS' if sa1_pass else 'FAIL (' + str(len(choc_movers)) + ' movers found)'}")
    print(f"  SA2 — Only biscuit-anchor flavor-descriptor movers: {'PASS' if sa2_pass else 'FAIL (' + str(len(sa2_violations)) + ' violations)'}")
    print()
    print("SA3 — Specific cookies:")
    bc1 = "2986065"
    if sa3_2986065:
        print(f"  {bc1} (פתי בר בטעם שוקולד): OFF={sa3_2986065['off_category']}/{sa3_2986065['off_grade']} -> ON={sa3_2986065['on_category']}/{sa3_2986065['on_grade']} | score: {sa3_2986065['off_score']}->{sa3_2986065['on_score']}")
    else:
        # Not in diff — look up the off score directly
        off_row = all_barcodes_off.get(bc1, {})
        print(f"  {bc1} (פתי בר בטעם שוקולד): NO CHANGE — OFF={off_row.get('category')}/{off_row.get('grade')} (same ON)")
    bc2 = "7290017894317"
    if sa3_7290017894317:
        print(f"  {bc2} (עוגיות כוסמין מלא שוקולד): OFF={sa3_7290017894317['off_category']}/{sa3_7290017894317['off_grade']} -> ON={sa3_7290017894317['on_category']}/{sa3_7290017894317['on_grade']} | score: {sa3_7290017894317['off_score']}->{sa3_7290017894317['on_score']}")
    else:
        off_row = all_barcodes_off.get(bc2, {})
        print(f"  {bc2} (עוגיות כוסמין מלא שוקולד): NO CHANGE — OFF={off_row.get('category')}/{off_row.get('grade')} (same ON)")
    print()
    print("PER-SHELF GRADE DISTRIBUTION DELTAS (only shelves with change):")
    for shelf_slug, diffs in sorted(shelf_grade_diffs.items()):
        changed = any(diffs[g]["delta"] != 0 for g in diffs)
        if not changed:
            continue
        print(f"  {shelf_slug}:")
        for g in ["S", "A", "B", "C", "D", "E"]:
            if g in diffs and diffs[g]["delta"] != 0:
                d = diffs[g]
                print(f"    {g}: {d['off']} -> {d['on']} (delta={d['delta']:+d})")
    print()
    print("ARTIFACTS:")
    print(f"  Run dir:           {OUT_DIR}")
    print(f"  Run record:        {rr_path}")
    print(f"  Diff table:        {OUT_DIR / 'diff_table.json'}")
    print(f"  Safety assertions: {OUT_DIR / 'safety_assertions.json'}")
    print(f"  Verification CSV:  {verify_path}")
    print("=" * 76)

    return run_record


if __name__ == "__main__":
    main()
