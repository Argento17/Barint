# Comparison Logic

## How products are ranked

The BSIP2 final score (0–100) is the primary ranking signal. Higher score = stronger analytical result across the dimensions the system evaluates. The score is absolute — derived from each product's own signals — and products are ranked against each other by comparing those absolute values.

---

## Grade as a comparison frame

Grades give a readable bracket for comparison. Two products in the same grade band may have meaningfully different scores within it.

| Grade | Score | Comparison framing |
|-------|-------|--------------------|
| A | 85–100 | Strong across most dimensions; no significant structural concerns |
| B | 70–84 | Good overall; minor concerns in one or more areas |
| C | 55–69 | Meaningful concerns; acceptable in context |
| D | 40–54 | Multiple concerns; compare alternatives |
| E | 0–39 | Significant structural issues; hard cap or veto applied |

A 70 and an 84 are both grade B, but the gap is analytically meaningful. The UI should reflect the score alongside the grade rather than collapsing all B-grade products into a single state.

---

## Category-relative comparison

Products are evaluated against category-specific thresholds, which means comparisons within a category are analytically fair by construction. Both products are scored against the same calorie density scale, the same processing expectations, and the same guardrail rules.

Cross-category comparisons are less straightforward. A grade A nut butter and a grade A yogurt are both excellent choices — in their respective categories. They are not nutritionally interchangeable.

**UI recommendation:** always surface the product category alongside the grade when displaying ranked results that span multiple categories. This prevents the interface from implying that a 90-score tahini and a 90-score yogurt are the same kind of choice.

---

## Where score differences come from

When two comparable products have different scores, the difference is always traceable to specific analytical signals. The ten dimensions are scored independently, so a score gap almost always concentrates in two or three dimensions.

Common sources of score gap between similar products:

| Dimension | What creates the gap |
|-----------|---------------------|
| Processing Quality | One product is NOVA 4; the other is NOVA 3. One has five additive markers; the other has one. |
| Glycemic Quality | One product has 28g sugar per 100g; the other has 8g. |
| Calorie Density | Both are snack bars — one at 380 kcal/100g, one at 470 kcal/100g. Different position on the snack bar threshold table. |
| Nutrient Density | One product has 12g protein and 5g fiber; the other has 4g protein and 1g fiber. |
| Hyper-Palatability | One product triggers a fat-sugar combination pattern; the other does not. |
| Additive Quality | One product has sweeteners + two emulsifiers; the other has no additives beyond salt. |

Surfacing the dimension gap makes the comparison informative. "Product A scores 72, Product B scores 58" is less useful than "Product A has no hyper-palatability patterns and significantly more fiber; Product B carries a red label on sugar and triggers an engineered fat-sugar combination."

---

## Calorie interaction rules

The calorie engine evaluates combinations that individual dimension scores do not fully capture. A product with moderate calorie density and moderate sugar may produce a significant combined concern.

| Combination | Effect on score |
|------------|-----------------|
| ≥ 500 kcal AND ≥ 25g sugar per 100g | Hard cap: score ≤ 50 |
| ≥ 470 kcal AND ≥ 20g sugar per 100g | Hard cap: score ≤ 60 |
| ≥ 430 kcal AND ≥ 15g sugar per 100g | Soft penalty: −5 |
| ≥ 500 kcal AND protein < 6g AND fiber < 3g | Hard cap: score ≤ 55 |
| ≥ 450 kcal AND protein < 8g AND fiber < 5g | Soft penalty: −6 |

These rules explain why two products at the same calorie count can score differently. If one has 12g protein and 6g fiber and the other has 3g protein and 1g fiber, the low-satiety version faces a penalty or cap the other does not.

---

## Tradeoff evaluation

Real food choices involve tradeoffs. The dimension structure makes them explicit rather than hiding them in a single net score.

### High protein vs. isolate sourcing

A product scoring well on protein quantity may carry a `protein_isolate` marker — protein added as an isolated fraction rather than from a whole food source. The marker applies a penalty to the protein quality dimension. In a comparison, a product using whole-food protein sources will score better on that dimension even at equal protein quantity.

### Whole-food fat vs. calorie density

A nut-based product at 600 kcal/100g is scored against the `whole_food_fat` calorie threshold table — not the same table as a snack bar at 600 kcal/100g. The calorie density score for the nut product will be higher. This is correct: the calorie sources and food matrices are different. The comparison is fair precisely because it is category-aware.

### Fiber vs. added sugar

A product may have good fiber content (positive for glycemic quality, nutrient density, and satiety) while also containing significant added sugar (negative for the same dimensions, plus guardrail risk). The net position in glycemic quality reflects both. In a comparison, both signals should be surfaced — not just the net score.

### Sweetener substitution

Products using non-nutritive sweeteners instead of sugar are not analytically better. The sweetener marker applies a hard cap (final score ≤ 70) and a dimension penalty. A product with 10g sugar and no sweetener may score better than one with 2g sugar and a sweetener, depending on other signals. Sugar substitution is not equivalent to quality improvement in this model.

---

## What the score does not compare

The BSIP2 score does not evaluate:
- Taste, texture, or sensory experience
- Suitability for any specific dietary goal or health condition
- Ethical sourcing, environmental impact, or production method
- Whether the product is appropriate for a specific individual

The score answers a structural analytical question: *given what this product is made of, how does its nutritional architecture compare to others in terms of what it delivers and what it contains?*

That is both more and less than a personalised recommendation. It is more, because it is rigorous and traceable. It is less, because it makes no claims about the individual consuming the product.
