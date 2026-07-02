# P471 / TASK-462 CI green, layer 4 (final): bsip0_gate stdout-rewrap breaks pytest on CI (route: C1-GROK)

## 1. Context
- Worktree `C:\bari_wt_t462a`, branch `ci/task462-green-python-off` (= PR #43), on top of `9470e273`. Never touch `C:\Bari`.
- PR #43 now: frontend GREEN, off-sweep GREEN; `python-tests` fails at step "BSIP0 exit gate tests (30)": `python -m pytest .../test_bsip0_gate.py` crashes on CI Python 3.12 with `collected 0 items` + `ValueError: I/O operation on closed file` in `_pytest/capture.py` — SAME crash you saw locally on 3.14, so it was never a version artifact.
- Root cause (orchestrator-diagnosed): `03_operations/bsip0/scrape/_shared/bsip0_gate.py` line 48 executes `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")` at MODULE IMPORT (Windows Hebrew-console hack). `test_bsip0_gate.py` imports it → pytest's capture stdout gets wrapped → capture teardown explodes.

## 2. Objective (two small fixes, then final green proof)
**Fix 1 — guard the rewrap.** In `bsip0_gate.py`, make line 48 conditional and safe:
```python
if hasattr(sys.stdout, "buffer") and (getattr(sys.stdout, "encoding", "") or "").lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
```
Preserves the Windows-console behavior (cp1252 consoles still get rewrapped); under pytest/CI (already utf-8, or captured objects without a usable buffer) it becomes a no-op. Check whether any OTHER module under `03_operations` does the same import-time `sys.stdout =` rewrap AND is imported by a CI-invoked test — if yes, guard it identically; list all occurrences either way.
**Fix 2 — align the CI step with the file's design.** In `.github/workflows/barint_ci.yml`, change the step "BSIP0 exit gate tests (30)" from `python -m pytest ... test_bsip0_gate.py -v --tb=short` to `python 03_operations/bsip0/scrape/_shared/test_bsip0_gate.py` (the file has its own 30-check runner with a proper nonzero-exit on failure — verify that exit contract by reading its `__main__` block; if it does NOT exit nonzero on failure, fix the runner's exit code instead of keeping pytest). This matches the existing convention (the enricher step already runs `python .../test_enricher.py` directly).
**Proof:** locally run BOTH invocations of the gate tests (direct = 30/30 exit 0; pytest with Fix 1 — report whether it now collects 30; if pytest still crashes locally on 3.14, say so — CI uses the direct invocation after Fix 2, so local pytest is informative, not gating). Then run the remaining workflow steps (live-corpus gate with `|| true`, spine smoke --dry-run) and the full static literal sweep from P470 one more time (must still be 0). Commit + `git push` (updates PR #43).

## 3. Boundaries
OFF ban absolute. FREEZE: no consumer copy. No data JSON edits. No test-assertion changes. You are the EXECUTOR — do NOT spawn subagents. Delete any stray tool droppings (terminals/, agent-tools/) before finishing; leave the tree clean.

## 4. Return
`tasks\returns\P471_contract.md` (NOT P471_return.md). Before/after of both fixes, the rewrap-occurrence sweep, every command + exit code, real sha256s, counts with denominators. Self-gate: `python 03_operations\validators\validate_return.py --md tasks\returns\P471_contract.md --root C:\bari_wt_t462a` exit 0 (PowerShell). Commit + push. Propose RETURNED.
