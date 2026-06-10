"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_008)
Source: Shufersal real scrape -> BSIP1 run_cereals_008 (TASK-198 pipeline bug fixes).
Engine: BARI_RECAL_P0=on (byte-identical to run_006/007).

Purpose: re-run after TASK-198 pipeline bug fixes:
  Bug 1 (EV-029 family — fat/sugar null, ALREADY fixed in run_cereals_006):
    The run_cereals_005 BSIP1 had fat_g=0.5, sugars_g=null, fat_saturated_g=null
    for all products including Lion (true values: fat=6.2g, sugar=24.7g, sat=2.5g).
    This was the primary driver of the Lion>Wittebix score inversion.

  Bug 2 (EV-051 — marketing-bleed ingredient detection, NEW in run_cereals_008):
    Lion's "ingredient list" was marketing copy ("ניתן להוסיף: חלב, פרי טרי" =
    serving suggestion; "תענוג פראי!" = promotional tagline), not a real ingredient
    declaration. This caused:
      - ingredient_count = 5 (5 bullet-point marketing phrases, not real ingredients)
      - has_fermentation = True (false positive: "שמר" substring matched "משמרים")
      - has_whole_grain = True (based on marketing phrase "חיטה מלאה", not verified)
    Fix: BSIP1 builder now detects marketing bleed (Tier 1: categorically diagnostic
    phrases) and sets ingredient_text_quality = "marketing_bleed".
    Fix: signal_extractor.py now uses word-boundary regex for "שמר" so "משמרים"
    (preservatives) does not trigger a fermentation positive.

  Before/after for Lion: run_005 = 78/B (inflated) → run_008 = expected ~52-56/C
  Wittebix: unchanged at ~75/B. Inversion resolved.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_008/
"""

import sys
import json
import pathlib
import logging
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_008\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_008")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
RUN_ID       = "run_cereals_008"

CEREAL_OK_CATEGORIES = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_batch():
    import os
    recal_flag = os.environ.get("BARI_RECAL_P0", "off")
    log.info("=== BSIP2 Breakfast Cereals — %s (BARI_RECAL_P0=%s) ===", RUN_ID, recal_flag)
    if recal_flag.lower() != "on":
        log.warning("BARI_RECAL_P0 is NOT 'on'. Run with BARI_RECAL_P0=on for live consistency.")

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_ROOT / "products"
    if prod_dir.exists():
        import shutil
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces, errors, misroutes = [], [], []
    pmap = {p.get("canonical_product_id"): p for p in products}

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            if trace.get("category") not in CEREAL_OK_CATEGORIES:
                ref = trace.get("input_reference") or {}
                name = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
                misroutes.append({"pid": pid, "name": name, "routed_to": trace.get("category")})
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    n = len(traces)
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    scores = sorted([t.get("final_score_estimate") for t in sufficient])
    median = scores[len(scores) // 2] if scores else None
    misroute_pct = round(100.0 * len(misroutes) / max(n, 1), 1)

    # Split summary by granola sub-pool
    def subpool(pid):
        gov = (pmap.get(pid, {}).get("cereals_governance") or {}).get("construct_1_granola_subpool") or {}
        return gov.get("subpool")
    granola = [t for t in sufficient if subpool(t.get("canonical_product_id")) == "granola"]
    standard = [t for t in sufficient if subpool(t.get("canonical_product_id")) != "granola"]

    # TASK-198 delta check — Lion vs Wittebix before/after
    lion_trace = next((t for t in traces if "5900020036407" in str(t.get("canonical_product_id",""))), None)
    witt_trace = next((t for t in traces if "5010029000061" in str(t.get("canonical_product_id",""))), None)
    task198_delta = {
        "lion_run_005_score": 78,
        "lion_run_005_grade": "B",
        "lion_run_008_score": round(lion_trace["final_score_estimate"]) if lion_trace else None,
        "lion_run_008_grade": lion_trace.get("grade_estimate") if lion_trace else None,
        "wittebix_run_005_score": 75,
        "wittebix_run_005_grade": "B",
        "wittebix_run_008_score": round(witt_trace["final_score_estimate"]) if witt_trace else None,
        "wittebix_run_008_grade": witt_trace.get("grade_estimate") if witt_trace else None,
        "inversion_resolved": (
            (witt_trace["final_score_estimate"] > lion_trace["final_score_estimate"])
            if (lion_trace and witt_trace) else None
        ),
    }
    log.info("TASK-198 delta: %s", task198_delta)

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": "proto_v0 / BARI_RECAL_P0=" + recal_flag + " (byte-identical to run_006/007)",
        "data_fixes": [
            "TASK-198 / EV-051 Bug1: fat/sugar/sat-fat pass-through corrected (run_cereals_006 fix, carried forward)",
            "TASK-198 / EV-051 Bug2: marketing-bleed detection added to BSIP1 builder (Lion ingredient_text_quality=marketing_bleed)",
            "TASK-198 / EV-051 Bug2b: fermentation word-boundary fix in signal_extractor (שמר not in משמרים)",
        ],
        "source": "Shufersal real scrape 2026-06-05 -> BSIP1 run_cereals_008 (TASK-198 fixes)",
        "processed": n,
        "scored": len(sufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "misroute_count": len(misroutes),
        "misroute_pct": misroute_pct,
        "misroutes": misroutes,
        "split_for_new_categories": {
            "breakfast_cereals_standard_count": len(standard),
            "granola_count": len(granola),
        },
        "task198_inversion_delta": task198_delta,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", path)
    log.info("Grades=%s median=%s misroute=%.1f%% | standard=%d granola=%d",
             dist, median, misroute_pct, len(standard), len(granola))
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
