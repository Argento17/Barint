# לחם — Corpus Report v1

**Generated:** 2026-05-28 16:52 UTC
**Source:** BSIP2 bread_retail_003 (Shufersal) + finalized insight lines v1

---

## Coverage

| Metric | Count |
|--------|-------|
| Coherent BSIP2 files (FULL/CAUTIOUS) | 81 |
| Matched insight line | 81 |
| Skipped (no insight line) | 0 |
| Missing image URL | 0 |

---

## Grade Distribution

| Grade | Count |
|-------|-------|
| A | 2 |
| B | 60 |
| C | 18 |
| D | 1 |
| E | 0 |

Average score: **68.3**

---

## Product Subtypes

| Subtype | Count |
|---------|-------|
| לחם | 70 |
| קרקר | 9 |
| בגט | 2 |

---

## Fermentation Signal

| Signal | Count |
|--------|-------|
| עם מחמצת (fermentation detected) | 37 |
| ללא מחמצת מזוהה | 44 |

---

## Missing Image URLs

_All products have image URLs_

---

## Skipped Products (no insight line)

These products are coherent BSIP2 files but have no assigned insight line.
This indicates a gap in the corpus — barcodes not in lechem_insight_lines_v1.md.

_none_

---

## Image URL Note

Image URLs are Shufersal Cloudinary CDN (`res.cloudinary.com/shufersal`).
**Action required before production:**
1. Add `res.cloudinary.com` to `next.config.ts` `images.remotePatterns`
2. Verify URLs are publicly accessible without referrer restriction

---

## Filter Dimensions

The following fields are available for UI filtering:

- `grade` → ציון (A/B/C/D)
- `fermentationDetected` → תסיסה (עם מחמצת / ללא מחמצת מזוהה)
- `breadSubtype` → סוג (לחם / קרקר / בגט / פיתה / לחמניה)
- `score` → מספרי (slider)

---

## Ready for Frontend?

**Verdict: CONDITIONAL PASS**

- Editorial corpus complete (barcode-keyed insight lines for all 81 products)
- Scores and grades from BSIP2 flat files
- Fermentation signal derived from BSIP0 ingredients_raw
- Image URLs present (Cloudinary accessibility unverified)
- Recommend: verify 5 Shufersal image URLs in browser before deploying
