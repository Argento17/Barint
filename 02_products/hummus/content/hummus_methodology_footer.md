# Hummus Methodology Footer

**Task:** TASK-062  
**Owner:** Content Agent  
**Date:** 2026-05-31  
**Status:** PRODUCTION  
**Aligned with:** hummus_content_v3.json methodology, hummus-comparison-page-data.ts

---

## Methodology Lines

Four lines displayed in the methodology footer section. Each is a standalone factual sentence. Rendered in order.

**Line 1 — How the score is calculated:**
```
הציון מחושב לפי מדדים מרובים: רמת עיבוד המוצר, נטל תוספי המזון, הרכב הערכים התזונתיים ומדדים נוספים הנוגעים למבנה המוצר.
```

**Line 2 — Score scale and comparison scope:**
```
הציון הסופי הוא ממוצע משוקלל על סולם של 0 עד 100. ההשוואה היא קטגורית בלבד — כל מוצר מוערך ביחס לממרחים ותוספות בלבד.
```

**Line 3 — Mandatory fat disclosure:**
```
ערכי השומן אינם מוצגים בקטגוריה זו בשל מגבלות באיכות מקור הנתונים.
```

**Line 4 — Non-recommendation disclaimer:**
```
הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.
```

---

## Mandatory Disclosure Sentence

The following sentence is required verbatim in the methodology footer per TASK-062 requirements. It appears as Line 3 above.

> **ערכי השומן אינם מוצגים בקטגוריה זו בשל מגבלות באיכות מקור הנתונים.**

This sentence must not be paraphrased, shortened, or omitted. It reflects the known data limitation documented in KL-1 of hummus_content_v3.json: fat_quality dimension suppressed due to Shufersal fat-row scraping defect (TASK-039), affecting 59 of 63 displayed products (94%).

---

## Grade Descriptions

For use in the grade legend or methodology expansion. Sourced from hummus_content_v3.json `grade_descriptions`. Based on the 63-product displayed corpus.

| Grade | Score range | Label | Count in corpus |
|-------|------------|-------|----------------|
| A | 80 ומעלה | מבנה תזונתי חזק | 2 |
| B | 65–79 | פרופיל כללי טוב | 28 |
| C | 50–64 | היבטים לעיון | 27 |
| D | 35–49 | חששות מבניים | 4 |

---

## Score Statistics Note

For display in methodology context if statistical note is shown.

```
הציון הממוצע בקטגוריה זו הוא 63.7 (חציון: 65.0). כחצי מהמוצרים מרוכזים בטווח 60–68.
```

Source: computed from 61 scored products in the 63-product displayed corpus.

---

## Category-Relative Note

```
ציון בקטגוריה זו אינו ניתן להשוואה ישירה עם ציון מקטגוריה אחרת. ממרח שמקבל ציון B בקטגוריה זו אינו בהכרח שווה-ערך לקטגוריה B של מוצר מקטגוריה אחרת.
```

---

## Writing Constraints Applied

- Line 2 does not mention ministry warning labels (corrected per TASK-064 B-3)
- Score interpretation framed as relative-to-category, never absolute
- No health claims in any methodology line
- Fat disclosure wording is verbatim mandatory disclosure — do not alter
