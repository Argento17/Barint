# TASK-566 Return Block — http.py shadow rename + grammar gate fail-loud

**Agent:** Data Agent (claude-sonnet-4-6)
**Date:** 2026-07-11
**Branch:** task506 (no commit, live tree edits)

---

## Work Performed

### Fix 1: Rename `integrations/clients/http.py` → `http_client.py`

**Root cause confirmed:** When `integrations/clients/` is on `sys.path[0]`, the file `http.py`
in that directory shadows the stdlib `http` package. Any subsequent `import http.client`
(done by urllib, which is done by transformers) fails with:
`ModuleNotFoundError: No module named 'http.client'; 'http' is not a package`

**Pre-fix shadow reproduction:**
```
Command: python -c "import sys; sys.path.insert(0, 'integrations/clients'); import http; import http.client"
Exit code: 1
Error: ModuleNotFoundError: No module named 'http.client'; 'http' is not a package
```

**Action taken:**
- Renamed `integrations/clients/http.py` → `integrations/clients/http_client.py` (content unchanged)
- Deleted the old `http.py`
- Updated ALL importers (found by grep over full live tree, excluding .venv, node_modules, tasks/, .git):
  - `integrations/clients/biorxiv.py` — `from .http import` → `from .http_client import`
  - `integrations/clients/analytics.py` — same
  - `integrations/clients/usda_fdc.py` — same
  - `integrations/clients/figma.py` — same
  - `integrations/clients/literature.py` — `from .http import get, get_json` → `from .http_client import`
  - `integrations/clients/tzameret.py` — `from .http import get_json` → `from .http_client import`
  - `integrations/clients/dsld.py` — same
  - `integrations/clients/il_prices.py` — `from .http import get` → `from .http_client import`
  - `integrations/clients/pagespeed.py` — `from .http import get_json` → `from .http_client import`
  - `integrations/clients/open_food_facts.py` — `from .http import HttpError, get_json` → `from .http_client import`
  - `integrations/clients/crossref.py` — same
  - `integrations/clients/pubchem.py` — same
  - `integrations/clients/openfda.py` — same
  - `integrations/clients/search_console.py` — `from .http import USER_AGENT, HttpError` → `from .http_client import`
  - `integrations/clients/semantic_scholar.py` — `from .http import HttpError, get_json` → `from .http_client import`
  - `03_operations/validators/verify_citations.py:74` — `from integrations.clients.http import HttpError` → `from integrations.clients.http_client import HttpError`
  - Total: 16 importer files updated

**Grep hits in tasks/ and .md files** (not code, no action needed):
  - `tasks/TASK-584.md` — historical record, mentions old import path — documentation only, not code
  - `03_operations/reports/research/magnesium_form_ladder_verification_v1.md` — command log in a report, not live code

**Post-fix verification:**
```
Command: python -c "import sys; sys.path.insert(0, 'integrations/clients'); import http; import http.client; print(http.__file__)"
Exit code: 0
Output: C:\Python314\Lib\http\__init__.py
```

### Fix 2: Grammar gate fail-loud

**Root cause per task:** `_load_model()` raised `RuntimeError` on `ImportError`, but:
1. `run_evals.py:_load_grammar_gate()` caught `except Exception` and returned `None` silently
2. With `--with-grammar` requested and the gate erroring, `grammar_analyze` was `None`
3. The gate silently didn't run; no per-string `gram_clean` entries were written
4. Caller couldn't distinguish "gate ran, all clean" from "gate didn't run"

**Changes to `integrations/clients/hebrew_grammar_gate.py` (v1.0 → v1.1):**
- Added `GateDidNotRunError(RuntimeError)` — a DISTINCT exception class with:
  - `SENTINEL_PREFIX = "ERROR / GATE-DID-NOT-RUN: hebrew_grammar_gate"` — log-scannable
  - All error paths in `_load_model()` now raise `GateDidNotRunError` (not plain `RuntimeError`)
  - Both `ImportError` and unexpected exceptions are caught and re-raised as `GateDidNotRunError`
- Added `gate_status() -> tuple[str, str | None]` — a probe function callers can use to
  fail fast before iterating a corpus without catching `analyze()` errors
- `analyze()` propagates `GateDidNotRunError` unchanged — it will NOT return `GrammarReport(is_clean=True)`
  when the gate failed to load

**Changes to `03_operations/evals/copy_evals/run_evals.py`:**
- `_load_grammar_gate(required: bool = False)` now takes a `required` parameter
- When `required=True` (i.e. `--with-grammar` was passed) and the gate fails:
  - Prints `ERROR / GATE-DID-NOT-RUN:` to stderr
  - Returns `None` (NOT a callable)
- `main()` now checks: `if args.with_grammar and grammar_analyze is None: return 1`
  — hard-fails with exit code 1 instead of silently running readability-only

**Caller audit for `_gate_run_379.py` and `_gate_run_379_efsa.py`:**
- These files do `import integrations.clients.hebrew_grammar_gate as gg` inside `if RUN_GRAMMAR:`
  WITHOUT a try/except — they already fail loud on ImportError (unhandled exception = crash)
