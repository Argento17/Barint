"""
BSIP1 Builder — Butter / חמאה (run_butter_001) from Shufersal BSIP0 raw.

Reads:  C:\\Bari\\02_products\\butter\\bsip0_outputs\\butter_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_{ts}.json
        + bsip1_outputs/butter_curation_report.json

Schema: bsip1_v0_1 — mirrors run_cereals_002 / run_yogurt_003 BSIP1 files.
Enrichment: core ingredient_enricher.py (additives / matrix / sweeteners / etc.)

CURATION RULES (corpus purity):
  EXCLUDE:
    - "ממרח" spreads (name starts with ממרח / contains ממרח חמאה) — these are
      butter-blend spreads with water + vegetable oil, not pure butter
    - Vegetable-fat "butter flavor" products (no dairy fat as primary ingredient)
    - Products labeled "חמאה למריחה" where ingredients show <30% milk fat
      and substantial water + stabilizers (heavily processed spread)
    - "בטעם חמאה" (butter-flavored) products — flavor descriptor, not butter
    - Products with no usable nutrition at all (zero dairy-fat signature)
  INCLUDE:
    - All products with שמנת / שומן חלב / שמנת מפוסטרת as primary ingredient
    - Reduced-fat butter where label says "חמאה" prominently and primary = milk fat
    - Cultured/fermented butters (מחמצת, תרבית לקטית)
    - Ghee (גהי, חמאה מזוקקת) — clarified milk fat
"""
from __future__ import annotations

import json
import re
import sys
import pathlib
import logging
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip1\core")))
from ingredient_enricher import enrich as enrich_product

