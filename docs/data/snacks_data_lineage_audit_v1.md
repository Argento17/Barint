# Snacks Data Lineage Audit v1

**Date:** 2026-05-29  
**Scope:** 18 products on `/hashvaot/snacks`  
**Mode:** Forensic audit only — no scoring, copy, or corpus changes

---

## Executive summary

| Layer | Nutrition | Ingredients | Verdict |
|-------|-----------|-------------|---------|
| BSIP0 (`observations_bsip0/yohananof/`) | **16/18** shelf products parsed from HTML | **16/18** parsed | Capture largely complete |
| BSIP1 (`canonical_bsip1/run_001/`) | **18/18** | **18/18** | **Intact** |
| BSIP2 (`bsip2_outputs/run_snack_bars_synthesis_001/`) | **18/18** in `L1_observed_signals` | **18/18** | **Scoring consumed data** |
| CE handoff → `snacks_frontend_v2.json` | **0/18** populated | **0/18** | **Intentional null handoff** |
| Production shelf (expansion panel) | **0/18** visible | **0/18** visible | **Display gap only** |

**CE red-team finding — refined verdict:**  
The claim that snack products have null nutrition and ingredients is **TRUE on the production shelf corpus** and **FALSE for the BSIP2 scoring run** that produced current scores. Data was **not lost upstream**; it was **not propagated into the frontend JSON** at CE v2 handoff.

---

## Pipeline diagram

```text
Yohananof scrape (2026-05-15)
        │
        ▼
BSIP0  observations_bsip0/yohananof/{barcode}/
       ├── nutrition.html
       ├── ingredients.html
       └── product.json          ← parsed nutrition + ingredients_raw_he
        │
        ▼
BSIP1  canonical_bsip1/run_001/bsip1_{barcode}.json
       ├── normalized_nutrition_per_100g
       └── ingredients_text_he
        │
        ▼
BSIP2  bsip2_outputs/.../bsip1_{barcode}/bsip2_trace.json
       ├── L1_observed_signals (nutrition + ingredient_list)
       ├── dimension_scores (nutrient_density, glycemic_quality, …)
       └── final_score_estimate  ← matches shelf score (rounded)
        │
        ▼
CE editorial  snack-page-data.ts + CE Handoff v2
       ├── scores, grades, insightLine, expansion copy
       └── confidence_level (structural, not nutrition-panel)
        │
        ▼
Production   snacks_frontend_v2.json
       ├── expansion.nutrition → ALL NULL (hardcoded)
       └── expansion.ingredients → ALL NULL
        │
        ▼
UI           ComparisonShelfPage → ProductRow → ExpansionSection
               (nutrition/ingredient block hidden when null)
```

---

## Stage-by-stage audit

### Stage 1 — BSIP0 (raw capture)

