# Bari Intelligence — Architectural Outcomes
## BSIP2 run_003 Post-Fix Assessment

**Date:** 2026-05-18

---

## What Changed After the Fixes

### Fix 1: Beverage Liquid Gate Expansion

**Problem identified in run_002:**
Alpro Almond (5411188112709) was classified as `whole_food_fat` because its product
name ('אלפרו שקדים ללא סוכר') contained no liquid-volume keyword. The beverage gate
zeroed the beverage score, allowing the 'שקד' (almond) signal in whole_food_fat to win.

Alpro Oat (5411188124689) was classified as `cereal` for the same reason:
'שיבולת שועל' (oat) had a strong cereal signal that won over a zero'd beverage score.

**Fix applied:**
The liquid gate now checks three fallback signals before zeroing beverage:
- **Fallback A** (boost +0.85): `nutrition_basis_claimed` field contains liquid unit
  (e.g. 'ל1 ליטר'). This is already-available BSIP1 data — no heuristics required.
- **Fallback B** (boost +0.75): Product brand is in `KNOWN_PLANT_MILK_BRANDS` set.
- **Fallback C** (boost +0.60): Product name contains plant-milk base term (שקדים,
  שיבולת שועל, etc.) without a solid-food exclusion term (חמאה, גבינה, etc.).

**Outcome:**
- Alpro Almond: `whole_food_fat` → `beverage` ✓
- Alpro Oat: `cereal` → `beverage` ✓
- All 18 other products: category unchanged ✓
- No regression on dairy products — their liquid gate passes via name keywords
  ('1 ליטר' etc.) before fallbacks are evaluated.

---

### Fix 2: SE Gate Beverage Threshold Reduction

**Problem identified in run_002:**
After Fix 1 correctly routes Alpro Almond to `beverage` category, the SE
(Structural Emptiness) gate still fires because kcal=15 < SE_BEVERAGE_KCAL=20.
This triggers calorie_density and fat_quality dimensions being capped at 50.

Plain unsweetened almond milk at 15 kcal is not 'structurally empty' in any
meaningful sense — it's dilute water + almonds. The SE gate was designed to catch
diet sodas and engineered near-zero-calorie beverages, not natural plant milks.

**Fix applied:**
`SE_BEVERAGE_KCAL` reduced from 20.0 → 10.0 kcal/100g.

**Rationale:**
- True diet beverages (cola zero, diet energy drinks) approach 0–5 kcal → still trigger SE
- Plain plant milks (almond 15 kcal, rice 48 kcal) → exempt at the new threshold
- Flavored/sweetened beverages: the SE gate has an additional engineered_signal condition
  (sweetener OR additive_count ≥ 2), so it continues to catch synthetic diet drinks

**Outcome:**
- Alpro Almond: SE=YES → SE=False ✓
- Score: 38.1 E → 43.4 D ✓ (moved into low D as targeted)
- No SE fires on any product in the 20-product corpus

---

## Does Beverage Logic Now Feel Coherent?

**Yes, with one caveat.**

All 16 beverages in the corpus are correctly classified as `beverage`. The dairy
products correctly classify as `dairy_protein`. The gate fallback hierarchy works
without false positives on this corpus.

**The remaining caveat:**
NOVA 4 classification for Alpro Almond is driven by 'חומרי טעם וריח' (generic
flavoring term). This may be natural flavoring — but the ingredient text doesn't
distinguish natural vs artificial. Until BSIP2 has a natural/artificial flavor
taxonomy, plain plant milks with this term will be penalized at NOVA 4.
This is the primary reason Alpro Almond sits at 43.4 (low D) rather than 48–52.

---

## Is a Beverage Modifier Layer Still Needed?

**Not urgently, but architecturally yes.**

The current approach (fixed gate + adjusted SE threshold) resolves the acute
misclassification failures. The beverage scoring itself — using the same dimension
weights as solid foods — produces directionally coherent results but has known
limitations:

1. **Satiety support dimension** doesn't adapt to beverage consumption context
   (you don't drink almond milk for satiety in the same way you eat a snack bar).

2. **Nutrient density** scores very low for all plant milks, which is correct per-100g
   but may not reflect how people actually consume them (as a dairy substitute in
   the full dietary context).

3. **Fat quality dimension** returns neutral 50 for all products with no saturated fat
   declared — this affects several plant milks where sat_fat is null in the data.

A dedicated beverage scoring engine (deferred) would address all three. For now,
the current architecture produces honest, explainable scores.

---

## Remaining Unresolved Weaknesses

| Issue | Severity | Deferred to |
|-------|---------|------------|
| NOVA 4 for generic 'חומרי טעם וריח' (may be natural) | Medium | proto_v1 |
| `kcal_plausible` range (20–700) penalizes low-kcal beverages unfairly | Low | proto_v1 |
| Satiety support formula uses kcal floor=50, which inflates scores for near-zero-cal products | Low | proto_v1 |
| Functional fiber (inulin, chicory) still classified as processed_food_modifier | Medium | proto_v0.2 |
| Beverage-specific dimension weights not yet implemented | Architecture | proto_v1+ |
| Real-food base fraction modifier not implemented | Architecture | proto_v1+ |

---

## Recommendation for Next Category

**Recommended: yogurts & cultured dairy**

Reasons:
- Natural extension of the milk category (same BSIP1 data source, retailer data available)
- Tests BSIP2's fermentation signal handling (תרבויות חיות, תרביות חיות)
- Tests protein quality at higher protein levels (10–18g range)
- Tests the dairy_protein category more deeply (currently only 5 products)
- Probiotic claims are common → tests signal vs marketing narrative
- Flavored yogurts (sugar + NOVA 3/4) would stress-test the guardrail system

**Alternative: spreads & oils (whole_food_fat category)**
- Would validate the WHOLE_FOOD_FAT_FLOOR (65) in a real corpus
- Tahini, olive oil, avocado would test NOVA 1/2 edge cases
- Less risk of new architectural failures
