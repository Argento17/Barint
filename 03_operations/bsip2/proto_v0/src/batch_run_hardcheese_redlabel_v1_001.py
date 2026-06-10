# -*- coding: utf-8 -*-
"""
BSIP2 Prototype v0 — Hard & Yellow Cheeses Batch Runner (run_hardcheese_redlabel_v1_001)
TASK-REDLABEL-001 — NOVA mismatch fix + BARI_REDLABEL_V1 + BARI_RECAL_P0.

Fixes applied vs run_hard_cheeses_yohananof_001:
  - BSIP2-HC-002: short-ingredient dairy NOVA 1 rule (fixes engine NOVA 2 vs BSIP1 NOVA 1)
  - R4 natural-colorant exclusion: beta-carotene/annatto no longer block NOVA 3→2 demotion
  - BSIP2-HC-001 sub-rule B: phosphate emulsifying salts → NOVA 4 (fixes engine NOVA 3
    for processed cheeses with E339/E450/E451)
  - BARI_REDLABEL_V1=on: continuous red-label scoring, graduated sodium bands, DD-6 null
    sat_fat imputation (eliminates cliff effects from TASK-REDLABEL-001)

Source: BSIP1 bsip1_outputs/ (same corpus as run_hard_cheeses_yohananof_001)
Output: 02_products/hard_cheeses/bsip2_outputs/run_hardcheese_redlabel_v1_001/
"""
import sys
import os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_REDLABEL_V1"] = "on"
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "on"

import json
import pathlib
import logging
import datetime

SRC = pathlib.Path(__file__).parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_outputs")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hardcheese_redlabel_v1_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\reports")
RUN_ID       = "run_hardcheese_redlabel_v1_001"

DAIRY_OK_CATEGORIES = {
    "dairy_protein", "dairy", "dairy_system", "cheese", "cheese_spreads", "hard_cheeses"
}


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    try:
        trace["structural_class"] = classify_structural_class(trace)
    except Exception:
        trace["structural_class"] = None
    return trace


def run_batch():
    log.info("=== BSIP2 Hard Cheeses — %s ===", RUN_ID)
    log.info("Engine flags: BARI_RECAL_P0=on BARI_REDLABEL_V1=on BARI_DAIRY_SAT_FAT_INFER=on")
    log.info("NOVA fixes: BSIP2-HC-002 (short-dairy NOVA1), R4 natural-colorant, HC-001B (phosphate)")

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
    sufficient = [t for t in traces if t.get("final_score_estimate") is not None]
    n = len(traces)

    dist = {}
    for t in sufficient:
        g = t.get("grade_estimate")
        dist[g] = dist.get(g, 0) + 1
    scores = sorted([t["final_score_estimate"] for t in sufficient if t.get("final_score_estimate") is not None])
    median = scores[len(scores) // 2] if scores else None

    pmap = {p.get("canonical_product_id"): p for p in products}
    subpool_stats = {}

    for t in sufficient:
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id")
        p = pmap.get(pid, {})
        pool = p.get("bsip_cheese_subpool", "unknown")
        ps = subpool_stats.setdefault(pool, {"count": 0, "scores": [], "grades": {}})
        ps["count"] += 1
        ps["scores"].append(t.get("final_score_estimate"))
        g = t.get("grade_estimate")
        ps["grades"][g] = ps["grades"].get(g, 0) + 1

    for ps in subpool_stats.values():
        sc = sorted(s for s in ps["scores"] if s is not None)
        ps["score_median"] = sc[len(sc) // 2] if sc else None
        ps["score_range"] = [sc[0], sc[-1]] if sc else None
        del ps["scores"]

    nova_dist = {}
    for t in traces:
        n_val = t.get("nova_proxy")
        nova_dist[f"NOVA_{n_val}"] = nova_dist.get(f"NOVA_{n_val}", 0) + 1

    misroute_pct = round(100.0 * len(misroutes) / max(n, 1), 1)
    graded = [t for t in sufficient if t.get("grade_estimate") not in (None, "insufficient_data")]

    summary = {
        "run_id":           RUN_ID,
        "generated":        run_dt,
        "task":             "TASK-REDLABEL-001",
        "engine":           "proto_v0 / 0.4.1 + BARI_RECAL_P0=on + BARI_REDLABEL_V1=on",
        "nova_fixes":       [
            "BSIP2-HC-002: short-ingredient dairy NOVA 1 rule (≤6 ings, no industrial additives)",
            "R4 natural-colorant exclusion: annatto/beta-carotene no longer block NOVA 3→2 demotion",
            "BSIP2-HC-001 sub-rule B: phosphate emulsifying salts (E339/E450/E451) → NOVA 4",
        ],
        "source":           "BSIP1 bsip1_outputs/ (67 products)",
        "processed":        n,
        "scored_with_grade": len(graded),
        "insufficient_data": len([t for t in traces if t.get("grade_estimate") in (None, "insufficient_data")]),
        "errors":           len(errors),
        "grade_distribution": dist,
        "score_median":     median,
        "score_range":      [scores[0], scores[-1]] if scores else None,
        "grade_thresholds": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
        "nova_distribution": nova_dist,
        "subpool_stats":    subpool_stats,
        "misroute_count":   len(misroutes),
        "misroute_pct":     misroute_pct,
        "misroutes":        misroutes,
        "error_detail":     errors,
    }
    path = OUTPUT_ROOT / "run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)

    scores_list = [
        {
            "pid":   (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id"),
            "name":  (t.get("input_reference") or {}).get("canonical_name_he") or "",
            "nova":  t.get("nova_proxy"),
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "status": t.get("evaluation_status"),
        }
        for t in traces
    ]
    scores_list.sort(key=lambda x: (x["score"] or 0), reverse=True)
    log.info("Scores (top→bottom):")
    for s in scores_list[:30]:
        log.info("  NOVA%s %s/%-2s  %s  (%s)", s["nova"], s["score"], s["grade"], s["name"][:45], s["status"])
    log.info("Grades=%s  median=%s  NOVA=%s", dist, median, nova_dist)


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
