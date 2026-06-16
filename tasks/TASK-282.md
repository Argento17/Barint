---
id: TASK-282
title: Wire additive severity (ADDITIVE_DB.tier) + category-rarity into scoring, not just display
owner: nutrition-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-14
blocker: "tripwire-1 scoring change; part of / feeds the Bari-wide red-label de-anchor project"
depends_on: []
blocks: []
category_id: null
summary: >
  ADDITIVE_DB.tier (functional/likely-neutral/dose-dependent/contested) drives only the display badge; the engine counts additives, doesn't weigh them (E150D scores like E500). Owner wants 'this one uses strange additives, unusual for biscuits' depth -> wire tier into additive_quality + add per-category additive frequency. Ref: additive_depth_ruling_v1 + orchestrator_report_v1 (TASK-275).
---

# TASK-282 — Wire additive severity (ADDITIVE_DB.tier) + category-rarity into scoring, not just display

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
