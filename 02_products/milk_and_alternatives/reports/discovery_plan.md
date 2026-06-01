# Milk & Alternatives — First Corpus Discovery Plan

**Created:** 2026-05-17  
**Target corpus size:** 25–40 products  
**Purpose:** Establish a first working dataset that covers structural diversity, not product diversity

---

## Guiding principle

The first corpus must not be a representative sample of what is on shelves. It must be a **structurally diverse** sample that exposes the full range of BSIP2 challenges in this category. One almond milk that exposes structural emptiness is worth more than five almond milks that expose nothing new.

---

## Proposed product type breakdown

### 1. Dairy milk (5–7 products)

| Product type | Priority | Why |
|---|---|---|
| Whole milk (3.5% fat) | High | Reference anchor — intact matrix, complete nutrition |
| Semi-skimmed milk (1.5% fat) | High | Fat reduction without matrix disruption |
| Skimmed milk (0% fat) | Medium | Tests whether fat removal is correctly neutral vs negative |
| Lactose-free whole milk | Medium | Same matrix, different carbohydrate form |
| High-protein milk (4–5g/100ml) | High | Baseline for protein comparison against plant alternatives |
| UHT whole milk | Low | Processing method comparison vs pasteurized |

**Recommended picks:** Whole milk, semi-skimmed, high-protein milk, lactose-free milk (4 products).

---

### 2. Soy milk (3–5 products)

| Product type | Priority | Why |
|---|---|---|
| Unsweetened plain soy milk | High | Most complete plant protein — baseline comparison |
| Sweetened soy milk | High | Sugar addition stress test |
| High-protein soy variant | High | Tests whether isolate enrichment scores differently from intact soy |
| Chocolate soy milk | Medium | Hyper-palatability + complete protein in same product |
| Barista soy milk | Low | Oil/emulsifier system test |

**Recommended picks:** Unsweetened soy, sweetened soy, high-protein soy, chocolate soy (4 products).

---

### 3. Oat milk (4–6 products)

| Product type | Priority | Why |
|---|---|---|
| Unsweetened plain oat milk | High | Beta-glucan benefit vs incomplete protein — ambiguous scoring case |
| Sweetened oat milk | High | Most common shelf variant; sugar addition |
| Barista oat milk | High | Added oils, emulsifiers, texture engineering — high additive load |
| Flavored oat milk (vanilla) | Medium | Sweetener + flavoring without chocolate payload |
| Chocolate oat milk | Medium | Hyper-palatability + oat base |
| "Reduced sugar" oat milk | Low | Marketing language stress test |

**Recommended picks:** Unsweetened oat, sweetened oat, barista oat, flavored oat (4 products).

---

### 4. Almond milk (3–5 products)

| Product type | Priority | Why |
|---|---|---|
| Ultra-low-calorie unsweetened almond milk | High | Primary structural emptiness test — ~13 kcal/100ml |
| Sweetened almond milk | High | Adds sugar to an already-hollow base |
| Enriched/fortified almond milk | High | Micronutrient fortification paradox test |
| "Protein-enriched" almond milk | Medium | Isolate addition to hollow base — synthetic protein quality |
| Vanilla sweetened almond milk | Low | Flavoring + sweetener variant |

**Recommended picks:** Ultra-low-cal unsweetened, sweetened, fortified/enriched (3 products).

---

### 5. Other plant milks (3–4 products)

| Product type | Priority | Why |
|---|---|---|
| Rice milk | Medium | Very high glycemic load, minimal protein — tests carbohydrate handling |
| Coconut milk drink (not canned) | Medium | High sat-fat plant source — tests sat-fat logic in beverages |
| Mixed grain milk (oat + rice blend) | Low | Blend formulation — matrix ambiguity |
| Hemp milk | Low | Omega-3 content — tests beneficial fat handling |

**Recommended picks:** Rice milk, coconut drink (2 products).

---

### 6. Protein-enriched beverages (2–3 products)

| Product type | Priority | Why |
|---|---|---|
| Whey protein milk drink | High | Engineered protein — tests whether satiety logic is gamed |
| Plant protein blend drink | High | Multi-source protein isolate — matrix vs formulation |
| High-protein low-fat dairy shake | Medium | Protein:calorie ratio extremes |

**Recommended picks:** Whey protein drink, plant protein blend (2 products).

---

### 7. Flavored milk and kids drinks (2–3 products)

| Product type | Priority | Why |
|---|---|---|
| Chocolate dairy milk | High | Hyper-palatability in intact dairy matrix |
| Sweetened kids milk drink (e.g. flavored UHT carton) | High | Sugar + marketing target — palatability + presentation mismatch |
| Vanilla flavored milk | Medium | Milder flavoring test |

**Recommended picks:** Chocolate dairy milk, kids sweetened milk drink (2 products).

---

## Proposed first corpus (25 products)

| # | Category | Product type | Priority reason |
|---|---|---|---|
| 1 | Dairy | Whole milk | Matrix anchor |
| 2 | Dairy | Semi-skimmed | Fat reduction reference |
| 3 | Dairy | High-protein milk | Protein comparison baseline |
| 4 | Dairy | Lactose-free whole | Carbohydrate form variation |
| 5 | Soy | Unsweetened plain | Complete plant protein baseline |
| 6 | Soy | Sweetened | Sugar addition test |
| 7 | Soy | High-protein (isolate) | Intact vs isolate distinction |
| 8 | Soy | Chocolate | Palatability + complete protein |
| 9 | Oat | Unsweetened plain | Beta-glucan vs incomplete protein |
| 10 | Oat | Sweetened | Most common shelf variant |
| 11 | Oat | Barista | Oil + emulsifier system |
| 12 | Oat | Vanilla flavored | Flavoring without chocolate payload |
| 13 | Almond | Ultra-low-cal unsweetened | Structural emptiness — critical test |
| 14 | Almond | Sweetened | Sugar on hollow base |
| 15 | Almond | Fortified/enriched | Fortification paradox |
| 16 | Rice | Plain | High glycemic, minimal protein |
| 17 | Coconut drink | Plain | High plant sat-fat |
| 18 | Protein bev. | Whey-enriched milk drink | Engineered protein satiety gaming |
| 19 | Protein bev. | Plant protein blend | Multi-isolate formulation |
| 20 | Flavored dairy | Chocolate milk | Hyper-palatability in intact matrix |
| 21 | Flavored dairy | Kids sweetened carton | Target demographic mismatch |
| 22 | Almond | Protein-enriched almond | Isolate on hollow base |
| 23 | Soy | Barista soy | Oil system in plant milk |
| 24 | Oat | Chocolate oat | Palatability + oat base |
| 25 | Dairy | Skimmed milk | Fat removal stress test |

---

## Retailer sourcing recommendation

**First priority:** Yohananof — existing BSIP0 infrastructure operational.  
**Second priority:** Carrefour — run in parallel once Yohananof scrape is done.

Expect 10–15 products to be available at each retailer. Cross-retailer overlap on dairy is likely high. Cross-retailer overlap on plant milks will depend on brand distribution.

---

## Success criteria for first corpus

The corpus is ready when it contains:
- At least 1 product with fewer than 20 kcal/100ml (structural emptiness test)
- At least 1 product with more than 4g protein/100ml from an intact source
- At least 1 product with more than 4g protein/100ml from an isolate source
- At least 1 product with added oils in ingredient list (barista or protein variant)
- At least 1 product clearly targeting children
- At least 1 chocolate or heavily flavored variant
- At least 1 product with artificial sweeteners

If any of these is missing, the corpus is not structurally complete.
