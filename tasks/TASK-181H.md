---
id: TASK-181H
title: Glass Box W4 QA OFF byte-identity verification plus ON score-impact analysis for owner go-live review
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-181G]
blocks: []
category_id: null
roadmap_impact: true
work_type: qa
summary: >
  Verify BARI_GLASSBOX_W4 OFF = byte-identical (0-diff on all golden/frozen corpora incl. milk run_005_headpin, snack 70/B, bread). Then produce the ON score-impact analysis: which products' D3 sub-score / caps / grades move when ON (esp. low/medium-confidence NOVA assignments moving toward neutral 50), and confirm frozen invariants do not breach (spec 4.3). This analysis is the input to the SEPARATE owner go-live decision (flag flip = frozen-invariant tripwire). Does not flip live.
---

# TASK-181H — Glass Box W4 QA OFF byte-identity verification plus ON score-impact analysis for owner go-live review

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
