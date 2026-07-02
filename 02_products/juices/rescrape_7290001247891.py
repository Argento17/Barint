"""
TASK-404: Re-scrape barcode 7290001247891 from all reachable retailers.
Attempt: Shufersal (storefront + price feed API) → Victory → Rami Levy.
Goal: recover the true per-100ml sugar and kcal values.
"""
import sys, os, json
sys.path.insert(0, r'C:\Bari\integrations')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import requests

BARCODE = '7290001247891'
UA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36',
    'Accept': 'application/json, text/html,*/*',
    'Accept-Language': 'he,en;q=0.9',
}

results = {}

# ========================
# 1. Shufersal storefront API
# ========================
print('=== 1. Shufersal storefront product API ===')
try:
    # Try the standard product page by barcode
    url1 = f'https://www.shufersal.co.il/online/he/p/{BARCODE}'
    r = requests.get(url1, timeout=20, headers=UA, allow_redirects=True)
    print(f'  Shufersal product page: HTTP {r.status_code}, len={len(r.content)}')
    results['shufersal_product_page'] = r.status_code
    if r.status_code == 200 and BARCODE in r.text:
        idx = r.text.find(BARCODE)
        print(f'  Barcode found at offset {idx}')
        print('  Context:', r.text[max(0,idx-200):idx+400])
    else:
        print(f'  Barcode NOT in response or non-200')
except Exception as e:
    print(f'  ERROR: {e}')
    results['shufersal_product_page'] = str(e)

print()

# Try Shufersal search API with term
print('=== 2. Shufersal search API — Hebrew name ===')
try:
    import urllib.parse
    term = 'ספרינג נקטר אפרסקים'
    encoded = urllib.parse.quote(term)
    url2 = f'https://www.shufersal.co.il/online/he/search/results?q={encoded}%3Arelevance&limit=10'
    r2 = requests.get(url2, timeout=20, headers=UA)
    print(f'  Status: {r2.status_code}, len={len(r2.content)}')
    if r2.status_code == 200:
        try:
            data = r2.json()
            results_list = data.get('results', [])
            print(f'  Results count: {len(results_list)}')
            for item in results_list[:10]:
                code = item.get('code', '')
                name = item.get('name', '')
                print(f'    barcode={code} name={name[:80]}')
                if code == BARCODE or BARCODE in str(item):
                    print(f'    *** TARGET FOUND ***')
                    print(json.dumps(item, ensure_ascii=False, indent=2)[:2000])
                    results['shufersal_target_found'] = True
            if not results_list:
                print('  Empty results for Hebrew search')
                results['shufersal_target_found'] = False
        except Exception as je:
            print(f'  JSON parse error: {je}')
            print('  Body snippet:', r2.text[:500])
except Exception as e:
    print(f'  ERROR: {e}')

print()

# ========================
# 3. Try Victory API
# ========================
print('=== 3. Victory store API ===')
try:
    # Victory uses a different search format
    url3 = f'https://api.victoryonline.co.il/api/items/{BARCODE}'
    r3 = requests.get(url3, timeout=15, headers=UA)
    print(f'  Victory item API: {r3.status_code}, len={len(r3.content)}')
    results['victory_item_api'] = r3.status_code
    if r3.status_code == 200:
        print('  Body:', r3.text[:500])
except Exception as e:
    print(f'  ERROR: {e}')

try:
    # Try Victory search
    import urllib.parse
    term2 = 'נקטר אפרסקים ספרינג'
    url4 = f'https://www.victoryonline.co.il/search?q={urllib.parse.quote(term2)}'
    r4 = requests.get(url4, timeout=15, headers=UA)
    print(f'  Victory search: {r4.status_code}, len={len(r4.content)}')
    if r4.status_code == 200:
        if BARCODE in r4.text:
            idx4 = r4.text.find(BARCODE)
            print(f'  BARCODE FOUND in Victory search at offset {idx4}')
            print('  Context:', r4.text[max(0,idx4-100):idx4+400])
            results['victory_target_found'] = True
        else:
            print(f'  Barcode not found in Victory search response')
            results['victory_target_found'] = False
except Exception as e:
    print(f'  ERROR: {e}')

print()

# ========================
# 4. Rami Levy
# ========================
print('=== 4. Rami Levy probe ===')
try:
    r5 = requests.get('https://www.ramilevi.co.il', timeout=10, headers=UA)
    print(f'  Rami Levy home: {r5.status_code}')
    results['rami_levy'] = r5.status_code
except Exception as e:
    print(f'  Rami Levy: {e}')
    results['rami_levy'] = str(e)

print()
print('=== SUMMARY ===')
print(json.dumps(results, ensure_ascii=False, indent=2))
print()

# ========================
# 5. Check existing Shufersal BSIP0 output for this barcode
# ========================
print('=== 5. Existing BSIP0 Shufersal output check ===')
import pathlib
bsip0_dir = pathlib.Path(r'C:\Bari\02_products\juices\bsip0_outputs')
for f in bsip0_dir.glob('*.json'):
    with open(f, 'r', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
        except:
            continue
    products = data.get('products', [])
    for prod in products:
        if str(prod.get('barcode', '')) == BARCODE:
            print(f'  Found in {f.name}:')
            print(json.dumps(prod, ensure_ascii=False, indent=2)[:2000])
            break
    else:
        retailer = data.get('retailer', f.name)
        print(f'  {f.name} ({retailer}): barcode NOT FOUND ({len(products)} products in file)')
