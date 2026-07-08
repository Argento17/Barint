---
id: TASK-524
title: trace_writer.py omits emulsifier_complexity_penalty from serialized penalties_applied ledger
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  assemble_trace() doesn't serialize the ECS-v1 emulsifier_complexity_penalty into penalties_applied, so a real earned penalty (e.g. the -4.0 that creates yogurt's first live E, barcode 55329) is invisible in the trace's own disclosed ledger even though score_engine.py correctly applies it (score==trace passes; only the trace's SELF-DISCLOSURE is incomplete). Benign for score correctness, load-bearing for a public grade's 'show your math' defensibility. Fix = serialize the field + regen affected traces.
---

# TASK-524 — trace_writer.py omits emulsifier_complexity_penalty from serialized penalties_applied ledger

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
