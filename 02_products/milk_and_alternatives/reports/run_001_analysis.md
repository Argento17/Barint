# Milk & Alternatives — BSIP2 Run 001 Analysis

**Run date:** 2026-05-17  
**Products scored:** 8  
**Pipeline errors:** 0  
**Architecture version:** bsip2_concept_v1 + score_resolution_contract_SRC-v1  
**Purpose:** Observational run — no fixes applied. Raw BSIP2 behavior documented as-is.

---

## Score Summary

| Product | Score | Grade | Category | NOVA | SE Gate | Cap |
|---------|-------|-------|----------|------|---------|-----|
| חלב מלא 3.5% (Whole dairy milk) | **75** | **B** | dairy_protein | 1 | No | — (floor 75) |
| חלב עשיר בחלבון 6% (High-protein dairy) | **71.2** | **B** | dairy_protein | 2 | No | — |
| משקה סויה ללא סוכר (Unsweetened soy milk) | **61.4** | **C** | beverage | 3 | No | 75 |
| משקה שקדים עשיר בחלבון (Protein almond) | **58.5** | **C** | beverage | 3 | No | 70 |
| חלב שוקולד ממותק (Chocolate dairy milk) | **49.4** | **D** | dairy_protein | 4 | No | 60 |
| משקה שקדים ללא סוכר (Ultra-low-cal almond) | **45.9** | **D** | beverage | 3 | **YES** | 75 |
| משקה שיבולת שועל ברסיטה (Barista oat milk) | **44.6** | **D** | beverage | 3 | No | 65 |
| משקה שיבולת שועל ללא תוספת סוכר (No-sugar-added oat) | **44.3** | **D** | beverage | 4 | No | 60 |

---

## Dimension Score Matrix

| Product | proc | nutdens | caldens | glyc | prot | add | sat | fat | reg | wfi |
|---------|------|---------|---------|------|------|-----|-----|-----|-----|-----|
| Whole dairy milk | 95 | 10.4 | 90 | 78.0 | 16.0 | 100 | 60.0 | 77.7 | 95 | 100 |
| High-protein dairy | 80 | 19.5 | 90 | 77.0 | 30.0 | 100 | 100 | 82.3 | 95 | 80 |
| Unsweetened soy | 55 | 12.5 | 70 | 88.8 | 16.5 | 82 | 99.2 | 94.9 | 95 | 50 |
| Protein almond | 55 | 13.1 | 70 | 89.8 | 14.9 | 49 | 100 | 98.0 | 95 | 50 |
| Chocolate dairy | 25 | 9.8 | 90 | 66.2 | 15.0 | 64 | 48.6 | 79.2 | 95 | 20 |
| Ultra-low-cal almond | 55 | 2.7 | **50*** | 90.5 | 2.0 | 64 | 25.6 | **50*** | 95 | 50 |
| Barista oat | 55 | 6.0 | 50† | 81.4 | 5.5 | 46 | 38.9 | 86.6 | 95 | 50 |
| No-sugar-added oat | 25 | 3.7 | 70 | 89.8 | 3.0 | 31 | 34.4 | 95.8 | 95 | 20 |

*SE gate applied (SRC-04): dimension capped at 50  
†70 kcal/100ml sits exactly at the beverage table boundary → score=50

---

## Four Mandatory Comparisons

---

### Comparison A: Whole Dairy Milk vs Ultra-Low-Cal Almond Milk

| Metric | Whole dairy (75, B) | Ultra-low-cal almond (45.9, D) |
|--------|---------------------|-------------------------------|
| Score | 75 | 45.9 |
| Grade | B | D |
| Score gap | **29.1 points** | |
| Category | dairy_protein | beverage |
| NOVA | 1 | 3 |
| SE gate | Not triggered | **Triggered** |
| Structural emptiness conditions | — | kcal<20 ✓, prot<3 ✓, fiber<1.5 ✓, fat<2 ✓, add≥2 ✓ |
| processing_quality | 95 | 55 |
| calorie_density | 90 | **50** (SE cap) |
| protein_quality | 16.0 | 2.0 |
| nutrient_density | 10.4 | 2.7 |
| fat_quality | 77.7 | **50** (SE cap) |
| additive_quality | 100 | 64 |
| Floor applied | nova1_single_ingredient → 75 | None |

**Dominant penalties for almond:** SE gate caps calorie_density and fat_quality at 50. NOVA 3 reduces processing_quality from 95→55 and wfi from 100→50. Near-zero protein and fiber collapse nutrient_density (2.7) and protein_quality (2.0).

