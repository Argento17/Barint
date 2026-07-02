# P468 / TASK-462 CI green, layer 2: enricher fixture paths + validate-corpus CI mode + full-job local proof (route: C1-GROK)

## 1. Context
- Worktree `C:\bari_wt_t462a`, branch `ci/task462-green-python-off` (= PR #43; pushing updates the PR — you MAY `git push` at the end, it is required). On top of merge `f5764e7d`. Never touch `C:\Bari`.
- PR #43's first fixes worked (BSIP0 nutrition 31/31, off-sweep green, ESLint green) but the jobs now reach their NEXT steps and fail there (onion layers):
  - `python-tests` → step "BSIP1 enricher tests (64)": `python 03_operations/bsip1/core/test_enricher.py` = 54/56, 2 FAIL, both `C:\Bari\03_operations\bsip1\run_001\output/...` hardcoded paths ("SB record file exists", "Yogurt files exist"). The fixtures ARE in-repo (`03_operations/bsip1/run_001/output/bsip1_16000423534.json` confirmed on origin/master).
  - `frontend` → step "Validate corpus": `node scripts/validate-corpus.mjs --all --handoff` = 972 errors. NOT fixable by data edits (and most touch copy under the owner freeze). The script itself documents two modes (see its header + ~line 284): **dev mode = LIVE-category failures are WARNINGS** (contract R1 mitigation), `--handoff` promotes everything to ERROR. CI wiring chose handoff mode aspirationally.

## 2. Objective
**Fix A — enricher test paths.** In `03_operations/bsip1/core/test_enricher.py`, replace every hardcoded `C:\Bari\...` path with repo-root-relative resolution derived from `__file__` (file sits at `03_operations/bsip1/core/`, repo root = 3 parents up). No assertion-logic changes. Gate: `python 03_operations/bsip1/core/test_enricher.py` exit 0, 56/56.

**Fix B — CI validate-corpus mode.** In `.github/workflows/barint_ci.yml`, change the "Validate corpus" step from `--all --handoff` to `--all` (dev mode), and add a YAML comment above it: `# dev mode: live-category failures warn (972-error backlog = TASK-462 follow-up under owner copy freeze); new/un-wired datasets still hard-fail. --handoff stays the manual handoff gate.` Do NOT touch scripts/validate-corpus.mjs itself — the validator's strength is unchanged; only the CI invocation mode changes to the script's own documented policy. Gate: `cd bari-web; node scripts/validate-corpus.mjs --all` exit 0 (live failures downgraded to warnings; if it still exits non-zero, find WHY — e.g. orphan/new-dataset errors — report exactly, and if the cause is the two §4.3 orphan files bread_frontend_v3.json/cheese_frontend_v4.json report-only, do NOT delete data files).

**Fix C — burn down the remaining onion NOW.** Run EVERY remaining step of the `python-tests` job locally in order, exactly as the workflow does: `run_router_regression.py`, `run_regression_check.py`, `pytest test_bsip0_qa_validator.py`, `pytest test_bsip0_gate.py`, `bsip0_gate.py ... || true`, `spine/smoke_test.py --dry-run`. For each: exit code. If a failure is the SAME class (hardcoded absolute path / Windows-only path), fix it the same way. If it fails for ANY other reason: do NOT fix; capture the error precisely in the return. Then run the full `frontend` job steps locally too (`npm ci` if needed, `npm run build`, `npm run lint`, corpus validate) and report exit codes.

## 3. Boundaries
- OFF ban absolute. FREEZE: no consumer copy/product-description edits of any kind; Fix B exists precisely to avoid mass copy edits. No score/data JSON changes. No new dependencies.
- You are the EXECUTOR. Do NOT spawn subagents.

## 4. Return
`tasks\returns\P468_contract.md` (NOT P468_return.md). Per-fix before/after, every command with exit code (the full job-step table is the core deliverable), real sha256s, counts with denominators + distribution marker on the 56-check claim. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P468_contract.md --root C:\bari_wt_t462a` exit 0 (PowerShell). Commit everything, `git push` (updates PR #43). Propose RETURNED (or BLOCKED listing any non-path-class failures).
