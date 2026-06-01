"""
End-to-end scoring orchestration with:
  - Concern coordination (prevents double-counting same root concern)
  - Family-aware penalty clamping
  - Full audit trace
"""
from typing import Dict, Any, List, Tuple
from collections import defaultdict
from dataclasses import asdict

from bsip2_models import (
    FoodProduct, FoodAssessment, GuardrailResult, ScoringTrace, TriggeredRule, utc_now_iso,
)
from bsip2_config import (
    DIMENSION_WEIGHTS, GRADE_BANDS, ALGORITHM_VERSION, PENALTY_FAMILIES,
    CONFIDENCE_LOW_THRESHOLD, CONFIDENCE_INSUFFICIENT_THRESHOLD,
)
from bsip2_feature_extraction import extract_features
from bsip2_dimensions import calculate_dimensions
from bsip2_guardrails import apply_guardrails
from bsip2_concern_coordinator import coordinate_concerns   # ← NEW IMPORT


def grade_for(score: float) -> str:
    for threshold, grade in GRADE_BANDS:
        if score >= threshold:
            return grade
    return "E"


def confidence_band(c: float) -> str:
    if c < CONFIDENCE_INSUFFICIENT_THRESHOLD: return "INSUFFICIENT"
    if c < CONFIDENCE_LOW_THRESHOLD:          return "LOW"
    if c < 80:                                return "MEDIUM"
    return "HIGH"


def weighted_base_score(dimensions: Dict[str, float]) -> float:
    return sum(dimensions[k] * w for k, w in DIMENSION_WEIGHTS.items())


# ---------------------------------------------------------------------------
# FAMILY CLAMP HELPERS (unchanged from v0.3.0)
# ---------------------------------------------------------------------------
def _clamp_penalties_per_family(
    penalties: List[TriggeredRule]
) -> Tuple[List[TriggeredRule], Dict[str, float]]:
    by_family: Dict[str, List[TriggeredRule]] = defaultdict(list)
    for p in penalties:
        by_family[p.family].append(p)

    effective: List[TriggeredRule] = []
    family_totals: Dict[str, float] = {}

    for family, rules in by_family.items():
        budget = PENALTY_FAMILIES.get(family, PENALTY_FAMILIES["general"])["max_total_penalty"]
        raw_total = sum(r.value for r in rules)

        if raw_total <= budget:
            effective.extend(rules)
            family_totals[family] = raw_total
        else:
            scale = budget / raw_total
            for r in rules:
                effective.append(TriggeredRule(
                    rule_id=r.rule_id, rule_type=r.rule_type,
                    value=round(r.value * scale, 2),
                    rationale=r.rationale + f" (scaled to family budget: {scale:.2f}×)",
                    framework_ref=r.framework_ref, family=r.family,
                ))
            family_totals[family] = budget

    return effective, family_totals


def _apply_caps_per_family(
    caps: List[TriggeredRule], current_score: float
) -> Tuple[float, List[Tuple[TriggeredRule, float, float]], Dict[str, float]]:
    score = current_score
    log: List[Tuple[TriggeredRule, float, float]] = []
    family_effective_cap: Dict[str, float] = {}

    by_family: Dict[str, List[TriggeredRule]] = defaultdict(list)
    for c in caps:
        by_family[c.family].append(c)

    family_winning_caps: List[Tuple[str, TriggeredRule, float]] = []
    for family, rules in by_family.items():
        floor = PENALTY_FAMILIES.get(family, PENALTY_FAMILIES["general"])["cap_floor"]
        lowest = min(rules, key=lambda r: r.value)
        effective = max(lowest.value, floor)
        family_effective_cap[family] = effective
        family_winning_caps.append((family, lowest, effective))

    family_winning_caps.sort(key=lambda x: x[2])
    for family, rule, effective in family_winning_caps:
        if effective < score:
            log.append((rule, score, effective))
            score = effective
        else:
            log.append((rule, score, score))

    return score, log, family_effective_cap


