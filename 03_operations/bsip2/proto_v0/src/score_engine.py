"""
BSIP2 Prototype v0 — Score Engine
Implements score_resolution_contract.md (SRC-v1) + bsip2_concept_v1 specification.
All formulas are preliminary. This is a diagnostic prototype, not a calibrated scorer.
Every intermediate value is retained for the trace.
"""
import math
import os
from constants import (
    DIMENSION_WEIGHTS, CALORIE_DENSITY_TABLES, lookup_calorie_density,
    NOVA_PROCESSING_SCORES, NOVA_WFI_SCORES, NOVA_HP_WEIGHTS,
    RED_LABEL_THRESHOLDS,
    SWEETENER_CAP_A, SWEETENER_CAP_B, SWEETENER_CAP_C,
    SWEETENER_PENALTY_A, SWEETENER_PENALTY_B, SWEETENER_PENALTY_C,
    TRANS_FAT_VETO_THRESHOLD, TRANS_FAT_HIGH_THRESHOLD,
    NOVA1_SINGLE_FLOOR, WHOLE_FOOD_FAT_FLOOR,
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
    PROTEIN_QUALITY_MATRIX_DISCOUNT, PROTEIN_MATRIX_DISCOUNT_BAR_CATEGORIES,
    ADDITIVE_IDENTITY_DELTAS, BHA_NAMED_PENALTY,
    FIBER_NOT_APPLICABLE_CATEGORIES,
    PROTEIN_SCALE_TABLES, lookup_protein_scale,
    RECAL_P0_FIBER_NOT_APPLICABLE, NOVA_DEMOTE_BLOCKING_ADDITIVE_CATS,
    VEG_SPREAD_WEIGHTS, VEG_SPREAD_IMMUNITY_CEILING,
    CULTURED_YOGURT_SUBTYPES, CULTURED_CHEESE_NAME_MARKERS_HE,
    FLUID_MILK_NAME_MARKERS_HE, DAIRY_SOLID_IDENTITY_MARKERS_HE,
    FLAVORED_VARIANT_MARKERS_HE,
    RED_LABEL_THRESHOLDS as _RED_LABEL_THRESHOLDS,
    score_to_grade,
)

# TASK-144 — same activation toggle as signal_extractor; gates Fix 2 (fiber-not-applicable).
# DEFAULT OFF (frozen behavior). Only the maadanim batch runner opts in via
# BARI_TASK144_FIXES=on. See signal_extractor.py for the full activation-scope rationale.
TASK144_FIXES_ON = os.environ.get("BARI_TASK144_FIXES", "off").lower() == "on"

# TASK-169 P0 — single rollback flag for ALL recalibration changes (R1–R7).
# DEFAULT OFF → engine byte-identical to 0.4.1 (safety contract + regression guard).
# Source of truth: 01_framework/bsip2_framework/recalibration_p0_design_v1.md.
RECAL_P0_ON = os.environ.get("BARI_RECAL_P0", "off").lower() == "on"


# ---------------------------------------------------------------------------
# Confidence calculation
# ---------------------------------------------------------------------------

def compute_confidence(product: dict, signals: dict, cat_result: dict, nova_result: dict) -> dict:
    """Compute BSIP2 confidence score (0-100) from multiple factors."""
    score = 100
    reductions = []

    nn = product.get("normalized_nutrition_per_100g") or {}
    l1 = signals["L1_observed_signals"]

    def deduct(amount, reason):
        nonlocal score
        score -= amount
        reductions.append({"factor": reason, "reduction": -amount})

    # Missing nutrition fields
    missing_map = {
        "energy_kcal": 10, "protein_g": 10, "carbohydrates_g": 10,
        "fat_g": 10, "dietary_fiber_g": 5, "sodium_mg": 5,
    }
    for field, penalty in missing_map.items():
        if nn.get(field) is None:
            deduct(penalty, f"missing: {field}")

    # Missing ingredients
    if not product.get("ingredients_list"):
        deduct(25, "missing: ingredient_list")
    elif product.get("ingredient_text_quality") in ("corrupted", "malformed"):
        deduct(10, f"ingredient_quality={product.get('ingredient_text_quality')}")

    # Data consistency failures
    checks = l1.get("consistency_checks", {})
    if checks.get("sugar_le_carbs") is False:
        deduct(20, "sugar > carbohydrates (data integrity failure)")
    if checks.get("satfat_le_fat") is False:
        deduct(20, "sat_fat > fat (data integrity failure)")
    if checks.get("kcal_plausible") is False:
        deduct(10, "energy_kcal outside plausible range 20-700")
    # TASK-144 — implausible macros (e.g. protein_g=190/100g from an OCR parse error)
    # are a hard data-integrity failure; deduct heavily so the product is flagged
    # insufficient_data rather than producing a spurious score/grade. Gated to the
    # TASK-144 activation scope so frozen-category outputs stay byte-identical; the
    # consistency flag itself is always computed (observable) and surfaced for any
    # cross-category data-integrity follow-up.
    if TASK144_FIXES_ON and checks.get("macros_plausible") is False:
        deduct(40, "macro values implausible per 100g (data integrity failure)")

    # BSIP1 trust level
    trust_level = product.get("canonical_trust_level") or "unknown"
    if trust_level == "low":
        deduct(10, "bsip1_trust_level=low")
    elif trust_level == "medium":
        deduct(5, "bsip1_trust_level=medium")

    # Nutrition consistency warnings from BSIP1
    if product.get("nutrition_consistency_status") == "suspicious":
        deduct(20, "bsip1_nutrition_consistency=suspicious (possible per-serving confusion)")
    elif product.get("nutrition_consistency_status") == "warnings":
        deduct(10, "bsip1_nutrition_consistency=warnings (cross-retailer disagreement)")

    # NOVA confidence
    if nova_result.get("nova_confidence_band") == "low":
        deduct(10, "nova_confidence=low")
    elif nova_result.get("nova_confidence_band") == "medium":
        deduct(5, "nova_confidence=medium")

    # Category confidence
    cat_conf = cat_result.get("category_confidence", 0.5)
    if cat_conf < CAT_CONF_MEDIUM:
        deduct(15, f"category_confidence=low ({cat_conf:.2f})")
    elif cat_conf < CAT_CONF_HIGH:
        deduct(8, f"category_confidence=medium ({cat_conf:.2f})")

    score = max(0, score)

    if score >= 80:
        band = "high"
        ceiling = None
    elif score >= 60:
        band = "medium"
        ceiling = None
    elif score >= 40:
        band = "low"
        ceiling = CONFIDENCE_LOW_CEILING
    else:
        band = "insufficient"
        ceiling = CONFIDENCE_INSUFFICIENT_CEILING

    return {
        "confidence_score": score,
        "confidence_band": band,
        "confidence_ceiling": ceiling,
        "confidence_reductions": reductions,
    }


# ---------------------------------------------------------------------------
# Structural emptiness gate (SRC-04)
# ---------------------------------------------------------------------------

def detect_structural_emptiness(nn: dict, category: str, l3: dict) -> dict:
    kcal  = nn.get("energy_kcal") or 0
    prot  = nn.get("protein_g") or 0
    fiber = nn.get("dietary_fiber_g") or 0
    fat   = nn.get("fat_g") or 0
    has_sw = l3.get("sweetener_detected", False)
    add_ct = l3.get("additive_marker_count", 0)

    thresh = SE_BEVERAGE_KCAL if category == "beverage" else SE_KCAL_THRESHOLD

    cond_kcal  = kcal < thresh
    cond_prot  = prot < SE_PROTEIN_THRESHOLD
    cond_fiber = fiber < SE_FIBER_THRESHOLD
    cond_fat   = fat < SE_FAT_THRESHOLD
    cond_eng   = has_sw or add_ct >= 2

    is_empty = cond_kcal and cond_prot and cond_fiber and cond_fat and cond_eng

    return {
        "structurally_empty": is_empty,
        "se_conditions": {
            "kcal_below_threshold": cond_kcal,
            "protein_below_threshold": cond_prot,
            "fiber_below_threshold": cond_fiber,
            "fat_below_threshold": cond_fat,
            "engineered_signal_present": cond_eng,
        },
        "se_note": ("SRC-04: calorie density dimension capped at 50; fat quality returns neutral 50" if is_empty else None),
    }


# ---------------------------------------------------------------------------
# Dimension scoring (prototype formulas — preliminary calibration)
# ---------------------------------------------------------------------------

def score_processing_quality(nova_level: int) -> tuple[float, str]:
    score = NOVA_PROCESSING_SCORES.get(nova_level, 50)
    return score, f"NOVA {nova_level} → processing_quality={score} (NOVA_PROCESSING_SCORES table)"


