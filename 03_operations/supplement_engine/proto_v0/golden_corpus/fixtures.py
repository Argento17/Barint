"""
SIE Prototype v0 — Golden Corpus (Phase-2 validation fixtures)
==============================================================
CONSTRUCTED ENGINEERING FIXTURES — synthetic (active, dose, form, claim) tuples
reusing the 5 MVP actives. NO real brands, NOT published consumer claims
(§11 D7 ruling 5). They force a specific sub-score signature and binding
constraint so the engine's distinguishing + attribution can be validated.

Two axes:
  A. §6 per-dimension PASS/FAIL anchors — each dimension exercised at both poles.
  B. §13 three attribution archetypes — the decisive inverted-E pair test.

Each fixture carries `expect`: the grade band AND the binding-constraint mechanism
the engine MUST produce. ALL numbers candidate / CALIBRATION-PENDING.
"""
from supplement_label import SupplementLabel, LabelActive
import constants as C


def _f(sku, name, claim, active, dossier_slug, **kw):
    """Build a (fixture-spec) dict. `flags` carries scorer context (premium/misleading...)."""
    expect = kw.pop("expect")
    flags = kw.pop("flags", {})
    return {
        "sku_id": sku,
        "dossier_slug": dossier_slug,
        "expect": expect,           # {"grade": "...", "binding": "<mech>"}
        "flags": flags,             # passed to score_label kwargs
        "label": SupplementLabel(
            sku_id=sku, product_name=name, primary_claim=claim, actives=[active], **kw),
    }


# ---------------------------------------------------------------------------
# A. §6 per-dimension PASS / FAIL anchors
# ---------------------------------------------------------------------------
FIXTURES = []

# --- Evidence (omega-3, claim is the variable, form held constant) ----------
FIXTURES.append(_f(
    "EV-PASS-omega3-tg", "Omega-3 TG (PASS)",
    "triglyceride lowering", LabelActive(
        active_slug="omega3", display_name="EPA/DHA", quantity=3000, unit="mg",
        form="triglyceride (TG)"),
    "omega3",
    expect={"grade_in": ["S", "A", "B"], "binding": C.MECH_BLEND_DOMINANT},
))
FIXTURES.append(_f(
    "EV-FAIL-omega3-brain", "Omega-3 brain/mood (FAIL)",
    "brain & mood / general cognition (BROAD consumer claim)", LabelActive(
        active_slug="omega3", display_name="EPA/DHA", quantity=3000, unit="mg",
        form="triglyceride (TG)"),
    "omega3",
    # Weak-evidence (35-59 band) drags the blend BELOW the TG-claim PASS anchor but
    # there is NO cap for Weak (only Insufficient caps, §3.2 cap 1). An otherwise-
    # excellent Weak product lands B (blend-bound by the Evidence dimension). The
    # FAIL is RELATIVE to the Strong-claim PASS anchor (same molecule, S vs B), which
    # is the omega-3 probe's whole point. See phase2_calibration_v1.md FLAG-1
    # (whether Weak should carry a B-ceiling cap is a Nutrition D8 question).
    expect={"grade_in": ["B", "C"], "binding": C.MECH_BLEND_DOMINANT},
))

# --- Dose (creatine) --------------------------------------------------------
FIXTURES.append(_f(
    "DOSE-PASS-creatine-5g", "Creatine 5g (PASS)",
    "strength / lean mass with resistance training", LabelActive(
        active_slug="creatine", display_name="Creatine monohydrate", quantity=5, unit="g",
        form="monohydrate"),
    "creatine",
    expect={"grade_in": ["S", "A"], "binding": C.MECH_BLEND_DOMINANT},
))
FIXTURES.append(_f(
    "DOSE-FAIL-creatine-1g", "Creatine HCl 1g (FAIL)",
    "strength / lean mass with resistance training", LabelActive(
        active_slug="creatine", display_name="Creatine HCl", quantity=1, unit="g",
        form="creatine HCl"),
    "creatine",
    expect={"grade_in": ["D"], "binding": C.MECH_CAP_2},
))

