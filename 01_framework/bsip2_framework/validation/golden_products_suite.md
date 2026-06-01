# Golden Products Suite

**Purpose:** Define canonical reference products that BSIP2 must handle correctly. These products function as a test suite for conceptual consistency. If the system produces a result that violates the expected qualitative behavior described here, it is evidence of a scoring problem — not a judgment about the product.

Exact scores are NOT assigned here. This document defines expected analytical behavior. Precise scoring will be calibrated against real product data in a later phase.

---

## How to read this document

Each entry describes:
- **Expected qualitative behavior** — high / medium / low / nuanced, with reasoning
- **Why** — the specific analytical properties that drive the expected outcome
- **Dangerous scoring trap** — what the system must avoid doing for this product

---

## SHOULD SCORE HIGH

These products should reach grade A or high-B territory. If they score C or lower, something is wrong with the system.

---

### Plain almonds (raw, unsalted)

**Expected behavior:** High — grade A or strong B. Near-maximum whole-food score.

**Why:** Single NOVA 1 ingredient. Whole-food fat source. Protein, fiber, micronutrient contribution from a whole matrix. No additives, no added sugar, no processing signals. The whole-food floor (minimum 75 for NOVA 1) applies.

**Dangerous trap:** Calorie density. Almonds at ~580 kcal/100g would be catastrophically over-penalised if evaluated against snack bar or default category thresholds. The `whole_food_fat` category classification is load-bearing for this product. Category misclassification is the primary failure risk.

---

### Pure tahini (100% sesame, no additives)

**Expected behavior:** High — grade A. Similar to plain almonds.

**Why:** Single-ingredient whole food. High fat from sesame matrix. Calcium, protein, polyunsaturated fats. No NOVA processing signals, no additives, no sugar.

**Dangerous trap:** Sodium — sesame naturally contains low sodium, so this shouldn't be an issue. The real risk is calorie density scoring if miscategorised as `sauce_spread` rather than `whole_food_fat`. A 600 kcal/100g tahini would score poorly on the `sauce_spread` calorie table; it should score well on the `whole_food_fat` table.

---

### Plain Greek yogurt (full-fat, no additives)

**Expected behavior:** High — grade A or strong B. Strong dairy_protein category result.

**Why:** Whole-food protein source. NOVA 1–2 (pasteurised, cultured). High protein per 100g. Minimal ingredients (milk, live cultures). No additives, no added sugar, no sweeteners.

**Dangerous trap:** Fat content may generate a fat quality concern depending on saturated fat levels. Full-fat Greek yogurt at 5–8g saturated fat/100g is in the zone where the dimension penalty applies. The score should still be high because the other dimensions (protein quality, processing quality, nutrient density) are very strong — but the fat quality dimension should create a visible tradeoff signal, not a hard cap.

---

### Plain oats (rolled oats, minimally processed)

**Expected behavior:** High — grade A or strong B.

**Why:** Whole grain. Low sugar. Fiber-rich. NOVA 1. Calorie density of ~380 kcal/100g sits at the boundary of the `cereal` category table (scores ~70 at that level). Overall strong across most dimensions.

**Dangerous trap:** Category classification. Oats sold in a context that makes them appear as a `snack_bar_granola` product would face much stricter thresholds. Also: if evaluated without the whole-grain signal, the processing and glycemic quality dimensions may not correctly credit the structural carbohydrate contribution.

---

### Plain cottage cheese (low-fat)

**Expected behavior:** High — grade A or strong B.

**Why:** High protein, low calorie density, minimal processing, no additives. Strong `dairy_protein` category profile.

**Dangerous trap:** Sodium. Cottage cheese typically carries 300–400mg sodium/100g. This is below the `HIGH_SODIUM_700MG_PLUS` guardrail threshold, but the sodium dimension should still create some signal. The system must not fail to score cottage cheese well simply because it has moderate sodium — sodium at this level is context-appropriate.

---

## SHOULD SCORE MEDIUM

These products should land in grade B or C territory. If they score A, the system is too lenient. If they score D or E, the system is too punitive.

---

### Hummus (chickpeas, tahini, olive oil, salt, lemon)