def score_nutrient_density(nn: dict, has_fortification: bool = False,
                           category: str = None) -> tuple[float, str]:
    prot  = nn.get("protein_g") or 0
    fiber_raw = nn.get("dietary_fiber_g")
    fiber = fiber_raw or 0
    # R1 — category-relative protein mass scale. Flag OFF → legacy supplement curve
    # (byte-identical via lookup_protein_scale's recal_on=False branch).
    def prot_score(g):
        return lookup_protein_scale(g, category, RECAL_P0_ON)
    def fiber_score(g):
        bps = [(0,0),(1,10),(2,20),(4,40),(6,55),(8,68),(10,78),(12,95)]  # R-03 ceiling 85→95
        for i in range(len(bps)-1):
            lo_g, lo_s = bps[i]; hi_g, hi_s = bps[i+1]
            if g <= hi_g:
                t = (g - lo_g) / (hi_g - lo_g) if hi_g > lo_g else 0
                return lo_s + t * (hi_s - lo_s)
        return 95
    ps = prot_score(prot)

    # TASK-144 Fix 2 / EV-027 — fiber "absent ≠ zero" for naturally fiber-free dairy.
    # TIGHTLY GATED: only when (a) the category is on the explicit fiber-not-applicable
    # allowlist AND (b) fiber is genuinely absent or ~0 in this product. In that case the
    # dimension is scored on PROTEIN ALONE (re-normalize 65/35 → 100/0) rather than
    # blending in a structural-zero fiber. Bread/cereal/bars/etc. are NOT on the allowlist
    # and keep the flat 65/35 blend (missing fiber there IS a real deficiency).
    # R2 — OR in BARI_RECAL_P0 so cheese (dairy_protein, already allowlisted) inherits the
    # EV-027 fiber-not-applicable path. Maadanim behaviour via BARI_TASK144_FIXES unchanged.
    fiber_not_applicable = (
        (TASK144_FIXES_ON or RECAL_P0_ON)
        and category in FIBER_NOT_APPLICABLE_CATEGORIES
        and (fiber_raw is None or fiber_raw <= 0)
    )
    if fiber_not_applicable:
        raw = round(ps, 1)
        na_note = (f"protein={prot}g→{ps:.1f}; fiber not-applicable for category "
                   f"'{category}' (EV-027: protein-only, 65/35→100/0) → {raw}")
        if has_fortification:
            score = round(raw * 0.80, 1)
            return score, na_note + f" × 0.80 fortification_discount → {score}"
        return raw, na_note

    fs = fiber_score(fiber)
    raw = round(0.65 * ps + 0.35 * fs, 1)
    if has_fortification:
        score = round(raw * 0.80, 1)
        return score, f"protein={prot}g→{ps:.1f}, fiber={fiber}g→{fs:.1f}, weighted 65/35={raw} × 0.80 fortification_discount → {score}"
    return raw, f"protein={prot}g→{ps:.1f}, fiber={fiber}g→{fs:.1f}, weighted 65/35={raw}"


def score_calorie_density(nn: dict, category: str, cat_confidence: float, se_result: dict) -> tuple[float, str]:
    kcal = nn.get("energy_kcal")
    if kcal is None:
        return 50.0, "energy_kcal absent: neutral 50"
    if se_result.get("structurally_empty"):
        return 50.0, f"SRC-04 structural emptiness gate: cap at 50 (raw kcal={kcal})"

    # SRC-07: relax threshold 10% at medium confidence
    if cat_confidence < CAT_CONF_HIGH:
        # Use slightly more generous table — same table but threshold scaled
        relax = 1 + CAT_MEDIUM_THRESHOLD_RELAX if cat_confidence < CAT_CONF_MEDIUM else 1.05
        adj_kcal = kcal / relax  # divide kcal so it falls into a better tier
        score = lookup_calorie_density(adj_kcal, category)
        return float(score), f"kcal={kcal}, category={category} (conf {cat_confidence:.2f}, relaxed by {relax:.2f}x) → {score}"
    score = lookup_calorie_density(kcal, category)
    return float(score), f"kcal={kcal}, category={category} → {score}"


# ---------------------------------------------------------------------------
# Sprint 1 — production scoring additions
# EV-012 fat ratio, EV-004 allulose, EV-003/019 additive tier, EV-005 polyol
# ---------------------------------------------------------------------------

_FAT_RATIO_GUARD        = 8.0   # EV-012: activate ratio path when fat_g >= this
_POLYOL_PENALTY_SINGLE  = 4     # EV-005: 1 penalty polyol
_POLYOL_PENALTY_MULTI   = 10    # EV-005: 2+ penalty polyols
_POLYOL_PENALTY_KETO    = 15    # EV-005: 2+ polyols in keto/sugar-free product
_ALLULOSE_SUGAR_REDUCE  = 0.30  # EV-004: reduce sugar_penalty by 30% when allulose present


def _fat_ratio_to_score(ratio: float) -> float:
    """EV-012 piecewise linear map: unsaturated/saturated ratio → fat quality score."""
    bps = [(0.00,10.0),(0.25,25.0),(0.50,40.0),(1.00,55.0),(2.00,70.0),(3.50,83.0),(6.00,93.0)]
    if ratio <= bps[0][0]:  return bps[0][1]
    if ratio >= bps[-1][0]: return bps[-1][1]
    for i in range(len(bps)-1):
        lo_r, lo_s = bps[i]; hi_r, hi_s = bps[i+1]
        if ratio <= hi_r:
            t = (ratio - lo_r) / (hi_r - lo_r)
            return lo_s + t * (hi_s - lo_s)
    return 93.0


# R3 — leanness reward (TASK-169 / EV-030). A genuinely lean whole-food matrix earns
# positive fat_quality credit rather than the legacy neutral-50 default. Gated by
# BARI_RECAL_P0; with the flag OFF the neutral-50 short-circuits are unchanged.
def _leanness_score(fat, sat_f):
    sat = sat_f or 0.0
    base = 92 - (fat or 0.0) * 6.0   # 0g→92, 1g→86, 2g→80, 3g→74
    base -= sat * 4.0                # mild sat-fat haircut: 0.6g → -2.4
    return round(max(50.0, min(95.0, base)), 1)


# R5 — graded saturated-fat penalty (TASK-169 / EV-031). Replaces the composite
# ISRAELI_RED_LABEL_1_SAT_FAT cliff cap with a fat-dimension penalty scaled to how far
# over the 5.0g/100g red-label threshold the product sits. regulatory_quality STILL
# counts the red label (signal not lost). Gated by BARI_RECAL_P0.
def _red_satfat_penalty(sat_f):
    thr = _RED_LABEL_THRESHOLDS["sat_fat"]
    if sat_f is None or sat_f <= thr:
        return 0.0
    excess = sat_f - thr
    return round(min(25.0, 3.0 + excess * 2.5), 1)   # 5g→0, 6g→5.5, 8g→10.5, 12g→20.5, cap 25


def _score_fat_quality_sprint1(nn: dict, l3: dict, se_result: dict) -> tuple:
    """EV-012: ratio-based fat quality. Falls back to v1 when fat_g < guard."""
    fat   = nn.get("fat_g") or 0
    sat_f = nn.get("fat_saturated_g")
    has_seed_oil = l3.get("has_seed_oil", False)
    if fat < 0.5 or se_result.get("structurally_empty"):
        if RECAL_P0_ON and not se_result.get("structurally_empty"):
            # R3: genuinely lean (incl. stranded sat_fat=None) → treat sat as 0
            ls = _leanness_score(fat, sat_f)
            return ls, f"R3 leanness: fat={fat}g (<0.5) sat={sat_f} → {ls}"
        return 50.0, "SRC-04: fat < 0.5g or structurally empty → neutral 50"
    if sat_f is None:
        if RECAL_P0_ON:
            ls = _leanness_score(fat, 0.0)
            return ls, f"R3 leanness: fat={fat}g sat_fat absent (treated 0) → {ls}"
        return 50.0, "sat_fat absent → neutral 50"
    trans_status = l3.get("trans_fat_status", "not_detected")
    trans_pen = 20 if trans_status in ("veto","high_concern") else (10 if trans_status=="present" else 0)
    seed_pen  = 10 if has_seed_oil else 0
    # R5 — graded red-label sat-fat penalty on the fat dimension (replaces the composite
    # cliff cap, which guardrails stops firing under RECAL_P0). 0 at/below 5.0g threshold.
    red_pen = _red_satfat_penalty(sat_f) if RECAL_P0_ON else 0.0
    if fat >= _FAT_RATIO_GUARD and sat_f > 0:
        ratio = max(0.0, fat - sat_f) / sat_f
        base  = _fat_ratio_to_score(ratio)
        score = round(max(0.0, base - seed_pen - trans_pen - red_pen), 1)
        note  = (f"EV-012 fat_ratio: fat={fat}g ratio={ratio:.3f}"
                 f" base={base:.1f}-seed{seed_pen}-trans{trans_pen}"
                 f"{('-red%.1f' % red_pen) if red_pen else ''}={score}")
    else:
        sat_frac = sat_f / fat if fat > 0 else 0
        base  = max(0.0, 100 - sat_f * 3.0 - sat_frac * 25)
        score = round(max(0.0, base - seed_pen - trans_pen - red_pen), 1)
        # R3 — leanness floor in the lean band (fat <= 3g): never worse than penalty curve.
        if RECAL_P0_ON and fat <= 3.0:
            ls = _leanness_score(fat, sat_f)
            if ls > score:
                note = (f"R3 leanness band: max(penalty_curve={score}, leanness={ls}) "
                        f"(fat={fat}g sat={sat_f}g)")
                score = ls
                return score, note
        note  = (f"fat_v1(fat={fat}g<{_FAT_RATIO_GUARD}): sat={sat_f}g"
                 f" base={base:.1f}-seed{seed_pen}-trans{trans_pen}"
                 f"{('-red%.1f' % red_pen) if red_pen else ''}={score}")
    return score, note


