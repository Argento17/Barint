"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_007_sodium)
Source: BSIP1 run_cereals_006 (TASK-190 clean data).

Purpose: TASK-189 sodium scoring fix (EV-049 / BARI_SODIUM_CEREAL).
  Run this script directly to produce the flag=ON traces.
  For byte-identity proof, run batch_run_cereals_007_sodium_off.py separately.

Outputs:
  run_cereals_007_sodium/products/  — per-product BSIP2 traces with BARI_SODIUM_CEREAL=on
"""

import sys
import json
import pathlib
import logging
import datetime
import os

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, BARI_SODIUM_CEREAL
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_006\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_007_sodium")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
RUN_ID       = "run_cereals_007_sodium"

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
    flag_str = "on" if BARI_SODIUM_CEREAL else "off"
    log.info("=== BSIP2 Cereals — %s (BARI_SODIUM_CEREAL=%s) ===", RUN_ID, flag_str)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    import shutil
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    prod_dir = OUTPUT_ROOT / "products"
    prod_dir.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
        except Exception as e:
            log.error("PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    scores_list = sorted([t.get("final_score_estimate") for t in sufficient])
    median = scores_list[len(scores_list) // 2] if scores_list else None

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": f"proto_v0 / BARI_SODIUM_CEREAL={flag_str}",
        "task": "TASK-189",
        "ev": "EV-049",
        "source": "BSIP1 run_cereals_006 (TASK-190 clean data)",
        "processed": len(traces),
        "scored": len(sufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores_list[0], scores_list[-1]] if scores_list else None,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary: %s", path)
    log.info("Grades=%s median=%s", dist, median)
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
