---
id: TASK-601
title: BSIP0 MUST workstream: capture provenance manifest + replay-everything harness (STF-converged prerequisite)
owner: data-agent
status: CLOSED
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

## CLOSED (orchestrator, 2026-07-11) — census delivered, Speed-1 merged
BUILD-HEAVY Codex terra. Orchestrator verified: C0 PASS; every census figure independently
re-derived from the manifest/baseline (893 total → 807 canonical / 86 superseded, 652 GTINs;
replay 8070 rows, 38 flagged = 37 comma_ambiguous + 1 out_of_bound); `--check` regression gate exit 0
against its own baseline; write-boundary clean (only manifest/ + census + return). Speed-1 internal
merge origin/master 92cf5acb → f6c5206d (--check green in merge worktree). Artifacts:
03_operations/bsip0/manifest/{build_manifest.py, replay_harness.py, build_census.py,
capture_manifest.json, replay_baseline.jsonl}; census 03_operations/reports/task601_bsip0_census.md.
KEY RESULT (owner's gap question): 359/757 served products HAVE a canonical capture, 398/757 do NOT
(bread, both cheese files, chocolates, juices, milk, yogurt-drinks, most yogurt-spoonable = 0 capture).
Parser-ambiguity is RARE (38/8070 rows). The "893" denominator Sol couldn't reproduce IS real — it
needed the manifest's membership+dedup (Sol had counted 2,321 undeduped objects). Regression baseline
now guards every future parser/capture change (Shadow1 pattern).