# Canonical BSIP0 numeric extraction (TASK-192 / EV-046) — single shared path so the
# "פחות מ N" handling + total_fat >= saturated_fat invariant never drift per-category.
sys.path.insert(0, str(pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\_shared")))
from bsip0_nutrition import (  # noqa: E402
    parse_num as _shared_parse_num,
    parse_sodium_mg as _shared_parse_sodium,
    parse_nutrition_numeric as _shared_parse_nutrition,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\butter\bsip0_outputs")
SOURCE = "shufersal"

# TASK-192 / EV-046: delegate to the canonical shared path (byte-identical for clean
# panels; adds the "פחות מ N" bound flag + total_fat >= saturated_fat invariant).
def _parse_num(raw):
    return _shared_parse_num(raw)


def _parse_sodium(raw):
    return _shared_parse_sodium(raw)


def _parse_nutrition(n: dict) -> dict:
    return _shared_parse_nutrition(n)


_SPLIT_RE = re.compile(r"[,;،]\s*")


def _parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []
    raw = re.sub(r"\s+", " ", raw).strip()
    # Strip trailing nutrition-info that bleeds through (common Shufersal artifact)
    # Nutrition values start with "ערכים תזונתיים" or a pattern of grams/kcal
    nutrition_bleed_re = re.compile(r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", re.DOTALL)
    raw = nutrition_bleed_re.sub("", raw).strip().rstrip(".")
    out = []
    for p in _SPLIT_RE.split(raw):
        p = p.strip().strip(".")
        if p and len(p) > 1:
            out.append(p)
    return out


def _classify_subtype(name: str, ingr: str) -> str:
    t = (name + " " + ingr).lower()
    if re.search(r"גהי|ghee|מזוקק|clarified", t):
        return "ghee_clarified"
    if re.search(r"מחמצת|cultured|מותסס|ferment|תרבית", t):
        return "cultured_fermented"
    if re.search(r"60%|חצי שמנ|reduced|מופחת שומן", t):
        return "reduced_fat"
    if re.search(r"עם מלח|מלוח|salted", t):
        return "salted"
    if re.search(r"ללא.*מלח|unsalted|ללת\"מ|ללתמ", t):
        return "unsalted"
    if re.search(r"מתובל|herb|תבלין", t):
        return "flavored_herbed"
    return "plain"


# ── Curation: exclude products that are NOT butter ─────────────────────────────

# "ממרח" spreads — butter-blend spreads with water + vegetable oil
SPREAD_NAME_RE = re.compile(r"^\s*ממרח|ממרח חמאה", re.I)

# "בטעם חמאה" — butter-flavored, not butter
BUTTER_FLAVOR_RE = re.compile(r"בטעם חמאה|butter[\s-]?flavou?r", re.I)

# Vegetable fat primary — product based on vegetable oils, not dairy fat
# Detected by: "שמנים צמחיים" / "שמן צמחי" / "שמן קוקוס" as first ingredient
VEGETABLE_FAT_PRIMARY_RE = re.compile(r"^(?:שמנים צמחיים|שמן צמחי|שמן קוקוס|שמן דקל|שמן תירס|שמן סויה)", re.I)

# Heavy-spread signature: substantial water content (>30%) + no cream as primary
# "חמאה למריחה" with water as first ingredient
WATER_PRIMARY_RE = re.compile(r"^מים\s+\d{2}", re.I)   # "מים 68.2%" as first ingredient


def _curate(raw: dict) -> str | None:
    """Return an exclusion reason string, or None if the product should be included."""
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"

    # "ממרח חמאה מופחת שומן" — Lurpak spread, water + rapeseed oil blend
    if SPREAD_NAME_RE.search(name):
        return "butter_spread_excluded"   # ממרח = spread, not pure butter

    # "בטעם חמאה" — flavored margarine substitute (Naturina/שמרית)
    if BUTTER_FLAVOR_RE.search(name):
        return "butter_flavor_excluded"   # flavor descriptor, not butter

    ingr_text = (raw.get("ingredients_raw") or "").strip()
    # Strip nutrition bleed from ingredient text before checking
    ingr_clean = re.sub(
        r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", "",
        ingr_text, flags=re.DOTALL
    ).strip()

    # Vegetable-fat primary (no dairy fat) — e.g. Naturina type
    if VEGETABLE_FAT_PRIMARY_RE.search(ingr_clean):
        return "vegetable_fat_excluded"

    # Water-primary spread — "מים 68.2%" as first major ingredient (heavy spread)
    if WATER_PRIMARY_RE.search(ingr_clean):
        return "water_primary_spread_excluded"

    nn = _parse_nutrition(raw.get("nutrition", {}))
    # Products with no nutrition AND no parseable ingredients = low confidence
    if nn.get("energy_kcal") is None and nn.get("fat_g") is None:
        # Allow if the barcode+name pattern is clearly butter AND has ingredients
        if not ingr_clean or len(ingr_clean) < 10:
            return "no_usable_nutrition"

    return None


def _confidence(nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "fat_g", "fat_saturated_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3
    ingr_ok = len(ingr_list) >= 1  # butter ingredients are short by nature

    if nutr_ok and ingr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "high", 0.80, "high"
    elif nutr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "medium", 0.65, "medium"
    elif ingr_ok:
        nutr_conf, id_conf, trust, lvl = "partial", "medium", 0.55, "medium"
    else:
        nutr_conf, id_conf, trust, lvl = "partial", "low", 0.45, "low"

    missing = []
    if not nutr_ok:
        missing += [f for f in nutr_fields if nn.get(f) is None]
    if not ingr_ok:
        missing.append("ingredients_list")

    return {
        "confidence": {
            "identity_confidence": id_conf,
            "barcode_confidence": "confirmed",
            "nutrition_confidence": nutr_conf,
            "matched_by": "shufersal_barcode_single_source",
            "observation_count": 1,
        },
        "canonical_trust_score": trust,
        "canonical_trust_level": lvl,
        "missing_fields": missing,
        "nutrition_consistency_status": "consistent" if nutr_ok else "partial",
        "data_sufficiency": "sufficient" if nutr_ok else "insufficient",
    }


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("butter_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No butter_bsip0_raw_*.json in %s", RAW_DIR)
        return

    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs") / f"butter_bsip1_{ts}.json"
    report_path = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs") / "butter_curation_report.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    included_records = []
    excluded = []
    seen = set()

    for raw in raws:
        name = (raw.get("name_he") or "").strip()
        barcode = str(raw.get("barcode", "")).strip()

        if barcode in seen:
            excluded.append({"barcode": barcode, "name": name, "reason": "duplicate_barcode"})
            continue

        reason = _curate(raw)
        if reason:
            excluded.append({"barcode": barcode, "name": name, "reason": reason})
            continue

        seen.add(barcode)

        nn = _parse_nutrition(raw.get("nutrition", {}))
        ingr_text = (raw.get("ingredients_raw") or "").strip()
        # Strip nutrition bleed from ingredient text
        ingr_clean = re.sub(
            r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", "",
            ingr_text, flags=re.DOTALL
        ).strip()
        ingr_list = _parse_ingredients(ingr_clean)
        claims_raw = raw.get("claims_raw", "")
        subtype = _classify_subtype(name, ingr_clean)
        conf = _confidence(nn, ingr_list)
        pid = f"bsip1_butter_{barcode}"

        record = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": raw.get("weight_g"),
            "unit_count": None, "unit_size_g": None,
            "serving_size_g": None,
            "country_of_origin": None,
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [SOURCE],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_clean,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "bsip0_scrape",
                "bsip0_status": "bsip0_scrape",
                "populated_at": "bsip1_build_butter_001",
                "missing": not bool(ingr_clean),
                "note": "Scraped from Shufersal product page (run_butter_001 / TASK-191)",
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": claims_raw,
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "Shufersal JSON-LD gtin13/sku.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "data_sufficiency": conf["data_sufficiency"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "clean" if ingr_clean else "missing",
            "ingredient_warnings": [] if ingr_clean else ["no_ingredient_list_in_source"],
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_butter_subtype"],
            "audit_ref": None,
            "bsip_butter_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
        }

        try:
            record = enrich_product(record)
        except Exception as e:
            log.warning("Enrichment error %s: %s", pid, e)
            for fld in ["extracted_additives", "extracted_flavors", "extracted_sweeteners",
                        "extracted_protein_markers", "extracted_matrix_markers",
                        "extracted_fermentation_markers", "extracted_roasting_markers"]:
                record.setdefault(fld, [])
            record.setdefault("enrichment_summary", {})
            record["enrichment_version"] = "bsip1_enrichment_v1"
            record["enrichment_warnings"] = [f"enrichment_error: {e}"]

        included_records.append(record)

    # ── Write BSIP1 output ───────────────────────────────────────────────────────
    out_path.write_text(json.dumps(included_records, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("BSIP1 output written: %s (%d products)", out_path, len(included_records))

    # ── Curation report ──────────────────────────────────────────────────────────
    n_ingr = sum(1 for r in included_records if r.get("ingredients_text_he"))
    n_suff = sum(1 for r in included_records if r.get("data_sufficiency") == "sufficient")
    n_enriched = sum(1 for r in included_records if r.get("enrichment_version"))
    n_additive = sum(1 for r in included_records if r.get("extracted_additives"))

    included_summary = []
    for r in included_records:
        included_summary.append({
            "barcode": r["barcode"],
            "name": r["canonical_name_he"],
            "brand": r["brand"],
            "subtype": r.get("bsip_butter_subtype"),
            "has_ingredients": bool(r.get("ingredients_text_he")),
            "nutrition_fields": sum(1 for v in r["normalized_nutrition_per_100g"].values() if v is not None),
            "data_sufficiency": r.get("data_sufficiency"),
            "additives": [a["term"] for a in r.get("extracted_additives", [])],
            "fermentation_markers": [f["term"] for f in r.get("extracted_fermentation_markers", [])],
            "price": r.get("price"),
        })

    report = {
        "run_id": "run_butter_001",
        "task": "TASK-191",
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raw_path),
        "raw_count": len(raws),
        "included_count": len(included_records),
        "excluded_count": len(excluded),
        "ingredient_coverage": f"{n_ingr}/{len(included_records)}",
        "data_sufficient": f"{n_suff}/{len(included_records)}",
        "enriched_count": n_enriched,
        "with_additives": n_additive,
        "included": included_summary,
        "excluded": excluded,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Curation report: %s", report_path)

    # ── Console summary ─────────────────────────────────────────────────────────
    log.info("Included %d  Excluded %d", len(included_records), len(excluded))
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included_records))
    log.info("Data sufficient: %d/%d", n_suff, len(included_records))

    return included_records, out_path


if __name__ == "__main__":
    main()
