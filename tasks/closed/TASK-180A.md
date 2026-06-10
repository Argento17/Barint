---
id: TASK-180A
title: Milk re-baseline — rescore on pinned HEAD baseline + owner sign-off + QA freeze
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
blocker: null
depends_on: []
blocks: []
category_id: null
close_reason: >
  CC close-readiness gate PASS (2026-06-04, all claims verified against artifacts).
  Milk re-baseline COMPLETE and LIVE. Step0: engine pinned as git tag
  engine-baseline-2026-06-04 (f075d9e). Rescore: run_005_headpin, 13/20 reproduction,
  3 grade-affecting moves (1 flip soy D->E + 2 >=2pt same-grade) + 4 cosmetic, top 85/A
  trio HELD (verified per-trace). Owner signed off all 3 moves. QA froze run_005_headpin
  AUTHORITATIVE (run_004 retired to history via SUPERSEDED.md, not deleted). CLAUDE.md
  frozen invariant updated to run_005_headpin. Frontend reshipped milk-comparison.json
  (5 rows moved, soy the only visible grade change; build+lint green; /hashvaot/milk-comparison
  prerendered). RICE EXCEPTION: owner chose (2026-06-04) to KEEP the TASK-169C manual
  override rice=52.3/C over the frozen engine value 49.4/D — documented as a do-not-revert
  override-layer note in run_005_headpin/AUTHORITATIVE.md for future rebuilds. Open Content
  nit (non-blocking): first-ever E grade label rendered as "חלש מאוד" — confirm house-correct.
  Reports: milk_rebaseline_TASK-180A + milk_baseline_freeze_TASK-180A (2026-06-04).
summary: >
  Step1 of TASK-180. Rescore milk (run_004 legacy) on engine-baseline-2026-06-04; reproduce the measured 13/20 drift; classify the 7 misses (1 D->E flip + 2 >=2pt + 4 cosmetic); owner signs off each grade-affecting move; confirm frozen invariant milk top 85/A (whole/4%/goat) HELD; QA freezes the new pinned milk baseline. No reship until signed.
---

# TASK-180A — Milk re-baseline — rescore on pinned HEAD baseline + owner sign-off + QA freeze

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
