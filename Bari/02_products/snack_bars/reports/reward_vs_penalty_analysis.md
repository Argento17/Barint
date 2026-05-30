# Reward vs. Penalty Analysis
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Priority 2 Analysis  
**Question:** Does the framework subtract weaknesses more aggressively than it rewards strengths?

---

## Verdict

**Yes, in one specific and consequential way: penalty signals trigger guardrail caps that amplify their effect far beyond the dimension penalty alone. Positive signals have no equivalent amplification mechanism. The dimension scoring is approximately balanced; the cap system is not.**

---

## 1. Dimension Architecture: Penalty vs. Reward Split

Every dimension is classified by its operative direction — whether its primary mechanism adds points from a low base or subtracts points from a high base.

| Dimension | Weight | Base | Direction | Maximum achievable | Notes |
|---|---|---|---|---|---|
| processing_quality | 0.18 | 100 | Penalty only | 100 | No mechanism adds above base |
| nutrient_density | 0.16 | 50 | Hybrid | 88 | protein cap=20, fiber cap=18; sugar subtracts |
| calorie_density_quality | 0.12 | varies | Neutral (lookup) | 90–95 | Rewards low-calorie food in category |
| glycemic_quality | 0.11 | 80 | Penalty + tiny bonus | 90 | Fiber adds ≤10; sugar subtracts heavily |
| hyper_palatability | 0.10 | 100 | Penalty only | 100 | No mechanism adds above base |
| protein_quality | 0.09 | 45 | Additive | 80 | base + protein×2.0 (cap=35); genuinely rewards protein |
| additive_quality | 0.07 | 90 | Penalty only | 90 | No mechanism adds above base |
| satiety_support | 0.06 | 45 | Hybrid | ~95 | protein cap=25, fiber cap=25; sugar subtracts |
| fat_quality | 0.06 | 70 | Hybrid | 78 | +8 for nut/seed marker; -8 for seed oil |
| regulatory_quality | 0.04 | 100 | Penalty only | 100 | -18 per red label |
| whole_food_integrity | 0.01 | 52 | Hybrid (non-functional) | 65 | Bonuses designed but never applied |

**Penalty-only dimensions (no mechanism above base):** processing_quality + glycemic_quality + hyper_palatability + additive_quality + regulatory_quality = **50% of total weight**

**Additive/hybrid dimensions (genuine upside):** nutrient_density + calorie_density_quality + protein_quality + satiety_support + fat_quality + whole_food_integrity = **50% of total weight**

The weight split is exactly even. The architecture is not a penalty engine by design.

---

## 2. Where the Asymmetry Actually Lives

### Asymmetry 1: Penalty signals cascade into guardrail caps; reward signals do not

The dimension system is balanced. The guardrail system is not.

When a product has 1 Israeli red label:
- `regulatory_quality` dimension: -18 pts × weight 0.04 = **-0.72 weighted points**
- `ISRAELI_RED_LABEL_1` guardrail cap: final score ceiling at **55**

For a product with a natural dimension score of 80: the regulatory dimension reduces it to ~79.3. The guardrail cap then reduces it to 55. The guardrail delivers **-24 weighted points** on a score that the dimensions assessed as 79.3. The regulatory dimension penalty is less than 1 point; the guardrail delivers 24 times that effect.

No equivalent positive amplifier exists. There is no guardrail that raises a score because protein is exceptionally high, or because the product is NOVA2 with zero additives.

### Asymmetry 2: Penalty magnitude per unit exceeds reward magnitude per unit

**NOVA4 penalty** (the single largest individual signal):

| Dimension | Penalty value | Weight | Weighted impact |
|---|---|---|---|
| processing_quality | -24 | 0.18 | **-4.32** |
| whole_food_integrity | -14 | 0.01 | **-0.14** |
| NOVA4 guardrail cap (60) | — | — | Variable, up to -20+ |
| **Subtotal (dimensions only)** | | | **-4.46** |

**Protein reward** (+8g protein, from 4g to 12g):

| Dimension | Bonus value | Weight | Weighted impact |
|---|---|---|---|
| nutrient_density | +9.6 | 0.16 | **+1.54** |
| protein_quality | +16.0 | 0.09 | **+1.44** |
| satiety_support | +11.2 | 0.06 | **+0.67** |
| **Subtotal** | | | **+3.65** |

The NOVA4 processing penalty (-4.46 weighted pts from dimensions alone) is larger than the entire protein reward (+3.65 pts for 8g more protein). No additional guardrail amplifies the protein reward. The NOVA4 cap at 60 can amplify the processing penalty further.

