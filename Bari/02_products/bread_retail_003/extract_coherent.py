import json, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BSIP2_DIR = Path(r'C:\Bari\02_products\bread_retail_003\bsip2')
BSIP0_RAW = Path(r'C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json')

# Load BSIP0 raw for ingredients + image URLs
with open(BSIP0_RAW, encoding='utf-8') as f:
    bsip0 = json.load(f)

barcode_to_bsip0 = {}
for item in bsip0:
    bc = str(item.get('barcode', '')).strip()
    if bc:
        barcode_to_bsip0[bc] = item

def detect_fermentation(ing_raw):
    if not ing_raw:
        return False
    markers = ['מחמצת', 'שאור', 'חמיצה', 'תסיסה', 'חומץ תפוחים', 'ferment', 'levain', 'sourdough']
    t = ing_raw.lower()
    for m in markers:
        if m.lower() in t:
            return True
    return False

def detect_whole_grain_first(ing_raw):
    if not ing_raw:
        return False
    first_ing = ing_raw.split('(')[0].split(',')[0].strip()
    whole_markers = ['מלא', 'מלאה', 'שלם', 'שלמה', 'integral', 'whole']
    return any(m in first_ing for m in whole_markers)

def detect_additives(ing_raw):
    if not ing_raw:
        return []
    found = []
    if re.search(r'E\d{3,4}', ing_raw):
        found.append('E-numbers')
    if any(x in ing_raw for x in ['DATEM', 'E471', 'E472', 'E481', 'E482', 'לציטין']):
        found.append('emulsifiers')
    if any(x in ing_raw for x in ['חמצן', 'ויטמין C', 'E300', 'E301', 'E302']):
        found.append('improvers')
    if any(x in ing_raw for x in ['אנזים', 'enzymes', 'E1100']):
        found.append('enzymes')
    if 'עמילן מעובד' in ing_raw:
        found.append('modified starch')
    return found

products = []
for f in sorted(BSIP2_DIR.glob('*.json')):
    with open(f, encoding='utf-8') as fp:
        t = json.load(fp)

    deg = t.get('degradation_level', '')
    score = t.get('final_score')
    if deg not in ('FULL', 'CAUTIOUS') or score is None:
        continue

    barcode = str(t.get('barcode', '')).strip()
    b0 = barcode_to_bsip0.get(barcode, {})
    ing_raw = b0.get('ingredients_raw', '') or ''
    # Clean cutoff markers
    for marker in ['מאפיינים נוספים', 'ערכים תזונתיים', 'אין להסתמך']:
        idx = ing_raw.find(marker)
        if idx > 10:
            ing_raw = ing_raw[:idx].strip()

    nv = t.get('nutrition', {})
    images = t.get('image_urls') or b0.get('image_urls', [])
    image_url = ''
    for url in images:
        if 'products_large' in url or 'products_zoom' in url:
            image_url = url
            break
    if not image_url and images:
        image_url = images[0]

    products.append({
        'name': t.get('name_he', '?'),
        'barcode': barcode,
        'score': round(float(score)),
        'grade': t.get('final_grade', '?'),
        'category': t.get('category', '?'),
        'fiber': nv.get('dietary_fiber_g'),
        'protein': nv.get('protein_g'),
        'kcal': nv.get('energy_kcal'),
        'sodium': nv.get('sodium_mg'),
        'ferm': detect_fermentation(ing_raw),
        'whole_first': detect_whole_grain_first(ing_raw),
        'additives': detect_additives(ing_raw),
        'ing_short': ing_raw[:120] if ing_raw else '',
        'image_url': image_url,
    })

products.sort(key=lambda x: x['score'], reverse=True)

for i, p in enumerate(products, 1):
    ferm_mark = ' | מחמצת' if p['ferm'] else ''
    fiber_str = ' | fiber=%sg' % p['fiber'] if p['fiber'] else ''
    add_str = ' | adds: %s' % ','.join(p['additives']) if p['additives'] else ''
    print('%3d. [%s/%s] %s (%s)%s%s%s' % (
        i, p['score'], p['grade'], p['name'], p['category'],
        fiber_str, ferm_mark, add_str))
    if p['ing_short']:
        print('     %s' % p['ing_short'])

print('\nTotal coherent: %d' % len(products))
