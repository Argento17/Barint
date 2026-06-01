---
id: TASK-129A
title: Fix P0 confidence gate validation
owner: nutrition-agent
status: IN_PROGRESS
priority: CRITICAL
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Confidence gate validates ingredient presence rather than ingredient quality; fix per hummus/maadanim/snacks/milk failure cases
---

# TASK-129A — Fix P0 confidence gate validation

**Origin:** `03_operations/bsip2/confidence_reaudit_launch_v1.md` §3 P0 #1.
**Deliverable:** `03_operations/bsip2/confidence_gate_fix_129a_v1.md` (full write-up) +
`03_operations/bsip2/sprint1/ingredient_quality_gate.py` (shared, unit-tested validator).

## Root cause
The §5 data-sufficiency gate is **presence-based** (`bool(ingredients_text)` / maadanim's
`confidence_score ≥ 75`) — nothing inspects ingredient-field *content*. Nutrition-panel bleed,
marketing prose, and allergen tails all pass as `verified`, and the explanation engine then derives
false ingredient-based positive signals from that text. The gate is duplicated across ≥3 build
scripts + the §5 spec (no single function).

## Demonstrated (reproduced against shipping corpora)
- **hummus** `חומוס גדול שופרסל` 85/A `verified` — ingredient field = "chickpeas" + the whole scraped
  nutrition table; positiveSignals quote the bled-in numbers.
- **maadanim** `מעדן חלבון בטעם וניל` 54/C `verified` (allergen prose tail); `גמדים לשתיה תות בננה`
  46/D (category-instability survivor).
- **snacks** `snk-001` 70/B `verified` with all 6 nutrition fields null (audit §2.4).
- **milk** 2 rows (LEGACY, corpus absent here).

## Proposed logic
Shared `gate_confidence()` / `assess_ingredients()`: `verified ⇐ ≥3/6 nutrition fields AND a REAL
ingredient list`; on downgrade, also suppress ingredient-derived positive signals. Validator built +
self-test green.

## Impact (calibrated — corrects the audit)
Label-only (verified→partial); **no score/grade/ordering change** (audit §2.5). Detector calibrated
through 3 cuts to **zero false-positives on genuine lists** (panel-only bleed tokens + footnote/tail
stripping). True relabel set: **hummus 5** (3 nutrition-bleed + 2 empty), **maadanim 0**. The audit's
15/63 estimate was inflated by the same footnote false-positive class this fix removes. maadanim's
real defect is category-contamination (audit §2.1/§2.2), not prose ingredients — owned by TASK-129
finalization. snacks/milk corpora not in this repo. Per-row delta: `confidence_gate_relabel_delta_129a.md`.

## Progress
- **DONE** Phase 1: validator `ingredient_quality_gate.py` (self-test green).
- **DONE** Phase 2: `launch_definition_v1.md` §5 amended (real-list requirement + signal suppression).
- **DONE** Phase 2.5: relabel set locked (dry-run, no corpus mutated).
- **PENDING** Phase 3: wire validator into `build_*.py` (maadanim = verified no-op; safe forward protection).
- **PENDING** Phase 4: **hummus** 5-row label-only re-freeze of frozen `run_hummus_002` — needs
  Controller sign-off; ships as a documented launch limitation, does **not** block hummus GO.

**Net:** scope collapsed from a feared 4-category sweep to a **5-row, hummus-only, freeze-governed
relabel** + forward-protective gate. Only the hummus re-freeze requires approval.
