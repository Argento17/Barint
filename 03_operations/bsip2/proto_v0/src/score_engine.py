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
    SERVING_SUGGESTION_PROSE_MARKERS_HE,
    RED_LABEL_THRESHOLDS as _RED_LABEL_THRESHOLDS,
    score_to_grade,
    GLASSBOX_D5_CONF_REDUCTION, GLASSBOX_DEMOTE_CEILING_BOUND, GLASSBOX_NULL_FLOOR,
    GLASSBOX_WITHHELD_LABEL, GLASSBOX_PARTIAL_FLAG,
    GLASSBOX_NUTRITION_BLEED_ANCHORS, GLASSBOX_GENERIC_ADDITIVE_TERMS,
    GLASSBOX_ENDEMIC_FLAVORING_TERMS, GLASSBOX_COMPOUND_TERMS,
    GLASSBOX_PROTEIN_BLEND_TERMS, GLASSBOX_PROTEIN_NAMED_SOURCES,
    GLASSBOX_PROTEIN_INCOMPLETE_NAMED,
    DIAAS_COMPLETE_SOURCES, DIAAS_DISCLOSURE_GAP_TRIGGERS,
    DIAAS_D2_CREDIT, DIAAS_D2_SCORE_CAP,
    GLASSBOX_W2_ADDITIVES,
)
import re as _re

# TASK-144 — same activation toggle as signal_extractor; gates Fix 2 (fiber-not-applicable).
# DEFAULT OFF (frozen behavior). Only the maadanim batch runner opts in via
# BARI_TASK144_FIXES=on. See signal_extractor.py for the full activation-scope rationale.
TASK144_FIXES_ON = os.environ.get("BARI_TASK144_FIXES", "off").lower() == "on"

# TASK-169 P0 — single rollback flag for ALL recalibration changes (R1–R7).
# DEFAULT OFF → engine byte-identical to 0.4.1 (safety contract + regression guard).
# Source of truth: 01_framework/bsip2_framework/recalibration_p0_design_v1.md.
RECAL_P0_ON = os.environ.get("BARI_RECAL_P0", "off").lower() == "on"

# TASK-169D — OPTIONAL yogurt top-trim (DECISION MODEL ONLY, default OFF).
# When ON (and RECAL_P0_ON), the live-culture +8 may lift a cultured yogurt to A but is
# capped so it cannot, by itself, manufacture an S: a yogurt that received the gated +8 is
# held at a pre-floor/pre-ceiling A-ceiling (RECAL_P0_YOGURT_TRIM_CEILING). This is the
# precedented A-ceiling construct (cf. cheese A-ceiling) applied to the yogurt apex — the
# cleanest "trim the top" lever, since the S-grades arise from the +8 stacking on an
# already-high base, not from the protein scale apex. OFF → no effect (option a).
RECAL_P0_YOGURT_TRIM = os.environ.get("BARI_RECAL_P0_YOGURT_TRIM", "off").lower() == "on"
RECAL_P0_YOGURT_TRIM_CEILING = 89.9

# TASK-179G — Glass Box D5 (transparency) + D6 (confidence) gate.
# DEFAULT OFF → engine byte-identical to today (verified by verify_glassbox_off_identical.py).
# Mirrors the RECAL_P0 / TASK144 flag pattern. Source: d5_d6_rule_spec_v1.md.
# EV-035…EV-039 (bsip2_evidence_registry_v1.md). With OFF: the D5 detector is not invoked,
# no D5 confidence reduction is applied, and the §2.2 gate state machine is not entered —
# the current ceiling / insufficient_data path runs verbatim.
GLASSBOX_D5D6_ON = os.environ.get("BARI_GLASSBOX_D5D6", "off").lower() == "on"

# TASK-179P — Glass Box W1.5 DIAAS protein-quality signal.
# DEFAULT OFF → engine byte-identical to BARI_GLASSBOX_D5D6 baseline.
# Source: diaas_source_table_v1.md §Nutrition Rule Definition (Phase 2). EV-040.
# Rule A (+3 D2 credit) requires Product D7 co-sign before activation.
# Rule B (D5 disclosure-gap flag) inherits Product approval via EV-037.
BARI_GLASSBOX_W15 = os.environ.get("BARI_GLASSBOX_W15", "off").lower() == "on"

# TASK-179S — Glass Box W2 D4 additive tier wire.
# DEFAULT OFF → engine byte-identical to BARI_GLASSBOX_W15 baseline.
# Source: additive_prototype_set_v1.md §Nutrition Phase 3 Co-sign. EV-041.
# No score movement; D4 signal is presentation-only for the W2 prototype.
# Additives not in GLASSBOX_W2_ADDITIVES → tier "unclassified" (never invented).
BARI_GLASSBOX_W2 = os.environ.get("BARI_GLASSBOX_W2", "off").lower() == "on"

# TASK-181G / TASK-181K — Glass Box W4 D3 de-moralization (confidence-scaled
# processing signal). DEFAULT OFF → engine byte-identical to BARI_GLASSBOX_W2 baseline.
# Source: d3_demoralization_spec_v1.md §2 / §4. Evidence registry: EV-042 — REVISED
# 2026-06-04 (TASK-181J, Nutrition + Product D7 both co-signed). TASK-181K re-implements
# the medium-band material/non-material split: the original single flat medium=0.70
# scale is replaced by medium-MATERIAL=0.70 (score pulls toward neutral, as before) vs
# medium-NON-MATERIAL=1.0 (D3 score does NOT move; the doubt routes to D6 confidence).
# With OFF: score_processing_quality runs the current NOVA_PROCESSING_SCORES lookup
# verbatim, the PROCESSING_LOAD caps and NOVA_HP_WEIGHTS scaling are unchanged, and no
# d3_processing_signal is emitted.
BARI_GLASSBOX_W4 = os.environ.get("BARI_GLASSBOX_W4", "off").lower() == "on"

# ---------------------------------------------------------------------------
# TASK-181G — Glass Box W4: D3 de-moralization helpers (EV-042 bound values).
# ALL constants below are inert unless BARI_GLASSBOX_W4 is ON (call sites are
# flag-guarded). bound_value_set_2 (confidence_scale) + bound_value_set_3
# (population_correlation) are bound verbatim from EV-042 / spec §2.4 / §2.5;
# bound_value_set_1 (confidence criteria) is implemented in _d3_compute_confidence.
# ---------------------------------------------------------------------------

# EV-042 bound_value_set_2 (REVISED TASK-181J) — confidence_scale is now selected by
# confidence band AND uncertainty materiality (bound_value_set_4):
#   high            = 1.0   (unchanged)
#   low             = 0.40  (unchanged)
#   medium-MATERIAL = 0.70  (the medium scale-down, applied ONLY when the gap is material)
#   medium-NON-MATERIAL = 1.0 (NO D3 move; doubt routes to D6 — bound_value_set_5)
# The flat-medium dict is retired; use _w4_confidence_scale(confidence, materiality).
W4_HIGH_SCALE      = 1.0
W4_MEDIUM_MATERIAL_SCALE = 0.70
W4_LOW_SCALE       = 0.40
W4_NEUTRAL = 50.0


def _w4_confidence_scale(confidence: str, materiality: str = None) -> float:
    """EV-042 bound_value_set_2 (revised) — confidence_scale selector.
    high→1.0; low→0.40; medium→0.70 if materiality=='material' else 1.0 (no move)."""
    if confidence == "high":
        return W4_HIGH_SCALE
    if confidence == "low":
        return W4_LOW_SCALE
    if confidence == "medium":
        return W4_MEDIUM_MATERIAL_SCALE if materiality == "material" else 1.0
    # Defensive default (never reached for the three bound bands): no move.
    return 1.0


