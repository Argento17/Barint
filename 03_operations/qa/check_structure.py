import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Check whether barcode field exists at all (vs null) in different categories
# and spot-check butter insufficient confidence

files = {
    "hummus": r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v5.json",
    "yogurts": r"C:\bari\bari-web\src\data\comparisons\yogurts_frontend_v2.json",
    "butter": r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json",
    "cereals": r"C:\bari\bari-web\src\data\comparisons\cereals_frontend_v1.json",
    "bread": r"C:\bari\bari-web\src\data\comparisons\bread_frontend_v2.json",
    "snacks": r"C:\bari\bari-web\src\data\comparisons\snacks_frontend_v2.json",
}

print("=== BARCODE FIELD PRESENCE CHECK ===")
for cat, fpath in files.items():
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", [])
    has_field = sum(1 for p in products if "barcode" in p)
    is_null   = sum(1 for p in products if p.get("barcode") is None)
    has_value = sum(1 for p in products if p.get("barcode") not in (None, ""))
    print(f"  {cat}: {has_field}/{len(products)} have field, {has_value} have non-null value, {is_null} are null")
    if has_value > 0 and has_value < len(products):
        sample = next(p for p in products if p.get("barcode") not in (None, ""))
        print(f"    sample barcode: {sample.get('barcode')} | id: {sample.get('id')}")

print()
print("=== BUTTER: confidence=insufficient products (score/grade check) ===")
with open(r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json", encoding="utf-8") as f:
    data = json.load(f)

for p in data["products"]:
    if p.get("confidence") == "insufficient":
        print(f"  {p['id']} | score={p.get('score')} | grade={p.get('grade')} | confidence=insufficient")

print()
print("=== HUMMUS: check 3 grade mismatches (score=65, grade=C) ===")
with open(r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v5.json", encoding="utf-8") as f:
    data = json.load(f)
for p in data["products"]:
    if p.get("score") == 65 and p.get("grade") == "C":
        print(f"  {p['id']} | score={p.get('score')} | grade={p.get('grade')}")

print()
print("=== CHEESE: check 2 grade mismatches (score=81, grade=B) ===")
with open(r"C:\bari\bari-web\src\data\comparisons\cheese_frontend_v2.json", encoding="utf-8") as f:
    data = json.load(f)
for p in data["products"]:
    if p.get("score") == 81 and p.get("grade") == "B":
        print(f"  {p['id']} | {p['name']} | score={p.get('score')} | grade={p.get('grade')}")

print()
print("=== BUTTER: rowVerdict check for bleed text ===")
with open(r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v2.json", encoding="utf-8") as f:
    data = json.load(f)
from collections import Counter
rv_counter = Counter(p.get("rowVerdict", "") for p in data["products"] if p.get("rowVerdict"))
print("  rowVerdict value counts:")
for rv, cnt in rv_counter.most_common():
    print(f"    [{cnt}x] '{rv}'")

print()
print("=== MAADANIM: check 3 grade mismatches ===")
with open(r"C:\bari\bari-web\src\data\comparisons\maadanim_frontend_v3.json", encoding="utf-8") as f:
    data = json.load(f)
for p in data["products"]:
    if p.get("score") in (50, 35) and p.get("grade") in ("D", "E"):
        expected_grade = "C" if p.get("score") == 50 else "D"
        if p.get("grade") != expected_grade:
            print(f"  {p['id']} | {p['name']} | score={p.get('score')} | grade={p.get('grade')} | expects={expected_grade}")

print()
print("=== CEREALS: check grade mismatches ===")
with open(r"C:\bari\bari-web\src\data\comparisons\cereals_frontend_v1.json", encoding="utf-8") as f:
    data = json.load(f)
for p in data["products"]:
    sc = p.get("score")
    gr = p.get("grade")
    if sc == 65 and gr == "C":
        print(f"  {p['id']} | {p['name']} | score={sc} | grade={gr} | expects=B")
    if sc == 35 and gr == "E":
        print(f"  {p['id']} | {p['name']} | score={sc} | grade={gr} | expects=D")

print()
print("=== HUMMUS: rowVerdict null — are these display-only (no-data) products? ===")
with open(r"C:\bari\bari-web\src\data\comparisons\hummus_frontend_v5.json", encoding="utf-8") as f:
    data = json.load(f)
null_rv = [p for p in data["products"] if p.get("rowVerdict") is None]
print(f"  {len(null_rv)} products with null rowVerdict")
for p in null_rv[:5]:
    print(f"    {p['id']} | score={p.get('score')} | grade={p.get('grade')} | confidence={p.get('confidence')}")
