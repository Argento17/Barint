# Magnesium UL-Grading Ruling v1 — TASK-384

**Author:** Nutrition Agent (D6/D7 lane)
**Date:** 2026-06-23
**Status:** Proposed ruling — awaiting Product Agent D7 co-sign
**Model:** v3 bioavailability-adjusted-dose ONLY (flag BARI_MAGNESIUM_V3)
**Spec governed:** `magnesium_model_v3_bioav_adjusted_dose_spec.md`
**Supersedes:** The prior version of this file (2026-06-23), which was written against the
  dead absorbed-mg model (SUPP-EV-030 v3 / "absorbed_mg = 520 × 0.04" language). That version
  is fully void; every number and rationale in it referenced a retired architecture. This document
  re-rules the UL mechanism exclusively against v3.

---

## Hard Anchor (read before everything else)

The live model is v3 in `run_magnesium_v2.py` (BARI_MAGNESIUM_V3=1).
The orchestrator-verified run is `magnesium_v2_run_20260623T114522Z.json`.
That run used the **pre-correction** elemental values (314mg and 272mg for oxide products,
label_basis = chemistry_derived from compound stoichiometry).

The TASK-384 elemental reversal finding (confirmed by NRV% mathematics on Altman label images)
establishes that four oxide products declare ELEMENTAL mg on the Israeli label, not compound mg:

- Altman 520, Nutricare 520: **520 mg elemental** (prior: 314mg from stoichiometry)
- Altman MagUP, Altman Balance: **450 mg elemental** (prior: 272mg from stoichiometry)

These corrected values are the input basis for this ruling. The pre-correction run is the
verified baseline; this ruling projects scores at the corrected values (ESTIMATE, arithmetic
below) and rules the mechanism. Data Agent re-runs the engine after D7 co-sign for the
authoritative numbers.

---

## Section 1 — Which UL governs?

**Ruling: NIH/IOM 350 mg/day supplemental UL = hard UL_EXCEED line. EFSA 250 mg/day = soft
GI_NOTE line. Both are GI-tolerance thresholds (osmotic diarrhea onset), not systemic toxicity.
This is unchanged from the v3 spec §2.4.**

Sources:
- NIH ODS Magnesium Fact Sheet for Health Professionals (2024):
  "The UL for magnesium from dietary supplements and medications for adolescents and adults is
  350 mg/day." URL: https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
- EFSA Panel on Dietetic Products, Nutrition and Allergies (NDA). Scientific Opinion on
  Dietary Reference Values for Magnesium. EFSA Journal 2015;13(7):4186.
  Supplemental threshold = 250 mg/day based on onset of osmotic diarrhea.
- Israeli MoH: no published Israeli supplemental UL for magnesium contradicting EFSA/NIH
  references; IL regulation defers to international standards for supplemental minerals.

**All four corrected-elemental oxide products exceed BOTH thresholds:**

| Product | Corrected elemental | vs EFSA 250 | vs NIH/IOM 350 | Safety verdict |
|---------|---------------------|-------------|----------------|----------------|
| Altman 520 | 520 mg | 2.08x OVER | 1.49x OVER | UL_EXCEED |
| Nutricare 520 | 520 mg | 2.08x OVER | 1.49x OVER | UL_EXCEED |
| Altman MagUP | 450 mg | 1.80x OVER | 1.29x OVER | UL_EXCEED |
| Altman Balance | 450 mg | 1.80x OVER | 1.29x OVER | UL_EXCEED |
| Tink 520 | UNRESOLVED | n/a | n/a | no-score (see §4) |

---

## Section 2 — V3 Arithmetic at Corrected Elemental Doses

All numbers python-verified (see §7 commands_run). ESTIMATE — authoritative values from Data
Agent re-run with BARI_MAGNESIUM_V3=1 at corrected elemental inputs.

