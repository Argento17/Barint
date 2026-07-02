"""Verify confectionery ingredient signal check for all 14 movers."""
import json, pathlib, sys, os
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r'C:\Bari\03_operations\bsip2\proto_v0\src')
from router_v2 import _R3_CHOC_CONFECTIONERY_ING_SIGNALS

corpus_dirs = [
    pathlib.Path(r'C:\Bari\03_operations\bsip1\run_cookies_001\output'),
    pathlib.Path(r'C:\Bari\03_operations\bsip1\run_cakes_001\output'),
]
corpus = {}
for d in corpus_dirs:
    for fp in d.glob('bsip1_*.json'):
        doc = json.loads(fp.read_text(encoding='utf-8'))
        bc = str(doc.get('barcode',''))
        if bc and bc not in corpus:
            corpus[bc] = doc

diff_bcs = [
    '7622201401900','7290106656727','4017100364112','46214731552','5901414200411',
    '8710502139017','7290018893036','313160','4823077633317','80083665',
    '8410376075915','8410376037784','2986065','7290017894317',
]

print('All 14 movers — confectionery ingredient signal check:')
print('(These should all have NO confectionery signal = R3 guard correctly allows yield)')
print()
for bc in diff_bcs:
    doc = corpus.get(bc)
    if not doc:
        print(f'BC={bc}: NO CORPUS MATCH')
        continue
    name_he = doc.get('canonical_name_he') or ''
    ing = (doc.get('ingredients_text_he') or '').lower()
    hits = [sig for sig in _R3_CHOC_CONFECTIONERY_ING_SIGNALS if sig in ing]
    ing_preview = ing[:120] if ing else '(empty)'
    status = 'CONFECTIONERY_SIG_FOUND (R3 should NOT yield)' if hits else 'no-confectionery-signal (R3 yields correctly)'
    print(f'BC={bc}')
    print(f'  Name: {name_he[:60]}')
    print(f'  Ing (preview): {ing_preview}')
    print(f'  Status: {status}')
    if hits:
        print(f'  Signals found: {hits}')
    print()
