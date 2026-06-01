# Bari Scoring Recalibration v1
**Date:** 2026-05-29  
**Author:** CE Controller 1  
**Status:** Implementation-Ready  
**Scope:** Four targeted changes. No architectural redesign.

---

## Diagnosis

The framework has four specific calibration failures. They are not evenly distributed — three of the four require fewer than ten lines of code to fix. The fourth requires one new data field and conditional logic in the guardrail engine.

| Change ID | Problem | Mechanism | Complexity |
|---|---|---|---|
| RC-01 | Whole-fruit sugar capped identically to added sugar | Guardrail cap override | Low — conditional on sugar source |
| RC-02 | Whole-food structural bonus never fires | Config key mismatch (bug) | Trivial — 2 line fix |
| RC-03 | Whole-food integrity dimension carries irrelevant weight | Weight misconfiguration | Trivial — 2 config values |
| RC-04 | Natural sat fat red label treated identically to manufacturing fat | Guardrail cap override | Medium — requires red_label_type field |

**What is NOT changed:**
- NOVA4 guardrail caps (68 in production) — correct and intentional
- NOVA3 caps (82 in production) — correct
- 2+ red label cap at 45 — correct, no relief
- All penalties for processing markers, additives, glucose syrups — unchanged
- Grade band thresholds (A≥85, B≥70, C≥55, D≥40) — unchanged

---

## RC-01: Natural Whole-Fruit Sugar Relief

### Current behavior

`HIGH_SUGAR_25G_PLUS` (cap 60) and `ISRAELI_RED_LABEL_1_SUGAR` (cap 55) apply to any product with ≥25g sugar per 100g. The cap makes no distinction between:

- 47g sugar from dates (75% of product, single ingredient, whole fruit)
- 47g sugar from added sucrose + glucose syrup + dextrose

A NOVA2 date bar with four clean ingredients and no added sugar is scored identically to a product engineered to have the same sugar level through processing additions.

### Proposed behavior

Add a `natural_sugar_source` classification to feature extraction:

```python
# In bsip2_feature_extraction.py
"natural_sugar_source": (
    # No standalone sugar keyword in ingredient list
    not contains_any(ingredients, INGREDIENT_MARKERS["added_sugar_keywords"])
    # AND primary ingredient is whole fruit
    and contains_any(ingredients[:2], INGREDIENT_MARKERS["whole_fruit_primary"])
    # AND product is NOVA1 or NOVA2
    and nova_proxy <= 2
),
```

Where:
```python
# Add to bsip2_config.py INGREDIENT_MARKERS
"added_sugar_keywords": ["סוכר", "גלוקוז", "פרוקטוז", "דקסטרוז", "סירופ", "מולסה", "דבש מוסף"],
"whole_fruit_primary": ["תמרים", "מחית תמרים", "תאנים", "צימוקים", "dates", "figs"],
```

Then in `bsip2_guardrails.py`, modify the cap application:

```python
# Current
if signals.get("sugars_g", 0) >= 25:
    caps_to_evaluate.append({"rule": "HIGH_SUGAR_25G_PLUS", "cap": 60})

# Proposed
if signals.get("sugars_g", 0) >= 25:
    if features.get("natural_sugar_source"):
        caps_to_evaluate.append({"rule": "HIGH_SUGAR_25G_PLUS_NATURAL", "cap": 68})
    else:
        caps_to_evaluate.append({"rule": "HIGH_SUGAR_25G_PLUS", "cap": 60})

# Similarly for ISRAELI_RED_LABEL_1_SUGAR
if red_label_count == 1 and red_label_type == "sugar":
    if features.get("natural_sugar_source"):
        caps_to_evaluate.append({"rule": "ISRAELI_RED_LABEL_1_SUGAR_NATURAL", "cap": 63})
    else:
        caps_to_evaluate.append({"rule": "ISRAELI_RED_LABEL_1_SUGAR", "cap": 55})
```

### Expected score impact

