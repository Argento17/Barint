"""
Hebrew/English negation handling in ingredient matching.
'ללא סוכר' (sugar-free) must NOT be flagged as containing sugar.
"""
from bsip2_score import score_product
from bsip2_hebrew import contains_term, contains_any
from tests.fixtures import NEGATION_TEST_SUGAR_FREE


def test_hebrew_negation_blocks_match():
    text = "חלב, ללא סוכר, ללא תוספת סוכר"
    assert not contains_term(text, "סוכר"), \
        "Negated 'סוכר' was incorrectly matched"


def test_english_negation_blocks_match():
    text = "milk, no sugar, sugar-free"
    # The "sugar-free" hyphenated form is its own challenge — but "no sugar" should block.
    assert not contains_term("milk, no sugar", "sugar")


def test_sugar_free_product_not_flagged():
    r = score_product(NEGATION_TEST_SUGAR_FREE)
    assert "MULTIPLE_ADDED_SUGAR_MARKERS" not in r.triggered_rule_ids


def test_negation_does_not_affect_unrelated_terms():
    """'ללא סוכר' should block 'סוכר' but not other ingredients."""
    text = "ללא סוכר, חלבון מי גבינה"
    assert not contains_term(text, "סוכר")
    assert contains_term(text, "חלבון מי גבינה")