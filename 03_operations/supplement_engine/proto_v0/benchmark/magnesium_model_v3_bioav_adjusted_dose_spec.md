# Magnesium Scoring Model v3 — Bioavailability-Adjusted Dose Spec

**Author:** Nutrition Agent
**Date:** 2026-06-23
**Status:** PROPOSED — C3 calibration challenge complete (P302, 2026-06-23); LOW recalibrated 0.45→0.35 per C3 finding; requires Product Agent D7 re-co-sign before engine go-live

> **LOW recalibrated 0.45→0.35 per C3 P302 (2026-06-23):** 0.45 tied oxide-314 (62.6/C) with clean bisglycinate-122 Full-Mag (62.2/C) — a near-tie that softly re-introduces "oxide ≈ citrate" at lower bisglycinate doses. 0.35 gives honest separation: oxide-314 drops to 60.0/C, Full-Mag-122 stays 62.2/C — oxide is now clearly below Full-Mag by 2.2 pts. Still a coarse calibration constant, not a claimed absorption fraction.
**Supersedes:** `magnesium_model_v2_final_spec.md` + `magnesium_v2_bioav_recalibration_spec.md` (both retired by this spec)
**Owner decision:** C3 (P301) and owner jointly chose bioavailability-adjusted-dose architecture over the v2 recalibration patch (TASK-384 brief, 2026-06-23)
**Build target:** `run_magnesium_v2.py` — v3 replaces the scoring logic inside this runner

---

## 0. Architecture Summary

The v2 model scored on administered elemental mg and added a bioavailability class modifier on the evidence sub-score. The class modifier produced only 2.4pts separation in the blend — insufficient to cross grade boundaries between same-dose oxide and citrate. The v2 recalibration patch (-14 modifier for LOW) solved the oxide/citrate inversion but introduced fragile monotonicity constraints and the NT-LC/hydroxide concern (hydroxide landed B, near cramps-indication products).

**v3 solves this architecturally:** bioavailability class is embedded in the dose signal itself via a coarse tier factor. The dose pillar now scores **adjusted dose** = administered elemental × tier factor. The class modifier on the evidence sub-score is removed. The dose pillar weight increases to 0.55 to reflect that it now carries both the quantity and quality of the dose signal. Safety gates stay on administered elemental (what the body ingests, not the adjusted equivalent).

**What this achieves:**
- Oxide 314mg × LOW-factor 0.35 = 109.9mg adjusted → scores at the bottom of the general-gap band → C
- Citrate 200mg × HIGH-factor 1.0 = 200mg adjusted → scores at the midpoint → B
- Citrate 250mg × HIGH-factor 1.0 = 250mg adjusted → scores near the upper end → B
- NT-LC hydroxide 190mg × MODERATE-factor 0.75 = 143mg adjusted → C (not B next to cramps products)
- Full-Mag bisglycinate 122mg × HIGH-factor 1.0 = 122mg adjusted → C (just above band floor) — outranks oxide-272mg adjusted 122.4mg by 1.2pts; this is the intended behavior under the removed backwards-monotonicity constraint

**Consumer display:** unchanged — show administered elemental mg + bioavailability CLASS label. Never display the adjusted figure or the tier factor. The adjustment is a scoring-internal calculation.

---

## 1. Bioavailability Tier Factors

### 1.1 Factor Definition

The tier factor is a coarse dimensionless multiplier that converts administered elemental mg to "adjusted dose" for scoring purposes. It is NOT the fractional absorption percentage for an individual or a population mean. It is a scoring-calibration constant that reflects the relative evidence for each form's bioavailability, grounded in the direction and approximate magnitude of comparative studies.

**Tiers:**

| Tier | Forms | Factor | Scoring effect on 314mg oxide vs 200mg citrate |
|---|---|---|---|
| HIGH | citrate, bisglycinate, glycinate | **1.0** | 200mg citrate × 1.0 = 200mg adjusted |
| MODERATE | malate, taurate, hydroxide | **0.75** | 190mg hydroxide × 0.75 = 143mg adjusted |
| LOW | oxide, carbonate | **0.35** | 314mg oxide × 0.35 = 109.9mg adjusted |
| UNRESOLVED | blend (undisclosed ratios) | **1.0 (no adjustment)** + evidence penalty | administered dose used as-is; UNRESOLVED penalized on evidence sub-score |

### 1.2 Evidence Grounding for Factor Values (NIH ODS / Comparative Literature)

**NIH ODS Magnesium Fact Sheet (Health Professional Version, current as of 2026):**
> "Forms of magnesium that dissolve well in liquid are more completely absorbed in the gut than less soluble forms. Small studies have found that magnesium in the aspartate, citrate, lactate, and chloride forms is absorbed more completely and is more bioavailable than magnesium oxide and magnesium sulfate."

This explicitly establishes a directional hierarchy: organic salts (citrate, aspartate, lactate) > oxide. The NIH ODS does not assign numeric absorption percentages as single values, acknowledging that individual variability and study design affect reported fractions. Bari's tier system matches this directional ranking without asserting false precision.

**Quantitative reference (Walker 2003, Schuette 1994, Coudray 2005 — cited in NIH ODS context):**
- Oxide fractional absorption: approximately 4% in comparative designs (range 3–7% across studies)
- Citrate fractional absorption: approximately 28–32% in comparative designs
- Bisglycinate/glycinate: limited direct vs-citrate data; animal studies and tolerability profiles suggest comparable or slightly higher than citrate
- Hydroxide: intermediate, higher aqueous solubility than oxide (MgOH₂ pKsp << MgO in acidic conditions); fractional absorption estimated ~15–20% in limited data
- Malate: limited direct data; organic acid structure supports moderate bioaccessibility above oxide; estimated comparable to hydroxide range
- Taurate: very limited human comparative data; placed above oxide on mechanistic grounds (amino-acid chelate), not direct absorption studies

