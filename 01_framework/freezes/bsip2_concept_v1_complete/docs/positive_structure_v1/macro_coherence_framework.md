# Macro Coherence Framework

**Status:** Design document — conceptual phase. No formulas or scoring thresholds are defined here.  
**Purpose:** Define how Bari can distinguish naturally coherent nutritional structure from engineered macro optimization — without asserting that natural is always superior.

---

## The core premise

Every whole food has a characteristic macro signature — a pattern of fat, protein, carbohydrate, fiber, and calorie density that arises from its biological composition. Almonds are high-fat, moderate-protein, low-carb, high-fiber. Chickpeas are high-carb, high-fiber, moderate-protein, low-fat. Oats are high-carb, moderate-fiber, moderate-protein, very-low-fat. Salmon is high-protein, high-fat, zero-carb, zero-fiber.

These signatures are not arbitrary — they reflect the evolutionary and biological structure of the food. They co-occur because the food's biology produced them together. The fat in an almond exists in the same cells as the protein; the fiber in a chickpea exists in the same seed coat as the starch and the mineral content.

Engineered foods can reproduce the macro numbers of any whole food or any desired nutritional target. They cannot reproduce the biological coherence that produced those numbers naturally. And the biological coherence is what determines how the food behaves in digestion, how its nutrients interact, and how its satiety signals operate.

**Macro coherence is the analytical tool for detecting this distinction.**

---

## What macro coherence is not

Before defining what macro coherence is, it is essential to define what it is not — to prevent this framework from becoming an argument for food conservatism.

**It is not a claim that natural macro ratios are optimal.** Some natural foods have problematic macro profiles: coconut oil is predominantly saturated fat; white rice is almost pure starch with negligible fiber; unprocessed cane sugar is pure sucrose. Natural origin does not make a macro profile coherent in any evaluative sense.

**It is not a claim that engineering always breaks coherence.** Greek yogurt is engineered (whey is removed, protein is concentrated) and maintains excellent macro coherence because the concentrated milk protein matrix is itself coherent. Traditional nut butters are mechanically engineered (grinding) and maintain coherence. Minimal culinary processing often improves nutritional availability without breaking coherence.

**It is not a claim that every product should match the macro profile of a known whole food.** A product can legitimately be a combination of whole foods that produces a hybrid macro profile with no perfect whole-food equivalent — muesli combines oats, nuts, and dried fruit into a macro profile that no single whole food matches, and remains highly coherent.

**It is a claim about whether the macro profile is explainable from the structural ingredients.** Coherence asks: could the declared primary ingredients plausibly produce the observed macro profile without fractional extraction, isolation, or supplementation? If yes, the product's macros are coherent. If no — if the protein is too high for the declared whole-food sources, the fiber too high for the declared grain sources, the fat too low given the declared fat sources — then reconstruction or supplementation is indicated.

---

## The macro signature approach

For macro coherence assessment, the key question is whether the product's declared nutritional profile is *consistent with* what its ingredient composition would naturally deliver.

This requires knowing — at least approximately — the macro contribution ranges of common ingredient categories. A draft sketch (not calibrated values):

**High-protein whole-food ingredients and their characteristic protein ranges:**
- Whole legumes (chickpeas, lentils, beans): 20–25g protein per 100g dry weight; accompanied by 6–12g fiber, <5g fat
- Nuts and seeds: 15–25g protein per 100g; accompanied by 40–60g fat, 5–12g fiber
- Whole dairy (milk, yogurt): 3–10g protein per 100g; accompanied by 3–10g fat, 0–4g carbs
- Eggs: 12–13g protein per 100g; accompanied by 10–11g fat, <1g carbs
- Whole grains (oats, wheat): 10–15g protein per 100g; accompanied by 60–70g carbs, 8–12g fiber
- Fish/meat (context): 18–25g protein per 100g; high fat to protein ratio varies by species

