# P174 / Counterfactual explanation method — minimal-change-to-next-grade (route: C1-GEMINI)

**Repo:** `C:\Bari` · branch `task-275-engine-fixes-abc` · HEAD `20fccbd496711d793666a264bbada4b1fa1fa20e`
**Read first:** `C:\Bari\tasks\TASK-323.md` (this is its delivery).
**Lane:** C1-GEMINI (C1-grade build/judgment, writes files + runs shell).

## Objective
Build a **standalone post-score method** that, given a product's BSIP2 trace, computes the **minimal label change that would move it up one grade band** — e.g. "≈150 mg/100g less sodium → C → B". This is a pure read-over-traces explanation layer. It **changes no score**, touches no engine path, and writes **no Hebrew copy** (consumer authoring is a later, separate Content/Sonnet step — out of scope here). Output is a structured English/numeric counterfactual record per product.

## What to build
1. **`03_operations/bsip2/proto_v0/src/method_counterfactual.py`** — a standalone module/CLI (run by path). Input: a BSIP2 trace (fired signals, per-dimension scores + weights, final score, grade boundaries). Logic: identify the smallest single-lever change (and optionally the smallest 2-lever combo) on a **label-observable** input (sodium, sugar, an at-risk additive removal, etc.) that lifts the final score across the next grade boundary. Output per product: `{barcode, shelf, current_score, current_grade, next_grade, levers: [{field, current_value, target_value, delta, dimension_affected}], achievable: true|false, note}`.
   - Grade boundaries: read them from the engine's resolution contract / `grade_boundary_policy_v1.json` — do not hardcode.
   - Where a lever isn't cleanly invertible from the trace, mark `achievable:false` with the reason rather than fabricating a precise number.
2. **Sample run** over the live shelves' traces (produce them via `python 03_operations/page_generator/rescore_all.py` if staging traces aren't already present) → write `03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json` (per-product records) + `sample.md` (a readable digest: how many products got a single-lever counterfactual, how many needed 2 levers, how many were `achievable:false`, with named denominators).

## Boundaries / guards (HARD)
- **NO SCORING CHANGE.** Read traces only. Do not edit `score_engine.py`, `constants.py`, any config, or any live page JSON. Do not re-rank, do not move a published score. If the method can't be built without writing to the scoring path, STOP and say so.
- **Label-observable levers only.** Counterfactuals may only propose changes to fields that appear on a label / in BSIP0 (sodium, sugar, additive presence, fat, fiber…). No "reduce acrylamide", no bioavailability, no non-label inputs.
- **OFF-ban absolute** (TASK-238): no Open Food Facts anywhere.
- **No Hebrew copy.** Structured/numeric output only; phrasing for consumers is a downstream Content step.
- New files only (the script + the report dir). No edits to existing engine modules. Do not commit, do not push.
- **Do not close the task — propose RETURNED** with the output paths.

## Return format
Prose summary + the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): `artifacts` (paths + sha256), `counts` (named denominators: products_processed, single_lever, two_lever, achievable_false), `commands_run` (with exit codes), `not_done`, acceptance-test result. Acceptance test = (a) method runs over live traces exit 0, (b) `sample.json` + `sample.md` exist and counts reconcile, (c) `git diff` shows **zero** changes to any engine module / config / live page JSON. A return without the JSON contract = CHANGES_REQUESTED.
