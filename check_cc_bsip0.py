import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

target = {"7290119043149","7290017962139","7290013453068","7296073453840","7296073453857"}

with open(r"C:\Bari\02_products\cookies_coffee\bsip0_outputs\cookies_coffee_bsip0_raw_20260613T163431.json", encoding="utf-8") as f:
    d = json.load(f)

prods = d if isinstance(d, list) else d.get("products", list(d.values()))
print(f"Total records: {len(prods)}")
print()

for p in prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc not in target:
        continue
    name = str(p.get("name_he", p.get("name", "?")))
    nutr = p.get("nutrition", {})
    print(f"BC={bc}  name={name[:60]}")
    print(f"  nutrition dict: {nutr}")
    # Look for any carb-related fields at any level
    for k,v in p.items():
        if "carb" in k.lower() or "sugar" in k.lower():
            print(f"  TOP-LEVEL {k}={v}")
        elif isinstance(v, dict):
            for kk,vv in v.items():
                if "carb" in kk.lower() or "sugar" in kk.lower():
                    print(f"  {k}.{kk}={vv}")
    print()
