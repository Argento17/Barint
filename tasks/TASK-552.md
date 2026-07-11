---
id: TASK-552
title: Scoring-engine ledger gap: score_after_cap - penalty != score_after_penalty (~4pt unlogged step; #37 7290102399802, likely systemic)
owner: nutrition-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-09
blocker: null
depends_on: []
blocks: []
category_id: null
summary: >
  Scoring-engine ledger gap: score_after_cap - penalty != score_after_penalty (~4pt unlogged step; #37 7290102399802, likely systemic)
---

# TASK-552 — Scoring-engine ledger gap: score_after_cap - penalty != score_after_penalty (~4pt unlogged step; #37 7290102399802, likely systemic)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Dispatch log
- 2026-07-11 03:xx (unattended orchestrate run) — **un-blocked by question-conversion rule**
  (loop-first, owner directive 2026-07-04): a READ-ONLY diagnosis moves no scores and is fully
  reversible (it is a report); tripwire-1 fires only on a score/philosophy CHANGE, which this
  dispatch explicitly forbids. Reversal condition: owner may discard the report; nothing else
  changes. Dispatched Nutrition Agent (claude-sonnet pin, DOMAIN-JUDGMENT capability, background,
  read-only, two permitted output files: report + return). Any fix remains owner/D6-gated.
