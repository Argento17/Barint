# BSIP2 Breakfast Cereals — run_cereals_001 Analysis Report

**Generated:** 2026-05-18 18:35 UTC
**Corpus:** breakfast_cereals (n=45, Yohananof scrape, 65 raw observations → 45 canonical)
**Framework:** BSIP2 v2 grade calibration (same constants as run_004_recalibrated)
**Purpose:** Stress-test BSIP2 against extrusion, fortification, fiber laundering,
granola density, kids cereals, protein engineering, hyper-palatability.

---

## 1. Corpus Summary

**Total canonical products:** 45
**Source:** Yohananof (real retailer scrape, single-source corpus)

**Subtype distribution:**

| Subtype | n  | Mean Score | Range     | Grade Distribution                  |
|---------|----|------------|-----------|-------------------------------------|
| unknown | 45 | 61.8       | 30.0–90.7 | S:1 | A:7 | B:11 | C:17 | D:4 | E:5 |

---

## 2. Grade Distribution

| Grade | Count | Pct |
|-------|-------|-----|
| S     | 1     | 2%  |
| A     | 7     | 16% |
| B     | 11    | 24% |
| C     | 17    | 38% |
| D     | 4     | 9%  |
| E     | 5     | 11% |


---

## 3. Full BSIP2 Leaderboard

