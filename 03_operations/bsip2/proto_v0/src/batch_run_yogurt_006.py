"""
BSIP2 Prototype v0 — Yogurt Batch Runner (run_yogurt_006)
Source: REAL Israeli yogurt SKUs from SHUFERSAL product pages (BSIP1 run_yogurt_005 corpus)
        — same BSIP1 input as run_005; run_006 adds TASK-250 methodology rulings.
Framework: proto_v0 / engine 0.4.0 + BSIP_RECAL_P0_YOGURT_TRIM (TASK-169D).
Purpose: apply TASK-250 rulings to produce run_006 scores + confidence bands.
         Key changes vs run_005:
         - Ruling 1: null sugar_g → confidence −10 (band moves to partial for null-sugar A products)
         - Ruling 2: null fat_saturated_g → confidence −5
         - Ruling 3: grade-before-round implemented in builder (batch runner unchanged)
         - Ruling 4: sweetener detection investigated — FINDING: not applicable (see note below)
         - Ruling 5: barcode 7290116932620 excluded (protein=190 corruption, RT-1)

RULING 4 FINDING (documented here for traceability):
  The three products flagged (7290102395231, 7290114311069, 7290112336712) have
  BSIP1 sweetener_count=1, but the detected sweetener is "דבש" (honey) or "סוכר" (sugar)
  appearing in the nutrition table text that was merged into the ingredient string
  during BSIP1 parsing. Neither honey nor table sugar are non-nutritive sweeteners —
  they are added sugars and are already counted in sugars_g. BSIP2's SWEETENER_TIER_*_HE
  lists contain only non-nutritive sweeteners (stevia, sorbitol, aspartame, etc.).
  The sweetener cap CANNOT and SHOULD NOT fire for these products — they contain no
  non-nutritive sweetener. The BSIP1 sweetener_count vocabulary mismatch is real but
  the correct resolution is: these products have no non-nutritive sweetener, the cap
  does not apply, no vocabulary fix is needed. The three products remain at their
  run_005 scores (80.8/A, 82.7/A, 89.9/A after trim). This finding supersedes the
  Ruling 4 prediction that the cap would fire.

Note: 0 OFF anywhere in this pipeline. Fallback = unknown/partial, never OFF.
Recal: BARI_RECAL_P0=on + BARI_RECAL_P0_YOGURT_TRIM=on (TASK-169D, owner-approved 2026-06-11).
Conf fixes: BARI_TASK250_CONF=on (TASK-250 Rulings 1+2, nutrition-agent ruling 2026-06-11).
Env vars set BEFORE engine module imports so module-level constants pick them up.
"""
import os, sys, json, pathlib, logging, datetime

# TASK-169D recal flags — must be set before importing score_engine (module-level constants).
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"

# TASK-250 — Ruling 1 + 2 confidence reductions (null sugar −10, null satFat −5).
os.environ["BARI_TASK250_CONF"] = "on"

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
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")
RUN_ID       = "run_yogurt_006"

# TASK-250 Ruling 5 + RT-1 (CRITICAL): barcode 7290116932620 has protein_g=190
# (corrupted OCR parse; actual value ~10g). Must be excluded until corrected.
EXCLUDED_BARCODES = {"7290116932620"}


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
    log.info("=== BSIP2 Yogurt — %s (TASK-250 rulings, REAL Shufersal corpus, 0 OFF) ===", RUN_ID)
    log.info("Active flags: RECAL_P0=on, RECAL_P0_YOGURT_TRIM=on, TASK250_CONF=on")
    log.info("Excluded barcodes: %s (RT-1 protein corruption)", EXCLUDED_BARCODES)
    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE); return [], []
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    products_all = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d (before exclusion)", len(products_all))

    # Apply exclusion list
    products = []
    excluded = []
    for p in products_all:
        barcode = str(p.get("barcode") or "")
        pid = p.get("canonical_product_id", "unknown")
        if barcode in EXCLUDED_BARCODES:
            log.warning("  EXCLUDED %s (barcode %s) — RT-1 protein corruption", pid, barcode)
            excluded.append({"product_id": pid, "barcode": barcode, "reason": "RT-1_protein_corruption"})
        else:
            products.append(p)

    log.info("Products to score: %d (excluded: %d)", len(products), len(excluded))

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            log.info("  %-40s score=%-5s grade=%-4s cat=%-14s nova=%s conf=%s/%s",
                     pid, trace.get("final_score_estimate"), trace.get("grade_estimate"),
                     trace.get("category"), trace.get("nova_proxy"),
                     trace.get("confidence_result", {}).get("confidence_score"),
                     trace.get("confidence_result", {}).get("confidence_band"))
        except Exception as e:
            log.error("  PIPELINE ERROR %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})
    log.info("Done. processed=%d excluded=%d errors=%d", len(traces), len(excluded), len(errors))

    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": "Shufersal — real Israeli yogurt SKUs (ingredient-bearing, 2026-06-11)",
        "engine": "proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM (TASK-169D)",
        "task250_rulings": {
            "ruling_1_null_sugar_conf": "−10 (BARI_TASK250_CONF=on)",
            "ruling_2_null_satfat_conf": "−5 (BARI_TASK250_CONF=on)",
            "ruling_3_grade_before_round": "implemented in builder (build_yogurts_frontend_v006.py)",
            "ruling_4_sweetener_detection": (
                "NOT APPLICABLE — three flagged products contain added sugars (honey/table sugar), "
                "not non-nutritive sweeteners; sweetener cap correctly does not fire; "
                "see module docstring for full finding"
            ),
            "ruling_5_ceiling_compression": "barcode 7290116932620 excluded (protein=190 corruption)",
        },
        "off_in_pipeline": False,
        "processed": len(traces),
        "excluded": len(excluded),
        "excluded_list": excluded,
        "errors": len(errors),
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
            "confidence_score": (t.get("confidence_result") or {}).get("confidence_score"),
            "confidence_band": (t.get("confidence_result") or {}).get("confidence_band"),
        } for t in traces],
    }
    (REPORT_ROOT / f"{RUN_ID}_run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info("Summary: %s", REPORT_ROOT / f"{RUN_ID}_run_summary.json")
    return traces, errors


if __name__ == "__main__":
    run_batch()
