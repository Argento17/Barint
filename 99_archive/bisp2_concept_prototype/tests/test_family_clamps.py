"""
Family budget clamps — bound damage per concern category.
"""
from bsip2_score import score_product
from tests.fixtures import EXTREME_SUGAR_BOMB, GRANOLA_BAR_SUGARY


def test_sugar_family_clamp_at_budget():
    """Even with 7 sugar markers, family penalty must not exceed budget."""
    r = score_product(EXTREME_SUGAR_BOMB)
    sugar_pen = r.family_penalties_applied.get("sugar", 0)
    from bsip2_config import PENALTY_FAMILIES
    budget = PENALTY_FAMILIES["sugar"]["max_total_penalty"]
    assert sugar_pen <= budget + 0.01, \
        f"Sugar family exceeded budget {budget}: got {sugar_pen}"


def test_family_cap_floor_protects_score():
    """A regulatory cap can't push score below the family's cap_floor."""
    r = score_product(GRANOLA_BAR_SUGARY)
    from bsip2_config import PENALTY_FAMILIES
    # Regulatory cap_floor protects against impossibly low caps
    floor = PENALTY_FAMILIES["regulatory"]["cap_floor"]
    if "regulatory" in r.family_caps_applied:
        assert r.family_caps_applied["regulatory"] >= floor


def test_total_penalty_bounded():
    """Sum of all family penalties should be bounded by sum of all family budgets."""
    r = score_product(GRANOLA_BAR_SUGARY)
    from bsip2_config import PENALTY_FAMILIES
    total_applied = sum(r.family_penalties_applied.values())
    max_possible = sum(f["max_total_penalty"] for f in PENALTY_FAMILIES.values())
    assert total_applied <= max_possible