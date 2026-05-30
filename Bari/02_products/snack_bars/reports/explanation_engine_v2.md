# Explanation Engine v2 — Snack Bars
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Priority 5  
**Scope:** Full rebuild specification for snack bar explanation quality  
**Companion:** `snacks_explanation_engine_review_v1.md` (audit baseline)

---

## Problem Statement

The explanation audit classified 22% of snacks explanations as Strong, 44% Plausible, 22% Generic, and 12% Unsupported or Misleading. The primary failure mode is not inaccuracy — it is genericity. Explanations describe product types rather than products. A consumer reading "עיבוד מרבי ובסיס מהונדס" learns nothing they couldn't infer from the D grade itself.

**The root cause:** Explanations were written at the category level, not at the product level. They describe patterns (NOVA4 product pattern, date bar pattern) rather than the specific product's composition.

**The v2 goal:** Every explanation must contain at least one fact that is true of exactly this product and false of its category siblings.

---

## Part 1: Six Required Questions

Before writing any explanation, the CE must answer these six questions. The answer to each question must appear somewhere in the explanation output.

| # | Question | Output field | Example of correct answer |
|---|---|---|---|
| 1 | What is the single most specific structural fact about this product's ingredients? | insightLine or positiveSignals | "קמח חיטה וסירופ גלוקוז מרכיבים 60% מהמוצר" |
| 2 | What is the single most specific limiting nutritional fact? | limitingFactors | "28ג׳ סוכר ל-100ג׳ — גבוה מהממוצע בקטגוריה ב-8ג׳" |
| 3 | Is there a sibling product (≥5 points different) that sharpens the explanation? | comparisonContext | "11 נקודות מתחת לחטיף התמרים המוביל, שנבנה מ-4 מרכיבים בלבד" |
| 4 | What would a consumer most likely be wrong about when looking at this product? | insightLine or bottomLine | "מיצוב 'פיטנס' — 22ג׳ חלבון אבל 8 מרכיבי עיבוד" |
| 5 | Does the product make a claim (name, label, marketing) that is contradicted by composition? | insightLine or limitingFactors | "שם: 'חטיף דגנים מלאים'. מרכיב ראשון: סוכר." |
| 6 | What single change to this product would most significantly improve its score? | bottomLine | "הסרת ציפוי שוקולד ייחסוך כ-8 נקודות של עיבוד" |

**Minimum passing threshold:** Questions 1, 2, and 4 must be answered in every explanation. Questions 3, 5, and 6 are required where the data supports them. An explanation that cannot answer question 1 with a specific number or ingredient name is not strong.

---

## Part 2: Banned Phrases

These phrases are prohibited in all v2 explanations. They describe categories, not products.

| Banned phrase | Reason | Replace with |
|---|---|---|
| עיבוד מרבי | Describes NOVA4 as a class | Name the specific processing markers present |
| בסיס מהונדס | Describes any ultra-processed product | Name the actual base ingredients |
| ריבוי ממתיקים | Describes a pattern | List the specific sweeteners present |
| מיצוב פיטנס | Describes a brand position | Quantify what "fitness" means for this product |
| מוצר מעובד מאוד | Tautology — the grade says this | Name what the processing consists of |
| בעיית סוכר | Too vague | State the exact sugar level and threshold |
| חלבון נמוך | Comparative without reference | State the exact protein and the category average |
| מרכיבים רבים | Vague | State the ingredient count and the threshold |
| ציון בסיסי | Means nothing | Explain what drives the score to this level |

---

## Part 3: Phrase Library — Strong vs. Generic

### For high-sugar products

**Generic (banned):** "תכולת סוכר גבוהה"  
**Strong:** "28ג׳ סוכר ל-100ג׳ — גבוה מהממוצע בקטגוריה ב-8ג׳"  
**Strong:** "סוכר גלם + סירופ גלוקוז מופיעים במרכיבים 2 ו-3"  
**Strong:** "מרכיב ראשון: סוכר לבן. הוא מכסה 28% מהמוצר לפי הצהרת תזונה."

