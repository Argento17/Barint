"""
Check carbohydrates for null-sugar products whose carbs were unknown.
Uses proper field access for hard-cheeses BSIP1 (flat structure, fields at root)
and other upstream sources.
"""
import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_float(record: dict, *keys):
    """Get first non-None numeric value from record across candidate keys."""
    for k in keys:
        v = record.get(k)
        if v is not None:
            try:
                return float(v)
            except (ValueError, TypeError):
                pass
    return None


# ─── HARD CHEESES ─────────────────────────────────────────────────────────────
print("=" * 80)
print("HARD CHEESES: checking carbs from BSIP1 files (flat structure)")
print("=" * 80)

bsip1_dir = r"C:\Bari\02_products\hard_cheeses\bsip1_outputs"
target_hc_barcodes = {
    "7290108502725", "7290019635192", "7290110324872", "7290102396672",
    "7290110323301", "7290116931524", "8711528211138", "7290004122348",
    "7290004137311", "7290102397204", "7290017065434", "7290108501346",
    "7290117265888", "7290117265918", "7290102394463", "7290014760912",
    "7290000057088", "7290004122683", "7290004125776", "7290014763395",
    "7290110320867",
}

hc_results = {}
for fname in os.listdir(bsip1_dir):
    if not fname.endswith(".json"):
        continue
    fpath = os.path.join(bsip1_dir, fname)
    with open(fpath, encoding="utf-8") as f:
        d = json.load(f)
    bc = str(d.get("barcode", "")).strip()
    if bc not in target_hc_barcodes:
        continue
    # Hard-cheese BSIP1: fields are flat at root level
    carbs = get_float(d, "carbohydrates_g", "carbs_g")
    sugar = get_float(d, "sugars_g", "sugar_g")
    name = d.get("canonical_name_he", d.get("name", "?"))
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    hc_results[bc] = (carbs, sugar, fires, name)

# Missing ones
for bc in target_hc_barcodes:
    if bc not in hc_results:
        print(f"  BC={bc:<22} NOT_FOUND in bsip1_outputs")
        hc_results[bc] = (None, None, None, "not_found")


# ─── CHEESE SPREADS ───────────────────────────────────────────────────────────
print()
print("=" * 80)
print("CHEESE (spreads/cottage): checking carbs from BSIP0 raw")
print("=" * 80)

cheese_bsip0 = r"C:\Bari\02_products\cheese_spreads\bsip0_outputs\cheese_bsip0_raw_20260602T054843.json"
target_cheese_barcodes = {
    "7290014758681", "4127077", "4127329", "41445", "7290110321277",
    "7290116934280", "4127336", "41452", "7290108506624", "56272",
    "7290116931241", "7290116934365", "7290014759084", "7290116935409",
    "7290014762831", "7290116936604", "4129101", "4129156", "7290116931982",
    "7290116933078",
}

cheese_results = {}
with open(cheese_bsip0, encoding="utf-8") as f:
    cheese_data = json.load(f)

if isinstance(cheese_data, dict) and "products" in cheese_data:
    cheese_prods = cheese_data["products"]
elif isinstance(cheese_data, list):
    cheese_prods = cheese_data
else:
    # Try factory_run outputs which might have different structure
    cheese_prods = list(cheese_data.values()) if isinstance(cheese_data, dict) else []

print(f"  Loaded {len(cheese_prods)} records from BSIP0")

for p in cheese_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id", ""))).strip()
    if bc not in target_cheese_barcodes:
        continue
    # Check various structures
    nutr = (p.get("normalized_nutrition_per_100g") or
            p.get("nutrition_per_100g") or
            p.get("nutrition") or {})
    if not isinstance(nutr, dict):
        nutr = {}
    carbs = (get_float(nutr, "carbohydrates_g", "carbs_g") or
             get_float(p, "carbohydrates_g", "carbs_g"))
    sugar = (get_float(nutr, "sugars_g", "sugar_g") or
             get_float(p, "sugars_g", "sugar_g"))
    name = p.get("name", p.get("product_name", p.get("name_he", "?")))
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    cheese_results[bc] = (carbs, sugar, fires, name)

for bc in target_cheese_barcodes:
    if bc not in cheese_results:
        print(f"  BC={bc:<22} NOT_FOUND in bsip0")
        cheese_results[bc] = (None, None, None, "not_found")


# ─── COOKIES-COFFEE (check factory_run_001) ───────────────────────────────────
print()
print("=" * 80)
print("COOKIES-COFFEE: checking factory_run_001 and bsip2_outputs")
print("=" * 80)

