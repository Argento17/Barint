# BSIP2 Archetype Philosophy

**Status:** Design specification
**Date:** 2026-05-18

---

## What an Archetype Is

An archetype is an **interpretation context**, not a separate scoring algorithm.

When a BSIP1 canonical product enters BSIP2, the scoring mathematics are identical regardless of what that product is. The 10 dimensions are scored. The concern families are evaluated. The confidence is computed. The waterfall trace is built.

What changes between a cereal and a cooking oil is not the mathematics — it is the **meaning** of the numbers. 450 kcal/100g in a cooking oil is unremarkable. 450 kcal/100g in a breakfast cereal is an important structural signal that warrants a specific guardrail. 3g of dietary fiber in an oat product is mediocre. 3g of dietary fiber in a milk product is irrelevant to the category's purpose.

An archetype provides the context that makes the mathematics meaningful.

---

## What an Archetype Contains

Every archetype must define exactly five things:

### 1. Calorie Density Table

A lookup table that maps kcal/100g ranges to calorie density scores (0-100). This table is **calibrated to the natural energy density range of products in that archetype**. Current tables live in `constants.py:CALORIE_DENSITY_TABLES`.

Example contrast:
- `cereal`: 300 kcal → 85 score (cereals at that density are acceptable)
- `snack_bar_granola`: 350 kcal → 55 score (dense for a snack bar)
- `whole_food_fat`: 350 kcal → 90 score (low density for a nut or oil product)

The same 350 kcal produces three different scores because the reference frame is different. This is correct. The archetype is the reference frame.

### 2. Guardrail Module

A set of archetype-specific guardrail activations: which caps fire, at what thresholds, and under what conditions. Some guardrails are universal (NOVA4 cap at 68, ISRAELI_RED_LABELS_2_PLUS cap at 45, TRANS_FAT_VETO). Others are archetype-specific.

Current archetype-specific guardrails embedded in `score_engine.py`:
- `category == "cereal" and sugar >= 20 and fiber <= 3` → HP_CRUNCH_SWEET (cereal only)
- `category == "snack_bar_granola" and kcal >= 430` → SNACK_BAR_HIGH_CAL cap at 70
- `category == "whole_food_fat" and (kcal > 500 or fat > 50)` → satiety_rules_gated = True (exemption)
- `category == "beverage"` → structural emptiness uses SE_BEVERAGE_KCAL threshold

These conditions are currently inline. In v3 they live in each archetype's guardrail module.

### 3. Floor Definitions

Which floors protect products in this archetype, and under what conditions. Current floors in `score_engine.py:apply_floors()`:
- `NOVA1_SINGLE_FLOOR = 85`: protects single-ingredient whole-food products
- `WHOLE_FOOD_FAT_FLOOR = 70`: protects NOVA 1-2 products in the whole_food_fat archetype

In v3, each archetype explicitly declares whether it participates in the NOVA1 floor, the whole-food floor, or defines its own minimum-score guarantee.

### 4. Local Signals

Signals that are meaningful only within this archetype's interpretation context. These are computed by the shared signal extractor but only interpreted by the archetype that declares them.

| Archetype | Local signals |
|---|---|
| cereal_system | matrix_integrity, extrusion_markers, fortification_cluster, instant_processing |
| dairy_liquid | fermentation_markers (for kefir/cultured), protein_concentration |
| snack_bar | coating_markers, compression_signals |
| whole_food_fat | roasting_markers, cold_press_markers |
| yogurt_system | fermentation_quality, live_cultures, heat_treatment |
| oil_system | fat_complexity, polyphenol_markers |

A local signal computed but not declared by an archetype has no effect on scoring. It may appear in the trace for informational purposes.

### 5. Dimension Weight Profile (Optional)

By default, all archetypes use the shared `DIMENSION_WEIGHTS` from `core/constants/`. An archetype may override individual dimension weights when the shared calibration is genuinely wrong for that food type.

Example: In an oil_system archetype, `nutrient_density` (protein + fiber) is nearly irrelevant — oils don't provide protein or fiber in meaningful amounts. The shared weight of 0.15 for nutrient_density overrepresents its importance for oils. An oil archetype might reduce this to 0.05 and redistribute weight to `fat_quality` and `calorie_density`.

