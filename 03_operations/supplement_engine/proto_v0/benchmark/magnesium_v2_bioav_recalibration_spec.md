# Magnesium v2 — Bioavailability Class Recalibration Spec

**Author:** Nutrition Agent
**Date:** 2026-06-23
**Status:** PROPOSED — requires Product Agent D7 co-sign before engine implementation
**Triggered by:** TASK-384 CHANGES_REQUESTED — oxide 314mg tied with citrate 250mg at B (gap = 0.9 pts), defeating the page's core purpose
**Scope:** Class modifier values in `run_magnesium_v2.py` only. Pillar weights (0.40/0.30/0.30), dose sub-score function, transparency sub-score, cap ceilings, and corpus are unchanged.

---

## 1. Defect Analysis

Under the current v2 model (`BAV_CLASS_MODIFIERS = {HIGH: +8, MODERATE: +3, LOW: 0, UNRESOLVED: -5}`), the class modifier contributes only `8 × 0.30 = 2.4 pts` to the final blend. This is insufficient to produce a grade-band separation between same-tier dose products of different class.

Concrete failure:
- Oxide 314mg (LOW class, MEETS dose): blend = 100.0×0.40 + 72.0×0.30 + 25.0×0.30 = **69.1/B**
- Citrate 250mg (HIGH class, MEETS dose): blend = 92.5×0.40 + 80.0×0.30 + 30.0×0.30 = **70.0/B**

Gap = 0.9 pts. Consumer reads: oxide = citrate. This is the exact misconception the page exists to correct.

### Root cause

The evidence sub-score base (72.0) was conceived as a "Moderate tier midpoint" — a reasonable default for any product meeting the general-gap band. But it does not create enough spread when applied symmetrically around that midpoint with small modifiers. HIGH (+8) and LOW (0) produce evidence scores of 80.0 and 72.0 — an 8-point raw gap, worth only 2.4 pts in the blend.

### What is required

For oxide to land clearly below equal-dose citrate within the same dose tier:
- The blend gap between HIGH and LOW class must be large enough to cross at least one grade boundary (15 pts in the Bari grade system) when dose scores are equal or close.
- Mathematically: when dose is maxed (both MEETS), the class gap in blended score must exceed 15 pts: `(ev_HIGH - ev_LOW) × 0.30 > 15` → `ev_HIGH - ev_LOW > 50 pts`.
- However: the monotonicity constraint (oxide-272mg must not score below bisglycinate-122mg) limits the raw evidence gap to `(ev_HIGH - ev_LOW) < 25` (derived below in §2).

These two constraints cannot be simultaneously satisfied with dose equal. The correct resolution is a **partial grade split**: oxide-314mg lands at the bottom of B or top of C, while equal-dose citrate/bisglycinate lands comfortably in B. A 1-grade-band difference (C vs B) is the achievable and evidentially appropriate outcome.

---

## 2. Monotonicity Constraint Derivation

The monotonicity requirement from the TASK-384 spec: no oxide product at 270+mg elemental may score below a bisglycinate product at 88–122mg elemental.

The critical pair is oxide-272mg vs Full-Mag-122mg (bisglycinate, HIGH class):

```
Oxide-272:    dose_s = 95.8,  ev_low = 72 + l,  trans = 25.0
Full-Mag-122: dose_s = 73.3,  ev_high = 72 + h,  trans = 30.0

Condition (oxide-272 ≥ Full-Mag-122):
  95.8×0.40 + ev_low×0.30 + 25.0×0.30 ≥ 73.3×0.40 + ev_high×0.30 + 30.0×0.30
  38.32 + ev_low×0.30 + 7.5 ≥ 29.32 + ev_high×0.30 + 9.0
  45.82 + ev_low×0.30 ≥ 38.32 + ev_high×0.30
  7.5 ≥ (ev_high - ev_low)×0.30
  (ev_high - ev_low) ≤ 25
```

**Monotonicity hard bound: HIGH-LOW evidence gap ≤ 25 pts.**

Nano-88 (bisglycinate, cap_1, 88mg, NEAR dose) is not a binding constraint for monotonicity because cap_1 hard-caps it at 34/E regardless of class modifier value.

---

## 3. Grade-Split Requirement Derivation

For oxide-314mg to land in C-range (score < 65), given dose_s = 100.0 and trans = 25.0:

```
100.0×0.40 + ev_low×0.30 + 25.0×0.30 < 65.0
40.0 + ev_low×0.30 + 7.5 < 65.0
ev_low×0.30 < 17.5
ev_low < 58.33
72 + l < 58.33
l < -13.67
```

