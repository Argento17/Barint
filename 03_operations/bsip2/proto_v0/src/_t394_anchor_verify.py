"""One-shot: verify anchor status of the 12 additional movers."""
import json, pathlib, sys, os
sys.stdout.reconfigure(encoding='utf-8')

os.environ['BARI_R3_BISCUIT_NARROW_V1'] = 'off'
sys.path.insert(0, r'C:\Bari\03_operations\bsip2\proto_v0\src')

from router_v2 import _check_anchors, BARI_R3_BISCUIT_NARROW_V1
print('Flag state (should be False):', BARI_R3_BISCUIT_NARROW_V1)

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

print()
print('All 14 movers — anchor verification:')
for bc in diff_bcs:
    doc = corpus.get(bc)
    if not doc:
        print(f'BC={bc}: NO CORPUS MATCH')
        continue
    name_he = doc.get('canonical_name_he') or ''
    name = name_he.lower()
    anchor = _check_anchors(name)
    if anchor:
        cat, subtype, conf, term = anchor
        print(f'BC={bc} | name={name_he[:50]} | anchor={cat}({conf}) term={term}')
    else:
        print(f'BC={bc} | name={name_he[:50]} | NO ANCHOR')
