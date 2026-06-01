# Hummus Insights v1

**Task:** TASK-062  
**Owner:** Content Agent  
**Date:** 2026-05-31  
**Source data:** `hummus_frontend_v1.json` (run_hummus_002) + BSIP1 canonical records  
**Coverage:** 69 products total — 63 in ranked display, 6 excluded (NOVA-1, not prepared spreads)  
**Status:** PRODUCTION — All Nutrition Agent corrections applied (TASK-064 R-2, R-3, R-4)

---

## Usage

Each row provides the `insightLine` field value for that `pid` in `hummus_frontend_v1.json`.  
Data Agent integrates these verbatim into the frontend dataset.  
All lines are in Hebrew. Lines verified under 80 characters.  
Each PID appears exactly once.

**Integration note:** The 6 products in Batch 1 are excluded from the ranked display page (TASK-069). Their insight lines are recorded here for completeness but should not be surfaced in the comparison UI.

---

## Insight Lines by Product ID

### Batch 1 — Whole / Raw / Frozen Chickpeas ⛔ EXCLUDED FROM RANKED DISPLAY

Single-ingredient or minimally processed whole chickpeas. Classified as `hummus_spread` by scraper but are not prepared hummus spreads. Excluded from /hashvaot/hummus ranked display per TASK-069. Insight lines retained for record; do not integrate into display layer.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7296073733324 | חומוס | 85.5 | A | 100% גרגרי חומוס — רכיב יחיד |
| bsip1_7296073733331 | חומוס ענק | 85.5 | A | גרגרי חומוס ענק — ללא תוספות |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 85.4 | A | גרגרי חומוס לבן גדולים — ללא תוספים |
| bsip1_7296073006015 | חומוס גדול שופרסל | 85.4 | A | גרגרי חומוס גדולים — ללא תוספים |
| bsip1_3643820 | חומוס ענק | 85.0 | A | גרגרי חומוס ענק — רכיב יחיד |
| bsip1_7296073705505 | חומוס מוקפא | 85.0 | A | גרגרי חומוס קפואים — רכיב יחיד |

---

### Batch 2 — Canned Whole Chickpeas, Branded (A–B grade)

Yichin and Kaiser branded canned whole chickpeas. Ingredient text scraped as marketing copy, not ingredient list. Preservative status not confirmed from scraped data.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7290018359686 | הקיסר חומוס ענק | 80 | A | גרגרי חומוס ענק בשימור — מידע רכיבים מלא לא אומת |
| bsip1_208428 | חומוס שלם יכין | 80 | B | גרגרי חומוס שלמים בשימור — מידע רכיבים מלא לא אומת |

---

### Batch 3 — Hummus, Ingredient Data Missing

Scored from nutrition data alone; no ingredient text captured in corpus.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_1990261 | חומוס | 73 | B | חומוס — פירוט רכיבים לא זמין |
| bsip1_3643714 | חומוס | 73 | B | חומוס — פירוט רכיבים לא זמין |

---

### Batch 4 — Insufficient Data (unscored)

Products with no nutrition panel data available. Shown on page without score.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7296073733317 | חומוס | — | — | מידע תזונתי לא מספיק לניתוח |
| bsip1_7296073733348 | חומוס ענק | — | — | מידע תזונתי לא מספיק לניתוח |

---

### Batch 5 — Restaurant-Style Hummus, High Tahini (A–B grade)

Short ingredient lists. Notable chickpea-to-tahini ratios declared on pack. One or two functional additives.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_6666307 | סלט חומוס | 80 | A | גרגירי חומוס, טחינה ותבלינים — רשימת רכיבים קצרה עם חומר משמר אחד |
| bsip1_7296073725404 | חומוס מסעדות | 76 | B | 34% חומוס, 31% טחינה גולמית — חומר משמר ותוספים נוספים |
| bsip1_7290106573642 | חומוס צנובר צבר | 67 | B | 67% חומוס, 15% טחינה ו-1.8% צנובר — חומר משמר אחד |
| bsip1_467320 | מלך החומוס אבו מרוואן | 65 | B | 51% חומוס, 26% טחינה גולמית — יחס טחינה גבוה |

