# Bread Corpus Representation Audit — 001

**Corpus:** `real_bread_retail_002_v2` — 110 products, Shufersal, scraped 2026-05-25
**Auditor:** Automated analysis against known Israeli retail bread market segments
**Verdict:** Significant wellness-skew bias confirmed. Mainstream Israeli bread is absent.

---

## 1. Executive Finding

The corpus **does not represent the Israeli bread shelf**. It represents a curated slice of the Shufersal shelf heavily weighted toward spelt, rye, sourdough-labeled, and "fitness" products.

The most commonly purchased bread products in Israel — standard white sliced loaves, plain white pita, plain challah, baguettes — are **entirely absent** from the 110-product corpus.

This is not a scraping failure. It is an acquisition design failure: the search queries used to seed the corpus were themselves wellness-biased, and the Shufersal search engine likely further amplified this by ranking promoted/premium products first.

---

## 2. Corpus Composition by Archetype

| Archetype | Count | % | Notes |
|:----------|:------|:--|:------|
| Cracker | 26 | 24% | Dominated by spelt/rye/fitness variants |
| Pita | 23 | 21% | Almost exclusively spelt/whole grain; no plain white pita |
| Sourdough-labeled (מחמצת) | 22 | 20% | Name carries sourdough claim, many with industrial yeast |
| Rolls (לחמניות) | 19 | 17% | Mostly spelt/whole grain; some challah rolls |
| Rye bread | 11 | 10% | Rye is a specialty product in Israeli retail |
| Spelt bread (non-pita) | 6 | 5% | |
| Whole grain generic | 1 | 1% | |
| Specialty diet (keto, GF) | 1 | 1% | |
| Standard white bread | **0** | **0%** | **The #1 Israeli bread segment is absent** |
| Toast loaf | **0** | **0%** | **Entirely missing** |
| Baguette | **0** | **0%** | **Entirely missing** |
| Laffah / lavash flatbread | **0** | **0%** | **Entirely missing** |
| Standard challah (loaf) | **0** | **0%** | Only challah-roll packages found |

---

## 3. Wellness Keyword Saturation

Of 110 products, the proportion carrying wellness/specialty signals:

| Signal | Count | % of corpus |
|:-------|:------|:------------|
| כוסמין (spelt) in product name | 29 | **26%** |
| מחמצת (sourdough label) in product name | 24 | **22%** |
| שיפון (rye) in product name | 17 | **15%** |
| מלא (whole grain marker) in product name | 12 | **11%** |
| פיטנס (fitness) in product name | 5 | 5% |
| **Total with at least one wellness signal** | **~70** | **~64%** |
| לבן (white) in product name | 1 | 1% |
| חיטה generic (plain wheat) in product name | 1 | 1% |
| טוסט (toast loaf) in product name | **0** | **0%** |
| אחיד (standard commercial loaf) in product name | **0** | **0%** |

**64% of the corpus carries explicit wellness/specialty signals.** In actual Israeli retail, mainstream white bread and plain pita account for the majority of bread volume by units sold.

---

## 4. Acquisition Bias Root Cause Analysis

### 4.1 — Search Queries (primary cause)

```
Queries used: ["לחם", "קרקר", "כוסמין", "שיפון", "פיתה", "לחמניה"]
```

Three of six queries are specialty terms:

| Query | Term type | Effect |
|:------|:----------|:-------|
| `לחם` | Generic | Should retrieve mainstream — but Shufersal search ranks premium/promoted first |
| `קרקר` | Category | Returns all crackers — reasonable |
| `כוסמין` | **Wellness term** | Exclusively retrieves spelt products |
| `שיפון` | **Wellness term** | Exclusively retrieves rye products |
| `פיתה` | Generic | Should retrieve all pita — but spelt pita is heavily promoted |
| `לחמניה` | Category | Roll format only |

**Missing queries that would have retrieved mainstream products:**

