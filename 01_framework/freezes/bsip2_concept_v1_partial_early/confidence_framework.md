# Confidence Framework

## What confidence measures

Every BSIP2 score comes with a confidence value (0–100) that reflects the system's certainty in the analytical result. Confidence is not a measure of food quality — it is a measure of how much the engine trusts its own inputs.

Low confidence does not mean a product is bad. It means the available data is insufficient to support a strong analytical conclusion, and the score should be interpreted accordingly.

---

## What reduces confidence

### Missing critical nutritional fields

Each missing field from the nutrition panel reduces confidence by a defined amount:

| Missing field | Confidence reduction |
|---------------|---------------------|
| Energy (kcal) | −10 |
| Protein | −10 |
| Carbohydrates | −10 |
| Fat | −10 |
| Fiber | −5 |
| Sodium | −5 |
| Ingredient list entirely absent | −25 |

A product missing energy, protein, carbohydrates, fat, and ingredient data starts at confidence 40 — which immediately triggers a confidence ceiling (see below).

### Suspicious data patterns

Data inconsistencies that suggest labelling error, unit confusion, or data corruption:

| Pattern | Confidence reduction |
|---------|---------------------|
| Sugar reported greater than total carbohydrates | −20 |
| Saturated fat reported greater than total fat | −20 |
| Energy value below 20 kcal/100g (implausible) | −10 |
| Energy value above 700 kcal/100g (possible unit error) | −10 |

These reductions are applied regardless of which direction the error would push the score. A product with suspiciously low declared calories is penalized in confidence even if lower calories would improve its score.

### Classification uncertainty

| Uncertainty type | Confidence reduction |
|-----------------|---------------------|
| Low NOVA classification confidence | Up to −10 (scaled by uncertainty) |
| Low category classification confidence | Up to −15 (scaled by uncertainty) |

Both NOVA and category classification are inferences, not database lookups. Their individual confidence scores are tracked and propagate into analytical confidence proportionally.

---

## Confidence bands

| Band | Range | Meaning |
|------|-------|---------|
| High | 80–100 | Strong data quality; classification certain; score reliable |
| Medium | 60–79 | Minor gaps or uncertainties; score directionally reliable |
| Low | 40–59 | Meaningful data gaps; score should be interpreted with care |
| Insufficient | < 40 | Critical data absent; score not analytically reliable |

---

## How confidence affects the final score

Confidence does not just sit alongside the score — it actively constrains it.

**Insufficient confidence (< 40):** The final score is capped at 50. A product with critical data missing cannot receive a high grade, because the data needed to justify that grade is not present.

**Low confidence (40–59):** The final score is capped at 70. Even if dimension scores and guardrails would produce a higher result, the ceiling applies.

**Medium and high confidence:** No ceiling applies. The score reflects the full analytical result.

This means a product with genuinely strong nutritional architecture but missing ingredient data cannot receive an A or B grade. The appropriate response is to obtain better source data, not to trust an incomplete analysis.

---

## Confidence bands in the product experience

Confidence bands communicate to the user how much weight to place on a score.

**High confidence:** Score can be presented without qualification. All signals are well-supported.

**Medium confidence:** Score is presented with a minor qualification. The user should know that the result is directionally sound but may shift with better data.

**Low confidence:** Score should be presented with explicit uncertainty framing. The grade is a best estimate, not a definitive assessment.

**Insufficient:** Score is not suitable for primary display. The product card should lead with the data gap rather than the score. A grade cannot responsibly be assigned.

---

## What confidence does NOT measure

Confidence is not:
- A reflection of how "natural" or "clean" the product is
- A measure of whether the manufacturer's claims are accurate
- A signal that the product is poor quality

A plain walnut with a complete nutrition panel will have high confidence. A functional protein bar with a missing fiber value will have lower confidence. The walnut may score better or worse than the bar — but the confidence difference is entirely about data quality, not product quality.

---

## Data-driven confidence improvements

The main paths to improving analytical confidence for a product:

1. Complete nutrition panel (energy, protein, carbs, fat, fiber, sodium, sugar)
2. Ingredient list present and parseable
3. Clear category signal (name or retailer classification)
4. No suspicious data patterns in the nutrition panel

Where multiple data sources are available for the same product (e.g., from multiple retailers), the BSIP1 data quality layer selects and validates the best observation before passing data to BSIP2.
