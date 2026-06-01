# Category Discrimination Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Can Bari Distinguish Categories?

---

## Verdict First

**Yes. Bari's scoring engine meaningfully distinguishes snacks, dairy desserts, and bread at the full-corpus level. Category discrimination is real and directionally correct.**

The discriminating power is strong between bread and everything else, moderate between maadanim and snacks, and internally strong within snacks by NOVA classification.

---

## Cross-Category Discrimination

| Category | Corpus N | Mean | StDev | Range |
|---|---|---|---|---|
| Bread | 24 | 72.00 | ~5 | 59–82 |
| Maadanim | 90 | 43.78 | 7.93 | 27–70 |
| Snacks (full corpus) | 53 | 37.20 | 15.43 | 13–70 |

### Bread vs. Everything Else

The 28–35 point gap between bread and snacks/maadanim is large, statistically robust, and structurally correct.

**Why bread scores higher:**
1. Fermented breads receive fermentation positive signals (sourdough = quality matrix marker)
2. Whole-grain content is a strong positive across nutrient_density, whole_food_integrity, and satiety_support
3. Bread typically has 4–8 ingredients — no additive load penalty
4. Bread has no Israeli red labels in the displayed corpus (naturally low sugar, moderate sodium)
5. NOVA distribution: very few NOVA4 breads exist in a real bread corpus

**This is correct behavior.** Sourdough whole-grain bread is genuinely a better-quality food than a chocolate-coated ultra-processed cereal bar. The 35-point gap is proportionate.

### Maadanim vs. Snacks (Full Corpus)

The 6.58-point gap (43.78 vs 37.20) is moderate but real. The direction is correct: dairy desserts score higher on average than snack bars.

**Why maadanim scores higher than full snacks:**
1. **Dairy protein:** Milk protein contributes directly to protein_quality (base 45 + protein_coef×protein_g) and nutrient_density. A product with 10g protein/100g (e.g., יופלה GO) receives +24 points to nutrient_density from protein alone.
2. **Lower calorie density:** Dairy desserts at 70–130 kcal/100g use the dairy_protein calorie tier (80→90 score for low-calorie dairy). Snack bars at 350–480 kcal/100g use the snack_bar_granola tier (430kcal → score 40).
3. **Fewer NOVA4 products:** Snacks is 58% NOVA4; maadanim has far fewer ultra-processed products relative to its corpus size.

**This 6.58-point gap is the true signal. It is consistent with real-world nutritional differences between the categories.**

The displayed snacks (43.50) appear to match maadanim (43.78) only because editorial selection removed 35 of 53 products — specifically, the 21 products scoring below 30 (all of them excluded from display).

---

## Within-Category Discrimination

### Snacks: NOVA-stratified discrimination

The scoring engine produces clear stratification within snacks by NOVA classification:

| Tier | NOVA | N (full corpus) | Mean | What it identifies |
|---|---|---|---|---|
| Tier 1 | 2 | 7 | 54.5 | Date bars, nut bars — whole-food base, minimal processing |
| Tier 2 | 3 | 15 | 47.4 | Granola bars, cereal bars — processed but structured |
| Tier 3 | 4 | 31 | 28.4 | Ultra-processed: coated bars, Fitness-brand, Corny family |

The 19-point step between NOVA3 and NOVA4 is the framework's strongest discriminating signal. Within each NOVA tier, the engine further differentiates by nutritional content (protein, fiber, sugar) and additive load.

**This is correct and meaningful.** A date bar with 4 ingredients (NOVA2) is categorically different from a chocolate-coated ultra-processed wafer bar (NOVA4), and the scoring reflects this.

### Maadanim: Protein-stratified discrimination

Maadanim products are primarily differentiated by:
1. Protein source quality (dairy protein vs. modified starch + sugar)
2. Sugar load (desserts vs. fermented dairy)
3. Additive complexity (natural dairy vs. engineered structure)

The spread in maadanim is narrower (StDev 7.93) because the ingredient diversity is narrower — all products start with milk or cream. The scoring engine correctly produces tight clustering in the mid-range.

### Bread: Fermentation-stratified discrimination

Bread discriminates primarily by:
1. Fermentation presence (sourdough vs. commercial yeast)
2. Whole-grain percentage
3. Ingredient complexity (bread improvers, sugars added)

The narrow spread (range 59–82, StDev ~5) reflects a corpus that was editorially selected to include only quality breads. The tight clustering is editorial, not a scoring limitation.

---

## Where Category Discrimination Fails

### 1. The 70 ceiling is shared across snacks and maadanim

Both categories have exactly one product reaching 70/B (snk-001 date bar and יופלה GO). The shared ceiling is not artificial — it reflects that BOTH products achieve near-perfect structural simplicity within their categories. A date bar with 4 ingredients and a protein dairy product with 3 ingredients genuinely should score similarly on a structural-first framework.

**However,** the shared grade (B) implies equal quality to a consumer who doesn't read the explanation. This is a communication problem, not a scoring problem.

### 2. Maadanim is penalized by red labels; snacks are not

Israeli red labels appear on many maadanim products (sugar content above threshold, saturated fat above threshold). These trigger regulatory caps. Snacks in the displayed corpus have fewer red labels.

This creates an asymmetric severity effect: the regulatory guardrail hits maadanim harder than it hits snacks. This may or may not be appropriate — it depends on whether snack products genuinely avoid red labels or whether the data didn't capture them.

### 3. Calorie density is category-specific — but the categories overlap

The `snack_bar_granola` calorie tier penalizes bars above 430 kcal severely. The `dairy_protein` tier is much more lenient (250 kcal → score 55, vs snack bar at 430 kcal → score 40). This is already category-specific discrimination built into the engine.

But some snacks route to `whole_food_fat` (e.g., date bars, nut bars) which uses the most lenient calorie tier. This routing is correct for genuine whole-food fat products (nuts, tahini) but may over-reward calorically dense date bars by categorizing them alongside olive oil.

### 4. The displayed corpus creates false equivalence between displayed-snack and maadanim means

A consumer comparing the snacks page (mean ~43.5) to the maadanim page (mean ~43.78) would conclude: "these categories have the same average quality." The full corpus says: "snacks are 6.6 points worse on average." This is the most significant discrimination failure — but it lives in the editorial layer, not the scoring layer.

---

## Summary: Discrimination Scorecard

| Test | Result |
|---|---|
| Bread vs. snacks/maadanim | **PASS — 35-point gap, strong** |
| Maadanim vs. full snacks corpus | **PASS — 6.6-point gap, directionally correct** |
| Within-snacks NOVA stratification | **PASS — 19-point step from NOVA3→NOVA4** |
| Displayed snacks vs. maadanim | **FAIL — editorial selection removes the gap** |
| Shared 70 ceiling across categories | **BORDERLINE — accurate scoring, poor consumer communication** |
| Category-specific calorie density | **PASS — already implemented via calorie tier routing** |

**Overall verdict: The scoring engine discriminates correctly. The display layer misrepresents the discrimination. These are two separate problems.**