| Product                                       | Score | Grade | Subtype | Category (⚠=misclassified?) | NOVA | Cap |
|-----------------------------------------------|-------|-------|---------|-----------------------------|------|-----|
| סובין שיבולת שועל 400 גרם                     | 90.7  | S     | unknown | cereal                      | 1    | —   |
| שיבולת שועל גלגולה קוואקר 500 גרם             | 85.4  | A     | unknown | cereal                      | 1    | —   |
| פתיתי כוסמין מלא 500 גרם                      | 85    | A     | unknown | cereal                      | 1    | —   |
| שיבולת שועל מהירה קוואקר 500 גרם              | 85.0  | A     | unknown | cereal                      | 1    | —   |
| שיבולת שועל גרוסה ספרוגרן 500 גרם             | 85.0  | A     | unknown | cereal                      | 1    | —   |
| שיבולת שועל מלאה תלמה 500 גרם                 | 85    | A     | unknown | cereal                      | 1    | —   |
| קורנפלקס אורגני ביו 300 גרם                   | 85    | A     | unknown | cereal                      | 1    | —   |
| בסיס שיבולת שועל לילה עם זרעי צ'יה ופשתן 400  | 81.1  | A     | unknown | cereal                      | 2    | —   |
| גרנולה זרעים עם שמן זית ודבש 350 גרם          | 75.8  | B     | unknown | whole_food_fat              | 3    | 82  |
| וויטביקס דגני בוקר חיטה מלאה 430 גרם          | 75.6  | B     | unknown | cereal                      | 3    | 82  |
| דגני בוקר פצפוצי חיטה מלאה 375 גרם            | 74.9  | B     | unknown | cereal                      | 3    | 82  |
| מוסלי בירכר בסיס 500 גרם                      | 74.3  | B     | unknown | snack_bar_granola           | 2    | —   |
| מוסלי פירות ואגוזים 500 גרם                   | 73.1  | B     | unknown | whole_food_fat              | 3    | 82  |
| דגני בוקר פתיתי דגנים מלאים מעורבים 375 גרם   | 73.0  | B     | unknown | cereal                      | 3    | 82  |
| מוסלי שוויצרי קלאסי 500 גרם                   | 70.8  | B     | unknown | snack_bar_granola           | 3    | 82  |
| דגני בוקר אול-בראן פתיתי סובין קלוגס 375 גרם  | 70.4  | B     | unknown | cereal                      | 3    | 72  |
| גרנולה דייטס ללא תוספת סוכר 400 גרם           | 69.2  | B     | unknown | whole_food_fat              | 3    | 82  |
| דייסת שיבולת שועל מיידית בטעם וניל קוואקר 340 | 69.0  | B     | unknown | cereal                      | 3    | 82  |
| דגני בוקר פתיתי סובין קלוגס 375 גרם           | 68.8  | B     | unknown | cereal                      | 3    | 72  |
| קורנפלקס קלוגס 375 גרם                        | 64.8  | C     | unknown | cereal                      | 3    | 82  |
| דגני בוקר חלבון מקסימום 27 גרם חלבון 300 גרם  | 64.1  | C     | unknown | cereal                      | 4    | 68  |
| קורנפלקס תלמה 500 גרם                         | 63.9  | C     | unknown | cereal                      | 3    | 82  |
| דגני בוקר ספשל K חלבון קלוגס 320 גרם          | 63.8  | C     | unknown | cereal                      | 4    | 68  |
| דגני בוקר פיטנס חלבון נסטלה 320 גרם           | 63.0  | C     | unknown | cereal                      | 4    | 68  |
| דגני בוקר ספשל K קלוגס 375 גרם                | 62.5  | C     | unknown | cereal                      | 3    | 82  |
| קורנפלקס נסטלה 375 גרם                        | 60.4  | C     | unknown | cereal                      | 3    | 72  |
| קורנפלקס דגנים מלאים קלוגס 375 גרם            | 58.0  | C     | unknown | snack_bar_granola           | 3    | 72  |
| גרנולה חלבון עם חלבון מי גבינה 350 גרם        | 58.0  | C     | unknown | dairy_protein               | 4    | 68  |
| דייסת שיבולת שועל מיידית בטעם דבש קוואקר 340  | 55.0  | C     | unknown | cereal                      | 3    | 55  |
| דגני בוקר צ'יריוס דבש ואגוזים 375 גרם         | 52.0  | C     | unknown | whole_food_fat              | 3    | 55  |
| דגני בוקר ספשל K פירות אדומים קלוגס 375 גרם   | 52.0  | C     | unknown | cereal                      | 3    | 55  |
| גרנולה פצפוצים פריכים עם דבש ואגוזים 400 גרם  | 52.0  | C     | unknown | whole_food_fat              | 3    | 55  |
| דגני בוקר שוקו-פיק נסטלה 375 גרם              | 52.0  | C     | unknown | cereal                      | 3    | 55  |
| דגני בוקר פיטנס שוקולד נסטלה 375 גרם          | 52.0  | C     | unknown | snack_bar_granola           | 3    | 55  |
| גרנולה קלאסטרס קלוגס 400 גרם                  | 51.2  | C     | unknown | snack_bar_granola           | 3    | 55  |
| דגני בוקר פיטנס נסטלה 375 גרם                 | 51.2  | C     | unknown | snack_bar_granola           | 3    | 72  |
| גרנולה עם אגוזים ודבש טבעי 400 גרם            | 47.0  | D     | unknown | whole_food_fat              | 3    | 55  |
| גרנולה עם חמוציות 400 גרם                     | 45.0  | D     | unknown | whole_food_fat              | 3    | 55  |
| דגני בוקר סמאקס דבש קלוגס 330 גרם             | 37.2  | D     | unknown | cereal                      | 4    | 55  |
| דגני בוקר טבעות שוקולד תלמה 375 גרם           | 36.5  | D     | unknown | cereal                      | 4    | 55  |
| דגני בוקר פרוט לופס קלוגס 375 גרם             | 33.3  | E     | unknown | cereal                      | 4    | 55  |
| גרנולה עם שבבי שוקולד 400 גרם                 | 33.0  | E     | unknown | snack_bar_granola           | 3    | 45  |
| דגני בוקר נסקוויק כדורי שוקולד נסטלה 375 גרם  | 32.8  | E     | unknown | cereal                      | 4    | 55  |
| דגני בוקר קוקו פופס קלוגס 375 גרם             | 31.8  | E     | unknown | cereal                      | 4    | 55  |
| דגני בוקר לייון נסטלה 400 גרם                 | 30.0  | E     | unknown | cereal                      | 4    | 45  |

---

## 4. Architectural Stress-Test — 10 Key Questions

### Q1: Do 'healthy cereals' collapse correctly?

**Answer: PARTIALLY.**

