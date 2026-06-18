# P175 / Omega-6:3 / specific-lipid extraction method + label-coverage dataset (route: C1-GROK)

**Repo:** `C:\Bari` · branch `task-275-engine-fixes-abc` · HEAD `20fccbd496711d793666a264bbada4b1fa1fa20e`
**Read first:** `C:\Bari\tasks\TASK-324.md` (this is its delivery).
**Template to mirror:** `03_operations/bsip2/proto_v0/src/method_hp_carb_sodium.py` (just-landed P173 pattern — standalone module under `proto_v0/src/`, report dir under `reports/methods/<name>/`, an `evaluate_*()` + `--calibrate`/`--single` CLI, inert constants, OFF-ban guards, missing→`insufficient_data`).
**Lane:** C1-GROK (spec-complete Python build + data run, repo access).

## Objective
Build a **standalone extraction method** that parses **omega-3 / omega-6 / specific-lipid** declarations from the in-house Hebrew labels (BSIP0 raw text + BSIP1 panel) where they are present, normalizes them to per-100g fields, and **measures live label coverage** (how many products on each shelf actually declare these). This is the data layer for a future EV-011-style signal (**applies when declared, no-op when absent — never worst-cases missing data**). Extraction + coverage data ONLY — no ratio is computed into any score.

## What to build
1. **`03_operations/bsip2/proto_v0/src/method_omega_lipid_extract.py`** — standalone module/CLI. Given a product's BSIP0/BSIP1 record it extracts, where declared: `omega3_mg_100g`, `omega6_mg_100g`, and any specific-lipid call-outs (EPA, DHA, ALA, אומגה 3/6, חומצות שומן אומגה). Returns `{omega3_mg_100g, omega6_mg_100g, omega6_3_ratio|null, specific_lipids:[...], declared: true|false, source_field}`. Hebrew + Latin term matching; if neither omega is declared → `declared:false` (NOT zero, NOT insufficient — simply not on this label).
2. **Coverage run** across the live shelves (same corpora the P173 calibrator used via `page_generator/configs/`). Emit `03_operations/bsip2/proto_v0/reports/methods/omega_lipid/coverage.json` (per product: barcode, shelf, declared flag, extracted values) + `coverage.md` (per-shelf coverage rate with named denominators: N declaring omega3 / omega6 / either / ratio-computable, out of N evaluated).

## Boundaries / guards (HARD)
- **NO SCORING.** Do not edit `score_engine.py`, `constants.py`, any config, or any live page JSON. No ratio is applied to a score; no published score moves. This is extraction + measurement only. If it can't be done without touching the scoring path, STOP and say so.
- **EV-011 contract:** absent declaration = `declared:false` and the field is simply unavailable — never default to a worst-case or a zero that could later penalize.
- **OFF-ban absolute (TASK-238):** omega/lipid values come only from the in-house BSIP0/BSIP1 panel/label text. Never read or fall back to Open Food Facts. Not declared = not declared.
- **Do not invent data.** No estimation of omega content from oil type — declared values only (note any "contains canola/flax oil" qualitative signal separately and clearly as NON-quantitative, do not convert it to mg).
- New files only (script + report dir). No edits to existing modules. Do not commit, do not push.
- **Do not close — propose RETURNED** with the output paths.

## Return format
Prose summary + the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): `artifacts` (paths + sha256), `counts` (named denominators: products_evaluated, declaring_omega3, declaring_omega6, declaring_either, ratio_computable, per-shelf coverage), `commands_run` (with exit codes), `not_done`, acceptance-test result. Acceptance test = (a) coverage run exit 0 over the live corpora, (b) `coverage.json` + `coverage.md` exist and counts reconcile, (c) `git diff` shows **zero** changes to `score_engine.py` / `constants.py` / configs / live page JSON. A return without the JSON contract = CHANGES_REQUESTED.
