# Hummus Content Count Reconciliation

**Task:** TASK-075  
**Agent:** Content Agent  
**Date:** 2026-05-31  
**Resolves:** QA warning W-1 from TASK-072  
**Input:** hummus_content_v2.json  
**Output:** hummus_content_v3.json

---

## Root Cause of W-1

`hummus_content_v2.json` (TASK-067) was written against the full 69-product corpus. After that file was finalized, TASK-069 excluded 6 NOVA-1 single-ingredient chickpea products from ranked display, reducing the displayed corpus from 69 to 63. All count-bearing fields in v2 still reflected the pre-exclusion state.

The 6 excluded products:

| ID | Name | NOVA | Display score |
|----|------|------|--------------|
| bsip1_7296073733324 | חומוס | 1 | 85.5 |
| bsip1_7296073733331 | חומוס ענק | 1 | 85.5 |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 1 | 85.4 |
| bsip1_7296073006015 | חומוס גדול שופרסל | 1 | 85.4 |
| bsip1_3643820 | חומוס ענק | 1 | 85.0 |
| bsip1_7296073705505 | חומוס מוקפא | 1 | 85.0 |

All 6 had scores and were grade A. Their removal reduced grade A count from 8 to 2 and shifted the mean score downward.

---

## Statistics: Full Corpus vs Displayed Corpus

All statistics computed programmatically from `hummus_frontend_v1.json` (deployed, `src/data/comparisons/`).

| Metric | Full corpus (69) | Displayed corpus (63) | Change |
|--------|-----------------|----------------------|--------|
| Total products | 69 | 63 | −6 |
| Scored products | 67 | 61 | −6 |
| Unavailable products | 2 | 2 | — |
| Grade A | 8 | 2 | −6 |
| Grade B | 28 | 28 | — |
| Grade C | 27 | 27 | — |
| Grade D | 4 | 4 | — |
| Score mean | 65.7 | 63.7 | −2.0 |
| Score median | 65.2 | 65.0 | −0.2 |
| Score min | 43 | 43 | — |
| Score max | 86 | 80 | −6 |
| IQR range (P25–P75) | 61.5–68.9 | 60–68 | shifted |
| ממרח חומוס products | 44 | 38 | −6 |
| מטבוחה products | 11 | 11 | — |
| ממרח חצילים products | 7 | 7 | — |
| ממרח פלפלים products | 5 | 5 | — |
| מסבחה products | 2 | 2 | — |
| fat_quality unreliable count | 58 (full corpus) | 59 (displayed) | see note |
| fat_quality unreliable % | ~84% (full corpus) | 93.7% (displayed) | see note |

**Fat quality note:** The 6 excluded NOVA-1 products had `fat_quality_reliable=True` (single-ingredient products with complete fat data). Their removal from the displayed corpus increases the unreliable percentage from ~84% to 93.7%. This explains both the incorrect `products_affected: 64` in v2 (which exceeded the displayed count of 63, an impossibility) and the incorrect "84%" consumer text.

---

## Changes Applied: v2 → v3

Eight fields corrected. No content structure altered. No approved text rewritten beyond the specific numbers changed.

### C-1 — `category_introduction.body[4]`: scored display count

| Version | Text |
|---------|------|
| v2 | "67 מוצרים מוצגים עם ציון מלא; שני מוצרים אינם מוצגים עם ציון בשל היעדר נתוני תזונה מלאים." |
| v3 | "61 מוצרים מוצגים עם ציון; שני מוצרים אינם מוצגים עם ציון בשל היעדר נתוני תזונה מלאים." |

67 → 61. Also removed "מלא" (full) — the display state is "scored," not "full." The "שני מוצרים" clause is unchanged.

---

### C-2 — `corpus_facts.displayable`: total displayed count

| Version | Value |
|---------|-------|
| v2 | 67 |
| v3 | 63 |

67 → 63. "Displayable" represents products shown on the page (61 scored + 2 unavailable = 63).

---

### C-3 — `corpus_facts.product_type_breakdown["ממרח חומוס"]`: displayed hummus spread count

| Version | Value |
|---------|-------|
| v2 | 44 |
| v3 | 38 |

44 → 38. All 6 excluded NOVA-1 products were `product_type: hummus_spread`. Other type counts unchanged.

---

### C-4 — `grade_descriptions.A.count_in_corpus`: grade A product count

| Version | Value |
|---------|-------|
| v2 | 8 |
| v3 | 2 |

8 → 2. All 6 excluded products were grade A (scores 85–86). The 2 remaining grade-A products are הקיסר חומוס ענק (score 80) and סלט חומוס (score 80).