# EV-042 bound_value_set_5 (NEW, TASK-181J) — D3→D6 confidence deductions.
# Non-material medium-band gap = −5 (half the D5 partial −10). Low-confidence NOVA = −10
# (equal to the D5 partial term). Both flag-gated, both max-combined with any D5 term for
# the SAME token (never summed). Stored as positive magnitudes; deducted at the call site.
W4_D6_NONMATERIAL_DEDUCTION = 5
W4_D6_LOW_CONFIDENCE_DEDUCTION = 10

# EV-042 bound_value_set_3 — fixed class-level population-correlation anchors
# (reference field in the trace; NOT a multiplier in the score arithmetic).
W4_POPULATION_CORRELATION = {1: 0.05, 2: 0.15, 3: 0.40, 4: 0.75}

# Spec §3.3 (Product D7 co-signed 2026-06-04) — final approved note_he strings.
# Candidate A: NOVA 1, high confidence, positive signal.
W4_NOTE_HE_A = (
    "מוצר בעיבוד מינימלי — דפוס ההרכב שלו מתאם, במחקרים גדולים על אוכלוסיות רבות, "
    "עם תוצאות תזונתיות חיוביות."
)
# Candidate B: NOVA 3–4, medium/high confidence, negative signal.
W4_NOTE_HE_B = (
    "דפוס הרכב זה מתאם, במחקרים גדולים על אוכלוסיות רבות, עם צריכה תזונתית גבוהה יותר "
    "של סוכר, שומן ונתרן — לא אמירה על מוצר זה בפני עצמו."
)
# Candidate C (full form): low confidence, any class.
W4_NOTE_HE_C = (
    "הרכב המוצר לא פורט במלואו — לא ניתן להעריך את דפוס העיבוד בביטחון. "
    "האומדן הנוכחי הוא זמני."
)
# Candidate C (mobile-compressed variant): low confidence, any class.
W4_NOTE_HE_C_MOBILE = "הרכב המוצר לא פורט במלואו — האומדן לדפוס העיבוד הוא זמני."


def _d3_compute_confidence(nova_result: dict, l3: dict, disclosure_profile) -> tuple[str, str]:
    """EV-042 bound_value_set_1 — confidence in the NOVA assignment, keyed to
    ingredient-evidence quality (NOT the NOVA class — the de-circularizing move).

    Returns (confidence_band, reason_note). Bands: "high" | "medium" | "low".

    Full rule (when BARI_GLASSBOX_D5D6 is ON and a disclosure_profile is available)
    reads D5's band + G4 generic-additive output. When D5D6 is OFF, the spec's
    two-signal fallback applies: ingredient-list present/absent + the NOVA
    classifier's own confidence band only.
    """
    ing_list = l3.get("ingredient_list") or []
    ing_present = len(ing_list) > 0
    nova_band = nova_result.get("nova_confidence_band")

    # --- low triggers (evaluated first; any one fires low) ---
    if not ing_present:
        return "low", "no ingredient list present"
    if nova_band == "low":
        # Classifier itself is low-confidence (name/category heuristic, no
        # corroborating ingredient evidence) — spec §2.3 low criterion (3).
        return "low", "nova classifier confidence band = low"

    # D5-dependent path (full rule) — only when D5D6 is ON and a profile exists.
    if disclosure_profile is not None:
        d5_band = disclosure_profile.get("d5_band")
        if d5_band in ("partial", "severe"):
            # closable gaps that could materially affect NOVA assignment
            return "low", f"d5_band={d5_band} (closable disclosure gaps)"
        # high requires: list present (checked) AND no severe band (checked) AND
        # the NOVA class is unambiguous from ingredient signals — single-ingredient
        # NOVA 1, or named additives (no bare generic G4 terms) with a clear pattern.
        single_ingredient = disclosure_profile.get("single_ingredient", False)
        generic_n = disclosure_profile.get("counts", {}).get("distinct_closable_classes", 0)
        bare_generic = generic_n > 0
        if (single_ingredient or not bare_generic) and nova_band == "high":
            return "high", "list present, no severe band, class unambiguous (D5 path)"
        return "medium", "list present, class plausible but not fully verifiable (D5 path)"

    # Two-signal fallback (D5D6 OFF) — ingredient list + classifier band only.
    if nova_band == "high":
        return "high", "list present + nova classifier band high (two-signal fallback)"
    return "medium", "list present, classifier band medium (two-signal fallback)"


def _d3_uncertainty_materiality(nova_level: int, confidence: str,
                                l3: dict, disclosure_profile) -> tuple[str, str]:
    """EV-042 bound_value_set_4 (NEW, TASK-181J/181K) — the material vs non-material test.

    Applies ONLY to the `medium` confidence band (high already scales 1.0 with no doubt
    to route; low already takes the 0.40 shrink regardless). For medium-confidence
    products, classify the unresolved/unknown signal as MATERIAL or NON-MATERIAL using
    observable inputs already computed by the engine.

    Returns (materiality, reason). materiality ∈ {"material","non_material"} for medium;
    None for high/low (no split applies). `disclosure_profile` is None when
    BARI_GLASSBOX_D5D6 is OFF → the two-signal fallback evaluates M1/M3/M4 only (omit M2).

    MATERIAL if ANY of:
      M1  the NOVA-deciding additive is a BARE-GENERIC additive term (D5 G4 detector hit)
          whose function class is itself the processed-vs-ultra-processed pivot — i.e. a
          present-but-unnamed NOVA-4 marker additive.
      M2  D5 band == "severe" (a severe-opaque panel cannot pin the read). [D5D6 only]
      M3  unresolved/unmatched ingredient-token fraction > 30% of the list, OR an unnamed
          compound ingredient ("תערובת"/"בתוספת...") that could carry NOVA-4 markers.
      M4  decisive worst-case test — hold the resolved portion's NOVA class fixed; assume
          the unknown is a NOVA-4 marker. If the class would FLIP given the rest of the
          list → material; if it would still HOLD → non-material.
    NON_MATERIAL if NONE of M1–M4 fire AND the visible signals already pin the read.
    """
    if confidence != "medium":
        return None, "materiality split applies to medium band only"

    reasons = []

    # --- signals from the D5 disclosure profile (full rule) ---
    has_bare_generic = False     # G4 detector — a bare-generic additive present-but-unnamed
    d5_severe = False
    has_unnamed_compound = False
    tokens_n = 0
    if disclosure_profile is not None:
        findings = disclosure_profile.get("findings", []) or []
        has_bare_generic = any(f.get("type") == "generic_additive" for f in findings)
        d5_severe = (disclosure_profile.get("d5_band") == "severe")
        has_unnamed_compound = any(f.get("type") == "compound" for f in findings)
        cnt = disclosure_profile.get("counts", {}) or {}
        # token count is reconstructable from the panel; recompute below from l3 too.

    # --- ingredient-list / unresolved-fraction (works in both full + fallback paths) ---
    ing_list = l3.get("ingredient_list") or []
    tokens_n = len(ing_list)
    # Unresolved-fraction proxy: matched/resolved tokens are those the taxonomy mapped.
    # l3 carries resolved-ingredient signals; treat ingredients with no L3 classification
    # match as unresolved. We approximate the unresolved set as tokens flagged unmatched
    # by the taxonomy layer (l3 'unmatched_ingredients') when present; else 0.
    unmatched = l3.get("unmatched_ingredients")
    if unmatched is None:
        # fall back to disclosure_profile findings count of bare-generic/compound as the
        # only observed "unresolved" markers (conservative — keeps small lists non-material).
        unresolved_n = (1 if has_bare_generic else 0) + (1 if has_unnamed_compound else 0)
    else:
        unresolved_n = len(unmatched)
    unresolved_frac = (unresolved_n / tokens_n) if tokens_n else 0.0

    # M1 — bare-generic NOVA-deciding additive present-but-unnamed.
    if has_bare_generic:
        reasons.append("M1 bare-generic NOVA-deciding additive (D5 G4 hit)")
    # M2 — D5 severe (D5D6 path only; omitted in two-signal fallback).
    if disclosure_profile is not None and d5_severe:
        reasons.append("M2 d5_band=severe")
    # M3 — large unresolved fraction OR an unnamed compound ingredient.
    if unresolved_frac > 0.30:
        reasons.append(f"M3 unresolved_frac={unresolved_frac:.2f}>0.30")
    if has_unnamed_compound:
        reasons.append("M3 unnamed compound ingredient (could carry NOVA-4 markers)")
    # M4 — worst-case NOVA-flip: assume the unknown is a NOVA-4 marker. If the product is
    # already classified NOVA 4, a NOVA-4 unknown cannot flip the class → does not fire on
    # its own. If the product sits at the NOVA 3↔4 pivot (NOVA 3 with a present-but-unnamed
    # additive marker), the worst-case unknown would flip 3→4 → material. The only direct
    # observable that lets a hidden NOVA-4 marker flip the class is an unresolved bare term
    # on a sub-NOVA-4 product; that is exactly M1/M3 above. So M4 fires when the class is
    # < 4 AND there is an unresolved/unnamed token (M1 or M3 trigger) that could be the
    # flipping marker. When the resolved list already pins NOVA 4, or the only unknowns are
    # peripheral named/whole-food tokens (no M1/M3 trigger), the worst case does not flip.
    m4_flip = (nova_level is not None and nova_level < 4
               and (has_bare_generic or has_unnamed_compound or unresolved_frac > 0.30))
    if m4_flip:
        reasons.append("M4 worst-case NOVA-4 unknown would flip class (sub-NOVA-4 + unresolved)")

    if reasons:
        return "material", "; ".join(reasons)
    return "non_material", ("visible signals pin the NOVA read; unresolved terms peripheral "
                            "(no M1–M4 trigger)")


