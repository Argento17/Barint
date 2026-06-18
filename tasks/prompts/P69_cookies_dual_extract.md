# P69 — Cookies: Gemini dual-extractor consensus (extraction trust) (route: C1-CURSOR)

**Task:** TASK-275 (factory run #7, `cookies-coffee`). **Lane:** C1-CURSOR — spec-complete generalization
of an existing module + run. The Gemini calls happen INSIDE `dual_extract.py` (extractor B).

## Why
The factory's extraction-trust stage (TASK-265, ★★ substrate "dual-extract trust"). Run Gemini against the
rule-based `replay_parse` BSIP0 on the SAME raw HTML, field-by-field, to independently catch parser errors
(e.g. the kind of nutrition mis-parse that produced a bogus "6000 mg" sodium plausibility flag). Brined got
27/27 AGREE; cookies needs the same trust check before its scores are accepted.

## The gap to close
`03_operations/spine/dual_extract.py` `main()` is hardcoded to the synthetic e2e fixtures
(`FIXTURES_DIR.glob("raw_e2e_*.html")`). Generalize it to run on a REAL banked raw_store category, WITHOUT
breaking the existing e2e default. The reusable core (`extract_a`, `extract_b`, `run_consensus`,
`_strip_json_fences`) stays as-is.

## Steps
1. **Add CLI args** to `dual_extract.py` (argparse), keeping current behavior as the default when no args:
   - `--raw-store <dir>` : a raw_store category dir containing per-code subfolders with banked HTML + `manifest.jsonl`
   - `--bsip0 <json>` : the BSIP0 raw JSON (array of products) for extractor A (the rule-based side)
   - `--corpus <json>` : optional `corpus_filter.json`; when given, restrict to the **IN_SCORED** barcodes
   - `--out <dir>` : output dir for the report (default keeps `_e2e_out`)
   - `--limit N` : optional cap (for rate-limit safety)
   When `--raw-store` is given: discover (barcode → html_path) from the manifest, pair each with its BSIP0
   record (extractor A reads the BSIP0 nutrition/ingredients), call Gemini (extractor B) on the banked HTML.
2. **Run it on cookies IN_SCORED:**
   - `--raw-store 03_operations/bsip0/raw_store/shufersal/cookies_coffee`
   - `--bsip0 02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json`
   - `--corpus 02_products/cookies_coffee/factory_run_001/corpus_filter.json`
   - `--out 02_products/cookies_coffee/factory_run_001/dual_extract`
3. **Rate limits:** Gemini may return 429 ("no capacity"). The script already marks B-side unavailable on
   timeout/error — keep that. If >30% of products come back B-unavailable, STOP early and report the
   agreement rate on what DID resolve + the unavailable count (do not fabricate consensus for unavailable
   ones). A representative resolved sample is acceptable if full coverage rate-limits out.

## Guards
- **No score/engine changes.** This is a read-only trust check; do not touch the scoring run or BSIP1.
- **OFF ban** — extractor B (Gemini) reads ONLY the banked HTML; it must not be prompted to use any external
  source. The existing prompt template is HTML-only — keep it that way.
- Reliability caveat: Gemini cannot be trusted to self-report. The script's consensus is computed
  DETERMINISTICALLY in `run_consensus` from both extractors' fields — rely on that, not on Gemini prose.

## Definition of done (report)
1. The generalized `dual_extract.py` (sha256) — confirm the e2e default path still works (1-line note).
2. The consensus report path (json + md, sha256).
3. **Agreement summary:** products processed, B-available count, B-unavailable (429/timeout) count, and the
   **field-by-field AGREE / DISAGREE tallies** (esp. energy_kcal, protein_g, fat_g, sodium_mg, sugars_g).
4. **List every DISAGREE on a nutrition field** with barcode + A-value vs B-value (this is the payload — it
   flags rule-based parser errors on IN_SCORED products).
5. Confirm 0 OFF references in the report.

## Return format
End with the return contract (`01_framework/operations/return_contract_v1.md`): task=P69,
proposed_status=RETURNED, artifacts (dual_extract.py + report json/md + sha256), counts (processed /
available / unavailable / agree / disagree per field), commands_run (exit codes), not_done, self_check.
Do NOT close — propose RETURNED. The orchestrator verifies the report + re-checks any flagged disagreement.
