---
id: TASK-181L
title: Glass Box W4 rework QA re-verify OFF identity plus new ON score-impact after medium split
owner: qa-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-04
blocker: "Waiting on TASK-181K (re-implemented engine must exist before re-verifying OFF identity + the new ON impact)."
depends_on: [TASK-181K]
blocks: []
category_id: null
roadmap_impact: true
work_type: qa
summary: >
  Re-verify BARI_GLASSBOX_W4 OFF = byte-identical (0-diff). Produce the NEW ON score-impact analysis after the material/non-material split: expect the net-downward shelf effect to collapse toward ~flat on quality (grade moves now only from material/low-certainty products; non-material peripheral-gap products no longer move grade, their doubt shows as confidence). Report new grade-move counts vs the prior 17-down/3-up, broken down by material vs non-material. Confirm frozen invariants hold (milk 85/A, snack 70/B). Analysis only - no flag flip, no published rescore.
---

# TASK-181L — Glass Box W4 rework QA re-verify OFF identity plus new ON score-impact after medium split

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
