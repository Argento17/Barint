"""
TASK-377: BARI_SUGAR_NULL_GUARD blast-radius scan.
READ-ONLY. No file mutations.

Strategy:
1. Collect all null-sugar products from frontend JSONs (expansion.nutrition.sugar is None).
2. For each, look up L1_observed_signals.carbohydrates_g from the upstream BSIP2 trace file.
3. Apply activation condition: sugars_g is None AND carbohydrates_g >= 5.0.
4. Report per-category counts, affected product details, carbs distribution, whole-food edge cases.
"""

import json
import os
import sys
import io
import glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ─── Paths ────────────────────────────────────────────────────────────────────
FRONTEND_DIR = r"C:\bari\bari-web\src\data\comparisons"
PRODUCTS_DIR = r"C:\Bari\02_products"

# ─── Category → frontend JSON + BSIP trace root ───────────────────────────────
CATEGORY_CONFIG = {
    "bread": {
        "json": "bread_frontend_v3.json",
        "bsip2_trace_root": r"C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_001\products",
        "trace_prefix": "bsip1_bread_",
    },
    "breakfast-cereals": {
        "json": "cereals_frontend_v2.json",
        "bsip2_trace_root": r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs",
        "trace_prefix": None,
    },
    "brined-cheeses": {
        "json": "brined_cheeses_frontend_v2.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "cakes": {
        "json": "cakes_hard_cookies_frontend_v1.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "cheese": {
        "json": "cheese_frontend_v4.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "chocolate-bars": {
        "json": "chocolate_bars_frontend_v1.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "chocolate-tablets": {
        "json": "chocolate_tablets_frontend_v1.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "cookies-coffee": {
        "json": "cookies_coffee_frontend_v2.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "granola": {
        "json": "granola_frontend_v1.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "hard-cheeses": {
        "json": "hard_cheeses_frontend_v2.json",
        "bsip2_trace_root": r"C:\Bari\02_products\hard_cheeses\bsip1_outputs",
        "trace_prefix": None,
    },
    "hummus": {
        "json": "hummus_frontend_v5.json",
        "bsip2_trace_root": r"C:\Bari\02_products\hummus\canonical_bsip1",
        "trace_prefix": None,
    },
    "juices": {
        "json": "juices_frontend_v3.json",
        "bsip2_trace_root": r"C:\Bari\02_products\juices\bsip1_outputs",
        "trace_prefix": None,
    },
    "milk-comparison": {
        "json": "milk_frontend_v1.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
    "protein-bars": {
        "json": "protein_combined_frontend_v2.json",
        "bsip2_trace_root": r"C:\Bari\02_products\snack_bars\canonical_bsip1",
        "trace_prefix": None,
    },
    "snacks": {
        "json": "snacks_frontend_v5.json",
        "bsip2_trace_root": None,
        "trace_prefix": None,
    },
}


def find_bsip_carbs(barcode: str, cat_config: dict) -> tuple:
    """
    Returns (carbohydrates_g, sugars_g_in_bsip, source_note).
    Searches the BSIP trace root for a file containing this barcode.
    Looks at L1_observed_signals.carbohydrates_g and .sugars_g.
    """
    trace_root = cat_config.get("bsip2_trace_root")
    if not trace_root or not os.path.isdir(trace_root):
        return (None, None, "no_trace_root")

    # For bread: subdirectory per product named bsip1_bread_{barcode}
    prefix = cat_config.get("trace_prefix")
    if prefix:
        subdir = os.path.join(trace_root, f"{prefix}{barcode}")
        trace_file = os.path.join(subdir, "bsip2_trace.json")
        if os.path.isfile(trace_file):
            with open(trace_file, encoding="utf-8") as f:
                t = json.load(f)
            l1 = t.get("L1_observed_signals", {})
            return (
                l1.get("carbohydrates_g"),
                l1.get("sugars_g"),
                f"bsip2_trace:{trace_file.split(PRODUCTS_DIR)[-1]}",
            )
        return (None, None, f"trace_file_missing:{subdir}")

    # Generic: scan all JSON files in the root for this barcode
    for fname in os.listdir(trace_root):
        if not fname.endswith(".json"):
            continue
        # Quick name match first
        if barcode in fname:
            fpath = os.path.join(trace_root, fname)
            with open(fpath, encoding="utf-8") as f:
                t = json.load(f)
            # Check multiple field locations
            for carb_field in ["carbohydrates_g", "carbs_g", "total_carbs_g"]:
                carbs = None
                sugars = None
                # Direct product nutrition
                nutr = t.get("normalized_nutrition_per_100g") or t.get("nutrition_per_100g") or {}
                if isinstance(nutr, dict):
                    carbs = nutr.get("carbohydrates_g") or nutr.get("carbs_g")
                    sugars = nutr.get("sugars_g") or nutr.get("sugar_g")
                # L1_observed_signals
                l1 = t.get("L1_observed_signals", {})
                if not carbs:
                    carbs = l1.get("carbohydrates_g")
                if sugars is None:
                    sugars = l1.get("sugars_g")
                if carbs is not None:
                    return (carbs, sugars, f"bsip_file:{fname}")

    return (None, None, "not_found_in_trace_root")


def get_carbs_from_frontend_nutrition(nutr: dict) -> float | None:
    """Some frontend nutrition objects include carbs directly."""
    return nutr.get("carbs") or nutr.get("carbohydrates") or nutr.get("carbohydrates_g")


# ─── Main scan ────────────────────────────────────────────────────────────────

all_null_sugar = []      # all products with null sugar in frontend
all_activated = []       # null sugar AND carbs >= 5.0 (rule fires)
category_rows = []

for cat, cfg in CATEGORY_CONFIG.items():
    fpath = os.path.join(FRONTEND_DIR, cfg["json"])
    with open(fpath, encoding="utf-8") as f:
        data = json.load(f)
    prods = data.get("products", data if isinstance(data, list) else [])
    total = len(prods)

    cat_null_sugar = []
    cat_activated = []

    for p in prods:
        exp = p.get("expansion", {})
        nutr = exp.get("nutrition", {}) if isinstance(exp, dict) else {}
        sugar = nutr.get("sugar") if isinstance(nutr, dict) else "PRESENT"

        if sugar is not None:
            continue  # sugar is present — not affected

        barcode = p.get("barcode", p.get("id", "UNKNOWN"))
        name = p.get("name", "UNKNOWN")
        score = p.get("score", "N/A")
        grade = p.get("grade", "N/A")
        rank = p.get("rank")
        is_top3 = rank is not None and isinstance(rank, int) and rank <= 3

        # Try to get carbs from frontend nutrition first
        carbs_g = get_carbs_from_frontend_nutrition(nutr) if isinstance(nutr, dict) else None
        carbs_source = "frontend_nutrition" if carbs_g is not None else None

        # If not in frontend, look in BSIP traces
        if carbs_g is None:
            carbs_g, bsip_sugars, carbs_source = find_bsip_carbs(str(barcode), cfg)
        else:
            bsip_sugars = None

        # Get ingredients from expansion
        ingredients = ""
        if isinstance(exp, dict):
            ing = exp.get("ingredients") or exp.get("ingredientsList") or ""
            if isinstance(ing, list):
                ingredients = ", ".join(str(x) for x in ing)
            else:
                ingredients = str(ing)

        entry = {
            "category": cat,
            "name": name,
            "barcode": barcode,
            "score": score,
            "grade": grade,
            "rank": rank,
            "is_top3": is_top3,
            "carbs_g": carbs_g,
            "carbs_source": carbs_source,
            "bsip_sugars": bsip_sugars,
            "ingredients": ingredients[:300],
            "frontend_nutrition": nutr,
        }

        cat_null_sugar.append(entry)
        all_null_sugar.append(entry)

        # Apply activation condition
        if carbs_g is not None and carbs_g >= 5.0:
            cat_activated.append(entry)
            all_activated.append(entry)
        elif carbs_g is None:
            # Carbs unknown — flag as "unknown carbs, cannot determine"
            entry["carbs_unknown"] = True

    category_rows.append({
        "category": cat,
        "total": total,
        "null_sugar": len(cat_null_sugar),
        "activated": len(cat_activated),
        "json_file": cfg["json"],
        "products": cat_null_sugar,
    })


# ─── Output ───────────────────────────────────────────────────────────────────

print("=" * 90)
print("TASK-377 BARI_SUGAR_NULL_GUARD BLAST-RADIUS SCAN")
print("Activation condition: sugars_g is None AND carbohydrates_g >= 5.0 g/100g")
print("=" * 90)
print()

print("SOURCE MAPPING (category → live frontend JSON):")
print("-" * 70)
for row in category_rows:
    print(f"  {row['category']:<25} {row['json_file']}")

print()
print("=" * 90)
print("CATEGORY SUMMARY TABLE")
print(f"  {'Category':<25} {'Null-Sugar':>12} {'Carbs>=5 (FIRES)':>17} {'Total':>7}")
print("-" * 70)
for row in category_rows:
    null_pct = (row["null_sugar"] / row["total"] * 100) if row["total"] > 0 else 0
    act_pct = (row["activated"] / row["total"] * 100) if row["total"] > 0 else 0
    print(
        f"  {row['category']:<25} {row['null_sugar']:>4}/{row['total']:<4} ({null_pct:>3.0f}%)"
        f"  {row['activated']:>4}/{row['total']:<4} ({act_pct:>3.0f}%)"
    )

print("-" * 70)
total_products = sum(r["total"] for r in category_rows)
total_null = len(all_null_sugar)
total_activated = len(all_activated)
print(
    f"  {'TOTAL':<25} {total_null:>4}/{total_products:<4}"
    f"  {total_activated:>4}/{total_products:<4}"
)

print()
print("=" * 90)
print("AFFECTED PRODUCTS (rule FIRES: null sugar + carbs >= 5.0)")
print("=" * 90)
for p in all_activated:
    top3_tag = " [TOP3]" if p["is_top3"] else ""
    print(f"\n  CATEGORY : {p['category']}")
    print(f"  NAME     : {p['name']}")
    print(f"  BARCODE  : {p['barcode']}")
    print(f"  SCORE    : {p['score']}  GRADE: {p['grade']}  RANK: {p['rank']}{top3_tag}")
    print(f"  carbs_g  : {p['carbs_g']}  (source: {p['carbs_source']})")
    print(f"  INGRED   : {p['ingredients'][:200] if p['ingredients'] else '(none in frontend)'}")

print()
print("=" * 90)
print("NULL-SUGAR PRODUCTS WITH UNKNOWN CARBS (cannot determine activation)")
print("=" * 90)
unknown_carbs = [p for p in all_null_sugar if p.get("carbs_unknown")]
for p in unknown_carbs:
    print(f"  {p['category']:<20} {p['barcode']:<20} {p['name'][:50]}  score={p['score']} grade={p['grade']}")

print()
print("=" * 90)
print("CARBS DISTRIBUTION (activated products only)")
print("=" * 90)
if all_activated:
    carbs_vals = sorted([p["carbs_g"] for p in all_activated if p["carbs_g"] is not None])
    n = len(carbs_vals)
    median = carbs_vals[n // 2]
    print(f"  count={n}  min={min(carbs_vals):.1f}  median={median:.1f}  max={max(carbs_vals):.1f}")
    print(f"  all: {[round(v, 1) for v in carbs_vals]}")
else:
    print("  No activated products.")

print()
print("=" * 90)
print("WHOLE-FOOD / SINGLE-INGREDIENT EDGE-CASE CHECK")
print("Product's co-sign condition: any product where null sugar = genuinely near-zero?")
print("=" * 90)
# Flag any product whose name or ingredients suggests fruit-only / whole food
whole_food_keywords = ["תמר", "צימוק", "משמש", "דבלה", "פרי", "fruit", "date", "raisin", "dried"]
flagged_whole_food = []
for p in all_activated:
    name_lower = p["name"].lower()
    ing_lower = p["ingredients"].lower()
    for kw in whole_food_keywords:
        if kw.lower() in name_lower or kw.lower() in ing_lower:
            flagged_whole_food.append((kw, p))
            break

if flagged_whole_food:
    print("  WARNING: potential whole-food / fruit products found:")
    for kw, p in flagged_whole_food:
        print(f"    TRIGGER='{kw}'  {p['category']}  {p['name']}  carbs={p['carbs_g']}")
        print(f"    INGRED: {p['ingredients'][:200]}")
else:
    print("  No whole-food / single-fruit products detected among activated set.")

print()
print("=" * 90)
print("BELOW-VIABLE-THRESHOLD CHECK (categories with < 10-12 displayable after discard)")
print("=" * 90)
for row in category_rows:
    remaining = row["total"] - row["activated"]
    if remaining < 12:
        flag = " *** BELOW 12 ***" if remaining < 12 else ""
        print(f"  {row['category']:<25} remaining={remaining} (total={row['total']} - activated={row['activated']}){flag}")
    else:
        print(f"  {row['category']:<25} remaining={remaining}  OK")

print()
print("=" * 90)
print("CHOCOLATE CROSS-CHECK (TASK-376 key-naming fix residual check)")
print("=" * 90)
for row in category_rows:
    if "chocolate" in row["category"]:
        print(f"  {row['category']}: total={row['total']}  null_sugar={row['null_sugar']}  activated={row['activated']}")
        if row["null_sugar"] == 0:
            print(f"    CLEAN: zero null-sugar products. TASK-376 fix left no residual.")
        else:
            print(f"    WARNING: {row['null_sugar']} null-sugar product(s) found — inspect:")
            for p in row["products"]:
                print(f"      {p['barcode']}  score={p['score']}  {p['name'][:50]}")
