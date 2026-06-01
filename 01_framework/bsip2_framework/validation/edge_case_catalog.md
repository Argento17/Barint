# Edge Case Catalog

**Purpose:** Capture products that stress-test BSIP2 assumptions. Each entry identifies which assumption the product challenges, which analytical dimensions conflict, which rules may collide, and what the system must avoid doing.

This is not a list of expected scores. It is a map of analytical stress points — places where the architecture is likely to be tested first and may fail in unexpected ways.

---

## Category 1 — High-fat whole foods

### Macadamia nuts (plain, raw)

**Assumption challenged:** Calorie density as a universal quality proxy.

**Macadamias at ~720 kcal/100g** represent near-maximum calorie density from a single-ingredient NOVA 1 whole food. The `whole_food_fat` category table accommodates this (≤ 750 kcal scores 65). But the system's interaction rules probe for high-calorie products in combination with other signals.

**Dimensions in conflict:** Calorie density quality (very high kcal) vs. processing quality (NOVA 1, excellent) vs. fat quality (primarily monounsaturated, positive). The dimension conflict should resolve correctly in favor of the whole-food matrix.

**Rules that may collide:** If macadamias are miscategorised into `default` (≤ 750 kcal → 35 points on the default table), the calorie density score collapses. The `HIGH_CAL_LOW_SATIETY_SEVERE` rule (≥ 500 kcal AND protein < 6g AND fiber < 3g) needs to be tested: macadamias have ~8g protein and ~9g fiber per 100g, so the threshold conditions may not be met, but this should be verified.

**What BSIP2 must avoid:** Scoring macadamias as D or E. The whole-food floor should protect against this; the category assignment is load-bearing.

---

### Coconut oil (pure, cold-pressed)

**Assumption challenged:** Fat quality is not simply a saturated fat proxy.

**Coconut oil is ~90% saturated fat** — the highest saturated fat content of any common food. The saturated fat dimension penalty formula (−max((sat_fat − 2g) × 4, 0)) would produce a very large negative value. However, coconut oil is a whole-food fat source (NOVA 1), single-ingredient, and is used in specific cultural and culinary contexts.

**Dimensions in conflict:** Fat quality (saturated fat penalty very large) vs. processing quality (NOVA 1, excellent) vs. whole-food integrity (maximum).

**Rules that may collide:** The saturated fat red label would fire at Israeli regulatory thresholds. `ISRAELI_RED_LABEL_1` for saturated fat routes to `FAT_QUALITY` concern family — cap at 55. The whole-food floor applies at minimum 65 for NOVA 1–2. When the cap and the floor conflict, the current architecture states that "confidence ceilings cannot be overridden by floor rules" — but the relationship between guardrail caps and whole-food floors is not the same as confidence ceilings vs. floors. This interaction needs explicit testing.

**What BSIP2 must avoid:** Treating coconut oil identically to palm oil or industrially hydrogenated fat. The processing distinction is real even if the saturated fat composition is superficially similar.

---

### Avocado-based spread (guacamole, 100% avocado)

**Assumption challenged:** `sauce_spread` category vs. `whole_food_fat`.

**Pure guacamole** from whole avocados sits at ~150–180 kcal/100g — moderate for a spread, excellent for a whole food. But its category classification is ambiguous: it could be `sauce_spread` or `whole_food_fat` depending on form factor.

**Dimensions in conflict:** No meaningful nutritional conflict. The conflict is entirely categorical.

**Rules that may collide:** None, if correctly classified. If classified as `sauce_spread`, the calorie density table is more conservative (≤ 150 kcal → 90 points; 150–180 would score lower). If classified as `whole_food_fat`, the table is very permissive. The difference in dimension score is meaningful.

**What BSIP2 must avoid:** Penalizing avocado-based products because of category ambiguity. The whole-food floor should provide a safety net, but the category should be correctly assigned by the classification engine.

---

## Category 2 — Low-calorie engineered foods

### Diet chocolate mousse (sweeteners, additives, 70 kcal/100g)

**Assumption challenged:** Calorie density as a positive quality signal.

**Low calorie does not mean high quality.** A mousse built from skimmed milk powder, modified starch, flavourings, three sweeteners, two emulsifiers, and stabilisers may score well on calorie density (~70 kcal → reasonable dessert score) while being a maximally engineered product.

**Dimensions in conflict:** Calorie density quality (positive) vs. processing quality (NOVA 4, cap at 60) vs. additive quality (multiple markers, cap at 55 or 65) vs. sweetener cap (≤ 70).

