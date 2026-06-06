"""
TASK-191 Phase A — BSIP1 Enrichment for Butter corpus.

Runs OFF (by barcode) → USDA FDC (by brand name, generic) for each of the
23 insufficient products. Updates butter_bsip1_merged.json in-place and writes
butter_enrichment_report_20260605.json.

EDPG rule: all external values are born verification_status=candidate. Nothing
goes near scoring. Only BSIP1 records are touched.

Usage:
    python 02_products/butter/enrich_butter_bsip1.py
"""
from __future__ import annotations

import json
import sys
import copy
from pathlib import Path
from datetime import datetime, timezone

# Allow importing integrations/ from the repo root
REPO_ROOT = Path(__file__).resolve().parents[2]  # C:\Bari (script is 2 levels deep: 02_products/butter/)
sys.path.insert(0, str(REPO_ROOT))

from integrations.clients import open_food_facts as off
from integrations.clients import usda_fdc as fdc
from integrations.clients.provenance import now_iso

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BSIP1_PATH = REPO_ROOT / "02_products" / "butter" / "bsip1_outputs" / "butter_bsip1_merged.json"
REPORT_PATH = REPO_ROOT / "02_products" / "butter" / "bsip1_outputs" / "butter_enrichment_report_20260605.json"

# ---------------------------------------------------------------------------
# OFF nutriment key → Bari canonical per-100g key
# ---------------------------------------------------------------------------
OFF_NUTRIMENT_MAP = {
    "energy-kcal_100g": "energy_kcal",
    "fat_100g": "fat_g",
    "saturated-fat_100g": "fat_saturated_g",
    "trans-fat_100g": "fat_trans_g",
    "cholesterol_100g": "cholesterol_mg",   # OFF stores in g; will multiply below
    "sodium_100g": "sodium_mg",             # OFF stores in g; will multiply ×1000
    "carbohydrates_100g": "carbohydrates_g",
    "sugars_100g": "sugars_g",
    "fiber_100g": "dietary_fiber_g",
    "proteins_100g": "protein_g",
}

# OFF stores sodium in grams per 100g; we need mg. Cholesterol also in g.
OFF_G_TO_MG = {"sodium_mg", "cholesterol_mg"}

# USDA FDC canonical key → Bari canonical per-100g key
FDC_KEY_MAP = {
    "energy_kcal": "energy_kcal",
    "fat_g": "fat_g",
    "satfat_g": "fat_saturated_g",
    "transfat_g": "fat_trans_g",
    "cholesterol_mg": "cholesterol_mg",
    "sodium_mg": "sodium_mg",
    "carb_g": "carbohydrates_g",
    "sugar_g": "sugars_g",
    "fiber_g": "dietary_fiber_g",
    "protein_g": "protein_g",
}

