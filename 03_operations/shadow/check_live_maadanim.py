import json, pathlib

moved_barcodes = [
    '2385455', '554532', '6492616', '7290011499129',
    '7290011499327', '7290017065236', '7290017065663',
    '7290000062488','7290000062518','7290000062563','7290000062570',
    '7290000425009','7290000425016','7290000425023','7290010644743',
    '7290010644750','7290010644767','7290010644774'
]

live_dir = pathlib.Path(r'C:\Bari\bari-web\src\data\comparisons')
for jf in sorted(live_dir.glob('*.json')):
    if 'archive' in str(jf):
        continue
    try:
        data = json.loads(jf.read_text(encoding='utf-8'))
    except Exception:
        continue
    products = data.get('products', [])
    for p in products:
        bc = str(p.get('barcode', p.get('id', '')))
        if bc in moved_barcodes:
            name = p.get('nameHe', p.get('name', ''))[:40]
            score = p.get('bsipScore', p.get('score'))
            grade = p.get('grade')
            print(f"LIVE in {jf.name}: {bc} | {name.encode('ascii', errors='replace').decode()} | score={score} grade={grade}")

print("\nCheck complete.")