**Score gap without SE gate:** Without SE, almond milk calorie_density = 85 (13 kcal → beverage table tier 2) and fat_quality ≈ 97.5 (very low sat fat). This would add ~9.1 points, raising almond milk from 45.9 → ~55. It would still lose to dairy (75), but at a smaller gap and higher grade (C vs B). **The SE gate is correctly preventing a false positive.**

**Architecture verdict:** CORRECT direction, CORRECT outcome. Dairy milk clearly outscores an empty almond drink. The SE gate is the key mechanism that prevents structural emptiness from being rewarded.

**Intuitive correctness:** High. A product that is 98% water should not score in the C range. 45.9 (D) is a reasonable position for a nutritionally hollow product.

**Gameable?** Partially — without the SE gate, it would move to C. The SE gate protects against this specific exploit, but the gate requires 2+ additive markers to trigger. An almond milk with only 1 additive marker category would NOT trigger the gate.

---

### Comparison B: High-Protein Dairy Milk vs Protein-Enriched Almond Milk

| Metric | High-protein dairy (71.2, B) | Protein almond (58.5, C) |
|--------|------------------------------|--------------------------|
| Score | 71.2 | 58.5 |
| Grade | B | C |
| Score gap | **12.7 points** | |
| Protein | 6.0g/100ml | 3.5g/100ml |
| Protein source | whole_food (intact dairy) | mixed (pea protein isolate) |
| Source factor (sf) | 1.0 | 0.85 |
| protein_quality score | 30.0 | 14.9 |
| protein_quality gap | **15.1 points** | |
| processing_quality | 80 (NOVA 2) | 55 (NOVA 3) |
| additive_quality | 100 | 49 (sweetener −15 + additive category) |
| satiety_support | 100 | 100 |
| NOVA | 2 | 3 |
| Sweetener | None | Stevia (E-960) |

**Why dairy wins:**
1. **Protein volume + quality**: 6.0g intact dairy protein vs 3.5g pea isolate. Both the gram count AND the source factor (1.0 vs 0.85) contribute to the protein_quality gap (30.0 vs 14.9 — 15 points).
2. **Processing**: NOVA 2 vs NOVA 3 (processing_quality: 80 vs 55, wfi: 80 vs 50).
3. **Additive quality**: Dairy has 0 additive categories → 100. Almond isolate has thickener + sweetener → additive_quality = 49.

**Protein source penalty quantified:** The isolate penalty (sf 1.0→0.85) on 3.5g protein reduces protein_quality from 17.5 to 14.9 — a 2.6-point reduction in the protein_quality dimension, which translates to 0.26 points on the final score (weight=0.10). **The protein quality distinction is correctly directional but dimensionally weak** — the real separation comes from the additive and processing dimensions, not protein quality itself.

**Architecture verdict:** PARTIALLY CORRECT. The right product wins by the right margin. However, the protein source distinction contributes less than 1 point to the final score. If the only difference between two products were 3.5g whole-food protein vs 3.5g isolate protein, the gap would be ~2.6 points — barely perceptible. The architecture detects protein quality differences but under-weights them relative to their food-structure significance.

**Intuitive correctness:** Moderate. 71.2 vs 58.5 feels about right. The specific drivers (additive quality, sweetener) are correct even if the protein quality signal is weak.

**Gameable?** Yes. A product builder could add enough pea protein isolate to reach 6g/100ml while keeping NOVA 3, and would close much of the gap with intact dairy protein products — primarily limited by additive penalties, not protein quality.

---

### Comparison C: Unsweetened Soy Milk vs Barista Oat Milk

| Metric | Unsweetened soy (61.4, C) | Barista oat (44.6, D) |
|--------|---------------------------|----------------------|
| Score | 61.4 | 44.6 |
| Grade | C | D |
| Score gap | **16.8 points** | |
| protein_quality | 16.5 | 5.5 |
| additive_quality | 82 | 46 |
| satiety_support | 99.2 | 38.9 |
| calorie_density | 70 | 50 |
| Additive categories | 1 (stabilizer) | 3 (thickener + stabilizer + acidity_regulator) |
| Seed oil | None | שמן קנולה (rapeseed) |
| Binding cap | 75 (NOVA 3) | 65 (ADDITIVE_MARKERS_3_PLUS) |
| SEED_OIL_PRESENT penalty | None | −3 points |

