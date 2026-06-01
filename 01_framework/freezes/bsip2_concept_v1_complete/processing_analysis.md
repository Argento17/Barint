# Processing Analysis

## What processing analysis evaluates

Processing analysis answers a question that macronutrients alone cannot: **what was done to this food before it reached the package?** Two products with nearly identical nutrition panels can have very different food quality profiles if one is a minimal-ingredient whole food and the other is an engineered assembly of refined fractions, additives, and flavour systems.

Bari's processing analysis operates across three interrelated layers: processing level classification (NOVA), additive burden evaluation, and hyper-palatability detection.

---

## Layer 1 — Processing level (NOVA)

NOVA is a classification system that groups foods by the nature and extent of industrial processing, not by nutrient content.

| Level | Definition | Examples |
|-------|-----------|---------|
| NOVA 1 | Unprocessed or minimally processed | Oats, eggs, fresh fruit, plain nuts |
| NOVA 2 | Processed culinary ingredient | Oils, butter, flour, salt |
| NOVA 3 | Processed food | Canned beans, cheese, pickled vegetables |
| NOVA 4 | Ultra-processed | Products with ingredient lists containing industrial additives, flavour systems, or textural agents not used in home cooking |

Bari infers NOVA level from ingredient markers and ingredient count. This is a **proxy classification** — not a database lookup. Confidence in the NOVA classification is tracked and propagates into overall analytical confidence.

**Score impact:**
- NOVA 4: hard cap of 60 on the final score; −24 to the processing quality dimension
- NOVA 3: hard cap of 75; −12 to the processing quality dimension
- NOVA 1: score floor of 75 (whole-food protection)

---

## Layer 2 — Additive burden

Beyond NOVA level, the system evaluates the density and composition of industrial additives present in the ingredient list.

**Additive categories evaluated:**

| Category | Role in food system | Signal weight |
|----------|--------------------|-|
| Sweeteners | Non-nutritive sweetening; taste engineering | High |
| Emulsifiers | Fat-water integration; texture manipulation | Moderate |
| Stabilizers | Texture, shelf-life, mouthfeel engineering | Moderate |
| Protein isolates | Protein fraction added back post-processing | Moderate |

**Additive burden rules:**
- 3–4 additive markers: hard cap of 65
- 5+ additive markers: hard cap of 55
- Each additive marker type: −12 to the additive quality dimension
- Sweetener present: additional −8 to additive quality; separate hard cap of 70

**Individual ingredient penalties (processing quality dimension):**
- Glucose syrup: −8
- Maltodextrin: −8
- Flavourings: −6
- Emulsifiers: −6
- Chocolate or compound coating: −8
- Extruded or puffed grain: −8

Ingredient count also contributes: each ingredient beyond 8 applies a further −1.2 to the processing quality dimension.

---

## Layer 3 — Hyper-palatability detection

Hyper-palatability refers to a specific nutritional architecture pattern associated with engineered taste reward: combinations of fat, sugar, sodium, and refined carbohydrates that, in certain concentrations and combinations, produce consumption patterns that override normal satiety signalling.

This is distinct from whether a product is "tasty" or "enjoyable." It is a structural analytical property of the product's composition.

### The four hyper-palatability patterns

**Pattern 1: Fat-Sodium** (characteristic of savoury chips, crackers, flavoured nuts)
- Triggered when: fat contributes ≥ 25% of calories AND sodium ≥ 300mg/100g
- Structural interpretation: fat provides caloric density; sodium provides taste drive

**Pattern 2: Fat-Sugar** (characteristic of chocolate products, pastries, cream-filled biscuits)
- Triggered when: fat contributes ≥ 20% of calories AND sugar contributes ≥ 20% of calories
- Structural interpretation: the fat-sugar combination is not present in whole foods at these concentrations; it is characteristic of manufactured confectionery

**Pattern 3: Refined Carb + Fat** (characteristic of cookies, crackers, coated cereals)
- Triggered when: carbohydrates ≥ 40% of calories AND fat ≥ 15% of calories AND fiber/carbohydrate ratio ≤ 10%
- Also triggered by architectural markers: presence of extruded grain, glucose syrup, or maltodextrin alongside fat
- Structural interpretation: refined starch + fat at low fiber density is a processing signature, not a whole-food pattern

**Pattern 4: Crunch-Sweet** (characteristic of coated cereals, confectionery bars)
- Triggered when: carbohydrates ≥ 50g/100g AND sugar ≥ 20g/100g AND (fiber ≤ 5g OR crispy cereal present) AND fat ≤ 10g/100g
- Structural interpretation: high-carbohydrate, high-sugar, low-fat, low-fiber — the reward profile of engineered cereal and candy products

### Amplifiers and moderators

**Amplifiers** — ingredients that intensify the hyper-palatability signal (up to 45% amplification):
- Chocolate or compound coating: +15%
- Glucose syrup or maltodextrin: +15%
- Extruded or puffed grain: +15%
- Artificial/natural flavourings: +5%
- Emulsifiers: +5%

**Moderators (matrix relief)** — whole-food structural signals that reduce hyper-palatability severity:
- Nuts or seeds (intact): −15%
- Whole grains: −8%
- Date or fruit paste: −8%

Relief reflects the observation that naturally complex food matrices — nuts in a bar, oats in granola — partially moderate the reward response pattern even when other hyper-palatability signals are present.

### Score impact

Each triggered pattern applies a penalty to the final score (up to −28 per pattern, modulated by amplifiers and moderators). Near-miss patterns (within 80–100% of the trigger threshold) apply half-strength penalties.

- 2 triggered patterns: hard cap of 60
- 3+ triggered patterns: hard cap of 50
- Category relief: products classified as `whole_food_fat` receive +15 points to the hyper-palatability score

The hyper-palatability penalty family is budget-limited: total penalties from this layer are capped to prevent disproportionate scoring impact even when multiple patterns trigger simultaneously.

---

## How processing signals interact

A product with NOVA 4 classification, 4 additive markers, and 2 hyper-palatability patterns would face:
- A NOVA 4 hard cap (final score ≤ 60)
- A 2-pattern hyper-palatability cap (final score ≤ 60)
- A 4-additive-marker cap (final score ≤ 65) — superseded by the lower caps above
- Processing quality and additive quality dimension penalties
- Hyper-palatability penalties

The concern coordination layer ensures these signals are not stacked blindly. Where multiple penalties share the same root concern (e.g., both NOVA 4 and glucose syrup penalize "processing"), the coordinator selects the primary signal and reduces the weight of overlapping signals.

---

## What this means for product display

Products with high processing concerns will typically appear in the D–E grade range. The signal system is specific enough that the primary reason can be stated precisely:

- "Ultra-processed (NOVA 4)" — driven by ingredient markers
- "Engineered fat-sugar combination" — driven by hyper-palatability pattern 2
- "High additive complexity" — driven by additive burden count
- "Refined grain structure with low fiber" — driven by pattern 3

These signals map directly to specific UI language in `ui_language.md`.
