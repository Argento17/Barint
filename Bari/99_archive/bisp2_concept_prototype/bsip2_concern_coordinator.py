"""
Concern Coordinator: prevents double-counting same root concern.
"""
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from bsip2_config import CONCERNS, CONTEXT_AWARE_CONCERN_MAPPING
from bsip2_models import TriggeredRule


def _resolve_concern(rule, features):
    if rule.rule_id in CONTEXT_AWARE_CONCERN_MAPPING:
        mapping = CONTEXT_AWARE_CONCERN_MAPPING[rule.rule_id]["concern_when"]
        for feature_key, concern in mapping.items():
            if features.get(feature_key) is True:
                return concern
        return ""
    for concern, cfg in CONCERNS.items():
        if rule.rule_id in cfg["rules"]:
            return concern
    return ""


def coordinate_concerns(caps, penalties, features):
    audit = {"concerns": {}}

    # ===== CAPS =====
    caps_by_concern = defaultdict(list)
    uncategorized_caps = []
    for cap in caps:
        concern = _resolve_concern(cap, features)
        if concern:
            caps_by_concern[concern].append(cap)
        else:
            uncategorized_caps.append(cap)

    effective_caps = list(uncategorized_caps)
    for concern, rules in caps_by_concern.items():
        winner = min(rules, key=lambda r: r.value)
        effective_caps.append(winner)
        supporting = [r for r in rules if r is not winner]
        audit["concerns"][concern] = {
            "cap_winner": winner.rule_id,
            "cap_winner_value": winner.value,
            "cap_supporting": [r.rule_id for r in supporting],
        }

    # ===== PENALTIES =====
    pens_by_concern = defaultdict(list)
    uncategorized_pens = []
    for pen in penalties:
        concern = _resolve_concern(pen, features)
        if concern:
            pens_by_concern[concern].append(pen)
        else:
            uncategorized_pens.append(pen)

    effective_penalties = list(uncategorized_pens)

    for concern, rules in pens_by_concern.items():
        winner = max(rules, key=lambda r: r.value)
        factor = CONCERNS.get(concern, {}).get("supporting_evidence_factor", 0.5)

        effective_penalties.append(winner)

        for r in rules:
            if r is winner:
                continue
            scaled = TriggeredRule(
                rule_id=r.rule_id,
                rule_type=r.rule_type,
                value=round(r.value * factor, 2),
                rationale=r.rationale + " (supporting evidence)",
                framework_ref=r.framework_ref,
                family=r.family,
            )
            effective_penalties.append(scaled)

        existing = audit["concerns"].get(concern, {})
        existing.update({
            "penalty_winner": winner.rule_id,
            "penalty_winner_value": winner.value,
            "penalty_supporting": [r.rule_id for r in rules if r is not winner],
            "supporting_factor": factor,
        })
        audit["concerns"][concern] = existing

    return effective_caps, effective_penalties, audit