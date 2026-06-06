"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_004)
Source: Shufersal real scrape -> BSIP1 run_cereals_002 (unchanged — no new scrape).
Engine: BARI_RECAL_P0=on + nova_proxy EV-044 quality-gate fix.
Purpose: Final clean run. Two fixes applied vs run_cereals_002:
         (1) router_v2.py category prior fix (CATEGORY_PRIOR_BOOST=2.0) — clears QA-CER-001 misroute gate.
         (2) nova_proxy.py EV-044 quality-gate — suppresses false NOVA 1 on bsip1_text_fallback
             ingredient data; 4 shaped baked-flake products (פתיתים אפויים) drop from NOVA 1/A
             to their correct NOVA 2+ / lower grade per Nutrition Agent ruling 2026-06-05.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_004/
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
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_004")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
CATEGORY_TAG = "breakfast_cereals"
RUN_ID       = "run_cereals_004"

CEREAL_OK_CATEGORIES = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}

SHAPED_BAKED_FLAKE_NAMES = {
    "פתיתים אפויים קוסקוס",
    "פתיתים אפויים כוכבים",
    "פתיתים אפויים טבעות",
    "פתיתים אפויים אורז",
}

APPROVED_A_PRODUCTS = {
    "שיבולת שועל עבה",
    "קוואקר שיבולת שועל",
}


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
        log.warning("BARI_RECAL_P0 is NOT set to 'on'. Run with BARI_RECAL_P0=on for live-category consistency.")

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
    shaped_flake_results = []
    a_grade_results = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            cat   = trace.get("category")
            ref   = trace.get("input_reference") or {}
            name  = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            nova  = trace.get("nova_proxy")

            if cat not in CEREAL_OK_CATEGORIES:
                misroutes.append({"pid": pid, "name": name, "routed_to": cat})

            for sbf in SHAPED_BAKED_FLAKE_NAMES:
                if sbf in name or name in sbf:
                    shaped_flake_results.append({"pid": pid, "name": name, "score": score,
                                                 "grade": grade, "nova": nova,
                                                 "nova_confidence": trace.get("nova_confidence")})

            if grade == "A" or (score is not None and score >= 80):
                approved = any(ap in name for ap in APPROVED_A_PRODUCTS)
                a_grade_results.append({"pid": pid, "name": name, "score": score,
                                        "grade": grade, "nova": nova,
                                        "nutrition_approved": approved})

        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Processed: %d, Errors: %d, Misroutes: %d", len(traces), len(errors), len(misroutes))
    _write_summary(traces, errors, misroutes, products,
                   shaped_flake_results, a_grade_results, recal_flag)
    return traces, errors


def _write_summary(traces, errors, misroutes, products,
                   shaped_flake_results, a_grade_results, recal_flag):
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
    median = scores[len(scores) // 2] if scores else None

    pmap = {p.get("canonical_product_id"): p for p in products}
    recon = []
    for t in sufficient:
        pid = t.get("canonical_product_id")
        p   = pmap.get(pid, {})
        gov = (p.get("cereals_governance") or {}).get("construct_1_granola_subpool") or {}
        subpool = gov.get("subpool")
        nova = t.get("nova_proxy")
        if subpool == "granola":
            recon.append({"pid": pid, "subpool": subpool, "nova": nova,
                          "nova_confirms": (nova is not None and nova >= 3)})

    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"
                    or t.get("final_score_estimate") is None]

    ref_002 = {"A": 7, "B": 10, "C": 48, "D": 25, "E": 2}
    grade_diff = {}
    for g in sorted(set(list(ref_002.keys()) + list(dist.keys()))):
        before, after = ref_002.get(g, 0), dist.get(g, 0)
        if before != after:
            grade_diff[g] = {"run_002": before, "run_004": after, "delta": after - before}

    a_unapproved = [r for r in a_grade_results if not r.get("nutrition_approved")]

    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / BARI_RECAL_P0=" + recal_flag,
        "nova_proxy_fix": "EV-044 quality-gate applied (bsip1_text_fallback NOVA 1 fast-path suppressed)",
        "source": "Shufersal real scrape -> BSIP1 run_cereals_002 (unchanged)",
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
        "qa_cer_001_gate": "PASS" if misroute_pct < 5.0 else "FAIL",
        "misroutes": misroutes,
        "shaped_baked_flake_scores_post_ev044": shaped_flake_results,
        "a_grade_results": a_grade_results,
        "a_grade_unapproved": a_unapproved,
        "grade_diff_vs_run_cereals_002": grade_diff,
        "ref_run_cereals_002": {"grade_distribution": ref_002, "score_median": 58.3,
                                "misroute_count": 7, "misroute_pct": 7.6},
        "granola_subpool_nova_reconciliation": recon,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s misroute=%.1f%% gate=%s insufficient=%d",
             dist, median, misroute_pct,
             "PASS" if misroute_pct < 5.0 else "FAIL", len(insufficient))
    if shaped_flake_results:
        log.info("Shaped baked-flake post-EV044 scores: %s", shaped_flake_results)
    if a_unapproved:
        log.warning("A-grade products NOT yet Nutrition-approved: %s", a_unapproved)


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
