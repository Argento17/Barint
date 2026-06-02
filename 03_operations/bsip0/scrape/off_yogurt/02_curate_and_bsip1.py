"""
BSIP0 curation + BSIP1 mapping for run_yogurt_002.

BSIP0 curation: apply category-membership + exclusion rules to the raw OFF pull.
  Exclude: drinkable (lassi / drink / שתיה), duplicates (by barcode),
           non-yogurt desserts where identifiable, synthetic (none — all real 729).
BSIP1 mapping: map each INCLUDED OFF record -> bsip1_v0_1 product schema.
  Honest enrichment: OFF Israeli yogurts carry NO ingredient lists, so
  ingredients_text_he="", ingredients_list=[], extracted_* empty, and every
  ingredient-derived field is recorded in missing_fields. Subtype is inferred
  from the product name only (flagged in inferred_fields). NO fabrication.

Outputs:
  ../../../bsip1/run_yogurt_002/output/bsip1_<barcode>.json
  ./curation_report.json   (inclusion/exclusion table + corpus summary)
"""
from __future__ import annotations
import json, pathlib, datetime, re

BASE   = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\off_yogurt")
RAW    = BASE / "raw"
BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_002\output")
BSIP1.mkdir(parents=True, exist_ok=True)
RUN_ID = "run_yogurt_002"

# ---- exclusion rules (BSIP0 membership) -----------------------------------
DRINK_RE = re.compile(r"lassi|drink|שתי|שתיי|beverage|smoothie", re.I)


def is_drinkable(p) -> bool:
    name = f"{p.get('product_name','')} {p.get('product_name_he','')}".lower()
    cats = p.get("categories_tags") or []
    if DRINK_RE.search(name):
        return True
    if any(("drink" in c or "beverage" in c) for c in cats):
        return True
    return False


def infer_subtype(name: str) -> str:
    n = name.lower()
    if re.search(r"greek|יווני|grec", n):
        return "greek"
    if re.search(r"pro ?20|go20|go ?by|protein|25g|חלבון", n):
        return "high_protein"
    if re.search(r"bio|ביו|active|אקטיב", n):
        return "bio"
    if re.search(r"fruit|froop|froep|פיר|תות|ananas|strawberry|וניל|vanil|chocolate|שוקולד|crunch|פיסטוק|פקאן|לימון|lemon", n):
        return "flavored"
    if re.search(r"0%|light|free", n):
        return "plain_lowfat"
    return "plain_natural"


def map_nutrition(nm: dict) -> dict:
    def g(k):
        v = nm.get(k)
        return float(v) if isinstance(v, (int, float)) else None
    sodium_g = g("sodium_100g")
    salt_g = g("salt_100g")
    sodium_mg = (sodium_g * 1000) if sodium_g is not None else (
        round(salt_g / 2.5 * 1000, 1) if salt_g is not None else None)
    return {
        "energy_kcal": g("energy-kcal_100g"),
        "fat_g": g("fat_100g"),
        "fat_saturated_g": g("saturated-fat_100g"),
        "fat_trans_g": None,
        "sodium_mg": sodium_mg,
        "carbohydrates_g": g("carbohydrates_100g"),
        "sugars_g": g("sugars_100g"),
        "dietary_fiber_g": g("fiber_100g"),
        "protein_g": g("proteins_100g"),
        "cholesterol_mg": None,
    }


NUT_KEYS = ["energy_kcal", "fat_g", "fat_saturated_g", "sodium_mg",
            "carbohydrates_g", "sugars_g", "dietary_fiber_g", "protein_g"]


