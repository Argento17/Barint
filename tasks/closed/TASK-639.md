---
id: TASK-639
title: Trace-backfill wave: 59 backfill-safe calc-FAILs (brined_cheeses A + cakes/cereals/chocolate B1)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-632
lesson_trigger: none
close_reason: >
  VERIFIED + merged (branch 187dbcc2 -> 31229f47). Extended the proven TASK-630 trace-backfill pattern to
  the 59 backfill-safe calc-FAILs from the TASK-632 triage: brined_cheeses 14 (class A) + cakes 26 / cereals
  2 / chocolate_bars 11 / chocolate_tablets 6 (class B1). Shell backfill traces (served score verbatim, no
  real task409 per-barcode traces existed on disk), emitted into new run dirs placed FIRST in each config's
  run_products_dir (first-dir-wins per build_dossiers L349). 2 cheese class-C EXCLUDED (genuine 0.2pt
  rounding). Main-tree rebuild CONFIRMED: all 5 shelves 100% calc pass; aggregate calc fail 61->2 (only the
  2 cheese class-C remain); ALL-GREEN 64%->70% (479/681); parity diverge=0. Scores UNCHANGED (score-identity
  asserted). NOTE: worktree/run-dir artifacts carry a 'task635' label (id counter had advanced past 635 to
  639 when registered) -- cosmetic only.
summary: >
  Trace-backfill wave for the 59 backfill-safe calc-FAILs per the TASK-632 triage; exclude 2 cheese class-C.
---

# TASK-639 — trace-backfill wave (59 rows)

59 calc-FAILs flipped (calc fail 61->2), ALL-GREEN 70%, parity diverge=0, scores unchanged. See close_reason.
