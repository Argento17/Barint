"""
SIE Prototype v0 — Score Engine
===============================
Implements methodology_v1.md v1.2:
  - §2.1-2.5  five dimension sub-scorers (0-100, reading label x dossier)
  - §2.2/§3   Dose short-circuit (Evidence=Insufficient -> Dose = N/A, excluded
              from the blend denominator, NOT 0)
  - §3        weighted blend over the APPLICABLE (non-N/A) dimensions
  - §3.2      caps / floors / veto, most-restrictive-wins
  - §4        grade banding
  - §12       binding-constraint identification (the ONE mechanism that bound the
              grade) + the structured signature

ALL numbers candidate / CALIBRATION-PENDING (constants.py). Reads in-house
dossiers + labels only (EDPG firewall, §9). No live API on the score path.
"""
from typing import Optional, Tuple

import constants as C
from supplement_label import SupplementLabel, LabelActive
from dossier_loader import load_dossier, _norm

NA = "N/A"


# ===========================================================================
# §2.4 Over-promise detection (over-specific claim markers)
# ===========================================================================
# A claim is OVER-SPECIFIC if it asserts a tier the evidence cannot bear —
# certainty language ("clinically proven"), a treatment verb ("cures"/"treats"),
# or a named disease/condition. Frozen marker set (NOT NLP): an exact substring
# scan of the normalized claim. Over-specific resolves to the REAL endpoint tier
# (§2.1) AND fires the §2.4 Honesty claim-vs-substance gap — resolution is not a
# free pass for a confident lie.
OVER_PROMISE_MARKERS = (
    "clinically proven", "scientifically proven", "proven to",
    "cure", "cures", "cure ", "treats", "treat ", "reverses", "reverse ",
    "fixes", "heals", "eliminates", "guaranteed",
    # named disease / condition tokens (structure/function language may NOT name these)
    "insomnia", "osteoporosis", "depression", "anxiety disorder",
    "diabetes", "hypertension", "alzheimer", "dementia", "nerve damage",
)


def detect_over_promise(claim: str) -> dict:
    """Frozen substring scan for over-specific over-promise (§2.4). Returns
    {'over_promise': bool, 'markers': [...]}. NO NLP / no inference."""
    n = _norm(claim)
    hits = [m.strip() for m in OVER_PROMISE_MARKERS if m.strip() in n]
    return {"over_promise": bool(hits), "markers": sorted(set(hits))}


# ===========================================================================
# Claim -> tier resolution (§2.1, with v1.3 claim resolution)
# ===========================================================================
_CLAIM_GENERIC_TOKENS = {
    "health", "support", "supports", "function", "and", "&", "the", "a", "of",
    "to", "for", "with", "general", "broad", "consumer", "claim",
    "structure", "function", "structure/function", "clinically", "scientifically",
    "proven", "cure", "cures", "treats", "treat", "reverses", "fixes", "heals",
    "quality",
}


import re as _re

# strip surrounding punctuation so "heart," == "heart" (frozen, not NLP).
# keep the Hebrew Unicode block (U+0590–U+05FF) so real Israeli-label claims
# (e.g. "עייפות"/fatigue) survive tokenization for umbrella lookup (TASK-171K).
_PUNCT = _re.compile(r"[^a-z0-9֐-׿]+")


def _tok_clean(text: str) -> list:
    return [t for t in _PUNCT.sub(" ", _norm(text)).split() if t]


def _claim_tokens(text: str) -> set:
    return {t for t in _tok_clean(text) if t not in _CLAIM_GENERIC_TOKENS}


def _match_studied_claim(tiers: dict, claim: str):
    """Try the EXISTING claim-specific path (explicit studied claim).
    1) exact key match, 2) whole-text containment, 3) distinctive-token overlap.
    Returns (claim_text, info) or None. Kept intact for studied claims so the
    14 existing fixtures behave identically; token-overlap additionally lets an
    over-specific claim ('...cure insomnia') still resolve to its real studied
    endpoint ('sleep quality / insomnia' = Weak) per §2.1 step 2 / §2.4."""
    if claim in tiers:
        return claim, tiers[claim]
    nclaim = _norm(claim)
    for ctext, info in tiers.items():
        if nclaim in _norm(ctext) or _norm(ctext) in nclaim:
            return ctext, info
    # distinctive-token overlap (frozen split, no NLP): an endpoint matches if a
    # distinctive token of the dossier claim appears in the label claim.
    claim_toks = _claim_tokens(claim)
    if claim_toks:
        for ctext, info in tiers.items():
            ctoks = _claim_tokens(ctext)
            if ctoks and (ctoks & claim_toks):
                return ctext, info
    return None


