# Category Calibration Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Category-Specific Reality Assessment

---

## The Core Question

Should a snack bar category produce a different score distribution than dairy desserts?

**Yes. Emphatically.**

The reasons are grounded in food reality, consumer expectation, and category purpose — not in scoring preference.

---

## Why Snacks and Maadanim Should Differ

### 1. Category Purpose Is Different

Dairy desserts (maadanim) are, by design, indulgent products. The category exists for pleasure. A consumer buying milky, panna cotta, or chocolate pudding is not making a health decision — they are making a pleasure decision with a known nutritional profile. The category baseline should reflect this: the median dairy dessert should sit lower than the median snack bar, because desserts are desserts.

Snack bars, by contrast, span a much wider purpose range:
- Functional nutrition (protein bars, oat bars — consumed as meal replacement or fuel)
- Convenience whole food (date bars, nut bars — consumed as "real food" alternative)
- Confectionery disguised as snacks (Corny, chocolate-coated cereal — consumed as candy)

The snack category is architecturally more complex than dairy desserts and should produce a wider, more differentiated distribution.

### 2. Ingredient Diversity Is Different

Dairy dessert ingredients are constrained: milk, cream, sugar, stabilizers, flavors. The variation space is narrow. Most products use the same 10–15 ingredients in different ratios.

Snack bars have much wider ingredient variation: dates, nuts, oats, quinoa, protein concentrate, glucose syrup, palm oil, chocolate coating, honey, peanuts, hazelnuts, cocoa, and dozens of stabilizers and emulsifiers. This wider ingredient space should produce more score differentiation.

The current data shows:
- Maadanim: StDev = 7.93 (tight)
- Snacks: StDev = 14.10 (nearly twice as wide)

Snacks IS already producing wider spread. The problem is not spread — it's mean anchor.

### 3. The Mean Should Be Category-Specific

If snacks spans from whole-food date bars (70/B) to chocolate wafer confectionery (13/E), and dairy desserts span from protein dairy (70/B) to milky cake (27/E), then:

**The snacks mean should be higher than maadanim, not equal to it.**

Here is why:
- The top snacks (date bars, oat bars) are categorically "better" products than the top maadanim (dairy desserts) because snack bars have a whole-food category that dairy desserts cannot match
- The bottom snacks (chocolate wafer, heavily processed bars) are categorically similar to bottom maadanim (milky cake)
- Therefore the snack distribution should be shifted slightly right (higher) compared to maadanim

The current means are nearly identical because the structural scoring treats both categories with the same lens and both happen to have similar proportions of processed-to-clean products. But the category reality does not support this equivalence.

### 4. Bread Demonstrates That Category Differentiation Is Possible

Bread mean = 72.00. Snacks/Maadanim means = ~43.50. This 28-point gap between bread and the other two categories is evidence that the system CAN differentiate categories. Bread scores higher because it contains a higher proportion of genuinely high-quality products (fermented sourdough, whole grains) and because the editorial curation excluded the worst products.

The bread experience shows that category mean IS malleable — it responds to the actual quality of products in the category AND to editorial curation.

---

## Is the Current Framework Too Universal?

**Yes, in three specific ways.**

### Way 1: Universal Caps

The caps (68, 55, 60) are applied identically to snacks and dairy desserts. But the structural significance of "high sugar" differs by category:

- A date bar with 60g/100g natural sugar should be capped differently than a chocolate pudding with 25g/100g added sugar
- The current cap at 55 treats all high-sugar products the same, regardless of whether the sugar is from whole-food sources or refined addition

Category-specific cap values would produce category-specific distributions:
- Snacks: natural-sugar products escape the sugar cap because the sugar source matters
- Maadanim: added-sugar products hit the cap harder because the category has no natural-sugar justification

### Way 2: Universal Grade Boundaries

A/B/C/D/E boundaries are applied universally. But what does a "C" grade mean in different categories?

- Bread C: Not fermented, not whole-grain. A genuine compromise relative to category best.
- Snacks C: A decent granola bar or date bar with minor processing. Reasonably good.
- Maadanim C: A yogurt with real fruit and limited additives. Above average for the category.

The grade label "C" implies the same quality level across categories, but it doesn't reflect that category. A consumer who sees Snacks C and Maadanim C has no basis for knowing which is relatively better within its category.

**Solution:** Grade boundaries should be category-specific. A snack bar scoring 53 (currently C) might be above the category median and deserve a B within the snack category. A maadanim product scoring 53 is in the top decile of dairy desserts and ALSO deserves a B within its category.

### Way 3: Universal Positive Signal Weights

"בסיס שלם" (whole-food base) gets the same positive signal weight whether the product is a snack bar or a dairy dessert. But in the snack context, "whole-food base" is a meaningful differentiator (date bars vs processed bars). In the dairy context, all products are fundamentally milk-based — "whole-food base" is not a useful discriminator.

Category-specific positive signal weights would allow the engine to reward what actually matters in each category:
- Snacks: whole-food base, minimal ingredient count, absence of added sweeteners
- Dairy desserts: protein density, absence of modified starch, fermentation evidence
- Bread: fermentation, whole-grain percentage, sourdough process

---

## What Should Category Distributions Look Like?

### Snacks (hypothetical well-calibrated distribution)
- Mean: ~48–52 (higher than current 43.5, reflecting that this category DOES contain genuinely good products)
- Min: ~10–15 (confectionery products appropriately floored)
- Max: ~72–75 (best whole-food bars could theoretically exceed the current 70 ceiling)
- StDev: ~15–18 (wide spread reflecting genuine heterogeneity)
- Grade distribution: A:0, B:2–3, C:5–7, D:6–8, E:3–5

### Maadanim (hypothetical well-calibrated distribution)
- Mean: ~38–42 (lower than current 43.78, reflecting that this is an indulgent category)
- Min: ~20–25 (confectionery desserts appropriately floored)
- Max: ~65–68 (a dairy dessert cannot be as clean as a 4-ingredient date bar)
- StDev: ~8–10 (medium spread — the category is inherently constrained)
- Grade distribution: A:0, B:1–2, C:12–18, D:55–65, E:15–20

### What this would communicate to consumers
- A snacks C (53/C) would represent "decent, meaningfully above average"
- A maadanim C (40/C) would represent "better than most dairy desserts"
- The categories would no longer be numerically comparable — which is correct

---

## Are We Forcing Categories Into the Same Statistical Shape?

Yes, but not deliberately.

The universal cap architecture creates a gravitational pull that compresses all categories toward the same center (approximately 35–55). The caps define the floor and ceiling of the "normal distribution zone" for any category with typical retail products.

This is a consequence of using universal caps, not a deliberate normalization choice. But the effect is normalization.

The correction is not to add normalization — it's to make the existing implicit normalization explicit and category-specific.

---

## Recommendations

1. **Set category-expected medians explicitly.** Snacks expected median: 48. Maadanim expected median: 40. Bread expected median: 72. Calibrate caps to produce these outcomes.

2. **Apply category-specific grade boundaries.** Do not use the same A/B/C/D/E thresholds across categories. Each category should define its own grade cutoffs based on what the best and worst achievable scores actually are.

3. **Differentiate the 70 ceiling.** Snacks and bread can potentially exceed 70 if a genuinely exceptional product is present. Maadanim should be capped lower (65 max) because the category cannot structurally achieve whole-food simplicity.

4. **Add "category context" to every explanation.** When a snack scores 53/C, the consumer should see: "מעל חציון הקטגוריה (48)" not just "C." This connects the absolute score to the category reality.
