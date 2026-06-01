---
id: TASK-111
title: Comparison UI Reference v2 data-dependency review
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on: []
blocks: []
category_id: null
summary: >
  Review the BariProductVM field dependencies for Comparison UI Reference v2
  (additive_count, base_pct, confidence, protein_g + others). Classify each as
  already-exists / safely-derivable / requires-new-pipeline / category-specific.
  Verdict: READY_WITH_MODIFICATIONS (base_pct needs new main-ingredient extraction;
  confidence promotion needs a hummus re-audit).
---

# TASK-111 — Comparison UI Reference v2 data-dependency review

Field inventory and readiness assessment for the v2 metric block
(protein · additives · base %) against the current view-model contract.
Analysis deliverable only — no implementation, no scoring change.
