---
id: TASK-331
title: G2 COVERAGE: allow documented nutrition nulls (sugar) to PASS instead of requiring 100%
owner: nutrition-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-18
depends_on: [TASK-330]
blocks: []
category_id: null
summary: >
  Spine reaches 7/8 gates; G2 correctly flags 3 SKUs missing a parsed sugar value (cereals 19/20, hummus 55/57). Per missing-data rule, never fabricate. Owner ruling 2026-06-18: relax G2 so DISCLOSED nulls ('data could not be retrieved') PASS rather than requiring 100% coverage — aligns with 'unknown is acceptable; OFF is not'. Nutrition-owned gate change, C3+Nutrition reviewed like the G6 word-boundary fix; scope which nutrition fields are null-allowable vs required. Lets a clean flip reach overall PASS.
---

# TASK-331 — G2 COVERAGE: allow documented nutrition nulls (sugar) to PASS instead of requiring 100%

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
