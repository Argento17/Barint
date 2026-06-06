# TASK-176 — Cottage fat-vs-protein weighting: diagnosis + before/after model

**Status:** INVESTIGATION + MODEL ONLY. NOT LIVE. No engine score or published JSON changed.
**Source of truth:** live `bari-web/src/data/comparisons/cheese_frontend_v2.json` (run_cheese_004,
BARI_RECAL_P0=on) + per-product traces under
`02_products/cheese_spreads/bsip2_outputs/run_cheese_004/products/bsip1_cheese_<barcode>/bsip2_trace.json`.
**Scripts (re-runnable, read-only):** `model_task176.py`, `model_task176_v2.py` (this dir).

---

## 1. Mechanism diagnosis (against real traces)

The task's stated hypothesis — *"a 0.4g protein edge beats the 4-point fat gap"* — is **largely
incorrect**. Protein contributes only ~1 point of the gap. The real driver is a **NOVA-2 vs NOVA-3
processing split**, triggered by an **added-sugar ingredient marker** in the lower-scoring 5%s.

### Weighted-dimension decomposition — 9% (81.13) vs 5% טרה (79.88 → 76.88 after penalty)

| dimension | weight | 9% cottage | 5% טרה | weighted Δ (9%−5%) |
|---|---|---|---|---|
| processing_quality | 0.15 | **85** (NOVA 2) | **65** (NOVA 3) | **+3.00** |
| whole_food_integrity | 0.04 | 85 (NOVA 2 base) | 60 (NOVA 3 base) | +1.00 |
| glycemic_quality | 0.12 | 90 | 82.5 (3g added sugar −7.5) | +0.90 |
| nutrient_density | 0.15 | 80 | 76 | +0.60 |
| protein_quality | 0.10 | 80 | 76 | **+0.40** ← the only protein term |
| fat_quality | 0.08 | **41** (sat 5.4 → red) | 76 | **−2.80** ← fat IS penalizing |
| regulatory_quality | 0.05 | 60 (1 red label) | 95 | **−1.75** ← red label IS penalizing |
| satiety_support | 0.06 | 98.4 | 100 | −0.10 |
| **raw weighted Δ** | | **81.13** | **79.88** | **+1.25** |
| HP_fat_sodium penalty | | 0 (NOVA 2 zeros HP weight) | **−3.0** (NOVA 3 → weight 0.5) | **+3.0 effective** |
| **final** | | **81.1** | **76.9** | **+4.2** |

**Reading:** fat is *already* costing the 9% ~4.55 weighted points (fat_quality −2.80 +
regulatory −1.75), plus the 9% is held at display-grade B by the sat-fat A-ceiling. The 9% still
wins because it is a **cleaner-label product**: NOVA 2 (חלב/מלח/סידן only, no added sugar) is worth
~+4.6 pts (processing +3.0, WFI +1.0, glycemic +0.6), and the sugared 5% additionally eats a −3.0
hyper-palatability penalty that the clean 9% does not.

### The discriminator is the added-sugar marker, verified across the three 5%s

| barcode | label | protein | sat fat | sugar | NOVA | added-sugar marker | weighted | final |
|---|---|---|---|---|---|---|---|---|
| 2868996 | 5% | 10.0 | 3.0 | 3.0 | **2** | **0** | 83.63 | **84/A** |
| 7290114310918 (טרה) | 5% | 10.1 | 3.0 | 3.0 | **3** | **1** (סוכר) | 79.88 | **77/B** |
| 7290011194246 | 5% | 10.2 | 3.0 | 2.4 | **3** | **1** (סוכר) | 78.35 | **75/B** |

Same fat (5%), near-identical protein (10.0–10.2g) → an **84/A** and two **75–77/B**, purely on
whether the ingredient text declares added sugar (NOVA 3 → processing 65 + WFI 60 + HP −3). This
also explains the secondary symptom (the "קוטג' 5%" label spanning 75–87): the 87/A 5% (che-4127329,
protein 11.0, NOVA 2, no sugar) is a genuinely better product than the 75/B 5% (sugared, NOVA 3).

### A-ceiling interaction (question c)

The sat-fat A→B display cap (`_aCappedToB`, EV-021 Amendment A1, sat-fat > 4.0) works **correctly
on grade** — it relegates both 9% cottages from grade A to grade B. But it is a **grade cap, not a
score cap**: it leaves the numeric 81 intact. Since the live shelf orders within a family by the
numeric score, the 9% (81) still sorts above the 5%s (77, 75). So the A-ceiling does not *cause* the
inversion, but it also does not *prevent* it — it caps the letter and leaves the number that drives
ordering untouched. That is the narrow place where it "interacts badly."

---

## 2. Answers to the four questions