**Why soy wins:**
1. **Satiety**: soy protein (3.3g) drives satiety_support to 99.2. Barista oat protein (1.1g) only reaches 38.9.
2. **Additives**: Barista oat has 3 additive categories (thickener from E461/E412, stabilizer from E412, acidity_regulator from E330/חומצה ציטרית) → cap lowered to 65, additive_quality=46. Soy has 1 additive category → additive_quality=82.
3. **Seed oil**: Rapeseed oil in barista oat → SEED_OIL_PRESENT penalty (−3 points) + fat_quality reduction.
4. **Calorie density**: Oat milk at 70 kcal hits the beverage table boundary exactly → score=50. Soy at 33 kcal → score=70.

**Architecture verdict:** CORRECT. The barista oat's engineering (added oil, 3 additive systems) is correctly penalized. Soy's protein advantage is correctly captured. The 16.8-point gap feels architecturally sound.

**Intuitive correctness:** High. An unsweetened plain soy milk (whole soybean base, one additive) should clearly score better than an oil-enriched oat milk engineered for foam performance.

**Gameable?** Limited. The barista oat penalties are real structural signals (the oil and additive systems are in the product). A product engineer couldn't remove these without changing the product's functional properties.

---

### Comparison D: Barista Oat Milk vs No-Sugar-Added Oat Beverage (Sweetener)

| Metric | Barista oat (44.6, D) | No-sugar-added oat (44.3, D) |
|--------|----------------------|-------------------------------|
| Score | 44.6 | 44.3 |
| Grade | D | D |
| Score gap | **0.3 points** | |
| NOVA | 3 | 4 |
| processing_quality | 55 | 25 |
| Sweetener | None | Stevia (E-960) |
| Flavor engineering | None | חומרי טעם וריח (ווניל) |
| additive_quality | 46 | 31 |
| Binding cap | 65 (ADDITIVE_3_PLUS) | 60 (NOVA_4) |
| Seed oil | Yes | No |
| fat_quality | 86.6 | 95.8 |

**The failure mode:** Two structurally different products score identically (44.6 vs 44.3 — within measurement noise). The barista oat milk is worse because of its oil system and 3-additive-category load. The no-sugar-added oat beverage is worse because of NOVA 4 classification (flavor engineering + sweetener) and lower processing/wfi scores. These two failure paths happen to cancel out, producing nearly identical final scores.

**What BSIP2 cannot distinguish:** The difference between "naturally low sugar in a plain drink" and "no sugar added because a sweetener was substituted." The sweetener penalty appears in additive_quality (−15 from sw_pen) and causes NOVA 4 classification (boosted by flavor_enhancer score), but these penalties are absorbed by other dimensions moving in the opposite direction (better fat_quality without seed oil, better glycemic_quality without sugar).

**Critical test for sweetener taxonomy (Comparison D as specified):** The brief asked for "plain unsweetened vs no-sugar-added sweetened version." The closest available pair within this corpus is:
- **Unsweetened soy milk (61.4, C)** — genuinely unsweetened, no sweetener, intact protein
- **No-sugar-added oat beverage (44.3, D)** — stevia sweetener, flavor engineering, NOVA 4

The gap here is 17.1 points (C vs D), which BSIP2 gets correct — but for the wrong reasons. The gap comes primarily from NOVA (soy=3 vs oat=4), protein content (soy=3.3g vs oat=0.6g), and additive load. The sweetener itself contributes only ~3-4 points of the total gap. **BSIP2 correctly ranks them but cannot cleanly isolate the sweetener penalty as a standalone signal.**

**Architecture verdict:** FAILED for the sweetener comparison within same base food. Passed for cross-product ranking. The sweetener signal is present but buried under other dimensions — it cannot distinguish "no sugar added" from "genuinely unsweetened" when other parameters are similar.

---

## 1. Products That Scored Surprisingly High

**Protein-enriched almond milk: 58.5 (C)**

This is 3.5g of pea protein isolate dissolved in water with stevia and thickeners. It beats barista oat milk (44.6), ultra-low-cal almond milk (45.9), and chocolate dairy milk (49.4). The score of 58.5 may be defensible but the reasoning reveals a gap: **BSIP2 sees 3.5g protein and rewards it proportionally, without adequately interrogating the food structure that protein sits in**. A product builder could engineer a similar score with any isolate in any aqueous base.

---

## 2. Products That Scored Surprisingly Low

**Whole dairy milk: 75 (B) — score represents a floor, not earned position**