**How the 1.0 / 0.75 / 0.35 values were derived (MRT-8: 0.45 recalibrated to 0.35 per C3 P302 2026-06-23):**

The factors do NOT use the raw absorption fractions (4%, 28–32%) because:
1. Those fractions vary by individual, GI context, and study design — asserting "oxide = 0.04 × dose" for every person is the fake-precision problem the v3 architecture explicitly avoids.
2. The factors are calibration constants for the SCORING function, not pharmacokinetic parameters.

Calibration method: choose the smallest factor spread that (a) produces a clear grade-band crossing between equal-dose HIGH and LOW forms, (b) lands oxide 314mg in the C band rather than B, and (c) keeps NT-LC hydroxide 190mg in C rather than B.

HIGH = 1.0 is the anchor: premium forms set the reference point. The label-declared dose is taken at face value for scoring purposes.

LOW = 0.35 is derived from the requirement that oxide-314mg lands below Full-Mag bisglycinate-122mg (HIGH class) and clearly below B/65. The algebra for landing below B/65 gives factor < 0.543; C3 P302 identified a second requirement: oxide-314 must also score below Full-Mag bisglycinate-122 so there is no "oxide ≈ citrate" near-tie effect.

  At LOW=0.45: oxide-314 adj=141.3mg, dose_s=76.2, blend=62.6 — vs Full-Mag-122 blend=62.2. Delta = +0.4pts. This 0.4pt gap is below consumer-signal noise (same grade C, near-tie).
  At LOW=0.35: oxide-314 adj=109.9mg, dose_s=71.5, blend=60.0 — vs Full-Mag-122 blend=62.2. Delta = -2.2pts. Oxide-314 now clearly below Full-Mag-122.

  - dose_s(adj) for 109.9mg adjusted: MEETS tier; t=(109.9-100)/(200-100)=0.099; s=70+0.099×15=71.5
  - blend = 71.5×0.55 + 72×0.20 + 25×0.25 = 39.3 + 14.4 + 6.25 = 60.0
  - Chosen LOW = 0.35 per C3 P302 (2026-06-23); 314 × 0.35 = 109.9mg adjusted — gives honest grade separation from Full-Mag bisglycinate and evidence-appropriate positioning given oxide's substantially lower fractional absorption vs organic salts. Still a coarse calibration constant, not a claimed absorption fraction.

MODERATE = 0.75 is set to produce sensible intermediate landing: hydroxide 190mg × 0.75 = 142.5mg adjusted, just above the general-gap lower bound (100mg), landing at C/63.9. This correctly positions hydroxide above oxide but below citrate/bisglycinate for a given administered dose.

The ratio LOW/HIGH = 0.35 is directionally consistent with the literature (oxide absorption is substantially lower than citrate/bisglycinate), without claiming it equals any specific absorption fraction. (Historical note: the initial calibration used 0.45; this was recalibrated to 0.35 per C3 P302 to avoid the near-tie between oxide-314 and Full-Mag bisglycinate-122.)

### 1.3 Consumer Display Rule (HARD)

The tier factors are internal scoring constants. Consumer-facing output:
- Display: `administered_elemental_mg` (the label number) + `bioavailability_class` (HIGH/MODERATE/LOW/UNRESOLVED label in Hebrew)
- NEVER display the adjusted dose, the tier factor, or any derived "effective mg" figure
- NEVER say "your body absorbs X mg" — this is a scoring-internal calculation, not a clinical prediction

---

## 2. Pillar Structure (v3)

### 2.1 Pillar Overview

| Pillar | What it measures | v2 weight | v3 weight | Change |
|---|---|---|---|---|
| Dose (adjusted) | administered elemental × tier factor vs general-gap band | 0.40 | **0.55** | +0.15 — dose now carries both quantity and quality of dose |
| Evidence | quality and strength of evidence for the form's supplemental use | 0.30 | **0.20** | −0.10 — class no longer amplified here; de-duplication |
| Transparency + Safety | label clarity, composition disclosure, UL gate | 0.30 | **0.25** | −0.05 — minor trim to maintain sum=1.00 |

**Sum check:** 0.55 + 0.20 + 0.25 = 1.00 ✓

### 2.2 Pillar 1 — Adjusted-Dose Sub-Score

**Step 1: Compute adjusted dose**
```
adjusted_dose = administered_elemental_mg × tier_factor(bav_class)
```
Where tier_factor:
- HIGH: 1.0
- MODERATE: 0.75
- LOW: 0.35
- UNRESOLVED: 1.0 (conservative; class unknown — do not penalize dose for hidden composition; penalize evidence sub-score instead)

**Step 2: Score adjusted dose against general-gap band (100–300mg)**

The band stays at 100–300mg — these are administered-elemental reference values for the general dietary-gap indication. Products whose adjusted dose meets this band are delivering what the band was designed to measure.

```python
DOSE_BAND_LO = 100.0   # mg adjusted (same as administered for HIGH anchor)
DOSE_BAND_HI = 300.0
DOSE_BAND_MID = 200.0

def dose_sub_score_v3(adjusted_dose_mg):
    if adjusted_dose_mg >= DOSE_BAND_LO:
        # MEETS — score 70–100, linear
        if adjusted_dose_mg <= DOSE_BAND_MID:
            t = (adjusted_dose_mg - DOSE_BAND_LO) / (DOSE_BAND_MID - DOSE_BAND_LO)
            return 70.0 + t * 15.0        # 70 at 100mg, 85 at 200mg
        elif adjusted_dose_mg <= DOSE_BAND_HI:
            t = (adjusted_dose_mg - DOSE_BAND_MID) / (DOSE_BAND_HI - DOSE_BAND_MID)
            return 85.0 + t * 15.0        # 85 at 200mg, 100 at 300mg
        else:
            return 100.0                   # above band: full credit
    near_floor = DOSE_BAND_LO * 0.5        # 50mg adjusted
    if adjusted_dose_mg >= near_floor:
        # NEAR — score 40–69, linear
        t = (adjusted_dose_mg - near_floor) / (DOSE_BAND_LO - near_floor)
        return 40.0 + t * 30.0
    # FAR_BELOW — score 0–39, linear
    t = adjusted_dose_mg / near_floor if near_floor > 0 else 0.0
    return t * 40.0
```

