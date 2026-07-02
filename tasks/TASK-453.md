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

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
