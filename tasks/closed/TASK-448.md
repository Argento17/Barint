---
id: TASK-448
title: OFF-ban breach in acquisition code — verify no OFF-origin nutrition reached live pages, neutralize active OFF dependency
owner: data-agent
status: CLOSED
close_reason: >
  Verified NO live OFF leak — provenance trace confirmed 16/16 live categories carry zero
  OFF-origin nutrition on any displayed product (record-level, incl. hummus 57/57 Shufersal).
  OFF dependency neutralized: 5 importing scripts guarded (import census 5→0), committed to
  branch task448/off-ban-neutralize-callers (beab5572) for durability. OFF client file left
  intact per hard rule (removal = owner written policy). Follow-up (separate, non-blocking):
  off_sweep detector has stale filenames — folded into the TASK-447 gate-enforcement theme.
priority: CRITICAL
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Capability audit (TASK-447) found the banned OFF client still IMPORTED + CALLED in acquisition scripts: 02_products/hard_cheeses/bsip0_rerun_real.py:28 (docstring: 'Nutrition: OFF per-barcode API only'), 02_products/juices/bsip0_rerun_real.py:25, yohananof_yogurt acquire. VERIFIED downstream ban IS enforced (granola excluded_off_products sweep per TASK-238; run_gates.py:69 + conformance.py:77 hard-fail on OFF markers) and NO OFF marker in live shipped frontend JSON. OPEN RISK (unverified): whether HC/juices/yogurt/cereals live nutrition originated from OFF at bsip0/bsip1 with marker stripped. Trip: OFF ban is hardest project rule, any OFF dependency = launch blocker. NOTE: OFF client file removal needs explicit owner written policy (per hard rule); this task neutralizes the DEPENDENCY (scripts calling it) + verifies provenance, not client deletion.
---

# TASK-448 — OFF-ban breach in acquisition code — verify no OFF-origin nutrition reached live pages, neutralize active OFF dependency

## RESOLUTION (2026-07-01, orchestrator-verified) — NO LEAK; dependency neutralized

**Provenance trace (a72aa91f) + hummus closeout (a341a70a):** **16/16 live categories CLEAN.** Every displayed product across all live categories traces to a real retailer scrape (shufersal/yohananof) at the feeding-corpus record level — **zero** OFF-origin nutrition displayed, zero stripped-marker cases. Hummus (the last untraced cat) verified 57/57 Shufersal, 0 OFF hits across 114 files. granola's historical OFF products correctly dropped/re-sourced (ban working).

**Why it was never a live leak:** the OFF client (`integrations/clients/open_food_facts.py`) is hard-disabled at source (`OFF_DISABLED=True`; `_enforce_off_ban()` raises before any network call). The 5 scripts that imported it would crash if run — dead code, not a live pull path.

**Neutralized (5/5, verified exit-1 each; import census 5→0 live importers):**
`02_products/build_bsip0_yohananof.py`, `hard_cheeses/bsip0_rerun_real.py`, `juices/bsip0_rerun_real.py`, `juices/build_juices_corpus.py`, `juices/scrape_juices_bsip0.py` — OFF import commented + hard `raise RuntimeError` guard + misleading docstrings corrected. OFF **client file untouched** (removal reserved for explicit owner written policy).

## OPEN (small, honest)
1. ~~The 5 edits are uncommitted~~ ✅ **DONE — owner said "commit"; committed to branch `task448/off-ban-neutralize-callers` (beab5572), off-master, durable. Not pushed.**
2. **`off_sweep/run_off_sweep_v2.py` (the automated OFF detector) throws file-not-found for stale filenames** (bread/snacks/yogurts/cheese/butter/granola/salty-snacks) → the enforcement tool may be partially blind to current live files. Separate follow-up; ties to the TASK-447 "gates not enforced" theme.
3. Dead OFF-string literals remain inside the 5 scripts' function bodies (unreachable post-guard; left per minimal-edit constraint).

## LESSON → memory [[off_ban_enforcement_verify_by_census]]
An OFF-purge is only real when verified by **import-census + record-level provenance trace**, NOT by a commit message (`juices/build_juices_corpus.py` was touched in a commit claiming "purge all OFF residue" yet kept the OFF import) and NOT by the off_sweep detector alone (it had stale filenames).

<!-- Live view: tasks/DISPATCH_BOARD.md TASK-448 line. Status stays IN_PROGRESS pending commit (#1). -->
<!-- opened with new_task.py -->

