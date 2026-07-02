import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json', encoding='utf-8') as f:
    data = json.load(f)

prods = data.get('products', [])
targets = {'2986065', '7290017894317', '313184', '7290018893845'}

print(f"Total products: {len(prods)}")
grade_dist = {}
for p in prods:
    g = p.get('grade', '?')
    grade_dist[g] = grade_dist.get(g, 0) + 1
print(f"Grade distribution: {sorted(grade_dist.items())}")

print("\nTarget products:")
for p in prods:
    bc = str(p.get('barcode', ''))
    if bc in targets:
        trace = p.get('_scoring_trace', {})
        cat = trace.get('category', 'NO_TRACE') if trace else p.get('category', 'NO_TRACE')
        print(f"  barcode={bc} score={p.get('score')} grade={p.get('grade')} category={cat}")
        il = p.get('insightLine', '')
        print(f"    insightLine={il[:80]}")
