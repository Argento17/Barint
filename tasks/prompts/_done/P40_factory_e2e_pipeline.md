# P40 / TASK-258 — Factory: generic executable end-to-end Spine pipeline (route: C1, Data Agent)

CONTEXT: Repo C:\Bari. We are building THE FACTORY: a machine that takes a shelf and
mechanically produces a gated page. Every stage already exists, but the chain has **never
actually executed end-to-end** — the only declared pipeline (`03_operations/spine/spine_yogurts.py`)
is import/verify only (no-op stages adopting existing artifacts; EXECUTE locked). Your job
is to wire a **generic, EXECUTABLE** pipeline that runs the real stages on a **throwaway
fixture**, proving the factory chains and exposing where the seams break.

## USE THESE — do not rebuild them
- DAG runner: `03_operations/spine/runner.py` (`Stage` + `run_pipeline` — toposort, hash-skip, output contract, lineage). Import and use it.
- Datastore: `03_operations/spine/spine_db.py` + `spine.db` (generated; rebuildable). Use it.
- Extraction (raw → structured): `03_operations/bsip0/raw_store/replay_parse.py` (parses banked raw pages). Inspect its real input/output interface first.
- Scoring: `03_operations/bsip2/proto_v0/src/score_engine.py`.
- Page-gen + gates: `03_operations/page_generator/generate_page.py` + `03_operations/page_generator/gates/run_gates.py`.
- **Reference only, DO NOT TOUCH:** `03_operations/spine/spine_yogurts.py` (import-only, locked; yogurts is on hold and off-limits).

## DELIVERABLE
A new generic pipeline file `03_operations/spine/pipeline_e2e.py` that declares EXECUTE-mode
`Stage`s (call the real scripts via subprocess where they're CLI; import where they're clean
callables) chaining:

  raw fixture → **extract** → BSIP1-shape records → **score** → BSIP2 traces → **generate_page** → gated page JSON

run through the existing `run_pipeline`. Plus a tiny **throwaway fixture**: 3–5 synthetic
sample products (raw input in the shape `replay_parse.py` expects) under a scratch dir
`03_operations/spine/_fixtures_e2e/`. **This fixture is fake throwaway data — NOT a real
shelf, NOT yogurts, NOT cereals, NOT any live category.** Output goes to a scratch dir
(e.g. `03_operations/spine/_e2e_out/`), never a consumer location.

## ACCEPTANCE
1. `python pipeline_e2e.py --execute` runs all stages **green** on the fixture and produces a throwaway gated page JSON.
2. `spine.db` shows `stage_runs` rows (status=ok) + `lineage` rows for the run (query and show them).
3. **Resume:** re-running with no input change → every stage reports **"skipped"**.
4. **Incremental:** editing ONE fixture input → only the stages **downstream** of it re-run.
5. **Seam-gap report:** for each stage boundary (extract→score, score→generate), state whether the upstream output format cleanly matches the downstream input. Where it does NOT, document the exact mismatch — that's the next build's target. At minimum, **score→generate must truly execute**; if extraction can't run on synthetic data, document precisely why and stub that one stage with a clear `SEAM_GAP` marker (do not fake downstream data).

## GUARDS
- **THROWAWAY ONLY.** No live category, no yogurts/cereals, no consumer page, no published output. Scratch dirs only.
- Do NOT modify `spine_yogurts.py`, any live artifact, any published score, the engine logic, or any consumer page.
- **OFF ban (TASK-238):** extraction must NEVER fall back to Open Food Facts or any substitute; a missing field stays null. Any OFF dependency is a launch blocker — flag, never introduce.
- Import/reuse `runner.py` + `spine_db.py`; do not rewrite them. stdlib + the existing scripts only; no new dependencies.

## RETURN BLOCK
The pipeline file path; the `--execute` run output (the `{stage: ran|skipped}` dict); the
`spine.db` evidence (the `stage_runs` + `lineage` rows you queried); the resume proof (2nd
run all-skipped) and incremental proof (edit → only-downstream-reran); the seam-gap table;
and exactly which stages executed for real vs were stubbed. End with the machine-readable
JSON return contract (`01_framework/operations/return_contract_v1.md`); counts must include
`stages_declared`, `stages_executed_real`, `stages_stubbed`, `seam_gaps_found`,
`resume_all_skipped: true|false`, `off_introduced: 0`. **Propose RETURNED — do NOT write
CLOSED; the orchestrator verifies and closes.**
