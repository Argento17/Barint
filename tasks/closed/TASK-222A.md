---
id: TASK-222A
title: "BSIP2 Phase 1 — emulsifier F1 identity deltas activation (sprint1 retirement)"
owner: orchestrator
status: CLOSED
priority: HIGH
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: [TASK-222]
blocks: []
roadmap_impact: false
cc_reviewed: true
work_type: execution
close_reason: >
  Final acceptance review complete. F1 emulsifier identity deltas activated and sprint1
  additive-count corrections retired. All 40 non-zero corpus deltas reviewed and approved.
  No double-counting, no ceiling breach, no unintended protein/nutrient-density/satiety
  changes, and no consumer-copy medical claims introduced. Evidence registry BEV-085
  scoped correctly. Router regression passed 16/16; golden regression passed with 11 PASS
  / 1 pre-existing WARN. Implementation matches TASK-222 decision matrix spec.
---

# TASK-222A — Emulsifier F1 identity deltas activation

**Part of:** TASK-222 (BSIP2 research-to-implementation). **Scope:** scoring engine
changes only — no frontend, no consumer copy, no methodology revision.

## What was done

- **Activated** `ADDITIVE_IDENTITY_DELTAS` in `constants.py`:
  - `emulsifier_concern_each=3` (−3 per high-risk concern on additive_quality)
  - `emulsifier_concern_cap=6` (hard ceiling, max stacked delta −6)
  - `lecithin_relief=2` (+2 for benign lecithin)
- **Retired** sprint1 +2/−1 additive-count corrections in `signal_extractor.py`:
  - `sprint1_additive_correction = 0` (always zero)
  - `sprint1_additive_count = additive_marker_count` (raw count, no correction)
  - Detection calls preserved (inert) for traceability / rollback
- **Updated** `score_engine.py` docstrings to reflect TASK-222A state
- **Registered** evidence BEV-085 (emulsifier identity deltas, human RCT + regulatory consensus)

## Verification

| Check | Result |
|-------|--------|
| Router regression (16 tests) | PASS |
| Golden corpus regression (12 entries) | 11 PASS, 1 WARN (pre-existing) |
| Snack bar ceiling (snk-001 = 70/B) | HELD |
| Milk ceiling (85/A) | HELD |
| Corpus diff gate (139 products) | 40 non-zero, all reviewed & APPROVED |
| No double-counting | Confirmed — sprint1 retired to zero |
| No collateral dimension changes | Confirmed — only additive_quality affected |

## Key files changed

- `03_operations/bsip2/proto_v0/src/constants.py` — ADDITIVE_IDENTITY_DELTAS activated
- `03_operations/bsip2/proto_v0/src/signal_extractor.py` — sprint1 corrections zeroed
- `03_operations/bsip2/proto_v0/src/score_engine.py` — docstrings updated
- `03_operations/bsip2/proto_v0/review/task_222a_corpus_diff_gate.md` — diff gate report
- `01_framework/governance/evidence_registry_v1.md` — BEV-085 added
