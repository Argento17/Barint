"""
BSIP2 Graceful Degradation Logic v1

Determines how BSIP2 output should be presented when data quality is
insufficient for a fully confident interpretation.

Degradation levels:
  FULL:         Normal score + grade. Information sufficient, routing stable.
  CAUTIOUS:     Score shown with confidence caveat. Grade shown as provisional.
                Applies when moderate gaps exist but scoring is still meaningful.
  UNCERTAINTY:  Score range instead of point score. Grade withheld or shown
                with prominent caveat. Applies when significant gaps exist.
  INSUFFICIENT: No score, no grade. Category + signal summary only.
                Applies when data is too sparse to produce a meaningful score.

Philosophy: the system should communicate uncertainty clearly and calmly,
not suppress all output. Even an UNCERTAINTY-level output should provide
the signals it CAN identify, so the analyst understands what was found.

Key rule: "When information quality drops, confidence should drop faster
than interpretive ambition."
"""

from __future__ import annotations
from constants import score_to_grade

DEGRADATION_LEVELS = {
    "FULL":         "Complete interpretation — score and grade are reliable",
    "CAUTIOUS":     "Partial interpretation — score usable, grade provisional",
    "UNCERTAINTY":  "Uncertain interpretation — score is a range, grade withheld",
    "INSUFFICIENT": "Insufficient data — score and grade cannot be assigned",
}


def determine_degradation_level(
    interpretation_conf: dict,
    score_result: dict,
    failures: list[dict],
) -> str:
    """
    Determine the degradation level for a product based on confidence and failures.
    Returns one of: FULL / CAUTIOUS / UNCERTAINTY / INSUFFICIENT
    """
    band = interpretation_conf.get("interpretation_confidence_band", "high")
    data_suf = score_result.get("data_sufficiency", "sufficient")

    # Hard rules for INSUFFICIENT
    if data_suf == "insufficient":
        return "INSUFFICIENT"
    if band == "insufficient_context":
        return "INSUFFICIENT"

    # Check for CRITICAL failures
    has_critical = any(f["severity"] == "CRITICAL" for f in failures)
    if has_critical:
        # CRITICAL: impossible data or missing everything → INSUFFICIENT
        crit_cats = {f["category"] for f in failures if f["severity"] == "CRITICAL"}
        if "MISSINGNESS" in crit_cats:
            return "INSUFFICIENT"
        if "RETAILER_INCONSISTENCY" in crit_cats:
            return "UNCERTAINTY"
        if "WEAK_SUPPRESSION" in crit_cats:
            return "UNCERTAINTY"

    # Supplement quarantine: product outside current food ontology — never FULL
    is_supplement = interpretation_conf.get("is_supplement_candidate", False)
    if is_supplement:
        return "UNCERTAINTY" if band in ("very_high", "high") else "INSUFFICIENT"

    # Band-driven degradation
    if band == "very_high":
        return "FULL"
    if band == "high":
        # High confidence but failures OR routing concern → cautious
        high_fails = [f for f in failures if f["severity"] in ("HIGH", "CRITICAL")]
        additional = interpretation_conf.get("additional_reductions", [])
        _ROUTING_CONCERN_KW = [
            "router_instability", "hybrid_routing", "anchor_secondary_tension",
            "supplement_candidate", "product_name_empty", "product_name_very_short",
            "product_name_short_no_anchor", "ingredient_text_absent",
        ]
        has_routing_concern = any(
            any(kw in r.get("factor", "") for kw in _ROUTING_CONCERN_KW)
            for r in additional
        )
        if high_fails or has_routing_concern:
            return "CAUTIOUS"
        return "FULL"
    if band == "moderate":
        return "CAUTIOUS"
    if band == "low":
        return "UNCERTAINTY"

    return "INSUFFICIENT"


