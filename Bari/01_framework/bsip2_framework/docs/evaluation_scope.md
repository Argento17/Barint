# Evaluation Scope

**Purpose:** Define which products BSIP2 is designed to evaluate normally, which require contextual interpretation, and which are outside Bari's intended scope. A system that does not define its own boundaries will apply its logic outside those boundaries and produce results that appear legitimate but are not.

---

## The three evaluation statuses

| Status | Meaning |
|--------|---------|
| `standard` | BSIP2 scoring is designed for this product type; results are analytically valid and directly comparable within category |
| `context_limited` | BSIP2 can produce a score, but the result requires contextual interpretation; the per-100g analytical frame may not reflect the product's actual dietary role |
| `out_of_scope` | BSIP2 was not designed for this product type; a score can be computed but will be analytically misleading; Bari should not surface a grade without explicit qualification |

The distinction is not about data availability. A product can have complete nutritional data and still be `context_limited` or `out_of_scope` — the issue is whether the analytical framework applies to the product's intended use and consumption context.

---

## Standard Evaluation Products

These are the products BSIP2 is calibrated for. The analytical framework, thresholds, category tables, and guardrail rules are designed with these product types in mind.

**Characteristics of standard evaluation products:**
- Consumed in quantities where per-100g values are meaningfully representative
- Evaluated by general consumers without specific dietary prescription
- Fit recognisably into one of the eight product categories
- No regulatory regime requires separate nutritional evaluation standards

**Product types:**
- Packaged snack bars, granola bars, cereal bars
- Breakfast cereals and muesli
- Spreads, dips, hummus, sauces, and condiments used as meal components
- Nut products, seed products, nut and seed butters
- Yogurts, dairy protein products, kefir
- Chocolate and confectionery
- Packaged beverages (juices, plant milks, soft drinks)
- Packaged whole foods (nuts, dried fruits, seeds)
- Bread, crackers, rice cakes evaluated as snacks or daily staples

---

## Context-Limited Products

These products can be evaluated by BSIP2, and the score is directionally informative — but the per-100g analytical frame distorts the result in specific ways that the user must be made aware of.

---

### Condiments used in very small quantities

**Products:** Miso paste, fish sauce, soy sauce, hot sauce, vinegar, certain dressings, preserved olives, capers

**Why standard scoring may fail:**
The per-100g frame is appropriate for foods consumed in 100g quantities. Miso paste is consumed in teaspoon quantities (5–15g). Its sodium concentration of 3,000–6,000mg/100g triggers every sodium guardrail at full force — producing a score that implies a level of sodium intake orders of magnitude greater than actual consumption. The score is analytically correct per-100g but practically misleading.

**What Bari should avoid implying:**
That miso paste is as harmful as a sodium-dense main dish. The score for a condiment used in small quantities does not represent the same dietary sodium load as an equivalent score for a product eaten at 100–200g portions.

**Future direction:**
Serving-size-adjusted evaluation — or a parallel display mode showing nutrient delivery per typical serving rather than per 100g — would resolve this. Until then, condiment products should surface a context note in the UI: "Evaluated per 100g; this product is typically consumed in small quantities."

---

### Meal replacements

**Products:** Liquid meal replacements (e.g. Huel, Soylent), meal replacement bars marketed as complete nutrition

**Why standard scoring may fail:**
Meal replacements are formulated to deliver complete nutrition in a single serving. They contain added vitamins, minerals, and fiber specifically because they replace a full meal. The additive markers that represent industrial fortification in a snack product represent nutritional completeness in a meal replacement. BSIP2's additive burden rules cannot distinguish between "additives that compensate for processing damage" and "additives that deliver deliberate nutritional completeness."

**What Bari should avoid implying:**
That a complete meal replacement is nutritionally inferior to a simpler product that happens to deliver fewer nutrients. The frame for a meal replacement is total nutritional delivery per meal, not per-100g quality relative to category peers.

**Future direction:**
Meal replacement products require a purpose-aware evaluation layer. A separate evaluation mode (or status flag) that scores completeness of macro and micronutrient delivery rather than processing burden would be more appropriate.

---

### Medical and clinical foods

**Products:** Infant formula, elemental nutrition, disease-specific formulas (diabetic, renal, oncology support), oral nutritional supplements (e.g. Ensure, Fortisip)

**Why standard scoring may fail:**
These products are formulated under different regulatory frameworks for populations with specific medical needs. Their ingredient lists contain compounds (medium-chain triglycerides, specific amino acid profiles, pre-digested proteins) that BSIP2 reads as heavy additive burden. Their calorie and macronutrient profiles are calibrated for medical need, not general health optimisation. A high-MCT formula for a patient with fat malabsorption is not meaningfully comparable to a snack product using MCT oil as a marketing ingredient.

**What Bari should avoid implying:**
Any comparison between medical nutrition products and general consumer food. These products should not receive a grade in the BSIP2 A–E system without explicit qualification that the grading framework was not designed for clinical nutrition.

**Future direction:**
Medical foods are `out_of_scope` for BSIP2 grading. A future status flag should route these products out of standard grading and into a separate "clinical nutrition" display mode that presents nutritional data without a comparative grade.

---

### Baby foods

**Products:** Infant purees, jarred baby food, baby cereals, follow-on formulas

