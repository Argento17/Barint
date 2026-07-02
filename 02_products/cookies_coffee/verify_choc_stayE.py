"""Verify: chocolate-named cookies that got a score nudge (R3 didn't fire) stayed E."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load diff table from task394 measurement to find the 12 score-nudge products
diff_path = r'C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_task394_r3_measure\diff_table.json'
with open(diff_path, encoding='utf-8') as f:
    diffs = json.load(f)

print(f"Diff table entries: {len(diffs)}")

# Check structure
if diffs:
    print(f"First entry keys: {list(diffs[0].keys())}")

# The 14 movers: 2 are grade-changers (moved D->E->D), 12 are score-only nudges
# Per the task spec: the 12 chocolate-named cookies that are score-only nudges -> stay E
grade_change_bc = {'2986065', '7290017894317'}  # these are the grade-changers (D->E in R3=off, D in R3=on)

score_nudge_products = []
for d in diffs:
    bc = str(d.get('barcode', ''))
    if bc not in grade_change_bc:
        score_nudge_products.append(d)

print(f"\nScore-only nudge products (should stay E): {len(score_nudge_products)}")

# Load final frontend JSON to check their grades
with open(r'C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json', encoding='utf-8') as f:
    frontend = json.load(f)

prod_map = {str(p.get('barcode','')): p for p in frontend.get('products', [])}

print("\nScore-nudge products in final frontend:")
for d in score_nudge_products:
    bc = str(d.get('barcode', ''))
    p = prod_map.get(bc)
    if p:
        grade = p.get('grade')
        cat = p.get('_scoring_trace', {}).get('category', 'no_trace')
        name = p.get('name', '')[:40]
        print(f"  {bc}: grade={grade} cat={cat} name={name}")
    else:
        print(f"  {bc}: NOT IN FRONTEND")
