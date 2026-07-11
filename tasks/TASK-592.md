---
id: TASK-592
title: Fix trace ledger completeness: trace_writer must serialize emulsifier_complexity_penalty + polyol_penalty (+ completeness selftest)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-552 diagnosis (verified 2026-07-11): score_engine.py:3959 subtracts polyol_penalty + emul_comp_penalty but trace_writer.py assemble_trace() never serializes them - 1165/5747 traces (20.3%) carry an unexplained ledger gap (1146 negative = emul/polyol omission; 19 positive = EV-094 hummus floor pre-RT-10, distinct class). Fix: add the missing penalty fields to the trace penalty block + a completeness selftest asserting engine-result penalty keys are a subset of trace keys (prevents the class, not the instance). FORWARD-ONLY: applies to future runs; do NOT regenerate existing traces of published shelves (TASK-563 territory, owner-adjacent). No scoring logic change, no score movement, no D7 needed per diagnosis report 03_operations/reports/nutrition/task552_ledger_gap_diagnosis_v1.md.
---

# TASK-592 — Fix trace ledger completeness: trace_writer must serialize emulsifier_complexity_penalty + polyol_penalty (+ completeness selftest)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
