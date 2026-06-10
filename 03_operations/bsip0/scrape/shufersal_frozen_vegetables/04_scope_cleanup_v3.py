"""
Scope cleanup v3: strictly filter only definitely-wrong products.
Keep all frozen/maybe-frozen produce. BSIP0 is a discovery census, not final curation.
"""
import sys, io, json, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = pathlib.Path(r"C:\Bari")
V2_PATH = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs" / "bsip0_shufersal_frozen_vegetables_v2.json"
OUTPUT_PATH = BASE / "02_products" / "frozen_vegetables" / "bsip0_outputs" / "bsip0_shufersal_frozen_vegetables_v3.json"

d = json.loads(V2_PATH.read_text(encoding="utf-8"))

# Only exclude things that are DEFINITELY NOT frozen vegetables
EXCLUSIONS = {
    "מרכך כביסה": "not_food: laundry softener",
    "מגבונים לחים": "not_food: wet wipes",
    "מגבון": "not_food: wipes",
    "קוקוס לשתיה": "not_vegetable: coconut drink",
    "לשון קפואה": "not_vegetable: frozen beef tongue",
    "בדין": "not_food: flowers",
    "זר ": "not_food: bouquet",
}

CAT_FROZEN_VEG = ["A160501", "A1605"]

products_clean = []
scope_excluded_v3 = []

for p in d["products"]:
    name = p.get("name_he") or ""
    code = p["product_code"]
    excluded = False
    
    for kw, reason in EXCLUSIONS.items():
        if kw in name:
            scope_excluded_v3.append({"code": code, "name": name, "reason": reason})
            excluded = True
            break
    
    if not excluded:
        products_clean.append(p)

d["products"] = products_clean
d["product_count"] = len(products_clean)
d["scope_excluded_v3"] = scope_excluded_v3
d["scope_excluded_total_v3"] = d.get("scope_excluded_count", 0) + len(scope_excluded_v3)
d["completeness"] = {
    "with_nutrition": sum(1 for p in products_clean if p.get("nutrition_raw")),
    "with_ingredients": sum(1 for p in products_clean if p.get("ingredients_raw")),
    "with_barcode_jsonld": sum(1 for p in products_clean if p.get("barcode_ld")),
    "with_image_url": sum(1 for p in products_clean if p.get("image_url") or p.get("image_url_jsonld")),
    "with_product_url": sum(1 for p in products_clean if p.get("product_url")),
    "with_raw_html": sum(1 for p in products_clean if p.get("raw_html_path")),
}

OUTPUT_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Products in scope: {len(products_clean)}")
print(f"Additional exclusions: {len(scope_excluded_v3)}")
for k, v in d["completeness"].items():
    print(f"  {k}: {v}/{len(products_clean)}")
print(f"\nExcluded:")
for e in scope_excluded_v3:
    print(f"  [{e['reason']}] {e['code']}: {e['name'][:50]}")

# Show remaining products without nutrition or ingredients
missing_nut = [p for p in products_clean if not p.get("nutrition_raw")]
missing_ing = [p for p in products_clean if not p.get("ingredients_raw")]
print(f"\nMissing nutrition ({len(missing_nut)}):")
for p in missing_nut:
    print(f"  {p['product_code']}: {(p.get('name_he') or '?')[:60]}")