| Missing query | What it would retrieve |
|:-------------|:----------------------|
| `טוסט` | Standard sliced white/whole wheat toast loaves (Berman, Wonder, Osem private label) |
| `לחם אחיד` | The single most common Israeli bread format |
| `לחם לבן` | Standard white loaves |
| `בגט` | Baguettes (bakery and packaged) |
| `חלה` | Challah loaves (not just rolls) |
| `לחם שחור` | Dark bread / standard pumpernickel |
| `לפה` | Laffah flatbread (Iraqi tradition, widely sold) |
| `לחם תירס` | Corn bread |

### 4.2 — Shufersal Search Ranking (amplifying cause)

The Shufersal search engine for the query "לחם" (bread) likely returns:
1. Promoted/sponsored products first
2. Organic/health category products (Shufersal promotes its premium range)
3. New/seasonal products
4. Standard commodity bread lower in results (page 2+)

The scraper used `pageSize=48` and took only the **first page of results** for each query. Commodity white bread — sold in volume but not promoted — likely appears on page 2+ for the generic "לחם" query.

### 4.3 — Category Navigation NOT Used

The scraper used search, not category browsing. Shufersal category codes identified in the corpus:

| Category code | Frequency | Likely meaning |
|:-------------|:----------|:--------------|
| A10 | 81 | General food / bread section |
| A44 | 48 | Organic / health products |
| A4402 | 47 | Organic sub-category |
| A1015 | 44 | Bread sub-category |

Category A44/A4402 (organic/health) appears in **48 of 110 products (44%)** — suggesting that the search results over-indexed on the organic shelf rather than the main bread aisle.

Browsing the standard bread category (A1015 / A1005) directly, without a wellness keyword filter, would retrieve commodity products that search misses.

### 4.4 — Exclusion Logic NOT the Cause

The exclusion filter removed only 2 products:
- `מארז שבלול עם צימוקים` (sweet pastry) — correct
- `קמח שיפון מלא` (raw flour ingredient) — correct

No mainstream bread was excluded. The exclusion rules are sound. The missing products were simply never acquired.

---

## 5. Missing Retail Segments

### Segment A — Standard Sliced White Bread (HIGH volume, FULLY absent)

The Israeli bread market's dominant category by volume. Every Israeli supermarket stocks multiple SKUs:

| Expected product | Brand | Status |
|:----------------|:------|:-------|
| לחם אחיד לבן (standard white loaf) | Wonder, Berman, Osem, private label | **ABSENT** |
| לחם טוסט לבן פרוס (sliced white toast) | Berman, Wonder | **ABSENT** |
| לחם חיטה פרוס (sliced wheat) | Berman, Wonder, private label | **ABSENT** |
| לחם קל / לייט (light bread) | Various | **ABSENT** |

### Segment B — Standard Pita (HIGH volume, ABSENT)

The corpus has 23 pita products, but almost every one is spelt or whole grain. The plain white pita — used for falafel and hummus across Israel — is invisible:

| Expected product | Status |
|:----------------|:-------|
| פיתות חיטה לבנה (plain white flour pita) | **ABSENT** |
| פיתות קמח לבן (plain white pita, standard pack) | **ABSENT** |
| פיתה רגילה (plain pita, no qualifier) | **ABSENT** |

The one product named "פיתה פיתה" has no ingredient text and was routed to `default` — it may be a generic white pita, but without data it cannot be confirmed.

### Segment C — Challah Loaf (PARTIALLY absent)

The corpus has 3 challah roll packages (לחמניות חלה). These are rolls, not the standard challah loaf sold for Shabbat:

| Expected product | Status |
|:----------------|:-------|
| חלה שבת (standard Shabbat challah loaf) | **ABSENT** |
| חלה פרוסה (pre-sliced challah) | **ABSENT** |
| חלה מתוקה (sweet challah loaf) | **ABSENT** |

### Segment D — Baguette and Bakery-Fresh (FULLY absent)

