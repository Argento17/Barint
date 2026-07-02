import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Bari\_rescore_staging\_spine_runs\_verify_palm_20260618T170038Z\hard_cheeses\hard_cheeses_rescored.json', encoding='utf-8') as f:
    hc_new = json.load(f)
with open(r'C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v2.json', encoding='utf-8') as f:
    hc_live = json.load(f)

print('=== HARD CHEESES RESCORED (new) ===')
prods_new = sorted(hc_new['products'], key=lambda p: -p['score'])
for p in prods_new:
    print(f"  {p['score']:5.1f}  {p['grade']}  {p['barcode']}  {p['name'][:55]}")

print()
print('=== HARD CHEESES LIVE ===')
prods_live = sorted(hc_live['products'], key=lambda p: -p['score'])
for p in prods_live:
    print(f"  {p['score']:5.1f}  {p['grade']}  {p['barcode']}  {p['name'][:55]}")

# Build diff table
live_by_bc = {p['barcode']: p for p in hc_live['products']}
new_by_bc = {p['barcode']: p for p in hc_new['products']}

print()
print('=== HARD CHEESES DIFF (new vs live, sorted by score change) ===')
diffs = []
for bc, pn in new_by_bc.items():
    pl = live_by_bc.get(bc)
    if pl:
        delta = pn['score'] - pl['score']
        grade_change = f"{pl['grade']}->{pn['grade']}"
        diffs.append((delta, bc, pl['score'], pn['score'], grade_change, pn['name'][:50]))

diffs.sort(key=lambda x: -x[0])
for delta, bc, old_s, new_s, gc, name in diffs:
    print(f"  {delta:+5.1f}  {old_s:5.1f} -> {new_s:5.1f}  {gc}  {bc}  {name}")

print(f"\n  Products in new not in live: {[bc for bc in new_by_bc if bc not in live_by_bc]}")
print(f"  Products in live not in new: {[bc for bc in live_by_bc if bc not in new_by_bc]}")