If a product declares 35g protein per 100g and its first three ingredients are oat flour, dates, and coconut — this is not coherent. Oat flour delivers ~13g protein per 100g; dates deliver ~2g; coconut ~3–4g. Even at 80% oat flour content, the product would deliver at most ~10–11g protein per 100g from these sources. 35g protein requires either undeclared protein sources or isolate supplementation. The macro profile is incoherent with the declared ingredients.

This incoherence detection does not require perfect knowledge. It requires approximate order-of-magnitude plausibility assessment.

---

## The five coherence signals

### Signal 1: Fiber-to-sugar ratio

In whole plant foods, wherever sugars occur naturally, fiber co-occurs at a meaningful ratio. This is a consequence of plant biology: the cell walls that contain and protect the sugars in fruit, grain, and root vegetables are themselves made of fiber. When you consume the sugar, you consume the fiber that surrounds it.

**Natural fiber-to-sugar ratios in whole plant foods (indicative ranges):**
- Whole oats: fiber/sugar ratio ~3.0 (8–10g fiber, 1–2g sugar per 100g)
- Whole apple: fiber/sugar ratio ~0.25 (2.4g fiber, 10g sugar — but the fiber is structurally present with the sugar)
- Whole dates: fiber/sugar ratio ~0.10 (8g fiber, 63g sugar — high sugar, some fiber context)
- Date syrup: fiber/sugar ratio ~0.005 (fiber discarded during extraction)
- White sugar: fiber/sugar ratio = 0 (no fiber at all)
- Fruit juice concentrate: fiber/sugar ratio ~0.01 (nearly all fiber discarded)

**The coherence implication:** When a product has high sugar AND very low fiber, the sugar is almost certainly free sugar from a high-fragmentation source (syrup, refined sugar, juice concentrate). When a product has high fiber AND high sugar, it may reflect whole-fruit or whole-grain ingredients where both are naturally present — but this requires examination of whether the fiber is in-matrix or added.

**The gaming test:** A product can game the fiber-to-sugar ratio by adding isolated fiber to a sugar-heavy product. This is why this signal must be cross-referenced with the fiber source type — isolated added fiber generates a numerically better ratio without generating the structural coherence that the ratio is intended to detect.

**Draft threshold for design discussion:** A fiber-to-sugar ratio below 0.08 in a non-beverage product suggests that the sugar arrives substantially without fiber context — either free sugar from refined sources, or natural fruit sugars whose fiber has been removed. This does not automatically penalize the product — it is one coherence signal among several.

---

### Signal 2: Protein fraction plausibility

No whole food naturally delivers more than approximately 35% of its calories from protein. This is a biological constraint — proteins are built from amino acids, which require nitrogen, and whole foods that are primarily protein sources (legumes, fish, dairy) are typically also significant sources of fat or carbohydrate that reduces the protein fraction.

**Approximate protein-calorie fractions in whole foods:**
- Legumes: 24–28% of calories from protein
- Eggs: 34% (borderline — eggs are unusual)
- Fish: 30–50% (fish is an outlier; high-protein, low-fat fish like cod can approach 50%)
- Greek yogurt: 35–45% (strained dairy concentrates protein; approaches the biological ceiling)
- Nuts: 12–18% (fat dominates)
- Grains: 10–15%
- Meat: 25–40% (variable by fat content)

**The coherence threshold:** When a product delivers more than approximately 35–40% of calories from protein, and its ingredient list does not include a plausible high-protein whole-food source (fish, egg, very lean meat, strained dairy) in a primary position, the protein fraction is incoherent with the ingredient declaration. It implies isolate supplementation even if not explicitly declared.

**Practical application:** A snack bar claiming 20g protein per 100g at 400 kcal/100g delivers 20% protein calories — plausible from nuts and legumes. A snack bar claiming 30g protein per 100g at 380 kcal/100g delivers 32% protein calories — possible but at the boundary. A snack bar claiming 40g protein per 100g at 400 kcal/100g delivers 40% protein calories — incoherent without isolates. The declared ingredients should be cross-checked against this biological plausibility ceiling.

---

### Signal 3: Fat composition fingerprint