| Expected product | Status |
|:----------------|:-------|
| בגט לבן (white baguette) | **ABSENT** |
| בגט מחיטה מלאה (whole wheat baguette) | **ABSENT** |
| לחם מחמצת בגט (sourdough baguette) | **ABSENT** |

*Note: Shufersal may not stock baguettes in its online catalog. This requires verification.*

### Segment E — Flatbread / Laffah (FULLY absent)

| Expected product | Status |
|:----------------|:-------|
| לפה (laffah, Iraqi flatbread) | **ABSENT** |
| פיתה עירקית (Iraqi pita) | **ABSENT** |
| לחם ערבי (Arabic flatbread) | **ABSENT** |

### Segment F — Standard Commercial Loaf (FULLY absent)

The "לחם אחיד" format — a rectangular sliced loaf sold in every Israeli supermarket — is completely absent. This is the baseline bread against which all others should be compared.

---

## 6. Ingredient Reality vs. Name Impression

The wellness framing is partly illusory even within the corpus. Among 83 products with ingredient text:

| Flour base in actual ingredients | Count | % of products with data |
|:---------------------------------|:------|:------------------------|
| קמח חיטה לבן / white wheat flour | 50 | **60%** |
| קמח כוסמין מלא / whole spelt | 21 | 25% |
| קמח שיפון מלא / whole rye | 21 | 25% |
| קמח חיטה מלא / whole wheat | 20 | 24% |

**60% of products with ingredient data use white wheat flour as the base** — even within this ostensibly "wellness" corpus. Many products with spelt or rye in their name use white flour as the primary base with specialty flour as a secondary ingredient.

This means the corpus overstates wellness quality even at the ingredient level.

---

## 7. Missing Brand Coverage

Israeli bread market key players by volume:

| Brand | Corpus presence | Notes |
|:------|:----------------|:------|
| ברמן (Berman) | **0 products** | Market leader in sliced bread |
| וונדר (Wonder) | **0 products** | Major white bread brand |
| מלאכים (Angels) | **0 products** | Major brand |
| אסם (Osem) | 3 products | Crackers only (קרקר אסם, לחמית אסם) |
| E-FREE | 2 products | Specialty GF-adjacent brand |

Berman and Wonder produce the most-purchased breads in Israel. Neither appears in the corpus.

---

## 8. Overall Bias Assessment

| Dimension | Assessment |
|:----------|:-----------|
| **Volume representation** | Heavily skewed toward low-volume premium/specialty SKUs |
| **Price tier** | Premium tier only; commodity tier absent |
| **Shopper represented** | Health-conscious premium buyer; not average Israeli bread shopper |
| **Brand coverage** | Specialty brands only; mass-market leaders absent |
| **Flour type** | Spelt/rye over-indexed; white wheat under-indexed (despite being 60% of actual ingredients) |
| **Format coverage** | Missing toast loaf, baguette, standard challah, plain pita, laffah |
| **Cause** | Search query design (wellness-biased terms); Shufersal search ranking (promotes premium); category browsing not used |
| **Exclusion logic** | NOT the cause — exclusion rules are correct |

**The corpus is suitable for analyzing the premium/wellness segment of the Shufersal bread shelf. It is NOT suitable for claims about "the Israeli bread market" or for comparing products against a mainstream baseline.**

---

## 9. Proposed Corrections — real_bread_retail_003

### 9.1 — Additional Search Queries

Add to `SEARCH_QUERIES` in `shufersal_probe.py`:

```python
SEARCH_QUERIES_MAINSTREAM = [
    "טוסט",          # sliced toast bread
    "לחם אחיד",      # standard loaf
    "לחם לבן",       # white bread
    "חלה",           # challah (loaf format)
    "לחם שחור",      # dark bread
    "לחם בריאות",    # health bread (commercial category name)
    "לפה",           # laffah flatbread
    "בגט",           # baguette (verify availability)
]
```

**Strategy:** Run mainstream queries first, deduplicate, then run wellness queries. Cap wellness queries at 40% of total product budget.

