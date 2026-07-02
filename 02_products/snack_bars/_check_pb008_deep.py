import sys, json, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")

# Deep check pb-008 (WIN cream milk barcode 7290015130028)
from batch_run_protein_bars_task365 import run_product, detect_protein_bar_signals, _adapt_product_for_engine
from constants import PROTEIN_ISOLATE_FAMILIES, PROTEIN_BAR_LENS_ON

corpus = json.loads(pathlib.Path(r"C:\Bari\02_products\snack_bars\protein_combined_corpus_task365_33_20260621_fix.json").read_text(encoding="utf-8"))
products = corpus["products"]

pb008 = next(p for p in products if p["barcode"] == "7290015130028")
print(f"pb-008: {pb008['name']} / barcode={pb008['barcode']}")
print(f"Lens active: {PROTEIN_BAR_LENS_ON}")
print()

# Run scoring
result = run_product(pb008)
pb_sig = result.get("protein_bar_signals", {})
print(f"score={result.get('final_score_estimate')} grade={result.get('grade_estimate')}")
print(f"collagen_detected={pb_sig.get('collagen_detected')}")
print(f"wholefood_protein_detected={pb_sig.get('wholefood_protein_detected')}")
print(f"isolate_stacking={pb_sig.get('isolate_stacking')}")
print(f"families_detected={pb_sig.get('families_detected')}")
print()
print(f"total_pb_penalty={result.get('total_pb_penalty')}")
print(f"effective_pb_cap={result.get('effective_pb_cap')}")
print(f"weighted_dim_score_pb={result.get('weighted_dimension_score_protein_bar')}")
print(f"score_after_pb_cap={result.get('score_after_pb_cap')}")
print(f"score_after_pb_penalty={result.get('score_after_pb_penalty')}")
print()

# Check dimension notes for protein_quality to confirm collagen penalty fired + wholefood suppressed
dim_notes = result.get("dimension_notes", {})
prq_note = dim_notes.get("protein_quality", "")
print(f"protein_quality note: {prq_note}")
print()

# Check caps fired
print(f"protein_bar_caps: {result.get('protein_bar_caps')}")
print(f"protein_bar_penalties: {result.get('protein_bar_penalties')}")
print()

# Confirm old score (before the fix, pb-008 had score=55, wholefood bonus fired, collagen penalty skipped)
# After fix: collagen penalty fires, wholefood bonus suppressed -> lower protein_quality score
dim_scores = result.get("dimension_scores", {})
print(f"dimension_scores: {dim_scores}")
print()

# Verify COND-2
print(f"cond2_double_fire_check={result.get('cond2_double_fire_check')}")
print(f"cond2_note={result.get('cond2_note')}")
