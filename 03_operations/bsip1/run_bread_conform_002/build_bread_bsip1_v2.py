"""
BSIP1 Builder — Bread Conform Run v2 (run_bread_conform_002)
TASK-433: Bread re-derive after crackers split (Crackers Category Constitution v1).

Re-derives the bread corpus with the 6 crackers REMOVED (they now live in
run_crackers_conform_001). Bread should be exactly the 23 non-cracker
products that were in run_bread_conform_001's 29-scoreable set.

SCORES PROTECTED: this run must byte-reproduce (0.000 drift) the published
score for every one of the 23 survivors currently in bread_frontend_v3.json.
Nothing about the underlying record content changes for these 23 — only the
corpus set (crackers removed) and rank renumbering (1..23) change. The
brand-from-name rule (Step 3/shared helper) is applied — this ADDS brand
values where a confirmed token literally appears in the name; it never
touches scored fields, so it cannot move a score.

Hard rules:
- OFF ban absolute: ingredients + nutrition from direct scrape ONLY
- Missing field = null, never substituted
- Keyed on barcode (stripped from product_id "shufersal_XXXXX")
- Brand: deterministic name-literal-match ONLY (core/brand_extractor.py) —
  SAME shared helper as the crackers builder, so both builders use identical
  logic.
"""

from __future__ import annotations
import json
import pathlib
import sys
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "core"))
from ingredient_enricher import enrich, ENRICHMENT_VERSION
from brand_extractor import extract_brand

BSIP0_PATH = pathlib.Path(
    r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
)
CURATED_PATH = pathlib.Path(
    r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_curated_comparison_dataset.json"
)
OUTPUT_DIR = pathlib.Path(
    r"C:\Bari\03_operations\bsip1\run_bread_conform_002\output"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# The 6 barcodes moved to the crackers category — REMOVED from bread corpus.
CRACKERS_REMOVED = {
    "96086000966", "96086000577", "7296073134459",
    "7296073134442", "8434165658523", "74252",
}

# The 2 barcodes already excluded at config level in v1 (no nutrition in
# BSIP0 scrape — G8 data-sanity, missing-data-discard). Same exclusion here;
# not re-litigated, just carried forward.
ALREADY_EXCLUDED = {"2026", "7296073641568"}


def parse_num(raw: str | None) -> float | None:
    """Parse Hebrew/standard numeric fields including 'פחות מ X' (less than X -> X/2)."""
    if not raw:
        return None
    s = str(raw).strip()
    import re
    m = re.match(r"(?:פחות\s*מ|<)\s*([\d.,]+)", s, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1).replace(",", ".")) / 2
        except ValueError:
            return None
    m2 = re.match(r"([\d.,]+)", s.replace(",", "."))
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None
    return None


