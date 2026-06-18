---
id: TASK-262
title: Factory: canonical schema v3 (milk-depth content) + generator + copy wiring
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-12
closed_at: 2026-06-12
depends_on: [TASK-260]
blocks: []
category_id: null
close_reason: >
  P43 delivered canonical schema v3 (= v2 + milk's 4 content fields: consumerTakeaway,
  consumerExplanation obj, bariInterpretation[], bestUseCases[]) plus generator + copy-engine
  updates. Orchestrator-verified: v3 schema has all 4 fields; re-run → 8/8 stages SKIPPED
  (execution + resume); final throwaway page 0 PENDING with all 4 fields populated; G2/G6 PASS
  + readability 85/85; ZERO OFF. CRITICAL INTEGRITY CHECK PASSED: bariInterpretation dimension
  scores trace to the REAL BSIP2 trace dimension_scores (processing_quality 85.0=85.0,
  additive_quality 100=100, nutrient_density 66.7=66.7) — real data, not fabricated. v2 stays
  valid (additive). The factory now emits milk-DEPTH pages. Next: real Content-Agent
  milk-quality authoring via the contract (P44).
summary: >
  Extend canonical-v2 to v3 with milk's content fields (consumerTakeaway, consumerExplanation obj, bariInterpretation[], bestUseCases[]). Update generate_page to emit them (deterministic dimension data + PENDING for authored text), build_copy_inputs fact-sheets, author_copy contract+baseline, merge+gates. Re-run throwaway chain: schema_carries_milk_depth=TRUE, 0 PENDING, gates pass. Synthesis = yogurts structure + milk depth. Throwaway only; OFF-ban.
---

# TASK-262 — Factory: canonical schema v3 (milk-depth content) + generator + copy wiring

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
