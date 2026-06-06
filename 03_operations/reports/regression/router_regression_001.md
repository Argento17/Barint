# BSIP2 Router v2 Regression Report

**Run date:** 2026-06-05 16:39 UTC
**Router:** router_v2
**Corpus:** v1
**Overall:** PASS

| Status | Count |
|--------|-------|
| PASS   | 16  |
| WARN   | 0  |
| FAIL   | 0  |
| TOTAL  | 16   |

---

## Results

### ✓ `wff_leakage_granola_nuts` — PASS

**Granola with almonds, hazelnuts and olive oil — ingredient WFF signals must NOT win over granola anchor**  
Failure mode tested: `whole_food_fat leakage`  
Category: **snack_bar_granola** (expected: snack_bar_granola) | Conf: 0.9 (high) | Anchor: True | Subtype: granola
Raw scores: `whole_food_fat=2.200  snack_bar_granola=2.100  cereal=0.550`

### ✓ `protein_contamination_granola` — PASS

**Granola bar with whey protein isolate in ingredient list — must NOT route to dairy_protein**  
Failure mode tested: `protein contamination`  
Category: **snack_bar_granola** (expected: snack_bar_granola) | Conf: 0.9 (high) | Anchor: True | Subtype: granola
Raw scores: `snack_bar_granola=3.200  cereal=0.550  dessert=0.500`

### ✓ `dairy_flavor_contamination_biscuit` — PASS

**Yogurt-flavored biscuit — must NOT route to dairy_protein despite yogurt mention**  
Failure mode tested: `dairy flavor contamination`  
Category: **snack_bar_granola** (expected: snack_bar_granola) | Conf: 0.92 (high) | Anchor: False | Subtype: None
Suppressed signals: `dairy_protein:יוגורט(flavor_suppressor)`
Raw scores: `snack_bar_granola=1.150  whole_food_fat=0.250  dairy_protein=0.095`

### ✓ `real_yogurt_anchors` — PASS

**Plain yogurt with flavor — anchor fires; must be dairy_protein**  
Failure mode tested: `anchor stability`  
Category: **dairy_protein** (expected: dairy_protein) | Conf: 0.92 (high) | Anchor: True | Subtype: yogurt
Raw scores: `dairy_protein=0.950`

### ✓ `beverage_plant_milk_oat` — PASS

**Oat drink (Oatly-style) — must route to beverage via liquid gate**  
Failure mode tested: `beverage leakage`  
Category: **beverage** (expected: beverage) | Conf: 0.74 (medium) | Anchor: False | Subtype: None
Raw scores: `beverage=2.400  cereal=1.400  whole_food_fat=0.250`

### ✓ `beverage_almond_plant_milk` — PASS

**Almond plant milk with no 'משקה' in name — plant_milk heuristic must catch it**  
Failure mode tested: `beverage leakage`  
Category: **beverage** (expected: beverage) | Conf: 0.82 (high) | Anchor: False | Subtype: None
Raw scores: `beverage=2.000  whole_food_fat=0.975`

### ✓ `anchor_almond_butter` — PASS

**Almond butter — anchor must fire for whole_food_fat**  
Failure mode tested: `anchor stability`  
Category: **whole_food_fat** (expected: whole_food_fat) | Conf: 0.93 (high) | Anchor: True | Subtype: nut_butter
Raw scores: `whole_food_fat=2.475  beverage=0.600`

### ✓ `anchor_muesli` — PASS

**Muesli with fruit — anchor must fire for snack_bar_granola**  
Failure mode tested: `anchor stability`  
Category: **snack_bar_granola** (expected: snack_bar_granola) | Conf: 0.88 (high) | Anchor: True | Subtype: muesli
Raw scores: `whole_food_fat=1.950  snack_bar_granola=1.900  dessert=1.700  cereal=0.550`

### ✓ `anchor_cornflakes` — PASS

**Cornflakes with added protein — anchor must fire for cereal**  
Failure mode tested: `anchor stability`  
Category: **cereal** (expected: cereal) | Conf: 0.93 (high) | Anchor: True | Subtype: cornflakes
Raw scores: `cereal=2.100  dairy_protein=0.700  snack_bar_granola=0.300`

### ✓ `context_gate_mixed_nuts` — PASS

**Mixed nuts — WFF context gate should fire (name IS a fat product)**  
Failure mode tested: `wff_context_gate`  
Category: **whole_food_fat** (expected: whole_food_fat) | Conf: 0.92 (high) | Anchor: False | Subtype: None
Raw scores: `whole_food_fat=3.100`

### ✓ `anchor_granola_cereal` — PASS

**Granola cereal (morning position) — more specific anchor wins over plain granola anchor**  
Failure mode tested: `anchor specificity`  
Category: **cereal** (expected: cereal) | Conf: 0.9 (high) | Anchor: True | Subtype: granola_cereal
Raw scores: `cereal=3.400  snack_bar_granola=2.100  whole_food_fat=0.250`

### ✓ `anchor_kefir` — PASS

**Kefir — anchor must fire for dairy_protein with kefir subtype**  
Failure mode tested: `anchor stability`  
Category: **dairy_protein** (expected: dairy_protein) | Conf: 0.93 (high) | Anchor: True | Subtype: kefir
Raw scores: `dairy_protein=0.950`

### ✓ `anchor_cream_cheese` — PASS

**Cream cheese — anchor must fire to dairy_protein (TASK-145)**  
Failure mode tested: `cream-cheese anchor gap (run_cheese_001 QA-CHS-001)`  
Category: **dairy_protein** (expected: dairy_protein) | Conf: 0.93 (high) | Anchor: True | Subtype: cream_cheese
Raw scores: ``

### ✓ `anchor_cheese_spread` — PASS

**Cheese spread (ממרח גבינה) — anchor to dairy_protein (TASK-145)**  
Failure mode tested: `cream-cheese anchor gap`  
Category: **dairy_protein** (expected: dairy_protein) | Conf: 0.92 (high) | Anchor: True | Subtype: cheese_spread
Raw scores: `sauce_spread=1.300  dairy_protein=1.150  whole_food_fat=0.800`

### ✓ `exclusion_napoleon_cake` — PASS

**Napoleon CAKE must NOT route to dairy via the נפוליאון anchor (TASK-145)**  
Failure mode tested: `cream-cheese anchor over-fire`  
Category: **default** (expected: default) | Conf: 0.3 (uncertain) | Anchor: False | Subtype: None
⚠ Instability: total_signal_mass<0.3 — routing to default
Raw scores: `snack_bar_granola=0.150`

### ✓ `exclusion_philadelphia_seasoning` — PASS

**Philadelphia SEASONING blend must NOT route to dairy via the פילדלפיה anchor (TASK-153 / EV-030)**  
Failure mode tested: `cream-cheese anchor over-fire (seasoning blend)`  
Category: **default** (expected: default) | Conf: 0.3 (uncertain) | Anchor: False | Subtype: None
⚠ Instability: total_signal_mass<0.3 — routing to default
Raw scores: ``

---

## Signal Suppression Log

These cases had contaminating signals that were suppressed by context gating.

- **dairy_flavor_contamination_biscuit** (snack_bar_granola): dairy_protein:יוגורט(flavor_suppressor)
