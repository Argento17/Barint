"""
grade_governance.py — BARI_A_GRADE_INGREDIENT_FLOOR guard

Implements the A-grade ingredient observability floor approved in TASK-188
(Product ruling + Nutrition co-sign, 2026-06-05).

Rule: A product may only reach grade A if ALL three conditions are satisfied.
If ANY condition fails, grade is capped at B and score is capped at 75.

Condition 1 — Ingredient list observed:
    The product has a non-null, non-empty ingredient list.
    An empty string or empty list fails. A single-element list (e.g. ["שמן זית"])
    is valid — no minimum length check.

Condition 2 — Additive observability confirmed:
    The engine made an active determination on additive signals. If the trace
    signals that additive evaluation was skipped due to null/malformed ingredient
    list, this condition fails. Checks the trace field additive_observability_skipped
    (True = skipped = fail) or additive_evaluated (False = skipped = fail).

Condition 3 — Four core nutritional fields non-null:
    energy_kcal, protein_g, fat_g, carbohydrates_g must ALL be non-null.
    Implements the Nutrition co-sign clarification: check field values directly,
    NOT band labels (band labels conflict between interpretation_confidence.py
    and compute_confidence(); bypassing them avoids naming-mismatch bugs).

Cap rule: grade → 'B', score → min(score, 75).

Flag: BARI_A_GRADE_INGREDIENT_FLOOR (default ON).
Set to 'false'/'off'/'0' to disable (for comparison runs against pre-guard output).

Usage:
    from grade_governance import apply_a_grade_floor

    score, grade = apply_a_grade_floor(
        score=score_int,
        grade=grade_str,
        ingredients=ingredient_text_or_list,
        nutrition=dict_with_core_fields,      # keys: energy_kcal, protein_g, fat_g, carbohydrates_g
        trace=bsip2_trace_dict,               # optional; used for Condition 2
    )

The function is a pure transform — it does not write to any file or registry.
Callers are responsible for writing the returned values to the frontend JSON.

Evidence registry: EV-TASK-188 (TASK-188 Product ruling + Nutrition co-sign 2026-06-05).
"""
from __future__ import annotations

import os
from typing import Any

_ENV_KEY = "BARI_A_GRADE_INGREDIENT_FLOOR"
_CAP_SCORE = 75
_CAP_GRADE = "B"


def _flag_on() -> bool:
    """Return True unless the flag is explicitly disabled in the environment."""
    return os.environ.get(_ENV_KEY, "true").lower() not in ("false", "off", "0", "no")


def _condition1_ingredient_observed(ingredients: Any) -> bool:
    """
    Condition 1: ingredient list is non-null AND non-empty.

    Accepts:
    - str  : non-empty, non-whitespace string
    - list : non-empty list (single-element lists are valid per Nutrition co-sign §1)
    - None : fails
    - ""   : fails
    - []   : fails
    """
    if ingredients is None:
        return False
    if isinstance(ingredients, str):
        return bool(ingredients.strip())
    if isinstance(ingredients, (list, tuple)):
        # At least one non-empty element
        return any(str(item).strip() for item in ingredients)
    # Unexpected type — treat as unknown, fail closed
    return False


def _condition2_additive_observability(trace: dict | None) -> bool:
    """
    Condition 2: the engine made an active additive determination.

    Checks (in priority order):
    1. trace["additive_observability_skipped"] == True  → fail (explicitly flagged as skipped)
    2. trace["additive_evaluated"] == False             → fail (engine says it didn't run)
    3. L3_inferred_classifications["additive_skip"]     → fail if truthy
    4. If none of the above keys exist → pass (assume evaluated; condition is belt-and-
       suspenders for the case where an ingredient list exists but evaluation was skipped
       due to parse failure; if the engine does not emit skip signals, we don't penalise)
    """
    if trace is None:
        return True  # no trace data; cannot verify — pass (Condition 1 is the load-bearing check)

    # Explicit skip flags
    if trace.get("additive_observability_skipped") is True:
        return False
    if trace.get("additive_evaluated") is False:
        return False

    # L3 classification layer skip signal
    l3 = trace.get("L3_inferred_classifications") or {}
    if l3.get("additive_skip"):
        return False

    return True


