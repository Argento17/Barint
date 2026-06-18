---
id: TASK-321C
title: Yogurt conformance config (OFF-clean run, avoid run_yogurt_002)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: []
blocks: []
category_id: null
summary: >
  C1-GEMINI (P172): draft configs/yogurts.json from an OFF-clean yogurt run (NOT run_yogurt_002), match the live yogurt universe, declare render_fields. No deploy.
---

# TASK-321C — Yogurt conformance config (OFF-clean run, avoid run_yogurt_002)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## ORCHESTRATOR VERIFIED 2026-06-17 — config conforming + gate-clean
Gemini rev2 (run_yogurt_shelfrel_v2, no-parity). Independently verified via generate_page re-run:
- 87 emitted initially (108 run − 21 milk-context); G8 DATA-SANITY failed on 4 nutrition-bleed records
  (5416415, 43944, 45771, 4119133) → orchestrator added 4 discards (missing-data-discard rule).
- After discards: 83 products, ALL gates PASS (G1-G8), OFF=0 in run/output, exit 0. baseline_json=null (legacy replaced).
- DATA/CONFIG half COMPLETE. Remaining: fresh Hebrew copy (Content/Sonnet) + frontend route. No deploy.
