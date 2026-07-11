---
id: TASK-612
title: EV-026 fat-placeholder proven damage (bread + corpus collector) — tripwire-1
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
close_reason: >
  Read-only diagnosis DELIVERED + orchestrator-verified (spot-checked bsip2_trace
  L1_observed_signals.fat_g=0.25 + fat_quality=90.5 for the grade-flip product 7290014321168).
  VERDICT: SCORE-MOVING (unlike cereals — bread trace scored on the placeholder fat, baked in at
  BSIP1 enrichment). Nutrition Agent reproduced the fat_quality formula exactly for all 18 and ran
  an isolated same-engine before/after sim: 14/18 move (Δ −0.1 to −6.0), 1 grade flip B→C
  (7290014321168 keto bread, 0.25→9.1g real fat), max |Δ|=6.0, all ≤30. Also independently
  re-confirmed the TASK-563 non-derivability (bread served run has no trace; current engine drifts
  ~4pt from the 06-18 proxy). Under the owner score-change authority (2026-07-11, |Δ|≤30) this is NOT
  owner-gated — the correction is the orchestrator's to apply. Handed to → TASK-614 (systematic
  re-score on current engine with corrected nutrition, after re-scrape baseline + parser fix; excl.
  7290016967074 identity anomaly). Diagnosis touched no published data.
depends_on: []
blocks: []
category_id: null
origin_task: TASK-602
lesson_trigger: recurrence
summary: >
  Collector for the EV-026 fat=placeholder pattern surfaced by the TASK-602 re-scrape. Bread proven 18/23 material fat discrepancy. Diagnose score-dependence (read-only), then owner rules per tripwire-1. Evidence: 02_products/bread/bsip0_outputs/task602_bread_rescrape_20260711/bread_diff.json.
---

# TASK-612 — EV-026 fat-placeholder proven damage (bread + corpus collector) — tripwire-1

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
