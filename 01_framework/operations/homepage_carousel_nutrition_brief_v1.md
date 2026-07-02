# Homepage Carousel - Nutrition Brief v1

**Author:** Nutrition Agent
**Date:** 2026-06-27
**Status:** DRAFT - requires Content Agent authoring + Adversarial QA sign-off before any string reaches the owner
**Data sources:** bari-web/src/data/comparisons/ frontend JSON files (read 2026-06-27). Every number cited has file + field provenance.

---

## 0. Current Carousel - Verified Issues

| Card ID | Issue | Severity |
|---|---|---|
| snack-bars-report | Stat says 14 products - snacks_frontend_v5.json shows categoryTotal: 21 | HIGH - factually wrong |
| dairy-vs-plant | Right-product score coded as 67 - actual score for the soy milk is 63.9 | MEDIUM - score discrepancy |
| bread-investigation | States 32 products, grade S through D - bread_frontend_v3.json has 29 products; lowest grade is C/57.6, no D or E | MEDIUM - stale count, grade range overstated |
| protein-products | Finding cites 26 products - source not traceable to any current comparison file | LOW - unverified stat |


## 1. Recommended 8 Carousel Slots

Ranked by educational impact and user surprise factor.

| Slot | Archetype | Category (Hebrew) | Nutrition Hook | Priority |
|---|---|---|---|---|
| 1 | comparison | granola | 36.7-point gap; 9.6g vs 25g sugar in same category | Tier 1 |
| 2 | comparison | breakfast cereals | 44.5-point gap; 4.2g vs 29.9g sugar; 3 synthetic dyes | Tier 1 |
| 3 | comparison | granola snack bars | Oat-and-honey label: 3% honey, white sugar position 2, 341mg sodium | Tier 1 |
| 4 | comparison | milk and alternatives | 1 ingredient vs 4% almonds + sugar position 2; 35.3-point gap | Tier 1 |
| 5 | investigation | bread | Two 100%-whole-wheat breads - 28.7-point gap reveals emulsifier architecture | Tier 2 |
| 6 | investigation | granola / snacks | Flagship ingredient is smallest: quinoa 2.9%, honey 2.1%, honey 3% | Tier 2 |
| 7 | category-report | breakfast cereals | 44.5-point spread across 20 products; confirmed synthetic dyes | Tier 2 |
| 8 | methodology | methodology | Why two 100%-whole-wheat labels score differently - 8 signals | Tier 3 |


---

## 2. Comparison Pairs - Verified Data

### Slot 1 - Granola: Sugar Architecture Gap

Source: granola_frontend_v2.json (.expansion.nutrition, .score, .grade, .rank)

LEFT PRODUCT
- Name: granola cranberries and almonds
- Hebrew name: granola hamuziyot v'shkedim
- Brand: Dani v'Galit
- Score: 69.7 / Grade: B / Rank: 1 of 22
- Sugar per 100g: 9.6g
- Added sugar sources: 0 (sweetened by apple juice concentrate only)
- Fiber per 100g: 14.5g -- SEE CAVEAT BELOW
- Sodium per 100g: 10mg
- D4 additives: none

RIGHT PRODUCT
- Name: rich granola
- Hebrew name: granola ashira
- Brand: Penina Rosenblum
- Score: 33.0 / Grade: E / Rank: 20 of 22
- Sugar per 100g: 25g
- Added sugar sources: 2 -- white sugar + isoglucose (fructose-glucose syrup)
- Fiber per 100g: 5.7g
- Sodium per 100g: 195mg
- D4 additive: E220 sulfite preservative (dose-dependent tier)

Score gap: 36.7 points (verified)

FIBER CAVEAT (mandatory copy constraint): The B product's 14.5g fiber includes added chicory inulin. The published insightLine confirms "a significant portion comes from added chicory." Any copy using this fiber figure must add: "including added chicory fiber."

Hebrew copy draft [DRAFT - Content + AQA sign-off required]:
- Title suggestion: "The gap inside granola"
- Tradeoff suggestion: "9.6g sugar vs 25g -- same category, 37-point gap"
- NOTE: Do not use the word for 'healthy' in Hebrew. Frame as label/score data only.

---

### Slot 2 - Cereals: Widest Verified Gap in the Dataset