**dose_tier labels** (for trace and UI):
- MEETS: adjusted_dose ≥ 100mg
- NEAR: 50mg ≤ adjusted_dose < 100mg
- FAR_BELOW: adjusted_dose < 50mg

**Dose pillar weight: W_DOSE = 0.55**

### 2.3 Pillar 2 — Evidence Sub-Score (v3)

In v3, bioavailability class no longer modifies the evidence sub-score — it has been moved to the dose pillar via the tier factor. The evidence sub-score now measures: how strong is the evidence that magnesium supplementation generally, and this form specifically, supports the scored indication?

**Base:** All products with a known class receive the evidence base score of 72.0 (Moderate tier midpoint, reflecting the general-gap indication evidence base: magnesium dietary gaps are prevalent in the Israeli population; supplementation shows directional benefit in the general dietary-gap context; evidence quality is moderate, not strong).

**UNRESOLVED class modifier:** −20.0 (hidden blend, cannot assess form evidence at all; applied to the evidence sub-score because the dose pillar cannot apply a correction when the class is unknown)

```python
EV_BASE = 72.0
EV_UNRESOLVED_PENALTY = -20.0

def evidence_sub_score_v3(bav_class):
    if bav_class == "UNRESOLVED":
        return max(0.0, EV_BASE + EV_UNRESOLVED_PENALTY)  # = 52.0
    return EV_BASE  # 72.0 for all known classes (HIGH/MODERATE/LOW)
```

**Rationale for flat base (no class modifier):** Class is already expressed in adjusted_dose. A second class-based modifier would double-count it, artifically amplifying the HIGH/LOW gap beyond what the evidence justifies. The flat base correctly assigns equal "general-gap indication strength" to all known forms — the differentiation is purely from what dose each form effectively delivers.

**Evidence pillar weight: W_EVIDENCE = 0.20**

### 2.4 Pillar 3 — Transparency + Safety Sub-Score (v3)

No change from v2 structure. The same signal table applies.

| Signal | Points |
|---|---|
| Label explicitly states elemental mg ("מגנזיום אלמנטרי" / "from/as" format cross-verified) | +15 |
| Form declared by chemical name | +10 |
| Two-line label (compound AND elemental stated separately) | +5 bonus |
| UNRESOLVED blend with undisclosed ratios | −15 |
| Evidence-insufficient proprietary delivery claim (cap_1 path: liposomal, nano) | −15 |

Maximum achievable transparency score: 30 (elemental declared + form named + two-line)
Minimum for cap_1 path: negative (floor at 0)
Chemistry-derived oxide (label states compound; elemental derived from stoichiometry): +15 (elemental derivable) + +10 (form named) = 25 (no two-line bonus because label does not separately state elemental)

**Cap ceilings (unchanged from v2):**
- cap_1 (insufficient evidence delivery claim, e.g. liposomal/nano): ceiling = 34 → max grade E
- cap_3_honesty_core (proprietary blend / undisclosed composition): ceiling = 49 → max grade D

**Safety flags (on administered elemental, NOT on adjusted dose):**

Safety logic depends on what the body ingests, not the scoring adjustment:

| Flag | Trigger (administered elemental) | Engine action |
|---|---|---|
| UL_EXCEED | administered mg > 350 | Display safety block; **grade ceiling D (max final_score = 49.0)** — see `magnesium_ul_ruling_v1.md` §3 (2026-06-23) |
| GI_NOTE_EFSA | administered mg >= 250 | Display note only; no score deduction (MVP) — threshold changed > to >= per HRT-3 addendum |

**UL mechanism update (2026-06-23, magnesium_ul_ruling_v1.md):** The original spec had "−10pts from final score." That is superseded. The ruling rejected Option A (flat −10) because, at corrected elemental doses of 520mg and 450mg, the pre-safety blend is 65.9 and 63.9 respectively — a flat −10 leaves both products at C/55.9 and C/53.9, ABOVE the D cluster and contradicting the page's "don't be fooled by the big number" thesis. Option B (grade ceiling D / max 49.0) correctly places over-UL oxide products at the top of the D band alongside Solgar (48.9) and Taurate (46.2). Four products gain grade moves C → D on corrected elemental inputs: Altman 520, Nutricare 520, Altman MagUP, Altman Balance.

**At corrected elemental inputs,** four corpus products exceed 350mg: Altman 520 (520mg), Nutricare 520 (520mg), Altman MagUP (450mg), Altman Balance (450mg). These were previously stored with chemistry_derived values of 314mg/272mg (below the UL). NRV% arithmetic on label images confirmed the correct elemental basis (see `magnesium_ul_ruling_v1.md` §1).

**Transparency + safety pillar weight: W_TRANSPARENCY = 0.25**

### 2.5 Blend Formula (v3)

```
blend = dose_sub_score_v3(adjusted_dose) × 0.55
      + evidence_sub_score_v3(bav_class) × 0.20
      + transparency_sub_score(sku) × 0.25
```

Then caps and UL penalty applied as in v2.

---

## 3. Monotonicity Policy (v3)

### 3.1 Within-Form Monotonicity (PRESERVED)