**Rules that may collide:** Multiple caps from different families. The concern coordination system handles caps within the same concern family, but caps from different families apply independently: NOVA cap + additive cap + sweetener cap all fire. The final score is determined by the strictest cap after all families are applied.

**What BSIP2 must avoid:** Producing a score above grade B for a product with six engineered additives simply because its calorie count is low. The sweetener cap (≤ 70) is the key safeguard here.

---

### Erythritol-sweetened snack bar (no sugar, high protein, all sweeteners)

**Assumption challenged:** Sugar-free = nutritionally better.

**Erythritol and monk fruit** are sometimes classified as natural sweeteners rather than synthetic ones. Depending on the BSIP2 marker detection for `SWEETENER_PRESENT`, these may or may not trigger the sweetener cap. The architectural question is: does the system correctly identify non-nutritive sweeteners regardless of whether they are synthetic or natural-derived?

**Dimensions in conflict:** Glycemic quality (no sugar — high score) vs. additive quality (sweetener presence — cap) vs. protein quality (high protein — positive) vs. processing quality (likely NOVA 4 — cap).

**Rules that may collide:** If erythritol is not in the sweetener marker list, the `SWEETENER_PRESENT` cap does not fire. The product would then score very high on glycemic quality and protein while avoiding the sweetener ceiling — potentially reaching A territory despite being a highly engineered product.

**What BSIP2 must avoid:** Producing an A grade for an engineered snack bar with multiple non-nutritive sweeteners because the marker detection missed them. The NOVA 4 classification should still apply a processing cap independently.

---

### Konjac jelly / zero-calorie glucose gel

**Assumption challenged:** What does BSIP2 do with a product that has essentially zero nutritional content?

**Konjac products** can have near-zero calories, near-zero protein, near-zero fat — but also near-zero concern signals. No sugar to flag, no fat to flag, no calorie density to flag. NOVA classification may be 3–4 (processing is significant). The product delivers essentially nothing — but scores could be misleadingly neutral or even high.

**Dimensions in conflict:** Calorie density (very low — high score), nutrient density (very low — low score), processing quality (moderate concern), satiety (zero protein, zero fiber).

**Rules that may collide:** The low satiety guardrail requires ≥ 450 kcal to fire — konjac products are below this threshold. None of the major calorie-based rules trigger.

**What BSIP2 must avoid:** Producing a misleadingly positive score for a food that delivers nothing. The nutrient density dimension should express the zero-nutrient nature, but the system currently has no specific mechanism to flag "nutritionally empty but not structurally problematic."

---

## Category 3 — Fortified foods

### Fortified breakfast cereal (whole grain base, added iron, B vitamins, sugar)

**Assumption challenged:** Does fortification improve analytical quality?

**The system explicitly does not credit post-processing fortification** as a positive nutritional signal. This is correct for engineered fortified products but needs testing against genuinely whole-grain products that also happen to be fortified.

**Dimensions in conflict:** Processing quality (whole grain is positive; fortification agent additives may create NOVA 3 signal) vs. nutrient density (fortification adds vitamins not measured in macros) vs. glycemic quality (added sugar in many fortified cereals).

**Rules that may collide:** If a cereal has whole grain, moderate sugar, and fortification only — no major guardrail rules should fire. But the `NOVA_PROXY_3_PROCESSED` cap (at 75) may apply if the fortification process is picked up as a processing indicator.

**What BSIP2 must avoid:** Penalizing a cereal's fortification in the processing dimension while also failing to credit it in the nutrient density dimension. The analytical inconsistency — penalizing the additives but not crediting the micronutrients they deliver — is a known limitation that should be explicitly acknowledged rather than accidentally producing a confused result.

---

### Infant formula (partially hydrolised whey, added DHA, vitamins, minerals)

**Assumption challenged:** BSIP2 was designed for consumer packaged food, not medical/specialist nutrition.

**Infant formula** would receive catastrophic analytical results under current rules: NOVA 4 (highly processed), multiple additives (vitamins, minerals, stabilisers), sweeteners sometimes present (lactose is present naturally; synthetic sweeteners sometimes added), and is specifically designed for an age group with completely different nutritional requirements.

**Dimensions in conflict:** Virtually all dimensions — the scoring architecture is inappropriate for this product type.

**Rules that may collide:** All processing caps would fire; all additive markers would fire; the satiety rules have no relevance; the calorie density scale is calibrated for adult foods.

**What BSIP2 must avoid:** Being applied to medical nutrition or infant formula at all. This edge case reveals the system boundary: BSIP2 should either (a) exclude medical nutrition product types from scope, or (b) return a clear "scope not applicable" signal rather than a misleadingly wrong score.