# ---------------------------------------------------------------------------
# RESOLUTION PIPELINE  ← THIS IS WHAT CHANGED
# ---------------------------------------------------------------------------
def resolve_with_trace(
    base: float,
    g: GuardrailResult,
    confidence: float,
    features: Dict[str, Any],          # ← NEW PARAMETER
) -> Tuple[float, ScoringTrace, Dict[str, float], Dict[str, float], Dict[str, Any]]:
    #                                                                    ↑
    #                                              NEW RETURN: concern_audit
    """
    Returns (final_score, trace, family_penalty_totals, family_caps_applied, concern_audit).
    """
    trace = ScoringTrace(base_score=base)
    score = base

    # ─── Veto short-circuit ───
    if g.veto is not None:
        trace.add("VETO", g.veto.rule_id, score, g.veto.value, g.veto.rationale)
        trace.final_score = g.veto.value
        return g.veto.value, trace, {}, {}, {}   # ← 5 values now, not 4

    # ─── STEP 1: Concern coordination (NEW) ───
    # Same root concern fires across families? Pick winner, demote others.
    effective_caps, effective_penalties, concern_audit = coordinate_concerns(
        g.caps, g.penalties, features
    )

    # Log concern coordination decisions in trace
    for concern, info in concern_audit.get("concerns", {}).items():
        supporting = (info.get("cap_supporting", []) or []) + \
                     (info.get("penalty_supporting", []) or [])
        if supporting:
            winner = info.get("cap_winner") or info.get("penalty_winner") or "—"
            trace.add(
                step="CONCERN",
                rule_id=concern,
                before=score,
                after=score,
                rationale=f"Winner={winner}; supporting evidence (demoted): {supporting}",
            )

    # ─── STEP 2: Apply caps with family floor protection ───
    score, cap_log, family_cap_applied = _apply_caps_per_family(effective_caps, score)
    for rule, before, after in cap_log:
        if after < before:
            trace.add("CAP", f"{rule.rule_id} [{rule.family}]", before, after, rule.rationale)
        else:
            trace.add("CAP-noop", f"{rule.rule_id} [{rule.family}]", before, after,
                      "Cap not binding")

    # ─── STEP 3: Apply penalties with family clamp ───
    final_penalties, family_penalty_totals = _clamp_penalties_per_family(effective_penalties)
    for pen in final_penalties:
        new = max(0, score - pen.value)
        trace.add("PEN", f"{pen.rule_id} [{pen.family}]", score, new,
                  f"-{pen.value}: {pen.rationale}")
        score = new

    # ─── STEP 4: Floors ───
    if g.highest_floor is not None and g.highest_floor.value > score:
        floor = g.highest_floor
        trace.add("FLOOR", floor.rule_id, score, floor.value, floor.rationale)
        score = floor.value

    # ─── STEP 5: Confidence ceiling ───

    # Extremely weak / incomplete data
    if confidence < CONFIDENCE_INSUFFICIENT_THRESHOLD and score > 50:
        trace.add(
            "CONF-CAP",
            "INSUFFICIENT_CONFIDENCE_CAP",
            score,
            50,
            f"Confidence {confidence:.0f} → capped at 50"
        )
        score = 50

    # Low confidence
    elif confidence < CONFIDENCE_LOW_THRESHOLD and score > 70:
        trace.add(
            "CONF-CAP",
            "LOW_CONFIDENCE_CAP",
            score,
            70,
            f"Confidence {confidence:.0f} → capped at 70"
        )
        score = 70

    score = max(0, min(100, score))
    trace.final_score = score
    return score, trace, family_penalty_totals, family_cap_applied, concern_audit


