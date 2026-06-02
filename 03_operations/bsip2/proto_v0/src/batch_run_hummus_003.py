"""
BSIP2 Prototype v0 — Hummus Batch Runner (run_hummus_003).

TASK-169B (P1 promotion). Same corpus as the frozen run_hummus_002 baseline
(C:\\Bari\\02_products\\hummus\\canonical_bsip1, 69 products), scored with
BARI_RECAL_P0=ON (owner-approved P0 recalibration: R1 category-relative protein,
R3 leanness, R5 graded sat-fat, R6 veg-spread fit + R4/R7 NOVA/culture for any
dairy-routed items — hummus is sauce_spread, so R1/R3/R5/R6 dominate).

run_hummus_002 is FROZEN (AUTHORITATIVE.md): future re-runs MUST be run_hummus_003+.
This writes a NEW run dir — it does NOT overwrite run_hummus_002.
Output: 02_products/hummus/intelligence_bsip2/run_hummus_003/
"""
import os
os.environ.setdefault("BARI_RECAL_P0", "on")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

import sys
import json
import pathlib
import logging
import datetime
import statistics

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hummus\intelligence_bsip2\run_hummus_003")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hummus\reports")
RUN_ID       = "run_hummus_003"


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    trace["run_id"] = RUN_ID
    return trace


def run_batch():
    log.info("=== BSIP2 Hummus — %s (engine 0.4.1, BARI_RECAL_P0=%s) ===",
             RUN_ID, os.environ.get("BARI_RECAL_P0"))
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
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(traces, errors)
    return traces, errors


def _write_summary(traces, errors):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    scores = sorted([t["final_score_estimate"] for t in sufficient])
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    cat_counts = {}
    for t in traces:
        c = str(t.get("category"))
        cat_counts[c] = cat_counts.get(c, 0) + 1
    veg = sum(1 for t in traces if t.get("recal_p0_veg_spread"))
    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / 0.4.1 + BARI_RECAL_P0=on (TASK-169B)",
        "recal_p0": os.environ.get("BARI_RECAL_P0"),
        "source": "Shufersal canonical_bsip1 (same corpus as frozen run_hummus_002)",
        "governance": "TASK-169 P0 recalibration (R1/R3/R5/R6 + EV-030/031/032/033)",
        "processed": len(traces),
        "scored": len(sufficient),
        "insufficient": len(traces) - len(sufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_statistics": {
            "count": len(scores),
            "min": scores[0] if scores else None,
            "max": scores[-1] if scores else None,
            "mean": round(statistics.mean(scores), 2) if scores else None,
            "median": round(statistics.median(scores), 2) if scores else None,
        },
        "category_routing": cat_counts,
        "veg_spread_archetype_count": veg,
        "grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s veg_spread=%d insufficient=%d",
             dist, summary["score_statistics"]["median"], veg, summary["insufficient"])


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