**Expected behavior:** Medium-high — grade B. A well-formulated hummus should be clearly above mediocre.

**Why:** Primarily whole-food ingredients. Meaningful protein and fiber from chickpeas. Fat from whole-food sources (tahini, olive oil). Moderate calorie density for a spread (~200–350 kcal/100g). NOVA 2 (mixed/ground, not chemically processed).

**Dangerous trap:** Sodium. Commercial hummus often carries 300–500mg sodium/100g — this is borderline on the sodium dimension. If the sodium dimension scores conservatively and the `sauce_spread` calorie table is applied, the combined effect should still leave hummus in B territory. The system must not push hummus below C; that would be analytically indefensible.

---

### Dark chocolate, 85% cacao

**Expected behavior:** Medium — grade B or upper C. Genuine tradeoff product.

**Why:** High fat from cacao butter (whole-food fat source). Meaningful fiber from cacao solids. Minimal sugar at 85% cacao. However: significant calorie density (~600 kcal/100g), saturated fat contribution, often NOVA 2–3. The `dessert` category is the appropriate context.

**Dangerous trap:** The system should not rate 85% dark chocolate the same as milk chocolate or confectionery bars. The key differentiation is: low sugar, whole-food fat source, meaningful fiber. The calorie density and saturated fat should create visible tradeoffs but should not produce a low score. If dark chocolate 85% scores D or E, the whole-food fat source signal is not registering correctly.

---

### Flavored Greek yogurt (with fruit puree, added sugar)

**Expected behavior:** Medium — grade B or C, depending on sugar content.

**Why:** Strong protein base from the dairy component. Added sugar and fruit puree push the glycemic quality dimension down. Likely NOVA 3 (added ingredients, flavouring). Good on protein and satiety signals; weaker on glycemic and processing.

**Dangerous trap:** The system should clearly differentiate between a flavored yogurt with 8g added sugar and one with 22g added sugar. Both may be in the same category but should produce meaningfully different scores. If the system collapses them into the same grade, the discrimination is insufficient.

---

### Oat milk (plain, no additives)

**Expected behavior:** Medium — grade B or C.

**Why:** Liquid format → strict beverage calorie thresholds. Relatively low calorie for a beverage (~40–50 kcal/100ml). Processed (NOVA 3: oats are processed, homogenised, fortified in most commercial versions). Lower protein than dairy. Often fortified with calcium and vitamins (which the current system does not heavily credit).

**Dangerous trap:** Fortification. The system should not penalize oat milk for having added vitamins (fortification is not the same as problematic additives). If the fortification is picked up as additive markers, the score will be unfairly depressed. Oat milk with only oats, water, salt, and added calcium should not face the same additive penalty as a product with six emulsifiers.

---

### Rice cakes (plain, unsalted)

**Expected behavior:** Medium — grade B or C.

**Why:** Very low calorie density (~380 kcal/100g dry weight, but typically eaten in small quantities). Low protein. Low fiber. NOVA 2 (processed grain, no additives). Not a nutritionally rich food but not a problematic one either. The calorie density score will depend on category — rice cakes are not a good fit for any of the eight categories without a `default` fallback.

**Dangerous trap:** If rice cakes are evaluated against the `default` calorie table, ~380 kcal/100g earns a score of 65 — reasonable. The low satiety signals (low protein, low fiber) should create a visible negative dimension without triggering the high-calorie-low-satiety guardrail (which requires ≥ 500 kcal). The system should represent rice cakes as nutritionally minimal but not harmful.

---

### Peanut butter (with added sugar and palm oil)

**Expected behavior:** Medium — grade B or upper C, below pure nut butter.

**Why:** Peanut base provides whole-food fat, protein, fiber. Added sugar and palm oil degrade the profile: sugar adds glycemic concern; palm oil is a lower-quality fat source compared to peanut's native fat. NOVA 3. The score should clearly sit below a pure peanut butter with no additives — and the system should make the reason visible.

**Dangerous trap:** The system should not rate commercial peanut butter with sugar/oil the same as plain tahini or plain almond butter. The added sugar is the primary differentiator: if ≥ 8g/100g, the glycemic quality dimension takes a visible hit. If ≥ 15g/100g with sufficient calorie density, interaction rules may apply. The system must produce a lower score than the pure version without producing an absurdly low one.