def build_reasons(features, guardrails: GuardrailResult, hp_result: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
    pos: List[str] = []
    neg: List[str] = []
    codes: List[str] = []

    if features["protein_g_100g"] >= 12:
        pos.append("High protein density"); codes.append("HIGH_PROTEIN")
    if features["fiber_g_100g"] >= 6:
        pos.append("Good fiber density"); codes.append("GOOD_FIBER")
    if features["has_whole_food_marker"]:
        pos.append("Contains recognizable whole-food ingredients"); codes.append("WHOLE_FOOD_INGREDIENT")
    if features["red_label_count"] == 0:
        pos.append("No visible Israeli red warning labels"); codes.append("NO_RED_LABELS")
    if features["inferred_category"] == "whole_food_fat":
        pos.append("Whole-food fat (naturally calorie dense)")
        codes.append("CALORIE_DENSE_BUT_WHOLE_FOOD_FAT")
    if not hp_result["triggered_combos"]:
        pos.append("No engineered hyper-palatability combinations detected")

    if guardrails.veto:
        neg.append(f"VETO: {guardrails.veto.rationale}")
        codes.append(guardrails.veto.rule_id)
    for cap in guardrails.caps:
        neg.append(f"Cap @ {cap.value} [{cap.family}]: {cap.rationale}")
        codes.append(cap.rule_id)
    for pen in guardrails.penalties:
        neg.append(f"-{pen.value} [{pen.family}]: {pen.rationale}")
        codes.append(pen.rule_id)

    codes.extend(features.get("_calorie_reason_codes", []))
    codes.extend(hp_result.get("reason_codes", []))
    codes = list(dict.fromkeys(codes))
    return pos, neg, codes


# ---------------------------------------------------------------------------
# MAIN ENTRY POINT  ← THIS IS THE "CALL SITE" THAT ALSO CHANGED
# ---------------------------------------------------------------------------
def score_product(raw_product: Dict[str, Any]) -> FoodAssessment:
    product = FoodProduct(raw_product)
    features = extract_features(product)
    dims_obj = calculate_dimensions(features)

    # Run guardrails (this populates features["_hp_result"])
    guardrails = apply_guardrails(features)
    hp_result = features["_hp_result"]

    # Inject HP score into dimensions
    dims = {k: v for k, v in dims_obj.__dict__.items() if k != "confidence"}
    dims["hyper_palatability"] = round(hp_result["score"], 1)
    confidence = dims_obj.confidence

    base = weighted_base_score(dims)

    # ─── CALL SITE UPDATED ───
    # OLD: final, trace, family_pen, family_cap = resolve_with_trace(base, guardrails, confidence)
    # NEW: pass features + receive concern_audit
    final, trace, family_pen, family_cap, concern_audit = resolve_with_trace(
        base, guardrails, confidence, features
    )

    # Missing-data protection — apply AFTER final score is resolved,
    # but BEFORE grade/reasons/output object is created.
    confidence_flags = []

    if confidence < CONFIDENCE_INSUFFICIENT_THRESHOLD:
        before = final
        final = min(final, 50)
        confidence_flags.append("INSUFFICIENT_CONFIDENCE_SCORE_CAP_50")
        trace.add(
            step="CONF-CAP",
            rule_id="INSUFFICIENT_CONFIDENCE_SCORE_CAP_50",
            before=before,
            after=final,
            rationale=f"Confidence {confidence:.0f} below insufficient threshold → cap at 50"
        )

    elif confidence < CONFIDENCE_LOW_THRESHOLD:
        before = final
        final = min(final, 70)
        confidence_flags.append("LOW_CONFIDENCE_SCORE_CAP_70")
        trace.add(
            step="CONF-CAP",
            rule_id="LOW_CONFIDENCE_SCORE_CAP_70",
            before=before,
            after=final,
            rationale=f"Confidence {confidence:.0f} below low-confidence threshold → cap at 70"
        )

    reasons_pos, reasons_neg, codes = build_reasons(features, guardrails, hp_result)

    triggered_ids = (
        ([guardrails.veto.rule_id] if guardrails.veto else []) +
        [r.rule_id for r in guardrails.caps] +
        [r.rule_id for r in guardrails.penalties] +
        [r.rule_id for r in guardrails.floors]
    )

    return FoodAssessment(
        barcode=str(product.get("barcode", "")),
        product_name=str(product.get("product_name_he",
                                     product.get("product_name_heb",
                                                 product.get("product_name", "")))),
        inferred_category=features["inferred_category"],
        base_score=round(base, 1),
        final_score=round(final, 1),
        grade=grade_for(final),
        confidence=round(confidence, 1),
        confidence_band=confidence_band(confidence),
        dimensions={k: round(v, 1) for k, v in dims.items()},
        guardrails={
            "veto": asdict(guardrails.veto) if guardrails.veto else None,
            "caps": [asdict(r) for r in guardrails.caps],
            "lowest_cap": guardrails.lowest_cap.value if guardrails.lowest_cap else None,
            "penalties": [asdict(r) for r in guardrails.penalties],
            "total_penalty": guardrails.total_penalty,
            "floors": [asdict(r) for r in guardrails.floors],
            "highest_floor": guardrails.highest_floor.value if guardrails.highest_floor else None,
        },
        reasons_positive=reasons_pos,
        reasons_negative=reasons_neg,
        reason_codes=codes,
        triggered_rule_ids=triggered_ids,
        calorie_reason_codes=features.get("_calorie_reason_codes", []),
        calorie_caps_triggered=features.get("_calorie_caps_triggered", []),
        calorie_penalties_triggered=features.get("_calorie_penalties_triggered", []),
        hyper_palatability_score=round(hp_result["score"], 1),
        hyper_palatability_combos=hp_result["triggered_combos"],
        hyper_palatability_near_miss=hp_result["near_miss_combos"],
        family_penalties_applied=family_pen,
        family_caps_applied=family_cap,
        concern_audit=concern_audit,                   # ← NEW FIELD ON OUTPUT
        trace=[asdict(s) for s in trace.steps],
        algorithm_version=ALGORITHM_VERSION,
        input_hash=product.input_hash(),
        computed_at=utc_now_iso(),
    )