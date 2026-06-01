"""
Hyper-palatability scoring.
Detects engineered combinations that override satiety mechanisms.
"""
from typing import Dict, Any, List, Tuple
from bsip2_config import HYPER_PALATABILITY_RULES, HP_DIMENSION_SCORING, HP_GUARDRAIL_RULES
from bsip2_models import TriggeredRule


def _num(f: Dict[str, Any], key: str, default: float = 0.0) -> float:
    v = f.get(key, default)
    return default if v is None else float(v)


def _kcal_pct(grams: float, kcal_per_g: float, total_kcal: float) -> float:
    if total_kcal <= 0:
        return 0.0
    return (grams * kcal_per_g) / total_kcal * 100


def _matrix_relief_factor(f: Dict[str, Any]) -> float:
    """
    Relief for bars where the reward signal is carried by a more intact food matrix:
    nuts, seeds, oats, dates, whole grains.

    Important: this is partial relief, not cancellation.
    A nut/date bar can still be sugary and calorie dense.
    """
    relief = 1.0

    if f.get("has_nut_or_seed_marker"):
        relief -= 0.15

    if f.get("has_whole_grain_marker"):
        relief -= 0.08

    if f.get("has_date_or_fruit_paste"):
        relief -= 0.08

    # Do not over-relieve if the product is still clearly confectionery engineered
    if f.get("has_chocolate_coating") or f.get("has_coating"):
        relief += 0.10

    if f.get("has_glucose_syrup") or f.get("has_maltodextrin"):
        relief += 0.10

    if f.get("has_emulsifier"):
        relief += 0.05

    return max(0.70, min(1.15, relief))


def _architecture_boost_factor(f: Dict[str, Any]) -> float:
    """
    Boost HP concern for engineered snack architecture:
    coating + syrup + puffed/extruded/refined cereal systems.
    """
    boost = 1.0

    if f.get("has_chocolate_coating") or f.get("has_coating"):
        boost += 0.15

    if f.get("has_glucose_syrup") or f.get("has_maltodextrin"):
        boost += 0.15

    if f.get("has_extruded_or_puffed_grain"):
        boost += 0.15

    if f.get("has_flavouring") or f.get("has_flavoring"):
        boost += 0.05

    if f.get("has_emulsifier"):
        boost += 0.05

    return max(1.0, min(1.45, boost))


def _evaluate_combo(rule_id: str, rule: Dict[str, Any], f: Dict[str, Any]) -> Tuple[bool, float]:
    kcal     = _num(f, "energy_kcal_100g")
    fat      = _num(f, "fat_g_100g")
    sugar    = _num(f, "sugars_g_100g")
    carb     = _num(f, "carbs_g_100g")
    fiber    = _num(f, "fiber_g_100g")
    sodium_g = _num(f, "sodium_mg_100g") / 1000

    if kcal <= 0:
        return False, 0.0

    fat_kcal_pct     = _kcal_pct(fat,   9, kcal)
    sugar_kcal_pct   = _kcal_pct(sugar, 4, kcal)
    carb_kcal_pct    = _kcal_pct(carb,  4, kcal)
    fiber_carb_ratio = (fiber / carb) if carb > 0 else 1.0

    if rule_id == "fat_sodium":
        fat_ratio    = fat_kcal_pct / rule["fat_kcal_pct_min"]
        sodium_ratio = sodium_g / rule["sodium_g_per_100g"]
        triggered = fat_ratio >= 1.0 and sodium_ratio >= 1.0
        intensity = min(fat_ratio, sodium_ratio)

    elif rule_id == "fat_sugar":
        fat_ratio   = fat_kcal_pct / rule["fat_kcal_pct_min"]
        sugar_ratio = sugar_kcal_pct / rule["sugar_kcal_pct_min"]
        triggered = fat_ratio >= 1.0 and sugar_ratio >= 1.0
        intensity = min(fat_ratio, sugar_ratio)

    elif rule_id == "refined_carb_fat":
        carb_ratio = carb_kcal_pct / rule["carb_kcal_pct_min"]
        fat_ratio  = fat_kcal_pct / rule["fat_kcal_pct_min"]
        refined    = fiber_carb_ratio <= rule["fiber_to_carb_max"]

        # Extra refined signal from food architecture
        if f.get("has_extruded_or_puffed_grain") or f.get("has_glucose_syrup") or f.get("has_maltodextrin"):
            refined = True

        triggered = carb_ratio >= 1.0 and fat_ratio >= 1.0 and refined
        intensity = min(carb_ratio, fat_ratio) if refined else 0.0

    elif rule_id == "crunch_sweet":
        carb_ratio  = carb / rule["carb_g_per_100g_min"]
        sugar_ratio = sugar / rule["sugar_g_per_100g_min"]
        low_fiber   = fiber <= rule["fiber_g_per_100g_max"]
        low_fat     = fat   <= rule["fat_g_per_100g_max"]

        # Crunch-sweet should also catch puffed/extruded cereal bars
        engineered_crunch = f.get("has_extruded_or_puffed_grain") or f.get("has_crispy_cereal")

        triggered = (
            carb_ratio >= 1.0
            and sugar_ratio >= 1.0
            and (low_fiber or engineered_crunch)
            and low_fat
        )
        intensity = min(carb_ratio, sugar_ratio) if (low_fiber or engineered_crunch) else 0.0

    else:
        return False, 0.0

    # Adjust intensity by structure
    intensity *= _architecture_boost_factor(f)
    intensity *= _matrix_relief_factor(f)

    return triggered, intensity


