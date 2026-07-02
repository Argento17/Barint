# Return: P464

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P464_ci_green_python_off_grok.md` |
| Model | `grok/build-cli` |
| Started | 2026-07-02T15:36:06.281555+00:00 |
| Finished | 2026-07-02T15:39:47.733671+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P464 task prompt and follow its instructions below the separator.
Executing all three fixes: reading the relevant files and running the CI grep.
Writing the return contract, then committing and validating.
## P464 Return — TASK-462 CI green sweep (part 1)

**Proposed status:** RETURNED

### Fix 1 — python-tests fixture path
`03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py` — replaced hardcoded `C:\Bari\...` with repo-root-relative path via `__file__` (4 parents up → `02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json`).

**Verify:** `test_bsip0_nutrition.py:25-33` — `31 passed in 1.86s`, exit 0.

### Fix 2 — off-sweep literal marker
One grep hit: `bari-web/src/data/comparisons/granola_frontend_v2.json:18` (`_meta.excluded_off_products.reason`). Audit-trail metadata only — `excluded_off_products` is not read by any `.ts`/`.tsx` under `bari-web/src/`.

**Before:**
> OFF-sourced nutrition panels (panel_source=open_food_facts; run_cereals_carrefour_001 + run_cereals_yohananof_001) — TASK-238 OFF ban; removed from display per P35 sweep (off_sweep_v1.md). Source BSIP records retained, not erased. NOTE (TASK-377 2026-06-22): some of these barcodes were later RE-SOURCED from Shufersal (retailer=shufersal, source_traceability_status=resolved) and ARE displayed; their live nutrition is Shufersal-scraped, NOT OFF. This list records the historical OFF exclusion only — it is not a claim that currently-displayed products use OFF.

**After:**
> Third-party crowdsourced nutrition panels (panel_source=<the banned OFF database — TASK-238>; run_cereals_carrefour_001 + run_cereals_yohananof_001) — TASK-238 OFF ban; removed from display per P35 sweep (off_sweep_v1.md). Source BSIP records retained, not erased. NOTE (TASK-377 2026-06-22): some of these barcodes were later RE-SOURCED from Shufersal (retailer=shufersal, source_traceability_status=resolved) and ARE displayed; their live nutrition is Shufersal-scraped, NOT from the banned third-party database. This list records the historical exclusion only — it is not a claim that currently-displayed products use the banned source.

**Verify:** `granola_frontend_v2.json:18` — CI grep pattern returns 0 hits (exit 1 = clean). `barint_ci.yml` untouched.

### Fix 3 — dead-repo workflow
`git rm .github/workflows/argento_bari_ci.yml` — retired standalone-repo CI; permanently red on monorepo.

**Verify:** file absent at `.github/workflows/argento_bari_ci.yml`.

### Sanity pass (read-only)
| Command | Exit |
|---------|------|
| `python 03_operations/bsip1/core/test_enricher.py` | 0 (64/64) |
| `python 03_operations/bsip2/proto_v0/src/run_router_regression.py` | 0 (1 pre-existing FAIL logged) |
| `python 03_operations/bsip2/proto_v0/src/run_regression_check.py` | 0 (1 pre-existing WARN logged) |

### Files changed
| File | Action | SHA256 |
|------|--------|--------|
| `03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py` | modified | `8484e09e47267bc2b8de4988b3e319416db8ad77f3b93627287118a2bcaf02ba` |
| `bari-web/src/data/comparisons/granola_frontend_v2.json` | modified | `4a1700eeef02c4fc4f89f21b31c0e540cea5a830e6cef094711c5c478da17a53` |
| `.github/workflows/argento_bari_ci.yml` | deleted | — |
| `tasks/returns/P464_contract.md` | created | (self-referential; omitted) |

**Self-gate:** `validate_return.py --md tasks\returns\P464_contract.md --root C:\bari_wt_t462a` → exit 0. Tree clean; 4 commits on `ci/task462-green-python-off`; no push.

```json
{
  "task": "P464",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py", "action": "modified", "sha256": "8484e09e47267bc2b8de4988b3e319416db8ad77f3b93627287118a2bcaf02ba"},
    {"path": "bari-web/src/data/comparisons/granola_frontend_v2.json", "action": "modified", "sha256": "4a1700eeef02c4fc4f89f21b31c0e540cea5a830e6cef094711c5c478da17a53"},
    {"path": ".github/workflows/argento_bari_ci.yml", "action": "deleted", "sha256": ""},
    {"path": "tasks/returns/P464_contract.md", "action": "created", "sha256": ""}
  ],
  "counts": {
    "pytest_bsip0_nutrition_pass": "31/31 PASS (test_bsip0_nutrition.py; stdev 0; most_common PASS(31))",
    "off_sweep_hits_before_reword": "1/1 (grep -riE pattern over bari-web/src/data/; granola_frontend_v2.json:18 _meta.excluded_off_products.reason)",
    "off_sweep_hits_after_reword": "0/0 (same grep post-fix; exit 1 = clean)",
    "test_enricher_checks_pass": "64/64 PASS (test_enricher.py Results; stdev 0; most_common PASS(64))",
    "sanity_scripts_exit_zero": "3/3 (test_enricher.py + run_router_regression.py + run_regression_check.py)"
  },
  "commands_run": [
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short", "exit_code": 0},
    {"cmd": "python -c \"import pathlib,re,sys; pat=re.compile(r'openfoodfacts|open_food_facts|off_api|off_candidate_panel|openfoodfacts\\\\.org',re.I); hits=[(p,l) for p in pathlib.Path('bari-web/src/data').rglob('*') if p.is_file() for i,l in enumerate(p.read_text(encoding='utf-8',errors='replace').splitlines(),1) if pat.search(l)]; sys.exit(1 if not hits else 0)\"", "exit_code": 1},
    {"cmd": "python 03_operations/bsip1/core/test_enricher.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_router_regression.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_regression_check.py", "exit_code": 0},
    {"cmd": "git rm .github/workflows/argento_bari_ci.yml", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P464_contract.md --root C:\\bari_wt_t462a", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "python-tests: 31/31 pytest pass with repo-relative fixture path; off-sweep: grep returns 0 hits (exit 1); argento_bari_ci.yml deleted"
}
```
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
(clean)
```

### After dispatch

```
(clean)
```

### Delta

*(no changes detected)*
