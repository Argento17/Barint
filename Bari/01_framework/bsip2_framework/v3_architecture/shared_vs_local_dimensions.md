# BSIP2 Shared vs Local Dimensions

**Status:** Design specification
**Date:** 2026-05-18

---

## Overview

BSIP2 v3 maintains 10 scored dimensions. They are divided into three tiers:

| Tier | Definition | Count |
|---|---|---|
| **Universal** | Same formula, same weights, same interpretation across all archetypes | 5 |
| **Universal with archetype-calibrated parameters** | Same formula, same weight, but one or more parameters differ by archetype | 3 |
| **Archetype-local** | Exists only within specific archetype contexts; absent or neutral elsewhere | 2+ |

---

## Tier 1 — Universal Dimensions

These five dimensions are scored identically for every product regardless of archetype. Their formulas, breakpoints, and weights do not change.

### processing_quality (weight: 0.15)

**Formula:** `NOVA_PROCESSING_SCORES[nova_level]`
**Values:** NOVA1=95, NOVA2=85, NOVA3=65, NOVA4=35

Processing burden from industrial formulation is universal. A NOVA4 product is ultra-processed regardless of whether it is a breakfast cereal, a dairy drink, or a sauce. The score meaning is identical across all archetypes.

**No archetype-specific variation.**

### additive_quality (weight: 0.10 → proposed 0.09 in v3)

**Formula:** `max(0, 100 - additive_marker_count * 18) - sweetener_penalty(15)`

Additive burden is universal. The marker patterns (emulsifier, stabilizer, color, flavor_enhancer, preservative) have the same interpretation everywhere — they represent industrial ingredient systems added to the product structure. The 18-point penalty per additive category is consistent across food types.