def _score_glycemic_quality_sprint1(nn: dict, l3: dict) -> tuple:
    """EV-004: allulose-adjusted glycemic quality."""
    sugar = nn.get("sugars_g") or 0
    fiber = nn.get("dietary_fiber_g") or 0
    has_whole_grain   = l3.get("has_whole_grain", False)
    allulose_detected = l3.get("sprint1_allulose_detected", False)
    sugar_penalty = min(80, sugar * 2.5)
    fiber_bonus   = min(20, fiber * 2.0)
    wg_bonus      = 5 if has_whole_grain else 0
    allulose_note = ""
    if allulose_detected:
        orig = sugar_penalty
        sugar_penalty = round(sugar_penalty * (1 - _ALLULOSE_SUGAR_REDUCE), 1)
        allulose_note = f" [EV-004 allulose: penalty {orig:.1f}→{sugar_penalty:.1f}]"
    sw_tier_val = l3.get("sweetener_tier")
    sw_note = (f" (sweetener tier-{sw_tier_val})" if sw_tier_val else "")
    raw = 90 - sugar_penalty + fiber_bonus + wg_bonus
    score = round(max(0, min(100, raw)), 1)
    note  = (f"90 - sugar_penalty({sugar_penalty:.1f}) + fiber({fiber_bonus:.1f})"
             f" + wg({wg_bonus}) = {raw:.1f}{allulose_note}{sw_note}")
    return score, note


def _identity_additive_deltas(l3: dict) -> tuple[float, list[str]]:
    """TASK-133 F1/F4 — per-identity point deltas on the additive_quality dimension.

    Consumes the TASK-133A taxonomy identity (carrageenan/CMC vs lecithin, native
    vs modified starch, BHA vs BHT). F1 emulsifier/starch deltas default to NEUTRAL
    (DEC-004 — directions are already live via the EV-003 sprint1 count correction;
    setting them non-zero now would double-count). F4's BHA named penalty is a
    genuinely new, non-double-counting signal (distinct from the generic
    antioxidant-category count BHA shares with BHT and benign tocopherol).
    Returns (signed_delta, notes).
    """
    delta = 0.0
    notes: list[str] = []

    # F1 — emulsifier identity (DEC-004-gated; default 0 to avoid double-count)
    concern = l3.get("tax_emulsifier_concern") or []
    if concern and ADDITIVE_IDENTITY_DELTAS["emulsifier_concern_each"]:
        d = max(-ADDITIVE_IDENTITY_DELTAS["emulsifier_concern_cap"],
                -len(concern) * ADDITIVE_IDENTITY_DELTAS["emulsifier_concern_each"])
        delta += d
        notes.append(f"F1 emulsifier_concern {concern} → {d:+.0f}")
    if (l3.get("tax_emulsifier_benign")) and ADDITIVE_IDENTITY_DELTAS["lecithin_relief"]:
        delta += ADDITIVE_IDENTITY_DELTAS["lecithin_relief"]
        notes.append(f"F1 lecithin relief +{ADDITIVE_IDENTITY_DELTAS['lecithin_relief']}")
    if l3.get("tax_native_starch") and ADDITIVE_IDENTITY_DELTAS["native_starch_relief"]:
        delta += ADDITIVE_IDENTITY_DELTAS["native_starch_relief"]
        notes.append(f"F1 native-starch relief +{ADDITIVE_IDENTITY_DELTAS['native_starch_relief']}")

    # F4 — BHA named penalty (BHT explicitly excluded)
    if l3.get("tax_bha_present"):
        delta -= BHA_NAMED_PENALTY
        notes.append(f"F4 BHA (E320) named penalty −{BHA_NAMED_PENALTY} "
                     f"(FDA reassessment active 2026-02-10; BHT differentiated)")
    return delta, notes


def _score_additive_quality_sprint1(l3: dict) -> tuple:
    """EV-003/019: uses sprint1_additive_count (emulsifier/gum tier corrections).
    TASK-133 F1/F4: applies per-identity point deltas on top (taxonomy identity)."""
    ac    = l3.get("sprint1_additive_count", l3.get("additive_marker_count", 0))
    ac_v1 = l3.get("additive_marker_count", 0)
    sw_tier = l3.get("sweetener_tier")
    _tier_penalties = {"A": SWEETENER_PENALTY_A, "B": SWEETENER_PENALTY_B, "C": SWEETENER_PENALTY_C}
    sw_pen = _tier_penalties.get(sw_tier, 0)
    base  = max(0, 100 - ac * 18)
    id_delta, id_notes = _identity_additive_deltas(l3)
    score = round(max(0, min(100, base - sw_pen + id_delta)), 1)
    tier_note = f" tier-{sw_tier}" if sw_tier else ""
    corr = l3.get("sprint1_additive_correction", 0)
    corr_note = (f" [EV-003/019: v1={ac_v1}→sprint1={ac} (Δ={corr:+d})]" if corr != 0 else "")
    id_note = (f" [{'; '.join(id_notes)}]" if id_notes else "")
    return score, (f"sprint1_additives={ac} base={base} sw{tier_note}_pen={sw_pen}"
                   f"{(' id_delta=%+.0f' % id_delta) if id_delta else ''}→{score}{corr_note}{id_note}")


def _compute_polyol_penalty(l3: dict, product_name: str = "") -> tuple:
    """EV-005: graduated penalty — humectant-declared polyols excluded."""
    polyol_count  = l3.get("sprint1_penalty_polyol_count",
                           l3.get("sprint1_polyol_count", 0))
    pen_polyols   = l3.get("sprint1_penalty_polyols",
                           l3.get("sprint1_detected_polyols", []))
    hum_polyols   = l3.get("sprint1_humectant_polyols", [])
    if polyol_count == 0:
        if hum_polyols:
            return 0.0, (f"EV-005: humectant-only polyols — no penalty"
                         f" ({', '.join(hum_polyols)})")
        return 0.0, "EV-005: no polyols detected"
    name_lower = product_name.lower()
    keto = any(t in name_lower for t in
               ["keto","קטו","sugar free","ללא סוכר","0% סוכר","sugar-free","slim","דייט","diet"])
    sw_tier = l3.get("sweetener_tier")
    keto = keto or (sw_tier in ("A","B") and polyol_count >= 2)
    if polyol_count >= 2 and keto:
        penalty, label = _POLYOL_PENALTY_KETO, "keto/strong"
    elif polyol_count >= 2:
        penalty, label = _POLYOL_PENALTY_MULTI, "multiple"
    else:
        penalty, label = _POLYOL_PENALTY_SINGLE, "single"
    hum_note = (f" [humectant-exempt: {', '.join(hum_polyols)}]" if hum_polyols else "")
    note = (f"EV-005: {polyol_count} penalty polyol(s) ({', '.join(pen_polyols)})"
            f"{hum_note} → {label} penalty = -{penalty}")
    return float(penalty), note


def score_glycemic_quality(nn: dict, l3: dict) -> tuple[float, str]:
    sugar = nn.get("sugars_g") or 0
    fiber = nn.get("dietary_fiber_g") or 0
    has_whole_grain = l3.get("has_whole_grain", False)
    has_sweetener   = l3.get("sweetener_detected", False)

    # Base: start at 90 and penalize sugar
    sugar_penalty = min(80, sugar * 2.5)
    fiber_bonus   = min(20, fiber * 2.0)
    wg_bonus      = 5 if has_whole_grain else 0
    # Sweetener: glycemic signal is low because no real sugar, but SWEETENER cap handles ceiling
    sw_tier_val = l3.get("sweetener_tier")
    _sw_cap_val = {"A": 75, "B": 73, "C": 70}.get(sw_tier_val, 70)
    sw_note = f" (sweetener tier-{sw_tier_val} present; glycemic score reflects low sugar, but sweetener cap={_sw_cap_val} applies)" if sw_tier_val else ""

    raw = 90 - sugar_penalty + fiber_bonus + wg_bonus
    score = round(max(0, min(100, raw)), 1)
    note = f"90 - sugar_penalty({sugar_penalty:.1f}) + fiber_bonus({fiber_bonus:.1f}) + wg_bonus({wg_bonus}) = {raw:.1f}"
    if has_sweetener:
        note += sw_note
    return score, note