---

### C-5 — `score_stats_note`: mean, median, IQR range, and qualifier

| Version | Text |
|---------|------|
| v2 | "הציון הממוצע בקטגוריה זו הוא 65.7 (חציון: 65.2). מרבית המוצרים מרוכזים בטווח 61–69." |
| v3 | "הציון הממוצע בקטגוריה זו הוא 63.7 (חציון: 65.0). כחצי מהמוצרים מרוכזים בטווח 60–68." |

- Mean: 65.7 → 63.7 (from full-corpus mean to displayed-corpus mean)
- Median: 65.2 → 65.0 (from full-corpus median to displayed-corpus median)
- IQR range: 61–69 → 60–68 (P25=60, P75=68 from displayed corpus)
- "מרבית" → "כחצי": the IQR range contains approximately 50% of scored products (30 of 61 = 49.2%). "מרבית" (majority, >50%) is incorrect. "כחצי" (approximately half) is accurate. This also applies the TASK-064 R-1 recommended fix, which was deferred in v2.

Computed from 61 scored displayed products:

```
Sorted scores: [43, 48, 49, 50, 50, 51, 52, 52, 54, 56, 58, 58, 58, 60, 60,
                60, 62, 62, 62, 62, 62, 63, 63, 63, 63, 64, 64, 64, 64, 64,
                65, 65, 65, 65, 65, 65, 65, 65, 65, 67, 68, 68, 68, 68, 68,
                68, 68, 68, 68, 68, 69, 69, 70, 71, 71, 73, 73, 76, 80, 80, 80]
Mean: 63.69 → displayed as 63.7
Median (index 30): 65.0
P25 (index 15): 60
P75 (index 45): 68
```

---

### C-6 — `KL-1.products_affected`: fat-quality-unreliable product count

| Version | Value |
|---------|-------|
| v2 | 64 |
| v3 | 59 |

64 → 59. The v2 value (64) exceeded the total displayed corpus (63), which is mathematically impossible. Verified from `fat_quality_reliable` field in source data: 59 of 63 displayed products have `fat_quality_reliable=False`.

---

### C-7 — `KL-1.consumer_text`: fat-quality-unreliable percentage

| Version | Text (excerpt) |
|---------|---------------|
| v2 | "...לא כללו נתוני שומן שלמים עבור **84%** מהמוצרים..." |
| v3 | "...לא כללו נתוני שומן שלמים עבור **94%** מהמוצרים..." |

84% → 94%. The 84% figure was derived from the full corpus (58/69 ≈ 84%). In the displayed corpus: 59/63 = 93.7% → rounded to 94%. The 6 excluded NOVA-1 products all had reliable fat data (single-ingredient products). Their removal increased the unreliable percentage.

---

### C-8 — `faq-01.answer`: comparison product count

| Version | Text |
|---------|------|
| v2 | "הושוו 69 מוצרי ממרח הנמכרים בשופרסל: ממרחי חומוס, מטבוחה, ממרח חצילים, ממרח פלפלים ומסבחה. הנתונים נאספו מהאתר של שופרסל בחודש מאי 2026." |
| v3 | "63 מוצרי ממרח מוצגים בהשוואה זו: ממרחי חומוס, מטבוחה, ממרח חצילים, ממרח פלפלים ומסבחה. 61 מוצרים מוצגים עם ציון; שני מוצרים מוצגים ללא ציון בשל היעדר נתוני תזונה. הנתונים נאספו מהאתר של שופרסל בחודש מאי 2026." |

"הושוו 69" → "63 מוצרי ממרח מוצגים". The FAQ question asks "מה הוערך בהשוואה זו?" (what was assessed in this comparison). The comparison contains 63 products; 69 were analyzed in the pipeline but 6 are not in the comparison display. Updated to reflect what the user actually sees in the comparison.

---

## Fields Verified Unchanged

The following fields were audited and confirmed correct against the displayed corpus. No changes made.

