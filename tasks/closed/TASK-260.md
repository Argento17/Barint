---
id: TASK-260
title: Factory: wire the copy stage into the DAG (fact-sheets to authored to merge to gate)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-12
closed_at: 2026-06-12
depends_on: [TASK-259]
blocks: []
category_id: null
close_reason: >
  P42 added 3 copy stages (build_copy_inputs → author_copy → merge_copy_and_gate) to
  pipeline_e2e.py (now 8 stages). Orchestrator-verified: independent re-run → all 8 stages
  SKIPPED (execution + resume); final throwaway page 0 PENDING_COPY; G6 COPY-SAFETY PASS +
  readability 29/29; ZERO OFF; baseline copy is standalone + law-abiding. spine.db records the
  copy stage_runs + lineage (page→fact_sheets→authored→final). Authoring contract delivered
  (03_operations/page_generator/copy/authoring_contract.json) so a real Content-Agent author
  swaps into the author_copy seam unchanged. KEY STRATEGIC FINDING (orchestrator-validated):
  schema_carries_milk_depth = FALSE — milk's 4 rich per-product content fields
  (consumerTakeaway, consumerExplanation, bariInterpretation, bestUseCases) are absent from
  canonical-v2 (which has only insightLine/rowVerdict/positiveSignals/limitingFactors/
  comparisonContext). The factory now produces copy-complete pages, but at granola/snacks
  content depth, NOT the owner's milk gold standard. Reaching milk depth needs a schema
  widening + real Content-Agent authoring — surfaced to owner as the next decision.
summary: >
  Add copy generation to pipeline_e2e as DAG stages: build_copy_inputs (fact-sheets) -> author (pluggable agent-in-loop stage) -> merge_copy -> copy-safety gate + readability. Produce a 0-PENDING throwaway page. Quality target = the MILK page content depth; flag if canonical-v2 schema cannot carry it. Throwaway only; OFF-ban; no live category.
---

# TASK-260 — Factory: wire the copy stage into the DAG (fact-sheets to authored to merge to gate)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
