"""
Whole-food protection — naturally nutrient/calorie-dense foods must not be
crushed by penalties meant for engineered junk.
"""
from bsip2_score import score_product
from tests.fixtures import (
    RAW_ALMONDS, OLIVE_OIL, TAHINI, ROLLED_OATS, WHOLE_FOOD_FAT_HP_NEAR_MISS,
)


def test_almonds_score_above_70():
    r = score_product(RAW_ALMONDS)
    assert r.final_score >= 72


def test_olive_oil_calorie_dense_but_protected():
    r = score_product(OLIVE_OIL)
    assert r.final_score >= 65
    assert r.dimensions["calorie_density_quality"] >= 40
    assert r.inferred_category == "whole_food_fat"


def test_tahini_no_hp_penalty():
    r = score_product(TAHINI)
    assert r.final_score >= 70
    assert r.hyper_palatability_score >= 80


def test_oats_score_high():
    r = score_product(ROLLED_OATS)
    assert r.final_score >= 72


def test_salted_almonds_hp_relief():
    """Salted roasted almonds — HP near-miss but relief should activate."""
    r = score_product(WHOLE_FOOD_FAT_HP_NEAR_MISS)
    assert r.inferred_category == "whole_food_fat"
    # Despite high sodium, score should not collapse
    assert r.final_score >= 60


def test_whole_food_fat_floor_engages():
    """Floor rule should rescue calorie-dense whole foods."""
    r = score_product(OLIVE_OIL)
    floor_ids = [f["rule_id"] for f in r.guardrails.get("floors", [])]
    assert "WHOLE_FOOD_FAT_FLOOR" in floor_ids