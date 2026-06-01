# Category Analysis

## Why category matters

A calorie threshold that correctly identifies a concerning beverage would incorrectly penalize a walnut. A sugar threshold calibrated for a breakfast cereal would wrongly flag a date-and-nut bar. Evaluating every food against a single universal benchmark produces results that are analytically correct in isolation and practically meaningless in context.

Bari evaluates products against the expectations of their category — not against all foods simultaneously.

---

## The eight categories

| Category | What it covers |
|----------|---------------|
| `whole_food_fat` | Products where caloric density comes primarily from intact fat sources: nut butters, tahini, seeds, avocado-based products, coconut products |
| `snack_bar_granola` | Cereal bars, granola bars, energy bars, flapjacks, granola mixes — the category most associated with health-halo mislabelling |
| `dessert` | Biscuits, cakes, pastries, confectionery, chocolate products — evaluated with awareness that these are treat foods |
| `beverage` | Drinks, juices, plant milks, smoothies, protein shakes |
| `dairy_protein` | Yogurts, quark, skyr, cottage cheese, kefir — products where protein density is a defining characteristic |
| `cereal` | Breakfast cereals, muesli, porridge oats, granola as a meal format |
| `sauce_spread` | Condiments, dips, hummus, sauces, dressings, jams |
| `default` | Products that don't fit a more specific category |

---

## Category-relative calorie density thresholds

Calorie density is scored not against a single threshold, but against a table of thresholds specific to the product's category. The scores below represent the quality score earned at each calorie level for each category.

### `whole_food_fat` — Nuts, seeds, nut butters

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 350 | 90 |
| ≤ 500 | 85 |
| ≤ 650 | 75 |
| ≤ 750 | 65 |
| ≤ 900 | 55 |
| > 900 | 45 |

*Design rationale:* Pure fat is ~900 kcal/100g. A natural almond butter at 600 kcal/100g is not calorie-concerning in the same sense as an engineered 600 kcal/100g bar — it delivers fat from a whole food matrix. Thresholds here reflect this.

### `snack_bar_granola` — Bars and granola

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 150 | 90 |
| ≤ 250 | 75 |
| ≤ 350 | 55 |
| ≤ 430 | 40 |
| ≤ 500 | 25 |
| > 500 | 15 |

*Design rationale:* This category carries the strongest health-halo risk. Products in this category are frequently marketed as health foods while delivering calorie densities approaching confectionery. Thresholds are accordingly strict. An additional rule caps any `snack_bar_granola` with ≥ 430 kcal/100g at a final score of 70 regardless of other signals.

### `dessert` — Biscuits, cakes, confectionery

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 150 | 85 |
| ≤ 250 | 70 |
| ≤ 350 | 55 |
| ≤ 430 | 40 |
| ≤ 520 | 25 |
| > 520 | 15 |

*Design rationale:* Dessert products are evaluated in context — the system does not impose the same calorie expectations on a biscuit as on a meal. But very high calorie density in this category still warrants clear signals.

### `beverage` — Drinks and liquid foods

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 10 | 95 |
| ≤ 25 | 85 |
| ≤ 45 | 70 |
| ≤ 70 | 50 |
| ≤ 100 | 30 |
| > 100 | 15 |

*Design rationale:* Liquid calories are not compensated for by reduced solid food intake in the same way as solid calories. Beverages are evaluated against a strict calorie scale. A 70 kcal/100ml drink earns a score of 50 on this dimension — not because it is bad, but because calorie-containing beverages should be flagged in a product context.

### `dairy_protein` — Yogurts and dairy protein products

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 80 | 90 |
| ≤ 130 | 80 |
| ≤ 180 | 70 |
| ≤ 250 | 55 |
| ≤ 350 | 40 |
| > 350 | 25 |

*Design rationale:* Dairy products with significant protein content earn credit for that density. Full-fat yogurt (80–100 kcal/100g) earns a strong calorie score. Cream-heavy products are flagged.

### `cereal` — Breakfast cereals and muesli

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 300 | 85 |
| ≤ 380 | 70 |
| ≤ 430 | 55 |
| ≤ 480 | 40 |
| ≤ 550 | 25 |
| > 550 | 15 |

*Design rationale:* Plain oats are ~380 kcal/100g. The scale is calibrated so that minimally processed whole grain cereals score well, while heavily sweetened or fat-coated cereals face clear penalties.

### `sauce_spread` — Condiments and spreads

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 150 | 90 |
| ≤ 300 | 75 |
| ≤ 450 | 60 |
| ≤ 600 | 50 |
| ≤ 750 | 40 |
| > 750 | 25 |

*Design rationale:* Spreads and condiments vary enormously — a light hummus at 150 kcal differs structurally from a palm-oil-based chocolate spread at 550 kcal. The scale captures this range while acknowledging that usage quantity for condiments differs from that of main foods.

### `default` — General products

| Calories per 100g | Score |
|-------------------|-------|
| ≤ 150 | 90 |
| ≤ 250 | 80 |
| ≤ 350 | 65 |
| ≤ 450 | 50 |
| ≤ 550 | 35 |
| > 550 | 20 |

---

## How category is determined

Category classification is inferred, not declared. It runs through three stages:

1. **Name matching** — Hebrew and English keywords in the product name are matched against category-specific keyword lists. A strong name match contributes weight 0.7 toward that category.
2. **Ingredient dominance** — Specific ingredient markers signal category membership (e.g., presence of crispy cereal and glucose syrup in a bar context → snack_bar_granola). This contributes weight 0.4.
3. **Retailer category field** — If the retailer provides a category classification, it is used as an additional signal.

If no category reaches sufficient confidence, the product falls through to `default`.

The confidence score for category classification is tracked explicitly. A product with low category confidence (`< 0.5`) receives a −7.5 penalty on overall analytical confidence. This propagates into a confidence ceiling on the final score.

---

## Whole-food protection

The category system works in tandem with a set of floor rules that prevent whole-food products from being misclassified as poor choices:

- **Single-ingredient whole food (NOVA 1):** minimum final score of 75
- **Whole-food fat (NOVA 1–2):** minimum final score of 65

These floors exist because many analytical penalties are calibrated for engineered products. A plain walnut — high in fat, calorie-dense, with a long ingredient list by weight — would be incorrectly penalized without category and whole-food context. The floor ensures the system cannot produce an analytically absurd result for a product that is self-evidently a high-quality whole food.

---

## The health-halo problem

The `snack_bar_granola` category is treated with particular care because it is the category most prone to health-halo effects — products that present as nutritious or "clean" while delivering nutritional profiles closer to confectionery.

Specific rules for this category:
- Products with ≥ 470 kcal/100g and ≥ 15g sugar are hard-capped at 60
- Products with ≥ 430 kcal/100g are hard-capped at 70
- Products with a red label on sugar are hard-capped at 55

These rules fire alongside, not instead of, the normal calorie density scoring. The effective final score is the strictest applicable limit.