- Nestlé Fitness Original: C (51.2) — correct. Classified as snack_bar_granola (from 'פיטנס' + ingredient signal), NOVA 3 cap=72 binding.
- Nestlé Fitness Chocolate: C (52.0) — correct. NOVA 3 + red label sugar (18.5g > 17.5g) → cap=55.
- Kellogg's Special K Original: C (62.5) — **questionable**. Special K has 17g sugar, 13.5g protein, high sodium (570mg).
  Scoring as C feels slightly generous — sodium just below red label threshold (600mg).
- Special K Red Berries: C (52.0) — correct. Red label sugar (18.5g) + flavor enhancer → cap=55.

**Finding:** Fitness/Special K products correctly land in C but the sodium near-miss
(570 vs 600mg threshold) means a 30mg difference creates a 10+ point scoring swing.
This cliff at 600mg sodium is a calibration concern for 'near-threshold' fortified cereals.

### Q2: Does Bari over-credit fortification?

**Answer: YES — CONFIRMED ARCHITECTURAL WEAKNESS.**

Fortification creates an **additive blindspot**:
- Vitamins listed as names (ויטמין B1, B2, B6, ניאצין, חומצה פולית) → **0 additive categories detected**.
- Vitamins listed as E-numbers (E-300) → triggers antioxidant AND flour_treatment → **2 additive categories**.

**Impact measured:**
- Kellogg's Cornflakes (vitamins by name): additive_ct=0 → additive_quality=100/100
- Nestlé Cornflakes (includes E-300): additive_ct=2 → additive_quality=64/100, cap=72 applied
- Kellogg's Cornflakes scores 64.8 (C, near-B) vs Nestlé 60.4 (C) — not because of real quality difference,
  but because labeling convention triggers different NOVA signals.

**Consequence:** A cornflakes product fortified with 8 vitamins, all listed by Hebrew name,
looks IDENTICAL to an unfortified product from the signal extractor's perspective.
BSIP2 cannot distinguish fortification from whole-food nutrition.

**Recommended fix:** Add a fortification detection layer:
- Detect vitamin/mineral name clusters (ויטמין B1 + B2 + B6 + ניאצין = fortification signal)
- Apply a moderate NOVA boost signal (not full additive) for detected fortification packages

### Q3: Does fiber laundering exist?

**Answer: YES — MOST SIGNIFICANT FINDING.**

All-Bran (28g fiber/100g) scored **B (70.4)**. Let's trace why:

- Glycemic quality formula: 90 − (16g sugar × 2.5) + (28g fiber × 2.0) + 0 = 90 − 40 + 56 = **106 → capped at 100**
- 28g fiber produces maximum glycemic quality (100) despite 16g added sugar (close to red label)
- Glycemic quality weight is 0.12 → this contributes 12.0 pts to the score
- Satiety support: (12×3 + 28×5) / 318 × 400 = 221 → **capped at 100** → contributes 6.0 pts

**The laundering mechanism:** The fiber bonus is uncapped within the glycemic formula.
At 28g fiber, even very high sugar content (16g) cannot produce a negative glycemic score.
All-Bran with 16g sugar and 28g fiber scores identically on glycemic quality to
plain oats with 1g sugar and 10g fiber — this is incorrect.

**Note:** All-Bran IS a NOVA 3 product with ADDITIVE_MARKERS_3_PLUS cap at 72.
The cap protects against runaway scores. But the natural score (77+) before cap is inflated.

**Recommended fix:** Apply a fiber-laundering discount when:
- sugar_g > 12 AND fiber_g > 15 AND the fiber is from bran/isolated sources (not whole food)
- Consider capping fiber_bonus at (sugar_g × 1.5) to prevent fiber from fully laundering sugar

### Q4: How harsh is extrusion pressure?

**Answer: MODERATE — EXTRUSION PRESSURE IS WELL-CALIBRATED BUT INCONSISTENT.**

Extruded products (cornflakes, puffed cereals) land in C (60–65):
- Kellogg's Cornflakes: 64.8 (C) — NOVA 3, no red labels, 8g sugar
- Telma Cornflakes: 63.9 (C) — similar profile
- Nestlé Cornflakes: 60.4 (C) — E-300 triggers 2 additive categories → cap=72

The extrusion pressure manifests through:
1. NOVA 3 classification → processing_quality = 65 (vs 95 for NOVA 1)
2. NOVA 3 cap at 82 (rarely binding for cornflakes at natural score ~65)
3. Nutrient density penalty: cornflakes protein (7g) scores ~35/100 on the protein formula

