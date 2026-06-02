---
id: TASK-168D
title: Phase 2 pilot QA — verify maadanim line rewrite (gates + no score drift + build)
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "QA gate: 3/4 PASS clean + 1 conditional now resolved. Gate1 scope (git diff 84/84 insertions all insightLine, 0 drift on score/grade/expansion/nutrition/signals by id) PASS. Gate2 publish (length/grade-ban/wellness) 0 fails PASS. Gate3 trace-anchor: clean on all flagged risks (6 sugar-null, diet cups, boilerplate puddings, sodium artifacts) except 2 lines rounding protein 8.7->9 -> CC fixed both to 8.7 (re-verified 41/49 chars, in-gate, diff still insightLine-only). Gate4 build tsc+next build exit 0, 34 routes. Advisory: 'סויה ביו 16 רכיבים' integer not cleanly countable from nested ingredient string — flagged for the rollout's counting convention, not a pilot blocker."
depends_on: [TASK-168C]
blocks: []
category_id: null
summary: >
  Verify every rewritten maadanim line passes the publish gates (35-80 chars, no grade-restatement tokens, leads-with-driver, trace-anchored/no fabrication vs the product's own data) AND that score/grade/all non-insightLine fields are byte-identical to HEAD; tsc/build clean.
---

# TASK-168D — Phase 2 pilot QA — verify maadanim line rewrite (gates + no score drift + build)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
