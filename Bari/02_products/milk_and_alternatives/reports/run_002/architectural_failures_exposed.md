# Architectural Failures Exposed — Real Retailer Corpus (Run 002)

**Generated:** 2026-05-17  
**Corpus:** 20 real Yohananof products  
**BSIP2 version:** proto_v0

---

## Overview

Run 002 with real retailer data confirmed 4 distinct architectural failures in BSIP2 proto_v0. These are not edge cases — they affect 3 of the 20 products directly (15%) and expose structural gaps in category classification, gate calibration, and NOVA penalty weighting.

---

## Failure 1: Beverage Liquid Gate — Category Misclassification

### Affected Products

| Barcode | Product Name | Classified As | Should Be | Score Impact |
|---------|-------------|---------------|-----------|--------------|
| 5411188112709 | אלפרו שקדים ללא סוכר | `whole_food_fat` | `beverage` | −7 to −12 pts |
| 5411188124689 | אלפרו שיבולת שועל ללא סוכר | `cereal` | `beverage` | minor |

### Root Cause

The beverage classifier requires a **liquid keyword in the product name only**:

```
liquid_keywords = ["מ\"ל", "ליטר", "משקה", "בקבוק", "שתייה"]
```

**Alpro almond (5411188112709):** Product name "אלפרו שקדים ללא סוכר" contains no liquid keyword. The word "שקדים" (almonds) triggers the `whole_food_fat` classifier (almond = whole food fat) before any liquid signal can override.

**Alpro oat (5411188124689):** Product name "אלפרו שיבולת שועל ללא סוכר" contains no liquid keyword. "שיבולת שועל" (oat/spelt) matches the `cereal` classifier.

### Cascade Effects

For Alpro almond, `whole_food_fat` classification causes two compounding errors:

1. **Category-specific scoring parameters** for `whole_food_fat` differ from `beverage` — energy density thresholds, protein expectations, and fat quality weights are calibrated for nuts/oils, not dilute plant milks.

2. **SE gate fires:** At 15 kcal/100ml, the SE (Structural Emptiness) gate triggers because `whole_food_fat` category has no liquid exception. With calorie_density = 0 and protein_quality = 0 under `whole_food_fat` parameters, the SE gate drops the score floor from ~45–50 to 38.1 (E grade).

For Alpro oat, the `cereal` category scores the product differently but the error is less severe because oat milk scoring parameters are closer to cereal than almond is to whole_food_fat.

### Evidence

```
Real product: אלפרו שקדים ללא סוכר
  Score under whole_food_fat: 38.1 (E)
  Estimated score under beverage:  ~45–50 (D)
  
Yohananof listing title: "אלפרו שקדים ללא סוכר 1 ליטר"  ← ליטר present on RETAILER LISTING
BSIP0 discovery.json name_field: "אלפרו שקדים ללא סוכר"  ← ליטר stripped in short name
```

The retailer listing includes "1 ליטר" but the discovery script captures the short product name, which omits the volume. The liquid gate checks the captured name, not the full listing title.

### Classification

**Severity: HIGH** — Misclassifies a legitimate plant milk as a food category, triggering a secondary gate that compounds the error.

---

## Failure 2: SE Gate — Over-Penalty for Ultra-Low-Calorie Beverages

### Affected Products

| Barcode | Product Name | kcal/100ml | SE Fires? | Score |
|---------|-------------|-----------|-----------|-------|
| 5411188112709 | אלפרו שקדים ללא סוכר | 15 | YES | 38.1 (E) |

### Root Cause

The SE (Structural Emptiness) gate fires when ALL 5 conditions are true:
1. `energy_kcal < 20`
2. `protein_g < 3`
3. `fiber_g < 1.5`
4. `fat_g < 2`
5. `engineered_signal` (≥2 additive categories)

Alpro almond (15 kcal) meets conditions 1–4 by its nature as a dilute almond drink. For condition 5, the product has calcium carbonate + emulsifier (lecithin) → classified as having ≥2 additive categories.

