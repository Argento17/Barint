"""
Hyper-palatability detector — combo recognition, near-miss handling,
whole-food-fat relief.
"""
import pytest
from bsip2_hyper_palatability import evaluate_hyper_palatability


def _features(**overrides):
    base = {
        "energy_kcal_100g": 0, "fat_g_100g": 0, "sugars_g_100g": 0,
        "carbs_g_100g": 0, "fiber_g_100g": 0, "sodium_mg_100g": 0,
        "inferred_category": "default",
    }
    base.update(overrides)
    return base


def test_fat_sugar_combo_triggers_on_chocolate():
    f = _features(energy_kcal_100g=540, fat_g_100g=38, sugars_g_100g=30,
                  carbs_g_100g=45, fiber_g_100g=7, sodium_mg_100g=10)
    r = evaluate_hyper_palatability(f)
    assert "fat_sugar" in r["triggered_combos"]
    assert "FAT_SUGAR_COMBO" in r["reason_codes"]


def test_fat_sodium_combo_triggers_on_chips():
    f = _features(energy_kcal_100g=540, fat_g_100g=33, sugars_g_100g=1,
                  carbs_g_100g=53, fiber_g_100g=4, sodium_mg_100g=480)
    r = evaluate_hyper_palatability(f)
    assert "fat_sodium" in r["triggered_combos"]


def test_refined_carb_fat_combo_triggers_on_cookies():
    f = _features(energy_kcal_100g=480, fat_g_100g=21, sugars_g_100g=32,
                  carbs_g_100g=67, fiber_g_100g=2, sodium_mg_100g=320)
    r = evaluate_hyper_palatability(f)
    assert "refined_carb_fat" in r["triggered_combos"]


def test_no_combos_for_olive_oil():
    f = _features(energy_kcal_100g=884, fat_g_100g=100, sugars_g_100g=0,
                  inferred_category="whole_food_fat")
    r = evaluate_hyper_palatability(f)
    assert r["triggered_combos"] == []
    assert r["score"] >= 95


def test_whole_food_fat_relief_applied():
    """Tahini might trigger near-miss — but whole-food-fat relief should rescue."""
    f = _features(energy_kcal_100g=595, fat_g_100g=54, sugars_g_100g=0,
                  carbs_g_100g=21, fiber_g_100g=9, sodium_mg_100g=11,
                  inferred_category="whole_food_fat")
    r = evaluate_hyper_palatability(f)
    assert r["score"] >= 80
    assert "HP_RELIEF_WHOLE_FOOD_FAT" in r["reason_codes"]


def test_score_decreases_with_more_combos():
    one_combo = _features(energy_kcal_100g=540, fat_g_100g=38, sugars_g_100g=30,
                          carbs_g_100g=45, fiber_g_100g=7, sodium_mg_100g=10)
    two_combos = _features(energy_kcal_100g=540, fat_g_100g=33, sugars_g_100g=30,
                           carbs_g_100g=53, fiber_g_100g=2, sodium_mg_100g=480)

    s1 = evaluate_hyper_palatability(one_combo)["score"]
    s2 = evaluate_hyper_palatability(two_combos)["score"]
    assert s2 < s1