---

## SHOULD SCORE LOW

These products should land in grade D or E territory. If they score C or above, the system is too lenient for genuinely problematic products.

---

### Coke Zero / Diet Cola (zero-calorie sweetened cola)

**Expected behavior:** Low — grade D or E.

**Why:** Non-nutritive sweetener triggers the `SWEETENER_PRESENT` cap (≤ 70). But Coke Zero also carries no nutritional value, no protein, no fiber, no beneficial components. The beverage calorie scale scores at 95 for near-zero calories — but the sweetener cap overrides this. Multiple sweeteners (typically aspartame + acesulfame K) may trigger additional additive concern. NOVA 4.

**Dangerous trap:** The beverage calorie dimension scoring very high and creating a misleadingly positive dimension contribution. The sweetener cap should prevent a high final score, and the NOVA 4 processing cap reinforces this. The dimension breakdown should clearly show high calorie density score offset by additive and processing concerns.

---

### Sugary granola bar (high sugar, high calorie, multiple additives)

**Expected behavior:** Low — grade D or E. The canonical health-halo failure product.

**Why:** This is exactly what the `snack_bar_granola` category rules are designed to identify. High calorie density (≥ 430 kcal/100g), significant sugar (≥ 15g/100g), glucose syrup, palm oil, multiple additives. Multiple guardrail rules fire. The health-halo cap (≤ 70 for ≥ 430 kcal), sugar-load rules, and possibly processing rules all converge.

**Dangerous trap:** The scoring system should not let a high-protein granola bar with these properties score medium simply because its protein dimension is strong. The structural concerns are primary; one strong dimension should not rescue a product with multiple hard caps and penalties.

---

### Instant noodles (heavily processed, high sodium, refined starch base)

**Expected behavior:** Low — grade D or E.

**Why:** NOVA 4. High sodium (typically 800–1400mg/100g for the product including seasoning). Refined carbohydrates with minimal fiber. Low protein. No meaningful micronutrient density. Low satiety signals. Multiple additive markers likely.

**Dangerous trap:** The sodium alone should trigger the `HIGH_SODIUM_700MG_PLUS` cap (≤ 60). Combined with the processing cap (NOVA 4, ≤ 60) and low satiety penalty, the product should comfortably score below 55. The system must not let a moderate calorie density profile (typically ~400–450 kcal/100g dry) pull the score toward medium; the combination of processing, sodium, and low satiety is decisive.

---

### Fruit juice (100%, no added sugar)

**Expected behavior:** Low-medium — grade D. Even 100% fruit juice should not score highly.

**Why:** Natural sugar content of juice (~10–12g/100ml) at beverage calorie density (~45 kcal/100ml). The beverage category applies strict calorie thresholds. More significantly: juice lacks the fiber present in whole fruit; it delivers sugar in a rapidly absorbable liquid form. The system should not reward "no added sugar" in a product where the structural concern is intrinsic sugar in liquid form.

**Dangerous trap:** "100% fruit juice" language should not cause the system to credit this as a whole-food product. It is not — it is a processed product (NOVA 2–3) that has removed the structural fiber. The score should be noticeably lower than for whole fruit and clearly below medium.

---

## SHOULD BE NUANCED / CONTENTIOUS

These products represent genuine analytical tradeoffs. The system must produce a score that reflects the complexity rather than collapsing to a simple verdict. The qualitative behavior is specific: the score should be in B–C range AND the dimension breakdown should make the tradeoff visible.

---

### Protein pudding with sweeteners (high protein, high additives)

**Expected behavior:** Contentious — grade B or C. Strong protein signal offset by sweetener cap and additive burden.

**Why:** A product with 15–20g protein per 100g in `dairy_protein` context represents a genuine nutritional contribution. But sweeteners trigger the ≤ 70 cap and NOVA 4 processing applies a processing cap. The result should be a product that cannot grade above B regardless of its protein strength — and the UI should make both the protein positive and the sweetener/processing negatives visible.

