# Strength Recognition Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Product Owner Challenge Response  
**Question:** Is Bari systematically under-rewarding genuinely good products?

---

## Direct Answer

**Partially yes — but not for the reason the product owner suspects.**

Bari is not primarily a penalty engine by design: 50% of total score weight sits in additive/hybrid dimensions that genuinely accumulate quality points. The under-rewarding is caused by three specific architectural problems, not by the general philosophy. One is a code bug. Two are calibration decisions that deserve reconsideration.

---

## 1. Is Bari a Penalty Engine?

**By dimension count:** No. 6 of 11 dimensions have genuine upside mechanisms.  
**By effective contribution:** The question is more nuanced.

### Architecture audit

| Dimension | Weight | Architecture | Base | Max possible | Notes |
|---|---|---|---|---|---|
| processing_quality | 0.18 | Penalty-from-ceiling | 100 | 100 | Only subtracts; no upside beyond base |
| nutrient_density | 0.16 | Hybrid (additive + penalty) | 50 | ~88 | Genuinely rewards protein (cap 20) and fiber (cap 18) |
| calorie_density_quality | 0.12 | Lookup table | varies | 90–95 | Rewards low-calorie foods in appropriate category |
| glycemic_quality | 0.11 | Penalty-from-ceiling + tiny fiber bonus | 80 | ~90 | Fiber adds ≤10 pts; mostly penalty-driven |
| hyper_palatability | 0.10 | Penalty-from-ceiling | 100 | 100 | Only subtracts for engineered combos |
| protein_quality | 0.09 | Additive (base + accumulation) | 45 | 80 | Strongest reward mechanism in the engine |
| additive_quality | 0.07 | Penalty-from-ceiling | 90 | 90 | No upside; only subtracts |
| satiety_support | 0.06 | Hybrid (additive + penalty) | 45 | ~95 | Rewards protein (cap 25) and fiber (cap 25) |
| fat_quality | 0.06 | Hybrid (penalty + nut bonus) | 70 | 78 | +8 for nut/seed presence; otherwise mostly penalty |
| regulatory_quality | 0.04 | Penalty-from-ceiling | 100 | 100 | Only subtracts for red labels |
| whole_food_integrity | 0.01 | Hybrid (broken) | 52 | ~65 | Weight too low to matter; bonus code non-functional |

**Penalty-from-ceiling weight:** processing_quality + glycemic_quality + hyper_palatability + additive_quality + regulatory_quality = **0.50**  
**Additive/hybrid weight:** nutrient_density + calorie_density_quality + protein_quality + satiety_support + fat_quality + whole_food_integrity = **0.50**

The split is exactly even. But this symmetry conceals two problems.

### Problem 1: Penalty signals cascade further than reward signals

NOVA4 classification propagates negative signals across **four** dimensions simultaneously:
- processing_quality: -24
- whole_food_integrity: -14
- Guardrail cap at 60 (non-binding currently, but present)
- Additional processing markers (glucose syrup, flavouring, emulsifier, coating) compound the penalty

High sugar (30g/100g) propagates negative signals across **three** dimensions:
- glycemic_quality: -(30-5)×1.4 = -35 pts
- nutrient_density: -(30-5)×0.9 = -22.5 pts
- satiety_support: -(30-15)×0.5 = -7.5 pts

High protein (12g vs 4g, +8g) propagates positive signals across **three** dimensions:
- nutrient_density: +8×1.2 = +9.6 pts
- protein_quality: +8×2.0 = +16 pts
- satiety_support: +8×1.4 = +11.2 pts

The raw dimension points are roughly symmetric. But the penalty signals then trigger GUARDRAIL CAPS — hard ceilings that cut the final score. Positive signals have no equivalent upward mechanism. This is the asymmetry.

### Problem 2: The regulatory cap double-penalizes the same signal

When a product has 1 Israeli red label:
1. `regulatory_quality` dimension: -18 pts × weight 0.04 = **-0.72 weighted points**
2. `ISRAELI_RED_LABEL_1` guardrail: hard cap at **55**

