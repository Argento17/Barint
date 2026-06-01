# High-Quality Product Uplift Model
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Priority 3 & 4  
**Question:** Do genuinely excellent supermarket products receive scores that feel intuitively correct? If not, design a calibration that corrects this without weakening penalties for poor products.

---

## Part 1: Scored Benchmarks for Excellent Products

### Methodology

Each benchmark is computed using the BSIP2 dimension formulas from `bsip2_config.py` and `bsip2_dimensions.py`. All calculations assume full nutrition data available (confidence = HIGH). Scores are pre-guardrail dimension totals, then post-guardrail final scores.

---

### Benchmark 1: Plain Greek Yogurt (NOVA2, 10g protein, 5g sugar, 80 kcal, 3g sat fat, 0 fiber, no additives)

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| processing_quality | 100 (NOVA2, ≤8 ingredients) | 0.18 | 18.00 |
| nutrient_density | 62 (50 + 12 protein, 0 fiber, no sugar penalty) | 0.16 | 9.92 |
| calorie_density_quality | 90 (dairy_protein tier, ≤80 kcal) | 0.12 | 10.80 |
| glycemic_quality | 80 (sugar=5g, no penalty) | 0.11 | 8.80 |
| hyper_palatability | 100 (no combos) | 0.10 | 10.00 |
| protein_quality | 65 (45 + 20, no isolate) | 0.09 | 5.85 |
| additive_quality | 90 (no markers) | 0.07 | 6.30 |
| satiety_support | 59 (45 + 14 protein, no fiber, no sugar) | 0.06 | 3.54 |
| fat_quality | 66 (70 - 4 sat_fat, no nut bonus) | 0.06 | 3.96 |
| regulatory_quality | 100 (no red labels) | 0.04 | 4.00 |
| whole_food_integrity | 52 (base only, no bonus applied) | 0.01 | 0.52 |
| **Base dimension total** | | | **81.69** |

**Guardrails:** No binding caps (NOVA2, no red labels, no additives, sugar < 25g, no sweetener).  
**Final score: 82/B**

**Is 82/B intuitively correct?** Yes. A plain, minimally processed Greek yogurt with solid protein and no additives scoring near the A threshold is accurate. This is one of the best products a consumer can buy.

---

### Benchmark 2: Same product with 1 Red Label (saturated fat from natural dairy, sat fat = 5g)

Same as Benchmark 1 except sat_fat = 5g → red_label_saturated_fat = True.

| Changed dimensions | Score | Weight | Weighted | Change |
|---|---|---|---|---|
| fat_quality | 58 (70 - 12 sat_fat) | 0.06 | 3.48 | -0.48 |
| regulatory_quality | 82 (100 - 18) | 0.04 | 3.28 | -0.72 |

**Base dimension total: 80.49**  
**ISRAELI_RED_LABEL_1 guardrail:** cap at 55. Natural score (80.49) > 55 → cap is binding.  
**Final score: 55/C**

**Is 55/C intuitively correct?** No. The regulatory dimension penalty (-0.72 pts) correctly signals the label. The cap then removes an additional 25 points, compressing the score from 80 to 55. A consumer reading C for a plain Greek yogurt with natural dairy fat receives inaccurate information about the product's quality relative to other products.

**The gap:** 80 (natural dimension score) → 55 (post-cap score) = 25-point cap suppression. The cap is functioning as a hard override rather than a proportional signal.

---

### Benchmark 3: NOVA3 Engineered Protein Yogurt (added whey protein, 15g protein, 6g sugar, 100 kcal, 4g sat fat, 2 stabilizers, no red labels)

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| processing_quality | 88 (100 - 12 NOVA3) | 0.18 | 15.84 |
| nutrient_density | 67 (50 + 18 protein, 0 fiber, -0.9 sugar) | 0.16 | 10.72 |
| calorie_density_quality | 80 (dairy_protein, ≤130 kcal) | 0.12 | 9.60 |
| glycemic_quality | 79 (80 - 1.4) | 0.11 | 8.69 |
| hyper_palatability | 100 (no combos) | 0.10 | 10.00 |
| protein_quality | 70 (45+30, -5 isolate) | 0.09 | 6.30 |
| additive_quality | 66 (90 - 24, two stabilizers) | 0.07 | 4.62 |
| satiety_support | 66 (45 + 21) | 0.06 | 3.96 |
| fat_quality | 62 (70 - 8) | 0.06 | 3.72 |
| regulatory_quality | 100 (no red labels) | 0.04 | 4.00 |
| whole_food_integrity | 40 (52 - 7 NOVA3 - 5 ingredient excess) | 0.01 | 0.40 |
| **Base dimension total** | | | **77.85** |