### For processing markers

**Generic (banned):** "מוצר מעובד עם תוספים"  
**Strong:** "ציפוי שוקולד + סירופ תירס + לציטין + מייצב = 4 מרכיבי עיבוד בקריאה ראשונה"  
**Strong:** "חומר טעם מופיע ברשימת המרכיבים ללא פירוט מקור"  
**Strong:** "6 מרכיבי עיבוד, לא כולל הגרגירים המנופחים שמשמשים כבסיס"

### For fitness/health positioning

**Generic (banned):** "מיצוב פיטנס מטעה"  
**Strong:** "22ג׳ חלבון — חזק. 8 מרכיבי עיבוד — לא פחות."  
**Strong:** "'High Protein' על האריזה; 68% מהקלוריות מפחמימות מזוקקות"  
**Strong:** "הציון נמוך מ-ממוצע הקטגוריה, על אף ה-22ג׳ חלבון — הפחמימות המזוקקות שוקלות יותר"

### For date bars / natural sugar

**Generic (banned):** "בסיס טבעי אך סוכר גבוה"  
**Strong:** "4 מרכיבים, אחד מהם תמרים שמספקים 35ג׳ סוכר — כולו מהפרי, אפס תוספת"  
**Strong:** "תמרים הם ~65% פחמימות; ב-100ג׳ חטיף זה מספק 35ג׳ סוכר גם ללא שורת ייצור אחת"  
**Strong:** "NOVA2 עם אפס תוספים — ה-B מגיע ממבנה, לא מתזונה"

### For whole-grain/oat bars

**Generic (banned):** "שיבולת שועל כבסיס עם בעיות"  
**Strong:** "שיבולת שועל מלאה ראשונה ברשימה (54%), אבל הוספת סוכר לבן ודבש מעלה את הסוכר הכולל ל-11ג׳"  
**Strong:** "NOVA3 — סירופ הגלוקוז לא מופיע בחזית האריזה, אבל הוא מרכיב מספר 4"  
**Strong:** "שיבולת שועל מלאה + שוקולד מריר + סוכר = 12 מרכיבים; 7 מהם מוסיפים עיבוד"

### For protein bars (NOVA4, engineered)

**Generic (banned):** "חלבון גבוה עם בעיות עיבוד"  
**Strong:** "חלבון מי גבינה כמרכיב ראשון, סירופ גלוקוז כשני — שני הכיוונים מוצגים בשקיפות על הפנל"  
**Strong:** "28ג׳ חלבון, אבל גם 20ג׳ סוכר ולציטין + 3 ממתיקים — הציון משקלל את שניהם"  
**Strong:** "6 ממתיקים שונים: מלטיטול, סוכרלוז, סטיביה, ממתיק אססולפאם, מלטוז, דקסטרוז"

---

## Part 4: Explanation Templates by Product Type

### Type A: Date Bars (NOVA2, whole-food base)

**Profile:** 3–6 ingredients, dates dominant, minimal processing, high natural sugar (25–50g/100g), low protein.

**insightLine template:**
```
[N] מרכיבים, [primary_ingredients] — [sugar]ג׳ סוכר ל-100ג׳, כולם מהפרי, ללא תוספת
```
Example: "4 מרכיבים, תמרים ושקדים — 35ג׳ סוכר ל-100ג׳, כולם מהפרי, ללא תוספת"

**positiveSignals template:**
- "[N] מרכיבים בלבד — רשימה הקצרה מ-90% מהחטיפים בקטגוריה"  
- "NOVA2: מוצר שעבר עיבוד מינימלי — בעיקר כבישה ועיצוב"  
- "אפס תוספים, אפס סירופ, אפס חומרי טעם"

**limitingFactors template:**
- "[sugar]ג׳ סוכר ל-100ג׳ — גבוה מהממוצע האירופי לחטיף בריאות ב-[delta]ג׳, גם אם הכל מתמרים"  
- "[protein]ג׳ חלבון — נמוך בהשוואה לחטיפי NOVA3 עם בסיס שיבולת שועל"

