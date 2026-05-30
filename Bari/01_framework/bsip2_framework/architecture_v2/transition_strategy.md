# BSIP2 Transition Strategy — v1 to v2 Architecture

**Status:** Architecture specification  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Companion:** layer_architecture.md, orchestration_v2.md, dimension_mapping.md

---

## The Transition Challenge

The current BSIP2 implementation (proto_v0) has scored ~73 products across multiple categories. These traces are the ground truth for the system's current behavior. Any transition to v2 must:

1. Preserve the directional correctness of existing scores (a B product should remain near-B in v2)
2. Not require re-scraping or re-building BSIP0/1 data
3. Maintain output format compatibility for downstream consumers
4. Enable gradual validation before full cutover
5. Allow parallel running of v1 and v2 for comparison

The transition is **not a rewrite**. It is a **restructuring**. The underlying signals, thresholds, and philosophical commitments largely survive. What changes is how they are organized, weighted, and coordinated.

---

## Transition Phases

### Phase 0 — Architecture Stabilization (Current phase)
*What:* Define the v2 architecture in framework documents.  
*Status:* This document is part of Phase 0.  
*Deliverables:* layer_architecture.md, dimension_mapping.md, orchestration_v2.md, framework_philosophy.md, future_ui_direction.md, transition_strategy.md  
*No code changes.*  
*Duration estimate:* 1–2 sessions.

---

### Phase 1 — Signal Layer Instrumentation
*What:* Instrument the existing signal_extractor.py to produce richer L3 outputs aligned with the v2 layer model — without changing the scoring engine.

**Specific additions:**
- **Reconstruction intensity signal**: A continuous 0–100 estimate of how far the product has traveled from whole-food form, computed from: ingredient fragmentation count (isolates/concentrates/hydrolyzates), reconstruction-specific additives (emulsifiers, texture agents), and NOVA as prior.
- **Matrix coherence signal**: A binary flag indicating whether the declared ingredient list is internally coherent as a food matrix.
- **Fortification flag**: Detection of synthetic fortification (added vitamins beyond incidental presence), with count.
- **Engineering intent signals**: Expanded additive detection separating structural additives (stabilizers, emulsifiers) from palatability additives (flavor enhancers, synthetic colors, sweetener systems).
- **Liquid calorie effect flag**: Explicit boolean for liquid category + caloric density above threshold.

*Changes:* signal_extractor.py additions only. score_engine.py unchanged. All new signals appear in trace as L3 fields.  
*Risk:* Low. No scoring logic touched. Existing outputs unchanged.

---

### Phase 2 — Layer Index Computation (Shadow Mode)
*What:* Add a new `compute_layer_indices()` function that takes the enriched signals from Phase 1 and computes four provisional Layer Index values (L1–L4 as 0–100 floats), without affecting the current scoring path.

The function runs in **shadow mode**: it computes Layer Indices and writes them to the trace as `layer_indices_shadow` fields, but the final_score_estimate is still computed via the existing dimension pathway.

**Purpose of shadow mode:**
- Compare Layer Indices against existing dimension scores on the full corpus
- Validate that v2 Layer 1 correlates well with current processing_quality + whole_food_integrity
- Validate that v2 Layer 2 correlates well with current nutrient_density + protein_quality
- Detect unexpected divergences before they become live scoring
- Build a calibration dataset

*Changes:* New function in score_engine.py. trace_writer.py includes new shadow fields.  
*Risk:* Low-medium. Shadow computation doesn't affect live outputs.

---

### Phase 3 — Orchestration Prototype
*What:* Implement the v2 orchestration logic as a parallel scoring path, producing a `shadow_final_score` alongside the current `final_score_estimate`.

**Implementation:**
1. Implement `orchestrate_layers()` based on orchestration_v2.md:
   - Stage 1: structural ceiling from L1 index
   - Stage 2: nutritional floor from L2 index
   - Stage 3: metabolic adjustment from L3 index
   - Stage 4: engineering pressure from L4 index
   - Stage 5: regulatory resolution
   - Stage 6: confidence ceiling

2. Run the full corpus through both paths (current and shadow)

3. Compare shadow vs. current scores for all 73+ scored products

4. Document divergences, with explanatory trace for each product whose shadow score differs from current score by more than 5 points

*Changes:* New `orchestrate_layers()` function. Traces include `shadow_score` and `shadow_grade`.  
*Risk:* Medium. The shadow score may diverge from current scores. Divergences need investigation, not suppression.

---

### Phase 4 — Calibration and Validation
*What:* Investigate all significant divergences from Phase 3. For each:
- Is the divergence in the correct direction (does v2 produce a more honest score)?
- Are the orchestration constants (structural ceiling table, floor table, engineering pressure weights) calibrated correctly?
- Do the golden products suite scores (from `golden_products_suite.md`) still fall in the right qualitative ranges?

**Calibration targets (from golden_products_suite.md):**
- Plain almonds, tahini: should remain high (B+)
- Greek yogurt, cottage cheese: should remain mid-to-high (C–B)
- Oat milk: should remain mid (C–D)
- Coke Zero: should remain low (D–E)
- Sugary granola bar: should remain low (D–E)
- Fortified breakfast cereal: should capture the C-4 tension (declared nutrition via fortification)

**If the shadow scores violate these targets:** adjust orchestration constants before proceeding to Phase 5. Do not adjust to make scores "feel right" — adjust only when the architecture logic clearly produces incorrect outputs for traceable reasons.

