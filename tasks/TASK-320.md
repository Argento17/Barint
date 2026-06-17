---
id: TASK-320
title: Spine step 5 — wire the flip→rescore→copy→gate chain into the Spine DAG runner (incremental skip + lineage)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-319]
blocks: []
category_id: null
close_reason: >
  Data Agent built spine_pipeline.py + spine_flip --via-spine/--force (commit bc68196af). Orchestrator-verified by running:
  runner.py/spine_db.py UNCHANGED (git clean; test_spine.py PASS = backward-compatible); unchanged inputs → all 6 stages
  'skipped' in 0.0s (incremental works); --force → all ran; one config content-change → only that shelf re-ran (skip-invalidation);
  frozen flag (BARI_RECAL_P0=on) → exit 2 hard-stop, 0 stages; 22 lineage rows recorded in spine.db (each page → its 9 engine files
  + config + corpus manifest). SPINE COMPLETE (steps 1-5): a scoring-flag change now flows to a gated, copy-applied, deploy-ready
  bundle via one command, incremental + lineage-recorded, frozen invariants absolute, no auto-deploy.
summary: >
  Final spine step (enhancement; core is complete at step 4). Run spine_flip's per-shelf chain THROUGH the Spine DAG runner
  (03_operations/spine/runner.py Stage/run_pipeline + spine_db.py) so re-runs are content-hashed + SKIPPED when inputs are
  unchanged (incremental/resume) and lineage (engine/config/corpus → staged page → gate report) is recorded automatically into
  spine.db. Per affected shelf declare Stages: rescore (inputs = 9 engine source files + config + corpus marker → output staged
  page) → copy (inputs = staged page + baseline_json → outputs copy-applied page + author_set) → gate (input = page → output gate
  report). Frozen gate still runs BEFORE the pipeline (no stages on a frozen breach). Acceptance: run once (stages 'ran'), run
  again unchanged (stages 'skipped'), and a spine.db lineage query shows the flag-run → page edges. spine.db is gitignored
  generated state. NO engine/score/page edits; NO push/deploy. Route Data Agent (owns Spine).
---

# TASK-320 — Spine step 5: DAG runner + lineage integration

See `tasks/prompts/P170_spine_dag_lineage.md`. Completes the spine: the flip flow becomes incremental + self-recording in the
datastore. Enhancement over the working step-4 core.