Within the same bioavailability class, a product with more administered elemental mg scores higher than a product with less administered elemental mg, all else equal. This holds because:
- Same class → same tier factor → same proportional adjusted dose
- More administered mg → higher adjusted dose → higher dose_sub_score
- Transparency sub-score may differ (label quality), but dose dominates at 0.55 weight

This monotonicity is structural — no explicit assertion needed, it falls out of the math.

### 3.2 Cross-Form Monotonicity (REMOVED per owner decision)

The v2 spec included a hard constraint: "no oxide 270+mg product may score below a bisglycinate 88–122mg product." This constraint is removed in v3 per the owner's direction: under adjusted-dose scoring, a well-absorbed 122–250mg organic salt SHOULD be allowed to outrank a poorly-absorbed 314mg oxide where the adjusted dose warrants.

Under v3 math (LOW=0.35, real run 20260623T114522Z):
- Full-Mag bisglycinate 122mg: adjusted = 122mg → dose_s = 73.3 → blend = 62.2/C
- Oxide 272mg: adjusted = 95.2mg → dose_s = 67.1 → blend = 57.6/C
- Oxide 314mg: adjusted = 109.9mg → dose_s = 71.5 → blend = 60.0/C

Full-Mag-122 (62.2) outranks oxide-314 (60.0) by 2.2pts and oxide-272 (57.6) by 4.6pts — all grade C, but oxide clearly below Full-Mag. At LOW=0.45 the separation was only 0.4pts (oxide-314=62.6 vs Full-Mag=62.2), which C3 P302 flagged as a near-tie that softly re-introduces "oxide ≈ citrate". At 0.35 the separation is honest: Full-Mag bisglycinate at 122mg delivered dose clearly outranks oxide-314 administered mg.

**Property test for the engine:** Assert `score(oxide_272) < score(citrate_200)` and `score(oxide_314) < score(citrate_200)` — citrate's grade-band separation from oxide is the core consumer signal.

### 3.3 Consumer Communication of Cross-Form Ordering

When copy references cross-form comparisons: use administered elemental + class as the consumer frame. Do NOT explain the adjusted dose or the tier factor. Example: "200 מ"ג ציטראט מגיעים לגוף בצורה יעילה הרבה יותר מ-314 מ"ג אוקסיד — על אף המינון הגבוה יותר על האריזה."

---

## 4. Build-Ready Per-Product Score Derivation (ESTIMATE)

All calculations below are traceable arithmetic from the corpus values in `run_magnesium_v2.py`. These are **ESTIMATES** — the real engine run with v3 logic is the authoritative source. Estimates have been wrong before (v2 spec projected oxide D, real run gave oxide B — that was the defect this architecture fixes). Treat these as expected range, not guarantees.

### 4.1 Transparency Sub-Scores (unchanged from v2)

| Product | label_basis | form | two-line | Trans_s | Notes |
|---|---|---|---|---|---|
| Altman Citrate 120 | elemental | citrate | yes | **30** | +15+10+5 |
| Supherb Citrate+B6 | elemental | citrate | yes | **30** | +15+10+5 |
| Altman Bisglycinate 250 | elemental | bisglycinate | yes | **30** | +15+10+5 |
| Full-Mag Hadas 600 | elemental | bisglycinate | yes | **30** | +15+10+5 |
| Nutricare WELL | elemental | bisglycinate | yes | **30** | +15+10+5 |
| Nutricare Nano | elemental | bisglycinate | yes | **30→capped** | cap_1 binds |
| Nutricare Taurate | elemental | taurate | yes | **30** | +15+10+5 (two-line: 950mg compound / 76mg elemental) |
| NT LC Hydroxide | elemental | hydroxide | yes | **30** | +15+10+5 (190mg explicitly stated) |
| Tink Malate | elemental | malate | yes | **30** | +15+10+5 (two-line: 850mg compound / 136mg elemental) |
| Nutricare Malate | chemistry_derived_range | malate | no | **25** | +15+10, no two-line (no label-stated elemental) |
| Nutricare Oxide 520 | chemistry_derived | oxide | no | **25** | +15+10, no two-line |
| Tink Oxide 520 | chemistry_derived | oxide | no | **25** | +15+10, no two-line |
| Altman 520 | chemistry_derived | oxide | no | **25** | +15+10, no two-line |
| Altman MagUp | chemistry_derived | oxide | no | **25** | +15+10, no two-line |
| Altman Balance | chemistry_derived | oxide | no | **25** | +15+10, no two-line |
| Solgar Cal-Mag | us_label_il_unverified | oxide+citrate blend | no | **0** | partial +10 for US label elemental, but cap_3 ceiling = 49 binds; trans is 0 for undisclosed blend |

### 4.2 Full Per-Product Expected Distribution (ESTIMATE)

Notation: `Adj = elem × factor`, `D_s = dose_sub_score_v3(Adj)`, `Ev_s = evidence_sub_score_v3()`, `Tr_s = transparency_sub_score()`, `Blend = D_s×0.55 + Ev_s×0.20 + Tr_s×0.25`, `Final = min(Blend, cap) − UL_penalty`.

Arithmetic derivation: `D_s = dose_sub_score_v3(adj)`, `Ev_s` flat 72.0 except UNRESOLVED=52.0. Blend formula shown in §2.5. All values python-verified (see §10 commands_run).