def _d3_modifier_score(nova_level: int, confidence: str, materiality: str = None) -> float:
    """EV-042 bound_value_set_2 (revised) — pull-toward-neutral confidence-scaled modifier.
    modifier_score = 50 + (base_score - 50) * confidence_scale(confidence, materiality)."""
    base = NOVA_PROCESSING_SCORES.get(nova_level, W4_NEUTRAL)
    scale = _w4_confidence_scale(confidence, materiality)
    return round(W4_NEUTRAL + (base - W4_NEUTRAL) * scale, 2)


def _d3_scaled_cap(base_cap: float, confidence: str, materiality: str = None) -> float:
    """EV-042 bound_value_set_2 (revised, TASK-181J) — cap-scaling, now BOUND:

        cap_effective = 100 − (100 − base_cap) × confidence_scale(confidence, materiality)

    Same scale as the score formula. A PROCESSING_LOAD cap is a ceiling; under uncertainty
    it is relaxed toward 100 (no-cap). Worked for the NOVA-4 cap (base 68):
      high            → 100−(100−68)×1.0  = 68    (today's cap, identical)
      medium-material → 100−32×0.70       = 77.6
      medium-non-mat. → 100−32×1.0        = 68    (cap unchanged — non-material loosens nothing)
      low             → 100−32×0.40       = 87.2
    Same form for the NOVA-3 cap (base 87). Material gaps loosen score AND cap toward
    neutral; non-material gaps loosen neither. Returns a float ceiling (callers round/int)."""
    scale = _w4_confidence_scale(confidence, materiality)
    return round(100 - (100 - base_cap) * scale, 2)


def _d3_processing_signal(nova_level: int, confidence: str, modifier_score: float,
                          modifier_note: str, uncertainty_materiality: str = None) -> dict:
    """EV-042 (revised) / spec §2.2 — the d3_processing_signal struct emitted on the
    professional/internal trace surface. `modifier` is the signed delta from the
    neutral 50 anchor (negative = pull below neutral, i.e. a processing penalty).
    `uncertainty_materiality` (new in the TASK-181J revision) carries the medium-band
    material/non_material verdict (None for high/low bands — no split applies)."""
    base = NOVA_PROCESSING_SCORES.get(nova_level, W4_NEUTRAL)
    if confidence == "low":
        note_he = W4_NOTE_HE_C
        note_he_mobile = W4_NOTE_HE_C_MOBILE
    elif nova_level >= 3:
        note_he = W4_NOTE_HE_B
        note_he_mobile = W4_NOTE_HE_B
    elif nova_level == 1:
        note_he = W4_NOTE_HE_A
        note_he_mobile = W4_NOTE_HE_A
    else:
        # NOVA 2, non-low confidence: positive-leaning but not the NOVA-1 reference
        # claim. Use the hedged B framing direction is wrong (B is negative); A
        # overclaims "minimally processed". NOVA 2 carries no co-signed string, so
        # emit no consumer note (struct still carries the numeric signal).
        note_he = None
        note_he_mobile = None
    return {
        "nova_class": nova_level,
        "confidence": confidence,
        "uncertainty_materiality": uncertainty_materiality,
        "population_correlation": W4_POPULATION_CORRELATION.get(nova_level),
        "modifier": round(modifier_score - W4_NEUTRAL, 2),
        "modifier_note": modifier_note,
        "note_he": note_he,
        "note_he_mobile": note_he_mobile,
    }


# ---------------------------------------------------------------------------
# TASK-179P — DIAAS protein-quality detector (Glass Box W1.5).
# Deterministic detector over the ingredient text. Returns Rule A (D2 credit)
# and Rule B (D5 disclosure-gap flag) signals.
# EV-040 (bsip2_evidence_registry). Source: diaas_source_table_v1 Phase 2.
# ONLY invoked when BARI_GLASSBOX_W15 is ON (call site is flag-guarded).
# ---------------------------------------------------------------------------

# Hebrew final→medial normalization shared with the D5 detector (_GLASSBOX_FINAL_MAP
# is defined below in the D5 section). We define a standalone helper here so the DIAAS
# detector can be called independently of the D5 path.
_DIAAS_FINAL_MAP = str.maketrans({"ם": "מ", "ן": "נ", "ץ": "צ", "ף": "פ", "ך": "כ"})


def _diaas_normalize(s: str) -> str:
    """Normalize Hebrew final-letter forms + collapse whitespace for DIAAS matching."""
    if not s:
        return ""
    s = s.replace("\n", " ").replace("\r", " ").replace(".n", " ")
    s = s.translate(_DIAAS_FINAL_MAP)
    s = _re.sub(r"\s+", " ", s)
    return s.strip().lower()


