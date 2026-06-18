# P45 / TASK-264 — Factory trust layer: property-based engine invariants (Shadow card #2) (route: C1, QA Agent)

CONTEXT: Repo C:\Bari. The factory chain is functionally complete; the trust layer makes it so
the machine can't silently ship a wrong score. Build a **property-based invariant suite** on
the scoring engine, homed in Shadow, that the factory can gate on.

## USE / READ
- Engine: `03_operations/bsip2/proto_v0/src/score_engine.py` (read its real I/O — it scores a
  BSIP1 record → score + grade + dimension_scores + trace). Inspect actual function signatures.
- Shadow home: `03_operations/shadow/` (README, baselines, `shadow_registry_v1.json`) +
  `03_operations/bsip2/proto_v0/src/shadow_backtest.py`. Put the suite here (e.g.
  `03_operations/shadow/engine_invariants.py`), matching Shadow's existing conventions.
- Inputs: synthetic generated records + a sample of REAL BSIP1 records (e.g.
  `02_products/bread_retail_001/bsip1/*.json`). Read-only over real data.

## INVARIANTS TO TEST (derive each from the engine — never assert one it doesn't guarantee)
Implement as property tests (stdlib only — hand-rolled random input generation within valid
nutrition ranges; no hypothesis/new deps):
1. **Bounds** — score within the engine's declared range; grade ∈ the valid grade set; every
   dimension_score within its range.
2. **Determinism** — same BSIP1 input scored twice → byte-identical score + dimension_scores.
3. **Null-safety** — a record missing any nutrition field does NOT crash; the missing field is
   handled per the engine's rule (honest null/absence, NOT silently treated as 0 unless the
   engine's rule explicitly says so — if it does, document that as the engine's choice).
4. **OFF-free** — no scoring path reads Open Food Facts; assert no OFF marker appears in any
   produced trace (TASK-238). Any OFF path = launch blocker.
5. **Grade consistency** — the score→grade mapping is consistent (same score always yields the
   same grade; grade boundaries monotonic).
6. **Monotonicity — ONLY where the engine provably guarantees it.** Where increasing a single
   positively-weighted nutrient (holding others fixed) should not decrease its dimension's
   sub-score, test it. Where the engine does NOT guarantee monotonicity, DO NOT assert it —
   document which relationships are/aren't monotone (a false invariant = false failures).

## DELIVERABLE
- `engine_invariants.py` — the suite, runnable: `python engine_invariants.py` → per-invariant
  PASS/FAIL with counts (N random cases + N real records each).
- Run it. Report results. **If any invariant FAILS on the real engine, that is a real finding —
  report it precisely (input → expected → actual), do NOT paper over it.**
- A one-paragraph note on how this wires into the factory as a gate (the scoring stage can't
  emit a score that violates an invariant).

## GUARDS
- Read-only over the engine + real data — do NOT modify the engine, any score, or any live
  artifact. stdlib only; no new deps. No OFF anywhere. This is a test/verification build, not
  an engine change.

## RETURN BLOCK
The suite path; the run output (per-invariant PASS/FAIL + case counts); any real invariant
violation found (precise repro); which monotonic relationships you could/couldn't assert and
why; the factory-gate wiring note. End with the machine-readable JSON return contract
(`01_framework/operations/return_contract_v1.md`); counts must include
`invariants_implemented`, `invariants_passing`, `invariants_failing`, `random_cases_run`,
`real_records_run`, `off_introduced: 0`, `engine_modified: false`. **Propose RETURNED — do NOT
write CLOSED; the orchestrator verifies and closes.**
