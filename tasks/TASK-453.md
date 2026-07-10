---
id: TASK-453
title: Gate-liveness sweep — verify every Bari gate is actually wired + fires (not decorative)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  Pattern found this session: multiple safety/quality gates are believed-active but dead/degraded (off_sweep stale [fixed TASK-450], verify_citations source lost [restored TASK-452], Stage-9 red-team + inversion/monotonicity invariants not auto-wired into run_gates, web QA a11y/perf/visual + Lighthouse not in CI). Restoring ONE dead gate (452) immediately caught 4 real citation defects. SWEEP: enumerate every gate Bari believes it has (C0 return-contract/validate_return, G1-G8 run_gates, two-gate content sign-off, conformance, Stage-9 red_team + invariants, CI barint_ci.yml, off_sweep, verify_citations) and for EACH prove WIRED+FIRES with a test that it fails when it should. Rank dead/degraded ones by risk; propose fixes. Read-only audit first.
---

# TASK-453 — Gate-liveness sweep — verify every Bari gate is actually wired + fires (not decorative)

## Backlog items routed here (orchestrator)
- 2026-07-03 (unattended pass) **run_gates.py CRASH on string-typed `consumerExplanation`:**
  `_collect_consumer_strings` (~run_gates.py:939-941) calls `.get()` without an `isinstance(ce, dict)`
  guard → `AttributeError` on the LIVE granola baseline (7 products carry string-typed
  consumerExplanation at origin/master). Found during TASK-461 granola handover execution; gate
  parity for that category was proven via a patched local workaround (identical crash on baseline
  and candidate, patched run = PASS on both; see `tasks/returns/TASK-461_exec_B_report.md`).
  Fix: guard + decide whether string-typed consumerExplanation is itself a schema defect (G1 should
  catch it, not crash on it). Also means run_gates G-gates have been silently un-runnable on granola.
- (Pre-existing, recorded elsewhere on the board): run_router_regression.py never exits nonzero on
  corpus failures; hebrew_readability תנובה/'נובה' false positive; no gate audits numeric claims in
  TS-adapter prose.
