---
id: TASK-357
title: Migrate SNACKS onto the shared comparison spine (drop bespoke renderer)
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - snacks_frontend_v5.json + /hashvaot/snacks route exist (asserted); migration completed via TASK-362/de-anchor sweep. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: HIGH
created_at: 2026-06-19
depends_on: []
blocks: []
category_id: snacks
summary: >
  Snacks route renders a bespoke SnacksComparisonPage/snack-product-detail-panel (caps_applied/glossary, leaks 'cap' token) and ignores insightLine/rowVerdict/comparisonContext. Migrate to the shared dropdown spine like JuicesComparisonPage, rendering getSnacksPageData() (v3, already shared-shape). Drop bespoke caps/glossary. Then a Tom-v1.0 voice pass on v3. Owner-directed 2026-06-19 (zero-different-category mandate).
---

# TASK-357 — Migrate SNACKS onto the shared comparison spine (drop bespoke renderer)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