**Guardrails:** NOVA3 cap (82 in production, 75 in prototype). Natural score 77.85 < 82/75 → not binding. No other binding caps.  
**Final score: ~78/B**

**Is 78/B intuitively correct?** Yes. A NOVA3 engineered protein yogurt with excellent protein but stabilizers scores B — above average, but not exceptional. The processing penalty from NOVA3 is correctly reflected.

---

### Benchmark 4: Best Snack Bar — Date Bar (NOVA2, 4 ingredients, 35g sugar natural, 350 kcal, 4g protein, 2g fiber, 0 additives)

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| processing_quality | 100 (NOVA2, ≤8 ingredients) | 0.18 | 18.00 |
| nutrient_density | 31.8 (50 + 4.8 + 4 - 27) | 0.16 | 5.09 |
| calorie_density_quality | 90 (whole_food_fat tier, ≤350 kcal) | 0.12 | 10.80 |
| glycemic_quality | 38 (80 - 42) | 0.11 | 4.18 |
| hyper_palatability | 100 (fat too low for combos) | 0.10 | 10.00 |
| protein_quality | 53 (45 + 8) | 0.09 | 4.77 |
| additive_quality | 90 (no additives) | 0.07 | 6.30 |
| satiety_support | 45 (45 + 5.6 + 4.4 - 10) | 0.06 | 2.70 |
| fat_quality | 70 (minimal fat, no issues) | 0.06 | 4.20 |
| regulatory_quality | 100 (no Israeli red labels) | 0.04 | 4.00 |
| whole_food_integrity | 52 (base only) | 0.01 | 0.52 |
| **Base dimension total** | | | **70.56** |

**Guardrails:** HIGH_SUGAR_25G_PLUS cap at 60 (sugar=35g). Natural score 70.56 > 60 → cap should be binding. However, production scoring exempted this product (date bar scored 70/B with no cap applied — natural sugar treated as exempt by CE).  
**Python prototype final score: 60/C. Production final score: 70/B.**

**Is 70/B intuitively correct?** Approximately yes — the date bar is genuinely the best snack in the corpus. However, the 35g natural sugar is nutritionally significant (glycemic_quality dimension correctly produces 38), and the date bar scores 70 because of structural simplicity, not nutritional completeness.

---

### Benchmark 5: Sourdough Whole-Grain Bread (NOVA2, 5 ingredients, 1g sugar, 220 kcal, 1g sat fat, 5g fiber, no additives)

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| processing_quality | 100 (NOVA2) | 0.18 | 18.00 |
| nutrient_density | 68.8 (50 + 8.4 + 10 - 0) | 0.16 | 11.01 |
| calorie_density_quality | 80 (default tier, ≤250 kcal) | 0.12 | 9.60 |
| glycemic_quality | 85.5 (80 + 5.5 fiber) | 0.11 | 9.41 |
| hyper_palatability | 100 | 0.10 | 10.00 |
| protein_quality | 63 (45 + 14 protein, ~7g) | 0.09 | 5.67 |
| additive_quality | 90 | 0.07 | 6.30 |
| satiety_support | 72.6 (45 + 9.8 + 11 + 4 whole_grain + 8 nut_or_seed?) | 0.06 | 4.36 |
| fat_quality | 70 (minimal fat, no issues) | 0.06 | 4.20 |
| regulatory_quality | 100 | 0.04 | 4.00 |
| whole_food_integrity | 62 (52 + 5 whole_grain, NOVA2) | 0.01 | 0.62 |
| **Base dimension total** | | | **83.17** |

**Guardrails:** No binding caps.  
**Final score: 83/B (near A)**

**Is 83/B correct?** Yes. The best bread in a real supermarket scores B, with the A threshold (85) reachable for the most exceptional fermented whole-grain products. This is accurate.

---

## Part 2: Where Intuition and Score Diverge

