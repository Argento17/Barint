# P470 Contract — TASK-462 CI green layer 3: purge C:\Bari literals from CI-invoked Python paths

**Worktree:** `C:\bari_wt_t462a` (branch `ci/task462-green-python-off`, PR #43)
**Status proposed:** RETURNED

## Summary

Replaced hardcoded `C:\Bari\...` path literals on every `python-tests` CI execution path (direct workflow steps + one-level imports) with repo-root-relative `pathlib.Path(__file__).resolve().parents[N]` resolution. No threshold, assertion, or scoring logic changes.

## Static sweep — CI-invoked paths (14 files)

Direct workflow steps (`.github/workflows/barint_ci.yml` `python-tests` job) plus one-level imports:

`test_bsip0_nutrition.py`, `bsip0_nutrition.py`, `test_enricher.py`, `ingredient_enricher.py`, `run_router_regression.py`, `run_regression_check.py`, `structural_classifier.py`, `router_v2.py`, `test_bsip0_qa_validator.py`, `bsip0_qa_validator.py`, `test_bsip0_gate.py`, `bsip0_gate.py`, `smoke_test.py`, `spine_db.py`

### Before fix (execution-path literals)

| file:line | literal | action |
|-----------|---------|--------|
| `run_regression_check.py:27` | `CORPUS_PATH = pathlib.Path(r"C:\Bari\01_framework\...\golden_corpus_manifest.json")` | **fixed** → `_REPO_ROOT / "01_framework/bsip2_framework/validation/golden_corpus/golden_corpus_manifest.json"` (`parents[4]`) |
| `run_regression_check.py:28` | `REPORT_ROOT = pathlib.Path(r"C:\Bari\03_operations\reports\regression")` | **fixed** → `_REPO_ROOT / "03_operations/reports/regression"` |
| `run_router_regression.py:28` | `REPORT_ROOT = pathlib.Path(r"C:\Bari\03_operations\reports\regression")` | **fixed** → `_REPO_ROOT / "03_operations/reports/regression"` (`parents[4]`) |
| `ingredient_enricher.py:489` | `BSIP0_YOHANANOF = pathlib.Path(r"C:\Bari\03_operations\bsip0\scrape\yohananof\outputs\yohananof")` | **fixed** → `_REPO_ROOT / "03_operations/bsip0/scrape/yohananof/outputs/yohananof"` (`parents[3]`) |

### Before fix (docstring-only, not execution path — not fixed)

| file:line | literal | action |
|-----------|---------|--------|
| `test_bsip0_qa_validator.py:6` | `python -m pytest C:/Bari/...` (module docstring usage example) | **not fixed** — docstring only |
| `test_bsip0_qa_validator.py:8` | `python C:/Bari/...` (module docstring usage example) | **not fixed** — docstring only |

### After fix (`git grep` on CI paths)

```
=== C:\\Bari ===  (0 matches)
=== C:/Bari ===
03_operations/bsip0/validators/test_bsip0_qa_validator.py:6:    python -m pytest C:/Bari/...
03_operations/bsip0/validators/test_bsip0_qa_validator.py:8:    python C:/Bari/...
=== c:\\Bari ===  (0 matches)
=== c:/Bari ===   (0 matches)
```

**Execution-path literal count:** 0/0 post-fix (docstring-only hits excluded; `ci_path_literals_fixed: 4/4`)

## Fixes applied

| file | change |
|------|--------|
| `03_operations/bsip2/proto_v0/src/run_regression_check.py` | `_REPO_ROOT = Path(__file__).resolve().parents[4]`; repo-relative `CORPUS_PATH` + `REPORT_ROOT` |
| `03_operations/bsip2/proto_v0/src/run_router_regression.py` | `_REPO_ROOT = Path(__file__).resolve().parents[4]`; repo-relative `REPORT_ROOT` |
| `03_operations/bsip1/core/ingredient_enricher.py` | `_REPO_ROOT = Path(__file__).resolve().parents[3]`; repo-relative `BSIP0_YOHANANOF` |

## python-tests job — local proof (all workflow steps)

| # | step | command | exit |
|---|------|---------|-----:|
| 1 | BSIP0 nutrition tests | `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short` | 0 |
| 2 | BSIP1 enricher tests | `python 03_operations/bsip1/core/test_enricher.py` | 0 |
| 3 | Router regression | `python 03_operations/bsip2/proto_v0/src/run_router_regression.py` | 0 |
| 4 | Scoring regression | `python 03_operations/bsip2/proto_v0/src/run_regression_check.py` | 0 |
| 5 | BSIP0 QA validator tests | `python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short` | 0 |
| 6 | BSIP0 exit gate tests (pytest) | `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short` | 1 |
| 6b | BSIP0 exit gate tests (direct) | `python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py` | 0 |
| 7 | BSIP0 exit gate live corpus | `python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json` | 1 |
| 7b | BSIP0 exit gate live (CI masked) | same + `\|\| true` | 0 |
| 8 | Spine smoke dry-run | `python 03_operations/spine/smoke_test.py --dry-run` | 0 |

### Regression check — corpus load proof

- Corpus loaded from: `C:\bari_wt_t462a\01_framework\bsip2_framework\validation\golden_corpus\golden_corpus_manifest.json`
- Report written to: `C:\bari_wt_t462a\03_operations\reports\regression\regression_check_001.md`
- Result: 12 entries checked; 11 PASS, 1 WARN (`anchor_soy_drink`), 0 FAIL

### Router regression — TASK-453 backlog note (report-only, no fix)

Exit 0 but internal failure count = 1:

- **Failing case:** `dairy_flavor_contamination_biscuit`
- **Issue:** `category='biscuit'` (expected `'snack_bar_granola'`); `anchor_override=True` (expected `False`)
- Report: `03_operations/reports/regression/router_regression_001.md`

### Non-path-class failures (not fixed, reported only)

- **Step 6 (pytest):** Local Python 3.14.5 + pytest 9.0.3 collects 0 items then crashes `ValueError: I/O operation on closed file` in `_pytest/capture.py`. CI uses Python 3.12; direct runner passes 30/30.
- **Step 7 (live gate):** OVERALL FAIL — G6_numeric_sanity (63 implausible panels), G9_run_summary (missing fields), G12_scope_boundary (9 out-of-scope chocolate tokens). CI step uses `|| true` by design.

## Backlog — C:\Bari literals outside CI paths (not fixed)

Representative sample from repo-wide `git grep` (full set deferred to future purge passes):

| file:line | context |
|-----------|---------|
| `03_operations/spine/dual_extract.py:39` | `REPO_ROOT = Path("C:/Bari")` |
| `03_operations/bsip2/proto_v0/src/p75_no_regression.py:4` | `ROOT = pathlib.Path(r"C:/Bari")` |
| `03_operations/bsip2/proto_v0/src/p75b_gate.py:3` | `ROOT = pathlib.Path(r"C:/Bari")` |
| `03_operations/bsip2/proto_v0/src/p99_shelf_relative_guards.py:3` | `ROOT = pathlib.Path(r"C:/Bari")` |
| `01_framework/bsip2_framework/project_rescore/spread_analysis_runner.py:312-398` | category corpus paths + out_path |
| `tasks/new_task.py:6-25` | registry docstring examples |
| `scripts/run_final_verification.py:5-7` | frontend JSON paths |
| `99_archive/command_center_retired_2026-06-13/*.py` | archived tooling (multiple) |

```json
{
  "task": "P470",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip2/proto_v0/src/run_regression_check.py", "action": "modified", "sha256": "efa454c1fe8105f904808a519a78223e90800db10d71b28eea88ad0808e05e5b"},
    {"path": "03_operations/bsip2/proto_v0/src/run_router_regression.py", "action": "modified", "sha256": "b235efbda4004c0d4ba31e9f8857e3dd84057aa7681181b124f0a5db280dd753"},
    {"path": "03_operations/bsip1/core/ingredient_enricher.py", "action": "modified", "sha256": "9ff9c3aa9c39f7e0b620983ccd87db45292cdccc915cabe7b592a425426306c2"}
  ],
  "counts": {
    "ci_path_literals_before": "4/4 (git grep on 14 CI-invoked Python files; execution-path literals only)",
    "ci_path_literals_after": "0/0 (git grep post-fix on 14 CI-invoked Python files; docstring-only hits in test_bsip0_qa_validator.py excluded)",
    "ci_path_literals_fixed": "4/4 (run_regression_check.py:27-28, run_router_regression.py:28, ingredient_enricher.py:489)",
    "regression_corpus_entries": "12/12 (run_regression_check.py; histogram PASS:11 WARN:1 FAIL:0 SKIP:0; most_common PASS(11); stdev 0.29)",
    "enricher_checks": "64/64 (test_enricher.py; histogram PASS:64 FAIL:0; most_common PASS(64); stdev 0)",
    "bsip0_nutrition_pytest": "31/31 (pytest test_bsip0_nutrition.py; all passed)",
    "bsip0_qa_validator_pytest": "22/22 (pytest test_bsip0_qa_validator.py; all passed)",
    "bsip0_gate_direct_tests": "30/30 (python test_bsip0_gate.py; histogram PASS:30 FAIL:0; most_common PASS(30))"
  },
  "commands_run": [
    {"cmd": "git grep C:\\\\Bari -- <14 CI Python files> (pre-fix)", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_nutrition.py -v --tb=short", "exit_code": 0},
    {"cmd": "python 03_operations/bsip1/core/test_enricher.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_router_regression.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_regression_check.py", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/validators/test_bsip0_qa_validator.py -v --tb=short", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short", "exit_code": 1},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json", "exit_code": 1},
    {"cmd": "python 03_operations/spine/smoke_test.py --dry-run", "exit_code": 0},
    {"cmd": "git grep C:\\\\Bari -- <14 CI Python files> (post-fix)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P470_contract.md --root C:\\bari_wt_t462a", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "post-fix CI-path literal sweep = 0 execution-path hits; run_regression_check.py loads corpus from repo-relative path and writes report to 03_operations/reports/regression/regression_check_001.md exit 0"
}
```