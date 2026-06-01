"""
BSIP2 Sprint 1 — Score Engine v2

Modified scoring functions for approved Group A findings:
  EV-012  fat_quality_v2          (ratio-based fat scoring, fat_g >= 8.0 guard)
  EV-003  emulsifier_tier_model   (uses sprint1_additive_count from signal_extractor_v2)
  EV-004  allulose_adjusted_sugar (conservative glycemic adjustment)
  EV-005  polyol_laxative_penalty (graduated penalty for polyol accumulation)

Architecture: imports all v1 functions and overrides only the changed ones.
The v1 functions remain available as score_fat_quality_v1, score_glycemic_quality_v1, etc.
Rollback: replace import of score_engine_v2 with score_engine to restore v1 behavior.
"""

import sys
import pathlib

_SRC = pathlib.Path(__file__).resolve().parent.parent / "proto_v0" / "src"
sys.path.insert(0, str(_SRC))

# Import everything from v1 — we override only what changes
from score_engine import (
    compute_confidence,
    score_processing_quality,
    score_nutrient_density,
    score_calorie_density,
    score_protein_quality,
    score_satiety_support,
    score_regulatory_quality,
    score_whole_food_integrity,
    detect_structural_emptiness,
    evaluate_guardrails,
    apply_floors,
    _identify_drivers,
    _collect_flags,
    _coordinate_family,
    _classify_sugar_context,
    # Keep v1 fat/glycemic/additive under alias for audit comparison
    score_fat_quality    as score_fat_quality_v1,
    score_glycemic_quality as score_glycemic_quality_v1,
    score_additive_quality as score_additive_quality_v1,
)
from constants import (
    DIMENSION_WEIGHTS, lookup_calorie_density,
    NOVA_HP_WEIGHTS, NOVA_WFI_SCORES, NOVA_PROCESSING_SCORES,
    SWEETENER_CAP_A, SWEETENER_CAP_B, SWEETENER_CAP_C,
    SWEETENER_PENALTY_A, SWEETENER_PENALTY_B, SWEETENER_PENALTY_C,
    TRANS_FAT_VETO_THRESHOLD, NOVA1_SINGLE_FLOOR, WHOLE_FOOD_FAT_FLOOR,
    PHYSIO_MODERATION_MIN, PHYSIO_2PLUS_LABELS_MIN,
    CONFIDENCE_INSUFFICIENT_CEILING, CONFIDENCE_LOW_CEILING,
    SE_KCAL_THRESHOLD, SE_BEVERAGE_KCAL, SE_PROTEIN_THRESHOLD,
    SE_FIBER_THRESHOLD, SE_FAT_THRESHOLD,
    HP_FAT_SUGAR_FAT_PCT, HP_FAT_SUGAR_SUGAR_G,
    HP_FAT_SODIUM_FAT_PCT, HP_FAT_SODIUM_SODIUM_G,
    HP_CRUNCH_SWEET_SUGAR, HP_CRUNCH_SWEET_FIBER,
    HP_FAT_SUGAR_PENALTY, HP_FAT_SODIUM_PENALTY, HP_CRUNCH_SWEET_PENALTY,
    HP_FAMILY_BUDGET, SUGAR_FAMILY_BUDGET, CALORIE_FAMILY_BUDGET,
    PROCESSING_FAMILY_BUDGET, SODIUM_FAMILY_BUDGET, FAT_QUALITY_FAMILY_BUDGET,
    RELATIVE_PENALTY_FACTOR_HIGH, RELATIVE_PENALTY_FACTOR_LOW,
    ABSOLUTE_SCORE_FLOOR, GRADE_E_FLOOR_STANDARD,
    CAT_CONF_HIGH, CAT_CONF_MEDIUM, CAT_MEDIUM_THRESHOLD_RELAX,
    PROCESSING_CAPS, FERMENTATION_DIRECT_BONUS,
    score_to_grade,
)

# ---------------------------------------------------------------------------
# Sprint 1 constants
# ---------------------------------------------------------------------------

FAT_RATIO_GUARD = 8.0        # EV-012: fat_g threshold to activate ratio logic

