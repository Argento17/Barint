"""
Concern coordinator — prevents double-counting same root concern.
"""
from bsip2_concern_coordinator import coordinate_concerns
from bsip2_models import TriggeredRule


def _make_rule(rule_id, rule_type, value, family="general"):
    return TriggeredRule(
        rule_id=rule_id, rule_type=rule_type, value=value,
        rationale=f"Test rule {rule_id}", family=family,
    )


def test_sugar_concern_picks_strongest_cap():
    caps = [
        _make_rule("HIGH_SUGAR_25G_PLUS", "cap", 60, "sugar"),
        _make_rule("ISRAELI_RED_LABEL_1", "cap", 55, "regulatory"),
    ]
    features = {"red_label_sugar": True}
    eff_caps, _, audit = coordinate_concerns(caps, [], features)

    sugar_audit = audit["concerns"]["SUGAR_LOAD"]
    assert sugar_audit["cap_winner"] == "ISRAELI_RED_LABEL_1"
    assert "HIGH_SUGAR_25G_PLUS" in sugar_audit["cap_supporting"]


def test_supporting_evidence_demoted_in_penalty():
    penalties = [
        _make_rule("MULTIPLE_ADDED_SUGAR_MARKERS", "penalty", 5, "sugar"),
        _make_rule("HIGH_CAL_HIGH_SUGAR_SOFT", "penalty", 5, "calorie_density"),
        _make_rule("HP_FAT_SUGAR_COMBO", "penalty", 5, "hyper_palatability"),
    ]
    _, eff_penalties, audit = coordinate_concerns([], penalties, {})

    sugar = audit["concerns"]["SUGAR_LOAD"]
    assert sugar["penalty_winner"] in [p.rule_id for p in penalties]
    assert len(sugar["penalty_supporting"]) == 2

    total = sum(p.value for p in eff_penalties if p.rule_type == "penalty")
    assert 5 + (5 * 0.4) + (5 * 0.4) == round(total, 1)

def test_red_label_routes_to_correct_concern():
    """ISRAELI_RED_LABEL_1 should attach to whatever concern its sticker is for."""
    cap = _make_rule("ISRAELI_RED_LABEL_1", "cap", 55, "regulatory")

    # When red label is for sugar
    features_sugar = {"red_label_sugar": True}
    _, _, audit_s = coordinate_concerns([cap], [], features_sugar)
    assert "SUGAR_LOAD" in audit_s["concerns"]

    # When red label is for sodium
    features_sodium = {"red_label_sodium": True}
    _, _, audit_n = coordinate_concerns([cap], [], features_sodium)
    assert "SODIUM_LOAD" in audit_n["concerns"]


def test_uncategorized_rules_pass_through_unchanged():
    rule = _make_rule("CUSTOM_UNKNOWN_RULE", "penalty", 7, "general")
    _, eff_penalties, audit = coordinate_concerns([], [rule], {})
    assert any(p.rule_id == "CUSTOM_UNKNOWN_RULE" for p in eff_penalties)
    assert audit["concerns"] == {}
