---
id: TASK-601
title: BSIP0 MUST workstream: capture provenance manifest + replay-everything harness (STF-converged prerequisite)
owner: data-agent
status: BLOCKED
blocker: owner go/no-go on the BSIP0 enhancement program start (STF memo 2026-07-11); do NOT dispatch until approved
priority: MEDIUM
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  STF memo 2026-07-11 (TASK-598 debate) converged: the prerequisite for all BSIP0 integrity work is (a) a capture provenance manifest (authoritative membership + dedup over the 2,321 raw-source objects in 104 containers - the '893 corpus' is not reproducible) then (b) a replay-everything harness that re-parses every manifest capture and diffs vs a committed baseline (Shadow1 pattern). Until replay exists, no integrity check can be quantified (probe returned parsed_nutrition_candidates=0). PROGRAM START - owner go/no-go required before dispatch (not a routine task). Downstream SHOULD/LATER items ranked in the memo. Do NOT start until owner approves.
---

# TASK-601 — BSIP0 MUST workstream: capture provenance manifest + replay-everything harness (STF-converged prerequisite)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
