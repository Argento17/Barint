---
id: TASK-289
title: Finish hummus comp JSON regen from run_hummus_shelfrel_002 + rewrite moved copy — release platform P-BASE prereq
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  DROPPED per owner (2026-06-16): "the hummus rescore and refreeze is so insignificant — just delete
  it altogether." The regen (verified correct: 69 prods, score==trace, OFF=0) was REVERTED —
  hummus_frontend_v5.json restored to committed HEAD (live stays v5-glassbox_w4). Content/Sonnet copy
  pass (a4f393a4) abandoned; its output not committed. Untracked regen scratch
  (03_operations/page_generator/configs/hummus_shelfrel_002.json + regen script) left untracked,
  harmless. No consumer-facing change. Not a defect — owner prioritization call to clear the pipeline.
summary: >
  hummus_v5.json is stale (2026-06-05 glassbox_w4, 64 prods); does not reflect run_hummus_shelfrel_002 (69 traces). Regen the comp JSON (scores/grades/_meta) from the shelfrel run, then Content/Sonnet rewrites moved insightLines + 'יורד ל-D' card + blog grade counts. Owner-ratified scores (TASK-278); deploy owner-gated.
---

# TASK-289 — Finish hummus comp JSON regen from run_hummus_shelfrel_002 + rewrite moved copy — release platform P-BASE prereq

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
