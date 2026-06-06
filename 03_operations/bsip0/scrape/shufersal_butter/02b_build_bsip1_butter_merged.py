"""
BSIP1 Builder — Butter Merged Corpus (TASK-191, Stage B).

Reads:  C:\\Bari\\02_products\\butter\\bsip0_outputs\\butter_merged_corpus.json
Writes: C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_merged.json

Differences from 02_build_bsip1_butter.py:
  - Reads the merged (multi-retailer) corpus, not just Shufersal.
  - Keeps off_miss records in corpus with data_sufficiency="insufficient"
    and extraction_confidence="off_miss" (owner decision: show as INSUFFICIENT).
  - Respects subtype_override from merge step (item 10 = flavored_herbed).
  - Respects extraction_confidence="medium" for items 6+7 (no nutrition panel).
  - Sets source_retailers from the retailer_id field.
  - CURATION: Applies same EXCLUDE_SIGNALS as before.
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

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

MERGED_PATH = pathlib.Path(r"C:\Bari\02_products\butter\bsip0_outputs\butter_merged_corpus.json")
OUT_DIR = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs")

_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _parse_num(raw):
    if not raw and raw != 0:
        return None
    s = str(raw).strip()
    # Strip thousands separators: if comma is followed by exactly 3 digits (and not a
    # decimal separator), it's a thousands comma — remove it. "1,200" → "1200".
    # Then handle decimal comma: "0,5" → "0.5".
    import re as _re
    s = _re.sub(r",(\d{3})(?!\d)", r"\1", s)  # remove thousands comma
    s = s.replace(",", ".")                     # remaining commas are decimal separators
    m = _NUM_RE.search(s)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def _parse_sodium(raw):
    val = _parse_num(raw)
    if val is None:
        return None
    s = str(raw).lower()
    # Israeli nutrition labels report sodium in mg/100g.
    # The heuristic: values ≤ 3000 mg/100g are plausible (table salt = ~38,000 mg;
    # most foods top out well below 3000 mg/100g). Values in the 1–10 range on
    # Shufersal labels are mg, not g — do NOT multiply by 1000. The old
    # "val <= 10 → treat as g" heuristic was wrong (7 mg unsalted butter is valid).
    if "mg" in s:
        return val
    if val <= 3000:
        return val   # Already mg/100g
    # val > 3000: implausible as mg (e.g. 7000, 8000 from g × 1000 bug) — null it out
    return None


def _parse_nutrition(n: dict) -> dict:
    return {
        "energy_kcal":     _parse_num(n.get("energy_kcal_raw")),
        "fat_g":           _parse_num(n.get("fat_raw")),
        "fat_saturated_g": _parse_num(n.get("saturated_fat_raw")),
        "fat_trans_g":     None,
        "cholesterol_mg":  None,
        "sodium_mg":       _parse_sodium(n.get("sodium_raw") or ""),
        "carbohydrates_g": _parse_num(n.get("carbs_raw")),
        "sugars_g":        _parse_num(n.get("sugar_raw")),
        "dietary_fiber_g": _parse_num(n.get("fiber_raw")),
        "protein_g":       _parse_num(n.get("protein_raw")),
    }


_SPLIT_RE = re.compile(r"[,;،]\s*")


def _parse_ingredients(raw: str) -> list[str]:
    if not raw:
        return []
    raw = re.sub(r"\s+", " ", raw).strip()
    nutrition_bleed_re = re.compile(
        r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", re.DOTALL
    )
    raw = nutrition_bleed_re.sub("", raw).strip().rstrip(".")
    out = []
    for p in _SPLIT_RE.split(raw):
        p = p.strip().strip(".")
        if p and len(p) > 1:
            out.append(p)
    return out


def _classify_subtype(name: str, ingr: str, override: str | None = None) -> str:
    if override:
        return override
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


SPREAD_NAME_RE = re.compile(r"^\s*ממרח|ממרח חמאה", re.I)
BUTTER_FLAVOR_RE = re.compile(r"בטעם חמאה|butter[\s-]?flavou?r", re.I)
VEGETABLE_FAT_PRIMARY_RE = re.compile(
    r"^(?:שמנים צמחיים|שמן צמחי|שמן קוקוס|שמן דקל|שמן תירס|שמן סויה)", re.I
)


def _curate(raw: dict) -> str | None:
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"
    if SPREAD_NAME_RE.search(name):
        return "butter_spread_excluded"
    if BUTTER_FLAVOR_RE.search(name):
        return "butter_flavor_excluded"
    ingr_text = (raw.get("ingredients_raw") or "").strip()
    ingr_clean = re.sub(
        r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", "",
        ingr_text, flags=re.DOTALL
    ).strip()
    if VEGETABLE_FAT_PRIMARY_RE.search(ingr_clean):
        return "vegetable_fat_excluded"
    return None


def _confidence(nn: dict, ingr_list: list[str], raw_conf: str, retailer_id: str = "unknown") -> dict:
    # If the raw record is off_miss (no nutrition from OFF), honour as insufficient
    if raw_conf == "off_miss":
        return {
            "confidence": {
                "identity_confidence": "low",
                "barcode_confidence": "confirmed",
                "nutrition_confidence": "missing",
                "matched_by": "seed_barcode_no_off_panel",
                "observation_count": 0,
            },
            "canonical_trust_score": 0.35,
            "canonical_trust_level": "low",
            "missing_fields": ["energy_kcal", "fat_g", "fat_saturated_g",
                               "protein_g", "carbohydrates_g"],
            "nutrition_consistency_status": "missing",
            "data_sufficiency": "insufficient",
        }

    nutr_fields = ["energy_kcal", "protein_g", "fat_g", "fat_saturated_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3
    ingr_ok = len(ingr_list) >= 1

    # "medium" from merge step (items 6+7 with no nutrition)
    if raw_conf == "medium" and not nutr_ok:
        return {
            "confidence": {
                "identity_confidence": "medium",
                "barcode_confidence": "confirmed",
                "nutrition_confidence": "partial",
                "matched_by": "retailer_barcode_no_panel",
                "observation_count": 1,
            },
            "canonical_trust_score": 0.45,
            "canonical_trust_level": "low",
            "missing_fields": [f for f in nutr_fields if nn.get(f) is None],
            "nutrition_consistency_status": "partial",
            "data_sufficiency": "insufficient",
        }

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
            "matched_by": f"{retailer_id}_barcode",
            "observation_count": 1,
        },
        "canonical_trust_score": trust,
        "canonical_trust_level": lvl,
        "missing_fields": missing,
        "nutrition_consistency_status": "consistent" if nutr_ok else "partial",
        "data_sufficiency": "sufficient" if nutr_ok else "insufficient",
    }


def main():
    if not MERGED_PATH.exists():
        log.error("Merged corpus not found: %s", MERGED_PATH)
        log.error("Run 03_merge_butter_corpus.py first.")
        return

    raws = json.loads(MERGED_PATH.read_text(encoding="utf-8"))
    log.info("Loaded %d records from merged corpus", len(raws))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "butter_bsip1_merged.json"
    report_path = OUT_DIR / "butter_curation_report_merged.json"

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

        raw_conf = (raw.get("extraction_confidence") or "high").lower()
        nn = _parse_nutrition(raw.get("nutrition", {}))
        ingr_text = (raw.get("ingredients_raw") or "").strip()
        ingr_clean = re.sub(
            r"(?:ערכים תזונתיים|הנתונים המדויקים|מכיל חלב|עלול להכיל).*", "",
            ingr_text, flags=re.DOTALL
        ).strip()
        ingr_list = _parse_ingredients(ingr_clean)
        claims_raw = raw.get("claims_raw", "")

        retailer_id = raw.get("retailer_id", "unknown")
        subtype_override = raw.get("subtype_override")
        subtype = _classify_subtype(name, ingr_clean, subtype_override)
        conf = _confidence(nn, ingr_list, raw_conf, retailer_id)
        pid = f"bsip1_butter_{barcode}"

        image_url = None
        image_urls = raw.get("image_urls") or []
        if image_urls:
            image_url = image_urls[0]

        # Provenance stamp
        prov = raw.get("provenance", {})

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
            "image_url": image_url,
            "image_urls": image_urls,
            "source_retailers": [retailer_id],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_clean,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": prov.get("source", "bsip0_scrape"),
                "bsip0_status": f"bsip0_{retailer_id}",
                "populated_at": "bsip1_build_butter_merged_001",
                "missing": not bool(ingr_clean),
                "note": (
                    f"Scraped from {retailer_id} (run_butter_merged_001 / TASK-191)"
                    if raw_conf != "off_miss"
                    else f"OFF miss — no panel retrieved for barcode {barcode}"
                ),
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": claims_raw,
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": f"{retailer_id} barcode / seed list",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "data_sufficiency": conf["data_sufficiency"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "clean" if ingr_clean else "missing",
            "ingredient_warnings": [] if ingr_clean else ["no_ingredient_list_in_source"],
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": (
                ["single_source_only"] if conf["canonical_trust_level"] != "low"
                else ["no_nutrition_panel", "seed_barcode_only"]
            ),
            "conflicts_summary": {
                "count": 0, "has_unresolved": False,
                "fields_in_conflict": [], "identity_conflicts": [],
                "nutrition_conflicts": [], "ingredient_conflicts": [],
                "labeling_conflicts": [], "completeness_conflicts": [],
            },
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_butter_subtype"],
            "audit_ref": None,
            "bsip_butter_subtype": subtype,
            "price": raw.get("price", ""),
            "price_per_100g": raw.get("price_per_100g"),
            "acquisition_query": raw.get("acquisition_query", ""),
            "retailer_id": retailer_id,
            # Provenance envelope (EDPG)
            "ingestion_provenance": prov if prov else None,
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

    # Write BSIP1 output
    out_path.write_text(json.dumps(included_records, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("BSIP1 merged output: %s (%d products)", out_path, len(included_records))

    # Curation report
    n_ingr = sum(1 for r in included_records if r.get("ingredients_text_he"))
    n_suff = sum(1 for r in included_records if r.get("data_sufficiency") == "sufficient")
    n_insuff = sum(1 for r in included_records if r.get("data_sufficiency") == "insufficient")
    n_enriched = sum(1 for r in included_records if r.get("enrichment_version"))

    retailer_counts: dict[str, int] = {}
    for r in included_records:
        rid = r.get("retailer_id", "unknown")
        retailer_counts[rid] = retailer_counts.get(rid, 0) + 1

    included_summary = []
    for r in included_records:
        included_summary.append({
            "barcode": r["barcode"],
            "name": r["canonical_name_he"],
            "brand": r["brand"],
            "retailer": r.get("retailer_id"),
            "subtype": r.get("bsip_butter_subtype"),
            "has_ingredients": bool(r.get("ingredients_text_he")),
            "nutrition_fields": sum(1 for v in r["normalized_nutrition_per_100g"].values() if v is not None),
            "data_sufficiency": r.get("data_sufficiency"),
            "additives": [a["term"] for a in r.get("extracted_additives", [])],
            "fermentation_markers": [f["term"] for f in r.get("extracted_fermentation_markers", [])],
        })

    report = {
        "run_id": "run_butter_merged_001",
        "task": "TASK-191",
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(MERGED_PATH),
        "raw_count": len(raws),
        "included_count": len(included_records),
        "excluded_count": len(excluded),
        "retailer_breakdown": retailer_counts,
        "ingredient_coverage": f"{n_ingr}/{len(included_records)}",
        "data_sufficient": f"{n_suff}/{len(included_records)}",
        "data_insufficient": f"{n_insuff}/{len(included_records)}",
        "enriched_count": n_enriched,
        "included": included_summary,
        "excluded": excluded,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Curation report: %s", report_path)
    log.info("Sufficient: %d  Insufficient: %d  Excluded: %d",
             n_suff, n_insuff, len(excluded))
    log.info("Retailer breakdown: %s", retailer_counts)

    return included_records, out_path


if __name__ == "__main__":
    main()
