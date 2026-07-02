import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'C:\Bari\bari-web\src\data\comparisons\snacks_frontend_v5.json', encoding='utf-8') as f:
    data = json.load(f)

prods = data['products']
print(f"Total: {len(prods)}")
print("\nTop 20 by score:")
for p in prods[:20]:
    score = p.get('score')
    grade = p.get('grade', '?')
    brand = p.get('brand', '')[:20]
    name = p.get('name_he', '')[:45]
    kcal = (p.get('nutrition_per_100g') or {}).get('energy_kcal', '?')
    has_ingr = bool((p.get('nutrition_per_100g') or {}).get('energy_kcal'))
    print(f"  {score:5.1f}/{grade} | {brand:<20} | {name}")

print("\nBottom 10:")
for p in prods[-10:]:
    score = p.get('score')
    grade = p.get('grade', '?')
    brand = p.get('brand', '')[:20]
    name = p.get('name_he', '')[:45]
    print(f"  {score:5.1f}/{grade} | {brand:<20} | {name}")

# Check brand coverage
no_brand = [p for p in prods if not p.get('brand', '').strip()]
no_ingr = [p for p in prods if not p.get('nutrition_per_100g')]
print(f"\nNo brand: {len(no_brand)}")
print(f"No nutrition: {len(no_ingr)}")

# Grade dist
from collections import Counter
grades = Counter(p.get('grade','?') for p in prods)
print(f"Grade distribution: {dict(sorted(grades.items()))}")