---

### Batch 6 — Standard Plain Hummus, B grade (3 additives)

Classic hummus: chickpeas + raw tahini + acidity regulator + preservative + additional additive. Most dominant segment in category.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7296073725565 | חומוס אסלי | 71 | B | חומוס אסלי עם טחינה גולמית — חומר משמר ותוספים נוספים |
| bsip1_7296073725589 | חומוס | 71 | B | חומוס עם טחינה גולמית — חומר משמר ותוספים נוספים |
| bsip1_7296073725381 | חומוס אבו גוש | 70 | B | 53% חומוס, 11% טחינה ושמן זית — מכיל עמילן ומשמר |
| bsip1_7290110579319 | חומוס גלילי | 69 | B | חומוס גלילי עם טחינה גולמית ותבלינים — עם חומר משמר |
| bsip1_7290110557478 | חומוס גלילי | 69 | B | חומוס גלילי עם טחינה גולמית — עם חומר משמר ומווסת חומציות |
| bsip1_7296073725374 | סלט חומוס עם טחינה | 68 | B | סלט חומוס עם תוספת טחינה — עם חומר משמר |
| bsip1_3727667 | חומוס מסעדה | 68 | B | 69% חומוס, 15% טחינה גולמית ושום — עם חומר משמר |
| bsip1_5174551 | חומוס יום יום | 68 | B | 61% חומוס, 15.5% טחינה גולמית — עם חומר משמר |
| bsip1_7290105964564 | חומוס | 68 | B | חומוס עם טחינה גולמית — עם חומר משמר ומווסת חומציות |
| bsip1_7290106576513 | חומוס מסעדה | 68 | B | חומוס מסעדה עם טחינה גולמית ושום — עם חומר משמר |
| bsip1_7290119387434 | חומוס ישראלי | 68 | B | חומוס ישראלי קלאסי עם טחינה — עם חומר משמר |
| bsip1_2987963 | חומוס | 68 | B | 61% חומוס, 15.5% טחינה גולמית ושום — עם חומר משמר |
| bsip1_8645935 | חומוס | 68 | B | חומוס עם טחינה גולמית — עם חומר משמר ומווסת חומציות |

---

### Batch 7 — Flavored Hummus (B grade, multiple additives)

Hummus with declared additions: zaatar, pine nuts, spicy, high-tahini enrichment, or matbucha. Slightly longer ingredient lists.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7290110564360 | חומוס עשיר ב40% טחינה | 68 | B | חומוס עם 40% טחינה מוצהרת על האריזה — עם חומר משמר |
| bsip1_7290104061424 | חומוס עם זעתר | 65 | B | 60% חומוס, 15% טחינה ושמן זית — בתוספת זעתר ועם חומר משמר |
| bsip1_7290104061431 | חומוס עם צנובר אחלה | 65 | B | חומוס עם טחינה גולמית ותוספת צנובר — עם חומר משמר |
| bsip1_7290106576537 | חומוס מסעדה צבר | 65 | B | חומוס מסעדה מקו צבר — עם טחינה גולמית ומשמר |
| bsip1_7290119373710 | חומוס מועשר 40% עם חריף | 65 | B | חומוס עם תוספת טחינה מועשרת (40% לפי האריזה) וחריף — עם מייצב ומשמר |
| bsip1_7290119374892 | חומוס עם מלא מטבוחה חריף | 65 | B | חומוס עם תוספת מטבוחה חריפה — עם חומר משמר |
| bsip1_7290122780314 | חומוס אבו מרוואן26%טחינה | 65 | B | חומוס עם 26% טחינה גולמית מוצהרת — עם חומר משמר |
| bsip1_7290106573598 | חומוס לבנוני צבר | 65 | B | 69% חומוס, 15% טחינה ושמן זית — בתוספת שום, פטרוזיליה ומשמר |

---

### Batch 8 — Hummus Spreads, C grade