Source: cereals_frontend_v2.json (.expansion.nutrition, .score, .grade, .rank, .insightLine)

LEFT PRODUCT
- Name: Weetabix
- Score: 74.7 / Grade: B / Rank: 1 of 20
- Sugar per 100g: 4.2g
- Fiber per 100g: 10g
- Wheat content: 95%
- Synthetic dyes: 0

RIGHT PRODUCT
- Name: Trix (children's cereal)
- Score: 30.2 / Grade: E / Rank: 20 of 20
- Sugar per 100g: 29.9g
- Synthetic dyes: 3 -- E110 Orange Yellow, E122 Carmoisine, E129 Allura Red

Score gap: 44.5 points (verified) -- highest verified gap across all categories in this corpus.

Educational value: Both are mass-market products on the same breakfast cereal shelf. The gap is not specialty vs mainstream. Three synthetic dyes in a children's product is high-salience for parents.

Hebrew copy draft [DRAFT]:
- Title suggestion: "Top and bottom of breakfast"
- Tradeoff suggestion: "4.2g sugar vs 30g -- 44-point gap between shelf neighbors"


---

### Slot 3 - Snacks: Oat-and-Honey Name Gap

Source: snacks_frontend_v5.json (data confidence: verified for both products via .confidence field)

LEFT PRODUCT
- Name: FREE Dates and Cinnamon bar
- Brand: FREE
- Score: 66.8 / Grade: B / Rank: 1 of 21
- Hero ingredient: medjool date paste at 8%
- Ingredient order: cereals 45%, chicory fiber, medjool date paste (8%), walnut, cashew, glycerol, date syrup, cinnamon 0.7%
- Sugar per 100g: 9.9g (all from dates/date syrup)
- Fiber per 100g: 22.9g (includes chicory fiber -- see copy caveat)
- Sodium per 100g: 24mg
- D4 additives: 0

RIGHT PRODUCT
- Name: Oat bar with honey (Nature Valley)
- Brand: Nature Valley
- Score: 34.6 / Grade: E / Rank: 6 of 21
- Hero ingredient: honey at 3% only
- Ingredient order: whole oats 60%, WHITE SUGAR (position 2), vegetable oils, water, honey (3%), salt, molasses, lecithin, baking soda
- Sugar per 100g: 26.8g
- Fiber per 100g: 6.4g
- Sodium per 100g: 341mg
- D4 additives: 2 (E322 lecithin -- functional; E500 baking soda -- functional)

Score gap: 32.2 points (verified)

The story: "Oat and honey" is an architectural claim, not a composition description. Honey is 3% by weight; white sugar precedes it at position 2 in the ingredient list. The sodium (341mg/100g) is high for a product positioned as a sweet snack.

Fiber caveat: FREE's 22.9g fiber includes added chicory. Do not characterize as whole-food fiber in copy.

Hebrew copy draft [DRAFT]:
- Title suggestion: "Oat and honey"
- Tradeoff suggestion: "Honey is 3% -- white sugar is ingredient #2. 341mg sodium in a bar sold as sweet and simple."

---

### Slot 4 - Milk: Formula Complexity Gap

Source: milk_frontend_v1.json (.score, .grade, .expansion.ingredients)

LEFT PRODUCT
- Name: whole milk (Tnuva)
- Score: 85 / Grade: A
- Ingredients: 1 -- milk only

RIGHT PRODUCT
- Name: almond drink Alternative (Tnuva)
- Score: 49.7 / Grade: D
- Hero ingredient: almonds at 4% only
- Sugar: position 2 in ingredient list
- Additives: stabilizers (confirmed from file)

Score gap: 35.3 points (verified from milk_frontend_v1.json)

Educational value: Same brand, same shelf, same unit format. The almond drink is 4% almonds -- the rest is water, sugar, and additives. This directly answers the consumer question about plant-based substitution.

Hebrew copy draft [DRAFT]:
- Title suggestion: "Same shelf, two different worlds"
- Tradeoff suggestion: "Whole milk: one ingredient. Almond drink: 4% almonds, sugar in position 2."


---

## 3. Editorial Slots - Verified Finding Data

### Slot 5 - Investigation: Bread - Same Claim, Different Score

Source: bread_frontend_v3.json (.score, .grade, .expansion.nutrition, .expansion.ingredients, .insightLine, .d4_additives)

ANCHOR PRODUCT (S grade)
- Name: green bread whole wheat flour (lahm yarok mikamach male)
- Score: 92.7 / Grade: S
- Whole wheat claim: 100%
- Protein per 100g: 12.6g
- Fiber per 100g: 6.4g
- Sodium per 100g: 382mg
- Additives: 1 -- E300 ascorbic acid (functional tier)

COMPARISON PRODUCT (C grade)
- Name: Angel whole wheat bread (lahm Angel chita mele'a)
- Score: 64.0 / Grade: C
- Whole wheat claim: 100%
- Protein per 100g: 13.9g (HIGHER than anchor)
- Fiber per 100g: 8g (HIGHER than anchor)
- Sodium per 100g: 352mg (LOWER than anchor)
- Additives: 3 emulsifiers -- E481 SSL (likely-neutral), E472e DATEM (likely-neutral), E471 mono-diglycerides (CONTESTED tier)

Score gap: 28.7 points (verified)

The counterintuitive finding: The C product has better macros on paper (more protein, more fiber, lower sodium) yet scores 28.7 points lower. The score reads the additive architecture -- three emulsifiers including E471 (contested tier). This is the most powerful illustration of what Bari measures that a nutrition label does not show.

BREAD CORPUS NOTE: The 29-product bread corpus contains NO D or E grade products. Range is S(94.8) to C(57.6). The current carousel card stating "grade S through D" is factually incorrect.

Hebrew copy draft [DRAFT]:
- Eyebrow: "100% whole wheat -- two meanings"
- Finding: "Both declare 100% whole wheat flour. Grade S vs C. The difference: three different emulsifiers in the ingredient list."
- Stat suggestion: { value: "28.7", label: "point gap on the same flour declaration" }

---

### Slot 6 - Investigation: The Name-Gap Pattern

Source: granola_frontend_v2.json and snacks_frontend_v5.json

Three verified instances where the ingredient that names the product is the smallest by weight:

PRODUCT 1: granola chocolate quinoa (Nestle Fitness)
- Name ingredient: quinoa
- Actual percentage: 2.9%
- Score: 39.8 / Grade: D
- Sugar precedes quinoa (sugar is position 2)
- Source field: granola_frontend_v2.json .insightLine + .expansion.ingredients

PRODUCT 2: honey fitness granola (Nestle Fitness)  
- Name ingredient: honey
- Actual percentage: 2.1%
- Score: 39.2 / Grade: D
- Sugar precedes honey (sugar is position 3; glucose syrup also present before honey)
- Source field: granola_frontend_v2.json .insightLine + .expansion.ingredients

PRODUCT 3: oat bar with honey (Nature Valley)
- Name ingredient: honey
- Actual percentage: 3%
- Score: 34.6 / Grade: E
- White sugar precedes honey (position 2)
- Source field: snacks_frontend_v5.json .expansion.ingredients (confidence: verified)

All three are D or E grade. In all three cases, a sugar or sugar derivative precedes the hero ingredient.

Hebrew copy draft [DRAFT]:
- Eyebrow: "What the name promises"
- Finding: "Quinoa = 2.9%, honey = 2.1%, honey = 3% -- in three different products, the headline ingredient is the smallest in the list."
- Stat suggestion: { value: "2.1%", label: "the honey in Honey Fitness Granola" }


---

### Slot 7 - Category Report: Cereals

Source: cereals_frontend_v2.json

Verified stats:
- Products in corpus: 20 (from scored_count: 20)
- Score spread: 44.5 points (74.7 to 30.2)
- Top product: Weetabix -- 74.7/B
- Bottom product: Trix -- 30.2/E
- Sugar range: 4.2g (top) to 29.9g (bottom) per 100g
- Synthetic dyes confirmed in Trix: 3 dyes (E110, E122, E129)

UNVERIFIED CLAIM REQUIRING FIX: The current carousel card states "15% of products have synthetic food dyes" (= 3 of 20 products). Only Trix was confirmed in this session. The 15% figure needs verification across the full 20-product corpus before publishing.

Hebrew copy draft [DRAFT]:
- Eyebrow: "Breakfast cereals"
- Finding: "44 points between the top and bottom -- same shelf, two different architectures."
- Stat suggestion: { value: "44.5", label: "point gap between B and E on the breakfast cereal shelf" }

---

### Slot 8 - Methodology

Source: bread finding from Slot 5 (verified data)

Anchor: Two "100% whole wheat" labels, 28.7 points apart. Use as the concrete example to explain that Bari reads processing architecture -- specifically additive depth -- not just macros. The C product actually has better macros on paper; the score tells a deeper story.

Hebrew copy draft [DRAFT]:
- Eyebrow: "How Bari calculates"
- Finding: "Two breads, both 100% whole wheat, grade S vs C -- because Bari measures processing architecture, not just declarations."

---

## 4. Category Summary Cards

One verified striking statistic per scored category (reference for copy and future cards).

BREAD (bread_frontend_v3.json, 29 products, score range S/94.8 to C/57.6)
- Key fact: NO D or E products in the current corpus.
- Striking stat: Two "100% whole wheat" breads are 28.7 points apart (S vs C) due to emulsifier count alone.
- Note for copy: The strength of the bread corpus is its top-end concentration. Framing should be about architecture quality, not fear.

GRANOLA (granola_frontend_v2.json, 22 products, score range B/69.7 to E/33.0)
- Striking stat: 25g sugar at E vs 9.6g at B; 195mg sodium at E vs 10mg at B; 2 added sugar sources at E vs 0 at B.
- Secondary stat: Score spread is 36.7 points within a single food category.

BREAKFAST CEREALS (cereals_frontend_v2.json, 20 products, score range B/74.7 to E/30.2)
- Striking stat: 44.5-point spread -- widest verified gap in the corpus. Sugar gap: 4.2g (B) vs 29.9g (E).
- Secondary stat: At least 1 product with 3 synthetic dyes (E110, E122, E129) confirmed.

GRANOLA SNACK BARS (snacks_frontend_v5.json, 21 products, score range B/66.8 to E, bottom unconfirmed below rank 6)
- Striking stat: Rank 1 -- 22.9g fiber, 24mg sodium, 0 additives. Rank 6 -- 26.8g sugar, 341mg sodium. Same "granola bar" shelf.
- Secondary stat: Name gap documented (honey = 3% in a bar with "honey" in the name).

MILK AND ALTERNATIVES (milk_frontend_v1.json, score range A/85 to E/31.5)
- Striking stat: Same brand -- 1-ingredient whole milk scores A(85); almond drink with 4% almonds, sugar position 2, scores D(49.7).
- Secondary stat: 35.3-point gap between A and D within a single aisle.

---

## 5. Copy Constraints Checklist

All carousel copy must pass these constraints before sign-off.

Rule 1: No use of the Hebrew word for "healthy" (bari/varid) -- absolute rule.
Rule 2: No health claims -- Bari scores architecture, not diet or health outcomes.
Rule 3: No internal taxonomy in consumer copy -- do not use BSIP, NOVA, structural_class, cap, floor.
Rule 4: Transparency framing only -- all copy presents label data as fact, not editorial verdict.
Rule 5: Data-grounded only -- no invented values, no approximations, cite exact figures from the label.

Violation examples and corrections:
- "The healthiest granola" -> "The granola with the highest score"
- "Helps maintain healthy weight" -> "Contains 4.2g sugar per 100g per label"
- "BSIP2 score" -> "The score is based on the nutrition panel and ingredient list"
- "A dangerous product" -> "Per label: white sugar is ingredient 2, honey is 3%"
- "About 20g sugar" -> "26.8g sugar per 100g (verified label data)"

NOTE: All Hebrew draft copy in this brief requires Content Agent authoring and Adversarial QA sign-off before any string is shown to the owner or goes live. This is a mandatory two-gate process per the 2026-06-20 owner ruling.


---

## 6. Red Flags

### RF-1 -- Stale snack count (HIGH)
Location: current live card snack-bars-report
Issue: States 14 products -- actual categoryTotal in snacks_frontend_v5.json is 21.
Risk: Any fraction expressed as "X of 14" in copy is factually wrong. Seven products are invisible to users.
Data trace: snacks_frontend_v5.json field categoryTotal: 21, confirmed in product objects for both rank-1 and rank-6 products.
Fix: Update stat to 21. This is a data correction -- no content sign-off needed.

### RF-2 -- Score discrepancy in dairy card (MEDIUM)
Location: current live card dairy-vs-plant
Issue: Right product (soy milk) score coded as 67 -- actual score in milk_frontend_v1.json is 63.9.
Risk: Published score is inflated by 3.1 points.
Fix: Update to 63.9. Data correction -- no content sign-off needed.

### RF-3 -- Bread grade range overstated (MEDIUM)
Location: current live card bread-investigation
Issue: States "grade S through D" -- no D or E products exist in the current 29-product bread corpus.
Risk: Overstates severity of scoring variation in the bread category.
Data trace: bread_frontend_v3.json -- lowest grade observed is C (score 57.6). No D or E products found in full file scan (lines 1-2133 read).
Fix: Correct to "grade S through C" and update product count from 32 to 29.

### RF-4 -- Fiber stat needs context in Slots 1 and 3 (LOW-MEDIUM)
Location: Slot 1 (granola B product) and Slot 3 (snack bars B product)
Issue: Slot 1 B product has 14.5g fiber partly from added chicory. Slot 3 B product has 22.9g fiber partly from chicory.
Both are real figures from the label, but represent industrial added fiber, not whole-grain fiber.
Risk: Copy celebrating "14g fiber" or "23g fiber" without source context could mislead about fiber quality.
Data trace: granola_frontend_v2.json insightLine for rank-1: "a significant portion comes from added chicory." snacks_frontend_v5.json expansion.ingredients for rank-1: "chicory dietary fiber" listed explicitly.
Fix: Any copy referencing these fiber figures must note the chicory source.

### RF-5 -- Cereals sodium stat needs product-name verification (LOW)
Location: Category summary for cereals
Issue: A cereal product with 435mg sodium per 100g was identified in a prior session but was not re-confirmed with product name in this session.
Risk: Publishing "435mg sodium" without a confirmed current product name if the product was updated or re-ranked.
Fix: Before publishing any sodium stat for cereals, confirm product name and sodium value in the current cereals_frontend_v2.json via direct product lookup.

### RF-6 -- Snack sodium framing must stay transparent (LOW)
Location: Slot 3 (new comparison card)
Issue: 341mg sodium per 100g in the honey oat bar is a striking figure. Calling it "high sodium" would be an editorial health claim, not a data statement.
Risk: Implicit health verdict rather than transparent data presentation.
Fix: Present as label fact only: "341mg sodium per 100g per label." No health framing.

---

## 7. Implementation Order

Step 1 - Immediate data corrections (no sign-off needed):
  - Fix RF-1: snack count 14 -> 21 in snack-bars-report card
  - Fix RF-2: soy milk score 67 -> 63.9 in dairy-vs-plant card
  - Fix RF-3: bread grade range "S through D" -> "S through C", count 32 -> 29 in bread-investigation card

Step 2 - Tier 1 comparison cards (Slots 1-4):
  - Data fully verified. Route to Content Agent for Hebrew copy authoring.
  - Then Adversarial QA gate before any owner-facing review.

Step 3 - Tier 2 editorial cards (Slots 5-6):
  - Data verified. Route to Content Agent after Tier 1 is approved.
  - Slot 5 (bread investigation) should link to or replace the current bread-investigation card.

Step 4 - Updated category-report (Slot 7):
  - Replaces stale cereals-report. Requires: verify "15% synthetic dyes" claim against full 20-product corpus before publishing.

Step 5 - Methodology card (Slot 8):
  - Update from current bari-methodology card once bread anchor example passes sign-off.

---

## 8. Data Provenance Summary

All scores and nutritional values cited in this brief are sourced directly from production frontend JSON files.
No nutritional values were invented or estimated.
Files read: bread_frontend_v3.json, granola_frontend_v2.json, cereals_frontend_v2.json, snacks_frontend_v5.json, milk_frontend_v1.json
Fields used: score, grade, rank, categoryTotal, expansion.nutrition, expansion.ingredients, insightLine, d4_additives[].tier, d4_additives[].e_number, confidence
Read date: 2026-06-27
