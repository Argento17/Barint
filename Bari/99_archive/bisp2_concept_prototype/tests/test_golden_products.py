"""
Golden product tests — end-to-end pipeline validation.
If any of these break, do not ship.
"""
import pytest
from bsip2_score import score_product
from tests.fixtures import ALL_PRODUCTS, EXPECTATIONS


@pytest.mark.parametrize("name", list(EXPECTATIONS.keys()))
def test_golden_product_matches_expectation(name):
    raw = ALL_PRODUCTS[name]
    exp = EXPECTATIONS[name]
    result = score_product(raw)

    msg_prefix = f"[{name}] score={result.final_score} grade={result.grade}"

    if "min_score" in exp:
        assert result.final_score >= exp["min_score"], \
            f"{msg_prefix} expected ≥{exp['min_score']}"
    if "max_score" in exp:
        assert result.final_score <= exp["max_score"], \
            f"{msg_prefix} expected ≤{exp['max_score']}"
    if "expected_grade" in exp:
        assert result.grade in exp["expected_grade"], \
            f"{msg_prefix} expected grade in {exp['expected_grade']}"
    if "category" in exp:
        assert result.inferred_category == exp["category"], \
            f"{msg_prefix} expected category {exp['category']}, got {result.inferred_category}"
    if "max_confidence" in exp:
        assert result.confidence <= exp["max_confidence"], \
            f"{msg_prefix} expected confidence ≤{exp['max_confidence']}, got {result.confidence}"


def test_score_is_in_valid_range():
    """No product should ever score outside [0, 100]."""
    for name, raw in ALL_PRODUCTS.items():
        r = score_product(raw)
        assert 0 <= r.final_score <= 100, f"{name}: score {r.final_score} out of range"
        assert 0 <= r.base_score <= 100, f"{name}: base {r.base_score} out of range"


def test_grade_consistency_with_score():
    """Grade must match the GRADE_BANDS thresholds for the score."""
    from bsip2_config import GRADE_BANDS
    for name, raw in ALL_PRODUCTS.items():
        r = score_product(raw)
        expected_grade = next(g for thr, g in GRADE_BANDS if r.final_score >= thr)
        assert r.grade == expected_grade, \
            f"{name}: score {r.final_score} → expected {expected_grade}, got {r.grade}"


def test_output_has_required_fields():
    """Every assessment must have all schema fields populated."""
    r = score_product(ALL_PRODUCTS["RAW_ALMONDS"])
    required = [
        "barcode", "product_name", "inferred_category", "base_score",
        "final_score", "grade", "confidence", "confidence_band",
        "dimensions", "guardrails", "reasons_positive", "reasons_negative",
        "reason_codes", "triggered_rule_ids", "trace",
        "algorithm_version", "input_hash", "computed_at",
        "hyper_palatability_score", "hyper_palatability_combos",
        "family_penalties_applied", "family_caps_applied",
    ]
    for field in required:
        assert hasattr(r, field), f"Missing required field: {field}"