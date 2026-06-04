---
id: TASK-180C
title: Bread re-baseline — rescore on pinned baseline, fold in TASK-169F 4 recal moves, owner sign-off + QA freeze + reship
owner: data-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-04
blocker: "Sequential: LAST — after 180A+180B signed + frozen. Rescore bread on the pinned baseline; separate pre-existing +6/+8 drift (83 grade-affecting) from the 4 recal-intended B->A (TASK-169F); owner signs off A-ceiling + shelf-compression; decide fate of the lechem-calibration layer; QA freeze + reship bread frontend JSON only if approved."
depends_on: [TASK-169F]
blocks: []
category_id: null
summary: >
  Step3 (final) of TASK-180. Rescore bread (real_bread_retail_003_v1) on engine-baseline-2026-06-04. Bread is the worst-affected legacy page (165/256, 83 upward grade drifts). Separate pre-existing drift from the 4 TASK-169F recal B->A moves; owner per-move sign-off on A-ceiling + shelf-compression; QA freeze; reship bread frontend JSON only if owner approves. Frozen provenance untouched.
---

# TASK-180C — Bread re-baseline — rescore on pinned baseline, fold in TASK-169F 4 recal moves, owner sign-off + QA freeze + reship

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
