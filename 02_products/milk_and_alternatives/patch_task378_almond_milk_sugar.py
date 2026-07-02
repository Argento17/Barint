"""TASK-378 Phase 4 — Point re-score: almond milk 7290014760141 with sugars_g = 6.0.

Phase-3 Shufersal scrape confirmed: barcode 7290014760141 משקה שקדים has
  - sugars_g = 6.0 g/100ml (from Shufersal label)
  - 'סוכר' is 2nd ingredient (confirmed added sugar source)

Prior BSIP1 record had sugars_g = null (parse miss); engine used sugar=0 → C/51.5.
This script patches sugars_g = 6.0 in-memory and re-runs ONLY this one product.

Expected output: 49.7 / D
  glycemic_quality: 90 - (6.0*2.5) = 75.0
  weighted_delta:  (75.0 - 90.0) * 0.12 = -1.8
  new_weighted:    51.54 - 1.8 = 49.74 → rounded 49.7 → grade D (< 50 C-floor)

All caps, penalties, and floors stay the same (sugar=6.0 < every active threshold).

No other product is touched.
No published files are modified by this script (read-only artifact).
"""

import os
import sys
import json
import pathlib
import datetime
import copy

# Engine flags — identical to run_006_shelfrel_refreeze
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_DAIRY_SAT_FAT_INFER"] = "off"

ROOT = pathlib.Path(r"C:\Bari")
ENGINE_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
sys.path.insert(0, str(ENGINE_SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

BSIP1_SOURCE = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
TARGET_BARCODE = "7290014760141"
SUGARS_G_CORRECTED = 6.0
SUGARS_SOURCE = "Shufersal label Phase-3 verified (TASK-378)"

print(f"=== TASK-378 Phase 4: almond milk sugar correction ===")
print(f"Target barcode: {TARGET_BARCODE}")
print(f"Corrected sugars_g: {SUGARS_G_CORRECTED} (source: {SUGARS_SOURCE})")
print()

# Load all BSIP1 products
products = load_batch(BSIP1_SOURCE)
print(f"BSIP1 products loaded: {len(products)}")

# Find the almond milk product
target = None
for p in products:
    if str(p.get("barcode", "")) == TARGET_BARCODE or \
       str(p.get("canonical_product_id", "")) == f"bsip1_{TARGET_BARCODE}":
        target = copy.deepcopy(p)
        break

if target is None:
    print(f"ERROR: barcode {TARGET_BARCODE} not found in BSIP1 source")
    sys.exit(1)

print(f"Found product: {target.get('canonical_name_he')} ({target.get('canonical_product_id')})")

# Log original sugar value
orig_sugars = target.get("normalized_nutrition_per_100g", {}).get("sugars_g")
print(f"Original sugars_g in BSIP1: {orig_sugars}")

# Patch sugars_g
target["normalized_nutrition_per_100g"]["sugars_g"] = SUGARS_G_CORRECTED
target["_patch_applied"] = {
    "field": "sugars_g",
    "old_value": orig_sugars,
    "new_value": SUGARS_G_CORRECTED,
    "source": SUGARS_SOURCE,
    "task": "TASK-378",
    "applied_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
}

print(f"Patched sugars_g: {target['normalized_nutrition_per_100g']['sugars_g']}")
print()

# Run the full engine pipeline on the patched product
signals     = extract_signals(target)
cat_result  = classify_category(target)
l3          = signals["L3_inferred_classifications"]
nova_result = infer_nova(target, l3)
eval_result = assign_evaluation_scope(target, cat_result["category"])
score_result = score_product(target, signals, cat_result, nova_result, eval_result)
trace       = assemble_trace(target, signals, cat_result, nova_result, eval_result, score_result)
trace["structural_class"] = classify_structural_class(trace)

# Results
new_score = trace.get("final_score_estimate")
new_grade = trace.get("grade_estimate")
weighted  = trace.get("weighted_dimension_score")
gq_score  = trace.get("dimension_scores", {}).get("glycemic_quality")
gq_note   = trace.get("dimension_notes", {}).get("glycemic_quality")
caps      = trace.get("caps_applied", [])
penalties = trace.get("penalties_applied", [])

print("=== RE-SCORE RESULT ===")
print(f"  final_score_estimate : {new_score}")
print(f"  grade_estimate       : {new_grade}")
print(f"  weighted_dimension   : {weighted}")
print(f"  glycemic_quality     : {gq_score}  ({gq_note})")
print(f"  caps_applied         : {caps}")
print(f"  penalties_applied    : {penalties}")
print()

# Verify expected outcome
EXPECTED_SCORE = 49.7
EXPECTED_GRADE = "D"
score_ok = abs((new_score or 0) - EXPECTED_SCORE) < 0.05
grade_ok = new_grade == EXPECTED_GRADE

print("=== VERIFICATION ===")
print(f"  Expected: {EXPECTED_SCORE}/{EXPECTED_GRADE}")
print(f"  Got:      {new_score}/{new_grade}")
print(f"  Score OK: {score_ok}")
print(f"  Grade OK: {grade_ok}")
print(f"  PASS: {score_ok and grade_ok}")

if not (score_ok and grade_ok):
    print(f"\nSTOP: unexpected result {new_score}/{new_grade} (expected {EXPECTED_SCORE}/{EXPECTED_GRADE})")
    print("Per TASK-378 instruction: do not guess, report and halt.")
    sys.exit(1)

# Write result artifact
ARTIFACT = ROOT / "02_products" / "milk_and_alternatives" / "task378_almond_milk_rescore.json"
artifact = {
    "task": "TASK-378",
    "phase": "phase_4_rescore",
    "run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "barcode": TARGET_BARCODE,
    "product_name_he": target.get("canonical_name_he"),
    "patch": {
        "field": "sugars_g",
        "old_value": orig_sugars,
        "new_value": SUGARS_G_CORRECTED,
        "source": SUGARS_SOURCE
    },
    "old_score": 51.5,
    "old_grade": "C",
    "new_score": new_score,
    "new_grade": new_grade,
    "weighted_dimension_score": weighted,
    "glycemic_quality_new": gq_score,
    "glycemic_quality_old": 90.0,
    "glycemic_note": gq_note,
    "caps_applied": caps,
    "penalties_applied": penalties,
    "verification": {
        "expected_score": EXPECTED_SCORE,
        "expected_grade": EXPECTED_GRADE,
        "pass": score_ok and grade_ok
    },
    "engine_flags": {
        "BARI_SHELF_RELATIVE_V1": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_RECAL_P0": "off",
        "BARI_REDLABEL_V1": "off",
        "BARI_DAIRY_SAT_FAT_INFER": "off"
    },
    "off_used": False,
    "other_products_changed": 0,
    "note": "Single-product point correction only. No other milk products re-scored."
}

ARTIFACT.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nArtifact written: {ARTIFACT}")
print("=== DONE ===")