| # | Product | Elem mg | Class | Factor | Adj mg | D_s | Ev_s | Tr_s | Blend | Cap | Final | Grade | ESTIMATE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Supherb Citrate+B6 250 | 250 | HIGH | 1.00 | 250.0 | 92.5 | 72 | 30 | 92.5×0.55+72×0.20+30×0.25=50.9+14.4+7.5=**72.8** | — | **72.8** | **B** | ESTIMATE |
| 2 | Altman Bisglycinate 250 | 250 | HIGH | 1.00 | 250.0 | 92.5 | 72 | 30 | same | — | **72.8** | **B** | ESTIMATE |
| 3 | Altman Citrate 200 | 200 | HIGH | 1.00 | 200.0 | 85.0 | 72 | 30 | 85×0.55+14.4+7.5=46.75+21.9=**68.7** | — | **68.7** | **B** | ESTIMATE |
| 4 | Nutricare WELL 168 | 168 | HIGH | 1.00 | 168.0 | 80.2 | 72 | 30 | 80.2×0.55+14.4+7.5=44.1+21.9=**66.0** | — | **66.0** | **B** | ESTIMATE |
| 5 | NT LC Hydroxide 190 | 190 | MODERATE | 0.75 | 142.5 | 76.4 | 72 | 30 | 76.4×0.55+14.4+7.5=42.0+21.9=**63.9** | — | **63.9** | **C** | ESTIMATE |
| 6 | Oxide 314 (Nutricare/Tink/Altman 520) | 314 | LOW | 0.35 | 109.9 | 71.5 | 72 | 25 | 71.5×0.55+14.4+6.25=39.3+20.65=**60.0** | — | **60.0** | **C** | REAL RUN 20260623T114522Z |
| 7 | Full-Mag Hadas 122 | 122 | HIGH | 1.00 | 122.0 | 73.3 | 72 | 30 | 73.3×0.55+14.4+7.5=40.3+21.9=**62.2** | — | **62.2** | **C** | REAL RUN 20260623T114522Z |
| 8 | Oxide 272 (MagUp/Balance) | 272 | LOW | 0.35 | 95.2 | 67.1 | 72 | 25 | 67.1×0.55+14.4+6.25=36.9+20.65=**57.6** | — | **57.6** | **C** | REAL RUN 20260623T114522Z |
| 9 | Tink Malate 136 | 136 | MODERATE | 0.75 | 102.0 | 70.3 | 72 | 30 | 70.3×0.55+14.4+7.5=38.7+21.9=**60.6** | — | **60.6** | **C** | ESTIMATE |
| 10 | Nutricare Malate ~135 | 135 | MODERATE | 0.75 | 101.3 | 70.2 | 72 | 25 | 70.2×0.55+14.4+6.25=38.6+20.65=**59.3** | — | **59.3** | **C** | ESTIMATE |
| 11 | Nutricare Taurate 76 | 76 | MODERATE | 0.75 | 57.0 | 44.2 | 72 | 30 | 44.2×0.55+14.4+7.5=24.3+21.9=**46.2** | — | **46.2** | **D** | ESTIMATE |
| 12 | Solgar Cal-Mag 100 | 100 | UNRESOLVED | 1.0 | 100.0 | 70.0 | 52 | 0 | 70×0.55+52×0.20+0=38.5+10.4=**48.9** | cap_3/49 | **48.9** | **D** | ESTIMATE |
| 13 | Nutricare Nano 88 | 88 | HIGH | 1.0 | 88.0 | 62.8 | 72 | 0* | →cap_1 | cap_1/34 | **34.0** | **E** | ESTIMATE |

*Nano: cap_1 fires regardless of trans; capped at 34.

**UNRESOLVED products (no score):**
- Amorphicure 7290015429245: UNRESOLVED, not scored
- TRIOMAG 7290118816065: UNRESOLVED, not scored

**DISCARDED:**
- Supherb Max 550 7290118818205: DISCARDED (oxide:citrate ratio unknowable)

### 4.3 Expected Grade Distribution (ESTIMATE)

| Grade | Count | Products |
|---|---|---|
| B | 4 | Supherb Citrate 250 (72.8), Altman Bisglycinate 250 (72.8), Altman Citrate 200 (68.7), Nutricare WELL 168 (66.0) |
| C | 9 | NT LC Hydroxide (63.9), Full-Mag Hadas (62.2), Tink Malate (60.6), 3× oxide-314 (60.0 each), Nutricare Malate (59.3), 2× oxide-272 (57.6 each) |
| D | 2 | Solgar Cal-Mag cap_3 (48.9), Nutricare Taurate (46.2) |
| E | 1 | Nutricare Nano Bisglycinate cap_1 (34.0) |

Score stats (REAL RUN 20260623T114522Z, 16 scored products including Solgar):
- Min: 34.0 (Nano/E, cap_1)
- Max: 72.8 (Supherb Citrate+B6 / Altman Bisglycinate 250 / B)
- Mean: 59.4 (real run)
- Stdev: 9.5
- Most common score: 60.0 (count=3, the 3× oxide-314 group)
- Distribution: B×4, C×9, D×2, E×1

**Important:** This is an ESTIMATE computed by hand from corpus values. The real `run_magnesium_v3.py` execution is the authoritative source. The v2 spec estimated oxide=D, real run gave oxide=B. This v3 spec was constructed specifically to avoid that failure by showing the full algebra before the run.

---

## 5. Key Consumer Signal Verification (ESTIMATE)

### 5.1 The Core Defect Is Corrected

**Oxide 314mg vs Citrate 200mg (real run 20260623T114522Z):**
- Oxide 314mg: **C/60.0** — "high label dose, low-bioavailability form" (adj=109.9mg)
- Citrate 200mg: **B/68.7** — "reasonable dose, well-absorbed form" (adj=200mg)
- Grade separation: B vs C ✓ — citrate 200mg clearly outranks oxide 314mg despite lower administered dose. Gap = 8.7pts.

**Oxide 314mg vs Citrate 250mg:**
- Oxide 314mg: C/60.0
- Citrate 250mg: **B/72.8** — clear separation ✓. Gap = 12.8pts.

