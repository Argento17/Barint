---
id: TASK-REDLABEL-001
title: "BARI_REDLABEL_V1 — Eliminate Israeli red-label threshold cliffs from scoring"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-08
closed_at: 2026-06-09
depends_on: []
blocks: []
roadmap_impact: true
cc_reviewed: 2026-06-09
work_type: scoring-engine
close_reason: "All 5 gate items independently verified against artifacts: (1) regression_check_001.md confirms 11 PASS / 1 known WARN / 0 FAIL, byte-identical to baseline with flag OFF; (2) both frontend JSONs (hard_cheeses_frontend_v2.json and bari-web/src/data/comparisons/hard_cheeses.json) confirm grade_distribution B=28/C=1/D=1, 30 products, run_id=run_hardcheese_redlabel_v1_001 — engine_tag is BARI_REDLABEL_V1+BARI_RECAL_P0+NOVA_FIX (NOVA_FIX suffix reflects pre-launch work from line 104-105, not a discrepancy, both files identical); (3) score_engine.py lines 1677-1680 and 1849-1851 confirm EV-REDLABEL-011 and EV-REDLABEL-009/010 scoped to REDLABEL_ENDEMIC_SATFAT_CATEGORIES; (4) task registry line 102 records Product Agent D7 co-sign APPROVED 2026-06-08, hard-cheese scope; (5) score_engine.py lines 2196-2202 confirm nova1_single_ingredient floor gated to ingredient_count<=1."
cc_comments: "Cross-category scope guard verified at score_engine.py:1680 and 1851 — sugar bands + sodium bands both gated to REDLABEL_ENDEMIC_SATFAT_CATEGORIES. Engine_tag in both frontend JSONs is BARI_REDLABEL_V1+BARI_RECAL_P0+NOVA_FIX; the +NOVA_FIX suffix is the pre-launch NOVA floor fix from the task's own activation checklist, not an unexpected divergence."
---

# TASK-REDLABEL-001 — Red Label Cliff Elimination

## Objective

Redesign Bari red-label logic so Israeli red labels do not govern grades through hard threshold
cliffs. Starting with cheese, then generalizing carefully.

**Constraint:** Do not remove red labels from the UI. Do not let red labels dominate the grade
unless multiple severe signals justify it. Bari scores food reality, not label-law artifacts.

## Problem Statement

The current engine has two cliff-edge mechanisms triggered by Israeli MoH red labels:

1. `ISRAELI_RED_LABELS_2_PLUS` cap=45 — fires for ANY 2+ labels regardless of category.
   In cheese, this fires when sat_fat (compositionally unavoidable) + sodium both exceed
   thresholds. BabyBel (NOVA-1, 4 ingredients): pre-cap weighted score 77.4 → final 39/D.

2. `HIGH_SODIUM_700MG_PLUS` cap=60 — hard cliff at 700mg. Natural goat cheese with 710mg
   sodium is treated identically to a 1300mg processed spread.

3. **Disclosure asymmetry**: 27 of 30 hard cheeses omit sat_fat from their label. These
   products escape the sat_fat cap entirely. Products that disclose sat_fat score 30–40 points
   lower than nutritionally identical undisclosed products.

## Corpus Audit (hard cheeses, 30 products)

| Product | Current score | Binding cap | Root cause |
|---------|---------------|-------------|------------|
| BabyBel 24% (hc-030) | 39/D | ISRAELI_RED_LABELS_2_PLUS=45 | sat_fat disclosed + sodium |
| גאודה הולנדית 30% (hc-027) | 54/C | HIGH_SODIUM_700MG_PLUS=60 | sodium 831mg |
| גאודה עיזים (hc-029) | 54/C | HIGH_SODIUM_700MG_PLUS=60 | natural goat cheese, 703mg |
| מותכת 13% (hc-028) | 54/C | HIGH_SODIUM_700MG_PLUS=60 | sodium 1300mg (defensible) |

## Design: BARI_REDLABEL_V1 (6 coordinated fixes)

All changes gated behind `BARI_REDLABEL_V1=on` (default OFF). Flag OFF = byte-identical.
**Product Agent D7 co-sign required before activation.**

### DD-1: Continuous regulatory_quality dimension
Replace 95/60/25 step function with severity-weighted per-label deduction:
`score = max(20, 95 − Σ min(28, 12 + excess_ratio × 15))`
Evidence: EV-REDLABEL-001 through EV-REDLABEL-004.

### DD-2: Family-aware multi-label cap (REFORMULABLE_LABELS_2_PLUS)
Exclude endemic sat_fat (dairy_protein / whole_food_fat) from the >=2 reformulable-label
count. BabyBel: reformulable_count=1 → 2+ cap does not fire.
Evidence: EV-REDLABEL-005, EV-REDLABEL-006.

