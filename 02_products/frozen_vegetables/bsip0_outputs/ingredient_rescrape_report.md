# Ingredient Re-Scrape Report — Frozen Vegetables (Shufersal BSIP0)

**Date:** 2026-06-10
**Source artifacts:** Raw HTML product pages in `03_operations/bsip0/scrape/shufersal_frozen_vegetables/product_pages/`
**Method:** BeautifulSoup extraction from existing raw HTML (no new HTTP requests)

## Why This Was Needed

The original v2/v3 scraper captured `ingredients_raw: "רכיבים"` (the Hebrew heading for "Ingredients") instead of the actual ingredient text. The audit found **0/50** scope-clean products had real ingredient data — only the heading label was captured. This was a block for BSIP1 readiness.

## Root Cause

The original scraper used `find_next(["div", "span", "p"])` from the heading element, which in some cases returned the heading again or short fragments. The regex fallback had an invalid capture pattern that only grabbed the heading word. The actual ingredient text lives in `<div class="componentsText">`, which the original scraper didn't target.

## Method

For each raw HTML artifact:

1. Find `<div class="componentsText">` — this holds the actual ingredient list
2. Validate: text is not empty, not just the heading "רכיבים", length > 2 chars
3. If `componentsText` not found, fall back to `<div class="info">` after the "רכיבים" heading
4. Mark `ingredients_present: true/false` and `ingredient_text_quality: scraped/missing`
5. Extract allergen sections from subsequent `<li>` siblings using `alergiesProperties` and `alergiesTracesProperties` classes

## Results

| Metric | Before (v1) | After (v2) |
|---|---|---|
| Products in scope | 50 | 53 |
| Nutrition coverage | 50/50 (100%) | 53/53 (100%) |
| Real ingredient coverage | **0/50 (0%)** | **53/53 (100%)** |
| Allergen "מכיל" (contains) | not captured | 8 |
| Allergen "עלול להכיל" (may contain) | not captured | 10 |
| Barcode coverage | 50/50 | 53/53 |
| Image URL coverage | 50/50 | 53/53 |

## Data Quality Notes

- Single-ingredient frozen vegetables (e.g., peas, broccoli, spinach) have short ingredient text — just the vegetable name in Hebrew. This is correct: the only ingredient IS the vegetable.
- 3 products have very short ingredient text (`במיה`, `תרד` ×2) — these are single-ingredient whole vegetables. Verified correct, not a parser issue.
- 12 products carry composite ingredients with percentages and sub-ingredients (mixes like לקט נורמנדי, לקט לקוסקוס).
- Some ingredient texts contain embedded `\n` newlines (from HTML formatting). Preserved as-is.

## Scope Changes vs v1

- **Added (3):** חומוס מוקפא (frozen chickpeas), ירקות ופסטה א-לה איטליה, לקט להקפצה פסטה פוזילי
  - All 3 are in A160501 (frozen veg category), have nutrition + real ingredient data
  - Pasta mixes are >75% vegetables; considered in-scope frozen vegetable products
- **Excluded (4):** קטניות מן הטבע ×4 (ambient dried legumes, no frozen indicator, no nutrition, no ingredients)

## Verification

- 0 false positives (no product has "רכיבים" as ingredient text)
- 0 false negatives (all 53 products have real ingredient text)
- All 53 have valid nutrition panels
- All 53 have valid barcodes from JSON-LD
- All 53 have raw HTML artifacts for traceability

## Recommendation

The ingredient re-scrape fixes the BSIP1 blocking issue. Proceed to QA verification for final BSIP1 readiness clearance.
