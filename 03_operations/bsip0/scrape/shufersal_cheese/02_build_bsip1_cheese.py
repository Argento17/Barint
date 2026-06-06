"""
BSIP1 Builder — Cottage / White Cheese (run_cheese_001) from Shufersal BSIP0 raw.

Reads:  C:\\Bari\\02_products\\cheese_spreads\\bsip0_outputs\\cheese_bsip0_raw_*.json (latest)
Writes: C:\\Bari\\03_operations\\bsip1\\run_cheese_001\\output\\bsip1_*.json
        + curation_report.json
        + cheese_constructs_report.json  (category-level rollup of the governance constructs)

Schema: bsip1_v0_1 — mirrors run_cereals_002 / run_yogurt_003 BSIP1 files.
Enrichment: core ingredient_enricher.py (additives / matrix markers / sweeteners / FERMENTATION_TERMS
  incl. the TASK-139B Israeli culture vocabulary).

APPLIES THE CHEESE GOVERNANCE CONSTRUCTS (cheese_spreads_stress_test_001.md, TASK-141 verdict B),
as label-observable CLASSIFICATION / DISCLOSURE layers — NOT score changes:
  C1 Sub-pool assignment    (Constitution Sec 2.9 dairy divergence axis + four-pool standing precedent:
                             Cottage / White-cheese-quark / Labaneh / Cream-cheese-spread; fat tiers = variants)
  C2 Developmental pool     (Constitution Sec 2.8; cheese D3 <=20g portion)
  C3 Light / reduced-fat    (Guardrails v2 Sec 5.2.1: >=25% fat reduction vs same-sub-pool standard reference;
                             relative-only; Marketing Divergence Finding when claim unsupported)
  C4 Fermentation credit    (EV-015 + TASK-139B FERMENTATION_TERMS, with EV-015 flavor-vs-marker guard)
  C5 A-ceiling inputs        (EV-021 / RULING-DAIRY-A-01 C1-C6; light cream cheese w/ stabilizers fails C2)
  C6 Endemic distortion flag (Sec 6.4: category-wide sodium/sat-fat DISTORTION-010; pool-specific light
                             reformulation DISTORTION-006/009)
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

RAW_DIR = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\bsip0_outputs")
OUT_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_001\output")
RUN_ID = "run_cheese_001"
SOURCE = "shufersal"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Curation signals (final pass — defends against scrape leakage) ──────────────
# Yellow/hard/processed-slice/brined cheese, yogurt/kefir, sweetened dessert, infant.
YELLOW_HARD_RE = re.compile(r"צהוב|קשקבל|גאודה|מוצרלה|mozzarella|פרמזן|parmesan|cheddar|צ'דר|אמנטל|"
                            r"משולש|פרוסות|מותכת|מעובדת|processed|חריצים|קממבר|camembert|ברי\b|brie|"
                            r"גרוויר|gruyere|גראנה|grana|פקורינו|pecorino|רוקפור|roquefort", re.I)
BRINED_RE      = re.compile(r"בולגרית|פטה|feta|צפתית|מלוחה|במלח|brined|חלומי|halloumi", re.I)
YOGURT_RE      = re.compile(r"יוגורט|yog[hu]?urt|קפיר|kefir|משקה|\bdrink\b|שתיה|שתייה", re.I)
DESSERT_RE     = re.compile(r"מילקי|פודינג|\bמוס\b|גלידה|ice ?cream|קרמברלה|דניאלה|מילקה|"
                            r"במילוי פיר|במילוי שוקולד|שוקולד למריחה|עוגת|עוגה|פס נפוליאון|מאפה", re.I)
# Cooking cheeses / cream — explicitly out of scope per Stress Test Sec 2.2 (ingredient role, not table spread)
COOKING_RE     = re.compile(r"ריקוטה|ricotta|מסקרפונה|mascarpone|שמנת לבישול|שמנת מתוקה|"
                            r"שמנת חמוצה|sour cream|שמנת להקצפה|cooking cream", re.I)
INFANT_RE      = re.compile(r"תינוק|מטרנה|סימילק|0-?3|לתינוקות", re.I)
# Plant-based (non-dairy) spreads — out of scope for dairy cheese-spreads v1 (future plant-cheese pool, not here)
PLANT_RE       = re.compile(r"טופו|tofu|סויה|soy|שקדים|almond|קוקוס|coconut|צמחי|טבעוני|vegan|"
                            r"ע\"ב קוקוס|על בסיס קוקוס|ממרח שקד", re.I)
# Butter / butter-spread (not cheese) — exclude when the product is butter, not a cheese
BUTTER_RE      = re.compile(r"ממרח חמאה|ממרח בטעם חמאה|\bחמאה\b", re.I)
# Prepared meals / sauces that carry a cheese token but are not a table cheese
PREPARED_RE    = re.compile(r"ארוחת|פסטה|מקרוני|רוטב|פיצה|לזניה|בורקס", re.I)
# Non-cheese white items that leak via the adjective 'לבנה' (white) — beans, fish roe, etc.
NONCHEESE_WHITE_RE = re.compile(r"שעועית|איקרה|עדשים|אורז|דג\b|דגים", re.I)
INFANT_RE      = re.compile(r"תינוק|מטרנה|סימילק|0-?3|לתינוקות", re.I)
# Must look like a fresh white cheese / spread to be admitted (bare 'ממרח' removed — too greedy)
CHEESE_RE      = re.compile(r"קוטג'|קוטג|cottage|גבינה לבנה|גבינת לבנה|לאבנה|\bלבנה\b|labaneh|labneh|"
                            r"קוורק|quark|טבורוג|tvorog|גבינת שמנת|ממרח גבינה|cream ?cheese|פילדלפיה|philadelphia|"
                            r"נפוליאון|napoleon|גבינה רכה|גבינת מטבח|גבינה 3%|גבינה 5%|גבינה 9%|"
                            r"גבינת עזים|גבינה", re.I)

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
    out = []
    for p in _SPLIT_RE.split(raw):
        p = p.strip().strip(".")
        if p and len(p) > 1:
            out.append(p)
    return out


def _curate(raw: dict) -> str | None:
    name = (raw.get("name_he") or "").strip()
    if not name:
        return "empty_name"
    if YELLOW_HARD_RE.search(name):
        return "yellow_hard_processed_excluded"
    if BRINED_RE.search(name):
        return "brined_cheese_excluded"
    if YOGURT_RE.search(name):
        return "yogurt_kefir_excluded_overlap"
    if DESSERT_RE.search(name):
        return "sweetened_dessert_or_cake_routes_maadanim"
    if COOKING_RE.search(name):
        return "cooking_cheese_out_of_scope"
    if PLANT_RE.search(name):
        return "plant_based_non_dairy_out_of_scope"
    if PREPARED_RE.search(name):
        return "prepared_meal_or_sauce_excluded"
    if NONCHEESE_WHITE_RE.search(name):
        return "non_cheese_white_item_excluded"
    if INFANT_RE.search(name):
        return "infant_excluded"
    # Butter / butter-spread is not cheese — exclude unless a real cheese token is also present
    if BUTTER_RE.search(name) and not re.search(r"גבינ", name):
        return "butter_not_cheese_excluded"
    if not CHEESE_RE.search(name):
        return "not_fresh_cheese"
    nn = _parse_nutrition(raw.get("nutrition", {}))
    if all(nn.get(k) is None for k in ("energy_kcal", "protein_g", "fat_g")):
        return "no_usable_nutrition"
    return None


def _confidence(nn: dict, ingr_list: list[str]) -> dict:
    nutr_fields = ["energy_kcal", "protein_g", "fat_g", "carbohydrates_g", "fat_saturated_g"]
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
# CHEESE GOVERNANCE CONSTRUCTS
# ══════════════════════════════════════════════════════════════════════════════

# White cheese = the compound 'גבינה לבנה' / 'גבינת לבנה' (literally "white cheese").
WHITE_RE     = re.compile(r"גבינה לבנה|גבינת לבנה|white ?cheese|גבינה 3%|גבינה 5%|"
                          r"גבינה 9%|גבינת מטבח|קוורק|quark|טבורוג|tvorog", re.I)
# Labaneh = standalone 'לבנה'/'לאבנה' (NOT preceded by גבינה) or labaneh/labneh.
LABANEH_RE   = re.compile(r"לאבנה|labaneh|labneh|\bלבנה\b", re.I)
COTTAGE_RE   = re.compile(r"קוטג'|קוטג|cottage", re.I)
CREAM_RE     = re.compile(r"גבינת שמנת|שמנת\b|ממרח גבינה|cream ?cheese|פילדלפיה|philadelphia|"
                          r"נפוליאון|napoleon|גבינה רכה", re.I)
QUARK_RE     = re.compile(r"קוורק|quark|טבורוג|tvorog", re.I)

# A 'light' CLAIM is explicit reduced-fat wording. A bare fat-% tier (5% / 3% / 9%) is the
# pool's DEFAULT VARIANT LABEL, not a light claim (Stress Test Sec 4.3: "5% white cheese is the
# default, not light vs itself") — so fat-% alone must NOT count as a light claim.
LIGHT_RE     = re.compile(r"דל שומן|מופחת שומן|מופחתת שומן|דל-שומן|\blight\b|לайт|לייט|"
                          r"חצי שומן|חצאי שומן|\b0%|מינוס|דל[ -]?קלוריות|reduced fat|low fat", re.I)
FAT_PCT_RE   = re.compile(r"(\d{1,2})\s*%")
KIDS_NAME_RE = re.compile(r"ילדים|kids|junior|ג'וניור|מיני\b|mini\b|קטנטנים", re.I)
CHILD_MASCOT_RE = re.compile(r"מילקי|milky|פרה שמ|בלה|cow ?bell|ספיידרמן|spider|דיסני|disney|"
                             r"קוקומון|cocomelon|במבה גבינה", re.I)
KIDS_CLAIM_RE = re.compile(r"לגדול|בית ?ספר|מתאים לילדים|growing", re.I)
NAV_BOILERPLATE_RE = re.compile(r"קטגוריה|לתפריט הראשי|טוען מוצרים")
# Culture/probiotic CLAIM in name/marketing (for the EV-015 flavor-vs-marker guard)
CULTURE_CLAIM_RE = re.compile(r"תרבית|פרוביוטי|חיידק|probiotic|culture|ביו\b|bio\b", re.I)
# Engineered additives that disqualify the A-ceiling C2 (stabilizers/gums/starch/maltodextrin)
ENGINEERED_ADDITIVE_CATS = {
    "stabilizer", "emulsifier", "thickener", "gum", "modified_starch", "starch",
    "maltodextrin", "carrageenan", "preservative", "color", "colour", "acidity_regulator",
}
ENGINEERED_ADDITIVE_RE = re.compile(r"מייצב|מתחלב|חומר ג'ל|גואר|guar|חרוב|locust|קרגינ|carrageenan|"
                                    r"קסנתן|xanthan|עמילן מעובד|modified starch|מלטודקסטרין|maltodextrin|"
                                    r"חנקתי|חומר משמר|preservativ|צבע מאכל", re.I)
ADDED_SUGAR_RE = re.compile(r"סוכר\b|גלוקוז|פרוקטוז|סירופ|syrup|דבש|honey|דקסטרוז|מולסה|"
                            r"סוכר חום|סוכר לבן", re.I)


def _classify_subpool(name: str, ingr_text: str, nn: dict) -> tuple[str, str]:
    """C1 — sub-pool assignment. Returns (pool_slug, basis). Order = most specific first."""
    # Classify on the NAME (ingredient text can mention 'שמנת'/'תרבית' as components and mislead).
    t = name
    if COTTAGE_RE.search(t):
        return "cottage", "name token קוטג'/cottage (Sec 2.9 curd-set, protein-forward pool)"
    if WHITE_RE.search(t):
        # 'גבינה לבנה' (white cheese) must win over the standalone-'לבנה' labaneh test.
        return "white_cheese_quark", "name token גבינה לבנה / קוורק / fat-tier % (parent fresh-cheese baseline)"
    if LABANEH_RE.search(t):
        return "labaneh", "name token לבנה/לאבנה/labaneh, standalone (Sec 2.9 strained + live-culture pool)"
    if CREAM_RE.search(t):
        return "cream_cheese_spread", "name token שמנת/ממרח גבינה/cream cheese (Sec 2.9 proxies: high fat + NOVA 3-4)"
    if QUARK_RE.search(t):
        return "white_cheese_quark", "name token קוורק/quark (white-cheese pool, high-protein variant)"
    # Fat-based fallback for bare 'גבינה'/'ממרח' names
    fat = nn.get("fat_g")
    if fat is not None and fat >= 18.0:
        return "cream_cheese_spread", f"fat fallback (fat {fat}g >= 18 → indulgent-spread architecture)"
    return "white_cheese_quark", "default fresh-cheese baseline (no specific pool token)"


def _developmental_construct(name: str, ingr_text: str, serving_g, subpool: str) -> dict:
    """C2 — Developmental Product Definition (Sec 2.8; cheese D3 <=20g per Stress Test Sec 2.3)."""
    text = name + " " + ingr_text
    mascot_brand = bool(CHILD_MASCOT_RE.search(name))
    d1_visual = True if mascot_brand else None
    d2_name = bool(KIDS_NAME_RE.search(name)) or mascot_brand
    d3_serving = serving_g is not None and serving_g <= 20.0
    d4_claim = bool(KIDS_CLAIM_RE.search(text))
    present = sum([d1_visual is True, bool(d2_name), bool(d3_serving), bool(d4_claim)])
    is_dev = present >= 2
    return {
        "is_developmental_product": is_dev,
        "indicators": {
            "D1_visual_mascot": d1_visual,
            "D2_name_language": d2_name,
            "D3_pediatric_serving_le20g": d3_serving,
            "D4_developmental_claim": d4_claim,
        },
        "indicators_present_count": present,
        "mascot_brand_detected": mascot_brand,
        "single_indicator_candidate": present == 1,
        "pool": "developmental" if is_dev else subpool,
        "recall_caveat": "Visual mascots / pediatric serving sizes are weakly observable from a text-only "
                         "scrape; recall is conservative. Single-indicator candidates flagged for CE review.",
        "anti_immunity": "Classification cannot improve score (Anti-Immunity Rule).",
        "evidence_ref": "cheese_spreads_stress_test_001 Sec 2.3 / Constitution Sec 2.8 (cheese D3 <=20g)",
    }


def _light_construct(name, claims, nn, pool_reference_fat) -> dict:
    """C3 — Light / reduced-fat (Guardrails Sec 5.2.1): >=25% fat reduction vs same-sub-pool standard ref.
    Relative-only (absolute cutoff deliberately not used). MDF when claim present but reduction <25%."""
    claim_text = f"{name} {claims}"
    light_claim = bool(LIGHT_RE.search(claim_text))
    fat = nn.get("fat_g")
    reduction_pct = None
    supported = None
    if fat is not None and pool_reference_fat and pool_reference_fat > 0:
        reduction_pct = round(100.0 * (pool_reference_fat - fat) / pool_reference_fat, 1)
        supported = reduction_pct >= 25.0
    # Marketing Divergence Finding: claim present but >=25% relative reduction not supported
    mdf = bool(light_claim and supported is False)
    return {
        "light_claim_present": light_claim,
        "declared_fat_g": fat,
        "pool_standard_reference_fat_g": pool_reference_fat,
        "relative_fat_reduction_pct": reduction_pct,
        "reduced_fat_threshold_met_ge25pct": supported,
        "marketing_divergence_finding": mdf,
        "mdf_note": ("'Light/reduced-fat' claim present but declared fat is <25% below the sub-pool's "
                     "standard-fat reference — the claim does not meet the ratified Sec 5.2.1 threshold."
                     if mdf else None),
        "evidence_ref": "cheese_spreads_stress_test_001 Sec 4 / Guardrails v2 Sec 5.2.1 (relative >=25%, same sub-pool)",
    }


def _fermentation_construct(name, claims, record) -> dict:
    """C4 — Fermentation credit (EV-015 + TASK-139B FERMENTATION_TERMS) with EV-015 flavor-vs-marker guard.
    Credit ONLY ingredient-grounded cultures (enricher reads ingredient text). If a culture/probiotic CLAIM
    appears in the name/marketing but no ingredient marker exists → flavor-vs-marker violation → do NOT credit."""
    markers = record.get("extracted_fermentation_markers", []) or []
    summary = record.get("enrichment_summary", {}) or {}
    has_ingredient_culture = bool(summary.get("has_live_cultures")) or any(
        m.get("category") in ("live_cultures", "live_bacteria", "lactobacillus", "bifidobacterium",
                              "st_thermophilus", "streptococcus", "lactococcus", "lb_bulgaricus",
                              "lb_acidophilus", "starter_cultures", "cultures_generic", "lactic_fermentation")
        for m in markers
    )
    culture_claim = bool(CULTURE_CLAIM_RE.search(f"{name} {claims}"))
    flavor_vs_marker_violation = culture_claim and not has_ingredient_culture
    credited = has_ingredient_culture and not flavor_vs_marker_violation
    return {
        "live_culture_ingredient_marker": has_ingredient_culture,
        "culture_marker_categories": sorted({m.get("category") for m in markers if m.get("category")}),
        "culture_claim_in_name_or_marketing": culture_claim,
        "ev015_flavor_vs_marker_violation": flavor_vs_marker_violation,
        "fermentation_credit_applied": credited,
        "evidence_ref": "EV-015 (fermentation bonus + flavor-vs-marker guard); TASK-139B FERMENTATION_TERMS (EV-022)",
    }


def _a_ceiling_construct(nn, record, ferment, subpool) -> dict:
    """C5 — A-ceiling C1-C6 inputs (EV-021 / RULING-DAIRY-A-01). All must hold for A-eligibility.
    C5 (correct dairy routing) is confirmed at BSIP2; C1-C4,C6 are label-observable here."""
    ingr_text = record.get("ingredients_text_he", "") or ""
    additives = record.get("extracted_additives", []) or []
    sweeteners = record.get("extracted_sweeteners", []) or []
    sugars = nn.get("sugars_g")
    # C1 — no added sugar (intrinsic lactose ~3-5g tolerated; added sugar pushes higher / sweetener markers)
    has_sweetener = len(sweeteners) > 0 or bool(ADDED_SUGAR_RE.search(ingr_text))
    c1_no_added_sugar = not has_sweetener and (sugars is None or sugars <= 6.0)
    # C2 — no engineered additives (stabilizers/gums/starch/maltodextrin/preservatives/colors)
    has_engineered = any(a.get("category") in ENGINEERED_ADDITIVE_CATS for a in additives) \
        or bool(ENGINEERED_ADDITIVE_RE.search(ingr_text))
    c2_no_engineered_additives = not has_engineered
    # C3 — live culture confirmed AND credited
    c3_culture_credited = ferment["fermentation_credit_applied"]
    # C4 — intact dairy matrix (proxy: no engineered additives AND not a processed spread profile)
    c4_intact_matrix = c2_no_engineered_additives
    # C6 — verified confidence
    c6_verified = record.get("data_sufficiency") == "sufficient" and record.get("canonical_trust_level") == "high"
    a_eligible_pre_routing = all([c1_no_added_sugar, c2_no_engineered_additives,
                                  c3_culture_credited, c4_intact_matrix, c6_verified])
    return {
        "C1_no_added_sugar": c1_no_added_sugar,
        "C2_no_engineered_additives": c2_no_engineered_additives,
        "C3_live_culture_confirmed_and_credited": c3_culture_credited,
        "C4_intact_dairy_matrix": c4_intact_matrix,
        "C5_correct_dairy_routing": "pending_bsip2",
        "C6_verified_confidence": c6_verified,
        "a_eligible_pre_routing": a_eligible_pre_routing,
        "fails": [c for c, ok in [
            ("C1_added_sugar", c1_no_added_sugar), ("C2_engineered_additives", c2_no_engineered_additives),
            ("C3_no_culture_credit", c3_culture_credited), ("C4_non_intact_matrix", c4_intact_matrix),
            ("C6_unverified", c6_verified)] if not ok],
        "evidence_ref": "EV-021 / RULING-DAIRY-A-01 (TASK-139A); A>=80 (TASK-139D/EV-023). "
                        "Light cream cheese with stabilizers fails C2 → not A-eligible regardless of macros.",
    }


def _find_latest_raw() -> pathlib.Path | None:
    cand = sorted(RAW_DIR.glob("cheese_bsip0_raw_*.json"),
                  key=lambda p: p.stat().st_mtime, reverse=True)
    return cand[0] if cand else None


def main():
    raw_path = _find_latest_raw()
    if not raw_path:
        log.error("No cheese_bsip0_raw_*.json in %s", RAW_DIR)
        return
    log.info("Loading %s", raw_path)
    raws = json.loads(raw_path.read_text(encoding="utf-8"))
    log.info("Loaded %d raw products", len(raws))

    for f in OUT_DIR.glob("bsip1_*.json"):
        f.unlink()

    # ── Pass 1: curate + parse + enrich + sub-pool (collect pool fat references) ──
    staged, excluded = [], []
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
        claims = "" if NAV_BOILERPLATE_RE.search(claims_raw_in) else claims_raw_in
        serving_g = raw.get("serving_size_g_hint")
        subpool, subpool_basis = _classify_subpool(name, ingr_text, nn)
        staged.append({
            "raw": raw, "name": name, "barcode": barcode, "nn": nn,
            "ingr_text": ingr_text, "ingr_list": ingr_list, "claims": claims,
            "serving_g": serving_g, "subpool": subpool, "subpool_basis": subpool_basis,
        })

    # Pool standard-fat reference = the pool's full-fat/standard tier (max declared fat in pool).
    # Light is measured against this (Sec 4.3: 5% white cheese is the default, not light vs itself).
    pool_ref_fat: dict[str, float] = {}
    for s in staged:
        fat = s["nn"].get("fat_g")
        if fat is not None:
            pool_ref_fat[s["subpool"]] = max(pool_ref_fat.get(s["subpool"], 0.0), fat)

    # ── Pass 2: build records + constructs ──────────────────────────────────────
    included = []
    for s in staged:
        raw, name, barcode = s["raw"], s["name"], s["barcode"]
        nn, ingr_text, ingr_list = s["nn"], s["ingr_text"], s["ingr_list"]
        claims, serving_g, subpool = s["claims"], s["serving_g"], s["subpool"]
        conf = _confidence(nn, ingr_list)
        pid = f"bsip1_cheese_{barcode}"

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
                "populated_at": "bsip1_build_cheese_001",
                "missing": not bool(ingr_text),
                "note": "Scraped from Shufersal product page (run_cheese_001)",
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
            "inferred_fields": ["bsip_cheese_subpool"],
            "audit_ref": None,
            "bsip_cheese_subpool": subpool,
            "product_type_dairy": True,
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

        # ── Apply the cheese governance constructs ────────────────────────────
        dev = _developmental_construct(name, ingr_text, serving_g, subpool)
        lt = _light_construct(name, claims, nn, pool_ref_fat.get(subpool))
        fr = _fermentation_construct(name, claims, record)
        ac = _a_ceiling_construct(nn, record, fr, subpool)
        final_pool = "developmental" if dev["is_developmental_product"] else subpool
        record["bsip_cheese_subpool"] = final_pool
        record["cheese_governance"] = {
            "construct_1_subpool": {"subpool": final_pool, "structural_subpool": subpool,
                                    "basis": s["subpool_basis"],
                                    "evidence_ref": "Constitution Sec 2.9 dairy divergence axis + four-pool standing precedent"},
            "construct_2_developmental": dev,
            "construct_3_light": lt,
            "construct_4_fermentation": fr,
            "construct_5_a_ceiling": ac,
        }

        (OUT_DIR / f"bsip1_{barcode}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        included.append({
            "barcode": barcode, "name": name, "subpool": final_pool, "structural_subpool": subpool,
            "has_ingredients": bool(ingr_text),
            "nutrition_fields": sum(1 for v in nn.values() if v is not None),
            "data_sufficiency": conf["data_sufficiency"],
            "is_developmental": dev["is_developmental_product"],
            "dev_candidate": dev["single_indicator_candidate"],
            "light_claim": lt["light_claim_present"],
            "light_supported": lt["reduced_fat_threshold_met_ge25pct"],
            "light_mdf": lt["marketing_divergence_finding"],
            "culture_credited": fr["fermentation_credit_applied"],
            "ev015_violation": fr["ev015_flavor_vs_marker_violation"],
            "a_eligible_pre_routing": ac["a_eligible_pre_routing"],
            "fat_g": nn.get("fat_g"), "sodium_mg": nn.get("sodium_mg"),
            "sat_fat_g": nn.get("fat_saturated_g"),
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
        "pool_standard_reference_fat_g": pool_ref_fat,
        "included": included,
        "excluded": excluded,
    }
    (OUT_DIR.parent / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── Constructs category-level rollup ───────────────────────────────────────
    displayable = [i for i in included if i["data_sufficiency"] == "sufficient"]
    n_disp = max(len(displayable), 1)
    pools = {}
    for i in displayable:
        pools.setdefault(i["subpool"], []).append(i)
    dev_pool = [i for i in displayable if i["is_developmental"]]
    light_claims = [i for i in displayable if i["light_claim"]]
    light_mdf = [i for i in displayable if i["light_mdf"]]
    culture_credited = [i for i in displayable if i["culture_credited"]]
    ev015_violations = [i for i in displayable if i["ev015_violation"]]
    a_eligible = [i for i in displayable if i["a_eligible_pre_routing"]]
    cream_pool = pools.get("cream_cheese_spread", [])
    # Sodium endemic (DISTORTION-010): products with non-trivial sodium
    sodium_present = [i for i in displayable if (i.get("sodium_mg") or 0) > 0]
    sodium_pct = 100.0 * len(sodium_present) / n_disp

    # The two APPROVED Sec 6.4 disclosure texts (TASK-141 Resolution 3) — verbatim, Hebrew-faced page copy.
    category_sodium_note_he = (
        "הערת קטגוריה — נתרן ושומן רווי\n\n"
        "גבינות לבנות טריות מכילות נתרן ושומן רווי בכמות משמעותית. הציון של Bari אינו כולל כעת "
        "נתרן או שומן רווי כגורם שלילי.\n\n"
        "מגבלה זו חלה על מרבית המוצרים בקטגוריה. הציון משקף חלבון, שלמות רכיבים, רמת עיבוד ותסיסה. "
        "הציון אינו לוכד עומס נתרן או שיעור שומן רווי. גבינה בעלת ציון גבוה עשויה עדיין להיות עתירת מלח "
        "או שומן רווי — בדקו זאת בתווית."
    )
    pool_light_note_he = (
        "הערת קטגוריה — ניסוח מחדש דל-שומן (מוצרי לייט וממרחים)\n\n"
        "כדי להחליף שומן שהוסר, גבינות 'לייט' וממרחים מוסיפים לעיתים מייצבים, מסטיקים או עמילן, "
        "ולעיתים מעלים את כמות המלח. ייתכן שציון העיבוד של Bari ידרג מוצר 'לייט' מתחת לגרסה מלאת-השומן "
        "שלו, והעלייה במלח אינה מתבטאת בציון.\n\n"
        "מגבלה זו חלה על מוצרי הלייט והממרחים בקטגוריה. הכיתוב 'לייט' מציין שומן נמוך יותר — לא בהכרח "
        "מוצר נקי או בריא יותר באופן כללי."
    )

    constructs_report = {
        "run_id": RUN_ID,
        "generated": datetime.now(timezone.utc).isoformat(),
        "displayable_count": len(displayable),
        "construct_1_subpools": {
            "pool_counts": {k: len(v) for k, v in sorted(pools.items())},
            "pool_standard_reference_fat_g": pool_ref_fat,
            "members": {k: [{"barcode": i["barcode"], "name": i["name"], "fat_g": i["fat_g"]} for i in v]
                        for k, v in sorted(pools.items())},
            "rule": "Constitution Sec 2.9 dairy divergence axis + four-pool standing precedent "
                    "(Cottage / White-cheese-quark / Labaneh / Cream-cheese-spread). Fat tiers are variants, not pools.",
        },
        "construct_2_developmental": {
            "developmental_pool_count": len(dev_pool),
            "members": [{"barcode": i["barcode"], "name": i["name"]} for i in dev_pool],
            "single_indicator_candidates_for_ce_review": [
                {"barcode": i["barcode"], "name": i["name"]} for i in displayable if i["dev_candidate"]],
            "rule": "Sec 2.8 — 2-of-4 indicators; cheese D3 <=20g portion (Stress Test Sec 2.3).",
        },
        "construct_3_light": {
            "light_claims_count": len(light_claims),
            "light_supported_count": sum(1 for i in light_claims if i["light_supported"]),
            "marketing_divergence_findings": len(light_mdf),
            "mdf_members": [{"barcode": i["barcode"], "name": i["name"], "fat_g": i["fat_g"]} for i in light_mdf],
            "rule": "Sec 5.2.1 — relative >=25% fat reduction vs same-sub-pool standard reference; MDF when claim unsupported.",
        },
        "construct_4_fermentation": {
            "culture_credited_count": len(culture_credited),
            "ev015_flavor_vs_marker_violations": len(ev015_violations),
            "violation_members": [{"barcode": i["barcode"], "name": i["name"]} for i in ev015_violations],
            "credited_members": [{"barcode": i["barcode"], "name": i["name"]} for i in culture_credited],
            "rule": "EV-015 fermentation bonus + flavor-vs-marker guard; TASK-139B FERMENTATION_TERMS (EV-022). "
                    "Credit only ingredient-grounded cultures; claim-without-marker → no credit.",
        },
        "construct_5_a_ceiling": {
            "a_eligible_pre_routing_count": len(a_eligible),
            "members": [{"barcode": i["barcode"], "name": i["name"], "subpool": i["subpool"]} for i in a_eligible],
            "rule": "EV-021 / RULING-DAIRY-A-01 C1-C6; C5 (routing) confirmed at BSIP2. "
                    "Light cream cheese with stabilizers fails C2 → not A-eligible.",
        },
        "construct_6_endemic_distortion": {
            "category_wide_sodium_satfat": {
                "distortion_ref": "DISTORTION-010 (Macro Obsession)",
                "scope": "category-wide (all pools)",
                "sodium_present_pct": round(sodium_pct, 1),
                "is_endemic": sodium_pct >= 50.0,
                "category_note_he": category_sodium_note_he,
            },
            "pool_specific_light_reformulation": {
                "distortion_ref": "DISTORTION-006 (Low-Calorie Halo) / DISTORTION-009 (Additive Overreaction)",
                "scope": "cream-cheese + light products only (must NOT appear on plain cottage/labaneh cards)",
                "applies_to_pools": ["cream_cheese_spread"],
                "light_product_count": len(light_claims),
                "category_note_he": pool_light_note_he,
            },
            "rule": "Sec 6.4 — apply existing protocol + milk multi-pool clarification (no amendment). "
                    "Both disclosure texts APPROVED by Product Owner 2026-06-01 (TASK-141 Resolution 3).",
        },
    }
    (OUT_DIR.parent / "cheese_constructs_report.json").write_text(
        json.dumps(constructs_report, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("Included %d  Excluded %d  -> BSIP1 at %s", len(included), len(excluded), OUT_DIR)
    log.info("Ingredient coverage (included): %d/%d", n_ingr, len(included))
    log.info("Data sufficient: %d/%d", n_suff, len(included))
    log.info("Pools: %s", {k: len(v) for k, v in sorted(pools.items())})
    log.info("Developmental: %d | Light claims: %d (MDF %d) | Culture credited: %d (EV-015 violations %d) | A-eligible(pre-routing): %d",
             len(dev_pool), len(light_claims), len(light_mdf), len(culture_credited),
             len(ev015_violations), len(a_eligible))
    tally = {}
    for e in excluded:
        tally[e["reason"]] = tally.get(e["reason"], 0) + 1
    for r, c in sorted(tally.items(), key=lambda x: -x[1]):
        log.info("  excluded[%s] = %d", r, c)


if __name__ == "__main__":
    main()