Weight overrides require explicit documentation of the rationale. They are not calibration tricks — they are structural decisions about what "quality" means for a specific food type.

---

## What an Archetype Is NOT

**Not a separate scorer.** There is no `CerealScorer`, `DairyScorer`, `NutScorer`. There is one scorer with different parameters.

**Not a fork.** No archetype contains copies of dimension scoring functions. The scoring math is in `core/scoring_engine/`. Archetypes inject parameters; they do not re-implement mathematics.

**Not an exhaustive classification.** An archetype does not need to cover every possible product in its category. It covers the products for which its calorie density table, guardrail module, and floor definitions produce valid, interpretable results. Products that don't fit are routed to the nearest archetype with a confidence penalty or to the `default` archetype with explicit uncertainty.

**Not a fixed taxonomy.** Archetypes can be split, merged, or deprecated as data accumulates. The cereal_system archetype might later be split into `extruded_grain` and `intact_grain` if the evidence supports distinct interpretation contexts. The architecture supports this without breaking existing products.

---

## Shared vs Archetype-Specific: The Core Tension

The most important architectural decision for any new dimension or rule is:

> Does this rule reflect something universal about food quality, or does it only make sense in the context of a specific product type?

**Universal rules** (shared across all archetypes):
- NOVA proxy classification and its processing quality penalty
- Additive burden (count and type)
- Israeli red-label thresholds (these are regulatory, not food-type dependent)
- Fat quality (saturated fat ratio, trans fat veto)
- Confidence computation (data quality is not category-specific)

**Archetype-specific rules** (only meaningful in context):
- Calorie density tables (what is "normal" density for this food type)
- Matrix integrity penalties (relevant for cereals, processed grains, extruded products; not for oils)
- Fermentation quality (relevant for yogurt, kefir, kombucha; not for cereals)
- Satiety_rules_gated exemption (only for pure fat products where protein and fiber are structurally absent)
- HP_CRUNCH_SWEET pattern (only for cereal-type products where sugar-dense-puffed products are a specific concern)

When a rule is added to BSIP2, its home (universal or archetype-specific) must be declared before implementation. This is a design question, not an implementation question.

---

## Currently Live Archetypes

As of run_cereals_001:

| Archetype name | Category constant | Status | Validation runs |
|---|---|---|---|
| cereal_system | `"cereal"` | Active, routing unstable | run_cereals_001 |
| dairy_liquid | `"dairy_protein"` + `"beverage"` | Active | run_004_recalibrated |
| snack_bar | `"snack_bar_granola"` | Active, routing unstable | run_004_recalibrated, cereals |
| whole_food_fat | `"whole_food_fat"` | Active | run_004_recalibrated, cereals |
| beverage | `"beverage"` | Active | run_004_recalibrated |
| sauce_spread | `"sauce_spread"` | Defined, untested | None |

The `dairy_liquid` and `beverage` archetypes are currently modeled as two separate categories but share many structural properties. They may be unified in v3 under a `liquid_system` archetype with subtypes, or kept separate if their guardrail profiles diverge sufficiently.

---

## Subtype Architecture Within Archetypes

An archetype can define **subtypes** — finer-grained interpretations within the same calorie density and guardrail framework. Subtypes do not change scoring math. They:

1. Affect routing confidence and trace labeling
2. May activate or suppress specific guardrail rules within the archetype
3. Enable subtype-level analysis in reports and leaderboards

Example — `cereal_system` subtypes:
- `granola` — triggers granola-specific calorie density context, escapes from HP_CRUNCH (different product structure)
- `oatmeal` — expects high protein and fiber; whole grain signals standard
- `extruded_cereal` — expects matrix_integrity disruption; NOVA 1 floor gated
- `kids_cereal` — high-sugar expected; HP_CRUNCH fires at NOVA4 weight
- `protein_cereal` — protein_quality dimension receives higher interpretive weight
- `muesli` — similar to oatmeal but calorie density higher; nuts/seeds normal

The `cereal_system` archetype handles all of these with one guardrail module and one calorie density table. Subtypes inject subtype-specific flags that modulate which rules activate within that module.

This pattern (archetype + subtypes) avoids the combinatorial explosion of a separate archetype per subtype, while maintaining the granularity needed to produce coherent scores.
