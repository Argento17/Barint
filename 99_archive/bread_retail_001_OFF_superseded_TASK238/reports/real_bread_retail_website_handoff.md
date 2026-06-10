# Website Handoff — Real Bread Retail 001

Generated: 2026-05-25 | Run: `real_bread_retail_001`

This document is for Cursor/website team.
All analysis, copy, and caveats are here.
Do not use the raw score_distribution or batch_summary reports for consumer-facing content.

---

## 1. Data Transparency (mandatory framing — include in all consumer content)

**What to say:**

> ניתחנו מוצרי לחם ישראלים מסופרמרקטים ישראליים על בסיס נתונים ממסד הנתונים הפתוח
> Open Food Facts. מסד נתונים זה כולל נתוני תזונה ורשימות מרכיבים שנלקחו ממדבקות
> מוצרים אמיתיים. מידע על 8 מוצרים היה מלא מספיק לניתוח אמין.
> שאר המוצרים חסרו נתוני מרכיבים ולא ייוצגו בדירוג.

**English equivalent:**

> We analyzed Israeli retail bread products using data from Open Food Facts,
> a public database of real product label data. 8 products had sufficient
> data for reliable scoring. The remaining products are listed with a data-availability
> note — they are not confirmed poor products.

**What NOT to say:**
- Do not say 'we analyzed 42 Israeli bread products' as if all 42 are fully scored
- Do not rank products without ingredient data against products with ingredient data
- Do not feature 'bottom products' that are there due to data gaps, not product quality

---

## 2. Key Stats — Safe to Publish

Based on 8 products with verified ingredient data:

- **Average fiber:** 7.3g per 100g
- **Grade distribution:**
  - Grade B: 5 products
  - Grade C: 3 products
- **Fermentation signals detected:** 4/8 products

---

## 3. Product Examples — Safe to Feature

### ✓ Tier 1 — Full Analysis (show score + grade as confirmed)

**לחם הרים שחום ורך** (שירליתה לחם פלא)
- Score: 69 | Grade: B | נתונים מלאים יחסית
- Fiber: 1.7g/100g
- Fermentation: ✓
- Seeds: ✓
- Category: bread
- Source: https://world.openfoodfacts.org/product/7290016877021/

**לחם אנג׳ל 100 קל בתוספת שיפון** (אנגל)
- Score: 68 | Grade: B | נתונים מלאים יחסית
- Fiber: 7.3g/100g
- Fermentation: ✗
- Seeds: ✓
- Category: bread
- Source: https://world.openfoodfacts.org/product/7290013027399/

**לחם אחיד פרוס** (אנג׳ל)
- Score: 63 | Grade: C | נתונים מלאים יחסית
- Fiber: 3.9g/100g
- Fermentation: ✗
- Seeds: ✗
- Category: bread
- Source: https://world.openfoodfacts.org/product/7290000379104/

**Whole wheat bread with grains** (Duet Bakery)
- Score: 62 | Grade: C | נתונים מלאים יחסית
- Fiber: 3.3g/100g
- Fermentation: ✓
- Seeds: ✓
- Category: bread
- Source: https://world.openfoodfacts.org/product/7290011142407/

### ~ Tier 2 — Partial Analysis (show score + provisional grade)

**אנג'ל לחם פרו** (Angel) — score=72 grade=B*
_נתונים חלקיים_ — fiber not recorded

**לחם פומפרניקל** (ברמן) — score=68 grade=B*
_נתונים חלקיים_ — 10.2g fiber | fermentation ✓

**לחם פרו 28** (אגמי) — score=68 grade=B*
_נתונים חלקיים_ — 12.7g fiber | fermentation ✓

**לחם 100% כוסמין מלא** (מאפיית לחמנו) — score=56 grade=C*
_נתונים חלקיים_ — 19.1g fiber

*Asterisk or label indicates provisional grade.*

---

## 4. Comparison Pairs — Recommended

These pairs are interesting for the article because they contrast real verified products.

### Pair 1 — Fiber Extremes (both verified)

- **High fiber:** לחם 100% כוסמין מלא (מאפיית לחמנו) — 19.1g/100g — score=56
- **Low fiber:** אנג'ל לחם פרו (Angel) — 0.0g — score=72

Story angle: same product category (bread), fiber differs 19x.

### Pair 2 — Fermentation vs Industrial

- **Fermented:** לחם הרים שחום ורך (שירליתה לחם פלא) — score=69 grade=B
- **Industrial:** לחם אנג׳ל 100 קל בתוספת שיפון (אנגל) — score=68 grade=B

