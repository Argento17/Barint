---
id: TASK-588
title: Catalog-registry alignment: register all live categories + CI parity gate
owner: frontend-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Owner-approved 2026-07-10. Catalog registry covers only 7 of ~20 live categories; everything since (yogurt, juices, chocolates, cookies, protein bars, cheese trio, milk) is invisible in /catalog. Register every live category whose data matches the registry contract (Hebrew names REUSED from existing signed-off page data, zero new consumer strings), add a CI parity check (registry ids vs served comparison JSONs), Stage 13 checkbox. BUILD-HEAVY: Codex gpt-5.6-sol in worktree.
---

# TASK-588 — Catalog-registry alignment: register all live categories + CI parity gate

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
