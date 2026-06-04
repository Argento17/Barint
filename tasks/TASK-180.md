---
id: TASK-180
title: Legacy engine re-baseline — execute TASK-178 plan (pin HEAD baseline; milk→snack→bread rescore w/ per-invariant owner sign-off + QA freeze)
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-04
depends_on: []
blocks: []
category_id: null
drift_ack: "Closure-drift false-positive: the return-header regex (TASK-\\d+) collapses sub-task headers **Task:** TASK-180A → TASK-180. The milk re-baseline deliverables are authored by 180A (CLOSED); the umbrella is legitimately IN_PROGRESS (snack 180B + bread 180C waves not yet run). Same pattern as TASK-169/179."
summary: >
  Owner approved 2026-06-04 (executes the TASK-178 audit re-baseline plan). The engine drifted unflagged since the May freezes; legacy pages render scores HEAD can't reproduce, so a naive rebuild would silently move grades (bread alone 3 A->~11 A from drift). Sequence: Step0 pin HEAD as engine-baseline-2026-06-04 -> milk (180A) -> snack (180B) -> bread (180C, folds in the 4 TASK-169F recal B->A moves), each rescored on the pinned baseline with per-invariant owner sign-off + QA freeze. No score ships without owner sign-off per wave.
---

# TASK-180 — Legacy engine re-baseline — execute TASK-178 plan (pin HEAD baseline; milk→snack→bread rescore w/ per-invariant owner sign-off + QA freeze)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
