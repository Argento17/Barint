---
id: TASK-564
title: Schema lag: page_output_schema_v1.json still requires comparisonContext (owner had it removed) + limitingFactors null
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10, commit 5b5b70d6 (branch task564-schema-lag, pushed; PR awaits owner). Schema updated to the MEASURED live shape across all 16 shelves (scan evidence in close commit): comparisonContext optional per owner-directed removal; positiveSignals/limitingFactors nullable; limitingFactors string OR {text,magnitude} (942/247 live); d3_processing_signal object|null 10-key (schema still claimed engine does not emit it); AdditiveEntry + cosmetic_mup (94 entries); filterTags/milkProductType(+Label)/volumeMl optional. G1 5/16 -> 10/16. Remaining 6 shelves fail on raw INTERNAL fields shipped in served JSONs (_scoring_trace, nutrition_per_100g, duplicate name_he/image_url) - real data-hygiene defect, deliberately NOT whitelisted -> TASK-572. Golden page passes G1. Structural prevention = TASK-569 (VM-generated schema).
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found probing run_gates (TASK-565). G1 SCHEMA fails on 11/16 live shelves. Two causes: (1) schema marks expansion.comparisonContext REQUIRED, but cross-referencing copy was deliberately REMOVED per owner direction (the de-cross-referencing done in TASK-546, 'comparisonContext cleared per golden precedent') -- so the golden brined_cheeses page fails its own schema on every product; (2) expansion.limitingFactors is typed array but is null on several products. Same class as the TASK-431 schema-lag defect (schema did not whitelist the already-shipping brand field). Fix the SCHEMA to match the owner-ratified page shape; do NOT re-add comparisonContext copy. Blocks run_gates in CI.
---

# TASK-564 — Schema lag: page_output_schema_v1.json still requires comparisonContext (owner had it removed) + limitingFactors null

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
