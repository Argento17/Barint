---
id: TASK-349
title: Bari Gold Set — expert-rubric accuracy gate (sibling to Shadow1): measures whether scores are RIGHT vs reviewed ground truth, never changes scores/engine
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
summary: >
  Phase 0 exploration (C1/C2/C3) then schema+seed (~30 reviewed products), gold_check.py harness (exit 0/1/2), CI wire. Read-only over engine+published scores; disagreements are FINDINGS routed to Nutrition, never auto-fixes. Sibling to TASK-253 Shadow1 (stability) — this is accuracy.
---

# TASK-349 — Bari Gold Set — expert-rubric accuracy gate (sibling to Shadow1): measures whether scores are RIGHT vs reviewed ground truth, never changes scores/engine

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
