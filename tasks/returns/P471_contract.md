# P471 Contract — TASK-462 CI green layer 4: bsip0_gate stdout-rewrap + CI step alignment

**Worktree:** `C:\bari_wt_t462a` (branch `ci/task462-green-python-off`, PR #43)
**Status proposed:** RETURNED

## Summary

Guarded import-time `sys.stdout` rewrap in `bsip0_gate.py` so pytest capture teardown no longer crashes. Aligned CI step "BSIP0 exit gate tests (30)" with the file's bare-runner design (direct `python test_bsip0_gate.py`, matching enricher convention). No test-assertion, data, or scoring changes.

## Fix 1 — stdout rewrap guard (`bsip0_gate.py:48`)

### Before (bsip0_gate.py:48)

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

### After (bsip0_gate.py:48-52)

    if hasattr(sys.stdout, "buffer") and (getattr(sys.stdout, "encoding", "") or "").lower() not in ("utf-8", "utf8"):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

## Fix 2 — CI step alignment (`.github/workflows/barint_ci.yml:74-75`)

### Before (barint_ci.yml:74-75)

    - name: BSIP0 exit gate tests (30)
      run: python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short

### After (barint_ci.yml:74-75)

    - name: BSIP0 exit gate tests (30)
      run: python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py

`test_bsip0_gate.py` `__main__` block (lines 324-339) exits `sys.exit(1 if failed else 0)` — nonzero on failure confirmed; no runner fix needed.

## Rewrap-occurrence sweep — `sys.stdout = io.TextIOWrapper` under `03_operations/`

| file:line | CI-invoked test import? | action |
|-----------|-------------------------|--------|
| `03_operations/bsip0/scrape/_shared/bsip0_gate.py:48` | **yes** (`test_bsip0_gate.py` imports it) | **guarded** (Fix 1) |
| `03_operations/tools/validate_insight_lines.py:40` | no | listed only |
| `03_operations/tools/patch_maadanim_grades.py:3` | no | listed only |
| `03_operations/page_generator/regen_d4_additives_display.py:28` | no | listed only |
| `03_operations/spine/dual_extract.py:33` | no | listed only |
| `03_operations/seo/run_all_faq_schemas.py:17` | no | listed only |
| `03_operations/seo/generate_faq_schema.py:25` | no | listed only |
| `03_operations/router/dispatch.py:80` | no | listed only |
| `03_operations/bsip2/proto_v0/src/batch_run_cereals_007_sodium_off.py:58` | no | listed only |
| `03_operations/bsip2/proto_v0/src/analyze_sodium_independence_189.py:23` | no | listed only |
| `03_operations/bsip2/proto_v0/src/enrich_salty_snacks_bsip1.py:8` | no | listed only |
| `03_operations/bsip2/proto_v0/src/generate_frozen_vegetables_frontend.py:3` | no | listed only |
| `03_operations/bsip2/proto_v0/src/build_cereals_multiretailer_frontend.py:15` | no | listed only |
| `03_operations/bsip2/proto_v0/src/build_yogurt_cheese_multiretailer_frontend.py:17` | no | listed only |
| `03_operations/bsip2/proto_v0/src/build_cereals_008_frontend.py:23` | no | listed only |
| `03_operations/bsip2/proto_v0/src/build_salty_snacks_frontend_v2.py:6` | no | listed only |
| `03_operations/bsip2/proto_v0/src/build_salty_snacks_frontend.py:6` | no | listed only |
| `03_operations/bsip2/proto_v0/src/run_ecs_integration.py:13` | no | listed only |
| `03_operations/bsip2/proto_v0/src/run_confidence_annotation_pass.py:18` | no | listed only |
| `03_operations/bsip2/proto_v0/src/run_cereals_007_delta_table.py:12` | no | listed only |
| `03_operations/bsip2/proto_v0/src/run_ev006_regression.py:12` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_yogurt/test_bsip1_yogurt_006_fixes.py:24` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/rescraper/resolve_salty_images.py:17` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/02_scrape_shufersal_v2.py:10` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/01_scrape_shufersal_frozen_vegetables.py:10` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/04_scope_cleanup_v3.py:6` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/03_post_process_v2.py:6` | no | listed only |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/05_bsip0_gate.py:43` | no | listed only |

**CI-path modules checked (14 files from P470):** `test_bsip0_nutrition.py`, `bsip0_nutrition.py`, `test_enricher.py`, `ingredient_enricher.py`, `run_router_regression.py`, `run_regression_check.py`, `structural_classifier.py`, `router_v2.py`, `test_bsip0_qa_validator.py`, `bsip0_qa_validator.py`, `test_bsip0_gate.py`, `bsip0_gate.py`, `smoke_test.py`, `spine_db.py` — only `bsip0_gate.py` had the rewrap on a CI import path.

## P470 static literal sweep (re-run)

    === C:\\Bari ===  (0 matches)
    === C:/Bari ===
    03_operations/bsip0/validators/test_bsip0_qa_validator.py:6:    python -m pytest C:/Bari/...
    03_operations/bsip0/validators/test_bsip0_qa_validator.py:8:    python C:/Bari/...
    === c:\\Bari ===  (0 matches)
    === c:/Bari ===   (0 matches)

**Execution-path literal count:** 0/0 post-fix (docstring-only hits excluded; unchanged from P470)

## Proof commands

| # | step | command | exit |
|---|------|---------|-----:|
| 1 | BSIP0 gate direct runner | `python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py` | 0 |
| 2 | BSIP0 gate pytest (informative, Fix 1) | `python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short` | 0 |
| 3 | BSIP0 exit gate live corpus | `python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json` | 1 |
| 3b | Live corpus (CI masked) | same + `\|\| true` | 0 |
| 4 | Spine smoke dry-run | `python 03_operations/spine/smoke_test.py --dry-run` | 0 |
| 5 | P470 static literal sweep | `git grep` on 14 CI Python files (4 case variants) | 0 |

### Gate test results

- **Direct runner:** 30 passed, 0 failed (30/30; histogram PASS:30 FAIL:0; most_common PASS(30); stdev 0)
- **pytest (Python 3.14.5, post Fix 1):** collected 30 items, 30 passed in 36.11s — no longer crashes (`collected 0` + `ValueError: I/O operation on closed file` resolved)
- **Live corpus gate:** OVERALL FAIL (G6_numeric_sanity 63 implausible, G9_run_summary missing fields, G12_scope_boundary 9 out-of-scope) — CI masks with `|| true` by design
- **Spine smoke:** PASS (0 hard failures, 0 freshness findings; 6 manifest entries, 7 routes)

```json
{
  "task": "P471",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip0/scrape/_shared/bsip0_gate.py", "action": "modified", "sha256": "3473abd8b83bf50184b4f12d56da3512fd42b814c3bd5a0ea1b1b4e6f3b11f4a"},
    {"path": ".github/workflows/barint_ci.yml", "action": "modified", "sha256": "a8786941ab8203d742f80b4fc7f0e4158672e97b6a4c94e1c5db9c0fd723561b"}
  ],
  "counts": {
    "stdout_rewrap_occurrences_03_operations": "28/28 (git grep sys.stdout = io.TextIOWrapper under 03_operations/)",
    "stdout_rewrap_ci_import_path": "1/1 (bsip0_gate.py imported by test_bsip0_gate.py; guarded)",
    "stdout_rewrap_guarded": "1/1 (bsip0_gate.py:48)",
    "bsip0_gate_direct_tests": "30/30 (python test_bsip0_gate.py; histogram PASS:30 FAIL:0; most_common PASS(30); stdev 0)",
    "bsip0_gate_pytest_post_fix": "30/30 (pytest test_bsip0_gate.py Python 3.14.5; collected 30 passed 30)",
    "ci_path_literals_after": "0/0 (git grep post-fix on 14 CI-invoked Python files; docstring-only hits in test_bsip0_qa_validator.py excluded)",
    "spine_smoke_routes": "7/7 (smoke_test.py --dry-run; PASS:7 DRY-RUN:7 FAIL:0)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py", "exit_code": 0},
    {"cmd": "python -m pytest 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py -v --tb=short", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/scrape/_shared/bsip0_gate.py 02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260601T152207.json", "exit_code": 1},
    {"cmd": "python 03_operations/spine/smoke_test.py --dry-run", "exit_code": 0},
    {"cmd": "git grep C:\\\\Bari -- <14 CI Python files> (P470 re-sweep)", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\validate_return.py --md tasks\\returns\\P471_contract.md --root C:\\bari_wt_t462a", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "bsip0_gate direct runner 30/30 exit 0; CI step now uses direct runner; pytest collects 30 post Fix 1; P470 literal sweep 0 execution-path hits"
}
```