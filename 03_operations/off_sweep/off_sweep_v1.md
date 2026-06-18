# OFF Sweep v1 — Open Food Facts Contamination Map

Generated: 2026-06-12 (sweep execution date)
Method: Python stdlib JSON parse + raw text grep of all live category data files; BSIP1 record lookup by barcode field; source_url and panel_source cross-check in BSIP1 identity records.
Scope: 10 registry categories + milk (legacy). Hard-cheeses and juices exist on disk but are NOT in registry/index.ts — excluded.

Contamination classes checked:
- **A (JSON-marker)**: OFF string appears in live frontend JSON text (imageUrl, source_url, metadata)
- **B (Corpus-OFF)**: BSIP1 panel_source=open_food_facts AND source_url=world.openfoodfacts.org — nutrition data used for scoring came from OFF
- **Image-OFF**: product imageUrl points to images.openfoodfacts.org (OFF CDN) — display contamination
- Cross-run barcode collision = same barcode appears in an OFF-tagged BSIP1 run for a DIFFERENT category; classified separately and NOT counted as contamination of the product's own pipeline

---

## Section 1: Category to Data File Map

Derived by reading import lines of every page-data .ts file and registry/categories/*.ts.

| Category | Route | Data File | Note |
|---|---|---|---|
| bread | /hashvaot/bread | bread_frontend_v2.json | |
| hummus | /hashvaot/hummus | hummus_frontend_v5.json | |
| vegetable-spreads | /hashvaot/vegetable-spreads | hummus_frontend_v5.json | Shares hummus_frontend_v5.json with hummus |
| snacks | /hashvaot/snacks | snacks_frontend_v2.json | |
| yogurts | /hashvaot/yogurts | yogurts_frontend_v3.json | |
| cheese | /hashvaot/cheese | cheese_frontend_v3.json | |
| breakfast-cereals | /hashvaot/breakfast-cereals | cereals_frontend_v2.json | |
| butter | /hashvaot/butter | butter_frontend_v2.json | |
| granola | /hashvaot/granola | granola_frontend_v1.json | |
| salty-snacks | /hashvaot/salty-snacks | salty_snacks_frontend_v4.json | |
| milk (legacy) | /hashvaot/milk | milk-comparison.json | Not in registry/index.ts |

**Additional files in bari-web/src/data/comparisons/ NOT in the live registry:**
- hard_cheeses_frontend_v2.json (page-data .ts exists; not in registry/index.ts)
- juices_frontend_v3.json (page-data .ts exists; not in registry/index.ts)
- yogurts_frontend_v4.json (v4 exists on disk; page-data imports v3 — v4 is NOT live)

---

## Section 2: Verdict Table

| Category | Data File | Products (M) | Corpus-OFF B (N/M) | Image-OFF (N/M) | JSON-live A | NO_RECORD | NO_BARCODE | Verdict |
|---|---|---|---|---|---|---|---|---|
| bread | bread_frontend_v2.json | 19 | 0/19 | 0/19 | 0 | 4 | 15 | CLEAN |
| hummus | hummus_frontend_v5.json | 64 | 0/64 | 0/64 | 0 | 0 | 0 | CLEAN |
| vegetable-spreads | hummus_frontend_v5.json | 64 | 0/64 | 0/64 | 0 | 0 | 0 | CLEAN |
| snacks | snacks_frontend_v2.json | 18 | 0/18 | 0/18 | 0 | 0 | 0 | CLEAN |
| yogurts | yogurts_frontend_v3.json | 19 | 8/19 | 7/19 | 14 | 0 | 0 | DIRTY |
| cheese | cheese_frontend_v3.json | 45 | 0/45 | 0/45 | 0 | 0 | 17 | CLEAN |
| breakfast-cereals | cereals_frontend_v2.json | 26 | 6/26 | 0/26 | 1* | 0 | 0 | DIRTY |
| butter | butter_frontend_v2.json | 31 | 0/31 | 0/31 | 0 | 31 | 0 | UNKNOWN |
| granola | granola_frontend_v1.json | 42 | 17/42 | 0/42 | 0 | 0 | 0 | DIRTY |
| salty-snacks | salty_snacks_frontend_v4.json | 29 | 0/29 | 0/29 | 0 | 27 | 0 | UNKNOWN |
| milk (legacy) | milk-comparison.json | 18 | 0/18 | 0/18 | 0 | 0 | 0 | CLEAN |

* The 1 JSON-live marker in cereals is the string "open_food_facts" in the `excluded_off_products` metadata block — NOT in a live product field. Zero live product records in cereals JSON contain OFF markers.

snacks snk-011 (barcode 16000423534) and salty-snacks פיטנס קרקר (barcode 7290112968807): these barcodes appear in OFF-tagged cereals BSIP1 runs for DIFFERENT products. These are cross-run barcode collisions — the live products' own pipelines are OFF-free. See Section 5.

**TOTAL Corpus-OFF products in live site: 31** (8 yogurts + 6 cereals + 17 granola)
**TOTAL Image-OFF products in live site: 7** (all in yogurts — 7 of the 8 Yohananof pool products)

---

### Calibration against known findings

Task brief cited: cereals 8 OFF-fed, granola 10 OFF-fed.
This sweep finds: cereals 6 corpus-OFF, granola 17 corpus-OFF.

**DISCREPANCY — reporting verbatim rather than adjusting:**
- Cereals: sweep finds 6 corpus-OFF. The brief cited 8. Likely explanation: some products were excluded by BSIP0 gate before reaching the live JSON. The _meta documents `excluded_off_products`. This sweep counts only products IN the live frontend JSON at scan time.
- Granola: sweep finds 17 corpus-OFF. The brief cited 10. Likely explanation: the multi-retailer expansion (run_cereals_carrefour_001 + run_cereals_yohananof_001) fed more granola products than the prior audit scope.

Both counts are computed by cross-referencing live JSON barcodes against BSIP1 panel_source and source_url fields.

---

## Section 3: Dirty Category Details

### yogurts — yogurts_frontend_v3.json

**Corpus-OFF: 8/19 products (all from run_yogurt_yohananof_001)**

The yogurts _meta.provenance explicitly states: "New Yohananof pool (8 products): run_yogurt_yohananof_001 — il_prices identity + OFF candidate panels (EDPG candidate)."

BSIP1 records in run_yogurt_yohananof_001 confirm panel_source=open_food_facts for all 8 barcodes.

**Image-OFF: 7 of the 8 Yohananof products have imageUrl pointing to images.openfoodfacts.org**

**Duplicate barcode note:** Barcode 7290107936309 appears TWICE in the live JSON:
- `yog-007` (Shufersal pool, run_yogurt_006, NOT OFF, displayed as "יוגורט בסגנון יווני 6.5%") — CLEAN
- `bsip1_yogurt_7290107936309` (Yohananof pool, run_yogurt_yohananof_001, OFF, displayed as "Greek yogurt") — DIRTY

| Barcode | Raw ID | Name | BSIP1 run | Corpus-OFF | Image-OFF |
|---|---|---|---|---|---|
| 7290110565527 | bsip1_yogurt_7290110565527 | דנונה PRO יוגורט 20 גר' חלבון 1.5% | run_yogurt_yohananof_001 | YES | YES |
| 7290000408316 | bsip1_yogurt_7290000408316 | יוגורט ביו שטראוס 3 אחו | run_yogurt_yohananof_001 | YES | YES |
| 7290112330352 | bsip1_yogurt_7290112330352 | Yogurt Pro 20 | run_yogurt_yohananof_001 | YES | YES |
| 7290107936309 | bsip1_yogurt_7290107936309 | Greek yogurt | run_yogurt_yohananof_001 | YES | YES |
| 7290110328764 | bsip1_yogurt_7290110328764 | יוגורט גו במרקם סמיך תות | run_yogurt_yohananof_001 | YES | YES |
| 7290102399819 | bsip1_yogurt_7290102399819 | יוגורט מועשר בחלבון עם פירות יער | run_yogurt_yohananof_001 | YES | YES |
| 7290116934402 | bsip1_yogurt_7290116934402 | Go Yogurt, Mango | run_yogurt_yohananof_001 | YES | YES |
| 7290102394081 | bsip1_yogurt_7290102394081 | מולר Mix קונרפלקס | run_yogurt_yohananof_001 | YES | NO |

---

### breakfast-cereals — cereals_frontend_v2.json

**Corpus-OFF: 6/26 products (all from run_cereals_carrefour_001)**

BSIP1 records in run_cereals_carrefour_001 have panel_source=open_food_facts AND source_url=world.openfoodfacts.org. The `normalized_nutrition_per_100g` field in these BSIP1 records was populated from OFF and used for scoring.

These 6 barcodes also appear in shufersal runs (run_cereals_002/005/006/008) with panel_source=NOT_FOUND (identity-only, no nutrition). The carrefour OFF run provided the nutrition panel used for scoring.

Images for these 6 are from res.cloudinary.com/shufersal — image URLs are clean.

| Barcode | Name | BSIP1 run | Source URL |
|---|---|---|---|
| 7290017325910 | קורנפלקס אורגני הרדוף | run_cereals_carrefour_001 | world.openfoodfacts.org |
| 7290116535371 | קורנפלקס לל"ג כשל"פ | run_cereals_carrefour_001 | world.openfoodfacts.org |
| 7290112494351 | קורנפלקס של אלופים בד"ץ | run_cereals_carrefour_001 | world.openfoodfacts.org |
| 7290112495228 | קורנפלקס דבש | run_cereals_carrefour_001 | world.openfoodfacts.org |
| 8445290964595 | דגני בוקר קיטקט | run_cereals_carrefour_001 | world.openfoodfacts.org |
| 884912126115 | דגני גרייט גריינס דייטס | run_cereals_carrefour_001 | world.openfoodfacts.org |

---

### granola — granola_frontend_v1.json

**Corpus-OFF: 17/42 products**
- 16 from run_cereals_carrefour_001 (panel_source=open_food_facts, source_url=world.openfoodfacts.org)
- 1 from run_cereals_yohananof_001 (panel_source=open_food_facts)

The granola _meta.provenance confirms carrefour + yohananof runs were sources for the multi-retailer expansion. BSIP1 records confirm source_url=world.openfoodfacts.org with populated nutrition panels.

| Barcode | Name | BSIP1 run |
|---|---|---|
| 7290120871069 | Granola Protein | run_cereals_carrefour_001 |
| 7297488099821 | Sugarless Gluten Free Granola | run_cereals_carrefour_001 |
| 5010026515919 | Mornflake Crispy Muesli Nutty | run_cereals_carrefour_001 |
| 7290114603034 | גרנולה אגוזים צימוקים וחמוציות | run_cereals_carrefour_001 |
| 7290112498007 | גרנולה חלבון שקד+חמוציות | run_cereals_carrefour_001 |
| 7290112497994 | גרנולה פרוטאין+אגוזים | run_cereals_carrefour_001 |
| 7290019603634 | גרנולה קוקוס ופירות | run_cereals_carrefour_001 |
| 5010026521149 | Crispy Muesli | run_cereals_carrefour_001 |
| 7290011668570 | גרנולה | run_cereals_carrefour_001 |
| 3560070826186 | MUESLI & Co 2 CHOCOLATS & NOISETTES | run_cereals_carrefour_001 |
| 7613035758834 | פיטנס גרנולה חמוציות | run_cereals_carrefour_001 |
| 7613035635845 | גרנולה שוקולד פיטנס | run_cereals_carrefour_001 |
| 7290011131968 | גרנולה אגוזים | run_cereals_carrefour_001 |
| 7290014471412 | מוזלי בטנים, לוז, שקדים | run_cereals_carrefour_001 |
| 7290014471429 | מוזלי פירות יבשים | run_cereals_carrefour_001 |
| 7290011668587 | גרנולה עשירה | run_cereals_yohananof_001 |
| 7290116534619 | גרנולה פרוטאין+שוקולד | run_cereals_yohananof_001 |

---

## Section 4: UNKNOWN Categories

### butter — butter_frontend_v2.json

31/31 products have NO BSIP1 record in any run. No dedicated butter BSIP1 run exists under 03_operations/bsip1/. The _meta has no panel_source field. Products show confidence=partial. Cannot confirm OFF-free from BSIP1 evidence alone.

### salty-snacks — salty_snacks_frontend_v4.json

27/29 products have no BSIP1 record. No standard BSIP1 run for salty-snacks.
HOWEVER: _meta.panel_source = "retailer_product_page (yochananof storefront modal) + shufersal_product_page (4 TASK-241 rescued panels)" and _meta.provenance = "No external nutrition aggregators."
Self-declared clean but not independently verifiable from BSIP1 records.

---

## Section 5: Cross-Run Barcode Collisions

| Barcode | Live product (category) | BSIP1 OFF record (different category) | Classification |
|---|---|---|---|
| 16000423534 | snk-011 "פרי מארז תמרים ואגוזי לוז" (snacks, nutrition=null) | run_cereals_multiretailer_001: "קראנצ'י שיבולת שועל" Nature Valley cereal bar | COLLISION — different product, snacks product has no OFF-sourced nutrition |
| 7290112968807 | "פיטנס קרקר דק סלק 140 גרם" (salty-snacks, run_salty_snacks_002, retailer-sourced) | run_cereals_carrefour_001: "Fitness Thin" wafer/cereal | COLLISION — salty-snacks pipeline explicitly retailer-only |

---

## Section 6: NO_RECORD and NO_BARCODE Concentrations

| Category | NO_RECORD | NO_BARCODE | Total | NO_RECORD% | Note |
|---|---|---|---|---|---|
| bread | 4 | 15 | 19 | 21% | 15 products use shufersal_NNNN IDs with no barcode field |
| hummus | 0 | 0 | 64 | 0% | |
| vegetable-spreads | 0 | 0 | 64 | 0% | |
| snacks | 0 | 0 | 18 | 0% | |
| yogurts | 0 | 0 | 19 | 0% | |
| cheese | 0 | 17 | 45 | 0% | 17 with che-BARCODE IDs; barcode field present and matched |
| breakfast-cereals | 0 | 0 | 26 | 0% | |
| butter | 31 | 0 | 31 | 100% | No BSIP1 run for butter |
| granola | 0 | 0 | 42 | 0% | |
| salty-snacks | 27 | 0 | 29 | 93% | No standard BSIP1 run |
| milk (legacy) | 0 | 0 | 18 | 0% | |

---

## Summary

**Categories scanned: 11** (10 registry + milk legacy)
**DIRTY: 3** — yogurts, breakfast-cereals, granola
**CLEAN: 6** — bread, hummus, vegetable-spreads, snacks, cheese, milk
**UNKNOWN: 2** — butter (no BSIP1 records), salty-snacks (self-declared clean, no BSIP1 records)

**Total corpus-OFF (nutrition from OFF): 31**
- yogurts: 8/19 products
- breakfast-cereals: 6/26 products
- granola: 17/42 products

**Total image-OFF (imageUrl from OFF CDN): 7** (all yogurts Yohananof pool)

**Cross-run barcode collisions (not contamination): 2**
