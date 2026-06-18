# P153 / Cereals generate_page migration — pattern-setter (TASK-292 / TASK-233F) (route: C1-GEMINI)

## Repo / context
- Repo root: `C:\Bari`. Branch `master`. Read first: `C:\Bari\tasks\TASK-292.md`.
- **Decision (orchestrator, 2026-06-16):** `generate_page.py` is THE shared packaging core for TASK-233F.
  `frontend_core.py` does NOT exist (phantom — its only importer is the dangling/parked yogurts-v4 builder).
  Do NOT use or recreate `frontend_core.py`.
- The core: `03_operations/page_generator/generate_page.py` — deterministic, self-gating (runs `gates/run_gates.py`),
  OFF-ban enforced. Config schema = its module docstring + the working examples
  `03_operations/page_generator/configs/granola.json` and `.../snacks.json` (keys: category, corpus_dirs,
  run_products_dir, baseline_json, retailer_scope, subpool_filter, dedup, exclusions, extension_fields,
  boundary_policy). Run with `--timestamp <fixed ISO8601>` for determinism.
- Cereals inputs (verified):
  - BSIP1 corpus: `03_operations/bsip1/run_cereals_008/output` (63 `bsip1_*.json`).
  - BSIP2 traces (run universe): `02_products/breakfast_cereals/bsip2_outputs/run_cereals_008/products` (63).
  - **Live page to reproduce:** `bari-web/src/data/comparisons/cereals_frontend_v2.json` — a **curated 20-of-63**
    subset, `_meta.run_id = run_cereals_008`.

## Objective — PROVE parity (do NOT publish)
1. Author `03_operations/page_generator/configs/cereals.json` (modeled on granola/snacks) whose
   `corpus_dirs` + `run_products_dir` point at the cereals paths above, and whose `subpool_filter` /
   `exclusions` reproduce the **curation that yields the live 20 products** (derive it by comparing the
   63-trace universe to the 20 barcodes in the live page — figure out what distinguishes the included 20).
2. Run `python 03_operations/page_generator/generate_page.py --config 03_operations/page_generator/configs/cereals.json --out 03_operations/page_generator/outputs/cereals_generated_v1.json --timestamp 2026-06-16T00:00:00Z`.
3. **Parity check vs the live page** (`cereals_frontend_v2.json`): same set of barcodes (20), and for each,
   `score`==trace `final_score_estimate` (|Δ|<0.6 rounding) and same `grade`. Copy fields will differ
   (generator emits PENDING_COPY; live has authored copy) — that is EXPECTED and not a parity failure.
4. Report parity: products matched/expected, score-match %, grade-match %, and any product-set deltas
   (included-but-shouldn't / missing). If you cannot reproduce the exact 20, REPORT the gap precisely
   (what curation the bespoke builder used that the config can't yet express) — that is a valid finding.

## Boundaries / guards
- **Write ONLY** `configs/cereals.json` + `outputs/cereals_generated_v1.json` (a NEW file). **Do NOT overwrite**
  `bari-web/src/data/comparisons/cereals_frontend_v2.json` or any live page. This is a parity PROOF.
- OFF ban (TASK-238): the generator already excludes OFF; never add an OFF source. Hebrew name required.
- Do NOT touch the engine, scoring, or any other category. Deterministic output (fixed `--timestamp`).
- Do NOT commit, push, or close. Propose RETURNED.

## Return format
- The `configs/cereals.json` you wrote (key fields, esp. the subpool/exclusion curation logic).
- Parity table: 20/20 barcodes? score-match %, grade-match %, list any deltas.
- `run_gates.py` self-gate result from the generator run.
- End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`, status RETURNED).