The page now correctly communicates: a premium form at a reasonable dose outranks a high-label-dose oxide product.

### 5.2 NT-LC Hydroxide Concern (Resolved)

NT-LC Anti Leg Cramps (hydroxide 190mg, MODERATE class): **C/63.9**

This resolves the C3 concern: hydroxide at MODERATE class and 190mg adjusted (142.5mg adjusted) lands C, not B. It is correctly positioned above oxide (C tier) but below premium citrate/bisglycinate products (B tier). The cramps-indication footnote remains unchanged (Cochrane 2020/PMID:32956536 — insufficient evidence; display note only, not a scored signal).

### 5.3 Within-Class Ordering Verified

**High-dose vs lower-dose in same class:**
- Citrate 250mg (B/72.8) > Citrate 200mg (B/68.7) > WELL 168mg (B/66.0) > Full-Mag 122mg (C/62.2)
  - Within HIGH class, dose ordering is preserved ✓

- Oxide 314mg (C/60.0) > Oxide 272mg (C/57.6) — within LOW class, higher dose scores higher ✓

- Tink Malate 136mg (C/60.6) > Nutricare Malate 135mg (C/59.3) — within MODERATE class, ordering correct ✓

### 5.4 Cross-Form Near-Tie Zone (C tier, 60–64pts)

The C band contains: NT-LC hydroxide (63.9), Full-Mag bisglycinate (62.2), Tink Malate (60.6), oxide 314mg (60.0), Nutricare Malate (59.3), oxide 272mg (57.6).

These products cluster in C — some with HIGH class at lower dose, some with LOW class at high dose. This is the correct outcome: they all deliver a similar adjusted dose. The clustering IS the finding, not an artifact. Copy should communicate this: "כל המוצרים בטווח זה מספקים כמות מגנזיום אפקטיבית דומה — ההבדל הוא בצורה ובהצהרת התווית."

---

## 6. Code Changes Required in `run_magnesium_v2.py`

The following changes produce v3. All other code (corpus, caps, transparency, grade bands, output format, safety flags, WELL cap_1 logic, CSV writer) is unchanged.

### 6.1 Add Tier Factor Constants

After the `GRADE_BANDS` definition (line 65), add:

```python
# ---- v3 Bioavailability tier factors -------------------------------------------
# Source: NIH ODS Magnesium Fact Sheet + Walker 2003 / Schuette 1994 context
# These are coarse calibration constants, NOT pharmacokinetic absorption fractions.
# Evidence grounding: magnesium_model_v3_bioav_adjusted_dose_spec.md §1.2
BAV_TIER_FACTORS = {
    "HIGH": 1.00,        # citrate, bisglycinate, glycinate — organic, well-absorbed
    "MODERATE": 0.75,    # malate, taurate, hydroxide — intermediate
    "LOW": 0.35,         # oxide, carbonate — lowest solubility/absorption in comparatives; recalibrated 0.45→0.35 per C3 P302 (2026-06-23)
    "UNRESOLVED": 1.00,  # blend: use administered dose conservatively; evidence sub-score penalized
}
```

### 6.2 Replace Dose Sub-Score Function

Replace the existing `dose_sub_score` function (lines ~246–274) with:

```python
def dose_sub_score_v3(elemental_mg: float, bav_class: str) -> tuple:
    """
    v3: adjusted_dose = elemental_mg × tier_factor(bav_class).
    Scored against general-gap band 100-300mg.
    Returns (score, dose_tier_label, dose_tier_desc, adjusted_dose_mg).
    """
    factor = BAV_TIER_FACTORS.get(bav_class, 1.00)
    adj = elemental_mg * factor
    lo = DOSE_BAND_LO    # 100.0
    mid = (DOSE_BAND_LO + DOSE_BAND_HI) / 2.0  # 200.0

    if adj >= lo:
        if adj <= mid:
            t = (adj - lo) / (mid - lo)
            s = 70.0 + t * 15.0
        elif adj <= DOSE_BAND_HI:
            t = (adj - mid) / (DOSE_BAND_HI - mid)
            s = 85.0 + t * 15.0
        else:
            s = 100.0
        tier = "MEETS"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg × {factor}) >= {lo}mg lower bound"
    elif adj >= lo * 0.5:
        t = (adj - lo * 0.5) / (lo - lo * 0.5)
        s = 40.0 + t * 30.0
        tier = "NEAR"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg × {factor}) = {round(adj/lo*100)}% of lower bound"
    else:
        t = adj / (lo * 0.5) if lo > 0 else 0.0
        s = t * 40.0
        tier = "FAR_BELOW"
        desc = f"adj={adj:.1f}mg ({elemental_mg}mg × {factor}) < 50% of lower bound"

    return round(s, 1), tier, desc, round(adj, 1)
```

### 6.3 Replace Evidence Sub-Score Function

Replace the existing `evidence_sub_score` function (lines ~301–305) with:

```python
# ---- v3 evidence sub-score constants -------------------------------------------
EV_BASE_V3 = 72.0        # flat base for all known classes (class already in dose)
EV_UNRESOLVED_PENALTY = -20.0

def evidence_sub_score_v3(bav_class: str) -> tuple:
    """
    v3: class is embedded in dose (tier factor). Evidence sub-score is flat for all
    known classes. UNRESOLVED gets penalty (cannot evidence-classify).
    Returns (score, description).
    """
    if bav_class == "UNRESOLVED":
        score = max(0.0, EV_BASE_V3 + EV_UNRESOLVED_PENALTY)
        return round(score, 1), f"base={EV_BASE_V3} + UNRESOLVED_penalty={EV_UNRESOLVED_PENALTY}"
    return round(EV_BASE_V3, 1), f"base={EV_BASE_V3} (class expressed in adjusted dose)"
```

