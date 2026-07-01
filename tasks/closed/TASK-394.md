---
id: TASK-394
title: Router R3 narrowing: stop chocolate-name marker mis-lensing flavor-descriptor biscuits
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-24
closed_at: 2026-06-24
close_reason: >
  Owner-approved (AskUserQuestion 2026-06-24) router fix BARI_R3_BISCUIT_NARROW_V1 (router_v2.4).
  R3 yields to a high-confidence (>=0.85) biscuit hard_anchor UNLESS ingredients show a
  genuine chocolate-confectionery signal (coating / chocolate-dominant) -> spares flavor-
  descriptor biscuits, preserves genuine chocolate + coated biscuits. Measured across 16
  shelves/572 products: 14 movers ALL on cookies_coffee (snack_bar_granola->biscuit), only
  2 GRADE changes (2986065 + 7290017894317 E->D, aligning chocolate Peti-Bar with butter twin),
  12 score-only nudges stay E, ZERO movement on chocolate_tablets/bars or any other shelf
  (orchestrator-verified vs diff_table + ingredient spot-checks of Milka Oreo/choc-sandwich/
  triple-choc-chip = all genuine biscuits correctly spared). Owner signed off; default flipped
  off->on (router_v2.py:44); cookies re-scored (run_cookies_task393_final) + baked: dist
  C10/D26/E83, score==trace 119/119 (orchestrator-verified). Engine change ships with the
  TASK-393 cookies rework deploy bundle (owner-gated).
depends_on: []
blocks: []
category_id: null
summary: >
  Router R3 narrowing: stop chocolate-name marker mis-lensing flavor-descriptor biscuits
---

# TASK-394 — Router R3 narrowing: stop chocolate-name marker mis-lensing flavor-descriptor biscuits

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
