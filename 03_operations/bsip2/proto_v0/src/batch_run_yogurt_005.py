"""
BSIP2 Prototype v0 — Yogurt Batch Runner (run_yogurt_005)
Source: REAL Israeli yogurt SKUs from SHUFERSAL product pages (BSIP0 run_yogurt_005, 2026-06-11)
        — WITH ingredient panels + Hebrew names + nutrition. Full re-acquisition per owner Option A.
Framework: proto_v0 / engine 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D owner-approved).
Purpose: produce reproducible machine scores on a full ingredient-bearing yogurt corpus.
         Replaces the thin 11-product yogurts_frontend_v3.json (0 ingredient coverage).
Output: 02_products/yogurt_system/bsip2_outputs/run_yogurt_005/
Note: 0 OFF anywhere in this pipeline. Fallback = unknown/partial, never OFF.
Recal: BARI_RECAL_P0=on + BARI_RECAL_P0_YOGURT_TRIM=on (TASK-169D, owner-approved 2026-06-11).
       +8 for qualifying high-quality yogurts; hard ceiling at 89.9 (no S grade).
       Env vars set BEFORE engine module imports so module-level constants pick them up.
"""
import os, sys, json, pathlib, logging, datetime

# TASK-169D recal flags — must be set before importing score_engine (module-level constants).
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_005\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_005")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")
RUN_ID       = "run_yogurt_005"


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
    log.info("=== BSIP2 Yogurt — %s (REAL Shufersal corpus, ingredient-bearing, 0 OFF, RECAL_P0_YOGURT_TRIM=on) ===", RUN_ID)
    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE); return [], []
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))
    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            log.info("  %-40s score=%-5s grade=%-4s cat=%-14s nova=%s suf=%s",
                     pid, trace.get("final_score_estimate"), trace.get("grade_estimate"),
                     trace.get("category"), trace.get("nova_proxy"),
                     trace.get("data_sufficiency"))
        except Exception as e:
            log.error("  PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})
    log.info("Done. processed=%d errors=%d", len(traces), len(errors))

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "Shufersal — real Israeli yogurt SKUs (ingredient-bearing, 2026-06-11)",
        "engine": "proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D)",
        "off_in_pipeline": False,
        "processed": len(traces), "errors": len(errors),
        "products": [{
            "id": t.get("product_id") or t.get("canonical_product_id"),
            "barcode": (t.get("input_reference") or {}).get("barcode"),
            "name": (t.get("input_reference") or {}).get("product_name_he")
                     or (t.get("input_reference") or {}).get("canonical_name_he"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "category": t.get("category"),
            "nova": t.get("nova_proxy"),
            "data_sufficiency": t.get("data_sufficiency"),
            "binding_cap": t.get("binding_cap"),
        } for t in traces],
    }
    (REPORT_ROOT / f"{RUN_ID}_run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("Summary: %s", REPORT_ROOT / f"{RUN_ID}_run_summary.json")
    return traces, errors


if __name__ == "__main__":
    run_batch()