def _resolve_via_umbrella(dossier: dict, claim: str) -> dict:
    """v1.3 §2.1 claim resolution. EXACT key-lookup of each label phrase against
    the dossier's structure_function_umbrella; select the BEST (highest) tier
    among the keys that map. Returns a resolution dict, or {'resolved': False}
    if the dossier has no umbrella. If the dossier HAS an umbrella but nothing
    maps, returns resolved=True with tier=Insufficient (cap-1 will fire, §3).
    NO NLP, NO inference, NO live literature — frozen dictionary lookup only."""
    umbrella = dossier.get("structure_function_umbrella", {})
    if not umbrella.get("has_umbrella"):
        return {"resolved": False}

    claim_toks = _claim_tokens(claim)
    matched = []     # umbrella entries whose key term is present on the label
    for entry in umbrella["mappings"]:
        key_toks = set(entry["key_tokens"])
        present = bool(key_toks & claim_toks)
        if present:
            matched.append(entry)

    mapped = [e for e in matched if e["maps"]]   # present AND a real cited tier
    if not mapped:
        # nothing on the label maps to a recognized cited endpoint -> Insufficient
        # (cap-1 fires, §3). Record the deliberate non-mappings for the trace.
        return {
            "resolved": True, "tier": "Insufficient", "via_umbrella": True,
            "umbrella_mapped": [], "claim_matched": None,
            "umbrella_present_nonmapping": [e["phrase"] for e in matched],
            "contested": False, "citations": [], "claim_scope": None,
            "resolved_endpoint": None, "resolved_phrase": None,
        }

    # select the BEST (highest) tier among the mapped keys (§2.1 step 2).
    best = max(mapped, key=lambda e: _TIER_RANK.get(e["resolved_tier"], -1))
    return {
        "resolved": True,
        "tier": best["resolved_tier"],
        "via_umbrella": True,
        "claim_matched": best["resolves_to"],
        "resolved_endpoint": best["resolves_to"],
        "resolved_phrase": best["phrase"],
        "citations": best["citations"],
        "supp_ev": best["supp_ev"],
        "contested": False,
        "claim_scope": None,
        "umbrella_mapped": [
            {"phrase": e["phrase"], "resolves_to": e["resolves_to"],
             "resolved_tier": e["resolved_tier"], "supp_ev": e.get("supp_ev")}
            for e in mapped],
        "umbrella_present_nonmapping": [
            e["phrase"] for e in matched if not e["maps"]],
    }


# tier ordering for "best plausibly-mapped" selection (§2.1 step 2)
_TIER_RANK = {"Insufficient": 0, "Weak": 1, "Moderate": 2, "Strong": 3}


