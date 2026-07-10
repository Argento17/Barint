---
id: TASK-537
title: Pre-existing WCAG AA contrast failures on comparison pages (found during TASK-534 Design pass)
owner: frontend-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Design Agent axe-core scan (2026-07-08) found two real serious contrast violations, both PRE-EXISTING and independent of the blendWhite diff (proven via control-page parity): (1) SITE-WIDE: category eyebrow label #4ca588 on white = 2.98:1 (floor 4.5:1), present on hummus control too, so template-level not yogurt-specific; (2) yogurt/yogurt-drinks insight-tag pills #7a817c on #f7f7f2 = 3.71:1, 11 nodes each. Fix the token(s) to clear 4.5:1. Evidence: scratchpad/design_t534/ geometry.json + axe output. Also consider adding these routes to e2e/a11y.spec.ts.
---

# TASK-537 — Pre-existing WCAG AA contrast failures on comparison pages (found during TASK-534 Design pass)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
