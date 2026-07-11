---
id: TASK-616
title: Yogurt shelf configs have baseline_json:null -> 67 products never built into dossiers
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-610
lesson_trigger: none
summary: >
  PD-2 join found yogurt_drinkable.json + yogurt_spoonable.json shelf configs carry baseline_json:null, so build_dossiers.py cannot reach their 67 registry products (17+50). Pre-existing config defect, unrelated to PD. Fix the two configs to point at the served baseline so all 687 registry products build into dossiers. build_dossiers.py already guards the resulting crash (skips null-baseline configs) so the other 16 shelves build.
---

# TASK-616 — Yogurt shelf configs have baseline_json:null -> 67 products never built into dossiers

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
