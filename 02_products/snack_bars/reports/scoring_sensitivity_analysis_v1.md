# Scoring Sensitivity Analysis v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Which Mechanisms Drive Outcomes?

---

## Overview

This document identifies which scoring mechanisms most strongly influence final scores and estimates the effect of changing the cap architecture or adding category-specific parameters.

---

## Part 1: Primary Score Drivers (Ranked by Impact)

### Driver 1: NOVA Classification (Highest Impact)

NOVA classification is the single most powerful factor in the snacks scoring engine.

| NOVA | Full corpus N | Mean score | Gap to next tier |
|---|---|---|---|
| NOVA 2 | 7 | 54.5 | +7.1 above NOVA3 |
| NOVA 3 | 15 | 47.4 | +19.0 above NOVA4 |
| NOVA 4 | 31 | 28.4 | — |

The 19-point gap between NOVA3 (47.4) and NOVA4 (28.4) is the largest discriminating signal in the corpus. The 7-point gap between NOVA2 and NOVA3 is secondary.

**Why NOVA dominates:**
The NOVA classification propagates across FOUR dimensions simultaneously:
- `processing_quality`: -24 for NOVA4 (vs -12 for NOVA3 vs 0 for NOVA2)
- `whole_food_integrity`: -14 for NOVA4 (vs -7 for NOVA3)
- Guardrail: NOVA4 cap at 60 (safety net; not currently binding for any product)
- Concern coordination: NOVA4 is used as a supporting signal for PROCESSING_LOAD concern

Combined effect: Changing a product from NOVA4 to NOVA3 adds approximately +12 points to `processing_quality` and +7 to `whole_food_integrity`, translating to roughly +12×0.18 + 7×0.01 = +2.2 + 0.07 = **~2.3 weighted points from these dimensions alone.** But real-world NOVA3 products also have fewer ingredient count penalties, fewer glucose syrup flags, and fewer additive markers — so the actual score lift from a NOVA3 reclassification is 8–15 points in practice.

**This is by design.** NOVA is the most evidence-backed categorical predictor of processed food health impact. Using it as the primary driver is scientifically defensible.

### Driver 2: Sugar Load (High Impact for high-sugar products)

For products with sugar ≥25g/100g, the sugar penalty propagates across THREE dimensions:
- `glycemic_quality`: -(sugar-5)×1.4 penalty (at 28g sugar: -32 points penalty on base 80)
- `nutrient_density`: -(sugar-5)×0.9 penalty
- `satiety_support`: -(sugar-15)×0.5 penalty (only above 15g threshold)

A product moving from 20g sugar to 30g sugar (a 10g increase) loses:
- glycemic_quality: -14 points × weight 0.11 = -1.54
- nutrient_density: -9 points × weight 0.16 = -1.44
- satiety_support: -2.5 points × weight 0.06 = -0.15
- **Total: ~3.1 weighted points** from sugar alone

Additionally, the HIGH_SUGAR_25G_PLUS guardrail cap at 60 becomes binding if the product would naturally score above 60 — which happens for clean-label products with above-threshold sugar (date bars: ~28g natural sugar, but they route to whole_food_fat category which has different handling).

### Driver 3: Calorie Density (Significant for snack bars)

The calorie density tiers are category-specific and have a large impact for snack bars:

| Score tier | snack_bar_granola | dairy_protein | whole_food_fat |
|---|---|---|---|
| ~350 kcal | 55 | — | 75 |
| ~430 kcal | 40 | — | 65 |
| ~480 kcal | 25 | — | 55 |

A snack bar at 430 kcal receives a calorie_density_quality score of 40 (weight 0.12) = **4.8 weighted points.**
The same product if misrouted to whole_food_fat would receive a score of 65 = **7.8 weighted points** — a 3.0 weighted point difference from routing alone.

This explains why products routing as `whole_food_fat` score higher than equivalent products routing as `snack_bar_granola`. Several products in the corpus were routed as `whole_food_fat` (date bars, nut bars) when their names contain "almond butter," "hazelnuts," or similar whole-food fat keywords. This routing is directionally correct but creates a calorie-density bonus for calorically dense bars.

### Driver 4: Additive Load (Medium Impact)

Each additive marker penalty: -12 points to `additive_quality` (base 90, weight 0.07).

- 0 markers: additive_quality = 90 → 6.3 weighted points
- 3 markers: additive_quality = 54 → 3.78 weighted points
- 5 markers: additive_quality = 30 → 2.1 weighted points

Net impact of going from 0 to 5 additive markers: **-4.2 weighted points** from this dimension alone. Plus the additional ADDITIVE_MARKERS_5_PLUS cap at 55, ADDITIVE_MARKERS_3_PLUS cap at 65.

### Driver 5: Protein Content (Moderate Impact)

The protein signal appears in THREE dimensions:
- `nutrient_density`: min(protein×1.2, 20)
- `protein_quality`: base 45 + min(protein×2.0, 35)
- `satiety_support`: min(protein×1.4, 25)

Going from 4g protein to 10g protein:
- nutrient_density: +7.2 points × 0.16 = +1.15
- protein_quality: +12 points × 0.09 = +1.08
- satiety_support: +8.4 points × 0.06 = +0.50
- **Total: ~2.73 weighted points** from protein

This is significant. The Nature Valley Protein bars scoring higher (47–48) than the Fitness Classic (46) reflects in part their higher protein content, even though both are NOVA4.

### Driver 6: Processing-Specific Signals (Medium Impact)

Beyond NOVA, specific processing markers apply additional penalties to `processing_quality`:
- Glucose syrup present: -8 points
- Flavouring present: -6 points  
- Emulsifier present: -6 points
- Chocolate coating: -8 points
- Extruded/puffed grain: -8 points

