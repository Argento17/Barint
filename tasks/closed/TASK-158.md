---
id: TASK-158
title: Fix homepage hummus featured-card hard-fail — false 'five A / 47-pt gap' lines now data-derived (0 grade-A, gap 17)
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
completed_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC close-gate PASS — fix verified against the live artifact + data, not the return prose. featured-hummus-intelligence-card.tsx no longer contains the literal 'חמישה מוצרים בציון A' or '47'; the A-grade line (:42-45) and gap line (:47-50) derive from aGradeCount + (topScore-bottomScore) over the displayed shelf, and the fat line is the 4th insight line (:56). Real numbers confirmed by recomputing from hummus_frontend_v3.json under the exact loader exclusion sets: 35 displayed spreads, 0 grade-A, top 77 / bottom 60 / gap 17 — matches what the card renders. No score touched (display-only). tsc/lint/build reported green."
roadmap_impact: false
depends_on: [TASK-156]
blocks: []
category_id: hummus
summary: >
  Corrected the QA hard-fail in featured-hummus-intelligence-card.tsx: the false 'חמישה מוצרים בציון A' and '47' lines are now DYNAMIC (aGradeCount + real top-bottom gap), plus a third contradicting fat line fixed. Verified real numbers: 0 grade-A, gap 17. tsc/lint/next build green.
---

# TASK-158 — Fix homepage hummus featured-card hard-fail — false 'five A / 47-pt gap' lines now data-derived (0 grade-A, gap 17)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