Lower-scoring hummus spreads with more complex additive profiles or multi-component structures.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7290115202434 | חומוס עם זעתר | 65 | C | חומוס עם תבלינים וזעתר — עם חומר משמר |
| bsip1_467153 | מלך החומוס סמיר הגדול | 64 | C | 90% בסיס חומוס עם תוספת טחינה גולמית — חומוס 48% מהמוצר |
| bsip1_7290106573819 | חומוס אבו גוש+צנובר+חריף | 64 | C | חומוס עם גרגרים שלמים, צנובר ופלפלים — מוצר מרובה רכיבים |
| bsip1_7290104061417 | חומוס עם טחינה אחלה | 64 | C | 56% חומוס, 17% טחינה — עם מייצבים ומשמר |
| bsip1_7290106573628 | חומוס עם טחינה צבר | 63 | C | 62% חומוס, 17% טחינה — עם מייצבים ותוספת 10% סלט טחינה |
| bsip1_7290104061448 | חומוס עם חריף אחלה | 63 | C | 57% חומוס, 14% טחינה ופלפל חריף יבש — עם מייצב ומשמר |
| bsip1_7290112968685 | חומוס גרגרים בתטבילה | 63 | C | גרגרי חומוס שלמים בתטבילה — עם חומר משמר ומווסת חומציות |
| bsip1_7290115202687 | חומוס עם חריף | 63 | C | חומוס עם חריף — עם מייצב, חומר משמר ומווסת חומציות |
| bsip1_7290119374885 | חומוס עם חציל פיקנטי | 58 | C | חומוס עם חציל חריף — עם חומר משמר |

---

### Batch 9 — Masabacha (B–C grade)

Whole-chickpea preparations in sauce or dip base.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7296073725367 | סלט חומוס+מסבחה | 68 | B | שילוב חומוס ומסבחה עם גרגרים שלמים — עם חומר משמר |
| bsip1_7296073725398 | חומוס מסבחה | 64 | C | חומוס מסבחה עם גרגרים שלמים — עם חומר משמר |

---

### Batch 10 — Matbucha (C–D grade)

Cooked tomato-and-pepper spreads. Most contain added sugar. Differences in tomato content, pepper ratio, and spice level.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7290107958639 | מטבוחה חריפה אש | 62 | C | מטבוחה חריפה עם עגבניות ופלפל — עם חומר משמר |
| bsip1_7290010931330 | סלט מטבוחה | 62 | C | 63% עגבניות מרוסקות ו-13% פלפל — מכיל סוכר לבן |
| bsip1_8644112 | סלט מטבוחה יום יום | 62 | C | מטבוחה יומיומית עם עגבניות ופלפל — עם חומר משמר |
| bsip1_7290011800642 | סלט מטבוחה מרוקאית | 62 | C | 75% רכיבי עגבניות, פלפל אדום — מכיל סוכר |
| bsip1_6666444 | סלט מטבוחה | 60 | C | ירקות, שמן ותבלינים — עם חומר משמר |
| bsip1_7290106520905 | סלט טורקי | 60 | C | סלט ירקות בסגנון טורקי עם תבלינים ומשמר |
| bsip1_7296073725633 | מטבוחה פיקנטית | 52 | C | מטבוחה פיקנטית עם עגבניות ופלפלים — עם חומר משמר |
| bsip1_7296073725510 | סלט מטבוחה פיקנטי | 52 | C | מטבוחה פיקנטית עם עגבניות ופלפלים — עם חומר משמר |
| bsip1_7290111563492 | מטבוחה חריפה | 50 | D | מטבוחה חריפה — ציון מבוסס על נתונים חלקיים |
| bsip1_7290106577572 | מטבוחה אמיתית | 49 | D | מטבוחה עם תוספות שונות — ציון מבוסס על נתונים חלקיים |

---

### Batch 11 — Eggplant Spreads (C grade)

