---
id: TASK-180
title: Legacy engine re-baseline — execute TASK-178 plan (pin HEAD baseline; milk→snack→bread rescore w/ per-invariant owner sign-off + QA freeze)
owner: qa-agent
status: CLOSED
priority: LOW
created_at: 2026-06-04
completed_at: 2026-06-05
cc_reviewed: "2026-06-05"
depends_on: []
blocks: []
category_id: null
close_reason: >-
  CC close-readiness gate PASS (2026-06-05). All three re-baseline waves complete and shipped:
  (1) TASK-180A MILK — run_005_headpin LIVE, top 85/A held, soy D→E owner-signed, cc_reviewed
  2026-06-04. (2) TASK-180B SNACKS — run_snackbars_007_headpin LIVE, zero grade-affecting moves,
  no-A invariant held, 11 cosmetic updates shipped, cc_reviewed 2026-06-05. (3) TASK-180C BREAD —
  run_bread_008_headpin LIVE, 13 grade-affecting moves owner-signed (7 B→A, 5 C→B, 1 A→B resolved
  by recal), TASK-169F obligation discharged, calibration layer retired, cc_reviewed 2026-06-05.
  Engine tag engine-baseline-2026-06-04 (f075d9e) is the pinned HEAD baseline across all three
  categories. TASK-180 umbrella complete per TASK-180C CC close record.
drift_ack: "Closure-drift false-positive: the return-header regex (TASK-\\d+) collapses sub-task headers **Task:** TASK-180A → TASK-180. The milk re-baseline deliverables are authored by 180A (CLOSED); the umbrella is legitimately IN_PROGRESS (snack 180B + bread 180C waves not yet run). Same pattern as TASK-169/179."
summary: >
  Owner approved 2026-06-04 (executes the TASK-178 audit re-baseline plan). The engine drifted unflagged since the May freezes; legacy pages render scores HEAD can't reproduce, so a naive rebuild would silently move grades (bread alone 3 A->~11 A from drift). Sequence: Step0 pin HEAD as engine-baseline-2026-06-04 -> milk (180A) -> snack (180B) -> bread (180C, folds in the 4 TASK-169F recal B->A moves), each rescored on the pinned baseline with per-invariant owner sign-off + QA freeze. No score ships without owner sign-off per wave.
---

# TASK-180 — Legacy engine re-baseline — execute TASK-178 plan (pin HEAD baseline; milk→snack→bread rescore w/ per-invariant owner sign-off + QA freeze)

## CC Close Record (2026-06-05)

**Close-readiness gate: PASSED**

All three sub-task waves independently closed with CC verification:

| Wave | Status | Engine run | Grade moves | Invariants |
|---|---|---|---|---|
| 180A — Milk | CLOSED 2026-06-04 | run_005_headpin | 1 D→E (soy), 2 cosmetic | 85/A top held |
| 180B — Snack bars | CLOSED 2026-06-05 | run_snackbars_007_headpin | 0 grade moves | 70/B ceiling held; no-A held |
| 180C — Bread | CLOSED 2026-06-05 | run_bread_008_headpin | 13 grade moves (7 B→A, 5 C→B, 1 A→B recal-resolved) | TASK-169F discharged; calibration retired |

Engine baseline: `engine-baseline-2026-06-04` (f075d9e) — frozen across all three categories.

**Status: CLOSED** (by CC Agent, delegated closing authority 2026-06-02)
