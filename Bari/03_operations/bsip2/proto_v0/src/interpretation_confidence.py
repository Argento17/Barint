"""
BSIP2 Interpretation Confidence Layer v1

Extends score_engine.compute_confidence() with a richer 5-band system,
router stability inputs, and calm analytical confidence narratives.

Philosophy: "When information quality drops, confidence should drop faster
than interpretive ambition."

Bands:
  very_high           (>=90)  Full data, stable routing, no gaps
  high                (>=75)  Minor gaps, routing stable, score reliable
  moderate            (>=55)  Some gaps or mild instability — usable with caveat
  low                 (>=35)  Significant gaps — score tentative; flag prominently
  insufficient_context (<35)  Too little to interpret reliably; grade withheld
"""

from __future__ import annotations

BAND_THRESHOLDS = {
    "very_high":          90,
    "high":               75,
    "moderate":           55,
    "low":                35,
    "insufficient_context": 0,
}

# Score ceiling per band — cap final_score_estimate to this value
# None = no ceiling applied by this layer
BAND_CEILINGS = {
    "very_high":          None,
    "high":               None,
    "moderate":           82,
    "low":                65,
    "insufficient_context": 40,
}

# Grade ceiling per band — grade cannot exceed this letter
BAND_GRADE_CEILINGS = {
    "very_high":          None,
    "high":               None,
    "moderate":           "B",
    "low":                "C",
    "insufficient_context": "D",
}


def _detect_supplement_candidate(product: dict) -> bool:
    """
    Detect protein powders and meal replacements that fall outside the current food ontology.
    Uses name signals and ingredient composition (whey + maltodextrin/sport context).
    """
    name = (product.get("canonical_name_he") or "").lower()
    ing_text = (product.get("ingredients_text_he") or "").lower()

    SUPPLEMENT_NAME_SIGNALS = [
        "אבקת חלבון", "שייק חלבון", "תחליף ארוחה", "חלבון ספורט", "אבקת מי גבינה",
    ]
    WHEY_TERMS = ["מי גבינה", "חלבון מי גבינה", "קזאין"]
    SPORT_NAME_KW = ["ספורט", "שייק", "אבקת", "פרוטאין"]

    for sig in SUPPLEMENT_NAME_SIGNALS:
        if sig in name:
            return True

    has_whey = any(w in ing_text for w in WHEY_TERMS)
    has_maltodextrin = "מלתודקסטרין" in ing_text
    has_sport_name = any(kw in name for kw in SPORT_NAME_KW)
    if has_whey and (has_maltodextrin or has_sport_name):
        return True

    return False