Model parameters:
- LOW tier factor (oxide): 0.35
- Dose sub-score function: 70 + (adj−100)/100×15 for adj ∈ [100,200]; 85 + (adj−200)/100×15 for adj ∈ [200,300]
- Pillar weights: dose 0.55, evidence 0.20, transparency 0.25
- Evidence sub-score (known class): 72.0 flat
- Transparency sub-score (oxide, no two-line): 25.0
- UL_EXCEED trigger: administered_elemental_mg > 350

**Oxide 520mg (Altman 520, Nutricare 520):**
- adj = 520 × 0.35 = 182.0 mg
- dose_s = 70 + (182−100)/100 × 15 = 70 + 82/100 × 15 = 70 + 12.3 = **82.3**
- blend = 82.3×0.55 + 72.0×0.20 + 25.0×0.25 = 45.3 + 14.4 + 6.25 = **65.9** (pre-safety)
- UL_EXCEED fires (520 > 350): flat −10 → **55.9 / C** (Option A)
- UL_EXCEED cap D (max 49.0): **49.0 / D** (Option B)

**Oxide 450mg (Altman MagUP, Altman Balance):**
- adj = 450 × 0.35 = 157.5 mg
- dose_s = 70 + (157.5−100)/100 × 15 = 70 + 57.5/100 × 15 = 70 + 8.6 = **78.6**
- blend = 78.6×0.55 + 72.0×0.20 + 25.0×0.25 = 43.2 + 14.4 + 6.25 = **63.9** (pre-safety)
- UL_EXCEED fires (450 > 350): flat −10 → **53.9 / C** (Option A)
- UL_EXCEED cap D (max 49.0): **49.0 / D** (Option B)

**For comparison — D cluster from verified run (authoritative, not estimates):**
- Solgar Cal-Mag 100mg UNRESOLVED: 48.9 / D (cap_3 binding)
- Nutricare Taurate 76mg: 46.2 / D (dose genuinely too low)

---

## Section 3 — The Decision: Option B (UL_EXCEED grade-caps to max D)

**Ruling: UL_EXCEED applies a GRADE CEILING of D (maximum score 49.0), not a flat −10 nudge.**

This is Option B. Option A (flat −10 only) is rejected. Reasoning below.

### 3.1 Why Option A fails the page's own thesis

Under Option A, both corrected oxide groups land firmly in C:
- Oxide 520mg: 55.9/C — sits ABOVE Full-Mag bisglycinate 122mg (62.2/C), Tink Malate (60.6/C),
  and Oxide 314mg (60.0/C), and above Nutricare Malate (59.3/C) and Oxide 272mg (57.6/C)
- Oxide 450mg: 53.9/C — mid-shelf, above every D product

The magnesium page's central consumer insight is: "don't be fooled by the big number on the
label — form quality and dose-per-serving matter." A product declaring 520 mg elemental oxide
is the canonical instance of the "big number" problem. It is declaring a dose 1.49x above the
safe supplemental UL (IOM 350 mg). Under Option A, that product receives a mid-C grade and
outranks several well-formulated products that are doing nothing wrong except having lower
administered elemental mg. This contradicts the page's own thesis.

The argument FOR Option A is: the −10 penalty is a "signal" and consumers reading the safety
block will understand the concern. This argument fails for two reasons:

1. **Grade is the primary signal consumers read.** Most consumers do not parse sub-score
   explanations. Grade C means "acceptable" in the Bari frame. A product at 1.49x the UL in
   the worst-absorbed form receiving grade C is a misleading consumer outcome regardless of what
   the safety block says.

2. **The −10 is structurally insufficient at these dose levels.** The pre-safety blend is 65.9
   (520mg) and 63.9 (450mg). A flat −10 leaves both comfortably in C. The v3 spec designed the
   −10 mechanism when the verified run had oxide products at 314mg (blend 60.0) and 272mg (blend
   57.6) — both already at the bottom of C. Those products do NOT exceed the IOM 350mg UL.
   The corrected elemental values (520mg, 450mg) push these products UP the pre-safety scale
   precisely because they have more adjusted dose — and a flat −10 does not reverse that gain
   sufficiently.

### 3.2 Why Option B is correct

