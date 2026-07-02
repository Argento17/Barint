# P461 / TASK-449 candidate REBUILD — joint-flag protocol, live-baseline only (route: C1-GROK)

## 1. Context — why the P459 candidate is invalid
You are in worktree `C:\bari_wt_t449` (branch `fix/task449-brined-inversion`). Your P459/P460 code commits are verified correct and stay as-is. The candidate artifact is WRONG: the live brined page ships BAKED de-anchored scores (sweep commit `7723c5c4`, merged PR #35) while `BARI_REDLABEL_CONTINUOUS_V1` defaults OFF — your rescore therefore produced pre-sweep scores and the swap reverted 3 live grade-flips (7290108509106, 7290108509755, 369617; orchestrator-verified). Also: every diff/gate in P459 used the STALE `C:\Bari` copy of `brined_cheeses_frontend_v2.json` as baseline. The TRUE live baseline is THIS WORKTREE's copy at `bari-web\src\data\comparisons\brined_cheeses_frontend_v2.json` (origin/master checkout). Never reference `C:\Bari` data files again.

## 2. Objective — rebuild the candidate under the joint-flag protocol
**Step A — reproduction gate (mandatory, before anything else):** with `BARI_REDLABEL_CONTINUOUS_V1=on` and `BARI_FERMENT_MARKER_BRINED_FIX_V1=off`, rescore brined and build a swap candidate from the worktree-live JSON. It must equal worktree-live EXACTLY: 36/36 identical scores AND grades, 0 diffs. This proves the joint run reproduces the published page. If it does not, STOP — write the diff table and return `proposed_status: BLOCKED` (that would mean additional unbaked drift; do not improvise).

**Step B — the real candidate:** with BOTH flags ON (`BARI_REDLABEL_CONTINUOUS_V1=on` + `BARI_FERMENT_MARKER_BRINED_FIX_V1=on`), rescore brined; rebuild the candidate from the worktree-live JSON (swap ONLY score/grade from the ON-ON traces, recompute rank competition-style with stable live-order tiebreak, keep live names/copy/schema); pin 36/36 barcodes. Overwrite `_rescore_staging\brined_cheeses\brined_cheeses_candidate_brinedfix.json` (single canonical candidate path) and regenerate `verification_table.csv` in the same ON-ON state.

**Step C — evidence:**
- Movement table vs WORKTREE-live (the true public impact): barcodes, old→new score/grade, direction. Expect ferment-fix-only movement, downward-only, and the 3 sweep flips PRESERVED (candidate must NOT equal stale-main on those 3).
- Full grade distribution before/after (min/max/median/stdev/histogram/most_common).
- Marker census under ON-ON (how many lose the +8).
- `run_gates.py` on the candidate with `--baseline` = the WORKTREE live file (never C:\Bari). Report all gates.
- Write contract to `tasks\returns\P461_contract.md` (NOT P461_return.md — the router overwrites that path), full Return Contract v1: real sha256s, Rule-5 dist markers inside counts, exit-code semantics noted, counts incl. `sweep_flips_preserved: 3/3`, `reproduction_gate: 36/36 identical (Step A)`. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P461_contract.md --root C:\bari_wt_t449` must exit 0 BEFORE you return. Commit the contract + any tooling-neutral staging notes: `git commit -m "P461: brined candidate rebuilt under joint-flag protocol vs live baseline"`.

## 3. Boundaries
No engine/code changes (flags via env only). No consumer-copy edits (Content redoes gate 1 after you). No push/PR/deploy. `C:\Bari` read-only and NEVER as a data baseline. OFF ban absolute. Leave tree clean (delete stray droppings you create; `_rescore_staging` is gitignored). If anything deviates from spec, BLOCKED honestly.

## 4. Return
Stdout summary: Step A result (0-diff proof), movement count vs live, 3-flip preservation check, gate results, contract path + validator exit 0, commit SHA. End with the same JSON contract.