Naturally occurring fats have characteristic fatty acid profiles that reflect their biological source. Palm oil is predominantly saturated; sunflower oil is predominantly polyunsaturated; olive oil is predominantly monounsaturated; dairy fat has a complex profile weighted toward saturated and monounsaturated; nut fat profiles are source-specific (almond: predominantly monounsaturated; walnut: predominantly polyunsaturated omega-3 and omega-6).

When a product's fat profile — readable from the declared saturated fat quantity in context of total fat — is inconsistent with the fat-contributing ingredients declared, this indicates either:
1. A non-declared fat source (typically palm oil or palm kernel oil, which are cheap and used to improve texture and shelf life)
2. A more highly saturated fat source than declared

**Design approach:** This signal requires sat_fat fraction (sat_fat_g / fat_g). If sat_fat fraction > 0.5 and primary fat sources are declared as nuts or vegetable oils (which should be low-saturated), the fat composition is incoherent with declarations. Palm oil presence should be flagged — it is a saturated fat source that changes the fat profile of products substantially and is used specifically for texture engineering.

**BSIP2 current state:** `sat_fat_g` and `fat_g` are available in L1. The fat quality dimension uses these. What is not currently done is cross-referencing the declared fat source (ingredient list) against the sat_fat fraction. This is the incremental step that makes fat composition a coherence signal rather than just a penalty trigger.

---

### Signal 4: Calorie density in context of declared ingredients

Some products have calorie densities that are inconsistent with their declared ingredient composition. This is less common because the nutrition panel is typically accurate — but it can reveal reconstruction.

**The relevant case:** A product claiming "oats, honey, dried fruit, and nuts" as primary ingredients should have a calorie density appropriate to that combination — roughly 380–450 kcal/100g for a granola-type product with modest fat from nuts. If the same declared ingredients produce 520+ kcal/100g, a high-fat undeclared ingredient (palm oil, typically) or a high-sugar one is implied.

More relevant for positive structure: a product with declared primary ingredients that are whole grains, nuts, and dried fruit, producing a calorie density of 350–430 kcal/100g, has a coherent calorie density. Its macro profile is not inflated beyond what those ingredients could produce. This is a mild positive coherence signal — the absence of calorie density inflation from added fats and refined sugars beyond what whole-food ingredients would generate.

---

### Signal 5: Macro disproportion index

This is the most synthetic signal — it captures the overall "engineered extremity" of the macro profile.

Natural foods exist in a macro space that, while wide, has boundaries. Products outside these boundaries are at elevated risk of reconstruction engineering. The relevant extremes:

**Very high protein, very low fat, very low carb:** Cannot arise from whole foods without isolate extraction. The closest natural product (tuna in water) is in a different category. A snack bar with 35g protein, 3g fat, 5g carbs per 100g is describing an isolate product, full stop.

**Very high fiber, very high protein, very low sugar:** An ideal engineered health product target. Natural foods with high fiber (legumes, whole grains) also have substantial carbohydrates. Very high fiber with very low net carbs implies added isolated fiber to a low-carb base.

**Very high fat, moderate protein, low carb, zero fiber:** This is possible from whole foods (certain nuts, dairy, eggs) — coherent. But the fiber absence combined with high fat and protein in a packaged snack is worth examining.

**Very low calorie, high fiber, zero protein, zero fat:** Diet jelly category. Hydrocolloid engineering. No whole food produces this macro profile. This is structural emptiness by a different detection path.

The disproportion index is not a precise calculation — it is a classification of whether the overall macro profile is achievable from whole or minimally processed foods, or requires extraction and reconstruction.

---

## Coherence is a composite assessment

No single signal definitively establishes macro coherence or incoherence. Each signal is probabilistic:

| Signal | Strong coherence indicator | Strong incoherence indicator |
|---|---|---|
| Fiber/sugar ratio | >0.15 with in-matrix fiber | <0.05 or low ratio despite claimed high fiber |
| Protein fraction | <30% of calories from recognizable sources | >35% with no plausible whole-food explanation |
| Fat composition | Sat_fat fraction matches declared fat sources | Sat_fat fraction inconsistent with declared "nut/vegetable" oils |
| Calorie density | Consistent with declared whole-food ingredients | Higher than ingredients could produce |
| Macro disproportion | Profile achievable from whole foods | Profile impossible from whole foods without extraction |

A product scoring well on 4–5 of these signals has genuinely coherent macro structure. A product scoring poorly on 3+ has likely been macro-optimized through reconstruction. A product with mixed signals requires ingredient-level verification.

---

## The coherence signal in practice: example products

**Date-and-almond bar (dates, almonds, cocoa):**
- Fiber/sugar: dates provide ~8g fiber with ~63g sugar; almonds provide fat and protein without adding much sugar; the ratio may be 0.10–0.15 — low-moderate coherence on this signal alone, but contextually appropriate for date-primary products
- Protein fraction: almonds contribute ~15% protein calories; dates are nearly zero protein; overall 5–8% protein calories is coherent
- Fat composition: almonds are predominantly monounsaturated; coherent
- Calorie density: dates + almonds → 380–440 kcal/100g depending on ratios; coherent
- Macro disproportion: achievable from declared ingredients; coherent
- **Overall: High coherence despite high sugar, because the sugar is contextually appropriate to the declared ingredients**

**Protein bar (whey isolate, chicory fiber, palm kernel oil, dark chocolate, erythritol):**
- Fiber/sugar: high fiber (from chicory inulin), very low sugar (from erythritol sweetening); ratio appears excellent but fiber is all isolated from a different food
- Protein fraction: 30–40% of calories from protein; incoherent with any declared whole-food protein source
- Fat composition: palm kernel oil → very high sat_fat fraction; possibly incoherent with "chocolate-flavored" framing
- Calorie density: lower than expected if isolate-derived — may be consistent only because protein isolate is used as a lean caloric base
- Macro disproportion: impossible to produce from whole foods; reconstruction confirmed
- **Overall: Low coherence — engineered macro optimization from isolated components**

**Plain rolled oats:**
- Fiber/sugar: ~8g fiber, ~1g sugar; ratio ~8; extremely coherent — fiber and starch co-present in grain matrix
- Protein fraction: ~14% of calories; coherent with grain
- Fat composition: trace fat, minimal sat_fat; coherent with grain
- Calorie density: ~380 kcal/100g; coherent
- Macro disproportion: a textbook whole-food macro profile
- **Overall: Very high coherence — reference product for this signal**

---

## BSIP2 design implications

1. **The fiber/sugar ratio signal is implementable now.** The `sugars_g` and `dietary_fiber_g` fields are both L1 observed signals. A computed L2 ratio is straightforward. The challenge is distinguishing in-matrix from supplemental fiber — this requires the fragmentation framework's fiber taxonomy. A provisional implementation could use fiber/sugar ratio as a coarse positive signal with a known limitation flagged in the trace.

2. **Protein fraction plausibility requires only L1 data.** `protein_g` and `energy_kcal` are sufficient to compute protein-calorie fraction. The biological ceiling (~35–40%) can be applied as a coherence test without ingredient detection — a product exceeding this ceiling is flagged as likely isolate-supplemented regardless of label claims.

3. **Fat composition fingerprint requires L1 and L3.** Sat_fat fraction from L1 compared to declared fat source inferred from L3 ingredient detection. The current architecture already has `has_seed_oil` in L3; extension to specific fat source identification is feasible.

4. **Macro disproportion is an aggregate inference at L4.** It synthesizes the above signals into a classification: coherent / partially coherent / incoherent. This is an interpreted signal (L4 layer), not a directly observed one.

5. **The coherence assessment should never override nutritional concern signals.** A product with highly coherent macros but very high saturated fat should still be penalized for the fat concern. Coherence is a structural positive signal; it does not neutralize genuine nutritional concerns. The interaction with the cap system is additive, not substitutive.