### DD-3: Physio floor trigger aligned with reformulable count
`PHYSIO_2PLUS_LABELS_MIN` trigger uses reformulable_rl_count under the flag.

### DD-4: Graduated sodium bands (SODIUM_GENERAL_BANDS)
Replace HIGH_SODIUM_700MG_PLUS cliff with graduated penalties within SODIUM_FAMILY_BUDGET:
`<450 → 0 | 450–599 → −2 | 600–699 → −4 | 700–899 → −8 | ≥900 → −12`
Evidence: EV-REDLABEL-009, EV-REDLABEL-010.

### DD-5: Graduated sugar penalty bands (SUGAR_GRADUATED_BANDS)
Near-threshold continuity: 12–17.49g → −2, 17.5–24.99g → −5 (stacked with cap).
Evidence: EV-REDLABEL-011.

### DD-6: Null sat_fat imputation (EV-REDLABEL-012)
When fat ≥ 15g in dairy category and sat_fat is null:
`sat_fat_implied = fat × 0.63`, applied at 50% confidence haircut.
Closes the disclosure asymmetry without punishing transparency.
Evidence: EV-REDLABEL-012.

## Implementation Status

### Completed

- [x] QA corpus audit: 30 hard cheeses, binding cap analysis (2026-06-08)
- [x] Nutrition Agent design: full BARI_REDLABEL_V1 spec (2026-06-08)
- [x] `constants.py`: EV-REDLABEL-001–012 constants block added (2026-06-08)
- [x] `score_engine.py`: `BARI_REDLABEL_V1` env flag added (2026-06-08)
- [x] `score_engine.py`: `score_regulatory_quality()` continuous function (DD-1, DD-6) (2026-06-08)
- [x] `score_engine.py`: `REFORMULABLE_LABELS_2_PLUS` cap check (DD-2) (2026-06-08)
- [x] `score_engine.py`: Graduated sodium bands non-cereal (DD-4) (2026-06-08)
- [x] `score_engine.py`: Graduated sugar penalty bands (DD-5) (2026-06-08)
- [x] `score_engine.py`: `reformulable_rl_count` in evaluate_guardrails return (2026-06-08)
- [x] `score_engine.py`: Physio floor trigger fix (DD-3) (2026-06-08)
- [x] `bsip2_evidence_registry_v1.md`: EV-REDLABEL-001–012 entries (2026-06-08)
- [x] Regression check: PASS (11 PASS / 1 known WARN — byte-identical to baseline with flag OFF)

### Pending (activation gate)

- [x] Product Agent D7 co-sign — APPROVED 2026-06-08 (pilot scope: hard-cheese corpus only)
- [x] Pilot run: hard cheeses batch with BARI_REDLABEL_V1=on + BARI_RECAL_P0=on — COMPLETE 2026-06-08 (run_hardcheese_redlabel_v1_001; 30/30 scored; 23 grade changes; 3 B→C regressions confirmed-accepted by owner; frontend JSON updated)
- [x] Cross-category regression validation under flag-ON — DONE 2026-06-09 (BLOCKED finding resolved: EV-REDLABEL-011 sugar bands + EV-REDLABEL-009/010 general sodium now scoped to REDLABEL_ENDEMIC_SATFAT_CATEGORIES only; DD-1/DD-2/DD-3/DD-6 remain global; 3 cross-category grade changes eliminated; regression check 12/12 PASS + 1 known WARN)
- [x] Pre-launch: resolve NOVA engine/BSIP1 mismatch — DONE 2026-06-08 (HC-002 dairy fast-path + nova1_single_ingredient floor gated to ingredient_count<=1; distribution A=0/B=28/C=1/D=1)
- [x] Pre-launch: surface reformulable_rl_count + endemic_sat_fat_excluded in score_product return dict — DONE 2026-06-08

## Expected Score Changes (flag ON, cheese corpus)

| Product | Current | Projected (BARI_REDLABEL_V1 + BARI_RECAL_P0) |
|---------|---------|------------------------------------------------|
| BabyBel (sat_fat disclosed) | 39/D | ~62/C |
| גאודה עיזים (null sat_fat) | 54/C | ~62/C (imputation closes asymmetry) |
| גאודה הולנדית 30% (null sat_fat, sodium 831mg) | 54/C | ~58/C |
| Euro Cheese Gouda (null sat_fat) | 80/B | ~68/B (imputation + sodium) |
| hc-002 Israeli goat gouda (null sat_fat) | 78/B | ~56/C (imputation + sodium) |

**Note:** Full cliff elimination for cheese requires `BARI_RECAL_P0=on` in addition to
`BARI_REDLABEL_V1=on`. `BARI_RECAL_P0` alone removes the single-label sat_fat cliff
(ISRAELI_RED_LABEL_1_SAT_FAT cap=55 via R5). Both flags co-deployed = complete fix.

## Rollback

`unset BARI_REDLABEL_V1` — engine returns to byte-identical baseline.