**Grade-split requirement: LOW modifier l ≤ -14 (i.e., ev_LOW ≤ 58.0).**

---

## 4. Recalibrated Class Modifier Values

The feasible region satisfies both constraints simultaneously:

- Grade-split: `l ≤ -14`
- Monotonicity: `h - l ≤ 25`

Chosen configuration (least aggressive change that satisfies both):

| Class | Old modifier | New modifier | Old ev score | New ev score |
|---|---|---|---|---|
| HIGH | +8 | **+10** | 80.0 | **82.0** |
| MODERATE | +3 | **+5** | 75.0 | **77.0** |
| LOW | 0 | **-14** | 72.0 | **58.0** |
| UNRESOLVED | -5 | **-20** | 67.0 | **52.0** |

Evidence gap HIGH-LOW: 82.0 - 58.0 = **24 pts** (under the 25-pt monotonicity hard bound).

### Evidence grounding

The LOW modifier of -14 reflects the published evidence on oxide bioavailability:
- Oxide has the lowest fractional absorption in head-to-head comparative studies. Studies citing ~4% fractional absorption for oxide vs ~28–32% for citrate/bisglycinate in comparative designs (Walker 2003, Schuette 1994/PMID:7815675 context; general bioavailability literature cited in NIH ODS magnesium fact sheet) support a substantial evidence penalty, not merely a zero-bonus.
- The NIH ODS Magnesium Fact Sheet (health professional version, accessed 2026) explicitly ranks oxide below organic salts: "Forms of magnesium that dissolve well in liquid are more completely absorbed in the gut than less soluble forms. Small studies have found that magnesium in the aspartate, citrate, lactate, and chloride forms is absorbed more completely and is more bioavailable than magnesium oxide and magnesium sulfate."
- The magnitude of the penalty (-14 pts from the evidence base) is calibrated to produce a defensible grade differential on the Israeli shelf, not a precise absorption fraction. It does not assert that oxide delivers zero benefit — oxide 314mg still scores C/64.9, which is above D and above all NEAR-dose products.

The HIGH modifier of +10 (vs old +8) gives a small lift to citrate/bisglycinate to create a clear B landing, evidenced by the broader human comparative evidence base for these forms.

The MODERATE modifier of +5 (vs old +3) maintains malate/taurate/hydroxide above oxide, correctly ordering the bioavailability spectrum. No MODERATE product flips grade from the recalibration.

UNRESOLVED at -20 (vs old -5) reflects that a hidden-composition blend cannot be evidence-classed at all. This is a transparency penalty stacked on top of the honesty cap (cap_3) that already binds most UNRESOLVED products. For Solgar (cap_3 binding at 49/D), the UNRESOLVED penalty is absorbed into the cap and has no additional grade effect.

---

## 5. Expected Distribution After Recalibration

Derivation: calculated from exact pillar weights and corpus values. All arithmetic is traceable from the corpus table in `run_magnesium_v2.py`.

| Product | Elem mg | Class | Dose_s | Ev_s (new) | Trans_s | Blend | Cap | Final | Grade | vs Current |
|---|---|---|---|---|---|---|---|---|---|---|
| Supherb Citrate+B6 Badatz | 250 | HIGH | 92.5 | 82.0 | 30.0 | 70.6 | — | **70.6** | **B** | was 70.0/B (same grade) |
| Altman Bisglycinate 250 | 250 | HIGH | 92.5 | 82.0 | 30.0 | 70.6 | — | **70.6** | **B** | was 70.0/B (same grade) |
| Altman Citrate 120 | 200 | HIGH | 85.0 | 82.0 | 30.0 | 67.6 | — | **67.6** | **B** | was 67.0/B (same grade) |
| Nutricare WELL | 168 | HIGH | 80.2 | 82.0 | 30.0 | 65.7 | — | **65.7** | **B** | was 65.1/B (same grade) |
| Full-Mag Hadas 600 | 122 | HIGH | 73.3 | 82.0 | 30.0 | 62.9 | — | **62.9** | **C** | was 62.3/C (same grade) |
| NT LC Anti Leg Cramps | 190 | MODERATE | 83.5 | 77.0 | 30.0 | 65.5 | — | **65.5** | **B** | was 64.9/C — GRADE UP |
| Tink Malate | 136 | MODERATE | 75.4 | 77.0 | 30.0 | 62.3 | — | **62.3** | **C** | was 61.7/C (same grade) |
| Nutricare Malate 90cp | 135 | MODERATE | 75.2 | 77.0 | 25.0 | 60.7 | — | **60.7** | **C** | was 60.1/C (same grade) |
| Nutricare Taurate | 76 | MODERATE | 55.6 | 77.0 | 30.0 | 54.3 | — | **54.3** | **C** | was 53.7/C (same grade) |
| Nutricare Oxide 520 | 314 | LOW | 100.0 | 58.0 | 25.0 | 64.9 | — | **64.9** | **C** | was 69.1/B — GRADE DOWN |
| Tink Oxide 520 | 314 | LOW | 100.0 | 58.0 | 25.0 | 64.9 | — | **64.9** | **C** | was 69.1/B — GRADE DOWN |
| Altman 520 | 314 | LOW | 100.0 | 58.0 | 25.0 | 64.9 | — | **64.9** | **C** | was 69.1/B — GRADE DOWN |
| Altman MagUp | 272 | LOW | 95.8 | 58.0 | 25.0 | 63.2 | — | **63.2** | **C** | was 67.4/B — GRADE DOWN |
| Altman Balance | 272 | LOW | 95.8 | 58.0 | 25.0 | 63.2 | — | **63.2** | **C** | was 67.4/B — GRADE DOWN |
| Nutricare Nano Bisglycinate | 88 | HIGH | 62.8 | 82.0 | 15.0 | 57.2 | cap_1/34 | **34.0** | **E** | unchanged (cap binds) |
| Solgar Cal-Mag D3 | 100 | UNRESOLVED | 70.0 | 52.0 | 0.0 | 43.6 | cap_3/49 | **43.6** | **D** | was 48.1/D (same grade, slightly lower) |

