# Bread Blog — Stabilization Refinement Pass v1
**Date:** 2026-05-27
**Source:** bread_blog_v3.md
**Scope:** Editorial stabilization only. No new architecture. No new sections.

---

## HOW TO USE THIS DOCUMENT

Each section below names a problem, shows the current text, and shows the rewrite.
The order is: highest-impact changes first.

---

# PRIORITY FIXES (do these first)

---

## FIX 1 — Remove ScoreDriverTable as a standalone section

**Problem:** The current article structure has:
- CompositionBreakdown (5 rows explaining dimensions)
- ScoreDriverTable (8 rows explaining the same dimensions again as "signal → impact")
- ProductComparisonMatrix (2 pairs)

That is 13 analytical rows in a row, before the first comparison. This is the biggest cognitive load problem in Article 1.

**Fix:** Remove ScoreDriverTable as a standalone section entirely. The CompositionBreakdown already carries this weight. If you need a compact reference, fold 2 lines at the end of CompositionBreakdown:

> "בסיס דגן מלא ראשון ברשימה + פחות מ-7 רכיבים + סיבים מהדגן = ציון גבוה בעקביות. בסיס לבן + אינולין + רשימה ארוכה = ציון נמוך או לא נוקד."

That is enough. The full 8-row table adds analytical weight without consumer clarity.

---

## FIX 2 — Rewrite the editorial spines

### Article 1 spine

**Before:**
> "Everyday breads ranged from 40 to 75 — and ingredient list position explained most of that gap, not the product name."

**Problem:** "ingredient list position" is semi-analytical. The phrase is accurate but feels internally derived. Also: the range 40–75 includes unscored products (40 = technical floor, not a real score).

**After:**
> "לחמים דומים על אותו מדף קיבלו ציונים שונים. מה שהסביר את הפרש בדרך כלל — מה שמופיע ראשון ברשימת הרכיבים, לא מה שמופיע על האריזה."

---

### Article 2 spine

**Before:**
> "The widest score divergence in the category was in the wellness segment — driven by three gaps: fermentation name vs. ingredient list, whole spelt vs. refined spelt, and fiber value vs. fiber source."

**Problem:** This is a table of contents, not a spine. Lists three technical gap types without building tension. Reads like a framework introducing itself.

**After:**
> "הסגמנט שהבטיח הכי הרבה — מחמצת, כוסמין, זרעים — גם הראה את הפערים הגדולים ביותר בין מה שמופיע על האריזה לבין מה שמופיע ברשימת הרכיבים."

---

## FIX 3 — Rewrite InsightCards: Article 1

InsightCards currently front-load all findings before the investigation has begun. Rewrite them as entry points that gain full meaning after the map and breakdown — not as spoilers.

---

**Card 1** — Finding

Before:
> **קמח מלא ראשון ברשימה הבדיל בין המוצרים יותר מכל גורם אחר.**
> מוצרים שציינו קמח מלא כרכיב ראשון קיבלו ציון ממוצע גבוה ב-12 נקודות ממוצרים עם קמח לבן כרכיב ראשון.

**Problem:** "הבדיל בין המוצרים יותר מכל גורם אחר" is analytical comparative language. Reads like a regression analysis conclusion, not a shelf observation. "גורם אחר" is framework-visible.

After:
> **לחמי שיפון שקיבלו ציון גבוה — כולם ציינו קמח מלא כרכיב ראשון.**
> ברשימת הרכיבים, הרכיב הראשון הוא הכי נפוח במוצר. כשקמח מלא מופיע ראשון, הוא הבסיס — לא תוספת. ממוצע הציון: גבוה ב-12 נקודות ממוצרים עם קמח לבן ראשון.

---

**Card 2** — Gap

Before:
> **46% מהמוצרים לא קיבלו ציון — הנתונים לא היו זמינים.**
> לא מדובר בכישלון ניתוח. נתוני הרכיבים פשוט לא היו זמינים לציבור עבור חלק גדול מהמדף. זה עצמו ממצא.

**Problem:** "לא מדובר בכישלון ניתוח" is defensive. The second sentence then re-explains the same thing. Two sentences to say one thing.