### 9.2 — Category-Browsing Supplement

Browse Shufersal bread categories directly, independent of search:

```
Target categories (to verify exact codes):
- Bread aisle: /online/he/categories/A1005  (or equivalent)
- Sliced bread: /online/he/categories/A1015
- Pita and flatbread: /online/he/categories/A101503

Method: paginate through category listing pages, collect all product codes,
then fetch product pages — same HTML parse logic as existing probe.
```

This bypasses search-ranking bias and retrieves all products Shufersal lists in a category, promoted or not.

### 9.3 — Composition Targets for real_bread_retail_003

| Segment | Target % | Notes |
|:--------|:---------|:------|
| Standard white/light sliced loaf | 15–20% | Berman, Wonder, private label |
| Standard whole wheat sliced | 10–15% | |
| Rye / spelt specialty | 15–20% | Down from current 36% |
| Sourdough-label breads | 15–20% | Down from current 20% |
| Plain white pita | 10–15% | Currently near-zero |
| Whole grain pita | 5–10% | Reduce from current over-indexing |
| Crackers | 15–20% | Keep |
| Challah (loaf format) | 5–10% | Currently only rolls |
| Rolls | 5–10% | Down from current 17% |
| Flatbread / laffah | 3–5% | Currently 0% |

**Minimum corpus size:** 150 products (current 110 insufficient for segment-level analysis).

### 9.4 — Explicit Retrieval Targets (must-have SKUs)

The following products should be explicitly verified on Shufersal and retrieved if present:

1. **לחם אחיד לבן** — standard white loaf (any brand)
2. **לחם טוסט** — sliced toast bread
3. **לחם פרנץ' (French bread)** — common Berman/Wonder format
4. **פיתות חיטה לבן** — plain white flour pita (not spelt)
5. **חלה שבת** — standard Shabbat challah loaf
6. **לפה** — laffah if available on Shufersal
7. **לחם קל** — light bread (lower calorie format)

### 9.5 — Acquisition Anti-Patterns to Avoid

| Anti-pattern | Fix |
|:-------------|:----|
| Only first page of search results | Paginate to page 2 for mainstream queries |
| 3/6 queries are wellness keywords | Max 2/8 queries should be specialty-only terms |
| No category browsing | Add category page traversal as supplemental source |
| No brand verification | Explicitly search for "ברמן", "וונדר" |
| No composition check during acquisition | Add mid-run archetype classifier to flag wellness over-indexing |

### 9.6 — Gate Additions for real_bread_retail_003

Add composition gates before declaring success:

```python
GATE_MIN_PRODUCTS = 150
GATE_MIN_MAINSTREAM_PCT = 0.20   # at least 20% non-wellness products
GATE_MAX_SPELT_PCT = 0.20        # spelt no more than 20% of corpus
GATE_MAX_SOURDOUGH_LABEL_PCT = 0.20  # מחמצת label no more than 20%
GATE_MIN_PLAIN_PITA = 2          # at least 2 plain white pita products
GATE_MIN_SLICED_LOAF = 3         # at least 3 standard sliced loaf products
```

---

## 10. Impact on Current Corpus Use

### What the current corpus CAN support:

- Analysis of the Shufersal premium/wellness bread shelf
- Comparison of spelt vs. rye crackers
- Fermentation quality analysis within the sourdough segment
- Fiber laundering detection in the wellness segment
- Consumer guidance for health-conscious buyers browsing the specialty shelf

### What it CANNOT support:

- Any claim about "Israeli market" breadth
- Comparison of premium products against a mainstream baseline
- Consumer guidance for buyers of standard bread (the majority)
- Price-tier analysis
- Brand competition analysis
- Category-level nutritional benchmarks for mainstream bread

### Required framing addition (all public-facing content):

> הניתוח מכסה את המדף הפרמיום/בריאות של שופרסל. לחמים מסחריים סטנדרטיים (טוסט לבן, פיתה רגילה, חלה רגילה) אינם מיוצגים בקורפוס זה. ממצאים אינם מייצגים את השוק הישראלי הכולל.

