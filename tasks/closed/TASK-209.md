---
id: TASK-209
title: "Project Beaver — Retailer field backfill: all categories except butter"
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-07
closed_at: 2026-06-07
depends_on: [TASK-207]
blocks: [TASK-210]
roadmap_impact: false
cc_reviewed: null
work_type: data-fix
project: beaver
close_reason: "All 8 in-scope files verified: 0 products missing retailer. Spot-checked yogurts (11/shufersal), cheese (52/shufersal), bread (24/shufersal) — each 100% populated. Butter untouched at {shufersal:18, yohananof:17, carrefour:4}. Snacks {yohananof:17, carrefour:1} confirmed against BSIP1 evidence. Superseded versions (hummus v3/v4, maadanim v2, cheese v1) and archived olive_oil_v1 correctly excluded per spec. Full verification script: 8/8 PASS."
cc_comments: "Snacks corpus is Yohananof+Carrefour only — no Shufersal snack bar products exist in the current corpus. TASK-210 (multi-retailer expansion) should add snacks to scope to get Shufersal snack bar coverage."
---

# TASK-209 — Retailer Field Backfill

## Context

The `retailer` field is populated on `butter_frontend_v2.json` (values: `shufersal`, `yohananof`, `carrefour`)
but is absent (`null`) on all other live categories. The field is needed for:
1. Frontend filtering by retailer (comparison page "filter by chain" feature, planned for Project Beaver frontend phase)
2. Multi-retailer expansion (TASK-210) — new products from additional chains need the same field
3. Data provenance: knowing which chain the score reflects

## Scope

All live frontend JSONs **except** `butter_frontend_v2.json` (already has retailer):

| File | n_products | Source retailer |
|------|-----------|----------------|
| hummus_frontend_v5.json | 64 | shufersal |
| yogurts_frontend_v2.json | 11 | shufersal |
| cereals_frontend_v1.json | 38 | shufersal |
| granola_frontend_v1.json | 53 | shufersal |
| snacks_frontend_v2.json | 18 | shufersal |
| maadanim_frontend_v3.json | 84 | shufersal |
| cheese_frontend_v2.json | 52 | shufersal |
| bread_frontend_v2.json | 24 | shufersal |

**Note on olive_oil_frontend_v1.json:** This file exists but the page was removed because all 13
products scored 60/C (no differentiation). Do NOT backfill this file — it's archived, not live.

## Instructions

For each file in scope:

1. Verify the source retailer by checking the BSIP0 scrape directory — e.g. `03_operations/bsip0/scrape/shufersal_hummus/` confirms source
2. Add `"retailer": "shufersal"` to every product object in the JSON
3. Preserve all other fields exactly — this is a pure additive change
4. The field should be added after `"confidence"` in the object key order (for readability) but JSON key order doesn't affect the schema

## Verification

After backfill, run this check:
```python
import json, glob
for f in glob.glob('bari-web/src/data/comparisons/*.json'):
    with open(f, encoding='utf-8') as fp:
        d = json.load(fp)
    prods = d.get('products', [])
    missing = sum(1 for p in prods if not p.get('retailer'))
    if missing > 0:
        print(f"{f}: {missing} products still missing retailer")
```
Expected output after fix: only `olive_oil_frontend_v1.json` may appear (it's excluded from scope).

## Acceptance criteria

- [ ] All 8 in-scope files updated — each product has a non-null `retailer` field
- [ ] Source retailer confirmed against BSIP0 scrape directory for each category (not assumed)
- [ ] Zero other fields modified — diff is purely additive
- [ ] Verification script shows 0 missing retailer across the 8 updated files
- [ ] `butter_frontend_v2.json` untouched

## Return block (for Data Agent)

Report:
1. Total products updated (should be ~364)
2. Confirm: source retailer for each category verified against BSIP0 directory (yes/no)
3. Any category where the source retailer was ambiguous or mixed (flag for review)

---

## Return Block — Data Agent, 2026-06-07

**Run script:** `C:\Bari\03_operations\scripts\task209_retailer_backfill.py`

### 1. Total products updated

344 products across 8 files. (Task spec estimated ~364; actual file counts are the authoritative figures.)

| File | Products updated | Retailer assigned |
|------|-----------------|-------------------|
| hummus_frontend_v5.json | 64 | shufersal |
| yogurts_frontend_v2.json | 11 | shufersal |
| cereals_frontend_v1.json | 38 | shufersal |
| granola_frontend_v1.json | 53 | shufersal |
| maadanim_frontend_v3.json | 84 | shufersal |
| cheese_frontend_v2.json | 52 | shufersal |
| bread_frontend_v2.json | 24 | shufersal |
| snacks_frontend_v2.json | 18 | yohananof (17) + carrefour (1) |

### 2. BSIP0 source directory confirmation

| Category | BSIP0 evidence | Confirmed |
|----------|----------------|-----------|
| hummus | `03_operations/bsip0/scrape/shufersal_hummus/` exists | YES |
| yogurts | `03_operations/bsip0/scrape/shufersal_yogurt/` exists | YES |
| cereals | `03_operations/bsip0/scrape/shufersal_cereals/` exists | YES |
| granola | `03_operations/bsip0/scrape/shufersal_cereals/` exists (shared shelf) | YES |
| maadanim | `03_operations/bsip0/scrape/shufersal_maadanim/` exists | YES |
| cheese | `03_operations/bsip0/scrape/shufersal_cheese/` exists | YES |
| bread | `02_products/bread_retail_003` bsip0 raw: `retailer_id = "shufersal"` across all 258 records | YES |
| snacks | No `shufersal_snacks` directory exists | FLAG — see below |

### 3. Snacks: source retailer ambiguity — CORRECTION TO TASK SPEC

The task spec listed snacks as `"shufersal"`, but this is incorrect per BSIP1 evidence:

- No `shufersal_snacks` BSIP0 directory exists in `03_operations/bsip0/scrape/`
- The snack bars `observations_bsip0/` has `carrefour/` and `yohananof/` subdirectories only
- BSIP1 `source_retailers` field across all 18 live snack products shows: Yohananof (17 products), Carrefour (1 product — snk-006 / bsip1_7290118427858)
- 2 additional products (snk-004, snk-019) also appear in Carrefour but have Yohananof as primary

**Decision (within lane, D2 Data):** Assigned per-product retailer from authoritative BSIP1 source_retailers rather than the incorrect spec value. snk-006 = `"carrefour"`, all 17 others = `"yohananof"`. Flagged here for Product Agent review — if the snacks page is intended to show Shufersal availability, that requires a corpus expansion (out of scope for this task).

### 4. Verification result

All 8 in-scope files: 0 products missing retailer field.

```
PASS hummus_frontend_v5.json:   all 64 products
PASS yogurts_frontend_v2.json:  all 11 products
PASS cereals_frontend_v1.json:  all 38 products
PASS granola_frontend_v1.json:  all 53 products
PASS maadanim_frontend_v3.json: all 84 products
PASS cheese_frontend_v2.json:   all 52 products
PASS bread_frontend_v2.json:    all 24 products
PASS snacks_frontend_v2.json:   all 18 products
```

`butter_frontend_v2.json` untouched (already had retailer field). `olive_oil_frontend_v1.json` untouched (archived, excluded per spec).

Old versions present in the directory (hummus v3/v4, maadanim v2, cheese v1) were not updated — they are superseded and not live.
