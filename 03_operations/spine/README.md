# Project Spine1 — Pipeline Datastore + Lean DAG Runner

**Task:** TASK-252 · **Mandate:** owner, 2026-06-11 ("start this project right now … you have my mandate")
**Concept:** `01_framework/operations/comparison_chain_tech_leaps_v1.html`, leaps 7 + 8 ("The Spine" tier)

## Mission

Replace JSON-file archaeology and bespoke per-category scripts with:

1. **One queryable datastore** — runs, products, scores, artifacts, lineage, live_state as
   real tables. "What changed between run 5 and 6?", "which scrape produced this live
   score?", and the live-state manifest become one-line SQL queries.
2. **A lean DAG runner** — stages declare what they read and write; the runner orders them,
   content-hashes everything, skips what hasn't changed (resume/incremental), and records
   lineage automatically. The factory artifacts stop being a checklist item because they
   *are* the pipeline's edges.

## Hard guards (Phase 1)

- **Read-only over the pipeline.** Spine hashes and records existing artifacts; it never
  modifies one. No score changes, no methodology changes, no consumer-facing changes.
- `spine.db` is **generated state** (gitignored, rebuildable from `python ingest.py`);
  `schema.sql` is the law.
- **Zero new dependencies** — stdlib `sqlite3` only. The schema stays portable so a later
  DuckDB/Postgres move is a port, not a rewrite.

## Files

| File | Role |
|---|---|
| `schema.sql` | Datastore schema v1 — 7 tables (runs, products, scores, artifacts, lineage, live_state, stage_runs) |
| `spine_db.py` | Connection + init, file hashing, artifact/lineage recording |
| `ingest.py` | Read-only sweep: BSIP2 trace runs → scores+lineage; frontend JSONs → live_state; run summaries |
| `runner.py` | `Stage` + `run_pipeline`: toposort, signature-based skip, output contract, lineage |
| `test_spine.py` | Pytest suite — 9 tests (runner semantics + ingest on fixtures) |

## Usage

```powershell
cd C:\Bari\03_operations\spine
python -m pytest test_spine.py -v     # test suite
python ingest.py                      # full read-only sweep -> spine.db
```

Example queries against `spine.db`:

```sql
-- live-state manifest (gap-analysis ADD-2):
SELECT data_file, version, run_id, product_count FROM live_state;

-- grade distribution of any run, reconstructed from traces:
SELECT grade, COUNT(*) FROM scores WHERE run_id='run_yogurt_006' GROUP BY grade;

-- lineage: which BSIP1 record produced this trace?
SELECT parent_path FROM lineage WHERE child_path LIKE '%<product>%bsip2_trace.json';
```

Declaring a pipeline (Phase 2 shape):

```python
from runner import Stage, run_pipeline

stages = [
    Stage("bsip1_build", build_fn, inputs=[raw_scrape], outputs=[bsip1_out]),
    Stage("bsip2_score", score_fn, inputs=[bsip1_out],  outputs=[trace_dir_index]),
    Stage("frontend",    pack_fn,  inputs=[trace_dir_index, copy_doc], outputs=[frontend_json]),
]
run_pipeline(stages)   # second run with unchanged inputs: all skipped
```

## Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Datastore + runner core + read-only ingestion, proven on real run data | **delivered** |
| 2 | Wrap the yogurts pipeline (BSIP1 → BSIP2 → frontend) as declared stages | open |
| 3 | Live-state manifest + post-deploy smoke test fed from the datastore | open |
| 4 | Migrate remaining category generators (converges with TASK-233F) | open |
