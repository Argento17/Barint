# BSIP2 v3 Proposed Folder Structure

**Status:** Proposed — not yet implemented
**Current code lives in:** `C:\Bari\03_operations\bsip2\proto_v0\src\`
**Target location:** `C:\Bari\03_operations\bsip2\v3\`

For each proposed file, the current source file is noted where applicable.

---

## Full Proposed Structure

```
bsip2/
│
├── core/
│   │
│   ├── constants/
│   │   ├── grade_thresholds.py          ← constants.py: GRADE_THRESHOLDS, score_to_grade()
│   │   ├── nova_tables.py               ← constants.py: NOVA_PROCESSING_SCORES, NOVA_WFI_SCORES, NOVA_HP_WEIGHTS
│   │   ├── red_label_thresholds.py      ← constants.py: RED_LABEL_THRESHOLDS
│   │   └── penalty_budgets.py           ← constants.py: *_FAMILY_BUDGET constants
│   │
│   ├── scoring_engine/
│   │   ├── dimensions.py                ← score_engine.py: all score_*() functions
│   │   ├── guardrails.py                ← score_engine.py: evaluate_guardrails(), _coordinate_family()
│   │   ├── floors.py                    ← score_engine.py: apply_floors()
│   │   ├── confidence.py                ← score_engine.py: compute_confidence()
│   │   └── structural_emptiness.py      ← score_engine.py: detect_structural_emptiness()
│   │
│   ├── orchestration/
│   │   ├── pipeline.py                  ← batch_run.py: run_pipeline() logic
│   │   ├── input_loader.py              ← input_loader.py (no change, relocate)
│   │   └── evaluation_scope.py          ← evaluation_scope.py (no change, relocate)
│   │
│   ├── signal_interpretation/
│   │   └── nova_proxy.py                ← nova_proxy.py (no change, relocate)
│   │
│   ├── waterfall/
│   │   ├── trace_writer.py              ← trace_writer.py (no change, relocate)
│   │   └── trace_schema.py              ← NEW: formal schema for trace output dict
│   │
│   └── utilities/
│       ├── interpolate.py               ← NEW: breakpoint interpolation helper (currently inline in score_engine.py)
│       └── table_lookup.py              ← constants.py: lookup_calorie_density()
│
├── ontology/
│   │
│   ├── signals/
│   │   ├── additive_patterns.py         ← signal_extractor.py: ADDITIVE_MARKER_PATTERNS
│   │   ├── sugar_markers.py             ← signal_extractor.py: ADDED_SUGAR_MARKERS_HE, SWEETENER_MARKERS_HE
│   │   ├── whole_grain_markers.py       ← signal_extractor.py: WHOLE_GRAIN_MARKERS_HE
│   │   └── fat_markers.py              ← signal_extractor.py: SEED_OIL_MARKERS_HE, etc.
│   │
│   ├── fortification/
│   │   └── vitamin_mineral_markers.py   ← NEW: FORTIFICATION_MARKERS_HE (v3 evolution #4)
│   │
│   ├── matrix_integrity/
│   │   └── disruption_markers.py        ← NEW: MATRIX_DISRUPTION_MARKERS_HE (v3 evolution #1)
│   │
│   ├── processing_patterns/
│   │   ├── nova_signal_weights.py       ← nova_proxy.py: NOVA4_STRONG_SIGNALS, NOVA4_MODERATE_SIGNALS
│   │   └── flavor_classification.py     ← NEW: NATURAL_FLAVOR_MARKERS_HE vs ARTIFICIAL_FLAVOR_MARKERS_HE
│   │
│   └── category_markers/
│       ├── hard_anchors.py              ← NEW: CATEGORY_HARD_ANCHORS (e.g., גרנולה → snack_bar_granola)
│       └── signal_weights.py            ← category_classifier.py: CATEGORY_SIGNALS, CATEGORY_SIGNALS_NAME_ONLY
│
├── router/
│   │
│   └── bsip2_router/
│       ├── router.py                    ← category_classifier.py: classify_category() — refactored
│       ├── beverage_gate.py             ← category_classifier.py: beverage liquid gate logic
│       ├── nutritional_hints.py         ← category_classifier.py: _nutritional_hints()
│       ├── anchor_resolver.py           ← NEW: hard anchor evaluation
│       └── hybrid_resolver.py           ← NEW: hybrid product detection (protein drink, fortified dairy)
│
├── archetypes/
│   │
│   ├── _base/
│   │   ├── archetype_base.py            ← NEW: base class / interface for all archetypes
│   │   └── default_archetype.py         ← NEW: fallback for unclassified products (current "default" category)
│   │
│   ├── cereal_system/
│   │   ├── __init__.py
│   │   ├── archetype.py                 ← NEW: cereal archetype definition
│   │   ├── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["cereal"]
│   │   ├── guardrail_module.py          ← score_engine.py: HP_CRUNCH gate, cereal-specific caps
│   │   ├── matrix_integrity.py          ← NEW: matrix disruption signals for cereals
│   │   └── subtypes.py                  ← NEW: granola, oatmeal, extruded, muesli, kids, protein subtypes
│   │
│   ├── dairy_liquid/
│   │   ├── __init__.py
│   │   ├── archetype.py
│   │   ├── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["dairy_protein"]
│   │   ├── guardrail_module.py
│   │   └── subtypes.py                  ← whole milk, plant-based, protein drinks, lactose-free
│   │
│   ├── snack_bar/
│   │   ├── __init__.py
│   │   ├── archetype.py
│   │   ├── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["snack_bar_granola"]
│   │   ├── guardrail_module.py          ← score_engine.py: SNACK_BAR_HIGH_CAL, SNACK_BAR_RED_SUGAR caps
│   │   └── subtypes.py                  ← granola_bar, date_bar, protein_bar, rice_cake
│   │
│   ├── whole_food_fat/
│   │   ├── __init__.py
│   │   ├── archetype.py
│   │   ├── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["whole_food_fat"]
│   │   ├── guardrail_module.py          ← score_engine.py: satiety_rules_gated exemption
│   │   └── subtypes.py                  ← nuts, seeds, nut_butter, avocado
│   │
│   ├── beverage/
│   │   ├── __init__.py
│   │   ├── archetype.py
│   │   ├── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["beverage"]
│   │   └── guardrail_module.py          ← score_engine.py: SE_BEVERAGE_KCAL gate
│   │
│   └── sauce_spread/
│       ├── __init__.py
│       ├── archetype.py
│       └── calorie_density_table.py     ← constants.py: CALORIE_DENSITY_TABLES["sauce_spread"]
│
└── outputs/
    ├── batch_runner.py                  ← batch_run.py: run_batch() — generic, archetype-agnostic
    └── report_generator.py              ← generate_*.py scripts — unified report generator
```

---

## Current File → Target Location Mapping

| Current file | Target location | Notes |
|---|---|---|
| `constants.py` | Split across `core/constants/` + `archetypes/*/calorie_density_table.py` | Grade thresholds and NOVA tables stay in core; calorie density tables move to archetypes |
| `score_engine.py` | `core/scoring_engine/` + `archetypes/*/guardrail_module.py` | Shared math stays in core; category-specific guardrail conditions move to archetypes |
| `nova_proxy.py` | `core/signal_interpretation/nova_proxy.py` | No logic change; pure relocation |
| `signal_extractor.py` | `core/` (extraction logic) + `ontology/signals/` (marker dictionaries) | The pattern dictionaries separate from the extraction algorithm |
| `category_classifier.py` | `router/bsip2_router/` + `ontology/category_markers/` | Signal weights move to ontology; routing logic moves to router |
| `trace_writer.py` | `core/waterfall/trace_writer.py` | No logic change; pure relocation |
| `input_loader.py` | `core/orchestration/input_loader.py` | No logic change; pure relocation |
| `evaluation_scope.py` | `core/orchestration/evaluation_scope.py` | No logic change; pure relocation |
| `batch_run_*.py` | `outputs/batch_runner.py` | Single generic batch runner; archetype-specific paths via config |
| `generate_*_reports.py` | `outputs/report_generator.py` | Single generator parameterized per run |

---

## What Is NOT in This Structure

- No `bsip2_cereal.py` — cereal logic is in `archetypes/cereal_system/`, not a fork of the engine
- No duplicate `constants.py` per archetype — constants live in `core/constants/` once; archetypes reference them
- No duplicate scoring math — `core/scoring_engine/dimensions.py` is the one scoring engine
- No category-specific `nova_proxy` — NOVA inference is universal; only the signal inputs differ by archetype context

---

## Implementation Notes

The structure above represents the end state. During migration (see `migration_strategy.md`), the flat `src/` structure continues to run. Files are relocated incrementally without restructuring scoring logic until migration phase 3.

The `archetypes/_base/archetype_base.py` will define the interface that all archetype modules must satisfy:
- `calorie_density_table: list[tuple[float, float]]`
- `guardrail_module: callable`
- `local_signals: list[str]`
- `dimension_weight_overrides: dict[str, float] | None`
- `floor_definitions: dict`

This interface is the contract. Anything that satisfies it can be plugged into the shared engine.