*Changes:* Constant adjustments in orchestration logic only. No architectural changes.  
*Duration:* Variable. Calibration is iterative and requires human review.

---

### Phase 5 — Cutover Preparation
*What:* Prepare the v2 scoring path for production cutover.

**Steps:**
1. Retire the current dimension-weighted path. The `compute_dimension_scores()` function is replaced by the `compute_layer_indices()` + `orchestrate_layers()` pipeline.

2. Update `constants.py`:
   - Remove current NOVA_PROCESSING_SCORES, NOVA_WFI_SCORES (absorbed into Layer 1)
   - Add structural ceiling table, nutritional floor table
   - Add engineering pressure weights

3. Update `trace_writer.py`:
   - Remove `dimension_scores` (or retain as `legacy_dimension_scores`)
   - Add `layer_indices`, `orchestration_trace` as primary fields
   - Add `contradiction_flags`, `tension_notes`

4. Update `batch_run_*.py` scripts to confirm compatibility

5. Freeze a full v2 shadow run on the complete corpus as the comparison baseline

*Changes:* Significant. This is the actual cutover.  
*Risk:* Medium-high. Mitigated by parallel shadow running in Phases 2–4.

---

### Phase 6 — Category Re-validation
*What:* After cutover, re-run all existing category batches (snack_bars, milk_and_alternatives) under v2 and validate results.

**Acceptance criteria:**
- No product's grade changes by more than one tier without a traceable, defensible reason
- The hierarchical ordering within categories is preserved (whole dairy > plant alternatives; plain > flavored/sweetened)
- Golden products suite targets are met
- No new systematic biases emerge (check average score by NOVA level — NOVA 1 should still score substantially higher than NOVA 4)

*Changes:* New batch runs. Trace files updated. Summary reports regenerated.

---

### Phase 7 — UI Implementation
*What:* Build the Level 0–3 UI views described in `future_ui_direction.md`.

**Priority order:**
1. Level 0 (Card) — lowest effort, highest reach
2. Level 1 (Interpretation Panel) — primary value delivery
3. Level 2 (Tension View) — when contradiction flags are active
4. Level 3 (Full Trace) — engineering/research view

The tension view (Level 2) is new and requires the contradiction_flags from Phase 5 to be populated.

*Changes:* Front-end only. Backend outputs from Phase 5 are stable.

---

## What Is NOT Changing in the Transition

These elements survive the transition unchanged:

| Element | Status |
|---------|--------|
| BSIP0 scraping pipeline | Unchanged |
| BSIP1 canonicalization | Unchanged |
| Signal taxonomy (L1–L6) | Unchanged conceptually; L3 enriched in Phase 1 |
| NOVA proxy inference | Unchanged; moves inside Layer 1 |
| Category classification | Unchanged; category context feeds Layer calibration |
| Trans fat veto | Unchanged; remains outside layer system |
| Israeli red label detection | Unchanged; moves to Stage 5 regulatory resolution |
| Confidence computation | Unchanged; applies in Stage 6 |
| Explainability budget (max 3 drivers) | Unchanged; enforced in orchestration output |
| Grade scale (A–E) | Unchanged |
| Trace format | Backwards-compatible additions; no removals until Phase 5 |

---

## The Regression Test Suite

Before Phase 5 cutover, a regression test suite is established from the current run_002 milk corpus results:

| Product | Current Score | Current Grade | v2 Allowed Range | v2 Allowed Grade |
|---------|--------------|--------------|-----------------|-----------------|
| Whole milk 3.4% | 75 | B | 70–82 | B |
| Soy drink no sugar | 66.1 | C | 60–75 | C |
| Alpro oat (fixed) | 49.1 | D | 44–58 | D |
| Go Milk protein | 39.5 | E | 32–50 | D–E |
| Alpro almond (fixed) | 43.4 | D | 38–55 | D |
| Alpro soy chocolate | 36.2 | E | 28–45 | E |

The allowed range is ±10 points, ±1 grade tier. Products landing outside this range during shadow mode trigger a mandatory review before proceeding.

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Shadow scores diverge significantly from current on NOVA 4 products | High | Medium | Phase 4 calibration; Layer 1 ceiling table may need adjustment |
| Orchestration constants are hard to calibrate without more corpus data | Medium | High | Expand corpus to 200+ products before Phase 5 |
| v2 Layer 2 under-credits fortification relative to current | Medium | Low | Fortification skepticism discount is explicitly tunable |
| C-1 tension products generate user confusion | Medium | Medium | UI tension callout design (Level 2) must be clear |
| The four layers over-segment a simple product | Low | Low | Simple products have narrow layer variance; orchestration produces clean output |
| Parallel running creates engineering overhead | Medium | Low | Shadow mode is additive, not replacement |

---

## Milestone Checklist

- [ ] Phase 0: Architecture documents complete and reviewed
- [ ] Phase 1: signal_extractor.py instrumented with new L3 signals
- [ ] Phase 2: Shadow layer indices running on full corpus, shadow fields in traces
- [ ] Phase 3: Shadow final scores computed; divergence report generated
- [ ] Phase 4: Calibration complete; golden products suite validated
- [ ] Phase 5: v2 scoring path live; legacy path retired; traces updated
- [ ] Phase 6: Existing category batches re-validated
- [ ] Phase 7: UI Level 0–2 implemented

---

*This document will be updated as each phase is completed. Phase completion is marked by a freeze of the relevant output files.*
