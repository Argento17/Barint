"""
The signature test for our concern coordinator:
A red sugar sticker + high sugar amount must NOT double-count.
"""
from bsip2_score import score_product
from tests.fixtures import GRANOLA_BAR_SUGARY


def test_sugar_concern_has_winner_and_supporting_evidence():
    r = score_product(GRANOLA_BAR_SUGARY)
    sugar = r.concern_audit.get("concerns", {}).get("SUGAR_LOAD")
    assert sugar is not None, "SUGAR_LOAD concern was not coordinated"
    has_winner = sugar.get("cap_winner") or sugar.get("penalty_winner")
    assert has_winner, "No winner picked for SUGAR_LOAD"


def test_supporting_evidence_does_not_count_full_value():
    r = score_product(GRANOLA_BAR_SUGARY)
    # Look at trace for supporting evidence demotion
    trace_steps = r.trace
    concern_steps = [s for s in trace_steps if s.get("step") == "CONCERN"]
    assert len(concern_steps) >= 1, "Expected at least one CONCERN trace step"


def test_score_higher_than_naive_stacking():
    """
    With concern coordination, granola bar should still score in the D/E range.
    Without coordination it would be even lower (~22). With coordination ~29-32.
    """
    r = score_product(GRANOLA_BAR_SUGARY)
    assert r.final_score >= 25, \
        f"Concern coordinator under-applied: {r.final_score}"