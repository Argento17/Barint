# Milk & Alternatives — Golden Corpus Candidates

**Created:** 2026-05-17  
**Purpose:** Identify 10–15 strategically important products for the first BSIP2 validation pass

These are not simply good examples of each product type. They are chosen because each one is likely to reveal something specific about how BSIP2 handles a structural challenge. An ideal golden product either confirms the system works correctly or visibly breaks it.

---

## Selection criteria

A product qualifies as a golden candidate if:
1. It sits at a structural edge — near the boundary of what BSIP2 can distinguish
2. It creates a scoring tension that has no obvious resolution
3. It is adversarial — it can be made to look better than it is through nutrient arithmetic
4. It represents a category that is likely to be common on shelves

---

## Recommended golden corpus (13 products)

---

### G01 — Whole Dairy Milk (3.5% fat)

**Type:** Intact dairy, full-fat  
**Strategic role:** Anchor reference. The most structurally complete product in the category.

If BSIP2 scores this below an ultra-processed plant drink, the system is fundamentally miscalibrated. Its score defines the floor for "structurally coherent beverage."

**Expected BSIP2 score:** High  
**Risk:** Penalized for saturated fat content — may score lower than fortified plant milks that avoid sat-fat  
**What to watch:** Does saturated fat penalty overwhelm matrix integrity and protein quality?

---

### G02 — Unsweetened Plain Soy Milk

**Type:** Plant milk, complete protein, no added sugar  
**Strategic role:** Best-case plant milk reference.

The only plant milk with a protein quality comparable to dairy. If BSIP2 cannot distinguish this from almond milk or oat milk on protein quality, the protein logic is flat.

**Expected BSIP2 score:** High  
**Risk:** May score the same as structurally inferior plant milks if protein source is not tracked  
**What to watch:** Does the system credit intact soy protein differently from isolate-enriched oat milk?

---

### G03 — Ultra-Low-Calorie Unsweetened Almond Milk (~13 kcal/100ml)

**Type:** Structural emptiness case  
**Strategic role:** Primary stress test for the hollow product problem.

This product is almost entirely water with trace almonds, minerals, and vitamins. It avoids every negative. A naive BSIP2 will score it high. A correct BSIP2 will recognize it as nutritionally void.

**Expected BSIP2 score:** Should be low — but likely to score falsely high  
**Risk:** Avoids sugar penalty, fat penalty, calorie penalty, HFSS threshold. Passes everything.  
**What to watch:** Does any mechanism detect that this product has almost no nutritional substance?

**This is the most important product in the golden corpus.**

---

### G04 — Fortified Oat Milk (calcium + vitamin D added)

**Type:** Fortification paradox case  
**Strategic role:** Tests whether fortification inflates the score.

This product contains 120mg calcium/100ml and vitamin D because they were added in. The nutrient panel looks like dairy milk's micronutrient profile. The food structure is oat extract + water.

**Expected BSIP2 score:** Should be moderate — will likely score high due to micronutrient profile  
**Risk:** Micronutrient fortification games the system into treating it as nutritionally complete  
**What to watch:** Does the system distinguish fortified from intrinsic micronutrients?

---

### G05 — Barista Oat Milk

**Type:** Engineering stress test  
**Strategic role:** Tests how BSIP2 handles added oils and emulsifier systems.

Barista oat milk adds rapeseed oil and lecithin (and sometimes acidity regulators) to standard oat milk. The caloric density increases by 30–50% over standard oat milk. The product is designed for processing, not nutrition.

**Expected BSIP2 score:** Should be penalized for oil addition and emulsifier load  
**Risk:** May not be penalized if fat quality is acceptable and total fat per 100ml stays moderate  
**What to watch:** Does BSIP2 detect added oils in the ingredient list? Does it penalize the processing-designed profile?

---

### G06 — Chocolate Dairy Milk

**Type:** Hyper-palatability in intact matrix  
**Strategic role:** Tests whether palatability engineering is penalized when the base food is nutritionally coherent.

The base is dairy milk (intact matrix, complete protein, calcium). Sugar and cocoa have been added. This is a different problem from chocolate oat milk — here the base food is real.

**Expected BSIP2 score:** Should be modestly penalized for added sugar and palatability  
**Risk:** High matrix quality may offset the sugar and flavoring penalty entirely  
**What to watch:** Can BSIP2 distinguish "good base food with bad additions" from "poor base food with bad additions"?

---

### G07 — High-Protein Dairy Milk (4–5g protein/100ml)

**Type:** Engineered intact dairy  
**Strategic role:** Tests whether protein enrichment on a strong base is correctly recognized.

This product starts from an intact dairy matrix and concentrates or supplements the protein content. Unlike isolate-enriched plant milks, the protein here is still dairy-sourced.

**Expected BSIP2 score:** High  
**Risk:** May score the same as isolate-enriched almond milk (inflated protein score without matrix quality difference)  
**What to watch:** Does source of protein enrichment matter in the score?

---

### G08 — "Protein Almond Milk" (pea protein isolate added)

**Type:** Isolate on hollow base  
**Strategic role:** Direct comparison to G07.

An almond milk base (structurally empty) with pea protein isolate added to reach 4–5g protein/100ml. Same protein gram count as G07. Completely different food structure.

