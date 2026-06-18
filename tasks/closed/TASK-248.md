---
id: TASK-248
title: "OFF code-path eradication: stub remaining 7 scrape scripts (carrefour_butter, multiretailer_cereals x2, shufersal_olive_oil, yohananof_butter, yohananof_cheese x2)"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-11
returned_at: 2026-06-11
closed_at: 2026-06-11
cc_reviewed: 2026-06-11
branch: task-248-off-eradication
commit: 0adbc926
close_reason: >
  Verified by CC against artifacts before close: commit 0adbc926 removes 1990 lines of OFF
  acquisition across 9 scripts (the 7 in scope + both yohananof_yogurt scripts not yet stubbed
  on this branch); CC's independent grep over the worktree finds zero live OFF code paths
  (remaining matches = 4 raise-guarded _deprecated_off files, verified, + gate detection
  tokens); stub headers carry the ban verbatim; bsip0_gate.py correctly left alone (it IS the
  detector). Integrated: salty-snacks-v4 fast-forwarded 37631998 -> 0adbc926. Evidence class:
  merged@salty-snacks-v4 (pipeline code, not consumer-facing; rides to master with the branch).
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-247 verification sweep found live OFF fallback code paths in 7 acquisition scripts beyond Victory (fixed in 247) and yohananof_yogurt (stubbed on rel/yogurts-v4). Butter raw outputs contain 5 OFF-hit rows (carrefour, 2026-06-05) but merged corpus + live page verified byte-clean (Shufersal direct scrape won the merge). Stub all OFF paths per the TASK-238/247 RuntimeError pattern; raw files stay untouched as provenance history.
---

# TASK-248 — OFF code-path eradication: stub remaining 7 scrape scripts (carrefour_butter, multiretailer_cereals x2, shufersal_olive_oil, yohananof_butter, yohananof_cheese x2)

## Return Block

**Branch:** `task-248-off-eradication`
**Worktree:** `C:\Bari-task248`
**Commit:** `0adbc926`

### Per-file actions

| File | Action | Reason |
|---|---|---|
| `carrefour_butter/01_scrape_carrefour_butter.py` | STUBBED (raise RuntimeError) | OFF-only acquisition — no replacement source; entire script was OFF panels by barcode |
| `multiretailer_cereals/01_acquire_multiretailer.py` | STUBBED (raise RuntimeError) | il_prices identity + OFF panels — OFF was the sole panel source; no direct scrape available |
| `multiretailer_cereals/02_build_bsip1_multiretailer.py` | STUBBED (raise RuntimeError) | Built from OFF candidate raw produced by the above; upstream disabled |
| `shufersal_olive_oil/_build_corpus_from_sources.py` | DELETED OFF branch (script kept) | Two-source script: Source 1 (il_gov_data identity) retained; Source 2 (OFF barcode-lookup) block deleted (-75 lines); nutrition stays NULL |
| `yohananof_butter/01_scrape_yohananof_butter.py` | STUBBED (raise RuntimeError) | il_prices identity + OFF panels — OFF was the sole panel source |
| `yohananof_cheese/01_acquire_yohananof_cheese.py` | STUBBED (raise RuntimeError) | il_prices identity + OFF panels — OFF was the sole panel source |
| `yohananof_cheese/02_build_bsip1_yohananof_cheese.py` | STUBBED (raise RuntimeError) | Built from OFF candidate raw; upstream disabled |

### bsip0_gate.py disposition

`03_operations/bsip0/scrape/_shared/bsip0_gate.py` — file exists only in the main working tree (untracked; not on `salty-snacks-v4`). Its OFF references (`OFF_TOKENS` tuple, `gate_off_contamination()`) are the gate's own contamination DETECTOR — the exact mechanism that catches OFF in incoming data. **Left alone per instructions.** Not an OFF data path.

The frozen-veg `05_bsip0_gate.py` and `_deprecated_off/` scripts also matched the grep — all are gate detection patterns or dead code behind a prior `raise RuntimeError` stub. No live OFF acquisition in any of them.

### Verification

Grep (zero files outside gate/deprecated):
```
03_operations/bsip0/scrape/salty_snacks_real/_deprecated_off/01_bsip0_off_panels.py      — raise-guarded dead code
03_operations/bsip0/scrape/salty_snacks_real/_deprecated_off/fix_apropo_caramel_trans.py — raise-guarded dead code
03_operations/bsip0/scrape/salty_snacks_real/_deprecated_off/fix_beet_cracker_trans.py   — raise-guarded dead code
03_operations/bsip0/scrape/salty_snacks_real/_deprecated_off/fix_trans_artifacts_corpus.py — raise-guarded dead code
03_operations/bsip0/scrape/shufersal_frozen_vegetables/05_bsip0_gate.py                  — detection token, not acquisition
```
No live OFF code path remains under `03_operations/bsip0/scrape`.

Tests: `test_bsip0_nutrition.py` — **31 passed, 0 failed**

### Guards confirmed

- Raw output JSONs untouched (provenance history preserved)
- No scoring changes
- No manual JSON patches
- Not pushed
