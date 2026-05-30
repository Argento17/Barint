# BSIP1 Batch Test 001 — Report

**Run date:** 2026-05-17 05:22 UTC  
**BSIP0 root:** `C:\Bari\03_operations\bsip0\scrape`  
**Retailers:** carrefour, yohananof

---

## Summary

| Metric | Count |
|--------|-------|
| Total observations | 66 |
| Barcode groups | 53 |
| → Multi-retailer groups | 10 |
| → Single-retailer groups | 43 |
| No-barcode observations | 3 |
| Products written | 53 |
| Schema valid | 53 |
| Schema invalid | 0 |

---

## Barcode Quality Distribution

| Status | Count |
|--------|-------|
| `inferred_from_text` | 39 |
| `confirmed_gs1` | 10 |
| `retailer_internal_id` | 4 |

---

## Nutrition Consistency Distribution

| Status | Count |
|--------|-------|
| `consistent` | 43 |
| `no_data` | 5 |
| `warnings` | 4 |
| `suspicious` | 1 |

---

## Ingredient Quality Distribution

| Quality | Count |
|---------|-------|
| `clean` | 39 |
| `malformed` | 5 |
| `corrupted` | 5 |
| `missing` | 4 |

---

## Conflict Category Totals (across all products)

| Category | Total Conflict Records |
|----------|------------------------|
| Identity (name, brand, barcode, size) | 19 |
| Nutrition (per-100g values) | 35 |
| Ingredient | 0 |
| Labeling (kosher, country, allergens) | 0 |
| Completeness (serving, image, etc.) | 0 |
| **Total** | **54** |

---

## No-Barcode Candidates

3 observation(s) queued in `reports/fuzzy_candidate_queue.json`.

- **carrefour_israel** — `חטיף דגנים עם חתיכות אגוזי לוז קלויים` (brand: Carrefour, size: 8 גרם)
- **carrefour_israel** — `חטיף דגנים עם שבבי שוקולד מריר אורגני` (brand: Carrefour, size: 23 גרם)
- **carrefour_israel** — `חטיף דגנים עם שוקולד חלב וקוקוס` (brand: Carrefour, size: 8 גרם)

---

## Products with Nutrition Warnings

| Product | Status | Warnings |
|---------|--------|----------|
| `bsip1_7290011498948` | `suspicious` | 1 warning(s) |
| `bsip1_7290107646154` | `warnings` | 5 warning(s) |
| `bsip1_7290118427896` | `warnings` | 5 warning(s) |
| `bsip1_8423207206488` | `warnings` | 5 warning(s) |
| `bsip1_8423207209885` | `warnings` | 5 warning(s) |

---

## Products with Ingredient Quality Issues

| Product | Quality | Warnings |
|---------|---------|----------|
| `bsip1_4011800000349` | `malformed` | 'Unmatched closing parenthesis in ingredient text.' |
| `bsip1_4011800628512` | `malformed` | 'Unmatched opening parenthesis(es) in ingredient text (1 unclosed).' |
| `bsip1_4011800630515` | `malformed` | 'Unmatched opening parenthesis(es) in ingredient text (1 unclosed).' |
| `bsip1_7290014525290` | `corrupted` | "Encoding artifact: 1 '???' sequence(s) in ingredient text. Source likely contained non-UTF-8 characters that were replaced." |
| `bsip1_7290014525306` | `corrupted` | "Encoding artifact: 1 '???' sequence(s) in ingredient text. Source likely contained non-UTF-8 characters that were replaced." |
| `bsip1_8410076610386` | `malformed` | 'Unmatched closing parenthesis in ingredient text.' |
| `bsip1_8410076610492` | `malformed` | 'Unmatched closing parenthesis in ingredient text.' |
| `bsip1_8423207206488` | `corrupted` | "Encoding artifact: 1 '???' sequence(s) in ingredient text. Source likely contained non-UTF-8 characters that were replaced." |
| `bsip1_8423207208260` | `corrupted` | "Encoding artifact: 1 '???' sequence(s) in ingredient text. Source likely contained non-UTF-8 characters that were replaced." |
| `bsip1_8423207208680` | `corrupted` | "Encoding artifact: 1 '???' sequence(s) in ingredient text. Source likely contained non-UTF-8 characters that were replaced." |