# P176 / Additive-burden aggregate index — representation method (route: C1-GROK)

**Repo:** `C:\Bari` · branch `task-275-engine-fixes-abc` · HEAD `20fccbd496711d793666a264bbada4b1fa1fa20e`
**Read first:** `C:\Bari\tasks\TASK-325.md` (this is its delivery).
**Template to mirror:** `03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py` (standalone module under `proto_v0/src/`, report dir under `reports/methods/<name>/`, `evaluate_*()` + `--calibrate`/`--single` CLI, inert constants, OFF-ban guards).
**Lane:** C1-GROK (spec-complete Python build + data run, repo access).

## Objective
Build a **standalone representation method** that rolls the engine's **already-existing** per-signal additive findings — EV-002 (at-risk additive count), EV-003 (emulsifier risk tier: high-risk synthetic / neutral / prebiotic), EV-019 (prebiotic-gum exemption) — read from BSIP2 traces, into a **single displayable "additive burden" aggregate index** per product. This is representation + explanation ONLY. It introduces **no new penalty**, computes nothing that feeds a score, and moves no published score. Think: a clean rollup the consumer UI / explanation layer could show ("3 high-risk additives, 1 neutral, 1 prebiotic → burden: HIGH"), derived entirely from signals the engine already fires.

## What to build
1. **`03_operations/bsip2/proto_v0/src/method_additive_burden.py`** — standalone module/CLI. Given a product's BSIP2 trace, read the already-fired additive signals (EV-002 at-risk count, EV-003 emulsifier tier classification, EV-019 prebiotic exemption) and compute an aggregate: `{at_risk_count, high_risk_emulsifiers:[...], neutral_emulsifiers:[...], prebiotic_exempt:[...], additive_burden_index, burden_band: NONE|LOW|MED|HIGH, components:{...}}`. The index is a transparent weighted rollup of the EXISTING signal outputs (document the weighting; keep it inert — `ADDITIVE_BURDEN_*` module constants, NOT in `constants.py`). Do not re-derive additive identity from scratch — consume what the trace already carries.
2. **Run** across the live shelves' traces (produce them via `python 03_operations/page_generator/rescore_all.py` if not already staged) → `03_operations/bsip2/proto_v0/reports/methods/additive_burden/index.json` (per product) + `index.md` (per-shelf burden-band distribution with named denominators; call out the highest-burden products).

## Boundaries / guards (HARD)
- **NO NEW PENALTY, NO SCORING CHANGE.** This is a rollup of signals the engine ALREADY produces. Do not edit `score_engine.py`, `constants.py`, any config, or any live page JSON. The aggregate index must never feed back into a score. If it can't be built without touching the scoring path, STOP and say so.
- **Consume existing signals only.** Read EV-002/003/019 outputs from the trace; do not invent a new additive taxonomy or re-penalize.
- **OFF-ban absolute (TASK-238):** trace data only; never read Open Food Facts. Missing signal in a trace = absent, not assumed.
- **Do not invent data.** If a trace lacks the additive signals, mark the product `index:null` with a reason; do not fabricate.
- New files only (script + report dir). No edits to existing modules. Do not commit, do not push.
- **Do not close — propose RETURNED** with the output paths.

## Return format
Prose summary + the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): `artifacts` (paths + sha256), `counts` (named denominators: products_processed, by burden_band, products_with_at_risk_additives, index_null), `commands_run` (with exit codes), `not_done`, acceptance-test result. Acceptance test = (a) run exit 0 over live traces, (b) `index.json` + `index.md` exist and counts reconcile, (c) `git diff` shows **zero** changes to `score_engine.py` / `constants.py` / configs / live page JSON, and (d) a spot-check confirming the index is a faithful rollup of the trace's existing EV-002/003/019 values (not a new computation). A return without the JSON contract = CHANGES_REQUESTED.
