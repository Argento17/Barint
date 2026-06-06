"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_003)
Source: Shufersal real scrape -> BSIP1 run_cereals_002 (unchanged — no new scrape).
Engine: BARI_RECAL_P0=on (TASK-169 live scoring consistent with all live categories)
Purpose: Re-run after category prior fix in router_v2.py.
         QA-CER-001 gate: misroute <5% (was 7.6% / 7 products in run_cereals_002).
         The category prior (CATEGORY_PRIOR_BOOST=2.0) applied in router Stage 2c
         is expected to correctly route the 7 previously misrouted cereal products.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_003/
"""
# Engine: BARI_RECAL_P0=on (TASK-169 live scoring consistent with all live categories)

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
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_003")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
CATEGORY_TAG = "breakfast_cereals"
RUN_ID       = "run_cereals_003"

# Routing families considered CORRECT for a breakfast cereal.
# 'cereal' is the canonical route; granola legitimately may route to snack_bar_granola.
CEREAL_OK_CATEGORIES = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}

# The 7 products that misrouted in run_cereals_002 — track individually in this run.
PREV_MISROUTE_NAMES = {
    "כוסמין מלא 100%",
    "פתיתים אורגנים כוסמין",
    "מוזלי",
    "דגני טבעות תירס ואורז",
    "כריות נוגט",
}

# Shaped baked-flake products flagged for Nutrition sign-off (A-ceiling concern).
SHAPED_BAKED_FLAKE_NAMES = {
    "פתיתים אפויים קוסקוס",
    "פתיתים אפויים כוכבים",
    "פתיתים אפויים טבעות",
    "פתיתים אפויים אורז",
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
        log.warning("BARI_RECAL_P0 is NOT set to 'on'. "
                    "This run should be executed with BARI_RECAL_P0=on for consistency with live categories.")

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
    prev_misroute_resolved = []
    shaped_baked_flake_results = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            cat = trace.get("category")
            ref = trace.get("input_reference") or {}
            name = ref.get("product_name_he") or ref.get("canonical_name_he") or ""

            if cat not in CEREAL_OK_CATEGORIES:
                misroutes.append({
                    "pid": pid,
                    "name": name,
                    "routed_to": cat,
                })

            # Track resolution of previously misrouted products
            for prev_name in PREV_MISROUTE_NAMES:
                if prev_name in name:
                    prev_misroute_resolved.append({
                        "pid": pid,
                        "name": name,
                        "routed_to": cat,
                        "now_correct": cat in CEREAL_OK_CATEGORIES,
                    })

            # Track shaped baked-flake products for Nutrition sign-off
            for sbf_name in SHAPED_BAKED_FLAKE_NAMES:
                if sbf_name in name or name in sbf_name:
                    shaped_baked_flake_results.append({
                        "pid": pid,
                        "name": name,
                        "routed_to": cat,
                        "score": trace.get("final_score_estimate"),
                        "grade": trace.get("grade_estimate"),
                        "nova": trace.get("nova_proxy"),
                    })

        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Processed: %d, Errors: %d, Misroutes: %d", len(traces), len(errors), len(misroutes))
    _write_summary(traces, errors, misroutes, products,
                   prev_misroute_resolved, shaped_baked_flake_results, recal_flag)
    return traces, errors


def _write_summary(traces, errors, misroutes, products,
                   prev_misroute_resolved, shaped_baked_flake_results, recal_flag):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    n = len(traces)
    misroute_pct = round(100.0 * len(misroutes) / max(n, 1), 1)

    # Grade distribution
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

    # Diff vs run_cereals_002 reference distribution (A7/B10/C48/D25/E2, median 58.3)
    ref_002 = {"A": 7, "B": 10, "C": 48, "D": 25, "E": 2}
    grade_diff = {}
    all_grades = set(list(ref_002.keys()) + list(dist.keys()))
    for g in sorted(all_grades):
        before = ref_002.get(g, 0)
        after  = dist.get(g, 0)
        if before != after:
            grade_diff[g] = {"run_002": before, "run_003": after, "delta": after - before}

    summary = {
        "run_id": RUN_ID,
        "generated": run_dt,
        "engine": "proto_v0 / BARI_RECAL_P0=" + recal_flag,
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
        "prev_misroute_resolution": prev_misroute_resolved,
        "shaped_baked_flake_scores": shaped_baked_flake_results,
        "grade_diff_vs_run_cereals_002": grade_diff,
        "ref_run_cereals_002": {
            "grade_distribution": ref_002,
            "score_median": 58.3,
            "misroute_count": 7,
            "misroute_pct": 7.6,
        },
        "granola_subpool_nova_reconciliation": recon,
        "error_detail": errors,
    }
    path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", path)
    log.info("Grades=%s median=%s misroute=%.1f%% (gate<5%%=%s) QA-CER-001=%s insufficient=%d",
             dist, median, misroute_pct, misroute_pct < 5.0,
             "PASS" if misroute_pct < 5.0 else "FAIL",
             len(insufficient))
    log.info("Grade diff vs run_cereals_002: %s", grade_diff)
    if shaped_baked_flake_results:
        log.info("Shaped baked-flake scores (Nutrition sign-off): %s", shaped_baked_flake_results)
    if prev_misroute_resolved:
        log.info("Previously misrouted products resolution: %s", prev_misroute_resolved)


if __name__ == "__main__":
    run_batch()
    log.info("Done.")
