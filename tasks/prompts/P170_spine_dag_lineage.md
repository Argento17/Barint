# P170 / TASK-320 — Spine step 5: DAG runner + lineage integration (route: Data Agent / C1)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Integrate with the EXISTING Spine runner; do not reimplement it. NO engine/score/page/bari-web edits. NO push/deploy. OFF-ban absolute. Propose RETURNED.

## Goal (final spine step — an enhancement; the core works at step 4)
Run `spine_flip.py`'s per-shelf chain THROUGH the Spine DAG runner so the spine becomes **incremental** (re-runs skip unchanged shelves) and **self-recording** (lineage in spine.db). Today spine_flip shells out per shelf every time with no skip/lineage.

## The runner (already built — TASK-252; use it, don't rebuild)
- `03_operations/spine/runner.py`: `Stage(name, fn, inputs=[Path], outputs=[Path])` + `run_pipeline(stages, force=False)`.
  - signature = sha256(name + code_version + input file hashes); a stage is SKIPPED when the same signature ran OK and recorded outputs still exist unchanged; after a run, outputs are hashed + recorded as artifacts and lineage rows link every output→every input.
  - returns `{stage_name: 'ran'|'skipped'}`.
- `03_operations/spine/spine_db.py`: `connect, record_artifact, record_lineage, sha256_file`. `spine.db` is gitignored generated state (rebuildable).

## Build
Add a Spine-runner-backed execution path (a new `--via-spine` mode on spine_flip.py, OR a thin `spine_pipeline.py` spine_flip imports). For each AFFECTED shelf (after the frozen gate passes — frozen breach still hard-stops BEFORE any pipeline), declare 3 stages:
1. `rescore_<shelf>` — inputs: the 9 engine source files (the ENGINE_FILES set used by shadow_backtest / the headpin run records) + the shelf config + a corpus marker (the corpus dir or its manifest); output: `_rescore_staging/<shelf>/<shelf>_rescored.json`. fn shells `rescore_all.py --shelf <shelf>`.
2. `copy_<shelf>` — inputs: the rescored page + the config's `baseline_json`; outputs: the copy-applied page + `_rescore_staging/<shelf>/author_set.json`. fn shells `copy_stage.py`.
3. `gate_<shelf>` — input: the copy-applied page; output: its gate report. fn shells `run_gates.py`.
Then `run_pipeline(all_stages)` — it orders, hashes, skips unchanged, records artifacts + lineage. Aggregate the spine_run_report exactly as step-4 does (reuse spine_flip's reporting), now also noting per-stage ran/skipped.

## Acceptance (prove incremental + lineage)
1. Run the via-spine flow on a flag what-if (e.g. `BARI_GLASSBOX_W4=on`, affects cereals+hummus). First run: stages report **'ran'**; report + bundle produced.
2. Run the SAME flow again with NOTHING changed → stages report **'skipped'** (incremental works). Show the run_pipeline result dict.
3. Query `spine.db` to show lineage was recorded: the staged page artifact links back to its inputs (engine/config/corpus). Paste the query + rows.
4. Touch a config (or pass `force`) → that shelf's stages re-run (skip invalidation works).
5. Frozen gate still hard-stops before any pipeline (re-confirm BARI_RECAL_P0=on → exit 2, no stages).

## Constraints
- Use the existing runner + spine_db; don't duplicate hashing/lineage. NO engine/score/page/bari-web edits. spine.db is generated (gitignored). NO push/deploy. OFF-ban absolute.

## Return (do NOT close — propose RETURNED)
The module/changes + the two-run incremental proof (ran → skipped) + the spine.db lineage query output + the force/invalidation proof + frozen-stop re-confirm. Files changed (path+action+sha256). End with the TASK-320 return-contract JSON (`01_framework/operations/return_contract_v1.md`): task, proposed_status, artifacts[], counts{} (with commands), commands_run[], not_done[], self_check.