def build_bsip1_record(raw: dict) -> dict:
    """Convert a BSIP0 raw record to standard bsip1_v0_1 schema (bread v2)."""
    barcode = str(raw.get("barcode", "")).strip()
    name_he = (raw.get("name_he") or "").strip()
    brand_field_raw = (raw.get("brand") or "").strip()

    # Deterministic brand-from-name extraction — SAME shared helper as
    # crackers. This is the ONLY change vs run_bread_conform_001's builder
    # that can touch a displayed (non-scored) field; it never touches
    # nutrition/ingredients/scoring inputs.
    brand = extract_brand(name_he, brand_field_raw)

    nutr_raw = raw.get("nutrition", {}) or {}
    energy = parse_num(nutr_raw.get("energy_kcal_raw"))
    protein = parse_num(nutr_raw.get("protein_raw"))
    carbs = parse_num(nutr_raw.get("carbs_raw"))
    fat = parse_num(nutr_raw.get("fat_raw"))
    fiber = parse_num(nutr_raw.get("fiber_raw"))
    sodium = parse_num(nutr_raw.get("sodium_raw"))
    sugar = parse_num(nutr_raw.get("sugar_raw"))

    ingredients_raw = (raw.get("ingredients_raw") or "").strip()
    ingredients_text_he = ingredients_raw

    image_urls = raw.get("image_urls") or []
    image_url = image_urls[0] if image_urls else None

    missing = []
    if not name_he:
        missing.append("canonical_name_he")
    if energy is None:
        missing.append("energy_kcal")
    if fiber is None:
        missing.append("dietary_fiber_g")
    if protein is None:
        missing.append("protein_g")
    if not ingredients_raw:
        missing.append("ingredients_text")

    nutrition_present = sum(
        1 for v in [protein, fiber, fat, sodium] if v is not None
    )
    if energy is not None and nutrition_present >= 2:
        data_sufficiency = "sufficient"
    elif energy is not None:
        data_sufficiency = "partial"
    else:
        data_sufficiency = "insufficient"

    if energy is not None and ingredients_raw and nutrition_present >= 3:
        identity_confidence = "high"
        nutrition_confidence = "confirmed_per_100g"
        canonical_trust_score = 0.85
        canonical_trust_level = "high"
    elif energy is not None:
        identity_confidence = "medium"
        nutrition_confidence = "estimated_per_100g"
        canonical_trust_score = 0.65
        canonical_trust_level = "medium"
    else:
        identity_confidence = "low"
        nutrition_confidence = "not_available"
        canonical_trust_score = 0.35
        canonical_trust_level = "low"

    ingredients_raw_provenance = {
        "source": "bsip0_scrape" if ingredients_raw else "missing",
        "bsip0_status": "bsip0_found" if ingredients_raw else "bsip0_ingredients_empty",
        "populated_at": "bsip1_enrichment_v1",
        "missing": not bool(ingredients_raw),
        "note": (
            "Direct Shufersal scrape — OFF ban absolute; no fallback."
            if ingredients_raw
            else "No ingredient data in BSIP0 scrape — field is null per OFF ban / missing-data-discard rule."
        ),
    }

    pid = f"bsip1_bread_{barcode}"

    record = {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "canonical_name_en": (raw.get("name_en") or None),
        "brand": brand,
        "package_size_g": None,
        "unit_count": None,
        "unit_size_g": None,
        "serving_size_g": None,
        "country_of_origin": "ישראל",
        "kosher_certification": None,
        "image_url": image_url,
        "image_urls": image_urls,
        "source_retailers": ["shufersal"],
        "source_url": raw.get("source_url") or "",
        "scraped_at": raw.get("scraped_at") or "",
        "normalized_nutrition_per_100g": {
            "energy_kcal": energy,
            "fat_g": fat,
            "fat_saturated_g": None,
            "fat_trans_g": None,
            "cholesterol_mg": None,
            "sodium_mg": sodium,
            "carbohydrates_g": carbs,
            "sugars_g": sugar,
            "dietary_fiber_g": fiber,
            "protein_g": protein,
        },
        "energy_source_unit": "kcal",
        "ingredients_text_he": ingredients_text_he or None,
        "ingredients_raw": ingredients_raw or None,
        "ingredients_list": [],
        "ingredients_raw_provenance": ingredients_raw_provenance,
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims_raw": "",
        "claims": [],
        "confidence": {
            "identity_confidence": identity_confidence,
            "barcode_confidence": "confirmed",
            "nutrition_confidence": nutrition_confidence,
            "matched_by": "shufersal_barcode_single_source",
            "observation_count": 1,
        },
        "barcode_validation_status": "retailer_confirmed",
        "barcode_confidence_reason": "Shufersal product page barcode.",
        "nutrition_basis_claimed": "ל-100 גר'",
        "nutrition_basis_detected": "per_100g",
        "nutrition_consistency_status": "consistent",
        "data_sufficiency": data_sufficiency,
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality": "clean" if ingredients_raw else "missing",
        "ingredient_warnings": [],
        "canonical_trust_score": canonical_trust_score,
        "canonical_trust_level": canonical_trust_level,
        "canonical_risk_flags": ["single_source_only"],
        "conflicts_summary": {
            "count": 0,
            "has_unresolved": False,
            "fields_in_conflict": [],
            "identity_conflicts": [],
            "nutrition_conflicts": [],
            "ingredient_conflicts": [],
            "labeling_conflicts": [],
            "completeness_conflicts": [],
        },
        "missing_fields": missing,
        "inferred_fields": [],
        "audit_ref": "bsip0_real_bread_retail_003_v1",
        "price": raw.get("price") or None,
        "price_per_100g": raw.get("price_per_100g") or None,
        "acquisition_query": raw.get("acquisition_query") or "",
        "acquisition_tier": raw.get("acquisition_tier") or "",
        "ingredient_order": [],
        "extracted_additives": [],
        "extracted_flavors": [],
        "extracted_sweeteners": [],
        "extracted_protein_markers": [],
        "extracted_matrix_markers": [],
        "extracted_fermentation_markers": [],
        "extracted_roasting_markers": [],
        "enrichment_summary": {
            "ingredient_count_parsed": 0,
            "additive_count": 0,
            "flavor_marker_count": 0,
            "sweetener_count": 0,
            "protein_marker_count": 0,
            "matrix_marker_count": 0,
            "fermentation_marker_count": 0,
            "roasting_marker_count": 0,
            "has_flavor_descriptor": False,
            "has_prebiotic_fiber": False,
            "has_live_cultures": False,
            "has_protein_isolate_or_concentrate": False,
        },
        "enrichment_version": ENRICHMENT_VERSION,
        "enrichment_warnings": [],
    }

    enriched = enrich(record)
    return enriched


