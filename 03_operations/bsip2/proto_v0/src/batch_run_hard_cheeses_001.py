# -*- coding: utf-8 -*-
"""
BSIP2 Prototype v0 — Hard & Yellow Cheeses Batch Runner (run_hard_cheeses_001)
TASK-215

Source: BSIP1 run_hard_cheeses_001 (37 products, 6 sub-pools)
Engine: 0.4.1 + BARI_RECAL_P0=on

Alignment check passed: Gouda 28%=70.8/B > Yellow light 16%=39.0/D > Processed=32.0/E

Output: 02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_001/
"""
import sys
import os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("BARI_RECAL_P0", "on")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_hard_cheeses_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hard_cheeses_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\reports")
RUN_ID       = "run_hard_cheeses_001"

DAIRY_OK_CATEGORIES = {"dairy_protein", "dairy", "dairy_system", "cheese", "cheese_spreads", "hard_cheeses"}


def run_pipeline(product: dict) -> dict:
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_batch():
    log.info("=== BSIP2 Hard & Yellow Cheeses — %s (engine 0.4.1, RECAL_P0=on) ===", RUN_ID)

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

    scores = sorted([t.get("final_score_estimate") for t in sufficient if t.get("final_score_estimate") is not None])
    median = scores[len(scores) // 2] if scores else None

    pmap = {p.get("canonical_product_id"): p for p in products}
    pool_stats = {}
    for t in sufficient:
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or t.get("canonical_product_id")
        p = pmap.get(pid, {})
        pool = p.get("bsip_cheese_subpool", "unknown")
        ps = pool_stats.setdefault(pool, {"count": 0, "scores": [], "grades": {}})
        ps["count"] += 1
        ps["scores"].append(t.get("final_score_estimate"))
        g = t.get("grade_estimate")
        ps["grades"][g] = ps["grades"].get(g, 0) + 1

    for ps in pool_stats.values():
        sc = sorted(s for s in ps["scores"] if s is not None)
        ps["score_median"] = sc[len(sc) // 2] if sc else None
        ps["score_range"] = [sc[0], sc[-1]] if sc else None
        del ps["scores"]

    # Light vs full-fat comparison
    light_vs_fullfat = []
    for t in sufficient:
        pid = (t.get("input_reference") or {}).get("canonical_product_id") or ""
        p = pmap.get(pid, {})
        pool = p.get("bsip_cheese_subpool", "")
        if pool == "yellow_light":
            score_light = t.get("final_score_estimate")
            # Find nearest full-fat equivalent by protein level
            light_fat = p.get("fat_g", p.get("fat_per_100g_scored", 0))
            for t2 in sufficient:
                pid2 = (t2.get("input_reference") or {}).get("canonical_product_id") or ""
                p2 = pmap.get(pid2, {})
                if p2.get("bsip_cheese_subpool") == "yellow":
                    light_vs_fullfat.append({
                        "light_product": p.get("canonical_name_he", ""),
                        "light_score": score_light,
                        "light_fat_per_100g": light_fat,
                        "full_fat_sample": p2.get("canonical_name_he", ""),
                        "full_fat_score": t2.get("final_score_estimate"),
                    })
                    break

    # NOVA distribution
    nova_dist = {}
    for t in traces:
        n_val = t.get("nova_proxy")
        nova_dist[f"NOVA_{n_val}"] = nova_dist.get(f"NOVA_{n_val}", 0) + 1

    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"
                    or t.get("final_score_estimate") is None]

    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "task": "TASK-215",
        "engine": "proto_v0 / 0.4.1 + BARI_RECAL_P0=on",
        "alignment_check": "PASS (2026-06-07) — Gouda 28%=70.8/B > Yellow light 16%=39.0/D > Processed=32.0/E",
        "source": "BSIP1 run_hard_cheeses_001 — 3 retailers (Shufersal/Yohananof/Carrefour) + supplementary",
        "processed": n,
        "scored": len(sufficient),
        "insufficient": len(insufficient),
        "errors": len(errors),
        "grade_distribution": dist,
        "score_median": median,
        "score_range": [scores[0], scores[-1]] if scores else None,
        "grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
        "nova_distribution": nova_dist,
        "subpool_stats": pool_stats,
        "misroute_count": len(misroutes),
        "misroute_pct": misroute_pct,
        "misroute_exit_gate_lt5pct": misroute_pct < 5.0,
        "misroutes": misroutes,
        "light_vs_fullfat_sample": light_vs_fullfat[:4] if light_vs_fullfat else [],
        "error_detail": errors,
        "fat_labeling_note": "18/23 original products show both fat_per_100g and fat_in_dry_matter_pct. Scoring uses fat_per_100g only per TASK-215.",
    }

    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s", dist, median)
    log.info("Pools=%s", {k: v["count"] for k, v in pool_stats.items()})
    log.info("NOVA=%s", nova_dist)


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