Cooked or chargrilled eggplant preparations. Additive count varies by complexity.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7296073725497 | סלט חצילים על האש | 62 | C | סלט חצילים על האש עם שמן ותבלינים — עם חומר משמר |
| bsip1_7296073725640 | מעדן חצילים | 58 | C | מעדן חצילים עם שמן ותבלינים — עם חומר משמר |
| bsip1_7290115207484 | חציל על האש | 58 | C | חציל על האש עם שמן ותבלינים — עם חומר משמר |
| bsip1_7290105366023 | סלט חציל בטעם כבד | 56 | C | סלט חציל עם טעם כבד — עם מספר תוספים |
| bsip1_3989096 | סלט חציל פיקנטי | 54 | C | סלט חציל חריף עם תבלינים — עם חומר משמר |
| bsip1_7290106577480 | חציל על האש בטחינה | 50 | C | 44% חציל על האש, 14% טחינה — עם מייצבים, עמילן מעובד ומשמר |

---

### Batch 12 — Pepper Spreads (C–D grade)

Oil-based or vegetable-based pepper preparations. Generally longer ingredient lists than hummus. Some contain added sugar or date syrup.

| PID | Name | Score | Grade | Insight Line |
|-----|------|-------|-------|--------------|
| bsip1_7290104721533 | סלט פלפלים קלויים | 64 | C | פלפלים קלויים עם תבלינים — עם חומר משמר |
| bsip1_7290015858175 | ממרח פלפלים קלויים | 60 | C | 70% פלפל קלוי ושום — עם מייצב ומשמר |
| bsip1_7290010154265 | פלפל צ'ומה | 51 | C | ממרח חריף מבוסס שמן עם 30% פלפל ו-20% שום — מכיל סוכר לבן |
| bsip1_7296073451969 | ממרח פלפלים קלויים | 48 | D | 67% פלפל קלוי עם סירופ סילאן ותוספת סוכר — רשימת רכיבים ארוכה |
| bsip1_6724786 | ממרח פלפלים קלויים | 43 | D | 54% פלפל אדום, עגבניות מיובשות וסילאן — 13 רכיבים כולל מייצב |

---

## Total Count Verification

| Batch | Description | Products | In display |
|-------|-------------|----------|-----------|
| 1 | Whole/raw/frozen chickpeas, NOVA-1 | 6 | ⛔ Excluded |
| 2 | Canned branded chickpeas, A–B | 2 | ✓ |
| 3 | Missing ingredient data | 2 | ✓ |
| 4 | Insufficient data (unscored) | 2 | ✓ |
| 5 | Restaurant/high-tahini, A–B | 4 | ✓ |
| 6 | Standard plain hummus, B | 13 | ✓ |
| 7 | Flavored hummus, B | 8 | ✓ |
| 8 | Hummus spreads, C | 9 | ✓ |
| 9 | Masabacha, B–C | 2 | ✓ |
| 10 | Matbucha, C–D | 10 | ✓ |
| 11 | Eggplant spreads, C | 6 | ✓ |
| 12 | Pepper spreads, C–D | 5 | ✓ |
| **Total** | | **69** | **63** |

---

## Corrections Applied (TASK-064 Review)

| Correction | Products affected | Change |
|-----------|------------------|--------|
| R-2 | bsip1_7290018359686, bsip1_208428 | "ללא חומר משמר" → "מידע רכיבים מלא לא אומת" |
| R-3 | bsip1_7296073725404, bsip1_7296073725565, bsip1_7296073725589 | "חומר משמר אחד" → "חומר משמר ותוספים נוספים" (additive_count=3 for all three) |
| R-4 | bsip1_7290119373710 | "40% טחינה" → "40% לפי האריזה" qualifier added |
| TASK-069 | Batch 1 (6 products) | Marked excluded from ranked display |

Corrections R-2 and R-4 were RECOMMENDED (non-blocking) in TASK-064. R-3 was flagged as a precision issue. All applied in this production version.

Additionally: bsip1_7290111563492 and bsip1_7290106577572 (D-grade matbucha) — insight lines updated to reflect the KL-4 caveat ("ציון מבוסס על נתונים חלקיים") rather than "רשימת רכיבים ארוכה," aligning with the approved caveated_product_messages from TASK-067.