After:
> **46% מהמדף לא קיבלו ציון.**
> רשימת הרכיבים לא הייתה זמינה לציבור עבור קרוב למחצית המוצרים. ברמן, וונדר ואנג'ל נכללים בחלק גדול ממקרים אלה. זה עצמו מה שמצאנו.

---

**Card 3** — Finding

Before:
> **17.4 גרם סיבים לא הצדיקו ציון גבוה — כשהסיבים הגיעו מאינולין.**
> מוצר עם הסיבים הגבוהים ביותר בקטגוריה (17.4g) קיבל את הציון הנמוך ביותר האפשרי בגלל מקור הסיבים, לא כמותם.

**Problem:** "לא הצדיקו" is a judgment word. "הציון הנמוך ביותר האפשרי" reveals the scoring system mechanics (the floor). The word "האפשרי" is odd in this context.

After:
> **המוצר עם הסיבים הגבוהים ביותר לא קיבל ציון.**
> לחמניות לס קיטו — 17.4 גרם סיבים, מקור: אינולין. לחם שיפון קל — 12.4 גרם סיבים, מקור: קמח שיפון מלא. שניהם על אותו מדף. הציון משקף את המקור, לא את המספר.

---

**Card 4** — Pattern

Before:
> **רשימות רכיבים קצרות ופשוטות יחסו ציונים עקביים.**
> מוצרים עם פחות מ-7 רכיבים והרכיב הראשון קמח מלא הפגינו עקביות גבוהה יותר בציון מאשר מוצרים ארוכי-רשימה עם אותו בסיס דגנים.

**Problem:** "יחסו ציונים עקביים" is odd — "bestowed consistent scores" doesn't land in Hebrew. "הפגינו עקביות" is analytical. "ארוכי-רשימה" is a slightly unnatural construction.

After:
> **4–6 רכיבים, קמח מלא ראשון — ציונים עקביים.**
> מוצרים עם רשימות קצרות ובסיס דגן מלא הציגו עקביות ניכרת. מוצרים עם רשימות ארוכות ובסיס קמח לבן — ציונים נמוכים יותר. ההשוואה נעשתה בתוך קטגוריות דומות.

---

## FIX 4 — Rewrite InsightCards: Article 2

---

**Card 1** — Finding

Before:
> **13 מוצרים שמו "מחמצת" בשמם — בכולם, שמרים תעשייתיים הם המחמיץ הראשי ברשימה.**
> מחמצת מופיעה ברשימת הרכיבים שלהם, אך שמרים תעשייתיים מופיעים לפניה. לא ניתן לאמת שמחמצת היא מנגנון ההתפחה הדומיננטי.

**Problem:** "המחמיץ הראשי" is an unusual compound. "מנגנון ההתפחה הדומיננטי" is technical — not consumer language.

After:
> **13 מוצרים כוללים "מחמצת" בשמם — בכולם, שמרים תעשייתיים מופיעים ברשימת הרכיבים לפני המחמצת.**
> ברי לא יכולה לאמת שמחמצת היא מה שמתפיח את הלחם. מחמצת מצוינת — אבל שמרים מופיעים קודם.

---

**Card 2** — Ambiguity

Before:
> **"כוסמין" ו-"כוסמין מלא" — לא אותו דבר.**
> כשהמילה "מלא" לא מופיעה לידי שם הדגן ברשימת הרכיבים, ברי אינה יכולה לאמת שמדובר בכוסמין מלא. זה לא שלילה — זה גבול הנתונים.

**Problem:** "זה לא שלילה — זה גבול הנתונים" is defensive/apologetic. Forbidden by the no-apology rule.

After:
> **"כוסמין" ו-"כוסמין מלא" — לא אותו דבר.**
> כשהמילה "מלא" לא מופיעה ברשימת הרכיבים לצד שם הדגן, ברי לא מאמתת כוסמין מלא — גם אם הוא מוצג ככזה על האריזה.

---

**Card 3** — Finding

