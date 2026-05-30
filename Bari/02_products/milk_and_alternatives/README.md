# Milk & Alternatives — Product Workspace

This directory is the category workspace for dairy milk and plant-based milk alternative products across all retailers.

## Why this category exists

Milk and alternatives is Bari's second major product category after snack bars. It is not simply "milk products." It is a category designed to **stress-test BSIP2 architecture** against problems that snack bars do not expose.

The category deliberately spans a wide nutritional and structural spectrum:
- Whole dairy milk (intact food matrix)
- Ultra-processed plant beverages (water + additives + fortification)
- High-protein engineered drinks
- Sweetened kids drinks
- Barista-format oat milks with oil-based fat systems
- Chocolate and flavored milk (hyper-palatability in liquid form)

This diversity forces BSIP2 to reason structurally rather than by category heuristic.

## Why milk alternatives are strategically important

### 1. Liquid nutrition logic
Beverages should not inherit satiety assumptions designed for solid foods. 200 kcal of oat milk and 200 kcal of a snack bar produce different physiological effects. BSIP2 must not treat them equivalently.

### 2. Structural emptiness
Many plant milks are nutritionally hollow: mostly water, gums, and minerals. A product can pass all individual thresholds (low sugar, low sat-fat, fortified with calcium) while having almost no real nutritional structure. BSIP2 must detect this rather than reward the absence of negatives.

### 3. Source-aware protein quality
Soy milk protein is nutritionally complete. Oat milk protein is not. Isolate-enriched almond milk sits in a different position from intact soy. The source of protein matters, not just the gram count. BSIP2 must distinguish these cases.

### 4. Fortification paradox
A product can be enriched with calcium, vitamin D, B12, and riboflavin while having weak macronutrient structure and heavy additives. Fortification should not carry the same weight as a naturally nutrient-dense matrix.

### 5. Sweetener handling
Plant milks split sharply between unsweetened (very different nutritional profile) and sweetened variants. Sugar-free flavored drinks introduce artificial sweeteners. BSIP2 must handle all three axes: added sugar, natural sugar, and non-caloric sweeteners.

### 6. Matrix integrity in liquids
Whole dairy milk has an intact biological food matrix — fat, protein, lactose, minerals in native association. Reconstructed plant beverages are formulations. BSIP2 should distinguish an intact matrix from an engineered approximation.

## Directory structure

```
milk_and_alternatives\
├── raw_sources\             Raw retailer data (HTML, images) before any BSIP processing
│   ├── carrefour\
│   ├── yohananof\
│   └── future_retailers\
│
├── observations_bsip0\      BSIP0-parsed structured observations, one dir per barcode
│
├── canonical_bsip1\         Cross-retailer consolidated canonical product records
│
├── intelligence_bsip2\      BSIP2 scored products and review artifacts
│
├── comparisons\             Side-by-side product comparisons and category contrast analyses
│
├── reports\                 Analysis reports for this category
│   ├── discovery_plan.md    First corpus selection plan (25–40 products)
│   ├── bsip2_challenge_map.md  Key BSIP2 stress points and conceptual challenges
│   └── golden_candidates.md    Strategically important first test products
│
└── README.md                This file
```

## Data flow

```
raw_sources\ → observations_bsip0\ → canonical_bsip1\ → intelligence_bsip2\
  (HTML/img)     (structured JSON)     (merged record)     (scored + graded)
```

## Expected BSIP2 stress points

| Stress point | Example product | Expected failure mode |
|---|---|---|
| Structural emptiness | Ultra-low-cal almond milk | Scores too high by avoiding negatives |
| Fortification paradox | Fortified oat milk | Micronutrient score inflated despite weak macro structure |
| Liquid satiety | Sweetened oat milk | Satiety logic incorrectly borrowed from solid food |
| Protein quality | Isolate-enriched almond milk | High protein score despite non-intact source |
| Sweetener handling | Sugar-free chocolate milk | Unclear penalty path for artificial sweeteners |
| Matrix integrity | Soy milk vs reconstructed "blend" | Intact soy vs formulated beverage treated equally |
| Barista editions | Barista oat milk | Emulsifier and oil system not penalized |
| Hyper-palatability | Chocolate milk, vanilla shake | Palatability engineering in liquid form not captured |

## Future subcategories

As the dataset grows, subcategories may be split off:

- `dairy_milk\` — whole, semi-skimmed, skimmed, lactose-free, high-protein
- `soy_milk\` — unsweetened, sweetened, protein-enriched
- `oat_milk\` — plain, barista, flavored
- `almond_milk\` — low-calorie, sweetened, enriched
- `other_plant_milk\` — rice, coconut drinks, blends
- `protein_beverages\` — engineered protein drinks and shakes
- `flavored_milk\` — chocolate, vanilla, kids drinks

Subcategory split is deferred until the corpus is large enough to justify it.

## Design principles

This category must not assume:
- Plant milk = healthier
- Dairy milk = healthier
- Low calorie = healthier
- Fortified = healthier
- Unsweetened = automatically good

Every score must be grounded in structural reasoning, not category intuition.