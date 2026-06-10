"""
BSIP2 — Hard Cheese BARI_REDLABEL_V1 Pilot Run (TASK-REDLABEL-001).

Scores the Yohananof hard-cheese corpus with:
  BARI_REDLABEL_V1=on   — continuous red-label scoring, family-aware cap,
                           graduated sodium/sugar bands, null sat_fat imputation
  BARI_RECAL_P0=on      — P0 recalibration (R1-R7, removes single-label sat_fat cliff)

D7 co-sign (Product Agent): APPROVED 2026-06-08.
Pilot scope: hard_cheese corpus only.

Source: C:\\Bari\\02_products\\hard_cheeses\\bsip1_outputs\\bsip1_hardcheese_*.json
Output: C:\\Bari\\02_products\\hard_cheeses\\bsip2_outputs\\run_hardcheese_redlabel_v1_001\\
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
# Activate flags before any engine import
os.environ["BARI_REDLABEL_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"

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
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hardcheese_redlabel_v1_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\reports")
RUN_ID       = "run_hardcheese_redlabel_v1_001"

ENGINE_TAG   = "BARI_REDLABEL_V1+BARI_RECAL_P0"


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
    log.info("=== BSIP2 Hard Cheese REDLABEL Pilot — %s ===", RUN_ID)
    log.info("    BARI_REDLABEL_V1=%s  BARI_RECAL_P0=%s",
             os.environ.get("BARI_REDLABEL_V1"),
             os.environ.get("BARI_RECAL_P0"))

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

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            log.info("  %-45s  score=%-4s  grade=%s",
                     pid[-45:],
                     trace.get("final_score_estimate"),
                     trace.get("grade_estimate"))
        except Exception as e:
            log.error("PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces if t.get("final_score_estimate") is not None]
    grades = {}
    for t in sufficient:
        g = t.get("grade_estimate"); grades[g] = grades.get(g, 0) + 1
    scores = sorted(t["final_score_estimate"] for t in sufficient)

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "engine_tag": ENGINE_TAG,
        "flags": ["BARI_REDLABEL_V1", "BARI_RECAL_P0"],
        "d7_approved": "2026-06-08",
        "pilot_scope": "hard_cheese",
        "task": "TASK-REDLABEL-001",
        "processed": len(traces),
        "scored": len(sufficient),
        "errors": len(errors),
        "grade_distribution": grades,
        "score_range": {"min": scores[0], "max": scores[-1],
                        "mean": round(sum(scores) / len(scores), 1)} if scores else None,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s  scored=%d  errors=%d  range=[%s, %s]",
             grades, len(sufficient), len(errors),
             scores[0] if scores else "–", scores[-1] if scores else "–")
    return traces, errors


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