def resolve_claim_tier(dossier: dict, claim: str) -> dict:
    """Select the dossier tier for the SKU's on-label claim (§2.1).

    Order of resolution:
      1. EXPLICIT studied-claim path (exact / containment / distinctive-token).
         Kept intact for explicit studied claims (existing behavior).
      2. v1.3 CLAIM RESOLUTION via the structure_function_umbrella: a vague
         structure/function claim resolves to the active's best plausibly-mapped
         studied endpoint (frozen exact key-lookup; §2.1).
      3. §2.1 default: if no studied claim matched AND (no umbrella OR nothing
         maps under it) -> Insufficient (the §3 cap-1 ceiling fires).

    An OVER-SPECIFIC claim (§2.4) still resolves to its REAL endpoint tier here
    (step 1 token-overlap or step 2), and is independently flagged for the
    Honesty claim-vs-substance gap by the caller (resolution is not a free pass).
    """
    tiers = dossier["claim_tiers"]

    # --- step 1: explicit studied claim (kept intact) ----------------------
    studied = _match_studied_claim(tiers, claim)
    if studied is not None:
        ctext, info = studied
        return {"claim_matched": ctext, "via_umbrella": False, **info}

    # --- step 2: v1.3 vague-claim resolution via the umbrella --------------
    res = _resolve_via_umbrella(dossier, claim)
    if res.get("resolved"):
        return {"claim_matched": res.get("claim_matched"),
                "via_umbrella": True,
                "tier": res["tier"],
                "contested": res.get("contested", False),
                "citations": res.get("citations", []),
                "claim_scope": res.get("claim_scope"),
                "resolved_endpoint": res.get("resolved_endpoint"),
                "resolved_phrase": res.get("resolved_phrase"),
                "supp_ev": res.get("supp_ev"),
                "umbrella_mapped": res.get("umbrella_mapped", []),
                "umbrella_present_nonmapping": res.get("umbrella_present_nonmapping", [])}

    # --- step 3: §2.1 default: untethered claim, no umbrella -> Insufficient
    return {"claim_matched": None, "via_umbrella": False, "tier": "Insufficient",
            "contested": False, "citations": [], "claim_scope": None}


# ===========================================================================
# §2.1 Evidence Strength
# ===========================================================================
def score_evidence(tier: str) -> dict:
    band = C.EVIDENCE_TIER_BANDS.get(tier)
    if band is None:
        # contested / unknown -> treated as Insufficient for scoring (deferred claims
        # should not reach the score path; if they do, fail safe to the floor band).
        band = C.EVIDENCE_TIER_BANDS["Insufficient"]
    value = (band[0] + band[1]) / 2.0
    return {"value": round(value, 1), "tier": tier}


# ===========================================================================
# §2.2 Dose Adequacy (with elemental / active-fraction basis + short-circuit)
# ===========================================================================
def _effective_label_quantity(label: SupplementLabel, active: LabelActive,
                              dossier: dict) -> Tuple[Optional[float], list]:
    """Resolve the comparable per-DAY active quantity, applying:
       - elemental conversion for minerals (§2.2 elemental trap)
       - per_serving -> per_day normalization
       Returns (quantity_in_dossier_basis, notes)."""
    notes = []
    if active.quantity is None:
        return None, ["dose_hidden_in_blend"]

    qty = float(active.quantity)

    # elemental conversion (minerals): label states COMPOUND mass; convert to elemental.
    elem = dossier.get("elemental_by_form", {})
    if elem and active.form is not None:
        frac = elem.get(_norm(active.form))
        if frac is not None:
            qty = qty * frac
            notes.append(f"elemental_conversion x{frac}")

    # normalize per_serving -> per_day if the dossier dose basis is per_day
    basis = dossier["dose"].get("basis")
    if basis == "per_day" and active.quantity_basis == "per_serving":
        qty = qty * label.servings_per_day
        if label.servings_per_day != 1.0:
            notes.append(f"x{label.servings_per_day}_servings_per_day")

    return qty, notes


def score_dose(label: SupplementLabel, active: LabelActive, dossier: dict,
               evidence_tier: str) -> dict:
    """Dose sub-score. SHORT-CIRCUIT (§2.2 v1.2): if Evidence tier = Insufficient,
    Dose = N/A (excluded from blend, NOT 0). Hidden-in-blend dose is unknowable -> N/A
    and handed to Honesty (§2.4)."""
    # ---- dose short-circuit: no evidence => no effective dose => N/A --------
    if evidence_tier == "Insufficient":
        return {"value": NA, "reason": "evidence_insufficient_dose_short_circuit"}

    # ---- hidden in a proprietary blend: per-active dose unknowable -> N/A ---
    if active.in_proprietary_blend or active.quantity is None:
        return {"value": NA, "reason": "dose_hidden_in_blend",
                "fairy_dust_suspected": True}

    qty, notes = _effective_label_quantity(label, active, dossier)
    dose = dossier["dose"]
    min_eff = dose.get("min_effective")
    upper = dose.get("upper_studied")
    if min_eff is None:
        return {"value": C.FORM_UNKNOWN, "reason": "no_effective_dose_in_dossier",
                "notes": notes}

    fairy_floor = C.FAIRY_DUST_FRACTION * min_eff

    if qty < fairy_floor:
        return {"value": C.DOSE_FAIRY_DUST, "reason": "fairy_dust",
                "label_qty_basis": round(qty, 3), "min_effective": min_eff,
                "fairy_dust_suspected": True, "notes": notes}
    if qty < min_eff:
        # sub-therapeutic: grade by proximity within [0.5*min, min)
        span = min_eff - fairy_floor
        frac = (qty - fairy_floor) / span if span > 0 else 0.0
        value = C.DOSE_SUBTHERAPEUTIC_LO + frac * (
            C.DOSE_SUBTHERAPEUTIC_HI - C.DOSE_SUBTHERAPEUTIC_LO)
        return {"value": round(value, 1), "reason": "sub_therapeutic",
                "label_qty_basis": round(qty, 3), "min_effective": min_eff,
                "notes": notes}
    if upper is not None and qty > upper:
        return {"value": C.DOSE_OVER_STUDIED, "reason": "over_studied_no_bonus",
                "label_qty_basis": round(qty, 3), "upper_studied": upper,
                "notes": notes}
    return {"value": C.DOSE_IN_RANGE, "reason": "in_range",
            "label_qty_basis": round(qty, 3), "min_effective": min_eff,
            "notes": notes}


