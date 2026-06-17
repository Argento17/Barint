---
id: TASK-320
title: Spine step 5 — wire the flip→rescore→copy→gate chain into the Spine DAG runner (incremental skip + lineage)
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-17
depends_on: [TASK-319]
blocks: []
category_id: null
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
