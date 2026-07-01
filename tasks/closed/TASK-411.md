---
id: TASK-411
title: Drill-down conformance: strip deep-dive narrative from cheese/bread/cakes to match golden standard
owner: frontend-agent
status: CLOSED
close_reason: >
  Deployed to origin/master 723675852 (push 646da02c9..723675852) 2026-06-26.
  Drill-down deep-dive narrative (5 fields) stripped from cheese(48)/bread(29)/cakes(63)
  to match golden standard. Verified: data-only, scores/grades/signals/verdicts byte-identical
  vs origin/master (orchestrator re-check), 0 residuals. Adversarial-QA render gate Track V PASS
  / Track C 0 CRITICAL 0 HIGH (narrative gone in real DOM, no double label, build exit 0, 3 routes 200).
priority: HIGH
created_at: 2026-06-26
depends_on: []
blocks: []
category_id: null
summary: >
  Drill-down conformance: strip deep-dive narrative from cheese/bread/cakes to match golden standard
---

# TASK-411 — Drill-down conformance: strip deep-dive narrative from cheese/bread/cakes to match golden standard

## Context
Owner reviewed the live cheese/bread product drill-downs (post TASK-409/410 deploy) and flagged
them off-standard; juices conforms. Root cause: cheese/bread/cakes carry a second "deep-dive"
narrative block (`consumerExplanation`/whyRated/good/watchOut/context, `bestUseCases`,
`consumerTakeaway`, `bariInterpretation`, `bottomLine`) that the golden reference
(brined-cheeses) and 6 live categories (incl. juices) do NOT carry — causing "מה עובד לטובת
המוצר?" to render twice. Owner approved "strip to match golden" (AskUserQuestion 2026-06-26).

## Deliverable (DONE — awaiting owner-gated deploy)
- Stripped the 5 deep-dive fields from every product in cheese_frontend_v4 (48),
  bread_frontend_v3 (29), cakes_hard_cookies_frontend_v1 (63). Standard block
  (+/− assessment, rowVerdict, shelf-context, nutrition, ingredients) retained.
- Deterministic script: `03_operations/page_generator/strip_deepdive.py`.
- INVARIANT (independently re-verified by orchestrator vs origin/master HEAD): only the 5 keys
  removed; score/grade/positiveSignals/limitingFactors/rowVerdict/comparisonContext/nutrition/
  ingredients/imageUrl byte-identical; product counts unchanged. 0 deep-dive residuals.
- Adversarial-QA render gate (drillqa): Track V PASS (narrative gone in real DOM, no double
  label, build exit 0, 3 routes HTTP 200), Track C 0 CRITICAL / 0 HIGH / 1 MEDIUM (the
  MEDIUM = inert `bottomLine`, now also stripped).
- Worktree `task411-drillstrip` (off origin/master 646da02c9), commit `723675852`. NOT pushed.

## Remaining
- Owner-gated deploy: `git push <worktree> 723675852:master` (consumer-facing — hard stop).
- After deploy: close + clean up worktree.
