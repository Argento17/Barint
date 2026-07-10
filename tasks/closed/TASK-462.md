---
id: TASK-462
title: CI green sweep: fix 3 failing Barint checks (python-tests fixture path, off-sweep literal marker, ESLint) + delete dead-repo workflow
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-02
closed_at: 2026-07-02
close_reason: >
  Merged via PR #43 (merge 6284546a); master push CI run "CI — Barint" = SUCCESS (verified via
  Actions API) — first honest green on master; dead argento_bari_ci.yml workflow removed. Four onion
  layers, each orchestrator-verified (C0 PASS on P464/P466/P468/P470/P471 contracts + key gates
  re-run: pytest 31/31, OFF grep clean, lint 0 errors): L1 fixture path + OFF-exclusion-note reword
  (gate grep untouched, field not consumer-rendered) + ESLint 12/12 (Cursor's 2 hydration-mismatch
  refactors caught in verification and reworked to SSR-safe pattern); L2 enricher paths 64/64 +
  validate-corpus CI switched to its own documented dev-mode policy (validator unweakened); L3 four
  C:\Bari literals purged from CI-invoked paths incl. import graph; L4 bsip0_gate.py import-time
  stdout-rewrap guarded + gate step on native runner (30/30). Backlog routed: 972-warning corpus
  copy debt (owner freeze), router-regression "1 failures at exit 0" tolerance → TASK-453.
depends_on: []
blocks: []
category_id: null
summary: >
  PR #37 + every master push show red CI: (1) test_bsip0_nutrition.py hardcodes C:\Bari fixture path (fixture IS in repo, repo-relative fixes it); (2) off-sweep greps a historical OFF-exclusion NOTE in granola_frontend_v2.json _meta (reword note, keep gate at full strength); (3) npm run lint fails on pre-existing errors; (4) argento_bari_ci.yml targets dead standalone layout - delete. Checks are advisory (no branch protection) but permanently-red CI trains owner to ignore it.
---

# TASK-462 — CI green sweep: fix 3 failing Barint checks (python-tests fixture path, off-sweep literal marker, ESLint) + delete dead-repo workflow

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
