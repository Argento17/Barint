# Snacks Distortion Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Halo Effect Audit

---

## Overview

A distortion occurs when a product receives a score that is systematically biased by a signal that does not accurately reflect overall product quality. Eleven distortion types are reviewed below for the snacks category.

---

## 1. Date Sugar Halo

**Definition:** Dates are whole-food, therefore date-based products score higher than their actual sugar/calorie profile warrants.

**Affected products:** snk-001, snk-002, snk-015, snk-011, snk-012

**Is Bari handling it correctly?**

No. The date sugar halo is the most active distortion in the snacks corpus. Date bars (snk-001, snk-002, snk-015) occupy the top 3 positions in the category. The scores reflect structural simplicity accurately but fail to account for the extreme sugar density of dates (60–70g sugar per 100g).

snk-001 (70/B) is composed primarily of dates. Dates contain approximately 62g of simple sugars per 100g, mostly fructose and glucose. A bar that is 60%+ dates delivers a sugar load comparable to candy — but receives the highest grade because the sugar source is "whole food."

The system correctly penalizes snk-011 and snk-012 (Pri Mearaz, 43/42 D) for "natural-gap" positioning — these products claim to be natural but have added sugar on top of dates, which correctly triggers a penalty. However, the initial date bars (snk-001, snk-002, snk-015) receive no sugar-density penalty because their sugar is "only" from dates.

**Is Bari over-rewarding?**

Yes. The structural simplicity of date bars (4–5 ingredients, NOVA2) should be rewarded. But the current reward magnitude (70/B, top of the category) is disproportionate when the primary macronutrient is concentrated simple sugar.

**Is Bari under-penalizing?**

Yes. No penalty exists for products where dates constitute the majority of calories and where those calories are almost entirely simple sugars.

**Recommended correction:**

When nutritional data is available, apply a sugar-density awareness signal at >40g/100g total sugar, regardless of whether the sugar source is whole-food. The signal should not eliminate the structural reward — a 4-ingredient date bar is still better than a 15-ingredient protein bar — but it should cap the maximum achievable grade. A product that is 60%+ simple sugars should not exceed B grade without fiber data to support glycemic offsetting.

---

## 2. Natural Sugar Halo

**Definition:** Products using "natural" sweeteners (honey, dates, fruit concentrates) receive implicit bonuses compared to products using equivalent amounts of refined sugar.

**Affected products:** snk-001, snk-002, snk-003, snk-015

**Is Bari handling it correctly?**

Partially. Nature Valley Crunchy (snk-003) is correctly penalized for using glucose syrup as the primary sweetener. But the distinction between glucose syrup and date sugar is not well-articulated in the scoring engine.

Honey in snk-003 is listed as a positive signal ("שיבולת שועל ראשון + ריכוז סיבים"). Honey as a sweetener is nutritionally near-identical to refined sugar at the volumes present in a processed bar. The "natural sweetener" positive signal is a mild halo effect.

**Recommended correction:**

Distinguish between sweetener source and sweetener volume. Natural sweetener source = minor positive signal. Sweetener volume >25g/100g = penalty regardless of source.

---

## 3. Protein Halo

**Definition:** Products positioned as "protein" or containing meaningful protein receive implicit score benefits even when the protein delivery mechanism is heavily processed.

**Affected products:** snk-009, snk-010, snk-017

**Is Bari handling it correctly?**

Partially. The protein bars (snk-009 at 47/D, snk-010 at 45/D) are correctly placed in D territory despite protein positioning. The system does not blindly reward protein content. This is one area where Bari resists the halo.

However, the actual protein content is null in all scores. If snk-009 delivers 15–20g protein per serving, the explanation should acknowledge this as a consumer-relevant fact even while penalizing the processing approach. "You get the protein, but here's what it costs" is stronger than "this product is heavily processed."

**Is Bari under-penalizing?**

No. The protein halo is not driving scores upward. The structural penalty correctly offsets the protein-positioning halo.

**Is Bari over-rewarding?**

No evidence of this.

**Status: HANDLED — but explanation quality needs improvement.**

---

## 4. Fiber Halo

**Definition:** Products claiming or containing oats/fiber receive implicit bonuses for perceived digestive health benefits regardless of overall product quality.

**Affected products:** snk-003, snk-018, snk-005, snk-019

**Is Bari handling it correctly?**

Partially. snk-003 (Nature Valley Crunchy Honey) lists "ריכוז סיבים מכובד" as a positiveSignal. This is appropriate — oats do contain meaningful fiber. However, the scoring system cannot verify the actual fiber content (null), so the "fiber-rich oats" positive signal is an inference, not a measurement.

snk-005 (Fitness Classic) lists "דגנים ברשימת הרכיבים" as its sole positiveSignal. If the grain fraction is small relative to flour and syrup, this positive signal is misleading — grains appearing in the ingredient list does not guarantee meaningful fiber delivery.

**Is Bari over-rewarding?**

Minor over-rewarding for the oat/fiber signal in the absence of verified fiber data.

**Recommended correction:**

Classify the fiber signal as "structural inference" not "verified signal" when actual fiber data is null. Reduce positive signal weight accordingly.

---

## 5. Clean Label Halo

**Definition:** Products with short ingredient lists receive a quality premium that may not reflect nutritional adequacy.

**Affected products:** snk-001 (4 ingredients), snk-002 (minimal), snk-015 (5 ingredients)

**Is Bari handling it correctly?**

No. The clean label halo is actively embedded in Bari's scoring philosophy. Short ingredient count = higher structural quality = higher score. This is a stated design choice, not an accident.

