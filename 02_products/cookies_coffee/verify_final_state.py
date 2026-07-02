import json, sys, io
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
print(f"Grade distribution: {dict(sorted(grade_dist.items()))}")

print("\nTarget products:")
for p in prods:
    bc = str(p.get('barcode', ''))
    if bc in targets:
        trace = p.get('_scoring_trace', {})
        cat = trace.get('category', 'NO_TRACE')
        trace_score = trace.get('final_score_estimate', 'NO_TRACE')
        front_score = p.get('score')
        grade = p.get('grade')
        score_match = "MATCH" if front_score == trace_score else f"MISMATCH (front={front_score} trace={trace_score})"
        pending = p.get('insightLine') == 'PENDING_COPY'
        print(f"  {bc}: cat={cat} score={front_score} grade={grade} score==trace:{score_match} PENDING_COPY:{pending}")

# score==trace check for all 119
mismatch = 0
for p in prods:
    bc = str(p.get('barcode', ''))
    trace = p.get('_scoring_trace', {})
    if not trace:
        continue
    trace_score = trace.get('final_score_estimate')
    front_score = p.get('score')
    if front_score != trace_score:
        print(f"  SCORE!=TRACE: {bc} front={front_score} trace={trace_score}")
        mismatch += 1

print(f"\nScore==trace check: {len(prods)} products, {mismatch} mismatches")
print(f"Result: {'PASS' if mismatch == 0 else 'FAIL'}")

# PENDING_COPY check
pending_barcodes = [str(p.get('barcode','')) for p in prods
                    if p.get('insightLine') == 'PENDING_COPY' or p.get('rowVerdict') == 'PENDING_COPY']
print(f"\nPENDING_COPY barcodes ({len(pending_barcodes)}): {sorted(pending_barcodes)}")

# OFF ban
s = json.dumps(data)
print(f"OFF ban: {'PASS' if 'open_food_facts' not in s.lower() and 'openfoodfacts' not in s.lower() else 'FAIL'}")
