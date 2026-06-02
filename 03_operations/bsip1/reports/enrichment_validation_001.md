# BSIP1 Ingredient Enrichment — Validation Report

**Generated:** 2026-06-01 15:15 UTC
**Enrichment version:** bsip1_enrichment_v1
**Mode:** DRY RUN (files not modified)
**Total products enriched:** 328

## 1. Coverage Summary

| Run | Products | Raw Available | Avg Ingredients | Avg Additives |
|---|---|---|---|---|
| run_001 | 53 | 49/53 (92%) | 12.2 | 4.8 |
| run_cereals_001 | 45 | 45/45 (100%) | 6.3 | 0.4 |
| run_hummus_001 | 69 | 65/69 (94%) | 7.8 | 2.4 |
| run_milk_001 | 8 | 8/8 (100%) | 5.1 | 1.8 |
| run_milk_002 | 20 | 20/20 (100%) | 5.4 | 2.1 |
| run_yogurt_001 | 45 | 45/45 (100%) | 4.0 | 0.7 |
| run_yogurt_003 | 88 | 88/88 (100%) | 10.0 | 2.0 |

**Raw ingredient text available:** 320/328 (97%)
**From BSIP0 scrape:** 44/328 (13%)
**BSIP1 text fallback:** 276/328 (84%)
**Missing (no source):** 8/328 (2%)

## 2. Ordered Ingredient Parsing

**Parse success rate:** 320/328 (97%)
**Average ingredient count:** 8.2
**Max ingredient count:** 30

**Sample parsed ingredient lists:**

- קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמ: [1]פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן) → [2]סוכר לבן → [3]שמנים צמחיים
- קראנצ'י חטיף שיבולת שועל עם דבש חמישייה: [1]פתיתי שיבולת שועל מלאה (60%) (מכיל גלוטן) → [2]סוכר לבן → [3]שמנים צמחיים
- קראנצ'י חטיף שיבולת שועל עם מייפל קנדי ח: [1]פתיתי שיבולת שועל מלאה (60%) (מכיל גלוטן) → [2]סוכר לבן → [3]שמנים צמחיים

## 3. Additive Extraction

**Products with ≥1 additive:** 196/328 (59%)

**Examples:**

- חטיפי דגנים פיטנס קרם ועוגיות שישייה: סודיום ביקרבונט, לציטין סויה, מלטודקסטרין, חומר תפיחה, חומרי הלחה
- פיטנס בר גרנולה שוקולד מריר: סודיום ביקרבונט, לציטין סויה, חומר תפיחה, ביקרבונט, דקסטרין
- חטיפי פיטנס שיבולת שועל דבש 5*38 גרם: סודיום ביקרבונט, לציטין סויה, חומר תפיחה, ביקרבונט, דקסטרין
- חטיף דגנים עם פירות יער: מווסת חומציות, מלטודקסטרין, חומר הלחה, טוקופרול, צבע מאכל
- חטיף דגנים מצופה שוקולד עם עוגיות בטעם קרמל ו: סודיום ביקרבונט, מווסת חומציות, חומרי הלחה, ביקרבונט, מתחלבים

## 4. Flavor Extraction

**Products with flavor markers:** 143/328 (43%)
**Products with flavor descriptor (בטעם):** 4/328 (1%)

**Examples:**

- קראנצ'י חטיף שיבולת שועל ושוקולד מריר חמישיה: חומר טעם וריח, חומר טעם

## 5. Sweetener Extraction

**Products with sweetener markers:** 209/328 (63%)

**Examples:**

- חטיפי דגנים פיטנס קרם ועוגיות שישייה: סירופ סוכר אינברטי, סירופ גלוקוזה, סוכר אינברטי, סירופ גלוקוז, סירופ סוכר
- חטיפי דגנים פיטנס שוקולד מריר שישייה: סירופ סוכר אינברטי, סירופ גלוקוזה, סוכר אינברטי, סירופ גלוקוז, סירופ סוכר
- סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6: סירופ סוכר אינברטי, סירופ גלוקוזה, סוכר אינברטי, סירופ גלוקוז, סירופ סוכר
- חטיפי דגנים פיטנס שוקולד בננה שישייה: סירופ סוכר אינברטי, סוכר אינברטי, סירופ גלוקוז, סירופ סוכר, סורביטול
- נייצר וואלי פרוטאין בוטנים ושבבי שוקולד רביעי: סירופ גלוקוזה, סירופ גלוקוז, סוכר לבן, גלוקוזה, פרוקטוז

## 6. Protein / Isolate Extraction

**Products with protein markers:** 64/328 (19%)
**Products with isolate or concentrate:** 0/328 (0%)

**Examples:**

- דגני בוקר חלבון מקסימום 27 גרם חלבון 300 גרם: חלבון מי גבינה, חלבון קזאין, מי גבינה, קזאין
- נייצר וואלי פרוטאין בוטנים בציפוי קרמל מלוח ר: חלבון סויה, מי גבינה, אבקת חלב
- נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה: אבקת חלב כחוש, מי גבינה, אבקת חלב
- דגני בוקר ספשל K חלבון קלוגס 320 גרם: חלבון מי גבינה, חלבון סויה, מי גבינה
- דגני בוקר פיטנס חלבון נסטלה 320 גרם: חלבון מי גבינה, חלבון חיטה, מי גבינה