Before:
> **הציון הגבוה ביותר בכל הקטגוריה הוא של קרקר, לא לחם — 82/A.**
> אף לחם לא הגיע לדרגה A. הציון הגבוה ביותר של לחם הוא 75/B. הפרש של 7 נקודות בין הקרקר הטוב ביותר ללחם הטוב ביותר — שניהם כוסמין מלא.

**Problem:** "הטוב ביותר" is ranking language — forbidden. Both products are the same grain type but the comparison is framed as a contest.

After:
> **הציון הגבוה ביותר בקטגוריה — 82/A — הוא של קרקר, לא לחם.**
> אף לחם לא הגיע לדרגה A. הציון הגבוה ביותר של לחם: 75/B. הפרש: קרקר כוסמין מלא ושומשום מול לחם שיפון קל — שניהם בסיס דגן מלא, שני מוצרים שונים לחלוטין בהרכב.

---

**Card 4** — Finding

Before:
> **17.4 גרם סיבים קיבלו ציון נמוך מ-12.4 גרם סיבים — כשהמקור שונה.**
> כמות הסיבים לבדה לא מספיקה לאמת הרכב. מוצר עם סיבים ממקור מטריצת הדגן קיבל ציון גבוה יותר ממוצר עם סיבים גבוהים יותר אך ממקורות מוספים.

**Problem:** "17.4 גרם סיבים קיבלו ציון" is confused syntax — grams don't "receive a score." "מטריצת הדגן" is framework vocabulary.

After:
> **מוצר עם 17.4 גרם סיבים קיבל ציון נמוך יותר ממוצר עם 12.4 גרם סיבים.**
> ההבדל: מאיפה הסיבים מגיעים. 12.4 גרם מקמח שיפון מלא — ציון גבוה. 17.4 גרם מאינולין — לא נוקד. הכמות לבדה לא מספיקה.

---

**Card 5** — Gap

Before:
> **זרעים על גבי בסיס מזוקק — לא אותו דבר כמו זרעים בתוך בסיס דגן מלא.**
> מוצרים עם זרעים כרכיב שניה עד שלישי ברשימה לאחר קמח מלא — שונים ממוצרים שבהם הזרעים מופיעים על גבי קמח לבן כרכיב ראשון.

**Problem:** "מזוקק" is a chemistry/industrial term consumers don't naturally use for bread. "כרכיב שניה עד שלישי" is list-position vocabulary — analytical.

After:
> **שני קרקרים עם זרעים. הפרש ציון: 10 נקודות.**
> מה הפריד ביניהם — לא הזרעים. הבסיס שעליו הזרעים מופיעים: קמח כוסמין מלא מול קמח חיטה לבן. הזרעים מוסיפים — הבסיס קובע.

---

# SECTION-BY-SECTION REFINEMENTS

---

## ARTICLE 1 — CompositionBreakdown

### Row 1 — Flour Position

**Before:**
> הרכיב הראשון ברשימת הרכיבים הוא הנפוח ביותר.

**Problem:** "הנפוח ביותר" is accurate but sounds technical. Consumers need to understand *why this matters*, not just the rule.

**After:**
> ברשימת הרכיבים, הרכיב הראשון הוא בדרך כלל הכי נפוח. כשקמח מלא מופיע ראשון — הוא הבסיס של המוצר, לא תוספת. כשקמח לבן מופיע ראשון — הבסיס לבן, גם אם קמח מלא מופיע מאוחר יותר.

---

### Row 3 — Ingredient List Length

**Before:**
> רשימה ארוכה אינה בהכרח בעיה, אבל רשימה ארוכה עם תוספים לצד בסיס קמח לבן מצביעה על הנדסת מוצר בהיעדר מטריצה חזקה.

**Problem:** "הנדסת מוצר בהיעדר מטריצה חזקה" is framework language. "אינה בהכרח בעיה" is a double negative that hedges before explaining.

**After:**
> מוצרים עם 4–6 רכיבים ובסיס דגן מלא הציגו עקביות ניכרת בציון. רשימה ארוכה עם קמח לבן ראשון ותוספי סיבים — דפוס שונה לחלוטין.

---

### Row 4 — Data Availability

