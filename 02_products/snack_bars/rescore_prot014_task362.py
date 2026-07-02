"""
prot-014 single-product re-score (Nutrition Agent ruling, REQ-362-R1 correction).

Context: prot-014 (חטיף חלבון קרם אגוזים, מקס ברנר, barcode 7290112913487) was
scored on the whole_food_fat engine path.  Its 15 shelf-mates use snack_bar_granola.
Rule 2 of REQ-362-R1 did not fire because its parsed ingredient_count (13) fell
below the >=15 threshold.  Nutrition Agent ruling (option b): force the snack_bar_granola
path for this product using the same anchor_override mechanism as Rule 1/Rule 2.

This script does NOT modify:
  - any engine file under 03_operations/bsip2/
  - the canonical BSIP1 file on disk
  - any other product in the frontend JSON

Mechanism: call _apply_req362_overrides() directly with the staged whole_food_fat
result + _req362_ingredient_count=15 injected into the product dict.  This is
byte-identical to what Rule 2 would produce if ingredient_count had been 15.
"""
from __future__ import annotations

import json
import pathlib
import sys
import datetime
import hashlib
import tempfile

ROOT = pathlib.Path(r"C:\Bari")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP2_SRC = ROOT / "03_operations" / "bsip2" / "proto_v0" / "src"
SNACKS_DIR = ROOT / "02_products" / "snack_bars"
SHARED = ROOT / "03_operations" / "bsip0" / "scrape" / "_shared"
CANON_BSIP1 = SNACKS_DIR / "canonical_bsip1" / "run_task362" / "bsip1_7290112913487.json"
FRONTEND_PATH = ROOT / "bari-web" / "src" / "data" / "comparisons" / "protein_bars_frontend_v1.json"

BARCODE = "7290112913487"
PRODUCT_ID = "prot-014"
RUN_ID = "rescore_prot014_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Add engine to path
sys.path.insert(0, str(BSIP2_SRC))
sys.path.insert(0, str(SHARED))

print(f"=== prot-014 Re-Score === run_id={RUN_ID}")
print(f"Canon BSIP1: {CANON_BSIP1}")

# ── 1. Load the canonical BSIP1 ─────────────────────────────────────────────

bsip1 = json.load(open(CANON_BSIP1, encoding="utf-8"))

# ── 2. Verify the natural route (Rule 2 not firing) ─────────────────────────

import router_v2
from router_v2 import _apply_req362_overrides, _R2_PROTEIN_THRESHOLD_G, _R2_INGREDIENT_COUNT_MIN

natural_result = router_v2.classify_category(dict(bsip1))
print(f"\nNatural route (unmodified): category={natural_result['category']}")
print(f"  req362_override_trace: {natural_result.get('req362_override_trace')}")

assert natural_result["category"] == "whole_food_fat", (
    f"Expected whole_food_fat as natural route, got {natural_result['category']}"
)
natural_count = natural_result["req362_override_trace"]["ingredient_count_used"]
print(f"  parsed ingredient_count: {natural_count} (threshold is {_R2_INGREDIENT_COUNT_MIN})")
print("CONFIRMED: natural route = whole_food_fat (Rule 2 did not fire)")

# ── 3. Apply the override using Rule 2 mechanism directly ───────────────────
# We call _apply_req362_overrides directly with:
#   - a staged result that reflects the whole_food_fat engine outcome
#   - _req362_ingredient_count=15 injected into the product dict
# This is exactly what Rule 2 executes when ingredient_count >= 15.

# Build the staged router result (from the natural run — correct whole_food_fat output)
staged_result = dict(natural_result)
# Remove the override trace so _apply_req362_overrides starts fresh
staged_result.pop("req362_override_trace", None)

# Inject the corrected ingredient count into a product copy
product_corrected = dict(bsip1)
product_corrected["_req362_ingredient_count"] = 15  # Force Rule 2 threshold

