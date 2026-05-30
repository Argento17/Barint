# Manual Trace Workshop — Results

**Date:** 2026-05-17
**Specification version:** bsip2_concept_v1
**Products traced:** 10
**Template:** validation/manual_trace_workshop_template.md

> This document records adversarial manual traces of 10 canonical products. The goal is to find contradictions while they are cheap to fix. Where the architecture produces absurd results, those are reported without defense.

---

## PRODUCT 1 — Plain Almonds

### Section A — Product Context

**Expected intuitive outcome:** Grade A. The canonical reference whole food. If almonds score poorly, the system is broken.

**Why adversarial:** Almonds are 580 kcal/100g — well above the threshold at which calorie-load rules begin to fire for snack bars. They contain 49g fat. The HIGH_CAL_LOW_SATIETY_SEVERE rule requires kcal≥500 AND protein<6g AND fiber<3g. Almonds have 21g protein and 12g fiber, so the rule does not fire — but only because both conditions happen to fail. If almond varieties with lower protein or fiber existed, the threshold interaction could produce unexpected results. The product is also fully dependent on correct `whole_food_fat` categorisation.

**Architectural tensions activated:**
- Category confidence (if miscategorised → catastrophic)
- Saturated fat dimension penalty on a whole food
- Whether the NOVA 1 floor is redundant here or load-bearing

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 580 kcal/100g
- Protein: 21g
- Total fat: 49g | Saturated fat: 3.7g
- Carbohydrates: 22g | Sugar: 4g
- Fiber: 12g
- Sodium: 1mg
- Ingredient list: "almonds" (single ingredient)
- No Israeli red labels

**L2 — Derived metrics:**
- Fat from kcal: 49×9/580 = 76%
- Saturated fat fraction: 3.7/49 = 0.076 (7.6%)
- Sugar-to-carb ratio: 4/22 = 0.18
- Protein-per-kcal: 21/580 = 0.036
- Ingredient count: 1
- Additive marker count: 0

**L3 — Inferred classifications:**
- Category: `whole_food_fat` — high confidence (~0.90); name and ingredient signal are unambiguous
- NOVA level: 1 — high confidence; single whole-food ingredient, no processing markers
- HP patterns: HP_FAT_SUGAR_COMBO requires sugar≥20g; almond sugar=4g → does NOT fire. HP_FAT_SODIUM_COMBO requires sodium≥300mg; almond sodium=1mg → does NOT fire. No HP patterns.
- Protein source: whole food
- Sweetener: absent

**L4 — Interpreted concerns:**
- SUGAR_LOAD rules: no rules fire (sugar=4g)
- CALORIE_LOAD: HIGH_CAL_LOW_SATIETY_SEVERE requires protein<6g AND fiber<3g; almonds have 21g protein, 12g fiber → does NOT fire. HIGH_CAL_LOW_SATIETY_SOFT requires protein<8g; almonds have 21g → does NOT fire.
- PROCESSING_LOAD: NOVA 1 → no rules fire
- SODIUM_LOAD: sodium=1mg → no rules fire
- FAT_QUALITY: no red label; no seed oil
- SWEETENER: none

**L5 — Behavioral hypotheses embedded:**
- The whole-food fat calorie density table (≤650 kcal → 75 points) embeds the hypothesis that high calorie density in intact fat-matrix foods is nutritionally neutral relative to engineered high-calorie products. This is directionally supported by evidence on nut consumption and satiety.
- The low-HP fire (no patterns) is consistent with the hypothesis that intact nuts do not drive appetite dysregulation in the way engineered fat-sugar products do.

**L6 — Normative judgements:**
- NOVA 1 floor (minimum 75) is a normative commitment: a single-ingredient whole food cannot receive a failing grade regardless of other signals.
- The `whole_food_fat` category table represents a normative judgement that fat from intact food sources should be evaluated on a different calorie scale than fat from engineered products.

---

### Section C — Dimension Trace

| Dimension | Weight | Est. Score | Key signals | Coherent? |
|-----------|--------|------------|-------------|-----------|
| Processing Quality | 15% | ~95 | NOVA 1 | Yes |
| Nutrient Density | 15% | ~88 | 21g protein, 12g fiber, vitamin E, Mg | Yes |
| Calorie Density | 15% | ~75 | 580 kcal → whole_food_fat table | Yes — but only with correct category |
| Glycemic Quality | 12% | ~88 | 4g sugar, 12g fiber, low GI matrix | Yes |
| Protein Quality | 10% | ~85 | Whole food source, 21g | Yes |
| Additive Quality | 10% | ~98 | No additives | Yes |
| Satiety Support | 6% | ~90 | 21g protein, 12g fiber | Yes |
| Fat Quality | 8% | ~72 | Sat fat 3.7g → dimension penalty −max((3.7−2)×4,0) = −6.8; otherwise excellent MUFA/PUFA profile | Minor concern — sat fat penalty on whole food is awkward |
| Regulatory Quality | 5% | ~95 | No red labels | Yes |
| Whole Food Integrity | 4% | ~100 | NOVA 1, 1 ingredient | Yes |

**Weighted dimension score estimate:** ~88
(Processing 14.25 + Nutrient 13.2 + Calorie 11.25 + Glycemic 10.56 + Protein 8.5 + Additive 9.8 + Satiety 5.4 + Fat 5.76 + Regulatory 4.75 + Whole food 4.0 = 87.5)

---

### Section D — Guardrail Trace

No guardrail rules fire. No caps, no penalties.

Floors: NOVA 1 single ingredient → minimum 75 (not needed; score is ~88).

**Final score: ~88. Grade A.**

---

### Section E — Category Stability

**Primary:** `whole_food_fat` — confidence ~0.90
**Secondary:** `default` — what happens if classifier fails?

Secondary trace with `default` category:
- 580 kcal → >550 kcal → calorie density score: 20 (catastrophic)
- Calorie density contribution: 0.15 × 20 = 3.0 vs. 0.15 × 75 = 11.25 — a gap of 8.25 points
- Weighted dimension score drops from ~88 to ~80
- NOVA 1 floor (75) would protect the score from going below 75 even with wrong category
- Final score with `default` category: ~80 (floor would likely still not bind since score is ~80)

**Score instability: ~8 points. Low-moderate.**

The NOVA 1 floor provides strong protection here. The main risk is not catastrophic miscategorisation — the floor catches it. This is the strongest product in terms of robustness.

---

### Section F — User Explanation Simulation

> **Score: 88 — Grade A**
> Strong nutritional structure. Whole food fat source. High protein and fiber content. Minimally processed.
> Category: Nut & seed products.

**Is this intellectually honest?** Yes. The explanation is accurate and traceable. The fat quality tradeoff (moderate saturated fat creating a slight drag on one dimension) could optionally be surfaced as context, but at 3.7g sat fat in a whole-food matrix, it is not a dominant signal.

---

### Section G — Failure Analysis

1. **Strongest:** Processing quality, nutrient density, whole food integrity. These are all unambiguously excellent and the scoring reflects that.
2. **Weakest:** The fat quality dimension applies a sat fat dimension penalty to a food whose saturated fat is inseparable from its food matrix. There is no mechanism to distinguish "sat fat in industrial palm oil" from "sat fat in whole almond." The penalty is correct in magnitude (small) but architecturally blunt.
3. **Philosophically inconsistent:** Nothing significant.
4. **Gaming risk:** The 25g sugar threshold and 500 kcal thresholds don't apply here. Gaming is not relevant for single-ingredient whole foods.
5. **Score reflects:** Meaningful food structure recognition. Almonds score A because the architecture correctly reads their matrix — not because they avoid penalties. This is the one product where the current architecture behaves as designed.

---

## PRODUCT 2 — Dates (Whole Dried)

### Section A — Product Context

**Expected intuitive outcome:** Grade B or high C. Nutritious whole fruit, traditional food, eaten across Middle Eastern and global diets. Should not score D or E.

**Why adversarial:** Dates contain 60–65g natural sugar per 100g — far above every sugar threshold in the system. The same rules designed to catch glucose-syrup-laden confectionery will fire on a NOVA 1 whole fruit. This is the primary test of whether the architecture distinguishes natural from added sugar, and whether the NOVA 1 floor protects against rules that were never intended for this product type.

**Architectural tensions activated:**
- NOVA 1 floor vs. sugar caps (explicit unresolved conflict)
- Natural sugar in whole food vs. added sugar in engineered products
- Israeli red label on a traditional whole food
- Glycemic quality dimension scoring a food with intact fiber

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 282 kcal/100g
- Protein: 2.5g | Fat: 0.4g | Saturated fat: ~0g
- Carbohydrates: 75g | Sugar: 63g
- Fiber: 8g | Sodium: 2mg
- Ingredient list: "dates" (single ingredient or "dates, pits removed")
- Israeli red label: sugar — ALMOST CERTAIN to fire at 63g sugar/100g given Israeli thresholds (typically 17.5g/100g for solids)

**L2 — Derived metrics:**
- Fat from kcal: 0.4×9/282 = 1.3% (negligible)
- Sugar-to-carb ratio: 63/75 = 0.84
- Protein-per-kcal: 2.5/282 = 0.009 (low)
- Ingredient count: 1
- Additive marker count: 0
- Added sugar markers: 0 (the sugar is intrinsic to the whole fruit)

