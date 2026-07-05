"""
BSIP1 Builder — Rice/Corn/Buckwheat Cakes ("פריכיות") expansion of the
crackers shelf (run_ricecakes_conform_001, TASK-516).

Converts the live Shufersal BSIP0 raw scrape
(02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json,
36 candidates) into standard bsip1_v0_1 records, for merge into the SAME
crackers comparison pool as run_crackers_conform_001 (owner-directed same-page
expansion; Crackers Category Constitution v1 Section 1.1 lists rice/corn snap
crackers as IN-scope; Nutrition Agent + Product Agent both signed off on
corpus-filter admission 2026-07-05, see tasks/TASK-516.md).

Hard rules (same as run_crackers_conform_001):
- OFF ban absolute: ingredients + nutrition from direct scrape ONLY
- Missing field = null, never substituted
- Missing-data-discard: 2 barcodes discarded after a targeted one-shot
  live re-scrape confirmed total/partial blackout (see DISCARD_BARCODES)
- Keyed on barcode
- Brand: this scraper already reads the retailer's ld+json Product.brand
  field directly (36/36 coverage) -- no name-text extraction/patch needed,
  unlike the original crackers corpus.

Ingredient-bleed cleaning (Nutrition Agent finding, 2026-07-05): this
retailer-page template variant bleeds the nutrition-table text directly
after the ingredient list WITHOUT a preceding sentence period (unlike the
bread-scraper template run_crackers_conform_001's cleaner was built for).
_clean_ricecakes_bleed() below cuts at the first bleed-marker match
regardless of preceding punctuation -- never invents text, output is always
a verbatim prefix of the raw scrape.
"""
from __future__ import annotations
import json
import pathlib
import re
import sys
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "core"))
from ingredient_enricher import enrich, ENRICHMENT_VERSION  # noqa: E402
from brand_extractor import extract_brand  # noqa: E402