**Expected BSIP2 score:** Should be lower than G07 (inferior matrix and protein source)  
**Risk:** Will likely score identically or higher than G07 if protein grams are the primary signal  
**What to watch:** This pair (G07 vs G08) is one of the cleanest tests of whether BSIP2 can distinguish protein quality.

---

### G09 — Sweetened Kids Milk Drink (flavored UHT carton)

**Type:** Palatability + target demographic mismatch  
**Strategic role:** Tests whether BSIP2 identifies products whose marketing and formulation diverge.

These products are designed to get children to drink more liquid. They contain added sugar, flavoring, and sometimes thickeners. The per-100ml nutrition looks acceptable. The absolute consumption context is not.

**Expected BSIP2 score:** Should be penalized for sugar and palatability engineering  
**Risk:** Per-100ml numbers may not trigger HFSS thresholds; no mechanism to flag target demographic concern  
**What to watch:** Does the scoring system have any sensitivity to product context beyond per-100ml arithmetic?

---

### G10 — Sweetened Oat Milk (mainstream shelf variant)

**Type:** Most common plant milk on shelf  
**Strategic role:** Baseline for what a "normal" plant milk should score.

This is what most consumers buy when they pick up oat milk. It has added sugar (typically 4–6g/100ml) and a relatively low protein level (0.5–1g/100ml). Its score should be moderate — not excellent, not terrible.

**Expected BSIP2 score:** Moderate  
**Risk:** May score too high (low fat, low calorie, no strong negatives) or too low (sugar penalty dominates)  
**What to watch:** Does the score feel calibrated against whole dairy milk (G01) and ultra-low-cal almond milk (G03)?

---

### G11 — Rice Milk

**Type:** High glycemic, minimal nutrition  
**Strategic role:** Tests carbohydrate quality handling in beverages.

Rice milk is high in simple carbohydrates, low in protein, low in fat. It has a high glycemic response. Nutritionally, it is weak relative to any dairy or soy reference point.

**Expected BSIP2 score:** Low-moderate  
**Risk:** May avoid penalties because per-100ml sugar is not always high (natural rice starch rather than added sugar) while protein is simply absent  
**What to watch:** Does absence of protein trigger a penalty, or only presence of sugar?

---

### G12 — "No Sugar Added" Vanilla Almond Milk with Stevia

**Type:** Sweetener handling edge case  
**Strategic role:** Tests whether non-caloric sweetener is treated differently from added sugar.

This product avoids sucrose but contains a sweet flavoring (vanilla) plus a non-caloric sweetener (steviol glycosides). It markets as "no sugar added." BSIP2 must not treat this as equivalent to truly unsweetened almond milk.

**Expected BSIP2 score:** Should be penalized for sweetener + flavoring, less than sweetened variant  
**Risk:** Avoids sugar penalty entirely; stevia may not trigger any current penalty path  
**What to watch:** Is there any mechanism to distinguish `no sugar added + sweetener` from `genuinely unsweetened`?

---

### G13 — Chocolate Soy Milk

**Type:** Palatability + complete protein  
**Strategic role:** The hardest trade-off case in the corpus.

Soy milk has the best protein profile of any plant milk. Chocolate soy milk adds sugar and cocoa to that strong base. This is a product where the base food is excellent and the additions are problematic. How does BSIP2 balance these?

**Expected BSIP2 score:** Moderate — should be penalized for palatability but credited for protein quality  
**Risk:** Either the soy protein credit overwhelms the sugar penalty (scores too high) or the sugar penalty overwhelms the protein credit (scores too low)  
**What to watch:** Can BSIP2 produce a nuanced score that reflects the trade-off?

---

## Priority order for first manual test

| Priority | Product | Reason |
|---|---|---|
| 1 | G03 — Ultra-low-cal almond milk | Most likely to expose structural emptiness failure |
| 2 | G08 — Protein almond milk (isolate) | Cleanest protein quality test |
| 3 | G07 — High-protein dairy milk | G08 comparison anchor |
| 4 | G01 — Whole dairy milk | Global anchor — sets the scale |
| 5 | G04 — Fortified oat milk | Fortification paradox test |
| 6 | G05 — Barista oat milk | Oil + emulsifier detection |
| 7 | G02 — Unsweetened soy milk | Best-case plant milk reference |
| 8 | G13 — Chocolate soy milk | Trade-off complexity |
| 9 | G12 — Vanilla almond milk with stevia | Sweetener taxonomy |
| 10 | G10 — Sweetened oat milk | Mainstream baseline |

The first three (G03, G08, G07) should be run before any others. Together they define whether BSIP2 can reason about protein quality and structural density. If it cannot distinguish G07 from G08 and cannot score G03 appropriately, the remaining tests will not add diagnostic value — they will just accumulate examples of the same underlying failure.

---

## What a failure looks like

The corpus has exposed a BSIP2 failure if any of the following is true:

- G03 (ultra-low-cal almond milk) scores above G01 (whole dairy milk)
- G08 (isolate-enriched almond milk) scores above G02 (unsweetened soy milk) on protein dimension
- G04 (fortified oat milk) and G01 (whole dairy milk) score identically on micronutrient dimension
- G12 (sweetened with stevia) and unsweetened plain almond milk score identically
- G05 (barista oat milk) scores above plain oat milk despite added oils
- G09 (kids sweetened milk drink) scores above moderate on any dimension related to quality

Any one of these outcomes indicates a BSIP2 scoring path that does not distinguish food structure from nutrient arithmetic.