# ===========================================================================
# §2.3 Form & Bioavailability
# ===========================================================================
def score_form(active: LabelActive, dossier: dict, sold_as_premium: bool = False) -> dict:
    ladder = dossier["form_ladder"]
    if active.form is None:
        return {"value": C.FORM_UNKNOWN, "match": "unknown"}
    f = _norm(active.form)

    def _in(group):
        return any(f in g or g in f for g in ladder.get(group, []))

    if _in("preferred"):
        return {"value": C.FORM_PREFERRED, "match": "preferred"}
    if _in("acceptable"):
        return {"value": C.FORM_ACCEPTABLE, "match": "acceptable"}
    if _in("poor"):
        if sold_as_premium:
            return {"value": C.FORM_POOR_AS_PREMIUM, "match": "poor_as_premium"}
        return {"value": C.FORM_POOR_HONEST, "match": "poor_honest"}
    # form named but not on the ladder -> unknown/acceptable-by-default, flagged
    return {"value": C.FORM_UNKNOWN, "match": "not_on_ladder"}


# ===========================================================================
# §2.4 Formulation Honesty (+ detects the cap inputs)
# ===========================================================================
def score_honesty(label: SupplementLabel, core: LabelActive, dossier: dict,
                  misleading_true: bool = False, claim_substance_gap: bool = False,
                  over_promise: bool = False) -> dict:
    """Honesty starts at 100, debited by detected deceptions. Hidden-dose blend is a
    CAP (handled in combine), but we also floor the honesty sub-score so the trace reads
    honestly. Concern-coordination (§3.2 #6): one deception is not triple-charged.

    §2.4 over-promise (v1.3): an over-specific over-promise ('clinically proven to
    cure X') is a claim-vs-substance gap on the CORE active when core is named in
    the over-claim -> sets over_promise_core so combine() can apply the §3 cap-3
    honesty-core ceiling. Resolution (§2.1) is not a free pass for a confident lie."""
    score = C.HONESTY_START
    debits = []
    hidden_blend = any(a.in_proprietary_blend for a in label.actives)
    hidden_core = bool(core and core.in_proprietary_blend)
    # an over-specific over-promise on the CORE active -> §3 cap-3 honesty-core
    over_promise_core = bool(over_promise and core and core.is_core)

    if hidden_blend:
        # the dominant signal: a hidden dose. Floor the sub-score; the product-level
        # cap is applied in combine(). Do NOT also re-charge it as filler/claim-gap.
        score = C.HONESTY_HIDDEN_BLEND_SUBSCORE
        debits.append("hidden_dose_blend")
    else:
        if claim_substance_gap:
            score -= C.HONESTY_DEBIT_CLAIM_SUBSTANCE
            debits.append("over_promise_claim_gap" if over_promise
                          else "claim_substance_gap")
        if misleading_true:
            score -= C.HONESTY_DEBIT_MISLEADING_TRUE
            debits.append("misleading_but_true_framing")
        if label.filler_dominant:
            score -= C.HONESTY_DEBIT_FILLER
            debits.append("filler_dominance")
        if label.pixie_roster:
            score -= C.HONESTY_DEBIT_PIXIE_ROSTER
            debits.append("pixie_dust_roster")

    return {"value": max(0, round(score, 1)), "debits": debits,
            "hidden_blend": hidden_blend, "hidden_core": hidden_core,
            "over_promise_core": over_promise_core}


