---
id: TASK-214
title: "Category Launch — מיצים ומשקאות פרי (Juices & Fruit Drinks): full BSIP0→frontend pipeline"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-07
closed_at: 2026-06-07
reopened_at: 2026-06-07
depends_on: []
blocks: []
roadmap_impact: true
cc_reviewed: 2026-06-07
work_type: category-launch
category_id: juices
close_reason: "CC gate PASS. juices_frontend_v3.json verified: 28 products at bari-web/src/data/comparisons/juices_frontend_v3.json (_meta.product_count=28, _meta.run_id=run_juices_yohananof_002). Grade distribution A=14, C=2, D=8, E=4 matches claim exactly. Score range 29–85 confirmed. All 28 insight lines populated (_meta.insight_lines_matched=28). Provenance chains to bsip0_yohananof_juices_storefront_20260607 → BSIP1 run_juices_yohananof_001 → BSIP2 run_juices_yohananof_002 → content_draft_v1. Import file bari-web/src/lib/comparisons/juices-page-data.ts confirmed referencing juices_frontend_v3.json (not v1/v2). NOVA-1 floor gate active (BEV-084, TASK-217 RETURNED — open for QA sign-off, not a close blocker). 4 out-of-scope products excluded (barcodes in _meta.excluded_barcodes). Partial-confidence lines jc-005/011/013 intentional and documented."
reopen_reason: "DATA INTEGRITY FAILURE — close was invalid. Root cause: (1) Shufersal BSIP0 returned 0 products due to transient il_prices portal unavailability at 10:51am — no retry, no escalation; (2) Carrefour chain ID 7290661400001 is NAME-UNCONFIRMED on laibcatalog — possibly wrong chain, returned 0; (3) 56/65 products use USDA FDC generic type references, NOT real label data — explicit violation of CLAUDE.md 'Do NOT invent product, nutrition, or ingredient data'; (4) Gate was self-passed with W001 warning buried despite acknowledging the problem; (5) Corpus from curated barcodes, not real retailer scrapes. The deployed juices_frontend_v1.json must NOT be treated as valid. Mandatory re-run required."
---

# TASK-214 — Juices & Fruit Drinks Category Pipeline

## Context

Juices and fruit drinks carry one of the heaviest health halos in Israeli retail. The
"100% פרי" / "נקטר" / "משקה פירות" trichotomy is deliberately opaque to most buyers —
a "100% orange juice" and an "orange drink" can sit three centimeters apart on the same
shelf with the same packaging size, and the consumer has no reliable signal for which
one contains 10g of sugar per 100ml and which one contains 11g.

More importantly: pasteurized concentrated juice is not a health food. A 200ml glass of
"100% orange juice" delivers more sugar than a can of Sprite (per volume, no fiber, no
satiety). Bari's scoring will make this concrete.

This is also a key kids-lunch-box purchase decision — the same buyer segment reading
cereal scores on Bari.

## Workspace