- No swallow-and-continue pattern present; no changes needed

**`hebrew_readability.py` audit:**
- Pure stdlib, no transformers/torch dependency — no environment-failure mode of this class exists
- No changes needed

### Regression Test Added

`integrations/clients/tests/test_task566_regressions.py` — 7 tests:
- `test_no_http_shadow_file` — asserts `http.py` does not exist under clients/
- `test_http_client_exists` — asserts `http_client.py` exists and is importable
- `test_stdlib_http_not_shadowed_by_clients_dir` — inserts clients dir on sys.path[0] and asserts stdlib http works
- `test_gate_did_not_run_error_is_distinct` — asserts `GateDidNotRunError` is importable and has correct sentinel
- `test_load_model_raises_gate_error_on_import_failure` — simulates ImportError, asserts `GateDidNotRunError` raised
- `test_analyze_propagates_gate_did_not_run_error` — asserts `analyze()` propagates not swallows the error
- `test_run_evals_load_grammar_gate_required_fails_loud` — asserts `_load_grammar_gate(required=True)` returns None and prints to stderr

---

## Verification Results

| Check | Exit Code | Result |
|---|---|---|
| Pre-fix shadow reproduction | 1 | CONFIRMED: `http.client` not importable |
| Post-rename stdlib http import | 0 | PASS: `http.__file__` = Python stdlib |
| All 16 importer modules import cleanly | 0 | PASS |
| `verify_citations.py --selftest` | 1 | 6/7 pass (TC-1 failure is PRE-EXISTING, not introduced by rename — confirmed by testing with stashed original code which also fails TC-1) |
| `gate_status()` returns `("ok", None)` | 0 | PASS — transformers+torch operational |
| `GateDidNotRunError` sentinel correct | 0 | PASS |
| New regression tests (7/7) | 0 | PASS |
| Pre-existing tests (6/6 in test_literature.py) | 0 | PASS |
| Full test suite (13/13 tests) | 0 | PASS |

**Note on TC-1:** The `verify_citations.py --selftest` TC-1 failure ("no parseable author/year in context — conservative pass") is pre-existing — confirmed by stashing my changes and running the original unmodified code, which also fails TC-1 with identical output. This is a pre-existing selftest correctness bug in the author-corroboration heuristic, unrelated to the http.py rename (TASK-566 scope is the rename and gate loudness only).

---

## Files Touched

### Created
- `integrations/clients/http_client.py` (renamed from http.py)
- `integrations/clients/tests/test_task566_regressions.py` (new regression test)

### Modified
- `integrations/clients/biorxiv.py`
- `integrations/clients/analytics.py`
- `integrations/clients/usda_fdc.py`
- `integrations/clients/figma.py`
- `integrations/clients/literature.py`
- `integrations/clients/tzameret.py`
- `integrations/clients/dsld.py`
- `integrations/clients/il_prices.py`
- `integrations/clients/pagespeed.py`
- `integrations/clients/open_food_facts.py`
- `integrations/clients/crossref.py`
- `integrations/clients/pubchem.py`
- `integrations/clients/openfda.py`
- `integrations/clients/search_console.py`
- `integrations/clients/semantic_scholar.py`
- `integrations/clients/hebrew_grammar_gate.py`
- `03_operations/validators/verify_citations.py`
- `03_operations/evals/copy_evals/run_evals.py`

### Deleted
- `integrations/clients/http.py` (renamed; original deleted)

---

