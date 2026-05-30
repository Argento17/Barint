"""
Calorie-density scoring + interaction rules.
Category-aware: penalizes engineered snacks harshly, treats whole-food fats
gently, and catches health-halo products via interaction penalties/caps.
"""
from typing import Dict, Any, List, Tuple
from bsip2_config import CALORIE_DENSITY_TIERS
from bsip2_models import TriggeredRule


def score_calorie_density(kcal: float, category: str) -> float:
    """Step-function scoring based on category-specific tiers."""
    tiers = CALORIE_DENSITY_TIERS.get(category, CALORIE_DENSITY_TIERS["default"])
    for max_kcal, score in tiers:
        if kcal <= max_kcal:
            return float(score)
    return float(tiers[-1][1])


def evaluate_calorie_interactions(features: Dict[str, Any]) -> Tuple[List[TriggeredRule], List[TriggeredRule], List[str]]:
    """
    Returns (caps, penalties, reason_codes) for calorie interactions.
    Reason codes are human-readable labels for the explainer.
    """
    caps: List[TriggeredRule] = []
    penalties: List[TriggeredRule] = []
    reason_codes: List[str] = []

    kcal = features.get("energy_kcal_100g", 0) or 0
    sugar = features.get("sugars_g_100g", 0) or 0
    protein = features.get("protein_g_100g", 0) or 0
    fiber = features.get("fiber_g_100g", 0) or 0
    category = features.get("inferred_category", "default")
    has_red_sugar = features.get("red_label_sugar") is True

    # ---- High calorie + high sugar combos ----
    if kcal >= 500 and sugar >= 25:
        caps.append(TriggeredRule(
            rule_id="HIGH_CAL_HIGH_SUGAR_SEVERE",
            rule_type="cap", value=50,
            rationale=f"Very calorie-dense ({kcal:.0f} kcal) AND very high sugar ({sugar:.0f}g) per 100g",
        ))
        reason_codes.append("HIGH_CALORIE_HIGH_SUGAR_COMBO")
    elif kcal >= 470 and sugar >= 20:
        caps.append(TriggeredRule(
            rule_id="HIGH_CAL_HIGH_SUGAR_MODERATE",
            rule_type="cap", value=60,
            rationale=f"Calorie-dense ({kcal:.0f} kcal) and high sugar ({sugar:.0f}g) per 100g",
        ))
        reason_codes.append("HIGH_CALORIE_HIGH_SUGAR_COMBO")
    elif kcal >= 430 and sugar >= 15:
        penalties.append(TriggeredRule(
            rule_id="HIGH_CAL_HIGH_SUGAR_SOFT",
            rule_type="penalty", value=5,
            rationale=f"Calorie-dense ({kcal:.0f} kcal) with notable sugar ({sugar:.0f}g) per 100g",
        ))
        reason_codes.append("HIGH_CALORIE_HIGH_SUGAR_COMBO")

    # ---- High calorie + low satiety ----
    if kcal >= 500 and protein < 6 and fiber < 3:
        caps.append(TriggeredRule(
            rule_id="HIGH_CAL_LOW_SATIETY_SEVERE",
            rule_type="cap", value=55,
            rationale=f"High calories ({kcal:.0f}) with low protein ({protein:.1f}g) and low fiber ({fiber:.1f}g) — poor satiety per calorie",
        ))
        reason_codes.append("LOW_SATIETY_PER_CALORIE")
    elif kcal >= 450 and protein < 8 and fiber < 5:
        penalties.append(TriggeredRule(
            rule_id="HIGH_CAL_LOW_SATIETY_SOFT",
            rule_type="penalty", value=6,
            rationale=f"Calorie-dense ({kcal:.0f}) with mediocre satiety markers (protein {protein:.1f}g, fiber {fiber:.1f}g)",
        ))
        reason_codes.append("LOW_SATIETY_PER_CALORIE")

    # ---- Snack-bar / granola specific (health-halo trap) ----
    if category == "snack_bar_granola":
        if kcal >= 470 and sugar >= 15:
            caps.append(TriggeredRule(
                rule_id="SNACK_BAR_HIGH_CAL_SUGAR",
                rule_type="cap", value=60,
                rationale=f"Snack/granola bar with high calorie density ({kcal:.0f}) and added sugar ({sugar:.0f}g)",
            ))
            reason_codes.append("CALORIE_DENSE_SNACK_BAR")
        elif kcal >= 430:
            caps.append(TriggeredRule(
                rule_id="SNACK_BAR_HIGH_CAL",
                rule_type="cap", value=70,
                rationale=f"Calorie-dense snack/granola bar ({kcal:.0f} kcal/100g)",
            ))
            reason_codes.append("CALORIE_DENSE_SNACK_BAR")
        if has_red_sugar:
            caps.append(TriggeredRule(
                rule_id="SNACK_BAR_RED_SUGAR_LABEL",
                rule_type="cap", value=55,
                rationale="Snack/granola bar carrying Israeli red-sugar warning label",
            ))
            reason_codes.append("CALORIE_DENSE_SNACK_BAR")

    # ---- Generic high-calorie reason (informational) ----
    if kcal >= 450 and category != "whole_food_fat":
        if "HIGH_CALORIE_DENSITY" not in reason_codes:
            reason_codes.append("HIGH_CALORIE_DENSITY")
    elif kcal >= 500 and category == "whole_food_fat":
        reason_codes.append("CALORIE_DENSE_BUT_WHOLE_FOOD_FAT")

    # Mark when any cap was applied
    if caps:
        reason_codes.append("CALORIE_CAP_APPLIED")

    return caps, penalties, reason_codes