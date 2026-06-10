---
id: TASK-181M
title: Prevent non-material confidence dents from independently triggering insufficient_data
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
depends_on: [TASK-181K]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
close_reason: >
  CC close-readiness gate PASS (2026-06-04). F3 boundary clamp implemented in score_engine.py
  (44/1, engine-only, behind BARI_GLASSBOX_W4): the −5 d3_nonmaterial_gap dent can no longer
  be the term that flips a graded product into insufficient_data; magnitude unchanged. OFF
  byte-identity INDEPENDENTLY verified 0-diff (342 products). Re-validation: the 3 maadanim
  that flipped under 181K are back to graded D (score identical 42.0/41.8/46.2); exactly 3
  rescues, 0 other diffs; genuine data-poor products still reach insufficient_data (25 no-gap
  + 12 genuinely-low-conf NOT wrongly rescued — guard is precise, not over-clamping); frozen
  invariants hold ON (milk 85/A, snack 70/B). No flag flip, no rescore, no published data.
  This was the last required fix before owner-authorized W4 go-live.
summary: >
  F3 fix (owner-accepted methodology finding, both D7 signers concur). Guard the insufficient_data gate so a non-material d3_nonmaterial_gap (-5) confidence dent cannot be the term that flips a graded product into insufficient_data. KEEP the -5 magnitude (correctly anchored at half the D5 partial -10); fix the BOUNDARY only: the dent reduces displayed confidence within the graded band but, if removing the d3_nonmaterial_gap term would leave the product at/above the insufficient_data boundary (=40), the product does NOT enter insufficient_data. Makes the engine honor the co-signed promise (confidence dent, never a grade cut) that 3 maadanim currently violate. Behind BARI_GLASSBOX_W4 (OFF byte-identical). Re-validate: 3 maadanim no longer flip; no new grade moves; frozen invariants hold (milk 85/A, snack 70/B); OFF 0-diff. This is the LAST required fix before owner-authorized W4 go-live.
---

# TASK-181M — Prevent non-material confidence dents from independently triggering insufficient_data

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