# --- Form (magnesium; elemental vs absorbed) --------------------------------
# NOTE (FLAG-2, phase2_calibration_v1.md): the magnesium dossier has min_effective=300
# mg ELEMENTAL but a governing UL=250 mg ELEMENTAL supplemental — an adequately-dosed
# Mg supplement structurally BREACHES the UL. Real dossier tension, flagged for Nutrition
# D8. To exercise the FORM axis cleanly (not confound it with a safety veto), these
# fixtures dose to ~245 mg elemental: just under the UL, landing sub-therapeutic-HIGH.
FIXTURES.append(_f(
    "FORM-PASS-mg-glycinate", "Mg glycinate (PASS)",
    "blood pressure reduction", LabelActive(
        active_slug="magnesium", display_name="Magnesium glycinate",
        quantity=1737, unit="mg", form="magnesium glycinate / bisglycinate"),
    "magnesium",
    # 1737 mg compound x 0.141 = ~245 mg elemental (just under UL, sub-therapeutic-high);
    # PREFERRED form + Moderate evidence -> blend-bound, lands B/C. PASS = good form.
    expect={"grade_in": ["B", "C"], "binding": C.MECH_BLEND_DOMINANT},
))
FIXTURES.append(_f(
    "FORM-FAIL-mg-oxide", "Mg oxide 'high elemental' (FAIL)",
    "blood pressure reduction", LabelActive(
        active_slug="magnesium", display_name="Magnesium oxide",
        quantity=406, unit="mg", form="magnesium oxide"),
    "magnesium",
    # 406 x 0.603 = ~245 mg elemental (same elemental as the glycinate PASS, just under
    # UL) but POOR form sold as premium + misleading 'high elemental' framing -> the
    # form-evidence coupling floor binds. Same dose, opposite Form verdict = the oxide paradox.
    flags={"form_sold_as_premium": True, "misleading_true": True,
           "form_evidence_coupling": True},
    expect={"grade_in": ["C", "D"], "binding": C.MECH_FLOOR_FORM_EV},
))

# --- Honesty (caffeine; disclosed vs hidden) --------------------------------
FIXTURES.append(_f(
    "HON-PASS-caffeine-200", "Caffeine 200mg disclosed (PASS)",
    "ergogenic / exercise performance (endurance, strength/power)", LabelActive(
        active_slug="caffeine", display_name="Caffeine anhydrous",
        quantity=200, unit="mg", form="caffeine anhydrous"),
    "caffeine",
    expect={"grade_in": ["S", "A", "B"], "binding": C.MECH_BLEND_DOMINANT},
))
FIXTURES.append(_f(
    "HON-FAIL-caffeine-blend", "Caffeine hidden in blend (FAIL)",
    "ergogenic / exercise performance (endurance, strength/power)", LabelActive(
        active_slug="caffeine", display_name="Caffeine (in proprietary energy blend)",
        quantity=None, unit="mg", form="caffeine anhydrous",
        is_core=True, in_proprietary_blend=True),
    "caffeine", proprietary_blend_total=1200, proprietary_blend_unit="mg",
    expect={"grade_in": ["D"], "binding": C.MECH_CAP_3_CORE},
))

# --- Safety (vitamin D3; within UL vs UL breach) ----------------------------
FIXTURES.append(_f(
    "SAFE-PASS-d3-2000", "Vitamin D3 2000 IU (PASS)",
    "correcting/maintaining vitamin D status (raising serum 25(OH)D)", LabelActive(
        active_slug="vitamin_d3", display_name="Vitamin D3", quantity=2000, unit="IU",
        form="D3 (cholecalciferol)"),
    "vitamin_d3",
    expect={"grade_in": ["S", "A"], "binding": C.MECH_BLEND_DOMINANT},
))
FIXTURES.append(_f(
    "SAFE-FAIL-d3-50k", "Vitamin D3 50,000 IU daily (FAIL)",
    "correcting/maintaining vitamin D status (raising serum 25(OH)D)", LabelActive(
        active_slug="vitamin_d3", display_name="Vitamin D3", quantity=50000, unit="IU",
        form="D3 (cholecalciferol)"),
    "vitamin_d3", labeled_regimen="daily",
    expect={"grade_in": ["E"], "binding": C.MECH_VETO_SAFETY},
))
# Safety control: 50k IU WEEKLY clinician-repletion -> regimen exemption (NOT vetoed)
FIXTURES.append(_f(
    "SAFE-CTRL-d3-50k-weekly", "Vitamin D3 50,000 IU weekly (clinical, control)",
    "correcting/maintaining vitamin D status (raising serum 25(OH)D)", LabelActive(
        active_slug="vitamin_d3", display_name="Vitamin D3", quantity=50000, unit="IU",
        form="D3 (cholecalciferol)"),
    "vitamin_d3", labeled_regimen="weekly",
    expect={"grade_not": ["E"], "binding_not": C.MECH_VETO_SAFETY},
))


# ---------------------------------------------------------------------------
# B. §13 THREE ATTRIBUTION ARCHETYPES — the decisive axis
# ---------------------------------------------------------------------------
ARCHETYPES = []

# 1. Good active / WASTED (1g fairy-dust creatine) -> D, binding = cap_2,
#    signature Evidence HIGH · Dose LOW.
ARCHETYPES.append(_f(
    "ARCH-wasted-creatine-1g", "Good active wasted (1g creatine)",
    "strength / lean mass with resistance training", LabelActive(
        active_slug="creatine", display_name="Creatine monohydrate",
        quantity=1, unit="g", form="monohydrate"),
    "creatine",
    expect={"grade_in": ["D"], "binding": C.MECH_CAP_2,
            "sig": {"evidence": "HIGH", "dose": "LOW"}},
))

