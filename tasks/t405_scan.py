import os, glob, json, sys
from collections import Counter

os.chdir(r"C:\Bari")

count_with_ingr = 0
count_total = 0
files_with_ingr = []

skip_names = {'run_report', 'curation_report', 'skipped', 'approved_candidates',
              'capture_status', 'discovery', 'dispatch', 'shelf_map',
              'corpus_filter', 'bsip0_gate', 'brand_backfill'}

for f in glob.glob(r'02_products/**/*.json', recursive=True):
    bn = os.path.basename(f).replace('.json', '')
    if any(x in bn for x in skip_names):
        continue
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            continue
        count_total += 1
        ingr = data.get('ingredients_text_he') or data.get('ingredients_raw')
        if ingr and isinstance(ingr, str) and len(ingr.strip()) > 0:
            count_with_ingr += 1
            files_with_ingr.append(f)
    except Exception:
        pass

print(f'Total product JSON files scanned: {count_total}')
print(f'Files with ingredient text: {count_with_ingr}')
print()
print('Breakdown by category:')
cats = Counter()
for f in files_with_ingr:
    parts = f.replace('\\', '/').split('/')
    if len(parts) >= 3:
        cats[parts[1]] += 1
for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
    print(f'  {cat}: {cnt}')
print()
print('All files with ingredients:')
for f in files_with_ingr:
    print(f'  {f}')