### The Design Problem

The SE gate was designed to penalize **diet sodas and sports drinks** that are nutritionally empty through engineering (artificial sweeteners, gums, flavors). Almond milk is nutritionally sparse because it is predominantly water with ~3% almond content — a structural property of the beverage category, not an engineering exploit.

The gate does not distinguish between:
- "Empty by engineering" (diet drinks, engineered protein waters)
- "Empty by nature of category" (dilute plant milks, herbal teas)

A product like Coca-Cola Zero meets the same gate profile as Alpro Almond. This is architecturally incorrect.

### Evidence from Non-SE Products

```
Oatly no-sugar oat:  44 kcal/100ml → SE does not fire → 50.0 (D)
Alpro almond:        15 kcal/100ml → SE fires → 38.1 (E) ← 11.9 pt gap from SE alone
```

The 11.9 point gap between these two products is driven entirely by the SE gate. Nutritionally, Alpro almond is not inferior to Oatly oat — it is simply less calorie-dense.

### Classification

**Severity: HIGH** — Category-agnostic gate punishes a product for its defining nutritional characteristic. 

---

## Failure 3: Functional Additive Conflation — Inulin as NOVA 4 Trigger

### Affected Products

| Barcode | Product Name | NOVA | Score | Key Ingredient |
|---------|-------------|------|-------|----------------|
| 7290119385560 | משקה סויה בריסטה אלפרו | 4 | 46.8 (D) | inulin |
| 7290110324926 | משקה סויה ללא תוספת סוכר | 3 | 56.2 (C) | none |

### Root Cause

Inulin (chicory root fiber) is classified as a `processed_food_modifier` in BSIP2's NOVA taxonomy, triggering NOVA 4. This drops the soy barista from NOVA 3 (which plain soy occupies due to its acidifiers/stabilizers) to NOVA 4.

The 9.4-point gap between plain soy (NOVA 3) and barista soy (NOVA 4) is attributable primarily to the inulin classification.

### The Design Problem

Inulin is a prebiotic dietary fiber with established health benefits. Its presence in barista oat/soy is functional (fiber enrichment, mouthfeel) rather than a processed food signal. The NOVA 4 classification framework from the original NOVA paper classifies inulin as an indicator of ultra-processing, but the original NOVA research applies to full dietary patterns, not individual product scoring.

In BSIP2, the same NOVA 4 penalty applies whether a product adds:
- Inulin (fiber)  
- Monk fruit extract (sweetener)
- Artificial flavoring

This conflation is architecturally incorrect for a product-level scoring system.

### Evidence

```
Soy barista: soya (water + soy protein) + sunflower oil + inulin + minerals + flavoring
Soy plain:   soya + water + calcium salts + acidity regulator

NOVA assignment: barista → 4, plain → 3
Score gap: 9.4 pts
Inulin-specific penalty: estimated 4–6 pts (via NOVA 3→4 transition)
```

### Classification

**Severity: MEDIUM** — Affects barista/functional beverage products specifically. Does not affect plain formulations.

---

## Failure 4: NOVA 4 Catastrophic Penalty for Predominantly Real-Food Products

### Affected Products

| Barcode | Product Name | NOVA | Real Food % | Score |
|---------|-------------|------|------------|-------|
| 7290110324773 | משקה חלב גו 27g חלבון | 4 | ~84% dairy | 39.5 (E) |
| 7290114313285 | מולר פרוטאין בטעם בננה | 4 | ~70% dairy | 47.7 (D) |

### Root Cause

Go Milk (27g protein) contains: whole milk + skim milk concentrate + dairy protein concentrate + vanilla flavoring + monk fruit extract. The product is approximately 84% dairy by mass. The 3 ultra-processed signals (flavoring, monk fruit, protein concentrate) trigger NOVA 4.

The NOVA 4 cap in BSIP2 limits the maximum score for any NOVA 4 product. This cap is designed to prevent engineered products from scoring high by stacking positive nutritional signals. For Go Milk, which has 7.4g/100ml protein (vs 3.3g for whole milk), the protein density is genuinely high — but the NOVA 4 cap prevents this from contributing meaningfully.

