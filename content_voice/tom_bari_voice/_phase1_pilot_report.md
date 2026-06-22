# Phase 1 pilot — Layer-1 naturalness pre-filter on bari-web/src/data/comparisons/protein_bars_frontend_v1.json

Consumer Hebrew strings scanned: 90

## [clean] /products[0]/insightLine
> כמעט היחיד כאן שבונה את החלבון מאגוז אמיתי ולא רק מאבקה — ומשלם על זה ב-17 גרם סוכר.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [medium] /products[0]/rowVerdict
> החזק במדף, וזה אמיתי: החלבון והסיבים (27 ו-13 גרם) נשענים על אגוזי לוז ותמרים, לא על תערובת מבודדים בלבד. אבל זה גם מה שמייקר אותו תזונתית — 17 גרם סוכר ו-17 גרם שומן, יותר מרוב שכניו. הכי קרוב למזון בקבוצה, עדיין לא נשנוש קל.

  - MEDIUM T1: «, לא על תערובת» — Possible 'X, לא Y' contrastive mid-text — judge whether it reads as a calque.
  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[0]/expansion/comparisonContext
> רוב המדף קונה את החלבון הגבוה בתערובת אבקות מבודדות; כאן הוא יושב על אגוז וקטנייה אמיתיים. זה היתרון שמרים אותו לראש — אבל גם מה שמשאיר 17 גרם סוכר בפנים, יותר מהשכנים שממותקים בתחליפים.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[0]/expansion/limitingFactors[0]/text
> 17 גרם סוכר ל-100 גרם — הסוכר האמיתי הזה גבוה ביחס למה שחטיף חלבון מבטיח

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[0]/expansion/limitingFactors[1]/text
> 17 גרם שומן ל-100 גרם — תורם לצפיפות הקלורית הגבוהה יחסית כאן

  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[0]/expansion/limitingFactors[2]/text
> חומר משמר אחד ברשימת הרכיבים

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[1]/insightLine
> מהגבוהים בקבוצה בחלבון (36 גרם), אבל מהמתוקים בה — 16 גרם סוכר, פי כמה מהשכנים דלי-הסוכר.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[1]/rowVerdict
> על החלבון הוא בין המובילים — 36 גרם, מהגבוהים בקבוצה, ועם שומן נמוך במיוחד. אבל בניגוד לאחיו מאותו מותג שמתיקותם מתחליפים, כאן יש 16 גרם סוכר אמיתי, וגם הנתרן מהגבוהים במדף. כמות החלבון מרשימה; שאר הפרופיל פחות נקי ממה שהשם מבטיח.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[1]/expansion/comparisonContext
> אותו מותג מוכר כמה גרסאות שמורידות סוכר בעזרת תחליפים. דווקא בגרסה הזו, עם החלבון מהגבוהים בקבוצה, הסוכר נשאר אמיתי וגבוה — וזה מה שמרחיק אותה מהקבוצה הנקייה יותר באותו מדף.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[1]/expansion/limitingFactors[0]/text
> 16 גרם סוכר ל-100 גרם — גבוה למשהו שנמכר כחטיף חלבון

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[1]/expansion/limitingFactors[1]/text
> 385 מ"ג נתרן ל-100 גרם — מהגבוהים במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[1]/expansion/limitingFactors[2]/text
> הבסיס הוא תערובת חלבונים מבודדים, לא מזון שלם

  - HIGH T1: «, לא מזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[2]/insightLine
> המספרים מושלמים — 34 גרם חלבון, כמעט בלי סוכר — אבל הם תוצאה של מעבדה, לא של מזון.

  - HIGH T1: «, לא של» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[2]/rowVerdict
> על הנייר זה הפרופיל החלומי: 33.7 גרם חלבון ובקושי 3 גרם סוכר. אבל ה'בלי סוכר' לא בא מהפחתה אמיתית — הוא מורכב מתחליפי מתיקות, ציפוי שוקולד מתועש ורשימת רכיבים ארוכה, עם 352 מ"ג נתרן. תוסף חלבון שעוצב למספרים, לא נשנוש עשוי מחומרי גלם אמיתיים.

  - HIGH T1: «, לא נשנוש» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[2]/expansion/comparisonContext
