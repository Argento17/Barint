# -*- coding: utf-8 -*-
"""Verify written trace files for run_task389_rescore_002."""
import json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

run_dir = pathlib.Path(r'C:\Bari\02_products\juices\bsip2_outputs\run_task389_rescore_002\products')
trace_files = list(run_dir.glob('**/bsip2_trace.json'))
print(f'Trace files found: {len(trace_files)}')

results = []
for fp in sorted(trace_files):
    t = json.loads(fp.read_text(encoding='utf-8'))
    ir = t.get('input_reference') or {}
    bc = str(ir.get('barcode',''))
    nm = (ir.get('product_name_he') or '')[:45]
    nova = t.get('nova_proxy')
    score = t.get('final_score_estimate')
    grade = t.get('grade_estimate')
    floors_a = t.get('floors_applied', [])
    ing_count = (t.get('L1_observed_signals') or {}).get('ingredient_count', 0)
    floor_names = []
    for f in floors_a:
        if isinstance(f, dict):
            floor_names.append(f.get('floor_type','?'))
        else:
            floor_names.append(str(f))
    results.append((bc, nm, nova, ing_count, score, grade, floor_names, fp))
    print(f'  {bc}  nova={nova}  ing={ing_count}  score={score}  grade={grade}  floors={floor_names}  {nm[:40]}')

print()

SI_BCS = {'7290000525969','7290003009640','7290004030100','7290013153395','7290013608260','7290110114886'}
print('=== SINGLE-INGREDIENT ACCEPTANCE CHECK (from written traces) ===')
all_pass = True
for bc, nm, nova, ing, score, grade, floors, fp in results:
    if bc not in SI_BCS:
        continue
    nova_ok = (nova == 1)
    floor_ok = any('nova1' in f.lower() for f in floors)
    score_ok = (score == 85)
    grade_ok = (grade == 'A')
    status = 'PASS' if (nova_ok and floor_ok and score_ok and grade_ok) else 'FAIL'
    if status != 'PASS':
        all_pass = False
    print(f'  {status}  {bc}  nova={nova}(ok={nova_ok})  floor={floor_ok}  score={score}(ok={score_ok})  grade={grade}(ok={grade_ok})  ing={ing}')

print()
print('Single-ingredient check:', 'ALL PASS' if all_pass else 'FAILURES DETECTED')
print(f'Total traces: {len(results)}  (expected 17)')

# Grade distribution from written traces
dist = {}
for _, _, _, _, _, grade, _, _ in results:
    dist[grade] = dist.get(grade, 0) + 1
print(f'Grade distribution from written traces: {dict(sorted(dist.items()))}')
print(f'Expected: A=6, D=7, E=4')
ok = (dist.get('A',0) == 6 and dist.get('D',0) == 7 and dist.get('E',0) == 4)
print(f'Distribution check: {"PASS" if ok else "FAIL"}')

# Confirm no TASK144 bleed in any trace (if TASK144 was on, the note would be different)
print()
print('=== TASK144 BLEED CHECK ===')
bleed_found = False
for fp in sorted(run_dir.glob('**/bsip2_trace.json')):
    t = json.loads(fp.read_text(encoding='utf-8'))
    ir = t.get('input_reference') or {}
    bc = str(ir.get('barcode',''))
    l1 = t.get('L1_observed_signals') or {}
    san = l1.get('ingredient_sanitization') or {}
    dropped = san.get('dropped', [])
    clean_count = san.get('clean_count', -1)
    raw_count = san.get('raw_count', -1)
    nova = t.get('nova_proxy')
    # The bleed symptom: raw_count=1, clean_count=0, dropped contains the product name
    if raw_count == 1 and clean_count == 0 and dropped:
        print(f'  BLEED DETECTED  {bc}  raw={raw_count}  clean={clean_count}  dropped={dropped}  nova={nova}')
        bleed_found = True

if not bleed_found:
    print('  No TASK144 bleed detected in any trace (clean_count correctly == raw_count for single-ingredient products)')
