import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_task394_r3_measure\on_scores.json', encoding='utf-8') as f:
    on_scores = json.load(f)

# Filter cookies_coffee
cc_products = {bc: r for bc, r in on_scores.items() if r.get('shelf') == 'cookies_coffee'}
print(f"cookies_coffee products in on_scores: {len(cc_products)}")

grade_dist = {}
for bc, r in cc_products.items():
    g = r.get('grade', '?')
    grade_dist[g] = grade_dist.get(g, 0) + 1

print(f"Grade distribution: {dict(sorted(grade_dist.items()))}")

# Show category distribution
cat_dist = {}
for bc, r in cc_products.items():
    c = r.get('category', '?')
    cat_dist[c] = cat_dist.get(c, 0) + 1
print(f"Category distribution: {dict(sorted(cat_dist.items()))}")

# How many have category = biscuit?
biscuit_products = {bc: r for bc, r in cc_products.items() if r.get('category') == 'biscuit'}
print(f"\nBiscuit-routed products: {len(biscuit_products)}")
biscuit_grade = {}
for bc, r in biscuit_products.items():
    g = r.get('grade', '?')
    biscuit_grade[g] = biscuit_grade.get(g, 0) + 1
print(f"Biscuit grade distribution: {dict(sorted(biscuit_grade.items()))}")