def compute_interpretation_confidence(
    base_confidence_result: dict,
    cat_result: dict,
    product: dict,
    signals: dict,
) -> dict:
    """
    Build the full interpretation_confidence record.

    Inputs:
      base_confidence_result  — output of score_engine.compute_confidence()
      cat_result              — output of router_v2.classify_category()
      product                 — raw product dict
      signals                 — extracted signal dict (L1-L6)
    """
    base_score = base_confidence_result.get("confidence_score", 0)
    base_band  = base_confidence_result.get("confidence_band", "insufficient")
    reductions = base_confidence_result.get("confidence_reductions", [])

    # Additional modifiers on top of base confidence score
    additional_reductions: list[dict] = []
    score = float(base_score)

    def deduct(amount: float, reason: str) -> None:
        nonlocal score
        score -= amount
        additional_reductions.append({"factor": reason, "reduction": -amount})

    # Router stability: instability flag cuts confidence
    if cat_result.get("category_instability_flag"):
        delta = cat_result.get("routing_instability_warning", "")
        deduct(12, f"router_instability: {delta}")

    # Routing uncertainty: low confidence band in routing
    cat_conf = cat_result.get("category_confidence", 1.0)
    if cat_conf < 0.50:
        deduct(10, f"category_confidence_very_low({cat_conf:.2f})")
    elif cat_conf < 0.65:
        deduct(5, f"category_confidence_low({cat_conf:.2f})")

    # Hybrid product: two competing interpretations reduce confidence
    if cat_result.get("is_hybrid"):
        deduct(8, "hybrid_routing: product straddles two categories")

    # Missing barcode or unreliable barcode
    barcode = product.get("barcode")
    barcode_status = product.get("barcode_validation_status", "")
    if not barcode:
        deduct(10, "missing_barcode")
    elif barcode_status in ("retailer_internal_id", "unvalidated"):
        deduct(5, f"barcode_reliability={barcode_status}")

    # Ingredient truncation signal
    ing_list = product.get("ingredients_list") or []
    ing_text = product.get("ingredients_text_he") or ""
    if len(ing_list) == 0 and len(ing_text) == 0:
        pass  # already penalized in base confidence for missing ingredients
    elif len(ing_list) > 0 and len(ing_text) == 0:
        deduct(14, "ingredient_text_absent: ingredient list present but text field empty")
    elif 1 <= len(ing_list) <= 2 and len(ing_text) > 20:
        deduct(8, "ingredient_truncation_suspected: list has 1-2 items but text is longer")

    # Trust level from BSIP1 (already in base, but reinforce low trust)
    trust = product.get("canonical_trust_level", "unknown")
    if trust == "low":
        pass  # already in base; no double-count
    elif trust == "unknown":
        deduct(8, "trust_level_unknown")

    # OCR quality
    ing_quality = product.get("ingredient_text_quality", "clean")
    if ing_quality == "corrupted":
        deduct(12, "ingredient_text_quality=corrupted")
    elif ing_quality == "malformed":
        deduct(8, "ingredient_text_quality=malformed")
    elif ing_quality == "partial":
        deduct(4, "ingredient_text_quality=partial")

    # Nutrition consistency
    consistency = product.get("nutrition_consistency_status", "consistent")
    if consistency == "suspicious":
        pass  # already in base
    elif consistency == "cross_retailer_conflict":
        deduct(12, "nutrition_consistency=cross_retailer_conflict")
    elif consistency == "unverified":
        deduct(6, "nutrition_consistency=unverified")

    # L1 consistency check failures
    l1 = signals.get("L1_observed_signals", {})
    checks = l1.get("consistency_checks", {})
    fail_count = sum(1 for v in checks.values() if v is False)
    if fail_count >= 2:
        pass  # already penalized in base
    elif fail_count == 1:
        pass  # already in base

    # Vague or empty product name — fundamental identity uncertainty
    # Exemption: short names that contain a strong product-identity keyword are
    # not genuinely ambiguous — "משקה שיבולת שועל" identifies a beverage unambiguously.
    # These words signal clear category identity even without a hard anchor firing.
    _IDENTITY_EXEMPT = {
        "משקה", "שתייה", "מיץ", "קפה", "תה", "לימונדה",  # beverages
        "חטיף", "חטיפי",                                    # snack bars
        "ממרח", "טחינה", "חומוס",                           # spreads
        "גבינה", "חלב",                                     # dairy (no hard anchor)
    }
    name_he = product.get("canonical_name_he") or ""
    name_words = [w for w in name_he.split() if len(w) > 1]
    name_has_identity_kw = any(kw in name_he for kw in _IDENTITY_EXEMPT)
    if len(name_words) == 0:
        deduct(20, "product_name_empty: no meaningful product name")
    elif len(name_words) <= 2:
        deduct(14, f"product_name_very_short: only {len(name_words)} word(s)")
    elif len(name_words) <= 4:
        if not cat_result.get("anchor_override") and not name_has_identity_kw:
            deduct(8, f"product_name_short_no_anchor: {len(name_words)} words, no anchor or identity keyword")

    # Anchor-secondary tension: anchor fired but secondary category has substantial signal
    # Only applies for semantically competing pairs — not closely-related sibling categories.
    # Pairs: hybrid-eligible category combinations where routing ambiguity is meaningful.
    _ANCHOR_TENSION_PAIRS: frozenset = frozenset({
        frozenset({"snack_bar_granola", "cereal"}),
        frozenset({"dairy_protein",     "beverage"}),
        frozenset({"dairy_protein",     "dessert"}),
        frozenset({"cereal",            "whole_food_fat"}),
        frozenset({"snack_bar_granola", "whole_food_fat"}),
        frozenset({"cracker",           "snack_bar_granola"}),
        frozenset({"cracker",           "cereal"}),       # sweet cracker vs oat cereal
        frozenset({"crispbread",        "cracker"}),
    })
    if cat_result.get("anchor_override"):
        primary_cat = cat_result.get("category", "")
        sec_cat_val = cat_result.get("secondary_category", "")
        sec_conf    = cat_result.get("secondary_confidence", 0.0)
        if frozenset({primary_cat, sec_cat_val}) in _ANCHOR_TENSION_PAIRS:
            if sec_conf >= 0.50:
                deduct(12, f"anchor_secondary_tension: anchor overrode strong sec_conf={sec_conf:.2f} ({sec_cat_val})")
            elif sec_conf >= 0.35:
                deduct(6, f"anchor_secondary_tension_mild: sec_conf={sec_conf:.2f} ({sec_cat_val})")

    # Extra kcal implausibility penalty (supplements + impossible macro combos)
    # Guard: only compute when all three macros are present — a missing macro makes
    # expected_min artificially low, causing false implausibility on Group B products.
    nn_check  = product.get("normalized_nutrition_per_100g") or {}
    kcal_check = nn_check.get("energy_kcal") or 0
    _fat_raw  = nn_check.get("fat_g")
    _carb_raw = nn_check.get("carbohydrates_g")
    _prot_raw = nn_check.get("protein_g")
    if (kcal_check > 0
            and _fat_raw is not None
            and _carb_raw is not None
            and _prot_raw is not None):
        fat_g  = float(_fat_raw)
        carb_g = float(_carb_raw)
        prot_g = float(_prot_raw)
        if (fat_g + carb_g + prot_g) > 0:
            expected_min = fat_g * 9 + (carb_g + prot_g) * 4
            if expected_min > 0 and (kcal_check > expected_min * 1.5 or kcal_check < expected_min * 0.4):
                deduct(10, f"kcal_implausible_extra: kcal={kcal_check:.0f} vs macros_implied={expected_min:.0f}")

    # Supplement candidate: protein powder / meal replacement outside current food ontology
    is_supplement = _detect_supplement_candidate(product)
    if is_supplement:
        deduct(22, "supplement_candidate: protein_supplement_candidate outside current food ontology")

    score = max(0.0, min(100.0, score))

    # Map to named band
    band = _score_to_band(score)
    ceiling = BAND_CEILINGS[band]
    grade_ceiling = BAND_GRADE_CEILINGS[band]

    # Generate narrative (calm, analytical)
    cautions = _collect_cautions(base_confidence_result, additional_reductions, product, cat_result)
    narrative = _build_narrative(band, score, cautions)

    return {
        "interpretation_confidence_score": round(score, 1),
        "interpretation_confidence_band":  band,
        "base_confidence_score":           round(base_score, 1),
        "base_confidence_band":            base_band,
        "additional_reductions":           additional_reductions,
        "all_reductions":                  reductions + additional_reductions,
        "score_ceiling":                   ceiling,
        "grade_ceiling":                   grade_ceiling,
        "interpretation_cautions":         cautions,
        "interpretation_narrative":        narrative,
        "is_supplement_candidate":         is_supplement,
    }