**bottomLine template:**
```
[score]/[grade]: מבנה מינימלי, אבל [sugar]ג׳ סוכר לא נעלמים גם אם המקור הוא תמר.
```

**comparisonContext:**
```
בקטגוריה זו, [best_date_bar] קיבל [score_best] — [current_product] נמוך ב-[delta] נקודות בגלל [specific_difference].
```

---

### Type B: Oat/Granola Bars (NOVA3, oat base with additives)

**Profile:** Oats as first or second ingredient, 8–15 ingredients, some added sugar, 1–3 processing markers.

**insightLine template:**
```
שיבולת שועל ראשונה ברשימה — אבל [additive_count] מרכיבי עיבוד (כולל [specific_additive]) מורידים את הציון ל-NOVA3
```
Example: "שיבולת שועל ראשונה ברשימה — אבל סירופ גלוקוז ולציטין מורידים את הציון ל-NOVA3"

**positiveSignals template:**
- "שיבולת שועל מלאה: [percentage]% מהמוצר, מקור סיבים ([fiber]ג׳ ל-100ג׳)"  
- "[protein]ג׳ חלבון — ממוצע עבור קטגוריה זו"  

**limitingFactors template:**
- "NOVA3: [specific_additive_1], [specific_additive_2] נוספו לרשימת המרכיבים מעבר לבסיס הדגן"  
- "[sugar]ג׳ סוכר ל-100ג׳ — [added_sugar_markers] תורמים [estimated_portion]ג׳ מהם"

**bottomLine template:**
```
[score]/[grade]: חטיף דגנים טוב יותר מהממוצע — הבסיס האמיתי הוא שיבולת שועל, אבל [specific_additive] מציין שזה עדיין מוצר מעובד.
```

---

### Type C: Protein Bars (NOVA4, engineered, high protein)

**Profile:** 15–25g protein, protein isolate, 8+ additives, glucose syrup or maltodextrin, 18–28g sugar.

**insightLine template:**
```
[protein]ג׳ חלבון — [isolate_type] + [primary_additive]: NOVA4 עם ציון [score]/[grade]
```
Example: "22ג׳ חלבון — חלבון מי גבינה + סירופ גלוקוז: NOVA4 עם ציון 47/D"

**positiveSignals template:**
- "[protein]ג׳ חלבון ל-100ג׳ — בין ה-[percentile]% הגבוהים בקטגוריה"  
- "[fiber]ג׳ סיבים — [comment if from chicory vs. genuine]"

**limitingFactors template:**
- "NOVA4: [list_3_specific_additives] — [count] מרכיבי עיבוד ברשימה"  
- "[sugar]ג׳ סוכר בנוסף ל-[protein]ג׳ חלבון — שניהם גבוהים בו זמנית"  
- "חלבון מבודד (לא מלא) — [isolate_type] מסומן בדרגה -5 בממד איכות החלבון"

**bottomLine template:**
```
[score]/[grade]: החלבון אמיתי, העיבוד גם כן — הציון משקלל את שניהם.
```

---

### Type D: Confectionery/Ultra-Processed Bars (NOVA4, low nutrition)

**Profile:** Sugar or glucose syrup as first ingredient, 6+ additives, chocolate coating, <5g protein, >30g sugar.

**insightLine template:**
```
[primary_ingredient_1] + [primary_ingredient_2] כמרכיבים 1-2 — [score]/E
```
Example: "סוכר לבן + שמן דקל כמרכיבים 1-2, ציפוי שוקולד, 8 תוספים — 13/E"

**positiveSignals template:**
- Only factual statements if any exist. If no genuine positive exists: omit positiveSignals rather than invent one.
- Exception: "ללא גלוטן" if certified — this is a factual constraint, not a quality statement.

**limitingFactors template:**
- "[sugar]ג׳ סוכר ל-100ג׳ — [primary_sugar_ingredient] מרכיב מספר [N]"  
- "[additive_count] מרכיבי עיבוד: [list_specific_ones]"  
- "[kcal] קק״ל ל-100ג׳ — צפיפות קלורית גבוהה עם ערך תזונתי נמוך"