**High sugar penalty** (+10g sugar, from 20g to 30g):

| Dimension | Penalty value | Weight | Weighted impact |
|---|---|---|---|
| glycemic_quality | -14 | 0.11 | **-1.54** |
| nutrient_density | -9 | 0.16 | **-1.44** |
| satiety_support | -5 | 0.06 | **-0.30** |
| HIGH_SUGAR_25G_PLUS guardrail cap (60) | — | — | Variable |
| **Subtotal (dimensions only)** | | | **-3.28** |

Sugar penalty (-3.28 pts per 10g increase) exceeds protein reward (+3.65 pts per 8g increase). With the guardrail cap, the sugar penalty can grow far larger.

### Asymmetry 3: Maximum positive contribution is smaller than maximum negative contribution

**Maximum weighted contribution of the highest-weight positive dimension:**

`nutrient_density`: max score = 88, base = 50. Max gain above floor: 38 pts × 0.16 = **+6.08 weighted points** above a zero-protein, zero-fiber product.

**Maximum weighted loss from the highest-weight penalty dimension:**

`processing_quality`: base = 100. A NOVA4 product with 5 processing markers: 100 - 24 (NOVA4) - 8 (glucose) - 6 (flavouring) - 6 (emulsifier) - 8 (coating) - 8 (extruded) = 40. Loss: 60 pts × 0.18 = **-10.8 weighted points**.

The maximum penalty from processing_quality (-10.8 pts) is 1.78× the maximum gain from nutrient_density (+6.08 pts). This is before guardrail caps are counted.

---

## 3. Quantified Penalty vs. Reward Summary

| Signal | Max effect (weighted pts) | Guardrail amplifier |
|---|---|---|
| NOVA4 classification | -4.46 (dimensions) + up to -20 (cap) | Yes — cap at 60 |
| 1 Israeli red label | -0.72 (dimension) + up to -24 (cap) | Yes — cap at 55 |
| 2 Israeli red labels | -1.44 (dimension) + up to -34 (cap) | Yes — cap at 45 |
| 5+ additive markers | -4.2 (additive_quality) + cap | Yes — cap at 55 |
| High sugar (25g+) | -3.28 per 10g + cap | Yes — cap at 60 |
| Peak protein (17.5g) | +4.95 | **No cap amplifier** |
| Peak fiber (9g nutrient + 11.4g satiety) | +5.46 | **No cap amplifier** |
| NOVA2 (vs NOVA3) | +2.16 (processing + WFI) | **No bonus amplifier** |
| whole_food_marker | +0.52 intended | **Non-functional in all scoring** |

---

## 4. Where the Framework Correctly Applies Asymmetry

The penalty asymmetry is not a pure design flaw. Several asymmetries are justified:

**Israeli red labels:** The Ministry of Health label is a regulatory warning. A product triggering a red label for added sugar is genuinely worse than the same product without added sugar. The cap at 55 for 1 red label reflects a policy decision that regulatory warnings must materially affect score. This is correct.

**NOVA4:** The NOVA classification has strong epidemiological evidence as a predictor of adverse health outcomes. Allowing a NOVA4 product to score 75+ through nutritional manipulation would undermine the framework's scientific grounding. The -4.46 weighted point penalty is a deliberate structural signal.

**Additive load:** A product with 5+ additive markers that would otherwise score 65 correctly signals that the nutritional profile does not tell the whole story.

---

## 5. Where the Asymmetry Is a Calibration Problem

**Problem A: Regulatory cap suppresses natural-food red labels identically to processed-food red labels**

A plain Greek yogurt (NOVA2, 5g saturated fat from natural dairy, 1 red label for sat fat) is capped at 55 identically to an engineered protein bar (NOVA3, 5g sat fat from palm oil, 1 red label). The cap does not distinguish between:
- Red label for a nutritional property inherent to the food's natural composition
- Red label for a manufacturing addition

Both score 55 maximum. One of these products' dimension performance would be ~82; the other ~70. Both are compressed to 55.

**Problem B: Maximum protein reward cannot offset moderate processing penalty**

`protein_quality` maximum contribution: 80 × 0.09 = 7.2 weighted points.  
`processing_quality` NOVA4 penalty alone: -24 × 0.18 = -4.32 weighted points.

A NOVA4 product with maximum protein still nets -4.32 + 7.2 (protein dimension max) - 4.46 (NOVA processing) = -1.58 weighted points relative to a NOVA2 product with the same protein. The framework correctly penalizes NOVA4 status, but the protein reward is insufficient to close the NOVA3→NOVA2 gap even for genuinely high-protein products.

