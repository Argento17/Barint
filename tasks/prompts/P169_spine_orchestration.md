# P169 / TASK-319 — Spine step 4: orchestration command (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Build ONE orchestration module that chains the existing spine pieces. Orchestration ONLY — call the existing CLIs; do NOT reimplement scoring/copy/gates. NO engine/scoring edits. Staging-only. **NO push, NO PR, NO deploy.** OFF-ban absolute. Propose RETURNED.

## The pieces (all built + verified — chain them, don't rebuild)
- **Step 2** `03_operations/page_generator/affected_set.py --set BARI_X=on [--out ...]` → affected_set.json (`affected_shelves[]`, `frozen_touched`, `frozen_breaches[]`, `affected_no_config[]`); exit 2 frozen / 1 movement / 0 none.
- **Trigger** `03_operations/page_generator/rescore_all.py --shelf <shelf>` → re-scores a shelf to `_rescore_staging/<shelf>/<shelf>_rescored.json` (now emits the full render contract — step 1).
- **Step 3** `03_operations/page_generator/copy_stage.py --staging <staging.json> --live <baseline.json> --shelf <shelf>` → carries grade-unchanged copy, writes `_rescore_staging/<shelf>/author_set.json` (grade-changed/new needing copy).
- **Gates** `03_operations/page_generator/gates/run_gates.py <page.json> --config <config.json> --baseline <live.json>` → G1-G8.
- Each shelf's live baseline = its config's `baseline_json`; shelf↔config map is the configs/ filenames.

## Build `03_operations/page_generator/spine_flip.py`
CLI: `python spine_flip.py --set BARI_X=on [--set ... ] [--note "..."] [--out-dir _rescore_staging/_spine_runs/<ts>]`

Flow:
1. **Affected-set + FROZEN GATE.** Run affected_set.py with the flag(s). If `frozen_touched` → **STOP immediately**, exit 2, write a report naming the frozen breaches. A frozen-invariant breach is a hard block — never proceed past it. If no affected shelves → exit 0 "no movement", done.
2. **Re-score** each affected shelf via rescore_all.py. Capture exit + the staging page path. A shelf that errors → record as a per-shelf failure (don't abort the whole run; report it).
3. **Copy** each via copy_stage.py against its config's baseline_json → carried + author_set.
4. **Gate** each via run_gates.py → record pass/fail + the gate report path. (Note: G1/G2/G6 "fail" against the v3 schema is the known match-live artifact — record the gate output honestly; the integrity gates that matter are G4 OFF / G5 score==trace / G7 parity / G8 data-sanity. Surface all, flag the integrity ones.)
5. **Aggregate** a `spine_run_report.json` + `.md`: flag_overrides, affected_shelves, per-shelf {score_moves, grade_moves vs baseline, carried, author_needed count, gate result, OFF count}, consolidated author_set (total products needing copy across shelves), frozen status, overall verdict.
6. **Deploy-ready bundle:** collect the staged (re-scored + copy-applied) pages for the affected shelves + the report + the consolidated author_set into `--out-dir`. Print a clear final line: "DEPLOY-READY: N shelves, M products need copy authoring, gates <PASS/REVIEW>, frozen breach <none/...>. No push performed."

## Hard constraints
- Orchestration only — shell out to the existing scripts (subprocess); do not duplicate their logic. NO engine/scoring/score changes. NO bari-web edits. **NO git push, NO PR, NO Vercel/deploy** — produce the bundle and stop; the owner runs the deploy/merge.
- Frozen gate is absolute (step 1 above). OFF-ban absolute.
- Graceful: one shelf failing is a recorded finding, not a crash.

## Verify end-to-end
Run `python spine_flip.py --set BARI_GLASSBOX_W4=on --note "spine e2e test"` (step 2 showed this affects cereals + hummus_shelfrel_002, ~3s for the shadow pass). Show: affected-set resolved, both shelves re-scored + copy-staged + gated, the spine_run_report, the consolidated author_set, frozen status clean, and that NO push/PR happened. Report total runtime. If a frozen flag is easy to demo the BLOCK path (e.g. a flag that moves milk), show the exit-2 stop too (optional).

## Return (do NOT close — propose RETURNED)
The module + the e2e run output (report + bundle contents + final DEPLOY-READY line) + the frozen-block behavior. Files changed (path+action+sha256). End with the TASK-319 return-contract JSON (`01_framework/operations/return_contract_v1.md`): task, proposed_status, artifacts[], counts{} (with commands), commands_run[], not_done[], self_check.