def build_degraded_output(
    product: dict,
    score_result: dict,
    cat_result: dict,
    interpretation_conf: dict,
    failures: list[dict],
    degradation_level: str,
) -> dict:
    """
    Build the final consumer-facing output with appropriate degradation applied.

    Returns a dict with:
      - product_id, name
      - degradation_level
      - presented_score (or None)
      - score_range (for UNCERTAINTY level)
      - presented_grade (or None/provisional)
      - grade_is_provisional (bool)
      - interpretation_narrative
      - interpretation_cautions
      - available_signals (what we CAN say regardless of degradation)
      - failure_summary
    """
    pid   = product.get("canonical_product_id", "unknown")
    name  = product.get("canonical_name_he", "")
    brand = product.get("brand", "")
    cat   = cat_result.get("category", "unknown")

    raw_score = score_result.get("final_score_estimate")
    raw_grade = score_result.get("grade_estimate")

    # Apply interpretation_confidence score ceiling first
    ceiling = interpretation_conf.get("score_ceiling")
    if ceiling is not None and raw_score is not None:
        raw_score = min(raw_score, ceiling)
        raw_grade = score_to_grade(raw_score)

    ic_score = interpretation_conf.get("interpretation_confidence_score", 100)
    narrative = interpretation_conf.get("interpretation_narrative", "")
    cautions  = interpretation_conf.get("interpretation_cautions", [])

    # Available signals — what we can confidently state regardless of score validity
    available_signals = _extract_available_signals(product, score_result, cat_result)

    # Build output per degradation level
    if degradation_level == "FULL":
        return {
            "product_id":             pid,
            "name_he":                name,
            "brand":                  brand,
            "degradation_level":      "FULL",
            "presented_score":        raw_score,
            "score_range":            None,
            "presented_grade":        raw_grade,
            "grade_is_provisional":   False,
            "category":               cat,
            "interpretation_narrative": narrative,
            "interpretation_cautions": cautions,
            "available_signals":      available_signals,
            "confidence_score":       ic_score,
        }

    if degradation_level == "CAUTIOUS":
        return {
            "product_id":             pid,
            "name_he":                name,
            "brand":                  brand,
            "degradation_level":      "CAUTIOUS",
            "presented_score":        raw_score,
            "score_range":            _score_to_range(raw_score, width=8),
            "presented_grade":        raw_grade,
            "grade_is_provisional":   True,
            "category":               cat,
            "interpretation_narrative": narrative,
            "interpretation_cautions": cautions,
            "available_signals":      available_signals,
            "confidence_score":       ic_score,
        }

    if degradation_level == "UNCERTAINTY":
        score_range = _score_to_range(raw_score, width=15) if raw_score is not None else None
        # Widen grade to adjacent grades
        grade_range = _grade_to_range(raw_grade) if raw_grade else None
        return {
            "product_id":             pid,
            "name_he":                name,
            "brand":                  brand,
            "degradation_level":      "UNCERTAINTY",
            "presented_score":        None,
            "score_range":            score_range,
            "presented_grade":        None,
            "grade_range":            grade_range,
            "grade_is_provisional":   True,
            "category":               cat,
            "interpretation_narrative": narrative,
            "interpretation_cautions": cautions,
            "available_signals":      available_signals,
            "confidence_score":       ic_score,
        }

    # INSUFFICIENT
    return {
        "product_id":             pid,
        "name_he":                name,
        "brand":                  brand,
        "degradation_level":      "INSUFFICIENT",
        "presented_score":        None,
        "score_range":            None,
        "presented_grade":        None,
        "grade_is_provisional":   False,
        "category":               cat,
        "interpretation_narrative": narrative,
        "interpretation_cautions": cautions,
        "available_signals":      available_signals,
        "confidence_score":       ic_score,
    }


def _score_to_range(score: float | None, width: int = 10) -> dict | None:
    if score is None:
        return None
    lo = max(0.0, round(score - width / 2, 1))
    hi = min(100.0, round(score + width / 2, 1))
    return {"low": lo, "high": hi}


def _grade_to_range(grade: str | None) -> list[str] | None:
    """Return a list of grades this product could plausibly be given uncertainty."""
    if grade is None:
        return None
    order = ["A", "B", "C", "D", "E"]
    if grade not in order:
        return [grade]
    idx = order.index(grade)
    candidates = []
    if idx > 0:
        candidates.append(order[idx - 1])
    candidates.append(grade)
    if idx < len(order) - 1:
        candidates.append(order[idx + 1])
    return candidates


def _extract_available_signals(
    product: dict,
    score_result: dict,
    cat_result: dict,
) -> dict:
    """
    Extract what the system CAN reliably state even under high uncertainty.
    These are the factual anchors — always shown regardless of degradation level.
    """
    nn = product.get("normalized_nutrition_per_100g") or {}
    signals: dict = {}

    cat = cat_result.get("category", "unknown")
    cat_conf = cat_result.get("category_confidence", 0)
    if cat_conf >= 0.65:
        signals["category"] = cat
        signals["category_confidence"] = cat_conf

    caps = score_result.get("caps_applied", [])
    if caps:
        signals["guardrails_fired"] = [c["rule"] for c in caps]

    dim_scores = score_result.get("dimension_scores", {})
    if dim_scores:
        worst_k = min(dim_scores.items(), key=lambda x: x[1])
        best_k  = max(dim_scores.items(), key=lambda x: x[1])
        if worst_k[1] < 35:
            signals["clear_weakness"] = f"{worst_k[0]}={worst_k[1]:.0f}"
        if best_k[1] > 75:
            signals["clear_strength"] = f"{best_k[0]}={best_k[1]:.0f}"

    sugar = nn.get("sugars_g")
    if sugar is not None:
        signals["sugar_g_per_100g"] = sugar

    fiber = nn.get("dietary_fiber_g")
    if fiber is not None:
        signals["fiber_g_per_100g"] = fiber

    prot = nn.get("protein_g")
    if prot is not None:
        signals["protein_g_per_100g"] = prot

    if score_result.get("trans_fat_veto_applied"):
        signals["trans_fat_veto"] = True

    return signals
