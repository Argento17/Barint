---
id: TASK-156
title: Live /hashvaot comparison-page QA audit (all 8 pages) — route to loader to JSON to render precedence; CONDITIONAL PASS
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — diagnostic deliverable; its findings independently confirmed by verifying the spawned fixes against artifacts. (1) HARD FAIL (homepage hummus card false 'five A / 47-pt') was real and is now fixed + verified — featured-hummus-intelligence-card.tsx:42-50 derives aGradeCount/scoreGap; live hummus_frontend_v3.json shows 0 grade-A and top77-bottom60=gap17 over the 35 displayed spreads (TASK-158). (2) 'no description' concern correctly diagnosed as 5 excluded JSON records + cache, not a live render gap. (3) Warnings all actioned: yogurt 11/11 imageUrl now populated, orphan JSONs archived, _meta corrected (TASK-160); cheese index-card photo wired (TASK-159); snk-006 image confirmed genuinely unrecoverable -> BLOCKED follow-up TASK-160A. Read-only audit; no artifact mutated by this task itself."
roadmap_impact: false
depends_on: []
blocks: [TASK-157, TASK-158, TASK-159, TASK-160]
category_id: null
summary: >
  Full read-only audit of all 8 live /hashvaot comparison pages tracing route->loader->JSON->render. Verdict CONDITIONAL PASS. Findings: no live product renders without a description (the concern = 5 excluded JSON records + cache); 1 HARD FAIL (homepage hummus card false 5 A's / 47-pt gap); warnings (yogurt 0/11 images, snk-006 no image, 3 orphaned JSONs, 2 stale _meta counts). Spawned TASK-157/158/159/160 to fix.
---

# TASK-156 — Live /hashvaot comparison-page QA audit (all 8 pages) — route to loader to JSON to render precedence; CONDITIONAL PASS

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
