import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# === CHEESE - get ALL null-sugar products' carbs_raw from BSIP0 ===
print("=== CHEESE BSIP0 carbs_raw for ALL null-sugar products ===")

target_cheese = {
    "7290014758681","4127077","4127329","41445","7290110321277",
    "7290116934280","4127336","41452","7290108506624","56272",
    "7290116931241","7290116934365","7290014759084","7290116935409",
    "7290014762831","7290116936604","4129101","4129156","7290116931982",
    "7290116933078",
}

with open(r"C:\Bari\02_products\cheese_spreads\bsip0_outputs\cheese_bsip0_raw_20260602T054843.json", encoding="utf-8") as f:
    cdata = json.load(f)

cheese_prods = cdata if isinstance(cdata, list) else cdata.get("products", [])

cheese_results = {}
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
    # Try to parse carbs_raw to float
    carbs_g = None
    if carbs_raw is not None and str(carbs_raw).strip() != "":
        try:
            carbs_g = float(str(carbs_raw).strip().replace(",","."))
        except Exception:
            pass
    fires = carbs_g >= 5.0 if carbs_g is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs_raw={str(carbs_raw):<8} carbs_g={str(carbs_g):<8} sugar_raw='{sugar_raw}'  status={status}  {str(name)[:50]}")
    cheese_results[bc] = (carbs_g, fires, name)

for bc in target_cheese:
    if bc not in cheese_results:
        print(f"  BC={bc:<22} NOT_FOUND")
        cheese_results[bc] = (None, None, "not_found")

print()
fires_cheese = [(bc, d) for bc,d in cheese_results.items() if d[1] is True]
print(f"CHEESE FIRES: {len(fires_cheese)}")
for bc, d in fires_cheese:
    print(f"  BC={bc}  carbs={d[0]}  {str(d[2])[:50]}")


# === BRINED CHEESES ===
print()
print("=== BRINED CHEESES BSIP0 carbs_raw ===")

target_brined = {"4861360","48413","369617"}

with open(r"C:\Bari\02_products\brined_cheeses\bsip0_outputs\brined_cheese_bsip0_raw_20260613T065721.json", encoding="utf-8") as f:
    bdata = json.load(f)

brined_prods = bdata if isinstance(bdata, list) else bdata.get("products", [])

brined_results = {}
for p in brined_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc not in target_brined:
        continue
    name = p.get("name_he", p.get("name","?"))
    nutr = p.get("nutrition", {})
    carbs_raw = nutr.get("carbs_raw") if isinstance(nutr, dict) else None
    sugar_raw = nutr.get("sugar_raw") if isinstance(nutr, dict) else None
    carbs_g = None
    if carbs_raw is not None and str(carbs_raw).strip() != "":
        try:
            carbs_g = float(str(carbs_raw).strip().replace(",","."))
        except Exception:
            pass
    fires = carbs_g >= 5.0 if carbs_g is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs_raw={str(carbs_raw):<8} carbs_g={str(carbs_g):<8} sugar_raw='{sugar_raw}'  status={status}  {str(name)[:50]}")
    brined_results[bc] = (carbs_g, fires, name)

for bc in target_brined:
    if bc not in brined_results:
        print(f"  BC={bc:<22} NOT_FOUND")

print()
fires_brined = [(bc, d) for bc,d in brined_results.items() if d[1] is True]
print(f"BRINED FIRES: {len(fires_brined)}")


# === BREAKFAST CEREALS ===
print()
print("=== CEREALS BSIP0 carbs_raw for rice puffs ===")

target_cer = {"7297488098688"}

with open(r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json", encoding="utf-8") as f:
    cdata2 = json.load(f)

cer_prods = cdata2 if isinstance(cdata2, list) else cdata2.get("products", list(cdata2.values()))

for p in cer_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id",""))).strip()
    if bc not in target_cer:
        continue
    name = p.get("name_he", p.get("name","?"))
    nutr = p.get("nutrition", {})
    carbs_raw = nutr.get("carbs_raw") if isinstance(nutr, dict) else None
    sugar_raw = nutr.get("sugar_raw") if isinstance(nutr, dict) else None
    carbs_g = None
    if carbs_raw is not None and str(carbs_raw).strip() != "":
        try:
            carbs_g = float(str(carbs_raw).strip().replace(",","."))
        except Exception:
            pass
    fires = carbs_g >= 5.0 if carbs_g is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs_raw={str(carbs_raw):<8} carbs_g={str(carbs_g):<8} sugar_raw='{sugar_raw}'  status={status}  {str(name)[:60]}")