```json
{
  "task": "TASK-566",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "integrations/clients/http_client.py", "action": "created", "sha256": "7f2a491c87414becfc6c9cba4b643f4a4ab4c40397a0db98ebb37c8c41eba927"},
    {"path": "integrations/clients/biorxiv.py", "action": "modified", "sha256": "8ecc4e04c58b98fd278b5ba8d2132fe5b5f046def5471c6e89511d29f570acab"},
    {"path": "integrations/clients/analytics.py", "action": "modified", "sha256": "152f9d50de6b8fcc20091f5d141ce71888d5a5d89f3bac058733e61e3dac4f1d"},
    {"path": "integrations/clients/usda_fdc.py", "action": "modified", "sha256": "2bdffe18c766e9951aa0ec6c09717d0f4bf6b34d00cbc3c1d727ab671a8b202a"},
    {"path": "integrations/clients/figma.py", "action": "modified", "sha256": "0f411399c91879f024acd8922c129dad1af4bd667769aa7867cca8df391ff770"},
    {"path": "integrations/clients/literature.py", "action": "modified", "sha256": "22aa2b48d52c273ec677f7d5ca009ffccda01581ac84ea6bbd985f7575ff184b"},
    {"path": "integrations/clients/tzameret.py", "action": "modified", "sha256": "9ca8a4327e4add32a00ff1b4282074d440a990a6be5e71b3c1c6c80ddb360ce6"},
    {"path": "integrations/clients/dsld.py", "action": "modified", "sha256": "d1493d6cbc0c7f0a5a9d10ad4e20842c222a1c822df74a78a0d96b0475228995"},
    {"path": "integrations/clients/il_prices.py", "action": "modified", "sha256": "5f00af653689e61e2eca5d088f33550c6a72cc050f13d23622231d52e760a234"},
    {"path": "integrations/clients/pagespeed.py", "action": "modified", "sha256": "fa7da1f1839096aea1434d8fedd9eff1ba9d4bb1535d418fcc706586512fc93c"},
    {"path": "integrations/clients/open_food_facts.py", "action": "modified", "sha256": "c574b195e5885599f52a6904ddd05d512cdc9af6c0c1d3dc6c4f4f50bcf3f469"},
    {"path": "integrations/clients/crossref.py", "action": "modified", "sha256": "06de33eea57fd719d2d5412610641095e49894057259a0a13c42939317390afc"},
    {"path": "integrations/clients/pubchem.py", "action": "modified", "sha256": "887c6cdadbf694b55db87fd42e2cd5cfca5f39d66ca822695c872ba35b042f7f"},
    {"path": "integrations/clients/openfda.py", "action": "modified", "sha256": "cab04338cdde7a323dd23c3766cc5622514c312d71bfaa5c90444cc94c83fd12"},
    {"path": "integrations/clients/search_console.py", "action": "modified", "sha256": "1e032df5f7456229a0ac93b70f7ecb4ca948e4701ec2feefc0943baa75b0c83e"},
    {"path": "integrations/clients/semantic_scholar.py", "action": "modified", "sha256": "9701959a79c07144065e88c81fe8e43a23d67cb1bdea7eb939a86449567387fa"},
    {"path": "integrations/clients/hebrew_grammar_gate.py", "action": "modified", "sha256": "35e344022b19ee3fe4594212b9b6ee72a73584ae0b624165ef7106b21140278b"},
    {"path": "03_operations/validators/verify_citations.py", "action": "modified", "sha256": "16908d1cdb7a06aa4f9128aaffd2cb8de027ae09bc0ea2b8a8b752b2444d1a43"},
    {"path": "03_operations/evals/copy_evals/run_evals.py", "action": "modified", "sha256": "cfa7077c13f77c28e94d745f5c27c7877630f74d91b2ed6618bd866b6834da84"},
    {"path": "integrations/clients/tests/test_task566_regressions.py", "action": "created", "sha256": "c5bc99f0f16e34fe184b8139c0a95919085a2bd6d67bd37ba4761664f6567730"}
  ],
  "counts": {
    "importers_updated": "16/16 (grep of live tree for 'from .http import' and 'integrations.clients.http' across integrations/ and 03_operations/, excluding .venv/tasks/.git) | dist: binary pass/fail per file, all 16 updated to http_client, stdev=0.0, most_common=pass(16)",
    "regression_tests_pass": "7/7 (pytest integrations/clients/tests/test_task566_regressions.py) | dist: binary PASS/FAIL per test, stdev=0.0, most_common=PASS(7)",
    "total_tests_pass": "13/13 (pytest integrations/clients/tests/ — 6 pre-existing + 7 new) | dist: binary PASS/FAIL per test, stdev=0.0, most_common=PASS(13)",
    "verify_citations_selftest_pass": "6/7 (TC-1 failure pre-existing before TASK-566 changes, confirmed by stash test) | dist: 6 PASS 1 FAIL, stdev=0.37, most_common=PASS(6)",
    "shadow_repro_confirmed": "1/1 (pre-fix: exit 1, ModuleNotFoundError; post-fix: exit 0, stdlib http loaded)"
  },
  "commands_run": [
    {"cmd": "python -c \"import sys; sys.path.insert(0, 'integrations/clients'); import http; import http.client\" (PRE-FIX shadow reproduction)", "exit_code": 1},
    {"cmd": "python -c \"import sys; sys.path.insert(0, 'integrations/clients'); import http; import http.client; print(http.__file__)\" (POST-FIX verification)", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.http_client import HttpError, get, get_json; ... (all 15 client modules imported)\"", "exit_code": 0},
    {"cmd": "python 03_operations\\validators\\verify_citations.py --selftest", "exit_code": 1},
    {"cmd": "python -c \"from integrations.clients.hebrew_grammar_gate import gate_status, GateDidNotRunError, CLIENT_VERSION; status, msg = gate_status(); print(status, msg)\"", "exit_code": 0},
    {"cmd": "python -m pytest integrations/clients/tests/test_task566_regressions.py -v", "exit_code": 0},
    {"cmd": "python -m pytest integrations/clients/tests/ -v", "exit_code": 0}
  ],
  "not_done": [],
  "self_check": "Acceptance test: (1) sys.path.insert(0,'integrations/clients') + import http.client succeeds post-rename (exit 0, __file__=stdlib); (2) GateDidNotRunError raised on simulated ImportError, not swallowed; (3) run_evals._load_grammar_gate(required=True) returns None + stderr ERROR message when gate fails; (4) 7/7 new regression tests pass; (5) 13/13 total tests pass. All observed results match expected."
}
```