**Before:**
> ~46% מהמוצרים לא קיבלו ציון מלא כי לא היו נתוני רכיבים מלאים זמינים לציבור. לא ניתן לנתח מוצר שרשימת רכיביו לא גלויה.

**Problem:** Second sentence is defensive — "לא ניתן לנתח" sounds like an excuse. The fact is enough.

**After:**
> 46% מהמדף לא קיבלו ציון. רשימת הרכיבים לא הייתה זמינה לציבור — ברמן, וונדר ואנג'ל בחלק גדול מהמקרים. ציון לא ניתן לחשב ללא נתונים.

---

### Row 5 — Whole Grain Claim Accuracy

**Before:**
> מוצרים שמציינים "100% מלא" או "מלא" בשמם אבל לא מאמתים זאת ברשימת הרכיבים (כלומר, קמח לבן מופיע ראשון) מקבלים ניתוח שמרני יותר.

**Problem:** "ניתוח שמרני יותר" is internal framework language. "כלומר" parenthetical reads like a footnote.

**After:**
> השם על האריזה ורשימת הרכיבים לא תמיד מסכימים. ברי מבססת את הציון על מה שמצוין ברשימת הרכיבים — לא על מה שמופיע בשם המוצר. דוגמה: לחם קמח מלא 100% — הציון מבוסס על מה שמופיע ראשון ברשימה.

---

## ARTICLE 1 — ProductComparisonMatrix

### Pair 2 explanation

**Before:**
> "שניהם לחמי שיפון מלא. שניהם ללא טענת 'מחמצת' גדולה על האריזה. הפרש הציון — 8 נקודות — נובע בעיקר מהפרש כמות הסיבים הנגזרת מהרכב הדגן: 12.4 גרם מול 5.8 גרם. לחם שיפון קל גם כולל מחמצת ברשימת הרכיבים — שיפון עגול לא. שני הציונים הם B, אך הפרש של 8 נקודות מייצג הבדל אמיתי ברמת הדגן."

**Problem:** "הנגזרת מהרכב הדגן" is technical. The word "נגזרת" (derivative) is chemistry language. Also the structure buries the clearest fact (fiber quantity difference) inside an analytical phrase.

**After:**
> "שניהם לחמי שיפון מלא. שניהם ללא 'מחמצת' על האריזה. ועדיין: הפרש ציון של 8 נקודות. מה הסביר את הפרש: כמות הסיבים — 12.4 גרם מול 5.8 גרם. ולחם שיפון קל כולל מחמצת ברשימת הרכיבים; שיפון עגול לא. שניהם B — 8 הנקודות מייצגות הבדל ממשי בהרכב."

---

## ARTICLE 1 — TakeawayList

### Bullet 1

**Before:**
> מיקום הקמח ברשימת הרכיבים הוא האינדיקטור שהפריד בין המוצרים יותר מכל גורם אחר.

**Problem:** "האינדיקטור" is an analytical/borrowed term. "גורם אחר" is framework language.

**After:**
> מה שהפריד בין המוצרים יותר מכל — מה שמצוין ראשון ברשימת הרכיבים.

---

### Bullet 2

**Before:**
> ערך הסיבים הגבוה לא תמיד מייצג מקור סיבים מהדגן — כדאי לבדוק אם אינולין או שורש עולש מופיעים ברשימה.

**Problem:** "כדאי לבדוק" is advisory. This is forbidden — Bari does not give recommendations. Also the bullet starts as a finding but ends as advice.

**After:**
> מוצר עם 17.4 גרם סיבים קיבל ציון נמוך יותר ממוצר עם 12.4 גרם סיבים — כשהסיבים מגיעים מאינולין, לא מהדגן. הכמות לבדה לא מספרת את הסיפור.

---

### Bullet 3

**Before:**
> 46% מהמוצרים על המדף לא היו זמינים לניתוח מלא — הנתונים עצמם חסרים, לא הציון.

**Problem:** "הנתונים עצמם חסרים, לא הציון" is an odd correction — it sounds defensive, like distinguishing the system from the data. The fact is enough.

