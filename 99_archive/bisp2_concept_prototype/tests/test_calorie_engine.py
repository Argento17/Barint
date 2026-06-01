"""
Calorie engine — category-aware tiers + interaction rules.
"""
import pytest
from bsip2_calorie_engine import score_calorie_density, evaluate_calorie_interactions


# ─────────── Tier scoring ───────────
@pytest.mark.parametrize("kcal,expected_min,expected_max,category", [
    (100, 85, 95, "default"),
    (300, 60, 70, "default"),
    (500, 30, 40, "default"),
    (700, 15, 25, "default"),
    # Whole-food fat: forgiving curve
    (600, 70, 80, "whole_food_fat"),
    (884, 50, 60, "whole_food_fat"),
    # Snack bar: harsh curve
    (430, 35, 45, "snack_bar_granola"),
    (500, 20, 30, "snack_bar_granola"),
])
def test_calorie_tiers(kcal, expected_min, expected_max, category):
    score = score_calorie_density(kcal, category)
    assert expected_min <= score <= expected_max, \
        f"kcal={kcal} cat={category}: got {score}, expected {expected_min}–{expected_max}"


# ─────────── Interaction rules ───────────
def test_high_cal_high_sugar_severe_triggers_cap_50():
    features = {
        "energy_kcal_100g": 510, "sugars_g_100g": 30,
        "protein_g_100g": 5, "fiber_g_100g": 2,
        "inferred_category": "default", "red_label_sugar": False,
    }
    caps, _, codes = evaluate_calorie_interactions(features)
    cap_values = [c.value for c in caps]
    assert 50 in cap_values
    assert "HIGH_CALORIE_HIGH_SUGAR_COMBO" in codes


def test_low_satiety_per_calorie_penalty():
    features = {
        "energy_kcal_100g": 460, "sugars_g_100g": 5,
        "protein_g_100g": 5, "fiber_g_100g": 2,
        "inferred_category": "default", "red_label_sugar": False,
    }
    _, penalties, codes = evaluate_calorie_interactions(features)
    assert any(p.rule_id == "HIGH_CAL_LOW_SATIETY_SOFT" for p in penalties)
    assert "LOW_SATIETY_PER_CALORIE" in codes


def test_snack_bar_red_sugar_label_caps_55():
    features = {
        "energy_kcal_100g": 420, "sugars_g_100g": 15,
        "protein_g_100g": 5, "fiber_g_100g": 3,
        "inferred_category": "snack_bar_granola", "red_label_sugar": True,
    }
    caps, _, codes = evaluate_calorie_interactions(features)
    cap_values = [c.value for c in caps]
    assert 55 in cap_values
    assert "CALORIE_DENSE_SNACK_BAR" in codes


def test_whole_food_fat_does_not_trigger_high_cal_alarm():
    features = {
        "energy_kcal_100g": 580, "sugars_g_100g": 4,
        "protein_g_100g": 21, "fiber_g_100g": 12,
        "inferred_category": "whole_food_fat", "red_label_sugar": False,
    }
    _, _, codes = evaluate_calorie_interactions(features)
    assert "HIGH_CALORIE_DENSITY" not in codes
    assert "CALORIE_DENSE_BUT_WHOLE_FOOD_FAT" in codes