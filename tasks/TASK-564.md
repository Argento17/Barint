---
id: TASK-564
title: Schema lag: page_output_schema_v1.json still requires comparisonContext (owner had it removed) + limitingFactors null
owner: frontend-agent
status: IN_PROGRESS
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