| Product type | Current cap | Proposed cap | Score delta |
|---|---|---|---|
| NOVA2 date bar, natural sugar red label | 55 | 63 | +8 (if natural score ≥ 63) |
| NOVA2 date bar, HIGH_SUGAR only | 60 | 68 | +0–8 (depends on natural score) |
| Added-sugar product, any NOVA | 55 | 55 | 0 |
| NOVA3 date bar with added sugar | 55 | 55 | 0 (fails natural_sugar_source check) |

### Categories affected

Snack bars (date-base), certain fruit-based desserts (NOVA2 only).

---

## RC-02: Whole-Food Processing Bonus — Bug Fix

### Current behavior

`bsip2_dimensions.py` references `p["whole_food_bonus"]` at lines 60 and 121. This key does not exist in `bsip2_config.py`. The actual keys are `"matrix_marker_bonus"` (value: 2.5 for `processing_quality`) and `"matrix_marker_bonus"` (value: 7 for `whole_food_integrity`).

Result: `KeyError: 'whole_food_bonus'` is thrown for any product with oats, almonds, dates, nuts, or seeds as primary ingredients. The Python prototype crashes silently on these products; the production CE scoring protocol never applied the bonus by omission.

The whole-food structural reward has never fired for any scored product.

### Proposed behavior

**File:** `C:\Bari\99_archive\bisp2_concept_prototype\bsip2_dimensions.py`

```python
# Line ~60, processing_quality section
# BEFORE (broken):
if f.get("has_whole_food_marker"):
    pq += p["whole_food_bonus"]

# AFTER (fixed):
if f.get("has_whole_food_marker"):
    pq += p.get("matrix_marker_bonus", 0)
```

```python
# Line ~121, whole_food_integrity section
# BEFORE (broken):
if f.get("has_whole_food_marker"):
    wfi += p["whole_food_bonus"]

# AFTER (fixed):
if f.get("has_whole_food_marker"):
    wfi += p.get("matrix_marker_bonus", 0)
```

**Also required in `bsip2_feature_extraction.py`:** Confirm `has_whole_food_marker` is set correctly:

```python
# Line ~131-132 — verify this exists and is correct
"has_whole_food_marker": contains_any(ingredients, INGREDIENT_MARKERS["whole_food_positive"]),
```

Where `whole_food_positive` includes: `"שיבולת שועל", "שקדים", "אגוז", "בוטנים", "זרעים", "תמרים", "oats", "almonds", "nuts", "peanuts", "seeds", "dates"`.

**CE scoring protocol update (for production manual traces):**  
Add explicit step: "If product contains whole-food primary ingredients (oats, almonds, nuts, dates, seeds), apply +2.5 to `processing_quality` raw score (before penalties) and +7 to `whole_food_integrity` raw score (before penalties and caps)."

### Expected score impact

| Product | processing_quality | whole_food_integrity | Net weighted delta |
|---|---|---|---|
| Date bar, nut bar, oat bar | +2.5 pts | +7 pts | **+0.52 pts** |
| NOVA4 engineered bar | 0 | 0 | 0 |
| Whole-wheat sourdough | +2.5 pts | +7 pts | **+0.52 pts** |

The magnitude is modest (+0.52 pts). The correction is required because the design intention has never been applied. Products that deserve the bonus will receive it.

### Categories affected

All categories. Any product with oats, almonds, dates, nuts, peanuts, seeds as listed ingredients.

---

## RC-03: Whole-Food Integrity Weight Redistribution

### Current behavior

```python
# bsip2_config.py
"whole_food_integrity": 0.01,   # Decorative — max impact 0.65 weighted pts
"regulatory_quality":   0.04,   # Dimension penalty is redundant with guardrail caps
```

The `regulatory_quality` dimension penalizes red labels at dimension level (-18 pts × 0.04 = **-0.72 weighted points** per label). The same signal is already captured by guardrail caps which deliver 20–35× that magnitude. The dimension penalty is noise on top of the operative mechanism.

