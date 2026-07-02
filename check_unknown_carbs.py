"""
Check carbohydrates for null-sugar products whose carbs were unknown in the main scan.
Reads from BSIP0 raw files and other available upstream sources.
"""
import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Barcodes with unknown carbs, by category
UNKNOWN = {
    "breakfast-cereals": {
        "barcodes": ["7297488098688"],
        "bsip0": r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260605T154620.json",
    },
    "brined-cheeses": {
        "barcodes": ["4861360", "48413", "369617"],
        "bsip0": r"C:\Bari\02_products\brined_cheeses\bsip0_outputs\brined_cheese_bsip0_raw_20260613T065721.json",
    },
    "cheese": {
        "barcodes": [
            "7290014758681", "4127077", "4127329", "41445", "7290110321277",
            "7290116934280", "4127336", "41452", "7290108506624", "56272",
            "7290116931241", "7290116934365", "7290014759084", "7290116935409",
            "7290014762831", "7290116936604", "4129101", "4129156", "7290116931982",
            "7290116933078",
        ],
        "bsip0": r"C:\Bari\02_products\cheese_spreads\bsip0_outputs\cheese_bsip0_raw_20260602T054843.json",
    },
    "cookies-coffee": {
        "barcodes": ["7290119043149", "7290017962139", "7290013453068", "7296073453840", "7296073453857"],
        "bsip0": r"C:\Bari\02_products\cookies_coffee\bsip0_outputs\cookies_coffee_bsip0_raw_20260613T163431.json",
    },
    "hard-cheeses": {
        "barcodes": [
            "7290108502725", "7290019635192", "7290110324872", "7290102396672",
            "7290110323301", "7290116931524", "8711528211138", "7290004122348",
            "7290004137311", "7290102397204", "7290017065434", "7290108501346",
            "7290117265888", "7290117265918", "7290102394463", "7290014760912",
            "7290000057088", "7290004122683", "7290004125776", "7290014763395",
            "7290110320867",
        ],
        "bsip0": r"C:\Bari\02_products\hard_cheeses\bsip0_outputs\bsip0_shufersal_raw.json",
    },
    "milk-comparison": {
        "barcodes": [
            "7290000051352", "7290019790259", "7290102392094", "7290114313865",
            "7290116936116", "7290110324926", "7290014760141", "5411188124689",
            "7290110325619", "5411188112709",
        ],
        "bsip0": None,  # milk uses inline data
    },
}


def extract_nutrition(product_record: dict) -> dict:
    """Try to extract a nutrition dict from various possible locations in a product record."""
    for key in [
        "normalized_nutrition_per_100g",
        "nutrition_per_100g",
        "nutrition",
        "L1_observed_signals",
    ]:
        if key in product_record and isinstance(product_record[key], dict):
            return product_record[key]
    return product_record  # fallback: treat the record itself as nutrition


def get_field(nutr: dict, *keys):
    for k in keys:
        v = nutr.get(k)
        if v is not None:
            return v
    return None


def scan_bsip0(filepath: str, target_barcodes: list) -> dict:
    """Load a BSIP0 raw file and extract carbs+sugars for target barcodes."""
    results = {}
    if not os.path.isfile(filepath):
        return {bc: ("FILE_MISSING", None) for bc in target_barcodes}

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    # Normalize to list
    if isinstance(data, list):
        prods = data
    elif isinstance(data, dict):
        prods = data.get("products", data.get("corpus", list(data.values())))
        if not isinstance(prods, list):
            prods = list(data.values())
    else:
        prods = []

    bc_set = set(target_barcodes)
    for p in prods:
        if not isinstance(p, dict):
            continue
        bc = str(p.get("barcode", "") or p.get("id", "") or p.get("barcode_il", "")).strip()
        if bc in bc_set:
            nutr = extract_nutrition(p)
            carbs = get_field(nutr, "carbohydrates_g", "carbs_g", "carbohydrates", "carbs")
            sugars = get_field(nutr, "sugars_g", "sugar_g", "sugars", "sugar")
            name = p.get("name", p.get("product_name", p.get("name_he", "?")))
            results[bc] = (carbs, sugars, str(name)[:50])

    # Fill missing
    for bc in target_barcodes:
        if bc not in results:
            results[bc] = (None, None, "NOT_FOUND_IN_FILE")

    return results


print("=" * 80)
print("CARBS VERIFICATION for null-sugar products with unknown carbs")
print("=" * 80)
print()

all_newly_activated = []
all_confirmed_safe = []
all_still_unknown = []

for cat, cfg in UNKNOWN.items():
    barcodes = cfg["barcodes"]
    bsip0 = cfg["bsip0"]

    print(f"--- {cat} ---")

    if bsip0 is None:
        # Milk: inline data - check by food knowledge
        print("  Milk comparison: carbs for dairy milk ~4.7g lactose/100g → NEAR threshold.")
        print("  Plant milks: oat milk ~6-9g/100g (ABOVE 5.0), almond/soy ~0-3g/100g (BELOW).")
        print("  Each milk product needs individual check — no BSIP0 file available.")
        for bc in barcodes:
            all_still_unknown.append((cat, bc, "milk_inline_no_bsip0"))
        continue

    results = scan_bsip0(bsip0, barcodes)
    for bc, data_tuple in results.items():
        if len(data_tuple) == 3:
            carbs, sugars, name = data_tuple
        else:
            carbs, sugars = data_tuple
            name = "?"

        fires = None
        if carbs is not None:
            fires = carbs >= 5.0
            status = "FIRES" if fires else "safe"
        else:
            status = "UNKNOWN"

        print(f"  BC={bc:<20} carbs={str(carbs):<8} sugar={str(sugars):<8} status={status}  {name}")

        if fires is True:
            all_newly_activated.append((cat, bc, carbs, name))
        elif fires is False:
            all_confirmed_safe.append((cat, bc, carbs, name))
        else:
            all_still_unknown.append((cat, bc, "carbs_null_in_bsip0"))

print()
print("=" * 80)
print("SUMMARY OF NEWLY ACTIVATED (carbs found in BSIP0 and >= 5.0)")
print("=" * 80)
if all_newly_activated:
    for cat, bc, carbs, name in all_newly_activated:
        print(f"  {cat:<25} BC={bc}  carbs={carbs}  {name}")
else:
    print("  None.")

print()
print("=" * 80)
print("CONFIRMED SAFE (carbs < 5.0 in BSIP0 — rule does NOT fire)")
print("=" * 80)
for cat, bc, carbs, name in all_confirmed_safe:
    print(f"  {cat:<25} BC={bc}  carbs={carbs}  {name}")

print()
print("=" * 80)
print("STILL UNKNOWN (carbs not found anywhere)")
print("=" * 80)
for item in all_still_unknown:
    print(f"  {item}")