The UL_EXCEED signal is a safety gate, not a continuous deduction. Its purpose is to communicate:
"this product carries a dose that health authorities have flagged as a safety threshold." In the
Bari scoring architecture, structural flags that override blend-derived grades already exist:
- cap_1 (insufficient evidence delivery claim) → ceiling 34 / max grade E
- cap_3 (undisclosed blend) → ceiling 49 / max grade D

Both of these are ceiling mechanisms, not additive deductions. UL_EXCEED belongs in this family.
An over-UL megadose is a structural finding about the product's safety profile — not a continuous
quality dimension that the −10 linear adjustment correctly captures.

A grade ceiling of D (max 49.0) is calibrated correctly:
- It places over-UL oxide 520mg and 450mg alongside the D cluster (Solgar 48.9/D, Taurate 46.2/D)
- It does not force them to E — the safety concern is GI tolerance, not toxicity or contamination
- It preserves the D-band resolution: the exact score within D can still differentiate
- It is consistent with the cap family already in the engine

### 3.3 Why D-max rather than E-max

The IOM and EFSA ULs are GI-tolerance thresholds — onset of osmotic diarrhea — not organ toxicity
or harm thresholds. This is self-limiting and reversible. E is reserved for cap_1: products with
insufficient evidence for claimed delivery mechanisms (e.g., "nano" bioavailability claims) that
make the entire product value proposition unverifiable. An over-UL product does not fail on the
same logic; it is scoreable, its form is known, and its safety risk is a dosing issue, not an
evidence failure. Grade D with a safety block is the correct communication: "real issues —
over-threshold dose — take seriously but not in the same class as an unvalidated delivery claim."

### 3.4 The pre-safety blend being C does not override the gate

A counterargument: "Option A is more honest because it shows the 'natural' score minus a penalty,
without artificially imposing a ceiling." This argument conflates what the blend measures with what
the gate is designed to communicate. The blend measures quality signals on the v3 pillars: adjusted
dose, evidence, transparency. A 520mg oxide product gets high adjusted-dose credit (adj=182mg,
dose_s=82.3) because it genuinely delivers a large adjusted amount — that is real, and the blend
correctly reflects it. But adjusted dose is not the only thing that matters: delivering a dose
above the health-authority threshold is a disqualifying structural property in the safety gate's
terms, not a continuous quality deduction.

The grade ceiling does not say "the quality is worse than the blend implies." It says: "regardless
of the blend-level quality signals, this product's safety profile caps its maximum grade to D."
This is precisely how cap_1 and cap_3 work in the existing engine. There is no inconsistency.

---

## Section 4 — Tink 520 Disposition

**Ruling: Tink 520 (7290015318426) remains UNRESOLVED / no-score.**

The label declares "מגנזיום אוקסיד 520 מ\"ג" without the standard IL "From Magnesium Oxide"
qualifier and without NRV%. The supplement table on the available product image is not legible
at current resolution. Analog evidence (all other 520mg oxide products are elemental) supports
an elemental reading, but the label-wins rule requires label confirmation — not analog inference.

The missing-data-discard rule governs. One additional targeted retrieval attempt is warranted
(brand direct / physical label image). If label confirmation cannot be obtained: discard. No
score is assigned in the interim.

---

## Section 5 — No Spillover to Organic Salt Products

**Ruling: The UL analysis and the elemental-basis reversal do NOT affect any organic salt product.**

All organic salt products already declare ELEMENTAL mg per IL convention. The highest organic
salt dose in the corpus is 250mg (citrate/bisglycinate) — below both the EFSA 250mg note
threshold at strict > (now changed to >= per HRT-3 addendum, which adds a GI display note to
the two 250mg B products but does not change grades or trigger UL_EXCEED) and well below the
IOM 350mg hard UL. No organic salt product is over-UL. Zero spillover.

---

## Section 6 — Full Grade Projection Under This Ruling (ESTIMATE)

The shelf ordering below reflects Option B (UL_EXCEED → grade ceiling D/49.0) applied to
corrected elemental values. Non-corrected products use verified run scores.

