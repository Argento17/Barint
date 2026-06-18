---
id: TASK-247
title: Victory/Yohananof retailer nutrition parsers — fix Yohananof header fabrication + asymmetric guards + zero tests; correct TASK-239 mislabel
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-11
closed_at: 2026-06-11
cc_reviewed: 2026-06-11
depends_on: [TASK-240]
blocks: []
category_id: null
branch: task-247-yohananof-parser
commit: 37631998
close_reason: >
  All claims independently verified by CC before close: commit 37631998 (worktree
  C:\Bari-task247, exact parent 5b295f8c, 5 files +266/-118); Victory OFF fallback fully
  removed (zero OFF code refs remain in 01_acquire_victory.py — a live OFF-ban violation
  eliminated); Yohananof verbatim basis header / unknown-basis rejection / structural guard /
  mg unit sniff verified in diff; test suite run by CC in the worktree: 31 passed, 0 failed.
  Integrated: salty-snacks-v4 fast-forwarded to 37631998 (verified). Follow-up OFF sweep
  finding (5 OFF-hit rows in butter carrefour raw; merged corpus + live page verified
  byte-clean against Shufersal direct scrape; 7 scripts still carrying OFF code paths)
  registered as TASK-248. Evidence class: merged@salty-snacks-v4 (integration branch;
  parser code is not consumer-facing — rides to master with the salty-snacks-v4 merge).
summary: >
  Remediate commit 5b295f8c: Yohananof parser fabricates selected_table_header, accepts unknown-basis silently, and ships untested while wired to a live scraper. Bring Yohananof to Victory's guard parity; add tests; re-attribute from CLOSED TASK-239 to TASK-240 #4.
---

# TASK-247 — Victory/Yohananof retailer nutrition parsers — fix Yohananof header fabrication + asymmetric guards + zero tests; correct TASK-239 mislabel

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
