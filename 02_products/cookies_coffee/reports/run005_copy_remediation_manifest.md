# run_005 Copy Remediation Manifest — cookies-coffee
**Generated:** 2026-06-14 (orchestrator; rebuilt after Data Agent socket failure)
**Source of truth:** run_cookies_005 traces. Live JSON already regenerated (score==trace 0 mismatch, C5/D22/E31).
**Content task:** fix ONLY the copy below. Do NOT touch scores/structural fields.

## A) Prologue — C-count changed 7 → 5
Current line: "שבעה מוצרים בלבד הגיעו לציון C." → must become **חמישה** (five). Verify the rest of the prologue distribution (58 / 24 / 28 / 6) is unchanged — those are nutrition red-label counts, NOT affected by Fix-A/B/C.

## B) Grade-change verdicts (rowVerdict cites the OLD grade — now false)

### 7290018893845 — פתי בר בטעם חמאה — צ'וקטה  (C→D, score now 36.0)
- has_phvo: False  markers: []  ing_count: 10
- STALE rowVerdict: פתי בר החמאה של צ'וקטה מגיע ל-C עם שומן רווי מינימלי — הנמוך ביותר בין ה-C. המגביל: סוכר של 21 גרם ל-100 גרם שחוצה את סף התווית האדומה. כשהשומן הוא לא הבעיה והסוכר כן — זה מה שמסביר את המיקום.
- STALE insightLine: פתי בר עם שומן רווי מינימלי — הסוכר הוא המגביל.
- FIX: grade letter → D; if has_phvo, NAME the hardened fat as the driver.

### 7290119041107 — עוגיות מרוקאיות עגול — VOILA  (C→D, score now 36.6)
- has_phvo: True  markers: ['מרגרינה']  ing_count: 9
- STALE rowVerdict: העוגיות המרוקאיות העגולות של VOILA מגיעות ל-C עם סוכר מתון (כ-14 גרם). הבלם הוא השומן הרווי — כ-7 גרם ל-100 גרם, שחוצה את הסף ומשאיר אותן בתחתית ה-C. רשימת הרכיבים במקור חלקית — ברי מציגה את מה שאומת.
- STALE insightLine: עוגייה מרוקאית מסורתית — שומן רווי חוצה את הסף.
- FIX: grade letter → D; if has_phvo, NAME the hardened fat as the driver.

### 7290018371930 — פתי בר קמח כוסמין אורגני — השדה  (D→E, score now 29.0)
- has_phvo: False  markers: []  ing_count: 7
- STALE rowVerdict: פתי בר הכוסמין האורגני של השדה מגיע ל-D עם שומן רווי שחוצה את הסף וסוכר של 24 גרם. שני מגבילים פועלים כאן. 'אורגני' הוא תווית תהליך — לא מספרת על כמות הסוכר או השומן הרווי. הכוסמין הוא יתרון ממשי שאינו מבטל שניהם.
- STALE insightLine: כוסמין אורגני — שני מגבילים: שומן רווי וסוכר.
- FIX: grade letter → E; if has_phvo, NAME the hardened fat as the driver.

### 74184 — פתי בר קלאסי — אסם  (D→E, score now 21.0)
- has_phvo: False  markers: []  ing_count: 9
- STALE rowVerdict: פתי בר הקלאסי של אסם מגיע ל-D עם שומן רווי נמוך יחסית וסוכר של 22 גרם שחוצה את הסף. ביסקוויט ישראלי מוכר שמגיע לאותו ציון D שרוב המדף מגיע אליו. פשוט, מוכר, ולא יוצא דופן.
- STALE insightLine: פתי בר ישראלי קלאסי — סוכר חוצה את הסף.
- FIX: grade letter → E; if has_phvo, NAME the hardened fat as the driver.

## C) Hardened-fat products (has_phvo=True) — verdict should NAME מרגרינה/מחמאה (owner comment #7)
These now correctly carry a fat_quality ceiling (40). The verdict should call out the cheap hardened fat as the reason — e.g. 'משתמשת במרגרינה/שומן מוקשה, חריג למדף, ולכן נענשת'.

### 7290013740540 — עוגיות אוזן פיל ללת"ס — קופסת העוגיות של רחלי  (score 43.5/D)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות אוזן הפיל ללא תוספת סוכר של קופסת העוגיות של רחלי מגיעות ל-D. הסוכר מאופס — אך השומן הרווי (כ-9 גרם ל-100 גרם) נשאר גבוה, זהה לגרסה הרגילה. הסרת הסוכר לא שינתה את פרופיל השומן.

### 7290017898506 — ביסקוטי — החוש השישי  (score 37.1/D)
- markers: ['מחמאה', 'שומנים מוקשים']  | verdict already names fat? False
- current rowVerdict: הביסקוטי של החוש השישי מגיע ל-D עם שומן רווי של 4 גרם ל-100 גרם וסוכר של 20 גרם. הסוכר הוא המגביל הבודד כאן. ביסקוטי אפוי פעמיים בצורתו המסורתית — ביסקוויט שמתנהג בדיוק כמו שצפוי ממנו.