def _score_to_band(score: float) -> str:
    if score >= BAND_THRESHOLDS["very_high"]:
        return "very_high"
    if score >= BAND_THRESHOLDS["high"]:
        return "high"
    if score >= BAND_THRESHOLDS["moderate"]:
        return "moderate"
    if score >= BAND_THRESHOLDS["low"]:
        return "low"
    return "insufficient_context"


def _collect_cautions(
    base_conf: dict,
    additional: list[dict],
    product: dict,
    cat_result: dict,
) -> list[str]:
    cautions: list[str] = []

    # Collect from base reductions
    for r in base_conf.get("confidence_reductions", []):
        factor = r.get("factor", "")
        if "missing: ingredient_list" in factor:
            cautions.append("רשימת הרכיבים אינה זמינה — חלק מהאותות מבוססים על פרטי תזונה בלבד")
        elif "ingredient_quality=corrupted" in factor:
            cautions.append("טקסט הרכיבים נראה פגום — ייתכן שחלק מהאותות אינם מדויקים")
        elif "missing: energy_kcal" in factor:
            cautions.append("ערך הקלוריות חסר — ציון צפיפות הקלוריות הוחלף בנייטרל 50")
        elif "missing: dietary_fiber_g" in factor:
            cautions.append("ערך הסיבים התזונתיים חסר — מדדי סיבים עשויים להיות חסרי דיוק")
        elif "missing: protein_g" in factor:
            cautions.append("ערך החלבון חסר — ניתוח מקור חלבון אינו זמין")
        elif "bsip1_nutrition_consistency=suspicious" in factor:
            cautions.append("פרטי התזונה מעוררים חשד (ייתכן בלבול בין ל-100 גרם ל-מנה) — הציון זהיר יותר")
        elif "sugar > carbohydrates" in factor:
            cautions.append("שגיאת עקביות: סוכר רשום גבוה מפחמימות — ייתכן שגיאת נתונים")
        elif "sat_fat > fat" in factor:
            cautions.append("שגיאת עקביות: שומן רווי רשום גבוה מהשומן הכולל — ייתכן שגיאת נתונים")

    # From additional reductions
    for r in additional:
        factor = r.get("factor", "")
        if "router_instability" in factor:
            cautions.append("הניתוב הקטגורי אינו יציב — המוצר קרוב לגבול בין שתי קטגוריות")
        elif "hybrid_routing" in factor:
            cautions.append("המוצר משתרע על פני שתי קטגוריות — ציון מחושב לפי הקטגוריה הראשית")
        elif "missing_barcode" in factor:
            cautions.append("ברקוד חסר — זיהוי מבוסס על שם ומותג בלבד")
        elif "ingredient_truncation" in factor:
            cautions.append("רשימת הרכיבים עשויה לא להיות שלמה — ייתכן שחסרים רכיבים")
        elif "trust_level_unknown" in factor:
            cautions.append("רמת האמינות של מקור הנתונים אינה ידועה")
        elif "ingredient_text_quality=corrupted" in factor:
            cautions.append("הטקסט של הרכיבים פגום — ניתוח הרכיבים מוגבל")
        elif "nutrition_consistency=cross_retailer_conflict" in factor:
            cautions.append("פרטי תזונה מתנגשים בין קמעונאים שונים — נעשה שימוש בנתון הרווח ביותר")
        elif "category_confidence_very_low" in factor:
            cautions.append("הקטגוריה לא נקבעה בביטחון — ייתכן שמדובר בסוג מוצר שונה")
        elif "ingredient_text_absent" in factor:
            cautions.append("טקסט הרכיבים ריק למרות שרשימת הרכיבים קיימת — אותות רכיבים מוגבלים")
        elif "product_name_empty" in factor:
            cautions.append("שם המוצר חסר לחלוטין — זיהוי מתבסס על נתוני תזונה בלבד")
        elif "product_name_very_short" in factor or "product_name_short_no_anchor" in factor:
            cautions.append("שם המוצר קצר מדי לזיהוי חד-משמעי — ייתכן חוסר ודאות בקטגוריה")
        elif "anchor_secondary_tension" in factor:
            cautions.append("הסיווג הראשי נסמך על עוגן שם, אך קיים אות מתחרה משמעותי — ייתכן פרשנות חלופית")
        elif "kcal_implausible_extra" in factor:
            cautions.append("ערך הקלוריות אינו עולה בקנה אחד עם המאקרונוטריאנטים — ייתכן שגיאת נתונים")
        elif "supplement_candidate" in factor:
            cautions.append("המוצר עשוי להיות תוסף חלבון / תחליף ארוחה — מחוץ לאונטולוגיה הנוכחית, ציון אינדיקטיבי בלבד")

    return cautions


