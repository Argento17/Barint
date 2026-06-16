---
id: TASK-246
title: Engine-level fix for BARI_RECAL_P0_YOGURT_TRIM Path A gap (fermentation keyword bonus uncapped in score_engine.py)
owner: nutrition-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-11
depends_on: [TASK-245]
blocks: []
category_id: null
summary: >
  Surfaced by yogurts v4 rebuild (run_yogurt_005, 2026-06-11): the TASK-169D yogurt trim does not cap the fermentation bonus path driven by ingredient keywords (Path A), so a product can exceed the cap at engine level; the v4 frontend builder applies an 89.9 post-cap as a stopgap (1 product affected: Danone Pro 21 90.4->90/A). Move the cap into score_engine.py trim condition, flag-gated, D7 co-sign (nutrition+product), owner sign-off before ship (tripwire 1). Until then every red-team/QA recompute of yogurts must apply the documented builder cap to reproduce published scores.
---

# TASK-246 — Engine-level fix for BARI_RECAL_P0_YOGURT_TRIM Path A gap (fermentation keyword bonus uncapped in score_engine.py)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
