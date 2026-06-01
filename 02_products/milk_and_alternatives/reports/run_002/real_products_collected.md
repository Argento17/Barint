# Milk & Alternatives — Run 002: Real Products Collected

**Collection date:** 2026-05-17  
**Retailer:** Yohananof (yochananof.co.il)  
**Method:** Live browser scraping via Playwright (01_discover → 02_approve → 03_scrape)  
**Discovery corpus:** 80 unique products found, 52 with confirmed barcodes  
**Priority subset scraped:** 20 products (adversarial coverage selection)  
**Pipeline errors:** 0 / 20  
**Provenance:** All products are real Yohananof listings with confirmed barcodes and scraped HTML

---

## Products by Category

### Dairy Milks (NOVA 1–2)

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 7290000051352 | חלב מלא בטעם של פעם 1ליטר לפחות 3.4%שומן | חלב תנובה | 75.0 | B | 1 | 67 | 3.3g |
| 7290019790259 | חלב טבעי 4% 1 ליטר | מחלבות רמת הגולן | 75.0 | B | 1 | 69 | 3.4g |
| 7290102392094 | חלב עיזים בקרטון 1 ליטר | משק צוריאל | 75.0 | B | 1 | 68 | 3.4g |
| 7290114313865 | חלב נטול לקטוז מועשר בחלבון 2% שומן 1 ליטר | טרה | 73.2 | B | 2 | 64 | 6.5g |
| 7290107932134 | חלב בבקבוק 1% מועשר מהדרין | יטבתה | 58.3 | C | 3 | 43 | 3.4g |

### Engineered Dairy Drinks

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 7290110324773 | משקה חלב גו 27 גרם חלבון 2% בטעם וניל 340 מ"ל | תנובה | 39.5 | E | 4 | 67 | 7.4g |
| 7290114313285 | מולר פרוטאין משקה חלבון בטעם בננה 25גרם חלבון 0%שומן | מולר | 47.7 | D | 4 | — | 7.2g |

### Soy Drinks

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 7290116936116 | משקה סויה ללא סוכרים 1 ליטר | תנובה אלטרנטיב | 66.1 | C | 2 | 32 | 3.3g |
| 7290110324926 | משקה סויה ללא תוספת סוכר | תנובה אלטרנטיב | 56.2 | C | 3 | 32 | 3.3g |
| 7290119385560 | משקה סויה בריסטה אלפרו 500 מ"ל | אלפרו | 46.8 | D | 4 | 46 | 3.3g |
| 5411188300328 | אלפרו שוקו משקה סויה | אלפרו | 36.2 | E | 4 | 61 | 3.1g |

### Oat Drinks

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 7394376620904 | משקה שיבולת שועל ללא סוכר | אוטלי | 50.0 | D | 3 | 44 | 1.0g |
| 7290110325619 | משקה שיבולת שועל | תנובה אלטרנטיב | 46.6 | D | 3 | 55 | 1.3g |
| 7394376619939 | משקה בריסטה שיבולת שועל | אוטלי | 48.8 | D | 3 | 61 | 1.1g |
| 7394376621451 | משקה בריסטה שיבולת שועל להקצפה | אוטלי | 48.8 | D | 3 | 61 | 1.1g |
| 5411188124689 | אלפרו שיבולת שועל ללא סוכר | אלפרו | 51.4 | D | 3 | 40 | 0g |

### Almond Drinks

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 7290014760141 | משקה שקדים | תנובה אלטרנטיב | 50.8 | D | 3 | 56 | 1.6g |
| 5411188112709 | אלפרו שקדים ללא סוכר | אלפרו | 38.1 | E | 4 | 15 | 0.5g |

### Rice & Coconut Drinks

| Barcode | Product Name (He) | Brand | Score | Grade | NOVA | kcal/100ml | Prot/100ml |
|---------|-------------------|-------|-------|-------|------|-----------|-----------|
| 8000215204219 | משקה אורז אורגני | ויטאריז | 48.5 | D | 2 | 55 | 0.3g |
| 8000215204554 | משקה אורז קוקוס אורגני | ויטאריז | 47.2 | D | 3 | 65 | 0.4g |

---

## Grade Distribution

```
Grade B (70–84):   4 products   Whole milks + lactose-free enriched
Grade C (55–69):   3 products   Enriched dairy 1%, unsweetened soy ×2
Grade D (40–54):  10 products   Oat drinks, almond drinks, rice drinks
Grade E (<40):     3 products   Alpro almond (SE), Go Milk, Alpro soy chocolate
```

---

## Discovery Statistics

- **Queries run:** 17
- **Total candidates discovered:** 80
- **Candidates with confirmed barcode:** 74
- **Auto-approved (YES):** 56
- **Manual review approved:** 2 (Oatly barista variants)
- **Rejected:** 22
- **Without barcode (skipped):** 6
- **Priority subset scraped:** 20 (adversarial selection for BSIP2 stress coverage)
- **Full corpus available for future scraping:** 52 products (see `all_approved_candidates_full.json`)

---

## Carrefour Status

No scraping infrastructure exists for Carrefour Israel. The `03_operations/bsip0/scrape/` directory contains only `yohananof/` and `yohananof_milk/` subdirectories. Carrefour data collection would require building a new scraper from scratch.

**All 20 products in this corpus are from Yohananof only.**