**bottomLine template:**
```
[score]/E: [specific_composition_fact_that_explains_the_score].
```
Example: "13/E: סוכר כמרכיב ראשון, ציפוי שוקולד, ורק 3ג׳ חלבון — שילוב שמאפיין את תחתית הקטגוריה."

---

## Part 5: Sibling Comparison Rules

### When to use a sibling comparison

**Required:** Whenever two products in the same corpus are within the same NOVA tier and differ by 5+ points.

**Prohibited:** When the compared products are from different NOVA tiers (a NOVA2 vs NOVA4 comparison states the obvious). When the gap is <5 points.

### Format

```
[delta] נקודות [above/below] [specific_product_name] (ציון [comparison_score]) — 
הפרש זה מוסבר על ידי [specific_compositional_difference].
```

**Strong example (from audit baseline — snk-015):**
"11 נקודות מתחת לחטיף התמרים המוביל (ציון 70) — אותה קטגוריה NOVA2, אבל ציפוי שוקולד מוסיף מרכיב עיבוד ומוריד 11 נקודות"

**Weak example (banned):**
"נמוך מהמוצרים הטובים יותר בקטגוריה" — no delta, no specific product, no explanation.

### Products available for comparison in snack bars corpus

| Product | Score | NOVA | Key distinguisher |
|---|---|---|---|
| חטיף תמרים במילוי חמאת שקדים | 70 | 2 | Best in category — reference point for date bars |
| מרבה סלים דליס (various) | 51–59 | 3 | Reference for NOVA3 chocolate-coated bars |
| Nature Valley Protein | 47–48 | 4 | Reference for NOVA4 protein-positioned bars |
| חטיפי פיטנס קלאסי | 46 | 4 | Reference for Nestlé Fitness line |
| Corny chocolate bars | 13–18 | 4 | Bottom of category — reference for confectionery |

---

## Part 6: Quality Gate

Each explanation is evaluated against this gate before approval. A "No" answer to any required question fails the explanation.

| Check | Required? | Pass criteria |
|---|---|---|
| insightLine contains a specific number | Yes | A quantity (g, %, kcal, count) appears |
| insightLine names a specific ingredient | Yes | A named ingredient (not "additives", not "sugar" alone) appears |
| insightLine does not use any banned phrase | Yes | None of the 9 banned phrases present |
| positiveSignals reference actual values | Yes | At least one bullet contains a measurable fact |
| limitingFactors explain the WHY | Yes | At least one bullet contains because/since/explains, not just the problem |
| comparisonContext references a real corpus product | If applicable | Named product with exact score from the corpus |
| Question 5 (claim vs. composition gap) is addressed | If applicable | If product name/label makes a claim, it's tested in explanation |
| Explanation is product-specific | Yes | Could this same explanation apply to another product in the corpus? If yes, it fails. |

---

## Part 7: Full Rebuilt Explanations — 6 Priority Products

### snk-001: חטיף תמרים במילוי חמאת שקדים — 70/B

**insightLine:**  
"4 מרכיבים בלבד: תמרים, חמאת שקדים, קקאו, קוקוס — ה-B מגיע ממבנה פשוט, לא מתזונה מושלמת"

**positiveSignals:**  
- "4 מרכיבים — רשימה קצרה יותר מ-90% מהחטיפים בקטגוריה"
- "NOVA2: ייצור מינימלי, ללא סירופ, ללא תוספים, ללא חומרי טעם"

**limitingFactors:**  
- "~35ג׳ סוכר ל-100ג׳ — גבוה, כולו מתמרים, אבל הגוף מגיב לסוכר פרי בצפיפות זו באופן דומה לסוכר רגיל"
- "4ג׳ חלבון ל-100ג׳ — נמוך; המלית מעשירה בשומן בריא, לא בחלבון"