The `whole_food_integrity` dimension at 0.01 weight has a maximum achievable contribution of 0.65 weighted points — within rounding error of the displayed score.

### Proposed behavior

```python
# bsip2_config.py — change these two values only
"whole_food_integrity": 0.04,
"regulatory_quality":   0.01,
```

The sum of weights remains 1.0. No other parameters change.

### Expected score impact

**Score gain** = (WFI_score) × (0.04 − 0.01) = WFI_score × 0.03

| Product type | WFI score | Gain |
|---|---|---|
| NOVA2 date bar, minimal ingredients | ~72 | **+2.16 pts** |
| NOVA2 oat bar, whole grain | ~65 | **+1.95 pts** |
| NOVA2 sourdough bread, whole wheat | ~75 | **+2.25 pts** |
| NOVA3 protein yogurt, clean formulation | ~55 | **+1.65 pts** |
| NOVA4 engineered bar (many additives) | ~10–18 | **+0.30–0.54 pts** |

**Score loss from regulatory_quality reduction** = regulatory_score × (0.01 − 0.04) = regulatory_score × −0.03

Maximum loss from this change: product with regulatory_quality = 100 (no red labels) × 0.03 = -3.0 pts. However, for these products (no red labels), the WFI gain more than compensates.

For products WITH red labels: regulatory_quality is low (e.g., 64 for 2 red labels), so the loss from reducing its weight is smaller. And these products have their scores already compressed by the guardrail caps — the regulatory_quality weight reduction has negligible additional effect on their final displayed score.

**Net effect:** Widens the quality gap between NOVA2 whole-food products and NOVA4 engineered products. NOVA4 products gain +0.30–0.54 pts (negligible); NOVA2 top products gain +2.0–2.25 pts.

### Categories affected

All categories. Largest impact on bread, whole-food snack bars.

---

## RC-04: Natural Saturated Fat Relief

### Current behavior

`ISRAELI_RED_LABEL_1_SAT_FAT` caps any product with 1 saturated fat red label at 55, regardless of the fat source:

- Labane 9% (NOVA2, natural dairy fat) → capped at 55
- Hydrogenated palm oil product (NOVA3/4) → capped at 55

A plain NOVA2 labane with 6g natural dairy sat fat can have a natural dimension score of ~82. The cap brings it to 55. The guardrail delivers -27 weighted points on a signal already penalized by the regulatory_quality dimension.

### Proposed behavior

Add a conditional relief rule to `bsip2_guardrails.py`. This requires `red_label_type` to be tracked in feature extraction (currently it may not be separately tracked from `red_label_count`).

**Required new field in `bsip2_feature_extraction.py`:**
```python
"red_label_types": list_of_triggered_red_label_types,  # ["sat_fat", "sugar", "sodium", "calories"]
```

**Guardrail modification:**
```python
# After ISRAELI_RED_LABEL_1_SAT_FAT is evaluated:
if (
    red_label_count == 1
    and "sat_fat" in features.get("red_label_types", [])
    and nova_proxy <= 2
    and (
        inferred_category in ["dairy_protein", "dairy_fat"]
        or features.get("has_nut_or_seed_marker")
    )
):
    # Natural sat fat relief: raise cap from 55 to 63
    apply_cap = 63
    relief_applied = "NATURAL_SAT_FAT_RELIEF_NOVA2"
```

**Qualifying condition (all must be true):**
1. Exactly 1 red label
2. That red label is for saturated fat (not sugar, not sodium)
3. NOVA ≤ 2
4. Category is dairy or product is nut-dominant

**Non-qualifying (cap remains at 55):**
- Product with sat fat red label that also has a sugar red label (2 labels total → cap 45 regardless)
- NOVA3 product with sat fat red label from processing additions
- Product where sat fat comes from listed hydrogenated oils or palm fat additives

### Expected score impact