### The Design Problem

BSIP2 does not model **degree of processing relative to base food proportion**. A product that is 84% real dairy with 3 flavoring/sweetening additives receives the same NOVA 4 treatment as a product that is 0% real food with 20 additives.

The architecture has no concept of:
- "Ultra-processed modifier on a real food base" (Go Milk)
- "Fully synthetic ultra-processed product" (engineered sports drink)

Both are NOVA 4. Both get the NOVA 4 cap. The score gap between Go Milk (39.5) and Alpro almond (38.1) is only 1.4 points — despite Go Milk having 14.8× more protein and being primarily real dairy.

### Comparison: NOVA Floor vs NOVA 4 Cap Asymmetry

```
Whole milk (NOVA 1):    floor = 75.0 (B) — floor protects single-ingredient whole foods
Go Milk (NOVA 4):       cap prevents score > ~50, actual = 39.5 (E)
Difference: 35.5 pts

Whole milk protein:     3.3g/100ml
Go Milk protein:        7.4g/100ml
Go Milk should outperform whole milk on protein_quality dimension — but NOVA cap erases this
```

### Classification

**Severity: MEDIUM** — Affects engineered dairy products specifically. The E grade for Go Milk is defensible from a food system perspective (NOVA 4 ultra-processed = discourage), but may be disproportionate for the target consumer (protein athlete drinks).

---

## Failure Summary Table

| Failure | Affected Products | Severity | Score Impact | Fix Complexity |
|---------|-----------------|----------|--------------|----------------|
| F1: Beverage liquid gate too narrow | 2 (Alpro almond, Alpro oat) | HIGH | −7 to −12 pts | Low (add brand/keyword fallback) |
| F2: SE gate category-agnostic | 1 (Alpro almond) | HIGH | −11.9 pts | Medium (add category exemption) |
| F3: Inulin as NOVA 4 trigger | 1 (Soy barista) | MEDIUM | −4 to −6 pts | Medium (functional fiber taxonomy) |
| F4: NOVA 4 cap vs real-food base | 2 (Go Milk, Müller) | MEDIUM | context-dependent | High (proportional NOVA model) |

---

## What the Architecture Got Right

Not all outcomes were failures. The following behaviors were confirmed correct by real data:

| Behavior | Product Evidence | Verdict |
|----------|-----------------|---------|
| NOVA 1 floor at 75 | 3 whole milks all score exactly 75.0 | CORRECT |
| Identical formula = identical score | Oatly barista + barista frothing: both 48.8 | CORRECT |
| NOVA 2 only −1.8 pts vs NOVA 1 for enzymatic processing | LF+protein = 73.2 vs 75.0 | CORRECT |
| Carrageenan NOVA 3 penalty (~15 pts) | 1% enriched dairy = 58.3 | ARGUABLE (see F4 context) |
| Plant milk ceiling below dairy | Best plant milk = 66.1 (C) vs dairy floor = 73.2 (B) | CORRECT by design |
| Sugar addition tracking across soy spectrum | 30-pt spread from plain soy to chocolate soy | CORRECT |

---

## Priority Order for Fixes

1. **Fix F1 (liquid gate):** Broadest impact, lowest complexity. Brand + ingredient liquid signals should override the name-only gate. See `beverage_modifier_recommendation.md`.

2. **Fix F2 (SE gate):** Requires adding a `beverage` category exemption or raising the kcal threshold for plant milk categories. Low complexity fix once F1 is resolved (correct classification required first).

3. **Fix F3 (inulin):** Requires a `functional_fiber` taxonomy class that distinguishes inulin/chicory from `processed_food_modifier`. Medium complexity — requires NOVA taxonomy extension.

4. **Fix F4 (NOVA 4 real food base):** Requires modeling `real_food_fraction` in the NOVA scoring modifier. High complexity — architectural change, not a parameter tweak.
