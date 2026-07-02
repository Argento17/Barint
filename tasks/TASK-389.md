---
id: TASK-389
title: Juices rework (freshness re-score + de-recite copy + intro)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-24
depends_on: []
blocks: []
category_id: null
summary: >
  Same exercise as granola/cereals applied to juices (high-traffic beverage staple). Live juices_frontend_v3.json = 17 products A/D/E, shelf-relative scoring (BARI_SHELF_RELATIVE_V1 on). Run ambiguity: live _meta=run_juices_shelfrel_001 (14/17 match) vs config run_products_dir=run_juices_yohananof_002 (11/17). Already has SUGAR_METRIC. Defect: 16/17 verdicts recite sugar panel. Stages: freshness re-score -> co-sign IF grade movers -> de-recite all 17 -> intro -> two-gate -> deploy.
---

# TASK-389 — Juices rework (freshness re-score + de-recite copy + intro)

## Stage 1 — Freshness re-score (DATA AGENT, 2026-06-24)

### Scope
17 curated products in live juices_frontend_v3.json. Engine: BARI_SHELF_RELATIVE_V1=on,
BARI_FAT_TECH_V1=on, BARI_RECAL_P0=on, BARI_TASK144_FIXES=off (matching juices.json config).
Shelf stats: sugars_g median=9.50 scale=2.82 iqr n=65.
Run artifacts: `02_products/juices/bsip2_outputs/run_task389_rescore_001/`.

### Authoritative-run finding
`_meta.run_id = "run_juices_shelfrel_001"` is a post-hoc label. The actual generator was
`run_juices_yohananof_002` (Jun 7). Evidence: (a) `_meta.provenance` says "BSIP2
run_juices_yohananof_002"; (b) config `run_products_dir` points to yohananof_002; (c)
shelfrel_001 scored 32 products while the live page has 17 products curated from yohananof_002's 28.

### 3-mismatch diagnosis (shelfrel_001 traces vs live page)
Products 7290019056720, 7290000136523, 7290019056737 are orphaned in the live page.
- shelfrel_001 traces: 41.8/D, 40.1/D, 32.3/E
- Live page: 39.8/D, 38.1/D, 30.3/E (exactly -2.0 each)
- Fresh rescore: 41.8/D, 40.1/D, 32.3/E (matches shelfrel_001)
- Root cause: a post-run manual -2.0 adjustment or now-lost engine state during the Jun 7→Jun 17
  packaging step. No stored run reproduces the live page values for these 3.
- All 3 are `juice_sub_pool: ''` (empty string) fruit drinks; the SR block fires (empty != None)
  but their final scores are purely from weighted dimensions (nova=4 in both old and fresh runs).

### 17-product table (live vs fresh, current engine)

| Barcode | ID | SubPool | LiveScore | LiveGrade | FreshScore | FreshGrade | Delta | Grade? |
|---|---|---|---|---|---|---|---|---|
| 7290110114886 | jc-011 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290013608260 | jc-006 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290013153395 | jc-005 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290004030100 | jc-003 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290003009640 | jc-002 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290000525969 | jc-001 | juice_100 | 85.0 | A | 85 | A | 0.0 | — |
| 7290008690713 | jc-017 | fruit_drink | 49.1 | D | 49.1 | D | 0.0 | — |
| 7290006822192 | jc-019 | fruit_drink | 39.9 | D | 39.9 | D | 0.0 | — |
| 7290019056720 | jc-018 | fruit_drink | 39.8 | D | 41.8 | D | +2.0 | — (orphan) |
| 7290000136523 | jc-020 | fruit_drink | 38.1 | D | 40.1 | D | +2.0 | — (orphan) |
| 7290001247891 | jc-021 | nectar | 37.4 | D | 37.4 | D | 0.0 | — |
| 7290001247723 | jc-022 | nectar | 36.9 | D | 36.9 | D | 0.0 | — |
| 7290001247730 | jc-024 | nectar | 35.4 | D | 35.4 | D | 0.0 | — |
| 7290019056355 | jc-025 | fruit_drink | 33.4 | E | 33.4 | E | 0.0 | — |
| 7290019056591 | jc-026 | fruit_drink | 33.3 | E | 33.3 | E | 0.0 | — |
| 7290019056737 | jc-023 | fruit_drink | 30.3 | E | 32.3 | E | +2.0 | — (orphan) |
| 7290013153418 | jc-027 | fruit_drink | 28.5 | E | 28.5 | E | 0.0 | — |

### Grade distribution
| Grade | Live | Fresh |
|---|---|---|
| A | 6 | 6 |
| D | 7 | 7 |
| E | 4 | 4 |

Score movers (|delta|>0): 3 (the 3 orphaned products, all +2.0, no grade change)
Grade movers: 0

### Recommendation
Live scores are structurally current — grade distribution A=6/D=7/E=4 is correct for the current
engine with the approved EV-091 shelf-relative config. No co-sign needed (no grade movers).
The 3 orphaned products have an unrecoverable 2.0-point discrepancy vs all stored runs; the fresh
scores (+2.0 each) are the engine-authoritative values. A rebake will normalize them to engine values.
The rebake decision is a Stage 2 input: if copy is being refreshed anyway, rebake simultaneously.

### Stage 1 status: RETURNED — no grade movers, co-sign not required
