# Category Distribution Analysis v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Revised Analysis (Data Lineage Confirmed)  
**Critical update:** BSIP1 and BSIP2 had full nutritional and ingredient access for all 18 displayed snacks. Previous analysis assumed data was missing. This document supersedes the relevant sections of `snacks_scoring_red_team_review_v1.md`.

---

## The Central Finding

**The mean convergence between snacks (43.50) and maadanim (43.78) is an editorial selection artifact, not a scoring framework failure.**

Evidence:

| Dataset | N | Mean | Median | StDev | Spread |
|---|---|---|---|---|---|
| Snacks — full BSIP2 corpus (53 products) | 53 | **37.20** | 38.7 | 15.43 | 56.6 |
| Snacks — displayed shelf (18 editorial picks) | 18 | **43.50** | 45.5 | 14.10 | 57.0 |
| Maadanim — displayed shelf (90 products) | 90 | **43.78** | 44.5 | 7.93 | 43.0 |
| Bread — displayed shelf (24 products) | 24 | **72.00** | 72.5 | ~5.0 | 23.0 |

**The full unedited snacks corpus (37.20) sits 6.58 points below maadanim (43.78).** This is the true cross-category comparison. The scoring engine is correctly producing different means for different categories.

The displayed snacks (43.50) appear to converge with maadanim because the editorial team selected 18 products from the better end of a 53-product corpus. That selection inflated the displayed mean by **+6.30 points** relative to the full corpus mean.

---

## Why the Displayed Mean Is 6.3 Points Above the True Mean

The 18 displayed snacks were selected by criteria including: score spread across categories, editorial interest, brand diversity, avoiding near-duplicates. This is correct editorial practice. But the consequence is that the displayed shelf overrepresents the top tier:

| Score band | Full corpus (53) | Displayed (18) | Over/Under-representation |
|---|---|---|---|
| 60–100 | 2 (4%) | 1 (6%) | Slight over |
| 50–60 | 15 (28%) | 7 (39%) | **Significantly over** |
| 40–50 | 8 (15%) | 8 (44%) | **Significantly over** |
| 30–40 | 7 (13%) | 2 (11%) | Roughly proportional |
| 0–30 | 21 (40%) | 0 (0%) | **Entirely excluded** |

All 21 products scoring below 30 — representing 40% of the full corpus — were excluded from display. This is editorially correct (very low-scoring products with similar composition should not dominate the shelf), but it creates a displayed distribution that is not representative of the full category quality distribution.

---

## The Real Category Comparison

When comparing categories at their actual corpus scope:

| Category | Full corpus N | Mean | What it tells us |
|---|---|---|---|
| Bread | 24 | 72.0 | High-quality category: fermentation, whole grains dominate |
| Maadanim | 90 | 43.78 | Mid-quality: dairy protein helps, but added sugar + processing hurts |
| Snacks (full) | 53 | 37.20 | Lower quality on average: NOVA4 dominates (31/53 = 58%) |
| Snacks (displayed) | 18 | 43.50 | Editorial selection — not representative of full category |

**The scoring engine IS producing meaningful category differentiation:**
- Bread sits 35 points above snacks (full corpus)
- Maadanim sits 6.6 points above snacks (full corpus)
- These gaps reflect real food quality differences

The 6.6-point gap between maadanim and full snacks makes nutritional sense:
1. Dairy products (maadanim) contain naturally-present protein that boosts nutrient_density and protein_quality dimensions
2. Dairy caloric density (~70-150 kcal/100g) is far lower than snack bars (~350-480 kcal/100g), benefiting calorie_density_quality
3. Snacks are 58% NOVA4 (vs much lower in maadanim), applying systematic processing penalties

---

## NOVA Classification Drives the Distribution

The scoring engine produces clear NOVA-stratified means within snacks:

| NOVA class | N (full corpus) | Mean score | Explanation |
|---|---|---|---|
| NOVA 2 | 7 | 54.5 | Date bars, minimal processing — whole-food base |
| NOVA 3 | 15 | 47.4 | Granola bars, cereal bars — processed but not ultra |
| NOVA 4 | 31 | 28.4 | Ultra-processed: cereal bars, coated bars, fitness bars |

This is a 19-point step between NOVA3 and NOVA4 averages, and a 7-point step between NOVA2 and NOVA3. The scoring engine is successfully using NOVA classification as a primary quality discriminator.

---

## Why Snacks and Maadanim Have Different Score Shapes

Even at the displayed level, the shapes of the distributions differ significantly:

- **Snacks (displayed):** StDev = 14.10. Bimodal: a clean-label cluster (55–70) and a processed cluster (13–47). Wide spread.
- **Maadanim (displayed):** StDev = 7.93. Compressed: 80% of 90 products cluster in the 30–50 range. Narrow spread.

This difference in shape is correct behavior:
- Maadanim has a structurally narrow ingredient diversity — all products start with milk or cream. The variation is limited.
- Snacks span from 4-ingredient date bars to 15-ingredient protein bars with chocolate coatings — the ingredient diversity is extreme, producing wide score spread.

The framework correctly captures this structural difference through the NOVA and processing dimensions.

---

## Verdict on the Distribution Similarity

| Question | Answer |
|---|---|
| Is the 43.5 vs 43.78 gap a scoring flaw? | **No. It is an editorial selection artifact.** |
| Does the full corpus show category discrimination? | **Yes. Full snacks=37.2, maadanim=43.78, bread=72.0.** |
| Is the shape of the distributions different? | **Yes. Snacks has wider spread (StDev 14 vs 8).** |
| Should Bari disclose the editorial selection effect? | **Yes. Showing 18/53 creates a biased impression.** |
| Is the scoring engine producing incorrect means? | **No. The engine's category outputs are directionally correct.** |

---

## Recommended Disclosure

The snacks shelf methodology should disclose the selection effect explicitly:

> "הצגנו 18 מוצרים מתוך 53 שנוקדו. ממוצע כלל 53 המוצרים: 37. הדגש על מוצרים מגוונים מעלה את ממוצע המדף המוצג. ממוצע גבוה יותר לא משקף את האיכות הממוצעת של מדף החטיפים."

Without this disclosure, the comparison page implies that snack bars are approximately as good as dairy desserts on average — which the full corpus does not support.