override_result = _apply_req362_overrides(staged_result, product_corrected)
print(f"\nOverride result: category={override_result['category']}")
print(f"  category_subtype={override_result.get('category_subtype')}")
print(f"  anchor_override={override_result.get('anchor_override')}")
print(f"  req362_override_trace: {override_result.get('req362_override_trace')}")

assert override_result["category"] == "snack_bar_granola", (
    f"Override did not fire: {override_result.get('req362_override_trace')}"
)
assert override_result.get("category_subtype") == "protein_bar"
assert override_result.get("anchor_override") is True
print("CONFIRMED: Rule 2 fires with ingredient_count=15 → snack_bar_granola/protein_bar")

# ── 4. Run full BSIP2 on a temp BSIP1 with monkey-patched router ─────────────
# We run run_bsip2 but intercept classify_category to return the override result.

from signal_extractor import extract_signals
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from input_loader import load_product, validate_product

print("\nRunning BSIP2 score_product on snack_bar_granola path...")

with tempfile.TemporaryDirectory() as tmpdir:
    # Write a temp BSIP1 with the corrected ingredient count
    tmp_bsip1_path = pathlib.Path(tmpdir) / f"bsip1_{BARCODE}.json"
    product_temp = dict(bsip1)
    product_temp["_req362_ingredient_count"] = 15
    tmp_bsip1_path.write_text(
        json.dumps(product_temp, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Run the pipeline manually, using override_result for the cat_result
    product = load_product(tmp_bsip1_path)
    product["_source_path"] = str(tmp_bsip1_path)
    errors = validate_product(product)
    product["_load_errors"] = errors

    signals = extract_signals(product)
    # Use our forced cat_result (snack_bar_granola, protein_bar, anchor_override=True)
    cat_result = override_result
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)

    # Write trace for traceability
    bsip2_out = SNACKS_DIR / "bsip2_outputs" / RUN_ID / "products"
    bsip2_out.mkdir(parents=True, exist_ok=True)
    trace_dir = bsip2_out / f"bsip1_{BARCODE}"
    trace_dir.mkdir(parents=True, exist_ok=True)
    write_trace(trace, trace_dir)
    print(f"  trace written: {trace_dir}")

new_score = trace.get("final_score_estimate") or trace.get("score")
new_grade = trace.get("grade_estimate") or trace.get("grade")
new_cat   = trace.get("category")
new_subtype = trace.get("category_subtype")

if new_score is None:
    print("ERROR: no score in trace. Trace keys:", list(trace.keys()))
    sys.exit(1)

new_score = round(float(new_score), 1)

print(f"\n=== BSIP2 RE-SCORE RESULT ===")
print(f"  score:    {new_score}")
print(f"  grade:    {new_grade}")
print(f"  category: {new_cat}")
print(f"  subtype:  {new_subtype}")

assert new_cat == "snack_bar_granola", f"Trace category should be snack_bar_granola, got {new_cat}"

# ── 5. Update protein_bars_frontend_v1.json ──────────────────────────────────

frontend = json.load(open(FRONTEND_PATH, encoding="utf-8"))
products = frontend["products"]

# Find prot-014
idx_014 = None
old_score = None
old_grade = None
old_rank  = None
for i, p in enumerate(products):
    if p["id"] == PRODUCT_ID:
        idx_014 = i
        old_score = p["score"]
        old_grade = p["grade"]
        old_rank  = p["rank"]
        break

assert idx_014 is not None, f"{PRODUCT_ID} not found in frontend JSON"
print(f"\nOLD prot-014: score={old_score}, grade={old_grade}, rank={old_rank}, "
      f"category={products[idx_014]['_scoring_trace']['category']}")

# Update prot-014's score, grade, and _scoring_trace.category ONLY
products[idx_014]["score"]  = new_score
products[idx_014]["grade"]  = new_grade
products[idx_014]["_scoring_trace"]["category"] = "snack_bar_granola"

# Do NOT touch nutrition, copy, expansion, image, barcode, name, confidence, or any other field.

# ── 6. Re-sort and re-rank with competition ranking ──────────────────────────

products.sort(key=lambda x: -(x["score"] or 0))

def assign_competition_ranks(prods):
    """Assign competition ranks: ties share the same rank, next skips count."""
    n = len(prods)
    i = 0
    while i < n:
        j = i
        while j < n and prods[j]["score"] == prods[i]["score"]:
            j += 1
        for k in range(i, j):
            prods[k]["rank"] = i + 1
        i = j
    return prods

products = assign_competition_ranks(products)

# Verify no id changed, all 16 products present
ids = [p["id"] for p in products]
assert "prot-014" in ids, "prot-014 lost"
assert len(products) == 16, f"Expected 16 products, got {len(products)}"
for p in products:
    assert p["categoryTotal"] == 16

frontend["products"] = products

# ── 7. Update _meta.copy_status ─────────────────────────────────────────────

frontend["_meta"]["copy_status"] = "COMPLETE"

# ── 8. Write the updated frontend JSON ──────────────────────────────────────

content_bytes = json.dumps(frontend, ensure_ascii=False, indent=2).encode("utf-8")
sha256_new = hashlib.sha256(content_bytes).hexdigest()

FRONTEND_PATH.write_text(
    json.dumps(frontend, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"\nFrontend JSON updated: {FRONTEND_PATH}")
print(f"SHA256: {sha256_new}")

# ── 9. Print new rank table ──────────────────────────────────────────────────

print(f"\n=== NEW RANK TABLE ({len(products)} products) ===")
print(f"{'rank':>4}  {'id':12}  {'score':>6}  {'grade':>5}  name")
for p in products:
    print(f"{p['rank']:>4}  {p['id']:12}  {p['score']:>6}  {p['grade']:>5}  {p['name_he'][:42]}")

# ── 10. Summary ─────────────────────────────────────────────────────────────

p014 = next(p for p in products if p["id"] == PRODUCT_ID)
print(f"\n=== prot-014 DELTA ===")
print(f"  score:    {old_score} → {p014['score']}")
print(f"  grade:    {old_grade} → {p014['grade']}")
print(f"  rank:     {old_rank} → {p014['rank']}")
print(f"  category: whole_food_fat → {p014['_scoring_trace']['category']}")
print(f"  categoryTotal: {p014['categoryTotal']} (unchanged)")

# ── 11. Run-record ───────────────────────────────────────────────────────────

run_record = {
    "run_id": RUN_ID,
    "date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "agent": "Data Agent",
    "ruling": "Nutrition Agent option b — REQ-362-R1 Rule 2 correction",
    "product_id": PRODUCT_ID,
    "barcode": BARCODE,
    "change": {
        "score": {"old": old_score, "new": p014["score"]},
        "grade": {"old": old_grade, "new": p014["grade"]},
        "rank":  {"old": old_rank,  "new": p014["rank"]},
        "category": {"old": "whole_food_fat", "new": "snack_bar_granola"},
    },
    "mechanism": (
        "Rule 2 anchor_override: _apply_req362_overrides called directly with "
        "whole_food_fat staged result + _req362_ingredient_count=15 injected. "
        f"protein_g=33.0 >= {_R2_PROTEIN_THRESHOLD_G}, count forced 13→15 >= {_R2_INGREDIENT_COUNT_MIN}."
    ),
    "engine_modified": False,
    "canonical_bsip1_modified": False,
    "bsip2_trace_dir": str(bsip2_out / f"bsip1_{BARCODE}"),
    "frontend_path": str(FRONTEND_PATH),
    "frontend_sha256": sha256_new,
}

record_path = SNACKS_DIR / f"{RUN_ID}_run_record.json"
record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRun record: {record_path}")
print("\n=== DONE ===")
