"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_002)
Source: Shufersal real scrape -> BSIP1 run_cereals_002 (with 4 governance constructs).
Engine: 0.4.0 UNMODIFIED — no score tuning, no manual edits (run_yogurt_003 discipline).
Purpose: score the real cereal corpus, measure routing accuracy (misroute <5% exit gate),
         and reconcile the BSIP1 granola sub-pool proxy against real NOVA.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_002/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_002\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_002")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
CATEGORY_TAG = "breakfast_cereals"
RUN_ID       = "run_cereals_002"

# Routing families considered CORRECT for a breakfast cereal.
# 'cereal' is the canonical route; granola legitimately may route to snack_bar_granola.
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
    log.info("=== BSIP2 Breakfast Cereals — %s (engine 0.4.0 unmodified) ===", RUN_ID)
    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_ROOT / "products"
    # Clear stale traces from prior runs so removed/curated-out products don't linger.
    if prod_dir.exists():
        import shutil
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces, errors, misroutes = [], [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            cat = trace.get("category")
            if cat not in CEREAL_OK_CATEGORIES:
                ref = trace.get("input_reference") or {}
                misroutes.append({
                    "pid": pid,
                    "name": ref.get("product_name_he") or ref.get("canonical_name_he") or "",
                    "routed_to": cat,
                })
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Processed: %d, Errors: %d, Misroutes: %d", len(traces), len(errors), len(misroutes))
    _write_summary(traces, errors, misroutes, products)
    return traces, errors


def _write_summary(traces, errors, misroutes, products):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    n = len(traces)
    misroute_pct = round(100.0 * len(misroutes) / max(n, 1), 1)

    # grade distribution
    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    scores = sorted([t.get("final_score_estimate") for t in sufficient])
    median = scores[len(scores)//2] if scores else None

    # NOVA reconciliation of the BSIP1 granola sub-pool proxy
    pmap = {p.get("canonical_product_id"): p for p in products}
    recon = []
    for t in sufficient:
        pid = t.get("canonical_product_id")
        p = pmap.get(pid, {})
        gov = (p.get("cereals_governance") or {}).get("construct_1_granola_subpool") or {}
        subpool = gov.get("subpool")
        nova = t.get("nova_proxy")
        if subpool == "granola":
            recon.append({"pid": pid, "subpool": subpool, "nova": nova,
                          "nova_confirms": (nova is not None and nova >= 3)})

    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"
                    or t.get("final_score_estimate") is None]

    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / 0.4.0 (unmodified)",
        "source": "Shufersal real scrape -> BSIP1 run_cereals_002",
        "processed": n,
        "scored": len(sufficient),
        "insufficient": len(insufficient),
        "insufficient_pct_of_displayable": round(100.0 * len(insufficient) / max(n, 1), 1),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "misroute_count": len(misroutes),
        "misroute_pct": misroute_pct,
        "misroute_exit_gate_lt5pct": misroute_pct < 5.0,
        "misroutes": misroutes,
        "granola_subpool_nova_reconciliation": recon,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s misroute=%.1f%% (gate<5%%=%s) insufficient=%d",
             dist, median, misroute_pct, misroute_pct < 5.0, len(insufficient))


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