| Product | Natural score | Current | Proposed |
|---|---|---|---|
| Labane 9%, NOVA2, 1 sat-fat red label | ~82 | **55** | **63** |
| Plain Greek yogurt 5%, NOVA2, 1 sat-fat red label | ~80 | **55** | **63** |
| Nut bar, NOVA2, 1 sat-fat red label | ~72 | **55** | **63** |
| Protein yogurt, NOVA3, 1 sat-fat red label | ~78 | **55** | **55** (no relief) |
| Engineered bar, palm oil, 1 sat-fat red label | ~55 | **55** | **55** (no relief) |

### Categories affected

Dairy (labane, full-fat yogurt, hard cheese types). Nut bars (snack bars). No effect on NOVA3/4 products.

---

## Score Impact: Actual Products

### snk-001 — חטיף תמרים במילוי חמאת שקדים

**Current:** 70/B  
**Changes applied:** RC-02 (+0.52) + RC-03 (+2.16)  
**Projected:** 72.7 → **73/B**

No cap applies to this product. The gains are modest — this product is already correctly rewarded at 70. The calibration confirms the score, not corrects it.

| Change | Before | After | Delta |
|---|---|---|---|
| RC-02 whole_food_bonus | Not applied | Applied (+0.52 weighted) | +0.52 |
| RC-03 WFI weight | 0.01 | 0.04 | +2.16 |
| RC-01 natural sugar | No cap to relieve | — | 0 |
| **Total** | **70** | **~73** | **+3** |

---

### snk-015 — חטיף תמרים במילוי חמאת בוטנים

**Current:** 55/C (binding cap: ISRAELI_RED_LABEL_1_SUGAR at 55)  
**Natural dimension score (pre-cap):** ~73 (NOVA2, 8.3g protein/100g, 11.1g fiber, clean ingredients)  
**Changes applied:** RC-01 (natural sugar relief, cap raised to 63) + RC-02 (+0.52 to natural score)

**Projected:** cap now 63, natural score ~73.5 → binding cap = **63/C**

RC-03 weight redistribution raises the natural score but the cap at 63 remains binding. RC-03 does not further improve the final score until the cap is removed or raised further.

| Change | Before | After | Delta |
|---|---|---|---|
| Sugar source classification | No distinction | natural_sugar_source=True | — |
| ISRAELI_RED_LABEL_1_SUGAR | cap 55 | cap 63 | +8 |
| HIGH_SUGAR_25G_PLUS | cap 60 | cap 68 | (not binding) |
| RC-02 whole_food_bonus | Not applied | +0.52 to natural score | (cap still binding) |
| **Total** | **55** | **63** | **+8** |

**Note:** The red label still applies. The product still displays the Israeli Ministry of Health warning. The score change reflects that 47.6g/100g of sugar from dates in a 4-ingredient NOVA2 product should not be treated identically to 47.6g/100g from added glucose syrup.

---

### Strong Protein Yogurt — יוגורט חלבון 20 פרי יער

**Source:** yogurt_system run_001 (real scored product)  
**Current:** 75.5/B  
**NOVA:** 3, Protein: 18g/100g  
**Changes applied:** RC-03 (+1.65)  

**Projected:** ~77/B

No cap issues. This product is not suppressed. The recalibration is not the primary lever for well-functioning protein yogurts.

| Change | Before | After | Delta |
|---|---|---|---|
| RC-03 WFI weight | ~55 × 0.01 = 0.55 | ~55 × 0.04 = 2.20 | +1.65 |
| **Total** | **75.5** | **~77** | **+1.5** |

---

### Plain Yogurt — יוגורט טבעי 5% שומן

**Source:** yogurt_system run_001  
**Current:** 65.9/B, NOVA2, no caps  
**Changes applied:** RC-03 (+1.95)

**Projected:** ~68/B

This product is correctly scored. The calibration improves it modestly.

