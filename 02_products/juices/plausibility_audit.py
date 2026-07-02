"""
BSIP0 plausibility audit over the juices corpus.
Gate: for drinks with no fat/protein/fiber, sugar*4 should account for
a substantial fraction of kcal. Flag where sugar explains <40% of kcal.
"""
import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

FRONTEND_PATH = r'C:\Bari\02_products\juices\juices_frontend_v3.json'
BSIP2_DIR = r'C:\Bari\02_products\juices\bsip2_outputs\run_task389_rescore_002\products'

with open(FRONTEND_PATH, 'r', encoding='utf-8') as f:
    frontend = json.load(f)

products = frontend.get('products', [])
print(f'=== PLAUSIBILITY AUDIT: juices_frontend_v3.json ({len(products)} products) ===')
print()
print(f'{"ID":<8} {"KCAL":>6} {"SUGAR":>6} {"SUGAR%KCAL":>10} {"FLAG"}')
print('-' * 60)

issues = []
for p in products:
    pid = p.get('id', '?')
    barcode = str(p.get('barcode', '?'))

    # Use expansion.nutrition for the full panel
    nutr = (p.get('expansion') or {}).get('nutrition') or {}
    kcal = nutr.get('energyKcal')
    sugar = nutr.get('sugar')
    fat = nutr.get('fat')
    protein = nutr.get('protein') or 0.0
    fiber = nutr.get('fiber') or 0.0

    if kcal is None or sugar is None:
        flag = 'MISSING_DATA'
        print(f'{pid:<8} {str(kcal):>6} {str(sugar):>6} {"N/A":>10} {flag}')
        continue

    sugar_kcal = sugar * 4.0
    sugar_pct = (sugar_kcal / kcal * 100) if kcal > 0 else 0.0

    # Is this a structurally empty macro product? (liquid with no fat/protein/fiber)
    is_empty = (fat is None or fat < 0.5) and protein < 0.5 and fiber < 0.5

    if is_empty and sugar_pct < 40.0:
        flag = 'IMPLAUSIBLE'
        issues.append({
            'id': pid,
            'barcode': barcode,
            'kcal': kcal,
            'sugar_g': sugar,
            'sugar_pct_of_kcal': round(sugar_pct, 1),
            'note': 'sugar explains <40% of kcal in empty-macro drink',
        })
    elif is_empty and sugar_pct < 60.0:
        flag = 'WARN_LOW_RATIO'
    else:
        flag = 'OK'

    print(f'{pid:<8} {kcal:>6.1f} {sugar:>6.2f} {sugar_pct:>9.1f}% {flag}')

print()
print(f'=== ISSUES FOUND: {len(issues)} ===')
for iss in issues:
    print(json.dumps(iss, ensure_ascii=False))

print()
print(f'Total products audited: {len(products)}')
print(f'Implausible: {len(issues)}')
print(f'Result: {"ONLY jc-021 is implausible" if len(issues) == 1 and issues[0]["id"] == "jc-021" else "SEE ISSUES ABOVE"}')