def detect_diaas_signal(ingredient_text: str) -> dict:
    """TASK-179P — detect DIAAS protein-quality signals from ingredient text.

    Returns:
        {
            "rule_a_fired": bool,        # True if a complete-protein whitelist source found
            "rule_a_source": str|None,   # The matched source label
            "rule_b_fired": bool,        # True if a disclosure-gap trigger found
            "rule_b_reason": str|None,   # Why Rule B fired
        }

    Rule A fires at most ONCE per product (guard against double-application).
    Rule B fires when the panel declares a generic protein term without naming a
    specific complete source.

    ONLY called when BARI_GLASSBOX_W15 is ON. Caller is responsible for the flag guard.
    """
    if not ingredient_text:
        return {
            "rule_a_fired": False, "rule_a_source": None,
            "rule_b_fired": False, "rule_b_reason": None,
        }

    norm = _diaas_normalize(ingredient_text)

    # Rule A — scan complete-protein whitelist (fire once only).
    rule_a_fired = False
    rule_a_source = None
    for pattern, label in DIAAS_COMPLETE_SOURCES:
        if _diaas_normalize(pattern) in norm:
            rule_a_fired = True
            rule_a_source = label
            break   # fire-once guard: stop at first match

    # Rule B — scan disclosure-gap triggers.
    # Rule B fires when a generic protein trigger is present AND Rule A did NOT fire
    # (Rule A means the label did name a complete source; no disclosure gap for the
    # credit-eligible component). If only generic terms appear (Rule A not fired) the
    # protein quality cannot be evaluated — that is the D5 gap.
    # Additional Rule B cases per EV-040 Phase 2 spec:
    #   - Pea + rice both appear but no proportions declared → blend ambiguity
    #   - Generic "מי גבינה" (not "חלבון מי גבינה") in a protein-featured context
    rule_b_fired = False
    rule_b_reason = None

    if not rule_a_fired:
        # Check explicit generic-protein trigger terms
        for pattern, reason in DIAAS_DISCLOSURE_GAP_TRIGGERS:
            if _diaas_normalize(pattern) in norm:
                rule_b_fired = True
                rule_b_reason = reason
                break

        # Pea + rice blend without proportions declared (canonical D5 gap, EV-040 §3.2)
        if not rule_b_fired:
            _pea_norm = _diaas_normalize("חלבון אפונה")
            _rice_norm = _diaas_normalize("חלבון אורז")
            _pea_en = "pea protein"
            _rice_en = "rice protein"
            pea_present  = _pea_norm in norm or _pea_en in norm
            rice_present = _rice_norm in norm or _rice_en in norm
            if pea_present and rice_present:
                rule_b_fired = True
                rule_b_reason = "pea_rice_blend_no_proportions"

    return {
        "rule_a_fired": rule_a_fired,
        "rule_a_source": rule_a_source,
        "rule_b_fired": rule_b_fired,
        "rule_b_reason": rule_b_reason,
    }


# ---------------------------------------------------------------------------
# TASK-179S — D4 additive tier detector (Glass Box W2; library extended in W3/TASK-181D).
# Scans the ingredient text for each additive in GLASSBOX_W2_ADDITIVES (20 in W2,
# extended to the full 36-additive tiered library in W3). Returns a list of matched
# findings (one per distinct detected additive, in first-occurrence order). No score
# movement — presentation-only (annotate-only).
# Source: additive_tiered_library_v1.md (EV-043); identity additive_library_expanded_v1.md.
# No detector LOGIC change in W3 — the loop iterates whatever the lookup table holds.
# ONLY called when BARI_GLASSBOX_W2 is ON (call site is flag-guarded).
# ---------------------------------------------------------------------------

# Hebrew final→medial normalization for D4 (same map as _DIAAS_FINAL_MAP).
_D4_FINAL_MAP = str.maketrans({"ם": "מ", "ן": "נ", "ץ": "צ", "ף": "פ", "ך": "כ"})


def _d4_normalize(s: str) -> str:
    """Normalize Hebrew final-letter forms + collapse whitespace for D4 matching."""
    if not s:
        return ""
    s = s.replace("\n", " ").replace("\r", " ").replace(".n", " ")
    s = s.translate(_D4_FINAL_MAP)
    s = _re.sub(r"\s+", " ", s)
    return s.strip().lower()


def detect_additives_d4(ingredient_text: str) -> list:
    """TASK-179S — detect D4 additive tier findings from ingredient text.

    Scans for each additive in GLASSBOX_W2_ADDITIVES (36 in the W3 tiered library) using:
      (a) E-number pattern: E{digits}, E-{digits}, or ה-{digits} (with optional space)
      (b) Hebrew name variants from match_patterns_he

    Returns a list of findings (one per distinct matched additive, first-occurrence order):
        [
            {
                "e_number": "E330",
                "name_he": "חומצת לימון",
                "tier": "functional",
                "function_he": "...",
                "match_source": "e_number" | "name_he" | "both",
            },
            ...
        ]

    Deduplicates: same additive matched by both E-number and name → one entry,
    match_source="both". Returns [] for empty or None ingredient_text.

    ONLY called when BARI_GLASSBOX_W2 is ON. Caller is responsible for the flag guard.
    """
    if not ingredient_text:
        return []

    norm = _d4_normalize(ingredient_text)
    # Track (e_number, first_occurrence_pos, match_source) per additive
    findings_map: dict = {}   # e_number → {entry, pos, match_source}

    for e_num, entry in GLASSBOX_W2_ADDITIVES.items():
        # Extract the numeric portion (E450, E472e → digits are 450, 472)
        # Match the full e_num string in various formats.
        e_bare = e_num.lstrip("E")   # e.g. "330", "472e", "450"

        # Build E-number patterns: E330, E-330, ה-330, with optional space before digits.
        # For composite E-numbers like E472e we match just the numeric part (E472 / E-472).
        e_digits = _re.match(r"(\d+)", e_bare)
        e_num_str = e_digits.group(1) if e_digits else e_bare

        e_patterns = [
            f"e{e_bare.lower()}",          # e330 / e472e
            f"e-{e_num_str}",              # e-330
            f"e {e_num_str}",              # e 330 (stray space)
            f"ה-{e_num_str}",             # ה-330 (Hebrew E-number citation)
        ]

        # TASK-181D digit-boundary guard: an E-number match must NOT be immediately
        # followed by another digit, otherwise "e141" falsely matches inside "e1412"
        # (E141 copper chlorophylls vs E1412 modified starch — both now in the table).
        # Find ALL occurrences of each pattern and accept the first one that is not
        # mid-number. Letter suffixes (E472e) and "i" roman tails (E450iii) are fine.
        e_match_pos = None
        for pat in e_patterns:
            start = 0
            while True:
                idx = norm.find(pat, start)
                if idx == -1:
                    break
                tail_pos = idx + len(pat)
                tail_char = norm[tail_pos] if tail_pos < len(norm) else ""
                if not tail_char.isdigit():   # reject only when the next char is a digit
                    if e_match_pos is None or idx < e_match_pos:
                        e_match_pos = idx
                    break
                start = idx + 1

        # Hebrew name matching (match_patterns_he from the entry)
        name_match_pos = None
        for pattern in entry.get("match_patterns_he", []):
            norm_pat = _d4_normalize(pattern)
            if not norm_pat:
                continue
            idx = norm.find(norm_pat)
            if idx != -1:
                if name_match_pos is None or idx < name_match_pos:
                    name_match_pos = idx

        if e_match_pos is None and name_match_pos is None:
            continue   # additive not found

        # Determine first occurrence position and match_source
        if e_match_pos is not None and name_match_pos is not None:
            first_pos = min(e_match_pos, name_match_pos)
            match_source = "both"
        elif e_match_pos is not None:
            first_pos = e_match_pos
            match_source = "e_number"
        else:
            first_pos = name_match_pos
            match_source = "name_he"

        findings_map[e_num] = {
            "e_number": e_num,
            "name_he": entry["name_he"],
            "tier": entry["tier"],
            "function_he": entry["function_he"],
            "match_source": match_source,
            "_pos": first_pos,
        }

    # Sort by first-occurrence position in the ingredient string, then build result list.
    sorted_findings = sorted(findings_map.values(), key=lambda f: f["_pos"])
    return [
        {k: v for k, v in f.items() if k != "_pos"}
        for f in sorted_findings
    ]


# ---------------------------------------------------------------------------
# TASK-179G — D5 disclosure-gap detector (Glass Box).
# Deterministic detector over the RAW BSIP0 panel (ingredients_raw). Emits a
# disclosure profile (which gap types fired) + a 4-level D5-band that feeds D6.
# Per Q2/DEC-006 it NEVER deducts grade points and never attributes intent.
# Spec: d5_d6_rule_spec_v1.md §1. EV-035 / EV-036.
# ONLY invoked when GLASSBOX_D5D6_ON (call site is flag-guarded).
# ---------------------------------------------------------------------------

# Hebrew final→medial letter normalization (P2; same trap as EV-029).
_GLASSBOX_FINAL_MAP = str.maketrans({"ם": "מ", "ן": "נ", "ץ": "צ", "ף": "פ", "ך": "כ"})


