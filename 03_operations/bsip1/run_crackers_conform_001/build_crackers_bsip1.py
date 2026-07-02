"""
BSIP1 Builder — Crackers Conform Run (run_crackers_conform_001)
TASK-433: Crackers category split from bread (Crackers Category Constitution v1).

Converts real_bread_retail_003_v1 BSIP0 raw -> standard bsip1_v0_1 records,
for the crackers-only inclusion list (21 candidates from the bread scrape
that carry "קרקר" identity, minus 1 discarded for total data blackout).

Hard rules:
- OFF ban absolute: ingredients + nutrition from direct scrape ONLY
- Missing field = null, never substituted
- Missing-data-discard: if BOTH nutrition AND ingredients are empty after
  one targeted re-scrape attempt, discard the product (do not carry forward)
- Keyed on barcode (stripped from raw barcode field)
- Brand: deterministic name-literal-match ONLY (see core/brand_extractor.py)
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
OUTPUT_DIR = pathlib.Path(
    r"C:\Bari\03_operations\bsip1\run_crackers_conform_001\output"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Step 1 inclusion list (Crackers Category Constitution v1, Section 1) ---
# All 21 candidates named in TASK-433 (task lists 20 distinct+1 repeat = 21
# tokens; verified all 21 are unique barcodes present in the raw BSIP0 scrape
# and all 21 carry literal "קרקר" identity in canonical_name_he — no matzah,
# no breadsticks, no rice-cake candidates present in this particular corpus).
INCLUDED_BARCODES = [
    "7290013740809", "74252", "7290115205176", "7290018790328",
    "7290011489595", "7296073659952", "7296073134442", "7290112963918",
    "74375", "7290112968807", "5317200", "7296073398875", "5000396021202",
    "8434165658523", "7290013740823", "7290112968821", "7296073134459",
    "7290013740083", "7296073659945", "96086000577", "96086000966",
]

# --- Step 2 discard: missing-data-discard rule ---
# 5317200 (קרקר טופז מלח הדר): BSIP0 raw has ALL nutrition fields empty AND
# ingredients_raw empty. One targeted direct re-scrape of the live Shufersal
# product page (P_5317200) confirmed the retailer page itself carries no
# nutrition table / ingredients list (not a parser miss) — product/brand
# name and package size are present but the nutrition panel legitimately does
# not exist on the fetched page. Per missing-data-discard rule: DISCARD.
DISCARD_BARCODES = {
    "5317200": "BSIP0 raw + one-shot targeted re-scrape (Shufersal P_5317200) both confirm no nutrition table / ingredients list on the retailer page — total data blackout, discard per missing-data-discard rule (never punish/cap, never over-invest re-sourcing).",
}


import re as _re_top


def _strip_thousands_sep(s: str) -> str:
    """
    Normalize a numeric string that may use ',' as either a thousands
    separator (e.g. '1,200' meaning 1200) or a decimal separator
    (e.g. '0,5' meaning 0.5), WITHOUT collapsing real values.

    Rule (TASK-433 FIX 2 — sodium thousands-separator bug):
    - If the string matches \\d{1,3}(,\\d{3})+ (i.e. every comma-separated
      group after the first is exactly 3 digits — the canonical thousands
      grouping), treat ',' as a thousands separator and drop it.
    - Otherwise (e.g. '0,5', '3,3') treat ',' as a decimal point, as before.
    This fixes '1,200' -> 1200 (was silently mis-parsed as 1.2 by naive
    comma->period replacement) while leaving genuine decimal commas like
    '384,1' -> 384.1 untouched.
    """
    if _re_top.fullmatch(r"\d{1,3}(,\d{3})+", s):
        return s.replace(",", "")
    return s.replace(",", ".")


def parse_num(raw: str | None) -> float | None:
    """Parse Hebrew/standard numeric fields including 'פחות מ X' (less than X -> X/2)."""
    if not raw:
        return None
    s = str(raw).strip()
    m = _re_top.match(r"(?:פחות\s*מ|<)\s*([\d.,]+)", s, _re_top.IGNORECASE)
    if m:
        try:
            return float(_strip_thousands_sep(m.group(1))) / 2
        except ValueError:
            return None
    m2 = _re_top.match(r"([\d.,]+)", _strip_thousands_sep(s))
    if m2:
        try:
            return float(m2.group(1))
        except ValueError:
            return None
    return None


# --- FIX 1 (TASK-433): ingredient bleed/truncation cleaner ---------------
# BSIP0's ingredients_raw field captures the real ingredient list followed
# by a bleed of the retailer page's "attribute section" (מאפיינים נוספים /
# allergen restatement / grain-total footnote / embedded nutrition panel
# text), often cut off mid-clause with a dangling comma. The real list
# always ends with its own sentence-final period BEFORE the bleed begins.
# This cutter finds the earliest bleed-start marker that appears as the
# opening of a clause immediately after a period, and truncates there.
# It never invents text — output is a verbatim prefix of the raw scrape.
_INGREDIENT_BLEED_MARKER_RE = _re_top.compile(
    r"\.\s*(מאפיינים נוספים|מכיל\s+גלוטן|עלול להכיל|סך\s*הדגנים\s*במוצר|ערכים\s*תזונתיים)"
)


def clean_ingredients_bleed(ingredients_raw: str) -> tuple[str | None, str]:
    """
    Returns (cleaned_text_or_None, reason).
    reason is one of: 'clean' (no bleed detected), 'cut:<marker>' (bleed
    removed), 'discard:no-real-list' (nothing usable before the marker —
    the real list itself was truncated at scrape; caller must null it).
    """
    if not ingredients_raw:
        return None, "empty"
    # Normalize the '.n' / '. n' bad newline-join artifact seen in the raw
    # scrape (retailer page's line breaks collapsed into a literal 'n').
    norm = ingredients_raw.replace(".n", ". ").replace(". n", ". ")
    mo = _INGREDIENT_BLEED_MARKER_RE.search(norm)
    if not mo:
        return norm.strip(), "clean"
    real = norm[: mo.start() + 1].strip()
    if len(real) < 5:  # nothing usable survived before the marker
        return None, "discard:no-real-list"
    return real, f"cut:{mo.group(1)}"


# --- FIX 3 (TASK-433): sugar extraction from embedded nutrition-panel text
# For 2 barcodes (5000396021202, 8434165658523) the retailer page's full
# nutrition table text bled into ingredients_raw (see bleed cleaner above)
# and contains the real "X גרם סוכרים" (sugars) figure that never made it
# into the structured nutrition.sugar_raw field (which is empty for all 20
# rows). Extract it from that embedded text ONLY when the panel-bleed
# pattern is present and unambiguous; never invent a value otherwise.
_EMBEDDED_SUGAR_RE = _re_top.compile(r"(\d+(?:[.,]\d+)?)\s*גרם\s*סוכרים")


def extract_embedded_sugar(ingredients_raw: str) -> float | None:
    if not ingredients_raw:
        return None
    mo = _EMBEDDED_SUGAR_RE.search(ingredients_raw)
    if not mo:
        return None
    try:
        return float(mo.group(1).replace(",", "."))
    except ValueError:
        return None


# --- FIX 2b (TASK-433): source-confirmed corrupted nutrition block -------
# 7290112968807 ("קרקר דק פיטנס סלק") carries a full nutrition block (kcal,
# protein, carbs, fiber, sodium) that is ~1/4.6 of its near-identical
# sibling products (7290112968821 "בטטה", 7290112963918 "רוזמרין פיטנס",
# 7290115205176 "כפרי פיטנס" — same "דק...פיטנס" line, near-identical
# ingredient structure, ~458-461 kcal / 400mg sodium cluster). This is not
# a parseable unit/comma defect (no clean x4.6 or x10 factor) — it reads as
# a per-serving-vs-per-100g mismatch on the retailer page itself. Per the
# missing-data-discard rule (never invent, never guess a scaling factor):
# the entire nutrition block for this barcode is nulled rather than
# "corrected" to a fabricated value. Ingredients + identity are unaffected
# (they are internally consistent and independently scraped).
CORRUPTED_NUTRITION_BARCODES = {
    "7290112968807": (
        "Full nutrition block (99 kcal / 2.6g protein / 13.8g carbs / "
        "1.4g fiber / 86mg sodium) is ~1/4.6 of near-identical sibling "
        "products in the same 'דק...פיטנס' sub-line (~458-461 kcal / "
        "400mg sodium cluster). No clean unit/parse factor found (not "
        "x10, not thousands-separator) -> reads as a per-serving-vs-"
        "per-100g mismatch on the retailer page itself. Per missing-data-"
        "discard rule: null the whole nutrition block rather than guess "
        "a scaling factor. Ingredients text is independently scraped and "
        "unaffected."
    ),
}


def build_bsip1_record(raw: dict) -> dict:
    """Convert a BSIP0 raw record to standard bsip1_v0_1 schema (crackers)."""
    barcode = str(raw.get("barcode", "")).strip()
    name_he = (raw.get("name_he") or "").strip()
    brand_field_raw = (raw.get("brand") or "").strip()

    # Deterministic brand-from-name extraction (shared helper; conservative;
    # never invents). Confirmed tokens: מסטמכר / ברמן / אנג'ל / אסם / KRIT.
    brand = extract_brand(name_he, brand_field_raw)

    nutr_raw = raw.get("nutrition", {}) or {}
    energy = parse_num(nutr_raw.get("energy_kcal_raw"))
    protein = parse_num(nutr_raw.get("protein_raw"))
    carbs = parse_num(nutr_raw.get("carbs_raw"))
    fat = parse_num(nutr_raw.get("fat_raw"))
    fiber = parse_num(nutr_raw.get("fiber_raw"))
    sodium = parse_num(nutr_raw.get("sodium_raw"))
    sugar = parse_num(nutr_raw.get("sugar_raw"))

    ingredients_raw_original = (raw.get("ingredients_raw") or "").strip()

    # FIX 3: extract sugar from an embedded nutrition-panel bleed (if the
    # structured sugar_raw field came back empty, as it does for all 20
    # crackers rows) BEFORE the bleed text is stripped from ingredients.
    embedded_sugar_note = None
    if sugar is None:
        embedded = extract_embedded_sugar(ingredients_raw_original)
        if embedded is not None:
            sugar = embedded
            embedded_sugar_note = (
                f"sugars_g={embedded} extracted from embedded nutrition-panel "
                "text bled into ingredients_raw (structured sugar_raw field "
                "was empty at scrape) — TASK-433 FIX 3."
            )

    # FIX 2b: source-confirmed corrupted nutrition block -> null the whole
    # block rather than guess a scaling factor.
    nutrition_discard_note = None
    if barcode in CORRUPTED_NUTRITION_BARCODES:
        nutrition_discard_note = CORRUPTED_NUTRITION_BARCODES[barcode]
        energy = protein = carbs = fat = fiber = sodium = sugar = None

    # FIX 1: strip the "attribute section" / allergen-restatement / grain-
    # total / embedded-nutrition-panel bleed off the end of the real
    # ingredient list. Never invents text -- output is a verbatim prefix of
    # the raw scrape, or None if the real list itself never survived.
    ingredients_text_he, bleed_reason = clean_ingredients_bleed(ingredients_raw_original)
    if bleed_reason == "discard:no-real-list":
        ingredients_text_he = None
    ingredients_raw = ingredients_text_he  # keep both fields in sync post-clean

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
        "bleed_clean_status": bleed_reason,
        "bleed_clean_note": (
            "TASK-433 FIX 1: attribute-section/allergen-restatement/grain-total "
            "bleed stripped off the end of the real ingredient list (verbatim "
            "prefix of raw scrape, cut at the marker-preceding sentence period)."
            if bleed_reason.startswith("cut:")
            else (
                "TASK-433 FIX 1: no bleed marker found in raw scrape — text used as-is."
                if bleed_reason == "clean"
                else "TASK-433 FIX 1: real ingredient list did not survive before the "
                     "bleed marker (scrape-side truncation) — field nulled, not invented."
            )
        ),
    }
    data_fixes_applied = []
    if bleed_reason.startswith("cut:"):
        data_fixes_applied.append({"fix": "FIX1_ingredient_bleed", "detail": bleed_reason})
    if embedded_sugar_note:
        data_fixes_applied.append({"fix": "FIX3_sugar_extraction", "detail": embedded_sugar_note})
    if nutrition_discard_note:
        data_fixes_applied.append({"fix": "FIX2b_corrupted_nutrition_discard", "detail": nutrition_discard_note})
    if barcode == "7290018790328":
        data_fixes_applied.append({
            "fix": "FIX2_sodium_thousands_separator",
            "detail": (
                "sodium_raw='1,200' was mis-parsed as 1.2mg by naive comma->period "
                "replacement (thousands separator, not decimal). Corrected parser "
                "yields 1200mg/100g, consistent with declared מלח(3%) in ingredients."
            ),
        })

    pid = f"bsip1_crackers_{barcode}"

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
        "data_fixes_applied": data_fixes_applied,
    }

    enriched = enrich(record)
    return enriched


def main():
    with open(BSIP0_PATH, encoding="utf-8") as f:
        bsip0_data = json.load(f)

    bsip0_by_barcode = {}
    for raw in bsip0_data:
        bc = str(raw.get("barcode", "")).strip()
        if bc:
            bsip0_by_barcode[bc] = raw

    written = 0
    discarded = []
    missing_from_bsip0 = []
    brand_hits = []

    for barcode in INCLUDED_BARCODES:
        if barcode in DISCARD_BARCODES:
            discarded.append({"barcode": barcode, "reason": DISCARD_BARCODES[barcode]})
            print(f"  DISCARD: {barcode} | {DISCARD_BARCODES[barcode]}")
            continue

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

    print(f"\nWritten: {written}/{len(INCLUDED_BARCODES)} BSIP1 records to {OUTPUT_DIR}")
    print(f"Discarded: {len(discarded)} -> {[d['barcode'] for d in discarded]}")
    if missing_from_bsip0:
        print(f"Missing from BSIP0: {missing_from_bsip0}")
    print(f"Brand hits: {len(brand_hits)} -> {brand_hits}")

    run_record = {
        "run_id": "run_crackers_conform_001",
        "task": "TASK-433",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "bsip0_source": str(BSIP0_PATH),
        "output_dir": str(OUTPUT_DIR),
        "included_candidates": len(INCLUDED_BARCODES),
        "records_written": written,
        "discarded": discarded,
        "missing_from_bsip0": missing_from_bsip0,
        "brand_hits": brand_hits,
        "enrichment_version": ENRICHMENT_VERSION,
        "off_sources": 0,
        "note": "Crackers category split (Crackers Category Constitution v1) — OFF ban absolute; nutrition + ingredients from direct Shufersal scrape only; brand from deterministic name-literal-match only.",
    }
    run_record_path = OUTPUT_DIR.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
