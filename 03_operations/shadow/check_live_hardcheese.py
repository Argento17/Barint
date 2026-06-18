import json

data = json.loads(open(r'C:\Bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v2.json', encoding='utf-8').read())
moved_barcodes = ['7290000062488','7290000062518','7290000062563','7290000062570','7290000425009','7290000425016','7290000425023','7290010644743','7290010644750','7290010644767','7290010644774']
products = data.get('products', [])
print(f"Total products in hard_cheeses live JSON: {len(products)}")
found = 0
for p in products:
    bc = str(p.get('barcode',''))
    if bc in moved_barcodes:
        found += 1
        name = p.get('nameHe', p.get('name', ''))[:40]
        score = p.get('bsipScore', p.get('score'))
        grade = p.get('grade')
        print(f"  LIVE: {bc} | {name.encode('ascii', errors='replace').decode()} | score={score} grade={grade}")
print(f"\nFound {found} of {len(moved_barcodes)} moved products in live hard_cheeses JSON")
