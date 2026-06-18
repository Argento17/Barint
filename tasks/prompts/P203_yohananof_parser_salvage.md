(route: C1-CURSOR)

# P203 — Salvage TASK-247 Yohananof parser + tests onto master's parser

## Context
The Yohananof nutrition parser (in `03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`)
was hardened on the now-retiring local branch `task-247-yohananof-parser` (commit `376319982`,
"TASK-240 #4 / TASK-247"), but that work never reached master. Master's current
`bsip0_nutrition.py` (829 lines, from PR #18 / TASK-239) is **Victory-only** — it has zero
Yohananof handling. We are salvaging the Yohananof additions so the branch can be deleted.

This is OFF-free, legitimate direct-scrape parsing infrastructure (the test fixture is a real
yochananof.co.il page captured by direct scrape, NOT Open Food Facts). Do NOT introduce any
OFF dependency — OFF is banned project-wide (hard rule).

## Task
1. Diff master's `_shared/bsip0_nutrition.py` against `git show 376319982:03_operations/bsip0/scrape/_shared/bsip0_nutrition.py`.
2. Port ONLY the **Yohananof-specific additions** onto master's current parser:
   - `_find_yohananof_basis` (verbatim basis read; the real caption is "ל100 גרם", NO hyphen — never synthesize "ל-100 גרם")
   - `_parse_yohananof_nutrition` (unknown basis → `insufficient=True, rows=[]`; >1 numeric token rejects panel)
   - `_sniff_unit` mg detection across all quote forms (bare מג, gershayim מ״ג, ASCII מ"ג) — for Victory AND Yohananof
   - Do NOT revert or weaken any existing master Victory logic. Additive only; if a shared
     helper (e.g. `_sniff_unit`) already exists on master, merge the mg-quote-form handling
     into it rather than duplicating.
3. Bring over the test additions from `git show 376319982:03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py`
   and the real fixture `_shared/fixtures/yohananof_16000423534.html` (Nature Valley, barcode
   16000423534). The suite is a bare runner (NO pytest): run it with
   `python 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py`.
4. ALL tests must pass (target: the 31-test count from TASK-247, or current master count + the
   new Yohananof tests). Paste the full runner output.

## Hard constraints
- No OFF anywhere. No score changes (this is a parser library; no category is re-scored here).
- Additive to master's parser — do not drop Victory dual-table handling from PR #18.
- Branch from `origin/master`, name it `sweep/yohananof-parser-salvage`, commit, push.

## Return (self-verifying)
- The exact `git diff --numstat origin/master` for your branch.
- Full test-runner stdout (pass/fail count).
- Confirmation: `grep -rn "off\.get_product\|open_food_facts" 03_operations/bsip0/scrape/_shared/bsip0_nutrition.py` returns nothing.
- The push confirmation line.