A product with a natural dimension score of 78 that has 1 red label (e.g., saturated fat from natural dairy) is:
- First reduced in regulatory_quality (mild: -0.72 pts)
- Then capped at 55 regardless of all other dimension scores (severe: effectively -23 pts)

The dimension penalty and the guardrail cap are both triggered by the same red label. This double-counts the penalty. For products where the red label reflects natural food composition (dairy saturated fat, nut fat density), the 55 cap is the primary mechanism suppressing "genuinely good" products.

### Problem 3: The whole-food positive signal is non-functional

`bsip2_dimensions.py` contains two code paths that award a bonus for `has_whole_food_marker`:

```python
# processing_quality (line 59–60)
if f.get("has_whole_food_marker"):
    pq += p["whole_food_bonus"]   # ← KeyError: 'whole_food_bonus' not in config

# whole_food_integrity (line 120–121)
if f.get("has_whole_food_marker"):
    wfi += p["whole_food_bonus"]  # ← KeyError: 'whole_food_bonus' not in config
```

`bsip2_config.py` uses the key `"matrix_marker_bonus"` (not `"whole_food_bonus"`) in both `processing_quality` and `whole_food_integrity` parameter blocks. This is a naming mismatch. If any product has `has_whole_food_marker=True`, the scoring engine throws a `KeyError`.

The consequence: the code path that was designed to reward genuinely whole-food products — giving them a bonus in processing_quality (value: 2.5 points) and whole_food_integrity (value: 7 points) — has never fired for any scored product. Products like date bars, nut bars, and fermented dairy receive no explicit processing_quality bonus for being whole-food based. They simply avoid being penalized.

This is not a philosophical problem. It is a bug.

---

## 2. Does the Framework Subtract Weaknesses More Aggressively Than It Rewards Strengths?

**In magnitude: roughly comparable at the dimension level.**  
**In effect: yes, because caps amplify penalties without equivalent reward amplification.**

| Mechanism | Type | Approximate effect on final score |
|---|---|---|
| NOVA4 reclassification (4→3) | Penalty relief | +8–15 pts (depends on processing markers) |
| 1 Israeli red label | Penalty + cap | Up to -23 pts (if cap is binding) |
| High protein (4g → 12g) | Reward | +2.73 pts |
| High sugar (20g → 30g) | Penalty | -3.1 pts |
| 5 additive markers (0 → 5) | Penalty | -4.2 pts (plus possible cap) |
| Whole-food marker bonus | Reward | 0 pts (non-functional) |
| whole_food_integrity dimension | Reward | ≤0.65 pts (weight too low) |

The asymmetry is clearest at the top: the maximum penalty from a binding regulatory cap (-23 pts) has no equivalent positive mechanism. The most powerful positive signal (NOVA2 status) is expressed as absence of a penalty rather than presence of a reward.

---

## 3. Strength Recognition Review by Category

### Bread (24 products, mean=72, stdev~5, range 59–82)

| Benchmark | Score | Grade | Is Bari rewarding correctly? |
|---|---|---|---|
| Best product (sourdough, whole grain, no additives) | ~82 | A | **YES** — Near-maximum achievable |
| Upper quartile (~75th percentile) | ~75–78 | B | **YES** — Strong B reflects genuine quality |
| Median | 72 | B | **YES** — Median bread is B; accurate |

**Bread verdict: Strength is correctly recognized.** The best available bread reaches A. The median commercial whole-grain bread lands at B. The score range (59–82) appropriately spans the actual quality range. No calibration change is needed for bread.

**Why bread works:** Sourdough whole-grain bread hits near-perfect scores across most dimensions: low sugar, low calories, high fiber, minimal additives, no red labels, NOVA2. The calorie density tier for bread (not the `snack_bar_granola` tier) is lenient. Every quality signal compounds.

---

### Maadanim / Dairy Desserts (90 products, mean=43.78, stdev=7.93, range 27–70)

| Benchmark | Score | Grade | Is Bari rewarding correctly? |
|---|---|---|---|
| Best product (יופלה GO — high protein, low cal, fermented, NOVA2) | 70 | B | **BORDERLINE** — B is accurate but ceiling is tight |
| Upper quartile (~75th percentile, ~49) | ~49 | D | **PROBLEMATIC** — D for the top quartile of a category feels wrong |
| Median | ~43–44 | D | Accurate — most maadanim ARE lower quality |