def evaluate_hyper_palatability(features: Dict[str, Any]) -> Dict[str, Any]:
    cfg = HP_DIMENSION_SCORING
    score = float(cfg["base"])

    triggered: List[str] = []
    near_miss: List[str] = []
    details: Dict[str, Dict[str, Any]] = {}
    reason_codes: List[str] = []

    architecture_boost = _architecture_boost_factor(features)
    matrix_relief = _matrix_relief_factor(features)

    for rule_id, rule in HYPER_PALATABILITY_RULES.items():
        is_triggered, intensity = _evaluate_combo(rule_id, rule, features)

        details[rule_id] = {
            "triggered": is_triggered,
            "intensity": round(intensity, 3),
            "label": rule["label"],
        }

        adjusted_weight = rule["weight"] * architecture_boost * matrix_relief

        if is_triggered:
            triggered.append(rule_id)
            score -= cfg["per_combo_penalty"] * adjusted_weight
            reason_codes.append(rule["label"])

        elif intensity >= (1.0 - cfg["near_miss_band"]):
            near_miss.append(rule_id)
            score -= cfg["per_combo_penalty"] * adjusted_weight * cfg["soft_match_factor"]
            reason_codes.append(f"NEAR_MISS_{rule['label']}")

    # Relief for genuine whole-food fat products, not coated snack bars
    if features.get("inferred_category") == "whole_food_fat":
        score = min(100, score + 15)
        reason_codes.append("HP_RELIEF_WHOLE_FOOD_FAT")

    # Partial relief for nut/seed/date bars, but only if not heavily engineered
    if (
        features.get("has_nut_or_seed_marker")
        and not features.get("has_extruded_or_puffed_grain")
        and not features.get("has_glucose_syrup")
    ):
        score = min(100, score + 8)
        reason_codes.append("HP_RELIEF_NUT_SEED_MATRIX")

    # Explicit engineered architecture drag
    if (
        (features.get("has_chocolate_coating") or features.get("has_coating"))
        and (features.get("has_glucose_syrup") or features.get("has_maltodextrin"))
    ):
        score -= 8
        reason_codes.append("HP_ENGINEERED_COATING_SYRUP_SYSTEM")

    score = max(0, min(100, score))

    return {
        "score": round(score, 1),
        "triggered_combos": triggered,
        "near_miss_combos": near_miss,
        "details": details,
        "reason_codes": list(dict.fromkeys(reason_codes)),
    }


def hyper_palatability_guardrails(features: Dict[str, Any], hp_result: Dict[str, Any]) -> List[TriggeredRule]:
    rules: List[TriggeredRule] = []
    cfg = HP_GUARDRAIL_RULES
    n = len(hp_result["triggered_combos"])

    matrix_relief = _matrix_relief_factor(features)
    architecture_boost = _architecture_boost_factor(features)

    guardrail_factor = architecture_boost * matrix_relief
    guardrail_factor = max(0.75, min(1.35, guardrail_factor))

    if n >= 1:
        for combo_id in hp_result["triggered_combos"]:
            rule = HYPER_PALATABILITY_RULES[combo_id]
            rules.append(TriggeredRule(
                rule_id=f"HP_{rule['label']}",
                rule_type="penalty",
                value=round(cfg["single_combo_penalty"] * rule["weight"] * guardrail_factor, 2),
                rationale=rule["rationale"],
                framework_ref="Fazzino et al. 2019 (extended); Bari matrix-adjusted",
                family="hyper_palatability",
            ))

    if n >= 3:
        rules.append(TriggeredRule(
            rule_id="HP_THREE_PLUS_COMBOS",
            rule_type="cap",
            value=cfg["three_plus_combos_cap"],
            rationale=f"Three or more hyper-palatability combinations triggered ({n})",
            framework_ref="Fazzino et al. 2019 (extended); Bari matrix-adjusted",
            family="hyper_palatability",
        ))

    elif n >= 2:
        rules.append(TriggeredRule(
            rule_id="HP_TWO_COMBOS",
            rule_type="cap",
            value=cfg["two_combos_cap"],
            rationale="Two hyper-palatability combinations triggered",
            framework_ref="Fazzino et al. 2019 (extended); Bari matrix-adjusted",
            family="hyper_palatability",
        ))

    return rules