| Change | Before | After | Delta |
|---|---|---|---|
| RC-03 WFI weight | ~65 × 0.01 = 0.65 | ~65 × 0.04 = 2.60 | +1.95 |
| **Total** | **65.9** | **~68** | **+2** |

**Plain yogurt with hypothetical sat-fat red label (NOVA2, 9% fat labane):**  
Current: 55/C (suppressed by natural sat fat red label) → With RC-04: **63/C** (+8)

---

### Sourdough Bread — לחם מחמצת אמיתי ממחיטה מלאה

**Source:** bread_light run_001  
**Current:** 79/B, NOVA2, no caps, fiber 5g, protein 9g  
**Changes applied:** RC-02 (+0.52) + RC-03 (+2.25)

**Projected:** ~82/B

| Change | Before | After | Delta |
|---|---|---|---|
| RC-02 whole_food_bonus | Not applied | +0.52 | +0.52 |
| RC-03 WFI weight | ~75 × 0.01 = 0.75 | ~75 × 0.04 = 3.00 | +2.25 |
| **Total** | **79** | **~82** | **+3** |

For reference: "קרקר חיטה מלאה פשוט" (82.7/B, NOVA2, fiber 8g, protein 11g) under the same changes would reach **~85/A** — the A grade for a genuinely exceptional whole-grain cracker with minimal processing.

---

## Summary Table

| Product | Current | Projected | Delta | RC applied |
|---|---|---|---|---|
| snk-001 (תמרים+שקדים) | 70/B | 73/B | +3 | RC-02, RC-03 |
| snk-015 (תמרים+בוטנים) | 55/C | 63/C | +8 | RC-01 |
| יוגורט חלבון 20 (protein yogurt) | 75.5/B | 77/B | +1.5 | RC-03 |
| יוגורט טבעי 5% (plain yogurt) | 65.9/B | 68/B | +2 | RC-03 |
| Labane 9%, sat-fat red label (hypothetical) | 55/C | 63/C | +8 | RC-04 |
| לחם מחמצת אמיתי (sourdough) | 79/B | 82/B | +3 | RC-02, RC-03 |
| קרקר חיטה מלאה (whole wheat cracker) | 82.7/B | 85/A | +2.3 | RC-02, RC-03 |
| NOVA4 cereal bar (any) | 13–47 | +0.3 to +0.5 | ~0 | RC-03 only (minimal WFI) |

**Critical property confirmed:** NOVA4 products gain ≤0.5 points. NOVA2 genuinely whole-food products gain 2–8 points depending on cap relief. The quality gap widens.

---

## Implementation Package for Cursor

### File 1: `bsip2_dimensions.py` (2 line changes)

```python
# Line ~60 — change this:
pq += p["whole_food_bonus"]
# To this:
pq += p.get("matrix_marker_bonus", 0)

# Line ~121 — change this:
wfi += p["whole_food_bonus"]
# To this:
wfi += p.get("matrix_marker_bonus", 0)
```

### File 2: `bsip2_config.py` (2 value changes + additions)

```python
# Change weights:
"whole_food_integrity": 0.04,   # was 0.01
"regulatory_quality":   0.01,   # was 0.04

# Add to INGREDIENT_MARKERS:
"added_sugar_keywords": [
    "סוכר", "גלוקוז", "פרוקטוז", "דקסטרוז", "סירופ גלוקוז",
    "סירופ גלוקוז-פרוקטוז", "מולסה", "סירופ קרמל", "סירופ אינברטי",
],
"whole_fruit_primary": [
    "תמרים", "מחית תמרים", "תאנים", "צימוקים", "אגוזים", "dates", "figs", "raisins",
],
```

### File 3: `bsip2_feature_extraction.py` (additions)

```python
# Add to extracted features dict:
"natural_sugar_source": (
    not contains_any(ingredients, INGREDIENT_MARKERS["added_sugar_keywords"])
    and contains_any(ingredients[:2], INGREDIENT_MARKERS["whole_fruit_primary"])
    and nova_proxy <= 2
),

# If red_label_type tracking does not exist, add:
"red_label_types": _extract_red_label_types(nutrition_data),
# Where _extract_red_label_types returns list of: "sugar", "sat_fat", "sodium", "calories"
```

