# P157 / TASK-298 — Quick re-score trigger (rescore_all) (route: C1-GROK)

Repo: C:\Bari (Agent OS root). Branch: task-275-engine-fixes-abc. Full repo access.
Read first: `tasks/TASK-298.md`; the PROVEN chain template `03_operations/spine/pipeline_e2e.py`
(esp. `stage_score_products` L437-493 + the `sys.path` score-engine shim L175-209, and `stage_generate_page`
L496-557); and one exemplar config `03_operations/page_generator/configs/cereals.json`.

## Objective
Build the release-platform core: ONE generic command that re-scores EVERY configured shelf in one go, under the
CURRENT scoring engine, and regenerates each page. This is the "flip-a-switch" trigger — it must be a SINGLE generic
code path that treats all shelves identically (no per-category branches, no bespoke loaders).

Create **`03_operations/page_generator/rescore_all.py`**. Behavior:
1. Discover shelf configs: every `03_operations/page_generator/configs/*.json` EXCEPT `_generated_*`. (9 today:
   brined_cheeses, cakes, cereals, cookies_coffee, granola, hard_cheeses, hummus_shelfrel_002, juices, snacks.)
2. For EACH config, run the SAME generic pipeline:
   a. Read the config's `corpus_dirs` (the BSIP1 source — already-scraped data; **do NOT re-scrape, no network**).
   b. Re-score: for each `bsip1_*.json` in the corpus, run the current engine chain EXACTLY as pipeline_e2e's
      `stage_score_products` does — `extract_signals → classify_category → infer_nova → assign_evaluation_scope →
      score_product → assemble_trace` (import from `03_operations/bsip2/proto_v0/src/` via the same sys.path shim).
      Write fresh `bsip2_trace.json` per product into a STAGING traces dir (e.g. `_rescore_staging/<shelf>/products/<pid>/`),
      NOT into the live `02_products/.../bsip2_outputs` run dirs.
   c. Run `generate_page.py` against a COPY of the config repointed at the staging traces dir, output the page to
      `_rescore_staging/<shelf>/<shelf>_rescored.json`. Self-gate must PASS.
   d. Verify: (i) score==trace — every page product `score` equals its staging trace `final_score_estimate`;
      (ii) OFF=0 in the page; (iii) gate exit 0.
   e. Diff vs the current LIVE page (`config.baseline_json`): count products, score-moves (rounded), grade-moves;
      list the grade-movers (barcode old→new).
3. Print a SUMMARY TABLE across all shelves: shelf · products · score-moves · grade-moves · gate(PASS/FAIL) · OFF-count.
4. Exit non-zero if ANY shelf fails its gate, has OFF>0, or breaks score==trace.

## Boundaries / guards (hard)
- **NEVER overwrite live**: all output under `_rescore_staging/` only. Do NOT touch `bari-web/`, do NOT touch the
  live `02_products/.../bsip2_outputs` run dirs, do NOT touch engine code under `proto_v0/src/`.
- **OFF ban (TASK-238):** the chain must not introduce any OFF fallback; a field that isn't in BSIP1 stays null.
  Any OFF marker in any output → fail that shelf and report (launch blocker).
- **Generic only:** one code path for all shelves. If a shelf needs special handling to even run, do NOT special-case
  it — report it as a finding (it means that shelf isn't truly uniform yet).
- **Determinism:** pass a fixed `--timestamp 2026-06-16T00:00:00Z` to generate_page; sort everything; same inputs → same output.
- Add `_rescore_staging/` to `.gitignore`. Do NOT commit, do NOT deploy.
- This RE-SCORES (moves published scores) but only to STAGING — it is the prep for an owner-gated deploy, not the deploy.

## Return format
- Confirm `rescore_all.py` created; show its `--help`/usage.
- The full SUMMARY TABLE (all 9 shelves) from an actual run: `python 03_operations/page_generator/rescore_all.py`.
- Per shelf: products, score-moves, grade-moves (+ the grade-mover barcodes old→new), gate exit, OFF count, score==trace OK?
- Any shelf that could NOT run generically → name it + why (a uniformity gap finding).
- Total wall-clock of the full run (proves "quick").
- **Do not close — propose RETURNED.** End with the machine-readable return contract
  (`01_framework/operations/return_contract_v1.md`): JSON `task`, `proposed_status`, `artifacts[]` (path+action+sha256),
  `counts{}` (per-shelf, trace-derived, with the command), `commands_run[]` (cmd+exit_code), `not_done[]`, `self_check`.
