---
id: TASK-321B
title: Cheese conformance config (run_cheese_001 → 45-product parity)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  C1-GROK (P171): draft configs/cheese.json from OFF-clean run_cheese_001, scope to the 45 live barcodes, verify score parity, declare render_fields. No deploy.
---

# TASK-321B — Cheese conformance config (run_cheese_001 → 45-product parity)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## ORCHESTRATOR VERIFIED 2026-06-17 — config conforming + gate-clean
Grok rev2 (run_cheese_004, no-parity). Independently verified by re-running generate_page:
- 58 emitted initially; G8 DATA-SANITY failed on 5 records (nutrition-panel text in ingredients field) → orchestrator added 5 discards (missing-data-discard rule).
- After discards: **53 products, ALL gates PASS (G1-G8), OFF=0 in run/corpus/output, exit 0.**
- run_cheese_004 (59 traces) − 1 non-cheese (seasoning) − 5 G8-fail = 53. baseline_json=null (legacy replaced).
- DATA/CONFIG half COMPLETE. Remaining: fresh Hebrew copy (Content/Sonnet) + frontend route. No deploy.
