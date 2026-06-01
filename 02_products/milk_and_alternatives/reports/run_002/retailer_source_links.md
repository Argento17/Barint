# Retailer Source Links — Run 002

**Retailer:** Yohananof (yochananof.co.il)  
**Scrape date:** 2026-05-17  
**Local raw HTML:** `03_operations/bsip0/scrape/yohananof_milk/outputs/yohananof_milk/<barcode>/`

---

## Product Source Reference Table

| Barcode | Product Name | Search Query Used | Local HTML Path | Capture Status |
|---------|-------------|-------------------|-----------------|----------------|
| 7290000051352 | חלב מלא בטעם של פעם 1ליטר | חלב 1% | yohananof_milk/7290000051352/ | all: success |
| 7290019790259 | חלב טבעי 4% 1 ליטר | חלב 1% | yohananof_milk/7290019790259/ | all: success |
| 7290102392094 | חלב עיזים בקרטון 1 ליטר | חלב 3% | yohananof_milk/7290102392094/ | all: success |
| 7290107932134 | חלב בבקבוק 1% מועשר מהדרין | חלב 1% | yohananof_milk/7290107932134/ | all: success |
| 7290114313865 | חלב נטול לקטוז מועשר בחלבון | חלב עשיר בחלבון | yohananof_milk/7290114313865/ | all: success |
| 7290110324926 | משקה סויה ללא תוספת סוכר | משקה סויה | yohananof_milk/7290110324926/ | all: success |
| 7290116936116 | משקה סויה ללא סוכרים 1 ליטר | משקה סויה | yohananof_milk/7290116936116/ | all: success |
| 7290119385560 | משקה סויה בריסטה אלפרו 500 מ"ל | משקה סויה | yohananof_milk/7290119385560/ | all: success |
| 5411188300328 | אלפרו שוקו משקה סויה | Alpro | yohananof_milk/5411188300328/ | all: success |
| 7290110325619 | משקה שיבולת שועל | משקה שיבולת שועל | yohananof_milk/7290110325619/ | all: success |
| 7394376620904 | משקה שיבולת שועל ללא סוכר | משקה שיבולת שועל | yohananof_milk/7394376620904/ | all: success |
| 7394376619939 | משקה בריסטה שיבולת שועל | חלב חצי שמן | yohananof_milk/7394376619939/ | all: success |
| 7394376621451 | משקה בריסטה שיבולת שועל להקצפה | משקה שיבולת שועל | yohananof_milk/7394376621451/ | all: success |
| 5411188124689 | אלפרו שיבולת שועל ללא סוכר | משקה אורז | yohananof_milk/5411188124689/ | all: success |
| 7290014760141 | משקה שקדים | משקה שקדים | yohananof_milk/7290014760141/ | all: success |
| 5411188112709 | אלפרו שקדים ללא סוכר | Alpro | yohananof_milk/5411188112709/ | all: success |
| 7290110324773 | משקה חלב גו 27גרם חלבון 340 מ"ל | משקה קוקוס | yohananof_milk/7290110324773/ | all: success |
| 7290114313285 | מולר פרוטאין בטעם בננה 25גרם | חלב דל שומן | yohananof_milk/7290114313285/ | all: success |
| 8000215204219 | משקה אורז אורגני | משקה אורז | yohananof_milk/8000215204219/ | all: success |
| 8000215204554 | משקה אורז קוקוס אורגני | משקה אורז | yohananof_milk/8000215204554/ | all: success |

---

## Search Query → Results Summary

| Query | Candidates Found | Unique in Corpus |
|-------|-----------------|-----------------|
| חלב 3% | 12 | 7290102392094 |
| חלב 1% | 9 | 7290000051352, 7290019790259, 7290107932134 |
| חלב דל שומן | 5 | 7290114313285 |
| חלב חצי שמן | 1 | 7394376619939 (found via cross-query) |
| חלב עשיר בחלבון | 4 | 7290114313865 |
| משקה סויה | 11 | 7290110324926, 7290116936116, 7290119385560 |
| משקה שיבולת שועל | 9 | 7290110325619, 7394376620904, 7394376621451, 5411188124689 |
| משקה שקדים | 8 | 7290014760141 |
| משקה קוקוס | 14 | 7290110324773 (cross-found) |
| משקה אורז | 9 | 8000215204219, 8000215204554, 5411188124689 |
| Alpro | 4 | 5411188112709, 5411188300328, 7290119385560 |
| Oatly | 11 | 7394376619939, 7394376621451 (via manual approval) |
| משקה צמחי חלב | 10 | No new unique barcodes |
| Others | — | Duplicates only |

---

## Carrefour

**Status: No infrastructure. No data.**  
Search URL that would need investigation: carrefour.co.il  
No source links available.

---

## Raw Evidence Preservation

Each product folder contains:
- `discovery.json` — original discovery metadata (name, query, card_text, image_url)
- `discovery.txt` — human-readable summary
- `ingredients.html` — scraped ingredients tab (raw HTML)
- `nutrition.html` — scraped nutrition tab (raw HTML)
- `allergens.html` — scraped allergen tab (raw HTML)
- `capture_status.json` — status of each tab capture
- `product_image.jpg` — product image downloaded from Yohananof CDN

All raw HTML is preserved verbatim. The BSIP0 parser reads from these files; original HTML is never modified.