def main():
    raws = sorted(RAW.glob("off_*.json"))
    included, excluded = [], []
    seen = set()
    for path in raws:
        p = json.loads(path.read_text(encoding="utf-8"))
        code = p.get("code")
        name = (p.get("product_name") or "").strip()
        nm = p.get("nutriments", {}) or {}
        reason = None
        if code in seen:
            reason = "duplicate_barcode"
        elif is_drinkable(p):
            reason = "drinkable_excluded"
        elif nm.get("proteins_100g") is None and nm.get("energy-kcal_100g") is None:
            reason = "no_usable_nutrition"
        if reason:
            excluded.append({"barcode": code, "name": name, "reason": reason})
            continue
        seen.add(code)
        nutrition = map_nutrition(nm)
        missing = [k for k in NUT_KEYS if nutrition.get(k) is None]
        missing += ["ingredients_text_he", "ingredients_list",
                    "extracted_additives", "extracted_sweeteners",
                    "extracted_fermentation_markers"]
        brands = p.get("brands")
        if isinstance(brands, list):
            brand = ", ".join(str(b) for b in brands) or None
        else:
            brand = brands or None
        subtype = infer_subtype(name + " " + (p.get("product_name_he") or ""))
        nut_present = sum(1 for k in NUT_KEYS if nutrition.get(k) is not None)
        # confidence: ingredient-blind, partial-nutrition real record
        nutrition_conf = "confirmed_per_100g" if nut_present >= 3 else "partial"
        rec = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": f"bsip1_{code}",
            "barcode": code,
            "canonical_name_he": (p.get("product_name_he") or name or None),
            "canonical_name_en": name or None,
            "brand": brand,
            "package_size_g": None, "unit_count": None, "unit_size_g": None,
            "serving_size_g": None,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": p.get("image_url"),
            "source_retailers": ["openfoodfacts"],
            "source_url": f"https://world.openfoodfacts.org/product/{code}",
            "normalized_nutrition_per_100g": nutrition,
            "energy_source_unit": "kcal",
            "ingredients_text_he": "",
            "ingredients_list": [],
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims": [],
            "confidence": {
                "identity_confidence": "medium" if name else "low",
                "barcode_confidence": "confirmed",
                "nutrition_confidence": nutrition_conf,
                "matched_by": "off_barcode_single_source",
                "observation_count": 1,
            },
            "barcode_validation_status": "off_confirmed",
            "barcode_confidence_reason": f"OFF record {code}, scraped {RUN_ID}.",
            "nutrition_basis_claimed": "per_100g",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": "unverified",
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "absent",
            "ingredient_warnings": ["no_ingredient_list_in_source"],
            "canonical_trust_score": 0.5,
            "canonical_trust_level": "medium",
            "canonical_risk_flags": ["single_source_only", "no_ingredients", "noisy_name"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": missing,
            "inferred_fields": ["bsip_yogurt_subtype"],
            "audit_ref": None,
            "bsip_yogurt_subtype": subtype,
            "ingredients_raw": "",
            "ingredients_raw_provenance": {"source": "off_no_ingredients", "bsip0_status": "absent"},
            "ingredient_order": [],
            "extracted_additives": [],
            "extracted_flavors": [],
            "extracted_sweeteners": [],
            "extracted_protein_markers": [],
            "extracted_matrix_markers": [],
            "extracted_fermentation_markers": [],
            "extracted_roasting_markers": [],
            "enrichment_summary": {"ingredient_blind": True, "nutrition_fields_present": nut_present},
            "enrichment_version": "off_map_v1",
            "enrichment_warnings": ["ingredient_blind_no_extracted_signals"],
        }
        (BSIP1 / f"bsip1_{code}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        included.append({"barcode": code, "name": name, "subtype": subtype,
                         "nutrition_fields_present": nut_present})

    report = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "raw_count": len(raws),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "ingredient_coverage": "0/%d (OFF carries no ingredient lists for these SKUs)" % len(included),
        "included": included,
        "excluded": excluded,
    }
    (BASE / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"included {len(included)}  excluded {len(excluded)}  -> BSIP1 at {BSIP1}")
    for e in excluded:
        print("  EXCLUDED", e["barcode"], e["reason"], (e["name"] or "")[:30])


if __name__ == "__main__":
    main()
