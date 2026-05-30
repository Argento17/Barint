# Beverage Modifier Recommendation — BSIP2 proto_v0

**Generated:** 2026-05-17  
**Based on:** Run 002 real retailer corpus (20 Yohananof products)  
**Status:** RECOMMENDATION ONLY — do not implement until explicitly approved

---

## Preamble

This document proposes concrete BSIP2 changes based on failures identified in run_002. Each recommendation is derived from real product evidence. No recommendation is based on hypothetical or simulated products.

Implementation order follows the priority ranking in `architectural_failures_exposed.md`.

---

## Recommendation 1: Expand the Beverage Liquid Gate

### Current Behavior

```python
# Current implementation (pseudo-code)
LIQUID_KEYWORDS = ["מ\"ל", "ליטר", "משקה", "בקבוק", "שתייה"]

def classify_category(product_name, ingredients, ...):
    if any(kw in product_name for kw in LIQUID_KEYWORDS):
        return "beverage"
    # Falls through to ingredient/taxonomy classifiers
```

Category classification reads `product_name` only. Products whose retailer listing includes "1 ליטר" but whose scraped short name omits it fall through to taxonomy classifiers.

### Proposed Change

Add two fallback signals **after** the name check and **before** the ingredient taxonomy:

**Signal A — Brand-based fallback:**

```python
KNOWN_PLANT_MILK_BRANDS = {"alpro", "אלפרו", "oatly", "אוטלי", "vitariz", "ויטאריז", "silk", "provamel"}

brand_token = product_name.lower().split()[0] if product_name else ""
if brand_token in KNOWN_PLANT_MILK_BRANDS:
    return "beverage"
```

Rationale: Alpro and Oatly are exclusively beverage brands in the Israeli milk market. If a product has one of these brand tokens and no competing solid-food signal, it is a beverage.

**Signal B — Plant-milk keyword + NOVA context:**

```python
PLANT_MILK_BASE_TERMS = ["שקדים", "שיבולת שועל", "אורז", "קוקוס", "סויה", "כשות", "שומשום"]
EXCLUDES_SOLID = ["חמאה", "גבינה", "יוגורט", "גלידה", "קוטג"]

if (any(term in product_name for term in PLANT_MILK_BASE_TERMS)
    and not any(ex in product_name for ex in EXCLUDES_SOLID)
    and nova_classification in (2, 3, 4)):  # plant milks are never NOVA 1
    return "beverage"
```

Rationale: "שקדים" alone is ambiguous (could be a nut product). But "שקדים" + NOVA 2/3/4 + no solid-food signal strongly indicates a processed plant milk.

**Signal C — Volume mention in raw listing title (BSIP0 enhancement):**

In `04_parse_and_build_bsip1.py`, preserve the full listing title from `discovery.json` alongside the short product name. The liquid gate should check both:

```python
listing_title = bsip0.get("discovery", {}).get("listing_title", "")
short_name = bsip0.get("product_name", "")
gate_text = f"{short_name} {listing_title}"

if any(kw in gate_text for kw in LIQUID_KEYWORDS):
    return "beverage"
```

This is the cleanest fix: no heuristics, just using already-available data.

### Impact

| Product | Before | After |
|---------|--------|-------|
| אלפרו שקדים ללא סוכר (5411188112709) | whole_food_fat | beverage |
| אלפרו שיבולת שועל ללא סוכר (5411188124689) | cereal | beverage |

Estimated score change: Alpro almond +7 to +12 pts (E → D); Alpro oat minor improvement.

### Implementation Complexity: Low

Changes required:
1. `04_parse_and_build_bsip1.py`: preserve `listing_title` in BSIP1 JSON
2. BSIP2 category classifier: check `listing_title` in gate logic
3. Optional: add brand-based fallback as belt-and-suspenders

---

## Recommendation 2: Add Category Exemption to SE Gate

### Current Behavior

SE (Structural Emptiness) gate fires when:
```
energy_kcal < 20 AND protein_g < 3 AND fiber_g < 1.5 AND fat_g < 2 AND engineered_signal
```

Gate is category-agnostic. Fires on Alpro almond (15 kcal) same as it would fire on a diet cola.

### Proposed Change

Add a **beverage category exemption** for dilute plant milks:

```python
DILUTE_PLANT_MILK_EXEMPT = True  # new config flag

def se_gate_fires(product, category):
    if DILUTE_PLANT_MILK_EXEMPT and category == "beverage":
        # For beverages, require engineered_signal AND at least one flavor/sweetener
        # Pure dilution (water + plant + minerals) does not trigger SE
        has_sweetener = product.additive_flags.get("sweetener", False)
        has_flavoring = product.additive_flags.get("flavoring", False)
        if not (has_sweetener or has_flavoring):
            return False  # SE does not fire on plain dilute plant milks
    
    # Original SE logic for all other cases
    return (
        product.energy_kcal < 20
        and product.protein_g < 3
        and product.fiber_g < 1.5
        and product.fat_g < 2
        and product.engineered_signal
    )
```

Alternative (simpler): Raise the kcal floor for `beverage` category from 20 to 10:

```python
kcal_threshold = 10 if category == "beverage" else 20
```

This would exempt Alpro almond (15 kcal > 10) while still catching true diet beverages approaching 0 kcal.

### Impact

| Product | Before | After (with F1 fix) |
|---------|--------|---------------------|
| אלפרו שקדים ללא סוכר | 38.1 (E), SE fires | ~45–50 (D), SE exempt |

