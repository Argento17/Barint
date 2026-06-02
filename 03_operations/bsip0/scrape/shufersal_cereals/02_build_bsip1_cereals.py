"""
BSIP1 Builder — Breakfast Cereals (run_cereals_002) from Shufersal BSIP0 raw.

Reads:  C:\\Bari\\02_products\\breakfast_cereals\\bsip0_outputs\\cereals_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\03_operations\\bsip1\\run_cereals_002\\output\\bsip1_*.json
        + curation_report.json
        + cereals_constructs_report.json  (category-level rollup of the 4 governance constructs)

Schema: bsip1_v0_1 — mirrors run_yogurt_003 BSIP1 files.
Enrichment: core ingredient_enricher.py (additives / matrix markers / sweeteners).

APPLIES THE FOUR CEREALS GOVERNANCE CONSTRUCTS (cereals_gap_resolution_v1.md), as
label-observable CLASSIFICATION / DISCLOSURE layers — NOT score changes:
  C1 Granola sub-pool      (Constitution Art. II Rule 5 / Resolution 3, Sec 2.9)
  C2 Children's product    (Constitution Art. II Sec 2.8 / Resolution 1)
  C3 Whole-grain threshold (Guardrails v2 Sec 5.2.1 / Resolution 4)
  C4 Endemic fortification (Constitution Art. VI Sec 6.4 / Resolution 2, DISTORTION-004)
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

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip0_outputs")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_002\output")
RUN_ID = "run_cereals_002"
SOURCE = "shufersal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Curation signals (final pass — defends against scrape leakage) ──────────────
BAR_RE       = re.compile(r"חטיף|\bbar\b|\bבר\b|מקופלת|ביסקוויט|עוגי|ופל|wafer", re.I)
# Non-cereal contaminants that leak via grain tokens (כוסמין/דגנים/שיבולת שועל):
# breads, pita, rolls, sourdough loaves, and dairy desserts. Same false-positive class as
# the run_yogurt_003 olive leak — removed at curation for corpus purity (Constitution Art. II).
NONCEREAL_RE = re.compile(r"קרקר|cracker|פריכי|rice cake|משקה|\bdrink\b|יוגורט|yog[hu]?urt|"
                          r"דייסת תינוק|מטרנה|סימילק|תוסף|קפסול|חמאת|ממרח|שוקולד למריחה|"
                          r"לחם|לחמני|פיתה|פיתות|מחמצת|בגט|baguette|מעדן|פודינג|מוס", re.I)
CEREAL_RE    = re.compile(r"דגני|דגנים|קורנפלקס|corn ?flakes|גרנולה|granola|מוזלי|מוסלי|muesli|"
                          r"שיבולת שועל|קוואקר|quaker|צ'יריוס|cheerios|נסקוויק|nesquik|"
                          r"קוקו ?פופס|coco ?pops|צ'וקפיק|chocapic|פצפוצי|פצפוצים|כריות|"
                          r"פתיתי|בראן|\bbran\b|fitness|פיטנס|kellogg|weetabix|ויטבי|כוסמין|"
                          r"\bcereal\b|דייסה", re.I)

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


def _classify_subtype(name: str, ingr: str) -> str:
    t = (name + " " + ingr).lower()
    if re.search(r"גרנולה|granola", t):
        return "granola"
    if re.search(r"מוזלי|מוסלי|muesli", t):
        return "muesli"
    if re.search(r"קוקו ?פופס|נסקוויק|צ'וקפיק|coco ?pops|nesquik|chocapic|כריות|frosties|טריקס|trix", t):
        return "childrens_character"
    if re.search(r"בראן|\bbran\b|סובין", t):
        return "bran"
    if re.search(r"שיבולת שועל|קוואקר|quaker|oat", t):
        return "oat_cereal"
    if re.search(r"פצפוצי|פצפוצים|puffed|מנופח", t):
        return "puffed_extruded"
    if re.search(r"מלא|כוסמין מלא|whole|דגנים מלאים|weetabix|ויטבי", t):
        return "whole_grain_flakes"
    if re.search(r"קורנפלקס|corn ?flakes|פתיתי תירס", t):
        return "cornflakes"
    return "cereal_other"


def _curate(raw: dict) -> str | None:
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"
    if BAR_RE.search(name):
        return "bar_excluded_snack_overlap"
    if NONCEREAL_RE.search(name):
        return "non_cereal_excluded"
    if not CEREAL_RE.search(name):
        return "not_cereal"
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
        "data_sufficiency": "sufficient" if nutr_ok else "insufficient",
    }


# ══════════════════════════════════════════════════════════════════════════════
# THE FOUR CEREALS GOVERNANCE CONSTRUCTS
# ══════════════════════════════════════════════════════════════════════════════

WHOLE_GRAIN_RE   = re.compile(r"מלא|מלאה|מלאים|דגן(?:ים)? מלא|חיטה מלאה|שיפון מלא|"
                              r"כוסמין מלא|שיבולת שועל|whole ?grain|whole ?wheat|wholemeal", re.I)
WHOLE_CLAIM_RE   = re.compile(r"מלא|מלאה|מלאים|דגנים מלאים|חיטה מלאה|whole ?grain|whole ?wheat|100%", re.I)
REFINED_FLOUR_RE = re.compile(r"קמח חיטה(?!\s*מלא)|קמח לבן|סולת|semolina|קמח תירס", re.I)
KIDS_NAME_RE     = re.compile(r"ילדים|kids|junior|ג'וניור|מיני\b|mini\b|קטנטנים|growing|לגדול", re.I)
# Recognized child-mascot cereal brands: the brand name IS the animated-mascot identity
# (Nesquik=Quicky, Trix=rabbit, Coco Pops=Coco the monkey, Chocapic, Frosties=Tony). For these,
# the brand token jointly satisfies D1 (visual mascot) + D2 (child-targeting name). Auditable list,
# not open-ended. Per cereals_gap_resolution_v1 Sec 2.8 D1 definition (child-targeted mascot brand).
CHILD_MASCOT_RE  = re.compile(r"נסקוויק|nesquik|קוקו ?פופס|coco ?pops|קוקומן|cocoman|"
                              r"צ'וקפיק|chocapic|frosties|פרוסטיז|טריקס|trix|smacks|"
                              r"honey monster|כריות נוגט|כריות שוקו|כריות במילוי|lion|ליאון", re.I)
KIDS_CLAIM_RE    = re.compile(r"גדיל|לגדול|בית ?ספר|לילדים|growing|מתאים לילדים", re.I)
NAV_BOILERPLATE_RE = re.compile(r"קטגוריה|לתפריט הראשי|טוען מוצרים")
FORTIFY_RE       = re.compile(r"ויטמין|מינרל|מועשר|fortif|vitamin|ברזל\b|iron|אבץ|zinc|"
                              r"חומצה פולית|folic|ניאצין|niacin|ריבופלבין|riboflavin|"
                              r"תיאמין|thiamin|\bb1\b|\bb2\b|\bb6\b|\bb12\b|סידן", re.I)
OIL_RE           = re.compile(r"שמן|oil", re.I)
SYRUP_RE         = re.compile(r"סירופ|סילאן|דבש|honey|syrup|מולסה|נופת", re.I)


def _whole_grain_construct(name, claims, ingr_text, ingredient_order) -> dict:
    """Construct 3 — Guardrails v2 Sec 5.2.1 whole-grain threshold + Marketing Divergence Finding.
    Claim text source = name + ingredient/marketing text (claims_raw is nav boilerplate, unusable)."""
    claim_text = f"{name} {ingr_text}"
    claim_present = bool(WHOLE_CLAIM_RE.search(claim_text))

    # First grain ingredient test (ordering-based, per 5.2.1 detection method)
    first_grain_whole = None
    first_grain_pos = None
    for item in sorted(ingredient_order, key=lambda x: x.get("position") or 999):
        txt = item.get("text", "")
        is_grain = bool(re.search(r"קמח|דגן|חיטה|שיפון|כוסמין|שיבולת שועל|תירס|אורז|שעורה|oat|wheat|corn|rice|grain", txt, re.I))
        if is_grain:
            first_grain_pos = item.get("position")
            first_grain_whole = bool(WHOLE_GRAIN_RE.search(txt)) and not REFINED_FLOUR_RE.search(txt)
            break

    whole_present = bool(WHOLE_GRAIN_RE.search(ingr_text))
    refined_present = bool(REFINED_FLOUR_RE.search(ingr_text))

    # Composition (>=30%): whole grain present AND not dominated by a refined flour ahead of it
    composition_supported = whole_present and (first_grain_whole is True or not refined_present)
    # Dominant (>=51%): whole grain is the first grain ingredient
    dominant_supported = first_grain_whole is True

    # Marketing Divergence Finding: claim present but composition not supported (all 3 conditions)
    mdf = claim_present and not composition_supported

    return {
        "whole_grain_claim_present": claim_present,
        "first_grain_ingredient_position": first_grain_pos,
        "first_grain_is_whole": first_grain_whole,
        "composition_threshold_supported_30pct": composition_supported,
        "dominant_threshold_supported_51pct": dominant_supported,
        "marketing_divergence_finding": mdf,
        "mdf_note": ("Whole-grain claim present but ingredient ordering does not support the "
                     ">=30% composition threshold (refined flour leads or no whole grain found)."
                     if mdf else None),
        "evidence_ref": "cereals_gap_resolution_v1 Sec 5.2.1 (Resolution 4); Guardrails v2",
    }


def _granola_construct(name, ingr_text, subtype, nn) -> dict:
    """Construct 1 — Architectural Divergence Sub-Category Rule (Rule 5 / Sec 2.9)."""
    sugar = nn.get("sugars_g")
    fat = nn.get("fat_g")
    ind_sugar = sugar is not None and sugar >= 15.0        # proxy for added sugar >=10 (Resolution 3 mitigation)
    ind_fat = fat is not None and fat >= 10.0
    ind_processing = bool(re.search(r"גרנולה|granola|מוזלי|muesli", name + " " + ingr_text, re.I)) \
        or (bool(OIL_RE.search(ingr_text)) and bool(SYRUP_RE.search(ingr_text)))
    score = sum([ind_sugar, ind_fat, ind_processing])
    name_granola = bool(re.search(r"גרנולה|granola", name, re.I))
    # 2-of-3 → granola sub-pool; boundary (name granola + any 1) defaults to granola (conservative)
    in_granola_pool = score >= 2 or (name_granola and score >= 1)
    return {
        "subpool": "granola" if in_granola_pool else "standard_cereal",
        "indicators": {
            "added_sugar_proxy_ge15g": ind_sugar,
            "fat_ge10g": ind_fat,
            "processing_proxy_nova3plus": ind_processing,
        },
        "indicator_count": score,
        "boundary_defaulted_to_granola": in_granola_pool and score < 2,
        "nova_confirmation_pending_bsip2": True,
        "evidence_ref": "cereals_gap_resolution_v1 Sec 2.9 (Resolution 3, Constitution Art. II Rule 5)",
    }


def _childrens_construct(name, ingr_text, serving_g) -> dict:
    """Construct 2 — Developmental Product Definition (Sec 2.8 / Resolution 1)."""
    text = name + " " + ingr_text
    mascot_brand = bool(CHILD_MASCOT_RE.search(name))
    # D1 visual mascot: not directly observable from text, EXCEPT recognized child-mascot brands
    # whose brand identity encodes the mascot (documented, auditable list).
    d1_visual = True if mascot_brand else None
    d2_name = bool(KIDS_NAME_RE.search(name)) or mascot_brand
    d3_serving = serving_g is not None and serving_g <= 25.0
    d4_claim = bool(KIDS_CLAIM_RE.search(text))
    present = sum([d1_visual is True, bool(d2_name), bool(d3_serving), bool(d4_claim)])
    is_childrens = present >= 2
    # single-indicator candidate: one signal only (e.g. generic 'kids' word, no mascot) — CE Controller resolves
    single_indicator_candidate = (present == 1)
    return {
        "is_childrens_product": is_childrens,
        "indicators": {
            "D1_visual_mascot": d1_visual,           # True only for recognized mascot brands; else null
            "D2_name_language": d2_name,
            "D3_pediatric_serving_le25g": d3_serving,
            "D4_developmental_claim": d4_claim,
        },
        "indicators_present_count": present,
        "mascot_brand_detected": mascot_brand,
        "single_indicator_candidate": single_indicator_candidate,
        "pool": "developmental" if is_childrens else "general",
        "recall_caveat": "Pure visual mascots on non-listed brands are not detectable from a text-only "
                         "scrape; D3 serving size was rarely on the page. Recall is conservative — "
                         "single-indicator candidates are flagged for CE Controller visual confirmation.",
        "anti_immunity": "Classification cannot improve score (Anti-Immunity Rule).",
        "evidence_ref": "cereals_gap_resolution_v1 Sec 2.8 (Resolution 1)",
    }


def _fortification_flag(claims, ingr_text) -> bool:
    """Construct 4 (per-product half) — DISTORTION-004 fortification presence."""
    return bool(FORTIFY_RE.search(f"{claims} {ingr_text}"))


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("cereals_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No cereals_bsip0_raw_*.json in %s", RAW_DIR)
        return
    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

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
        claims_raw_in = raw.get("claims_raw", "")
        # Shufersal claims_raw is polluted with nav-menu boilerplate; blank it when detected.
        claims = "" if NAV_BOILERPLATE_RE.search(claims_raw_in) else claims_raw_in
        serving_g = raw.get("serving_size_g_hint")
        conf = _confidence(nn, ingr_list)
        subtype = _classify_subtype(name, ingr_text)
        pid = f"bsip1_cereal_{barcode}"

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
            "serving_size_g": serving_g,
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
                "populated_at": "bsip1_build_cereals_002",
                "missing": not bool(ingr_text),
                "note": "Scraped from Shufersal product page (run_cereals_002)",
            },
            "allergens_contains": [],
            "allergens_may_contain": [],
            "claims_raw": claims,
            "claims": [],
            "confidence": conf["confidence"],
            "barcode_validation_status": "retailer_confirmed",
            "barcode_confidence_reason": "Shufersal JSON-LD gtin13/sku.",
            "nutrition_basis_claimed": "ל-100 גרם",
            "nutrition_basis_detected": "per_100g",
            "nutrition_consistency_status": conf["nutrition_consistency_status"],
            "data_sufficiency": conf["data_sufficiency"],
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
            "inferred_fields": ["bsip_cereal_subtype"],
            "audit_ref": None,
            "bsip_cereal_subtype": subtype,
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

        ingredient_order = record.get("ingredient_order", [])

        # ── Apply the four governance constructs ──────────────────────────────
        wg = _whole_grain_construct(name, claims, ingr_text, ingredient_order)
        gr = _granola_construct(name, ingr_text, subtype, nn)
        ch = _childrens_construct(name, ingr_text, serving_g)
        fortified = _fortification_flag(ingr_text, ingr_text)
        record["cereals_governance"] = {
            "construct_1_granola_subpool": gr,
            "construct_2_childrens": ch,
            "construct_3_whole_grain": wg,
            "construct_4_fortification_flag": {
                "fortified": fortified,
                "evidence_ref": "cereals_gap_resolution_v1 Sec 6.4 (Resolution 2, DISTORTION-004)",
            },
        }

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({
            "barcode": barcode, "name": name, "subtype": subtype,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "data_sufficiency": conf["data_sufficiency"],
            "subpool": gr["subpool"],
            "is_childrens": ch["is_childrens_product"],
            "childrens_candidate": ch["single_indicator_candidate"],
            "wg_claim": wg["whole_grain_claim_present"],
            "wg_mdf": wg["marketing_divergence_finding"],
            "fortified": fortified,
        })

    # ── Curation report ──────────────────────────────────────────────────────
    n_ingr = sum(1 for i in included if i["has_ingredients"])
    n_suff = sum(1 for i in included if i["data_sufficiency"] == "sufficient")
    report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_file": str(raw_path),
        "raw_count": len(raws),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "ingredient_coverage": f"{n_ingr}/{len(included)}",
        "data_sufficient": f"{n_suff}/{len(included)}",
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── Constructs category-level rollup ───────────────────────────────────────
    displayable = [i for i in included if i["data_sufficiency"] == "sufficient"]
    n_disp = max(len(displayable), 1)
    granola_pool = [i for i in displayable if i["subpool"] == "granola"]
    childrens_pool = [i for i in displayable if i["is_childrens"]]
    childrens_candidates = [i for i in displayable if i.get("childrens_candidate")]
    mdf_list = [i for i in displayable if i["wg_mdf"]]
    wg_claims = [i for i in displayable if i["wg_claim"]]
    fortified = [i for i in displayable if i["fortified"]]
    fort_pct = 100.0 * len(fortified) / n_disp

    if fort_pct >= 80:
        lang = "most products in this category"
    elif fort_pct >= 66:
        lang = "the majority of products"
    elif fort_pct >= 50:
        lang = "approximately half of products"
    else:
        lang = None  # not endemic

    endemic_note = None
    if lang:
        endemic_note = (
            "CATEGORY NOTE — Fortification\n\n"
            "מוצרי דגני בוקר מועשרים לעיתים קרובות בוויטמינים ובמינרלים (ברזל, ויטמיני B, סידן, ויטמין D). "
            "הציון של Bari אינו כולל את תרומת המיקרו-נוטריאנטים כגורם חיובי.\n\n"
            f"מגבלה זו חלה על {('כמחצית המוצרים' if fort_pct < 66 else ('רוב המוצרים' if fort_pct < 80 else 'מרבית המוצרים בקטגוריה'))} בקטגוריה. "
            "הציון משקף ארכיטקטורת מאקרו-נוטריאנטים, איכות עיבוד ושלמות רכיבים. "
            "הציון אינו לוכד את הערך התזונתי של ויטמינים ומינרלים מוספים. "
            "מוצר מועשר עשוי לספק תועלת מיקרו-נוטריאנטית משמעותית שאינה נראית בציון."
        )

    constructs_report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "displayable_count": len(displayable),
        "construct_1_granola_subpool": {
            "granola_pool_count": len(granola_pool),
            "standard_pool_count": len(displayable) - len(granola_pool),
            "granola_members": [{"barcode": i["barcode"], "name": i["name"]} for i in granola_pool],
            "rule": "Art. II Rule 5 proxy 2-of-3 (added-sugar>=15g proxy / fat>=10g / processing); NOVA confirmed at BSIP2.",
        },
        "construct_2_childrens": {
            "developmental_pool_count": len(childrens_pool),
            "members": [{"barcode": i["barcode"], "name": i["name"]} for i in childrens_pool],
            "single_indicator_candidates_for_ce_review": [
                {"barcode": i["barcode"], "name": i["name"]} for i in childrens_candidates],
            "rule": "Sec 2.8 — 2-of-4 indicators. Recognized child-mascot brands satisfy D1+D2 jointly; "
                    "single-indicator products flagged for CE Controller visual confirmation.",
        },
        "construct_3_whole_grain": {
            "products_with_whole_grain_claim": len(wg_claims),
            "marketing_divergence_findings": len(mdf_list),
            "mdf_members": [{"barcode": i["barcode"], "name": i["name"]} for i in mdf_list],
            "rule": "Sec 5.2.1 — first-grain-ingredient test; MDF when claim present but composition <30% unsupported.",
        },
        "construct_4_fortification_endemic": {
            "fortified_count": len(fortified),
            "fortified_pct": round(fort_pct, 1),
            "endemic_threshold_pct": 50,
            "is_endemic": lang is not None,
            "graduated_language": lang,
            "category_note_he": endemic_note,
            "rule": "Sec 6.4 — category-level note required when DISTORTION-004 affects >=50% of displayable products.",
        },
    }
    (OUT_DIR.parent / "cereals_constructs_report.json").write_text(
        json.dumps(constructs_report, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("Included %d  Excluded %d  -> BSIP1 at %s", len(included), len(excluded), OUT_DIR)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included))
    log.info("Data sufficient: %d/%d", n_suff, len(included))
    log.info("Granola pool: %d | Children's: %d | WG claims: %d | MDF: %d | Fortified: %d/%d (%.1f%%, endemic=%s)",
             len(granola_pool), len(childrens_pool), len(wg_claims), len(mdf_list),
             len(fortified), len(displayable), fort_pct, lang is not None)
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)


if __name__ == "__main__":
    main()
