"""
BSIP2 Prototype v0 — Yogurt Batch Runner (run_yogurt_006)

Source: Shufersal BSIP0 real Israeli yogurt SKUs re-acquired 2026-06-11.
        BSIP1 run_yogurt_006 — disclaimer-stripped, macros_plausible gated,
        marketing-prose detected, Activia cultures corrected.

TASK-249 corpus remediation pipeline fixes applied in BSIP1:
  RT-2: Shufersal disclaimer strip (67/88 products)
  RT-1: macros_plausible gate — barcode 7290116932620 excluded (protein=190)
  RT-3: Activia Oat Plum excluded (cereal_misroute_excluded)
  RT-5: E414 detection in parenthesized phrases
  RT-12: Activia live-cultures correction
  RT-7: serving_size_g from weight_g
  RT-10: Marketing-prose detection (barcode 7290102395231 → marketing_bleed)

TASK-249 / TASK-250 methodology rulings applied in score_engine:
  Ruling 1: null sugar_g → confidence reduction −10
  Ruling 2: null fat_saturated_g → confidence reduction −5
  Ruling 3: grade-before-round fix applied in build_yogurts_frontend_v006.py
  Ruling 4: sweetener detection gap — for 2/3 RT-10 products resolved by RT-2 strip;
             Bio Natural uses marketing prose (marketing_bleed), trusted signals null.
  Ruling 5: no score change; caveat copy update routes to Content Agent.

Framework: proto_v0 / engine 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D owner-approved).
           BARI_TASK144_FIXES=on (enables macros_plausible gate in score_engine).

0 OFF anywhere in this pipeline. Fallback = unknown/partial, never OFF.
"""
import os
import sys
import json
import pathlib
import logging
import datetime

# TASK-169D recal flags — must be set before importing score_engine (module-level constants).
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
# TASK-144 macros_plausible gate — enables the protein_implausible deduction in score_engine.
os.environ["BARI_TASK144_FIXES"] = "on"

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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_006\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")
RUN_ID       = "run_yogurt_006"


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
    log.info("=== BSIP2 Yogurt — %s (TASK-249 corpus remediation, 0 OFF, "
             "RECAL_P0_YOGURT_TRIM=on, TASK144_FIXES=on) ===", RUN_ID)
    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

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
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat   = trace.get("category")
            nova  = trace.get("nova_proxy")
            suf   = trace.get("data_sufficiency")
            log.info("  %-42s score=%-5s grade=%-20s cat=%-14s nova=%s suf=%s",
                     pid, score, grade, cat, nova, suf)
        except Exception as e:
            log.error("  PIPELINE ERROR %s: %s", pid, e)
            import traceback
            traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Done. processed=%d errors=%d", len(traces), len(errors))

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "Shufersal — real Israeli yogurt SKUs (TASK-249 corpus remediation, 2026-06-11)",
        "engine": "proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D) + TASK144_FIXES",
        "off_in_pipeline": False,
        "task249_fixes_applied": [
            "RT-2: disclaimer strip (67/88 BSIP1 products)",
            "RT-1: macros_plausible gate (BSIP1 excludes barcode 7290116932620)",
            "RT-3: cereal_misroute_excluded (barcode 7290112346797)",
            "RT-5: E414 in parenthesized phrases",
            "RT-12: Activia live-cultures correction",
            "RT-7: serving_size_g from weight_g",
            "RT-10: marketing_bleed detection (barcode 7290102395231)",
        ],
        "task250_rulings_applied": [
            "Ruling 1: null sugar_g → confidence -10",
            "Ruling 2: null fat_saturated_g → confidence -5",
            "Ruling 3: grade-before-round fix in frontend builder",
            "Ruling 4: sweetener gap resolved by RT-2/RT-10 (no vocabulary expansion needed)",
            "Ruling 5: ceiling compression caveat — routes to Content Agent",
        ],
        "processed": len(traces),
        "errors": len(errors),
        "products": [
            {
                "id": t.get("product_id") or t.get("canonical_product_id"),
                "barcode": (t.get("input_reference") or {}).get("barcode"),
                "name": (
                    (t.get("input_reference") or {}).get("canonical_name_he")
                    or (t.get("input_reference") or {}).get("product_name_he")
                ),
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
                "category": t.get("category"),
                "nova": t.get("nova_proxy"),
                "data_sufficiency": t.get("data_sufficiency"),
                "binding_cap": t.get("binding_cap"),
                "confidence_band": (t.get("confidence_result") or {}).get("confidence_band"),
            }
            for t in traces
        ],
    }

    summary_path = REPORT_ROOT / f"{RUN_ID}_run_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    log.info("Summary: %s", summary_path)
    return traces, errors


if __name__ == "__main__":
    run_batch()