**L3 — Inferred classifications:**
- Category: `default` — high confidence. Dates don't match `whole_food_fat` (not fat-dominant), `snack_bar_granola` (not a bar), `dessert` (a whole fruit). `default` is most defensible. Secondary: `dessert` (if commercial packaging implies a treat).
- NOVA level: 1 — single whole-food ingredient
- HP patterns: HP_FAT_SUGAR_COMBO requires fat≥30% kcal AND sugar≥20g. Fat=1.3% → does NOT fire. No HP patterns.
- Protein source: whole food (but negligible)

**L4 — Interpreted concerns (HERE IS WHERE IT BREAKS):**

- SUGAR_LOAD:
  - `HIGH_SUGAR_25G_PLUS`: sugar=63g ≥ 25g → **FIRES: cap 60**
  - `ISRAELI_RED_LABEL_1` (sugar): red label fires → **FIRES: cap 55**
  - Coordination: both SUGAR_LOAD caps → strictest = **cap 55**
  - `MULTIPLE_ADDED_SUGAR_MARKERS`: no added sugar sources (intrinsic fruit sugar) → does NOT fire
  - `HIGH_CAL_HIGH_SUGAR_SOFT`: kcal=282 < 430 → does NOT fire

- CALORIE_LOAD: kcal=282 < 430 → no rules fire
- PROCESSING_LOAD: NOVA 1 → no rules fire
- SODIUM_LOAD: sodium=2mg → no rules fire
- FAT_QUALITY: negligible fat → no rules fire

**L5 — Behavioral hypotheses embedded (and wrong here):**
- `HIGH_SUGAR_25G_PLUS` embeds the hypothesis that sugar ≥ 25g/100g represents a structural glycemic concern. This hypothesis is calibrated for products where the sugar is added or refined. For whole dates, fiber (8g) substantially moderates the glycemic response — the hypothesis does not apply cleanly.
- The Israeli red label embeds a regulatory hypothesis calibrated for the general food population, which is dominated by processed foods. The label does not distinguish natural from added sugar.

**L6 — Normative judgements in conflict:**
- Normative commitment 1: NOVA 1 single-ingredient products deserve a minimum score of 75 (the whole-food floor)
- Normative commitment 2: Sugar ≥ 25g/100g triggers a cap at 60, regardless of source

**These two normative commitments directly conflict for dates.**

The specification does not say which wins.

---

### Section C — Dimension Trace

| Dimension | Weight | Est. Score | Notes |
|-----------|--------|------------|-------|
| Processing Quality | 15% | ~95 | NOVA 1 |
| Nutrient Density | 15% | ~60 | High fiber offset by very low protein, negligible fat micronutrients |
| Calorie Density | 15% | ~65 | 282 kcal → default table, ≤350 → 65 |
| Glycemic Quality | 12% | ~25 | 63g sugar — the dimension correctly identifies this as a concern, but cannot weight that fiber=8g moderates actual glycemic response |
| Protein Quality | 10% | ~30 | 2.5g protein, whole food but negligible quantity |
| Additive Quality | 10% | ~98 | No additives |
| Satiety Support | 6% | ~50 | Good fiber (8g) but essentially no protein |
| Fat Quality | 8% | ~90 | Negligible fat |
| Regulatory Quality | 5% | ~30 | Red label (sugar) applies |
| Whole Food Integrity | 4% | ~100 | NOVA 1, 1 ingredient |

**Weighted dimension score:** ~63
(Processing 14.25 + Nutrient 9.0 + Calorie 9.75 + Glycemic 3.0 + Protein 3.0 + Additive 9.8 + Satiety 3.0 + Fat 7.2 + Regulatory 1.5 + Whole food 4.0 = 64.5)

---

### Section D — Guardrail Trace — THE CRITICAL FAILURE

**Binding cap after coordination:** 55 (SUGAR_LOAD family, coordinated from HIGH_SUGAR_25G_PLUS and ISRAELI_RED_LABEL_1)

**Penalties:** None (no added sugar markers, no calorie-load rules)

**Score before floor:** min(64.5, 55) − 0 = **55. Grade C.**

**Floor application: NOVA 1 single ingredient → minimum 75**

**CONFLICT: cap=55, floor=75. The specification does not resolve this.**

| Resolution | Final Score | Grade | Assessment |
|-----------|-------------|-------|------------|
| Floor wins (75) | 75 | B | Philosophically correct for a whole fruit |
| Cap wins (55) | 55 | C | Analytically consistent but arguably wrong |
| Cap has precedence, floor is overridden | 55 | C | The less defensible outcome |

**This is the most important architectural gap exposed in this workshop.** The floor was designed to protect whole foods. The cap was designed to flag sugar-dense products. They collide on exactly the product both were meant to treat differently.

---

### Section E — Category Stability

**Primary:** `default` — confidence ~0.70
**Secondary:** `dessert` — what if dates are sold in a commercial snack context?

Secondary trace with `dessert`:
- 282 kcal → ≤350 kcal → calorie density score: 55 (vs. 65 in default)
- Score drops ~1.5 points from dimension weighting change
- All guardrail rules are the same (not category-dependent for sugar rules)
- Score instability: ~1.5 points — LOW. Category is not decisive for dates.

The main category risk is NOT a score cliff — it is a false floor. If dates are miscategorised as `snack_bar_granola`, no rule specifically fires worse (calories are too low for snack bar health-halo rules), but the calorie density dimension would score 282 kcal on the snack bar table (≤350 → 55 points) — same as dessert. No catastrophe from category here.

**Paradox: the floor-vs-cap conflict is the dominant risk, not category.**

---

### Section F — User Explanation Simulation

**If floor wins:**
> **Score: 75 — Grade B**
> Whole food with high natural sugar content — moderated by significant fiber. Minimal processing.
> Note: Natural sugar concentration is high; this product carries an Israeli regulatory warning for sugar content.
> Category: General food.

**If cap wins:**
> **Score: 55 — Grade C**
> High sugar concentration triggers a structural scoring constraint. Score is capped due to sugar content.
> Category: General food.

**Is the cap-wins explanation intellectually honest?** No. "High sugar concentration triggers a structural scoring constraint" is accurate but misleading applied to a whole fruit. The constraint was designed for products where sugar is an industrial addition. Applying the same language to dates conflates two structurally different situations and produces an explanation that would confuse any informed user.

---

### Section G — Failure Analysis

1. **Strongest:** Processing quality and whole food integrity are correctly excellent. The fiber signal partly compensates in the glycemic dimension.
2. **Weakest:** The glycemic quality dimension cannot distinguish "63g natural fruit sugar co-present with 8g fiber in a NOVA 1 matrix" from "63g added sugar in an engineered product." Both produce the same low dimension score. This is a genuine analytical failure.
3. **Philosophically inconsistent:** The system simultaneously says "this product is as whole and unprocessed as possible" (NOVA 1 floor) and "this product's sugar content is a structural concern" (cap at 55). These two claims produce contradictory scoring instructions.
4. **Gaming risk:** None applicable — this is a whole food.
5. **Score reflects:** Punishment avoidance failure. The architecture's sugar detection machinery fires on a whole food for reasons it was not designed for. The score does not reflect the actual structural quality of dates; it reflects the unintended application of rules calibrated for engineered products.

---

## PRODUCT 3 — Coconut Oil

### Section A — Product Context

**Expected intuitive outcome:** Grade B. A single-ingredient whole food used as a cooking fat. Should score well despite its extreme saturated fat content, because the source is whole and the use context is as a fat, not a primary food.

**Why adversarial:** Coconut oil is ~86% saturated fat and ~862 kcal/100g. It will trigger: HIGH_CAL_LOW_SATIETY_SEVERE (high kcal, zero protein, zero fiber), the saturated fat dimension penalty at enormous magnitude, and an Israeli red label for saturated fat. It is structurally identical to a NOVA 1 product in terms of processing, but its compositional profile fires every calorie and fat quality rule in the system.

