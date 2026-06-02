"""
BSIP1 Builder — Yogurt (run_yogurt_003) from Shufersal BSIP0 raw.

Reads:  C:\\Bari\\02_products\\yogurt_system\\bsip0\\yogurt_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\03_operations\\bsip1\\run_yogurt_003\\output\\bsip1_*.json
        + curation_report.json (inclusion/exclusion table)

Schema: bsip1_v0_1 — mirrors the maadanim / snack-bar / bread-retail BSIP1 files.
Enrichment: core ingredient_enricher.py (additives / sweeteners / fermentation /
            protein markers) — this is what makes ingredient-driven yogurt scoring
            possible, unlike the ingredient-blind OFF run_yogurt_002.

Curation (final pass, on top of scrape-time name filtering):
  - dedup by barcode
  - exclude drinkable / dessert / supplement (name signals)
  - require spoon-yogurt identity
  - require usable nutrition (>=1 of energy/protein/carbs) to enter BSIP1
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

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip0")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_004\output")
RUN_ID = "run_yogurt_004"
SOURCE = "shufersal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Curation signals (final pass — mirrors scraper but defends against leakage)
DRINK_RE = re.compile(
    r"משקה|שתי|drink|שייק|smoothie|כפיר|kefir|איראן|ayran|לאסי|lassi|"
    r"אקטימל|actimel|יקולט|yakult|דנאקטיב|danactive", re.I)
DESSERT_RE = re.compile(
    r"מעדן|מילקי|מוס|פודינג|ברולה|פנה ?קוטה|קינוח|דניאלה", re.I)
SUPPLEMENT_RE = re.compile(r"תוסף|קפסול|טבליות|כמוסות", re.I)
NONYOGURT_RE = re.compile(
    r"גלידה|ice cream|חמאה|מרגרינה|שמנת|גבינה צהובה|גבינה לבנה|קוטג|קצפת|"
    r"זית|זיתים|olive", re.I)  # TASK-139C: olives leaked in via the "יווני"/greek include token
YOGURT_RE = re.compile(
    r"יוגורט|yog[hu]?urt|יווני|greek|סקיר|skyr|אקטיביה|activia|"
    r"\bביו\b|\bbio\b|\bפרו\b|\bpro\b|\bgo\b|froop|פרופ|מולר|m[uü]ller", re.I)

_NUM_RE = re.compile(r"(\d+(?:[.,]\d+)?)")


def _parse_num(raw):
    if not raw:
        return None
    m = _NUM_RE.search(str(raw).replace(",", "."))
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
    if "mg" in str(raw).lower() or val > 10:
        return val
    return val * 1000


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
    out = []
    for p in _SPLIT_RE.split(raw):
        p = p.strip().strip(".")
        if p and len(p) > 1:
            out.append(p)
    return out


def _classify_subtype(name: str) -> str:
    nl = name.lower()
    if re.search(r"יווני|greek|skyr|סקיר", nl):
        return "greek"
    if re.search(r"פרו|pro|go ?20|go20|25g|20g|חלבון|protein", nl):
        return "high_protein"
    if re.search(r"אקטיביה|activia|פרוביו|probiotic", nl):
        return "probiotic"
    if re.search(r"\bביו\b|\bbio\b", nl):
        return "bio"
    if re.search(r"0%|light|free|דל|ללא שומן|נטול", nl):
        return "plain_lowfat"
    if re.search(r"פירות|תות|פטל|אוכמ|וניל|vanil|פרי|בטעם|froop|פרופ|שוקולד|פיר|לימון|אפרסק|מנגו", nl):
        return "flavored"
    return "plain_natural"


def _curate(raw: dict) -> str | None:
    """Return exclusion reason, or None if included."""
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"
    if DRINK_RE.search(name):
        return "drinkable_excluded"
    if DESSERT_RE.search(name):
        return "dessert_excluded"
    if SUPPLEMENT_RE.search(name):
        return "supplement_excluded"
    if NONYOGURT_RE.search(name):
        return "non_yogurt_dairy_excluded"
    if not YOGURT_RE.search(name):
        return "not_spoon_yogurt"
    nn = _parse_nutrition(raw.get("nutrition", {}))
    if all(nn.get(k) is None for k in ("energy_kcal", "protein_g", "carbohydrates_g")):
        return "no_usable_nutrition"
    return None


def _confidence(nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "sugars_g", "fat_g", "carbohydrates_g"]
    n_present = sum(1 for f in nutr_fields if nn.get(f) is not None)
    nutr_ok = n_present >= 3
    ingr_ok = len(ingr_list) >= 2
    if nutr_ok and ingr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "high", 0.80, "high"
    elif nutr_ok:
        nutr_conf, id_conf, trust, lvl = "confirmed_per_100g", "medium", 0.65, "medium"
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
    }


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("yogurt_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No yogurt_bsip0_raw_*.json in %s", RAW_DIR)
        return
    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

    # clear stale output
    for f in OUT_DIR.glob("bsip1_*.json"):
        f.unlink()

    included, excluded = [], []
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
        ingr_list = _parse_ingredients(ingr_text)
        conf = _confidence(nn, ingr_list)
        subtype = _classify_subtype(name)
        pid = f"bsip1_yogurt_{barcode}"

        record = {
            "schema_version": "bsip1_v0_1",
            "file_type": "product",
            "canonical_product_id": pid,
            "barcode": barcode,
            "canonical_name_he": name,
            "canonical_name_en": None,
            "brand": raw.get("brand", ""),
            "package_size_g": raw.get("weight_g"),
            "unit_count": None, "unit_size_g": None, "serving_size_g": None,
            "country_of_origin": "ישראל",
            "kosher_certification": None,
            "image_url": (raw.get("image_urls") or [None])[0],
            "image_urls": raw.get("image_urls", []),
            "source_retailers": [SOURCE],
            "source_url": raw.get("source_url", ""),
            "normalized_nutrition_per_100g": nn,
            "energy_source_unit": "kcal",
            "ingredients_text_he": ingr_text,
            "ingredients_list": ingr_list,
            "ingredients_raw": ingr_text,
            "ingredients_raw_provenance": {
                "source": "bsip0_scrape",
                "bsip0_status": "bsip0_scrape",
                "populated_at": "bsip1_build_yogurt_003",
                "missing": not bool(ingr_text),
                "note": "Scraped from Shufersal product page (run_yogurt_003)",
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": raw.get("claims_raw", ""),
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "Shufersal JSON-LD gtin13/sku.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "nutrition_consistency_warnings": [],
            "ingredient_text_quality": "clean" if ingr_text else "missing",
            "ingredient_warnings": [] if ingr_text else ["no_ingredient_list_in_source"],
            "canonical_trust_score": conf["canonical_trust_score"],
            "canonical_trust_level": conf["canonical_trust_level"],
            "canonical_risk_flags": ["single_source_only"],
            "conflicts_summary": {"count": 0, "has_unresolved": False,
                                  "fields_in_conflict": [], "identity_conflicts": [],
                                  "nutrition_conflicts": [], "ingredient_conflicts": [],
                                  "labeling_conflicts": [], "completeness_conflicts": []},
            "missing_fields": conf["missing_fields"],
            "inferred_fields": ["bsip_yogurt_subtype"],
            "audit_ref": None,
            "bsip_yogurt_subtype": subtype,
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

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({
            "barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "has_cultures": record.get("enrichment_summary", {}).get("has_live_cultures", False),
            "ferment_markers": record.get("enrichment_summary", {}).get("fermentation_marker_count", 0),
        })

    n_ingr = sum(1 for i in included if i["has_ingredients"])
    report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raw_path),
        "raw_count": len(raws),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "ingredient_coverage": f"{n_ingr}/{len(included)}",
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    log.info("Included %d  Excluded %d  -> BSIP1 at %s", len(included), len(excluded), OUT_DIR)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included))
    # exclusion reason tally
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)


if __name__ == "__main__":
    main()
