import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Check cookies-coffee factory_run_001 for the 3 barcodes not found in BSIP0
# These are: 7290013453068, 7296073453840, 7296073453857
import os

cc_dir = r"C:\Bari\02_products\cookies_coffee"
target = {"7290013453068","7296073453840","7296073453857"}

print("=== Searching all cookies-coffee files for 3 missing barcodes ===")
for root, dirs, files in os.walk(cc_dir):
    for fname in files:
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            continue

        def scan_for_bc(obj, depth=0):
            if depth > 3:
                return
            if isinstance(obj, dict):
                bc = str(obj.get("barcode", obj.get("id",""))).strip()
                if bc in target:
                    name = obj.get("name_he", obj.get("name","?"))
                    nutr = obj.get("nutrition", obj.get("normalized_nutrition_per_100g", {}))
                    carbs_raw = nutr.get("carbs_raw") if isinstance(nutr, dict) else None
                    carbs = nutr.get("carbohydrates_g") if isinstance(nutr, dict) else None
                    sugar_raw = nutr.get("sugar_raw") if isinstance(nutr, dict) else None
                    relpath = fpath.replace(cc_dir, "")
                    print(f"  FOUND BC={bc} carbs_raw={carbs_raw} carbs={carbs} sugar_raw={sugar_raw} in {relpath}")
                    print(f"    name={str(name)[:50]}")
                for v in obj.values():
                    scan_for_bc(v, depth+1)
            elif isinstance(obj, list):
                for item in obj:
                    scan_for_bc(item, depth+1)

        scan_for_bc(raw)

# Also check cheese BSIP0 for carbs_raw pattern
print()
print("=== Cheese BSIP0 - checking carbs_raw pattern ===")
with open(r"C:\Bari\02_products\cheese_spreads\bsip0_outputs\cheese_bsip0_raw_20260602T054843.json", encoding="utf-8") as f:
    cdata = json.load(f)

target_cheese = {"7290014758681","4127077","4127329","41445","7290110321277"}
cheese_prods = cdata if isinstance(cdata, list) else cdata.get("products", [])
for p in cheese_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc not in target_cheese:
        continue
    name = p.get("name_he", p.get("name","?"))
    nutr = p.get("nutrition", {})
    carbs_raw = nutr.get("carbs_raw") if isinstance(nutr, dict) else None
    sugar_raw = nutr.get("sugar_raw") if isinstance(nutr, dict) else None
    carbs_g = nutr.get("carbohydrates_g", nutr.get("carbs_g")) if isinstance(nutr, dict) else None
    print(f"  BC={bc}  carbs_raw={carbs_raw}  carbs_g={carbs_g}  sugar_raw={sugar_raw}  name={str(name)[:50]}")

# Same check for milk - look for milk BSIP0 file
print()
print("=== Searching for milk BSIP0 or corpus file ===")
milk_dirs = [
    r"C:\Bari\02_products\milk_and_alternatives",
]
for milk_dir in milk_dirs:
    if os.path.isdir(milk_dir):
        print(f"  Found: {milk_dir}")
        for root, dirs, files in os.walk(milk_dir):
            for fname in files:
                if fname.endswith(".json"):
                    print(f"    {os.path.join(root,fname).replace(milk_dir,'')}")