---

## Category 4 — Medical and sports nutrition

### Pre-workout powder (creatine, beta-alanine, caffeine, artificial flavours, sweeteners)

**Assumption challenged:** Product purpose vs. nutritional structure.

**Pre-workout formulations** are not designed as food — they are supplements. Their ingredient lists include compounds that have no analogue in the food analytical framework (creatine monohydrate, beta-alanine, citrulline). The additive marker detection, NOVA classification, and dimension scoring would produce outputs that are analytically meaningless for this product type.

**Dimensions in conflict:** All dimensions — the framework has no calibration for supplement products.

**What BSIP2 must avoid:** Producing an analytically coherent-looking score for a product that is outside the system's analytical scope. The confidence mechanism may help — missing nutritional fields (there may be no standard kcal/protein/carb breakdown) would reduce confidence severely. But the confidence mechanism alone is insufficient to prevent a misleading result if the data is present in some form.

---

### Electrolyte sports drink (sucrose, fructose, sodium, potassium)

**Assumption challenged:** High sugar in a specific performance context.

**Sports drinks** use specific carbohydrate and electrolyte ratios designed for performance use. Their sugar content (~6–8g/100ml) is intentional and context-specific. In BSIP2, the beverage calorie threshold and sugar rules do not distinguish between sugar for performance and sugar as dietary excess.

**Dimensions in conflict:** Glycemic quality (high sugar, negative) vs. purpose (sugar is the intended delivery mechanism).

**Rules that may collide:** `HIGH_SUGAR_25G_PLUS` will not fire at 6g/100ml. But the glycemic quality dimension will score this unfavorably. The beverage calorie table at 45 kcal/100ml scores ~70 — moderate.

**What BSIP2 must avoid:** Scoring a sports drink identically to a sugary soda. The sodium content (typically 400–600mg/L = 40–60mg/100ml) differentiates it from a soda. The specific electrolyte composition is not captured in the current analytical framework.

---

## Category 5 — Cultural foods

### Miso paste (fermented soybean, salt, koji)

**Assumption challenged:** High sodium in a fermented traditional food.

**Miso** contains 3,000–6,000mg sodium/100g — far above the `HIGH_SODIUM_700MG_PLUS` guardrail threshold. But it is a NOVA 1–2 fermented whole food used in very small quantities as a condiment or soup base. It is a traditional Japanese and broader Asian dietary staple with documented nutritional properties.

**Dimensions in conflict:** Sodium dimension (catastrophic by concentration) vs. processing quality (minimal, fermented) vs. whole-food integrity.

**Rules that may collide:** `HIGH_SODIUM_700MG_PLUS` fires (cap at 60). `HP_FAT_SODIUM_COMBO` may fire depending on fat content (miso has ~6g fat/100g — moderate). Sodium family budget clamp applies.

**What BSIP2 must avoid:** Producing a score below grade D for a traditional food that is consumed at tablespoon scale and has established nutritional benefits. The current architecture has no mechanism to account for serving-size-adjusted evaluation. This is a known limitation: the system evaluates per 100g, not per serving. Miso will score poorly by concentration metrics regardless of its actual dietary impact.

---

### Preserved olives (black or green, brined)

**Assumption challenged:** Sodium concentration in a whole food with traditional dietary role.

**Brined olives** carry 1,000–2,000mg sodium/100g — triggering the sodium guardrail and potentially the HP fat-sodium pattern (olives are ~15g fat/100g, ~10–20% of kcal). But olives are NOVA 1 or 2, whole food, with established health properties from their fat composition (primarily monounsaturated) and polyphenol content.

**Dimensions in conflict:** Sodium load (severe by concentration) vs. fat quality (excellent monounsaturated source) vs. whole-food integrity (maximum).

**Rules that may collide:** The whole-food floor (65 minimum for NOVA 1–2 whole food fat) should protect against the worst outcome. But the sodium cap at 60 conflicts with the whole-food floor at 65. The resolution between the floor and the cap is not explicitly specified in the current architecture for this combination.

**What BSIP2 must avoid:** Scoring brined olives below grade C. This edge case is an explicit test of the floor-vs-cap resolution mechanism.

---

### Tahini sesame butter vs. defatted sesame flour

**Assumption challenged:** Same ingredient, radically different nutritional profiles.

**Sesame-based products** span an enormous range: whole tahini (56% fat, ~600 kcal/100g) to defatted sesame flour (~18% fat, ~350 kcal/100g). Both may be classified similarly in NOVA and category terms, but their nutritional profiles are structurally different.