**Inconsistency found:** Organic cornflakes (single ingredient, 100% corn) scores A (85).
This is the NOVA 1 floor. A mechanically extruded corn product at 373 kcal, 84g carbs,
7g protein receiving A grade feels architecturally generous. The single-ingredient NOVA 1
floor was designed for whole-food fats (nuts, seeds), not for extruded corn products.

**The extrusion gap:** NOVA 1 floor (85) for single-ingredient extruded corn vs C (64) for
multi-ingredient cornflakes with vitamins — a 21-point spread for essentially the same product.

### Q5: Do granolas become unfairly punished?

**Answer: CLASSIFICATION CHAOS — MORE COMPLEX THAN PUNISHMENT.**

6 of 8 granola products were NOT classified as snack_bar_granola or cereal:

| Product | Expected | Actual | Score | Grade |
|---------|---------|--------|-------|-------|
| Honey-nuts granola | snack_bar | whole_food_fat | 47.0 | D |
| Chocolate granola | snack_bar | snack_bar | 33.0 | E |
| Protein granola | snack_bar | dairy_protein | 58.0 | C |
| Date granola | snack_bar | whole_food_fat | 69.2 | B |
| Cranberry granola | snack_bar | whole_food_fat | 45.0 | D |
| Crunchy cluster granola | snack_bar | whole_food_fat | 52.0 | C |
| Seeds granola | snack_bar | whole_food_fat | 75.8 | B |
| Kellogg's granola clusters | snack_bar | snack_bar | 51.2 | C |

**Root cause:** Products containing nuts ('שקדים', 'אגוזים', 'אגוזי לוז') trigger
whole_food_fat signals (0.7 weight) that compete with snack_bar_granola signals.
Seeds granola also contains 'שמן זית' (olive oil, 0.95 whole_food_fat signal).
Protein granola's 'חלבון מי גבינה' (whey protein) triggers dairy_protein classification.

**Consequence of misclassification:**
- whole_food_fat: calorie density at 450 kcal → 45 pts (table calibrated for oils/nuts)
  vs snack_bar: same product → 25 pts → **20-point swing from table alone**
- whole_food_fat products escape SNACK_BAR_HIGH_CAL (70 cap) and SNACK_BAR_RED_SUGAR (55 cap)
- Seeds granola at 75.8 (B) would likely score ~45 (D) if correctly classified as snack_bar

**Finding:** Granola scoring is currently **lottery-based on classification**.
Natural language signals in product names create unstable, large-swing category assignments.

### Q6: Do protein cereals exploit the architecture?

**Answer: PARTIALLY — HIGH PROTEIN BUYS LIMITED BUT REAL CREDIT.**

| Product | Score | Grade | Protein | Sweetener | Cap |
|---------|-------|-------|---------|-----------|-----|
| Special K Protein | 63.8 | C | 20g | No | 68 (NOVA4) |
| Fitness Protein | 63.0 | C | 18g | Yes | 68 (NOVA4) |
| Generic Protein (Syntech) | 64.1 | C | 22g | Yes | 68 (NOVA4) |

Protein cereals with sweeteners hit the SWEETENER_CAP (70) independently.
The NOVA 4 cap (68) binds first. Net result: max score ~68 regardless of protein content.
The sweetener cap (70) is not the binding constraint here — NOVA4 at 68 is.

**The genuine exploitation:**
- protein_quality and nutrient_density dimensions both credit 20-22g protein heavily
- At 22g protein, nutrient_density ≈ 85+ pts (near-ceiling) × 0.15 weight = 12.75 pts
- This dimension credit PARTIALLY offsets the NOVA 4 processing penalty
- Without the NOVA 4 cap, a 22g protein product could score ~72+ (low B)

**Assessment:** The NOVA 4 cap at 68 is correctly preventing protein cereals from
escaping D/C territory. The sweetener cap provides a secondary barrier.
Current calibration is defensible but the C grade for engineered protein cereals
feels slightly permissive — they should likely be D.

### Q7: Do kids cereals correctly collapse?

**Answer: MOSTLY YES — WITH ONE NOTABLE EXCEPTION.**

