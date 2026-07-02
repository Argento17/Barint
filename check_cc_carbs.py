import json, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

target = {"7290119043149","7290017962139","7290013453068","7296073453840","7296073453857"}

# Check cookies-coffee frontend for any carbs data
with open(r"C:\bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v2.json", encoding="utf-8") as f:
    d = json.load(f)
print("=== Cookies-Coffee Frontend Expansion.Nutrition for target products ===")
for p in d["products"]:
    bc = str(p.get("barcode",""))
    if bc in target:
        exp = p.get("expansion", {})
        nutr = exp.get("nutrition", {})
        name = p.get("name","?")
        print(f"  BC={bc}  nutr={nutr}  name={name[:50]}")

# Check cookies-coffee BSIP2 run outputs (traces)
print()
print("=== Cookies-Coffee BSIP2 traces ===")
bsip2_dir = r"C:\Bari\02_products\cookies_coffee\bsip2_outputs"
for run_dir in os.listdir(bsip2_dir):
    run_path = os.path.join(bsip2_dir, run_dir)
    if not os.path.isdir(run_path):
        continue
    for fname in os.listdir(run_path):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(run_path, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        # list or dict?
        prods = []
        if isinstance(data, list):
            prods = data
        elif isinstance(data, dict):
            prods = data.get("products", data.get("scored_products", data.get("corpus", [])))
            if not isinstance(prods, list):
                # might be a single product
                bc = str(data.get("barcode", data.get("id","")))
                if bc in target:
                    prods = [data]
        for p in prods:
            if not isinstance(p, dict):
                continue
            bc = str(p.get("barcode", p.get("id","")))
            if bc in target:
                l1 = p.get("L1_observed_signals", {})
                nutr = p.get("normalized_nutrition_per_100g", {})
                carbs = l1.get("carbohydrates_g") or nutr.get("carbohydrates_g")
                sugar = l1.get("sugars_g") or nutr.get("sugars_g")
                print(f"  [{run_dir}/{fname}] BC={bc}  carbs={carbs}  sugar={sugar}")

# Check the brined cheeses bsip0 more carefully
print()
print("=== Brined Cheeses BSIP0 structure check ===")
bsip0_path = r"C:\Bari\02_products\brined_cheeses\bsip0_outputs\brined_cheese_bsip0_raw_20260613T065721.json"
with open(bsip0_path, encoding="utf-8") as f:
    bdata = json.load(f)
print(f"Top-level type: {type(bdata).__name__}")
if isinstance(bdata, dict):
    print(f"Top keys: {list(bdata.keys())[:10]}")
    prods = bdata.get("products", [])
elif isinstance(bdata, list):
    prods = bdata
else:
    prods = []

target_brined = {"4861360","48413","369617"}
print(f"Loaded {len(prods)} records. Searching for {target_brined}")
for p in prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc in target_brined:
        # Look everywhere for carbs
        found = {}
        for k,v in p.items():
            if isinstance(v, dict):
                for kk,vv in v.items():
                    if "carb" in kk.lower():
                        found[f"{k}.{kk}"] = vv
            elif "carb" in k.lower():
                found[k] = v
        print(f"  BC={bc}  carb-fields: {found}  name={str(p.get('name','?'))[:50]}")
        print(f"  All keys: {list(p.keys())[:20]}")

# Check cereals BSIP0 for rice puffs
print()
print("=== Cereals BSIP0 for rice puffs (7297488098688) ===")
cer_bsip0 = r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json"
with open(cer_bsip0, encoding="utf-8") as f:
    cdata = json.load(f)
target_cer = "7297488098688"
prods = cdata if isinstance(cdata, list) else cdata.get("products", list(cdata.values()))
for p in prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc == target_cer:
        found = {}
        for k,v in p.items():
            if isinstance(v, dict):
                for kk,vv in v.items():
                    if "carb" in kk.lower() or "sugar" in kk.lower():
                        found[f"{k}.{kk}"] = vv
            elif "carb" in k.lower() or "sugar" in k.lower():
                found[k] = v
        print(f"  BC={bc}  carb/sugar fields: {found}  name={str(p.get('name','?'))[:60]}")
