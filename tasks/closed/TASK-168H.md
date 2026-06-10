---
id: TASK-168H
title: Rollout verdicts — cheese
owner: content-agent
status: CLOSED
priority: HIGH
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "51 cheese verdicts rewritten to v2 model, insightLine-only (QA 51/51), no quoted ingredients (withheld), sodium/sat-fat framed as OUTSIDE the score (high!=healthy). Nutrition: 1 false protein (che-7290011499624 4.3->5.5) fixed by CC. OPEN governance item: sat-fat cited on 25 cheese + 2 yogurt lines is TRUE (from traces) + well-framed but not in displayed nutrition block / off current guide -> owner decision (surface satFat vs amend guide). Live + tsc clean."
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
summary: >
  Rewrite all insightLine in cheese_frontend_v1.json to verdict model (standard v2 + grounding §3). Sodium/sat-fat are OUTSIDE the score — high score != healthy; ingredient string withheld (use signals).
---

# TASK-168H — Rollout verdicts — cheese

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
