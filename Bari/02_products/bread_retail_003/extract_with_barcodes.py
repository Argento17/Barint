import json, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BSIP2_DIR = Path(r'C:\Bari\02_products\bread_retail_003\bsip2')
BSIP0_RAW = Path(r'C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json')

with open(BSIP0_RAW, encoding='utf-8') as f:
    bsip0 = json.load(f)

barcode_to_ing = {}
for item in bsip0:
    bc = str(item.get('barcode', '')).strip()
    if bc:
        ing = item.get('ingredients_raw', '') or ''
        for m in ['מאפיינים נוספים', 'ערכים תזונתיים', 'אין להסתמך']:
            idx = ing.find(m)
            if idx > 10:
                ing = ing[:idx].strip()
        barcode_to_ing[bc] = ing

products = []
for f in sorted(BSIP2_DIR.glob('*.json')):
    with open(f, encoding='utf-8') as fp:
        t = json.load(fp)
    deg = t.get('degradation_level', '')
    score = t.get('final_score')
    if deg not in ('FULL', 'CAUTIOUS') or score is None:
        continue
    barcode = str(t.get('barcode', '')).strip()
    ing = barcode_to_ing.get(barcode, '')
    ferm = any(m in ing for m in ['מחמצת', 'שאור', 'חמיצה'])
    nv = t.get('nutrition', {})
    products.append({
        'barcode': barcode,
        'name': t.get('name_he', '?'),
        'score': round(float(score)),
        'grade': t.get('final_grade', '?'),
        'category': t.get('category', '?'),
        'fiber': nv.get('dietary_fiber_g'),
        'ferm': ferm,
        'ing_first_80': ing[:80] if ing else '',
        'has_e': bool(re.search(r'E\d{3,4}', ing)),
        'has_emuls': any(x in ing for x in ['E471', 'E472', 'E481', 'DATEM', 'מתחלב']),
        'ing_full': ing,
    })

products.sort(key=lambda x: x['score'], reverse=True)
for i, p in enumerate(products, 1):
    ferm_str = ' M' if p['ferm'] else ''
    e_str = ' E' if p['has_e'] else ''
    em_str = ' EM' if p['has_emuls'] else ''
    print('%3d. BC=%s [%s/%s]%s%s%s %s (%s)' % (
        i, p['barcode'], p['score'], p['grade'],
        ferm_str, e_str, em_str, p['name'], p['category']))
    print('     %s' % p['ing_first_80'])

print('\nTotal: %d' % len(products))
print('\nDuplicate names:')
from collections import Counter
name_counts = Counter(p['name'] for p in products)
for name, cnt in sorted(name_counts.items()):
    if cnt > 1:
        dupes = [p for p in products if p['name'] == name]
        print('  "%s" x%d: %s' % (name, cnt, ', '.join(p['barcode'] for p in dupes)))