# ===========================================================================
# §2.5 Safety Ceiling (veto/cap)
# ===========================================================================
def score_safety(label: SupplementLabel, active: LabelActive, dossier: dict) -> dict:
    """Returns a sentinel: 'neutral' (no lift) or 'veto' (floor). §2.5 / §2.5 edge cases.
    Clinical-megadose exemption: labeled regimen decides (§2.5, D7 ruling 4)."""
    safety = dossier["safety"]
    ul = safety.get("upper_limit_UL")          # hard VETO line (toxicity-relevant)
    note_threshold = safety.get("ul_note_threshold")  # FLAG-2: GI-tolerance soft-band floor
    risky = bool(safety.get("risky_flags_active"))  # explicit banned/risky active present

    if risky:
        return {"value": C.SAFETY_VETO, "reason": "risky_active"}

    if ul is None or active.quantity is None:
        return {"value": C.SAFETY_NEUTRAL, "reason": "no_ul_or_no_dose"}

    # §2.5: UL comparison MUST use the same basis as the dossier (elemental, daily,
    # adult). Reuse the dose normalizer so a compound label mass is converted to
    # elemental + per-day before comparison to an elemental supplemental UL.
    daily, _notes = _effective_label_quantity(label, active, dossier)
    if daily is None:
        return {"value": C.SAFETY_NEUTRAL, "reason": "dose_unknowable"}

    # clinical-megadose exemption: a clearly-labeled weekly repletion SKU is exempt
    # from the consumer-DAILY veto (flagged clinical_use + safety note).
    if label.labeled_regimen != "daily":
        return {"value": C.SAFETY_NEUTRAL, "reason": f"non_daily_regimen_{label.labeled_regimen}",
                "clinical_use_flag": True}

    if daily > ul:
        return {"value": C.SAFETY_VETO, "reason": "exceeds_UL",
                "daily": round(daily, 2), "ul": ul}

    # FLAG-2 (Nutrition D8): graded Safety NOTE band. A reversible GI-tolerance
    # threshold (e.g. EFSA 250 mg supplemental Mg = onset of osmotic diarrhea) is a
    # SOFT line, NOT a toxicity veto. A dose above this note threshold but at/below the
    # hard UL earns a Safety NOTE + modest soft penalty in the blend — it must NOT
    # auto-fail an effective dose. (Rationale recorded in magnesium.yaml ul_governing_decision.)
    if note_threshold is not None and daily > note_threshold:
        return {"value": C.SAFETY_NOTE, "reason": "above_gi_tolerance_note_below_UL",
                "daily": round(daily, 2), "note_threshold": note_threshold, "ul": ul}

    return {"value": C.SAFETY_NEUTRAL, "reason": "within_ul",
            "daily": round(daily, 2), "ul": ul}


# ===========================================================================
# §3 Combination + §3.2 caps/floors/veto (most-restrictive-wins) + §12 binding
# ===========================================================================
def _grade_for(score: float) -> str:
    for letter, floor in C.GRADE_BANDS:
        if score >= floor:
            return letter
    return "E"


def _weighted_blend(subs: dict) -> float:
    """Blend over APPLICABLE (non-N/A) dimensions only (§3 N/A rule). An N/A dim is
    DROPPED from the denominator (not treated as 0, not re-weighted to inflate)."""
    total_w = 0.0
    acc = 0.0
    for dim, w in C.DIMENSION_WEIGHTS.items():
        v = subs[dim]["value"]
        if v == NA:
            continue
        if dim == "safety":
            # safety 'neutral' does not lift the score; 'veto' is handled as a floor.
            # Enter the blend at a modest fixed value so it neither rewards nor (here) punishes.
            if v == C.SAFETY_NEUTRAL:
                v = C.SAFETY_NEUTRAL_BLEND_VALUE
            elif v == C.SAFETY_NOTE:
                # FLAG-2: GI-tolerance soft-penalty band — a modest drag, NOT a floor.
                v = C.SAFETY_NOTE_BLEND_VALUE
            elif v == C.SAFETY_VETO:
                v = C.SAFETY_NEUTRAL_BLEND_VALUE  # veto enforced separately as a floor
        acc += w * float(v)
        total_w += w
    if total_w == 0:
        return 0.0
    return acc / total_w