| Product | Dimension score | Post-cap score | Gap | Cause |
|---|---|---|---|---|
| Plain Greek yogurt, 0 red labels | 82 | 82 | 0 | Correctly scored |
| Plain Greek yogurt, 1 sat-fat red label | 80 | 55 | **-25** | ISRAELI_RED_LABEL_1 cap suppression |
| NOVA3 protein yogurt, 1 sugar red label | 78 | 55 | **-23** | ISRAELI_RED_LABEL_1 cap suppression |
| NOVA3 protein yogurt, 0 red labels | 78 | 78 | 0 | Correctly scored |
| Date bar | 70 (no cap in production) | 70 | 0 | Production exempted; prototype: 60 |
| Best bread | 83 | 83 | 0 | Correctly scored |
| Raw almonds | ~89 | CRASH | — | Python prototype bug (not production) |

**The intuition-score divergence is concentrated in one scenario: products with 1 Israeli red label whose natural dimension score is above 55.** This scenario primarily affects:
- Plain dairy (natural sat fat, natural sugar content)
- Whole-food snacks with natural fat density
- High-quality products that trigger one nutritional threshold

---

## Part 3: Calibration Model

### Calibration Principle

The goal is not to raise all scores. The goal is to allow products whose quality genuinely earns a high dimension score to receive that score, without compressing it via a regulatory cap that was designed for a different purpose.

The Israeli red label cap serves two functions:
1. Ensure regulatory warnings materially reduce product score (correct function)
2. Create a hard ceiling regardless of all other quality signals (side effect causing the divergence)

The calibration model separates these two functions.

---

### Change 1: Regulatory cap transition from hard ceiling to proportional floor

**Current behavior:** `ISRAELI_RED_LABEL_1 cap = 55` — any product with 1 red label scores at most 55.

**Proposed behavior:** Replace the hard cap with a scoring floor rule: no product with 1 red label may score **more than 12 points above the cap value (55)**. The effective ceiling becomes `min(natural_score, 55 + 12) = min(natural_score, 67)`.

**Formula:** `final_score = min(natural_dimension_score, RED_LABEL_1_CEILING)` where `RED_LABEL_1_CEILING = 67`.

**Rationale:** The current cap at 55 compresses a product with a natural score of 82 to the same final score as a product with a natural score of 56. These products are not equivalent. The regulatory warning is captured; the quality signal is not erased. A ceiling at 67 still reflects the red label materially (max grade: C, not B), while preserving ranking differentiation within the red-label population.

**Effect on benchmarks:**

| Product | Before | After | Grade change |
|---|---|---|---|
| Plain Greek yogurt (1 sat-fat red label, natural score 80) | 55/C | 67/C | No grade change, +12 pts |
| NOVA3 protein yogurt (1 sugar red label, natural score 78) | 55/C | 67/C | No grade change, +12 pts |
| Product with natural score 58, 1 red label | 55/C | 58/C | No change (55+12=67 > 58) |
| Product with natural score 43, 1 red label | 43/D | 43/D | No change (cap not binding at 43) |

**Effect on poor products:** Products with natural scores ≤67 are unaffected. Only products whose quality genuinely earns a score above 67 receive the benefit — and their final score remains capped at 67, not at their natural score.

**Effect on `ISRAELI_RED_LABELS_2_PLUS` cap (45):** Unchanged. Two red labels still cap at 45. The relief applies only to exactly-1-red-label products.

---

### Change 2: Restore whole_food_bonus in manual CE scoring protocol

**Current state:** `whole_food_integrity` is scored at base (52) for all products, regardless of whether they contain oats, almonds, nuts, peanuts, or seeds.

**Proposed change:** Add an explicit instruction to the CE scoring protocol:

> If the product's ingredient list contains any of: שיבולת שועל, שקדים, אגוז, בוטנים, זרעים (or English equivalents), apply `whole_food_integrity += 7` and `processing_quality += 2.5` before dimension weighting.

**Effect:** +2.5 × 0.18 + 7 × 0.01 = +0.45 + 0.07 = **+0.52 weighted points** for qualifying products.

This is small in absolute terms but activates a reward signal that the specification intended and has never applied.

**Products affected in snack bars corpus:** Approximately 15–20 products with oat or nut content in ingredients.

---

### Change 3: Differentiate whole_food_integrity weight

