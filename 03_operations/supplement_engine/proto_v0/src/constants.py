"""
Supplement Intelligence Engine (SIE) — Prototype v0 — Scoring Constants
========================================================================
Source: 01_framework/supplement_framework/methodology_v1.md (v1.2, D7 co-signed).

SEPARATE TREE from BSIP2 (food). These constants are SIE's own; they share NO
values with bsip2/proto_v0/src/constants.py. The frozen food invariants are
structurally untouchable because this is a sibling engine (TASK-171, §0).

ALL NUMBERS BELOW ARE  # CALIBRATION-PENDING  — candidate values per methodology
v1.2. Nothing here is authoritative until Nutrition D8 implementation-verify and
the per-rule SUPP-EV/D7 path. No published score, no frontend, no category launch.
"""

SIE_ENGINE_VERSION = "proto_v0"
SIE_ALGORITHM_VERSION = "0.2.0"  # CALIBRATION-PENDING — v1.3 claim-resolution rule (TASK-171E)
METHODOLOGY_VERSION = "methodology_v1.md v1.3"

# ---------------------------------------------------------------------------
# §3.1 Five-dimension weights (candidate; sum to 1.0)
# Evidence + Dose are gating; Form modulates; Honesty + Safety are cap/veto.
# SHAPE is fixed by the spec (do NOT change which 5 dims / their roles); only
# these candidate VALUES are calibratable.
# ---------------------------------------------------------------------------
DIMENSION_WEIGHTS = {
    "evidence": 0.30,   # CALIBRATION-PENDING — gate + weight (§2.1)
    "dose":     0.25,   # CALIBRATION-PENDING — gate + weight (§2.2); can be N/A
    "form":     0.20,   # CALIBRATION-PENDING — weight (§2.3)
    "honesty":  0.15,   # CALIBRATION-PENDING — weight + cap source (§2.4)
    "safety":   0.10,   # CALIBRATION-PENDING — veto/cap, rarely additive (§2.5)
}

# ---------------------------------------------------------------------------
# §4 Grade bands (candidate; D7 ruling 1 = start aligned with BSIP2 bands,
# any supplement-specific drift must be EARNED with Phase-2 data).
# Lookup: first band whose floor <= score wins, evaluated high→low.
# ---------------------------------------------------------------------------
GRADE_BANDS = [
    ("S", 90),  # CALIBRATION-PENDING
    ("A", 80),  # CALIBRATION-PENDING
    ("B", 65),  # CALIBRATION-PENDING
    ("C", 50),  # CALIBRATION-PENDING
    ("D", 35),  # CALIBRATION-PENDING
    ("E", 0),   # CALIBRATION-PENDING
]

# ---------------------------------------------------------------------------
# §2.1 Evidence sub-score bands per dossier tier (candidate).
# Midpoint of each band is used as the representative sub-score.
# ---------------------------------------------------------------------------
EVIDENCE_TIER_BANDS = {
    "Strong":       (85, 100),  # CALIBRATION-PENDING
    "Moderate":     (60, 84),   # CALIBRATION-PENDING
    "Weak":         (35, 59),   # CALIBRATION-PENDING
    "Insufficient": (0, 34),    # CALIBRATION-PENDING
}

# ---------------------------------------------------------------------------
# §2.2 Dose adequacy bands (candidate). Representative sub-score per condition.
# ---------------------------------------------------------------------------
DOSE_IN_RANGE = 92          # CALIBRATION-PENDING — dose >= min_effective, <= upper_studied
DOSE_OVER_STUDIED = 72      # CALIBRATION-PENDING — > upper_studied, below UL (no bonus)
DOSE_SUBTHERAPEUTIC_HI = 84 # CALIBRATION-PENDING — band ceiling for [0.5*min, min)
DOSE_SUBTHERAPEUTIC_LO = 50 # CALIBRATION-PENDING — band floor for [0.5*min, min)
DOSE_FAIRY_DUST = 20        # CALIBRATION-PENDING — dose < 0.5*min_effective
DOSE_HIDDEN = 0             # CALIBRATION-PENDING — hidden in blend (also caps via honesty)

FAIRY_DUST_FRACTION = 0.5   # CALIBRATION-PENDING — §2.2 fairy_dust_fraction candidate

# ---------------------------------------------------------------------------
# §2.3 Form & bioavailability bands (candidate). Representative sub-score.
# ---------------------------------------------------------------------------
FORM_PREFERRED = 92             # CALIBRATION-PENDING
FORM_ACCEPTABLE = 72            # CALIBRATION-PENDING
FORM_POOR_AS_PREMIUM = 22       # CALIBRATION-PENDING — poor form sold as premium
FORM_POOR_HONEST = 45           # CALIBRATION-PENDING — poor form, honestly cheap
FORM_UNKNOWN = 50               # CALIBRATION-PENDING — form not resolvable

