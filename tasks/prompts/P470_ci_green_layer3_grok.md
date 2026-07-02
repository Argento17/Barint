# P470 / TASK-462 CI green, layer 3: purge C:\Bari literals from all CI-invoked python paths (route: C1-GROK)

## 1. Context
- Worktree `C:\bari_wt_t462a`, branch `ci/task462-green-python-off` (= PR #43). On top of `75eb63a3`. Never touch `C:\Bari`.
- After P468, PR #43 shows frontend GREEN + off-sweep GREEN; `python-tests` fails at step "Scoring regression (golden corpus)": `run_regression_check.py:27` hardcodes `CORPUS_PATH = C:\Bari\01_framework\...\golden_corpus_manifest.json` → FileNotFoundError on the Linux runner. The manifest IS in-repo at `01_framework/bsip2_framework/validation/golden_corpus/golden_corpus_manifest.json`.
- **WHY YOUR P468 LOCAL PROOF MISSED IT:** on this machine `C:\Bari` EXISTS, so absolute-path bugs pass local runs. Local exit-0 is NOT evidence for this bug class. The deterministic local gate is a STATIC literal sweep.

## 2. Objective
**Fix 1:** `03_operations/bsip2/proto_v0/src/run_regression_check.py` lines 27-28: make `CORPUS_PATH` and `REPORT_ROOT` repo-relative via `pathlib.Path(__file__).resolve().parents[N]` (src → repo root = parents[4]; verify by counting). 
**Fix 2:** `03_operations/bsip2/proto_v0/src/run_router_regression.py` line 28: same for its `REPORT_ROOT` (on Linux it currently creates a literal `C:\Bari\...`-named file in the workdir — silent junk).
**Fix 3 — close the class:** static sweep `git grep -n "C:\\\\Bari"` (and case variants `C:/Bari`, `c:\\Bari`) across every python file the `python-tests` job invokes DIRECTLY (workflow steps in `.github/workflows/barint_ci.yml`) AND their local imports (follow the import graph one level: e.g. run_regression_check imports score_engine/router_v2/constants — check those too). Fix every literal that sits on a CI execution path the same repo-relative way. Literals in files NOT on CI paths: do NOT fix; list them in the return (they become backlog).
**Gates:** (a) static sweep post-fix = 0 literals on CI-invoked paths (show the grep); (b) all workflow step commands still exit 0 locally (regression check must actually LOAD the corpus and produce its report under the repo-relative path — show the report path it wrote); (c) `git push` (updates PR #43) — the FINAL acceptance is CI green, which the orchestrator will poll.
**Do not** change any threshold/assertion/scoring logic. Note (report-only, no fix): router regression prints "ROUTER REGRESSION: 1 failures" yet exits 0 — capture the failing case name from its report for the TASK-453 backlog.

## 3. Boundaries
OFF ban absolute. FREEZE: no consumer copy. No data JSON edits. No workflow YAML edits this pass. You are the EXECUTOR — do NOT spawn subagents. Also delete the stray untracked `agent-tools/` dropping if you created it (check `git status`); leave the tree clean.

## 4. Return
`tasks\returns\P470_contract.md` (NOT P470_return.md). The sweep results before/after (file:line per literal, fixed vs backlog), every command + exit code, real sha256s, counts with denominators. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P470_contract.md --root C:\bari_wt_t462a` exit 0 (PowerShell). Commit + push. Propose RETURNED.