# ---------------------------------------------------------------------------
# USDA FDC search queries for products that are unlikely to appear in OFF
# (prioritized brand names → generic butters)
# ---------------------------------------------------------------------------
FDC_SEARCH_MAP = {
    # barcode → (query_label, prefer_generic, fdc_id_override)
    #
    # fdc_id_override: fetch this specific FDC entry directly (skip search).
    # All per-100g SR Legacy / Foundation entries have been verified for field
    # count before being pinned here. The Kerrygold FDC Branded entry (2757263)
    # is per-serving and unusable; replaced with SR Legacy generic.
    #
    # Unsalted generic: 173430 "Butter, without salt" SR Legacy — 9 fields
    # Salted generic:   173410 "Butter, salted" SR Legacy — 10 fields
    # Ghee:             171314 "Butter, Clarified butter (ghee)" SR Legacy — 10 fields
    # President unsalted: 1868389 — Branded, 10 fields, per-100g confirmed
    # President salted:   1868388 — Branded, 10 fields, per-100g confirmed
    # Lurpak unsalted:    1856663 — Branded, 8 fields, per-100g confirmed

    "5099460004149": ("Kerrygold unsalted butter — SR Legacy generic", True, 173430),
    "5099460004132": ("Kerrygold salted butter — SR Legacy generic", True, 173410),
    "5099460004156": ("Kerrygold unsalted butter 250g — SR Legacy generic", True, 173430),
    "5099460010935": ("Kerrygold unsalted butter Carrefour — SR Legacy generic", True, 173430),
    "5740900400221": ("Lurpak unsalted butter — Branded", False, 1856663),
    "5740900400238": ("Lurpak salted butter — SR Legacy generic", True, 173410),
    "7290000066028": ("Tnuva plain butter — SR Legacy generic unsalted", True, 173430),
    "7290000066035": ("Tnuva salted butter — SR Legacy generic salted", True, 173410),
    "3228021530005": ("President unsalted butter — Branded", False, 1868389),
    "3228021530012": ("President salted butter — Branded", False, 1868388),
    "9414544900015": ("Anchor unsalted butter — SR Legacy generic", True, 173430),
    "9414544900022": ("Anchor salted butter — SR Legacy generic", True, 173410),
    "7290113401022": ("Adom Adom butter — SR Legacy generic unsalted", True, 173430),
    "7290006325046": ("Yotvata butter — SR Legacy generic unsalted", True, 173430),
    "7290105953020": ("Beit HaEmek butter — SR Legacy generic unsalted", True, 173430),
    "7290002492086": ("Noga butter — SR Legacy generic unsalted", True, 173430),
    "4820217240114": ("FERMA butter 82.5% — SR Legacy generic unsalted", True, 173430),
    "3161911229199": ("Alweer soft butter — SR Legacy generic unsalted", True, 173430),
    "8906060890143": ("Pure Ghee — SR Legacy ghee", True, 171314),
    "4260268321030": ("Ghee oil — SR Legacy ghee", True, 171314),
    "3760088100025": ("Echire AOP butter — SR Legacy generic unsalted", True, 173430),
    "3412130012558": ("Paysan Breton unsalted butter — SR Legacy generic", True, 173430),
    "3412130012534": ("Paysan Breton salted butter — SR Legacy generic", True, 173410),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_off_nutrition(nutriments: dict) -> dict:
    """Convert OFF nutriments dict to Bari's normalized_nutrition_per_100g format."""
    result: dict = {}
    for off_key, bari_key in OFF_NUTRIMENT_MAP.items():
        val = nutriments.get(off_key)
        if val is None:
            result[bari_key] = None
            continue
        try:
            val = float(val)
        except (TypeError, ValueError):
            result[bari_key] = None
            continue
        # OFF sodium is in g/100g → convert to mg
        if bari_key in OFF_G_TO_MG:
            val = round(val * 1000, 2)
        result[bari_key] = val
    return result


def extract_fdc_nutrition(food: "fdc.Food") -> dict:
    """Convert FDC Food.values to Bari's normalized_nutrition_per_100g format."""
    result: dict = {}
    for fdc_key, bari_key in FDC_KEY_MAP.items():
        val = food.values.get(fdc_key)
        result[bari_key] = round(float(val), 2) if val is not None else None
    return result


def count_non_null(nutrition: dict) -> int:
    return sum(1 for v in nutrition.values() if v is not None)


def assess_sufficiency(nutrition: dict) -> str:
    """Mirror the same logic the BSIP1 builder uses: ≥4 non-null fields = sufficient."""
    return "sufficient" if count_non_null(nutrition) >= 4 else "insufficient"


def log(msg: str) -> None:
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="backslashreplace").decode("ascii"), flush=True)


# ---------------------------------------------------------------------------
# Main enrichment loop
# ---------------------------------------------------------------------------