def _build_narrative(band: str, score: float, cautions: list[str]) -> str:
    """Generate a calm, analytical interpretation note — not an error message."""
    if band == "very_high":
        return (
            "נתוני המוצר שלמים ועקביים. הניתוב הקטגורי יציב. "
            "הציון מבוסס על מלוא הנתונים הזמינים."
        )
    if band == "high":
        if cautions:
            note = cautions[0]
            return f"הניתוח אמין. {note}."
        return "הניתוח אמין — פערים קלים בנתונים אינם משפיעים על האיכות הכוללת של הציון."
    if band == "moderate":
        base = "הניתוח שמיש אך כולל אי-ודאות. "
        if cautions:
            base += f"{cautions[0]}. "
        if len(cautions) > 1:
            base += f"כמו כן: {cautions[1]}."
        return base.strip()
    if band == "low":
        base = "הציון הוא הערכה זהירה בלבד. "
        if cautions:
            base += "; ".join(cautions[:2]) + ". "
        base += "מומלץ לאמת את הנתונים לפני הסקת מסקנות."
        return base
    # insufficient_context
    base = "אין מספיק נתונים לניתוח מהימן. "
    if cautions:
        base += cautions[0] + ". "
    base += "לא מוצג ציון — נדרשים נתוני תזונה ורכיבים מלאים."
    return base


def apply_confidence_ceiling(
    score_result: dict,
    interpretation_conf: dict,
) -> dict:
    """
    Apply the interpretation_confidence ceiling to the final score.
    Returns updated score_result with ceiling applied if needed.
    """
    ceiling = interpretation_conf.get("score_ceiling")
    if ceiling is None:
        return score_result

    current = score_result.get("final_score_estimate")
    if current is None:
        return score_result

    if current > ceiling:
        updated = dict(score_result)
        updated["final_score_estimate"] = float(ceiling)
        updated["grade_estimate"] = _score_to_grade_capped(ceiling)
        updated["interpretation_confidence_ceiling_applied"] = (
            f"interpretation_confidence_ceiling={ceiling} "
            f"(band={interpretation_conf['interpretation_confidence_band']}, "
            f"score={interpretation_conf['interpretation_confidence_score']:.1f})"
        )
        return updated

    return score_result


def _score_to_grade_capped(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 65:
        return "B"
    if score >= 50:
        return "C"
    if score >= 35:
        return "D"
    return "E"