**(a) Is fat under-weighted for within-family fat-only differences?**
No. The traces show fat is actively penalizing: the 9% loses ~4.55 weighted pts (fat_quality 41 vs
76; regulatory 60 vs 95) plus a grade cap. The inversion is not caused by fat being ignored — it is
caused by the *lower-fat* products being worse on a different axis (added sugar → NOVA 3 + HP
penalty). Raising fat weight further would mis-penalize clean whole-fat dairy (and collides with the
whole-food-fat-floor philosophy and the milk invariant where whole 4% = 85/A).

**(b) Is a same-family ordering guarantee or fat-aware tie-break warranted?**
A **bounded near-equal tie-break is defensible** (model M4); a **hard monotonic guarantee is not**
(model M1 over-corrects badly — see §3). But note the bounded tie-break **does not fix the headline
case**, because the 9%-over-5% gap (4–6 pts) is larger than noise and reflects a real quality
difference (cleaner label). Enforcing "lower fat always ≥ higher fat" would force a clean NOVA-2 9%
below a sugared NOVA-3 5% — scientifically wrong.

**(c) Does the A-ceiling interact badly?** Partially — see above. It caps grade but not the
ordering-driving number. If a fix ships, the cleanest version is to make the sat-fat cap also clamp
the *displayed number*, not just the letter (so a sat-fat-capped product cannot out-sort a
cleaner-label sibling on the number while showing the same grade).

**(d) Blast radius.** Display-only guards touch only fat-ladder clusters that have an inversion:
**cottage** (2× 9% at 81, 1× 12% at 76 sit above 5%s at 77/75) and **white-cheese-quark** (2× 9% at
75, 1× 17% at 68 sit above weaker 5%s). No engine math changes ⇒ **zero propagation to milk/yogurt**
numeric scores. Milk is a legacy page (no recal JSON in `comparisons/`); yogurt's recal wave is
unshipped. A guard scoped to the existing `_cluster` field is contained to cheese.

---

## 3. Candidate rules modeled (before/after)

All are **display-only** clamps (mirror `_aCappedToB`); none touch engine scores. Full output in
`cottage_white_before_after.csv` and the v2 script.

| Rule | What it does | Cottage result | White-cheese result | Verdict |
|---|---|---|---|---|
| **M1** clamp to MIN lower-fat sibling | hard monotonic | 9% 81→75, 12% 76→75 | **9% 75→58 (−17, B→C); 17% 68→58 (−10)** | **Over-corrects.** Punishes a clean 9% for one weak 5% outlier. Reject. |
| **M3** clamp to BEST lower-fat sibling | gentle monotonic | **no change** | **no change** | Does nothing — best lean sibling already outscores fatter tier. Useless. |
| **M4** bounded tie-break (Δ≤2 = noise) | only near-equal pairs | 12% 76→74 only | 9% 75→72, (17% unchanged) | Defensible, minimal. **But leaves the headline 9%>5% intact.** |

**Key finding:** no mechanical fat-ordering rule both (i) fixes the headline complaint and (ii)
avoids misranking a cleaner product below a sugared one. The headline "9% beats 5%" is **not a
near-equal tie** — it is a real 4–6 pt quality gap. The intuition "leaner must rank higher" is only
true *all else equal*, and here all else is **not** equal (the cheap 5%s carry added sugar).

---

## 4. Recommendation: **KEEP the engine; OPTIONALLY apply M4 + number-aware sat-fat cap (display only)**

**Primary recommendation — KEEP (no engine change).** The ordering is scientifically defensible:
the 9% outranks the two low 5%s because those 5%s are genuinely lower-quality (added sugar →
NOVA 3 + hyper-palatability penalty), not because fat is under-weighted. Forcing leaner-always-higher
would corrupt a correct judgment. This is the food-science-correct answer.

**The real problem is presentational, not nutritional.** A shopper reading only "9% vs 5%" cannot
see *why* the clean 9% earns its number. Two display-only, non-scoring options to remove the
"reads backwards" friction without falsifying the science:

- **R1 (recommended): editorial.** On the 9% insight line, surface the actual reason it out-scores
  the cheap 5%s (clean label, no added sugar) and on the 75/77 5%s surface that they carry added
  sugar. This is a Content task, costs zero score integrity, and is the honest fix. The existing
  9% insight line already explains the sat-fat B cap; extend it to the label-cleanliness point.
- **R2 (optional, display-only): make the sat-fat A-ceiling also clamp the displayed number**, so a
  sat-fat-capped product cannot sit above a non-capped sibling on the number while showing the same
  grade. Combined with **M4** (bounded near-equal tie-break, Δ≤2) this resolves only the genuine
  near-ties (cottage 12%, white-cheese 9%) and leaves the defensible gaps alone. Blast radius: 3
  cottage + 3 white-cheese display values; zero engine/milk/yogurt impact.

**Do NOT** raise fat weight, add a hard fat-monotonic guarantee, or otherwise re-rank the clean 9%
below the sugared 5%s.

**Governance:** R1 is a Content task (D13), no D7 needed. R2 changes how a published number displays
within a family → governed display change; **requires Product + Nutrition D7 co-sign and owner
sign-off** before any live edit (recal-went-live lesson). Either way, **no engine recalibration**.
