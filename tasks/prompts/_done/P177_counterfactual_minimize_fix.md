# P177 / Counterfactual method — fix continuous-lever minimization (route: C1-GROK)

**Repo:** `C:\Bari` · branch `task-275-engine-fixes-abc` · HEAD `20fccbd496711d793666a264bbada4b1fa1fa20e`
**Read first:** `C:\Bari\tasks\TASK-323.md` (the `changes_requested_reason` is the exact gap).
**This is a RETRY of P174** (Gemini built the method; structure is sound but the central "minimal" property is wrong for continuous levers). **Fix the EXISTING file in place — do not rewrite from scratch.**
**Lane:** C1-GROK.

## Existing artifact (keep + improve, do not discard)
- `03_operations/bsip2/proto_v0/src/method_counterfactual.py` — works, read-only over traces, scope-clean, label-observable levers, honest `achievable:false`. **Preserve all of that.**
- Reports: `03_operations/bsip2/proto_v0/reports/methods/counterfactual/sample.json` + `sample.md` (regenerate after the fix).

## The ONE defect to fix
The method does not return the **minimal** change for **continuous** levers. Today it sets `sugars_g` target to `0.0` (the extreme) and `ingredient_count` to a fixed `12`. The DoD requires the **smallest** change that lifts the score across the **next grade boundary** (the example in the spec is `sodium -X mg → C to B` — i.e. solve for X).

Fix:
1. **Continuous levers (sugars_g, sodium_mg, fat_g, etc.):** solve for the **minimal target value** at which the recomputed final score just crosses into the next grade band — e.g. binary-search / threshold-solve the lever between its current value and its floor, find the smallest delta that flips the grade, and report THAT target (not 0.0). If even the lever's floor (e.g. 0) doesn't cross the boundary, that lever alone is `achievable:false` — don't claim it.
2. **Binary levers (has_seed_oil true→false) and genuine cliff thresholds (ingredient_count penalty cliff):** these are already minimal — keep as-is. For the ingredient-count cliff, confirm `12` is the real engine penalty threshold (cite where in the engine/contract it lives); if the cliff is elsewhere, use the real value.
3. Re-run over the same 53 live traces; regenerate `sample.json` + `sample.md`. Expect achievable counts to possibly change (some continuous-only cases that needed an extreme will become `achievable:false`; others will now report a realistic partial delta). Report the new distribution honestly.

## Boundaries / guards (HARD — unchanged from P174)
- **NO SCORING CHANGE.** Read traces + recompute scores in your own simulation only. Do NOT edit `score_engine.py`, `constants.py`, configs, or any live page JSON. The recompute must be a local simulation that mirrors the engine, never a write to it. Scope-guard `git diff` on those paths MUST stay empty.
- **Label-observable levers only.** No non-label inputs.
- **OFF-ban absolute** (TASK-238). **No Hebrew copy** (later Content step). **No invented data** — if a trace lacks the inputs to solve a lever, mark it `achievable:false` with the reason.
- Modify only `method_counterfactual.py` + regenerate the two report files. Do not commit, do not push.
- **Do not close — propose RETURNED.**

## Return format
Prose summary + the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): `artifacts` (paths + sha256), `counts` (products_processed, achievable, single/double, achievable_false, **and how many continuous-lever counterfactuals now report a partial (non-extreme) target**), `commands_run` (exit codes), `not_done`, acceptance-test result. Acceptance = (a) run exit 0 over the 53 traces; (b) for at least one continuous-lever case, the reported target is a **partial** boundary value, NOT the lever's extreme, and the note shows the grade flips exactly at that value; (c) scope-guard `git diff` empty on score_engine/constants/configs/live JSON. A return without the JSON contract = CHANGES_REQUESTED.