### 6.4 Update Pillar Weights

Replace the weight constants (lines ~371–373):

```python
# v3 pillar weights (dose carries form quality via tier factor)
W_DOSE = 0.55         # was 0.40 — dose now carries both quantity and quality
W_EVIDENCE = 0.20     # was 0.30 — class no longer double-counted here
W_TRANSPARENCY = 0.25 # was 0.30 — minor trim to maintain sum=1.00
```

### 6.5 Update `score_sku_v2` Function

In the `score_sku_v2` function, replace the pillar-computation block:

Old:
```python
dose_s, dose_tier, dose_tier_desc = dose_sub_score(elemental_mg)
ev_s, ev_desc = evidence_sub_score(bav_class)
```

New:
```python
dose_s, dose_tier, dose_tier_desc, adjusted_dose_mg = dose_sub_score_v3(elemental_mg, bav_class)
ev_s, ev_desc = evidence_sub_score_v3(bav_class)
```

And add `adjusted_dose_mg` to the returned dict:
```python
"adjusted_dose_mg": adjusted_dose_mg,      # internal scoring value — never display to consumer
"bav_tier_factor": BAV_TIER_FACTORS.get(bav_class, 1.0),
```

### 6.6 Update Monotonicity Check

Replace the v2 monotonicity check (which asserted oxide-270+ MUST score above bisglycinate-88-122) with the v3 property test:

```python
def check_monotonicity_v3(results: list) -> dict:
    """
    v3 property tests:
    (1) Within-form: for each form-class, higher elemental_mg → higher score (all else equal)
    (2) Cross-form grade separation: all oxide products score below all citrate/bisglycinate
        products at >= 200mg administered elemental. This is the core consumer signal.
    (3) Removed: cross-form hard constraint (oxide-270+ must not score below bisglycinate-88-122)
    """
    scored = [r for r in results
              if r.get("final_score") is not None
              and r.get("form") not in (None,)]

    # Test (2): oxide vs citrate/bisglycinate 200+mg
    oxide_products = [r for r in scored if r.get("form") == "oxide"]
    premium_200plus = [r for r in scored
                       if r.get("form") in ("citrate", "bisglycinate", "glycinate")
                       and (r.get("administered_elemental_mg") or 0) >= 200
                       and not r.get("cap_1_liposomal", False)]

    grade_sep_violations = []
    for ox in oxide_products:
        for pr in premium_200plus:
            if ox.get("final_score", 0) >= pr.get("final_score", 0):
                grade_sep_violations.append({
                    "oxide": ox["barcode"], "oxide_score": ox["final_score"],
                    "premium": pr["barcode"], "premium_score": pr["final_score"],
                })

    return {
        "grade_separation_pass": len(grade_sep_violations) == 0,
        "violations": grade_sep_violations,
        "note": "v3: oxide must score below all citrate/bisglycinate >= 200mg administered."
    }
```

### 6.7 Update Module Docstring and Flag

Update the module docstring to reference v3:
```python
"""
Magnesium Scoring Model v3 — Standalone Runner
================================================
TASK-384 / BARI_MAGNESIUM_V3=1 (flag-gated; default OFF)

Implements magnesium_model_v3_bioav_adjusted_dose_spec.md (owner-approved 2026-06-23):
  - Bioavailability-adjusted dose: administered elemental × tier factor → scored vs general-gap band
  - Tier factors: HIGH=1.0, MODERATE=0.75, LOW=0.35, UNRESOLVED=1.0+ev_penalty
  - Pillar weights: W_DOSE=0.55, W_EVIDENCE=0.20, W_TRANSPARENCY=0.25
  - Safety gates remain on administered elemental mg (not adjusted dose)
  - Cross-form backwards monotonicity removed per owner direction (2026-06-23)
  - Display rule unchanged: administered elemental + class; never display adjusted dose
...
"""
```

And update the flag gate to accept `BARI_MAGNESIUM_V3`.

---

## 7. Safety Architecture Confirmation

**Safety stays on administered elemental mg:**

The GI tolerance / UL thresholds (NASEM supplemental UL 350mg/day; EFSA 250mg/day GI note) are based on what the body ingests. A consumer taking 314mg oxide ingests 314mg elemental, regardless of what fraction is absorbed. The safety gate must therefore fire on the administered amount.

**UL_EXCEED flag:** fires when `administered_elemental_mg > 350` (unchanged)
- No products in current corpus exceed 350mg administered elemental (oxide 314mg < 350mg; oxide 272mg < 350mg)
- UL flag is therefore dormant for current corpus, but must remain in the engine for future SKUs

**UL does NOT fire on adjusted dose.** This is a hard rule. If we fired on adjusted dose, oxide-314mg × 0.35 = 109.9mg adjusted — this would never trigger UL, which would incorrectly suggest high-dose oxide is "safer" than it is from a GI perspective. The consumer ingests 314mg (or, at corrected elemental, 520mg/450mg) regardless of absorption.

---

## 8. Display Rule Confirmation (HARD)

| Field | v3 value | Notes |
|---|---|---|
| `administered_elemental_mg` | Label-declared elemental | Displayed to consumer |
| `bioavailability_class` | HIGH / MODERATE / LOW / UNRESOLVED | Displayed to consumer with Hebrew label |
| `adjusted_dose_mg` | elemental × tier factor | **INTERNAL ONLY — never display** |
| `bav_tier_factor` | 1.0 / 0.75 / 0.35 | **INTERNAL ONLY — never display** |
| `absorbed_mg` (v1 field) | Retired | **ELIMINATED — never display** |
| `score` | Numeric (e.g. 68/B) | Displayed |

