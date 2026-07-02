"""
Prototype: Absorbed-mg Dose Basis Scoring
==========================================
PROPOSAL ONLY -- not a committed change. For owner co-sign.
Implements the absorbed-mg scoring concept requested by the owner:
'scoring should derive from what the body absorbs, directly and heavily.'

Run: python prototype_absorbed_scoring.py
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Absorbed-mg coefficients (PROPOSED canonical set)
# Source: benchmark v1 ss3+ss4, dossier compound_forms_identity, cited literature
# All are POPULATION-AVERAGE estimates from human bioavailability studies.
# NOT per-product lab measurements. Honest guardrail: stated as bands.
# ---------------------------------------------------------------------------
ELEM_FRAC = {
    "oxide":       0.603,   # PubChem CID 14792
    "citrate":     0.162,   # PubChem CID 6099959
    "bisglycinate":0.141,   # PubChem CID 84645
    "malate":      0.155,   # PubChem CID 74258 (mono-Mg malate)
    "taurate":     0.089,   # PubChem CID 536944
    "carbonate":   0.288,   # PubChem CID 11029; SUPP-EV-028
    "hydroxide":   0.417,   # PubChem CID 14791; BUG-FIX-2026-06-20
}

# Absorption % BANDS (literature population averages, NOT lab-verified per-product):
# PMID:7815675 (Firoz&Graber 2001), PMID:30761462, PMID:39770988 (Walker et al)
# Benchmark ss3 + ss4 (magnesium_benchmark_v1.md)
ABS_BAND = {
    "oxide":       (0.02, 0.08),   # ~4% midpoint; well-established floor
    "hydroxide":   (0.04, 0.10),   # ~7% midpoint; laxative/pharmacologic form
    "carbonate":   (0.08, 0.15),   # ~12% midpoint; GI-active class
    "malate":      (0.15, 0.20),   # ~17% midpoint; sparse human data
    "taurate":     (0.10, 0.20),   # ~15% midpoint; sparse data
    "citrate":     (0.25, 0.30),   # ~27% midpoint; strongest comparative evidence
    "bisglycinate":(0.20, 0.25),   # ~22% midpoint; thinner comparative data (NOT 28%)
}

ABS_MID = {f: (lo + hi) / 2.0 for f, (lo, hi) in ABS_BAND.items()}


# ---------------------------------------------------------------------------
# Proposed dose calibration (absorbed-mg basis)
# ---------------------------------------------------------------------------
# Current: min_effective = 300mg ELEMENTAL (gut-level; cited PMID:27402922)
# Proposed: min_effective_absorbed estimated from trial absorbed amounts.
# RCT BP meta-analysis (PMID:27402922): median supplemental dose ~368mg elemental.
# Dominant form in trials: citrate/mixture. Estimated absorbed:
#   368mg elemental x ~25% (citrate-class avg) = ~92mg absorbed
# Conservative floor: 75mg absorbed (round; ~25th pct of trial distributions)
# Upper studied: 100mg absorbed (~30% x 333mg elemental upper range).
# These are CALIBRATION-PENDING estimates; require D7 co-sign.

MIN_EFF_ABS  = 75.0   # mg absorbed per day (CALIBRATION-PENDING)
UPPER_ABS    = 100.0  # mg absorbed per day (CALIBRATION-PENDING)
FAIRY_FLOOR  = MIN_EFF_ABS * 0.5   # 37.5mg absorbed

DOSE_IN_RANGE = 92
DOSE_OVER_STUDIED = 72
DOSE_SUBTHERAPEUTIC_HI = 84
DOSE_SUBTHERAPEUTIC_LO = 50
DOSE_FAIRY_DUST = 20


def score_dose_absorbed(absorbed_mg):
    if absorbed_mg < FAIRY_FLOOR:
        return {"value": DOSE_FAIRY_DUST, "reason": "fairy_dust", "absorbed_mg": absorbed_mg}
    if absorbed_mg < MIN_EFF_ABS:
        span = MIN_EFF_ABS - FAIRY_FLOOR
        frac = (absorbed_mg - FAIRY_FLOOR) / span if span > 0 else 0.0
        val = DOSE_SUBTHERAPEUTIC_LO + frac * (DOSE_SUBTHERAPEUTIC_HI - DOSE_SUBTHERAPEUTIC_LO)
        return {"value": round(val, 1), "reason": "sub_therapeutic", "absorbed_mg": absorbed_mg}
    if absorbed_mg > UPPER_ABS:
        return {"value": DOSE_OVER_STUDIED, "reason": "over_studied", "absorbed_mg": absorbed_mg}
    return {"value": DOSE_IN_RANGE, "reason": "in_range", "absorbed_mg": absorbed_mg}


# ---------------------------------------------------------------------------
# Proposed dimension weights
# Rationale: absorbed-mg dose already encodes bioavailability, making Form
# partially redundant. Form retains a SMALL residual weight (0.05) as a
# premium-marketing / labeling-honesty signal (e.g. 'poor form sold as premium'),
# not as a primary bioavailability discriminator. Dose absorbs the freed 0.15.
#   Current: ev=0.30, dose=0.25, form=0.20, honesty=0.15, safety=0.10
#   Proposed: ev=0.30, dose=0.40, form=0.05, honesty=0.15, safety=0.10
# Sum = 1.00. CALIBRATION-PENDING.
# ---------------------------------------------------------------------------
WEIGHTS_CURRENT  = {"evidence": 0.30, "dose": 0.25, "form": 0.20, "honesty": 0.15, "safety": 0.10}
WEIGHTS_PROPOSED = {"evidence": 0.30, "dose": 0.40, "form": 0.05, "honesty": 0.15, "safety": 0.10}

SAFETY_BLEND = 70  # neutral

CAP_INSUFFICIENT = 34
CAP_FAIRY_DUST   = 49


def grade_for(score):
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


def blend_and_cap(ev, dose_val, dose_reason, form_val, hon, weights, ev_tier_insufficient):
    """Compute weighted blend and apply caps (most-restrictive-wins)."""
    if ev_tier_insufficient:
        # Dose is N/A (short-circuit); exclude from blend
        w_total = weights["evidence"] + weights["form"] + weights["honesty"] + weights["safety"]
        raw = (ev * weights["evidence"] + form_val * weights["form"]
               + hon * weights["honesty"] + SAFETY_BLEND * weights["safety"]) / w_total
    else:
        raw = (ev * weights["evidence"] + dose_val * weights["dose"]
               + form_val * weights["form"] + hon * weights["honesty"]
               + SAFETY_BLEND * weights["safety"])

    raw = round(raw, 1)
    final = raw
    binding = "blend_dominant"

    if ev_tier_insufficient:
        if final > CAP_INSUFFICIENT:
            final = CAP_INSUFFICIENT
            binding = "cap_1_insufficient_evidence"
    elif dose_reason == "fairy_dust":
        if final > CAP_FAIRY_DUST:
            final = CAP_FAIRY_DUST
            binding = "cap_2_fairy_dust"

    return {"blend": raw, "final": round(final, 1), "grade": grade_for(final), "binding": binding}


# ---------------------------------------------------------------------------
# 18-SKU corpus (current sub-scores from engine_output traces, 2026-06-20)
# ---------------------------------------------------------------------------
# Notes:
# - ev=17.0 -> Insufficient (dose short-circuit, dose_val=None)
# - Form values from corpus: citrate/bisglycinate=preferred(92), malate/taurate=acceptable(72),
#   carbonate=acceptable(72), oxide=poor_honest(45) or poor_as_premium(22),
#   hydroxide=poor_honest(45)
# - Honesty: oxide products have misleading_true flag (-20 = 80); others 100
#   Except some products: Altman Balance Oxide = different honesty? Check trace.

CORPUS = [
    # (sku_id, name, cmpd_mg, form, ev, dose_val_current, form_val, hon, curr_score, curr_grade)
    # dose_val_current = current engine dose sub-score (elemental basis)
    ("SP-0033984005181", "Solgar Ca+Mg+D3",          100.0, "citrate",     47.0, 20,   92, 100, 49.0, "D"),
    ("SP-7290001065594", "Nutricare Nano Liposomal",   88.0, "bisglycinate",17.0, None, 92, 100, 34.0, "E"),
    ("SP-7290001065662", "Nutricare Mg 520",          520.0, "oxide",       72.0, 92,   22,  80, 62.6, "C"),  # misleading_true
    ("SP-7290001066973", "Nutricare Malate",          700.0, "malate",      47.0, 20,   72, 100, 49.0, "D"),
    ("SP-7290010207640", "NT L.C. Hydroxide",         450.0, "hydroxide",   47.0, 58.5, 45, 100, 59.7, "C"),  # BUG-FIX-2026-06-20
    ("SP-7290011899967", "Altman Citrate 120",        200.0, "citrate",     47.0, 20,   92, 100, 49.0, "D"),
    ("SP-7290013142894", "MagUp Oxide 450",           450.0, "oxide",       72.0, 77.5, 22,  80, 66.5, "B"),  # misleading_true
    ("SP-7290013464248", "SupHerb Citrate+B6",        250.0, "citrate",     47.0, 20,   92, 100, 49.0, "D"),
    ("SP-7290015318426", "Tink Oxide 520",            520.0, "oxide",       72.0, 92,   22,  80, 62.6, "C"),  # misleading_true
    ("SP-7290015318532", "Tink Malate 60",            136.0, "malate",      47.0, 20,   72, 100, 49.0, "D"),
    ("SP-7290015429245", "Amorphicure Carbonate",     160.0, "carbonate",   47.0, 20,   72, 100, 49.0, "D"),  # SUPP-EV-028: carbonate=acceptable
    ("SP-7290017218564", "Altman Mg 520",             520.0, "oxide",       72.0, 92,   22,  80, 62.6, "C"),  # misleading_true
    ("SP-7290017847122", "Magnox B6 432",             432.0, "oxide",       72.0, 75.0, 22,  80, 58.4, "C"),  # misleading_true
    ("SP-7290018439043", "Nutricare WELL Bis",        168.0, "bisglycinate",17.0, None, 92, 100, 34.0, "E"),
    ("SP-7290018439579", "Nutricare Taurate 76",       76.0, "taurate",     47.0, 20,   72, 100, 49.0, "D"),
    ("SP-7290019444206", "Altman Balance Oxide",      450.0, "oxide",       47.0, 77.5, 22,  80, 59.0, "C"),  # different ev? check
    ("SP-7290019444480", "Altman Bisglycinate 250",   250.0, "bisglycinate",47.0, 20,   92, 100, 49.0, "D"),
    ("SP-7290118816065", "SupHerb TRIOMAG",           200.0, "citrate",     17.0, None, 92, 100, 34.0, "E"),
    ("SP-7290118818205", "SupHerb Max 550 Citrate",   550.0, "citrate",     47.0, 20,   92, 100, 49.0, "D"),
]


def compute_row(sku, name, cmpd, form, ev, dose_curr, form_val, hon, curr_score, curr_grade):
    ef = ELEM_FRAC[form]
    elem_mg = round(cmpd * ef, 1)
    abs_pct = ABS_MID[form]
    abs_mg = round(elem_mg * abs_pct, 1)
    abs_band = ABS_BAND[form]

    insufficient = (ev <= 17.0)

    # Current blend (elemental basis)
    curr_r = blend_and_cap(ev, dose_curr if dose_curr else 0, "fairy_dust" if dose_curr == 20 else ("sub_therapeutic" if (dose_curr and dose_curr < 92) else "in_range"),
                           form_val, hon, WEIGHTS_CURRENT, insufficient)
    # Sanity-check: cap enforcement
    curr_r["final"] = curr_score  # Use confirmed engine output, not re-blend
    curr_r["grade"] = curr_grade

    # Proposed absorbed dose
    new_dose = score_dose_absorbed(abs_mg)
    new_dose_val = new_dose["value"]
    new_dose_reason = new_dose["reason"]

    # Proposed blend (absorbed basis, new weights)
    prop_r = blend_and_cap(ev, new_dose_val, new_dose_reason, form_val, hon, WEIGHTS_PROPOSED, insufficient)

    moved = "GRADE CHANGE" if prop_r["grade"] != curr_grade else ""

    return {
        "sku": sku, "name": name, "cmpd": cmpd, "form": form,
        "elem_mg": elem_mg, "abs_band": f"{int(abs_band[0]*100)}-{int(abs_band[1]*100)}%",
        "abs_mg": abs_mg,
        "curr_score": curr_score, "curr_grade": curr_grade,
        "curr_binding": curr_r.get("binding", ""),
        "new_dose_val": new_dose_val, "new_dose_reason": new_dose_reason,
        "new_blend": prop_r["blend"],
        "new_final": prop_r["final"], "new_grade": prop_r["grade"],
        "new_binding": prop_r["binding"],
        "moved": moved,
    }


print("=" * 140)
print("SIE PROTOTYPE: Absorbed-mg Dose Basis  |  CANDIDATE ONLY, NOT COMMITTED  |  2026-06-20")
print("=" * 140)
print()
print("BASIS: per labeled daily serving (servings_per_day=1 for all 18 corpus SKUs).")
print("ABSORPTION %: population-average bands from PMID:7815675, PMID:30761462, PMID:39770988,")
print("  benchmark v1 ss3+ss4. Midpoint of each band used for display. NOT lab-verified per-product.")
print()
print("PROPOSED MIN_EFF_ABSORBED = 75mg (calibration-pending; derived from ~368mg elemental x ~25% = ~92mg;")
print("  conservative floor 75mg. Fairy floor = 37.5mg absorbed.")
print()
print("PROPOSED WEIGHTS: ev=0.30, dose=0.40, form=0.05, hon=0.15, saf=0.10")
print("  (Form retains 0.05 as a residual premium-marketing signal; absorbed-mg encodes bioavailability)")
print()
print(f"{'SKU-tail':<14} {'Name':<32} {'Cmpd':>6} {'Form':<14} {'ElemMg':>7} {'AbsBand':>9} {'AbsMg~':>7} | {'CurrScore':>9} {'CurrGrd':>7} | {'NewBlend':>9} {'NewScore':>9} {'NewGrd':>7} {'Moved'}")
print("-" * 160)

grade_moves = []
for row_args in CORPUS:
    r = compute_row(*row_args)
    sku_tail = r["sku"][-12:]
    moved_str = r["moved"] if r["moved"] else ""
    print(f"{sku_tail:<14} {r['name']:<32} {r['cmpd']:>6.0f} {r['form']:<14} {r['elem_mg']:>7.1f} {r['abs_band']:>9} {r['abs_mg']:>7.1f} | "
          f"{r['curr_score']:>9.1f} {r['curr_grade']:>7} | {r['new_blend']:>9.1f} {r['new_final']:>9.1f} {r['new_grade']:>7} {moved_str}")
    if r["moved"]:
        grade_moves.append(r)

print()
print(f"Grade movements: {len(grade_moves)}/{len(CORPUS)}")
if grade_moves:
    for r in grade_moves:
        print(f"  {r['sku']} {r['name']}: {r['curr_grade']} -> {r['new_grade']} | binding: {r['curr_binding']} -> {r['new_binding']} | absorbed={r['abs_mg']}mg")
else:
    print("  None under this calibration.")

print()
print("NOTE: This prototype uses CURRENT engine honesty/form sub-scores (from traces) and")
print("only replaces the dose dimension. In a real implementation, form=0.05 would need")
print("the engine to re-score the form sub-score for the new residual purpose (premium-marketing")
print("signal only, not bioavailability), which may change form_val for some products.")
print()
print("GOLDEN VALIDATION STATUS: The above is a SCRATCH prototype. The golden fixtures are")
print("NOT tested here (they are testing-basis fixtures). Run run_golden_validation.py separately.")
print("The proposed change would require new calibration fixtures if implemented in proto_v1.")