**What BSIP2 must handle:** The category and calorie table should handle the score gap correctly. The analytical concern is that the ingredient detection may see both as "sesame-based" without correctly accounting for the processing implied by defatting.

---

## Category 6 — Liquid meals

### Plant-based protein shake (commercial, sweetened, high protein)

**Assumption challenged:** Beverage format vs. meal replacement function.

**A 400ml protein shake** with 30g protein, 8g sugar, and multiple additives is evaluated per 100ml as a beverage. At 60 kcal/100ml it scores at the lower end of the beverage table. But its protein contribution is substantial — it functions as a partial meal replacement, not a beverage in the usual sense.

**Dimensions in conflict:** Calorie density (low for a meal, appropriate for a beverage) vs. protein quality (high, but from isolate) vs. processing quality (NOVA 4, likely).

**Rules that may collide:** Sweetener cap (if present). NOVA 4 cap. Protein isolate dimension penalty.

**What BSIP2 must avoid:** Scoring a 400ml, 30g protein shake lower than a 200ml juice that delivers only sugar. The beverage calorie table is calibrated for drinks, not meal replacements. This is a scope limitation that may require explicit acknowledgment.

---

## Category 7 — Hybrid products

### Protein bar made entirely from dates, oats, and almond butter (no added sugar, no additives)

**Assumption challenged:** `snack_bar_granola` category strictness applied to a genuinely clean product.

**A bar with 480 kcal/100g made entirely from dates, oats, and almond butter** falls into `snack_bar_granola` by form factor. The category health-halo cap fires at ≥ 430 kcal (cap at 70). NOVA 1 or 2 whole-food floor (minimum 65) also applies. The cap and the floor are close — the product ends up constrained in a narrow range.

**What BSIP2 must handle:** The dimension scores should clearly differentiate this product from a sugary bar at the same calorie density. The cap at 70 (from the snack bar health-halo rule) is the right call — but the reasoning should be visible: this product is capped not because it's problematic but because the category expectation for calorie density is strict. This is analytically defensible; it must be communicable.

---

## Category 8 — Products with incomplete data

### Product with energy, protein, carbs listed but no fiber, no sodium, no ingredient list

**Assumption challenged:** Confidence ceiling vs. score accuracy.

This represents a common real-world data quality scenario. The product has partial nutrition panel data.

**Confidence calculation:** Missing fiber (−5), missing sodium (−5), missing ingredient list (−25) = −35. Starting confidence of 100 becomes 65 — medium band. Score is not capped. But the NOVA classification cannot be derived without ingredients (missing), so NOVA confidence is low — up to −10 additional reduction. Final confidence may be ~55 — low band. Score capped at 70.

**What BSIP2 must handle:** The analytical result is directionally correct but incomplete. The confidence ceiling at 70 is appropriate. The UI must surface the data gap clearly.

---

## Category 9 — Health-halo products

### Coconut sugar (marketed as "natural", high-glycemic whole-food sugar)

**Assumption challenged:** "Natural" as an analytical category.

**Coconut sugar** has approximately the same glycemic index as regular sugar. It is less processed than white sugar (NOVA 2 vs. NOVA 1 for raw sugar, but still a concentrated sugar source). It is marketed with a health halo but delivers essentially the same glycemic burden as table sugar.

**What BSIP2 must handle:** Sugar is sugar by concentration. Whether it is "coconut" or "cane" or "beet" sugar, the glycemic quality dimension scores it at the same level for the same concentration. The system correctly does not have a "natural sugar" modifier that would exempt coconut sugar from the same rules as white sugar.

---

## Category 10 — Nutritionally good but heavily processed

### Protein-fortified quark with added calcium, inulin, and stevia (NOVA 4)

**Assumption challenged:** When does beneficial fortification become problematic additives?

**Quark fortified with protein concentrate, inulin (prebiotic fiber), calcium citrate, and stevia** may have genuinely excellent macros: 18g protein, 5g fiber from inulin, low sugar, 120 kcal/100g. But NOVA 4, sweetener cap at 70, and additive markers all fire.

**Dimensions in conflict:** Nutrient density (excellent) vs. processing quality (NOVA 4 cap) vs. sweetener (hard cap at 70).

**What BSIP2 must handle:** This product cannot score above B grade, and should not. The score should reflect a genuine tradeoff: strong nutrition delivered through a heavily engineered process with a sweetener. The dimension breakdown should make this explicit. The dangerous outcome is either (a) the protein and fiber scores pull it to A despite the caps, or (b) the caps and penalties collapse it to D, ignoring the genuine nutritional delivery.
