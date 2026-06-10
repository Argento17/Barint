---
id: TASK-168C
title: Phase 2 pilot (maadanim) — rewrite all 84 description lines to the standard
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "Pilot rewrite delivered + QA-verified (TASK-168D). All 84 maadanim insightLine values rewritten to row_description_standard_v1 + grounding_v1: decision-driver-first, 35-80char/<=12word (QA: 0 fails, range 39-51), 0 grade-restatement/wellness tokens, trace-anchored (QA: 0 fabrication — sugar-null cups cite no sugar value, diet cups not called high-protein, implausible sodium artifacts never cited). Leads with the maadanim icon-paradox where apt (מילקי 'הגביע הכי מוכר במדף — חלבון 3 גרם, חמישה מייצבים'; קולגן 'כמות לא מצוינת'->'קולגן 1.5% בתווית — לא אותו חלבון של חלב מלא'). insightLine-only (git: 84/84, 0 non-insightLine drift). 2 protein-rounding lines (8.7->9) caught by QA + fixed by CC to 8.7. No scores changed; tsc/build(34 routes) clean."
summary: >
  Rewrite every maadanim insightLine in maadanim_frontend_v2.json to row_description_standard_v1 + grounding_v1: decision-driver-first, no grade-restate, 35-80 chars, category voice, trace-anchored to each product's real data. insightLine ONLY; no scores/grades/other fields. Pilot before the 5-category rollout.
---

# TASK-168C — Phase 2 pilot (maadanim) — rewrite all 84 description lines to the standard

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