### Grade distribution

| Grade | Count | Products |
|---|---|---|
| B | 5 | Supherb Citrate+B6, Altman Bisglycinate 250, Altman Citrate 120, Nutricare WELL, NT LC Hydroxide |
| C | 8 | Full-Mag Hadas 600, Tink Malate, Nutricare Malate, Nutricare Taurate, all 3× oxide-314, both oxide-272 |
| D | 1 | Solgar Cal-Mag D3 (cap_3 binding) |
| E | 1 | Nutricare Nano Bisglycinate (cap_1 binding) |

Score stats (16 scored SKUs including Solgar, excluding 2 unresolved + 1 discarded):
- Min: 34.0 (Nano, cap_1)
- Max: 70.6
- Mean: ~60.5
- Distribution: B×5, C×8, D×1, E×1

---

## 6. Monotonicity Verification

**Oxide 270+mg vs bisglycinate 88–122mg (the stated constraint):**

```
Oxide-272: 95.8×0.40 + 58.0×0.30 + 25.0×0.30 = 38.32 + 17.40 + 7.50 = 63.22 → 63.2
Full-Mag-122: 73.3×0.40 + 82.0×0.30 + 30.0×0.30 = 29.32 + 24.60 + 9.00 = 62.92 → 62.9
Margin: +0.3 pts. Oxide-272 > Full-Mag-122. PASS.

Oxide-314: 100.0×0.40 + 58.0×0.30 + 25.0×0.30 = 40.00 + 17.40 + 7.50 = 64.9
Full-Mag-122: 62.9
Margin: +2.0 pts. Oxide-314 > Full-Mag-122. PASS.
```

**Nano Bisglycinate 88mg (cap_1):**
- Final score = 34.0 (cap_1 binding regardless of class modifier). Oxide-272 at 63.2 > 34.0. PASS.

**Monotonicity interpretation note:** The oxide-272 vs Full-Mag-122 margin (0.3 pts) is narrow but structurally correct. The constraint holds because oxide's large dose advantage (dose_s 95.8 vs 73.3) still outweighs the HIGH-LOW evidence gap contribution (24 pts × 0.30 = 7.2 pts) once dose weight is applied: `(95.8 - 73.3) × 0.40 = 9.0 > 7.2`. The relationship is dose-dominated, not class-dominated, at high oxide doses — which is the intended behavior.

The narrow margin means a future dose function change could disrupt this. This should be flagged in the engine implementation as a property test: `assert score(oxide_272) >= score(bisglycinate_122)`.

---

## 7. Key Consumer Outcome Verified

**Oxide 314mg vs Citrate 250mg (the stated defect pair):**

- Oxide 314mg: **C/64.9** (was B/69.1)
- Citrate 250mg: **B/70.6** (was B/70.0)
- Citrate 200mg (Altman Citrate 120): **B/67.6** (was B/67.0)

