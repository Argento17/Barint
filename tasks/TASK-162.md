---
id: TASK-162
title: Bread comparison: switch front-of-row bar from protein to fiber
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — verified BREAD_METRIC_SPECS=[FIBER_METRIC] in bread-comparison-page.tsx. fiber_g added to BariProductMetricsVM + MetricNumberKey; FIBER_METRIC spec added (scaleMax 20, good 7, poor 4, aria 'גרם סיבים ל-100 גרם'), modeled on PROTEIN_METRIC. bread builder reads metrics.fiber_g from expansion.nutrition.fiber (null passes through, no fabrication). PROTEIN_METRIC/DAIRY_PROTEIN_METRIC intact — other categories untouched. Display-only, no scores changed. tsc/build/corpus-validate all exit 0."
depends_on: []
blocks: []
category_id: bread
summary: >
  Nutrition (TASK-161A) judged fiber the more meaningful headline for bread than protein. Data is present (fiber on all 24). Needs fiber wired into the metrics view-model + a fiber metric spec, then point bread at it. Display-only, no score change.
---

# TASK-162 — Bread comparison: switch front-of-row bar from protein to fiber

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
