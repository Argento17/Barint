import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

trace_dir = r'C:\Bari\_rescore_staging\hard_cheeses\products'
print(f"{'product':<55} {'sat_fat':>8} {'subpool':<20} {'fat_tech':>8} {'score':>6} {'grade'}")
print("-" * 110)

results = []
for prod_dir in sorted(os.listdir(trace_dir)):
    trace_path = os.path.join(trace_dir, prod_dir, 'bsip2_trace.json')
    if not os.path.exists(trace_path):
        continue
    with open(trace_path, encoding='utf-8') as f:
        t = json.load(f)

    name = t.get('input_reference', {}).get('product_name_he', '')[:50]
    sat_fat = t.get('L1_observed_signals', {}).get('fat_saturated_g')

    # Find subpool in L1 signals or L3 or bsip1
    l3 = t.get('L3_inferred_classifications', {})

    # Check caps/penalties for fat_tech related signals
    caps_applied = t.get('caps_applied', [])
    penalties_applied = t.get('penalties_applied', [])
    score = t.get('final_score_estimate')
    grade = t.get('grade_estimate')

    fat_tech_signal = 'N/A'
    for p in penalties_applied:
        if 'FAT_TECH' in str(p) or 'PHVO' in str(p) or 'MARG' in str(p):
            fat_tech_signal = str(p.get('rule', ''))[:15]

    results.append((name, sat_fat, fat_tech_signal, score, grade, prod_dir))
    print(f"{name:<55} {str(sat_fat):>8} {'':>20} {fat_tech_signal:>8} {score:>6} {grade}")

# Now check bsip1 files for subpool
print("\n--- Checking bsip1 files for subpool data ---")
bsip1_dir = r'C:\Bari\02_products\hard_cheeses\bsip1_outputs'
count_with_subpool = 0
count_with_sat_fat = 0
for fname in os.listdir(bsip1_dir):
    if not fname.endswith('.json'):
        continue
    with open(os.path.join(bsip1_dir, fname), encoding='utf-8') as f:
        b = json.load(f)
    subpool = b.get('bsip_cheese_subpool') or b.get('_subPool') or b.get('subPool')
    sat_fat = None
    # Check nested nutrition
    nn = b.get('normalized_nutrition_per_100g', {})
    sat_fat = nn.get('fat_saturated_g') if nn else None
    name = b.get('product_name_he', '')[:40]
    bc = b.get('barcode', '')
    print(f"  {bc}  {name:<40}  subpool={subpool!r}  sat_fat={sat_fat}")
    if subpool:
        count_with_subpool += 1
    if sat_fat is not None:
        count_with_sat_fat += 1

print(f"\nTotal bsip1 files: {len(os.listdir(bsip1_dir))}")
print(f"Files with subpool: {count_with_subpool}")
print(f"Files with sat_fat: {count_with_sat_fat}")
