---
id: TASK-435
title: Bread page shelf-filter chips reference stale cluster ids that match zero products (pre-existing since v3)
owner: frontend-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: bread
summary: >
  BREAD_SHELF_LENS_OPTIONS ids (fermentation/strong/...) don't match actual _website_cluster values in bread_frontend (high_protein/wholegrain/sourdough/everyday/wellness_ambig/pita/specialty). Most bread filter chips silently match 0 products; live since v3, surfaced during TASK-433 frontend wiring. Align the filter taxonomy (Content/Data decide labels) to the real clusters. Not blocking crackers.
---

# TASK-435 — Bread page shelf-filter chips reference stale cluster ids that match zero products (pre-existing since v3)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
