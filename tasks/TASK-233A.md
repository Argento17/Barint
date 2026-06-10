---
id: TASK-233A
title: "Validation gate harness — wire frontend-JSON checks as build-blocking gates (root cause #2)"
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-233]
blocks: []
roadmap_impact: true
work_type: qa-tooling
---

# TASK-233A — Validation gate harness

From the TASK-233 confirmation sweep (`reports/task_233_confirmation_sweep.md`), root cause #2:
the checks already exist conceptually but **none run as a build/pre-ship gate**. Make them
runnable + blocking on the bari-web copy of every shipped comparison JSON.

## Scope (a single runnable validator + CI/pre-commit wiring)
- `is_clean` leak gate (`integrations/clients/hebrew_readability.py`) over **every consumer
  string field** of every shipped JSON (name, insightLine, expansion.*, rowVerdict, bottomLine,
  comparisonContext, signals, limitingFactors, caveats, confidence labels/tooltips).
- `BariProductVM` runtime conformance + **internal-key allowlist** (reject `source_traceability_status`,
  `novaGroup`, `_calibration`, `_cluster`, `_subpool`, `_internal_cluster`, etc.).
- Duplicate-barcode uniqueness on the **final** JSON (not just the QA sample).
- `score` is an integer 0–100.
- **grade == score-derived grade** consistency (the check that does not exist anywhere today; it
  is what let DA-009 drift through).

## DoD
- [ ] One validator runs all checks over all live JSONs; exits non-zero on any failure
- [ ] Wired as a blocking gate (pre-commit and/or `npm run build` step) — not a manual script
- [ ] Extends `run_schema_validation_gate.py` coverage from 4 files to all live files
- [ ] Read-only to data/scores; this task adds checking, not fixes
