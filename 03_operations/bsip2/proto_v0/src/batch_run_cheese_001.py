"""
BSIP2 Prototype v0 — Cottage / White Cheese Batch Runner (run_cheese_001)
Source: Shufersal real scrape -> BSIP1 run_cheese_001 (4 sub-pools + cheese governance constructs).
Engine: 0.4.0 UNMODIFIED — no score tuning, no manual edits, no router changes
        (run_cereals_002 / run_yogurt_003 discipline; CLAUDE.md "do not redesign scoring").
Purpose: score the real cheese corpus on the calibrated dairy engine, measure routing accuracy
         (misroute <5% exit gate), and surface A-ceiling outcomes for Nutrition review.
Output: 02_products/cheese_spreads/bsip2_outputs/run_cheese_001/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\reports")
CATEGORY_TAG = "cheese_spreads"
RUN_ID       = "run_cheese_001"

# Routing families considered CORRECT for a fresh white cheese / spread.
# 'dairy_protein' is the canonical dairy route (cottage anchor + is_plain_dairy cap relief, R-04).
# Other dairy buckets the engine may emit are accepted as in-family.
DAIRY_OK_CATEGORIES = {"dairy_protein", "dairy", "dairy_system", "cheese", "cheese_spreads"}


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
    log.info("=== BSIP2 Cottage/White Cheese — %s (engine 0.4.0 unmodified) ===", RUN_ID)
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
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            cat = trace.get("category")
            if cat not in DAIRY_OK_CATEGORIES:
                ref = trace.get("input_reference") or {}
                misroutes.append({
                    "pid": pid,
                    "name": ref.get("product_name_he") or ref.get("canonical_name_he") or "",
                    "subpool": product.get("bsip_cheese_subpool"),
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

    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    scores = sorted([t.get("final_score_estimate") for t in sufficient])
    median = scores[len(scores)//2] if scores else None

    # Per-sub-pool grade + score rollup
    pmap = {p.get("canonical_product_id"): p for p in products}
    pool_stats = {}
    a_ceiling_landed = []
    for t in sufficient:
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id")
        p = pmap.get(pid, {})
        pool = p.get("bsip_cheese_subpool", "unknown")
        ps = pool_stats.setdefault(pool, {"count": 0, "scores": [], "grades": {}})
        ps["count"] += 1
        ps["scores"].append(t.get("final_score_estimate"))
        g = t.get("grade_estimate")
        ps["grades"][g] = ps["grades"].get(g, 0) + 1
        # A-ceiling cross-check: any product landing grade A and its pre-routing A-eligibility
        if g == "A":
            ac = (p.get("cheese_governance") or {}).get("construct_5_a_ceiling") or {}
            a_ceiling_landed.append({
                "pid": pid, "name": p.get("canonical_name_he", ""), "pool": pool,
                "score": t.get("final_score_estimate"), "routed_to": t.get("category"),
                "a_eligible_pre_routing": ac.get("a_eligible_pre_routing"),
                "a_ceiling_fails": ac.get("fails"),
            })
    for ps in pool_stats.values():
        sc = sorted(s for s in ps["scores"] if s is not None)
        ps["score_median"] = sc[len(sc)//2] if sc else None
        ps["score_range"] = [sc[0], sc[-1]] if sc else None
        del ps["scores"]

    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"
                    or t.get("final_score_estimate") is None]

    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / 0.4.0 (unmodified)",
        "source": "Shufersal real scrape -> BSIP1 run_cheese_001",
        "governance": "cheese_spreads_stress_test_001 (TASK-141, verdict B); dairy calibration TASK-139A/B/D",
        "processed": n,
        "scored": len(sufficient),
        "insufficient": len(insufficient),
        "insufficient_pct_of_displayable": round(100.0 * len(insufficient) / max(n, 1), 1),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
        "subpool_stats": pool_stats,
        "a_ceiling_grade_A_landed": a_ceiling_landed,
        "misroute_count": len(misroutes),
        "misroute_pct": misroute_pct,
        "misroute_exit_gate_lt5pct": misroute_pct < 5.0,
        "misroutes": misroutes,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s misroute=%.1f%% (gate<5%%=%s) insufficient=%d",
             dist, median, misroute_pct, misroute_pct < 5.0, len(insufficient))
    log.info("Pools=%s", {k: v["count"] for k, v in pool_stats.items()})


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
