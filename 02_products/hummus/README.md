# Hummus and Savory Dips — Category Workspace

**Category ID:** hummus  
**Stage:** BSIP0 ready (Stage 2 scaffolding complete)  
**Date scaffolded:** 2026-05-30  
**Tasks:** TASK-018 (Stage 0–1), TASK-024 (Execution Plan), TASK-025 (Shelf Mapping), TASK-026 (Scope Decision), TASK-027 (Stage 2)

---

## Category scope

**Primary:** Hummus (all variants) — plain, flavoured, light, organic, protein-enriched  
**Secondary:** Eggplant spreads, matbucha, Turkish salad, cooked pepper spreads  
**Excluded:** Ready-to-eat tahini dips (defer to Tahini category), dairy spreads, condiments, schug/harissa, pickles

See [corpus_filter.md](corpus_filter.md) for full IN/OUT rules and the tahini-hummus blend decision (TASK-026).

---

## Workspace structure

```
hummus/
├── corpus_filter.md          Locked scope definition (TASK-026 gate)
├── README.md                 This file
├── observations_bsip0/
│   ├── shufersal/            Shufersal scrape outputs
│   │   ├── candidate_review.csv    (created by 01_discover)
│   │   ├── all_discovered_raw_*.json
│   │   └── {product_code}.json     (one per approved product)
│   └── yohananof/            Yohananof scrape outputs
│       ├── candidate_review.csv
│       ├── all_discovered_raw.json
│       └── {barcode}/              (one dir per approved product)
│           ├── discovery.json
│           ├── ingredients.html
│           ├── nutrition.html
│           ├── allergens.html
│           └── capture_status.json
├── canonical_bsip1/          BSIP1 enriched records (populated after BSIP0 gate)
├── intelligence_bsip2/
│   └── run_hummus_001/       BSIP2 scored traces (populated after BSIP1)
└── reports/                  Gate reports, analysis
```

---

## Pipeline — BSIP0 execution order

### Step 1 — Shufersal discovery (run first)

```
cd C:\Bari\03_operations\bsip0\scrape\shufersal_hummus
python 01_discover_hummus_shufersal.py
```

Opens: `observations_bsip0/shufersal/candidate_review.csv`  
Edit: set `approved_for_scrape = YES` for IN-scope products using `corpus_filter.md` rules.

### Step 2 — Shufersal scrape

```
python 02_scrape_hummus_shufersal.py
```

Outputs one JSON per approved product to `observations_bsip0/shufersal/`.

### Step 3 — Shufersal BSIP0 gate audit

```
python 03_audit_bsip0_hummus.py
```

Gate criteria (from `corpus_filter.md`):

| Criterion | Minimum |
|---|---|
| Approved products | ≥ 30 (target 50–60) |
| Nutrition coverage | ≥ 80% |
| Ingredient coverage | ≥ 70% |
| Image availability | ≥ 90% |
| Retailer traceability | 100% |

If gate fails on product count, uncomment A162405 traversal in the discover script.

### Step 4 — Yohananof discovery (supplementary)

```
cd C:\Bari\03_operations\bsip0\scrape\yohananof_hummus
python 01_discover_hummus_yohananof.py
```

Requires: `playwright install chromium`  
Opens: `observations_bsip0/yohananof/candidate_review.csv`  
Edit: set `approved_for_scrape = YES` for net-new products not already captured from Shufersal.

### Step 5 — Yohananof scrape

```
python 02_scrape_hummus_yohananof.py
```

Outputs per-barcode subdirectory (HTML tabs + discovery JSON) to `observations_bsip0/yohananof/`.

---

## BSIP0 gate thresholds (from corpus_filter.md)

| Criterion | Minimum |
|---|---|
| Total approved products | ≥ 30 (target 50–60) |
| Nutritional label coverage | ≥ 80% (calories + protein + carbs + fat) |
| Ingredient list availability | ≥ 70% |
| Product image availability | ≥ 90% |
| Retailer traceability | 100% |
| Corpus filter filed | Yes |

---

## Expected product distribution

| Type | Count estimate |
|---|---|
| Plain hummus (all brands) | 15–20 |
| Flavoured hummus (garlic, spicy, za'atar, pine nut) | 10–15 |
| Light / 0% / protein hummus | 5–8 |
| Organic / bio hummus | 3–5 |
| Eggplant spreads (secondary) | 8–12 |
| Matbucha / Turkish salad / pepper spreads | 6–10 |
| **Total** | **47–70** |

---

## Key decisions (locked)

- **Tahini dips excluded** — TASK-026: ready-to-eat tahini dips route to `whole_food_fat`, not `sauce_spread`. Defer to Tahini category.
- **Schug / harissa excluded** — hot condiments, different consumer purpose.
- **Multi-packs excluded** — single consumer units only.
- **Catering sizes (≥1 kg) excluded** — consumer retail only.

See `corpus_filter.md` for the tahini-hummus blend rule.

---

## Stage progression

| Stage | Status | Task |
|---|---|---|
| Stage 0 — scope definition | ✅ Complete | TASK-018 |
| Stage 1 — corpus filter + shelf mapping | ✅ Complete | TASK-025, TASK-026 |
| Stage 2 — BSIP0 scaffolding | ✅ Complete | TASK-027 |
| Stage 3 — BSIP0 execution (scrape + gate) | ⏳ Ready to run | — |
| Stage 4 — BSIP1 enrichment | ⏳ Pending BSIP0 gate | — |
| Stage 5 — BSIP2 scoring | ⏳ Pending BSIP1 | — |
| Stage 6 — Frontend dataset | ⏳ Pending BSIP2 | — |
