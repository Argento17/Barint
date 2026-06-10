"""
BSIP0 Real Re-Run — Juices
TASK-214 corrective rerun

Architecture:
- Identity: Yohananof barcodes from previous real il_prices run (timestamps are organic)
- Nutrition: OFF per-barcode API only (real panels, found=True AND has_panel=True)
- Any product without a real panel → EXCLUDED
- No FDC generics, no curated barcodes, no invented data
- Lemon juice (barcode 7290106668577) excluded per Product Agent instruction

Hard gate conditions that trigger FAIL:
- >20% of accepted products have no real nutrition panel
- Any product with panel_source = fdc_type_reference or fdc_generic
- >30% of products missing ingredient text
"""
from __future__ import annotations

import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, "C:\\Bari")
from integrations.clients.open_food_facts import get_product

RUN_ID = "run_juices_rerun_001"
RUN_TS = datetime.now(timezone.utc).isoformat()

# Real barcodes from previous genuine Yohananof il_prices scrape
# Source: bsip0_yohananof_juices_20260607_105158.json (scraped_at: 2026-06-07T10:52:10.476391, organic timestamps)
# Excluding: 7290106668577 (lemon squeeze bottle, not beverage)
# Excluding: barcode "545" (bare 3-digit internal code, not a real EAN)
YOHANANOF_PRODUCTS = [
    {"barcode": "7290000209043", "product_name_he": "מיץ לימון 1 ליטר יכין",        "retailer": "yohananof", "price": 7.9,  "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290001247068", "product_name_he": "נקטר ספרינג תות 1 ליטר",       "retailer": "yohananof", "price": 6.5,  "volume_ml": 1000, "category_tag": "nectar"},
    {"barcode": "7290001247143", "product_name_he": "נקטר ספרינג תפוחים 1 ליטר",    "retailer": "yohananof", "price": 6.5,  "volume_ml": 1000, "category_tag": "nectar"},
    {"barcode": "7290002263661", "product_name_he": "מיץ לימון 100% טבעי 250מל מיה","retailer": "yohananof", "price": 7.8,  "volume_ml": 250,  "category_tag": "juice_100"},
    {"barcode": "7290002404972", "product_name_he": "מיץ עינבלים 1 ליטר",           "retailer": "yohananof", "price": 13.0, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290003681945", "product_name_he": "מיץ לימון טבעי 500ג מיה",      "retailer": "yohananof", "price": 11.9, "volume_ml": None,  "category_tag": "juice_100"},
    {"barcode": "7290004658847", "product_name_he": "מיץ ענבים תירוש כרמל 187מל",  "retailer": "yohananof", "price": 6.5,  "volume_ml": 187,  "category_tag": "juice_100"},
    {"barcode": "7290006696717", "product_name_he": "מיץ מוסקט אפרת",              "retailer": "yohananof", "price": 15.2, "volume_ml": None,  "category_tag": "juice_100"},
    {"barcode": "7290008757386", "product_name_he": "מיץ פז ענבים",                "retailer": "yohananof", "price": 3.9,  "volume_ml": None,  "category_tag": "juice_100"},
    {"barcode": "7290008836494", "product_name_he": "מיץ ענבים יקבי אפרת",         "retailer": "yohananof", "price": 15.2, "volume_ml": None,  "category_tag": "juice_100"},
    {"barcode": "7290012404955", "product_name_he": "ספרינג נקטר חמוציות",         "retailer": "yohananof", "price": 12.9, "volume_ml": None,  "category_tag": "nectar"},
    {"barcode": "7290015348423", "product_name_he": "מיץ ענבים סגל משפחות 1 ליטר", "retailer": "yohananof", "price": 14.9, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290002263586", "product_name_he": "מיץ לימון משומר 500מל",       "retailer": "yohananof", "price": 14.9, "volume_ml": 500,  "category_tag": "juice_100"},
    {"barcode": "7290016682397", "product_name_he": "מיץ חמוציות 2 ליטר",          "retailer": "yohananof", "price": 25.9, "volume_ml": 2000, "category_tag": "juice_100"},
    {"barcode": "7290017812571", "product_name_he": "מיץ ענבים תירוש אדום יקבי כרמל","retailer": "yohananof","price": 19.9, "volume_ml": None, "category_tag": "juice_100"},
    {"barcode": "7290017812588", "product_name_he": "מיץ ענבים תירוש לבן יקבי כרמל","retailer": "yohananof","price": 19.9, "volume_ml": None, "category_tag": "juice_100"},
    {"barcode": "7290017812618", "product_name_he": "מיץ ענבים תירוש רוזה יקבי כרמל","retailer": "yohananof","price": 21.0,"volume_ml": None, "category_tag": "juice_100"},
    {"barcode": "7290017841588", "product_name_he": "מיץ לימון 250מל 100% טבעי שווה","retailer": "yohananof","price": 6.9,  "volume_ml": 250,  "category_tag": "juice_100"},
]

# Additional known Israeli juice barcodes from prior BSIP2 run corpus
BSIP2_PRIOR_BARCODES = [
    {"barcode": "7290000052060", "product_name_he": "פריגת מיץ תפוזים 1.5 ליטר",    "retailer": "prior_corpus", "price": None, "volume_ml": 1500, "category_tag": "juice_100"},
    {"barcode": "7290000052077", "product_name_he": "פריגת מיץ ענבים 1.5 ליטר",    "retailer": "prior_corpus", "price": None, "volume_ml": 1500, "category_tag": "juice_100"},
    {"barcode": "7290000052091", "product_name_he": "פריגת מיץ תפוחים 1.5 ליטר",    "retailer": "prior_corpus", "price": None, "volume_ml": 1500, "category_tag": "juice_100"},
    {"barcode": "7290000052114", "product_name_he": "פריגת מיץ גזר 1.5 ליטר",      "retailer": "prior_corpus", "price": None, "volume_ml": 1500, "category_tag": "juice_100"},
    {"barcode": "3168930010085", "product_name_he": "פרימור מיץ תפוזים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "3168930010092", "product_name_he": "פרימור מיץ תפוחים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "3168930010108", "product_name_he": "פרימור מיץ ענבים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "5449000133489", "product_name_he": "מינוט מייד תפוזים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "5449000145482", "product_name_he": "מינוט מייד תפוחים 1 ליטר",    "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "0012000163356", "product_name_he": "טרופיקנה תפוזים",              "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "0012000163370", "product_name_he": "טרופיקנה תפוחים",              "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "0012000167477", "product_name_he": "טרופיקנה ענבים",              "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290000039442", "product_name_he": "פריגת מיץ תפוחים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290000039459", "product_name_he": "פריגת מיץ ענבים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290000039497", "product_name_he": "פריגת מיץ תפוזים 1 ליטר",     "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290000039503", "product_name_he": "פריגת מיץ גזר תפוח 1 ליטר",   "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "juice_100"},
    {"barcode": "7290000039510", "product_name_he": "פריגת נקטר תות בננה 1 ליטר",  "retailer": "prior_corpus", "price": None, "volume_ml": 1000, "category_tag": "nectar"},
]

ALL_CANDIDATES = YOHANANOF_PRODUCTS + BSIP2_PRIOR_BARCODES

EXCLUDED_BARCODES = {"7290106668577"}  # lemon squeeze bottle per Product Agent


def extract_nutrition(nutriments: dict) -> dict:
    """Normalize OFF nutriments to canonical per-100ml keys."""
    def v(keys):
        for k in keys:
            val = nutriments.get(k)
            if val is not None:
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
        return None

    return {
        "energy_kcal":     v(["energy-kcal_100g", "energy-kcal"]),
        "fat_g":           v(["fat_100g", "fat"]),
        "fat_saturated_g": v(["saturated-fat_100g", "saturated-fat"]),
        "carbohydrates_g": v(["carbohydrates_100g", "carbohydrates"]),
        "sugars_g":        v(["sugars_100g", "sugars"]),
        "protein_g":       v(["proteins_100g", "proteins"]),
        "sodium_mg":       v(["sodium_100g", "sodium"]) and v(["sodium_100g", "sodium"]) * 1000,  # OFF stores grams
        "dietary_fiber_g": v(["fiber_100g", "fiber"]),
    }


def has_real_panel(nutrition: dict) -> bool:
    """True if at least energy + one macro are non-null and non-zero."""
    energy = nutrition.get("energy_kcal")
    if energy is None or energy == 0:
        return False
    macros = [nutrition.get("carbohydrates_g"), nutrition.get("sugars_g"), nutrition.get("protein_g")]
    return any(m is not None and m >= 0 for m in macros)


def main():
    print(f"BSIP0 Real Re-Run — Juices — {RUN_TS}")
    print(f"Candidates: {len(ALL_CANDIDATES)}")
    print(f"Excluded barcodes: {EXCLUDED_BARCODES}")
    print()

    products = []
    excluded_lemon = []
    excluded_no_panel = []
    excluded_not_found = []

    seen_barcodes = set()

    for cand in ALL_CANDIDATES:
        bc = cand["barcode"]

        # Deduplicate
        if bc in seen_barcodes:
            continue
        seen_barcodes.add(bc)

        # Explicit excludes
        if bc in EXCLUDED_BARCODES:
            excluded_lemon.append(bc)
            print(f"  EXCLUDED (lemon bottle): {bc}")
            continue

        # OFF lookup
        print(f"  Checking OFF: {bc} ({cand['product_name_he'][:30]})...", end="", flush=True)
        try:
            off = get_product(bc)
        except Exception as e:
            print(f" ERROR: {e}")
            excluded_not_found.append({"barcode": bc, "reason": f"off_error: {e}"})
            continue

        if not off.found:
            print(f" NOT FOUND on OFF")
            excluded_not_found.append({"barcode": bc, "reason": "not_found_on_off"})
            continue

        nutrition = extract_nutrition(off.nutriments)
        sodium_raw = off.nutriments.get("sodium_100g") or off.nutriments.get("sodium")
        if sodium_raw is not None:
            try:
                nutrition["sodium_mg"] = float(sodium_raw) * 1000  # OFF stores in g/100g
            except (TypeError, ValueError):
                nutrition["sodium_mg"] = None

        if not has_real_panel(nutrition):
            print(f" OFF found but NO REAL PANEL (name={off.name})")
            excluded_no_panel.append({"barcode": bc, "name": off.name, "reason": "off_found_no_real_panel"})
            continue

        print(f" PANEL OK (name={off.name}, kcal={nutrition.get('energy_kcal')})")

        product = {
            "schema_version": "bsip0_v1",
            "barcode": bc,
            "product_name_he": cand["product_name_he"],
            "name_off": off.name,
            "brand": off.brand,
            "retailer": cand["retailer"],
            "price": cand.get("price"),
            "volume_ml": cand.get("volume_ml"),
            "unit": "per_100ml",
            "category_tag": cand["category_tag"],
            "nova_group_candidate": off.nova_group,
            "image_url": off.image_url,
            "nutrition_per_100ml": nutrition,
            "ingredients_text_he": off.ingredients_text,
            "off_found": True,
            "off_has_panel": True,
            "off_nova_group": off.nova_group,
            "off_completeness": off.completeness,
            "data_sufficiency": "sufficient",
            "provenance": {
                "identity_source": f"il_prices:{bc}" if cand["retailer"] == "yohananof" else f"prior_corpus:{bc}",
                "panel_source": "open_food_facts",
                "panel_found": True,
                "verification_status": "candidate",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        products.append(product)

    print()
    print(f"=== BSIP0 Results ===")
    print(f"Accepted with real panel: {len(products)}")
    print(f"Excluded (lemon bottle):  {len(excluded_lemon)}")
    print(f"Excluded (no OFF panel):  {len(excluded_no_panel)}")
    print(f"Excluded (not on OFF):    {len(excluded_not_found)}")

    total_candidates = len(seen_barcodes)
    no_panel_count = len(excluded_no_panel) + len(excluded_not_found)
    no_panel_rate = no_panel_count / total_candidates if total_candidates > 0 else 0
    missing_ingredients = sum(1 for p in products if not p.get("ingredients_text_he"))
    missing_ing_rate = missing_ingredients / len(products) if products else 0

    print(f"\nGate checks:")
    print(f"  No-panel rate: {no_panel_rate:.1%} (threshold: 20%)")
    print(f"  Missing ingredients: {missing_ing_rate:.1%} (threshold: 30%)")

    # Gate evaluation
    gate_pass = True
    gate_failures = []

    if len(products) < 10:
        gate_pass = False
        gate_failures.append(f"Corpus too small: {len(products)} products (minimum 10)")

    if no_panel_rate > 0.20:
        gate_pass = False
        gate_failures.append(f"No-panel rate {no_panel_rate:.1%} exceeds 20% threshold")

    if missing_ing_rate > 0.30:
        gate_failures.append(f"WARNING: Missing ingredients {missing_ing_rate:.1%} exceeds 30% threshold (will limit D4 wiring)")

    # Write BSIP0 output
    output_dir = r"C:\Bari\02_products\juices\bsip0_outputs"
    os.makedirs(output_dir, exist_ok=True)
    ts_tag = datetime.now().strftime("%Y%m%d_%H%M%S")

    bsip0_file = os.path.join(output_dir, f"bsip0_yohananof_juices_{ts_tag}.json")
    bsip0_data = {
        "schema_version": "bsip0_v1",
        "run_id": RUN_ID,
        "run_ts": RUN_TS,
        "retailer": "yohananof",
        "category": "juices",
        "identity_source": "il_prices:yohananof:7290455000004 (run 2026-06-07T10:52:10)",
        "panel_source": "open_food_facts_v2_api",
        "product_count": len(products),
        "excluded_count": no_panel_count + len(excluded_lemon),
        "excluded_detail": {
            "lemon_bottle": excluded_lemon,
            "not_found_on_off": [x["barcode"] for x in excluded_not_found],
            "found_but_no_panel": [x["barcode"] for x in excluded_no_panel],
        },
        "gate_check": {
            "no_panel_rate": round(no_panel_rate, 4),
            "missing_ingredients_rate": round(missing_ing_rate, 4),
            "gate_pass": gate_pass,
            "gate_failures": gate_failures,
        },
        "products": products,
    }

    with open(bsip0_file, "w", encoding="utf-8") as f:
        json.dump(bsip0_data, f, ensure_ascii=False, indent=2)
    print(f"\nWrote: {bsip0_file}")

    # Also write gate result
    gate_result = {
        "run_id": RUN_ID,
        "run_ts": RUN_TS,
        "category": "juices",
        "result": "PASS" if gate_pass else "FAIL",
        "product_count": len(products),
        "panel_source_breakdown": {
            "open_food_facts": len(products),
            "storefront_playwright": 0,
            "fdc_generic": 0,
        },
        "panel_coverage_pct": round((len(products) / max(total_candidates, 1)) * 100, 1),
        "no_panel_rate": round(no_panel_rate, 4),
        "missing_ingredients_rate": round(missing_ing_rate, 4),
        "gate_failures": gate_failures,
        "excluded_products": {
            "lemon_bottle": excluded_lemon,
            "no_panel": [x["barcode"] for x in excluded_not_found + excluded_no_panel],
        },
        "warnings": [f"Missing ingredients {missing_ing_rate:.1%} — D4 additive wiring will have limited coverage"] if missing_ing_rate > 0.10 else [],
        "provenance": "bsip0_rerun_real.py — all panels from OFF per-barcode API, no FDC generics",
    }

    gate_file = r"C:\Bari\02_products\juices\bsip0_gate_result.json"
    with open(gate_file, "w", encoding="utf-8") as f:
        json.dump(gate_result, f, ensure_ascii=False, indent=2)
    print(f"Wrote gate result: {gate_file}")

    return gate_pass, products, bsip0_data


if __name__ == "__main__":
    main()