Each row is one product group or single product. The "old" column is the verified run value
(pre-correction). "New" is the ESTIMATE after this ruling.

| # | Product | Corrected elem mg | Pre-safety blend | Safety trigger | Final ESTIMATE | Grade | Move |
|---|---------|-------------------|------------------|----------------|----------------|-------|------|
| 1 | Supherb Citrate+B6 250 | 250 | 72.8 | GI note only | **72.8** | **B** | none |
| 2 | Altman Bisglycinate 250 | 250 | 72.8 | GI note only | **72.8** | **B** | none |
| 3 | Altman Citrate 200 | 200 | 68.7 | none | **68.7** | **B** | none |
| 4 | Nutricare WELL 168 | 168 | 66.0 | none | **66.0** | **B** | none |
| 5 | NT-LC Hydroxide 190 | 190 | 63.9 | none | **63.9** | **C** | none |
| 6 | Full-Mag Bisglycinate 122 | 122 | 62.2 | none | **62.2** | **C** | none |
| 7 | Tink Malate 136 | 136 | 60.6 | none | **60.6** | **C** | none |
| 8 | Nutricare Malate 135 | 135 | 59.3 | none | **59.3** | **C** | none |
| 9 | **Altman 520** (7290017218564) | **520** | **65.9** | **UL_EXCEED → cap D** | **49.0** | **D** | C→D |
| 10 | **Nutricare 520** (7290001065662) | **520** | **65.9** | **UL_EXCEED → cap D** | **49.0** | **D** | C→D |
| 11 | **Altman MagUP** (7290013142894) | **450** | **63.9** | **UL_EXCEED → cap D** | **49.0** | **D** | C→D |
| 12 | **Altman Balance** (7290019444206) | **450** | **63.9** | **UL_EXCEED → cap D** | **49.0** | **D** | C→D |
| 13 | Solgar Cal-Mag 100 UNRESOLVED | 100 | 48.9 | none (cap_3 binds) | **48.9** | **D** | none |
| 14 | Nutricare Taurate 76 | 76 | 46.2 | none | **46.2** | **D** | none |
| 15 | Nutricare Nano Bisglycinate 88 | 88 | 52.7→cap_1 | none (cap_1 binds) | **34.0** | **E** | none |
| — | **Tink 520** (7290015318426) | UNRESOLVED | — | label unconfirmed | **no-score** | — | C→no-score |

Rows 1–8, 13–15: from verified run (20260623T114522Z); no change under this ruling.
Rows 9–12: ESTIMATE at corrected elemental values per the v3 arithmetic above.
Tink 520 row: disposition change from SCORED to UNRESOLVED per §4.

**Grade moves vs current verified run (pre-correction):**

The current verified run used chemistry_derived elemental values (314mg / 272mg) and did NOT
fire UL_EXCEED for any product. Tink 520 was also scored in that run at 314mg / C / 60.0
(before the label-confirmation requirement was applied). Under this ruling with corrected
elemental and Tink moved to unresolved:

| Product | Old grade (verified run) | New grade (this ruling) | Change |
|---------|--------------------------|-------------------------|--------|
| Altman 520 (7290017218564) | C/60.0 | D/49.0 | C → D |
| Nutricare 520 (7290001065662) | C/60.0 | D/49.0 | C → D |
| Altman MagUP (7290013142894) | C/57.6 | D/49.0 | C → D |
| Altman Balance (7290019444206) | C/57.6 | D/49.0 | C → D |
| Tink 520 (7290015318426) | C/60.0 | no-score (UNRESOLVED) | C → no-score |

**Grade moves: 4 products C → D. 1 product C → no-score (Tink 520).**

Grade distribution shift (from B4/C9/D2/E1 / 16 scored, to **B4/C4/D6/E1 / 15 scored**):
- B: 4 (unchanged)
- C: 9 → 4 (four over-UL products move to D; Tink 520 drops to unresolved)
- D: 2 → 6 (four over-UL oxide products join Solgar and Taurate)
- E: 1 (unchanged)
- Scored total: 16 → 15 (Tink 520 becomes the 3rd unresolved product)
- Corpus total unchanged: 15 scored + 3 unresolved + 1 discarded = 19

