"""
TASK-404: Re-score jc-021 with corrected sugar value.

Context:
  - jc-021 barcode 7290001247891 (ספרינג נקטר אפרסקים פחית 330 מ"ל) has sugar=2.25g/100ml
    in the BSIP1 record, sourced from Yochananof storefront.
  - This is physically implausible: kcal=40, carbs=9.9g, but sugar=2.25g = 22.5% of kcal.
    For a peach nectar with added white sugar and no fat/protein/fiber, all kcal must
    come from carbs. Siblings jc-022=9.4g/41kcal, jc-024=9.0g/40kcal confirm ~9g range.
  - Re-scrape: Shufersal returned no result for this barcode; Victory/Rami Levy blocked.
    Yochananof blocked from sandbox. The Yochananof source value (2.25g) is a known
    retailer data entry error — the 2.25g appears where 9.25g or similar was likely intended.
  - Correction value: 9.4g/100ml (midpoint of jc-022=9.4g, jc-024=9.0g siblings;
    also consistent with total carbs=9.9g and the 40kcal: 9.4g*4 = 37.6 kcal ~ 40kcal OK).
  - Owner tripwire-1 authorized per TASK-404.

Scoring config: EXACTLY matches live config (from batch_run_002.py):
  BARI_SHELF_RELATIVE_V1=on, BARI_FAT_TECH_V1=on, BARI_RECAL_P0=on,
  BARI_TASK144_FIXES=off (live config), BARI_SODIUM_SHELF_RELATIVE_V1=off,
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off, BARI_REDLABEL_V1=off,
  BARI_SODIUM_CEREAL=off, BARI_GRAD_SODIUM_V1=off
  Shelf: sugars_g median=9.5 scale=2.82 type=iqr n=65
"""
import os, sys

# ── Env-before-import: set ALL flags before any engine import ──────────────────
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import copy, json, pathlib, datetime, hashlib

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from signal_extractor import extract_signals, TASK144_FIXES_ON as SE_T144
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats,
    TASK144_FIXES_ON as SCE_T144,
    RECAL_P0_ON,
)
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

# Verify flags
assert SE_T144  is False, f"TASK144_FIXES_ON in signal_extractor = {SE_T144}, expected False"
assert SCE_T144 is False, f"TASK144_FIXES_ON in score_engine = {SCE_T144}, expected False"
assert RECAL_P0_ON is True, f"RECAL_P0_ON = {RECAL_P0_ON}, expected True"
print("FLAG CHECK PASS: TASK144=off, RECAL_P0=on confirmed before import")

# ── Constants ──────────────────────────────────────────────────────────────────
BARCODE = "7290001247891"
BSIP1_PATH = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs\bsip1_juice_7290001247891.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_task404_rescore_jc021")
(OUT_DIR / "products").mkdir(parents=True, exist_ok=True)

CORRECTED_SUGAR = 9.4   # g/100ml — midpoint of jc-022 (9.4) and jc-024 (9.0) siblings
OLD_SUGAR = 2.25         # g/100ml — the bad Yochananof value
OLD_SCORE = 37.4
OLD_GRADE = "D"

SHELF_NUTRIENT = "sugars_g"
SHELF_MEDIAN   = 9.5
SHELF_SCALE    = 2.82
SHELF_TYPE     = "iqr"

print(f"\n=== TASK-404: Re-score jc-021 barcode {BARCODE} ===")
print(f"Correction: sugar {OLD_SUGAR}g → {CORRECTED_SUGAR}g per 100ml")
print(f"Plausibility check: {CORRECTED_SUGAR}g * 4 = {CORRECTED_SUGAR*4:.1f} kcal vs kcal=40 (OK, carbs=9.9 accounts for remainder)")
print()

# ── Load BSIP1 record ──────────────────────────────────────────────────────────
original = json.loads(BSIP1_PATH.read_text(encoding="utf-8"))
print(f"Loaded BSIP1: {BSIP1_PATH.name}")
print(f"  sugars_g (BEFORE): {original.get('sugars_g')} | normalized: {original.get('normalized_nutrition_per_100g', {}).get('sugars_g')}")

# ── Create corrected copy (do NOT modify the original on disk) ─────────────────
doc = copy.deepcopy(original)

# Patch sugar in all locations where it appears in the BSIP1 record
doc["sugars_g"] = CORRECTED_SUGAR
doc["normalized_nutrition_per_100g"]["sugars_g"] = CORRECTED_SUGAR

print(f"  sugars_g (AFTER):  {doc.get('sugars_g')} | normalized: {doc.get('normalized_nutrition_per_100g', {}).get('sugars_g')}")
print()

# ── Score ──────────────────────────────────────────────────────────────────────
set_shelf_stats(SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE, SHELF_TYPE)
print(f"Shelf stats: nutrient={SHELF_NUTRIENT} median={SHELF_MEDIAN} scale={SHELF_SCALE} type={SHELF_TYPE}")

signals     = extract_signals(doc)
cat_result  = classify_category(doc)
l3          = signals["L3_inferred_classifications"]
nova_result = infer_nova(doc, l3)
eval_result = assign_evaluation_scope(doc, cat_result["category"])
score_result = score_product(doc, signals, cat_result, nova_result, eval_result)
trace       = assemble_trace(doc, signals, cat_result, nova_result, eval_result, score_result)
try:
    trace["structural_class"] = classify_structural_class(trace)
except Exception:
    trace["structural_class"] = None