**Dangerous trap:** Either extreme is wrong: a score of 80+ ignores the sweetener and processing concerns; a score of 35 ignores the genuine protein contribution. The system must land in a range that forces the user to see both signals. This is the canonical test for whether BSIP2 can communicate a tradeoff rather than a verdict.

---

### Whey protein isolate powder

**Expected behavior:** Contentious — grade C or D for the powder format; stronger in `dairy_protein` context if used as supplementation.

**Why:** High protein from isolate — the `protein_isolate` marker fires (protein quality dimension penalty). Often carries sweeteners, flavourings, additives. NOVA 4. But delivers genuine protein density. The processing and additive burden is severe; the protein delivery is real.

**Dangerous trap:** Protein isolate powders are frequently evaluated out of context. The system should not produce a high score for a product that is heavily engineered simply because its protein number is large. The processing cap, sweetener cap, and protein isolate penalty should combine to place this comfortably below grade A. But it should not score E — the protein contribution is analytically real.

---

### Baby food puree (plain, single-ingredient)

**Expected behavior:** High for analytical quality, but with a confidence/context note.

**Why:** Plain baby food (e.g. mashed carrots, apple puree, pure vegetable) is minimally processed, no additives, no sugar, NOVA 1. It should score well analytically. However: serving size, calorie density per 100g, and purpose context are all different from adult food. A carrot puree at 35 kcal/100g scores near 95 on the beverage/default calorie scale; that is analytically accurate but may be uninformative for this product type.

**Dangerous trap:** The system should not produce an analytically wrong result for baby food. The whole-food NOVA 1 floor protects it. The issue is contextual usefulness rather than analytical accuracy. This product type exposes a limitation: BSIP2 evaluates nutritional structure per 100g and is not currently designed to evaluate age-specific nutrition needs.

---

### Dates (whole, dried)

**Expected behavior:** Contentious — grade B or upper C despite high sugar content.

**Why:** Whole fruit. NOVA 1. High natural sugar (~60–65g/100g total sugars) but from a whole-food matrix with fiber, minerals, and micronutrients intact. The fiber (6–8g/100g) moderates the glycemic concern. No additives, no processing, no industrial sugar addition.

**Dangerous trap:** High sugar content may trigger `HIGH_SUGAR_25G_PLUS` (cap at 60) even though the sugar is entirely natural and present in a fiber-rich whole-food matrix. The whole-food floor (minimum 75 for NOVA 1) should override this — but the interaction between the cap and the floor needs to be tested. If the floor doesn't protect dates, the system is failing to distinguish between added sugar and natural whole-food sugar, which is a fundamental analytical error.

---

### Ultra-processed vegan meat substitute

**Expected behavior:** Contentious — grade C or D. Processing concerns visible but protein contribution real.

**Why:** NOVA 4 by definition. High additive burden (binders, emulsifiers, flavourings, colourings). High processing. But often high protein (from soy or pea protein isolate). Sodium varies widely. The product challenges the system's ability to score ultra-processed but protein-rich products.

**Dangerous trap:** A vegan meat substitute with 20g protein and severe processing concerns should not score higher than a whole-food product with less protein. The NOVA 4 cap (≤ 60), additive caps, and protein isolate penalty should combine to place it in C territory, regardless of the protein number. If protein alone lifts it into B, the system is being gamed by a single dimension.

---

### Breakfast cereal with fortification (high sugar, added vitamins)

**Expected behavior:** Low-medium — grade C or D. Fortification should not rescue a product with high sugar.

**Why:** The classic health-halo product. A cereal with 28g sugar/100g, added B vitamins, and added iron presents as nutritious through marketing. Analytically: high sugar triggers glycemic quality dimension penalties and potentially `HIGH_SUGAR_25G_PLUS` cap. The vitamins are added post-processing (NOVA 4 typically). The current system does not credit fortification as a meaningful positive signal — this is intentional.

**Dangerous trap:** The system should not produce a high score because the vitamin content is impressive. Fortification with vitamins after stripping nutritional value through ultra-processing is not nutritional quality improvement — it is remediation of processing damage. If the system cannot hold a high-sugar fortified cereal to grade C or D, it is vulnerable to fortification-washing.
