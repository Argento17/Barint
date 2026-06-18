# P156 / TASK-296 Piece A — single-path configs for brined + butter + bread (route: C1-GROK)

Repo: C:\Bari  (Agent OS root). Branch: task-275-engine-fixes-abc. You have full repo access.
Read first: `tasks/TASK-296.md` (the task), and the EXEMPLAR config `03_operations/page_generator/configs/cereals.json`
plus the generator `03_operations/page_generator/generate_page.py` (skim — you only author config, not code).

## Objective
Bring THREE categories onto the SINGLE shared generator `generate_page.py` via a config each — exactly the
cereals pattern. NO bespoke Python, NO per-category loader, NO new code. One `configs/<cat>.json` per
category, pointing at the BSIP2 run that ACTUALLY produced the live page's scores, with an explicit
exclusion list so the generated product set matches the live curated set.

Categories + their live pages (the parity target) + candidate run trees:
1. **brined_cheeses** — live: `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` (48 products / 48 scored, `_meta.run_id=run_brined_005`).
   Run: `02_products/brined_cheeses/bsip2_outputs/run_brined_005/products`. ⚠️ This is the GOLDEN page — reproduce exactly.
2. **butter** — live: `bari-web/src/data/comparisons/butter_frontend_v2.json` (31 products / 39 scored, `_meta.run_id=butter_run_003`).
   Run: `02_products/butter/bsip2_outputs/butter_run_003/products`. 39 scored → 8 excluded to reach 31 displayed.
3. **bread** — live: `bari-web/src/data/comparisons/bread_frontend_v2.json` (19 products / 24 scored, no `_meta.run_id`).
   Candidate run: `02_products/bread_retail_003/bsip2_outputs/run_bread_008_headpin/products`. ⚠️ `bread_light` is a DIFFERENT
   category — do NOT use it. 24 scored → 5 excluded to reach 19 displayed. CLAUDE.md: bread provenance = real_bread_retail_003_v1.

## The score-provenance rule (HARD — this is where the last wave failed)
Do NOT trust `_meta.run_id`. Confirm the run by **score-provenance**: the run you choose must be the one whose
trace `final_score_estimate` values MATCH the live page product scores (barcode-by-barcode). If the obvious
run's scores don't match the live page, find the run that does (list the dirs under each category's
`bsip2_outputs/`), and report the mismatch. A run is correct only when its scores reproduce the live page.

## For EACH category
1. Find the matching BSIP1 corpus dir (pattern mirrors cereals: `03_operations/bsip1/<run>/output`; locate the one
   whose `bsip1_*.json` barcodes cover the run's traces). Set `corpus_dirs` to it.
2. Author `03_operations/page_generator/configs/<cat>.json` in the cereals shape: `category`, `corpus_dirs`,
   `run_products_dir`, `baseline_json` (= the live JSON above), `subpool_filter` (null unless one equality field
   cleanly separates the subpool), `dedup`, `exclusions` (every barcode in the run-universe but NOT on the live
   page, each with a concrete reason: `off_banned` / `out_of_scope: <why>` / `dedup` / `no_hebrew_name` / subpool),
   `extension_fields` (only those the live page actually carries), `boundary_policy`
   (`C:\Bari\01_framework\governance\grade_boundary_policy_v1.json`).
3. Generate to a NEW scratch file (NEVER overwrite live):
   `python 03_operations/page_generator/generate_page.py --config configs/<cat>.json --out configs/_generated_<cat>.json --timestamp 2026-06-16T00:00:00Z`
   Self-gate must PASS (exit 0).
4. Prove parity: the generated `products[]` vs the live page — same barcode SET, and for every shared barcode
   `score` identical and `grade` identical. Report counts: run-universe N, excluded N, generated N, live N, and
   score/grade mismatch count (target 0).

## Boundaries / guards
- **OFF ban (TASK-238):** any product whose corpus record carries an OFF marker → exclude with reason `off_banned`.
  If any displayed live product traces back to OFF, STOP and report it (launch blocker).
- **Never overwrite or edit any file under `bari-web/`** — live pages are read-only parity targets.
- Output ONLY: the 3 `configs/<cat>.json` files + 3 `configs/_generated_<cat>.json` scratch files. Touch no engine code.
- Do NOT publish, do NOT commit. **Do not close — propose RETURNED.**
- If a category cannot reach parity (no run reproduces the live scores), do NOT force it: report it as a finding
  with the score deltas, leave its config out, and continue with the others.

## Return format
Per category: chosen run (+ why, with the score-provenance evidence), corpus dir, config path, generated/excluded/
live counts, score-mismatch count, grade-mismatch count, self-gate exit code. Then a one-line verdict per category
(PARITY / DRIFT-FOUND / NO-MATCHING-RUN). End with the machine-readable return contract
(`01_framework/operations/return_contract_v1.md`): JSON with `task`, `proposed_status`, `artifacts[]` (path+action+sha256),
`counts{}` (per-category, trace-derived with the command that produced them), `commands_run[]` (cmd+exit_code),
`not_done[]`, `self_check`.
