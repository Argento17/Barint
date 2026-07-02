import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v2.json', encoding='utf-8') as f:
    sn_live = json.load(f)

print("=== LIVE SNACKS: all products with score < 40 ===")
for p in sorted(sn_live['products'], key=lambda x: x['score']):
    nn = p.get('expansion', {}).get('nutrition', {})
    lf = p.get('expansion', {}).get('limitingFactors', [])
    print(f"\n  {p['score']}  {p['grade']}  {p['barcode']}  {p['name'][:50]}")
    print(f"  kcal={nn.get('energyKcal')} fat={nn.get('fat')} sat_fat={nn.get('saturatedFat')} sodium={nn.get('sodium')} sugar={nn.get('sugar')}")
    print(f"  limitingFactors: {lf}")
    print(f"  insightLine: {p.get('insightLine','')[:80]}")

print("\n\n=== LIVE SNACKS: all 18 products (barcode check) ===")
for p in sorted(sn_live['products'], key=lambda x: -x['score']):
    print(f"  {p['score']:5.1f}  {p['grade']}  {p['barcode']}  {p['name'][:50]}")

print(f"\nMeta: {sn_live.get('_meta', {})}")