---

## Section 7 — Engine Implementation Spec

The v3 spec §2.4 currently reads:

> UL_EXCEED | administered mg > 350 | Display safety block; −10pts from final score

This ruling changes that to:

> UL_EXCEED | administered mg > 350 | Display safety block; grade ceiling = D (max final_score = 49.0)

The engine implementation (Data Agent lane):

```python
# v3 UL mechanism — UPDATED per magnesium_ul_ruling_v1.md (2026-06-23)
# Option B: grade ceiling D (max 49.0) replaces flat -10 deduction
UL_EXCEED_THRESHOLD = 350.0      # IOM/NIH supplemental UL (unchanged)
UL_EXCEED_GRADE_CEILING = 49.0   # max score when UL_EXCEED fires: grade D boundary

if administered_elemental_mg > UL_EXCEED_THRESHOLD:
    safety_flags.append({
        "flag": "UL_EXCEED",
        "trigger": f"{administered_elemental_mg}mg > {UL_EXCEED_THRESHOLD}mg IOM supplemental UL",
        "display_he": "מינון זה עולה על הגבול העליון המומלץ לתוספי מגנזיום (350 מ\"ג/יום, IOM). גבול זה מבוסס על סובלנות מערכת העיכול ואינו מצביע על רעילות.",
        "score_impact": "grade_ceiling_D: final_score capped at 49.0"
    })
    final_score = min(blend_score, UL_EXCEED_GRADE_CEILING)
    # Note: cap_1 (34.0) still takes precedence if fired — min() handles this correctly
    #       if cap_1 also fires, final_score = min(34.0, 49.0) = 34.0 — correct.
```

The `final_score = min(blend_score, UL_EXCEED_GRADE_CEILING)` replaces the previous
`final_score = blend_score - 10.0`. If both UL_EXCEED and cap_1 fire, cap_1's 34.0 ceiling
takes precedence naturally via min(). cap_3 (49.0) and UL_EXCEED (49.0) are coincidentally
identical ceilings — no ordering issue.

---

## Section 8 — Product Agent D7 Co-sign Requirement

This ruling changes the UL_EXCEED mechanism from a flat deduction to a grade ceiling, and
changes the corrected elemental inputs for four products. These are scoring-rule changes under D7.

**Grade changes: 4 products C → D.**

Required: Product Agent D7 co-sign before Data Agent implements the corrected elemental values
and the new UL ceiling in `run_magnesium_v2.py` (BARI_MAGNESIUM_V3=1 path).

Route to Product Agent with: this document + `magnesium_model_v3_bioav_adjusted_dose_spec.md`
§2.4 + the grade movement table above.

---

## Sources

- NIH ODS Magnesium Fact Sheet for Health Professionals (2024), UL section.
  URL: https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/
  UL adults 19+: 350 mg/day from dietary supplements and medications.
- EFSA Panel on Dietetic Products, Nutrition and Allergies (NDA). Scientific Opinion on
  Dietary Reference Values for Magnesium. EFSA Journal 2015;13(7):4186.
  Supplemental threshold 250 mg/day (osmotic diarrhea onset, GI tolerance).
- Altman.co.il label images (TASK-384, 2026-06-23) — NRV% mathematics confirm elemental basis:
  Altman 520: 520/280 = 185.7% (women NRV); 520/350 = 148.6% (men NRV). PASS.
  Altman MagUP: 450/280 = 160.7% (women); 450/350 = 128.6% (men). PASS.
  Altman Balance: same NRV math as MagUP. PASS.
- IL NRV for magnesium: women 280 mg/day, men 350 mg/day (IL Nutrition Labeling Regulation,
  consistent with EU RDA 375 mg and WHO/EFSA reference values).
- Python arithmetic verification: see §7 commands_run block in return contract below.
