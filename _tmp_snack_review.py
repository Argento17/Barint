import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Bari\_rescore_staging\_spine_runs\_verify_palm_20260618T170038Z\snacks\snacks_rescored.json', encoding='utf-8') as f:
    sn_new = json.load(f)
with open(r'C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v2.json', encoding='utf-8') as f:
    sn_live = json.load(f)

print('=== SNACKS RESCORED (new) — top 30 by score ===')
prods_new = sorted(sn_new['products'], key=lambda p: -p['score'])
for p in prods_new[:35]:
    print(f"  {p['score']:5.1f}  {p['grade']}  {p['barcode']}  {p['name'][:55]}")

print()
print('=== SNACKS LIVE ===')
prods_live = sorted(sn_live['products'], key=lambda p: -p['score'])
for p in prods_live:
    print(f"  {p['score']:5.1f}  {p['grade']}  {p['barcode']}  {p['name'][:55]}")

# Diff
live_by_bc = {p['barcode']: p for p in sn_live['products']}
new_by_bc = {p['barcode']: p for p in sn_new['products']}

print()
print('=== SNACKS DIFF (barcodes in BOTH, sorted by delta) ===')
diffs = []
for bc, pn in new_by_bc.items():
    pl = live_by_bc.get(bc)
    if pl:
        delta = pn['score'] - pl['score']
        gc = f"{pl['grade']}->{pn['grade']}"
        diffs.append((delta, bc, pl['score'], pn['score'], gc, pn['name'][:50]))

diffs.sort(key=lambda x: -x[0])
for delta, bc, old_s, new_s, gc, name in diffs:
    flag = '  <-- grade change' if gc[0] != gc[-1] else ''
    print(f"  {delta:+5.1f}  {old_s:5.1f} -> {new_s:5.1f}  {gc}  {bc}  {name}{flag}")

print(f"\nProducts in new not in live: {len([bc for bc in new_by_bc if bc not in live_by_bc])}")
print(f"Products in live not in new: {len([bc for bc in live_by_bc if bc not in new_by_bc])}")

# Grade distribution summary
from collections import Counter
new_grades = Counter(p['grade'] for p in sn_new['products'])
live_grades = Counter(p['grade'] for p in sn_live['products'])
print(f"\nGrade dist NEW (all 53): {dict(sorted(new_grades.items()))}")
print(f"Grade dist LIVE (18):    {dict(sorted(live_grades.items()))}")
