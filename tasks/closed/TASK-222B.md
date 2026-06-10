---
id: TASK-222B
title: "BSIP2 Phase 1 — protein-bar matrix discount activation (F2 reconstructed/collagen)"
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
  F2 protein-bar matrix discount activated (reconstructed=0.80, collagen=0.55).
  DEC-004 placeholder values confirmed — midpoint of 47-81% DIAAS band for
  reconstructed, incomplete-AA discount for collagen. Corpus diff gate: 0 non-zero
  score deltas (2 products with reconstructed form, both 0g protein; 0 collagen).
  No ceiling breach. No collateral dimension changes (protein mass, nutrient-density,
  satiety unchanged). No double-counting with matrix_integrity.py (not wired into
  composite). Router regression 16/16 PASS; golden regression 11 PASS / 1 pre-existing
  WARN. Evidence registry BEV-086 added.
---

# TASK-222B — Protein-bar matrix discount activation

**Part of:** TASK-222 (BSIP2 research-to-implementation). **Scope:** scoring engine
confirmation — code was structurally live with DEC-004 placeholder values; TASK-222B
confirms the values, runs corpus diff gate, and formalizes activation.

## What was done

- **Confirmed** `PROTEIN_QUALITY_MATRIX_DISCOUNT` values:
  - `reconstructed=0.80` — bar-format isolate: midpoint of 47–81% DIAAS band
  - `collagen=0.55` — incomplete AA profile, lowest matrix DIAAS
- **Verified** no double-counting with `matrix_integrity.py` (not wired into composite)
- **Verified** protein mass untouched (feeds satiety_support + nutrient_density directly)
- **Verified** no collateral dimension changes (nutrient_density, satiety, additive_quality)
- **Updated** `constants.py` comments — DEC-004 placeholder → TASK-222B activated
- **Registered** evidence BEV-086 (protein-bar matrix discount, commercial DIAAS)

## Verification

| Check | Result |
|-------|--------|
| Router regression (16 tests) | PASS |
| Golden corpus regression (12 entries) | 11 PASS, 1 WARN (pre-existing) |
| Snack bar ceiling (snk-001 = 70/B) | HELD |
| Milk ceiling (85/A) | HELD |
| Corpus diff gate (53 snack bar products) | 0 non-zero score deltas |
| Collateral dimension changes | None confirmed |
| Double-counting with matrix_integrity.py | None confirmed (not wired into composite) |

## Roadmap note

TASK-222B is **structural future-proofing** — the discount is correct and ready, but with only 2 products triggering it (both 0g protein) and zero collagen products in the current corpus, it becomes **important only when Bari ingests actual protein bars with meaningful protein content and/or collagen**. Until then, the code is active but dormant. Revisit after significant snack_bar_granola corpus expansion.

## Key files changed

- `03_operations/bsip2/proto_v0/src/constants.py` — DEC-004 placeholder comments updated to TASK-222B activation
- `03_operations/bsip2/proto_v0/review/task_222b_corpus_diff_gate.md` — diff gate report
- `01_framework/governance/evidence_registry_v1.md` — BEV-086 added