### 7290119041152 — עוגיות ריפ'את — VOILA  (score 36.6/D)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות הריפ'את של VOILA מגיעות ל-D עם פרופיל קרוב לאחיות שלהן באותה מותג. הסוכר לא חוצה את הסף — השומן הרווי הוא מה שמושך את הציון. מוצר שמשקף את טווח ה-D הנפוץ במדף זה.

### 7290119041107 — עוגיות מרוקאיות עגול — VOILA  (score 36.6/D)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: העוגיות המרוקאיות העגולות של VOILA מגיעות ל-C עם סוכר מתון (כ-14 גרם). הבלם הוא השומן הרווי — כ-7 גרם ל-100 גרם, שחוצה את הסף ומשאיר אותן בתחתית ה-C. רשימת הרכיבים במקור חלקית — ברי מציגה את מה שאומת.

### 7290119041053 — עוגיות סגנון מרוקאי — VOILA  (score 36.6/D)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות הסגנון המרוקאי של VOILA מגיעות ל-D עם שומן רווי של כ-7 גרם ל-100 גרם וסוכר מתון. השומן הרווי הוא המגביל הבודד, אבל רמת העיבוד גבוהה יותר מגרסת ה-C של אותו מוצר — זה מה שמסביר את ההבדל.

### 7290013453631 — עוגיות חמאת בוטנים כשל"פ — דני וגלית  (score 32.0/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות חמאת הבוטנים של דני וגלית מכילות כ-15 גרם חלבון ל-100 גרם — תוצאה ישירה של חמאת הבוטנים כרכיב מוביל, לא של תוסף חלבון. אבל הסוכר עומד על כ-25 גרם ל-100 גרם ושני הסף נחצו: גם סוכר וגם שומן רווי. חלבון גבוה מבוטנים הוא עובדה תזונתית; הוא לא הופך את העוגייה לבחירה בריאה יותר. הציון E משקף את משקל הסוכר והשומן הרווי, לא את החלבון.

### 7290013740694 — עוגיות אלפחורס — קופסת העוגיות של רחלי  (score 28.3/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות האלפחורס של קופסת העוגיות של רחלי מגיעות ל-E עם שומן רווי גבוה וסוכר של 21 גרם. שני הסף נחצו, ורמת העיבוד גבוהה יותר מרוב המוצרים באותו מותג. עוגיית מילוי מסורתית שמביאה עמה פרופיל מאתגר.

### 7290119043798 — עוגיות אוזניות — לה פזואלוס  (score 25.8/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות האוזניות של לה פזואלוס מגיעות ל-E עם שומן רווי גבוה וסוכר של כ-20 גרם. שני הסף נחצו. מוצר שמשלב צורה מסורתית עם פרופיל שומן וסוכר הטיפוסי לתחתית הקטגוריה.

### 4820180816590 — עוגיות עם גרעיני חמנייה — PASTICERE  (score 24.0/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות גרעיני החמנייה של PASTICERE מגיעות ל-E עם שומן רווי גבוה וסוכר של 26 גרם. שני הסף נחצו. גרעיני חמנייה כרכיב לא משנים את הפרופיל הכולל של שומן וסוכר.

### 4820180816576 — עוגיות עם שבבי קוקוס — PASTICERE  (score 24.0/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות שבבי הקוקוס של PASTICERE מגיעות ל-E עם שומן רווי גבוה וסוכר של כ-22 גרם. שני הסף נחצו בבירור. קוקוס הוא מקור שומן רווי גבוה מבסיסו — הרכיב שמסביר את פרופיל השומן.

### 7290119040803 — עוגיות קינמון מסוכרות — לה פזואלוס  (score 19.0/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות הקינמון המסוכרות של לה פזואלוס מגיעות ל-E עם שומן רווי גבוה וסוכר של 20 גרם. שני הסף נחצו, ורמת העיבוד גבוהה. 'קינמון מסוכר' הוא תיאור מדויק של מה שנמצא כאן.

### 99804 — עוגיות שוקולד לבן חלבי — שופרסל  (score 17.3/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות שוקולד לבן חלבי של שופרסל מגיעות ל-E עם שומן רווי גבוה מאוד וסוכר של 37 גרם. שוקולד לבן מכיל שומן רווי גבוה מבסיסו. הציון משקף את מבנה המוצר בצורה ישרה.

### 4820180816552 — עוגיות עם ש.שועל קוקוס — PASTICERE  (score 16.0/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות שיבולת השועל והקוקוס של PASTICERE מגיעות ל-E עם סוכר של 37 גרם ל-100 גרם — מהגבוהים ביותר במדף — לצד שומן רווי גבוה. שני הסף נחצו בבירור. 'שיבולת שועל' כיתוב ממשי; הסוכר הוא הסיפור האמיתי.

### 7290119040179 — עוגיות פרח עם ריבת תות — VOILA  (score 11.8/E)
- markers: ['מרגרינה']  | verdict already names fat? False
- current rowVerdict: עוגיות הפרח עם ריבת תות של VOILA מגיעות ל-E עם הסוכר הגבוה ביותר בקטגוריה — 44 גרם ל-100 גרם — לצד שומן רווי גבוה. ריבת תות כמילוי מוסיפה סוכר בצורה משמעותית. הציון הנמוך משקף זאת.

## Summary
- Grade-change verdicts to fix: 4
- has_phvo products to enrich: 14
- Prologue C-count fix: 1
