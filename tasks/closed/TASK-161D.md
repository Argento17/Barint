---
id: TASK-161D
title: Verify row-format parity across all comparison pages + build/regression
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — QA Checks 1/2/3/5 PASS: row parity (+/- rowReason wins over insightLine, comparison-row.tsx:119-129), metric bars per 161A decision, 0 products fall to insightLine fallback (every row has >=1 signal), tsc/lint/build(34 routes)/corpus-validate all exit 0, zero NEW regressions. QA Check-4 'FAIL' is NOT a 161 defect — QA confirmed '161 display change is verifiably score-neutral' (bread/snacks byte-identical to HEAD); the score deltas it flags (hummus 58 / maadanim 70 / yogurts 11) are co-resident OTHER-task rescores in the uncommitted tree (TASK-149/150 shipped+approved; TASK-143 yogurts). That is a commit-bundle decision for the owner (holding on commit), tracked on TASK-160 — not a row-format regression."
depends_on: [TASK-161C, TASK-161E]
blocks: []
category_id: null
summary: >
  Confirm every comparison row renders +/- rowReason + metric bar matching hummus; no insightLine fallbacks remain where signals exist; scores unchanged; tsc/next build/corpus-validate clean.
---

# TASK-161D — Verify row-format parity across all comparison pages + build/regression

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