def _glassbox_normalize(s: str) -> str:
    """P2 — normalize Hebrew final-letter forms + collapse stray whitespace/newlines."""
    if not s:
        return ""
    s = s.replace("\n", " ").replace("\r", " ")
    s = s.replace(".n", " ")          # observed scrape artifact (".nמכיל")
    s = s.translate(_GLASSBOX_FINAL_MAP)
    s = _re.sub(r"\s+", " ", s)
    return s.strip()


def _glassbox_truncate_bleed(raw: str) -> str:
    """P1 — strip the nutrition-table bleed; everything at/after an anchor is not ingredients."""
    cut = len(raw)
    for anchor in GLASSBOX_NUTRITION_BLEED_ANCHORS:
        a = _glassbox_normalize(anchor)
        idx = raw.find(a)
        if idx != -1:
            cut = min(cut, idx)
    return raw[:cut].strip(" ,")


def _glassbox_split_tokens(s: str) -> list:
    """Split an ingredient string on commas that are OUTSIDE parentheses."""
    tokens, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            tokens.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        tokens.append("".join(cur).strip())
    return [t for t in tokens if t]


def _glassbox_term_is_bare(norm_panel: str, term_norm: str) -> bool:
    """A class term is 'bare' (gap) when it is NOT immediately followed by '(' or ':'
    introducing a specific name/E-code (after optional whitespace)."""
    bare = False
    start = 0
    while True:
        idx = norm_panel.find(term_norm, start)
        if idx == -1:
            break
        after = norm_panel[idx + len(term_norm):].lstrip()
        if not after[:1] in ("(", ":"):
            bare = True
        start = idx + len(term_norm)
    return bare


def compute_disclosure_profile(product: dict, signals: dict, nova_result: dict) -> dict:
    """D5 — disclosure profile + D5-band over the raw BSIP0 panel. Spec §1."""
    nn = product.get("normalized_nutrition_per_100g") or {}
    raw = (product.get("ingredients_raw")
           or product.get("ingredients_text_he")
           or "")
    if not raw and product.get("ingredients_list"):
        raw = ", ".join(product["ingredients_list"])

    # P1 truncate bleed, P2 normalize.
    norm_raw = _glassbox_normalize(raw)
    panel = _glassbox_truncate_bleed(norm_raw)

    # P3 — empty/absent panel: do not run gap detection (already-counted missing-ingredient).
    # The spec's "< 15 non-space chars" rule targets blank/garbage panels. A coherent
    # single-ingredient whole food (e.g. אגוזי מלך = 8 chars) must NOT be read as absent —
    # single-ingredient protection (§1.2 G1) requires it to resolve to the FULL band, not
    # withhold. So the panel is ABSENT only when it is both sub-threshold AND lacks a
    # coherent ingredient token (≥2 Hebrew/Latin letters). This keeps the genuinely empty
    # case in P3 while protecting short clean whole foods.
    _toks = _glassbox_split_tokens(panel)
    _has_coherent_token = any(len(_re.sub(r"[^\w]", "", t)) >= 2 for t in _toks)
    panel_present = (len(panel.replace(" ", "")) >= 15) or _has_coherent_token
    findings = []
    endemic_flavoring = False
    protein_to_d2 = []

    if not panel_present:
        return {
            "panel_present": False, "single_ingredient": False, "findings": [],
            "counts": {"structural_n": 0, "closable_n": 0, "endemic_flavoring": False,
                       "protein_source_to_d2": []},
            "d5_band": "severe", "d5_completeness": 0,
        }

    tokens = _glassbox_split_tokens(panel)
    single_ingredient = len(tokens) == 1

    # --- G1 undisclosed proportions (structural). Single-ingredient protection. ---
    if not single_ingredient:
        pct_n = len(_re.findall(r"\d+(?:[.,]\d+)?\s*%", panel))
        lead = tokens[0] if tokens else ""
        lead_has_pct = bool(_re.search(r"\d+(?:[.,]\d+)?\s*%", lead))
        if len(tokens) >= 2 and (pct_n == 0 or not lead_has_pct):
            findings.append({"type": "proportions", "severity": "structural",
                             "tokens_n": len(tokens), "pct_n": pct_n})

    # --- G4 generic additive class without E-code/name (closable) + endemic flavoring ---
    for term in GLASSBOX_GENERIC_ADDITIVE_TERMS:
        tn = _glassbox_normalize(term)
        if tn in panel and _glassbox_term_is_bare(panel, tn):
            findings.append({"type": "generic_additive", "term": term, "severity": "closable"})
    for term in GLASSBOX_ENDEMIC_FLAVORING_TERMS:
        tn = _glassbox_normalize(term)
        if tn in panel:
            endemic_flavoring = True
            break

    # --- G2 compound without internal breakdown (closable) ---
    for term in GLASSBOX_COMPOUND_TERMS:
        tn = _glassbox_normalize(term)
        start = 0
        while True:
            idx = panel.find(tn, start)
            if idx == -1:
                break
            after = panel[idx + len(tn):].lstrip()
            if not after[:1] == "(":
                findings.append({"type": "compound", "severity": "closable", "token": term})
                break
            start = idx + len(tn)

    # --- G3 protein blend (structural) / collagen-gelatin → D2 signal (not a gap) ---
    blend_fired = False
    for term in GLASSBOX_PROTEIN_BLEND_TERMS:
        if _glassbox_normalize(term) in panel:
            named = any(_glassbox_normalize(s) in panel for s in GLASSBOX_PROTEIN_NAMED_SOURCES)
            if not named:
                findings.append({"type": "protein_source", "subtype": "blend_unspecified",
                                 "severity": "structural"})
                blend_fired = True
                break
    for term in GLASSBOX_PROTEIN_INCOMPLETE_NAMED:
        if _glassbox_normalize(term) in panel:
            protein_to_d2.append(term)
            findings.append({"type": "protein_source", "subtype": "incomplete_named",
                             "note": "feeds D2, not a gap"})
            break

    # --- G5 declared-quantity-missing (names legacy six; sat-fat/sugar = NEW closable) ---
    legacy_six = {"energy_kcal", "protein_g", "carbohydrates_g", "fat_g",
                  "dietary_fiber_g", "sodium_mg"}
    for field in legacy_six:
        if nn.get(field) is None:
            findings.append({"type": "missing_field", "field": field, "severity": "structural"})
    # sat-fat / sugar absence — NOT in the legacy −10/−5 map → new closable gap.
    if nn.get("fat_saturated_g") is None:
        findings.append({"type": "missing_field", "field": "fat_saturated_g",
                         "severity": "closable"})
    if nn.get("sugars_g") is None:
        findings.append({"type": "missing_field", "field": "sugars_g", "severity": "closable"})

    # --- Band assignment (after single-ingredient + endemic-flavoring exclusions) ---
    band_findings = [f for f in findings
                     if f.get("subtype") != "incomplete_named"]   # D2 signal, not band-raising
    structural_n = sum(1 for f in band_findings if f.get("severity") == "structural")
    closable = [f for f in band_findings if f.get("severity") == "closable"]
    closable_n = len(closable)
    distinct_closable_classes = len(set(
        (f.get("type"), f.get("term") or f.get("field") or f.get("token")) for f in closable))

    if single_ingredient or not band_findings:
        d5_band, d5_completeness = "full", 95
    elif closable_n == 0:
        d5_band, d5_completeness = "minor", 80
    else:
        severe = (distinct_closable_classes >= 3) or (blend_fired and closable_n >= 2)
        if severe:
            d5_band, d5_completeness = "severe", 40
        else:
            d5_band, d5_completeness = "partial", 57

    return {
        "panel_present": True,
        "single_ingredient": single_ingredient,
        "findings": findings,
        "counts": {"structural_n": structural_n, "closable_n": closable_n,
                   "distinct_closable_classes": distinct_closable_classes,
                   "endemic_flavoring": endemic_flavoring,
                   "protein_source_to_d2": protein_to_d2},
        "d5_band": d5_band,
        "d5_completeness": d5_completeness,
    }


