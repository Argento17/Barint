# P154 / TASK-233F migration bucket A — juices, cheese → generate_page (TASK-293) (route: C1-GROK)

## Context
- Repo `C:\Bari`, branch `master`. Read first: `C:\Bari\tasks\TASK-293.md`.
- **THE shared core = `03_operations/page_generator/generate_page.py`.** `frontend_core.py` is a PHANTOM — do
  NOT use or recreate it. **Proven exemplar: `03_operations/page_generator/configs/cereals.json`** (just landed;
  reproduces the live curated cereals page 20/20, 0 score/grade mismatch). Follow that pattern exactly.
- Config schema = `generate_page.py` docstring + `configs/{cereals,granola,snacks}.json` (keys: category,
  corpus_dirs, run_products_dir, baseline_json, retailer_scope, subpool_filter, dedup, exclusions,
  extension_fields, boundary_policy).
- Spine live_state (rebuild `python 03_operations/spine/ingest.py`; query `spine.db` `live_state`) maps each
  live page → version + run_id + product_count. Use it to find each category's source run + expected count.

## For EACH category in this bucket — **juices, cheese**
1. Identify the live page (`bari-web/src/data/comparisons/<cat>_frontend_*.json` — `_meta` gives
   version/run_id/product_count), its BSIP2 traces run dir, and its BSIP1 corpus dir.
2. Author `03_operations/page_generator/configs/<cat>.json` (model on `cereals.json`) — derive
   `subpool_filter`/`exclusions` to reproduce the live page's curated product set.
3. Run `python 03_operations/page_generator/generate_page.py --config 03_operations/page_generator/configs/<cat>.json --out 03_operations/page_generator/outputs/<cat>_generated_v1.json --timestamp 2026-06-16T00:00:00Z`.
4. **Parity vs the live page:** identical barcode set, `score`==trace `final_score_estimate` (|Δ|<0.6), same
   `grade`. Copy fields differ (generator emits PENDING_COPY) — EXPECTED, not a failure.
5. If a category uses a BESPOKE loader (single merged JSON / curated builder not `load_batch`-compatible) →
   STOP on it, do NOT force; report "bespoke loader — needs custom loader" as a finding.

## Boundaries / guards
- Write ONLY `configs/<cat>.json` + `outputs/<cat>_generated_v1.json` (NEW files) per category. **NEVER
  overwrite any live `bari-web` page.** OFF ban (TASK-238). No engine touch. Deterministic (`--timestamp`).
- Do NOT commit, push, or close. Propose RETURNED.

## Return format
- Per category: parity table (barcodes matched/expected, score-match %, grade-match %, deltas) + self-gate
  result, OR the bespoke-loader finding.
- End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`, RETURNED).
