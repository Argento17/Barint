---
id: TASK-457
title: Wire apply_protein_bar_lens into uniform score_engine.py + fix grade-boundary reproduction (unblocks protein_bars de-anchor)
owner: nutrition-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-07-02
blocker: "Engine wiring + grade-reproduction analysis (Nutrition/Data); needs Nutrition/Product co-sign since it changes the protein_bars scoring path"
depends_on: [TASK-456]
blocks: []
category_id: protein_bars
summary: >
  TASK-456 found apply_protein_bar_lens (approved TASK-365 methodology) is NOT called from score_engine.py (comment-only ~line 2334); generic path uses wrong weights/caps. The bespoke batch driver (batch_run_protein_bars_task365.py) made the live page but its flag-off grades diverge from live for 2/32 products (C where live=D at same score), so the de-anchor delta can't be isolated. Wire the lens into the uniform engine + reconcile grade-boundary logic so flag-off byte-reproduces the published page (scores AND grades); merge the 2 approved worktree-absent files (rescore_task365_inplace.py, batch_run_protein_bars_task365.py from master@6871d374). THEN protein_bars ships its genuine 3-flip de-anchor via the canonical path. Uniform-baseline-doctrine fix.
---

# TASK-457 — Wire apply_protein_bar_lens into uniform score_engine.py + fix grade-boundary reproduction (unblocks protein_bars de-anchor)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
