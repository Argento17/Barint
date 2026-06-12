---
id: TASK-252
title: "Project Spine1 — pipeline datastore + lean DAG runner (typed/hashed artifacts, lineage, resume)"
owner: orchestrator
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-11
depends_on: []
blocks: []
category_id: null
summary: >
  Owner mandate 2026-06-11 ("start this project right now. Call it Project Spine1.
  you have my mandate."). Tech-leap program from comparison_chain_tech_leaps_v1
  (leaps 7+8, "The Spine"): replace JSON-file archaeology + bespoke per-category
  scripts with (a) one queryable SQLite datastore (runs, products, scores,
  artifacts, lineage, live_state) and (b) a lean dependency-aware stage runner
  with content-hashed artifacts, skip-if-unchanged resume, and recorded lineage.
  Phase 1 = datastore + runner core + read-only ingestion of existing artifacts,
  proven against real run data. NON-GOALS: no score changes, no methodology
  changes, no consumer-facing changes, frozen invariants untouched — Spine reads
  the pipeline; it does not alter it.
---

# TASK-252 — Project Spine1

## Mandate

Owner, 2026-06-11: *"start this project right now. Call it Project Spine1. you have my mandate."*
Source concept: `01_framework/operations/comparison_chain_tech_leaps_v1.html` — leaps 7 (real DAG)
+ 8 (one queryable datastore), the "Spine" tier. Build order per the endorsed recommendation:
datastore first, runner second, then real pipelines land on it.

## Phases

| Phase | Scope | Status |
|---|---|---|
| 1 | Datastore (schema + db layer) · lean DAG runner (signatures, resume, lineage) · read-only ingestion of existing BSIP2 traces + frontend JSONs · tests · proof-of-life against real run data | **delivered this task** |
| 2 | Wrap one real category pipeline (yogurts: BSIP1 → BSIP2 → frontend build) as declared stages; runner executes it end-to-end with incremental skip | **delivered (import mode)** |
| 3 | Live-state manifest generation from the datastore + post-deploy smoke-test integration (feeds gap-analysis ADD-1/ADD-2) | **delivered** |
| 4 | Migrate remaining category generators onto Spine stages (converges with TASK-233F shared packaging core) | open |

## Phase 1 deliverables

- `03_operations/spine/README.md` — charter, architecture decisions, usage
- `03_operations/spine/schema.sql` — datastore schema v1 (7 tables)
- `03_operations/spine/spine_db.py` — connection, hashing, artifact + lineage recording
- `03_operations/spine/ingest.py` — read-only sweep: BSIP2 trace runs, frontend JSONs, run summaries
- `03_operations/spine/runner.py` — Stage + run_pipeline: toposort, signature skip, output contract, lineage
- `03_operations/spine/test_spine.py` — pytest suite (runner + ingest on fixtures)
- Proof-of-life: real ingest run + verification queries (see return block when proposed)

## Phase 1 Return Block (2026-06-11)

**Status proposal:** Phase 1 DELIVERED — task stays IN_PROGRESS for Phases 2–4.

- **Tests:** 9/9 pass (`python -m pytest test_spine.py -v`, pytest 9.0.3, Python 3.14.5):
  runner run/skip/resume semantics, input-change re-run, output-tamper re-run, output
  contract, toposort + cycle detection, lineage recording, BSIP2 + frontend ingest.
- **Real ingest sweep:** 38 BSIP2 runs · **2,268 traces** · 976 products · 3,751 hashed
  artifacts · 2,215 lineage edges · 13 frontend files in live_state — the full pipeline
  history of every category, in one queryable DB, in seconds.
- **Guard check PASS:** run_yogurt_006 grade distribution from the datastore =
  A:14 **B:31** C:20 D:23 E:1 over 89 traces; minus the macros_plausible-blocked product
  (7290116932620, scored 66.2/B in traces, blocked at frontend) = **A:14 B:30 C:20 D:23 E:1
  over 88 — exactly the run record.**
- **Independent verification bonus:** the run_005→run_006 diff query returned **14 grade
  changes** — independently confirming TASK-249's return-block claim ("14 products changed
  grade") from raw traces, including the corrupted 89.9/A→66.2/B product. The datastore can
  now do CC-style claim verification as SQL.
- **Live-state manifest (ADD-2) exists as a query:** 13 rows, route-data file → version →
  run_id → product count.
- **Not committed:** working tree is on `task-244-confidence-structural-fix` with unrelated
  changes; commit/PR routing left to the orchestrator's next git pass.

## Phase 2 + 3 Return Block (2026-06-11, same day)

**Status proposal:** Phases 2 + 3 DELIVERED — task stays IN_PROGRESS for Phase 4.

### Phase 2 — yogurts pipeline as a declared DAG (`spine_yogurts.py`)
- The real run_yogurt_006 chain declared as 3 stages (BSIP1 build → BSIP2 score → frontend
  staging) with the true artifacts as typed inputs/outputs (88 BSIP1 records → 88 traces →
  staging JSON; engine + builder scripts hashed as inputs).
- **Import-state mode** (terraform-import pattern): existing artifacts adopted with full
  hashing + lineage; run 1 = adopted, run 2 = all `skipped` (verified). **EXECUTE mode is
  code-locked** with an explicit refusal message until the TASK-250 Ruling 3 owner sign-off
  + QA freeze land — Spine cannot regenerate pending-verification artifacts even by accident.
- **Live drift catch on day one:** Spine flagged a scores row whose trace no longer exists on
  disk — barcode 7290112346797, the RT-3 cereal misroute, whose trace dir was removed from
  run_006 by the concurrently active remediation session between ingest and DAG import.
  Ingest gained deletion-reconciliation (stale scores/artifacts/lineage rows removed,
  logged); re-ingest now reports run_006 = 88 traces, matching disk exactly.

### Phase 3 — manifest + production smoke test
- `manifest.py` → `live_manifest.json` (ADD-2): 13 entries — data file, category, version,
  run_id, product_count, sha256, + trace grade distribution when the producing run is known.
- `smoke_test.py` (ADD-1): asserts HTTP 200 + zero OFF markers + non-trivial body per route;
  404 = ABSENT (informational). **Live run against bari.digital: 12/12 routes PASS,
  0 OFF refs** (bread, butter, breakfast-cereals, granola, snacks, salty-snacks, yogurts,
  cheese, hard-cheeses, hummus, maadanim, juices). Exit code is CI-ready.
- Tests after changes: 9/9 pass.

### Commit
- Branch `project-spine1` (from master, via worktree — main working tree untouched):
  spine module + TASK-252 registry record. See branch log for hash.

## Guards

- Spine is **read-only** over pipeline artifacts in Phase 1 — it hashes and records, never modifies.
- `spine.db` is generated state, gitignored; `schema.sql` is the law.
- Zero new Python dependencies (stdlib `sqlite3`); a later DuckDB/Postgres move is a port, not a rewrite.
- Verification of ingest correctness: score/grade distribution reconstructed from the datastore must
  match the run record (run_yogurt_006: A:14 B:30 C:20 D:23 E:1, 88 products).