target_cc_barcodes = {
    "7290119043149", "7290017962139", "7290013453068", "7296073453840", "7296073453857"
}

cc_dir = r"C:\Bari\02_products\cookies_coffee"
cc_results = {}

# Try factory_run_001 JSON files
fr_dir = os.path.join(cc_dir, "factory_run_001")
if os.path.isdir(fr_dir):
    for fname in os.listdir(fr_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(fr_dir, fname)
        with open(fpath, encoding="utf-8") as f:
            raw = json.load(f)

        # Could be a list of products or a dict with products key
        if isinstance(raw, list):
            prods = raw
        elif isinstance(raw, dict):
            prods = raw.get("products", raw.get("corpus", [raw]))
            if not isinstance(prods, list):
                prods = [raw]
        else:
            continue

        for p in prods:
            if not isinstance(p, dict):
                continue
            bc = str(p.get("barcode", p.get("id", ""))).strip()
            if bc not in target_cc_barcodes:
                continue
            nutr = (p.get("normalized_nutrition_per_100g") or
                    p.get("nutrition_per_100g") or
                    p.get("nutrition") or {})
            if not isinstance(nutr, dict):
                nutr = {}
            carbs = (get_float(nutr, "carbohydrates_g", "carbs_g", "carbs") or
                     get_float(p, "carbohydrates_g", "carbs_g", "carbs"))
            sugar = (get_float(nutr, "sugars_g", "sugar_g", "sugar") or
                     get_float(p, "sugars_g", "sugar_g", "sugar"))
            name = p.get("name", p.get("product_name", p.get("canonical_name_he", "?")))
            fires = carbs >= 5.0 if carbs is not None else None
            status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
            print(f"  [{fname}] BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:40]}")
            if bc not in cc_results:
                cc_results[bc] = (carbs, sugar, fires, name)

for bc in target_cc_barcodes:
    if bc not in cc_results:
        print(f"  BC={bc:<22} NOT_FOUND in factory_run_001")
        cc_results[bc] = (None, None, None, "not_found")


# ─── BRINED CHEESES ───────────────────────────────────────────────────────────
print()
print("=" * 80)
print("BRINED CHEESES: checking BSIP0 raw")
print("=" * 80)

brined_bsip0 = r"C:\Bari\02_products\brined_cheeses\bsip0_outputs\brined_cheese_bsip0_raw_20260613T065721.json"
target_brined_barcodes = {"4861360", "48413", "369617"}
brined_results = {}

with open(brined_bsip0, encoding="utf-8") as f:
    brined_data = json.load(f)

if isinstance(brined_data, dict) and "products" in brined_data:
    brined_prods = brined_data["products"]
elif isinstance(brined_data, list):
    brined_prods = brined_data
else:
    brined_prods = list(brined_data.values())

print(f"  Loaded {len(brined_prods)} records")
for p in brined_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id", ""))).strip()
    if bc not in target_brined_barcodes:
        continue
    nutr = (p.get("normalized_nutrition_per_100g") or
            p.get("nutrition_per_100g") or
            p.get("nutrition") or {})
    if not isinstance(nutr, dict):
        nutr = {}
    carbs = (get_float(nutr, "carbohydrates_g", "carbs_g") or
             get_float(p, "carbohydrates_g", "carbs_g"))
    sugar = (get_float(nutr, "sugars_g", "sugar_g") or
             get_float(p, "sugars_g", "sugar_g"))
    name = p.get("name", p.get("product_name", "?"))
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    brined_results[bc] = (carbs, sugar, fires, name)

for bc in target_brined_barcodes:
    if bc not in brined_results:
        print(f"  BC={bc:<22} NOT_FOUND")
        brined_results[bc] = (None, None, None, "not_found")


# ─── BREAKFAST CEREALS ────────────────────────────────────────────────────────
print()
print("=" * 80)
print("BREAKFAST CEREALS: checking BSIP0 raw")
print("=" * 80)

cereals_bsip0 = r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json"
target_cereals = {"7297488098688"}

with open(cereals_bsip0, encoding="utf-8") as f:
    cereals_data = json.load(f)

if isinstance(cereals_data, dict) and "products" in cereals_data:
    cereals_prods = cereals_data["products"]
elif isinstance(cereals_data, list):
    cereals_prods = cereals_data
else:
    cereals_prods = list(cereals_data.values())

print(f"  Loaded {len(cereals_prods)} records")
cereals_results = {}
for p in cereals_prods:
    if not isinstance(p, dict):
        continue
    bc = str(p.get("barcode", p.get("id", ""))).strip()
    if bc not in target_cereals:
        continue
    nutr = (p.get("normalized_nutrition_per_100g") or
            p.get("nutrition_per_100g") or
            p.get("nutrition") or {})
    if not isinstance(nutr, dict):
        nutr = {}
    carbs = (get_float(nutr, "carbohydrates_g", "carbs_g", "carbs") or
             get_float(p, "carbohydrates_g", "carbs_g", "carbs"))
    sugar = (get_float(nutr, "sugars_g", "sugar_g", "sugar") or
             get_float(p, "sugars_g", "sugar_g", "sugar"))
    name = p.get("name", p.get("product_name", p.get("canonical_name_he", "?")))
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    cereals_results[bc] = (carbs, sugar, fires, name)

for bc in target_cereals:
    if bc not in cereals_results:
        print(f"  BC={bc:<22} NOT_FOUND in bsip0")
        cereals_results[bc] = (None, None, None, "not_found")


# ─── MILK: Check factory/milk data source ─────────────────────────────────────
print()
print("=" * 80)
print("MILK COMPARISON: checking milk_frontend_v1 inline carbs field")
print("=" * 80)

# The milk frontend JSON has carbs directly in expansion.nutrition.carbs for some products
import json
with open(r"C:\bari\bari-web\src\data\comparisons\milk_frontend_v1.json", encoding="utf-8") as f:
    milk_data = json.load(f)

milk_products = milk_data.get("products", [])
target_milk = {
    "7290000051352", "7290019790259", "7290102392094", "7290114313865",
    "7290116936116", "7290110324926", "7290014760141", "5411188124689",
    "7290110325619", "5411188112709",
}
milk_results = {}
for p in milk_products:
    bc = str(p.get("barcode", "")).strip()
    if bc not in target_milk:
        continue
    exp = p.get("expansion", {})
    nutr = exp.get("nutrition", {}) if isinstance(exp, dict) else {}
    carbs = nutr.get("carbs") if isinstance(nutr, dict) else None
    sugar = nutr.get("sugar") if isinstance(nutr, dict) else None
    name = p.get("name", "?")
    fires = carbs >= 5.0 if carbs is not None else None
    status = "FIRES" if fires else ("safe" if fires is False else "UNKNOWN (carbs=None)")
    print(f"  BC={bc:<22} carbs={str(carbs):<8} sugars={str(sugar):<8} status={status}  {str(name)[:50]}")
    milk_results[bc] = (carbs, sugar, fires, name)

for bc in target_milk:
    if bc not in milk_results:
        print(f"  BC={bc:<22} NOT_FOUND")
        milk_results[bc] = (None, None, None, "not_found")


# ─── FINAL SUMMARY ───────────────────────────────────────────────────────────
print()
print("=" * 80)
print("FINAL ADDITIONAL ACTIVATIONS (from this secondary scan)")
print("=" * 80)

all_secondary_activated = []
all_secondary_safe = []
still_unknown_final = []

for cat, results in [
    ("hard-cheeses", hc_results),
    ("cheese", cheese_results),
    ("cookies-coffee", cc_results),
    ("brined-cheeses", brined_results),
    ("breakfast-cereals", cereals_results),
    ("milk-comparison", milk_results),
]:
    for bc, data in results.items():
        carbs, sugar, fires, name = data
        if fires is True:
            all_secondary_activated.append((cat, bc, carbs, name))
        elif fires is False:
            all_secondary_safe.append((cat, bc, carbs, name))
        else:
            still_unknown_final.append((cat, bc, carbs, name))

print()
print("ADDITIONAL FIRES (null sugar + carbs >= 5.0 found in secondary sources):")
if all_secondary_activated:
    for cat, bc, carbs, name in all_secondary_activated:
        print(f"  {cat:<25} BC={bc}  carbs={carbs}  {name}")
else:
    print("  None.")

print()
print("CONFIRMED SAFE (carbs < 5.0 — rule does NOT fire):")
for cat, bc, carbs, name in all_secondary_safe:
    print(f"  {cat:<25} BC={bc}  carbs={carbs}  {str(name)[:50]}")

print()
print("STILL UNKNOWN (carbs not found in ANY source):")
for cat, bc, carbs, name in still_unknown_final:
    print(f"  {cat:<25} BC={bc}  {str(name)[:40]}")