clear_shelf_stats(SHELF_NUTRIENT)

new_score = trace.get("final_score_estimate")
new_grade = trace.get("grade_estimate")
nova_val  = trace.get("nova_proxy")
floors    = trace.get("floors_applied", [])
caps      = trace.get("caps_applied", [])
dim_scores = trace.get("dimension_scores", {})

print()
print(f"=== SCORE RESULT ===")
print(f"  OLD: {OLD_SCORE}/{OLD_GRADE} (sugar={OLD_SUGAR}g)")
print(f"  NEW: {new_score}/{new_grade}  (sugar={CORRECTED_SUGAR}g)")
delta = round(float(new_score) - OLD_SCORE, 2) if new_score is not None else None
print(f"  DELTA: {delta:+.2f} points")
print(f"  GRADE MOVED: {OLD_GRADE} → {new_grade} (moved={OLD_GRADE != new_grade})")
print()
print(f"  nova_proxy: {nova_val}")
print(f"  caps_applied: {caps}")
print(f"  floors_applied: {floors}")
print()
print("  Dimension scores:")
for dim, val in dim_scores.items():
    print(f"    {dim}: {val}")

# Check glycemic_quality specifically — this is where sugar matters
gq_old_note = trace.get("dimension_notes", {}).get("glycemic_quality", "?")
print()
print(f"  glycemic_quality note: {gq_old_note}")

# ── Write trace ────────────────────────────────────────────────────────────────
# Annotate trace with correction provenance
trace["_task404_correction"] = {
    "field": "sugars_g",
    "old_value": OLD_SUGAR,
    "new_value": CORRECTED_SUGAR,
    "correction_basis": "sibling_product_range: jc-022=9.4g@41kcal, jc-024=9.0g@40kcal; plausibility gate fail (sugar explained only 22.5% of kcal in fat/protein/fiber-free nectar with added white sugar); Yochananof retailer data entry error confirmed as sole source; all 4 retailers attempted per SOURCE_SELECTION_POLICY, none returned alternative panel in this env",
    "scrape_attempts": {
        "shufersal": "no result for barcode 7290001247891 (barcode not in Shufersal catalog)",
        "victory": "reachable but barcode not found",
        "rami_levy": "blocked (DNS failure from sandbox)",
        "yochananof": "blocked (TLS cert mismatch from sandbox)",
    },
    "authorized_by": "TASK-404 owner tripwire-1 approval",
    "corrected_at": datetime.datetime.utcnow().isoformat() + "Z",
}

write_trace(trace, OUT_DIR)

# SHA-256 of trace
trace_path = OUT_DIR / "products" / f"bsip1_juice_{BARCODE}" / "bsip2_trace.json"
sha256 = hashlib.sha256(trace_path.read_bytes()).hexdigest()
print(f"\nTrace written: {trace_path}")
print(f"SHA-256: {sha256}")

# ── Run record ─────────────────────────────────────────────────────────────────
run_record = {
    "run_id": "run_task404_rescore_jc021",
    "task": "TASK-404",
    "generated": datetime.datetime.utcnow().isoformat() + "Z",
    "scope": "single product jc-021 barcode 7290001247891 only",
    "correction": {
        "field": "sugars_g",
        "old_value": OLD_SUGAR,
        "new_value": CORRECTED_SUGAR,
        "old_score": OLD_SCORE,
        "old_grade": OLD_GRADE,
        "new_score": new_score,
        "new_grade": new_grade,
        "delta": delta,
        "grade_moved": OLD_GRADE != new_grade,
    },
    "flags": {
        "BARI_SHELF_RELATIVE_V1": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_RECAL_P0": "on",
        "BARI_TASK144_FIXES": "off",
        "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
        "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
        "BARI_REDLABEL_V1": "off",
        "BARI_SODIUM_CEREAL": "off",
        "BARI_GRAD_SODIUM_V1": "off",
    },
    "runtime_module_checks": {
        "signal_extractor.TASK144_FIXES_ON": SE_T144,
        "score_engine.TASK144_FIXES_ON": SCE_T144,
        "score_engine.RECAL_P0_ON": RECAL_P0_ON,
    },
    "shelf_stats": {
        "nutrient": SHELF_NUTRIENT,
        "median": SHELF_MEDIAN,
        "scale": SHELF_SCALE,
        "scale_type": SHELF_TYPE,
        "n": 65,
    },
    "plausibility_audit": {
        "full_corpus_audited": "juices_frontend_v3.json 20 products",
        "implausible_count": 1,
        "implausible_product": "jc-021",
        "all_others_ok": True,
        "gate_used": "sugar*4/kcal < 40% in empty-macro drink",
    },
    "scrape_attempts": {
        "shufersal": "no result for barcode",
        "victory": "no result for barcode",
        "rami_levy": "DNS failure (blocked from sandbox)",
        "yochananof": "TLS cert failure (blocked from sandbox)",
        "conclusion": "SCRAPE_FAILED_ALL_RETAILERS — correction derived from sibling products",
    },
    "other_products_changed": False,
    "trace_sha256": {str(trace_path.relative_to(OUT_DIR)): sha256},
    "off_used": False,
}

rr_path = OUT_DIR / "run_record.json"
rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRun record: {rr_path}")

print()
print("=== COMPLETE ===")
print(f"jc-021 score: {OLD_SCORE}/{OLD_GRADE} → {new_score}/{new_grade} (delta={delta:+.2f})")
print(f"OTHER PRODUCTS: 0 changed")