# ---------------------------------------------------------------------------
# Confidence calculation
# ---------------------------------------------------------------------------

def compute_confidence(product: dict, signals: dict, cat_result: dict, nova_result: dict,
                       disclosure_profile: dict = None) -> dict:
    """Compute BSIP2 confidence score (0-100) from multiple factors.

    TASK-179G (Glass Box D6): when GLASSBOX_D5D6_ON and a disclosure_profile is supplied,
    adds the SINGLE new D5-band reduction term (EV-037) and derives the three-state gate
    (unconstrained / demote / withhold→null, EV-038). disclosure_profile=None or flag OFF
    → behavior is byte-identical to today (no new term, no gate fields).
    """
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

    # TASK-179G / EV-037 — Glass Box D5-band → D6 confidence reduction (the ONLY new
    # term). Structural-only gaps (full/minor) do not erode confidence; closable opacity
    # (partial −10 / severe −20) does. NO double-count: the legacy missing-field
    # deductions above already covered G5's legacy six — D5 only NAMES them, it does NOT
    # re-deduct (spec §1.2 G5 / §2.1). Guarded by the flag → OFF is byte-identical.
    d5_band = None
    if GLASSBOX_D5D6_ON and disclosure_profile is not None:
        d5_band = disclosure_profile.get("d5_band")
        d5_red = GLASSBOX_D5_CONF_REDUCTION.get(d5_band, 0)
        if d5_red:
            deduct(d5_red, f"d5_disclosure={d5_band} (closable gaps)")

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

    result = {
        "confidence_score": score,
        "confidence_band": band,
        "confidence_ceiling": ceiling,
        "confidence_reductions": reductions,
    }

    # TASK-179G / EV-038 — D6 gate state machine (extends the ceiling-only outcome into
    # unconstrained · demote · withhold→null). Only computed under the flag; OFF leaves
    # the result dict exactly as today.
    if GLASSBOX_D5D6_ON and disclosure_profile is not None:
        panel_present = disclosure_profile.get("panel_present", True)
        context_flag = (signals.get("_context_flag")
                        if isinstance(signals, dict) else None)
        panel_absent = (not panel_present) or context_flag == "no_nutrition_data"
        b_severe = (d5_band == "severe")
        floor_failure = panel_absent or (score < GLASSBOX_NULL_FLOOR and b_severe)
        if floor_failure:
            gate_state = "withhold"
        elif score < GLASSBOX_DEMOTE_CEILING_BOUND:
            gate_state = "demote"
        else:
            gate_state = "unconstrained"
        result["d5_band"] = d5_band
        result["d6_gate_state"] = gate_state
        result["d6_panel_absent"] = panel_absent

    return result


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