def combine(subs: dict, ctx: dict) -> dict:
    """Apply §3 blend, then §3.2 caps/floors/veto (most-restrictive-wins), then grade.
    Identify the §12 binding constraint (the mechanism that ACTUALLY bound the grade)."""
    blend = _weighted_blend(subs)
    blend_grade = _grade_for(blend)

    # Collect every applicable cap/floor/veto with its imposed ceiling/floor.
    # A CAP imposes an upper bound (score cannot EXCEED it). A VETO/FLOOR imposes a
    # hard floor that overrides positives -> we model it as the final score (floored).
    caps = []   # list of (mechanism, kind, value)  kind in {"ceiling","floor"}

    ev_tier = subs["evidence"]["tier"]
    if ev_tier == "Insufficient":
        caps.append((C.MECH_CAP_1, "ceiling", C.CAP_INSUFFICIENT_EVIDENCE))

    dose_reason = subs["dose"].get("reason")
    dose_val = subs["dose"]["value"]
    if dose_val != NA and dose_reason == "fairy_dust":
        caps.append((C.MECH_CAP_2, "ceiling", C.CAP_FAIRY_DUST))
    if subs["honesty"].get("hidden_blend"):
        if subs["honesty"].get("hidden_core"):
            caps.append((C.MECH_CAP_3_CORE, "ceiling", C.CAP_HONESTY_CORE))
        else:
            caps.append((C.MECH_CAP_3_SECONDARY, "ceiling", C.CAP_HONESTY_SECONDARY))
        # a hidden dose is also a fairy-dust-suspected dose (cap 2 family); record cap 2
        # but concern-coordination keeps the honesty cap as the named one if more restrictive.
    elif subs["honesty"].get("over_promise_core"):
        # §2.4 / §13.4 R3: an over-specific over-promise on the CORE active fires the
        # §3 cap-3 honesty-core ceiling (a confident lie about a Weak-tier endpoint
        # cannot earn the honest-vague grade). Resolution still gave the REAL (Weak)
        # tier above; this is the SECOND markdown (claim-vs-substance gap).
        caps.append((C.MECH_CAP_3_CORE, "ceiling", C.CAP_HONESTY_CORE))
    if subs["safety"]["value"] == C.SAFETY_VETO:
        caps.append((C.MECH_VETO_SAFETY, "floor", C.VETO_SAFETY_FLOOR))

    if ctx.get("form_evidence_coupling"):
        caps.append((C.MECH_FLOOR_FORM_EV, "ceiling", C.FLOOR_FORM_EVIDENCE_COUPLING))

    # ---- resolve final score via most-restrictive-wins --------------------
    final = blend
    binding = None

    # apply all ceilings (cap final down to the LOWEST ceiling)
    ceilings = [(m, v) for (m, k, v) in caps if k == "ceiling"]
    floors = [(m, v) for (m, k, v) in caps if k == "floor"]

    # The binding constraint is the single mechanism on which the final grade RESTS.
    # Evaluate: the most-restrictive outcome = min(blend, lowest ceiling) then floored.
    effective_ceiling = None
    if ceilings:
        effective_ceiling_mech, effective_ceiling = min(ceilings, key=lambda x: x[1])
    else:
        effective_ceiling_mech = None

    # A safety veto FLOORS the score and OVERRIDES positive dimensions (§3.2 cap 4).
    # In practice for our fixtures a veto means the product is forced into E regardless.
    veto_active = bool(floors)
    if veto_active:
        veto_mech, veto_floor = min(floors, key=lambda x: x[1])

    if veto_active:
        # safety veto: the score is the veto floor (overriding all positives).
        final = float(veto_floor)
        binding = veto_mech
    elif effective_ceiling is not None and effective_ceiling < blend:
        final = float(effective_ceiling)
        binding = effective_ceiling_mech
    else:
        # grade came from the blend itself -> dominant limiting dimension (§12.1)
        final = blend
        binding = C.MECH_BLEND_DOMINANT

    final = max(0.0, min(100.0, final))
    grade = _grade_for(final)

    # ---- §12: also_fired = every other mechanism that triggered -----------
    also_fired = []
    for (m, k, v) in caps:
        if m == binding:
            continue
        also_fired.append({"mechanism": m, "kind": k, "value": v})

    return {
        "blend": round(blend, 1),
        "blend_grade": blend_grade,
        "final_score": round(final, 1),
        "grade": grade,
        "binding_constraint": {
            "mechanism": binding,
            "machine_reason": C.MACHINE_REASON.get(binding, "limited_by_blend"),
        },
        "caps_vetoes_fired": [{"mechanism": m, "kind": k, "ceiling_or_floor": v}
                              for (m, k, v) in caps],
        "also_fired": also_fired,
    }


