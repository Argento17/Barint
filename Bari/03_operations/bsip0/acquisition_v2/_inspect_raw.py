import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAW = r"C:\Bari\02_products\bread_retail_002\real_bread_retail_002_v2_20260525T165557_bsip0_raw.json"

with open(RAW, encoding="utf-8") as f:
    products = json.load(f)

print(f"Total products: {len(products)}")
p = products[0]
print(f"Top-level keys: {list(p.keys())}")
nutr = p.get("nutrition", {})
print(f"Nutrition keys: {list(nutr.keys())}")
print(f"name_he: {p.get('name_he')}")
print(f"barcode: {p.get('barcode')}")
print(f"source_url: {p.get('source_url','')[:80]}")
print(f"energy_kcal_raw: {nutr.get('energy_kcal_raw')}")
print(f"fiber_raw: {nutr.get('fiber_raw')}")
print(f"category_raw: {p.get('category_raw','')[:60]}")
print(f"ingredients: {p.get('ingredients_raw','')[:120]}")
print()

n_nutr = sum(1 for p in products if p.get("nutrition", {}).get("energy_kcal_raw", ""))
n_ingr = sum(1 for p in products if p.get("ingredients_raw", ""))
n_fiber = sum(1 for p in products if p.get("nutrition", {}).get("fiber_raw", ""))
print(f"With energy: {n_nutr}/{len(products)}")
print(f"With fiber:  {n_fiber}/{len(products)}")
print(f"With ingr:   {n_ingr}/{len(products)}")

print("\n--- Sample products ---")
for p in products[:15]:
    nutr = p.get("nutrition", {})
    print(f"  {p.get('name_he',''):<35} | {nutr.get('energy_kcal_raw',''):>5} kcal | fiber={nutr.get('fiber_raw',''):>5} | ingr={bool(p.get('ingredients_raw',''))}")
