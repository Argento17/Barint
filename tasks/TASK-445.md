---
id: TASK-445
title: Golden-page copy cleanup + G6 Hebrew leakage coverage: brined has pre-existing Hebrew framework tokens (מדד עיבוד/תקרת עיבוד) G6 can't catch; add Hebrew patterns to run_gates.py G6
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Adversarial QA found (pre-existing, not a re-flow regression): brined golden page has 'מדד עיבוד'/'תקרת עיבוד' (processing metric/ceiling) framework leakage in 7 places/4 products; 'נקי ופשוט' convention on preservative-containing lists (11); bc-004 'lowest sodium' should be 'tied for lowest'. Also: run_gates.py G6 FRAMEWORK_LEAKAGE_PATTERNS is English-only -> add Hebrew coverage.
---

# TASK-445 — Golden-page copy cleanup + G6 Hebrew leakage coverage: brined has pre-existing Hebrew framework tokens (מדד עיבוד/תקרת עיבוד) G6 can't catch; add Hebrew patterns to run_gates.py G6

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