| Product | Sugar | NOVA | Score | Grade | Cap |
|---------|-------|------|-------|-------|-----|
| Nestlé Lion | 28g | 4 | 30.0 | E | 45 |
| Kellogg's Coco Pops | 35g | 4 | 31.8 | E | 55 |
| Nestlé Nesquik | 36g | 4 | 32.8 | E | 55 |
| Kellogg's Froot Loops | 39g | 4 | 33.3 | E | 55 |
| Nestlé Chocapic | 26g | 3 | 52.0 | C | 55 |
| Kellogg's Smacks | 38g | 4 | 37.2 | D | 55 |
| Telma Choco Rings | 30g | 4 | 36.5 | D | 55 |
| Honey Nut Cheerios | 24g | 3 | 52.0 | C | 55 |

**High-sugar NOVA 4 kids cereals correctly land E.** The HP_CRUNCH_SWEET penalty fires
for cereal-category products with sugar >= 20g and fiber <= 3g: +5 pts at NOVA4 weight=1.0.

**Chocapic at C (52) is the notable exception.** 26g sugar, NOVA 3 (whole grain detected
from 'דגנים מלאים (חיטה מלאה 40%)' reduces NOVA from what should be 4).
The whole grain NOVA discount saves Chocapic from NOVA 4 classification despite
containing 'חומרי טעם וריח' (flavor compounds) — the score 3 from flavor_enhancer
minus 1 from whole_grain = 2, landing on NOVA 3 boundary instead of 4.

**Architectural tension:** Chocapic is 40% whole grain + flavor enhancers + 26g sugar.
NOVA 3 cap at 82 barely constrains it. The 55 cap comes from the red label sugar.
This is correct mechanically but Chocapic at C feels like it should be D.

### Q8: Does oatmeal emerge as structural anchor?

**Answer: YES — DECISIVELY. First S-tier product in the Bari system.**

| Product | Score | Grade | NOVA | Mechanism |
|---------|-------|-------|------|-----------|
| Oat Bran | **90.7** | **S** | 1 | Single ingredient, 17.3g protein, 15.4g fiber |
| Quaker Rolled Oats | 85.4 | A | 1 | Single ingredient, floor (natural ≈85.4) |
| Telma Oats | 85.0 | A | 1 | Floor (natural just at 85) |
| Quaker Quick Oats | 85.0 | A | 1 | Floor (natural just at 85) |
| Steel-Cut Oats | 85.0 | A | 1 | Floor (natural just at 85) |
| Overnight Oats Base | 81.1 | A | 2 | NOVA 2, clean ingredients, high fiber |
| Instant Oatmeal Vanilla | 69.0 | B | 3 | NOVA 3 (whole grain reduces NOVA4 score) |
| Instant Oatmeal Honey | 55.0 | C | 3 | Red label sugar (18.5g) → cap=55 |

**Oat bran (90.7) breaks the S-tier barrier.** At 246 kcal, 17.3g protein, 15.4g fiber,
1.5g sugar, single ingredient → NOVA 1 floor 85 was not binding. Natural score exceeded 90.

**The instant oatmeal divergence is architecturally revealing:**
- Vanilla instant oatmeal (16g sugar, 'ואניל' flavor signal): NOVA 3, score=69 (B)
- Honey instant oatmeal (18.5g sugar, 'חומרי טעם וריח'): NOVA 3, score=55 (C, capped)
The 2.5g sugar difference (16 vs 18.5) pushed honey oatmeal over the 17.5g red label
threshold. This is a cliff that doesn't reflect proportional product quality difference.

### Q9: Does Bari preserve meaningful differentiation inside cereals?

**Answer: YES — STRONG SPREAD WITH MEANINGFUL HIERARCHY.**

Score range: 30.0 (Lion cereal) to 90.7 (Oat bran) — **60.7 point spread.**

**Internal hierarchy preserved:**
- Pure whole food oats > muesli > whole grain cereals > cornflakes ≥ fitness cereals
- Clean granola (NOVA 2, no vanillin) > granola with additives
- Kids cereal collapse is steep and intentional

**Differentiation gaps found:**
- Chocapic (26g sugar kids cereal, 52) scores same as Seeds Granola (8g sugar, whole grain, 52ish)
  — these should NOT be equivalent