Story angle: fermentation claim is a real signal, not just marketing — compare ingredient lists.

### Pair 3 — Verified vs Nutrition-Only (for transparency narrative)

- **Verified:** אנג'ל לחם פרו (Angel) — score=72 | has ingredients | grade=B
- **Nutrition-only:** לחם שיפון גרעינים (אנג׳ל) — internal score=82 | no ingredients | grade NOT shown

Story angle: transparency in data matters — same analysis, but only one product can
earn a confirmed grade because its ingredients are publicly available.

---

## 5. Confidence Language for UI

Use these exact labels in the product UI. Do not invent alternatives.

| Label (He) | Label (En) | When to use |
|:-----------|:-----------|:------------|
| נתונים מלאים יחסית | Relatively complete data | FULL degradation + ingredient text present |
| נתונים חלקיים | Partial data | CAUTIOUS degradation + ingredient text |
| חסרים נתונים מהותיים | Missing essential data | Nutrition only, no ingredients; or UNCERTAINTY |
| לא מספיק לניתוח ודאי | Insufficient for certain analysis | INSUFFICIENT degradation |

**Score display rules:**
- Score visible: FULL or CAUTIOUS + has ingredient text → show
- Grade confirmed: FULL + has ingredient text → show without asterisk
- Grade provisional: CAUTIOUS + has ingredient text → show with asterisk or 'provisional' label
- No score: everything else → show confidence label only

---

## 6. Recommended Blog Narrative

### Title options
- מה באמת יש בלחם שלכם? ניתחנו מוצרי לחם ישראלים
- הלחם הטוב ביותר שמצאנו — ומה שהיינו רוצים לדעת
- שקיפות בלחם: מה הציון שלנו אומר ומה הוא לא יכול לומר

### Opening (honest framing)

> ניתחנו מוצרי לחם ישראלים שנמכרים בסופרמרקטים. לא כל המוצרים קיבלו ציון —
> חלק לא כללו מספיק נתונים לניתוח אמין. הציונים שמוצגים כאן מבוססים על
> 8 מוצרים שכללו גם רשימת מרכיבים וגם נתוני תזונה מלאים.

### Recommended structure

1. **הממצאים המאומתים** — 8 מוצרים עם נתוני מרכיבים מלאים
2. **מה שגילינו** — ציפוי סיבים, תסיסה אמיתית לעומת מלאכותית, זרעים על גבי בסיס מזוקק
3. **מה שלא יכולנו לבדוק** — מוצרים ללא רשימת מרכיבים
4. **כיצד קוראים את הציון** — מה המשמעות של כוכבית

### Safe claims (backed by verified data)

- לחם מחמצת אמיתי (עם מרכיב 'מחמצת' ברשימה) נמצא ב-4 מוצרים מתוך 8 מאומתים
- ממוצע סיבים תזונתיים במוצרים מאומתים: 7.3 גרם ל-100 גרם
- 3 מוצרים מאומתים עם סיבים ≥8g/100g — לחם סיבים גבוה בפועל

### Claims that require caveat

- 'הלחם עם הציון הגבוה ביותר' → specify it's from the verified set only
- Any fiber laundering claim → only from verified products with ingredient text
- Comparison to synthetic corpus → note synthetic was designed for stress testing, not market rep.

---

## 7. Visual Recommendations

- **Score dial / grade badge:** show only for verified (8) products
- **Confidence tag:** small pill label under product name for all products
- **Fiber bar chart:** show for products with fiber data (31 products)
- **Ingredient text indicator:** icon showing whether ingredient list was available
- **Data availability panel:** always visible — 'מבוסס על 8 מוצרים מאומתים מתוך 42'
- **Grade with asterisk:** use ✱ or 'משוקלל חלקית' for CAUTIOUS-tier grades
- **No bottom-5 list** unless filtered to verified products only

---

## 8. Dataset Files for Cursor

- `real_bread_retail_001_website_dataset.json` — full product dataset with all fields
- `real_bread_retail_001_website_dataset.csv` — same, CSV format

Key fields to use in UI:
- `consumer_score` — null if not displayable
- `consumer_grade` — null if not displayable
- `consumer_grade_provisional` — true if grade is provisional
- `confidence_label_he` — always set, use in UI
- `tier` — verified / nutrition_only / uncertain / data_gap
- `has_ingredient_text` — boolean filter

*Handoff generated by generate_bread_retail_handoff.py — 2026-05-25*