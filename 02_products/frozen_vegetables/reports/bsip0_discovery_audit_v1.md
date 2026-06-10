# BSIP0 Discovery Audit — Frozen Vegetables

**Date:** 2026-06-10  
**Auditors:** research-agent + data-agent  
**Artifact reviewed:** `discovery_candidates_frozen_vegetables_v1.json`

---

## Classification: **B — BSIP0 discovery candidate set only**

This is **not** a true BSIP0 scrape output. It is a manually compiled candidate list from web research.

---

## Scrape Status

| Dimension | Status |
|-----------|--------|
| scrape_status | **manual_discovery_only** |
| Raw HTML snapshots | 0 |
| Retailer API JSON | 0 |
| Screenshots | 0 |
| Scrape logs | 0 |
| Raw product page captures | 0 |
| Actual scrape artifacts | **0 files** |

---

## Files Found (2)

| File | Size | Type |
|------|------|------|
| `bsip0_outputs/discovery_candidates_frozen_vegetables_v1.json` | 26 KB | Manual discovery candidate set |
| `reports/bsip0_discovery_report.md` | 6 KB | Discovery report |

No `bsip0_outputs/` scrape artifacts exist. No `bsip0_scrape/` directory exists.

---

## Products with Real Source Evidence (28/33)

Products marked `[SOURCE]` in evidence_notes reference specific retailer pages (shufersal.co.il, wolt.com) or cross-referenced barcodes. These have **verbal** retailer confirmation — no captured HTML or API response.

| Evidence class | Count | Meaning |
|----------------|-------|---------|
| SOURCE (retailer site named) | 28 | Product name, brand, size, and price observed on retailer site via manual browse |
| CROSS-REF (third-party site) | 3 | Product name/size confirmed via shoretzki.com (Harduf organic, Willy Food) — retailer presence inferred |
| WEB RESEARCH (article) | 2 | Yohananof products — store visit or article reference, no direct site confirmation |

---

## Products Missing Source Evidence (0/33)

All 33 products have some evidence note. However:

**Field-by-field completeness:**
| Field | Complete | Rate |
|-------|----------|------|
| source_retailer | 33/33 | 100% |
| product_name_he | 33/33 | 100% |
| brand | 33/33 | 100% |
| package_size | 33/33 | 100% |
| category_path | 33/33 | 100% |
| raw_price | 31/33 | 94% |
| barcode | 15/33 | **45%** |
| product_url | 1/33 | **3%** |
| image_url | 0/33 | **0%** |
| evidence_notes | 33/33 | 100% |
| exclusion_risk | 33/33 | 100% |

---

## Known Issues

1. **Product count mismatch:** JSON header says 32, actual products array has 33. (Likely added a product after header was written.) Fixed in `discovery_candidates_v1`.
2. **No scrape infrastructure:** No `bsip0_scrape/` directory, no Playwright scripts, no API scrapers. The candidates can be scraped from Shufersal's online storefront, but no code exists.
3. **Barcodes incomplete:** Only Sunfrost barcodes confirmed (via rabbanimarket.co.il). Shufersal private label, Harduf, Willy Food, Dorot, and Yohananof barcodes all missing.
4. **Image URLs all missing:** Zero product images captured. Shufersal online store serves images — would need actual scrape to capture them.
5. **Product URLs nearly all missing:** Only 1/33 has a URL. Shufersal online store uses unique product URLs — scrape would capture these.

---

## Recommendation: **Hold — do not proceed to BSIP1**

**Rationale:**
- This is a discovery candidate set, not a scrape output
- BSIP1 requires actual nutrition panels and ingredient lists, which require real retailer page captures
- Proceeding to BSIP1 with this data would create fabricated records

**Path to BSIP1 readiness:**
1. Run Playwright/API scrape against Shufersal frozen vegetables category
2. Capture: product URLs, image URLs, barcodes, nutrition panels, ingredient lists
3. Store raw artifacts (HTML, API JSON) in `bsip0_scrape/` directory structure
4. Rebuild the JSON as a true `bsip0_outputs/bsip0_{retailer}_raw.json` with scraped_at timestamps
5. Run the BSIP0 QA validator before proceeding to BSIP1

**Estimated effort:** 1-2 days for Playwright scrape + validation.