# ---------------------------------------------------------------------------
# §2.4 Formulation honesty debits (candidate). Honesty starts at 100.
# ---------------------------------------------------------------------------
HONESTY_START = 100
HONESTY_DEBIT_CLAIM_SUBSTANCE = 35  # CALIBRATION-PENDING — claim-vs-substance gap (major, scaled)
HONESTY_DEBIT_MISLEADING_TRUE = 20  # CALIBRATION-PENDING — misleading-but-true framing (moderate)
HONESTY_DEBIT_FILLER = 12           # CALIBRATION-PENDING — filler/bulking dominance (minor-moderate)
HONESTY_DEBIT_PIXIE_ROSTER = 20     # CALIBRATION-PENDING — pixie-dust roster (moderate)
# A hidden-dose proprietary blend is handled as a CAP (§3.2 cap 3), not a smooth
# debit, but we also floor the honesty SUB-SCORE so the trace reads honestly.
HONESTY_HIDDEN_BLEND_SUBSCORE = 25  # CALIBRATION-PENDING

# ---------------------------------------------------------------------------
# §2.5 Safety sub-score sentinels (candidate). Safety is a veto/cap, not a
# smooth contributor — "neutral" does not lift the score (absence of harm is
# not a virtue). Encoded as a sentinel handled in the blend.
# ---------------------------------------------------------------------------
SAFETY_NEUTRAL = "neutral"   # excluded from positive credit (treated like a pass-through)
SAFETY_VETO = "veto"         # triggers §3.2 cap 4 floor
SAFETY_NOTE = "note"         # FLAG-2 (Nutrition D8): graded soft-penalty band between a
                             # reversible GI-tolerance threshold (ul_note_threshold) and the
                             # hard toxicity veto line (upper_limit_UL). NOT a veto.
SAFETY_NEUTRAL_BLEND_VALUE = 70  # CALIBRATION-PENDING — value used IF safety enters the blend
                                 # (kept modest so a clean product is not *rewarded* for safety)
                                 # FLAG-3 (Nutrition D8): genuinely arbitrary — needs SUPP-EV-006.
SAFETY_NOTE_BLEND_VALUE = 45     # CALIBRATION-PENDING — FLAG-2: a SKU in the GI-tolerance band
                                 # (above ul_note_threshold, below upper_limit_UL) enters the blend
                                 # at a modest soft-penalty value instead of a veto floor.

# ---------------------------------------------------------------------------
# §3.2 Caps, floors, vetoes (candidate ceilings/floors). All most-restrictive-wins.
# ---------------------------------------------------------------------------
CAP_INSUFFICIENT_EVIDENCE = 34   # CALIBRATION-PENDING — cap 1: Evidence=Insufficient → grade E ceiling
CAP_FAIRY_DUST = 49              # CALIBRATION-PENDING — cap 2: fairy-dust/hidden dose → D-band ceiling
CAP_HONESTY_CORE = 49            # CALIBRATION-PENDING — cap 3: hidden CORE active → D-band ceiling
CAP_HONESTY_SECONDARY = 64       # CALIBRATION-PENDING — cap 3: hidden SECONDARY active → C-band ceiling
VETO_SAFETY_FLOOR = 20           # CALIBRATION-PENDING — cap 4: safety veto → E-band floor
FLOOR_FORM_EVIDENCE_COUPLING = 49  # CALIBRATION-PENDING — cap 5: poor-form-for-evidence-claim ceiling (form-honesty band)

# Mechanism identifiers (stable strings for the §12.2 trace contract)
MECH_CAP_1 = "cap_1_insufficient_evidence"
MECH_CAP_2 = "cap_2_fairy_dust_hidden_dose"
MECH_CAP_3_CORE = "cap_3_honesty_core"
MECH_CAP_3_SECONDARY = "cap_3_honesty_secondary"
MECH_VETO_SAFETY = "veto_safety"
MECH_FLOOR_FORM_EV = "floor_form_evidence_coupling"
MECH_BLEND_DOMINANT = "blend_dominant_limit"

# Machine reasons (language-free keys; consumer Hebrew prose is Phase 4, NOT here).
# These must avoid efficacy-overclaim and necessity tokens (§12.3).
MACHINE_REASON = {
    MECH_CAP_1: "no_reliable_evidence_for_claim",
    MECH_CAP_2: "underdosed_or_unverifiable_dose",
    MECH_CAP_3_CORE: "core_active_dose_hidden_in_blend",
    MECH_CAP_3_SECONDARY: "secondary_active_dose_hidden_in_blend",
    MECH_VETO_SAFETY: "dose_exceeds_safe_ceiling",
    MECH_FLOOR_FORM_EV: "poor_form_for_evidence_backed_claim",
    MECH_BLEND_DOMINANT: "limited_by_weakest_applicable_dimension",
}
