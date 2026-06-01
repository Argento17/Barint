# Classification Instability

**Purpose:** Address the risk of catastrophic scoring outcomes caused by incorrect product category or NOVA classification. Classification instability is currently the single biggest practical scoring risk in BSIP2 — not because classification is likely to be wrong in most cases, but because when it is wrong, the consequence is a score that is internally consistent but analytically absurd.

---

## Why category classification is the single biggest practical scoring risk

The BSIP2 scoring engine applies fundamentally different analytical frameworks depending on which category a product is assigned. The same product, scored with two different category assignments, can produce scores 20–40 points apart — not because the analytical result changed, but because the frame of reference changed entirely.

This is by design. Category-relative evaluation is correct. A walnut and a snack bar should not be evaluated against the same calorie density table. But this correctness creates a structural fragility: the entire analytical result depends on a classification that is itself an inference (L3 signal) with imperfect confidence.

**The core problem:**
- Hard caps in the `snack_bar_granola` category are severe (70 cap at ≥ 430 kcal; 55 cap at ≥ 470 kcal + ≥ 15g sugar)
- Whole-food floors protect NOVA 1 products at a minimum of 75
- A whole-food product that is NOVA 2 (just above the floor protection threshold) and is miscategorised into `snack_bar_granola` has no floor protection and faces the harshest possible category rules
- The gap between the correct score and the miscategorised score for such a product can exceed 30 points

This is not a marginal calibration error. It is a categorical analytical error that produces a misleading result.

---

## Anatomy of a classification disaster

**Scenario:** A date, almond, and oat ball at 480 kcal/100g, NOVA 2 (minimal processing, whole-food ingredients).

**Correct category assignment: `whole_food_fat`**
- Calorie density score at 480 kcal: ≤ 500 kcal → score 85
- NOVA 2: no processing cap
- No sugar rules fire (dates contribute natural sugar but typically ~40g/100g, triggering `HIGH_SUGAR_25G_PLUS` — see below)
- Whole-food fat floor: minimum 65 (NOVA 1–2)
- Expected final score: ~70–80, reflecting the calorie density and natural sugar with strong whole-food context

**Miscategorised as `snack_bar_granola`**
- Calorie density score at 480 kcal: ≤ 500 kcal → score 25 (the snack bar table is very strict)
- `SNACK_BAR_HIGH_CAL` fires: cap at 70 (≥ 430 kcal)
- `HIGH_SUGAR_25G_PLUS` fires on date sugar content: cap at 60
- NOVA 2: no processing cap, but calorie damage is severe
- No whole-food floor protection (NOVA 2, not NOVA 1)
- Expected final score: ~45–55 — grade D or low C

**The gap:** ~30 points. A product that should grade B scores D because a name-matching algorithm assigned it to the wrong category.

**The secondary problem:** This error is invisible in the scoring output. The score of ~50 is internally consistent — all the rules that applied were applied correctly to the category assignment. Nothing in the output indicates that the category assignment may be wrong.

---

## How classification instability manifests

### Type 1 — Ambiguous form factor

Products whose physical form is ambiguous between categories:
- A dense energy ball could be `whole_food_fat` or `snack_bar_granola`
- A spreadable nut cream could be `whole_food_fat` or `sauce_spread`
- A granola sold as a topping could be `snack_bar_granola` or `cereal`
- An oat-based bar could be `snack_bar_granola` or `cereal`

The category classification engine uses name matching and ingredient signals. For these products, the signals are genuinely ambiguous — reasonable classification algorithms will disagree.

### Type 2 — Cross-language classification

The classification engine uses Hebrew and English keywords. A product labelled entirely in Hebrew with a name that contains no category-specific keyword will fall through to `default`. But `default` has different thresholds from any specific category — the product may be evaluated against incorrect standards simply because its name was in a script the classifier handles with lower confidence.

### Type 3 — Novel product categories

New product formats (functional beverages, high-protein dairy innovations, plant-based dairy alternatives) may not match any existing category well. These products tend to fall into `default`, which applies moderate-but-not-correct thresholds.

### Type 4 — NOVA misclassification

NOVA proxy classification infers NOVA level from ingredient markers. Markers can be absent from the list despite a product being genuinely ultra-processed (FM-09 in the failure mode catalog). A NOVA 4 product classified as NOVA 2 avoids the processing cap and may score significantly higher than its actual structural quality warrants.

---

## Current mitigations and their limits

### Mitigation 1: Confidence propagation

Low category classification confidence (< 0.5) reduces analytical confidence by up to −15. This can trigger a confidence ceiling (score ≤ 70 for low confidence). The ceiling limits damage but does not correct the wrong-category score or surface the misclassification to the user.