**Architectural tensions activated:**
- HIGH_CAL_LOW_SATIETY_SEVERE firing on a pure cooking fat (no protein/fiber because it's a fat, not a food)
- Saturated fat dimension penalty formula applied to a product where sat fat is the entire substance
- NOVA 1 floor vs. multiple caps (second floor-cap conflict)
- Fat quality cap vs. whole-food floor

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 862 kcal/100g
- Protein: 0g | Carbs: 0g | Sugar: 0g
- Total fat: 100g | Saturated fat: 87g
- Fiber: 0g | Sodium: 0mg
- Ingredient list: "coconut oil" (single ingredient)
- Israeli red label: saturated fat — CERTAIN to fire at 87g sat fat/100g

**L2 — Derived metrics:**
- Fat from kcal: 100%
- Saturated fat fraction: 87/100 = 0.87
- Sat fat dimension penalty: −max((87−2)×4, 0) = −340 → fat quality dimension score = max(100−340, 0) = 0
- Ingredient count: 1 | Additive markers: 0

**L3 — Inferred classifications:**
- Category: `whole_food_fat` — high confidence (~0.85); name "coconut oil" strongly signals this category
- NOVA level: 1 — cold-pressed or expeller-pressed single ingredient
- HP patterns: HP_FAT_SODIUM_COMBO requires sodium≥300mg; sodium=0 → does NOT fire. HP_FAT_SUGAR_COMBO requires sugar≥20g; sugar=0 → does NOT fire.

**L4 — Interpreted concerns:**

- CALORIE_LOAD:
  - `HIGH_CAL_LOW_SATIETY_SEVERE`: kcal=862≥500 AND protein=0<6g AND fiber=0<3g → **FIRES: cap 55**
  - `HIGH_CAL_LOW_SATIETY_SOFT`: kcal=862≥450 AND protein=0<8g AND fiber=0<5g → **FIRES: penalty −6**

  **Philosophical problem:** This rule was designed to identify calorie-dense products that fail to deliver satiety-supporting nutrients. Coconut oil fails the protein/fiber conditions because it is a *pure fat* — not because it is nutritionally deficient in any relevant sense. A cooking oil is not expected to have protein or fiber. The rule fires correctly by its letter but incorrectly by its intent.

- FAT_QUALITY:
  - `ISRAELI_RED_LABEL_1` (saturated fat): red label fires → cap 55 (FAT_QUALITY concern family)

- All other guardrail rules: do not fire (no sugar, no additives, no sodium, no processing signals)

**L5 — Behavioral hypothesis failure:**
The LOW_SATIETY rules embed the hypothesis that calorie-dense, protein-free, fiber-free products fail to support satiety. This hypothesis is designed for snack foods and meal foods. Applied to a cooking fat, it is a category error: no one evaluates coconut oil's satiety contribution in isolation from the meal it is part of.

**L6 — Normative conflict:**
- Normative commitment (NOVA 1 floor): a single-ingredient whole food cannot score below 75.
- Normative commitment (LOW_SATIETY rules): a product with 862 kcal, 0 protein, 0 fiber should be capped at 55.
- Normative commitment (sat fat red label): regulatory signal must be respected with cap at 55.

Three normative commitments; two produce cap=55; one produces floor=75. **Conflict is identical to dates.**

---

### Section C — Dimension Trace

| Dimension | Weight | Est. Score | Notes |
|-----------|--------|------------|-------|
| Processing Quality | 15% | ~95 | NOVA 1 |
| Nutrient Density | 15% | ~10 | Zero protein, zero fiber, zero micronutrients — pure fat |
| Calorie Density | 15% | ~55 | 862 kcal → whole_food_fat table, ≤900 → 55 |
| Glycemic Quality | 12% | ~95 | Zero sugar, zero carbs |
| Protein Quality | 10% | ~20 | Zero protein — dimension cannot score positively |
| Additive Quality | 10% | ~98 | No additives |
| Satiety Support | 6% | ~15 | Zero protein, zero fiber — structurally satiety-free |
| Fat Quality | 8% | ~0 | Sat fat penalty formula produces ~0; dimension floored |
| Regulatory Quality | 5% | ~20 | Sat fat red label |
| Whole Food Integrity | 4% | ~100 | NOVA 1, 1 ingredient |

**Weighted dimension score:** ~55
(Processing 14.25 + Nutrient 1.5 + Calorie 8.25 + Glycemic 11.4 + Protein 2.0 + Additive 9.8 + Satiety 0.9 + Fat 0 + Regulatory 1.0 + Whole food 4.0 = 53.1)

---

### Section D — Guardrail Trace

**Caps from different families (apply independently):**
- CALORIE_LOAD cap: 55 (HIGH_CAL_LOW_SATIETY_SEVERE)
- FAT_QUALITY cap: 55 (ISRAELI_RED_LABEL_1 sat fat)
- Binding cap: **55**

**Penalties:**
- CALORIE_LOAD: HIGH_CAL_LOW_SATIETY_SOFT → −6

**Score before floor:** min(53, 55) − 6 = 53 − 6 = **47. Grade D.**

**Floor: NOVA 1 single ingredient → minimum 75.**

**CONFLICT: cap-derived-then-penalised score = 47, floor = 75. Gap = 28 points.**

This is the largest floor-cap conflict of any product in this workshop. The sat fat dimension penalty formula alone (producing ~0 on the fat quality dimension) already pushes the dimension score to ~53 before any guardrail cap. The cap is barely binding. The penalties then push to 47. The NOVA 1 floor at 75 would override an entire set of analytically legitimate negative signals.

| Resolution | Final Score | Grade | Assessment |
|-----------|-------------|-------|------------|
| Floor wins | 75 | B | Protects whole food but hides real sat fat concern |
| Cap wins | 47 | D | Punishes a whole food for being a pure fat, which is definitionally protein/fiber-free |

**Neither resolution is clearly correct. This is a genuine architectural failure.**

---

### Section E — Category Stability

**Primary:** `whole_food_fat` — confidence ~0.85
**Secondary:** `sauce_spread` — if a retail platform categorises "coconut oil for cooking" as a spread

Secondary trace with `sauce_spread` category:
- 862 kcal → >750 kcal → calorie density score: 25 (vs. 55 in whole_food_fat)
- Calorie density dimension contribution: 0.15 × 25 = 3.75 vs. 0.15 × 55 = 8.25 — gap of 4.5 points
- No additional guardrail rules fire differently
- Dimension score drops from ~53 to ~48
- After cap and penalty: 48 − 6 = 42 (floor still at 75 if NOVA 1 floor applies)

**Score instability: ~5 points from category alone.** The floor-cap conflict dominates regardless.

---

### Section F — User Explanation Simulation

**If floor wins:**
> **Score: 75 — Grade B**
> Whole food fat source. Minimally processed. High saturated fat concentration carries a regulatory warning. Use as a cooking fat; evaluate in meal context.
> Category: Nut & seed products.

**If cap wins:**
> **Score: 47 — Grade D**
> Very high calorie density. High saturated fat. Regulatory warning for saturated fat content. Structural scoring constraints applied.
> Category: Nut & seed products.

**Is either honest?** The cap-wins explanation is technically accurate but produces "Grade D — Notable structural concerns" for pure coconut oil. This is not intellectually honest for a product where every structural concern is an inevitable consequence of it being a pure fat. The floor-wins explanation is more honest but sweeps the genuine sat fat signal under the floor.

**The honest explanation doesn't exist yet in the current architecture:** "This product is a whole-food fat. Its saturated fat content is high and carries a regulatory warning. Evaluated as a cooking fat, not a primary food; satiety and protein signals are not applicable in this context."

---

### Section G — Failure Analysis

1. **Strongest:** Processing quality, additive quality, whole food integrity — all correctly excellent.
2. **Weakest:** HIGH_CAL_LOW_SATIETY_SEVERE fires on coconut oil because it has zero protein and fiber — by definition, because it's a pure fat. The rule is architecturally blind to product type. This is the most significant rule-misfires in the entire workshop.
3. **Philosophically inconsistent:** The system applies a "low satiety" penalty to a product that is not consumed for satiety. This is a category error at the rule-design level.
4. **Gaming risk:** None applicable — single ingredient whole food.
5. **Score reflects:** Punishment avoidance failure. Coconut oil's score is determined almost entirely by rules misfiring on a product type they were not designed for.

---

## PRODUCT 4 — Brined Olives

### Section A — Product Context

**Expected intuitive outcome:** Grade B or high C. A traditional Mediterranean food consumed in small quantities. Excellent fat quality. Penalised by sodium concentration rules calibrated for primary foods, not condiments.

**Why adversarial:** Three tensions collide: (1) sodium concentration at 1,500mg/100g fires the highest sodium cap; (2) the HP_FAT_SODIUM_COMBO pattern fires on natural olive fat + salt brine (HP overreach on a whole food); (3) the whole-food floor at 65 is lower than the sodium cap at 60.

**Architectural tensions activated:**
- Per-100g evaluation of a condiment consumed in 20–40g quantities
- HP overreach: natural fat + salt brine vs. engineered fat-sodium palatability
- Floor (65) vs. sodium cap (60)
- Evaluation scope: should olives be `context_limited`?

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 115 kcal/100g
- Protein: 1g | Fat: 11g | Saturated fat: 1.7g
- Carbohydrates: 6g | Sugar: 0g
- Fiber: 3g | Sodium: 1,500mg
- Ingredient list: olives, water, salt (3 ingredients)
- No Israeli red labels (sat fat 1.7g well below threshold; sugar 0g; sodium label may apply at 1,500mg)

**L2 — Derived metrics:**
- Fat from kcal: 11×9/115 = 86%
- Saturated fat fraction: 1.7/11 = 0.15
- Additive markers: 0 (salt is not an additive marker)

**L3 — Inferred classifications:**
- Category: `whole_food_fat` — medium confidence (~0.65); secondary `sauce_spread` (~0.55). Ambiguous form factor.
- NOVA level: 2 — brining is traditional processing; no synthetic additives. Medium-high confidence.
- HP_FAT_SODIUM_COMBO: fat from kcal = 86% ≥ 25% AND sodium = 1,500mg ≥ 300mg → **FIRES** at L3 classification level
  - **HP overreach flag:** This is natural olive fat and preservation brine, not engineered palatability engineering.

**L4 — Interpreted concerns:**

- SODIUM_LOAD:
  - `HIGH_SODIUM_700MG_PLUS`: sodium=1,500mg ≥ 700mg → **FIRES: cap 60**
  - `HP_FAT_SODIUM_COMBO`: both conditions met → **FIRES: HP penalty** (est. raw −6 to −8)
  - Coordination: cap winner = HIGH_SODIUM_700MG_PLUS (only cap); penalty winner = HP_FAT_SODIUM_COMBO (only penalty, applied at full value ~−6)
  - Family budget max: 8 → −6 within budget

- All other rules: no sugar rules fire; calorie rules don't fire (115 kcal); no processing rules fire (NOVA 2).

**L5 — Behavioral hypothesis misapplication:**
HP_FAT_SODIUM_COMBO embeds the hypothesis that high-fat, high-sodium combinations indicate a product engineered to drive palatability beyond normal regulation. Brined olives have high fat (natural to olives) and high sodium (from preservation brine). Neither property was engineered for palatability purposes. The hypothesis is being applied to a product for which it was not calibrated.

---

### Section C — Dimension Trace

| Dimension | Weight | Est. Score | Notes |
|-----------|--------|------------|-------|
| Processing Quality | 15% | ~85 | NOVA 2 — traditional processing |
| Nutrient Density | 15% | ~60 | Low protein, moderate fiber, good monounsaturated fat |
| Calorie Density | 15% | ~90 | 115 kcal → whole_food_fat table ≤350 → 90 |
| Glycemic Quality | 12% | ~90 | No sugar, 3g fiber |
| Protein Quality | 10% | ~30 | Very low protein |
| Additive Quality | 10% | ~98 | No additives |
| Satiety Support | 6% | ~35 | Low protein, moderate fiber |
| Fat Quality | 8% | ~75 | Sat fat 1.7g → penalty −max((1.7−2)×4,0) = 0 (below threshold); excellent MUFA profile |
| Regulatory Quality | 5% | ~70 | Sodium may trigger regulatory warning depending on label |
| Whole Food Integrity | 4% | ~90 | 3 ingredient NOVA 2 |

**Weighted dimension score:** ~75
(Processing 12.75 + Nutrient 9.0 + Calorie 13.5 + Glycemic 10.8 + Protein 3.0 + Additive 9.8 + Satiety 2.1 + Fat 6.0 + Regulatory 3.5 + Whole food 3.6 = 74.1)

---

### Section D — Guardrail Trace

**Caps:**
- SODIUM_LOAD: cap 60

**Penalties:**
- HP_FAT_SODIUM_COMBO: −6 (at full — sole penalty in family, applied as winner)

**Score before floor:** min(74, 60) − 6 = 60 − 6 = **54. Grade D.**

**Floor: NOVA 1–2 whole-food fat → minimum 65.**

**CONFLICT: cap-then-penalised score = 54, floor = 65. Gap = 11 points.**

| Resolution | Final Score | Grade |
|-----------|-------------|-------|
| Floor wins | 65 | C |
| Cap wins | 54 | D |

---

### Section E — Category Stability

**Primary:** `whole_food_fat` — 0.65 confidence
**Secondary:** `sauce_spread` — 0.55 confidence

Secondary trace (`sauce_spread`): 115 kcal → ≤150 → calorie density score 90 (same as whole_food_fat for this calorie level). No significant difference. All guardrail rules are category-independent for this product. Score instability: **< 3 points.** Category is not the decisive risk here. The sodium cap and HP_FAT_SODIUM_COMBO dominate.

---

### Section F — User Explanation Simulation

> **Score: 54 (cap wins) or 65 (floor wins) — Grade D or C**
> High sodium concentration: regulatory scoring constraint applied. Fat-sodium combination flagged.
> Note: Sodium reflects preservation brine; this product is typically consumed in small portions. Per-100g evaluation may not reflect dietary sodium impact.
> Category: Nut & seed products.

**Is this honest?** Partially. The score is driven by rules designed for primary foods applied to a condiment consumed in 25–30g servings. Surfacing the context note is essential, but the grade of C or D for brined olives will confuse any Mediterranean diet advocate with good reason.

---

### Section G — Failure Analysis

1. **Strongest:** Calorie density, glycemic quality, additive quality — all correctly excellent for this food.
2. **Weakest:** HP_FAT_SODIUM_COMBO fires on a product where both components (fat and sodium) are natural and traditional, not engineered for palatability. This is the clearest HP overreach in the workshop.
3. **Philosophically inconsistent:** The sodium cap at 60 applied to a condiment is a per-100g rule that does not reflect dietary impact. This is a known `context_limited` product per `evaluation_scope.md`. The architecture does not currently have a mechanism to modify rule application for context_limited products.
4. **Gaming risk:** None applicable.
5. **Score reflects:** Punishment coordination engine. The score of 54 (if cap wins) is produced entirely by a sodium cap and an HP penalty that both misfire on a traditional whole food.

---

## PRODUCT 5 — Whole-Food Date-Nut Bar

### Section A — Product Context

**Expected intuitive outcome:** Grade B or high C. Four whole-food ingredients, NOVA 2, genuinely nutritious. Should clearly outscore a sugary granola bar. Currently faces the most dangerous combination of risks in this workshop.

**Why adversarial:** This product is the canonical category classification disaster case. It will likely be classified as `snack_bar_granola` by name-matching alone — at which point it faces the harshest category rules. Even with correct classification, its natural date sugar triggers all sugar caps. And the HP_FAT_SUGAR_COMBO pattern fires on natural nuts + natural dates. This product stress-tests category instability, natural sugar handling, HP overreach, and floor-cap conflict simultaneously.

**Architectural tensions activated:**
- `snack_bar_granola` vs. `whole_food_fat` — 30+ point score gap
- Natural sugar triggering sugar caps
- HP_FAT_SUGAR_COMBO on whole-food ingredients
- Multiple floor-cap conflicts

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 460 kcal/100g
- Protein: 6g | Fat: 18g | Saturated fat: 2g
- Carbohydrates: 60g | Sugar: 50g (entirely from dates)
- Fiber: 6g | Sodium: 5mg
- Ingredient list: dates, almonds, cashews, cocoa (4 ingredients)
- NOVA: 2 (pressed/formed from whole ingredients, no chemical processing)
- Israeli red label: sugar — FIRES at 50g sugar (certain)

**L2 — Derived metrics:**
- Fat from kcal: 18×9/460 = 35%
- Sugar-to-carb ratio: 50/60 = 0.83
- Additive markers: 0

**L3 — Inferred classifications:**
- **Primary (likely) category: `snack_bar_granola` — confidence ~0.70** (the word "bar" in name/description; bar form factor)
- **Correct category: arguably `whole_food_fat`** — confidence ~0.55 (all ingredients are whole food fat sources or whole fruit)
- **There is no "whole food bar" category.** This is a genuine scope gap.
- NOVA: 2 — medium-high confidence
- HP_FAT_SUGAR_COMBO: fat=35% kcal ≥ 30% AND sugar=50g ≥ 20g → **FIRES**
  - **HP overreach: both fat (nuts) and sugar (dates) are whole-food, unengineered components**

**L4 — Interpreted concerns (BOTH CATEGORY SCENARIOS):**

Sugar rules (category-independent):
- `HIGH_SUGAR_25G_PLUS`: 50g ≥ 25g → **FIRES: cap 60**
- `ISRAELI_RED_LABEL_1` (sugar): fires → **FIRES: cap 55**
- Coordination: cap 55 (strictest, SUGAR_LOAD)
- `HP_FAT_SUGAR_COMBO`: FIRES → HP penalty (est. −6)
- Penalty coordination (SUGAR_LOAD): HP is winner at full = −6; total sugar family penalty = 6

Calorie rules (CATEGORY-DEPENDENT):
- `SNACK_BAR_HIGH_CAL` (if `snack_bar_granola`): kcal=460 ≥ 430 → **FIRES: cap 70** (CALORIE_LOAD)
- `HIGH_CAL_LOW_SATIETY_SOFT`: kcal=460 ≥ 450, protein=6g < 8g, fiber=6g ≥ 5g → fiber condition NOT met → does NOT fire

Processing rules:
- NOVA 2: no processing caps fire

---

### Section C — Dimension Trace (BOTH SCENARIOS)

| Dimension | `snack_bar_granola` | `whole_food_fat` |
|-----------|---------------------|-----------------|
| Calorie Density | **25** (460 kcal on snack bar table) | **85** (460 kcal on wff table) |
| Processing Quality | 88 | 88 |
| Nutrient Density | 60 | 60 |
| Glycemic Quality | ~30 (50g sugar despite fiber) | ~30 |
| Protein Quality | 55 | 55 |
| Additive Quality | 98 | 98 |
| Satiety Support | 60 | 60 |
| Fat Quality | 80 | 80 |
| Regulatory Quality | 25 (red label sugar) | 25 |
| Whole Food Integrity | 92 | 92 |

**Weighted dimension score:**
- `snack_bar_granola`: ~60 (calorie density dimension drags heavily: 0.15×25=3.75 vs. 0.15×85=12.75)
- `whole_food_fat`: ~70 (calorie density is strong)

---

### Section D — Guardrail Trace

**Scenario A — `snack_bar_granola`:**
- SUGAR_LOAD cap: 55
- CALORIE_LOAD cap: 70 (SNACK_BAR_HIGH_CAL)
- Binding cap: 55 (SUGAR_LOAD strictest)
- Penalties: sugar family −6 (HP_FAT_SUGAR_COMBO)
- Score: min(60, 55) − 6 = 55 − 6 = **49. Grade D.**
- Floor (NOVA 2 whole-food, if applicable): 65 → **CONFLICT**
- Floor wins → 65, Floor loses → 49

**Scenario B — `whole_food_fat`:**
- SUGAR_LOAD cap: 55
- No additional calorie cap fires (no snack bar rule)
- Binding cap: 55
- Penalties: sugar family −6
- Score: min(70, 55) − 6 = 55 − 6 = **49. Grade D.** (same result despite very different calorie dimension score)
- Floor: 65 → **CONFLICT**

**Critical observation:** The final score (49 pre-floor) is IDENTICAL regardless of category. The calorie density dimension contributes +8.25 extra points in the correct category, but this is irrelevant because the sugar cap (55) already binds the score below where the dimension scoring produces. The category determines the dimension score, but the binding sugar cap makes the dimension score irrelevant above ~61.

**The category classification problem is partially masked by the sugar cap.** This is unexpected — the 30-point category score gap identified earlier exists only in the pre-cap dimension score. Post-cap, the gap collapses.

If the floor wins: Score = 65 in both scenarios. Category truly doesn't matter.
If the floor loses: Score = 49 in both scenarios. Category also doesn't matter.

---

### Section E — Category Stability

**Score instability from category change: near zero post-cap.** The sugar cap dominates. Category primarily affects the dimension score, which is already below the binding cap.

**This reveals a deeper problem:** When a binding cap is in place, improving any dimension below the cap has zero effect on the final score. The scoring system becomes informationally deaf to positive signals.

---

### Section F — User Explanation Simulation

> **Score: 65 (if floor wins) or 49 (if floor loses) — Grade C or D**
> High natural sugar concentration from dates triggers a structural scoring constraint. Fat-sugar combination also detected in composition. Note: all ingredients are whole food.
> Category: [General food or Bars & granola depending on classification]

**Is this honest?** No. The explanation "Fat-sugar combination detected" is the same language used for engineered chocolate confectionery. Applying it to dates + almonds is factually accurate (the composition matches) but analytically misleading (the mechanism is entirely different).

---

### Section G — Failure Analysis

1. **Strongest:** Additive quality, whole food integrity, processing quality — perfectly reflect a clean whole-food product.
2. **Weakest:** Sugar cap fires identically on this product and on a glucose-syrup granola bar. The architecture cannot distinguish them. HP_FAT_SUGAR_COMBO fires on natural whole-food composition. Both are the same architectural failure.
3. **Philosophically inconsistent:** This product and a sugary granola bar both receive a sugar cap of 55. If the floor doesn't protect the date-nut bar, they could both land at the same grade. That is the architecture's most indefensible outcome.
4. **Gaming risk:** None applicable (single ingredient whole foods cannot be gamed).
5. **Score reflects:** Punishment coordination engine. The score is entirely driven by sugar rules misfiring on whole-food ingredients.

---

## PRODUCT 6 — Sugary Granola Bar

### Section A — Product Context

**Expected intuitive outcome:** Grade D or E. The canonical health-halo failure product. If this scores above C, the system is too lenient.

**Why adversarial:** This is the product the system was explicitly calibrated for. The question is whether the score is correct *for the right reasons*, or whether it is correct by coincidence while conceptually overlapping with the date-nut bar in problematic ways.

**Architectural tensions activated:**
- Multiple rules firing — explainability complexity test
- Whether the same score as the date-nut bar (if floors fail) represents a philosophical failure
- Whether Rule explosion produces analytically correct results for the wrong reasons

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 460 kcal/100g | Protein: 4g | Fat: 18g | Saturated fat: 6g
- Carbohydrates: 68g | Sugar: 32g (added: glucose syrup, honey, sugar — 3 distinct sources)
- Fiber: 4g | Sodium: 100mg
- Ingredients: oats, glucose syrup, palm oil, honey, sugar, puffed rice, chocolate chips, soy lecithin, salt, flavor — 10 ingredients
- NOVA: 4 | Additive markers: soy lecithin, possible natural flavor, glucose syrup → ~3 markers
- Israeli red label: sugar (32g — certain)

**L3 — Inferred classifications:**
- Category: `snack_bar_granola` — very high confidence (~0.92)
- NOVA 4: high confidence (glucose syrup, palm oil, multiple industrial ingredients)
- HP_FAT_SUGAR_COMBO: fat=35% kcal AND sugar=32g ≥ 20g → **FIRES** (legitimately — this IS engineered)
- Multiple added sugar sources: glucose syrup, honey, sugar → 3 sources → **FIRES**

**L4 — Interpreted concerns:**

SUGAR_LOAD:
- `HIGH_SUGAR_25G_PLUS`: 32g → **FIRES: cap 60**
- `ISRAELI_RED_LABEL_1` (sugar): → **FIRES: cap 55**
- `MULTIPLE_ADDED_SUGAR_MARKERS`: 3 added sugar sources → **FIRES: penalty −5**
- `HIGH_CAL_HIGH_SUGAR_SOFT`: kcal=460≥430 AND sugar=32g≥15g → **FIRES: penalty −5**
- `HP_FAT_SUGAR_COMBO`: → **FIRES: HP penalty ~−6**
- Coordination (SUGAR_LOAD caps): strictest = 55
- Coordination (penalties): HP wins at full (−6); others at 40%: −2, −2 = total −10 (at budget)

CALORIE_LOAD:
- `SNACK_BAR_HIGH_CAL`: kcal=460≥430 → **FIRES: cap 70**
- `HIGH_CAL_LOW_SATIETY_SOFT`: kcal=460≥450, protein=4g<8g, fiber=4g<5g → **FIRES: penalty −6**
- Budget: −6 within max 8

PROCESSING_LOAD:
- `NOVA_PROXY_4_ULTRA_PROCESSED`: → **FIRES: cap 60**
- `ADDITIVE_MARKERS_3_PLUS`: 3 markers → **FIRES: cap 65**
- Coordination: strictest = 60

FAT_QUALITY:
- `ISRAELI_RED_LABEL_1` (sat fat): 6g → likely fires → **FIRES: cap 55**
- `SEED_OIL_PRESENT`: palm oil → **FIRES: penalty −3**

**All caps (different families, apply independently):**
- SUGAR_LOAD: 55
- CALORIE_LOAD: 70
- PROCESSING_LOAD: 60
- FAT_QUALITY: 55
- Binding cap: **55**

**Total penalties:**
- Sugar family: −10 (at budget)
- Calorie density family: −6
- Fat quality family: −3
- Total: **−19**

---

### Section C — Dimension Trace

| Dimension | Weight | Est. Score |
|-----------|--------|------------|
| Calorie Density | 15% | 25 (460 kcal, snack_bar table) |
| Processing Quality | 15% | 15 (NOVA 4) |
| Nutrient Density | 15% | 35 (low protein, moderate fiber) |
| Glycemic Quality | 12% | 25 (32g added sugar) |
| Protein Quality | 10% | 30 (low protein, isolated context) |
| Additive Quality | 10% | 40 (3 markers, not maximum) |
| Satiety Support | 6% | 35 (low protein, borderline fiber) |
| Fat Quality | 8% | 30 (palm oil, 6g sat fat) |
| Regulatory Quality | 5% | 20 (two red labels) |
| Whole Food Integrity | 4% | 20 (NOVA 4) |

**Weighted dimension score:** ~27
(3.75 + 2.25 + 5.25 + 3.0 + 3.0 + 4.0 + 2.1 + 2.4 + 1.0 + 0.8 = 27.6)

---

### Section D — Guardrail Trace

- Binding cap: 55
- Score: min(28, 55) = 28 — **cap is not binding** — dimension score is already well below cap
- After penalties (−19): 28 − 19 = **9. Grade E.**

A score of 9 is extreme. The problem: penalties (19 points) are being deducted from a dimension score (28) that is already very low. The cumulative effect puts the score in single digits.

**Recalibration note:** Either the penalty magnitudes are too high, or the penalty system should be bounded by the pre-penalty dimension score. A product cannot realistically receive a valid score of 9/100 — this is deeper into Grade E territory than the architecture conceptually supports.

**Revised estimate (more conservative penalty values):** If HP_FAT_SUGAR_COMBO raw = −4 (not −6), total penalties = 8+6+2 = 16. Score = 28−16 = 12. Still Grade E.

**The sugary granola bar lands in Grade E by a significant margin.** Whether 9 or 15, Grade E is the analytically correct direction.

---

### Section E — Category Stability

**Primary:** `snack_bar_granola` — confidence 0.92. No meaningful secondary category. Score instability: minimal. The product is correctly categorised with high confidence.

---

### Section F — User Explanation Simulation

> **Score: ~12–28 pre-penalty — Grade E**
> Ultra-processed. Multiple added sugar sources. High calorie density for category. Regulatory warning: sugar and saturated fat. Engineered fat-sugar combination detected.
> Category: Bars & granola.

**Active signal count: 8+ rules.** This product exceeds the explainability budget (max 3 dominant signals). The explanation would need to be collapsed to the three most important: ultra-processed, high added sugar, calorie density for category. The rest would be surfaced as "additional concerns" in the expanded view.

**Is this honest?** Yes — this product deserves Grade E and the signals are real. The concern is that the score of ~12 is lower than the architecture likely intends, suggesting penalty calibration is off.

---

### Section G — Failure Analysis

1. **Strongest:** The system correctly identifies every real concern with this product. This is BSIP2 working as designed.
2. **Weakest:** The cumulative penalty system produces a score of ~12, which may be too extreme. The architecture has no floor protection for Grade E territory — penalties can compound below any meaningful scale.
3. **Philosophically inconsistent:** The score of ~12 for the sugary granola bar and the score of 49 (if floor fails) for the date-nut bar differ by 37 points. Correct. But the score of 65 (if floor wins) for the date-nut bar and ~12 for the granola bar differ by 53 points — a meaningful and defensible gap.
4. **Gaming opportunity: CRITICAL.** The `SNACK_BAR_HIGH_CAL_SUGAR` rule requires kcal≥470 AND sugar≥15g. This product at 460 kcal avoided it. The `HIGH_CAL_HIGH_SUGAR_MODERATE` rule requires kcal≥470. At 460 kcal, this product narrowly avoids both rules. A reformulation from 460 kcal to 469 kcal (no meaningful nutritional change) continues to avoid them. A reformulation from 472 kcal to 468 kcal saves the product from ~2 additional penalty points. These cliffs are commercially actionable.
5. **Score reflects:** Punishment coordination engine — but correctly so for this product. This is the intended use case.

---

## PRODUCT 7 — Coke Zero

### Section A — Product Context

**Expected intuitive outcome:** Grade D or E. Zero nutritional value. Should not receive a passing grade.

**Why adversarial:** The calorie density dimension scores Coke Zero at 95/100 — the highest possible score on the most heavily weighted dimension (15%). The beverage category table rewards near-zero calorie content unconditionally, regardless of nutritional emptiness. This is the structural emptiness paradox in its clearest form.

**Architectural tensions activated:**
- Calorie density dimension rewarding structural emptiness
- Whether NOVA 4 and processing caps can overcome the dimension paradox
- The sweetener cap being non-binding when the processing cap is stricter
- Whether Grade D is the correct outcome for a product with zero nutritional value

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: ~1 kcal/100ml | Protein: 0g | Fat: 0g | Carbs: 0g | Sugar: 0g | Fiber: 0g | Sodium: 12mg
- Ingredients: water, caramel color (E150d), phosphoric acid, natural flavors, caffeine, acesulfame K, aspartame, citric acid
- NOVA: 4 | Additive markers: acesulfame K, aspartame (sweeteners), caramel color E150d, phosphoric acid, citric acid → 5 markers

**L3 — Inferred classifications:**
- Category: `beverage` — very high confidence (~0.97)
- NOVA: 4 — very high confidence
- HP patterns: no fat, no significant sodium, no sugar → none fire

**L4 — Interpreted concerns:**
- PROCESSING_LOAD:
  - `NOVA_PROXY_4_ULTRA_PROCESSED`: **FIRES: cap 60**
  - `ADDITIVE_MARKERS_5_PLUS`: 5 markers → **FIRES: cap 55**
  - Coordination: strictest = **55**
- SWEETENER_PRESENT: acesulfame K + aspartame → **FIRES: independent cap 70**
- All other families: no rules fire (no sugar, no sodium, no fat, negligible calories)

**Binding cap:** 55 (PROCESSING_LOAD stricter than SWEETENER cap of 70)

---

### Section C — Dimension Trace — THE STRUCTURAL EMPTINESS PARADOX

| Dimension | Weight | Score | Commentary |
|-----------|--------|-------|------------|
| **Calorie Density** | **15%** | **95** | ≤10 kcal/100ml in beverage table → maximum score. **The most-weighted dimension scores this product near-perfectly.** |
| Processing Quality | 15% | ~12 | NOVA 4, heavy additive burden |
| Nutrient Density | 15% | ~0 | Zero protein, zero fiber, zero nutrients |
| Glycemic Quality | 12% | ~92 | Zero sugar — dimension scores excellently |
| Protein Quality | 10% | ~15 | Zero protein |
| Additive Quality | 10% | ~15 | 5 additive markers including 2 sweetener types |
| Satiety Support | 6% | ~15 | Zero protein, zero fiber |
| Fat Quality | 8% | ~90 | Zero fat — dimension scores very well |
| Regulatory Quality | 5% | ~80 | No red labels |
| Whole Food Integrity | 4% | ~5 | NOVA 4 synthetic beverage |

**Weighted dimension score:** ~44
(0.15×95=14.25 + 0.15×12=1.8 + 0.15×0=0 + 0.12×92=11.04 + 0.10×15=1.5 + 0.10×15=1.5 + 0.06×15=0.9 + 0.08×90=7.2 + 0.05×80=4.0 + 0.04×5=0.2 = 42.4)

**The calorie density dimension (14.25) is the single largest contributor to the final score for Coke Zero.** The glycemic quality dimension (11.04) and fat quality dimension (7.2) also contribute positively — all three of these are rewarding the absence of macronutrients in a product that is nutritionally absent.

---

### Section D — Guardrail Trace

- Binding cap: 55
- Dimension score: 42
- min(42, 55) = 42 — **cap does not bind** (score already below cap)
- Penalties: 0 (no penalty rules fire — no sugar, no sodium, no seed oil, no long ingredient list [8 ingredients])
- **Final score: ~42. Grade D.**

**The NOVA 4 cap and sweetener cap both fail to bind.** The score of 42 comes entirely from the dimension scoring — specifically, from the dimension scores producing a result that is already below the cap. The guardrail layer is analytically irrelevant for this product because dimension-level penalties from NOVA 4 and additive burden already suppress the score.

**But here is the paradox:** the score of 42 is produced by two competing forces that cancel each other: positive scores from calorie density (95), glycemic quality (92), and fat quality (90) are fighting against near-zero scores from processing quality (12), nutrient density (0), and whole food integrity (5). The result is a false averaging effect — the 42 does not mean Coke Zero is a mediocre food. It means the scoring system produces a number that is the algebraic average of "very good at having no calories" and "terrible at being food."

---

### Section E — Category Stability

**Primary:** `beverage` — 0.97 confidence. No meaningful alternative. Score instability: minimal.

---

### Section F — User Explanation Simulation

> **Score: 42 — Grade D**
> Ultra-processed. Contains non-nutritive sweeteners. No nutritional content.
> Category: Beverages.

**Is this honest?** Partially. The grade D is defensible. But the explanation cannot say "calorie density: excellent" while also saying "no nutritional content" — these signals point in opposite directions for opposite reasons, and the averaging is invisible to the user.

**The honest explanation requires a concept the architecture doesn't have:** "This product contains no nutritional structure. Its score reflects its processing burden. Calorie density signal is not applicable to a nutritionally empty product."

---

### Section G — Failure Analysis

1. **Strongest:** Processing quality and additive quality correctly identify the engineered nature of this product.
2. **Weakest:** The calorie density dimension is the product's single biggest score contributor at 14.25 points. This dimension is rewarding the product for having no calories — which is the mechanism of structural emptiness, not a quality signal.
3. **Philosophically inconsistent:** Coke Zero's score of 42 is higher than plain rice cakes (estimated ~55) would initially seem to imply, and close to instant noodles (estimated ~24-32). Whether this relative ordering makes sense depends on how you weight nutritional emptiness vs. nutritional harm.
4. **Gaming risk:** A manufacturer who adds nutritional content to avoid the nutrient density penalty would score *higher* on BSIP2 while adding processed protein or sugar. The score incentivises some nutrient additions that are not genuine quality improvements.
5. **Score reflects:** Additive skepticism fighting calorie moderation in a draw. The calorie dimension is the system's primary analytical frame and it produces a paradoxical result here.

---

## PRODUCT 8 — Diet Chocolate Mousse

### Section A — Product Context

**Expected intuitive outcome:** Grade D. Heavily engineered, multiple sweeteners, high additive burden. Should clearly score worse than plain yogurt and worse than dark chocolate.

**Why adversarial:** Low calorie density (60 kcal/100g in the dessert category) scores the calorie dimension at 85/100. Three sweeteners trigger the sweetener cap. NOVA 4 triggers the processing cap. But all caps may be non-binding if dimension scoring already places the product below the caps. The structural emptiness paradox is present but less extreme than Coke Zero.

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 60 kcal | Protein: 4g | Fat: 2g | Sat fat: 1g | Carbs: 8g | Sugar: 4g | Fiber: 1g | Sodium: 80mg
- Ingredients: water, skimmed milk powder, cocoa powder, modified corn starch, acesulfame K, aspartame, sucralose, soy lecithin, carrageenan, xanthan gum, mono- and diglycerides, natural flavoring (~13 ingredients)
- NOVA: 4 | Additive markers: 3 sweeteners + soy lecithin + carrageenan + xanthan gum + mono/diglycerides + modified starch → 7-8 markers

**L4 — Interpreted concerns:**
- PROCESSING_LOAD:
  - NOVA 4: cap 60
  - ADDITIVE_MARKERS_5_PLUS: 7+ markers → cap 55
  - Coordination: **cap 55**
  - LONG_INGREDIENT_LIST: 13 > 12 → penalty −4
- SWEETENER_PRESENT: 3 sweeteners → independent cap 70
- No sugar, calorie-load, or sodium rules fire
- Binding cap: **55** (processing stricter than sweetener)

---

### Section C — Dimension Trace

| Dimension | Weight | Score | Commentary |
|-----------|--------|-------|------------|
| Calorie Density | 15% | **85** | 60 kcal in dessert table (≤150 → 85). **Paradox repeats.** |
| Processing Quality | 15% | 12 | NOVA 4 |
| Nutrient Density | 15% | 35 | Some protein (4g) from milk powder, minimal fiber |
| Glycemic Quality | 12% | 70 | Low sugar but modified starch; uncertain glycemic profile |
| Protein Quality | 10% | 45 | Protein present but from milk powder concentrate context |
| Additive Quality | 10% | 8 | 3 sweeteners + multiple emulsifiers + stabilizers |
| Satiety Support | 6% | 35 | Some protein, minimal fiber |
| Fat Quality | 8% | 85 | Very low fat |
| Regulatory Quality | 5% | 80 | No red labels |
| Whole Food Integrity | 4% | 5 | NOVA 4 reconstruction |

**Weighted dimension score:** ~47
(12.75 + 1.8 + 5.25 + 8.4 + 4.5 + 0.8 + 2.1 + 6.8 + 4.0 + 0.2 = 46.6)

---

### Section D — Guardrail Trace

- Binding cap: 55
- min(47, 55) = 47 — **cap does not bind** (score already below 55)
- Penalties: −4 (LONG_INGREDIENT_LIST)
- **Final score: 47 − 4 = 43. Grade D.**

**The caps (55 and 70) are both non-binding.** The score of 43 is produced by the dimension scoring system, not the guardrail layer. The sweetener cap and processing cap are informationally irrelevant for this product.

**The guardrail layer is doing nothing here.** This is an architectural anomaly: a product with three synthetic sweeteners and NOVA 4 classification escapes all hard caps because the dimension scoring already suppresses the score below those caps.

---

### Section E — Category Stability

**Primary:** `dessert` — confidence ~0.82
**Secondary:** `dairy_protein` — if milk powder content is seen as primary

Secondary trace with `dairy_protein`:
- 60 kcal → ≤80 kcal → calorie density score: 90 (slightly higher than 85 in dessert)
- Score difference: trivial (~0.75 points)
- **Score instability: minimal.** Category is not decisive here.

---

### Section F — User Explanation Simulation

> **Score: 43 — Grade D**
> Ultra-processed. Very high additive complexity. Contains three non-nutritive sweeteners.
> Category: Desserts & confectionery.

**Is this honest?** Mostly. The score is right. But again: the calorie dimension score of 85 is the second-largest contributor to the final score (12.75 points). The user's experience of "this is a diet product and BSIP2 likes the low calories" would be partially correct — and that is wrong. Low calories should not be a standalone quality signal.

---

### Section G — Failure Analysis

1. **Strongest:** Additive quality dimension correctly scores this very low (0.8 contribution). The NOVA 4 processing quality is correctly terrible.
2. **Weakest:** The caps don't bind. The sweetener cap at 70 is supposed to be a meaningful guardrail — but at this level of NOVA 4 and additive burden, the dimension scoring is already below 70. The sweetener cap has no effect on this product.
3. **Philosophically inconsistent:** A product with three synthetic sweeteners has a stronger sweetener presence than a product with one. The `SWEETENER_PRESENT` cap is binary — it doesn't distinguish. Three sweeteners = same effect as one sweetener. The additive quality dimension captures some of this gradient, but the regulatory signal doesn't.
4. **Gaming risk:** A manufacturer can add a second or third sweetener to improve taste profile without any additional scoring penalty. The sweetener signal is already at its maximum for the first sweetener.
5. **Score reflects:** Additive skepticism and processing ideology, but partially undermined by calorie moderation inadvertently rewarding structural emptiness.

---

## PRODUCT 9 — Plain Greek Yogurt (Full Fat)

### Section A — Product Context

**Expected intuitive outcome:** Grade A or strong B. The reference high-quality dairy product. Strong protein, clean ingredient list, fermented.

**Why adversarial:** Full-fat Greek yogurt has ~5g fat and ~3.5g saturated fat per 100g. The sat fat dimension penalty applies. The question is whether the dimension penalty creates meaningful drag or whether the overall profile is strong enough to absorb it cleanly.

**Architectural tensions activated:**
- Saturated fat dimension penalty on a whole fermented dairy food
- Whether fermentation is credited (currently: no)
- Whether the score correctly lands just below A (as it should) or unnecessarily drops to mid-B

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 100 kcal | Protein: 10g | Fat: 5g | Sat fat: 3.5g | Carbs: 4g | Sugar: 4g (lactose) | Fiber: 0g | Sodium: 50mg
- Ingredients: milk, cream, live cultures (3 ingredients)
- NOVA: 2 (fermented; pasteurised)
- No Israeli red labels (3.5g sat fat below threshold; 4g sugar far below threshold)

**L3 — Inferred classifications:**
- Category: `dairy_protein` — very high confidence (~0.93)
- NOVA: 2 — high confidence
- HP patterns: HP_FAT_SODIUM_COMBO requires sodium≥300mg; sodium=50mg → does NOT fire. HP_FAT_SUGAR_COMBO requires sugar≥20g; sugar=4g → does NOT fire. **No HP patterns.**
- Sweetener: absent

**L4 — Interpreted concerns:** No guardrail rules fire. Not one.

---

### Section C — Dimension Trace

| Dimension | Weight | Score | Commentary |
|-----------|--------|-------|------------|
| Processing Quality | 15% | 88 | NOVA 2 — fermentation is not credited, but NOVA 2 avoids all processing caps |
| Nutrient Density | 15% | 85 | Strong: 10g protein, dairy micronutrients; zero fiber is the gap |
| Calorie Density | 15% | 80 | 100 kcal → dairy_protein table ≤130 → 80 |
| Glycemic Quality | 12% | 82 | Low sugar, no added sugars; lactose is natural |
| Protein Quality | 10% | 88 | High protein from whole dairy source |
| Additive Quality | 10% | 97 | No additives |
| Satiety Support | 6% | 70 | Strong on protein; zero fiber is a genuine satiety gap |
| Fat Quality | 8% | ~68 | Sat fat 3.5g → dimension penalty: −max((3.5−2)×4,0) = −6; otherwise dairy fat profile is reasonable |
| Regulatory Quality | 5% | 95 | No red labels |
| Whole Food Integrity | 4% | 92 | 3 ingredient NOVA 2 |

**Weighted dimension score:** ~84
(13.2 + 12.75 + 12.0 + 9.84 + 8.8 + 9.7 + 4.2 + 5.44 + 4.75 + 3.68 = 84.4)

---

### Section D — Guardrail Trace

**No guardrail rules fire. No caps, no penalties.**

**Final score: ~84. Grade B (high).**

The score of 84 correctly lands just below A (85) due to three genuine tradeoffs: moderate calorie density (not the lowest in dairy_protein), zero fiber (satiety gap), and saturated fat dimension penalty. All three are analytically real. The explanation is honest.

---

### Section E — Category Stability

**Primary:** `dairy_protein` — 0.93 confidence
**Secondary:** `default` — if product lacks clear dairy signals

Secondary trace with `default`:
- 100 kcal → ≤150 → calorie density score: 90 (vs. 80 in dairy_protein)
- Score slightly HIGHER in default by ~1.5 points. No catastrophe.
- Score instability: minimal.

Greek yogurt is one of the most category-robust products in this workshop.

---

### Section F — User Explanation Simulation

> **Score: 84 — Grade B**
> Good overall profile. High protein from whole dairy source. Simple ingredient list. Minimal processing.
> Tradeoffs: No fiber content (modest satiety gap). Moderate saturated fat from dairy fat.
> Category: Dairy & protein.

**Is this honest?** Yes. This is the best explanation produced by the architecture in this workshop. Every signal is real, traceable, and proportionate. The tradeoffs are genuine and the user is left with correct information. This is BSIP2 behaving as a food structure interpretation tool.

---

### Section G — Failure Analysis

1. **Strongest:** Everything. This product is the workshop's cleanest trace. All signals align. The score is correct for the right reasons.
2. **Weakest:** Fermentation is not credited. Greek yogurt earns its score despite fermentation, not because of it. The positive properties of fermentation (protein bioavailability improvement, probiotic culture presence, lactose reduction) are invisible to the scoring system. This is a known limitation, not a contradiction.
3. **Philosophically consistent:** Greek yogurt reveals what the architecture is capable of when the product fits its assumptions. The score is explainable in three signals without reference to any rule identifier.
4. **Gaming risk:** Negligible for a genuine food like this.
5. **Score reflects:** Food structure recognition — the single example in this workshop where the score reflects what the product delivers rather than what rules it avoids.

---

## PRODUCT 10 — Instant Noodles

### Section A — Product Context

**Expected intuitive outcome:** Grade D or E. High sodium, NOVA 4, palm oil, refined carbs, minimal whole-food character. Should score clearly in the bottom tier.

**Why adversarial:** The sodium level (1,500mg/100g including seasoning) fires the highest sodium cap. NOVA 4 fires the processing cap. Sat fat red label may fire. HP_FAT_SODIUM_COMBO fires. But calorie-load rules may NOT fire — protein at ~9g/100g is just above the 8g threshold for HIGH_CAL_LOW_SATIETY_SOFT, and calories at 450 kcal are just at the edge of the calorie threshold. Near-threshold behavior test.

**Architectural tensions activated:**
- Near-threshold calorie-load rules (kcal=450, protein=9g)
- Cumulative penalty stacking — whether final score is analytically reasonable
- HP_FAT_SODIUM_COMBO on a legitimately engineered product (correct HP fire vs. whole-food misfires)

---

### Section B — Signal Trace

**L1 — Observed facts:**
- Energy: 450 kcal | Protein: 9g | Fat: 18g | Sat fat: 8g | Carbs: 62g | Sugar: 2g | Fiber: 2g | Sodium: 1,500mg
- Ingredients: refined wheat flour, palm oil, salt, MSG, soy sauce powder, sugar, modified starch, caramel color, disodium guanylate, disodium inosinate, artificial flavors, sodium phosphates — 15 ingredients
- NOVA: 4 | Additive markers: MSG, modified starch, caramel color, disodium guanylate, disodium inosinate, sodium phosphates, artificial flavors → 7 markers
- Israeli red label: sat fat (8g — likely); sodium label may also apply

**L4 — Interpreted concerns:**

SUGAR_LOAD: 2g sugar → no rules fire

CALORIE_LOAD:
- `HIGH_CAL_LOW_SATIETY_SEVERE`: kcal=450 < 500 → does NOT fire (just below threshold)
- `HIGH_CAL_LOW_SATIETY_SOFT`: kcal=450 ≥ 450 AND protein=9g — protein threshold is <8g; 9g is NOT <8g → does NOT fire

**Both calorie-load rules avoid firing by near-threshold margins.** A product with 8g protein at 450 kcal would fire the soft rule. At 9g protein, it escapes. **This is a cliff-threshold near-miss.**

PROCESSING_LOAD:
- NOVA 4: cap 60
- ADDITIVE_MARKERS_5_PLUS: 7 markers → cap 55
- LONG_INGREDIENT_LIST: 15 > 12 → penalty −4
- Coordination: cap **55**

SODIUM_LOAD:
- `HIGH_SODIUM_700MG_PLUS`: 1,500mg → **FIRES: cap 60**
- `HP_FAT_SODIUM_COMBO`: fat=18×9/450=36% ≥ 25% AND sodium=1,500mg ≥ 300mg → **FIRES: penalty ~−6** (correctly fires — this IS engineered)

FAT_QUALITY:
- `ISRAELI_RED_LABEL_1` (sat fat): 8g → **FIRES: cap 55**
- `SEED_OIL_PRESENT`: palm oil → penalty −3

**All caps:**
- PROCESSING_LOAD: 55
- SODIUM_LOAD: 60
- FAT_QUALITY: 55
- Binding cap: **55**

**Total penalties:** PROCESSING −4, SODIUM −6 (HP), FAT_QUALITY −3 = **−13**

---

### Section C — Dimension Trace

| Dimension | Weight | Score |
|-----------|--------|-------|
| Calorie Density | 15% | 50 (450 kcal → default table ≤450 → 50) |
| Processing Quality | 15% | 12 (NOVA 4) |
| Nutrient Density | 15% | 30 (some protein, refined carbs, very low fiber) |
| Glycemic Quality | 12% | 55 (low sugar but refined wheat with minimal fiber) |
| Protein Quality | 10% | 40 (moderate protein but refned food context) |
| Additive Quality | 10% | 12 (7 additive markers) |
| Satiety Support | 6% | 35 (borderline protein, very low fiber) |
| Fat Quality | 8% | 15 (8g sat fat; palm oil; dimension score very low) |
| Regulatory Quality | 5% | 30 (sat fat red label; sodium signals) |
| Whole Food Integrity | 4% | 8 (NOVA 4, 15 ingredients, no whole food character) |

**Weighted dimension score:** ~34
(7.5 + 1.8 + 4.5 + 6.6 + 4.0 + 1.2 + 2.1 + 1.2 + 1.5 + 0.32 = 30.7)

---

### Section D — Guardrail Trace

- Binding cap: 55
- min(31, 55) = 31 — **cap does not bind**
- Penalties: −13
- **Final score: 31 − 13 = 18. Grade E.**

A score of 18 is extremely low. Like the sugary granola bar, penalties applied to an already-low dimension score push the result deep into Grade E. The cap was never binding — the dimension scoring did all the work, and the penalties compounded on a very low base.

**Critical near-miss observation:** If the protein had been 7g (not 9g), `HIGH_CAL_LOW_SATIETY_SOFT` would have fired, adding −6 more penalty. Score would have been 18 − 6 = 12. The difference between 7g protein and 9g protein is an additional 6 penalty points and 6 score points. **This is a gaming cliff.** A manufacturer reformulating to 9g protein (still very low) saves 6 score points.

---

### Section E — Category Stability

**Primary:** `default` — confidence ~0.60 (no noodle category exists)
**Secondary:** `cereal` — oat-equivalent grain structure

Secondary trace with `cereal`:
- 450 kcal → ≤480 → calorie density score: 40 (vs. 50 in default)
- Score drops ~1.5 points from dimension weighting change
- Score instability: minimal. All guardrail rules are category-independent.

---

### Section F — User Explanation Simulation

> **Score: 18 — Grade E**
> Ultra-processed. Very high additive complexity. High sodium: regulatory constraint applied. High saturated fat: regulatory warning. High fat-sodium concentration.
> Category: General food.

**Is this honest?** Yes — Grade E is correct. The active signal count is high (5+ signals), but the dominant drivers (NOVA 4, high sodium, high sat fat) are each individually clear. The explanation can be collapsed to three: ultra-processed, high sodium, high saturated fat.

---

### Section G — Failure Analysis

1. **Strongest:** Multiple rules correctly fire on a genuinely poor-quality product. The HP_FAT_SODIUM_COMBO correctly fires — this is an engineered sodium-fat combination, not a natural one.
2. **Weakest:** The score of 18 may be too extreme. Penalty stacking on a low base dimension score is creating scores in the bottom 20% of the scale for a product that arguably warrants Grade D (40–54), not deep Grade E.
3. **Gaming cliff:** The protein threshold for HIGH_CAL_LOW_SATIETY_SOFT is 8g. At 9g protein, the rule escapes. This is a trivially small reformulation to save 6 penalty points. The cliff is commercially meaningful.
4. **Near-miss curiosity:** Both `HIGH_CAL_LOW_SATIETY_SEVERE` (kcal<500) and `HIGH_CAL_LOW_SATIETY_SOFT` (protein≥8g) narrowly miss firing. Instant noodles at exactly the threshold values escape both calorie-load rules. The score is still Grade E from other rules — but the near-miss illustrates how threshold positioning creates arbitrary distinctions.
5. **Score reflects:** Punishment coordination engine — but correctly applied to a legitimately poor product. The concern is calibration (18 vs. 35), not direction.

---

## Consolidated Summary Table

| # | Product | Expected | Est. Score | Est. Grade | Floor/Cap Conflict? | HP Overreach? | Category Risk | Architecture Mode |
|---|---------|----------|------------|------------|---------------------|---------------|--------------|-------------------|
| 1 | Plain almonds | A | 88 | A | No | No | Low (floor protects) | Food structure recognition ✓ |
| 2 | Dates | B | 55–75 | C or B | **YES — critical** | No | Low | Punishment misfires |
| 3 | Coconut oil | B | 47–75 | D or B | **YES — critical** | No (but LOW_SATIETY misfire) | Low | Rule misfires |
| 4 | Brined olives | B–C | 54–65 | D or C | **YES** | **YES** | Low | Punishment misfires |
| 5 | Date-nut bar | B | 49–65 | D or C | **YES** | **YES** | Moderate (masked by cap) | Punishment misfires |
| 6 | Sugary granola bar | D–E | ~15–28 | E | No | No (legitimate) | Low | Punishment engine ✓ (excessive?) |
| 7 | Coke Zero | D–E | ~42 | D | No | No | Minimal | Paradox (calorie dimension) |
| 8 | Diet mousse | D | ~43 | D | No | No | Low | Caps don't bind |
| 9 | Greek yogurt | A–B | ~84 | B | No | No | Low | Food structure recognition ✓ |
| 10 | Instant noodles | D–E | ~18 | E | No | No (legitimate) | Low | Punishment engine (excessive?) |

---

## Floor vs. Cap Resolution Addendum

The architecture specification leaves the floor-cap conflict unresolved for four products. Both resolutions are stated for each:

| Product | Cap | Floor | If floor wins | If cap wins |
|---------|-----|-------|---------------|-------------|
| Dates | 55 | 75 (NOVA 1) | B — philosophically correct | C — analytically consistent but wrong |
| Coconut oil | 47 (post-penalty) | 75 (NOVA 1) | B — protects whole food | D — misfiring rules punish a pure fat |
| Brined olives | 54 (post-penalty) | 65 (NOVA 2 WFF) | C — defensible | D — context-limited product over-punished |
| Date-nut bar | 49 (post-penalty) | 65 (NOVA 2 WFF) | C — correct for a whole-food bar | D — same as sugary granola bar after floor fails |

**The floor-cap resolution is the single most important architectural decision required before implementation.** Every other problem in this workshop is a calibration or refinement issue. This one is a specification gap that will produce different results depending on how the engineer implementing it decides to resolve the ambiguity.