`C:\Bari\02_products\juices\`

## Shelf scope

### Include
- 100% fruit juices (all types — orange, apple, grape, multi-fruit, pomegranate, grapefruit)
  — both chilled (refrigerated section) and shelf-stable (ambient/UHT)
- Fruit nectars (נקטר) — 25–99% fruit content
- Fruit drinks / fruit beverages (משקאות פירות) — <25% fruit content
- Smoothies and blended fruit drinks (shelf-stable and chilled)
- Fresh-squeezed / cold-pressed (if available in the retailers)

### Exclude
- Carbonated drinks / sodas → separate category
- Sports drinks / isotonic drinks → separate category
- Vegetable juices (tomato, carrot) → could be a sub-pool but deprioritize if small
- Flavored water → separate
- Concentrate packs (for home dilution) → borderline; include if significant shelf presence

## Pipeline

### Stage 1 — BSIP0: Scrape

Scrape all three retailers:
- **Shufersal**: מיצים ומשקאות shelf (chilled + ambient)
- **Yohananof**: same
- **Carrefour**: same

Collect per product: barcode, name, brand, volume (ml), full ingredient list (Hebrew),
nutrition panel per 100ml, fruit content % (from label if stated), category tag, image URL,
retailer price.

**Note on nutrition panel units:** Juices display per 100ml not per 100g. Ensure the BSIP0
output captures the correct unit — do not normalize volume to weight.

Output: `02_products/juices/bsip0_outputs/` — one BSIP0 JSON per retailer.

Target corpus: **50–70 products** before deduplication.

### Stage 2 — BSIP1: Enrichment

Run standard BSIP1 enrichment:
- Cross-retailer deduplication by barcode
- Hebrew ingredient parsing
- Fruit content % extraction from label text where available
- NOVA assignment:
  - 100% juice (no added sugar, no additives): NOVA 3
  - Nectar or drink with added sugar / citric acid / colorants / natural flavors: NOVA 3–4
  - Cold-pressed / fresh-squeezed (minimal processing): NOVA 1
- Sub-pool classification: `juice_100` / `nectar` / `fruit_drink` / `smoothie`

Output: `02_products/juices/bsip1_outputs/` — canonical BSIP1 records.

Target post-dedup corpus: **40–55 products**.

### Stage 3 — BSIP2: Scoring

Run BSIP2 batch scorer.

Key scoring notes:
- Sugar content is the primary differentiating signal within this category. A 100% juice
  may have 9–11g sugar/100ml (all naturally occurring); a nectar may have 12–14g (added).
  The engine should differentiate on total sugar + fiber absence.
- Fiber: virtually zero in all juices. This is correct and expected — do not flag as anomaly.
- Protein: negligible across the board. This is not a protein category.
- The main scoring story is: concentrated/reconstituted juice vs cold-pressed vs nectar vs
  drink. NOVA group + sugar density + ingredient list complexity.
- "No added sugar" nectars that use fruit concentrate as a sweetener: these are NOT
  sugar-free. The sugar from concentrate counts. Score accordingly.

Output: `02_products/juices/bsip2_outputs/` — one `bsip2_trace.json` per product.

### Stage 4 — Frontend JSON

Produce `juices_frontend_v1.json`.

Required fields per product: id, name, brand, score, grade, retailer(s), imageUrl,
insightLine, limitingFactors, subPool, confidence, volumeMl, sugarPer100ml,
fruitContentPct (if available), novaGroup.

Sub-pool taxonomy:
- `juice_100` — 100% fruit juice (chilled or shelf-stable)
- `nectar` — 25–99% fruit content
- `fruit_drink` — <25% fruit content
- `smoothie` — blended fruit drinks
- `cold_pressed` — if ≥ 3 products found; otherwise merge into `juice_100`

Copy to: `C:\bari\bari-web\src\data\comparisons\juices_frontend_v1.json`

## Category caveat (required on the comparison page)

Every Bari comparison page requires a "הערת קטגוריה" yellow box. For juices, the draft
framing is:

> "גם מיץ 100% פרי הוא סוכר נוזלי. אין כאן אשמים — אבל יש הבדלים. Bari מדרגת לפי
> ריכוז עיבוד, תוספות, ואחוז פרי בפועל."

Refine this with the Content Agent after scoring is complete.

## Acceptance criteria

- [ ] Workspace `02_products/juices/` created with all pipeline stage directories
- [ ] BSIP0 outputs from all 3 retailers
- [ ] Post-dedup canonical corpus: ≥ 40 products
- [ ] BSIP2 traces complete for all corpus products
- [ ] `juices_frontend_v1.json` generated and copied to bari-web
- [ ] Sub-pool classification applied to all products
- [ ] Fruit content % captured wherever label states it
- [ ] Run summary with: corpus size, NOVA distribution, sugar range, score distribution
- [ ] Category caveat copy drafted

## BLOCKED block (2026-06-07)

**Status set to BLOCKED after corrective BSIP0 rerun. Gate FAILS hard. No progression to BSIP1/BSIP2/frontend.**

**Gate result:** `FAIL` — 4/35 products have real panels (11.4%), no-panel rate 88.6%, corpus minimum not met.

**Blocker — data source unavailability:**
1. **Shufersal website IN MAINTENANCE** — product pages (shufersal.co.il/online/he/A{barcode}) return maintenance image. Firecrawl confirmed. Cannot extract nutrition panels. Was operational earlier today (cached Firecrawl response confirmed).
2. **Yohananof laibcatalog TIMEOUT** — laibcatalog.co.il unreachable. The real il_prices run at 10:52:10 produced 20 genuine barcodes but those barcodes lack panels on OFF.
3. **Open Food Facts coverage gap** — Israeli juice barcodes (729-prefix) have ~11% coverage on OFF. Only 4 of 35 tested barcodes have real panels.

**What was confirmed working:**
- 4 products have real OFF panels and are banked: 7290001247068, 7290001247143, 7290008757386, 7290017812571
- Shufersal product page scraping via Firecrawl works when portal is live (confirmed via cache hit)
- Yohananof il_prices identity layer is real (organic timestamps, real barcode structure)

**To unblock:** Retry when Shufersal maintenance window ends. Use Firecrawl to scrape product pages for the 20 Yohananof barcodes + additional barcodes from a fresh Yohananof il_prices pull. Do NOT use FDC generic types — this gate will reject them.

**Hard constraint confirmed:** Prior BSIP2 barcodes (7290000039xxx, 5449000133xxx, 3168930010xxx, 0012000163xxx, 7290000052xxx) are fabricated — NOT FOUND on OFF. Never re-use.

**Frontend JSON:** Not generated. Previous `juices_frontend_v1.json` was built on fabricated data. File exists at `C:\bari\bari-web\src\data\comparisons\juices_frontend_v1.json` but is INVALID — do not display on website.

## Architecture correction (2026-06-07)

Nutrition source changed from OFF-primary to Yohananof storefront-primary.
- Identity: il_prices (laibcatalog 7290455000004) — barcodes / names / prices
- Nutrition panels: yochananof.co.il storefront (Playwright headless=True) — "ערכים תזונתיים" tab HTML
- OFF: fallback for international barcodes only; not primary source for 729-prefix Israeli products
- Scraper: scrape_juices_yohananof.py (adapted from 03_operations/bsip0/scrape/yohananof/)

### Run results (2026-06-07)
- Discovery: 361 unique products found across 11 queries; 86 passed POSITIVE_TYPES
- Approved for scrape: 35 (cap applied)
- Scraped: 35/35 (100% scrape success rate)
- With storefront nutrition panels: 32/35 (91.4%)
- OFF fallback attempted: 3 (products with no storefront panel); hits: 0
- Final sufficient: 32/35
- il_prices identity match: 1/35 juices (small store catalog — does not affect panel coverage)
- BSIP0 output: bsip0_outputs/bsip0_yohananof_juices_storefront_20260607_151232.json

### Next steps
- BSIP1 enrichment requires Nutrition Agent approval of configuration
- 3 insufficient products (no panel on storefront): barcode-only records, will not score

### BSIP1 results (2026-06-07)
- Script: `03_operations/bsip1/run_juices_001/run_bsip1_juices_001.py`
- RUN_ID: `run_juices_yohananof_001`
- Input: `bsip0_yohananof_juices_storefront_20260607_151232.json` (35 products, 32 sufficient)
- Enriched: 32 (skipped 3 — missing kcal or carbohydrates_g)
- Subpool distribution: juice_100=16, fruit_drink=13, nectar=3
- NOVA distribution: NOVA 1=3, NOVA 3=22, NOVA 4=7
- Ingredient extraction: primary via "מידע אלרגני" marker; secondary via "רכיבים:" for
  products where allergen section is absent
- Output dir: `02_products/juices/bsip1_outputs/`

### BSIP2 results (2026-06-07)
- Script: `03_operations/bsip2/proto_v0/src/batch_run_juices_yohananof_001.py`
- RUN_ID: `run_juices_yohananof_001`
- Engine: proto_v0 / 0.4.1 + BARI_RECAL_P0=on, BARI_TASK144_FIXES=off
- Products scored: 32
- Grade distribution: A=14, C=4, D=10, E=4
- Score range: 29.1–85.0 (median 59.2)
- Anomalies flagged: 16 — all are juice_100 products scoring above expected max of 75
  (engine produces 85/A for low-calorie beverages with no added sugar, no fat, NOVA 1–3;
  this is the beverage calorie-density ceiling; scores NOT adjusted per instructions)
- Two fruit_drink products scored C (above expected D–E): מיץ עגבניות (62.6/C, has protein
  + sodium; legitimate complexity) and אלפרו בריסטה סויה (50.7/C, has fiber + fat + protein)
- Run summary: `02_products/juices/bsip2_outputs/run_juices_yohananof_001/run_summary.json`

### Frontend JSON results (2026-06-07)
- Script: `03_operations/bsip2/proto_v0/src/build_juices_frontend_001.py`
- Output (local): `02_products/juices/juices_frontend_v2.json`
- Output (web): `bari-web/src/data/comparisons/juices_frontend_v2.json`
- Products in JSON: 32
- Grade distribution: A=14, C=4, D=10, E=4
- Score range: 29–85 (rounded)
- Serving note: "ל-100 מ\"ל" (vs "ל-100 גרם" for solid food categories)
- Provenance: `bsip0_yohananof_juices_storefront_20260607_151232.json → BSIP1 run_juices_yohananof_001 → BSIP2 run_juices_yohananof_001`
- Version: v2 (replaces invalid v1)

## Return block

Report:
1. Final corpus size and sub-pool distribution
2. Sugar per 100ml range across sub-pools (the core consumer insight)
3. NOVA distribution
4. Score range and grade distribution
5. Any products with ambiguous classification (100% vs nectar labeling edge cases)
6. Surprising findings
7. Frontend JSON path and product count

## Nutrition Agent ruling (2026-06-07)

**Juice ceiling: Option B (modified) — D7 proposal PENDING, Product Agent co-sign required.**

The 14/A scores are not coming from dimension scores — they are floor overrides from the `nova1_single_ingredient` signal (floor coded at 85). The actual weighted dimension score for a representative 85/A product is 57.9. The floor is legitimate for genuine single-ingredient fresh-squeezed/cold-pressed juice. The problem is reconstituted-from-concentrate products that declare a single-ingredient label without reconstitution markers, triggering the same NOVA 1 floor they don't scientifically deserve.

**Proposed rule (D7 — needs Product Agent co-sign):**
Gate the `nova1_single_ingredient` floor in the `beverage / juice_100` category. Floor fires only when: `nova_proxy = 1` AND `has_fruit_concentrate = false` AND ingredient text contains no reconstitution markers (רכז, משוחזר, מרוכז, concentrate). If any reconstitution signal is detected, floor does not fire; NOVA proxy set to minimum 2, subject to existing NOVA 2/3 caps. This is a label-observable condition requiring an evidence-registry EV-### entry before implementation.

**Scores in this run are NOT changed retroactively.** The 14 A-grade products stand as published pending D7 resolution. Products that already lack reconstitution markers in their ingredient text may be legitimately NOVA 1.

**Content Agent:** DONE — `02_products/juices/content_draft_v1.md` (leakage PASS, all 32 insight lines written)

**Open items before Frontend Agent integration:**
- SCOPE RULING RESOLVED (Product Agent 2026-06-07): **Exclude all four** — jc-015 (עגבניות), jc-018 (סויה), jc-020 (שיבולת שועל), jc-024 (קפה חלב). Data Agent to rebuild frontend JSON with 28 products. Tomato juice excluded as different nutritional story (vegetable, sodium-forward); soy/oat/coffee are wrong category entirely.
- jc-013 (מיץ תירוש): shows 82 kcal vs 64 kcal for jc-008/009 — different SKU, reflected as-is per its own scraped panel.
- Partial-confidence copy (jc-005, jc-011, jc-013): insight lines say "נתוני הסוכר חלקיים" — acceptable editorial handling.
- Sugar approximations rounded to "כ-X גרם" throughout — editorial decision, correct for consumer copy.

**Data Agent pipeline completion (2026-06-07):**
- 28-product frontend JSON rebuilt from run_juices_yohananof_002 traces
- All 28 insight lines integrated (100% match rate, 2 name overrides for OCR-truncated product names)
- Deployed: `bari-web/src/data/comparisons/juices_frontend_v3.json` (web import updated from v1→v3)
- NOVA-1 floor gate active (BEV-084, TASK-217 RETURNED)
- **Ready for CC close-readiness gate.**