**Problem C: Whole-food quality reward (whole_food_integrity) contributes ≤0.65 weighted points at maximum**

Even if fixed and fully functional: `whole_food_integrity` maximum achievable score ~65 (base 52 + nut/seed +8 + whole grain +5) × weight 0.01 = 0.65 weighted points. A product that is categorically superior on whole-food composition receives the same signal from this dimension as a product that is average — to within a rounding error on the final displayed score.

---

## 6. Penalty vs. Reward Balance: Category-by-Category Verdict

### Bread (mean=72, range 59–82)

Penalty mechanisms: Primarily NOVA classification and ingredient complexity. Most bread products are NOVA2, so processing penalties are low. The cap system rarely binds (no red labels on standard bread, no sugar caps, no additive caps).

Reward mechanisms: Whole grain adds to nutrient_density, fiber, satiety_support. Fermentation adds to processing_quality indirectly (few processing markers). Low calorie density is rewarded (default tier: ≤350 kcal → 65).

**Verdict: Balanced.** The framework correctly rewards quality bread. The best sourdough whole-grain bread scores ~82/A. The 35-point gap between bread and full snacks corpus mean reflects genuine quality differences.

### Dairy / Maadanim (mean=43.78, range 27–70)

Penalty mechanisms: Israeli red labels (saturated fat, sugar) bind hard via the 45 and 55 caps. Many dairy products carry red labels, suppressing scores regardless of nutritional excellence. NOVA3 classification applies to engineered dairy (protein yogurts, desserts).

Reward mechanisms: Protein genuinely accumulates across protein_quality, nutrient_density, satiety_support. Calorie density rewards low-calorie dairy via the dairy_protein tier (≤80 kcal → score 90). 

**Verdict: Imbalanced for red-label products.** A plain NOVA2 Greek yogurt scores ~82 (correctly). The same yogurt with 1 sat-fat red label scores 55 (cap suppresses 27 points of genuine nutritional quality). The penalty for one regulatory flag exceeds the positive contribution of exceptional protein, low sugar, and minimal processing combined.

### Snacks (mean full corpus=37.2, range 13–70)

Penalty mechanisms: NOVA4 penalty dominates (-4.46 weighted points from dimensions; guardrail cap at 68 in production). Sugar caps, additive caps, and hyper-palatability penalties layer on top. Most snack bars (58% NOVA4) are structurally penalized before nutritional quality is evaluated.

Reward mechanisms: Protein and fiber add modest positive signals. Whole-food routing (date bars, nut bars → whole_food_fat tier) grants more lenient calorie density scoring. NOVA2 products escape the -4.46 penalty.

**Verdict: Correct direction, correct magnitude.** The median snack bar scores 38.7 (E/D). This reflects genuine product quality. NOVA2 snack bars scoring 55–70 are correctly identified as better. The framework is not suppressing snacks unfairly — most snack bars genuinely are poor-quality products.

---

## 7. Numerical Calibration: Penalty and Reward at Scale

For a product that avoids all penalties (NOVA2, no additives, no red labels, low sugar, no HP combos), the five penalty-only dimensions contribute near-maximum:

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| processing_quality | 100 | 0.18 | 18.0 |
| glycemic_quality | ~80 | 0.11 | 8.8 |
| hyper_palatability | 100 | 0.10 | 10.0 |
| additive_quality | 90 | 0.07 | 6.3 |
| regulatory_quality | 100 | 0.04 | 4.0 |
| **Subtotal** | | | **47.1** |

For a product with maximal positive signals (peak protein, peak fiber, ideal calorie density):

| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| nutrient_density | 88 | 0.16 | 14.1 |
| calorie_density_quality | 90 | 0.12 | 10.8 |
| protein_quality | 80 | 0.09 | 7.2 |
| satiety_support | ~95 | 0.06 | 5.7 |
| fat_quality | 78 | 0.06 | 4.7 |
| whole_food_integrity | 65 | 0.01 | 0.65 |
| **Subtotal** | | | **43.15** |

**Theoretical maximum for a product that avoids all penalties AND maximizes all positive signals: 47.1 + 43.15 = 90.25**

In practice, no product achieves both simultaneously. The observed maximum in the corpus is 70/B for snacks and dairy, 82/A for bread. The framework's ceiling is correctly calibrated to the realistic range of supermarket products — the problem is not that excellent products can't reach high scores, it's that the regulatory cap compresses them to 55 before the ceiling is reached.
