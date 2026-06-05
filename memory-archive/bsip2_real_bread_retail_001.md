---
name: bsip2-real-bread-retail-001
description: "BSIP2 Real Retailer Bread/Cracker Run — 42 real Israeli products, 12 reports, brutal reality gap vs synthetic"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Real retailer bread/cracker corpus run completed 2026-05-25.

**Why:** First run with real (non-synthetic) Israeli product data. Reality test against synthetic bread_light corpus.

**How to apply:** When assessing pipeline robustness or data strategy, this run documents the actual state of publicly accessible Israeli food data and the gaps that block a 100-product real corpus.

## Source

Open Food Facts (world.openfoodfacts.org) — real barcodes (729xxxxxxx GS1 Israel), real Hebrew ingredients, real nutrition tables.

Israeli retail websites (Shufersal, Rami Levy, Victory, Carrefour) blocked: Shufersal in maintenance mode; all others returned HTTP 403.

## Products

- Fetched: 42 unique relevant products (scrape across categories, keywords, brands)
- Target: 100 minimum — NOT ACHIEVED. This is the honest outcome.
- OFF has ~41 Israeli-tagged bread products. Crackers: near-zero.

## File locations

- Raw JSON: `C:\Bari\02_products\bread_retail_001\raw\off_BARCODE.json`
- BSIP1 format: `C:\Bari\02_products\bread_retail_001\bsip1\bsip1_BARCODE.json`
- Reports: `C:\Bari\02_products\bread_retail_001\reports\` (12 reports)
- Scrape log: `C:\Bari\02_products\bread_retail_001\scrape_log.json`

## Key pipeline results

| Metric | Real (42) | Synthetic (32) |
|:-------|:----------|:----------------|
| Avg score | 56.8 | 62.8 |
| Avg fiber | 7.0g | 5.9g |
| FULL degradation | 9% | 87% |
| INSUFFICIENT | 40% | 0% |

- Routing: 52% → bread, 42% → default (English-only name, no anchor possible)
- Confidence bands: insufficient_context=40%, low=21%, moderate=21%, high=12%, very_high=4%

## Critical real-world gaps (vs synthetic)

1. **Ingredient text missing:** 31/42 (73%) have NO ingredient text. Signal extraction severely degraded.
2. **Hebrew name missing:** 27/42 (64%) have Hebrew product name. Others are in French/English/Dutch.
3. **Sodium missing:** 21/42 (50%). Trans fat: 40/42 (95%).
4. **Crackers gap:** OFF Israeli cracker coverage near-zero. Cannot test cracker ontology on real data.
5. **Retailer provenance:** OFF stores field mostly empty for Israeli products.

## What worked in real data

- Anchor routing on real Hebrew names (לחם, מחמצת) fires correctly
- Confidence calibration patch fires appropriately: INSUFFICIENT for English-only names, CAUTIOUS for incomplete nutrition
- Genuine מחמצת / sourdough products detected alongside industrial yeast products
- Fiber laundering signal detection works on real Hebrew ingredient text when present

## Scraper

`scrape_bread_retail.py` — queries OFF by category, keyword (Hebrew+English), and brand (אנג'ל, ברמן, אוסם, שטראוס, etc.)

`batch_run_bread_retail_001.py` — full BSIP2 pipeline + 12 reports

## Reports (12)

All at `C:\Bari\02_products\bread_retail_001\reports\`:
- `real_bread_retail_001_scrape_inventory.md`
- `real_bread_retail_001_scrape_quality.md`
- `real_bread_retail_001_batch_summary.md`
- `real_bread_retail_001_routing_distribution.md`
- `real_bread_retail_001_score_distribution.md`
- `real_bread_retail_001_missingness_report.md`
- `real_bread_retail_001_fiber_laundering.md`
- `real_bread_retail_001_seed_halo.md`
- `real_bread_retail_001_fermentation_claims.md`
- `real_bread_retail_001_deceptive_patterns.md`
- `real_bread_retail_001_top_coherent_products.md`
- `real_bread_retail_001_real_vs_synthetic_comparison.md`

[[bsip2-calibration-patch-v1]]
[[bsip2_bread_light_sprint]]