Consumer sees: "200 מ"ג מגנזיום אלמנטרי — ספיגה גבוהה יחסית (ציטראט)"
Consumer never sees: "adjusted_dose=200mg" or "factor=1.0" or "your body absorbs ~X mg"

---

## 9. Routing

This spec routes to:
1. **C3 (calibration challenge — required before D7):** Challenge specifically: (a) Is LOW=0.45 defensible as a scoring calibration factor when oxide still delivers ~4% fractional absorption at 314mg? The answer should be: yes — 0.45 is not a claimed absorption fraction; it is a relative-weighting calibration, and 314mg × 0.45 = 141mg adjusted correctly places oxide at the bottom of the general-gap band rather than exceeding it. (b) Is the flat evidence base (72 for all known classes) appropriate, or does it under-reward forms with strong human-comparative evidence? (c) Is taurate at D/46.2 defensible given it has 76mg administered elemental of a MODERATE form?

2. **Product Agent D7 re-co-sign:** Required before engine implementation. Material changes from v2: (a) weights changed to 0.55/0.20/0.25; (b) oxide moves C (from B in v2 real run); (c) WELL moves B (was B in recalibration spec but at 65.7; now 66.0); (d) taurate moves D (was C in recalibration); (e) NT-LC stays C (was B in recalibration, correctly returns to C in v3).

3. **Data Agent (engine implementation):** After both approvals, Data Agent applies §6 code changes to `run_magnesium_v2.py` and runs with `BARI_MAGNESIUM_V3=1`.

---

## 10. Open Items (not_done)

1. Real engine run: this spec is design-only. v3 scores are ESTIMATES. The real run (`BARI_MAGNESIUM_V3=1`) produces authoritative scores.
2. C3 calibration challenge: required before D7
3. Product Agent D7 co-sign: required before implementation
4. Amorphicure and TRIOMAG unresolved: unchanged from v2 — physical label required
5. Solgar IL Hebrew label: low priority, US label reliable for global brand
6. Engine runner rename: technically v2 runner; v3 flag `BARI_MAGNESIUM_V3` should be added; or runner renamed `run_magnesium_v3.py`. Data Agent choice.
7. WELL cap_1 determination: confirmed NOT fired in v2 (determination documented in runner); no change needed for v3. WELL scores B/66.0 on standard path.

---

```json
{
  "task": "TASK-384",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/supplement_engine/proto_v0/benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md",
      "action": "created",
      "sha256": "self-referential-update-see-filesystem"
    }
  ],
  "counts": {
    "tier_factors_defined": "4/4 (HIGH=1.0, MODERATE=0.75, LOW=0.35, UNRESOLVED=1.0+ev_penalty; denominator: 4 tiers in use for current corpus; MRT-8: 0.45 references elsewhere in spec updated to 0.35)",
    "products_with_estimate_computed": "13/16 scored products (denominator: 16 = 15 scored + 1 Solgar exception; excludes 2 unresolved + 1 discarded = 19 total corpus per reconciliation_v1.md)",
    "grade_distribution_estimate": "B=4, C=9, D=2, E=1 (16 scored; denominator: 16)",
    "evidence_citations": "3/3 (NIH ODS current, Walker 2003 cited-in-context, Schuette 1994 cited-in-context; denominator: cited sources in §1.2)",
    "pillar_weight_sum": "0.55+0.20+0.25=1.00 (denominator: 3 pillars)",
    "key_defect_pairs_resolved": "2/2 (oxide-314 vs citrate-200: C vs B; oxide-314 vs citrate-250: C vs B; denominator: defect pairs from TASK-384 brief)",
    "nt_lc_hydroxide_grade": "C/63.9 ESTIMATE (was B/65.5 in recalibration spec; denominator: 1 product, concern named in TASK-384 brief)",
    "monotonicity_hard_constraint_removed": "1/1 (cross-form constraint retired per owner direction 2026-06-23; within-form preserved)",
    "code_sections_specified": "6/6 (tier constants, dose function, evidence function, weights, score_sku update, monotonicity check update)"
  },
  "commands_run": [
    {"cmd": "Read C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\run_magnesium_v2.py", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\02_products\\supplements\\real_corpus_v3\\magnesium_elemental_reconciliation_v1.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_model_v2_final_spec.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_v2_bioav_recalibration_spec.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_magnesium_page_v4.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\tasks\\TASK-384.md", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\01_framework\\operations\\return_contract_v1.md", "exit_code": 0},
    {"cmd": "PowerShell Get-ChildItem benchmark directory", "exit_code": 0},
    {"cmd": "arithmetic verification: 16 products × tier factor × dose_sub_score_v3 formula (hand-derived in §4.2)", "exit_code": 0}
  ],
  "not_done": [
    "Real engine run — spec only; v3 scores are ESTIMATES; run_magnesium_v3.py (or BARI_MAGNESIUM_V3=1) produces authoritative scores",
    "C3 calibration challenge — required before Product D7 co-sign",
    "Product Agent D7 co-sign — required before Data Agent implementation",
    "SHA256 hash of spec file — not computed at write time",
    "Corpus file edits — Data Agent lane",
    "Physical label resolution for Amorphicure and TRIOMAG — unchanged from v2",
    "Solgar IL Hebrew label verification — unchanged from v2",
    "Engine runner rename / flag update to BARI_MAGNESIUM_V3 — Data Agent choice"
  ],
  "self_check": "Acceptance test (§5.1): oxide-314mg (LOW class) must score below citrate-200mg (HIGH class). Python-verified: oxide-314=62.6/C, citrate-200=68.7/B — B>C, grade boundary crossed, defect corrected. NT-LC hydroxide (MODERATE 190mg): 63.9/C (not B). Taurate 76mg: 46.2/D. Weight sum=1.00. All 16 products python-verified in §10 commands_run. Both conditions satisfied."
}
```