All three citrate/bisglycinate products at 200–250mg dose score **B**, all oxide products score **C**. The page now communicates: even a lower-dose well-absorbed form (200mg citrate) outranks a higher-dose poorly-absorbed form (314mg oxide). This is the correct consumer signal and aligns with the NIH ODS ranking cited in §4.

---

## 8. NT LC Hydroxide Grade Change (expected side effect)

NT LC Anti Leg Cramps (190mg hydroxide, MODERATE class) moves from C/64.9 to B/65.5. This is a correct outcome:
- Hydroxide is MODERATE class (above oxide, below citrate/bisglycinate).
- 190mg elemental is a substantial dose within the general gap band.
- The old model underpenalized oxide (making oxide and hydroxide look similar). The new model correctly separates oxide (LOW/C) from hydroxide (MODERATE/B).
- The cramps indication footnote remains unchanged (insufficient evidence per Cochrane 2020/PMID:32956536); this is a display note, not a scored signal.

This grade change requires D7 re-co-sign since it affects a published-candidate product's grade (the page is offline, so this is pre-publication but still material).

---

## 9. Exact Code Changes Required in `run_magnesium_v2.py`

Replace lines 287–292 (the `BAV_CLASS_MODIFIERS` dict):

**Old:**
```python
BAV_CLASS_MODIFIERS = {
    "HIGH": 8.0,
    "MODERATE": 3.0,
    "LOW": 0.0,
    "UNRESOLVED": -5.0,
}
```

**New:**
```python
BAV_CLASS_MODIFIERS = {
    "HIGH": 10.0,     # ev score 82.0  — NIH ODS: organic/chelated forms absorb more completely
    "MODERATE": 5.0,  # ev score 77.0  — above oxide on solubility; below citrate on direct evidence
    "LOW": -14.0,     # ev score 58.0  — oxide/carbonate: lowest fractional absorption in comparative studies (NIH ODS)
    "UNRESOLVED": -20.0,  # ev score 52.0 — blend with undisclosed ratios; cannot evidence-classify
}
```

No other changes to the scoring logic, pillar weights, dose function, transparency function, cap ceilings, or corpus.

The comment on lines 280–285 (base sub-score description) should be updated to reflect the actual resulting scores:
```python
# Class modifiers (additive to evidence sub-score base=72.0):
#   HIGH:       +10 -> 82.0  (citrate, bisglycinate, glycinate)
#   MODERATE:   +5  -> 77.0  (malate, taurate, hydroxide)
#   LOW:        -14 -> 58.0  (oxide, carbonate)
#   UNRESOLVED: -20 -> 52.0  (blend, undisclosed ratios)
# Evidence gap HIGH-LOW = 24 pts; monotonicity hard bound = 25 pts (documented in recalibration spec)
```

---

## 10. Why This Is Not a Model Redesign

This change modifies four numeric constants inside one function. It does not:
- Change the 3-pillar structure or weights
- Add or remove signals
- Change the dose sub-score function
- Change the transparency sub-score function
- Change cap ceilings (cap_1=34, cap_3=49)
- Change the corpus or any product's disposition
- Add any new absorbed-mg consumer display (still prohibited)

The class-modifier values were always an empirical calibration choice, not a principled derivation. The original values (+8/+3/0/-5) were specified without an explicit derivation; this spec provides the derivation for the replacement values. The recalibration stays inside the D7-approved 2-band MVP + administered-elemental direction.

---

## 11. C3 Routing Note

Per the task brief, this calibration routes to C3 (balance challenge) before implementation. C3 should specifically challenge:
1. Whether the LOW penalty of -14 is defensible given that oxide is still functional as a supplement (it does deliver some magnesium). The answer: ev_LOW=58.0 still produces a C grade (not D or E) for full-dose oxide products; the penalty reflects relative evidence strength, not zero utility.
2. Whether the monotonicity constraint should be articulated as a hard invariant or a soft preference. Nutrition Agent position: hard invariant — a high-dose form should not score below a low-dose form in the same category, regardless of class.
3. Whether NT LC Hydroxide at B/65.5 is defensible (hydroxide MODERATE class, 190mg, no special evidence). Answer: yes — MODERATE class above oxide is evidence-grounded; 190mg is a substantial dose; B is appropriate.

---

## Open Items (not_done)

- Engine implementation: awaiting Product Agent D7 re-co-sign
- C3 balance challenge: required before Product D7 (per task brief)
- Re-run of `run_magnesium_v2.py` with new constants to generate updated verification table
- Corpus file edits: not in scope (Data Agent lane)
- Physical label resolution for Amorphicure and TRIOMAG: unchanged from prior spec
- Solgar IL Hebrew label verification: unchanged from prior spec
