# The Signal System

## Overview

The BSIP2 engine extracts over 50 structured signals from each product before any scoring begins. These signals fall into five groups: nutritional values, food architecture markers, regulatory flags, structural inferences, and data quality indicators. Every score the system produces is grounded in one or more of these signals.

---

## Group 1 — Nutritional values

Direct values from the nutrition panel, normalized to per-100g.

| Signal | Description |
|--------|-------------|
| `energy_kcal` | Total energy in kilocalories |
| `protein_g` | Protein content |
| `carbohydrates_g` | Total carbohydrates |
| `sugars_g` | Of which sugars |
| `fat_g` | Total fat |
| `saturated_fat_g` | Of which saturated fat |
| `dietary_fiber_g` | Dietary fiber |
| `sodium_mg` | Sodium content |

**Derived signals** computed from the above:
- Fat as a percentage of total calories (`fat_kcal_pct`)
- Sugar as a percentage of total calories (`sugar_kcal_pct`)
- Carbohydrates as a percentage of total calories (`carb_kcal_pct`)
- Fiber-to-carbohydrate ratio (used in glycemic quality and hyper-palatability evaluation)

---

## Group 2 — Food architecture markers

The ingredient list is parsed for the presence of specific structural markers. These are not ingredient-count metrics — they identify functionally significant ingredients that have known relationships with processing level, nutritional quality, or eating behaviour.

| Marker | What it identifies |
|--------|-------------------|
| `added_sugar` | Sugars added during manufacturing beyond intrinsic fruit/dairy sugars |
| `multiple_added_sugars` | Multiple distinct added-sugar sources (e.g., glucose syrup + dextrose + invert sugar) |
| `sweetener` | Non-nutritive sweeteners (artificial or natural) |
| `emulsifier` | Industrial emulsifiers (lecithins, mono/diglycerides) |
| `stabilizer` | Gelling agents, thickeners, modified starches added for texture |
| `protein_isolate` | Concentrated protein extracts (whey isolate, soy isolate) |
| `seed_oil` | Refined seed oils (sunflower, canola, soybean, palm) |
| `whole_food_positive` | Presence of intact whole-food ingredients |
| `glucose_syrup` | Glucose-fructose syrup or corn syrup |
| `maltodextrin` | Rapidly-digested starch derivative used as filler or bulking agent |
| `flavouring` | Added natural or artificial flavours |
| `chocolate_coating` | Chocolate or compound chocolate coating |
| `extruded_or_puffed_grain` | Industrial grain extrusion or puffing (associated with NOVA 4) |
| `crispy_cereal` | Crispy rice or similar puffed cereal component |
| `nut_or_seed` | Whole or minimally processed nuts or seeds |
| `whole_grain` | Declared whole grain ingredients |
| `date_or_fruit_paste` | Whole dried fruit or date paste (a whole-food sweetening signal) |
| `hydrogenated_fat` | Partially or fully hydrogenated fat (trans fat risk signal) |

**Additive burden** is the count of sweeteners + emulsifiers + stabilizers + protein isolates. This is used independently from individual marker signals to evaluate overall additive complexity.

---

## Group 3 — Regulatory flags

Israeli nutrition labeling requires a front-of-pack red label for any of three nutrients exceeding defined thresholds per serving.

| Flag | Threshold condition |
|------|--------------------|
| `red_label_sugar` | Sugar per serving exceeds Israeli red-label threshold |
| `red_label_sodium` | Sodium per serving exceeds Israeli red-label threshold |
| `red_label_saturated_fat` | Saturated fat per serving exceeds Israeli red-label threshold |
| `red_label_count` | Total number of red labels (0–3) |

Red label signals are structural — they indicate that a product exceeds a government-defined limit on a concern nutrient. The count (1 vs. 2+) determines the severity of the guardrail applied.

---

## Group 4 — Structural inferences

Two classification inferences are made from the combination of nutritional signals and ingredient markers. Both are heuristic — they come with an explicit confidence score, and their uncertainty propagates into the product's overall analytical confidence.

### NOVA classification (1–4)

A proxy estimate of food processing level based on the Nova classification system:

| Level | Meaning |
|-------|---------|
| 1 | Unprocessed or minimally processed whole food |
| 2 | Processed culinary ingredient (oils, flours, butter) |
| 3 | Processed food (tinned vegetables, cheese, cured meat) |
| 4 | Ultra-processed product (typically: emulsifiers, glucose syrup, flavourings, extrusion) |

The inference is driven by ingredient markers, ingredient count, and nutritional pattern. The confidence score for NOVA classification affects both the processing quality dimension and the overall product confidence.

### Category classification

Products are assigned to one of eight functional categories:

| Category | Description |
|----------|-------------|
| `whole_food_fat` | Nuts, seeds, nut butters, avocado-based products — naturally calorie-dense |
| `snack_bar_granola` | Cereal bars, granola bars, energy bars, granola mixes |
| `dessert` | Biscuits, cakes, confectionery, chocolate products |
| `beverage` | Drinks, juices, plant milks, protein shakes |
| `dairy_protein` | Yogurts, quark, cottage cheese, dairy-based protein products |
| `cereal` | Breakfast cereals, muesli, porridge oats |
| `sauce_spread` | Spreads, dips, condiments, sauces |
| `default` | Products that don't match a more specific category |

Category drives calorie density evaluation — each category has its own calorie thresholds. Category confidence propagates into analytical confidence.

---

## Group 5 — Data quality indicators

For each critical nutritional field (energy, protein, carbohydrates, fat, fiber, sodium, sugar), the system records whether the value was present in the source data or absent. Missing fields reduce analytical confidence and, at sufficient severity, impose a confidence ceiling on the final score.

Suspicious data patterns — sugar greater than total carbohydrates, saturated fat greater than total fat, energy values outside physiological range — are also flagged and reduce confidence independently.

---

## How signals combine

No single signal produces a score in isolation. Signals feed into dimensions, guardrails, and the hyper-palatability engine, which combine them with defined weights, thresholds, and interaction rules. The same signal can influence multiple dimensions simultaneously — for example, `whole_grain` reduces the processing quality penalty, improves satiety support, and provides partial hyper-palatability matrix relief. This is by design: real nutritional quality is compositional.
