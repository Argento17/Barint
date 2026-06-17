# P168 / TASK-318 — Spine step 3: automated copy stage (route: Data Agent / C1)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Build a reusable module by generalizing two proven one-off scripts. NO engine/scoring changes. NO bari-web edits. OFF-ban absolute. No commit, no deploy. Propose RETURNED.

## Goal
The spine must apply copy automatically after a re-score, instead of the hand-listed-per-shelf one-offs we used this week. Generalize:
- `_rescore_staging/copy_carryover.py` (TASK-305 — carry live copy for grade-UNCHANGED barcodes; leave PENDING on grade-changed/new; flag score-moved≥3)
- `_rescore_staging/schema_strip.py` (TASK-307 — reduce a staging page to its live copy-field schema)
into ONE config-driven module: `03_operations/page_generator/copy_stage.py`.

## Behavior (per category)
Inputs: a freshly generated staging page (e.g. `_rescore_staging/<shelf>/<shelf>_rescored.json`) + the live baseline JSON
(`config.baseline_json`). For each product:
- **In both & SAME grade** → carry the live product's copy fields (insightLine, rowVerdict, consumerTakeaway,
  expansion.consumerExplanation.*, bariInterpretation[].interpretation, bestUseCases, expansion.comparisonContext — whichever
  exist in the live schema for that category; the live page is the source of truth for which copy fields exist).
- **Grade-CHANGED or NET-NEW** → leave PENDING_COPY in the live-set copy fields AND add the barcode to the author-set
  (with old→new grade, score, and which fields need authoring).
- Keep all staging NUMBERS (score, grade, nutrition, render fields from step 1 — bariInterpretation key/label/score/strength).
- **Schema-match:** strip staging-only fields not present in the live schema (port schema_strip's per-shelf field-set logic, but
  derive the live copy-field set from the live JSON itself rather than a hand-coded table where possible).
- **Flag** grade-unchanged-but-score-moved ≥3 pts (carried copy may be stale — surface for review, like copy_carryover did).

Outputs: the copy-applied staging page (written back / to a chosen path) + `author_set.json`:
`{shelf, authored_needed:[{barcode, name, old_grade, new_grade, score, fields:[...]}], carried:N, score_moved_flags:[...]}`.

## Constraints
- Config-driven / parameterized — NO per-shelf hand-listing of barcodes or field tables baked into the module (that was the one-off
  smell). Drive the copy-field set from the live page schema + a small per-category override only if genuinely unavoidable (justify it).
- Idempotent + reproducible. Reuse the existing one-off scripts as the reference implementation; don't reinvent their proven rules.
- OFF-ban absolute (never introduce OFF; carry only what the live page already has). NO engine/scoring/score changes. NO bari-web edits.

## Verify (one category end-to-end)
Pick one category (e.g. cereals): regenerate its staging via `python 03_operations/page_generator/rescore_all.py --shelf cereals`,
run copy_stage on it vs its live baseline, and show: N carried (grade-unchanged), the author-set (grade-changed/new), 0 PENDING on
carried products, schema matches live, scores unchanged. Confirm it reproduces what TASK-305/307 did for that shelf.

## Return (do NOT close — propose RETURNED)
The module + the one-category proof (carried count, author-set, schema-match, score-unchanged). Files changed (path+action+sha256).
End with the TASK-318 return-contract JSON (`01_framework/operations/return_contract_v1.md`): task, proposed_status, artifacts[],
counts{} (with commands), commands_run[], not_done[], self_check.
