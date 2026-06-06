"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_005)
Source: Shufersal real scrape -> BSIP1 run_cereals_005 (CLEAN corpus, EV-045 applied).
Engine: BARI_RECAL_P0=on + nova_proxy EV-044 quality-gate fix (UNCHANGED from run_004).

Purpose: re-run after the EV-045 corpus-purity fix (TASK-140 contamination, owner 2026-06-05).
  The run_cereals_002/004 corpus contained 13 non-cereals — 10 Israeli ptitim PASTA
  ("פתיתים אפויים [shape]" + organic spelt ptitim) and 3 yeast-leavened breads
  (כוסמין מלא 100% etc.). These are REMOVED at curation (corpus problem, not a scoring
  problem — see contamination_not_calibration_v1). Engine is byte-identical to run_004:
  this run proves the survivors' scores are UNCHANGED and the contaminants are gone.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_005/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_005\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_005")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
RUN_ID       = "run_cereals_005"

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

    # Split summary by granola sub-pool (granola becomes its own category — TASK-140 owner 2026-06-05)
    def subpool(pid):
        gov = (pmap.get(pid, {}).get("cereals_governance") or {}).get("construct_1_granola_subpool") or {}
        return gov.get("subpool")
    granola = [t for t in sufficient if subpool(t.get("canonical_product_id")) == "granola"]
    standard = [t for t in sufficient if subpool(t.get("canonical_product_id")) != "granola"]

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": "proto_v0 / BARI_RECAL_P0=" + recal_flag + " (byte-identical to run_004)",
        "corpus_fix": "EV-045 — 13 non-cereals removed at curation (10 ptitim pasta + 3 yeast bread)",
        "source": "Shufersal real scrape -> BSIP1 run_cereals_005 (clean)",
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
        "vs_run_004": {"processed": 92, "note": "run_004 included 13 contaminants now removed"},
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
