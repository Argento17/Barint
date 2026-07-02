"""
circularity_verify_probe.py — verification cross-checks on macro_circularity_probe results.
Runs quick sanity checks:
  1. Category sums vs reported totals (accounting for score=None products)
  2. Cross-category vs within-category twin breakdown
  3. Per-category R² summary table
  4. High-confidence note: by_category counts ALL products with stated %;
     the labeled subset (645/318) filters to those WITH a valid matrix score
     (i.e. has grain or refined markers -> score != None).
     Cheese/dairy products have ingredients with stated % but no grain markers
     -> score=None -> excluded from the labeled subset.
"""
import json
from pathlib import Path

RESULTS = Path("C:/Bari/03_operations/bsip2/proto_v0/analysis/macro_circularity_probe_results.json")

r = json.loads(RESULTS.read_text(encoding="utf-8"))

print("=== VERIFICATION ===")

# 1. by_category sums
q1 = r["q1_labeled_subset"]["by_category"]
total_high = sum(v["high"] for v in q1.values())
total_order = sum(v["order"] for v in q1.values())
total_none = sum(v["none"] for v in q1.values())
total_all  = sum(v["total"] for v in q1.values())
print(f"\nQ1 by-category artifact sums:")
print(f"  by_category total_high  = {total_high}")
print(f"  by_category total_order = {total_order}")
print(f"  by_category total_none  = {total_none}")
print(f"  grand total (all cat)   = {total_all}")
print(f"\nQ1 labeled subset (WITH valid matrix score):")
print(f"  high_confidence (score != None) = {r['q1_labeled_subset']['high_confidence']}")
print(f"  order_only      (score != None) = {r['q1_labeled_subset']['order_only']}")
print(f"\n  Note: by_category counts ALL products with stated % regardless of matrix score.")
print(f"  {total_high - r['q1_labeled_subset']['high_confidence']} products have stated % but score=None")
print(f"  (these are cheese/dairy/juice products where grain markers = 0, no matrix score applies)")
print(f"\n  Grand total check: {total_all} == {r['q1_labeled_subset']['total_products']} -> {'OK' if total_all == r['q1_labeled_subset']['total_products'] else 'MISMATCH'}")

# 2. Twin pair cross-category breakdown
pairs = r["q4_macro_twins"]["examples"]
cross_cat = [p for p in pairs if p["cat1"] != p["cat2"]]
same_cat  = [p for p in pairs if p["cat1"] == p["cat2"]]
print(f"\nQ4 twin pair category breakdown (examples shown, not all {r['q4_macro_twins']['twin_pairs']} pairs):")
print(f"  Cross-category pairs in examples: {len(cross_cat)}")
print(f"  Same-category pairs in examples:  {len(same_cat)}")
print(f"  Total reported pairs: {r['q4_macro_twins']['twin_pairs']}")
print(f"  Unique products in pairs: {r['q4_macro_twins']['unique_products_in_pairs']}")
print(f"  As % of labeled pool: {r['q4_macro_twins']['twin_pct_of_labeled_pool']}%")
print(f"\n  Example cross-category twins:")
for p in cross_cat[:5]:
    print(f"    {p['cat1']} vs {p['cat2']}: score_diff={p['score_diff']}")

# 3. Per-category R²
print(f"\nQ2 per-category R² summary:")
for cat, dr in sorted(r["q2_regression"]["by_category"].items()):
    if dr.get("status") == "ok":
        print(f"  {cat:25s}: n={dr['n']:3d}  R2={dr.get('r2', '?')}  MAE={dr.get('mae', '?')}")
    else:
        print(f"  {cat:25s}: n={dr['n']:3d}  {dr['status']}")

pool = r["q2_regression"]["pooled"]
print(f"\nPooled: n={pool['n']}, R2={pool['r2']}, MAE={pool['mae']}")

# 4. Q3 correlation table
print(f"\nQ3 macro-composition correlations:")
for f, rv in r["q3_redundancy"]["per_macro_r"].items():
    print(f"  {f:20s}: r = {rv}")
print(f"  max_single_abs_r = {r['q3_redundancy']['max_single_macro_abs_r']}")
print(f"  multi_r (predicted vs true) = {r['q3_redundancy']['multi_macro_r_predicted_vs_true']}")

# 5. Q5 coverage
print(f"\nQ5 nutrition coverage (food corpus only, N=1276):")
for f, d in r["q5_coverage"]["per_field"].items():
    print(f"  {f:20s}: {d['present']}/{d['total']} ({d['pct']}%)")
core = r["q5_coverage"]["core_complete_sugar_fat_sodium"]
print(f"  Core complete (sugar+fat+sodium): {core['count']}/{r['q5_coverage']['total_food']} ({core['pct']}%)")

print("\n=== VERIFICATION COMPLETE ===")