---

## Appendix — Full Product Name List (alphabetical)

All 110 products in corpus, for reference:

```
10 פיתות כוסמין (×2)
10 פיתות מחמצת
12 פיתות ביס
טורטיה כוסמין
כוסמין מלא 100% (×2)
לחם E-FREE מקמח חיטה
לחם E-FREE מקמח כוסמין
לחם אקסקלוסיבי שיפון מלא
לחם הארץ שיפון אגוזים
לחם כוסמין
לחם מחמצת אגוזים (×2)
לחם מחמצת אגוזים פרוס
לחם מחמצת אגוזים צימוקים
לחם מחמצת אגוזים+צימוקים
לחם מחמצת דגנים (×2)
לחם מחמצת דגנים פרוס
לחם מחמצת זיתי קלמטה
לחם מחמצת כוסמין
לחם מחמצת כוסמין פרוס
לחם מחמצת מכוסמין
לחם מחמצת עגבניות
לחם מחמצת עגבניות פרוס
לחם מחמצת צרפתי (×2)
לחם מחמצת צרפתי פרוס
לחם מחמצת שיפון (×3)
לחם מחמצת שיפון פרוס
לחם מחמצת שיפון+אגוזים
לחם קמח מלא 100%
לחם שיפון 100%פרוס
לחם שיפון גרעינים
לחם שיפון כהה
לחם שיפון כפרי
לחם שיפון מלא פרוס
לחם שיפון עגול
לחם שיפון קל
לחמית שיפון אסם
לחמניות אצבע ג'וניור
לחמניות המבורגר
לחמניות כוסמין במתיקות
לחמניות לס קיטו
לחמניות מחמצת טבעית
לחמניות פשתן טרי
לחמניות קלות כוסמין
לחמניות קלות קמח מלא
מארז לחמניות אצבע
מארז לחמניות ביס
מארז לחמניות דגנים
מארז לחמניות המבורגר
מארז לחמניות חלה (×2)
מארז לחמניות חלה מתוקה
מארז לחמניות חלה קלות
מארז לחמניות כוסמין
מארז לחמניות כפריות
מארז לחמניות קלות
מארז לחמניות קשר
מארז פיתות אסליות (×3)
מארז פיתות ביס
מארז פיתות בסגנון תימני
מארז פיתות כוסמין (×2)
מארז פיתות קמח מלא
מארז שבלול עם צימוקים [EXCLUDED]
מיני פיתות כוסמין מלא
מקלות כוסמין
פיתה פיתה
פיתות 100% כוסמין מלא
פיתות אסליות
פיתות אסליות מארז
פיתות ביס 100% כוסמין
פיתות במרקם מיוחד
פיתות ג'וניור כוסמין לבן
פיתות כוסמין מלא
פיתות כוסמין קלות
פיתות קלות כוסמין
קמח שיפון מלא [EXCLUDED]
קרם קרקר
קרקר
קרקר דגנים ללת"ס
קרקר דק כפרי
קרקר דק כפרי פיטנס
קרקר דק פיטנס בטטה
קרקר דק פיטנס זיתים
קרקר דק פיטנס סלק
קרקר דק רוזמרין
קרקר דק רוזמרין פיטנס
קרקר זהב אסם
קרקר חומוס מתובל
קרקר טופז מלח הדר
קרקר טופז שומשום
קרקר כוסמין אורגני
קרקר כוסמין דק כפרי
קרקר כוסמין דק רוזמרין
קרקר כוסמין טבעי
קרקר כוסמין מלא ושומשום
קרקר כוסמין סלק
קרקר מרובע מלוח
קרקר פריך בסגנון שוודי
קרקר פריך ירקות אורגני
קרקר פריך עם קמח שיפון
קרקר קרם קרקר
קרקר שומשום אסם
```

*Generated 2026-05-25 | Auditor: BSIP0 corpus analysis*
