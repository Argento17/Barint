**Task:** TASK-179G

# Glass Box D5/D6 — Proof A: FLAG-OFF Byte-Identical (the hard gate)

**Date:** 2026-06-04 · **Author:** Data Agent · **Flag:** `BARI_GLASSBOX_D5D6` (default OFF)
**Result: PASS — 0-diff on all 342 products across golden + the 3 frozen corpora.**

---

## 1. What this proves

With `BARI_GLASSBOX_D5D6=off`, the engine output is **byte-identical** to the pre-change
engine — same discipline as `BARI_RECAL_P0` (`verify_recal_off_identical.py`). The hard
contract (spec §2.4, §4; EV-039): OFF executes none of §2.1/§2.2 — the D5 detector is not
invoked, the D5 confidence-reduction term is skipped, the gate state machine is not entered,
and **no Glass Box keys are added to the result dict** — so the current ceiling /
`insufficient_data` code path runs verbatim.

## 2. Method (correct anchor)

`score_product()` is the **single** function modified by this change. An OFF-identical
result there guarantees every downstream consumer (bread synthesis, trace writers, frontend
packagers) is unaffected. The proof captures the **full `score_product` result dict** for
every product through the standard pipeline with the *unmodified* engine (baseline
snapshot, taken before any edit), then re-runs with the flag OFF after the edit and asserts
deep stable-JSON equality on the entire dict (`sort_keys`, every key compared).

Harness: `src/verify_glassbox_off_identical.py` (`snapshot` then `check`).
Baseline: `reports/glass_box/_off_baseline.json`.

> **Why a self-baseline, not the published traces.** The published frozen traces are NOT a
> clean byte-identical anchor for the *current* engine: `run_004_recalibrated` was generated
> with `BARI_RECAL_P0=on` (run_004 IS the recalibrated milk run — top still 85/A), and
> `run_snack_bars_001` predates sprint1/TASK-133 engine changes (41 deltas vs the current
> engine OFF, all pre-existing and unrelated to Glass Box; snk-001 ceiling still 70/B). "OFF
> must be byte-identical to today" means *to the current engine* — which the self-baseline
> isolates exactly. We verified the milk OFF-vs-published deltas vanish when RECAL_P0 is
> re-enabled, proving they are RECAL, not Glass Box.

## 3. Result

```
check golden_milk  n=  20 diffs=0      (frozen: milk run_004 lineage; top 85/A preserved)
check snack_bars   n=  53 diffs=0      (frozen: snk-001 = 70/B ceiling preserved)
check hummus       n=  69 diffs=0      (pilot)
check maadanim     n= 200 diffs=0      (pilot)

FLAG-OFF BYTE-IDENTICAL: PASS (0-diff)
```

- **Golden corpus regression** (`run_regression_check.py`, flag OFF): PASS — no FAIL,
  1 pre-existing WARN (unrelated to this change). The golden anchors are engine-agnostic
  (read published traces) and are unmoved.
- **Frozen invariants:** milk top = **85/A** (unchanged under OFF); snack-bar B ceiling =
  **70/B** (unchanged under OFF). No frozen score moved.

## 4. Verdict

**PASS.** Flag OFF is byte-identical to today across all golden + frozen + pilot products
(342 total, 0 diffs). The wiring is correct: all D5/D6 additions are additive and guarded by
`GLASSBOX_D5D6_ON`; the existing ceiling/`insufficient_data` path is the fall-through.
Rollback = unset the flag (no code revert).