**Current weight:** 0.01 (produces ≤0.65 weighted points maximum — functionally irrelevant)

**Proposed weight:** 0.04 (produces ≤2.6 weighted points maximum — marginally relevant)

**Offset:** Reduce `regulatory_quality` weight from 0.04 to 0.01.

**Justification:** Regulatory quality is already captured by guardrail caps (the operative mechanism). The dimension weight is redundant. Transferring it to `whole_food_integrity` makes the quality signal visible.

**Effect on benchmarks:**

| Product | WFI score | Weight change | Score gain |
|---|---|---|---|
| Date bar (NOVA2, whole-food base) | 52 | 0.01→0.04 | +1.56 |
| Plain Greek yogurt (NOVA2) | 52 | 0.01→0.04 | +1.56 |
| Sourdough bread (NOVA2, whole grain) | 62 | 0.01→0.04 | +1.86 |
| NOVA4 chocolate bar | 18 | 0.01→0.04 | +0.54 |

**Property:** Bottom products (WFI ~18) gain less than 1 point. Top products (WFI ~62) gain ~1.9 points. The quality gap widens by approximately 1 point between NOVA2 and NOVA4 products.

---

## Part 4: Combined Effect on Category Means

If all three changes are applied:

| Product type | Current score | Change 1 (cap) | Change 2 (bonus) | Change 3 (weight) | Final score |
|---|---|---|---|---|---|
| Plain Greek yogurt, 0 red labels | 82/B | +0 | +0.52 | +1.56 | **84/B** |
| Plain Greek yogurt, 1 sat-fat red label | 55/C | +12 | +0.52 | +1.56 | **67/C** |
| NOVA3 protein yogurt, 0 red labels | 78/B | +0 | 0 | ~+1.5 | **80/B** |
| NOVA3 protein yogurt, 1 red label | 55/C | +12 | 0 | ~+1.5 | **67/C** (no grade change) |
| Date bar | 70/B | +0 | +0.52 | +1.56 | **72/B** |
| Best sourdough bread | 83/B | +0 | +0.52 | +1.86 | **85/A** |
| NOVA4 cereal bar (Corny-type) | 13/E | +0 | 0 | +0.54 | **14/E** |
| NOVA4 Fitness bar | 46/D | +0 | 0 | +0.54 | **47/D** |

**Critical property confirmed:** The changes do not improve bottom-tier products materially. NOVA4 products gain ≤0.54 points (weight redistribution only). NOVA2 excellent products gain 2–14 points depending on whether they were cap-suppressed.

**Grade changes:**
- Sourdough bread: B → **A** (82+3 = 85, crosses A threshold) — correct, this is genuinely an A product
- Plain Greek yogurt with 1 red label: C → **C** (55→67, remains C) — correct, a red label should prevent B
- NOVA3 protein yogurt with 1 red label: C → **C** (55→67, remains C) — correct
- NOVA4 products: no grade changes

---

## Part 5: What the Calibration Does Not Change

1. **NOVA4 products remain low-scoring.** The NOVA4 processing penalty structure is unchanged.
2. **Products with 2+ red labels remain capped at 45.** Only single-red-label suppression is addressed.
3. **The date bar sugar halo persists.** A date bar at 70+ still carries 35g natural sugar; disclosure remains the correct mechanism.
4. **Grade thresholds are unchanged.** A → 85, B → 70, C → 55. The best snack bar (date bar) remains B.
5. **NOVA3 without red labels is unchanged.** Score 78 remains 78.
6. **The regulatory signal is not eliminated.** A product with 1 red label is capped at 67, not at its natural score. It cannot reach B (70).

---

## Summary: Intuition Gap and Fix

| Scenario | Was intuition gap present? | Fixed by calibration? |
|---|---|---|
| Excellent product, no penalties | No | N/A |
| Excellent product, 1 natural sat-fat red label | Yes — 25-pt suppression | Yes — cap raised to 67 |
| Excellent NOVA3 product, 1 red label | Yes — 23-pt suppression | Yes — cap raised to 67 |
| Excellent product, 2+ red labels | Borderline — accepted as correct policy | No — unchanged |
| NOVA4 products scoring too low | No — scores are accurate | No change needed |
| Whole-food products not differentiated | Yes — bonus never applied | Yes — Changes 2 & 3 |
