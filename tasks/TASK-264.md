---
id: TASK-264
title: Factory trust layer: property-based engine invariants (Shadow card #2)
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
closed_at: 2026-06-13
depends_on: [TASK-263]
blocks: []
category_id: null
close_reason: >
  P45 delivered 03_operations/shadow/engine_invariants.py — a property-based invariant suite on
  score_engine.py. Orchestrator-verified: independent re-run → 6/6 PASS (I1 bounds, I2
  determinism, I3 null-safety, I4 OFF-free, I5 grade-consistency, I6 monotonicity), 342 cases
  (300 synthetic + 42 real bread BSIP1), exit 0. Monotonicity discipline correct — asserted only
  the 3 relationships the engine provably guarantees (satiety∝protein, fermentation bonus≥0,
  protein-scale non-decreasing) and explicitly did NOT assert non-monotone ones (calorie_density
  decreases in kcal, glycemic decreases in sugar, caps are discontinuous, composite non-monotone
  by design) — no false invariants. Engine unmodified by P45 (its only artifact is the suite; the
  M on score_engine.py is a pre-existing session-start change). Wires into the factory as the
  scoring-stage gate (halt before writing an out-of-bounds/non-deterministic/OFF/crashing score);
  complements Shadow backtest (regressions) with per-record contracts. Trust layer 4a complete.
summary: >
  Property-based invariant suite on score_engine.py homed in Shadow: bounds (0-100), determinism, null-safety, OFF-free path, score->grade consistency, monotonicity where provable. Run on synthetic + sample real BSIP1; report violations. Gate so the factory cannot ship an invariant-violating score. stdlib only.
---

# TASK-264 — Factory trust layer: property-based engine invariants (Shadow card #2)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
