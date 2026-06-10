import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

files = {
    "maadanim": r"C:\bari\bari-web\src\data\comparisons\maadanim_frontend_v3.json",
    "cheese":   r"C:\bari\bari-web\src\data\comparisons\cheese_frontend_v2.json",
    "granola":  r"C:\bari\bari-web\src\data\comparisons\granola_frontend_v1.json",
}

for cat, fpath in files.items():
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", [])
    has_field = sum(1 for p in products if "barcode" in p)
    has_value = sum(1 for p in products if p.get("barcode") not in (None, ""))
    print(f"  {cat}: {has_field}/{len(products)} have barcode field, {has_value} non-null")
    if has_value > 0:
        for p in products[:3]:
            if p.get("barcode"):
                print(f"    sample: {p['id']} barcode={p.get('barcode')}")

print()
# Also check what fields each format has
print("=== FIELD SURVEY (first product of each category) ===")
all_files = {
    "hummus": r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v5.json",
    "yogurts": r"C:\bari\bari-web\src\data\comparisons\yogurts_frontend_v2.json",
    "cereals": r"C:\bari\bari-web\src\data\comparisons\cereals_frontend_v1.json",
    "granola": r"C:\bari\bari-web\src\data\comparisons\granola_frontend_v1.json",
    "snacks":  r"C:\bari\bari-web\src\data\comparisons\snacks_frontend_v2.json",
    "maadanim":r"C:\bari\bari-web\src\data\comparisons\maadanim_frontend_v3.json",
    "cheese":  r"C:\bari\bari-web\src\data\comparisons\cheese_frontend_v2.json",
    "butter":  r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json",
    "bread":   r"C:\bari\bari-web\src\data\comparisons\bread_frontend_v2.json",
}

for cat, fpath in all_files.items():
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", [])
    if products:
        keys = list(products[0].keys())
        has_barcode = "barcode" in keys
        has_retailer = "retailer" in keys or any("retailer" in p for p in products)
        print(f"  {cat}: fields={keys} | barcode_present={has_barcode}")
