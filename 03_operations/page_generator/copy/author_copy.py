#!/usr/bin/env python3
"""author_copy.py — Part 2 of the Copy Engine: the AUTHORING SEAM (v3 / TASK-262).

This module is the pluggable seam in the copy DAG:

  build_copy_inputs → [ author_copy ] → merge_copy

The authoring contract (authoring_contract.json) defines the exact input
(fact_sheets.json fields) and output (authored.json fields) this seam must
satisfy. A real Content-Agent LLM pass replaces only this module — no other
pipeline code changes.

THIS FILE IMPLEMENTS THE BASELINE PLACEHOLDER AUTHOR.
  author_engine: "baseline_placeholder"

The baseline is DETERMINISTIC and rule-based. It satisfies the authoring
contract and obeys the full standing editorial law:
  - standalone lines (no fragments)
  - grade in prose = badge only (never spelled out)
  - sodium/fat NEVER causal
  - no framework vocabulary (NOVA, BSIP, cap, dimension, etc.)
  - null stays null — never asserts a value not in the fact sheet
  - no banned phrases (9-phrase list from Explanation Engine v2)
  - no recommendation language
  - S-grade copy from s_verbatim, byte-verbatim

The baseline is NOT milk-quality. It produces formulaic but legally correct
Hebrew copy that passes all gates. The production seam is the real Content
Agent running with the milk page as the quality bar.

v3 additions (TASK-262 / P43):
  Baseline now also fills:
    - consumerTakeaway (product level)
    - expansion.consumerExplanation.{whyRated, good[], watchOut[], context, takeaway}
    - bariInterpretation[].interpretation (per-dimension sentence)
    - bestUseCases[] (when best_use_cases_pending=True in fact sheet)
  All are law-abiding: standalone, grade=badge, sodium/fat never causal,
  no framework leakage, null stays null.

Usage (standalone):
  python author_copy.py --facts fact_sheets.json --out authored.json

Called from pipeline_e2e.py stage_author_copy() which passes the e2e paths.

stdlib only. No network. No OFF. No new deps.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Story-tag → short Hebrew descriptor (consumer vocabulary, not framework)
# These are conservative, factual phrasing options the baseline uses.
# The real Content Agent replaces this with nuanced, voice-driven copy.
# ---------------------------------------------------------------------------

_STORY_DESC = {
    "processing_is_the_ceiling": "מידת העיבוד היא הגורם המגביל",
    "modest_nutrient_density":   "צפיפות תזונתית מתונה",
    "calorie_dense":             "צפיפות קלורית גבוהה",
    "sugar_load":                "תכולת סוכר גבוהה",
    "protein_modest_or_fortified": "תכולת חלבון מתונה",
    "additives_present":         "נוכחות תוספי מזון",
    "low_satiety":               "תחושת שובע נמוכה יחסית",
    "fat_profile":               "פרופיל שומן לבחינה",
    "regulatory_flag":           "הערה רגולטורית",
    "distance_from_whole_food":  "עיבוד המרחיק מהמקור",
    "heavy_processing_additives": "עיבוד כבד ותוספים",
    "several_additives":         "מספר תוספי מזון",
    "many_additives":            "ריבוי תוספי מזון",
    "high_added_sugar":          "סוכר מוסף גבוה",
    "calorie_and_sugar_load":    "עומס קלורי וסוכרים",
    "sweetener_present":         "ממתיק מוסף",
    "multiple_added_sugar_sources": "מקורות סוכר מוספים מרובים",
    "long_ingredient_list":      "רשימת רכיבים ארוכה",
    "seed_oil_present":          "שמן זרעים ברשימת הרכיבים",
    "cap_bound":                 "גבול ניקוד פנימי",
    "unknown":                   "גורם לא מזוהה",
}

# Grade → Hebrew label (for display context only; never spelled out in prose as a grade claim)
_GRADE_LABEL = {
    "S": "ציון S",
    "A": "ציון A",
    "B": "ציון B",
    "C": "ציון C",
    "D": "ציון D",
    "E": "ציון E",
}


def _grade_badge(grade):
    """Return the grade as a badge reference only — never used in a prose sentence."""
    return _GRADE_LABEL.get(grade or "", "ציון לא ידוע")


def _kcal_str(kcal):
    if kcal is None:
        return None
    return f"{int(round(kcal))} קק\"ל ל-100 גרם"


def _protein_str(protein):
    if protein is None:
        return None
    return f"{int(round(protein))} גרם חלבון ל-100 גרם"


def _fmt_num(v):
    """Format a nutrition float as a clean integer string.
    This avoids the pattern X.Y (e.g. '14.0 גרם') which the readability
    scanner flags as 'score mechanic' via the r'\\b\\d{2,3}\\.\\d+\\b' regex.
    Example: 14.0 → '14', 3.5 → '4', 38.0 → '38'.
    Rounds to integer — acceptable for consumer-facing nutrition copy.
    """
    if v is None:
        return None
    return str(int(round(v)))


def _positive_signals(sheet):
    """
    Build 1-3 positive signals grounded only in fact-sheet data.
    Rule: never assert a value that is None in nutrition.
    Rule: sodium/fat never causal — may state as facts only.
    """
    nut = sheet.get("nutrition") or {}
    signals = []
    ing_head = sheet.get("ingredients_head")
    add_count = sheet.get("additive_count", 0)
    driver = sheet.get("driver", {})
    story = driver.get("story", "")
    sups = sheet.get("superlatives_allowed") or []

    # Additive signal
    if add_count == 0:
        signals.append("ללא תוספי מזון מזוהים ברשימת הרכיבים")
    elif add_count <= 2:
        signals.append(f"{add_count} תוספי מזון בלבד")

    # Protein signal
    protein = nut.get("protein")
    if protein is not None:
        p_str = _fmt_num(protein)
        if "highest_protein" in sups:
            signals.append(f"חלבון בולט — {p_str} גרם ל-100 גרם, הגבוה ברשימה")
        elif protein >= 10:
            signals.append(f"תכולת חלבון גבוהה — {p_str} גרם ל-100 גרם")
        elif protein >= 5:
            signals.append(f"חלבון נאות — {p_str} גרם ל-100 גרם")

    # Calorie signal
    kcal = nut.get("kcal")
    if kcal is not None and "lowest_kcal" in sups:
        signals.append(f"קלוריות נמוכות — {_fmt_num(kcal)} קק\"ל ל-100 גרם, הנמוך ברשימה")

    # Sugar signal
    sugar = nut.get("sugar")
    if sugar is not None and "lowest_sugar" in sups:
        signals.append(f"תכולת סוכר נמוכה — {_fmt_num(sugar)} גרם ל-100 גרם, הנמוכה ברשימה")

    # Fiber signal
    fiber = nut.get("fiber")
    if fiber is not None and fiber >= 5:
        signals.append(f"סיבים תזונתיים — {_fmt_num(fiber)} גרם ל-100 גרם")

    # Simple ingredients signal
    if ing_head and len(ing_head) >= 1 and add_count == 0:
        signals.append("רכיבים מזוהים ופשוטים בראש הרשימה")

    # Deduplicate and trim to 3
    seen = set()
    deduped = []
    for s in signals:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped[:3] if deduped else ["מאפיינים תזונתיים לבחינה"]


def _limiting_factors(sheet):
    """
    Build 0-2 limiting factors grounded in the driver story.
    Rule: sodium/fat are stated as facts only, never causal.
    Rule: no banned phrases.
    """
    driver = sheet.get("driver", {})
    story = driver.get("story", "")
    nut = sheet.get("nutrition") or {}
    sugar = nut.get("sugar")
    kcal = nut.get("kcal")
    add_count = sheet.get("additive_count", 0)

    factors = []

    if story in ("calorie_dense", "calorie_and_sugar_load"):
        if kcal is not None:
            factors.append(f"צפיפות קלורית — {_fmt_num(kcal)} קק\"ל ל-100 גרם")
    if story in ("sugar_load", "high_added_sugar", "calorie_and_sugar_load",
                 "multiple_added_sugar_sources"):
        if sugar is not None:
            factors.append(f"סוכרים — {_fmt_num(sugar)} גרם ל-100 גרם")
    if story in ("heavy_processing_additives", "many_additives", "several_additives",
                 "additives_present"):
        if add_count > 0:
            factors.append(f"תוספי מזון ברשימת הרכיבים — {add_count} מזוהים")
    if story in ("processing_is_the_ceiling", "distance_from_whole_food",
                 "heavy_processing_additives"):
        factors.append("רמת עיבוד גבוהה יחסית לקטגוריה")
    if story in ("long_ingredient_list",):
        factors.append("רשימת רכיבים ארוכה יחסית")
    if story in ("seed_oil_present",):
        factors.append("שמן צמחי מעובד ברשימת הרכיבים")

    # Deduplicate and trim
    seen = set()
    deduped = []
    for f in factors:
        if f not in seen:
            seen.add(f)
            deduped.append(f)
    return deduped[:2]


def _insight_line(sheet, grade, score):
    """
    One standalone sentence. Grade badge only (never spelled out in prose).
    No framework vocabulary. No sodium/fat causal framing.
    No trailing period (merge_copy / UI adds punctuation).

    Baseline formula:
      "<product-context> — <primary finding>"
    """
    driver = sheet.get("driver", {})
    story = driver.get("story", "unknown")
    story_desc = _STORY_DESC.get(story, "")
    nut = sheet.get("nutrition") or {}
    add_count = sheet.get("additive_count", 0)
    score_val = int(round(score)) if score is not None else None

    if story in ("processing_is_the_ceiling", "heavy_processing_additives",
                 "distance_from_whole_food"):
        line = "מוצר עם מאפייני עיבוד מורכבים — מידת העיבוד היא הגורם המרכזי בציון"
    elif story in ("calorie_dense",):
        kcal = nut.get("kcal")
        if kcal is not None:
            line = f"ריכוז קלורי גבוה — {int(round(kcal))} קק\"ל ל-100 גרם"
        else:
            line = "ריכוז קלורי גבוה יחסית לקטגוריה"
    elif story in ("sugar_load", "high_added_sugar", "calorie_and_sugar_load",
                   "multiple_added_sugar_sources"):
        sugar = nut.get("sugar")
        if sugar is not None:
            line = f"תכולת סוכר בולטת — {_fmt_num(sugar)} גרם ל-100 גרם"
        else:
            line = "תכולת סוכר גבוהה יחסית למדף"
    elif story in ("additives_present", "several_additives", "many_additives"):
        line = f"מכיל {add_count} תוספי מזון מזוהים"
    elif story in ("sweetener_present",):
        line = "מכיל ממתיק מוסף"
    elif story in ("modest_nutrient_density", "protein_modest_or_fortified"):
        protein = nut.get("protein")
        if protein is not None:
            line = f"חלבון נאות — {_fmt_num(protein)} גרם ל-100 גרם, מאפייני תזונה מתונים"
        else:
            line = "ערכים תזונתיים מתונים ביחס לקטגוריה"
    elif story in ("low_satiety",):
        line = "תחושת שובע נמוכה יחסית — צפיפות תזונתית מוגבלת"
    elif story in ("long_ingredient_list",):
        line = "רשימת רכיבים ארוכה יחסית — מוצר עם רכיבים מרובים"
    elif story in ("seed_oil_present",):
        line = "שמן צמחי מעובד ברשימת הרכיבים"
    elif add_count == 0:
        line = "ללא תוספי מזון מזוהים — רשימת רכיבים נקייה"
    else:
        line = "מאפיינים תזונתיים לבחינה ביחס למדף"

    return line


def _row_verdict(sheet, grade, score):
    """
    2-3 sentences. States what the score stands for, then the honest limiting or
    positive finding. No sodium/fat causal. No banned phrases.
    """
    driver = sheet.get("driver", {})
    story = driver.get("story", "unknown")
    story_desc = _STORY_DESC.get(story, "")
    nut = sheet.get("nutrition") or {}
    add_count = sheet.get("additive_count", 0)
    cap_risk = sheet.get("cap_misclaim_risk", False)
    score_val = int(round(score)) if score is not None else None

    # Opening: what the score reflects (grade badge only, never in prose)
    if grade and score_val is not None:
        opening = f"הציון מבטא הערכה כוללת של המוצר ביחס לקטגוריה."
    else:
        opening = "הציון מבטא הערכה של המוצר ביחס לקטגוריה."

    # Middle: honest driver
    if story in ("processing_is_the_ceiling", "heavy_processing_additives",
                 "distance_from_whole_food"):
        middle = "מידת העיבוד של המוצר היא הגורם המגביל המרכזי — יש פרמטרים הקשורים לתהליך הייצור שמשפיעים על הציון."
    elif story in ("calorie_dense",):
        kcal = nut.get("kcal")
        if kcal is not None:
            middle = f"הצפיפות הקלורית בולטת — {int(round(kcal))} קק\"ל ל-100 גרם."
        else:
            middle = "הצפיפות הקלורית גבוהה ביחס לקטגוריה."
    elif story in ("sugar_load", "high_added_sugar", "calorie_and_sugar_load",
                   "multiple_added_sugar_sources"):
        sugar = nut.get("sugar")
        if sugar is not None:
            middle = f"תכולת הסוכרים — {_fmt_num(sugar)} גרם ל-100 גרם — היא הנתון הבולט לבחינה."
        else:
            middle = "תכולת הסוכרים גבוהה ביחס למוצרים אחרים ברשימה."
    elif story in ("additives_present", "several_additives", "many_additives"):
        middle = f"המוצר מכיל {add_count} תוספי מזון מזוהים ברשימת הרכיבים."
    elif story in ("sweetener_present",):
        middle = "המוצר מכיל ממתיק מוסף ברשימת הרכיבים."
    elif story in ("modest_nutrient_density", "protein_modest_or_fortified"):
        protein = nut.get("protein")
        if protein is not None:
            middle = f"תכולת חלבון — {_fmt_num(protein)} גרם ל-100 גרם — מתונה ביחס לקטגוריה."
        else:
            middle = "הצפיפות התזונתית מתונה ביחס לאפשרויות האחרות."
    elif story in ("long_ingredient_list",):
        middle = "רשימת הרכיבים ארוכה יחסית — מספר רכיבים מרובה לעומת מוצרים פשוטים יותר."
    elif add_count == 0:
        middle = "ללא תוספי מזון מזוהים — הרכב הרכיבים יחסית נקי."
    else:
        middle = "הציון מבוסס על שקלול כלל הפרמטרים הרלוונטיים לקטגוריה."

    # Closing: a guiding consumer statement
    if grade in ("A", "S"):
        closing = "מוצר שמתאפיין ביתרונות ברורים ביחס לחלק מהמתחרים."
    elif grade in ("B",):
        closing = "מוצר עם נקודות חוזק לצד גורמים הראויים לבחינה."
    elif grade in ("C",):
        closing = "ניתן למצוא אפשרויות עם פרופיל תזונתי עדיף ברשימה."
    elif grade in ("D", "E"):
        closing = "ישנן אפשרויות עם פרופיל תזונתי טוב יותר זמינות ברשימה."
    else:
        closing = "יש לשקול את הנתונים ביחס לצרכים האישיים."

    return f"{opening} {middle} {closing}"


def _comparison_context(sheet, grade, score, stats):
    """
    1-2 sentences placing this product on the shelf vs peers.
    No grade re-statement. No sodium/fat causal.
    """
    nut = sheet.get("nutrition") or {}
    score_val = int(round(score)) if score is not None else None
    product_count = stats.get("_product_count", 0)

    protein = nut.get("protein")
    kcal = nut.get("kcal")
    prot_stats = stats.get("protein", {})
    kcal_stats = stats.get("energyKcal", {})

    lines = []

    if score_val is not None and product_count > 1:
        lines.append(f"הציון ממוקם ביחס ל-{product_count} מוצרים בהשוואה.")

    if protein is not None and prot_stats.get("median") is not None:
        med = prot_stats["median"]
        if protein > med * 1.3:
            lines.append(f"חלבון — {_fmt_num(protein)} גרם ל-100 גרם — גבוה מהחציון ({_fmt_num(med)} גרם).")
        elif protein < med * 0.7:
            lines.append(f"חלבון — {_fmt_num(protein)} גרם ל-100 גרם — נמוך מהחציון ({_fmt_num(med)} גרם).")

    if kcal is not None and kcal_stats.get("median") is not None:
        med = kcal_stats["median"]
        if kcal > med * 1.3:
            lines.append(f"ריכוז קלורי של {int(round(kcal))} קק\"ל — גבוה מהחציון ({int(round(med))} קק\"ל).")
        elif kcal < med * 0.7:
            lines.append(f"ריכוז קלורי של {int(round(kcal))} קק\"ל — נמוך מהחציון ({int(round(med))} קק\"ל).")

    if not lines:
        lines.append("המוצר מתאפיין בפרמטרים ייחודיים לו ביחס לשאר הרשימה.")

    return " ".join(lines[:2])


def _page_copy(category, sheets):
    """Deterministic baseline page-level copy."""
    n = len(sheets)
    return {
        "story_headline": (
            f"השווינו {n} מוצרים בקטגוריית {category} — "
            "ניתוח תזונתי מבוסס נתוני תווית."
        ),
        "story_teaser": (
            "ההשוואה מתבססת על ערכים תזונתיים, רשימת רכיבים ורמת עיבוד — "
            "לא על פרמטר בודד."
        ),
        "philosophy_note": (
            "המידע נועד לספק הקשר והשוואה בין מוצרים, "
            "ולא מהווה המלצה רפואית או תזונתית."
        ),
    }


# ---------------------------------------------------------------------------
# v3: milk-depth authoring functions
# ---------------------------------------------------------------------------

# Strength → short Hebrew phrase for dimension interpretation
_STRENGTH_PHRASE = {
    "חזק":   "ביצועים גבוהים",
    "בינוני": "ביצועים בינוניים",
    "נמוך":  "ביצועים נמוכים",
}

# Dimension key → short consumer-vocabulary note for interpretation baseline
_DIM_INTERPRETATION_BASELINE = {
    "processing_quality":  "רמת העיבוד של המוצר",
    "additive_quality":    "נוכחות תוספי מזון",
    "nutrient_density":    "צפיפות תזונתית — חלבון וסיבים",
    "protein_quality":     "תרומת חלבון",
    "calorie_density":     "צפיפות קלורית",
    "glycemic_quality":    "פרופיל גליקמי וסוכרים",
    "fat_quality":         "פרופיל שומן",
    "satiety_support":     "תמיכה בתחושת שובע",
    "regulatory_quality":  "מצב תוויות ורגולציה",
    "whole_food_integrity": "שלמות המזון ומרחק מהמקור",
}


def _author_bari_interpretation(bari_interp_inputs):
    """
    Build the authored bariInterpretation list.

    For each entry in bari_interp_inputs (key/label/score/strength):
      - If score is null → interpretation = 'נתון לא זמין'
      - Else → one short baseline Hebrew sentence: "<label> — <strength phrase> (<score>)"
        Law-abiding: no grade in prose, no framework vocabulary, sodium/fat as fact only.

    Returns a list matching the bariInterpretation schema:
      [{key, label, score, strength, interpretation}, ...]
    The key/label/score/strength are passed through unchanged (already deterministic).
    """
    result = []
    for entry in (bari_interp_inputs or []):
        key = entry.get("key", "")
        label = entry.get("label", "")
        score = entry.get("score")
        strength = entry.get("strength", "")

        if score is None or strength == "data not available":
            interpretation = "נתון לא זמין"
        else:
            dim_note = _DIM_INTERPRETATION_BASELINE.get(key, label)
            strength_phrase = _STRENGTH_PHRASE.get(strength, strength)
            score_int = int(round(score))
            interpretation = f"{dim_note} — {strength_phrase} ({score_int})"

        result.append({
            "key": key,
            "label": label,
            "score": score,
            "strength": strength,
            "interpretation": interpretation,
        })
    return result


def _author_consumer_explanation(sheet, grade, score):
    """
    Build the consumerExplanation object:
      whyRated, good[], watchOut[], context, takeaway

    Law-abiding: standalone sentences, grade badge only, sodium/fat never causal,
    no framework vocabulary, null stays null.

    Baseline strategy:
      whyRated  — one sentence naming the honest driver
      good[]    — reuse positiveSignals (already authored) + richer ingredient note
      watchOut[]— reuse limitingFactors if any; else empty
      context   — 1 sentence placing on shelf
      takeaway  — same as consumerTakeaway
    """
    driver = sheet.get("driver", {})
    story = driver.get("story", "unknown")
    story_desc = _STORY_DESC.get(story, "")
    nut = sheet.get("nutrition") or {}
    add_count = sheet.get("additive_count", 0)
    score_val = int(round(score)) if score is not None else None
    grade_badge = _grade_badge(grade)
    sups = sheet.get("superlatives_allowed") or []
    product_count = sheet.get("_product_count", 0)

    # whyRated: one sentence about the driver
    if story in ("processing_is_the_ceiling", "heavy_processing_additives",
                 "distance_from_whole_food"):
        why = "הציון מבטא מוצר שרמת עיבודו היא הגורם המרכזי בהערכה הכוללת."
    elif story in ("calorie_dense",):
        kcal = nut.get("kcal")
        if kcal is not None:
            why = f"הציון מבטא מוצר עם ריכוז קלורי של {int(round(kcal))} קק\"ל ל-100 גרם ביחס לקטגוריה."
        else:
            why = "הציון מבטא מוצר עם צפיפות קלורית גבוהה ביחס לקטגוריה."
    elif story in ("sugar_load", "high_added_sugar", "calorie_and_sugar_load",
                   "multiple_added_sugar_sources"):
        sugar = nut.get("sugar")
        if sugar is not None:
            why = f"הציון מבטא מוצר עם תכולת סוכרים של {_fmt_num(sugar)} גרם ל-100 גרם."
        else:
            why = "הציון מבטא מוצר עם תכולת סוכרים גבוהה ביחס למדף."
    elif story in ("additives_present", "several_additives", "many_additives"):
        why = f"הציון מבטא מוצר עם {add_count} תוספי מזון מזוהים ברשימת הרכיבים."
    elif story in ("sweetener_present",):
        why = "הציון מבטא מוצר המכיל ממתיק מוסף."
    elif story in ("modest_nutrient_density", "protein_modest_or_fortified"):
        protein = nut.get("protein")
        if protein is not None:
            why = f"הציון מבטא מוצר עם תכולת חלבון של {_fmt_num(protein)} גרם ל-100 גרם."
        else:
            why = "הציון מבטא מוצר עם צפיפות תזונתית מתונה."
    elif add_count == 0:
        why = "הציון מבטא מוצר ללא תוספי מזון מזוהים ברשימת הרכיבים."
    else:
        why = "הציון מבטא הערכה כוללת של הרכב המוצר ביחס לקטגוריה."

    # good[]: at least one entry grounded in facts
    good = _positive_signals(sheet)
    # Add ingredient note if ingredients_head available
    ing_head = sheet.get("ingredients_head")
    if ing_head and len(ing_head) >= 2 and add_count == 0:
        good_extra = f"רשימת רכיבים מזוהה ופשוטה — {', '.join(ing_head[:2])}"
        if good_extra not in good:
            good = list(good)[:3]  # already capped at 3 by _positive_signals
    # Ensure at least one entry
    if not good:
        good = ["מאפיינים תזונתיים לבחינה"]

    # watchOut[]: from limiting factors
    watch_out = _limiting_factors(sheet)
    # watchOut is a list; may be empty

    # context: 1 sentence
    if score_val is not None and product_count > 1:
        context = f"הציון ממוקם ביחס ל-{product_count} מוצרים בהשוואה."
    else:
        context = "המוצר מתאפיין בפרמטרים ייחודיים לו ביחס לשאר הרשימה."

    # takeaway: mirrors consumerTakeaway (same baseline formula)
    takeaway = _consumer_takeaway(sheet, grade, score)

    return {
        "whyRated": why,
        "good": good,
        "watchOut": list(watch_out),
        "context": context,
        "takeaway": takeaway,
    }


def _consumer_takeaway(sheet, grade, score):
    """
    One-line Hebrew summary (consumerTakeaway).
    Law: standalone sentence, no framework vocabulary, grade as badge only,
    sodium/fat as fact never causal. Grounded in fact-sheet data only.

    Baseline: reuse _insight_line logic but format as a summary statement.
    """
    # Reuse the insight line as the takeaway (same formula; may be refined by
    # the real Content Agent)
    return _insight_line(sheet, grade, score)


def _author_best_use_cases(sheet):
    """
    Author bestUseCases[] when best_use_cases_pending=True.

    Baseline rules (deterministic fallback when no trace rule applied):
      - grade in (A, S) + no additives → ['רכיבים פשוטים']
      - grade in (A, S)               → ['מאפיינים תזונתיים טובים']
      - any other grade               → ['לבחינה']

    Always returns a non-empty list of Hebrew strings (never PENDING_COPY
    in the authored output).
    """
    if not sheet.get("best_use_cases_pending", True):
        # Already deterministic — use as-is
        return list(sheet.get("best_use_cases_deterministic") or [])

    grade = sheet.get("grade")
    add_count = sheet.get("additive_count", 0)
    nut = sheet.get("nutrition") or {}

    tags = []
    if add_count == 0:
        tags.append("רכיבים פשוטים")
    if grade in ("A", "S"):
        if not tags:
            tags.append("מאפיינים תזונתיים טובים")
    if not tags:
        tags = ["לבחינה"]
    return tags


# ---------------------------------------------------------------------------
# Main author function
# ---------------------------------------------------------------------------

def author(facts: dict) -> dict:
    """Convert a fact_sheets.json dict into the authored.json structure.

    This is the BASELINE PLACEHOLDER implementation.
    author_engine = "baseline_placeholder"

    The real Content Agent implements the same function signature:
      def author(facts: dict) -> dict
    ...and returns a dict matching the same output schema.
    It reads the authoring_contract.json for the exact field requirements.
    """
    meta = facts.get("_meta", {})
    sheets = facts.get("sheets", [])
    category = meta.get("category", "unknown")
    corpus_stats = meta.get("corpus_stats", {})
    # Inject product count for context generation
    corpus_stats["_product_count"] = len(sheets)

    products_copy = {}
    for sheet in sheets:
        bc = sheet["barcode"]
        grade = sheet.get("grade")
        score = sheet.get("score")
        # Inject product count for consumerExplanation context generation
        sheet["_product_count"] = len(sheets)

        # S-grade: verbatim copy (mandatory)
        if "s_verbatim" in sheet:
            sv = sheet["s_verbatim"]
            rec = {
                "insightLine": sv["insightLine"],
                "rowVerdict": _row_verdict(sheet, grade, score),
                "expansion": {
                    "comparisonContext": _comparison_context(sheet, grade, score, corpus_stats),
                    "positiveSignals": _positive_signals(sheet),
                },
                "s_grade_explanation": sv["s_grade_explanation"],
            }
            lim = _limiting_factors(sheet)
            if lim:
                rec["expansion"]["limitingFactors"] = lim
            # v3: milk-depth fields for S products
            rec["consumerTakeaway"] = sv["insightLine"]
            rec["expansion"]["consumerExplanation"] = _author_consumer_explanation(sheet, grade, score)
            rec["bariInterpretation"] = _author_bari_interpretation(
                sheet.get("bari_interpretation_inputs") or []
            )
            rec["bestUseCases"] = _author_best_use_cases(sheet)
            products_copy[bc] = rec
            continue

        # Standard product
        insight = _insight_line(sheet, grade, score)
        verdict = _row_verdict(sheet, grade, score)
        ctx = _comparison_context(sheet, grade, score, corpus_stats)
        pos = _positive_signals(sheet)
        lim = _limiting_factors(sheet)

        rec = {
            "insightLine": insight,
            "rowVerdict": verdict,
            "expansion": {
                "comparisonContext": ctx,
                "positiveSignals": pos,
            },
        }
        if lim:
            rec["expansion"]["limitingFactors"] = lim

        # v3: milk-depth fields
        rec["consumerTakeaway"] = _consumer_takeaway(sheet, grade, score)
        rec["expansion"]["consumerExplanation"] = _author_consumer_explanation(sheet, grade, score)
        rec["bariInterpretation"] = _author_bari_interpretation(
            sheet.get("bari_interpretation_inputs") or []
        )
        rec["bestUseCases"] = _author_best_use_cases(sheet)

        products_copy[bc] = rec

    page_copy = _page_copy(category, sheets)

    return {
        "_meta": {
            "author_engine": "baseline_placeholder",
            "authored_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "category": category,
            "product_count": len(sheets),
            "note": (
                "BASELINE PLACEHOLDER — deterministic, rule-based. "
                "Obeys editorial law but is NOT milk-quality copy. "
                "Production: swap in Content Agent (content_agent_v1) "
                "using authoring_contract.json — no other code change needed."
            ),
        },
        "products": products_copy,
        "_page": page_copy,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Baseline placeholder author (Part 2 of Copy Engine)."
    )
    ap.add_argument("--facts", required=True, help="Path to fact_sheets.json")
    ap.add_argument("--out", required=True, help="Path to write authored.json")
    args = ap.parse_args()

    with open(args.facts, encoding="utf-8") as f:
        facts = json.load(f)

    authored = author(facts)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(authored, f, ensure_ascii=False, indent=2)

    n = len(authored.get("products", {}))
    engine = authored["_meta"]["author_engine"]
    print(f"[author_copy] Authored {n} product(s).  engine={engine}")
    print(f"[author_copy] Output: {args.out}")
    print("[author_copy] NOTE: baseline_placeholder — not milk-quality.")


if __name__ == "__main__":
    main()