def score_protein_quality(nn: dict, l3: dict, category: str = None) -> tuple[float, str]:
    prot = nn.get("protein_g") or 0
    source = l3.get("protein_source", "unknown")
    # TASK-144 Fix 3 / EV-028 — "dairy" = complete, high-DIAAS dairy protein (factor 1.0).
    # Distinct from "mixed" (0.85), which remains for genuinely blended/uncertain sources.
    source_factors = {"whole_food": 1.0, "dairy": 1.0, "mixed": 0.85, "isolate": 0.70, "unknown": 0.80}
    sf = source_factors.get(source, 0.80)

    # R1 — category-relative protein mass scale (flag OFF → legacy supplement curve).
    base = lookup_protein_scale(prot, category, RECAL_P0_ON)
    quality = base * sf

    # F2 / TASK-133B — matrix discount on the protein-QUALITY contribution only.
    # Protein MASS is untouched (satiety_support + nutrient_density read protein_g
    # directly). DEC-004 gates the magnitudes (PROTEIN_QUALITY_MATRIX_DISCOUNT).
    matrix_form = l3.get("protein_matrix_form")
    discount = 1.0
    disc_note = ""
    if matrix_form == "collagen":
        discount = PROTEIN_QUALITY_MATRIX_DISCOUNT["collagen"]
        disc_note = (f", F2 collagen matrix discount ×{discount} "
                     f"(incomplete AA profile, lowest matrix DIAAS)")
    elif matrix_form == "reconstructed" and category in PROTEIN_MATRIX_DISCOUNT_BAR_CATEGORIES:
        discount = PROTEIN_QUALITY_MATRIX_DISCOUNT["reconstructed"]
        disc_note = (f", F2 bar-format reconstructed-protein discount ×{discount} "
                     f"(isolate-bar gaming hole; DIAAS 47–81% of label)")

    score = round(quality * discount, 1)
    return score, f"protein={prot}g base={base:.1f}, source={source}(×{sf}){disc_note} → {score}"


def score_additive_quality(l3: dict) -> tuple[float, str]:
    ac = l3.get("additive_marker_count", 0)
    sw_tier = l3.get("sweetener_tier")
    _tier_penalties = {"A": SWEETENER_PENALTY_A, "B": SWEETENER_PENALTY_B, "C": SWEETENER_PENALTY_C}
    sw_pen = _tier_penalties.get(sw_tier, 0)
    base = max(0, 100 - ac * 18)
    score = round(max(0, base - sw_pen), 1)
    tier_note = f" tier-{sw_tier}" if sw_tier else ""
    return score, f"additive_categories={ac} → base={base}, sweetener{tier_note}_penalty={sw_pen} → {score}"


def score_satiety_support(nn: dict) -> tuple[float, str]:
    prot  = nn.get("protein_g") or 0
    fiber = nn.get("dietary_fiber_g") or 0
    kcal  = max(50, nn.get("energy_kcal") or 50)  # floor 50 to avoid division by tiny kcal
    numerator = prot * 3.0 + fiber * 5.0
    raw = (numerator / kcal) * 400
    score = round(max(0, min(100, raw)), 1)
    return score, f"(protein×3 + fiber×5) / max(50,kcal) × 400 = ({prot}×3 + {fiber}×5) / {kcal} × 400 = {score}"


def score_fat_quality(nn: dict, l3: dict, se_result: dict) -> tuple[float, str]:
    fat   = nn.get("fat_g") or 0
    sat_f = nn.get("fat_saturated_g")
    trans = nn.get("fat_trans_g") or 0
    has_seed_oil = l3.get("has_seed_oil", False)

    if fat < 0.5 or se_result.get("structurally_empty"):
        return 50.0, "SRC-04: fat < 0.5g or structurally empty → neutral 50"
    if sat_f is None:
        return 50.0, "sat_fat absent → neutral 50"

    sat_frac = sat_f / fat if fat > 0 else 0
    base = max(0, 100 - sat_f * 3.0 - sat_frac * 25)
    seed_pen = 10 if has_seed_oil else 0
    # Trans fat dimension penalty: use classified status from L3.
    # threshold_declaration (==0.5g, Israeli labeling artifact) carries no penalty.
    trans_status = l3.get("trans_fat_status", "not_detected")
    if trans_status in ("veto", "high_concern"):
        trans_pen = 20
    elif trans_status == "present":
        trans_pen = 10
    else:
        trans_pen = 0
    score = round(max(0, base - seed_pen - trans_pen), 1)
    note = (f"sat_fat={sat_f}g, frac={sat_frac:.2f}: base={base:.1f} "
            f"- seed_oil_pen={seed_pen} - trans_pen={trans_pen} = {score}")
    return score, note


def score_regulatory_quality(l3: dict) -> tuple[float, str]:
    count = l3.get("red_label_count", 0)
    labels = l3.get("red_labels", [])
    if count == 0:
        return 95.0, "no Israeli red labels"
    elif count == 1:
        return 60.0, f"1 red label: {labels}"
    else:
        return 25.0, f"{count} red labels: {labels}"


def score_whole_food_integrity(nova_level: int, ing_count: int, has_fermentation: bool = False) -> tuple[float, str]:
    base = NOVA_WFI_SCORES.get(nova_level, 50)
    complexity_pen = max(0, (ing_count - 8) * 2) if ing_count > 8 else 0
    ferm_bonus = 5 if has_fermentation else 0
    score = round(min(100, max(0, base - complexity_pen + ferm_bonus)), 1)
    ferm_note = f" + ferm_bonus={ferm_bonus}" if has_fermentation else ""
    return score, f"NOVA {nova_level} base={base}, ing_count={ing_count} complexity_pen={complexity_pen}{ferm_note} → {score}"


# ---------------------------------------------------------------------------
# Guardrail evaluation
# ---------------------------------------------------------------------------

