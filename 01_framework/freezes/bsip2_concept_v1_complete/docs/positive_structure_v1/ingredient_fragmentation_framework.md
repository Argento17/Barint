# Ingredient Fragmentation Framework

**Status:** Design document — conceptual phase. No formulas or scoring thresholds are defined here.  
**Builds on:** `ingredient_fragmentation_concept.md` (fragmentation spectrum vocabulary)  
**Purpose:** Extend the fragmentation concept into a structured analytical framework — with explicit treatment of beneficial fragmentation, detection challenges, and BSIP2 design constraints.

---

## Starting point

The existing `ingredient_fragmentation_concept.md` establishes the fragmentation spectrum:

```
Whole food → Mechanical transformation → Fractional extraction → Molecular reconstruction
```

This framework takes that spectrum further: it introduces a two-axis model (fragmentation intensity × fragmentation purpose), a formal taxonomy for ingredient forms, treatment of beneficial fragmentation cases, and an analysis of the gaming surface this concept creates.

---

## The two-axis model

Fragmentation is a single dimension only if we assume that all fragmentation serves the same purpose. It does not. A useful analysis requires two axes:

**Axis 1: Fragmentation intensity**  
How far has the ingredient moved from its source food's structural state?

- Level 0: Intact (whole almond, oat groat, whole egg, whole date)
- Level 1: Mechanically altered, matrix preserved (almond butter, rolled oats, ground flaxseed, scrambled egg)
- Level 2: Mechanically altered, matrix partially lost (fine oat flour, almond meal — fiber present but surface area altered)
- Level 3: Single-fraction extraction, primary fraction (cold-pressed olive oil, tahini — major component extracted but as the product's defining character)
- Level 4: Multi-fraction separation — target component enriched, others discarded (oat bran concentrate, milk whey, fruit juice)
- Level 5: Molecular isolation (oat protein isolate >85%, whey protein isolate >90%, maltodextrin, pure inulin from chicory)
- Level 6: Reconstructed from multiple Level 4–5 fractions (plant-based burger from soy isolate + methylcellulose + beet extract; protein bar from whey isolate + chicory fiber + palm kernel oil)

**Axis 2: Fragmentation purpose**

- **Extraction as product:** The fragmented form IS the product (olive oil, tahini, butter, cheese). The fragmentation serves the product's culinary or functional purpose; this is not a disguised attempt to reconstruct whole food nutrition.
- **Concentration:** Water removal to increase density or extend shelf life (tomato paste, dried fruit, nut butter). The fragmentation is minimal; co-nutritional elements remain present.
- **Structural improvement:** Fragmentation that improves the food's nutritional or safety properties (milling removes outer husk to reduce arsenic in some grains; cooking denatures antinutrients in legumes; straining yogurt concentrates protein while retaining the fermented matrix).
- **Reconstruction ingredient:** The extracted fraction is an ingredient used to build a target nutritional profile in a different product. Whey protein isolate in a protein bar; chicory root inulin added to a cereal bar. This is the problematic purpose category — the fragmentation is specifically to create a component that can be assembled into a product that mimics whole-food nutrition.

The BSIP2 scoring concern is concentrated in the fourth purpose category: **fragmentation as reconstruction ingredient**. An extracted fiber added to a sugar-heavy product to boost its fiber score, or an isolated protein added to a low-protein base food to claim a protein benefit, uses fragmentation to simulate structural quality that isn't present.

---

## Beneficial fragmentation: a rigorous treatment

Arguing against fragmentation categorically would be wrong. The following cases demonstrate where fragmentation serves a legitimate purpose that BSIP2 should not penalize.

---

### Pressing to extract oil

**Process:** Olives, seeds, or nuts are pressed to extract their oil fraction.  
**Fragmentation intensity:** Level 3 (single-fraction extraction)  
**Purpose:** Extraction as product — olive oil is not pretending to be an olive  
**Nutritional character:** The fat matrix of the source food is transferred largely intact to the product. In cold-pressed olive oil, polyphenols from the olive dissolve into the oil; the fatty acid profile reflects the source olive composition; the tocols are preserved. This is not a neutral extraction — it transfers specific beneficial elements of the olive to the extracted product.  
**Assessment:** High fragmentation, legitimate purpose, nutritional integrity preserved within the extracted dimension. BSIP2 correctly evaluates this product as oil (whole_food_fat category) rather than penalizing its "processed" status.

---

### Fermenting dairy: Greek yogurt straining

**Process:** Milk → fermented with live cultures → whey strained off → concentrated protein product  
**Fragmentation intensity:** Level 2–3 (structural alteration + whey separation)  
**Purpose:** Structural improvement — straining concentrates the milk protein matrix and produces a product with superior satiety properties per calorie compared to unfermented milk  
**Key distinction:** Straining yogurt to make Greek yogurt is **concentration of the fermented matrix**, not destruction of it. The casein proteins remain in their fermented structural state; the live cultures remain active; the fat globules (in full-fat versions) are intact. The only fraction removed is whey — itself a legitimate food product.  
**Assessment:** This fragmentation improves matrix density without destroying matrix coherence. BSIP2 should credit this, not penalize it.

---

### Stone milling whole grain

**Process:** Whole grain → milled to flour  
**Fragmentation intensity:** Level 1–2 (mechanical alteration)  
**The grain's endosperm, bran, and germ remain co-present in whole grain flour** (unlike refined milling, which deliberately separates bran and germ to extend shelf life, discarding most of the fiber, vitamins, and fat). Stone-milled whole wheat flour retains all grain fractions in approximately original proportions.  
**Purpose:** Culinary transformation — flour is needed for baking; the milling serves the product's legitimate purpose  
**Assessment:** Minimal fragmentation concern. The detection challenge is distinguishing whole grain flour (all fractions present) from refined flour enriched with added bran (bran returned artificially). These can appear similar on a label. Whole grain flour as first ingredient is a positive signal; "refined wheat flour, wheat bran" as separate ingredients suggests reconstitution.

---

### Concentration by dehydration

**Process:** Fresh fruit → water removed → dried fruit  
**Fragmentation intensity:** Level 1 (water removal; all solid components remain present)  
**All solid nutritional components — fiber, polyphenols, minerals, natural sugars — are concentrated together.** There is no separation of fractions.  
**Distinction from fruit concentrate:** When fruit is pressed and the juice is concentrated (removing the fiber), the result is a sugar concentrate — an entirely different product despite "fruit" in its name. Dried fruit retains the fiber; fruit juice concentrate does not.  
**Assessment:** Dehydration of whole fruit is legitimate concentration, not structural fragmentation. BSIP2 should distinguish dried fruit from fruit juice concentrate in ingredient detection — they currently both generate sugar signals, but dried fruit also generates fiber co-presence that juice concentrate does not.

---

### Fermentation of grains

**Process:** Grain flour + water + fermentation starter → sourdough or injera or other fermented grain product  
**Fragmentation intensity:** Level 1 (mechanical) + fermentation transformation  
**The fermentation process in traditional grain ferments performs specific structural improvements:**
- Phytate reduction (phytic acid in grain binds zinc, iron, calcium; fermentation breaks phytate down, dramatically improving mineral absorption)
- Protein pre-digestion (gluten and other grain proteins partially hydrolyzed, making them more bioavailable and often better tolerated)
- Starch modification (resistant starch formation in sourdough produces slower glycemic response than non-fermented bread from the same flour)
- Anti-nutrient reduction without chemical intervention  

**Assessment:** This is nutritionally beneficial fragmentation. BSIP2 currently has no mechanism to credit it. A fermentation flag in L3 that recognizes sourdough fermentation (detectable from "sourdough starter," "levain," specific acidic pH signals from lactic acid bacteria markers in the ingredient list) would be a meaningful structural signal.

---

## The problematic fragmentation cases

These are the cases where fragmentation serves the **reconstruction ingredient** purpose — where it is used to simulate whole-food nutrition rather than to serve a culinary or concentration purpose.

---

### Protein isolation for bar enrichment

**Process:** Whey → protein isolate (>90% protein); or peas/oats → legume/grain isolate  
**Fragmentation intensity:** Level 5  
**Purpose:** Reconstruction ingredient — the isolate is added to a product to boost its protein score on the nutritional label  
**What's lost:** In whey protein isolate: essentially all fat and lactose, and therefore all of the co-nutritional elements (CLA, fat-soluble vitamins, natural phospholipids). In legume protein isolate: the fiber that co-occurs with the protein in the source legume; the starch; the iron that accompanies legume protein in its food matrix. The protein arrives in the target product entirely without its natural co-factors.

**Assessment:** This is the core fragmentation concern. The protein grams on the label are real; the structural context of those protein grams is entirely absent.

**Detection note for BSIP2:** The presence of protein isolate in the ingredient list is a strong signal. Terms to detect: [protein isolate, whey isolate, pea protein isolate, soy protein isolate, rice protein concentrate, oat protein concentrate, milk protein concentrate, casein]. These are distinct from whole food protein sources [chickpeas, peas, oats, milk, eggs, nuts]. A product whose protein content is predominantly explained by isolate enrichment has lower structural protein quality than its label suggests.

---

### Fiber isolation for bar enrichment

**Process:** Chicory root → inulin extraction; Apple pomace → pectin extraction; Oat bran → beta-glucan concentrate  
**Fragmentation intensity:** Level 5  
**Purpose:** Reconstruction ingredient — extracted fiber is added to products to increase their dietary fiber declaration

**The specific gaming problem:** A cereal bar can add 5–8g of chicory root inulin and declare "high in fiber." The inulin is a real fiber, and its fermentation by gut bacteria does produce short-chain fatty acids with health benefits. But:
- It arrives in the food without any connection to the chicory plant's other nutritional properties
- It was not present in the primary ingredients (oat flour, sugar, palm oil) in any meaningful quantity
- The fiber score improvement is entirely due to an additive, not to structural whole-food composition
- The fiber-to-sugar ratio of the primary food matrix (before inulin addition) might be very poor

**Assessment:** The fiber count is correct; the structural signal it implies is misleading. A positive structure framework must distinguish in-matrix fiber from supplemental extracted fiber.

**Detection challenge:** Inulin, chicory root fiber, FOS (fructooligosaccharides), and chicory root extract are all the same substance declared with different labels. A robust detection system needs to flag all known extracted fiber sources as "supplemental fiber" rather than as structural fiber. This is a labeling recognition problem with an achievable solution.

---

### Syrup systems as sweeteners

**Process:** Dates/figs/agave/coconut palm → sugar extraction and concentration  
**Fragmentation intensity:** Level 4–5 depending on method  
**The specific problem:** "Date syrup," "coconut blossom syrup," "agave nectar," and "brown rice syrup" are marketed as whole-food or natural sweeteners. Nutritionally, they are free-sugar systems: sugars extracted from the source food, refined to concentrate the sweet fraction.

**Dates vs. date syrup:**
- Whole dates contain 6.7g fiber per 100g, co-located with their sugars; the sugars in a whole date are consumed with a fiber context that slows absorption
- Date syrup contains <0.5g fiber per 100g; the fiber was discarded during extraction; the product is essentially a moderately refined sugar with micronutrient traces

Date syrup in a product is a Level 4 fragmentation of date sugars — not a "date ingredient." The sugar signal it creates is real; the implied whole-date-matrix benefit is absent. BSIP2's sugar context classification (SRC-02) should treat date syrup as added sugar (SC-4 at best, SC-5 if extraction is clearly synthetic), not as a fruit-matrix-intact ingredient.

---

### "Re-wholefood" reconstruction

**Process:** Product A is assembled from multiple Level 4–5 fractions and declares a "made with real X" claim, where X appears in small quantity

**Example:** "Oat & nut protein bar" with ingredients: whey protein isolate, chicory fiber, palm kernel oil, oat flour (8%), cashew pieces (5%), brown rice syrup, cocoa powder, flavors, salt

The oat flour (8%) and cashew pieces (5%) create a halo of whole-food legitimacy. The product can claim "with oats," "with cashews," and potentially "whole grain" (if the oat flour is whole grain). But 87% of the product by weight is fractional extractions from multiple foods — none of which retain their food matrices.

**Assessment:** The BSIP2 matrix integrity assessment must weight ingredients by their declared proportion (or by list position as a proxy). Minor whole-food inclusions in a reconstruction-base product should not generate a high structural integrity signal. A threshold — perhaps requiring that the top-3 ingredients by list position are whole or mechanically-altered foods — would substantially reduce this gaming vector.

---

## The detection taxonomy

For BSIP2 to use fragmentation as a signal, ingredient detection must include fragmentation-level metadata. A draft taxonomy:

**Intact / Level 0–1:**
- Named whole fruits, vegetables, nuts, seeds, legumes, grains
- Named whole dairy (milk, cream, eggs)
- Named whole animal proteins (meat, fish, eggs)

**Mechanically transformed / Level 1–2:**
- Nut butters (almond butter, peanut butter, tahini)
- Rolled or flaked grains (rolled oats, flaked barley)
- Nut and seed flours when declared as whole grain
- Cold-pressed or stone-ground oils when declared as such
- Ground spices, whole grain flours

**Concentrated / Level 3:**
- Pressed oils (olive oil, sunflower oil — unless "cold-pressed" declared)
- Tomato paste, fruit purees
- Dried fruits (where fiber and solids are concentrated, not separated)
- Full-fat nut pastes (tahini, natural peanut butter without additives)
- Greek yogurt, strained dairy products

**Fractionated / Level 4:**
- Fruit juices and juice concentrates (sugar concentrated; fiber discarded)
- Oat bran, wheat germ (fractions separated from grain)
- Skim milk, whey (fat fraction separated)
- Cocoa powder (fat partially removed from cocoa)
- Natural flavors (extracted aroma fractions — ambiguous but Level 4+)

**Isolated / Level 5:**
- Any ingredient declared as "isolate": whey protein isolate, pea protein isolate, soy protein isolate
- Any ingredient declared as "concentrate" in the protein context: milk protein concentrate, oat protein concentrate
- Maltodextrin (starch fraction extracted and partially hydrolyzed)
- Pure inulin, chicory root fiber, FOS (extracted soluble fiber)
- Casein, caseinates (isolated milk protein fraction)
- Glucose syrup, high-fructose corn syrup, rice syrup (isolated sugar fractions)

**Reconstructed / Level 6:**
- Products where the majority of declared ingredients are Level 4–5
- This is an aggregate assessment, not a single ingredient detection

---

## The anti-ideology principle

This framework must not become a rule that "more whole food ingredients are always better." Three counterexamples that must remain correctly evaluated:

**Counterexample 1: Whole-food ingredients in bad proportions**  
A product with oat flour (43%), sugar (25%), palm oil (15%), cocoa (10%), and salt (2%) has all "whole" or "mechanical" ingredients — and also contains 25% added sugar and 15% palm oil in a highly engineered format. Low fragmentation does not rescue an unhealthy macro composition.

**Counterexample 2: High fragmentation for legitimate clinical purpose**  
Protein powders are Level 5 fragmentation by design. They are a legitimate nutritional tool. Their score in BSIP2 should reflect their structural limitation accurately — they deliver protein without matrix — but they are not "bad products." They are correctly-characterized products.

**Counterexample 3: Low-fragmentation product with problematic composition**  
Butter is Level 1–2 fragmentation (cream is mechanically churned). The fat matrix of cream is substantially intact in butter. But butter's macro profile (80% fat, predominantly saturated) is correctly evaluated by the fat quality and calorie density dimensions regardless of its low fragmentation.

The fragmentation signal should influence structural quality assessment, not override nutritional composition evaluation.

---

## BSIP2 design implications

1. **Ingredient detection must include fragmentation-level tagging.** The current L3 classification includes `protein_source` (whole_food / mixed / isolate / unknown). This is a prototype of what a full fragmentation taxonomy requires. Extension to fiber sources, fat sources, and sweetener sources is the necessary next step.

2. **Primary ingredient weighting matters.** A fragmentation score should weight the first three to five ingredients heavily. Minor whole-food inclusions in reconstruction products should not dominate the signal.

3. **The fiber signal must distinguish structural from supplemental fiber.** This is the most important immediate addition. Chicory fiber, inulin, FOS, and related isolated fibers should be flagged as supplemental; their fiber gram contribution should be tracked separately from in-matrix fiber.

4. **Date syrup, brown rice syrup, agave nectar, and similar "natural" sweeteners must be classified as Level 4 free sugars,** not as whole-food ingredients. Their marketing as natural alternatives to refined sugar should not generate positive structural signals.

5. **The detection problem is real and bounded.** Not all fragmentation levels can be inferred from Israeli product labels. "Natural flavors" is ambiguous. "Oat fiber" could be oat bran (Level 3) or oat beta-glucan extract (Level 5). The framework should be implemented where detection is reliable and explicitly agnostic where it is not — with the agnostic cases defaulting to a neutral rather than positive structural signal.
