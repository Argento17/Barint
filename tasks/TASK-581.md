---
id: TASK-581
title: Adopt the generated page schema as the contract (review 42 diffs, fix magnitude typing, sync ops copy)
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Follow-up to TASK-569. The generated schema (bari-web/schema/page-output-schema.generated.json) passes 18/18 shelves; the hand-maintained page_output_schema_v1.json has 42 categorized differences and types limitingFactors[].magnitude as string while chocolate_bars/chocolate_tablets/snacks emit numbers (G1's checker validates property presence, not value types, so it never caught this). Work: review the 42-diff list in TASK-569_return, decide field-by-field which side is right, fix the hand schema or the contract type accordingly, add a CI step that regenerates and diffs so lag can never return, and define the sync between bari-web/schema and 03_operations/page_generator/contract.
---

# TASK-581 — Adopt the generated page schema as the contract (review 42 diffs, fix magnitude typing, sync ops copy)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
