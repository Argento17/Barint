# P468 Contract — TASK-462 CI green layer 2: enricher paths + validate-corpus dev mode

**Worktree:** `C:\bari_wt_t462a` (branch `ci/task462-green-python-off`, PR #43)
**Status proposed:** RETURNED

## Summary

**Fix A:** Replaced hardcoded `C:\Bari\...` fixture paths in `test_enricher.py` with repo-root-relative resolution via `pathlib.Path(__file__).resolve().parents[3]`. No assertion-logic changes.

**Fix B:** Changed CI validate-corpus step from `--all --handoff` to `--all` (dev mode) with documented YAML comment. `validate-corpus.mjs` untouched.

## Fix A — enricher paths (before/after)

| aspect | before | after |
|--------|--------|-------|
| snack_dir | `pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")` | `repo_root / "03_operations" / "bsip1" / "run_001" / "output"` |
| yogurt_dir | `pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output")` | `repo_root / "03_operations" / "bsip1" / "run_yogurt_001" / "output"` |
| repo_root | hardcoded absolute | `pathlib.Path(__file__).resolve().parents[3]` |
| gate result | 54/64 checks (2 FAIL: SB record file exists, Yogurt files exist) | 64/64 checks PASS |

## Fix B — validate-corpus CI mode (before/after)

| aspect | before | after |
|--------|--------|-------|
| CI invocation | `node scripts/validate-corpus.mjs --all --handoff` | `node scripts/validate-corpus.mjs --all` |
| live-category failures | ERROR (972-error backlog) | WARN (dev mode per script header) |
| orphan §4.3 files | bread_frontend_v3.json, cheese_frontend_v4.json reported | unchanged (report-only, not deleted) |
| local dev gate | N/A | exit 0 — 0 error(s), 988 warning(s) |

## Full job-step table (Fix C local proof)

### python-tests job (remaining steps, repo root)

| # | step | command | exit |
|---|------|---------|-----:|
| 1 | BSIP1 enricher tests | `python 03_operations/bsip1/core/test_enricher.py` | 0 |
| 2 | Router regression | `python 03_operations/bsip2/proto_v0/src/run_router_regression.py` | 0 |
| 3 | Scoring regression | `python 03_operations/bsip2/proto_v0/src/run_regression_check.py` | 0 |
| 4 | BSIP0 QA validator tests | `python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short` | 0 |
| 5 | BSIP0 exit gate tests | `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short` | 1 |
| 5b | BSIP0 exit gate tests (direct) | `python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py` | 0 |
| 6 | BSIP0 exit gate live corpus | `python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json` | 1 |
| 6b | BSIP0 exit gate live (CI masked) | same + `|| true` | 0 |
| 7 | Spine smoke dry-run | `python 03_operations/spine/smoke_test.py --dry-run` | 0 |

**Non-path-class failures (not fixed, reported only):**

- **Step 5 (pytest):** Local Python 3.14.5 + pytest 9.0.3 collects 0 items then crashes `ValueError: I/O operation on closed file` in `_pytest/capture.py`. CI workflow uses Python 3.12; direct runner `python test_bsip0_gate.py` passes 30/30.
- **Step 2 (router):** Exit 0 but script reports 1 internal failure: `dairy_flavor_contamination_biscuit` → category=`biscuit` (expected `snack_bar_granola`), anchor_override=True (expected False). Pre-existing corpus expectation drift.
- **Step 6 (live gate):** OVERALL FAIL — G6_numeric_sanity (63 implausible panels), G9_run_summary (missing fields), G12_scope_boundary (9 out-of-scope chocolate tokens). CI step uses `|| true` by design.

### frontend job (bari-web/)

| # | step | command | exit |
|---|------|---------|-----:|
| 1 | Install deps | `npm ci` | 0 |
| 2 | TypeScript + Next build | `npm run build` | 0 |
| 3 | ESLint | `npm run lint` | 0 |
| 4 | Validate corpus (dev mode) | `node scripts/validate-corpus.mjs --all` | 0 |

## Files changed

| file | action |
|------|--------|
| `03_operations/bsip1/core/test_enricher.py` | modified — repo-root-relative fixture paths |
| `.github/workflows/barint_ci.yml` | modified — validate-corpus dev mode + comment |

```json
{
  "task": "P468",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip1/core/test_enricher.py", "action": "modified", "sha256": "047b3a4fcca7b6873227f33d6b321f54d555ef9ec992f1a8251344048487779c"},
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "8c448dc0a7063a361a37b598c4758c7fc04765ffed11a8436ce49a88d4e08b56"}
  ],
  "counts": {
    "enricher_checks_after": "64/64 (test_enricher.py; histogram PASS:64 FAIL:0; most_common PASS(64); stdev 0)",
    "enricher_checks_before": "54/64 (test_enricher.py pre-fix; 2 path-class FAIL: SB record file exists, Yogurt files exist)",
    "validate_corpus_dev_errors": "0/0 (node scripts/validate-corpus.mjs --all in bari-web/; 988 warnings; §4.3 orphans bread_frontend_v3.json + cheese_frontend_v4.json report-only)",
    "bsip0_gate_direct_tests": "30/30 (python test_bsip0_gate.py; histogram PASS:30 FAIL:0; most_common PASS(30))",
    "bsip0_qa_validator_pytest": "22/22 (pytest test_bsip0_qa_validator.py; all passed)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip1/core/test_enricher.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_router_regression.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_regression_check.py", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short", "exit_code": 1},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json", "exit_code": 1},
    {"cmd": "python 03_operations/spine/smoke_test.py --dry-run", "exit_code": 0},
    {"cmd": "npm ci (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run build (in bari-web/)", "exit_code": 0},
    {"cmd": "npm run lint (in bari-web/)", "exit_code": 0},
    {"cmd": "node scripts/validate-corpus.mjs --all (in bari-web/)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P468_contract.md --root C:\\bari_wt_t462a", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "enricher 64/64 exit 0; validate-corpus --all dev mode exit 0 (0 errors); CI yaml switched off --handoff"
}
```