These stack independently. A product with all five (common in ultra-processed cereal bars) loses 36 additional points from processing_quality beyond the NOVA4 base penalty. This is what drives products like Corny (13) vs Fitness Classic (46) apart — both are NOVA4, but Corny has all five processing markers while Fitness Classic has fewer.

---

## Part 2: Cap Sensitivity Analysis

### Current cap binding status (snacks corpus)

| Cap | Value | Trigger | Binding products | Effect on mean |
|---|---|---|---|---|
| NOVA4 processing cap | 60 | nova_proxy==4 | **0 of 31** (max=47.4) | **0 points** |
| NOVA3 processing cap | 75 | nova_proxy==3 | **0 of 15** (max=62.2) | **0 points** |
| 2+ red labels | 45 | regulatory | Some products | Variable |
| HIGH_SUGAR_25G_PLUS | 60 | sugar≥25g | Some products (not binding if score already <60) | Small |
| ADDITIVE_5_PLUS | 55 | additives≥5 | Unknown (need per-product audit) | Small |

**Key insight: Changing the NOVA4 cap from 60 to 50, 40, or 75 would have ZERO effect on current snacks rankings.** No NOVA4 product currently scores above 47.4. The cap is not in the active region.

### Simulated effect of cap changes

**Scenario A: Raise NOVA4 cap from 60 → 75**
Expected effect on rankings: Zero. No product currently constrained by the 60 cap.
Expected effect on mean: Zero.

**Scenario B: Lower NOVA4 cap from 60 → 40**
Expected effect: 7 NOVA4 products (those scoring 40–47.4) would be capped at 40. Others already below 40.
New mean for NOVA4 tier: ~26 (vs current ~28.4)
Effect on full corpus mean: ~-1.4 points
Effect on displayed mean: small reduction (only a few displayed products are NOVA4 above 40)

**Scenario C: Add category-specific snacks NOVA4 cap at 50**
Products affected: 7 NOVA4 products currently scoring 40–47.4
New max NOVA4 score: 50 (currently 47.4, so effectively no change)
Effect: Near-zero.

**Scenario D: Introduce category-specific grade boundaries for snacks**
Current C threshold: 55 → Proposed snacks C threshold: 48
Under new threshold: Products currently graded D at 48–54 would grade up to C
Affected displayed products: snk-009 (47/D → still D at 47), snk-005 (46/D → still D at 46)
Actually, this would move most products at 48–54 from D to C. Looking at the displayed corpus:
- snk-003 (53), snk-016 (51), snk-009 (47), snk-005 (46), snk-018 (46) — under 48 threshold, snk-003 and snk-016 move from C to C (already C), snk-009 stays D (47<48).
- Actually at threshold 48: snk-003 (53→C), snk-016 (51→C), snk-018 (46→D), snk-009 (47→D)... wait, 48 as C threshold means 48+ = C. So snk-009 at 47 stays D, and 46-47 range stays D.

**The most meaningful grade boundary change: lowering C threshold from 55 to 48 would move 4–5 products from D to C.** This changes the displayed grade distribution visibly without changing any underlying score.

---

## Part 3: What Would Materially Change Rankings?

The only changes that would materially change rankings (not just grades) are changes to the dimension weights or the NOVA penalty values.

### Sensitivity to NOVA4 penalty change

Current: `nova_4_penalty: 24` in processing_quality, `nova_4_penalty: 14` in whole_food_integrity.

If NOVA4 penalty were halved (12 instead of 24 for processing, 7 for WFI):
- Processing_quality for NOVA4 bars would rise by ~12 points
- WFI would rise by ~7 points
- Combined weighted effect: +12×0.18 + 7×0.01 = +2.2 points
- Real-world effect (including downstream cascading): +5–8 points for most NOVA4 products
- New NOVA4 mean: ~28.4 + 7 = ~35

This would bring NOVA4 products up into the 30–50 range from the 15–47 range, and change several E-grade products to D. It would NOT collapse the NOVA2/NOVA3/NOVA4 stratification — the 15-point gap between NOVA3 and NOVA4 would become an 8-point gap, which is still meaningful.

### Sensitivity to additive penalty change

Current: `per_marker_penalty: 12` per additive marker.

If reduced to 8:
- 5-marker products: additive_quality goes from 30 to 50 (+20 points)
- Weighted: +20×0.07 = +1.4 weighted points
- Small effect. Does not change relative rankings meaningfully.

### Sensitivity to calorie density routing

Rerouting all snack bars from `snack_bar_granola` to `whole_food_fat` (the lenient tier):
- Calorie_density_quality at 430 kcal: 40 → 65 (+25 points)
- Weighted: +25×0.12 = +3.0 weighted points per product
- This would be a moderate uplift for all bars — but wrong, since snack bars are not whole-food fat products.

---

## Summary: What Drives Snack Bar Scores

| Mechanism | Effect size | Controllable via caps? | Currently binding? |
|---|---|---|---|
| NOVA classification | 8–19 points per tier | No (caps redundant) | N/A |
| Sugar load (>25g) | 3–5 points | Minor (cap at 60) | Rarely |
| Calorie density routing | 3–5 points | No | N/A |
| Additive load (5+ markers) | 3–4 points | Minor (cap at 55) | Rarely |
| Protein content | 2–3 points | No | N/A |
| Processing markers (syrup/coating/etc.) | 1–3 points per marker | No | N/A |

**Conclusion:** NOVA classification is the dominant driver. Cap architecture changes would have minimal effect on current rankings. The most impactful structural change would be modifying the NOVA4 penalty values or adding category-specific grade thresholds.