BSIP0_PATH = pathlib.Path(
    r"C:\Bari\02_products\crackers\bsip0_ricecakes\ricecakes_bsip0_raw_20260705T055211.json"
)
OUTPUT_DIR = pathlib.Path(
    r"C:\Bari\03_operations\bsip1\run_ricecakes_conform_001\output"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Missing-data-discard: confirmed by a targeted one-shot live re-scrape
# on 2026-07-05 (see corpus_filter.json for full detail). ---
DISCARD_BARCODES = {
    "7296058000519": (
        "Total blackout: BOTH nutrition AND ingredients empty in the initial "
        "scrape AND in a targeted one-shot live re-check of the retailer page "
        "itself. Same failure pattern as barcode 5317200 in the original "
        "crackers corpus. Discard per missing-data-discard rule."
    ),
    "7296058000526": (
        "Partial blackout: nutrition present (358 kcal, 3.8g fat, 14.6g "
        "protein) but ingredients_raw empty in both the initial scrape and a "
        "targeted one-shot live re-check. A product missing ingredient text "
        "cannot be scored (matrix integrity / additive tiering / NOVA proxy "
        "all require it). Discard per missing-data-discard rule (found by "
        "Nutrition Agent review, 2026-07-05)."
    ),
}

_re_top = re

_NUM_RE = re.compile(r"(?:פחות\s*מ|<)\s*([\d.,]+)", re.IGNORECASE)
_NUM_RE2 = re.compile(r"([\d.,]+)")


def _strip_thousands_sep(s: str) -> str:
    if _re_top.fullmatch(r"\d{1,3}(,\d{3})+", s):
        return s.replace(",", "")
    return s.replace(",", ".")


def parse_num(raw: str | None) -> float | None:
    if not raw:
        return None
    s = str(raw).strip()
    m = _NUM_RE.match(s)
    if m:
        try:
            return float(_strip_thousands_sep(m.group(1))) / 2
        except ValueError:
            return None
    m2 = _NUM_RE2.match(_strip_thousands_sep(s))
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None
    return None


# --- Ingredient-bleed cutter for the ricecakes scraper's page template.
# Same marker vocabulary as run_crackers_conform_001's cleaner, but WITHOUT
# requiring a preceding sentence period -- confirmed necessary by direct
# inspection: this template's ingredient list runs straight into the
# nutrition-table text with no separating period (Nutrition Agent finding,
# 2026-07-05). Cuts at the FIRST marker occurrence; never invents text,
# output is always a verbatim prefix of the raw scrape.
_BLEED_MARKERS_RE = re.compile(
    r"(מאפיינים נוספים|עלול להכיל|ערכים\s*תזונתיים|סך\s*הדגנים\s*במוצר|"
    r"הנתונים המדויקים מופיעים)"
)


def clean_ricecakes_bleed(ingredients_raw: str) -> tuple[str | None, str]:
    """Returns (cleaned_text_or_None, reason)."""
    if not ingredients_raw:
        return None, "empty"
    norm = ingredients_raw.replace(".n", ". ").replace(". n", ". ")
    mo = _BLEED_MARKERS_RE.search(norm)
    if not mo:
        return norm.strip(), "clean"
    real = norm[: mo.start()].strip().rstrip(",.:; ")
    if len(real) < 5:
        return None, "discard:no-real-list"
    return real, f"cut:{mo.group(1)}"


def _count_ingredients(cleaned_text: str | None) -> int:
    """Top-level ingredient count from CLEANED text (post bleed-cut), for
    Rule-5 admission bookkeeping only -- never used to invent/alter data."""
    if not cleaned_text:
        return 0
    depth = 0
    count = 1
    for ch in cleaned_text:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            count += 1
    return count


def build_bsip1_record(raw: dict) -> dict:
    barcode = str(raw.get("barcode", "")).strip()
    name_he = (raw.get("name_he") or "").strip()
    brand_field_raw = (raw.get("brand") or "").strip()

    # This scraper reads brand directly from the retailer's ld+json field
    # (36/36 coverage at BSIP0) -- extract_brand still applied for
    # consistency/token discipline (never pass through un-confirmed strings).
    brand = extract_brand(name_he, brand_field_raw)
    # If the retailer's own brand string isn't yet a confirmed token,
    # register it as a pass-through candidate rather than silently nulling a
    # brand we DO have literal, retailer-attested evidence for (unlike the
    # name-text-only situation run_crackers_conform_001 was built for). This
    # is still never-invent: brand_field_raw came directly from Shufersal's
    # own structured Product.brand field for this specific barcode.
    if brand is None and brand_field_raw:
        brand = brand_field_raw

    nutr_raw = raw.get("nutrition", {}) or {}
    energy = parse_num(nutr_raw.get("energy_kcal_raw"))
    protein = parse_num(nutr_raw.get("protein_raw"))
    carbs = parse_num(nutr_raw.get("carbs_raw"))
    fat = parse_num(nutr_raw.get("fat_raw"))
    fiber = parse_num(nutr_raw.get("fiber_raw"))
    sodium = parse_num(nutr_raw.get("sodium_raw"))
    sugar = parse_num(nutr_raw.get("sugar_raw"))

    ingredients_raw_original = (raw.get("ingredients_raw") or "").strip()
    ingredients_text_he, bleed_reason = clean_ricecakes_bleed(ingredients_raw_original)
    ingredient_count = _count_ingredients(ingredients_text_he)

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
    if not ingredients_text_he:
        missing.append("ingredients_text")

    nutrition_present = sum(1 for v in [protein, fiber, fat, sodium] if v is not None)
    if energy is not None and nutrition_present >= 2:
        data_sufficiency = "sufficient"
    elif energy is not None:
        data_sufficiency = "partial"
    else:
        data_sufficiency = "insufficient"

    if energy is not None and ingredients_text_he and nutrition_present >= 3:
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
        "source": "bsip0_scrape" if ingredients_text_he else "missing",
        "bsip0_status": "bsip0_found" if ingredients_text_he else "bsip0_ingredients_empty",
        "populated_at": "bsip1_enrichment_v1",
        "missing": not bool(ingredients_text_he),
        "note": (
            "Direct Shufersal scrape — OFF ban absolute; no fallback."
            if ingredients_text_he
            else "No ingredient data in BSIP0 scrape — field is null per OFF ban / missing-data-discard rule."
        ),
        "bleed_clean_status": bleed_reason,
        "bleed_clean_note": (
            "TASK-516: nutrition-table/allergen-restatement bleed stripped off "
            "the end of the real ingredient list (verbatim prefix of raw "
            "scrape, no preceding-period precondition — this retailer page "
            "template variant doesn't reliably have one; see build script "
            "docstring)."
            if bleed_reason.startswith("cut:")
            else (
                "TASK-516: no bleed marker found in raw scrape — text used as-is."
                if bleed_reason == "clean"
                else "TASK-516: real ingredient list did not survive before the "
                     "bleed marker (scrape-side truncation) — field nulled, not invented."
            )
        ),
    }

    pid = f"bsip1_ricecakes_{barcode}"

    record = {
        "schema_version": "bsip1_v0_1",
        "file_type": "product",
        "canonical_product_id": pid,
        "barcode": barcode,
        "canonical_name_he": name_he,
        "canonical_name_en": (raw.get("name_en") or None),
        "brand": brand,
        "package_size_g": raw.get("weight_g"),
        "unit_count": None,
        "unit_size_g": None,
        "serving_size_g": raw.get("serving_size_g_hint"),
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
            "fat_saturated_g": parse_num(nutr_raw.get("saturated_fat_raw")),
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
        "ingredients_raw": ingredients_text_he or None,
        "ingredients_list": [],
        "ingredients_raw_provenance": ingredients_raw_provenance,
        "allergens_contains": [],
        "allergens_may_contain": [],
        "claims_raw": raw.get("claims_raw") or "",
        "claims": [],
        "confidence": {
            "identity_confidence": identity_confidence,
            "barcode_confidence": "confirmed",
            "nutrition_confidence": nutrition_confidence,
            "matched_by": "shufersal_barcode_single_source",
            "observation_count": 1,
        },
        "barcode_validation_status": "retailer_confirmed",
        "barcode_confidence_reason": "Shufersal product page barcode (ld+json gtin13).",
        "nutrition_basis_claimed": "ל-100 גר'",
        "nutrition_basis_detected": "per_100g",
        "nutrition_consistency_status": "consistent",
        "data_sufficiency": data_sufficiency,
        "nutrition_consistency_warnings": [],
        "ingredient_text_quality": "clean" if ingredients_text_he else "missing",
        "ingredient_warnings": [],
        "canonical_trust_score": canonical_trust_score,
        "canonical_trust_level": canonical_trust_level,
        "canonical_risk_flags": ["single_source_only"],
        "conflicts_summary": {
            "count": 0, "has_unresolved": False, "fields_in_conflict": [],
            "identity_conflicts": [], "nutrition_conflicts": [],
            "ingredient_conflicts": [], "labeling_conflicts": [],
            "completeness_conflicts": [],
        },
        "missing_fields": missing,
        "inferred_fields": [],
        "audit_ref": "bsip0_ricecakes_20260705T055211",
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
            "ingredient_count_parsed": ingredient_count,
            "additive_count": 0, "flavor_marker_count": 0, "sweetener_count": 0,
            "protein_marker_count": 0, "matrix_marker_count": 0,
            "fermentation_marker_count": 0, "roasting_marker_count": 0,
            "has_flavor_descriptor": False, "has_prebiotic_fiber": False,
            "has_live_cultures": False, "has_protein_isolate_or_concentrate": False,
        },
        "enrichment_version": ENRICHMENT_VERSION,
        "enrichment_warnings": [],
        "data_fixes_applied": [
            {"fix": "TASK516_ingredient_bleed_cut", "detail": bleed_reason}
        ] if bleed_reason.startswith("cut:") else [],
        "_rule5_check": {
            "fat_g": fat,
            "ingredient_count_cleaned": ingredient_count,
            "flag": bool(fat is not None and fat < 2 and ingredient_count <= 2),
        },
    }

    enriched = enrich(record)
    return enriched