# EV-005: Polyol laxative penalty tiers
POLYOL_PENALTY_SINGLE   = 4   # 1 polyol type: mild flag
POLYOL_PENALTY_MULTIPLE = 10  # 2+ polyol types: stronger flag
POLYOL_PENALTY_KETO     = 15  # 2+ polyols in keto/sugar-free product

# EV-004: Allulose sugar penalty reduction factor (conservative)
ALLULOSE_SUGAR_REDUCTION = 0.30  # Reduce sugar_penalty by 30% when allulose present


# ---------------------------------------------------------------------------
# EV-012: fat_quality_v2
# ---------------------------------------------------------------------------

def _ratio_to_fat_score(ratio: float) -> float:
    """
    Piecewise linear mapping from unsaturated/saturated ratio to fat quality score.

    Calibration anchors (ratio → score):
      0.00 → 10  (entirely saturated, e.g. pure coconut fat)
      0.25 → 25  (heavy palm/coconut oil, e.g. most industrial chocolate coatings)
      0.50 → 40  (majority saturated, moderate unsaturated)
      1.00 → 55  (equal sat/unsat — nutritionally borderline)
      2.00 → 70  (2x more unsat than sat — Heart-healthy zone)
      3.50 → 83  (very good lipid profile, e.g. olive-oil dominant)
      6.00 → 93  (excellent — tahini, almond butter, natural nut butters)
    """
    breakpoints = [
        (0.00, 10.0),
        (0.25, 25.0),
        (0.50, 40.0),
        (1.00, 55.0),
        (2.00, 70.0),
        (3.50, 83.0),
        (6.00, 93.0),
    ]
    if ratio <= breakpoints[0][0]:
        return breakpoints[0][1]
    if ratio >= breakpoints[-1][0]:
        return breakpoints[-1][1]
    for i in range(len(breakpoints) - 1):
        lo_r, lo_s = breakpoints[i]
        hi_r, hi_s = breakpoints[i + 1]
        if ratio <= hi_r:
            t = (ratio - lo_r) / (hi_r - lo_r)
            return lo_s + t * (hi_s - lo_s)
    return 93.0


def score_fat_quality_v2(nn: dict, l3: dict, se_result: dict) -> tuple[float, str]:
    """
    EV-012: fat_quality_v2

    Guard: activates ratio logic only when fat_g >= FAT_RATIO_GUARD (8.0g).
    Below guard: uses v1 formula (absolute sat fat) unchanged.
    Above guard: uses unsaturated/saturated ratio → piecewise linear score.

    Both v1 and v2 formulas apply the same trans fat and seed oil adjustments.
    """
    fat   = nn.get("fat_g") or 0
    sat_f = nn.get("fat_saturated_g")
    has_seed_oil = l3.get("has_seed_oil", False)

    if fat < 0.5 or se_result.get("structurally_empty"):
        return 50.0, "SRC-04: fat < 0.5g or structurally empty → neutral 50"
    if sat_f is None:
        return 50.0, "sat_fat absent → neutral 50"

    # Shared adjustments (same as v1)
    trans_status = l3.get("trans_fat_status", "not_detected")
    if trans_status in ("veto", "high_concern"):
        trans_pen = 20
    elif trans_status == "present":
        trans_pen = 10
    else:
        trans_pen = 0
    seed_pen = 10 if has_seed_oil else 0

    if fat >= FAT_RATIO_GUARD and sat_f > 0:
        # EV-012 ratio path
        unsat_fat = max(0.0, fat - sat_f)
        ratio = unsat_fat / sat_f
        base = _ratio_to_fat_score(ratio)
        score = round(max(0.0, base - seed_pen - trans_pen), 1)
        note = (
            f"EV-012 fat_quality_v2: fat={fat}g≥{FAT_RATIO_GUARD} "
            f"ratio={ratio:.3f} (unsat={unsat_fat:.1f}/sat={sat_f}) "
            f"→ base={base:.1f} - seed_pen={seed_pen} - trans_pen={trans_pen} = {score}"
        )
    else:
        # Below guard: v1 formula preserved exactly
        sat_frac = sat_f / fat if fat > 0 else 0
        base = max(0.0, 100.0 - sat_f * 3.0 - sat_frac * 25)
        score = round(max(0.0, base - seed_pen - trans_pen), 1)
        note = (
            f"fat_quality_v1 (fat={fat}g<{FAT_RATIO_GUARD}): "
            f"sat_fat={sat_f}g frac={sat_frac:.2f} base={base:.1f} "
            f"- seed_pen={seed_pen} - trans_pen={trans_pen} = {score}"
        )

    return score, note