# ===========================================================================
# Top-level: score one label end to end
# ===========================================================================
def score_label(label: SupplementLabel, dossier: dict,
                form_sold_as_premium: bool = False,
                misleading_true: bool = False,
                claim_substance_gap: bool = False,
                form_evidence_coupling: bool = False) -> dict:
    core = label.core_active()

    # §2.1 evidence (claim selects tier; v1.3 vague claims resolve via umbrella)
    tier_info = resolve_claim_tier(dossier, label.primary_claim)
    ev = score_evidence(tier_info["tier"])

    # §2.4 over-promise (over-specific claim): resolution is NOT a free pass.
    # An over-specific claim resolves to the REAL endpoint tier (above) AND fires
    # the §2.4 claim-vs-substance Honesty gap. Detected here, OR passed by caller.
    op = detect_over_promise(label.primary_claim)
    over_promise = op["over_promise"]
    # the Honesty claim-gap fires if the caller asserted it OR an over-specific
    # claim was detected (e.g. "clinically proven to cure insomnia").
    claim_gap = claim_substance_gap or over_promise

    # §2.2 dose (short-circuits on Insufficient evidence)
    dose = score_dose(label, core, dossier, tier_info["tier"])

    # §2.3 form
    form = score_form(core, dossier, sold_as_premium=form_sold_as_premium)

    # §2.4 honesty
    honesty = score_honesty(label, core, dossier,
                            misleading_true=misleading_true,
                            claim_substance_gap=claim_gap,
                            over_promise=over_promise)

    # §2.5 safety
    safety = score_safety(label, core, dossier)

    subs = {"evidence": ev, "dose": dose, "form": form,
            "honesty": honesty, "safety": safety}

    ctx = {"form_evidence_coupling": form_evidence_coupling}
    combined = combine(subs, ctx)

    # §2.1 claim-resolution audit block (v1.3) — which umbrella key resolved, to
    # which endpoint + tier, so the "why" is auditable (carried into the trace).
    claim_resolution = {
        "via_umbrella": bool(tier_info.get("via_umbrella")),
        # the studied endpoint the tier came from: the umbrella target if resolved
        # via the umbrella, else the matched claims[] endpoint (token/containment).
        "resolved_endpoint": tier_info.get("resolved_endpoint")
                             or tier_info.get("claim_matched"),
        "resolved_phrase": tier_info.get("resolved_phrase"),
        "resolved_tier": tier_info["tier"],
        "resolution_supp_ev": tier_info.get("supp_ev"),
        "resolution_citations": tier_info.get("citations", []),
        "umbrella_mapped": tier_info.get("umbrella_mapped", []),
        "umbrella_present_nonmapping": tier_info.get("umbrella_present_nonmapping", []),
        "over_promise": over_promise,
        "over_promise_markers": op["markers"],
    }

    return {
        "sku_id": label.sku_id,
        "active": dossier["canonical_name"],
        "on_label_claim": label.primary_claim,
        "claim_matched": tier_info["claim_matched"],
        "claim_resolution": claim_resolution,
        "sub_scores": subs,
        "combination": combined,
        "supp_ev_refs": dossier.get("supp_ev_refs", []),
    }