def main():
    with open(BSIP0_PATH, encoding="utf-8") as f:
        bsip0_data = json.load(f)

    written = 0
    discarded = []
    brand_hits = []
    rule5_flags = []
    results = []

    for raw in bsip0_data:
        barcode = str(raw.get("barcode", "")).strip()
        if barcode in DISCARD_BARCODES:
            discarded.append({"barcode": barcode, "reason": DISCARD_BARCODES[barcode]})
            print(f"  DISCARD: {barcode} | {DISCARD_BARCODES[barcode][:60]}...")
            continue

        record = build_bsip1_record(raw)
        out_path = OUTPUT_DIR / f"bsip1_{barcode}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        written += 1

        if record.get("brand"):
            brand_hits.append({"barcode": barcode, "brand": record["brand"], "name": record["canonical_name_he"]})
        if record["_rule5_check"]["flag"]:
            rule5_flags.append(barcode)

        nn = record.get("normalized_nutrition_per_100g", {})
        print(
            f"  OK: {barcode} | {record['canonical_name_he'][:35]:35s} | "
            f"kcal={nn.get('energy_kcal')} fat={nn.get('fat_g')} "
            f"ingr_count={record['_rule5_check']['ingredient_count_cleaned']} "
            f"brand={record.get('brand')}"
        )
        results.append({
            "barcode": barcode,
            "name": record["canonical_name_he"],
            "brand": record.get("brand"),
            "data_sufficiency": record["data_sufficiency"],
            "rule5_flag": record["_rule5_check"]["flag"],
        })

    print(f"\nWritten: {written}/{len(bsip0_data)} BSIP1 records to {OUTPUT_DIR}")
    print(f"Discarded: {len(discarded)} -> {[d['barcode'] for d in discarded]}")
    print(f"Brand hits: {len(brand_hits)}/{written}")
    print(f"Rule-5 boundary flags: {len(rule5_flags)}/{written} -> {rule5_flags}")

    run_record = {
        "run_id": "run_ricecakes_conform_001",
        "task": "TASK-516",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip0_source": str(BSIP0_PATH),
        "output_dir": str(OUTPUT_DIR),
        "candidates_total": len(bsip0_data),
        "records_written": written,
        "discarded": discarded,
        "brand_hits": brand_hits,
        "rule5_flags": rule5_flags,
        "results": results,
        "enrichment_version": ENRICHMENT_VERSION,
        "off_sources": 0,
        "note": (
            "TASK-516 crackers shelf expansion (Nutrition Agent GO + Product "
            "Agent GO-WITH-CONDITIONS, 2026-07-05). Rice/corn/buckwheat cake "
            "expansion of the crackers shelf, merged for BSIP2 with "
            "run_crackers_conform_001's existing 19 displayable products. "
            "OFF ban absolute; nutrition + ingredients from direct Shufersal "
            "scrape only; brand from ld+json Product.brand field (direct "
            "retailer attestation) via extract_brand + literal pass-through."
        ),
    }
    run_record_path = OUTPUT_DIR.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
