# BSIP0 Scrape Report — Frozen Vegetables (Shufersal)

**Run:** `shufersal_frozen_vegetables_scrape_002`
**Date:** 2026-06-10
**Retailer:** Shufersal
**Method:** Static HTTP (requests + BeautifulSoup)

## Results

| Metric | Value |
|---|---|
| Products discovered | 259 |
| Scope IN | 164 |
| Scope OUT (initial keyword filter) | 37 |
| Scope OUT (post-filter: laundry, wipes, flowers, meat, drinks) | 10 |
| Product pages scraped | 164/164 |

## Completeness

| Field | Coverage |
|---|---|
| Nutrition panel (re-extracted v2) | 145/164 (88%) |
| Ingredients | 144/164 (88%) |
| Barcode (JSON-LD) | 164/164 (100%) |
| Image URL | 164/164 (100%) |
| Product URL | 164/164 (100%) |
| Raw HTML artifact | 164/164 (100%) |

## Nutrition Detail

Re-extracted with correct HTML structure (`.text` label + `.number` value + `.name` unit). Typical panels include: energy, protein, carbs, fats, sodium, dietary fiber.

## Missing Nutrition (19)

All are single-ingredient whole foods or non-frozen items captured by broad search:
- Fresh produce: asparagus, baby carrots, fresh packed broccoli/cauliflower, corn on cob, leaf spinach, microgreens, sprouts, snow peas
- Dried legumes: "קטניות מן הטבע" brand (4 SKUs)
- Ambiguous: corn, cauliflower+broccoli tray

## Artifacts

| Path | Description |
|---|---|
| `02_products/frozen_vegetables/bsip0_outputs/bsip0_shufersal_frozen_vegetables_v3.json` | BSIP0 output v3 (cleanest) |
| `02_products/frozen_vegetables/bsip0_outputs/bsip0_shufersal_frozen_vegetables_v2.json` | BSIP0 output v2 (re-extracted nutrition) |
| `02_products/frozen_vegetables/bsip0_outputs/bsip0_shufersal_frozen_vegetables_raw.json` | BSIP0 output v1 (initial scrape) |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/product_pages/` | Raw HTML artifacts (164 files) |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/search_pages/` | Search page HTML (34 files) |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/category_pages/` | Category page HTML (9 files) |
| `03_operations/bsip0/scrape/shufersal_frozen_vegetables/scrape_log.json` | Run metadata |

## URL Pattern Discovered

Product URL: `https://www.shufersal.co.il/online/he/p/P_{code}` (not `A{barcode}` or `p/{code}` as previously assumed). All product pages accessible via static HTTP.

## Recommendations

1. Proceed to BSIP1 (scoring) — all identity data + nutrition/ingredients captured
2. Manual review the 19 missing-nutrition products — they may need removal from scope
3. The discovery_candidates manual set (33 products) can be superseded by this true scrape