**Maadanim verdict: The best products are appropriately scored, but the D-grade upper quartile exposes a category calibration gap.**

The 75th percentile of maadanim landing in D-grade means that a product genuinely better than 75% of its category is still labeled D. This is the correct score in universal terms, but it communicates poorly: a consumer seeing D does not understand "this is the best available in this category."

**The specific 50–60 complaint:** A high-quality NOVA3 protein yogurt (engineered, protein isolate added, but low sugar, low calorie, minimal additives) would score approximately:

| Dimension | Score | Weighted |
|---|---|---|
| processing_quality | 88 (NOVA3: -12) | 15.84 |
| nutrient_density | 67 (15g protein, low sugar) | 10.72 |
| calorie_density_quality | 80 (100 kcal, dairy_protein tier) | 9.60 |
| glycemic_quality | 79 (6g sugar) | 8.69 |
| hyper_palatability | 100 (no HP combos) | 10.00 |
| protein_quality | 70 (45+30, -5 isolate) | 6.30 |
| additive_quality | 66 (2 stabilizers: 90 - 24) | 4.62 |
| satiety_support | 66 (protein dominant) | 3.96 |
| fat_quality | 62 (moderate sat fat) | 3.72 |
| regulatory_quality | 82 (1 red label: 100 - 18) | 3.28 |
| whole_food_integrity | 40 (NOVA3 - ingredients) | 0.40 |
| **Natural total** | | **~77.1** |

Without any binding cap, this product scores ~77/B. But if it has 1 red label (saturated fat threshold), the ISRAELI_RED_LABEL_1 guardrail caps it at **55/C** — a -22 point suppression from a single regulatory flag.

**This is the 50–60 problem.** The product's natural dimension performance would score ~77/B. The binding 1-red-label cap reduces it to 55. The product owner's intuition is correct that this product's quality is not fully expressed in the score — but the suppression mechanism is the regulatory cap, not the penalty engine.

---

### Snacks (53 products full corpus, mean=37.2, stdev=15.43, range 13–70)

| Benchmark | Score | Grade | Is Bari rewarding correctly? |
|---|---|---|---|
| Best product (date bar, NOVA2, 4 ingredients) | 70 | B | **YES** — date bars genuinely are the best available |
| Upper quartile (~75th percentile, ~47.6) | ~47–48 | D | **APPROXIMATELY RIGHT** — upper quartile of snacks IS D quality |
| Median | 38.7 | E | **MOSTLY RIGHT** — the median snack bar is poor quality |

**Snacks verdict: The scoring is broadly correct, but the date bar at 70 captures a philosophical concern.**

The best minimally-processed snack available in supermarkets (4-ingredient date/nut bar) correctly scores 70/B. A genuinely clean nut bar (almonds, salt, nothing else) would score approximately 68–72. The NOVA2 category is well-rewarded.

The concern is within NOVA3 snacks: oat-based bars with modest additives scoring 47–55 feel like D or barely C, when they are genuinely better than most snacks available. The product owner is correct that "better than 80% of available snacks" should not read as D to a consumer. This is a grade threshold calibration issue, not a scoring issue — confirmed by the prior advisory board analysis (Option A2).

---

### Protein Yogurts (cross-category analysis)

This product type sits in maadanim but deserves specific analysis since it triggered this review.

**Scenario 1: Plain Greek yogurt (NOVA2, 10g protein, 5g sugar, 80 kcal, no additives)**
Estimated score: **~83–85/B → A**. This product is correctly rewarded. A plain, genuinely unprocessed Greek yogurt should score B+. It does.

**Scenario 2: NOVA3 protein yogurt (engineered, good nutritional profile, no red labels)**
Estimated score: **~77/B**. Appropriate. The NOVA3 processing penalty is reflected but nutrition compensates partially.

**Scenario 3: NOVA3 protein yogurt (same as above, 1 red label for saturated fat)**
Estimated score after cap: **55/C**. This is the complaint. The cap mechanism, not the dimension scoring, produces a score the product owner finds inaccurate.