**Location:** `C:\Bari\02_products\snack_bars\observations_bsip0\yohananof\`

| Metric | Value |
|--------|------:|
| Product directories | 48 |
| `nutrition.html` files | 48 |
| `ingredients.html` files | 48 |
| `product.json` files | 48 |
| Audit: `usable_raw` | 39 |
| Audit: `partial_raw` | 9 |

**Shelf cohort (18 barcodes):**

| BSIP0 status | Count | Products |
|--------------|------:|----------|
| Parsed nutrition + ingredients | 16 | All except snk-006, snk-019 folder lookup |
| No yohananof folder | 1 | snk-006 (`7290118427858`) — not on Yohananof scrape |
| Folder under alternate barcode | 1 | snk-019 — data at `7290118247896/` (image URL typo); `product.json` declares correct barcode `7290118427896` |

**Parsing quality notes:**
- Most shelf products: `parser_status.nutrition_present=true`, `ingredients_present=true`, basis `per_100g`.
- snk-020 (`7290014525306`): audit `partial_raw`; ingredients string truncated (`ס????`) but nutrition fully parsed (402 kcal, 35.5g sugar).
- snk-001 (`7290011498870`): parsed 92 kcal/100g — **implausible for a date bar** (likely retailer label basis error; see BSIP0 recovery doc). Data still flowed to BSIP1/BSIP2 as captured.

**Loss at this stage:** None for yohananof-scraped products. snk-006 never captured at yohananof (Carrefour-only SKU).

---

### Stage 2 — BSIP1 (canonical normalization)

**Location:** `C:\Bari\02_products\snack_bars\canonical_bsip1\run_001\bsip1_*.json`

| Metric | Shelf (18) |
|--------|----------:|
| BSIP1 file exists | 18/18 |
| `normalized_nutrition_per_100g.energy_kcal` non-null | 18/18 |
| `ingredients_text_he` non-empty | 18/18 |

**Example (snk-001):**

```json
"normalized_nutrition_per_100g": {
  "energy_kcal": 92.0,
  "protein_g": 1.6,
  "sugars_g": 15.5,
  "fat_g": 0.0
},
"ingredients_text_he": "תמרים ( 76%), מחית שקדים מולבנים (22%), …"
```

**snk-006 exception:** Single-source Carrefour (`source_retailers: ["carrefour_israel"]`), full nutrition + 520-char ingredient string. No yohananof BSIP0 folder.

**Loss at this stage:** **None.** BSIP0 → BSIP1 promotion succeeded for all scored products.

---

### Stage 3 — BSIP2 (scoring engine)

**Location:** `C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_synthesis_001\products\bsip1_{barcode}\bsip2_trace.json`

Verified 2026-05-29: all 18 shelf scores match `final_score_estimate` (±1 rounding).

| Product | Shelf score | BSIP2 estimate | L1 kcal | L1 ingredient_count |
|---------|------------:|---------------:|--------:|--------------------:|
| snk-001 | 70 | 70.0 | 92 | 3 |
| snk-004 | 58 | 58.6 | 97 | 5 |
| snk-002 | 56 | 56.7 | 93 | 2 |
| snk-015 | 55 | 55.0 | 405 | 4 |
| snk-003 | 53 | 53.3 | 196 | 9 |
| snk-016 | 51 | 50.7 | 90 | 9 |
| snk-009 | 47 | 47.4 | 196 | 18 |
| snk-005 | 46 | 46.5 | 78 | 16 |
| snk-018 | 46 | 44.3 | 198 | 13 |
| snk-010 | 45 | 45.7 | 198 | 19 |
| snk-011 | 43 | 43.7 | 398 | 6 |
| snk-012 | 42 | 42.3 | 395 | 7 |
| snk-019 | 41 | 39.8 | 89 | 19 |
| snk-017 | 39 | 38.7 | 139 | 24 |
| snk-020 | 32 | 33.1 | 402 | 13 |
| snk-007 | 29 | 29.4 | 392 | 22 |
| snk-006 | 17 | 17.9 | 479 | 21 |
| snk-013 | 13 | 16.6 | 451 | 15 |

**Active scoring dimensions using nutrition (snk-001 trace):**
- `nutrient_density` — protein, fiber
- `calorie_density` — energy_kcal
- `glycemic_quality` — sugars_g penalty
- `satiety_support` — protein × kcal
- `confidence_score` — reductions for missing fiber/sodium fields

**Loss at this stage:** **None.** Engine operated on BSIP1 nutrition and ingredients for all 18 products.

---

### Stage 4 — CE handoff (`snack-page-data.ts`)

**Location:** `src/lib/comparisons/snack-page-data.ts`

Contains structural scoring metadata used for filters and engine routes:
- `ingredient_count`, `nova`, `structural_base`, `explainability_tags`, `confidence_level`
- Does **not** embed per-product nutrition tables or ingredient strings

Confidence mapping:

| `confidence_level` | Hebrew label | Basis |
|--------------------|--------------|-------|
| `full` | נתונים מלאים יחסית | Structural metadata complete |
| `partial` | נתונים חלקיים | Structural gaps or single-source |

**Not** tied to `expansion.nutrition` population.

---

### Stage 5 — CE Handoff v2 → `snacks_frontend_v2.json`

**Authoritative doc:** `C:\Bari\02_products\snack_bars\reports\snacks_ce_handoff_v2.md`

Explicit instruction (line 127):

> Do not invent product details or **fill in null nutrition values**

**Legacy builder** (`scripts/build-snacks-frontend-v2.ts`, deprecated) hardcodes:

```typescript
nutrition: {
  energyKcal: null, protein: null, sugar: null,
  fat: null, fiber: null, sodium: null,
},
ingredients: null,
```

CE v2 corpus rewrite preserved this null pattern while adding `limitingFactors`, score order, and editorial expansion copy.

**Loss at this stage:** **Intentional.** Nutrition and ingredients were available in BSIP1 but excluded from the shelf-facing JSON schema population step.

---

### Stage 6 — Production UI

**Loader:** `src/lib/comparisons/snacks-comparison-page-data.ts` — static import of JSON  
**Display:** `src/components/shared/expansion-section.tsx`

```typescript
// Nutrition block only renders when any value is non-null
Object.values(expansion.nutrition).some((v) => v != null)
// Ingredients hidden when null/empty
Boolean(expansion.ingredients?.trim())
```

Maadanim contrast: `maadanim_frontend_v2.json` ships populated `energyKcal`, `protein`, `ingredients` from audit export — snacks never received equivalent mapping pass.

---

## Where data was lost

| Transition | Lost? | Intentional? |
|------------|-------|--------------|
| BSIP0 → BSIP1 | No | — |
| BSIP1 → BSIP2 | No | — |
| BSIP2 → snack-page-data scores | No (scores copied) | — |
| BSIP1 → snacks_frontend_v2 expansion | **Yes** | **Yes** — CE v2 scope excluded nutrition panel population |
| Deprecated builder null template | Reinforces nulls | Legacy artifact; must not re-run |

---

## Audit tooling

Reproducible cross-layer check:

```bash
node scripts/audit-snacks-data-lineage.mjs
```

Outputs per-product BSIP0/BSIP1/frontend comparison and summary counts.

---

## Conclusion

Bari is **not** missing product information in the historical scrape/canonical/scoring pipeline for the 18 displayed snacks. Bari **is** missing that information on the **production shelf JSON and UI**, by an intentional CE v2 handoff decision and the deprecated builder's null template.

Before any scoring-system redesign, the priority gap is **frontend corpus hydration** from existing BSIP1 assets — not re-scraping or re-architecting BSIP2.