## 7. Matrix Degradation Markers

**Products with matrix markers:** 121/328 (36%)

**Examples:**

- חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה: פתיתי שיבולת שועל, פתיתי חיטה, פתיתי תירס, קמח חיטה
- שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי: פתיתי שיבולת שועל, פתיתי תירס, קמח חיטה, קמח אורז
- סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב 6: קמח חיטה מלא, מלטודקסטרין, עמילן חיטה, קמח חיטה
- נייצ'ר וואלי צ'ואי בוטנים קלויים חמישייה: פתיתי שיבולת שועל, מלטודקסטרין, קמח חיטה, קמח אורז
- נייצ'ר וואלי צ'ואי שוקולד מריר בוטנים ושקדים : פתיתי שיבולת שועל, מלטודקסטרין, קמח חיטה, קמח אורז

## 8. Fermentation Markers

**Products with fermentation markers:** 96/328 (29%)
**Products with live cultures:** 92/328 (28%)

**Examples:**

- יוגורט טבעי 1.5% שומן: לקטובציל אסידופילוס, ביפידובקטריום, תרבויות חיות
- יוגורט טבעי 3% שומן: תרבויות חיות, תרבויות
- יוגורט טבעי 5% שומן יוטבתה: תרבויות חיות, תרבויות
- יוגורט עיזים 9% שומן: תרבויות חיות, תרבויות
- יוגורט יווני 0% שומן: תרבויות חיות, תרבויות
- יוגורט יווני 2% שומן: תרבויות חיות, תרבויות

## 9. Roasting / Baking Markers

**Products with roasting/baking markers:** 77/328 (23%)

**Examples:**

- חטיף דגנים שוקולד חלב קרמל מלוח קורני שישייה: קלויים, קלוי
- קורני חטיפי דגנים בוטנים מתוק מלוח: קלויים, קלוי
- שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי: קלוי
- קורני חטיפי דגנים+שוקולד חלב: קלויים, קלוי
- חטיף דגנים עם אגוזים: קלויים, קלוי
- קורני חטיפי דגנים שוקולד בננה: קלוי

## 10. Products with Missing Ingredient Data

- `bsip1_7290018333952` (run_001): חטיף אגוזים וחמוציות רפאלס 5*30 גרם
- `bsip1_7290019545545` (run_001): חטיף פאי פקאן רפאלס 5*30 גרם
- `bsip1_7290118427872` (run_001): חטיפי פיטנס שיבולת שועל חמוציות 5*38 גרם
- `bsip1_8423207208703` (run_001): חטיף דגנים מצופה שוקולד מריר סלים דליס
- `bsip1_1990261` (run_hummus_001): חומוס
- `bsip1_3643714` (run_hummus_001): חומוס
- `bsip1_7296073733317` (run_hummus_001): חומוס
- `bsip1_7296073733348` (run_hummus_001): חומוס ענק

## 11. Enrichment Warnings

- `bsip1_7290018333952`: ingredients_raw: no text available from any source
- `bsip1_7290019545545`: ingredients_raw: no text available from any source
- `bsip1_7290118427872`: ingredients_raw: no text available from any source
- `bsip1_8423207208703`: ingredients_raw: no text available from any source
- `bsip1_1990261`: ingredients_raw: no text available from any source
- `bsip1_3643714`: ingredients_raw: no text available from any source
- `bsip1_7296073733317`: ingredients_raw: no text available from any source
- `bsip1_7296073733348`: ingredients_raw: no text available from any source

## 12. Known Limitations

1. **Nested sub-ingredient parsing:** Nested groups (e.g., `שבבי שוקולד (סוכר, שמן, לציטין)`) are included in full-text extraction but position is attributed to the parent ingredient position.
2. **Homonym terms:** Single-word terms like `קרמל` (caramel) may be a color additive OR a flavor depending on context. The extraction reports the match without resolving ambiguity — BSIP2 must apply context logic.
3. **BSIP0 coverage:** Only Yohananof scrape data is currently indexed. Products from other retailers will use the `bsip1_text_fallback` provenance.
4. **Synthetic BSIP1 records** (cereals_001, yogurt_001): These were generated programmatically, not canonicalized from BSIP0. The `ingredients_text_he` field is the authoritative source; provenance is `bsip1_text_fallback`.
5. **E-number detection:** E-number matching uses exact string match. E-numbers with dashes (E-322 vs E322) both patterns are covered but formatting variants may be missed.
6. **Fiber laundering proxy:** `inulin`, `שורש עולש`, `שורש ציקוריה` are flagged as `prebiotic_fiber` in the additive list. Whether this constitutes fiber laundering requires nutritional context (fiber %/100g) which is available in the nutrition fields.
7. **Percentage extraction:** Only explicitly declared percentages in parentheses are captured. Ranges (e.g., 3-5%) are not parsed.

*Report generated by `enrich_runner.py` — BSIP1 enrichment pipeline*