Note: Recommendation 2 depends on Recommendation 1 being implemented first. If Alpro almond remains in `whole_food_fat`, the beverage exemption cannot apply.

### Implementation Complexity: Low-Medium

Changes required:
1. BSIP2 SE gate function: add category parameter and exemption logic
2. Integration test: verify Alpro almond score rises without diet beverages also rising

---

## Recommendation 3: Functional Fiber Taxonomy Class

### Current Behavior

Inulin (chicory root fiber) classified as `processed_food_modifier` → contributes to NOVA 4.

### Proposed Change

Add `functional_fiber` as a distinct additive category that:
- Does NOT trigger `processed_food_modifier`
- Counts positively in fiber estimation if no explicit fiber value is available
- Does NOT increment the NOVA-4 additive counter

```python
# In NOVA taxonomy
ADDITIVE_CLASSES = {
    "sweetener": {"nova_signal": 4, "additive_quality_hit": True},
    "artificial_flavor": {"nova_signal": 4, "additive_quality_hit": True},
    "processed_food_modifier": {"nova_signal": 4, "additive_quality_hit": True},
    "functional_fiber": {"nova_signal": 3, "additive_quality_hit": False},  # NEW
    "stabilizer": {"nova_signal": 3, "additive_quality_hit": True},
    ...
}

FUNCTIONAL_FIBERS = ["inulin", "אינולין", "chicory root", "שורש עולש", "FOS", "GOS", "pea fiber", "סיבי אפונה"]

def classify_additive(ingredient_name):
    if any(f in ingredient_name.lower() for f in FUNCTIONAL_FIBERS):
        return "functional_fiber"
    ...
```

### Impact

| Product | Before | After |
|---------|--------|-------|
| משקה סויה בריסטה אלפרו (7290119385560) | NOVA 4, 46.8 (D) | NOVA 3 (estimated), ~51–54 (D) |

### Implementation Complexity: Medium

Changes required:
1. BSIP2 additive taxonomy: add `functional_fiber` class
2. Additive classifier: add functional fiber keyword matching
3. NOVA assignment logic: `functional_fiber` → max NOVA 3 contribution, not NOVA 4

---

## Recommendation 4: Real-Food Base Fraction Modifier (Deferred)

### Current Behavior

NOVA 4 cap applies uniformly regardless of real-food proportion in product.

### Proposed Change (Conceptual — Not Ready for Implementation)

Add a `real_food_base_fraction` field to BSIP1:

```json
{
  "real_food_base_fraction": 0.84,  // Go Milk: ~84% dairy
  "engineering_layer": "flavoring + sweetener + protein concentrate"
}
```

In BSIP2 scoring:

```python
if nova == 4 and real_food_fraction >= 0.70:
    # "NOVA 4 on a real food base" — apply partial cap, not full cap
    cap_modifier = real_food_fraction  # 0.84 → 84% of cap restriction lifted
    effective_cap = BASE_NOVA4_CAP + (1 - BASE_NOVA4_CAP) * cap_modifier * 0.3
```

### Why Deferred

Estimating `real_food_base_fraction` from ingredient lists requires:
1. Quantitative ingredient proportion estimation (Yohananof does not display percentages)
2. A taxonomy of "base food" vs "additive" ingredients
3. Validation that the estimation is reliable before using it in scoring

This is a significant architectural addition. It should not be implemented until:
- The liquid gate (Rec 1) and SE gate (Rec 2) fixes are validated on a larger corpus
- A quantitative ingredient estimation module is prototyped and tested separately

**Status: Deferred to BSIP2 proto_v1 or later.**

---

## Implementation Roadmap

| Priority | Recommendation | Complexity | Prerequisite | Expected Run |
|----------|---------------|-----------|--------------|-------------|
| 1 | Liquid gate expansion (brand + listing_title) | Low | None | proto_v0.1 |
| 2 | SE gate beverage exemption | Low-Medium | Rec 1 | proto_v0.1 |
| 3 | Functional fiber taxonomy | Medium | None | proto_v0.2 |
| 4 | Real-food base fraction modifier | High | Separate module | proto_v1+ |

---

## Validation Criteria for Recommendations 1 + 2

After implementation, re-run BSIP2 on the 20-product run_002 corpus. The following outcomes should hold:

| Check | Expected |
|-------|---------|
| Alpro almond category | `beverage` (not `whole_food_fat`) |
| Alpro almond score | 45–52 (D), not E |
| Alpro almond SE gate | Does NOT fire |
| Alpro oat category | `beverage` (not `cereal`) |
| Whole milk scores | Unchanged (75.0) — fix must not affect NOVA 1 products |
| Oatly barista scores | Unchanged (48.8) — fix must not affect already-correctly-classified products |
| Go Milk score | Unchanged (~39.5) — Rec 1+2 do not address NOVA 4 cap failure |

Run the full 20-product batch and confirm no regressions on the 17 correctly-classified products before declaring the fix validated.

---

## What NOT to Change (Constraints)

The following behaviors are **architecturally correct** and must NOT be changed as part of these recommendations:

1. **NOVA 1 floor at 75** — Confirmed working correctly. Do not alter.
2. **Identical formula = identical score** — Oatly barista and barista frothing correctly receive 48.8. The architecture is right to not distinguish marketing variants.
3. **Plant milk ceiling below dairy** — The best plant milk scoring lower than whole dairy is a design intent, not a bug. Do not attempt to close this gap.
4. **Carrageenan penalty (NOVA 3)** — The 1% enriched dairy (7290107932134) correctly scores lower for carrageenan as stabilizer. This is working as designed.
