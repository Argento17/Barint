---
id: TASK-372
title: D4 display perception gap: contested-but-not-scored additives (RT-M4)
owner: product-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-21
closed_at: 2026-06-21
depends_on: [TASK-369]
blocks: []
category_id: null
close_reason: >
  Product ruling (RETURNED, orchestrator-verified — no-op resolution): RT-M4 resolved via option (b) tooltip-only
  disclosure. The signed TASK-369 copy already carries the epistemic weight ("מוקדם ולא שוכפל") that explains why
  E300/E330/E202 show contested but don't move the score; a new visual sub-tier would be disproportionate for 3
  LOW-conf additives on a not-yet-live layer and against conformance-phase design-token discipline (anchored to Score
  Presentation v1 Rule 5: uncertainty handled by text qualifier, not visual encoding). ZERO score/engine/copy/frontend
  changes. Reversal condition logged: revisit a visual sub-label only if post-live consumer data attributes confusion
  specifically to the score-display gap (not tooltip language).
summary: >
  Red-Team RT-M4 (TASK-369): E300/E330/E202 are shown as 'contested' tier in the Glass Box additive tooltip but are score_eligible=False (LOW-confidence, do NOT affect the headline score). When the D4 tooltip display surfaces, a consumer could notice 'flagged as contested but not penalized' -> trust gap. Product to rule on how the display distinguishes scored-contested (high-conf) from displayed-only contested (low-conf), or accept the gap. Display-architecture decision; not a copy/score change.
---

# TASK-372 — D4 display perception gap: contested-but-not-scored additives (RT-M4)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