The natural pre-floor score was ~68.8, driven down primarily by `nutrient_density=10.4` — the lowest dimension. The reason: nutrient_density is scored on protein + fiber, and whole dairy milk has zero dietary fiber. A score of 10.4 on nutrient density is the same zone as ultra-processed snack bars. **BSIP2 does not credit dairy's intact food matrix, naturally-occurring vitamins, or bioavailable minerals.** The NOVA 1 floor rescues the score to 75, but the rescue is a policy mechanism, not a structural one. The natural score without the floor would be B only because of the floor, not because of intrinsic dimension quality.

**The dairy milk floor dependency is a structural flaw:** Remove the floor and dairy milk's natural score (68.8) is only 7 points above unsweetened soy milk (61.4) — a difference that feels too small given how fundamentally different these products are.

---

## 3. Structural Emptiness — Did It Emerge?

**Yes — on exactly the product it was designed for.**

Ultra-low-cal almond milk (13 kcal/100ml) triggered the SE gate:
- cond_kcal: 13 < 20 (beverage threshold) ✓
- cond_prot: 0.4 < 3.0 ✓
- cond_fiber: 0.4 < 1.5 ✓
- cond_fat: 1.1 < 2.0 ✓
- cond_eng: 2 additive categories ≥ 2 ✓

**Effect of SE gate:** calorie_density capped at 50 (without gate: would be 85, a top-tier beverage score). fat_quality capped at 50 (without gate: would be ~97.5). **Total SE-prevented inflation: ~9.1 points.** Without the gate, almond milk would score ~55 (C), which would be architecturally indefensible.

**SE gate limitation:** The gate requires 2+ additive categories as an "engineered signal" condition. An almond milk with only 1 additive category (e.g., only one stabilizer type) would NOT trigger the gate, and would score ~55 (C). The gate is correct when it fires but can be evaded by minimalist formulation.

---

## 4. Did Isolate-Enriched Products Exploit Satiety Logic?

**Partially — but the exploit is bounded.**

Protein-enriched almond milk (3.5g pea isolate) scored satiety_support=100 (capped). This is the same satiety score as high-protein dairy milk (6.0g intact protein). The satiety formula is:

```
(protein × 3 + fiber × 5) / max(50, kcal) × 400
```

For protein almond: (3.5×3 + 0.5×5)/max(50,35)×400 = 13/50×400 = 104 → capped at 100.

**The liquid satiety problem:** This formula produces a satiety_support of 100 for a beverage with 35 kcal/100ml and 3.5g protein. A solid snack bar with 350 kcal and equivalent macros would score much lower on satiety_support (350 kcal denominator). **BSIP2 inadvertently rewards low-calorie beverages with any protein content for "satiety" — which contradicts the established physiology of liquid nutrition.** A 250ml glass of protein almond milk delivers 87.5g protein (actually 8.75g protein, 87.5 kcal) and a satiety_support score of 100. This is not what 100/100 satiety means for a solid food.

**The exploit:** A manufacturer could add 3.5g pea isolate to any aqueous base, claim satiety_support=100, and the score would reflect this. The satiety logic is completely blind to the liquid vs solid distinction.

---

## 5. Did Fortification Distort Results?

**Not significantly in this run — but only because fortification is invisible to BSIP2.**

All plant milks in this corpus are fortified with calcium, vitamin D, and B12 (in the ingredients list). BSIP2 currently has no mechanism to read or reward/penalize micronutrient content. The regulatory_quality score is based purely on Israeli red labels (sugar, sat fat, sodium thresholds) — it does not credit calcium or vitamin D.

**Implication:** Fortification neither helps nor hurts a product's BSIP2 score in the current architecture. This means the fortification paradox (hollow almond milk scoring well because of calcium fortification) cannot occur yet — but only because BSIP2 has no micronutrient dimension at all. When a micronutrient dimension is added in a future version, the fortification paradox will immediately become a live risk.

---

## 6. Did Liquid Products Cluster Unnaturally?

**Partially.** The beverage-category products cluster in a narrow range (44.3–61.4) while dairy_protein products span a wider range (49.4–75.0).

The key issue is that beverage calorie density scoring puts most plant milks in the 33–70 kcal range where the beverage table scores them 50–70 — a compressed range. This creates artificial clustering in the middle of the scoring range for beverages. Compare:
- 13 kcal → calorie_density=50 (SE gate)
- 33 kcal → calorie_density=70
- 35 kcal → calorie_density=70
- 70 kcal → calorie_density=50 (boundary)

