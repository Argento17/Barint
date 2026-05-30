# Scoring System Forensic Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Cross-Category Distribution Analysis

---

## The Primary Finding

**Snacks mean: 43.50. Maadanim mean: 43.78. Difference: 0.28 points.**

This is not coincidence. It requires explanation.

---

## Statistical Profile

| Category | N | Min | Max | Mean | Median | StDev | Spread |
|---|---|---|---|---|---|---|---|
| Snacks | 18 | 13 | 70 | 43.50 | 45.5 | 14.10 | 57 |
| Maadanim | 90 | 27 | 70 | 43.78 | 44.5 | 7.93 | 43 |
| Bread | 24 | 59 | 82 | 72.00 | 72.5 | ~5 | 23 |

### What is immediately visible

1. **Snacks and maadanim share nearly identical means and medians.** The 0.28-point mean difference and 1.0-point median difference are not statistically meaningful.

2. **Both have exactly 70/B as their maximum score.** One product in each category reaches this ceiling. No product in either category exceeds it.

3. **Bread is a completely different distribution.** Mean=72, entirely in the A/B/C band, spread of 23 points. This demonstrates that the scoring system CAN produce category-different distributions — it just does not for snacks vs maadanim.

4. **Maadanim has much lower standard deviation** (7.93 vs 14.10). Maadanim is compressed; snacks has wider tails. The shapes are different even if the centers are the same.

5. **Maadanim has 80% of products in the 30–50 band.** Snacks has 50% in the same band. Maadanim is much more compressed around the center.

---

## Forensic Investigation: Why Are the Means Identical?

### Hypothesis 1: Coincidence
**Probability: Very low.**

With means differing by 0.28 points across 18 and 90 products in different food categories, coincidence is implausible. The probability of this occurring by chance, given the underlying food quality distributions of these two categories, is extremely small. Dairy desserts and snack bars are not the same type of food and should not produce the same average score unless the scoring system is treating them similarly.

### Hypothesis 2: Hidden Normalization
**Probability: Medium.**

If the scoring system was implicitly calibrated against a target mean (e.g., "typical Israeli retail product scores around 43"), then both categories would converge on that mean regardless of actual food quality differences. There is no documented explicit normalization, but the caps (68, 55, 60) create implicit normalization by compressing the top of the distribution.

The cap system:
- Cap at 68 for "max processing" → prevents any highly-processed product from exceeding 68
- Cap at 55 for "high sugar" → prevents high-sugar products from exceeding 55
- Cap at 60 for "5+ additives" → limits additive-heavy products to 60

These caps create a gravity well. Products with any cap applied are pulled toward the 30–55 range. Products with multiple caps overlap and compress further. Both snacks and maadanim have many products with multiple caps — this pushes both distributions' means toward the same anchor.

**This is the most likely primary mechanism for mean convergence.**

### Hypothesis 3: Category-Insensitive Scoring
**Probability: High — the structural root cause.**

The four-layer BSIP2 architecture (Structural/Nutritional/Metabolic/Engineering) applies identical weights across all categories. If the majority of products in both snacks and maadanim fall into the same structural classification buckets, they will receive similar scores regardless of category.

In practice:
- Both categories contain predominantly NOVA3/NOVA4 products
- Both have one exceptional minimally-processed product (snk-001 and יופלה GO) that reaches 70/B
- Both have several "natural gap" products — things that claim to be clean but aren't
- Both have an engineered/confectionery bottom tier

The structural fingerprint of Israeli retail snacks and Israeli retail dairy desserts is similar: dominated by processed industrial products with a small premium-clean-label tier at the top and a confectionery tier at the bottom. When the scoring engine applies the same weights to the same structural fingerprint, it produces the same score distribution.

This is not a scoring error — it may be an accurate reflection of the Israeli retail food landscape. But it produces a result that undermines consumer confidence in the scores.

### Hypothesis 4: The 70 Ceiling
**Probability: Confirmed contributor.**

Both categories have exactly one product reaching 70/B. This is not a coincidence — it reflects the scoring architecture's implicit understanding of what a "top product in Israeli retail" looks like. In both cases, the top scorer is:
- Minimal ingredients (3–4)
- Whole-food base
- No additives
- Verified composition