**bottomLine:**  
"70/B: הטוב ביותר בקטגוריה — מבנה נקי, אבל מי שמתמקד בסוכר יבחין שמדובר בחטיף פירות דחוס, לא חטיף דל-קלוריות"

**comparisonContext:**  
"הניקוד הגבוה ביותר בקטגוריית חטיפי החטיפים. המוצר הדומה ביותר (תמרים + ציפוי שוקולד) קיבל 56 — 14 נקודות פחות בגלל מרכיב הציפוי."

---

### snk-005: נייצר וואלי פרוטאין בוטנים ושבבי שוקולד — 47/D

**insightLine:**  
"22ג׳ חלבון אמיתי — אבל סירופ גלוקוז, ציפוי שוקולד, ולציטין מסמנים NOVA4 עם ציון 47/D"

**positiveSignals:**  
- "22ג׳ חלבון ל-100ג׳ — גבוה מהממוצע בקטגוריה NOVA4 ב-8ג׳"
- "5ג׳ סיבים — בינוני-גבוה לחטיף מסוג זה"

**limitingFactors:**  
- "סירופ גלוקוז כמרכיב מספר 2 — תורם לציון ה-NOVA4 ומוריד 8 נקודות מממד העיבוד"
- "18ג׳ סוכר ל-100ג׳ בנוסף ל-22ג׳ חלבון — שניהם גבוהים בו זמנית; אין פשרה"
- "ציפוי שוקולד: מרכיב עיבוד נוסף שמוסיף 8 נקודות של עיבוד לעומת הגרסה ללא ציפוי"

**bottomLine:**  
"47/D: חלבון אמיתי במסגרת מהונדסת — לצרכן שמחפש חלבון בלבד, ניקוד D מגיב לכל שאר המרכיבים"

**comparisonContext:**  
"1 נקודה מעל לגרסת הקרמל-מלוח (46/D) — ההבדל: ציפוי קרמל מוסיף מרכיב עיבוד נוסף"

---

### snk-013: שחור ולבן חטיף דגנים בטעם שוקולד עם 30% מילוי קרם — 13/E

**insightLine:**  
"סוכר לבן מרכיב ראשון, שמן דקל שני — 30% מילוי קרם פירושו 30% שומן+סוכר בתוך גרגיר מנופח"

**positiveSignals:**  
(None — no genuine positive signal to report for this product.)  
"ללא נתונים חיוביים שניתן לדווח עליהם בנאמנות"

**limitingFactors:**  
- "סוכר כמרכיב 1 + שמן דקל כמרכיב 2 — שני הבסיסים הם תוספים, לא דגן"
- "8 מרכיבי עיבוד: לציטין, חומצה ציטרית, נתרן ביקרבונט, חומר טעם, צבע מאכל, מייצב, מתחלב, ומולסה"
- "3ג׳ חלבון ו-2ג׳ סיבים ל-100ג׳ — הנמוכים בין כל 18 המוצרים המוצגים"

**bottomLine:**  
"13/E: תחתית הקטגוריה — בסיס סוכר+שמן, מוצג כחטיף דגנים; הגרגיר המנופח מופיע רק כמרכיב מספר 5"

**comparisonContext:**  
"34 נקודות מתחת לממוצע הקטגוריה (47) — הפרש מוסבר על ידי בסיס שונה מהיסוד: שם בסיס הדגן, כאן בסיס הסוכר"

---

### snk-009: קראנצ'י חטיף שיבולת שועל עם חתיכות בטעם שוקולד — 45/D

**insightLine:**  
"שיבולת שועל מלאה ראשונה (54%), אבל סירופ גלוקוז ודבש מרימים את הסוכר ל-11ג׳ — NOVA3, ציון 45/D"

**positiveSignals:**  
- "שיבולת שועל מלאה: 54% מהמוצר — מרכיב ראשון ומשמעותי"
- "3ג׳ סיבים — בינוני לקטגוריה זו"