> זה בדיוק הסיפור של הקטגוריה במוצר אחד: 33.7 גרם חלבון וסוכר נמוך שלא הושגו בעזרת מזון פשוט אלא בעזרת ממתיקים מלאכותיים ורשימת רכיבים ארוכה. נוסיף לזה 352 מ"ג נתרן — מהמלוחים בקבוצה — ומתקבל פרופיל שמרשים במספרים אבל תעשייתי בהרכב.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[2]/expansion/limitingFactors[0]/text
> 352 מ"ג נתרן ל-100 גרם — מהמלוחים בקבוצת חטיפי החלבון

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[2]/expansion/limitingFactors[1]/text
> הסוכר הנמוך לא בא מהפחתה אמיתית אלא מממתיקים מלאכותיים ורשימת רכיבים ארוכה

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[2]/expansion/limitingFactors[2]/text
> 4.9 גרם שומן רווי ל-100 גרם

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[3]/insightLine
> הכי הרבה סיבים בקבוצה (19 גרם) — אבל הם מוספים מחומר מילוי, לא מדגן או אגוז.

  - HIGH T1: «, לא מדגן» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[3]/rowVerdict
> המספרים הפונקציונליים מרשימים: 36 גרם חלבון ו-19 גרם סיבים, הכי הרבה בקבוצה, עם שומן נמוך. אבל הסיבים האלה אינם מגיעים מדגן או אגוז — הם נוספו מחומר מילוי, וגם הנתרן (387 מ"ג) מהגבוהים במדף. עובד כמקור חלבון וסיבים מרוכז, פחות כנשנוש עשוי ממאכל אמיתי.

  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[3]/expansion/comparisonContext
> מוביל הסיבים בקבוצה, אבל כדאי לדעת מאיפה הם באים: לא מדגן מלא או אגוז, אלא מחומר מילוי שנוסף בייצור. עם נתרן גבוה (387 מ"ג), זה מקור חלבון וסיבים מרוכז יותר משהוא חטיף שמורכב מרכיבים אמיתיים.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[3]/expansion/limitingFactors[0]/text
> 387 מ"ג נתרן ל-100 גרם — מהגבוהים במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[3]/expansion/limitingFactors[1]/text
> הסיבים מוספים מחומר מילוי, לא ממזון שלם

  - HIGH T1: «, לא ממזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[3]/expansion/limitingFactors[2]/text
> 12 גרם סוכר ל-100 גרם

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[4]/insightLine
> מאותה משפחה מהונדסת, אבל הגרסה המאוזנת בה — נתרן מתון (160 מ"ג) במקום הנתרן הגבוה של אחיו.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[4]/rowVerdict
> אותו מתכון משפחתי — חלבון גבוה (34 גרם) וכמעט בלי סוכר — אבל זו הגרסה שמחזיקה את הנתרן במתינות (160 מ"ג) במקום לזנק כמו חלק מאחיו. עדיין נשען על תחליפי סוכר ותערובת מבודדים, אבל בתוך הקבוצה המתועשת הוא מהמאוזנים.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[4]/expansion/comparisonContext
> כמה גרסאות באותה משפחה חולקות מתכון כמעט זהה ונבדלות בעיקר בנתרן. כאן הנתרן מתון (160 מ"ג), וזה מה שמציב את הגרסה הזו מהמאוזנות בקבוצה — אותו חלבון גבוה וסוכר נמוך, בלי קפיצת המלח של אחיו.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[4]/expansion/limitingFactors[0]/text
> המתיקות הנמוכה מושגת בתחליפים, לא בהפחתה אמיתית

  - HIGH T1: «, לא בהפחתה» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[4]/expansion/limitingFactors[1]/text
> הבסיס תערובת חלבונים מבודדים, לא מזון שלם

  - HIGH T1: «, לא מזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[5]/insightLine
> שקדים וקשיו אמיתיים בפנים — אבל המתיקות הנמוכה עדיין באה מתחליפים, וצפיפות קלורית של 406 קלוריות.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [medium] /products[5]/rowVerdict
> כאן יש משהו אמיתי שרוב הקבוצה חסרה — שקדים וקשיו ממש בתוך החטיף, לא רק אבקות. החלבון גבוה (33 גרם) והסוכר נמוך, אבל המתיקות עדיין מהונדסת מתחליפים, ועם 20 גרם שומן זה גם מהצפופים בקבוצה. האגוזים האמיתיים הם היתרון; הצפיפות הקלורית היא המחיר.

  - MEDIUM T1: «, לא רק אבקות.» — Possible 'X, לא Y' contrastive mid-text — judge whether it reads as a calque.
  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[5]/expansion/comparisonContext
> רוב הקבוצה בונה את החלבון מאבקות בלבד. כאן יש שקדים וקשיו אמיתיים בפנים — היתרון שמבדל אותו. אבל הוא משלם על זה בשומן: 20 גרם ל-100 גרם, מהצפופים בקבוצה, והמתיקות עדיין מתחליפים ולא מהפחתה אמיתית.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[5]/expansion/limitingFactors[0]/text
> המתיקות הנמוכה באה מתחליפים וחומר מילוי, לא מהפחתה אמיתית

  - HIGH T1: «, לא מהפחתה» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[5]/expansion/limitingFactors[1]/text
> 7.4 גרם שומן רווי ל-100 גרם — מהגבוהים בקבוצה

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[5]/expansion/limitingFactors[2]/text
> 406 קלוריות ל-100 גרם — צפיפות קלורית מורגשת

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[6]/insightLine
> מספרים יפים — 32 גרם חלבון, כמעט בלי סוכר ונתרן נמוך — אבל המתיקות באה כולה מתחליפים.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[6]/rowVerdict
> הפרופיל קורא נקי: חלבון גבוה (32 גרם), כמעט בלי סוכר ונתרן נמוך מאוד (100 מ"ג). אבל המתיקות לא הופחתה — היא הוחלפה בתחליפים, והבסיס תערובת חלבונים מבודדים. מצוין כתוסף חלבון נוח; פחות כמזון אמיתי.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[6]/expansion/comparisonContext
> מהנקיים בקבוצה על הנייר — חלבון גבוה, כמעט בלי סוכר ונתרן נמוך. אבל המתיקות לא נחסכה, היא הומרה בתחליפים, והבסיס הוא תערובת מבודדים. תוסף חלבון נוח יותר משהוא חטיף של ממש.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[6]/expansion/limitingFactors[0]/text
> המתיקות באה מתחליפים, לא מהפחתה אמיתית של סוכר

  - HIGH T1: «, לא מהפחתה» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[6]/expansion/limitingFactors[1]/text
> הבסיס תערובת חלבונים מבודדים, לא מזון שלם

  - HIGH T1: «, לא מזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[7]/insightLine
> כמעט תאום לאחיו דלי-הסוכר, אבל עם נתרן גבוה יותר — 272 מ"ג, כמעט פי שלושה משלהם.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[7]/rowVerdict
> אותו מתכון משפחתי — חלבון גבוה (35 גרם), כמעט בלי סוכר, מתיקות מתחליפים — אבל כאן הנתרן קופץ ל-272 מ"ג, גבוה בהרבה מהגרסאות הקרובות לו. החלבון משמעותי, אבל זו גרסה מלוחה יותר של אותו תוסף תעשייתי.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[7]/expansion/comparisonContext
> חולק כמעט הכל עם הגרסאות הקרובות לו במדף — חלבון גבוה, סוכר נמוך מתחליפים. ההבדל המעשי הוא הנתרן: 272 מ"ג כאן, כמעט פי שלושה מהגרסאות דלות-הנתרן באותה משפחה.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[7]/expansion/limitingFactors[0]/text
> 272 מ"ג נתרן ל-100 גרם — גבוה בהרבה מהגרסאות הקרובות לו במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[7]/expansion/limitingFactors[1]/text
> המתיקות מתחליפים והבסיס תערובת מבודדים

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[8]/insightLine
> עוד טעם באותה משפחה — המספרים נקיים (33 גרם חלבון, נתרן נמוך), ההרכב תעשייתי כמו אצל אחיו.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [medium] /products[8]/rowVerdict
> כמעט בלתי-נבדל מאחיו הקרובים: חלבון גבוה (33 גרם), כמעט בלי סוכר ונתרן נמוך (100 מ"ג). ההבדל הוא הטעם, לא ההרכב — אותה מתיקות מתחליפים ואותו בסיס מבודדים. נוח כתוסף חלבון, רחוק ממאכל אמיתי.

  - MEDIUM T1: «, לא ההרכב —» — Possible 'X, לא Y' contrastive mid-text — judge whether it reads as a calque.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[8]/expansion/comparisonContext
> עוד טעם באותה משפחה. המספרים נקיים — חלבון גבוה, סוכר נמוך, נתרן נמוך — אבל מה שמבדל אותו משכניו הקרובים הוא הטעם בלבד, לא ההרכב. אותה מתיקות מתחליפים ואותו בסיס מבודדים.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[8]/expansion/limitingFactors[0]/text
> המתיקות באה מתחליפים, לא מהפחתה אמיתית

  - HIGH T1: «, לא מהפחתה» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[8]/expansion/limitingFactors[1]/text
> הבסיס תערובת חלבונים מבודדים, לא מזון שלם

  - HIGH T1: «, לא מזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[9]/insightLine
> בסיס החלבון תקין — מה שמושך אותו מטה הוא דווקא שכבת הקרמל, שלבדה מוסיפה 8.2 גרם שומן רווי.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[9]/rowVerdict
> החלבון אמיתי וגבוה (33 גרם), אבל מה שמושך אותו מטה הוא דווקא שכבת הקרמל: היא מוסיפה 8.2 גרם שומן רווי, נמוכה בסיבים (4.9 גרם בלבד) ובנויה משומן צמחי וממתיקים. החלבון נושא אותו, השאר ציפוי תעשייתי.

  - F2-signal: hedges=0 verdict_marker=True risk=low

## [clean] /products[9]/expansion/comparisonContext
> ליד אחיו מאותו מותג, אבל החלש שבהם: שכבת הקרמל מוסיפה 8.2 גרם שומן רווי, והסיבים הנמוכים (4.9 גרם) מציבים אותו מתחת לרובם. הסוכר הנמוך, כרגיל בקבוצה, נשען על ממתיקים.

  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[9]/expansion/limitingFactors[0]/text
> 8.2 גרם שומן רווי ל-100 גרם — שכבת הקרמל מכבידה כאן

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[9]/expansion/limitingFactors[1]/text
> 4.9 גרם סיבים בלבד ל-100 גרם — נמוך לקטגוריה

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[9]/expansion/limitingFactors[2]/text
> שכבת הקרמל בנויה מתחליפי מתיקות ושומן צמחי

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[10]/insightLine
> הבסיס מחלבוני חלב אמין — הציפוי המתוק הוא שמכביד, עם 8.5 גרם שומן רווי ושורת תוספים שבונים אותו.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[10]/rowVerdict
> הבסיס דווקא אמין — חלבון גבוה (34 גרם) מחלבוני חלב וסיבים סבירים. מה שמכביד עליו הוא הציפוי המתוק: 8.5 גרם שומן רווי, שומן קוקוס ושורת תוספים שבונים את הקרמל. עובד כתוסף חלבון; פחות מוצלח כנשנוש נקי.

  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[10]/expansion/comparisonContext
> החלבון גבוה כמו שאר הקבוצה, והבסיס סביר. מה שמוריד אותו הוא הציפוי המתוק — שכבת קרמל שמוסיפה שומן רווי גבוה (8.5 גרם) ושורת תוספים, ולא תורמת ערך מעבר לטעם.

  - F2-signal: hedges=1 verdict_marker=False risk=high

## [clean] /products[10]/expansion/limitingFactors[0]/text
> 8.5 גרם שומן רווי ל-100 גרם — מהגבוהים בקבוצה, רובו משכבת הקרמל

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[10]/expansion/limitingFactors[1]/text
> שכבת הקרמל בנויה משומן צמחי ושורת תוספים, לא ממזון

  - HIGH T1: «, לא ממזון» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[11]/insightLine
> החלבון בא מבוטנים אמיתיים — אבל זה גם החטיף הצפוף בקבוצה: 496 קלוריות ל-100 גרם.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [medium] /products[11]/rowVerdict
> כאן החלבון (26 גרם) בא מבוטנים קלויים אמיתיים ולא רק מאבקה, וזה לזכותו. אבל הוא משלם על זה ביוקר: הצפוף ביותר בקבוצה ב-496 קלוריות, עם 29.5 גרם שומן, ובניגוד למשפחה המתוקה-בתחליפים, כאן הסוכר אמיתי וגבוה (16 גרם). מקור חלבון ממאכל ממשי, באריזה קלורית כבדה.

  - MEDIUM T4: «לזכותו» — Calqued metaphor — reads as English figure of speech in Hebrew.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[11]/expansion/comparisonContext
> מציע משהו שרוב הקבוצה לא נותנת — חלבון מבוטנים אמיתיים ולא רק מאבקה. אבל זה גם הצפוף ביותר במדף, 496 קלוריות, והסוכר כאן אמיתי וגבוה ולא הומר בתחליפים. היתרון במקור, החיסרון בצפיפות.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[11]/expansion/limitingFactors[0]/text
> 496 קלוריות ל-100 גרם — הצפוף ביותר במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[11]/expansion/limitingFactors[1]/text
> 29.5 גרם שומן ל-100 גרם — הגבוה במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[11]/expansion/limitingFactors[2]/text
> 16 גרם סוכר ל-100 גרם — סוכר אמיתי, לא תחליף; וגם הנתרן גבוה (354 מ"ג)

  - HIGH T1: «, לא תחליף;» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[12]/insightLine
> כמו אחיו — חלבון מבוטנים אמיתיים, אבל 489 קלוריות ו-17 גרם סוכר אמיתי הופכים אותו לכבד.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [medium] /products[12]/rowVerdict
> אותו עיקרון כמו הגרסה האחרת מהמותג: החלבון (25 גרם) בא מבוטנים קלויים אמיתיים, וזה לזכותו. אבל גם כאן זה אחד הצפופים בקבוצה — 489 קלוריות, 28 גרם שומן ו-17 גרם סוכר אמיתי. מקור חלבון ממאכל ממשי, עטוף בצפיפות קלורית גבוהה.

  - MEDIUM T4: «לזכותו» — Calqued metaphor — reads as English figure of speech in Hebrew.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[12]/expansion/comparisonContext
> החלבון נשען על בוטנים אמיתיים יותר מרוב הקבוצה. אבל הצפיפות הקלורית הגבוהה והסוכר האמיתי (לא תחליף) מציבים אותו נמוך, לצד הגרסה הקרובה לו מאותו מותג.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[12]/expansion/limitingFactors[0]/text
> 489 קלוריות ו-28.3 גרם שומן ל-100 גרם — מהצפופים בקבוצה

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[12]/expansion/limitingFactors[1]/text
> 17.2 גרם סוכר ל-100 גרם — סוכר אמיתי וגבוה לחטיף חלבון

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[12]/expansion/limitingFactors[2]/text
> 375 מ"ג נתרן ל-100 גרם

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[13]/insightLine
> בזמן שכל הקבוצה מורידה סוכר בתחליפים, כאן 31 גרם סוכר אמיתי — רמת לוח שוקולד שמוכר את עצמו על החלבון.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[13]/rowVerdict
> כדאי לקרוא לזה כמו שזה: בעוד רוב הקבוצה מורידה סוכר בכל דרך, כאן יש 31 גרם סוכר אמיתי, כמעט כמו בלוח שוקולד, עם 11 גרם שומן רווי — מהגבוהים במדף. החלבון אמנם גבוה, אבל המבנה כאן הוא של ממתק, לא של חטיף חלבון.

  - HIGH T1: «, לא של» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[13]/expansion/comparisonContext
> נמכר כחטיף חלבון, אבל יושב בקצה הסוכרי של הקבוצה: בעוד שכניו ממותקים בתחליפים, כאן 31 גרם סוכר אמיתי ו-11 גרם שומן רווי — קרוב יותר לממתק שוקולד מאשר לחטיף חלבון.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[13]/expansion/limitingFactors[0]/text
> 31 גרם סוכר ל-100 גרם — סוכר אמיתי ברמה של ממתק שוקולד, לא תחליף

  - HIGH T1: «, לא תחליף» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[13]/expansion/limitingFactors[1]/text
> 11 גרם שומן רווי ל-100 גרם — מהגבוהים במדף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[13]/expansion/limitingFactors[2]/text
> 465 קלוריות ל-100 גרם — צפוף

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[14]/insightLine
> נמכר על החלבון, אבל הוא גם הכי מתוק וגם הכי מלוח במדף בו-זמנית (35 גרם סוכר, 396 מ"ג נתרן) — מבנה של ממתק.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[14]/rowVerdict
> החלבון אמנם גבוה (34 גרם), אבל זה מעט מאוד מול שאר הפרופיל: 35 גרם סוכר ו-396 מ"ג נתרן — שניהם מהגבוהים במדף — בלי טיפת סיבים. שוקולד חלב וקרם נוגט מלוח הם הסיפור האמיתי כאן. ממתק שעוטף את עצמו בטענת חלבון.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[14]/expansion/comparisonContext
> בתחתית הקבוצה, ובמקום נדיר: גם הכי מתוק וגם כמעט הכי מלוח במדף בו-זמנית. בעוד שכניו מורידים סוכר בתחליפים, כאן 35 גרם סוכר אמיתי לצד 396 מ"ג נתרן — מבנה של ממתק, לא של חטיף חלבון.

  - HIGH T1: «, לא של» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[14]/expansion/limitingFactors[0]/text
> 35 גרם סוכר ל-100 גרם — הגבוה בקבוצה, סוכר אמיתי

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[14]/expansion/limitingFactors[1]/text
> 396 מ"ג נתרן ל-100 גרם — הגבוה בקבוצה

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[14]/expansion/limitingFactors[2]/text
> 9 גרם שומן רווי ל-100 גרם, בלי טיפת סיבים

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [HIGH-BLOCK] /products[15]/insightLine
> זו קונפקציית שוקולד שהוסיפו לה חלבון, לא חטיף חלבון — 27 גרם סוכר ואפס סיבים מסגירים את זה.

  - HIGH T1: «, לא חטיף» — Contrastive 'X, לא Y' closer (calque). Resolve with 'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on a bare 'X, לא Y'.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [medium] /products[15]/rowVerdict
> החלבון גבוה (34 גרם), אבל הוא הדבר היחיד שמזכיר כאן חטיף חלבון. כל השאר שוקולד וממתק: 27 גרם סוכר, 24 גרם שומן, 465 קלוריות ובלי טיפת סיבים. קונפקציית שוקולד שמוסיפה חלבון, לא חטיף חלבון. תחתית הקבוצה, ובצדק.

  - MEDIUM T1: «, לא חטיף חלבון.» — Possible 'X, לא Y' contrastive mid-text — judge whether it reads as a calque.
  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[15]/expansion/comparisonContext
> החלבון גבוה, אבל הוא כמעט הדבר היחיד שמבדיל את זה מקונפקציית שוקולד רגילה: 27 גרם סוכר ברמת ממתק, צפיפות קלורית גבוהה ובלי טיפת סיבים. תחתית הקבוצה.

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[15]/expansion/limitingFactors[0]/text
> 27 גרם סוכר ל-100 גרם — ברמה של ממתק שוקולד

  - F2-signal: hedges=0 verdict_marker=False risk=medium

## [clean] /products[15]/expansion/limitingFactors[1]/text
> 24 גרם שומן ו-465 קלוריות ל-100 גרם, בלי טיפת סיבים

  - F2-signal: hedges=0 verdict_marker=False risk=medium

---
SUMMARY: 18 HIGH-block · 6 medium-only · 66 clean (of 90 strings)