The beverage calorie density table heavily rewards the 25-45 kcal range (scores 70-85) but penalizes both lower (SE gate) and the 70 kcal boundary. This creates a non-intuitive "sweet spot" for beverages at moderate calorie density.

---

## 7. Did Beverage Products Expose Category Instability?

**Yes — two products raised instability flags.**

Barista oat milk and no-sugar-added oat beverage both contain "שיבולת שועל" (oats) in the product name. The cereal classifier picks up "שיבולת שועל" at 0.8 weight while the beverage classifier picks up "משקה" at 0.9 weight. The delta (0.1) is below the instability threshold (0.3), and category confidence is below 0.80 → both products flag as category-unstable.

```
Barista oat: beverage(0.9+hint) vs cereal(0.8) → delta=0.1 → INSTABILITY FLAG
No-sugar-added oat: same pattern → INSTABILITY FLAG
```

This is a real architectural signal. Oat beverages sit ambiguously between "beverage" and "cereal" because oats are a cereal grain. The category classifier was not designed for this case. If either product were classified as "cereal" instead of "beverage," its calorie_density score would change significantly (different lookup table) and the score could shift by 10-15 points.

---

## 8. Which Assumptions Failed First?

**Ranked by severity:**

### Failure 1: Dairy matrix advantage is not captured (CRITICAL)
Whole dairy milk's natural score before the floor is 68.8, driven down by nutrient_density=10.4 because fiber=0. BSIP2 cannot distinguish an intact biological food matrix (dairy milk with native fat globules, casein micelles, naturally-occurring vitamins) from a reconstructed formulation. The NOVA 1 floor (75) saves the score as a policy commitment, but the policy is compensating for a missing structural dimension, not reflecting real food quality.

### Failure 2: Protein source distinction is dimensionally weak (SIGNIFICANT)
The protein_quality dimension correctly applies source factors (whole_food=1.0, mixed=0.85) but the magnitude is insufficient. Moving from intact whole-food protein to pea isolate reduces protein_quality score by only ~2.6 points at 3.5g protein. This is less than the SEED_OIL_PRESENT penalty (3 points) for a single seed oil. Protein source quality is a more fundamental food structure distinction than the presence of one seed oil, but BSIP2 treats it less severely.

### Failure 3: Liquid satiety logic is uncorrected (SIGNIFICANT)
Any product with modest protein in a low-calorie liquid base scores satiety_support=100. This is physiologically incorrect for beverages. A 250ml serving of protein almond milk should not earn the same satiety credit as 250g of a solid food with equivalent macros.

### Failure 4: Sweetener taxonomy cannot distinguish "no sugar added" from "genuinely unsweetened" when other parameters match (MODERATE)
The 0.3-point gap between barista oat (44.6) and no-sugar-added oat (44.3) demonstrates that BSIP2 cannot use the sweetener signal as a meaningful standalone differentiator. The sweetener penalty is real but absorbed by other dimensional differences.

### Failure 5: Oat beverage category instability (MODERATE)
Both oat products have instability flags due to the beverage/cereal ambiguity. This is a genuine architectural gap: oat-based beverages do not fit cleanly into either category, and the category choice significantly affects calorie_density scoring.

---

## Most Dangerous Observed Failure Mode

**The protein isolate scoring exploit.**

The protein-enriched almond milk (pea isolate + water + thickener + stevia) scored 58.5 — 12.7 points below high-protein dairy milk (71.2), but only **2.9 points below unsweetened soy milk (61.4)**.

Soy milk contains intact soybeans at 7.4%, a complete protein source, with natural fat, fiber, and minimal processing. The protein-enriched almond milk contains 1.5% almonds in water with extracted pea protein isolate, thickeners, and an artificial sweetener.

These two products are not nutritionally comparable. BSIP2 scores them 2.9 apart.

The mechanism: pea isolate receives a source penalty (sf=0.85) but still produces protein_quality=14.9 vs soy's 16.5. The gap is 1.6 points on protein_quality, which translates to 0.16 points on the final score (weight=0.10). The remaining 2.73-point gap comes from additive and processing differences, not food structure.

**The practical implication:** A product developer who adds pea isolate to water can score within 3 points of a genuine whole-food plant milk. The current architecture cannot block this route to a C grade.

---

## Strongest Architectural Success

**Structural emptiness gate on ultra-low-cal almond milk.**

The SE gate correctly identified that 13 kcal/100ml, 0.4g protein, 0.4g fiber, and 1.1g fat in a water base represents structural emptiness. It capped calorie_density at 50 and fat_quality at 50, preventing ~9 points of false inflation.