# 2. Bad active / EXCELLENT product (no-evidence claim, impeccably made) ->
#    E (evidence ceiling), signature Evidence LOW · Dose N/A · Form HIGH · Honesty HIGH.
#    Use creatine marketed for FAT LOSS (dossier: Insufficient) at a perfect 5g / good form.
ARCHETYPES.append(_f(
    "ARCH-noevidence-creatine-fatloss", "Bad active excellent product (creatine for fat loss)",
    "fat loss / fat burning", LabelActive(
        active_slug="creatine", display_name="Creatine monohydrate",
        quantity=5, unit="g", form="monohydrate"),
    "creatine",
    expect={"grade_in": ["E"], "binding": C.MECH_CAP_1,
            "sig": {"evidence": "LOW", "dose": "N/A", "form": "HIGH"}},
))

# 3. Good active / DANGEROUS (50,000 IU D3 daily) -> E (safety floor),
#    signature Evidence HIGH · Safety VETO.
ARCHETYPES.append(_f(
    "ARCH-dangerous-d3-50k", "Good active dangerous (50k IU D3 daily)",
    "correcting/maintaining vitamin D status (raising serum 25(OH)D)", LabelActive(
        active_slug="vitamin_d3", display_name="Vitamin D3", quantity=50000, unit="IU",
        form="D3 (cholecalciferol)"),
    "vitamin_d3", labeled_regimen="daily",
    expect={"grade_in": ["E"], "binding": C.MECH_VETO_SAFETY,
            "sig": {"evidence": "HIGH", "safety": "VETO"}},
))


# ---------------------------------------------------------------------------
# C. §13.4 CLAIM-RESOLUTION fixtures (v1.3, TASK-171E) — proves the rule is
#    FAIR, not a loophole. R1 vague/evidenced -> B/A (NOT cap-1); R2 vague/snake-oil
#    -> E (cap-1); R3 over-specific-false -> D (cap-3 honesty / Weak tier).
# ---------------------------------------------------------------------------
RESOLUTION_FIXTURES = []

# R1. vague-claim / active-HAS-evidence (magnesium PoC-shaped: includes "heart"
#     so heart->BP=Moderate is the best mapped tier). 200 mg elemental bisglycinate,
#     preferred form, honest, safe. Resolution lifts it off a wrongful E.
#     Expected: B/A, binding = blend_dominant_limit (cap-1 must NOT fire).
RESOLUTION_FIXTURES.append(_f(
    "R1-vague-evidenced-mg", "Vague claim / magnesium has evidence (R1)",
    "supports bone, heart and muscle health", LabelActive(
        active_slug="magnesium", display_name="Magnesium bisglycinate",
        quantity=200, unit="mg", form="bisglycinate"),
    "magnesium",
    # heart->BP=Moderate (best), bone->BMD=Weak, muscle->sarcopenia=Weak.
    # 200 mg elemental, Moderate tier -> Dose computable, Form preferred (92),
    # Honesty 100, Safety neutral (<250). Resolution off E.
    expect={"grade_in": ["B", "A"], "binding": C.MECH_BLEND_DOMINANT},
))

# R2. vague-claim / SNAKE-OIL: constructed all-null umbrella active. Nothing maps.
#     Expected: E, binding = cap_1_insufficient_evidence; Dose = N/A.
RESOLUTION_FIXTURES.append(_f(
    "R2-vague-snakeoil", "Vague claim / snake-oil all-null umbrella (R2)",
    "supports wellness & vitality", LabelActive(
        active_slug="fixture_snakeoil", display_name="Wellness Blend X",
        quantity=500, unit="mg", form="proprietary"),
    "fixture_snakeoil",
    expect={"grade_in": ["E"], "binding": C.MECH_CAP_1,
            "sig": {"evidence": "LOW", "dose": "N/A"}},
))

# R3. OVER-SPECIFIC FALSE claim: magnesium "clinically proven to cure insomnia".
#     sleep endpoint resolves to Weak (real tier) AND the over-promise fires the
#     §2.4 claim-vs-substance gap -> §3 cap-3 honesty-core. Expected: D (marked
#     down, NOT a free A), binding = cap_3_honesty_core.
RESOLUTION_FIXTURES.append(_f(
    "R3-overspecific-false-mg", "Over-specific false claim / magnesium (R3)",
    "clinically proven to cure insomnia", LabelActive(
        active_slug="magnesium", display_name="Magnesium bisglycinate",
        quantity=200, unit="mg", form="bisglycinate"),
    "magnesium",
    expect={"grade_in": ["D"], "binding": C.MECH_CAP_3_CORE},
))


ALL_FIXTURES = FIXTURES + ARCHETYPES + RESOLUTION_FIXTURES
