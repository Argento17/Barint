---
id: TASK-181K
title: Glass Box W4 rework Data re-implement material non-material split behind BARI_GLASSBOX_W4 OFF byte-identical
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-181J]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
summary: >
  Re-implement the D3 rule in score_engine.py to the revised rule from 181J: replace the flat medium=0.70 score-pull with the material/non-material split - material uncertainty shrinks the score (low-band treatment), non-material uncertainty does NOT move the D3 score (routes to D6/confidence only). Keep everything behind BARI_GLASSBOX_W4 (default OFF); OFF = byte-identical to current baseline (re-run verify_glassbox_w4_off_identical.py, 0-diff). Re-emit the impact preview. Does NOT flip the flag, rescore published data, or touch frozen invariants.
---

# TASK-181K — Glass Box W4 rework Data re-implement material non-material split behind BARI_GLASSBOX_W4 OFF byte-identical

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