The problem is that "clean label" conflates ingredient-count simplicity with nutritional quality. A 4-ingredient date bar is clean-label but is approximately 65% simple sugars. A 12-ingredient protein bar with protein concentrate, oats, nuts, and multiple stabilizers is "processed" but may deliver better macronutrient balance.

The clean label = structural quality equivalence is the foundational assumption of Bari's scoring. If this assumption is challenged, the entire ranking of the top 5 changes.

**Verdict on the assumption:** The clean label heuristic is defensible as a consumer orientation tool (simpler processing = clearer provenance). It is NOT defensible as a nutritional quality claim. Bari must choose which of these it is and communicate it explicitly.

---

## 6. Nut & Seed Halo

**Definition:** Products containing nuts or seeds receive quality bonuses that may be disproportionate.

**Affected products:** snk-001 (almonds), snk-015 (peanuts), snk-016 (hazelnuts)

**Is Bari handling it correctly?**

Yes, for snk-001 and snk-015 — these are genuine whole-nut compositions. For snk-016, "אגוזי לוז אמיתיים" appears as a positiveSignal with partial confidence. If the hazelnut presence is verified, the signal is appropriate. If hazelnuts are a minor component, it's a halo.

**Status: LOW RISK — but requires ingredient verification for snk-016.**

---

## 7. Fitness / Health Store Halo

**Definition:** Products marketed as "fitness," "wellness," or sold in health-adjacent settings receive implicit quality bonuses.

**Affected products:** snk-004 (Slim Delice — "fitness positioning"), snk-005 (Fitness brand), snk-009/010 (Nature Valley Protein), snk-016 (Slim), snk-019 (Fitness)

**Is Bari handling it correctly?**

Yes. The fitness halo is the primary distortion that Bari was designed to counter. The system actively penalizes fitness-positioned products that have poor structural profiles. snk-005 (46/D) and snk-019 (41/D) are correctly de-haloed — both carry fitness branding while having flour/syrup-first ingredient lists.

The penalization of "marketing divergence" between positioning and composition is one of Bari's clearest strengths.

**Status: HANDLED WELL — this is where Bari adds genuine value.**

---

## 8. No Added Sugar Halo

**Definition:** "ללא סוכר מוסף" claims create the impression that a product is low-sugar, regardless of intrinsic sugar content.

**Affected products:** snk-001, snk-002

**Is Bari handling it correctly?**

Partially. The "ללא ממתיקים מוספים" observation is listed as a positiveSignal for snk-002. The system rewards absence of added sugar without penalizing intrinsic sugar density. In a date-based product, "no added sugar" is almost meaningless — the product is already 60%+ intrinsic sugar.

**Recommended correction:**

Add a qualifier: "ללא סוכר מוסף" is a positive structural signal only when total sugar is below a threshold (e.g., 20g/100g). Above that threshold, the signal should be neutral, not positive.

---

## 9. Premium Product Halo

**Definition:** Premium-priced or premium-marketed products are assumed to have better composition.

**Affected products:** snk-009 (Nature Valley Protein — premium price point), snk-001 (Free brand premium positioning)

**Is Bari handling it correctly?**

Yes. Price and positioning are not input variables in the scoring system. No premium halo risk detected.

---

## 10. Mini Portion Halo

**Definition:** Small-portion products appear healthier because per-bar nutritional totals look modest.

**Affected products:** Not clearly present in current corpus — most bars are single-bar format.

**Status: NOT ACTIVE — serving size standardization (per-100g) prevents this distortion.**

---

## 11. Vegan Halo

**Definition:** Vegan or plant-based products receive quality bonuses for being plant-derived regardless of processing level.

**Affected products:** Date bars (snk-001, snk-002, snk-015) are implicitly plant-based.

**Is Bari handling it correctly?**

The vegan status of products is not an explicit input variable. The clean-label / whole-food positive signals for date bars are driven by ingredient count and NOVA classification, not by plant-based status. The vegan halo risk is low.

**Status: NOT ACTIVE as a direct distortion — overlaps with clean label halo.**

---

## Distortion Summary Table

| Distortion | Status | Risk Level | Products Affected | Action Required |
|---|---|---|---|---|
| Date Sugar Halo | ACTIVE — not handled | HIGH | snk-001, 002, 015 | Add sugar-density awareness to top-end cap |
| Natural Sugar Halo | PARTIALLY ACTIVE | MEDIUM | snk-001, 003 | Distinguish source vs volume |
| Protein Halo | HANDLED | LOW | snk-009, 010 | Improve explanation quality |
| Fiber Halo | PARTIALLY ACTIVE | LOW-MEDIUM | snk-003, 005 | Flag as structural inference when data is null |
| Clean Label Halo | EMBEDDED — by design | HIGH | snk-001, 002, 015 | Requires explicit philosophical disclosure |
| Nut & Seed Halo | LOW RISK | LOW | snk-016 | Verify ingredient presence |
| Fitness/Health Halo | HANDLED | LOW | snk-005, 019 | No action needed |
| No Added Sugar Halo | PARTIALLY ACTIVE | MEDIUM | snk-001, 002 | Threshold-qualify the positive signal |
| Premium Product Halo | NOT ACTIVE | NONE | — | No action needed |
| Mini Portion Halo | NOT ACTIVE | NONE | — | Per-100g prevents this |
| Vegan Halo | NOT ACTIVE | NONE | — | Overlaps with clean label |

**Critical finding:** The Date Sugar Halo and Clean Label Halo are the two most significant distortions in the snacks corpus and are structurally embedded in the scoring philosophy. They cannot be "fixed" with a calibration patch — they require a philosophical clarification about what Bari is actually measuring.