def _condition3_core_nutrition_non_null(nutrition: dict | None) -> bool:
    """
    Condition 3: energy_kcal, protein_g, fat_g, carbohydrates_g are ALL non-null.

    Implements Nutrition co-sign clarification: check the four field values directly.
    Do NOT check band labels — naming conflicts between confidence layers make band
    labels unreliable as a proxy for this condition.

    The nutrition dict may come from different sources:
    - BSIP2 trace L1_observed_signals    → keys: energy_kcal, protein_g, fat_g, carbohydrates_g
    - BSIP1 normalized_nutrition_per_100g → same keys
    - BariNutritionVM (frontend shape)    → keys: energyKcal, protein, fat (no carbs)

    This function handles all three shapes:
    - Tries BSIP1/trace keys first
    - Falls back to VM keys for callers that only have the VM dict
    - If carbohydrates_g is absent from the VM dict, that field is treated as None
      (the VM omits it; a VM-only caller cannot satisfy Condition 3 for energy+protein
      unless they pass the raw nutrition dict instead — callers should prefer the raw dict)
    """
    if nutrition is None:
        return False

    def _get(d: dict, *keys) -> Any:
        for k in keys:
            v = d.get(k)
            if v is not None:
                return v
        return None

    energy = _get(nutrition, "energy_kcal", "energyKcal")
    protein = _get(nutrition, "protein_g", "protein")
    fat = _get(nutrition, "fat_g", "fat")
    carbs = _get(nutrition, "carbohydrates_g", "carbs")

    return (
        energy is not None
        and protein is not None
        and fat is not None
        and carbs is not None
    )


def apply_a_grade_floor(
    score: int | float | None,
    grade: str | None,
    ingredients: Any = None,
    nutrition: dict | None = None,
    trace: dict | None = None,
) -> tuple[int | float | None, str | None]:
    """
    Apply the BARI_A_GRADE_INGREDIENT_FLOOR guard.

    Returns (score, grade) — possibly capped if any condition fails.

    Args:
        score       : the engine score (int or float). Returned as-is if no cap needed.
        grade       : the engine grade string ('A', 'B', 'C', 'D', 'E'). If None, returned
                      as None (insufficient/unscored products are never capped).
        ingredients : ingredient text (str) or ingredient list (list[str]).
                      Pass whatever the builder has. None = not observed.
        nutrition   : dict with nutrition fields (BSIP1, trace L1, or VM shape).
                      Must contain energy_kcal, protein_g, fat_g, carbohydrates_g.
        trace       : full BSIP2 trace dict for Condition 2 check. Optional.

    Returns:
        (score, grade) — same values if guard is off or grade is not A,
                         or (min(score, 75), 'B') if any condition fails and grade == 'A'.
    """
    # Guard is off: return unchanged
    if not _flag_on():
        return score, grade

    # Only A-grade products are subject to this guard
    if grade != "A":
        return score, grade

    # Unscored products: not subject
    if score is None:
        return score, grade

    # Evaluate all three conditions
    c1 = _condition1_ingredient_observed(ingredients)
    c2 = _condition2_additive_observability(trace)
    c3 = _condition3_core_nutrition_non_null(nutrition)

    if c1 and c2 and c3:
        # All conditions pass: A is earned
        return score, grade

    # Any condition failed: cap grade at B, cap score at 75
    capped_score = min(score, _CAP_SCORE) if score is not None else None
    return capped_score, _CAP_GRADE


def floor_reasons(
    ingredients: Any = None,
    nutrition: dict | None = None,
    trace: dict | None = None,
) -> list[str]:
    """
    Return a list of human-readable reasons why the floor would fire.
    Empty list means the floor would NOT fire (all conditions pass).
    Useful for logging and run records.
    """
    reasons = []
    if not _condition1_ingredient_observed(ingredients):
        reasons.append("C1_FAIL: ingredient list absent or empty")
    if not _condition2_additive_observability(trace):
        reasons.append("C2_FAIL: additive evaluation was skipped (ingredient parse failure)")
    if not _condition3_core_nutrition_non_null(nutrition):
        reasons.append("C3_FAIL: one or more core nutrition fields null (energy/protein/fat/carbs)")
    return reasons