def enrich() -> None:
    log(f"[{now_iso()}] TASK-191 Phase A — Butter BSIP1 enrichment starting")

    with open(BSIP1_PATH, encoding="utf-8") as f:
        products: list[dict] = json.load(f)

    # Index by barcode for quick lookup
    by_barcode: dict[str, dict] = {p["barcode"]: p for p in products}

    # Identify insufficient products (the 23 targets)
    insufficient = [p for p in products if p.get("data_sufficiency") == "insufficient"]
    log(f"Insufficient products to enrich: {len(insufficient)}")

    report_entries: list[dict] = []
    enriched_count = 0

    for prod in insufficient:
        barcode = prod["barcode"]
        name = prod.get("canonical_name_he", "")
        brand = prod.get("brand", "")
        log(f"\n--- {barcode} | {brand} | {name}")

        entry = {
            "barcode": barcode,
            "name": name,
            "brand": brand,
            "retailer": prod.get("retailer_id") or prod.get("source_retailers", [None])[0],
            "off_result": "not_tried",
            "fdc_result": "not_tried",
            "source_used": None,
            "fields_recovered": [],
            "fields_remaining_null": [],
            "new_data_sufficiency": prod.get("data_sufficiency"),
            "notes": [],
        }

        nutrition_applied: dict | None = None
        ingredients_applied: str | None = None
        prov_dict: dict | None = None
        source_name: str | None = None

        # ----------------------------------------------------------------
        # Step 1: Try OFF by barcode
        # ----------------------------------------------------------------
        try:
            off_prod = off.get_product(barcode, timeout=30)
        except Exception as exc:
            log(f"  OFF error: {exc}")
            entry["off_result"] = f"error: {exc}"
            off_prod = None

        if off_prod and off_prod.found:
            log(f"  OFF: FOUND — name={off_prod.name!r} completeness={off_prod.completeness}")
            entry["off_result"] = "found"

            if off_prod.has_panel:
                nutrition_applied = extract_off_nutrition(off_prod.nutriments)
                log(f"  OFF panel extracted: {count_non_null(nutrition_applied)} non-null fields")
                prov_dict = off_prod.provenance.as_dict() if off_prod.provenance else None
                source_name = "open_food_facts"
            else:
                log(f"  OFF: found but no panel (completeness={off_prod.completeness})")
                entry["off_result"] = "found_no_panel"

            # Ingredients from OFF (Hebrew preferred)
            if off_prod.ingredients_text:
                ingredients_applied = off_prod.ingredients_text
                log(f"  OFF ingredients: {ingredients_applied[:80]!r}...")
        else:
            if off_prod:
                log(f"  OFF: not found")
                entry["off_result"] = "not_found"

        # ----------------------------------------------------------------
        # Step 2: If OFF gave no panel, try USDA FDC
        # ----------------------------------------------------------------
        if nutrition_applied is None and barcode in FDC_SEARCH_MAP:
            query, prefer_generic, fdc_id_override = FDC_SEARCH_MAP[barcode]
            entry["fdc_result"] = "searched"
            food = None
            try:
                if fdc_id_override is not None:
                    # Fetch the specific known FDC entry directly — avoids search mis-hits
                    log(f"  FDC: direct fetch fdc_id={fdc_id_override} ('{query}')")
                    food = fdc.get_food(fdc_id_override)
                else:
                    log(f"  FDC: searching '{query}' (prefer_generic={prefer_generic})")
                    food = fdc.lookup(query, prefer_generic=prefer_generic)
            except Exception as exc:
                log(f"  FDC error: {exc}")
                entry["fdc_result"] = f"error: {exc}"

            if food and food.found and food.values:
                log(f"  FDC: FOUND — {food.description!r} (fdc_id={food.fdc_id}, type={food.data_type})")
                nutrition_applied = extract_fdc_nutrition(food)
                log(f"  FDC panel extracted: {count_non_null(nutrition_applied)} non-null fields")
                prov_dict = food.provenance.as_dict() if food.provenance else None
                source_name = "usda_fdc"
                entry["fdc_result"] = f"found: {food.description!r} fdc_id={food.fdc_id}"
                is_generic = prefer_generic or fdc_id_override in (173430, 173410, 171314, 789828)
                entry["notes"].append(
                    f"{'Generic' if is_generic else 'Branded'} composition reference from USDA FDC "
                    f"(fdc_id={food.fdc_id}, type={food.data_type}, description={food.description!r}). "
                    f"{'Not a SKU match — directional generic enrichment.' if is_generic else 'Brand-matched entry.'}"
                )
            else:
                log(f"  FDC: not found")
                entry["fdc_result"] = "not_found"

        # ----------------------------------------------------------------
        # Step 3: Apply findings to the BSIP1 record
        # ----------------------------------------------------------------
        if nutrition_applied is not None:
            # Patch the record in by_barcode (which points to the same dict in products)
            target = by_barcode[barcode]
            old_sufficiency = target.get("data_sufficiency")

            target["normalized_nutrition_per_100g"] = nutrition_applied
            target["external_nutrition_provenance"] = prov_dict
            target["data_sufficiency"] = assess_sufficiency(nutrition_applied)
            target["nutrition_basis_detected"] = "per_100g"
            target["nutrition_basis_claimed"] = "per_100g (external source)"
            target["confidence"]["nutrition_confidence"] = "candidate_external"
            target["enrichment_version"] = "bsip1_enrichment_v1_ext_20260605"

            if ingredients_applied and not target.get("ingredients_text_he"):
                target["ingredients_text_he"] = ingredients_applied
                target["ingredients_raw"] = ingredients_applied
                target["ingredients_raw_provenance"] = {
                    "source": source_name,
                    "populated_at": "bsip1_enrichment_v1_ext_20260605",
                    "missing": False,
                    "note": f"Ingredients from {source_name} (barcode {barcode}); candidate status.",
                    "verification_status": "candidate",
                }

            recovered = [k for k, v in nutrition_applied.items() if v is not None]
            remaining_null = [k for k, v in nutrition_applied.items() if v is None]
            entry["source_used"] = source_name
            entry["fields_recovered"] = recovered
            entry["fields_remaining_null"] = remaining_null
            entry["new_data_sufficiency"] = target["data_sufficiency"]

            log(f"  Applied. sufficiency: {old_sufficiency} → {target['data_sufficiency']}")
            if target["data_sufficiency"] == "sufficient":
                enriched_count += 1
        else:
            entry["source_used"] = None
            entry["fields_recovered"] = []
            entry["fields_remaining_null"] = list(
                by_barcode[barcode].get("normalized_nutrition_per_100g", {}).keys()
            )
            entry["new_data_sufficiency"] = "insufficient"
            log(f"  No data found — remains insufficient.")

        report_entries.append(entry)

    # ----------------------------------------------------------------
    # Rebuild products list preserving original order
    # ----------------------------------------------------------------
    updated_products = [by_barcode.get(p["barcode"], p) for p in products]

    # Write updated BSIP1
    with open(BSIP1_PATH, "w", encoding="utf-8") as f:
        json.dump(updated_products, f, ensure_ascii=False, indent=2)
    log(f"\nWrote updated BSIP1: {BSIP1_PATH}")

    # ----------------------------------------------------------------
    # Compute summary counts for report
    # ----------------------------------------------------------------
    resolved = sum(1 for e in report_entries if e["new_data_sufficiency"] == "sufficient")
    still_insufficient = sum(1 for e in report_entries if e["new_data_sufficiency"] != "sufficient")

    report = {
        "run_id": "butter_enrichment_20260605",
        "task": "TASK-191",
        "phase": "A",
        "stage": "BSIP1_external_enrichment",
        "generated_utc": now_iso(),
        "bsip1_source": str(BSIP1_PATH),
        "total_insufficient_targeted": len(insufficient),
        "resolved_to_sufficient": resolved,
        "still_insufficient": still_insufficient,
        "enrichment_sources_used": ["open_food_facts", "usda_fdc"],
        "edpg_status": "all_external_data_candidate_status",
        "notes": [
            "All external nutrition values are born verification_status=candidate.",
            "USDA FDC entries are generic composition references, not SKU matches.",
            "OFF entries are barcode-matched but crowd-sourced; pending QA promotion.",
            "No scored traces were modified. Phase B (BSIP2) is blocked until QA gate.",
        ],
        "products": report_entries,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    log(f"\nWrote enrichment report: {REPORT_PATH}")
    log(f"\nSummary: {resolved}/{len(insufficient)} products resolved to sufficient.")
    log(f"Still insufficient: {still_insufficient}")


if __name__ == "__main__":
    enrich()
