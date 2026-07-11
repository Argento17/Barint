---
id: TASK-632
title: Classify the remaining 61 PD calc-FAILs (derivability triage) backfill-safe vs run-mismatch vs genuine defect
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: none
close_reason: >
  VERIFIED. Read-only Codex triage classified all 61 remaining calc-FAILs: 14 class-A (brined_cheeses,
  stale post-reflow traces) + 45 class-B1 (cakes 26 / cereals 2 / chocolate_bars / chocolate_tablets --
  RUN-MISMATCH where served baseline is an explicit traceable re-derive but the config run_products_dir
  points at an older run's traces) + 0 class-B2 + 2 class-C (cheese 7290019635383/56272, genuine 0.2pt
  rounding discrepancy). So 59/61 are backfill-safe (served is the authoritative score-of-record), 2 need
  a rounding-policy look. B1 provenance VERIFIED not-invented: cakes served _meta.run_id =
  task409_rederive_cakes_20260626 ('TASK-409 clean+traceable re-derive v2'); config points at stale
  run_cakes_shelfrel_001. ACTION: backfill wave dispatched as TASK-639 (14 A + 45 B1, exclude the 2
  class-C). Report: 03_operations/product_dossier/reports/task632_calcfail_triage.json.
summary: >
  Triage the remaining 61 PD calc-FAILs into backfill-safe / run-mismatch / genuine-defect classes, per the
  TASK-563 don't-certify-wrong-scores caution.
---

# TASK-632 — remaining calc-FAIL derivability triage

61 calc-FAILs -> 14 A + 45 B1 (backfill-safe) + 2 C (genuine rounding). Backfill wave = TASK-639. See close_reason.