# ---------------------------------------------------------------------------
# EV-004: score_glycemic_quality_v2
# ---------------------------------------------------------------------------

def score_glycemic_quality_v2(nn: dict, l3: dict) -> tuple[float, str]:
    """
    EV-004: Allulose-adjusted glycemic quality.

    When allulose is detected, reduces the sugar penalty component by
    ALLULOSE_SUGAR_REDUCTION (30%). This is conservative:
    - No calorie recalculation
    - No sugar elimination
    - Only reduces the penalty exposure from declared sugars
    - Rationale: allulose is a declared carbohydrate but not metabolically active
    """
    sugar = nn.get("sugars_g") or 0
    fiber = nn.get("dietary_fiber_g") or 0
    has_whole_grain = l3.get("has_whole_grain", False)
    has_sweetener   = l3.get("sweetener_detected", False)
    allulose_detected = l3.get("sprint1_allulose_detected", False)

    sugar_penalty = min(80, sugar * 2.5)
    fiber_bonus   = min(20, fiber * 2.0)
    wg_bonus      = 5 if has_whole_grain else 0

    allulose_note = ""
    if allulose_detected:
        original_penalty = sugar_penalty
        sugar_penalty = round(sugar_penalty * (1 - ALLULOSE_SUGAR_REDUCTION), 1)
        allulose_note = (f" [EV-004: allulose detected → sugar_penalty "
                        f"{original_penalty:.1f}×{1-ALLULOSE_SUGAR_REDUCTION:.0%}"
                        f"={sugar_penalty:.1f}]")

    sw_tier_val = l3.get("sweetener_tier")
    sw_note = (f" (sweetener tier-{sw_tier_val})" if sw_tier_val else "")

    raw = 90 - sugar_penalty + fiber_bonus + wg_bonus
    score = round(max(0, min(100, raw)), 1)
    note = (f"90 - sugar_penalty({sugar_penalty:.1f}) + fiber_bonus({fiber_bonus:.1f}) "
            f"+ wg_bonus({wg_bonus}) = {raw:.1f}{allulose_note}{sw_note}")
    return score, note


# ---------------------------------------------------------------------------
# EV-003: score_additive_quality_v2
# ---------------------------------------------------------------------------

def score_additive_quality_v2(l3: dict) -> tuple[float, str]:
    """
    EV-003/019: Uses sprint1_additive_count (corrected count after emulsifier tier adjustments).

    sprint1_additive_count reflects:
    - Lecithin-only emulsifier removed from count (-1 if sole emulsifier reason)
    - Prebiotic gum removed from stabilizer count (-1 if sole stabilizer reason)
    - High-risk emulsifier detected adds +2 to count

    Scoring formula is otherwise identical to v1.
    """
    # Use corrected count if available, fall back to v1 count
    ac = l3.get("sprint1_additive_count", l3.get("additive_marker_count", 0))
    ac_v1 = l3.get("additive_marker_count", 0)
    sw_tier = l3.get("sweetener_tier")
    _tier_penalties = {"A": SWEETENER_PENALTY_A, "B": SWEETENER_PENALTY_B, "C": SWEETENER_PENALTY_C}
    sw_pen = _tier_penalties.get(sw_tier, 0)
    base = max(0, 100 - ac * 18)
    score = round(max(0, base - sw_pen), 1)
    tier_note = f" tier-{sw_tier}" if sw_tier else ""

    correction = l3.get("sprint1_additive_correction", 0)
    correction_str = f" [EV-003/019: v1_count={ac_v1}→sprint1_count={ac} (correction={correction:+d})]" if correction != 0 else ""

    return score, (f"sprint1_additive_count={ac} → base={base}, "
                   f"sweetener{tier_note}_penalty={sw_pen} → {score}{correction_str}")