| Field | v2 value | Verified |
|-------|----------|---------|
| `corpus_facts.total_products` | 69 | ✓ 69 total analyzed |
| `corpus_facts.unavailable` | 2 | ✓ 2 unavailable products |
| `corpus_facts.retailer` | שופרסל | ✓ |
| `corpus_facts.scrape_date` | מאי 2026 | ✓ |
| `corpus_facts.product_type_breakdown["מטבוחה"]` | 11 | ✓ |
| `corpus_facts.product_type_breakdown["ממרח חצילים"]` | 7 | ✓ |
| `corpus_facts.product_type_breakdown["ממרח פלפלים"]` | 5 | ✓ |
| `corpus_facts.product_type_breakdown["מסבחה"]` | 2 | ✓ |
| `grade_descriptions.B.count_in_corpus` | 28 | ✓ |
| `grade_descriptions.C.count_in_corpus` | 27 | ✓ |
| `grade_descriptions.D.count_in_corpus` | 4 | ✓ |
| `grade_descriptions.*.score_range` | A:80+, B:65–79, C:50–64, D:35–49 | ✓ |
| `KL-2.products_affected` | 2 | ✓ |
| `KL-3.products_affected` | 2 | ✓ |
| `KL-4.products_affected` | 2 | ✓ |
| `KL-5.products_affected` | 2 | ✓ |
| `faq-08.answer` (scrape date) | 30 במאי 2026 | ✓ matches `bsip0_scrape_date: 2026-05-30` |
| All `caveated_product_messages` | unchanged | ✓ no counts in these fields |
| `mandatory_disclosure` | unchanged | ✓ no counts |
| `methodology.body` | unchanged | ✓ no counts |
| `category_relative_note` | unchanged | ✓ no counts |
| faq-02 through faq-07 | unchanged | ✓ no corpus counts |

---

## Consistency Verification

### dataset ↔ content package (v3)

| Fact | Dataset value | v3 value | Match |
|------|--------------|----------|-------|
| Displayed products | 63 | `corpus_facts.displayable: 63` | ✓ |
| Scored displayed | 61 | `body[4]: "61 מוצרים"` | ✓ |
| Unavailable displayed | 2 | `corpus_facts.unavailable: 2` | ✓ |
| Grade A count | 2 | `grade_descriptions.A.count_in_corpus: 2` | ✓ |
| Grade B count | 28 | `grade_descriptions.B.count_in_corpus: 28` | ✓ |
| Grade C count | 27 | `grade_descriptions.C.count_in_corpus: 27` | ✓ |
| Grade D count | 4 | `grade_descriptions.D.count_in_corpus: 4` | ✓ |
| ממרח חומוס count | 38 | `product_type_breakdown["ממרח חומוס"]: 38` | ✓ |
| Score mean | 63.7 | `score_stats_note: "63.7"` | ✓ |
| Score median | 65.0 | `score_stats_note: "(חציון: 65.0)"` | ✓ |
| IQR range | 60–68 | `score_stats_note: "60–68"` | ✓ |
| Fat unreliable count | 59 | `KL-1.products_affected: 59` | ✓ |
| Fat unreliable % | 93.7% | `KL-1.consumer_text: "94%"` (rounded) | ✓ |
| FAQ product count | 63 | `faq-01.answer: "63 מוצרי ממרח"` | ✓ |

### content package (v3) ↔ website rendering

The live page (`hummus-comparison-page-data.ts`) derives its counts from the deployed JSON, not from `hummus_content_v3.json`. Direct comparison:

| Display element | Live page | v3 value | Match |
|----------------|-----------|----------|-------|
| Metadata line | "63 מוצרים בדירוג" | `corpus_facts.displayable: 63` | ✓ |
| Prologue sentence 3 | "61 מוצרים מקבלים ציון" | `body[4]: "61 מוצרים"` | ✓ |
| Desktop stats "בדף ההשוואה" | 63 | `displayable: 63` | ✓ |
| Grade A products in list | 2 | `grade_descriptions.A.count_in_corpus: 2` | ✓ |
| First ranked product | הקיסר חומוס ענק (80, A) | consistent with A=2 | ✓ |

---

## W-1 Resolution Status

**QA warning W-1 (MEDIUM): `hummus_content_v2.json` counts are stale post-NOVA-1 exclusion**

All stale fields identified in W-1 have been corrected:
- [x] `corpus_facts.displayable`: 67 → 63
- [x] `grade_descriptions.A.count_in_corpus`: 8 → 2

Additional stale fields discovered during full audit and corrected:
- [x] `category_introduction.body[4]`: "67 מוצרים" → "61 מוצרים"
- [x] `corpus_facts.product_type_breakdown["ממרח חומוס"]`: 44 → 38
- [x] `score_stats_note`: mean 65.7→63.7, median 65.2→65.0, range 61-69→60-68
- [x] `KL-1.products_affected`: 64 → 59 (was impossibly > total displayed 63)
- [x] `KL-1.consumer_text`: "84%" → "94%"
- [x] `faq-01.answer`: "69 מוצרי ממרח" → "63 מוצרי ממרח"

**W-1 is resolved in `hummus_content_v3.json`.**

---

*Content Agent — TASK-075 — 2026-05-31*