def evaluate_guardrails(nn: dict, l3: dict, nova_level: int, category: str,
                         cat_confidence: float, eval_status: dict) -> dict:
    """
    Evaluate all guardrail rules. Returns dict with all fired caps and penalties
    per concern family, plus coordination outcomes.
    """
    kcal   = nn.get("energy_kcal") or 0
    sugar  = nn.get("sugars_g") or 0
    fat    = nn.get("fat_g") or 0
    sat_f  = nn.get("fat_saturated_g") or 0
    prot   = nn.get("protein_g") or 0
    fiber  = nn.get("dietary_fiber_g") or 0
    sodium = nn.get("sodium_mg") or 0
    trans  = nn.get("fat_trans_g") or 0
    ing_ct = l3.get("additive_marker_count", 0)  # using additive markers as proxy
    ingredients_count = len(l3.get("added_sugar_matches", []))  # not using this
    red_label_sugar   = "sugar" in l3.get("red_labels", [])
    red_label_sat_fat = "sat_fat" in l3.get("red_labels", [])
    red_label_count   = l3.get("red_label_count", 0)
    additive_ct       = l3.get("additive_marker_count", 0)
    added_sugar_ct    = l3.get("added_sugar_sources_count", 0)
    ing_list_count    = len(l3.get("ingredient_list", [])) if "ingredient_list" in l3 else 0
    fat_pct           = l3.get("fat_pct_of_kcal", 0) or 0  # from L2
    has_seed_oil      = l3.get("has_seed_oil", False)
    has_sweetener     = l3.get("sweetener_detected", False)
    is_snack_bar      = category == "snack_bar_granola"
    context_flag      = eval_status.get("context_flag")

    # SRC-02: sugar context routing
    sc_class = _classify_sugar_context(l3, nn, nova_level)

    # SRC-06: HP NOVA gate
    hp_nova_weight = NOVA_HP_WEIGHTS.get(nova_level, 0.5)

    # SRC-03: LOW_SATIETY gate for cooking oils
    satiety_rules_gated = (category == "whole_food_fat" and (kcal > 500 or fat > 50))

    caps_considered   = []
    caps_applied      = []
    penalties_considered = []
    penalties_applied = []

    # -----------------------------------------------------------------------
    # Trans fat veto
    # -----------------------------------------------------------------------
    trans_veto = trans > TRANS_FAT_VETO_THRESHOLD
    if trans_veto:
        return {
            "trans_fat_veto": True,
            "veto_score": 0,
            "sc_class": sc_class,
            "caps_considered": [{"rule": "TRANS_FAT_VETO", "cap": 0, "fired": True}],
            "caps_applied": [{"rule": "TRANS_FAT_VETO", "cap": 0}],
            "penalties_considered": [], "penalties_applied": [],
            "concern_family_coordination": {},
            "effective_cap": 0,
            "total_coordinated_penalty": 0,
            "hp_nova_weight": hp_nova_weight,
            "sc_class": sc_class,
            "satiety_rules_gated": satiety_rules_gated,
        }

    # -----------------------------------------------------------------------
    # SUGAR_LOAD family (with SRC-02 routing)
    # -----------------------------------------------------------------------
    sugar_caps_fired = []
    sugar_pens_fired = []

    # SRC-02 threshold adjustments
    sugar_threshold_25 = 25 if sc_class not in ("SC-1", "SC-2") else (1e9 if sc_class == "SC-1" else 40)
    sugar_threshold_20 = 20 if sc_class not in ("SC-1", "SC-2") else (1e9 if sc_class == "SC-1" else 35)
    sugar_threshold_15 = 15 if sc_class not in ("SC-1",) else 1e9

    def check_cap(rule, condition, cap, family_list):
        caps_considered.append({"rule": rule, "cap": cap, "condition": condition, "fired": condition})
        if condition:
            family_list.append((rule, cap))
            caps_applied.append({"rule": rule, "cap": cap})

    def check_penalty(rule, condition, amount, family_list, note=""):
        penalties_considered.append({"rule": rule, "amount": amount, "condition": str(condition), "fired": condition})
        if condition:
            family_list.append((rule, amount))
            penalties_applied.append({"rule": rule, "amount": amount, "note": note})

    # RC-01: SC-2 (whole-fruit primary, NOVA1-2, no added sugar) gets elevated caps.
    # Date/fig/raisin sugar ≠ glucose-syrup sugar; a 4-ingredient NOVA2 date bar
    # should not be capped identically to an engineered confection.
    sc2_natural = (sc_class == "SC-2")
    # R-04: plain dairy NOVA1–2 lactose-only gets same cap relief as SC-2
    is_plain_dairy = (
        nova_level in (1, 2)
        and l3.get("product_type_dairy", False)
        and added_sugar_ct == 0
    )
    sc2_or_plain_dairy = sc2_natural or is_plain_dairy

    # Sugar caps
    check_cap("HIGH_CAL_HIGH_SUGAR_SEVERE",   kcal >= 500 and sugar >= sugar_threshold_25, 50, sugar_caps_fired)
    check_cap("HIGH_CAL_HIGH_SUGAR_MODERATE", kcal >= 470 and sugar >= sugar_threshold_20, 60, sugar_caps_fired)
    _h25_cap = 68 if sc2_or_plain_dairy else 60
    check_cap("HIGH_SUGAR_25G_PLUS",          sugar >= sugar_threshold_25, _h25_cap, sugar_caps_fired)
    check_cap("SNACK_BAR_HIGH_CAL_SUGAR",     is_snack_bar and kcal >= 470 and sugar >= sugar_threshold_15, 60, sugar_caps_fired)
    _snack_sugar_cap = 63 if sc2_or_plain_dairy else 55
    check_cap("SNACK_BAR_RED_SUGAR_LABEL",    is_snack_bar and red_label_sugar, _snack_sugar_cap, sugar_caps_fired)
    # ISRAELI_RED_LABEL_1 sugar: only if SC-2+ (suspended for SC-1); SC-2 gets elevated cap
    if sc_class == "SC-1":
        caps_considered.append({"rule": "ISRAELI_RED_LABEL_1_SUGAR", "cap": 55, "condition": red_label_sugar,
                                 "fired": False, "note": "SRC-02: SC-1 product, cap suspended"})
    else:
        _isr_sugar_cap = 63 if sc2_or_plain_dairy else 55
        check_cap("ISRAELI_RED_LABEL_1_SUGAR", red_label_sugar, _isr_sugar_cap, sugar_caps_fired)
    check_cap("ISRAELI_RED_LABELS_2_PLUS",    red_label_count >= 2, 45, sugar_caps_fired)

    # Sugar penalties
    check_penalty("MULTIPLE_ADDED_SUGAR_MARKERS", added_sugar_ct >= 2, 5, sugar_pens_fired,
                  f"added_sugar_sources={added_sugar_ct}")
    check_penalty("HIGH_CAL_HIGH_SUGAR_SOFT",     kcal >= 430 and sugar >= sugar_threshold_15, 5, sugar_pens_fired)

    sugar_cap, sugar_pen, sugar_detail = _coordinate_family(sugar_caps_fired, sugar_pens_fired, SUGAR_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # CALORIE_LOAD family
    # -----------------------------------------------------------------------
    calorie_caps_fired = []
    calorie_pens_fired = []

    if not satiety_rules_gated:
        check_cap("HIGH_CAL_LOW_SATIETY_SEVERE", kcal >= 500 and prot < 6 and fiber < 3, 55, calorie_caps_fired)
    else:
        caps_considered.append({"rule": "HIGH_CAL_LOW_SATIETY_SEVERE", "cap": 55,
                                 "fired": False, "note": "SRC-03: gated for cooking oil/pure fat category"})

    check_cap("SNACK_BAR_HIGH_CAL", is_snack_bar and kcal >= 430, 70, calorie_caps_fired)

    if not satiety_rules_gated:
        check_penalty("HIGH_CAL_LOW_SATIETY_SOFT", kcal >= 450 and prot < 8 and fiber < 5, 6, calorie_pens_fired)
    else:
        penalties_considered.append({"rule": "HIGH_CAL_LOW_SATIETY_SOFT", "amount": 6,
                                      "fired": False, "note": "SRC-03: gated"})

    calorie_cap, calorie_pen, calorie_detail = _coordinate_family(calorie_caps_fired, calorie_pens_fired, CALORIE_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # PROCESSING_LOAD family
    # -----------------------------------------------------------------------
    proc_caps_fired = []
    proc_pens_fired = []

    check_cap("NOVA_PROXY_4_ULTRA_PROCESSED", nova_level == 4, 68, proc_caps_fired)
    check_cap("ADDITIVE_MARKERS_5_PLUS",      additive_ct >= 5, 60, proc_caps_fired)
    check_cap("ADDITIVE_MARKERS_3_PLUS",      3 <= additive_ct < 5, 72, proc_caps_fired)
    _nova3_cap = next(c for rule, _, c in PROCESSING_CAPS if rule == "NOVA_PROXY_3_PROCESSED")
    check_cap("NOVA_PROXY_3_PROCESSED",       nova_level == 3, _nova3_cap, proc_caps_fired)

    # Ingredient count for LONG_INGREDIENT_LIST uses full ingredients_list if available
    actual_ing_count = len(l3.get("added_sugar_matches", []))  # placeholder; use real count below
    # We'll pass ingredient count from product in caller; here use additive_ct as proxy
    # Actually fixed below: we need the real ing_list_count
    check_penalty("LONG_INGREDIENT_LIST", ing_list_count > 12, 4, proc_pens_fired,
                  f"ingredient_count={ing_list_count}")

    proc_cap, proc_pen, proc_detail = _coordinate_family(proc_caps_fired, proc_pens_fired, PROCESSING_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # SODIUM_LOAD family (SRC-03 for brined foods)
    # -----------------------------------------------------------------------
    sodium_caps_fired = []
    sodium_weight = 0.7 if context_flag == "brined_food" else 1.0
    raw_sodium_fires = sodium >= 700
    if raw_sodium_fires:
        effective_sodium_cap = int(60 / sodium_weight) if sodium_weight < 1.0 else 60
        # For brined foods, apply at 70% weight → effective cap slightly higher
        actual_cap = max(60, int(60 + (100-60) * (1-sodium_weight))) if sodium_weight < 1 else 60
        sodium_caps_fired.append(("HIGH_SODIUM_700MG_PLUS", actual_cap))
        caps_considered.append({"rule": "HIGH_SODIUM_700MG_PLUS", "cap": actual_cap, "fired": True,
                                 "note": f"sodium={sodium}mg (context weight={sodium_weight})"})
        caps_applied.append({"rule": "HIGH_SODIUM_700MG_PLUS", "cap": actual_cap})
    else:
        caps_considered.append({"rule": "HIGH_SODIUM_700MG_PLUS", "cap": 60,
                                 "fired": False, "condition": f"sodium={sodium}<700"})

    sodium_cap, sodium_pen, sodium_detail = _coordinate_family(sodium_caps_fired, [], SODIUM_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # FAT_QUALITY family
    # -----------------------------------------------------------------------
    fat_caps_fired = []
    fat_pens_fired = []

    # R5 — under RECAL_P0 the composite cliff cap is replaced by a graded fat-dimension
    # penalty (applied in _score_fat_quality_sprint1). Suppress the cap so it never fires;
    # flag OFF → unchanged.
    if RECAL_P0_ON:
        caps_considered.append({"rule": "ISRAELI_RED_LABEL_1_SAT_FAT", "cap": 55,
                                 "fired": False,
                                 "note": "R5: composite cap → graded fat-dimension penalty (RECAL_P0)"})
    else:
        check_cap("ISRAELI_RED_LABEL_1_SAT_FAT", red_label_sat_fat, 55, fat_caps_fired)
    check_penalty("SEED_OIL_PRESENT", has_seed_oil, 3, fat_pens_fired)

    fat_cap, fat_pen, fat_detail = _coordinate_family(fat_caps_fired, fat_pens_fired, FAT_QUALITY_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # SWEETENER (independent — SRC note: outside CONCERNS graph)
    # -----------------------------------------------------------------------
    _sw_caps = {"A": SWEETENER_CAP_A, "B": SWEETENER_CAP_B, "C": SWEETENER_CAP_C}
    sw_tier = l3.get("sweetener_tier")
    sweetener_cap_active = _sw_caps.get(sw_tier) if sw_tier else None

    # -----------------------------------------------------------------------
    # HP family (with SRC-06 NOVA gate)
    # -----------------------------------------------------------------------
    # fat_pct_kcal comes from L2 which is in l3 for convenience access
    l2_fat_pct = fat_pct  # passed in l3 from caller for convenience

    hp_pens_fired = []
    hp_fat_sugar  = (l2_fat_pct >= HP_FAT_SUGAR_FAT_PCT and sugar >= HP_FAT_SUGAR_SUGAR_G)
    hp_fat_sodium = (l2_fat_pct >= HP_FAT_SODIUM_FAT_PCT and sodium >= HP_FAT_SODIUM_SODIUM_G)
    hp_crunch     = (category == "cereal" and sugar >= HP_CRUNCH_SWEET_SUGAR
                     and fiber <= HP_CRUNCH_SWEET_FIBER)

    if hp_fat_sugar:
        effective_pen = round(HP_FAT_SUGAR_PENALTY * hp_nova_weight, 1)
        if effective_pen > 0:
            hp_pens_fired.append(("HP_FAT_SUGAR_COMBO", effective_pen))
            penalties_applied.append({"rule": "HP_FAT_SUGAR_COMBO", "amount": effective_pen,
                                      "note": f"raw_pen={HP_FAT_SUGAR_PENALTY} × nova_weight={hp_nova_weight}"})
        penalties_considered.append({"rule": "HP_FAT_SUGAR_COMBO", "amount": HP_FAT_SUGAR_PENALTY,
                                      "fired": True, "nova_weight": hp_nova_weight, "effective": effective_pen})
    else:
        penalties_considered.append({"rule": "HP_FAT_SUGAR_COMBO", "fired": False,
                                      "condition": f"fat_pct={l2_fat_pct:.1f}<{HP_FAT_SUGAR_FAT_PCT} or sugar={sugar}<{HP_FAT_SUGAR_SUGAR_G}"})

    if hp_fat_sodium:
        effective_pen = round(HP_FAT_SODIUM_PENALTY * hp_nova_weight, 1)
        if effective_pen > 0:
            hp_pens_fired.append(("HP_FAT_SODIUM_COMBO", effective_pen))
            penalties_applied.append({"rule": "HP_FAT_SODIUM_COMBO", "amount": effective_pen,
                                      "note": f"raw_pen={HP_FAT_SODIUM_PENALTY} × nova_weight={hp_nova_weight}"})
        penalties_considered.append({"rule": "HP_FAT_SODIUM_COMBO", "fired": True,
                                      "nova_weight": hp_nova_weight, "effective": effective_pen})
    else:
        penalties_considered.append({"rule": "HP_FAT_SODIUM_COMBO", "fired": False})

    if hp_crunch:
        effective_pen = round(HP_CRUNCH_SWEET_PENALTY * hp_nova_weight, 1)
        if effective_pen > 0:
            hp_pens_fired.append(("HP_CRUNCH_SWEET_COMBO", effective_pen))
        penalties_considered.append({"rule": "HP_CRUNCH_SWEET_COMBO", "fired": True,
                                      "nova_weight": hp_nova_weight, "effective": effective_pen})
    else:
        penalties_considered.append({"rule": "HP_CRUNCH_SWEET_COMBO", "fired": False,
                                      "note": "only applies to cereal category" if category != "cereal" else ""})

    hp_cap, hp_pen, hp_detail = _coordinate_family([], hp_pens_fired, HP_FAMILY_BUDGET)

    # -----------------------------------------------------------------------
    # Assemble binding caps and total penalties
    # -----------------------------------------------------------------------
    all_caps = {
        "sugar_load":     sugar_cap,
        "calorie_load":   calorie_cap,
        "processing_load": proc_cap,
        "sodium_load":    sodium_cap,
        "fat_quality":    fat_cap,
        "sweetener":      sweetener_cap_active,
    }
    binding_cap = min(v for v in all_caps.values() if v is not None) if any(v is not None for v in all_caps.values()) else None

    total_penalty = round(sugar_pen + calorie_pen + proc_pen + sodium_pen + fat_pen + hp_pen, 1)

    return {
        "trans_fat_veto": False,
        "sc_class": sc_class,
        "satiety_rules_gated": satiety_rules_gated,
        "hp_nova_weight": hp_nova_weight,
        "caps_considered": caps_considered,
        "caps_applied": caps_applied,
        "penalties_considered": penalties_considered,
        "penalties_applied": penalties_applied,
        "concern_family_coordination": {
            "sugar_load":     {"binding_cap": sugar_cap, "coordinated_penalty": sugar_pen, "detail": sugar_detail},
            "calorie_load":   {"binding_cap": calorie_cap, "coordinated_penalty": calorie_pen, "detail": calorie_detail},
            "processing_load": {"binding_cap": proc_cap, "coordinated_penalty": proc_pen, "detail": proc_detail},
            "sodium_load":    {"binding_cap": sodium_cap, "coordinated_penalty": sodium_pen, "detail": sodium_detail},
            "fat_quality":    {"binding_cap": fat_cap, "coordinated_penalty": fat_pen, "detail": fat_detail},
            "hp":             {"binding_cap": None, "coordinated_penalty": hp_pen, "detail": hp_detail},
        },
        "all_family_caps": all_caps,
        "binding_cap": binding_cap,
        "total_coordinated_penalty": total_penalty,
    }


def _coordinate_family(caps: list, penalties: list, budget: float) -> tuple:
    """Concern coordination: strictest cap, winner penalty at full, others at 40%. Budget clamp."""
    binding = min(c[1] for c in caps) if caps else None

    if not penalties:
        return binding, 0.0, {"winner": None, "supporters": [], "total_before_budget": 0}

    sorted_pens = sorted(penalties, key=lambda x: x[1], reverse=True)
    total = sorted_pens[0][1]
    supporters = []
    for name, amount in sorted_pens[1:]:
        contrib = round(amount * 0.4, 2)
        total += contrib
        supporters.append({"rule": name, "scaled_to": contrib})

    if total > budget:
        total = budget

    detail = {
        "winner": {"rule": sorted_pens[0][0], "amount": sorted_pens[0][1]},
        "supporters": supporters,
        "total_before_budget": total,
        "budget_applied": total >= budget,
    }
    return binding, round(total, 2), detail


def _classify_sugar_context(l3: dict, nn: dict, nova_level: int) -> str:
    """SRC-02: Classify sugar context class SC-1 through SC-5."""
    ingredients = l3.get("ingredient_list", []) if "ingredient_list" in l3 else []
    has_fruit_conc = l3.get("has_fruit_concentrate", False)
    added_sg_ct    = l3.get("added_sugar_sources_count", 0)
    ing_text       = " ".join(ingredients)

    # SC-5: refined added sugar explicitly listed
    refined_sugar_terms = ["סוכר", "סוכר קנים", "סוכר חום"]
    for term in refined_sugar_terms:
        if term in ing_text:
            return "SC-5"

    # SC-4: fruit concentrate / syrup used as sweetener ingredient
    if has_fruit_conc:
        return "SC-4"

    # SC-3: fruit juice as primary component (liberated sugar)
    if "מיץ" in ing_text or "תמצית" in ing_text:
        return "SC-3"

    # SC-2: whole fruit as primary in multi-ingredient product (NOVA 1-2)
    if nova_level <= 2 and added_sg_ct == 0:
        return "SC-2"

    # SC-1: single-ingredient whole fruit (NOVA 1, no added sugar signals)
    ingredients_count = len(ingredients)
    if nova_level == 1 and ingredients_count <= 2 and added_sg_ct == 0:
        return "SC-1"

    return "SC-5"  # default: treat as added sugar if ambiguous


# ---------------------------------------------------------------------------
# Floor application (SRC-01)
# ---------------------------------------------------------------------------

def apply_floors(pre_floor_score: float, nova_level: int, nova_conf: float,
                  category: str, guardrail_result: dict, red_label_count: int) -> dict:
    """Apply floors per SRC-01 floor-cap hierarchy."""
    floors_considered = []
    floors_applied = []

    # Determine which floor is applicable
    single_ingredient_nova1 = (nova_level == 1 and nova_conf >= 0.70)
    whole_food_fat_nova12   = (nova_level <= 2 and category == "whole_food_fat")

    if single_ingredient_nova1:
        target_floor = NOVA1_SINGLE_FLOOR
        floor_type = "nova1_single_ingredient"
    elif whole_food_fat_nova12:
        target_floor = WHOLE_FOOD_FAT_FLOOR
        floor_type = "whole_food_fat_nova1_2"
    else:
        floors_considered.append("no_applicable_floor")
        return {"final_score_after_floors": pre_floor_score, "floors_considered": floors_considered,
                "floors_applied": floors_applied, "floor_type": None}

    floors_considered.append({"floor_type": floor_type, "floor_value": target_floor})

    # SRC-01: Classify binding caps as Class A (mismatch) or Class B (physiological)
    class_b_caps = {
        "HIGH_CAL_HIGH_SUGAR_SEVERE", "HIGH_CAL_HIGH_SUGAR_MODERATE", "HIGH_SUGAR_25G_PLUS",
        "SNACK_BAR_HIGH_CAL_SUGAR", "SNACK_BAR_RED_SUGAR_LABEL",
        "ISRAELI_RED_LABEL_1_SUGAR", "ISRAELI_RED_LABELS_2_PLUS",
        "HIGH_CAL_LOW_SATIETY_SEVERE", "HIGH_CAL_LOW_SATIETY_SOFT",
        "HIGH_SODIUM_700MG_PLUS",
        "ISRAELI_RED_LABEL_1_SAT_FAT",
    }

    fired_cap_rules = {c["rule"] for c in guardrail_result.get("caps_applied", [])}
    has_class_b_cap = bool(fired_cap_rules & class_b_caps)

    if not has_class_b_cap:
        # Full floor applies
        effective_floor = target_floor
        note = "SRC-01: no Class B physiological caps fired → full floor applies"
    else:
        # Physiological moderation
        if red_label_count >= 2:
            effective_floor = PHYSIO_2PLUS_LABELS_MIN
            note = f"SRC-01: Class B caps fired + 2+ red labels → floor={PHYSIO_2PLUS_LABELS_MIN}"
        else:
            effective_floor = PHYSIO_MODERATION_MIN
            note = f"SRC-01: Class B caps fired on whole food → physiological moderation minimum={PHYSIO_MODERATION_MIN}"

    if pre_floor_score < effective_floor:
        post_floor = effective_floor
        floors_applied.append({"floor_type": floor_type, "floor_value": effective_floor,
                                "pre_floor": pre_floor_score, "note": note})
    else:
        post_floor = pre_floor_score
        floors_considered[-1]["note"] = f"floor={effective_floor} not binding (score={pre_floor_score:.1f})"

    return {
        "final_score_after_floors": post_floor,
        "floors_considered": floors_considered,
        "floors_applied": floors_applied,
        "floor_type": floor_type,
        "effective_floor": effective_floor,
        "floor_was_binding": pre_floor_score < effective_floor,
    }


# ---------------------------------------------------------------------------
# Main score function
# ---------------------------------------------------------------------------

def score_product(product: dict, signals: dict, cat_result: dict,
                  nova_result: dict, eval_result: dict) -> dict:
    """
    Full scoring pipeline. Returns complete score trace.
    """
    pid = product.get("canonical_product_id", "unknown")
    nn  = product.get("normalized_nutrition_per_100g") or {}

    l1 = signals["L1_observed_signals"]
    l3 = signals["L3_inferred_classifications"]

    # Inject L2 fat_pct into l3 for convenience access
    l3["fat_pct_of_kcal"] = signals["L2_derived_signals"].get("fat_pct_of_kcal") or 0
    l3["ingredient_list"] = l1.get("ingredient_list") or []

    category     = cat_result["category"]
    cat_conf     = cat_result["category_confidence"]
    nova_level   = nova_result["nova_level"]
    nova_conf    = nova_result["nova_confidence"]
    red_label_ct = l3.get("red_label_count", 0)

    # Stage 0 gate: out_of_scope
    if eval_result.get("evaluation_status") == "out_of_scope":
        return {
            "product_id": pid,
            "evaluation_status": "out_of_scope",
            "final_score_estimate": None,
            "grade_estimate": None,
            "score_not_produced_reason": eval_result.get("context_note"),
        }

    # Stage 1: Confidence
    conf_result = compute_confidence(product, signals, cat_result, nova_result)
    confidence  = conf_result["confidence_score"]

    # Stage 2: Structural emptiness gate
    se_result = detect_structural_emptiness(nn, category, l3)

    # Stage 3: Dimension scoring
    has_fortification = l3.get("has_fortification", False)
    has_fermentation  = l3.get("has_fermentation", False)

    pq_score,  pq_note  = score_processing_quality(nova_level)
    nd_score,  nd_note  = score_nutrient_density(nn, has_fortification, category)
    cd_table_key = category
    if cat_result.get("category_subtype") == "yogurt":
        cd_table_key = "yogurt"
    cd_score,  cd_note  = score_calorie_density(nn, cd_table_key, cat_conf, se_result)
    gq_score,  gq_note  = _score_glycemic_quality_sprint1(nn, l3)   # EV-004
    prq_score, prq_note = score_protein_quality(nn, l3, category)    # F2: matrix discount
    aq_score,  aq_note  = _score_additive_quality_sprint1(l3)        # EV-003/019 + F1/F4 identity
    ss_score,  ss_note  = score_satiety_support(nn)
    fq_score,  fq_note  = _score_fat_quality_sprint1(nn, l3, se_result)  # EV-012
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

    # R6 — veg_spread archetype re-weighting (TASK-169 / EV-032), gated by BARI_RECAL_P0.
    # Detected at routing: a sauce_spread whose subtype is a whole-vegetable spread AND
    # whose protein < 3g (not a legume/dairy protein food). Re-weight so the score
    # reflects ingredient cleanliness, whole-veg base, low energy density, sodium
    # discipline — not protein density. Anti-immunity guard below.
    VEG_SPREAD_SUBTYPES = {"matbucha", "pepper_spread", "pepper_chuma", "eggplant_spread"}
    prot_g = nn.get("protein_g") or 0
    cat_subtype = cat_result.get("category_subtype")
    is_veg_spread = (
        RECAL_P0_ON
        and category == "sauce_spread"
        and cat_subtype in VEG_SPREAD_SUBTYPES
        and prot_g < 3.0
    )
    veg_spread_immunity_clamped = False
    if is_veg_spread:
        active_weights = VEG_SPREAD_WEIGHTS
    else:
        active_weights = DIMENSION_WEIGHTS

    weighted_sum = sum(dim_scores[k] * active_weights[k] for k in dim_scores)
    weighted_dim_score = round(weighted_sum, 2)

    # R6 anti-immunity guard: a veg_spread cannot exceed the immunity ceiling unless its
    # additives are clean (no markers) AND sodium is sub-red-label. Prevents an
    # engineered / sodium-heavy spread from reaching A on the re-weight.
    if is_veg_spread and weighted_dim_score > VEG_SPREAD_IMMUNITY_CEILING:
        clean_additives = (l3.get("additive_marker_count", 0) == 0)
        sodium_ok = "sodium" not in l3.get("red_labels", [])
        if not (clean_additives and sodium_ok):
            weighted_dim_score = round(VEG_SPREAD_IMMUNITY_CEILING, 2)
            veg_spread_immunity_clamped = True

    # R-02: direct fermentation bonus (pre-cap, NOVA1–3)
    # R7 v1.1 (TASK-169A): gate the live-culture +8 to GENUINELY cultured dairy.
    # Supersedes the v1 "product_type_dairy + plain ⇒ cultured" assumption, which leaked
    # the +8 onto plain FLUID MILK (85/A breach) and over-credited table-stakes
    # fresh-cheese culturing. Two qualifying paths; flag OFF → Path A only (HEAD behavior).
    #   Path A — declared culture marker (has_fermentation). Unchanged from HEAD.
    #   Path B — inherently-cultured TYPE: yogurt subtypes OR aged/specialty cultured-cheese
    #            name marker. Hard-excludes fluid milk / plant drinks; excludes flavored
    #            variants; excludes cottage + white-cheese fresh subtypes (cottage ruling).
    # Router reconciliation (v1.1 call #4): the live router emits NO `milk_dairy` and NO
    # top-level `yogurt` category — milk, cheese AND yogurt all route to `dairy_protein`.
    # So Path B is keyed off the router's real yogurt SUBTYPES + cheese NAME markers, and
    # fluid milk is hard-excluded by a fluid-milk NAME marker. See constants.py R7 v1.1.
    fermentation_bonus = 0
    fermentation_bonus_note = None
    r7_culture_credit = False
    r7_path = None
    eligible_ferm = has_fermentation                       # Path A (declared culture)
    if RECAL_P0_ON and not has_fermentation and nova_level <= 3:
        _name = (product.get("canonical_name_he")
                 or product.get("product_name_he") or "")
        _ing  = " ".join(l3.get("ingredient_list") or [])
        _hay  = (_name + " " + _ing)
        subtype = cat_result.get("category_subtype")
        # Token-aware name set: avoids the substring trap where the fluid-milk marker
        # חלב (milk) matches inside חלבון (protein). Markers are matched against whole
        # whitespace-delimited tokens; multi-word markers (e.g. גבינת שמנת) still use
        # substring containment on the full name.
        _name_tokens = set(_name.split())

        def _name_has(markers):
            return any((" " in m and m in _name) or (m in _name_tokens) for m in markers)

        # Path B.1 — yogurt subtype (cultured by definition). The ROUTER subtype is the
        # most reliable cultured-TYPE signal, so a confirmed yogurt subtype qualifies
        # outright and is NOT second-guessed by the fluid-milk name heuristic.
        is_yogurt = (category == "yogurt"
                     or subtype in CULTURED_YOGURT_SUBTYPES)

        # Hard-exclude fluid milk / drinks: a fluid-milk name TOKEN without a dairy-solid
        # identity marker (גבינה/קוטג/לבנה/יוגורט/…). Plant drinks (משקה …) caught here.
        # Only consulted for the non-yogurt-subtype path (cheese-name path), since a
        # confirmed yogurt subtype already establishes a cultured type.
        has_solid_identity = _name_has(DAIRY_SOLID_IDENTITY_MARKERS_HE)
        is_fluid_milk = _name_has(FLUID_MILK_NAME_MARKERS_HE) and not has_solid_identity

        # Flavored / seasoned variant disqualifies Path B (matches R4's flavored-variant
        # logic; kept independent — separate test, no shared state).
        is_flavored_variant = any(m in _hay for m in FLAVORED_VARIANT_MARKERS_HE)

        # Path B.2 — aged/specialty cultured cheese by name. Cottage (קוטג') and
        # white-cheese (גבינה לבנה / לבנה) fresh subtypes are NOT in the marker set, so
        # they do not qualify here → plain cottage lands at its R1+R2+R4 value (~90/A).
        is_cultured_cheese = (category in ("dairy_protein", "default")
                              and any(m in _name for m in CULTURED_CHEESE_NAME_MARKERS_HE)
                              and not is_fluid_milk)

        if is_yogurt and not is_flavored_variant:
            eligible_ferm = True
            r7_culture_credit = True
            r7_path = "yogurt_subtype"
        elif is_cultured_cheese and not is_flavored_variant:
            eligible_ferm = True
            r7_culture_credit = True
            r7_path = "cultured_cheese_name"
    if eligible_ferm and nova_level <= 3:
        fermentation_bonus = FERMENTATION_DIRECT_BONUS
        weighted_dim_score = round(min(100, weighted_dim_score + fermentation_bonus), 2)
        fermentation_bonus_note = (
            f"R-02 fermentation_bonus: +{fermentation_bonus} (direct, pre-cap)"
            + (f" [R7 v1.1 Path B: {r7_path}]" if r7_culture_credit else ""))

    # Stage 4: Guardrail evaluation
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
            "explanation_drivers": ["Trans fat veto: score = 0 (trans fat > 1.0g/100g)"],
            "unresolved_flags": [],
        }

    # Stage 5: Cap application
    binding_cap = gr.get("binding_cap")
    score_after_cap = min(weighted_dim_score, binding_cap) if binding_cap is not None else weighted_dim_score

    # Stage 6: Relative penalty scaling (SRC-05)
    total_pen = gr.get("total_coordinated_penalty", 0)
    penalty_factor = RELATIVE_PENALTY_FACTOR_LOW if score_after_cap < 30 else RELATIVE_PENALTY_FACTOR_HIGH
    max_relative_pen = score_after_cap * penalty_factor
    if total_pen > max_relative_pen:
        scaled_penalty = round(max_relative_pen, 2)
        penalty_scaling_note = (f"SRC-05: penalty {total_pen} exceeds {penalty_factor*100:.0f}% "
                                f"of pre-penalty score {score_after_cap:.1f} → scaled to {scaled_penalty}")
    else:
        scaled_penalty = total_pen
        penalty_scaling_note = None

    # Stage 7: Penalty application (guardrails + EV-005 polyol post-cap)
    product_name = (product.get("canonical_name_he") or product.get("product_name_he") or "")
    polyol_penalty, polyol_note = _compute_polyol_penalty(l3, product_name)
    score_after_penalty = round(score_after_cap - scaled_penalty - polyol_penalty, 2)
    score_after_penalty = max(ABSOLUTE_SCORE_FLOOR, score_after_penalty)  # absolute floor

    # Stage 8: Floor application (SRC-01)
    floor_result = apply_floors(score_after_penalty, nova_level, nova_conf, category, gr, red_label_ct)
    score_after_floors = floor_result["final_score_after_floors"]

    # Stage 9: Confidence ceiling
    ceiling = conf_result.get("confidence_ceiling")
    if ceiling is not None and score_after_floors > ceiling:
        final_score = ceiling
        ceiling_note = f"confidence ceiling {ceiling} applied (confidence={confidence}, band={conf_result['confidence_band']})"
    else:
        final_score = score_after_floors
        ceiling_note = None

    final_score = round(final_score, 1)
    grade = score_to_grade(final_score)

    # Data sufficiency gate: when confidence is insufficient or nutrition panel is absent,
    # the score is tentative — do not assign a normal letter grade.
    is_insufficient = (confidence < 40 or eval_result.get("context_flag") == "no_nutrition_data")
    if is_insufficient:
        data_sufficiency = "insufficient"
        grade = "insufficient_data"
    else:
        data_sufficiency = "sufficient"

    # Explanation drivers
    drivers = _identify_drivers(gr, floor_result, conf_result, dim_scores, binding_cap, ceiling)

    # Unresolved flags
    flags = _collect_flags(product, signals, cat_result, nova_result, gr, floor_result,
                            se_result, eval_result)

    return {
        "product_id": pid,
        "evaluation_status": eval_result["evaluation_status"],
        "context_flag": eval_result.get("context_flag"),
        "context_note": eval_result.get("context_note"),
        "structural_emptiness_result": se_result,
        "confidence_result": conf_result,
        "dimension_scores": dim_scores,
        "dimension_notes": dim_notes,
        "dimension_weights": active_weights,
        "recal_p0_veg_spread": is_veg_spread if RECAL_P0_ON else None,
        "recal_p0_veg_spread_immunity_clamped": veg_spread_immunity_clamped if RECAL_P0_ON else None,
        "weighted_dimension_score": weighted_dim_score,
        "fermentation_bonus_applied": fermentation_bonus if fermentation_bonus else None,
        "fermentation_bonus_note": fermentation_bonus_note,
        "caps_considered": gr.get("caps_considered", []),
        "caps_applied":    gr.get("caps_applied", []),
        "binding_cap":     binding_cap,
        "score_after_cap": round(score_after_cap, 2),
        "penalties_considered": gr.get("penalties_considered", []),
        "penalties_applied":    gr.get("penalties_applied", []),
        "total_penalty_before_scaling": total_pen,
        "total_penalty_after_scaling":  scaled_penalty,
        "penalty_scaling_note": penalty_scaling_note,
        "polyol_penalty":       polyol_penalty,
        "polyol_penalty_note":  polyol_note if polyol_penalty > 0 else None,
        "score_after_penalty":  score_after_penalty,
        "concern_family_coordination": gr.get("concern_family_coordination", {}),
        "floors_considered": floor_result.get("floors_considered", []),
        "floors_applied":    floor_result.get("floors_applied", []),
        "score_after_floors": score_after_floors,
        "confidence_ceiling_applied": ceiling_note,
        "final_score_estimate": final_score,
        "grade_estimate": grade,
        "data_sufficiency": data_sufficiency,
        "sugar_context_class": gr.get("sc_class"),
        "hp_nova_weight": gr.get("hp_nova_weight"),
        "explanation_drivers": drivers,
        "unresolved_flags": flags,
    }


def _identify_drivers(gr, floor_result, conf_result, dim_scores, binding_cap, ceiling):
    drivers = []
    if ceiling is not None:
        drivers.append(f"DOMINANT: Confidence ceiling active at {ceiling} (data quality limitation)")
    if binding_cap is not None:
        applied_rules = [c["rule"] for c in gr.get("caps_applied", [])]
        drivers.append(f"DOMINANT: Binding cap={binding_cap} from rules: {applied_rules}")
    if not drivers:
        # Find dimension most below neutral
        worst_dim = min(dim_scores.items(), key=lambda x: x[1])
        drivers.append(f"PRIMARY SIGNAL: {worst_dim[0]}={worst_dim[1]:.1f} (lowest dimension)")
    if floor_result.get("floor_was_binding"):
        drivers.append(f"FLOOR APPLIED: {floor_result.get('floor_type')} → minimum {floor_result.get('effective_floor')}")
    pens = gr.get("penalties_applied", [])
    if pens:
        drivers.append(f"PENALTIES: {[p['rule'] for p in pens]}")
    return drivers[:4]


def _collect_flags(product, signals, cat_result, nova_result, gr, floor_result, se_result, eval_result):
    flags = []
    l1 = signals["L1_observed_signals"]
    l4 = signals["L4_interpreted_concerns"]

    # Data quality flags
    for f in l4.get("pre_evaluation_flags", []):
        flags.append(f)

    # Category instability
    if cat_result.get("category_instability_flag"):
        flags.append(f"CATEGORY_INSTABILITY: primary={cat_result['category']} "
                     f"secondary={cat_result['secondary_category']}, "
                     f"confidence={cat_result['category_confidence']}")

    # Structural emptiness
    if se_result.get("structurally_empty"):
        flags.append("STRUCTURAL_EMPTINESS: calorie density dimension capped at 50 (SRC-04)")

    # Floor-cap conflict
    if floor_result.get("floor_was_binding") and gr.get("caps_applied"):
        flags.append(f"FLOOR_CAP_INTERACTION: floor overrode cap "
                     f"(floor={floor_result.get('effective_floor')}, "
                     f"caps={[c['rule'] for c in gr.get('caps_applied', [])]})")

    # Context limited
    if eval_result.get("evaluation_status") == "context_limited":
        flags.append(f"CONTEXT_LIMITED: per-100g score may be misleading "
                     f"({eval_result.get('context_flag')})")

    # Trans fat concern
    # threshold_declaration (fat_trans==0.5g) is the Israeli labeling convention for "<1g".
    # It is annotated in L3.trans_fat_threshold_declaration_possible but NOT added as an
    # unresolved flag, since it is not a confirmed real trans fat signal.
    trans_status = signals["L3_inferred_classifications"].get("trans_fat_status")
    if trans_status == "high_concern":
        flags.append("HIGH_TRANS_FAT_CONCERN: trans_fat in 0.5-1.0g range (exclusive), no veto but flagged")
    elif trans_status == "present":
        flags.append("TRANS_FAT_PRESENT: trans_fat 0.2-0.5g (confirmed above threshold declaration)")

    # Low NOVA confidence
    if nova_result.get("nova_confidence_band") == "low":
        flags.append(f"LOW_NOVA_CONFIDENCE: NOVA inference unreliable "
                     f"({nova_result.get('nova_confidence')})")

    return flags
