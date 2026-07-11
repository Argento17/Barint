---
id: TASK-552
title: Scoring-engine ledger gap: score_after_cap - penalty != score_after_penalty (~4pt unlogged step; #37 7290102399802, likely systemic)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-09
closed_at: 2026-07-11
close_reason: >
  Diagnosis complete and orchestrator-verified (read-only; no score changed, none proposed to change).
  ROOT CAUSE: legitimate engine step, serialization omission - score_engine.py:3959 subtracts
  polyol_penalty + emul_comp_penalty (ECS-v1/EV-045) but trace_writer.py assemble_trace() penalty
  block (verified lines ~78-95) never serializes those fields. Seed product 7290102399802:
  62.89 - 2.0 - 4.0(emul: modified_starch w3 + pectin w1) = 56.89, matches trace; orchestrator
  reproduced on v1/v2/v3 run dirs. SYSTEMIC CENSUS independently re-run by orchestrator, exact match:
  5747 traces scanned, 1165 gap (20.3%) = 1146 negative (this omission class) + 19 positive (hummus
  EV-094 floor pre-RT-10, distinct class); 0/5747 traces carry emulsifier_complexity_penalty.
  Independent of TASK-563 (that was run_id/frontend mismatch; its seeds had emul=0). C0 PASS exit 0.
  Report: 03_operations/reports/nutrition/task552_ledger_gap_diagnosis_v1.md.
  FIX registered same-cycle as TASK-592 (forward-only trace-completeness fix + selftest; backfill of
  existing traces deliberately excluded - TASK-563 owner-decision territory).
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