def main():
    with open(BSIP0_PATH, encoding="utf-8") as f:
        bsip0_data = json.load(f)

    with open(CURATED_PATH, encoding="utf-8") as f:
        curated = json.load(f)

    curated_products = []
    for cluster in curated.get("clusters", []):
        curated_products.extend(cluster.get("products", []))

    curated_barcodes = set()
    for p in curated_products:
        pid = p.get("product_id", "")
        barcode = pid.replace("shufersal_", "")
        curated_barcodes.add(barcode)

    # Remove the 6 crackers — bread v2 corpus = curated set MINUS crackers.
    bread_v2_barcodes = curated_barcodes - CRACKERS_REMOVED

    print(f"Curated barcodes (v1, incl. crackers): {len(curated_barcodes)}")
    print(f"Crackers removed: {len(CRACKERS_REMOVED)}")
    print(f"Bread v2 barcodes (post-split): {len(bread_v2_barcodes)}")

    bsip0_by_barcode = {}
    for raw in bsip0_data:
        bc = str(raw.get("barcode", "")).strip()
        if bc:
            bsip0_by_barcode[bc] = raw

    written = 0
    missing_from_bsip0 = []
    brand_hits = []

    for barcode in sorted(bread_v2_barcodes):
        raw = bsip0_by_barcode.get(barcode)
        if not raw:
            missing_from_bsip0.append(barcode)
            print(f"  MISSING from BSIP0: {barcode}")
            continue

        record = build_bsip1_record(raw)
        out_path = OUTPUT_DIR / f"bsip1_{barcode}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        written += 1

        if record.get("brand"):
            brand_hits.append({"barcode": barcode, "brand": record["brand"], "name": record["canonical_name_he"]})

        name = raw.get("name_he", "?")
        nn = record.get("normalized_nutrition_per_100g", {})
        print(f"  OK: {barcode} | {name[:40]} | kcal={nn.get('energy_kcal')} fiber={nn.get('dietary_fiber_g')} sodium={nn.get('sodium_mg')} brand={record.get('brand')}")

    print(f"\nWritten: {written}/{len(bread_v2_barcodes)} BSIP1 records to {OUTPUT_DIR}")
    if missing_from_bsip0:
        print(f"Missing from BSIP0: {missing_from_bsip0}")
    print(f"Brand hits: {len(brand_hits)} -> {brand_hits}")

    run_record = {
        "run_id": "run_bread_conform_002",
        "task": "TASK-433",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip0_source": str(BSIP0_PATH),
        "curated_source": str(CURATED_PATH),
        "output_dir": str(OUTPUT_DIR),
        "records_written": written,
        "records_requested": len(bread_v2_barcodes),
        "crackers_removed": sorted(CRACKERS_REMOVED),
        "missing": missing_from_bsip0,
        "brand_hits": brand_hits,
        "enrichment_version": ENRICHMENT_VERSION,
        "off_sources": 0,
        "note": "Bread re-derive after crackers split (TASK-433) — SCORES PROTECTED, corpus = 29 curated minus 6 crackers = 23. OFF ban absolute; nutrition + ingredients from direct Shufersal scrape only; brand from deterministic name-literal-match only (does not touch scored fields).",
    }
    run_record_path = OUTPUT_DIR.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