- Honey instant oatmeal (55) scores same as Kellogg's granola clusters (51) — very different products
- Vanilla instant oatmeal (69, B) vs Fitness Original (51, C) — questionable spread
  for products with similar processing levels

### Q10: Does the recalibrated distribution feel coherent?

**Answer: MOSTLY COHERENT — GRANOLA CHAOS AND CLASSIFICATION GAPS UNDERMINE IT.**

Grade distribution: S:1 | A:7 | B:11 | C:17 | D:4 | E:5

**What works:**
- S tier correctly has only one product (oat bran)
- A tier correctly has oats and overnight oats base
- E tier correctly has the worst kids cereals
- D tier is small and contains legitimately problematic products

**What doesn't work:**
- Seeds granola at B (75.8) is the same grade as Weetabix (75.6) — incoherent
  because seeds granola is whole_food_fat-classified, escaping snack_bar penalties
- Protein granola at C (58, dairy_protein-classified) vs cornflakes at C (64.8)
  — the protein granola actually has better nutrition but lower C
- The C tier is extremely crowded (38%): 17 products in 50–65 range
  Many of these are genuinely different quality levels


---

## 5. Major Architectural Observations

### O1: Fortification Blindspot (CONFIRMED WEAKNESS)
Vitamins listed by Hebrew name are invisible to the signal extractor. A product with
'ויטמין B1, B2, B6, ניאצין, חומצה פולית, ברזל' gets additive_quality=100, indistinguishable
from an unfortified product. This is the most significant gap exposed by cereals.

### O2: Fiber Laundering (CONFIRMED WEAKNESS)
The glycemic quality formula allows extreme fiber values (28g in All-Bran) to produce
a maximum glycemic score (100) despite substantial added sugar (16g). The fiber bonus
is uncapped relative to sugar content.

### O3: Granola Classification Instability (CONFIRMED WEAKNESS)
Nuts and seeds in product names/ingredients trigger whole_food_fat category signals.
This causes 6/8 granola products to escape snack_bar penalty caps (SNACK_BAR_HIGH_CAL,
SNACK_BAR_RED_SUGAR_LABEL). Seeds granola gains ~25+ points from misclassification alone.

### O4: Single-Ingredient NOVA1 Floor Scope Creep
The NOVA1_SINGLE_FLOOR (85) was calibrated for whole-food fats and dairy proteins.
Applied to extruded organic cornflakes (single ingredient, high-carb, low-protein),
it produces an A grade that conflicts with the architecture's intent.

### O5: Whole Grain NOVA Discount (EXPECTED — WELL-CALIBRATED)
The −1 NOVA4 score for whole grain presence correctly reduces NOVA classification
for borderline products (instant oatmeal, Chocapic). This is a known design choice
but may require a floor: 'whole grain + flavor enhancers' should never be NOVA 2.

### O6: HP_CRUNCH Pattern — Category-Specific Correctly
The HP_CRUNCH_SWEET penalty (sugar≥20g AND fiber≤3g, cereal category only) works
correctly for high-sugar cereal products. It fires appropriately for Coco Pops,
Nesquik, Froot Loops, Smacks at NOVA4 weight=1.0.
NOTE: Granola products misclassified as whole_food_fat **escape this penalty**,
which further inflates scores for misclassified products.


---

## 6. Biggest Surprises

1. **Oat bran breaking S-tier (90.7)** — First S-grade product in the Bari system.
   Not surprising in retrospect, but validates that S-tier is achievable.

2. **Organic cornflakes at A (85)** — The single-ingredient NOVA1 floor applies to extruded
   corn, giving it an A grade equivalent to pure rolled oats. This is architecturally
   inconsistent: 'קמח תירס מלא' (processed corn flour) ≠ 'שיבולת שועל' (whole rolled oats).

3. **Seeds granola at B (75.8)** — Near-equivalent to Weetabix (75.6). This is entirely
   an artifact of whole_food_fat misclassification and should be C or low-B at best.

4. **Vanilla instant oatmeal at B (69.0)** — A flavored, sugar-added, instant oatmeal
   scores B because: NOVA 3 (whole grain neutralizes flavor enhancer), sugar (16g) is
   below the 17.5g red label threshold. Feels too generous.

