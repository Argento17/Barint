import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_task394_r3_measure\on_scores.json', encoding='utf-8') as f:
    on_scores = json.load(f)

# All shelves combined - find cookies_coffee products
# on_scores is keyed by barcode -> record
targets = {'2986065', '7290017894317', '313184', '7290018893845'}

print(f"Total barcodes in on_scores: {len(on_scores)}")

# Get grade distribution for cookies_coffee products
# Need to know which shelf each barcode belongs to
# Check the first few entries for structure
first_key = list(on_scores.keys())[0]
first_val = on_scores[first_key]
print(f"\nFirst entry keys: {list(first_val.keys())}")
print(f"First entry: barcode={first_key}, score={first_val.get('score')}, grade={first_val.get('grade')}, shelf={first_val.get('shelf')}")

# Find target products
print("\nTarget products in on_scores:")
for bc in targets:
    if bc in on_scores:
        r = on_scores[bc]
        print(f"  {bc}: score={r.get('score')}, grade={r.get('grade')}, category={r.get('category')}, shelf={r.get('shelf')}")
    else:
        print(f"  {bc}: NOT FOUND")
