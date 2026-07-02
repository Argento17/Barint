import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Look at the original live JSON to understand what caused the 39/D scores
with open(r'C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v2.json', encoding='utf-8') as f:
    hc_live = json.load(f)

print("=== LIVE JSON: 39/D products ===")
for p in hc_live['products']:
    if p['score'] == 39.0:
        print(f"\n  {p['barcode']}  {p['name']}")
        exp = p.get('expansion', {})
        nn = exp.get('nutrition', {})
        print(f"  nutrition: kcal={nn.get('energyKcal')} fat={nn.get('fat')} sat_fat={nn.get('saturatedFat')} sodium={nn.get('sodium')}")
        print(f"  insightLine: {p.get('insightLine','')[:100]}")
        print(f"  limitingFactors: {exp.get('limitingFactors', [])}")

# Now check the run_hard_cheeses_yohananof_001 BSIP2 run to find the trace
print("\n\n=== Checking for original run traces ===")
orig_trace_base = r'C:\Bari\02_products\hard_cheeses\bsip2_outputs'
for run_dir in os.listdir(orig_trace_base):
    run_path = os.path.join(orig_trace_base, run_dir)
    if not os.path.isdir(run_path):
        continue
    prods_path = os.path.join(run_path, 'products')
    if not os.path.isdir(prods_path):
        continue
    count = len(os.listdir(prods_path))
    print(f"  Run: {run_dir}  ({count} product dirs)")

# Check a specific 39/D product in the older run
sample_trace = r'C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hardcheese_redlabel_v1_001\products\bsip1_hardcheese_7290004122270\bsip2_trace.json'
print("\n=== OLD TRACE for 7290004122270 (was 39/D, now 69.1/B) ===")
if os.path.exists(sample_trace):
    with open(sample_trace, encoding='utf-8') as f:
        t = json.load(f)
    print(f"  score: {t.get('final_score_estimate')}  grade: {t.get('grade_estimate')}")
    print(f"  caps_applied: {t.get('caps_applied', [])}")
    print(f"  penalties_applied: {t.get('penalties_applied', [])}")
    print(f"  binding_cap: {t.get('binding_cap')}")
    nn = t.get('L1_observed_signals', {})
    print(f"  sat_fat: {nn.get('fat_saturated_g')}  sodium: {nn.get('sodium_mg')}")
    print(f"  red_labels: {t.get('L3_inferred_classifications', {}).get('red_labels')}")
    dim = t.get('dimension_notes', {})
    print(f"  regulatory_quality note: {dim.get('regulatory_quality')}")
else:
    print("  Not found")
