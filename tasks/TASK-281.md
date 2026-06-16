---
id: TASK-281
title: PHVO/hardened-fat matching robustness: scope to parsed ingredient list + handle negation
owner: nutrition-agent
status: BLOCKED
priority: HIGH
created_at: 2026-06-14
blocker: "tripwire-1 scoring change: needs Nutrition+Product D7 + rescore/bleed gate; route after the Bari-wide red-label project or as a standalone gated fix"
depends_on: []
blocks: []
category_id: null
summary: >
  _PHVO_MARKERS does naive substring match on full text incl. marketing/negation; false-fired has_phvo on a product whose label said margarine was REMOVED ('יצאו מהתהליך'). Fix: match only within the parsed ingredient list, and skip markers in negation context (יצאו/הוצא/ללא/נטול). Found in cookies run_005 (TASK-275). Score-moving -> full gate.
---

# TASK-281 — PHVO/hardened-fat matching robustness: scope to parsed ingredient list + handle negation

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
