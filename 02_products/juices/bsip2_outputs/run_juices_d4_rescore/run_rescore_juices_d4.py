"""
run_rescore_juices_d4.py — Juices D4 scoring activation (BARI_D4_SCORE_V1=on).

PURPOSE: Re-score the juices corpus with BARI_D4_SCORE_V1=on added to the
existing config flag vector. All other flags held exactly as in the live juices config.
Output writes new BSIP2 trace files to run_juices_d4_rescore/products/.

Flags applied (live juices flags + D4=on):
  BARI_SHELF_RELATIVE_V1=on
  BARI_FAT_TECH_V1=on
  BARI_RECAL_P0=on
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_GRAD_SODIUM_V1=off
  BARI_TASK144_FIXES=off
  BARI_D4_SCORE_V1=on    <- NEW

Modelled on batch_run_juices_yohananof_002.py (same API pattern).
Hard rules:
  - OFF=0: no Open Food Facts data
  - No consumer copy authored
  - No deploy/commit
  - Traces written here; generate_page called separately
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import logging
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[4]   # C:\Bari
RUN_DIR = Path(__file__).resolve().parent     # run_juices_d4_rescore/
PRODUCTS_DIR = RUN_DIR / "products"
SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
BSIP1_DIR = REPO / "02_products" / "juices" / "bsip1_outputs"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Flag vector — set BEFORE importing engine modules
# ---------------------------------------------------------------------------
JUICES_D4_FLAGS = {
    "BARI_SHELF_RELATIVE_V1":          "on",
    "BARI_FAT_TECH_V1":                "on",
    "BARI_RECAL_P0":                   "on",
    "BARI_SODIUM_SHELF_RELATIVE_V1":   "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1":  "off",
    "BARI_REDLABEL_V1":                "off",
    "BARI_SODIUM_CEREAL":              "off",
    "BARI_GRAD_SODIUM_V1":             "off",
    "BARI_TASK144_FIXES":              "off",
    "BARI_D4_SCORE_V1":                "on",     # activation
    # Ensure glass box W2 is on (required for detect_additives_d4 to run)
    "BARI_GLASSBOX_W2":                "on",
}

# Apply flags BEFORE imports (engine reads os.environ at module level)
for k, v in JUICES_D4_FLAGS.items():
    os.environ[k] = v

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))

# ── Engine imports AFTER flag setting ────────────────────────────────────────
from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, BARI_D4_SCORE_V1, set_shelf_stats
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# Scope-excluded product IDs (from batch_run_juices_yohananof_002.py)
EXCLUDED_PIDS = {
    "bsip1_juice_7290013608680",   # tomato juice
    "bsip1_juice_5411188115434",   # soy drink
    "bsip1_juice_7290110558420",   # oat drink
    "bsip1_juice_7290110325893",   # coffee-milk drink
}


def run_pipeline(product: dict) -> dict:
    """Identical call pattern to batch_run_juices_yohananof_002.py."""
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    try:
        trace["structural_class"] = classify_structural_class(trace)
    except Exception:
        trace["structural_class"] = None
    return trace


def main() -> int:
    print("=" * 72)
    print("Juices D4 Rescore — BARI_D4_SCORE_V1=on activation")
    print(f"BARI_D4_SCORE_V1 engine flag: {BARI_D4_SCORE_V1}")
    print("=" * 72)

    if not BARI_D4_SCORE_V1:
        print("FAIL: D4 flag not ON — module cached with old value; restart interpreter")
        return 1

    PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Load BSIP1 corpus ─────────────────────────────────────────────────────
    log.info("Loading BSIP1 corpus from: %s", BSIP1_DIR)
    all_products = load_batch(BSIP1_DIR)
    log.info("Products loaded (before exclusion): %d", len(all_products))

    products = [
        p for p in all_products
        if p.get("canonical_product_id") not in EXCLUDED_PIDS
    ]
    skipped = [p.get("canonical_product_id") for p in all_products
               if p.get("canonical_product_id") in EXCLUDED_PIDS]
    log.info("Products after exclusion: %d  (excluded: %s)", len(products), skipped)

    # ── Set shelf stats for juice×sugar (from constants.py EV-091 / juices.json) ──
    # Must be set BEFORE scoring (scored by set_shelf_stats global in score_engine)
    set_shelf_stats(
        nutrient="sugars_g",
        median=9.50,
        scale=2.82,
        scale_type="iqr",
    )
    log.info("Shelf stats set: sugars_g median=9.50 scale=2.82 (EV-091, juices.json live values)")

    # ── Score each product ────────────────────────────────────────────────────
    traces, errors = [], []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        barcode = str(product.get("barcode", "") or "")
        try:
            trace = run_pipeline(product)
            write_trace(trace, RUN_DIR)
            traces.append(trace)

            final_score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate") or score_to_grade(final_score)
            d4_pen = trace.get("d4_score_penalty") or 0

            print(f"  OK  {barcode:16s}  score={str(final_score):6s}  grade={grade}  d4_penalty={d4_pen}  pid={pid}")
        except Exception as e:
            import traceback
            log.error("PIPELINE ERROR for %s: %s", pid, e)
            traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print(f"Scored: {len(traces)} products, {len(errors)} errors")
    movers = [t for t in traces if (t.get("d4_score_penalty") or 0) > 0]
    print(f"D4 movers (penalty > 0): {len(movers)}")
    for t in movers:
        bc = t.get("input_reference", {}).get("barcode", "")
        print(f"  BC={bc:16s}  score={t.get('final_score_estimate')}  d4_penalty={t.get('d4_score_penalty')}")

    summary = {
        "run_id": "run_juices_d4_rescore",
        "run_ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "flags": JUICES_D4_FLAGS,
        "products_scored": len(traces),
        "errors": len(errors),
        "d4_movers": len(movers),
        "error_list": errors,
    }
    out_summary = RUN_DIR / "run_summary.json"
    out_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Summary written to: {out_summary}")
    print("=" * 72)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
