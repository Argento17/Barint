# Return: P470

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P470_ci_green_layer3_grok.md` |
| Model | `grok/build-cli` |
| Started | 2026-07-02T16:17:45.867465+00:00 |
| Finished | 2026-07-02T16:25:41.290321+00:00 |
| Exit code | 0 |

---

## Output

```
I'll read the P470 task prompt and execute it per the instructions below the separator.
Reading the files to fix and mapping CI-invoked Python paths.
Checking CI-invoked Python files and their one-level imports for `C:\Bari` literals.
Checking for an example return contract and applying fixes.
Found another CI-path literal in `ingredient_enricher.py`; inspecting and fixing it.
Fixing the `C:\Bari` literal in `ingredient_enricher.py` on the CI import path.
Gathering file hashes and checking git status before writing the return contract.
Removing the self-referential contract entry from artifacts, matching prior contracts.
## P470 — RETURNED

Purged hardcoded `C:\Bari` path literals from all `python-tests` CI execution paths. The Linux `FileNotFoundError` in `run_regression_check.py` is fixed.

### Files changed

| File | Change |
|------|--------|
| `03_operations/bsip2/proto_v0/src/run_regression_check.py:27-29` | `_REPO_ROOT = parents[4]`; repo-relative `CORPUS_PATH` + `REPORT_ROOT` |
| `03_operations/bsip2/proto_v0/src/run_router_regression.py:27-29` | `_REPO_ROOT = parents[4]`; repo-relative `REPORT_ROOT` |
| `03_operations/bsip1/core/ingredient_enricher.py:488-489` | `_REPO_ROOT = parents[3]`; repo-relative `BSIP0_YOHANANOF` (CI import path via `test_enricher.py`) |
| `tasks/returns/P470_contract.md` | Return contract (validate_return exit 0) |

### Verify at file:line

- `run_regression_check.py:27-29` — no `C:\Bari`; corpus resolves to `01_framework/bsip2_framework/validation/golden_corpus/golden_corpus_manifest.json`
- `run_router_regression.py:28-29` — report writes under `03_operations/reports/regression/` (not a literal `C:\Bari\...` dirname on Linux)
- `ingredient_enricher.py:488-489` — `BSIP0_YOHANANOF` is repo-relative

### Static sweep (CI paths, post-fix)

**0 execution-path literals.** Only docstring hits remain in `test_bsip0_qa_validator.py:6,8` (usage examples, not executed).

### Local gates

| Command | Exit |
|---------|-----:|
| `run_regression_check.py` | 0 — corpus loaded, report at `03_operations/reports/regression/regression_check_001.md` |
| `run_router_regression.py` | 0 |
| All other `python-tests` steps | 0 (except pre-existing pytest 3.14 capture bug on gate tests; live gate exit 1 masked by `\|\| true`) |

### TASK-453 backlog (report-only)

Router regression exits 0 but reports **1 failure**: `dairy_flavor_contamination_biscuit` → `category='biscuit'` (expected `'snack_bar_granola'`), `anchor_override=True` (expected `False`).

Pushed to `ci/task462-green-python-off` (PR #43). Final acceptance = CI green on Linux runner.

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
    "ci_path_literals_fixed": "4/4 (run_regression_check.py:27-28, run_router_regression.py:28, ingredient_enricher.py:489)",
    "ci_path_literals_after": "0/0 (git grep post-fix on 14 CI-invoked Python files)",
    "regression_corpus_entries": "12/12 (PASS:11 WARN:1 FAIL:0)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip2/proto_v0/src/run_regression_check.py", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P470_contract.md --root C:\\bari_wt_t462a", "exit_code": 0},
    {"cmd": "git push", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "post-fix CI-path literal sweep = 0 execution-path hits; regression check loads corpus and writes report exit 0"
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
?? terminals/
```

### Delta

### New / modified since dispatch
  ?? terminals/
