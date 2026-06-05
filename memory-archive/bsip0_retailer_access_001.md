---
name: bsip0-retailer-access-001
description: BSIP0 Israeli retailer access audit — v1 all blocked; v2 (with VPN) Shufersal accessible, gate PASSED 110 products
metadata: 
  node_type: memory
  type: project
  originSessionId: f6d27b4e-04d2-40ff-8b87-daa80ab5c329
---

Real Israeli retailer scrape audit run 2026-05-25.

**Why:** User required a real retailer bread/cracker corpus with 20+ products, minimum acceptance gate with nutrition/ingredient coverage. Previous real_bread_retail_001 used OFF as primary source — not acceptable.

**How to apply:** VPN (Israeli IP) is required for retailer access. Without VPN, all sites block. Shufersal is the primary working source. Do not use OFF as primary corpus.

## Gate Result (v2 — with VPN)

**PASSED** — 110 products, gate criteria all met. Ready for BSIP1/BSIP2.

- Run ID: `real_bread_retail_002_v2_20260525T165557`
- Products: 110 from Shufersal
- Nutrition coverage: 83/110 (75%)
- Ingredient coverage: 83/110 (75%)

## Retailer Status (as of 2026-05-25, WITH VPN)

| Retailer | Status | Method | Evidence |
|:---------|:-------|:-------|:---------|
| Shufersal | **ACCESSIBLE** | Static HTTP + HTML parse | 110 products, full nutrition + ingredients from product pages |
| Victory | Blocked | Browser (Playwright) | Angular SPA — no product cards rendered in browser |
| Carrefour Israel | Partial | Browser (Playwright) | VPN unlocked it; login wall prevents catalog browse |
| Wolt Market | Partial | Browser (Playwright) | Login wall — auth token required for product catalog |
| Rami Levy | Not tested in v2 | — | HTTP 403 in v1; untested with VPN |
| Tiv Taam | Not tested in v2 | — | HTTP 403 in v1; on Wolt as tiv-taam-ibn-gabirol |

## Shufersal Extraction Method (working)

- Search: `https://www.shufersal.co.il/online/he/search?q=<query>&pageSize=48`
- Products in `<li data-product-name="..." data-product-code="P_XXXXX" data-food="true">`
- Product page: `https://www.shufersal.co.il/online/he/p/<lowercase_code>` → redirects
- Nutrition: `<div class="nutritionList"><div class="nutritionItem">` — value/unit/label triplets
- Ingredients: text after "רכיבים" in product tab section
- JSON-LD: `@type=Product` with `sku`, `gtin13`, `image[]`
- Requires VPN (Israeli IP) — without VPN: maintenance placeholder or 403

## Gate Thresholds (v2)

- GATE_MIN_PRODUCTS = 20
- GATE_NUTRITION_PCT = 0.70
- GATE_INGREDIENT_PCT = 0.40
- GATE_MIN_RETAILERS = 1

## Files (v2)

- Source files: `C:\Bari\03_operations\bsip0\acquisition_v2\`
- Probe: `shufersal_probe.py` (HTML parse), `victory_probe.py`, `carrefour_probe.py`, `wolt_probe.py`
- Orchestrator: `acquisition_audit_v2.py`
- Raw products: `C:\Bari\02_products\bread_retail_002\real_bread_retail_002_v2_20260525T165557_bsip0_raw.json`
- Manifest: `C:\Bari\02_products\bread_retail_002\bsip0_source_manifest_v2.json`
- Audit: `C:\Bari\02_products\bread_retail_002\bsip0_acquisition_v2_audit.md`

## What Would Unlock Other Retailers

1. Carrefour: Login session cookies (VPN already unlocked geo-block)
2. Wolt Market: Wolt auth token or session cookies
3. Victory: Need to inspect what JS framework is actually in use (ng-version not detected)
4. Rami Levy/Tiv Taam: Retry with VPN

[[bsip2-real-bread-retail-001]]