**After:**
> 46% מהמדף לא קיבלו ציון — רשימת הרכיבים פשוט לא הייתה זמינה לציבור.

---

## ARTICLE 2 — ThreeGapBreakdown

### Gap 1 — Product evidence display

**Before (dev-style):**
> לחם מחמצת שיפון — score 74/B — fermentation_real=false — "שמרים תעשייתיים לפני מחמצת"

**Problem:** "fermentation_real=false" is a database field, not consumer language. The dash-separated format reads like a CSV.

**After:**
> לחם מחמצת שיפון — 74/B — שמרים מופיעים ברשימה לפני המחמצת
> לחם מחמצת צרפתי פרוס — שמרים תעשייתיים עיקריים
> לחם מחמצת מכוסמין — שמרים עיקריים, בסיס לא מאומת כמלא

---

### Gap 2 — Repetition fix

**Before:**
> כמה מוצרים: כמה מוצרים מציינים כוסמין ללא "מלא"

**Problem:** "כמה מוצרים: כמה מוצרים" — duplicate.

**After:**
> כמה מוצרים: ברי זיהתה מוצרים שמציינים "כוסמין" ברשימת הרכיבים ללא קידומת "מלא".

---

### Gap 3 — Symbol removal

**Before:**
> כוסמין מלא 100% — 11.0g — מוסף (⚠)

**Problem:** ⚠ is an emoji/symbol. Forbidden by display rules.

**After:**
> כוסמין מלא 100% — 11.0g — מקור: אינולין

---

## ARTICLE 2 — ProductComparisonMatrix

### Pair 1 explanation

**Before:**
> "שני לחמי שיפון, ציון כמעט זהה. אבל: לחם שיפון קל לא כולל 'מחמצת' בשמו — ומחמצת מצוינת ברשימת הרכיבים לפני השמרים. לחם מחמצת שיפון כולל 'מחמצת' בשמו — אך שמרים תעשייתיים מופיעים ראשון ברשימה. הציון הוא B בשני המקרים. ההבדל הוא ביחס בין שם המוצר לרשימת הרכיבים."

**Problem:** "הציון הוא B בשני המקרים" appears late and interrupts the flow. The final sentence is strong but the structure buries the irony.

**After:**
> "שני לחמי שיפון — שניהם B. אבל: לחם שיפון קל לא כולל 'מחמצת' בשמו — ומחמצת מצוינת ברשימת הרכיבים לפני השמרים. לחם מחמצת שיפון כולל 'מחמצת' בשמו — ושמרים תעשייתיים מופיעים ראשון. הציון זהה; היחס בין השם לרשימה — הפוך."

---

### Pair 3 explanation

**Before:**
> "שני מוצרים עם 'כוסמין מלא' בשמם. ערכי הסיבים דומים. אבל: בקרקר כוסמין מלא, הסיבים מגיעים מקמח כוסמין מלא כרכיב ראשון. ב-כוסמין מלא 100%, הניתוח מצביע על סיבים ממקורות מוספים. הציון משקף את ההבדל הזה."

**Problem:** "הניתוח מצביע על" is framework-visible. "ממקורות מוספים" is still slightly technical. Better to name the actual ingredient.

**After:**
> "שני מוצרים, שניהם עם 'כוסמין מלא' בשם. ערכי הסיבים דומים. אבל: בקרקר כוסמין מלא ושומשום — קמח כוסמין מלא הוא הרכיב הראשון ברשימה. בכוסמין מלא 100% — אינולין מופיע כמקור הסיבים. הציון משקף את ההבדל."

---

## ARTICLE 2 — SynthesisParagraph

### Paragraph 1 — minor fix

**Before:**
> מה שמפריד את המוצרים בקטגוריה הזו הוא לא הצגת המוצר — זה מה שמופיע ראשון ברשימת הרכיבים.

**Problem:** "הצגת המוצר" is vague. Does it mean the packaging? The name? The design?

**After:**
> מה שמפריד את המוצרים בקטגוריה הזו הוא לא השם ולא האריזה — זה מה שמופיע ראשון ברשימת הרכיבים.

---

### Paragraph 2 — closing sentence