# ---------------------------------------------------------------------------
# EV-005: polyol_laxative_penalty
# ---------------------------------------------------------------------------

def compute_polyol_penalty(l3: dict, product_name: str = "") -> tuple[float, str]:
    """
    EV-005: Graduated penalty for polyol accumulation.

    Humectant refinement (TASK-046B):
      Polyols declared within a manufacturer-labelled humectant group
      ("חומרי הלחה (גליצרול, סורביטול)") are functional moisture-retention
      agents, not sweetener loads.  They are excluded from the penalty count.
      sprint1_penalty_polyol_count carries only scoring-relevant polyols.

    Single penalty polyol  → POLYOL_PENALTY_SINGLE (4 pts)
    2+ penalty polyols     → POLYOL_PENALTY_MULTIPLE (10 pts)
    2+ polyols in keto/sugar-free context → POLYOL_PENALTY_KETO (15 pts)
    """
    # Use penalty count (excludes humectant-declared polyols) with graceful fallback
    polyol_count     = l3.get("sprint1_penalty_polyol_count",
                              l3.get("sprint1_polyol_count", 0))
    detected_polyols = l3.get("sprint1_penalty_polyols",
                              l3.get("sprint1_detected_polyols", []))
    humectant_polyols = l3.get("sprint1_humectant_polyols", [])

    if polyol_count == 0:
        if humectant_polyols:
            return 0.0, (
                f"EV-005: polyols in humectant group only — no penalty "
                f"({', '.join(humectant_polyols)} declared as חומרי הלחה)"
            )
        return 0.0, "EV-005: no polyols detected"

    # Check for keto/sugar-free product context
    name_lower = product_name.lower()
    keto_context = any(t in name_lower for t in [
        "keto", "קטו", "sugar free", "ללא סוכר", "0% סוכר", "sugar-free",
        "slim", "דייט", "diet",
    ])
    sw_tier = l3.get("sweetener_tier")
    keto_context = keto_context or (sw_tier in ("A", "B") and polyol_count >= 2)

    if polyol_count >= 2 and keto_context:
        penalty = POLYOL_PENALTY_KETO
        label = "strongest"
    elif polyol_count >= 2:
        penalty = POLYOL_PENALTY_MULTIPLE
        label = "multiple"
    else:
        penalty = POLYOL_PENALTY_SINGLE
        label = "single"

    humectant_note = (f" [humectant-exempt: {', '.join(humectant_polyols)}]"
                      if humectant_polyols else "")
    note = (f"EV-005: {polyol_count} penalty polyol(s) ({', '.join(detected_polyols)})"
            f"{humectant_note} → {label} laxative risk penalty = -{penalty}")
    return float(penalty), note


# ---------------------------------------------------------------------------
# Main score function (v2)
# ---------------------------------------------------------------------------

