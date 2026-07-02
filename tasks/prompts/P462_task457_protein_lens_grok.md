# P462 / TASK-457 wire apply_protein_bar_lens into the uniform engine + byte-reproduce the live page (route: C1-GROK)

## 1. Context / baseline
- You are ALREADY in isolated worktree `C:\bari_wt_t457` (branch `fix/task457-protein-lens`, cut from origin/master `47a51248`). Repo root = this worktree. Never touch `C:\Bari` (read-only for reference docs), never `git stash/checkout` outside this tree. Commit here; NO push/PR/deploy.
- Read FIRST: `C:\Bari\tasks\TASK-457.md` and DISPATCH_BOARD sections on TASK-456/457 (`C:\Bari\tasks\DISPATCH_BOARD.md`, search "protein_bars — de-anchor HELD").
- The defect (uniform-baseline doctrine violation): the approved TASK-365 lens `apply_protein_bar_lens` is NOT called from `03_operations\bsip2\proto_v0\src\score_engine.py` (comment-only around line ~2334 — locate it). The live page `bari-web\src\data\comparisons\protein_combined_frontend_v2.json` (in THIS worktree = the published truth, 32 products) was produced by a bespoke driver, and flag-off runs of the uniform engine reproduce its SCORES but produce wrong GRADES for 2/32 (engine says C where live=D at the same score — a grade-boundary logic divergence).
- Two approved files are absent from this tree but exist in commit `6871d374` (a WIP snapshot on the feature branch — read-only source): `git -C C:\Bari show 6871d374:<path>` for `rescore_task365_inplace.py` and `batch_run_protein_bars_task365.py` (find their exact paths via `git -C C:\Bari show 6871d374 --stat | grep -i protein`). Use them as REFERENCE for what the lens path must do — the deliverable is the uniform engine doing it, not the bespoke driver.
- Weight profile already in constants: `EV-PBAR-005` block (`constants.py`, search "EV-PBAR-005"; sum=1.00 confirmed). `PROTEIN_BAR_LENS_ON = os.environ BARI_PROTEIN_BAR_V1` exists (constants.py ~line 1798).

## 2. Objective — make flag-ON byte-reproduce the published page, prove flag-OFF touches nothing
**Commit 1 — wiring:** call `apply_protein_bar_lens` from the uniform `score_engine.py` scoring path, gated on the EXISTING flag `BARI_PROTEIN_BAR_V1` (default OFF stays). Resolve the grade-boundary divergence so the uniform path reproduces live grades too (diagnose WHERE the bespoke driver's grade mapping differs — likely a boundary/rounding rule; implement the same rule inside the gated path, never globally). Emit a trace note (`protein_bar_lens_applied: true`) in bsip2 traces when the lens fires (Rule-7 auditability).

**Reproduction gates (both mandatory):**
- **Gate A (flag OFF):** full cross-corpus rescore (`03_operations\page_generator\rescore_all.py`) — byte-identical scores AND grades for ALL live categories vs the committed frontend JSONs in this worktree, protein included at its current (wrong-path) values? NO — flag-off after wiring must equal flag-off before wiring = the engine's current output, and since the wiring is fully gated, that is automatic; PROVE it anyway (0 diffs vs a pre-change flag-off run).
- **Gate B (flag ON, the acceptance test):** rescore protein_bars with `BARI_PROTEIN_BAR_V1=on`, corpus-pinned to the published 32 barcodes → **32/32 EXACT score AND grade match to `protein_combined_frontend_v2.json`.** Emit the Rule-7 flat table (barcode, score, grade, binding_caps, nova, fat, sodium, context_flag). If any product mismatches: STOP, report the per-product diff table, propose BLOCKED (do not tune anything to force a match — a mismatch means the divergence diagnosis is wrong).

**Explicitly OUT of scope:** the de-anchor 3-flip activation (that is a later, gated deploy); any other category's scoring; any copy.

## 3. Contract / return
- Write the full return to `tasks\returns\P462_contract.md` (NOT P462_return.md — the router overwrites that path). Real sha256 for every touched file (compute them). Counts with denominators + Rule-5 distribution markers (grade dist of the 32 at flag-ON with stdev + most_common). Exit-code semantics noted per command. commands_run with the exact env-var prefixes.
- Self-gate before returning: `python 03_operations\validators\validate_return.py --md tasks\returns\P462_contract.md --root C:\bari_wt_t457` must exit 0 (run from PowerShell, not Git Bash — bash mangles the --root backslashes).
- Commit the contract. Leave the tree clean (delete stray droppings; `_rescore_staging` is gitignored).
- OFF ban absolute. No invented data. Propose RETURNED (or BLOCKED per Gate B).