def score_processing_quality(nova_level: int, w4_confidence: str = None,
                             w4_materiality: str = None) -> tuple[float, str]:
    # TASK-181G / TASK-181K / EV-042 (revised) — Glass Box W4 D3 de-moralization. When the
    # flag is ON the caller passes a w4_confidence band (and, for the medium band, a
    # w4_materiality verdict) and the fixed NOVA_PROCESSING_SCORES lookup is replaced by
    # the confidence-scaled pull-to-neutral modifier (bound_value_set_2 revised).
    # medium-NON-MATERIAL → scale 1.0 → score does NOT move (identical to the lookup).
    # Flag OFF (w4_confidence is None) → the current lookup runs verbatim (byte-identical).
    if BARI_GLASSBOX_W4 and w4_confidence is not None:
        base = NOVA_PROCESSING_SCORES.get(nova_level, W4_NEUTRAL)
        scale = _w4_confidence_scale(w4_confidence, w4_materiality)
        score = _d3_modifier_score(nova_level, w4_confidence, w4_materiality)
        note = (f"W4 D3 de-moralization: NOVA {nova_level} base={base} × "
                f"confidence_scale({w4_confidence}"
                f"{'/' + w4_materiality if w4_materiality else ''})={scale} "
                f"→ 50+(base-50)×scale = {score} (EV-042 revised, TASK-181J)")
        return score, note
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
                         cat_confidence: float, eval_status: dict,
                         w4_confidence: str = None, w4_materiality: str = None) -> dict:
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
    # TASK-181G / EV-042 — Glass Box W4 removes NOVA-class amplification of HP
    # penalties (spec §1.3 O3 / §4.1 item 3). The HP detection signals fire on their
    # own direct observational criteria at full magnitude; their size no longer
    # depends on NOVA class. Flag ON (w4_confidence is not None) → weight = 1.0 for
    # every class. Flag OFF → the current NOVA_HP_WEIGHTS scaling runs verbatim.
    if BARI_GLASSBOX_W4 and w4_confidence is not None:
        hp_nova_weight = 1.0
    else:
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

    # TASK-181G / TASK-181K / EV-042 (revised) — Glass Box W4 confidence-scales the two
    # NOVA-driven PROCESSING_LOAD caps via _d3_scaled_cap, using the SAME scale as the
    # score (bound_value_set_2 revised: cap_effective = 100 − (100−base_cap) × scale).
    # The scale now depends on materiality: medium-non-material → scale 1.0 → cap
    # UNCHANGED (a non-material gap does not loosen the ceiling). The additive-marker caps
    # are direct-observation, NOT NOVA-driven, so they are left unchanged. Flag OFF → both
    # caps run at 68 / 87 verbatim (byte-identical).
    _w4_on = BARI_GLASSBOX_W4 and w4_confidence is not None
    _nova3_cap = next(c for rule, _, c in PROCESSING_CAPS if rule == "NOVA_PROXY_3_PROCESSED")
    if _w4_on:
        _nova4_cap_val = _d3_scaled_cap(68, w4_confidence, w4_materiality)
        _nova3_cap_val = _d3_scaled_cap(_nova3_cap, w4_confidence, w4_materiality)
    else:
        _nova4_cap_val = 68
        _nova3_cap_val = _nova3_cap
    check_cap("NOVA_PROXY_4_ULTRA_PROCESSED", nova_level == 4, _nova4_cap_val, proc_caps_fired)
    check_cap("ADDITIVE_MARKERS_5_PLUS",      additive_ct >= 5, 60, proc_caps_fired)
    check_cap("ADDITIVE_MARKERS_3_PLUS",      3 <= additive_ct < 5, 72, proc_caps_fired)
    check_cap("NOVA_PROXY_3_PROCESSED",       nova_level == 3, _nova3_cap_val, proc_caps_fired)

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
    # TASK-179G — Glass Box D5 detector runs (flag-guarded) over the raw BSIP0 panel and
    # feeds D6. With the flag OFF the detector is NOT invoked and compute_confidence runs
    # exactly as today (disclosure_profile stays None → byte-identical).
    disclosure_profile = None
    if GLASSBOX_D5D6_ON:
        disclosure_profile = compute_disclosure_profile(product, signals, nova_result)
        # surface the evaluation-scope context flag to the gate (panel_absent input)
        if isinstance(signals, dict):
            signals["_context_flag"] = eval_result.get("context_flag")
    conf_result = compute_confidence(product, signals, cat_result, nova_result,
                                     disclosure_profile)
    confidence  = conf_result["confidence_score"]

    # Stage 2: Structural emptiness gate
    se_result = detect_structural_emptiness(nn, category, l3)

    # Stage 3: Dimension scoring
    has_fortification = l3.get("has_fortification", False)
    has_fermentation  = l3.get("has_fermentation", False)

    # TASK-181G / TASK-181K / EV-042 (revised, TASK-181J) — Glass Box W4 D3
    # de-moralization. Compute the NOVA-assignment confidence ONCE (keyed to ingredient-
    # evidence quality, not the NOVA class), then — for the medium band only — compute the
    # uncertainty materiality (bound_value_set_4, M1–M4). Thread both into the D3 dimension
    # score AND the NOVA-driven PROCESSING_LOAD caps + HP de-amplification. The doubt for
    # the non-material / low-confidence cases routes to D6 confidence (bound_value_set_5:
    # non-material −5, low-confidence −10; both max-combined with any D5 term, never summed).
    # Flag OFF → w4_confidence stays None → every W4 call site falls back to the current
    # behavior (byte-identical).
    w4_confidence = None
    w4_conf_note = None
    w4_materiality = None
    w4_low_confidence_nova = False
    w4_nonmaterial_gap = False
    # TASK-181M / F3 — track the magnitude of the d3_nonmaterial_gap term that was ACTUALLY
    # applied to the confidence accumulator (after max-combine with D5). The insufficient_data
    # gate (Stage 9b) uses this to ensure a non-material peripheral dent can lower the displayed
    # confidence WITHIN the graded band but is never the term that crosses a product into
    # insufficient_data. ONLY the d3_nonmaterial_gap (−5) term is tracked/guarded here — the
    # low-confidence-NOVA (−10) and D5 terms are genuine data-poverty signals and are NOT
    # rescued, so a truly data-poor product still reaches insufficient_data via those terms.
    w4_nonmaterial_applied_increment = 0
    if BARI_GLASSBOX_W4:
        w4_confidence, w4_conf_note = _d3_compute_confidence(nova_result, l3, disclosure_profile)
        # bound_value_set_4 — materiality applies to the medium band only (None otherwise).
        w4_materiality, w4_materiality_note = _d3_uncertainty_materiality(
            nova_level, w4_confidence, l3, disclosure_profile)

        # bound_value_set_5 — the D3→D6 confidence ladder. Both terms act THROUGH
        # confidence only (Q2 firewall), are gated by the flag, and are MAX-combined with
        # any D5 disclosure reduction already applied for the same unresolved token (never
        # summed). We implement max-combine by adding only the increment of the D3 term
        # beyond the already-applied D5 magnitude, so the net effect == max(d3, d5).
        _d5_applied_mag = 0
        for _r in conf_result.get("confidence_reductions", []):
            if "d5_disclosure" in _r.get("factor", ""):
                _d5_applied_mag = max(_d5_applied_mag, abs(_r.get("reduction", 0)))

        _w4_d6_target = 0
        _w4_d6_reason = None
        if w4_confidence == "low":
            # Spec §2.6 — on insufficient ingredient data D3 does NOT invent a NOVA class:
            # confidence=low, score pulled toward neutral (handled by the modifier formula),
            # and a low_confidence_nova signal routes to D6 at −10 (bound_value_set_5),
            # max-combined with any D5 term. Skip if an equivalent nova_confidence=low term
            # was already deducted upstream.
            w4_low_confidence_nova = True
            _already_low = any("nova_confidence=low" in r.get("factor", "")
                               for r in conf_result.get("confidence_reductions", []))
            if not _already_low:
                _w4_d6_target = W4_D6_LOW_CONFIDENCE_DEDUCTION   # 10
                _w4_d6_reason = ("w4_low_confidence_nova (D3 → D6 −10, EV-042 "
                                 "bound_value_set_5; max-combined with D5)")
        elif w4_confidence == "medium" and w4_materiality == "non_material":
            # medium-NON-MATERIAL → D3 score does NOT move; the peripheral unknown surfaces
            # as a small confidence dent only (−5, half the D5 partial term).
            w4_nonmaterial_gap = True
            _w4_d6_target = W4_D6_NONMATERIAL_DEDUCTION          # 5
            _w4_d6_reason = ("d3_nonmaterial_gap (peripheral unresolved term; processing "
                             "read pinned) (D3 → D6 −5, EV-042 bound_value_set_5; "
                             "max-combined with D5)")

        # Apply the max-combined increment (never sum). If D5 already deducted >= the D3
        # target for the same token, the D3 term adds nothing (max already reached).
        _w4_increment = max(0, _w4_d6_target - _d5_applied_mag)
        if _w4_increment > 0:
            conf_result["confidence_score"] = max(0, conf_result["confidence_score"] - _w4_increment)
            conf_result.setdefault("confidence_reductions", []).append(
                {"factor": _w4_d6_reason, "reduction": -_w4_increment})
            # TASK-181M / F3 — record ONLY the non-material gap increment for the gate guard.
            # (The low-confidence-NOVA term is intentionally NOT recorded → not gate-guarded.)
            if w4_nonmaterial_gap:
                w4_nonmaterial_applied_increment = _w4_increment
            # Re-derive the ceiling/band from the adjusted score so the downstream ceiling
            # read (Stage 9) sees it.
            _cs = conf_result["confidence_score"]
            # TASK-181M / F3 — band-floor for the non-material dent. If the ONLY reason the
            # adjusted score fell below the insufficient boundary (=40) is the d3_nonmaterial_gap
            # (−5) term — i.e. adding that increment back would leave it at/above 40 — the band
            # must not drop to "insufficient" (which would both flip the grade label AND swap the
            # ceiling 75→50, potentially moving the score). It floors at "low" so the dent shows
            # as reduced confidence WITHIN the graded band, not as a label/ceiling cut. Genuine
            # low-confidence-NOVA / D5-driven below-40 cases are NOT rescued (their increment is
            # not added back here), so a truly data-poor product still drops to insufficient.
            _w4_band_floor_low = (
                w4_nonmaterial_gap and _w4_increment > 0
                and _cs < 40 and (_cs + _w4_increment) >= 40)
            if _cs >= 80:
                conf_result["confidence_band"], conf_result["confidence_ceiling"] = "high", None
            elif _cs >= 60:
                conf_result["confidence_band"], conf_result["confidence_ceiling"] = "medium", None
            elif _cs >= 40 or _w4_band_floor_low:
                conf_result["confidence_band"], conf_result["confidence_ceiling"] = "low", CONFIDENCE_LOW_CEILING
            else:
                conf_result["confidence_band"], conf_result["confidence_ceiling"] = "insufficient", CONFIDENCE_INSUFFICIENT_CEILING
            confidence = _cs  # keep the local in sync with the adjusted accumulator

    pq_score,  pq_note  = score_processing_quality(nova_level, w4_confidence, w4_materiality)
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

    # TASK-179P — DIAAS W1.5 Rule A + Rule B (flag-guarded: BARI_GLASSBOX_W15).
    # Flag OFF → dim_scores is unchanged and no diaas_ keys are added to result (byte-identical).
    # Flag ON  → Rule A: +3 to protein_quality (D2), capped at DIAAS_D2_SCORE_CAP (100).
    #             Rule B: d5_protein_disclosure_gap flag added to trace (D5 annotation only).
    diaas_result = None
    diaas_d2_credit_applied = 0
    diaas_d5_disclosure_gap = False
    if BARI_GLASSBOX_W15:
        _ing_text = (
            product.get("ingredients_raw")
            or product.get("ingredients_text_he")
            or ""
        )
        if not _ing_text and product.get("ingredients_list"):
            _ing_text = ", ".join(product["ingredients_list"])
        diaas_result = detect_diaas_signal(_ing_text)
        if diaas_result["rule_a_fired"]:
            _old_prq = dim_scores["protein_quality"]
            _new_prq = round(min(DIAAS_D2_SCORE_CAP, _old_prq + DIAAS_D2_CREDIT), 1)
            dim_scores["protein_quality"] = _new_prq
            dim_notes["protein_quality"] = (
                dim_notes["protein_quality"]
                + f" [W15 Rule A: +{DIAAS_D2_CREDIT} D2 credit"
                f" ({diaas_result['rule_a_source']}), {_old_prq}→{_new_prq}]"
            )
            diaas_d2_credit_applied = DIAAS_D2_CREDIT
        if diaas_result["rule_b_fired"]:
            diaas_d5_disclosure_gap = True

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
        # TASK-169D ship-prep: when the yogurt-trim construct is ON, drop serving-suggestion
        # marketing-prose ingredient items before the flavored scan. BSIP1 falls back to
        # marketing copy when BSIP0 is absent and can mis-capture a serving suggestion
        # ("...בתוספת פירות... דבש מתוק או פשוט ככה...") as an ingredient item, naming an
        # add-on the product does NOT contain (e.g. דבש/honey) and falsely tripping this
        # exclusion. The NAME is always scanned (real flavored SKUs carry the flavor in the
        # name); only marketing-prose ingredient items are excluded. Real seasoned variants
        # (e.g. tzatziki — שום/שמיר in a genuine ingredient list) carry no prose markers and
        # are unaffected. Fully gated behind RECAL_P0_YOGURT_TRIM → no effect when OFF.
        if RECAL_P0_YOGURT_TRIM:
            _ing_items = l3.get("ingredient_list") or []
            _real_items = [it for it in _ing_items
                           if not any(pm in it for pm in SERVING_SUGGESTION_PROSE_MARKERS_HE)]
            _flav_hay = _name + " " + " ".join(_real_items)
        else:
            _flav_hay = _hay
        is_flavored_variant = any(m in _flav_hay for m in FLAVORED_VARIANT_MARKERS_HE)

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
        # TASK-169D option (b): yogurt top-trim — a +8 that fired via the yogurt-subtype
        # path may lift to A but not manufacture an S on its own.
        if (RECAL_P0_YOGURT_TRIM and r7_culture_credit and r7_path == "yogurt_subtype"
                and weighted_dim_score > RECAL_P0_YOGURT_TRIM_CEILING):
            weighted_dim_score = RECAL_P0_YOGURT_TRIM_CEILING
            fermentation_bonus_note += (
                f" [169D trim: yogurt +8 A-ceiling {RECAL_P0_YOGURT_TRIM_CEILING}]")

    # Stage 4: Guardrail evaluation
    # TASK-181G — pass the W4 confidence so the NOVA-driven PROCESSING_LOAD caps are
    # confidence-scaled and HP penalties are de-amplified (flag OFF → w4_confidence
    # is None → byte-identical guardrail evaluation).
    gr = evaluate_guardrails(nn, l3, nova_level, category, cat_conf, eval_result,
                             w4_confidence, w4_materiality)

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

    # TASK-181M / F3 — non-material confidence-dent boundary guard (behind BARI_GLASSBOX_W4).
    # Both D7 signers' basis was explicit: a non-material peripheral gap surfaces as a
    # confidence DENT, NEVER a grade cut. A flip to insufficient_data IS a grade-label cut.
    # The d3_nonmaterial_gap (−5) may lower the DISPLAYED confidence within the graded band,
    # but it must NOT be the term that crosses a product from a graded state into
    # insufficient_data. Operationalized (Nutrition spec, option 2): if removing the
    # d3_nonmaterial_gap term would leave confidence AT/ABOVE the boundary (=40), the product
    # does NOT enter insufficient_data on account of that term.
    #   - Guard is scoped to the d3_nonmaterial_gap increment ONLY: the no_nutrition_data
    #     context_flag and any below-40 driven by real low-confidence/D5 terms are untouched,
    #     so a genuinely data-poor product still reaches insufficient_data correctly.
    #   - This is a boundary clamp, not a magnitude change: the −5 still reduces the displayed
    #     confidence value; it is simply barred from independently tripping the gate.
    if (BARI_GLASSBOX_W4 and is_insufficient
            and w4_nonmaterial_applied_increment > 0
            and eval_result.get("context_flag") != "no_nutrition_data"
            and (confidence + w4_nonmaterial_applied_increment) >= 40):
        is_insufficient = False

    if is_insufficient:
        data_sufficiency = "insufficient"
        grade = "insufficient_data"
    else:
        data_sufficiency = "sufficient"

    # TASK-179G / EV-038 — Glass Box D6 gate effect (flag-guarded; OFF leaves all of the
    # above verbatim). The gate can only DEMOTE or WITHHOLD, never promote (spec §2.4):
    #   - withhold → score:null, grade label "לא נוקד" (floor-of-observability failure)
    #   - demote   → existing ceiling already applied above; surface a visible "ניתוח חלקי"
    glassbox_flag = None
    if GLASSBOX_D5D6_ON and disclosure_profile is not None:
        gate_state = conf_result.get("d6_gate_state")
        if gate_state == "withhold":
            final_score = None
            grade = GLASSBOX_WITHHELD_LABEL
            data_sufficiency = "withheld"
            glassbox_flag = GLASSBOX_WITHHELD_LABEL
        elif gate_state == "demote":
            glassbox_flag = GLASSBOX_PARTIAL_FLAG

    # Explanation drivers
    drivers = _identify_drivers(gr, floor_result, conf_result, dim_scores, binding_cap, ceiling)

    # Unresolved flags
    flags = _collect_flags(product, signals, cat_result, nova_result, gr, floor_result,
                            se_result, eval_result)

    result = {
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
    # TASK-179G — Glass Box keys are added ONLY when the flag is ON, so an OFF result dict
    # is byte-identical to today (no extra keys to diff). Spec §4.
    if GLASSBOX_D5D6_ON and disclosure_profile is not None:
        result["glassbox_disclosure_profile"] = disclosure_profile
        result["glassbox_d6_gate_state"] = conf_result.get("d6_gate_state")
        result["glassbox_flag"] = glassbox_flag

    # TASK-179P — DIAAS W1.5 keys are added ONLY when BARI_GLASSBOX_W15 is ON, so an OFF
    # result dict is byte-identical to the D5D6 baseline. EV-040.
    if BARI_GLASSBOX_W15 and diaas_result is not None:
        result["diaas_w15_signal"] = diaas_result
        result["diaas_d2_credit_applied"] = diaas_d2_credit_applied
        result["diaas_d5_protein_disclosure_gap"] = diaas_d5_disclosure_gap

    # TASK-181G / TASK-181K / EV-042 (revised) — Glass Box W4 D3 de-moralization signal
    # added ONLY when BARI_GLASSBOX_W4 is ON, so an OFF result dict is byte-identical to
    # the BARI_GLASSBOX_W2 baseline (no extra keys to diff). Spec §2.2 / §2.6 / §4.
    if BARI_GLASSBOX_W4 and w4_confidence is not None:
        result["d3_processing_signal"] = _d3_processing_signal(
            nova_level, w4_confidence, pq_score, pq_note, w4_materiality)
        result["d3_processing_signal"]["confidence_note"] = w4_conf_note
        result["d3_processing_signal"]["materiality_note"] = (
            w4_materiality_note if w4_confidence == "medium" else None)
        result["d3_low_confidence_nova"] = w4_low_confidence_nova
        result["d3_nonmaterial_gap"] = w4_nonmaterial_gap

    # TASK-179S — D4 additive tier findings added ONLY when BARI_GLASSBOX_W2 is ON.
    # Flag OFF → d4_additives key is absent → result dict is byte-identical to the
    # BARI_GLASSBOX_W15 baseline. No score/grade/gate fields modified. EV-041.
    # Ingredient text sourced the same way as the DIAAS W1.5 detector (same fallback chain).
    if BARI_GLASSBOX_W2:
        _d4_ing_text = (
            product.get("ingredients_raw")
            or product.get("ingredients_text_he")
            or ""
        )
        if not _d4_ing_text and product.get("ingredients_list"):
            _d4_ing_text = ", ".join(product["ingredients_list"])
        result["d4_additives"] = detect_additives_d4(_d4_ing_text or "")

    return result


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