Note: In v3, fortification cluster detection (Evolution #4) adds a soft additive signal for Hebrew-named vitamins. This signal feeds into additive_quality universally — it is not cereal-specific.

**No archetype-specific variation in scoring formula.** The signal inputs (additive_marker_count) may differ because local signals contribute to the count, but the scoring function itself is universal.

### fat_quality (weight: 0.08)

**Formula:** `max(0, 100 - sat_fat * 3.0 - sat_frac * 25) - seed_oil_penalty - trans_penalty`

Saturated fat ratio and trans fat presence have the same physiological meaning regardless of product type. Fat quality concerns are universal.

**Exception note:** The structural emptiness gate (`fat < 0.5g → neutral 50`) is universal but calibrated to avoid penalizing beverages for having no fat. This is not archetype-specific — it is a data validity gate.

**No archetype-specific variation.**

### regulatory_quality (weight: 0.05 → proposed 0.04 in v3)

**Formula:** `95 if 0 labels, 60 if 1 label, 25 if 2+ labels`

Israeli red labels (sugar ≥ 17.5g, sat_fat ≥ 5.0g, sodium ≥ 600mg) are regulatory thresholds applied identically to all solid food products in Israel. The meaning of a red label does not change based on product category — it is a national regulatory signal.

**No archetype-specific variation.** The thresholds themselves are legally defined.

### confidence (not a scored dimension, but universal)

The confidence system (`compute_confidence()`) evaluates data quality: missing fields, BSIP1 trust level, NOVA confidence, category confidence, and data consistency checks. These quality signals are universal — a missing fiber value is equally problematic for a cereal as for a sauce.

**No archetype-specific variation.**

---

## Tier 2 — Universal Dimensions with Archetype-Calibrated Parameters

These three dimensions use the same formula and the same weight, but at least one parameter varies by archetype.

### calorie_density (weight: 0.15)

**Formula:** `lookup_calorie_density(kcal, archetype)` → lookup against archetype-specific table

The formula is universal: find the calorie density band for this product's energy content. What changes is the table — the band boundaries are calibrated to what is "normal" for this food type.

**Archetype-specific parameter: the lookup table.**

Current tables in `constants.py:CALORIE_DENSITY_TABLES`:

| Archetype | Table calibration | Rationale |
|---|---|---|
| `cereal` | 300 kcal→85, 430 kcal→55, 550 kcal→25 | Cereals are moderate density; above 430 is a concern |
| `snack_bar_granola` | 250 kcal→75, 350 kcal→55, 430 kcal→40 | Granola/snack bars run dense; calibrated harsher |
| `whole_food_fat` | 350 kcal→90, 650 kcal→75, 900 kcal→55 | Oils/nuts are inherently calorie-dense; table is generous |
| `beverage` | 10 kcal→95, 45 kcal→70, 100 kcal→30 | Beverages should be near-zero calorie for high scores |
| `dairy_protein` | 80 kcal→90, 180 kcal→70, 350 kcal→40 | Dairy protein at high kcal is unusual; moderate table |

**This table IS the archetype's calorie density stance.** It is the most impactful single archetype-specific parameter.

### nutrient_density (weight: 0.15)

**Formula:** `0.65 * prot_score(protein_g) + 0.35 * fiber_score(fiber_g)` with shared breakpoint tables

The formula is universal. The breakpoint tables are currently shared. In v3, archetypes may override the 65/35 split or the breakpoints to reflect what "density" means for that food type.

**Proposed archetype-specific variation:**

| Archetype | Proposed adjustment | Rationale |
|---|---|---|
| `oil_system` | protein weight → 0.10, fiber weight → 0.10, remainder neutral | Oils provide neither protein nor fiber — penalizing oils for this is wrong |
| `cereal_system` | No change from shared (65/35 correct for cereal context) | Protein and fiber are both meaningful cereal quality signals |
| `dairy_liquid` | protein weight → 0.80, fiber weight → 0.20 | Dairy protein context: protein is the primary density signal |

**Implementation note:** These overrides are NOT yet deployed. The current 65/35 is used universally. The override mechanism should be built into the archetype interface but populate with `None` (use shared) until calibrated against data.

### glycemic_quality (weight: 0.12)

**Formula:** `90 - min(80, sugar*2.5) + fiber_laundering_cap(fiber, sugar) + wg_bonus`

The formula is universal. One parameter differs by archetype: the **fiber laundering cap behavior** proposed in Evolution #3 is universal but its threshold (12g sugar trigger) may need archetype-specific calibration.

**In a dessert archetype:** 12g sugar would be low; the laundering cap trigger should be higher.
**In a cereal archetype:** 12g sugar is elevated; current 12g threshold is correct.
**In a beverage archetype:** sugar content is the dominant signal; fiber is typically 0; the laundering cap has no effect.

**This is the most subtle Tier 2 variation.** The formula is the same; the meaning of "elevated sugar" differs by food type.

---

## Tier 3 — Archetype-Local Dimensions

These signals exist for specific archetypes only. For archetypes where they are irrelevant, they return a neutral value (50) or are excluded from scoring with a weight of 0.

### matrix_integrity (replacing whole_food_integrity, weight: 0.04 → proposed 0.07 in v3)

**Current implementation:** `score_whole_food_integrity(nova_level, ing_count)` — NOVA base + complexity penalty.

**v3 implementation:** Expands to include matrix disruption signals. Signals: `קמח` (flour, -20), `עמילן` (starch, -30), `נפוח` (puffed, -20), `פתיתים מיידיים` (instant flakes, -10).

**Archetype relevance:**

| Archetype | matrix_integrity relevance | Behavior |
|---|---|---|
| `cereal_system` | HIGH — central to the extruded vs intact grain distinction | Full matrix disruption signals apply |
| `snack_bar_granola` | MEDIUM — some snack bars use extruded or puffed bases | Disruption signals apply at reduced weight |
| `whole_food_fat` | LOW — nuts and seeds have inherent matrix integrity | Disruption signals apply only to reconstituted nut products (nut butters with starch additives) |
| `dairy_liquid` | MINIMAL — liquid products; matrix concept is less applicable | Returns NOVA-based WFI only; disruption signals not applicable |
| `beverage` | NONE — return neutral 50 | No matrix interpretation for liquids |

**Scoring behavior for irrelevant archetypes:** The dimension returns the NOVA-based base score (same as current `score_whole_food_integrity` behavior, without disruption penalties). The disruption penalty only activates for archetypes that declare it.

### satiety_support (weight: 0.06 → proposed 0.05 in v3)

**Formula:** `(protein*3 + fiber*5) / max(50, kcal) * 400`, capped at 100

This dimension is nominally universal but is effectively disabled for whole_food_fat via the `satiety_rules_gated` flag (the cooking-oil exemption). The exemption is currently inline in `evaluate_guardrails()`. In v3, it is declared in the `whole_food_fat` archetype's guardrail module.

For other archetypes, satiety_support is computed identically. The formula is universal; the exemption is archetype-declared.

---

## Future Archetype-Local Dimensions (Not Yet Implemented)

These are proposed for future archetypes. They do not exist in the current codebase.

### fermentation_quality

**Target archetypes:** yogurt_system, kefir, kombucha, cultured dairy
**Signal inputs:** `has_fermentation` (already computed in `nova_proxy.py` as evidence_against for NOVA4); count of live culture claims; heat treatment markers
**Formula sketch:** `base = 60; base + 20 if live_cultures_claimed; base + 10 if specific_strain_named; base - 20 if heat_treated`
**Rationale:** Fermentation is a genuine food structural quality for probiotic products. A yogurt with heat-treated bacteria is fundamentally different from one with live cultures. This distinction is not captured by NOVA or additive burden.

### roasting_quality

**Target archetypes:** whole_food_fat (nuts), oil_system, coffee
**Signal inputs:** roasting level claims, cold-press markers, processing temperature signals
**Formula sketch:** Light roast and cold-press preserve more bioactive compounds; heavy roasting and solvent extraction are degradation signals
**Rationale:** The current framework cannot distinguish raw almonds from heavily roasted almonds or extra virgin olive oil from refined oil. For whole-food-fat archetypes, the processing method is more informative than NOVA level alone.

### fat_complexity (oil_system)

**Target archetypes:** oil_system
**Signal inputs:** fatty acid profile (if available), polyphenol claims, smoke point markers
**Formula sketch:** Favors high oleic acid content, polyphenol-rich oils; penalizes refined and partially hydrogenated products
**Rationale:** The fat_quality dimension measures saturated fat ratio, which is insufficient for evaluating oils where the relevant distinction is between refined and unrefined, and between oleic-rich and polyunsaturated-dominant profiles.

### fortification_signal

**Target archetypes:** cereal_system, dairy_liquid, supplement_system
**Signal inputs:** `fortification_cluster_detected`, `fortification_count` (from Evolution #4)
**Behavior:** Acts as an input to additive_quality and nova_proxy, not a standalone dimension
**Rationale:** Fortification is not a standalone quality dimension — it is a signal that modifies other dimensions. It belongs in the archetype's guardrail module or as a modifier to processing_quality, not as an independent scored dimension.

---

## Dimension Weight Profiles by Archetype

Current shared weights (all archetypes):

```
processing_quality:   0.15
nutrient_density:     0.15
calorie_density:      0.15
glycemic_quality:     0.12
protein_quality:      0.10
additive_quality:     0.10 → 0.09 proposed
satiety_support:      0.06 → 0.05 proposed
fat_quality:          0.08
regulatory_quality:   0.05 → 0.04 proposed
matrix_integrity:     0.04 → 0.07 proposed (replaces whole_food_integrity)
```

Proposed archetype weight overrides (speculative — requires data validation):

| Dimension | cereal_system | dairy_liquid | whole_food_fat | oil_system |
|---|---|---|---|---|
| processing_quality | 0.15 | 0.15 | 0.15 | 0.12 |
| nutrient_density | 0.15 | 0.10 | 0.10 | 0.05 |
| calorie_density | 0.15 | 0.15 | 0.10 | 0.15 |
| glycemic_quality | 0.12 | 0.10 | 0.05 | 0.02 |
| protein_quality | 0.10 | 0.20 | 0.05 | 0.03 |
| additive_quality | 0.09 | 0.09 | 0.09 | 0.10 |
| satiety_support | 0.05 | 0.05 | 0.02 | 0.02 |
| fat_quality | 0.08 | 0.08 | 0.30 | 0.40 |
| regulatory_quality | 0.04 | 0.04 | 0.04 | 0.04 |
| matrix_integrity | 0.07 | 0.04 | 0.10 | 0.07 |
| **Sum** | **1.00** | **1.00** | **1.00** | **1.00** |

**These overrides are hypotheses, not calibrated values.** The oil_system and dairy_liquid profiles in particular require empirical validation against a corpus before deployment. The cereal_system profile is closest to the shared weights and should be the first to validate.

**Rule:** Archetype weight overrides should only be deployed after a minimum of 20 products in that archetype have been scored and the hierarchy has been validated by human review. Deploying hypothetical weights without validation is worse than using the shared profile.
