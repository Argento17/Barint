---
id: TASK-402
title: Bread fat-sentinel engine flag → master (reproducibility lineage)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-25
depends_on: []
blocks: []
category_id: null
blocker: Tangled with task-374 engine divergence (324 lines on score_engine.py); do as part of that branch's reconciliation to master, not a standalone surgical patch.
summary: >
  Bread fat-sentinel engine flag → master (reproducibility lineage)
---

# TASK-402 — Bread fat-sentinel engine flag → master (reproducibility lineage)

## Context
TASK-397 deployed the bread fat-sentinel re-score to origin/master (`0d4cc1a1c`):
the bread_frontend_v3.json scores are live + correct + conform. But the ENGINE
CODE that produces them lives on branch `task-374`, NOT master:
- `03_operations/bsip2/proto_v0/src/score_engine.py` — `BARI_FAT_SENTINEL_V1` flag (~L231) + guard in `_score_fat_quality_sprint1` (~L1731-1744). Flag default OFF.
- `03_operations/bsip1/run_bread_conform_001/build_bread_bsip1.py` — `is_ceiling_declaration()` + `fat_sentinel` field (~L64, L92).
- `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-107.
- Staging run: `02_products/bread/staging/task397_rescore/`.

## Why blocked / deferred
Copying task-374's `score_engine.py` wholesale to master would drag **324 lines
of unrelated task-374 divergence** → clobber risk. The fat-sentinel changes are
additive (new flag + new guard + new function) and must be extracted SURGICALLY,
which is safest done when the task-374 branch's engine work is reconciled to
master as a unit. Rushing it risks a subtle scoring bug.

## DoD
- The 3 engine/lineage changes land on master with ONLY the fat-sentinel delta (verified diff).
- Flag-OFF byte-identical regression PASS (already proven in staging).
- A bread re-flow (spine_flip with flag wired into the bread config) reproduces the deployed scores (score==trace) — i.e. wire `BARI_FAT_SENTINEL_V1=on` into the bread scoring config so the re-flow is reproducible.
- 0 cross-category score movement (0 sentinel products elsewhere — already verified).