**Before:**
> המסקנה מהנתונים: מה שמצוין ברשימת הרכיבים — ולא מה שמצוין על האריזה — הוא מה שניתן לאמת.

**Problem:** "המסקנה מהנתונים:" is a robot-conclusion opener. Sounds like an automated report, not investigative writing.

**After:**
> מה שניתן לאמת — מצוין ברשימת הרכיבים. זה מה שמצאנו.

---

## ARTICLE 2 — BreadWellnessMap Cluster Labels

**Before:**
- C: "שם מחמצת / שמרים עיקריים"

**Problem:** Cluster C label reads like a code condition, not a shelf description. The "/" separator is technical shorthand.

**After:**
- C: "מחמצת בשם — שמרים ראשונים ברשימה"

**Annotation line on map:**

**Before:**
> "ציון גבוה לא תמיד אומר תסיסה מאומתת"

**After:**
> "ציון B — גם ללא תסיסה מאומתת"

Reason: shorter, more concrete, less like a framework lesson.

---

## ARTICLE 2 — Card 3 — ranking fix

**Before:**
> "הפרש של 7 נקודות בין הקרקר הטוב ביותר ללחם הטוב ביותר — שניהם כוסמין מלא."

**Problem:** "הטוב ביותר" twice — ranking language. The card is about an observation, not declaring a winner.

**After:**
> "קרקר כוסמין מלא ושומשום (82/A) מול לחם שיפון קל (75/B) — שניהם בסיס דגן מלא, הפרש של 7 נקודות."

---

# NARRATIVE FLOW RECOMMENDATIONS

---

## The investigation arc problem

**Current structure:**
```
Intro → InsightCards (all 4 findings revealed) → Map → Breakdown → Score Table → Comparisons → Takeaways
```

**Problem:** InsightCards front-load every finding before the investigation has begun. Readers are told the conclusion at the start, then shown the evidence. This is analytical order, not investigation order.

**Milk comparison worked** because the reader discovered things gradually:
- First: surprising stat
- Then: what explains it
- Then: product evidence
- Then: contrast
- Then: patterns

**Recommended arc for Article 1:**
```
Intro (what is this shelf) →
Card 1 + Card 2 (one finding, one data gap — frame, don't spoil) →
Map (show the shelf visually — the reader starts exploring) →
CompositionBreakdown (explain what they're seeing — discovery mode) →
Comparisons (two specific product contrasts — payoff) →
Cards 3 + 4 moved here as "What else we found" (Pattern / Ambiguity after the reader has context) →
Takeaways
```

**How to implement without restructuring:**
- Keep InsightCards in their current position
- Rewrite Cards 3 and 4 as "entry points" (questions, partial observations) rather than complete findings
- The full finding payoff comes in CompositionBreakdown and the Comparisons

**Card 3 rewritten as entry point:**
> **ערך הסיבים לא מספר את הסיפור המלא.**
> בקטגוריה הזו — מאיפה מגיעים הסיבים מסביר יותר מכמה. לחמניות לס קיטו ולחם שיפון קל — שניהם ציינו ערכי סיבים גבוהים. הציונים היו שונים לחלוטין.

*The CompositionBreakdown then reveals the fiber source difference fully.*

---

## Article 2 — The three-gap reveal

**Recommended arc for Article 2:**
```
Intro (why this segment has the widest divergence) →
Card 1 (13-product sourdough finding — the opening shock) →
Map (show the cluster distance visually, Cluster C annotation) →
ThreeGapBreakdown (systematic explanation of the 3 gaps) →
Comparisons (paired evidence for each gap) →
Cards 2–5 as "pattern discoveries" revealed after the reader has absorbed the gaps →
Synthesis paragraph
```

**Current structure puts Cards 2–5 before the map and gap breakdown**, which means readers are exposed to all three gap types analytically before seeing any product evidence. Same inversion problem as Article 1.

**Minimal fix**: Rewrite Cards 2, 4, 5 as questions/partial observations:

Card 2 entry-point version:
> **"כוסמין" ו-"כוסמין מלא" — ברי בדקה את ההבדל.**
> כשהמילה "מלא" מופיעה ברשימת הרכיבים — ברי יכולה לאמת. כשהיא לא מופיעה — ברי לא מאמתת, גם אם המוצר מוצג ככוסמין מלא. פרטים בהמשך.

---

# SHELF INTUITION IMPROVEMENTS

---

## Article 1 — Intro paragraph guidance

Add shelf segmentation at the start of the intro paragraph. Readers should immediately understand what type of shelf this is.

**Add to intro:**
> "המדף הזה כולל לחמי שיפון ושיפון מלא, לחמי חיטה ושיפון, לחמניות פיתות ולחמי בסיס, ומוצרים עם טענות בריאות — סיבים, קיטו, קל. 108 מוצרים, שופרסל, מאי 2026."

This one sentence tells the reader: "yes, I know these shelves." Without it, "everyday bread" is abstract.

---

## Article 1 — BreadEverydayMap cluster labels (consumer-facing)

**Current (too analytical):**
- A: "קמח מלא + סיבים מטריצה"
- B: "קמח מלא + מקור סיבים לא ברור"
- C: "בסיס לבן + תוספי סיבים"
- D: "לא זמין לניתוח"

**Recommended (shelf-intuitive):**
- A: "שיפון / חיטה מלאה — הרכב ברור"
- B: "דגן מלא — מקור הסיבים פחות מאומת"
- C: "בסיס לבן, סיבים מוספים"
- D: "נתונים לא זמינים"

**Map title:**
Before: "מה מפריד בין המוצרים — שני ממדים"
After: "איפה עומד כל מוצר: דגן ומקור הסיבים"

---

## Article 2 — intro paragraph guidance

Add segment description. Readers should immediately recognize the wellness shelf.

**Add to intro:**
> "המדף הזה — מוצרי מחמצת, כוסמין, שיפון, זרעים, קרקרים ולחמי גורמה — הוא הסגמנט עם הציפיות הגבוהות ביותר. הוא גם זה שבו נמצאו הפערים הגדולים ביותר בין שם המוצר לרשימת הרכיבים."

---

# COGNITIVE LOAD REDUCTIONS

---

## Remove: "Score Driver System explanation" as a labeled section

**Problem:** After CompositionBreakdown (5 rows), "Score Driver System explanation (prose + ScoreDriverTable)" adds 8 more rows of the same content in tabular form. The total is 13 analytical rows before the first product comparison.

**Fix:**
1. Remove the "Score Driver System" section heading entirely
2. Remove the ScoreDriverTable
3. If you want a compact reference, use this 2-line summary at the end of CompositionBreakdown:

> "בקצרה: בסיס קמח מלא ראשון + סיבים מהדגן + פחות מ-7 רכיבים = ציון עקבי. בסיס לבן + אינולין + רשימה ארוכה = ציון נמוך."

That is all the consumer needs.

---

## Compress: InsightCards 4 in Article 1

Card 4 ("רשימות רכיבים קצרות") is currently the weakest card — abstract, not tied to a specific product, and redundant with Card 1 and CompositionBreakdown Row 3. Consider replacing with a more concrete product finding:

**Stronger replacement:**
> **Pattern:**
> **לחמי שיפון קל, שיפון עגול, ואקסקלוסיבי שיפון מלא — שלושה מוצרים עם בסיס שיפון מלא, שלושה ציונים בין 67 ל-75.**
> מוצרים עם אותו בסיס דגן ורשימה קצרה הראו עקביות ניכרת. ההבדל ביניהם — כמות הסיבים ומחמצת.

---

# WORDING SIMPLIFICATIONS — GLOBAL

The following terms appear throughout both articles and should be simplified wherever possible:

| Technical/analytical | Consumer-clear |
|---|---|
| מטריצת הדגן / מטריצה | הדגן עצמו / הדגן המלא |
| מחמיץ ראשי | מה שמתפיח את הלחם |
| מנגנון ההתפחה | מה שמתפיח |
| מאומת / לא מאומת | מצוין ברשימה / לא מצוין ברשימה |
| confidence_level | (never use in consumer-facing copy) |
| אינדיקטור | מה שמצביע / מה שמסביר |
| הנגזרת מהרכב | שנובעת מהרכב |
| ניתוח שמרני | ברי מבססת על רשימת הרכיבים בלבד |
| fiber_laundering | (never use in consumer copy) |
| fermentation_real | (never use in consumer copy) |
| ביחס ל / אפקט על הציון | השפעה על הציון |

---

# READER TEST — PASS RESULTS

Running the Task 10 reader test on each major section:

---

**Section: InsightCards Article 1 (current)**

Q: Would a normal consumer understand why these products differ?
→ **PARTIAL.** Card 1 mentions "first ingredient" but doesn't explain why that matters. Card 3 has good numbers but "הצדיקו" is confusing.

Q: What mattered?
→ **PARTIAL.** Ingredient position — yes. Fiber source — somewhat. But "גורם אחר" is abstract.

Q: What Bari actually found?
→ **PARTIAL.** 12-point gap is specific. The 17.4g fiber finding is strong. But Cards 3 and 4 blend together.

Q: Why did the shelf behave this way?
→ **WEAK.** No shelf context until the map.

**After the rewrites above: PASS.**

---

**Section: CompositionBreakdown (current)**

Q: Why do these products differ?
→ **GOOD.** Five clear rows. Row 1 and Row 2 are the strongest.

Q: What mattered?
→ **GOOD.** Flour position, fiber source — clear.

Q: What Bari actually found?
→ **PARTIAL.** Row 3 (length) is too vague. Row 5 (whole grain claim) uses "ניתוח שמרני" which loses readers.

**After the rewrites above: PASS.**

---

**Section: Pair 1 — Article 1 (current)**

Q: Why do these products differ?
→ **PASS.** Fiber source difference is clear. The closing line "הציון משקף את המקור, לא את המספר" lands well.

Q: What mattered?
→ **PASS.** Specific numbers. Specific ingredient (אינולין).

---

**Section: Pair 1 — Article 2 (current)**

Q: Why do these products differ?
→ **PASS.** The fermentation inversion is clear.

Q: What Bari found?
→ **PASS.** But "הציון הוא B בשני המקרים" appears at the wrong moment — buries the irony. Fixed above.

---

**Section: ScoreDriverTable (current)**

Q: Would a consumer understand this?
→ **FAIL.** "מגביר" / "מוריד" column language is fine, but placing a separate 8-row analytical table between CompositionBreakdown and Comparisons kills reading rhythm. Most consumers will skip it.

**Fix: Remove. See Fix 1 above.**

---

**Section: SynthesisParagraph — Article 2 (current)**

Q: What Bari found?
→ **PARTIAL.** Paragraph 1 is clear. Paragraph 2 ends with "המסקנה מהנתונים:" which sounds like an automated summary.

**After the rewrites above: PASS.**

---

# SUMMARY — WHAT TO APPLY

**Must apply (high impact):**
1. Remove ScoreDriverTable as standalone section — Fix 1
2. Rewrite editorial spines — Fix 2
3. Rewrite InsightCards Article 1, Cards 1, 3, 4 — Fix 3
4. Rewrite InsightCards Article 2, Cards 1, 2, 4, 5 — Fix 4
5. Add shelf segmentation to intro paragraphs (both articles)
6. Rewrite BreadEverydayMap cluster labels (consumer-facing)
7. Fix TakeawayList Bullet 2 (advisory language)
8. Fix SynthesisParagraph paragraph 2 closing sentence

**Should apply (medium impact):**
9. CompositionBreakdown Row 1 consumer translation addition
10. CompositionBreakdown Rows 3, 4, 5 rewrites
11. Article 2 Pair 3 explanation (remove "הניתוח מצביע על")
12. Article 2 Pair 1 structure (move B-score disclosure earlier)
13. ThreeGapBreakdown product evidence format
14. BreadWellnessMap Cluster C annotation

**Nice to have (low impact):**
15. Article 2 Card 3 ranking language fix
16. Global wording substitution table
17. InsightCards reframed as entry points (narrative flow)

---