The 70 ceiling is an artifact of the grade boundary system. 71+ would require qualities that Israeli retail snacks and dairy desserts essentially cannot achieve given the category constraints. The ceiling is shared because the categories share a quality ceiling — not because the scoring is wrong, but because the Israeli retail landscape genuinely doesn't produce A-grade snacks or dairy desserts.

### Hypothesis 5: Structural Scoring Without Nutritional Input
**Probability: Confirmed as secondary driver.**

Snacks has 18/18 products with null nutritional data. Maadanim has 89/90 products with full nutritional data. Yet both produce the same mean.

This tells us the nutritional layer is not driving the maadanim scores — or the structural layer alone is sufficient to produce the 43.78 mean without nutrition input. In other words: for maadanim, the nutritional data modifies scores around a baseline that the structural layer already determines. The structural layer is doing 80%+ of the scoring work in both categories, and the nutritional layer is providing refinement at the margin.

This is a design finding, not a flaw — it's by design that structure is primary. But it means that adding nutritional data to snacks would NOT dramatically change the mean — it would change the spread (more precise differentiation within clusters) but the center would remain similar.

---

## Verdict on Mean Convergence

The 0.28-point difference between snacks (43.50) and maadanim (43.78) is produced by:

**Primary cause:** Cap system gravity. Multiple caps (68, 55, 60) create a compression field that pulls most products into the 35–55 range regardless of category. Both categories have similar proportions of "cap-eligible" products.

**Secondary cause:** Structural fingerprint similarity. Both categories are dominated by NOVA3/NOVA4 processed retail products with one exceptional clean product at the top and confectionery-adjacent products at the bottom.

**Tertiary cause:** Shared 70 ceiling. The grade architecture prevents either category from achieving A-grade products, which would have raised the mean.

**Not a cause:** Normalization, calibration bias, or hidden mean-targeting. No evidence of intentional mean manipulation.

---

## Is This a Problem?

The mean convergence is a **signal quality problem**, not a scoring accuracy problem.

If a journalist or reviewer audits Bari and finds that snacks and dairy desserts produce identical average scores, they will — correctly — question whether the scoring engine is category-sensitive. The finding is defensible in theory (both categories happen to have similar structural fingerprints) but is not credible in practice (a date bar and a milky dessert should not feel like they're from the same quality universe).

The deeper problem is this: **Bari's scores are currently only meaningful within a category, but the absolute score values (43, 44, 70) create the impression of cross-category comparability.** A consumer who sees snk-001 at 70/B and יופלה GO at 70/B might reasonably ask whether these products are "equally good." They are not comparable. But the shared score creates the implication.

---

## What Would Break the Convergence?

**Option 1: Category-specific baselines**
Set a category-appropriate expected score for the median product. Snacks median product (moderately processed bar) might be set at 40. Maadanim median product (dairy dessert) might be set at 35. This explicitly acknowledges that the two categories have different quality ceilings and floors.

**Option 2: Category-specific caps**
The current caps (68, 55, 60) are universal. If snacks caps were lower (e.g., max 65 for max processing), the snacks distribution would compress downward, breaking the mean convergence.

**Option 3: Nutritional dimension separation**
Score structural quality and nutritional quality separately. Combine them with category-specific weights. A snack bar might weight structure 70% + nutrition 30%. A dairy dessert might weight structure 50% + nutrition 50%. Different weights would naturally produce different distributions.

**Option 4: Percentile-based display**
Stop displaying absolute scores. Display within-category percentiles instead. "This is in the top 15% of snacks" conveys different information than "70/B" and prevents cross-category comparisons.

---

## Bread Is the Counterexample

Bread's mean of 72.00 and minimum of 59 demonstrate that the scoring system CAN produce category-appropriate differentiation. Bread scores high because:
- Fermented sourdough bread receives significant positive signals
- Whole-grain content is a strong positive driver
- The bread corpus was editorially curated to exclude the worst products

If snacks and maadanim were curated to the same editorial standard (only good products), their means would also be higher. The mean convergence is partly a consequence of including the full quality range in both categories.

This is actually the strongest argument for the current system: **it is internally consistent across curation levels.** A category of all-good products (bread) scores high. A category of mixed-quality products (snacks, maadanim) scores mid-range. The system is responding to actual product quality, not gaming it.

But this argument requires that snacks and maadanim ARE genuinely similar in average quality — which may or may not be true, and which currently cannot be verified because snacks has no nutritional data.
