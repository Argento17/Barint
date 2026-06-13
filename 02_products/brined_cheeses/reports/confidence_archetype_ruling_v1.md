# Confidence Archetype Ruling v1 — fiber-null is not a data gap for dairy

**Author:** Nutrition Agent (C1), 2026-06-13 · TASK-266 follow-up · orchestrator-verified.
**Trigger:** Stage 9 red-team RT-H1 — 30/48 brined cheeses falsely flagged `confidence:"partial"` because `fiber=null`, while having complete ingredients + all other macros (incl. the 89/A shelf leader).

## Ruling
A confidence assessment measures whether the data needed for a reliable score is present. A field
that is **structurally absent for a food archetype** is an **expected null**, not a data gap.
Counting expected-nulls as "required" produces false-partials that misrepresent data quality.

**Fiber** is indigestible plant cell-wall material → **structurally ~zero in animal-source products**
(dairy, meat, fish, eggs, pure fats). `dietary_fiber_g = null` for cheese/yogurt/butter is EXPECTED
ABSENCE. The scoring engine already encodes this (EV-027, fiber-not-applicable for fiber-free dairy);
the confidence logic must recognize the same archetype structure.

## Archetype → expected-null (confidence-required = FALSE)
| Archetype | Expected-null fields | Why |
|---|---|---|
| `dairy_protein` (cheese, yogurt) | `dietary_fiber_g` | no plant cell wall |
| `whole_food_fat` (butter, oils) | `dietary_fiber_g`, `sugars_g` | fat product |
| `meat_fish` | `dietary_fiber_g`, `sugars_g` | animal tissue |
| `beverage_juice` | `fat_g`, `fat_saturated_g` | near-zero fat by structure |

**Always-required (every archetype):** `energy_kcal`, `protein_g`, `sodium_mg`.
**Conditional:** `sugars_g` required for dairy/cereal/snack/beverage/bread; `fat_g`/`fat_saturated_g`
required except pure beverages; `dietary_fiber_g` required for plant archetypes only.

## Semantics
- **verified/full** = ingredients present AND all *archetype-required* nutrition fields non-null.
- **partial** = an archetype-required field is null, OR ingredients missing. Sub-reasons unchanged
  (`missing_ingredients` / `missing_nutrition` / `partial_field`).

## Honesty guard (orchestrator-verified on brined shelf)
Fix NARROWS false-partials only. Verified before/after: 30 `partial_field` have fiber as the SOLE
null (0 exceptions) → become verified; the 3 `missing_nutrition` genuinely lack **sugar** (required) →
STAY partial; 12 `missing_ingredients` STAY partial. Result: verified 3→33, partial 45→15.

## Two fix scopes
1. **THIS page (brined, hand-built):** the brined `frontend_v2.json` was NOT produced by
   `generate_page.py` (it emits `sub_reason:"low_extraction"`, not `"partial_field"`) — it was
   hand-rendered (P50). So a generator change does NOT fix this page; the 30 confidence fields are
   corrected **directly in the artifact** per this ruling (verified="מבוסס על נתונים מלאים", sub=null).
2. **SYSTEMATIC (deferred → TASK below):** `generate_page.py` `build_confidence_fields()`
   (lines ~234-237: `core_nutrition_fields` hardcodes `dietary_fiber_g`). Make it archetype-aware
   via an `ARCHETYPE_EXPECTED_NULL` map + per-category `"archetype"` config. **MANDATORY** cross-corpus
   confidence diff vs committed baseline before ship (return-contract rule 8); only false-partials
   move partial→verified; generic-archetype categories (cereals/granola/bread/snacks/hummus/
   veg-spreads/salty-snacks) must show ZERO change. Salty-snacks fiber-null is a REAL gap (plant
   snacks have fiber) — must NOT move.

Related: EV-027, `.claude/scoring.md`, `generate_page.py`.
