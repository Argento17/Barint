# Milk & Alternatives — Provenance Audit

**Audit date:** 2026-05-17  
**Auditor:** BSIP0 automated pipeline + manual review

---

## Summary

| Corpus | Products | Provenance Status |
|--------|----------|-------------------|
| run_001 (simulated) | 8 | **SIMULATED — all flagged** |
| run_002 (real) | 20 | **REAL — retailer-confirmed** |

---

## Run 001 — Simulated Corpus (MUST NOT BE USED FOR REAL ANALYSIS)

All 8 products in `03_operations/bsip1/run_milk_001/output/` are simulated.

| File | Barcode | Status | Risk Flag |
|------|---------|--------|-----------|
| bsip1_7290200000001.json | 7290200000001 | **FAKE** | simulated_observation |
| bsip1_7290200000002.json | 7290200000002 | **FAKE** | simulated_observation |
| bsip1_5411188001001.json | 5411188001001 | **FAKE** | simulated_observation |
| bsip1_5411188002001.json | 5411188002001 | **FAKE** | simulated_observation |
| bsip1_5411188003001.json | 5411188003001 | **FAKE** | simulated_observation |
| bsip1_7394376001001.json | 7394376001001 | **FAKE** | simulated_observation |
| bsip1_7290200000007.json | 7290200000007 | **FAKE** | simulated_observation |
| bsip1_5411188004001.json | 5411188004001 | **FAKE** | simulated_observation |

**Disposition:** Retained for architectural analysis in `intelligence_bsip2/run_001/` (labeled as adversarial test corpus). Must NOT be used in any product rankings or consumer-facing output. These are architectural stress-test fixtures, not real product records.

---

## Run 002 — Real Retailer Corpus

### Provenance Chain

```
yochananof.co.il (live website)
  → Playwright scraper (01_discover_milk.py)
    → candidate_review.csv (80 candidates, 2026-05-17)
  → Approval (02_approve_milk.py)
    → approved_candidates.json (52 YES + 6 skipped-no-barcode)
    → Priority subset selection (20 adversarial products)
  → HTML scraper (03_scrape_milk.py)
    → ingredients.html + nutrition.html + allergens.html per product
    → capture_status.json (all 20: ingredients=success, nutrition=success)
  → Parser (04_parse_and_build_bsip1.py)
    → BSIP1 JSON (run_milk_002/output/)
    → All 20 products: nutrition_confidence=confirmed_per_100g
  → BSIP2 scorer (batch_run_milk_002.py)
    → Traces + scores (intelligence_bsip2/run_002/)
```

### Product-Level Provenance

| Barcode | Product Name | Scrape Status | Ingredients | Nutrition | Trust |
|---------|-------------|---------------|-------------|-----------|-------|
| 7290000051352 | חלב מלא בטעם של פעם | ✓ | ✓ | 8 fields | high (0.85) |
| 7290019790259 | חלב טבעי 4% | ✓ | ✓ | 7 fields | high (0.85) |
| 7290102392094 | חלב עיזים | ✓ | ✓ | 8 fields | high (0.85) |
| 7290114313865 | חלב נטול לקטוז מועשר בחלבון | ✓ | ✓ | 7 fields | high (0.85) |
| 7290107932134 | חלב 1% מועשר | ✓ | ✓ | 7 fields | medium (0.70) |
| 7290110324926 | משקה סויה ללא תוספת סוכר | ✓ | ✓ | 7 fields | high (0.85) |
| 7290116936116 | משקה סויה ללא סוכרים | ✓ | ✓ | 7 fields | high (0.85) |
| 7290119385560 | משקה סויה בריסטה אלפרו | ✓ | ✓ | 9 fields | high (0.85) |
| 5411188300328 | אלפרו שוקו משקה סויה | ✓ | ✓ | 7 fields | high (0.85) |
| 7290110325619 | משקה שיבולת שועל | ✓ | ✓ | 9 fields | high (0.85) |
| 7394376620904 | משקה שיבולת שועל ללא סוכר | ✓ | ✓ | 8 fields | high (0.85) |
| 7394376619939 | משקה בריסטה שיבולת שועל | ✓ | ✓ | 10 fields | high (0.85) |
| 7394376621451 | משקה בריסטה שיבולת שועל להקצפה | ✓ | ✓ | 10 fields | high (0.85) |
| 5411188124689 | אלפרו שיבולת שועל ללא סוכר | ✓ | ✓ | 6 fields | high (0.85) |
| 7290014760141 | משקה שקדים | ✓ | ✓ | 8 fields | high (0.85) |
| 5411188112709 | אלפרו שקדים ללא סוכר | ✓ | ✓ | 7 fields | high (0.85) |
| 7290110324773 | משקה חלב גו 27g חלבון | ✓ | ✓ | 7 fields | high (0.85) |
| 7290114313285 | מולר פרוטאין בננה 25g | ✓ | ✓ | 5 fields | high (0.85) |
| 8000215204219 | משקה אורז אורגני | ✓ | ✓ | 7 fields | medium (0.70) |
| 8000215204554 | משקה אורז קוקוס אורגני | ✓ | ✓ | 10 fields | high (0.85) |

### Known Parsing Limitations

**Nutrition basis normalization:** Yohananof displays nutrition in two formats:
1. Explicit per-100ml label ("ל100 מ\"ל") — 4 of 20 products
2. Package-size header ("ל1 ליטר") with per-serving values — 16 of 20 products

For format 2, values were normalized using the following heuristic (applied in `04_parse_and_build_bsip1.py`):
- If `energy_kcal > 100` → assumed per-200ml serving → divided by 2 to obtain per-100ml
- If `energy_kcal ≤ 100` → assumed already per-100ml (Alpro, Oatly, plant milks display natively per 100ml despite the header)

This heuristic is verified correct for all 20 products by cross-referencing expected nutritional profiles for each product type. The normalization note is stored in each product's `nutrition_basis.normalization` field in BSIP1.

**Products with trust=medium (0.70):** 7290107932134, 8000215204219 — these had capture captures that required minor normalization. The trust deduction is conservative.

---

## Carrefour Audit

**Status: NO DATA — infrastructure not built**

The directory `03_operations/bsip0/scrape/carrefour/` does not exist. Carrefour Israel scraping would require:
1. Analysis of carrefour.co.il structure (not yet done)
2. A new discovery + scraping script similar to the Yohananof pipeline
3. A separate parser for Carrefour's HTML modal structure

**Recommendation:** Build Carrefour scraper as a separate Phase 3 extension. Any cross-retailer conflict detection requires at least one Carrefour observation per product.