def score_product(product: dict, signals: dict, cat_result: dict,
                  nova_result: dict, eval_result: dict) -> dict:
    """
    Sprint 1 scoring pipeline.

    Changes from v1:
    - score_fat_quality → score_fat_quality_v2   (EV-012)
    - score_glycemic_quality → score_glycemic_quality_v2  (EV-004)
    - score_additive_quality → score_additive_quality_v2  (EV-003/019)
    - polyol_laxative_penalty applied post-cap  (EV-005)
    """
    pid = product.get("canonical_product_id", "unknown")
    nn  = product.get("normalized_nutrition_per_100g") or {}

    l1 = signals["L1_observed_signals"]
    l3 = signals["L3_inferred_classifications"]

    l3["fat_pct_of_kcal"] = signals["L2_derived_signals"].get("fat_pct_of_kcal") or 0
    l3["ingredient_list"] = l1.get("ingredient_list") or []

    category   = cat_result["category"]
    cat_conf   = cat_result["category_confidence"]
    nova_level = nova_result["nova_level"]
    nova_conf  = nova_result["nova_confidence"]
    red_label_ct = l3.get("red_label_count", 0)
    has_fermentation = l3.get("has_fermentation", False)
    has_fortification = l3.get("has_fortification", False)

    # Stage 0: Out of scope gate
    if eval_result.get("evaluation_status") == "out_of_scope":
        return {
            "product_id": pid,
            "evaluation_status": "out_of_scope",
            "final_score_estimate": None,
            "grade_estimate": None,
        }

    # Stage 1: Confidence
    conf_result = compute_confidence(product, signals, cat_result, nova_result)
    confidence  = conf_result["confidence_score"]

    # Stage 2: Structural emptiness
    se_result = detect_structural_emptiness(nn, category, l3)

    # Dimension scoring — Sprint 1 overrides
    pq_score,  pq_note  = score_processing_quality(nova_level)
    nd_score,  nd_note  = score_nutrient_density(nn, has_fortification)
    cd_score,  cd_note  = score_calorie_density(nn, category, cat_conf, se_result)
    gq_score,  gq_note  = score_glycemic_quality_v2(nn, l3)        # EV-004
    prq_score, prq_note = score_protein_quality(nn, l3)
    aq_score,  aq_note  = score_additive_quality_v2(l3)             # EV-003/019
    ss_score,  ss_note  = score_satiety_support(nn)
    fq_score,  fq_note  = score_fat_quality_v2(nn, l3, se_result)   # EV-012
    rq_score,  rq_note  = score_regulatory_quality(l3)
    wfi_score, wfi_note = score_whole_food_integrity(nova_level, l1.get("ingredient_count", 0), has_fermentation)

    dim_scores = {
        "processing_quality":   pq_score,
        "nutrient_density":     nd_score,
        "calorie_density":      cd_score,
        "glycemic_quality":     gq_score,
        "protein_quality":      prq_score,
        "additive_quality":     aq_score,
        "satiety_support":      ss_score,
        "fat_quality":          fq_score,
        "regulatory_quality":   rq_score,
        "whole_food_integrity": wfi_score,
    }
    dim_notes = {
        "processing_quality": pq_note, "nutrient_density": nd_note,
        "calorie_density": cd_note, "glycemic_quality": gq_note,
        "protein_quality": prq_note, "additive_quality": aq_note,
        "satiety_support": ss_note, "fat_quality": fq_note,
        "regulatory_quality": rq_note, "whole_food_integrity": wfi_note,
    }

    weighted_sum = sum(dim_scores[k] * DIMENSION_WEIGHTS[k] for k in dim_scores)
    weighted_dim_score = round(weighted_sum, 2)

    # R-02: fermentation bonus (unchanged from v1)
    fermentation_bonus = 0
    if has_fermentation and nova_level <= 3:
        fermentation_bonus = FERMENTATION_DIRECT_BONUS
        weighted_dim_score = round(min(100, weighted_dim_score + fermentation_bonus), 2)

    # Guardrails (unchanged from v1)
    gr = evaluate_guardrails(nn, l3, nova_level, category, cat_conf, eval_result)

    if gr.get("trans_fat_veto"):
        return {
            "product_id": pid,
            "evaluation_status": eval_result["evaluation_status"],
            "trans_fat_veto_applied": True,
            "final_score_estimate": 0,
            "grade_estimate": "E",
            "dimension_scores": dim_scores,
            "guardrail_result": gr,
            "confidence_result": conf_result,
            "sprint1_signals": _get_sprint1_summary(l3),
        }

    # Cap application
    binding_cap = gr.get("binding_cap")
    score_after_cap = min(weighted_dim_score, binding_cap) if binding_cap is not None else weighted_dim_score

    # Relative penalty scaling
    total_pen = gr.get("total_coordinated_penalty", 0)
    penalty_factor = RELATIVE_PENALTY_FACTOR_LOW if score_after_cap < 30 else RELATIVE_PENALTY_FACTOR_HIGH
    max_relative_pen = score_after_cap * penalty_factor
    scaled_penalty = round(min(total_pen, max_relative_pen), 2)

    # EV-005: Polyol penalty applied POST-cap (safety signal, not a nutritional quality signal)
    product_name = (product.get("canonical_name_he") or product.get("product_name_he") or "")
    polyol_penalty, polyol_note = compute_polyol_penalty(l3, product_name)

    score_after_penalty = round(score_after_cap - scaled_penalty - polyol_penalty, 2)
    score_after_penalty = max(ABSOLUTE_SCORE_FLOOR, score_after_penalty)

    # Floor application
    floor_result = apply_floors(score_after_penalty, nova_level, nova_conf, category, gr, red_label_ct)
    score_after_floors = floor_result["final_score_after_floors"]

    # Confidence ceiling
    ceiling = conf_result.get("confidence_ceiling")
    if ceiling is not None and score_after_floors > ceiling:
        final_score = ceiling
    else:
        final_score = score_after_floors

    final_score = round(final_score, 1)
    grade = score_to_grade(final_score)

    is_insufficient = (confidence < 40 or eval_result.get("context_flag") == "no_nutrition_data")
    if is_insufficient:
        data_sufficiency = "insufficient"
        grade = "insufficient_data"
    else:
        data_sufficiency = "sufficient"

    try:
        drivers = _identify_drivers(gr, floor_result, conf_result, dim_scores, binding_cap, ceiling)
    except Exception:
        drivers = []
    try:
        flags = _collect_flags(product, signals, cat_result, nova_result, gr, floor_result,
                                se_result, eval_result)
    except Exception:
        flags = []

    return {
        "product_id": pid,
        "evaluation_status": eval_result["evaluation_status"],
        "context_flag": eval_result.get("context_flag"),
        "structural_emptiness_result": se_result,
        "confidence_result": conf_result,
        "dimension_scores": dim_scores,
        "dimension_notes": dim_notes,
        "dimension_weights": DIMENSION_WEIGHTS,
        "weighted_dimension_score": weighted_dim_score,
        "fermentation_bonus_applied": fermentation_bonus if fermentation_bonus else None,
        "caps_applied": gr.get("caps_applied", []),
        "binding_cap": binding_cap,
        "score_after_cap": round(score_after_cap, 2),
        "total_coordinated_penalty": total_pen,
        "scaled_penalty": scaled_penalty,
        "polyol_penalty": polyol_penalty,
        "polyol_penalty_note": polyol_note if polyol_penalty > 0 else None,
        "score_after_penalty": round(score_after_penalty, 2),
        "floor_result": floor_result,
        "confidence_ceiling": ceiling,
        "final_score_estimate": final_score,
        "grade_estimate": grade,
        "data_sufficiency": data_sufficiency,
        "explanation_drivers": drivers,
        "unresolved_flags": flags,
        "sprint1_signals": _get_sprint1_summary(l3),
        "nova_proxy": nova_result.get("nova_level"),
        "category": category,
        "input_reference": {
            "canonical_product_id": product.get("canonical_product_id"),
            "canonical_name_he": product.get("canonical_name_he"),
            "product_name_he": product.get("product_name_he"),
            "brand": product.get("brand"),
        },
    }


def _get_sprint1_summary(l3: dict) -> dict:
    """Extract Sprint 1 signal summary for comparison reporting."""
    return {
        "high_risk_emulsifier":    l3.get("sprint1_high_risk_emulsifier_detected", False),
        "neutral_emulsifier":      l3.get("sprint1_neutral_emulsifier_detected", False),
        "prebiotic_gum":           l3.get("sprint1_prebiotic_gum_detected", False),
        "additive_correction":     l3.get("sprint1_additive_correction", 0),
        "sprint1_additive_count":  l3.get("sprint1_additive_count"),
        "v1_additive_count":       l3.get("additive_marker_count"),
        "allulose_detected":       l3.get("sprint1_allulose_detected", False),
        "polyol_count":            l3.get("sprint1_polyol_count", 0),          # total (audit)
        "detected_polyols":        l3.get("sprint1_detected_polyols", []),
        "humectant_polyols":       l3.get("sprint1_humectant_polyols", []),    # excluded
        "penalty_polyol_count":    l3.get("sprint1_penalty_polyol_count", 0), # scored
        "penalty_polyols":         l3.get("sprint1_penalty_polyols", []),
    }


