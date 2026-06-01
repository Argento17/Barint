# BSIP2 v3 Migration Strategy

**Status:** Design specification
**Date:** 2026-05-18

---

## Principle: Zero Breakage, Additive Migration

The current BSIP2 proto_v0 (`C:\Bari\03_operations\bsip2\proto_v0\src\`) is a working, validated system. It has scored two product categories (milk, cereals) with a fully traceable waterfall. Its scores are reference points.

The migration to v3 architecture must satisfy these constraints:

1. **Existing batch runs must reproduce identical scores** at every phase boundary. Regression is detected by re-running `batch_run_cereals_001.py` and `batch_run_milk_004.py` and comparing output traces.

2. **No phase blocks another.** Each phase is independently deployable. The project can stop at any phase and the system continues to function.

3. **No logic duplication.** If a function exists in both `proto_v0` and the new structure during migration, it must be an import alias, not a copy. Two versions of `score_glycemic_quality()` existing simultaneously is a maintenance failure.

4. **Each phase produces a validation artifact** — a re-run of existing batch jobs that confirms identical output.

---

## Migration Phases

### Phase 0 (NOW) — Fix the Breaking Issues Before Migrating

Before restructuring anything, apply the four targeted fixes from the Evolution Proposal:

1. Granola hard anchor → `category_classifier.py`
2. Fiber laundering cap → `score_engine.py:score_glycemic_quality()`
3. Whole-grain laundering control (signal split + NOVA proxy gate) → `signal_extractor.py`, `nova_proxy.py`
4. NOVA1 floor gate (matrix disruption signal + apply_floors gate) → `signal_extractor.py`, `score_engine.py:apply_floors()`
5. Threshold smoothing (graduated soft penalties) → `score_engine.py:evaluate_guardrails()`

**Rationale:** Migrate a working, well-calibrated system — not a broken one. Running `run_cereals_002` on the fixed proto_v0 provides the validated baseline that v3 migration must reproduce.

**Deliverable:** `run_cereals_002` batch run with fixed proto_v0. Scores are the new baseline.

**Regression requirement:** None — this phase changes scores deliberately. Document changes in run_cereals_002 batch summary.

---

### Phase 1 — Ontology Separation

**What:** Extract all signal vocabulary dictionaries from `signal_extractor.py` and category constants from `category_classifier.py` and `constants.py` into the `ontology/` directory structure. No logic moves in this phase — only data.

**Files created:**
- `ontology/signals/additive_patterns.py` — `ADDITIVE_MARKER_PATTERNS` from `signal_extractor.py`
- `ontology/signals/sugar_markers.py` — `ADDED_SUGAR_MARKERS_HE`, `SWEETENER_MARKERS_HE`
- `ontology/signals/whole_grain_markers.py` — `WHOLE_GRAIN_MARKERS_HE`
- `ontology/signals/fat_markers.py` — seed oil markers
- `ontology/processing_patterns/nova_signal_weights.py` — NOVA4_STRONG_SIGNALS, NOVA4_MODERATE_SIGNALS
- `ontology/processing_patterns/flavor_classification.py` — natural vs artificial flavor split
- `ontology/category_markers/signal_weights.py` — `CATEGORY_SIGNALS`, `CATEGORY_SIGNALS_NAME_ONLY`
- `ontology/category_markers/hard_anchors.py` — `CATEGORY_HARD_ANCHORS` (new, already implemented in Phase 0)
- `ontology/matrix_integrity/disruption_markers.py` — `MATRIX_DISRUPTION_MARKERS_HE` (from Phase 0)

**Files modified (import redirects only):**
- `signal_extractor.py` — replaces inline dicts with `from ontology.signals.additive_patterns import ADDITIVE_MARKER_PATTERNS`
- `category_classifier.py` — replaces inline dicts with imports from `ontology/category_markers/`
- `nova_proxy.py` — replaces inline lists with imports from `ontology/processing_patterns/`

**Files NOT touched:** `score_engine.py`, `constants.py`, `trace_writer.py`, `input_loader.py`

**Regression requirement:** Re-run `batch_run_cereals_001.py` and `batch_run_milk_004.py`. Output traces must be bit-identical to Phase 0 baseline (same scores, same trace structure). Any diff is a Phase 1 bug.

**Effort:** Low. All changes are data extraction and import rewiring.

---

### Phase 2 — Router Upgrade

**What:** Refactor `category_classifier.py` into the router architecture described in `router_design.md`. The output contract (dict with `category`, `category_confidence`, `secondary_category`, `category_instability_flag`, `classification_basis`, `confidence_band`) must remain identical for backward compatibility.

**Files created:**
- `router/bsip2_router/__init__.py`
- `router/bsip2_router/router.py` — main routing function, replaces `classify_category()`
- `router/bsip2_router/anchor_resolver.py` — Stage 1 anchor check
- `router/bsip2_router/beverage_gate.py` — extracted from current classifier
- `router/bsip2_router/nutritional_hints.py` — `_nutritional_hints()` function
- `router/bsip2_router/hybrid_resolver.py` — new, but may initially return no-hybrid for all products

**Files modified:**
- All `batch_run_*.py` files — change import from `category_classifier` to `router.bsip2_router.router`
- `category_classifier.py` — becomes a thin shim: `from router.bsip2_router.router import classify_category`

**New trace fields added (backward-compatible additions):**
- `routing_basis`
- `anchor_override`
- `archetype_subtype` (initially null for most products)
- `routing_version`

**Regression requirement:** Re-run `batch_run_cereals_001.py` and `batch_run_milk_004.py`. Scores must be identical to Phase 0 baseline. Routing decisions may change for granola products (improvements already deployed in Phase 0), but no new regressions for correctly-routed products.

**Effort:** Medium. The signal-gating refinements (context-gated signals) require careful testing.

---

### Phase 3 — Core Extraction

**What:** Extract the scoring engine into `core/scoring_engine/`. This is a structural relocation — no logic changes.

**Files created:**
- `core/scoring_engine/dimensions.py` — all `score_*()` functions from `score_engine.py`
- `core/scoring_engine/guardrails.py` — `evaluate_guardrails()`, `_coordinate_family()`
- `core/scoring_engine/floors.py` — `apply_floors()`
- `core/scoring_engine/confidence.py` — `compute_confidence()`
- `core/scoring_engine/structural_emptiness.py` — `detect_structural_emptiness()`
- `core/constants/grade_thresholds.py` — `GRADE_THRESHOLDS`, `score_to_grade()`
- `core/constants/nova_tables.py` — NOVA score tables
- `core/constants/red_label_thresholds.py` — `RED_LABEL_THRESHOLDS`
- `core/constants/penalty_budgets.py` — `*_FAMILY_BUDGET` constants
- `core/waterfall/trace_writer.py` — relocation, no changes
- `core/orchestration/input_loader.py` — relocation, no changes
- `core/orchestration/evaluation_scope.py` — relocation, no changes

**Files modified:**
- `score_engine.py` — becomes a thin shim with re-exports from `core/`
- `constants.py` — becomes a thin shim with re-exports from `core/constants/`

**Regression requirement:** Identical. Re-run both batch jobs, compare traces. No score changes expected.

**Effort:** Low-medium. Pure relocation. The shim pattern means existing batch runners don't need to change.

---

### Phase 4 — Archetype Shell Creation

**What:** Create the `archetypes/` directory structure and extract archetype-specific logic from `score_engine.py` into archetype modules. The scoring engine remains shared; archetype modules declare the parameters they inject.

**Files created:**
- `archetypes/_base/archetype_base.py` — base interface
- `archetypes/cereal_system/archetype.py` — wraps cereal-specific guardrail conditions
- `archetypes/cereal_system/calorie_density_table.py` — cereal kcal table
- `archetypes/cereal_system/guardrail_module.py` — HP_CRUNCH gate logic
- `archetypes/snack_bar/archetype.py`
- `archetypes/snack_bar/guardrail_module.py` — SNACK_BAR_HIGH_CAL, SNACK_BAR_RED_SUGAR
- `archetypes/whole_food_fat/archetype.py`
- `archetypes/whole_food_fat/guardrail_module.py` — satiety_rules_gated exemption
- `archetypes/dairy_liquid/archetype.py`
- `archetypes/beverage/archetype.py`

**Files modified:**
- `core/scoring_engine/guardrails.py` — archetype-specific conditions are now injected by the archetype module rather than hardcoded as `category == "cereal"` checks. The function signature changes to accept an optional `archetype_context` dict.

**This is the most structurally significant change.** The inline category checks in `evaluate_guardrails()`:
```python
# Current (hardcoded in guardrails.py):
hp_crunch = (category == "cereal" and sugar >= HP_CRUNCH_SWEET_SUGAR and fiber <= HP_CRUNCH_SWEET_FIBER)
is_snack_bar = category == "snack_bar_granola"
satiety_rules_gated = (category == "whole_food_fat" and ...)
```
Become:
```python
# v3 (injected by archetype module):
hp_crunch = archetype_context.get("hp_crunch_eligible", False) and sugar >= HP_CRUNCH_SWEET_SUGAR and fiber <= HP_CRUNCH_SWEET_FIBER
is_snack_bar = archetype_context.get("snack_bar_caps_active", False)
satiety_rules_gated = archetype_context.get("satiety_rules_gated", False)
```

**Regression requirement:** Identical. The archetype modules must produce exactly the same `archetype_context` dict that reproduces the current hardcoded behavior for all existing products.

**Effort:** Medium-high. Requires careful extraction and regression testing.

---

### Phase 5 — Batch Runner Unification

**What:** Replace the multiple `batch_run_*.py` files with a single `outputs/batch_runner.py` that accepts a run configuration.

**Current state:** `batch_run.py`, `batch_run_cereals_001.py`, `batch_run_milk.py`, `batch_run_milk_002.py`, `batch_run_milk_003.py`, `batch_run_milk_004.py` — six copies of essentially the same pipeline with different paths and `RUN_ID`s.

**Target:** One generic batch runner. Run configuration specifies:
- Source directory (BSIP1 outputs)
- Output directory
- Run ID
- Category tag (for reporting)

**Regression requirement:** Outputs identical to existing batch run outputs.

**Effort:** Low. The pipeline logic is already nearly identical across all batch runners.

---

## Migration Timeline

| Phase | Prerequisite | Estimated effort | Regression gate |
|---|---|---|---|
| 0 (bug fixes) | None | 1 session | Document intended score changes |
| 1 (ontology) | Phase 0 complete | 1-2 sessions | run_cereals_002, run_milk_004 identical |
| 2 (router) | Phase 1 complete | 2-3 sessions | run_cereals_002, run_milk_004 identical |
| 3 (core extraction) | Phase 2 complete | 1-2 sessions | run_cereals_002, run_milk_004 identical |
| 4 (archetypes) | Phase 3 complete | 3-4 sessions | run_cereals_002, run_milk_004 identical |
| 5 (batch unification) | Phase 4 complete | 1 session | All batch runs reproduced |

**Total: approximately 9-12 sessions.** Phases 1-3 are purely structural and can be done quickly. Phase 4 is the meaningful architectural change and requires the most care.

---

## What NOT to Do During Migration

**Do not migrate and modify simultaneously.** If Phase 3 (core extraction) discovers that `apply_floors()` should be refactored, note the refactor but do not perform it during Phase 3. Keep one axis of change at a time. Structural relocation and behavioral changes must be separate commits.

**Do not move files without shims.** Every moved file must leave behind an import shim so that existing code (`batch_run_cereals_001.py`, `generate_cereals_001_reports.py`) continues to import from the old location without modification.

**Do not create archetype weight overrides in Phase 4.** The archetype modules in Phase 4 must reproduce current behavior identically. Dimension weight overrides (the oil_system and dairy_liquid profiles in `shared_vs_local_dimensions.md`) require a separate calibration run after Phase 4 is complete.