**limitingFactors:**  
- "סוכר לבן + סירופ גלוקוז + דבש = 3 מקורות סוכר ברשימת המרכיבים"
- "12 מרכיבים: כל מרכיב מעל 8 מוסיף עיבוד ומוריד ניקוד"
- "חומר טעם וריח — לא מצוין מקור (טבעי/מלאכותי)"

**bottomLine:**  
"45/D: שיבולת שועל אמיתית לא מספיקה כשהיא מגיעה עם 3 מקורות סוכר ו-12 מרכיבים"

**comparisonContext:**  
"8 נקודות מתחת לגרסת המייפל (53/C) של אותה חברה — ההבדל: גרסת המייפל יש לה פחות מרכיבים ומרכיב הדגן גבוה יותר"

---

### snk-019: קורני חטיפי דגנים+שוקולד חלב — 16/E

**insightLine:**  
"סוכר כמרכיב ראשון, ציפוי שוקולד חלב, סירופ תירס — Corny כבסיס לשוקולד, לא הפוך"

**positiveSignals:**  
(None applicable.)

**limitingFactors:**  
- "סוכר לבן מרכיב 1: לפי חוק, הוא המרכיב בכמות הגדולה ביותר — יותר מהדגן עצמו"
- "ציפוי שוקולד חלב: מוסיף לציטין, שמן קנולה, ולחות שוקולד (סוכר+שמן+קקאו)"
- "30ג׳ סוכר ל-100ג׳ — הנמוך מ-4 מוצרי Corny בקטגוריה. הגבוה עומד על 36ג׳"

**bottomLine:**  
"16/E: שם המותג Corny מתייחס לתירס, לא לאיכות תזונתית. המוצר הוא שוקולד חלב עם גרגיר דגן — לא דגן עם שוקולד."

**comparisonContext:**  
"2 נקודות מעל לגרסת קוקוס (14/E) של אותה משפחה — כל ה-Corny נמצאים ב-13–19, הפרשים של 1–3 נקודות בלבד"

---

### snk-020: חטיפי פיטנס שקדים ודבש — 45/D

**insightLine:**  
"'שקדים ודבש' בשם — שקדים בפועל: 5% מהמוצר. קמח חיטה + סוכר + סירופ גלוקוז כ-60%"

**positiveSignals:**  
- "3ג׳ חלבון מהשקדים (5%) + 4ג׳ נוספים מהדגן — בינוני"

**limitingFactors:**  
- "פיטנס = מותג Nestlé, לא תיאור תזונתי: 45ג׳ פחמימות ל-100ג׳, רובן מזוקקות"
- "שקדים ב-5%: בכמות זו, הם מרכיב טעם, לא מרכיב מזין"
- "28ג׳ סוכר ל-100ג׳: גבוה מהממוצע בקטגוריה NOVA4 ב-4ג׳"

**bottomLine:**  
"45/D: 'שקדים ודבש' הוא שם שיווקי. הקריאה בתזונה מראה פחמימות מזוקקות כבסיס, לא שקדים."

**comparisonContext:**  
"1 נקודה פחות מגרסת Fitness Classic (46/D) — הפרש שנובע מאחוז השקד הגבוה מעט יותר בקלאסי"

---

## Part 8: Writing Cadence and Version Protocol

**v2 explanations replace v1 explanations.** No product should have both. When a v2 explanation is approved for a product, the v1 insightLine is removed from the frontend data.

**Approval flow:**  
1. Draft explanation against 6 questions  
2. Pass quality gate (Part 6)  
3. CE Controller review  
4. Update `snacks_frontend_v2.json` — replace `insightLine` and update `expansion` fields

**Target:** 18 products, rebuild all explanations. Estimate: 45–60 minutes per product for draft + review.

**Priority order for rebuild:**  
1. snk-013, snk-006, snk-019, snk-020 — currently Generic or Unsupported (highest risk)  
2. snk-002, snk-007, snk-008, snk-010, snk-011, snk-012, snk-014, snk-016, snk-017 — currently Plausible (moderate risk)  
3. snk-001, snk-003, snk-004, snk-005, snk-015, snk-018 — currently Strong (verify, light edit only)
