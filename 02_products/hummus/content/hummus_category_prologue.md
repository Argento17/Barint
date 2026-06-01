# Hummus Category Prologue

**Task:** TASK-062  
**Owner:** Content Agent  
**Date:** 2026-05-31  
**Status:** PRODUCTION  
**Aligned with:** hummus_content_v3.json, hummus-comparison-page-data.ts

---

## Mobile / Shelf View — Prologue Sentences

Four sentences displayed beneath the page title in the mobile shelf view and desktop prologue section. Rendered in order. Each is a standalone factual sentence.

```
בדקנו 69 מוצרי חומוס וממרחים הנמכרים בשופרסל — לפי הרכב המוצר, רשימת הרכיבים, סימוני האריזה ומבנה המוצר.
```

```
הקטגוריה כוללת ממרחי חומוס, מטבוחה, ממרח חצילים, ממרח פלפלים ומסבחה.
```

```
61 מוצרים מקבלים ציון; שני מוצרים אינם מוצגים עם ציון בשל היעדר נתוני תזונה.
```

```
ערכי השומן אינם מוצגים בקטגוריה זו בשל מגבלות באיכות מקור הנתונים.
```

---

## Desktop Hero — Description Line

Single sentence rendered as the hero description paragraph in the desktop comparison view. Uses `prologueSentences[0]`.

```
בדקנו 69 מוצרי חומוס וממרחים הנמכרים בשופרסל — לפי הרכב המוצר, רשימת הרכיבים, סימוני האריזה ומבנה המוצר.
```

---

## Desktop Hero — Category Insight Lines

Four rotating insight lines shown in the desktop hero. Category-level observations, not per-product. Based on the 63-product displayed corpus.

```
63 מוצרים בדירוג — ממרחי חומוס, מטבוחה, חצילים, פלפלים ומסבחה
```

```
2 מוצרים בציון A: הרכב חזק עם תוספים מוגבלים
```

```
פער ציון של 37 נקודות בין הממרח המוביל לתחתית הרשימה
```

```
ערכי שומן אינם מוצגים — מגבלת נתוני מקור, מפורטת בתחתית הדף
```

---

## Extended Category Introduction

For use in the category introduction section if a longer text block is rendered. Aligned with `category_introduction.body` in hummus_content_v3.json.

> בארי ניתחה 69 מוצרי חומוס וממרחים הנמכרים בשופרסל, שנאספו בחודש מאי 2026.
>
> הקטגוריה כוללת ממרחי חומוס, מטבוחה, ממרח חצילים, ממרח פלפלים ומסבחה.
>
> כל מוצר הוערך לפי מתודולוגיית בארי, הבוחנת את הרכב המוצר, רמת העיבוד, נטל התוספים, ואיכות הערכים התזונתיים.
>
> הציון אינו מבוסס על מרכיב בודד או על ערך תזונתי מסוים, אלא משקף הערכה כוללת של מבנה המוצר ביחס לשאר הממרחים בקטגוריה.
>
> 61 מוצרים מוצגים עם ציון; שני מוצרים אינם מוצגים עם ציון בשל היעדר נתוני תזונה מלאים.

---

## Why Hummus Products Differ — Background Context

For editorial / SEO use if a contextual paragraph is needed. Consumer-facing, no health claims.

חומוס הוא אחד המוצרים הנפוצים ביותר במקרר הישראלי — אך מאחורי השם המוכר מסתתרים מוצרים שונים מאוד זה מזה. הרכב המרכיבים, אחוז החומוס והטחינה, סוג השמן, ורשימת התוספים — כולם משתנים משמעותית בין מוצר למוצר, גם כשהאריזה נראית דומה.

ההשוואה של בארי בוחנת כל מוצר לפי מה שרשום על האריזה: רשימת המרכיבים, ערכי התזונה, ורמת העיבוד. כל ממרח מוערך ביחס לשאר הממרחים בקטגוריה — לא ביחס לכלל המזון.

---

## Writing Constraints Applied

- No health claims ("בריא", "מזין", "מומלץ לצרכן")
- No dietary recommendations ("כדאי לאכול", "עדיף להימנע")
- No superlatives based on score ("הטוב ביותר", "הגרוע ביותר")
- No framework vocabulary (BSIP, NOVA, binding cap, structural class)
- All counts consistent with hummus_content_v3.json (63 displayed, 61 scored, 2 unavailable)
