# P464 / TASK-462 CI green sweep, part 1: python-tests fixture path + off-sweep marker + dead-repo workflow (route: C1-GROK)

## 1. Context / baseline
- You are ALREADY in isolated worktree `C:\bari_wt_t462a`, branch `ci/task462-green-python-off`, cut from origin/master `b632f9c6`. Repo root = this worktree. Never touch `C:\Bari` (read-only for reference). Commit here; NO push/PR/deploy.
- Every push to master and every PR shows 3 red GitHub-Actions checks from `.github/workflows/barint_ci.yml` plus a permanently-red `argento_bari_ci.yml`. You fix two of the three + delete the dead workflow. (ESLint is a separate lane — do NOT touch any `.ts`/`.tsx` file.)
- Evidence from CI run 28601493400 (PR #37, and identical on master pushes):
  - `python-tests` job, step "BSIP0 nutrition tests (20)": 3 tests fail with `FileNotFoundError: C:\\Bari\\02_products\\breakfast_cereals\\bsip0_outputs\\cereals_bsip0_raw_20260601T152207.json` — the test file `03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py` (lines ~25-28) hardcodes a Windows-absolute `C:\Bari\...` path. The fixture EXISTS in the repo at the repo-relative path `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json` (blob dbc94a44 on master) — the Linux runner just can't see `C:\`.
  - `off-sweep` job: the grep `openfoodfacts|open_food_facts|off_api|off_candidate_panel|openfoodfacts\.org` over `bari-web/src/data/` matches `bari-web/src/data/comparisons/granola_frontend_v2.json` line ~18 — a `"reason"` string on the HISTORICAL exclusion list documenting that products were REMOVED because OFF-sourced (TASK-238). It is a record of the ban being enforced, not an OFF dependency.

## 2. Objective — make `python-tests` and `off-sweep` pass without weakening any gate
**Fix 1 — test fixture path.** In `03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py`, replace the hardcoded `CEREALS_RAW` Windows path with a repo-root-relative resolution derived from `__file__` (the test file sits at `03_operations/bsip0/scrape/_shared/`, so repo root = 4 parents up; join `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json`). No skip-if-missing, no logic change to any assertion — the fixture is in the repo; the tests must actually RUN and PASS. Gate: `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short` exit 0, all 31 collected tests pass (CI showed 3 failed / 28 passed).

**Fix 2 — off-sweep literal marker.** Run the EXACT CI grep locally first and enumerate ALL hits:
`grep -riE "openfoodfacts|open_food_facts|off_api|off_candidate_panel|openfoodfacts\.org" bari-web/src/data/`
For each hit that is a historical-exclusion/audit-trail NOTE (like the granola `"reason"` string): reword the string so it no longer contains any literal banned marker while keeping the exact meaning and all traceability (e.g. `panel_source=open_food_facts` → `panel_source=<the banned OFF database — TASK-238>` phrased naturally; keep run ids, dates, TASK references intact). **Do NOT touch the workflow file `barint_ci.yml` — the gate's grep stays at full strength, byte-identical.** If ANY hit is in a live data-bearing field (a displayed product's provenance/panel_source/nutrition source rather than an exclusion note): STOP, report it precisely, propose BLOCKED — that would be a real OFF dependency = launch blocker, not a rewording job.
Also verify the field you edit is not consumer-rendered: grep `bari-web/src` (outside `data/`) for the JSON key path that holds the reason string and report where/whether it is read. Gate: the exact CI grep returns 0 hits (exit 1 from grep = clean).

**Fix 3 — dead-repo workflow.** `git rm .github/workflows/argento_bari_ci.yml`. It targets the RETIRED standalone-repo layout (root `package.json`, `src/**` — see its `cache-dependency-path: package-lock.json`, which does not exist at the monorepo root), so it fails on every master push and can never pass. Deploy topology law: Argento17/bari is DEAD. Do not touch the other three workflows.

**Sanity pass (read-only):** run the other python-tests steps locally and report exit codes (do not fix anything in them; they passed in CI): `python 03_operations/bsip1/core/test_enricher.py`, `python 03_operations/bsip2/proto_v0/src/run_router_regression.py`, `python 03_operations/bsip2/proto_v0/src/run_regression_check.py`.

## 3. Boundaries
- OFF ban absolute (TASK-238); Fix 2 STRENGTHENS enforcement hygiene, never weakens the grep.
- FREEZE: do not modify any product description field (rowVerdict/insightLine/expansion) — owner project in flight. The exclusion-list `"reason"` metadata string is NOT a product description; touch ONLY that string (and any sibling hits of the same audit-trail kind).
- No `.ts`/`.tsx`/lint changes (separate lane). No invented data. No push/PR.
- You are the EXECUTOR of this task. Do NOT spawn any subagents; do every step yourself with your own tools.

## 4. Return
Write to `tasks\returns\P464_contract.md` (NOT P464_return.md — the router overwrites that path): per-fix description, the full before/after of the reworded reason string(s), the pytest summary line, the grep-clean proof, exit codes for every command, real sha256 for every touched file, counts with denominators. Full Return Contract v1 JSON. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P464_contract.md --root C:\bari_wt_t462a` exit 0 (run from PowerShell, not Git Bash). Commit code + contract (separate commits fine). Leave tree clean. Propose RETURNED (or BLOCKED per Fix 2).