**Limit:** The confidence propagation only fires when classification confidence is explicitly low. A misclassification with high classification confidence (the algorithm is wrong but certain) produces no confidence reduction. Confident misclassification is the hardest case to detect.

### Mitigation 2: Whole-food floors

NOVA 1 products have a minimum score of 75; NOVA 1–2 whole-food fat products have a minimum of 65. These floors partially protect genuinely whole-food products even when miscategorised.

**Limit:** The floor only protects NOVA 1 (or NOVA 1–2 for whole-food fat). A NOVA 2 date-nut ball that is not categorised as `whole_food_fat` has no floor protection. The floor only helps when the NOVA classification is correct and low enough to qualify.

### Mitigation 3: Default category as a fallback

Products with insufficient classification confidence fall to `default`, which applies moderate thresholds rather than the most severe category rules.

**Limit:** `default` is better than `snack_bar_granola` for most products, but it may still produce wrong results for products that should be in `whole_food_fat` or `dairy_protein`.

---

## What a severity-sensitive category rule looks like

The current architecture applies category rules at full severity regardless of category confidence. A more robust architecture would scale rule severity by category confidence:

**Proposed principle:**
When category confidence is below a defined threshold (e.g. 0.65), apply category-specific caps and penalties at reduced severity or not at all, and fall back to the `default` category rules for that product.

**Implementation concept:**
- If `category_confidence` ≥ 0.80: apply full category rules
- If `category_confidence` 0.50–0.79: apply a blended score between the inferred category and `default` category, weighted by confidence
- If `category_confidence` < 0.50: apply `default` category rules only; flag the product as "category uncertain" in the output

This approach means that a product classified as `snack_bar_granola` with 60% confidence does not face the full weight of snack bar category rules — it faces a weighted blend of snack bar rules and default rules. The damage from a confident-but-wrong classification is reduced.

---

## Secondary-category simulation

**Concept:** For every product scored, run the scoring engine a second time with the next-most-likely category assignment and record the score difference.

**Purpose:** Surface large score sensitivity to category assignment before the score is displayed. If a product scores 52 in its primary category and 79 in its secondary category, this is a flag that the score is classification-sensitive and should be presented with a wider uncertainty range.

**Implementation concept:**
- The category classifier already produces a ranked list of categories with confidence scores
- The secondary category is the second entry in this ranked list
- A secondary simulation re-runs the relevant scoring modules (calorie density table, category-specific caps) with the secondary category assignment
- The delta between primary and secondary score is stored as `category_sensitivity` in the output record
- Products with `category_sensitivity` > 15 points are flagged as high-sensitivity in the output

This is not a replacement for correct classification — it is a diagnostic that surfaces when correct classification matters most.

---

## Uncertainty propagation in scoring

The current architecture makes one classification decision and scores against it. A more robust architecture would propagate classification uncertainty through the score.

**In principle:** If a product is 70% likely to be `snack_bar_granola` and 25% likely to be `whole_food_fat`, the "expected score" under uncertainty is 0.7 × (snack bar score) + 0.25 × (whole food fat score) + 0.05 × (default score). This expected score is less sensitive to the binary classification outcome.

**In practice:** This requires that the scoring engine be able to compute scores for multiple categories simultaneously and combine them. This is a significant architectural change — not appropriate for the current phase, but worth documenting as a direction.

**The simpler alternative:** Use secondary-category simulation (above) to bound the score rather than to compute an expected value. Report the range rather than a point estimate when classification uncertainty is high.

---

## Instability-aware scoring: practical recommendations for the current phase

Before implementation, the following practices should be adopted to reduce classification instability impact:

1. **Track `category_confidence` and `nova_classification_confidence` in every output record.** These values should be first-class output fields, not internal diagnostics.

2. **Flag products with `category_confidence` < 0.65** as "category-uncertain" in the output. These products should receive a UI note: "Product category is uncertain; score may vary with better category information."

3. **Run secondary-category simulation** for all products in the golden products suite before implementation. Record the score delta for each product. Any product with delta > 15 is a high-priority calibration case.

4. **Define explicit category rules for the highest-risk ambiguous cases** before the full product database is scored: date-nut bars, avocado-based spreads, high-protein dairy variants, oat-based snacks.

5. **Review the whole-food floor to cover NOVA 2** (not only NOVA 1) for products confirmed as `whole_food_fat` category with high confidence. Currently NOVA 2 products in this category have no floor — only the `whole_food_fat` calorie table provides any protection, and that protection disappears with misclassification.