5. **Granola chocolate chips at E (33.0)** — Cap=45 from ISRAELI_RED_LABELS_2_PLUS
   (sugar + sat_fat both red labels). The double red label cap stacked with low natural
   score produces E. Correct punishment — but only because sat_fat was 5.5g > 5.0g.
   At 5.0g sat_fat, it would score C. A 0.5g sat_fat difference = 2+ grade shift.

6. **Cheerios misclassified as whole_food_fat (52, C)** — 'אגוזים' (nuts) in the product
   name triggered whole_food_fat classification. A kids cereal with 24g sugar scoring C
   as if it were an oil or nut product.


---

## 7. Products That Broke Assumptions

| Product | Score | Issue |
|---------|-------|-------|
| Oat Bran | 90.7 (S) | First S-tier. NOVA1 floor irrelevant — natural score already >90 |
| Organic Cornflakes | 85 (A) | NOVA1 single-ingredient floor for extruded corn — scope mismatch |
| Seeds Granola | 75.8 (B) | whole_food_fat misclassification inflating by ~25 pts |
| Date Granola | 69.2 (B) | Same misclassification — 'ריבת תמרים' triggers 'ריבה' sugar marker |
| All-Bran | 70.4 (B) | Fiber laundering: 28g fiber neutralizes 16g sugar |
| Vanilla Instant Oatmeal | 69.0 (B) | Flavored + sugar, but NOVA 3 via whole grain discount |
| Protein Granola | 58.0 (C) | dairy_protein misclassification from whey protein in name |
| Cheerios | 52.0 (C) | whole_food_fat misclassification from 'אגוזים' in name |
| Chocapic | 52.0 (C) | NOVA3 via whole grain discount saves heavily sugared kids cereal from D/E |


---

## 8. Recommended Next BSIP2 Refinements

### Priority 1: Fortification Detection Layer
Add a dedicated fortification signal extractor. Detect vitamin name clusters
(ויטמין B1/B2/B6 + ניאצין + ברזל = fortification signature) and apply a
moderate NOVA processing signal (not additive count, but a separate flag).
This will expose the quality difference between whole-food protein and spray-on vitamins.

### Priority 2: Fiber Laundering Cap
In the glycemic quality formula, cap the fiber_bonus at min(20, sugar_g × 1.2).
This prevents extreme bran fiber from fully laundering high added sugar.
A product with 28g fiber but 16g sugar should NOT score 100 on glycemic quality.

### Priority 3: Granola Category Signal Rebalancing
Add 'גרנולה' to category_classifier with name-only matching at higher weight.
Reduce interference from 'שקד', 'אגוז' in granola context by adding a conjunction
check: whole_food_fat signals only apply if there are no cereal/granola signals.
Alternatively, enforce: products with 'גרנולה' in name always → snack_bar_granola.

### Priority 4: NOVA1 Floor Scope Restriction
Restrict NOVA1_SINGLE_FLOOR (85) to products where kcal < 450 AND protein > 5g.
This excludes high-calorie, low-protein single-ingredient extruded products
(corn flour, rice flour) from the whole-food floor rescue.

### Priority 5: Whole Grain NOVA Discount Cap
Limit the whole grain −1 NOVA4 discount: if flavor_enhancer is detected,
the minimum NOVA level should be 3, not reducible to 2 by whole grain presence.
Formula: nova_level = max(3, computed_level) when flavor_enhancer is detected.

### Priority 6: Sodium Cliff Smoothing
The sodium red label at 600mg creates a binary cliff. Products at 570mg escape
entirely; at 610mg they get a 60-cap. Consider a graduated approach:
450–600mg: soft penalty; 600–750mg: current cap; >750mg: harsher cap.


---

## 9. Visuals

Generated in `visuals/`:
- `grade_utilization_cereals.png` — grade distribution bar chart
- `score_by_subtype_cereals.png` — score strip chart by subtype
- `leaderboard_cereals.png` — full 45-product leaderboard
- `subtype_comparison_cereals.png` — score range per subtype (mean + range)
- `category_confusion_cereals.png` — category classifier behaviour by subtype