**Scenario 4: NOVA3 protein yogurt with sweeteners and 3+ additives**
Estimated score: **45–50/D**. Appropriate. This product has genuine structural problems.

**Conclusion:** The complaint about "50–60 feels wrong" is specifically about Scenario 3, not Scenario 4. The distinction matters for the fix.

---

## 4. What Score Should the Best Realistically Available Product Receive?

| Category | Best available product type | Current score | Appropriate range | Assessment |
|---|---|---|---|---|
| Bread | Sourdough whole grain, 4–6 ingredients | 80–82 | 80–88 | **CORRECT** |
| Dairy | Plain Greek yogurt / labane, NOVA2 | ~83–85 | 78–88 | **CORRECT** (if no red labels) |
| Dairy | Strong protein yogurt, NOVA3, 1 red label | 55 (capped) | 65–75 | **UNDER-REWARDED by cap** |
| Snacks | Date/nut bar, NOVA2, 3–5 ingredients | 68–72 | 65–78 | **CORRECT** |
| Snacks | Clean oat-based bar, NOVA3, minimal additives | 47–55 | 52–62 | **BORDERLINE** |

The framework correctly identifies the best products in each category. The under-rewarding is specific: products whose quality is suppressed by a binding regulatory cap (1 red label) even when their dimension profile is strong.

---

## 5. Where Positive Credit Is Genuinely Too Thin

### Gap 1: Whole-food bonus is non-functional (code bug)
Products with `has_whole_food_marker=True` receive no bonus in processing_quality (intended: +2.5) or whole_food_integrity (intended: +7). The code references a key that does not exist in the config. Effect: ~0.2–0.5 weighted points of positive signal are never applied.

### Gap 2: whole_food_integrity weight makes the dimension irrelevant
Even if the bonus code were fixed, `whole_food_integrity` at weight 0.01 contributes a maximum of 0.65 weighted points. A genuinely whole-food product scores the same as an average product on the final score because this dimension is essentially invisible.

### Gap 3: Regulatory cap double-penalizes without relief mechanism
One Israeli red label triggers BOTH a dimension penalty (-0.72 weighted pts) AND a guardrail cap at 55 (up to -23 pts if binding). There is no "natural source" relief for red labels that are inherent to whole-food composition (dairy fat, nut density).

### Gap 4: Protein quality caps too early
protein_quality maximum is base(45) + cap(35) = 80 × weight(0.09) = 7.2 weighted points. Going from 10g to 20g protein adds only +7 pts to protein_quality (from min(10×2, 35)=20 to min(20×2,35)=35 → +15 dimension points × 0.09 = +1.35 weighted pts). The marginal reward for exceptional protein diminishes sharply above 10g.

### Gap 5: Fermentation depth is not differentiated
A 4-hour commercial yeast bread and a 48-hour naturally fermented sourdough score identically on fermentation credit. The `has_whole_grain_marker` bonus exists but there is no equivalent signal depth recognition for fermentation quality.

---

## 6. Verdict

| Question | Answer |
|---|---|
| Is Bari primarily a penalty engine? | By design: no (50/50 weight split). By effect: partially, due to cap amplification |
| Does it subtract weaknesses more than it rewards strengths? | Yes, because caps have no equivalent positive amplification mechanism |
| Does bread receive enough positive credit? | Yes — scoring is accurate and well-calibrated |
| Does dairy receive enough positive credit? | Yes for NOVA2; No for NOVA3 products with 1 binding red label |
| Do minimally processed snacks receive enough credit? | Yes at NOVA2; borderline at NOVA3 |
| Is the 50–60 protein yogurt score wrong? | Yes — the binding 1-red-label cap is the primary suppressor, not the dimension engine |
| Is the framework identifying quality products correctly? | Yes — the dimension engine produces accurate rankings |
| Is it expressing them with scores that are too low? | Only in the specific case of regulatory cap over-suppression |

**The framework is not systematically under-rewarding quality. It is correctly identifying quality. The scores are being suppressed in specific scenarios by a cap mechanism that is doing more work than intended for products whose red label reflects natural food composition rather than manufacturing choices.**

The fix is targeted, not architectural. See `positive_signal_recalibration_v1.md`.