Without the gate, ultra-low-cal almond milk would score ~55 (C), which is indefensible — a C grade for a product that is 98% water with trace almonds. With the gate, it scores 45.9 (D), which correctly places it below both soy milk (61.4) and even chocolate dairy milk (49.4) — a product with real nutritional payload despite added sugar and NOVA 4 processing.

**The gate is clean:** It fires on quantitative conditions (all 5 must be true), it produces a specific documented effect (cap at 50 on two dimensions), and it does not distort other dimensions. This is the most architecturally sound guardrail in the current system for this category.

---

## 9. Recommendation: Unified, Modifier, or Split?

**Recommendation: Add a product_form modifier. Do NOT split.**

### Evidence from this run:

| Issue | Unified fix possible? | Modifier needed? | Requires split? |
|-------|----------------------|------------------|-----------------|
| Liquid satiety discount | No | **Yes** (satiety_support discount for liquids) | No |
| Oat beverage category instability | Partly (better classifier) | Yes (liquid gate improvement) | No |
| Dairy matrix deficit | No | Possibly (WFI dimension for intact matrix) | No |
| Protein source underweighted | Partly (increase sf penalty) | No | No |
| Sweetener taxonomy gap | Partly (add separate sweetener signal) | No | No |
| SE gate evasion (1 additive cat) | Partly (lower cond_eng threshold) | No | No |

None of the identified failures require fundamentally incompatible logic between beverages and solids. They require conditional adjustments to specific dimensions when `product_form == liquid`.

### Proposed modifier structure:
```python
if product_form == "liquid":
    satiety_support *= LIQUID_SATIETY_DISCOUNT  # ~0.6
    # calorie_density table already category-conditioned (beverage table exists)
    # se gate threshold already category-conditioned (SE_BEVERAGE_KCAL)
```

The calorie density and SE gate are already conditioned on category (beverage category uses different table and threshold). The only missing liquid-specific adjustment is the satiety discount.

**Threshold for splitting:** If more than 3 dimensions require fundamentally incompatible logic (not just scaled differently) between liquid and solid forms, split. We are currently at 1 (satiety). Do not split yet.

---

## 10. Recommended Next Category After Milk & Alternatives

**Recommendation: Fermented dairy products (yogurt, kefir, labneh).**

### Why:
1. **Fermentation benefit not captured** — BSIP2 has a `has_fermentation` signal in L3 but it is not connected to any scoring dimension. Yogurt is the natural test for whether fermentation is rewarded.
2. **Protein quality at different processing levels** — Greek yogurt (strained, concentrated protein) vs regular yogurt vs flavored yogurt mirrors the protein quality questions in milk.
3. **Sugar complexity** — plain yogurt has natural lactose. Flavored yogurt adds sucrose. Fruit yogurt has both lactose and fruit sugar. The SC classification system was built for solid foods and may misfire on fermented dairy.
4. **Red label stress test** — full-fat labneh may trigger sat_fat red label. This tests floor-cap interaction on NOVA 1-2 whole foods (same mechanism as dairy milk, but more severe fat content).
5. **Shared category infrastructure** — uses dairy_protein category (already validated in this run). No new infrastructure required.

**Alternative candidate: Breakfast cereals.** The cereal category is the most common NOVA 4 food type in Israeli supermarkets. It would stress-test hyper-palatability detection (HP_CRUNCH_SWEET_COMBO), which is not tested by milk or snack bars.

**Deferred: Chocolate and confectionery.** Too simple — everything scores E. No interesting architectural questions.

---

## Summary of Run 001 Findings

| Finding | Type | Severity |
|---------|------|---------|
| SE gate correctly fires on 13 kcal almond milk | Architectural success | — |
| Dairy matrix quality invisible to scoring (fiber=0 → nutrient_density=10.4) | Structural gap | HIGH |
| Protein isolate within 3 points of intact whole-food plant milk | Scoring exploit | HIGH |
| Liquid satiety always 100 for any protein-containing beverage | Logic error | SIGNIFICANT |
| Oat beverages flagged with category instability | Classification gap | MODERATE |
| Sweetener indistinguishable from "genuinely unsweetened" at same baseline | Taxonomy gap | MODERATE |
| Chocolate dairy milk (NOVA 4) correctly penalized despite intact matrix | Correct behavior | — |
| High-protein dairy correctly outscores pea isolate almond by 12.7 pts | Correct behavior | — |
| Unsweetened soy correctly outscores barista oat by 16.8 pts | Correct behavior | — |