**Why standard scoring may fail:**
Baby foods are formulated for a population with completely different calorie requirements, micronutrient priorities, and developmental needs. A plain carrot puree scoring 95 on the beverage calorie scale is analytically correct but informationally empty — the score tells adults nothing useful about whether this is an appropriate infant food.

Additionally, BSIP2's whole-food floor (minimum 75 for NOVA 1) would correctly protect plain vegetable purees — but the A grade this produces carries implications for the adult food context that simply do not translate.

**What Bari should avoid implying:**
That a baby food's BSIP2 score is meaningful guidance for infant nutrition. Infant nutrition is governed by entirely different scientific and regulatory standards.

**Future direction:**
Baby foods are `out_of_scope`. The category classification engine should detect these and flag them as scope-out rather than assigning a standard grade.

---

### Sports and performance nutrition

**Products:** Pre-workout powders, intra-workout supplements, electrolyte tablets, creatine, BCAAs, beta-alanine products

**Why standard scoring may fail:**
Sports supplements contain compounds that do not belong in a food nutritional matrix (creatine monohydrate, beta-alanine, citrulline malate). These compounds have no nutritional role in the food quality sense that BSIP2 evaluates. Their presence may trigger additive markers inappropriately. The calorie and macronutrient profiles (often zero or near-zero) produce evaluations that are meaningless in the sports supplement context.

**What Bari should avoid implying:**
That a pre-workout supplement's BSIP2 score reflects its value as a supplement. The score for a sports supplement measures food quality; it cannot measure supplement efficacy, safety, or suitability.

**Future direction:**
Sports supplements are `out_of_scope`. The product detection layer should route these to a scope flag rather than a grade.

---

### Electrolyte and hydration products

**Products:** Electrolyte tablets, isotonic sports drinks, oral rehydration salts

**Status:** `context_limited`

**Why standard scoring may fail:**
Electrolyte products contain intentional sodium, potassium, and magnesium concentrations calibrated for hydration rather than flavour or preservation. Their sodium content, evaluated per-100g, triggers BSIP2's sodium guardrails. But in a sports or hydration context, this sodium is the intended functional delivery, not a concern.

The distinction between electrolyte sports drinks (context_limited) and pre-workout supplements (out_of_scope) is that electrolyte products have a clear nutritional composition that BSIP2 can evaluate — the question is whether that evaluation is informative in context, which it is only partially.

**Future direction:**
Surface the score with an explicit note: "This product contains intentional electrolytes for hydration use; sodium evaluation may not reflect dietary impact."

---

### Protein powders

**Products:** Whey protein, casein, plant protein isolates, blended protein powders

**Status:** `context_limited`

**Why standard scoring may fail:**
Protein powders are consumed diluted — 30g of powder in 300ml water produces a very different per-100g nutritional profile than the dry powder. The dry-powder per-100g evaluation applies BSIP2's standard rules to a product format that is not consumed dry. Calorie density of a protein powder (~380–400 kcal/100g dry) evaluated against a food category table produces misleading results.

**What Bari should avoid implying:**
That a protein powder's score reflects the quality of the drink it produces when reconstituted.

**Future direction:**
Protein powders should be evaluated against a "as-consumed" profile where possible, with explicit reconstitution assumptions. Until then, scores for dry powders should carry a prominent context note.

---

### Sports gels and energy gels

**Status:** `out_of_scope`

**Why:** Sports gels are formulated for a specific physiological window (during sustained exercise) where rapid sugar absorption is beneficial rather than concerning. BSIP2's sugar rules would fire heavily on a product that is analytically correct for its use case. The evaluation frame is fundamentally wrong.

---

## Out of Scope Products — Summary

| Product type | Why |
|-------------|-----|
| Infant formula | Different regulatory framework, different population, different nutritional priorities |
| Medical/clinical nutrition | Disease-specific formulation; grading is inappropriate |
| Baby foods | Different age-group nutritional requirements |
| Sports supplements (non-food) | Compounds outside food quality analytical framework |
| Sports gels | Formulated for physiological window incompatible with per-100g food evaluation |
| Alcohol products | Not currently in scope; alcohol as a nutrient has no dimension |
| Raw agricultural commodities (flour, sugar, oil sold in bulk) | These are ingredients, not consumer products; BSIP2 evaluates finished products |

---

## Evaluation Status Decision Tree

When a new product type is encountered:

1. **Is it consumed in roughly 100g-scale quantities?** If no → `context_limited` at minimum.
2. **Is it formulated for a specific clinical or developmental population?** If yes → `out_of_scope`.
3. **Does it contain compounds that have no food-quality meaning in BSIP2's analytical framework?** If yes → `out_of_scope`.
4. **Does the analytical result produce a score that would mislead a general consumer about the product's dietary role?** If yes → `context_limited`.
5. Otherwise → `standard`.

---

## What this means for implementation

Every product ingested into BSIP2 should be assigned an evaluation status before scoring runs. This status should be:
- Stored alongside the score in the output record
- Surfaced in the UI for any non-standard product
- Used to gate grade display: `out_of_scope` products should not display an A–E grade without explicit qualification

The evaluation status is not a confidence measure — a product can be `out_of_scope` with perfect data quality. It is a scope measure: does this analytical system apply to this product type?