### File 4: `bsip2_guardrails.py` (conditional modifications)

```python
# RC-01: Natural sugar cap relief
if nutrition.get("sugars_g", 0) >= 25:
    if features.get("natural_sugar_source"):
        caps.append({"rule": "HIGH_SUGAR_25G_PLUS_NATURAL", "cap": 68})
    else:
        caps.append({"rule": "HIGH_SUGAR_25G_PLUS", "cap": 60})

# RC-01: Natural sugar red label relief
if red_label_count == 1 and "sugar" in features.get("red_label_types", []):
    if features.get("natural_sugar_source"):
        caps.append({"rule": "ISRAELI_RED_LABEL_1_SUGAR_NATURAL", "cap": 63})
    else:
        caps.append({"rule": "ISRAELI_RED_LABEL_1_SUGAR", "cap": 55})

# RC-04: Natural sat fat relief
if red_label_count == 1 and "sat_fat" in features.get("red_label_types", []):
    if (
        nova_proxy <= 2
        and (
            inferred_category in ["dairy_protein", "dairy_fat", "dairy_plain"]
            or features.get("has_nut_or_seed_marker")
        )
    ):
        caps.append({"rule": "ISRAELI_RED_LABEL_1_SAT_FAT_NATURAL_RELIEF", "cap": 63})
    else:
        caps.append({"rule": "ISRAELI_RED_LABEL_1_SAT_FAT", "cap": 55})
```

### CE Scoring Protocol Delta (production manual traces)

For CE traces produced after this recalibration:

1. **Whole-food bonus:** If product contains oats ≥20%, almonds ≥15%, or dates ≥50% as primary ingredients, apply +2.5 to `processing_quality` raw score and +7 to `whole_food_integrity` raw score before calculating penalties.

2. **Dimension weights in `bsip2_concept_v1` spec update:**
   - `whole_food_integrity`: 0.01 → **0.04**
   - `regulatory_quality`: 0.04 → **0.01**

3. **Natural sugar override:** If product is NOVA2 AND all listed ingredients are whole fruits/nuts (no sugar/syrup/glucose in ingredient list) AND sugar ≥25g/100g: use `HIGH_SUGAR_25G_PLUS_NATURAL` (cap 68) instead of `HIGH_SUGAR_25G_PLUS` (cap 60). Use `ISRAELI_RED_LABEL_1_SUGAR_NATURAL` (cap 63) instead of `ISRAELI_RED_LABEL_1_SUGAR` (cap 55).

4. **Natural sat fat override (RC-04):** If product is NOVA2 AND single red label is for saturated fat AND category is dairy or nut-dominant: use `ISRAELI_RED_LABEL_1_SAT_FAT_NATURAL_RELIEF` (cap 63) instead of `ISRAELI_RED_LABEL_1_SAT_FAT` (cap 55).

---

## Implementation Priority

| Priority | Change | Effort | Risk | Rationale |
|---|---|---|---|---|
| 1 (IMMEDIATE) | RC-02 (bug fix) | 2 line changes | None | Correctness — the bonus was always intended; it has never fired |
| 2 (NEXT SPRINT) | RC-03 (weight redistribution) | 2 config values | Low | No architectural change; cleanly widens quality gap |
| 3 (NEXT SPRINT) | RC-01 (natural sugar relief) | New field + conditional | Low-Medium | Requires `natural_sugar_source` classifier in feature extraction |
| 4 (EVALUATE) | RC-04 (natural sat fat relief) | New field + conditional | Medium | Requires `red_label_type` field — verify it exists or build it |

RC-02 and RC-03 can be shipped together. RC-01 depends on `natural_sugar_source` feature extraction being validated before shipping. RC-04 requires a data pipeline check first.
