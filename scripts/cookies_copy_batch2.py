import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

copy_data = {

"ck-7290119040568": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגת קראנץ אגוזים — סוכר 30 גרם ושומן רווי 8 גרם, שמנים מוקשים.",
    "rowVerdict": "עוגת קראנץ אגוזים מגיעה ל-E. 30 גרם סוכר ל-100 גרם, שומן רווי גבוה ורשימת תוספים ארוכה הכוללת E422, E481, E300, E551, E202, E282, E1414, E471, E322, E415 — כולם יחד מסמנים מוצר שאינו קראנץ אגוזים ביתי בשום פנים.",
    "bottomLine": "רשימת תוספים ארוכה מאוד ושמנים מוקשים — מאפה תעשייתי.",
    "consumerTakeaway": "30 גרם סוכר ל-100 גרם ויותר מעשרה תוספים — E.",
    "consumerExplanation": "האגוזים מופיעים ברשימה, אבל מוקפים בסירופ גלוקוז, E422, E481, E202, E282, שמנים מוקשים ועוד. המוצר מתוייג _category_routed=snack_bar_granola — מסמן שאינו ביסקוויט פשוט.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "מעל עשרה תוספים ברשימה כולל חומרי שימור E202 ו-E282, חומר הלחה E422, מייצב E415, ועמילן מטופל E1414. שמנים מוקשים כמקור שומן."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם — גבוה מאוד. סירופ גלוקוז ברשימה מוסיף לעומס."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E422, E481, E300, E551, E202, E282, E1414, E471, E322, E415 — רשימת תוספים חריגה באורכה גם לפי תקני הקטגוריה."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 8 גרם ל-100 גרם עם סוכר גבוה — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["אין שימוש יומי מומלץ — מנת טעימה חד-פעמית"]
},

"ck-7290118423904": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קרמוגית קראנץ שוקו וניל — 45% קרם וניל עם שברי עוגיות.",
    "rowVerdict": "קרמוגית קראנץ שוקו וניל מגיעה ל-E. 45% מהמוצר הוא קרם וניל מעובד שמכיל E503, E500 ולציטין סויה. אבקת קקאו 4.5% מצדיקה 'שוקו' בשם, אבל הפרופיל הכולל הוא E — שמנים צמחיים, E450, E500, E471.",
    "bottomLine": "כמעט מחצית מהמוצר הוא קרם תעשייתי — לא ביסקוויט.",
    "consumerTakeaway": "45% קרם תעשייתי מעובד עם עוגיות — שוקו וניל כתיוג בלבד.",
    "consumerExplanation": "45% קרם וניל שמכיל E503, E500, לציטין סויה, שמנים צמחיים, E450 ו-E471 — זה לא קרם ביתי. הציון ל-E נגזר מהשילוב של כמות הסוכר בנתון ליחידה (6.3 גרם) ועיבוד גבוה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "45% קרם תעשייתי עם E503, E500, E450, E471, לציטין סויה. הרכיב הראשי הוא מוצר מעובד בתוך מוצר מעובד."},
        {"dimension": "glycemic_quality", "score": 35, "label_he": "עומס גליקמי", "explanation_he": "נתוני הסוכר ליחידה (6.3 גרם) לא מתורגמים ל-100 גרם — הפרופיל הגליקמי האמיתי לא אומת."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "E503, E500, E450, E471, לציטין סויה — חמישה תוספים בקרם בלבד, ועוד בחלק הביסקוויט."},
        {"dimension": "calorie_density", "score": 38, "label_he": "צפיפות קלורית", "explanation_he": "94 קק\"ל ליחידה מסמן מוצר עשיר. שמנים צמחיים בקרם ובביסקוויט."}
    ],
    "bestUseCases": ["כיבוד ילדים במנה אחת"]
},

"ck-7290118422617": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קרמוגית קראנץ קרם וניל — מבנה זהה לגרסת השוקו, ללא קקאו.",
    "rowVerdict": "קרמוגית קראנץ קרם וניל מגיעה ל-E. המבנה זהה לגרסת השוקו וניל — 45% קרם תעשייתי, E450, E500, E471, שמנים צמחיים — בלי אבקת הקקאו. הציון E נגזר מאותם גורמים.",
    "bottomLine": "זהה לגרסת השוקו ללא קקאו — E מאותן סיבות.",
    "consumerTakeaway": "גרסת וניל טהור של קרמוגית — פרופיל תעשייתי מלא.",
    "consumerExplanation": "ללא קקאו, הגרסה הזו מציעה וניל בלבד מעל אותו קרם תעשייתי. 45% קרם עם E450, E471, E500 ולציטין — הפרופיל זהה לגרסת השוקו וניל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "45% קרם תעשייתי. E450, E471, E500, לציטין — זהה לגרסת השוקו."},
        {"dimension": "glycemic_quality", "score": 35, "label_he": "עומס גליקמי", "explanation_he": "נתוני הסוכר ליחידה (6.0 גרם) לא מתורגמים ל-100 גרם. הפרופיל הגליקמי לא אומת במלואו."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "E450, E471, E500, לציטין — זהה לגרסת השוקו וניל."},
        {"dimension": "calorie_density", "score": 38, "label_he": "צפיפות קלורית", "explanation_he": "94 קק\"ל ליחידה עם שמנים צמחיים — זהה לגרסת השוקו."}
    ],
    "bestUseCases": ["כיבוד ילדים במנה אחת"]
},

"ck-7290019293804": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "33% ציפוי שוקולד לבן — סוכר 33 גרם ושומן רווי 16 גרם ל-100 גרם.",
    "rowVerdict": "קראנץ אגוזי לוז מגיע ל-E עם 33 גרם סוכר ו-16 גרם שומן רווי ל-100 גרם — שניהם גבוהים מאוד. הציפוי בשוקולד לבן (33%) הוא מקור השומן הרווי העיקרי. E476 בציפוי הוא פוליגליצרול — תוסף שנוי-במחלוקת.",
    "bottomLine": "שוקולד לבן כציפוי עיקרי — סוכר ושומן רווי גבוהים מאוד.",
    "consumerTakeaway": "33% ציפוי שוקולד לבן הוא הגורם לסוכר ושומן רווי גבוהים.",
    "consumerExplanation": "14.5% ממרח אגוזי לוז אמיתי הוא יתרון. אבל 33% שוקולד לבן (סוכר כרכיב ראשוני), 16 גרם שומן רווי ו-E476 בציפוי הופכים את הפרופיל ל-E ברור.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "ציפוי שוקולד לבן עם E476, שומן צמחי, E471, גואר גאם — מוצר מרובד בתוספים. ממרח אגוזי לוז 14.5% לא מציל."},
        {"dimension": "glycemic_quality", "score": 20, "label_he": "עומס גליקמי", "explanation_he": "33 גרם סוכר ל-100 גרם — גבוה מאוד. שוקולד לבן מורכב בעיקרו מסוכר ולחמאת קקאו."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E476 (פוליגליצרול) בציפוי — תוסף שנוי-במחלוקת. E471 וגואר גאם מוסיפים."},
        {"dimension": "calorie_density", "score": 25, "label_he": "צפיפות קלורית", "explanation_he": "16 גרם שומן רווי ל-100 גרם — גבוה מאוד לכל קנה מידה."}
    ],
    "bestUseCases": ["מנת ממתק בודדת לעיתים נדירות"]
},

"ck-7296073453840": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קוקיס שוקולד חלבי עם חמאה ומרגרינה — שומן רווי 13.6 גרם.",
    "rowVerdict": "קוקיס שוקולד חלבי מגיע ל-E. 13.6 גרם שומן רווי ל-100 גרם ושוקולד חלב 19.3% — שניהם תורמים לצפיפות הקלורית הגבוהה. חמאה ומרגרינה יחד ברשימה — שני מקורות שומן שונים, כולל E200 ו-E202 כחומרי שימור במרגרינה.",
    "bottomLine": "חמאה ומרגרינה יחד — שומן רווי גבוה מאוד.",
    "consumerTakeaway": "חמאה ומרגרינה יחד ברשימה, שוקולד חלב 19.3%, שומן רווי 13.6 גרם.",
    "consumerExplanation": "חמאה ומרגרינה יחד ברשימה — השילוב מגביר את השומן הרווי מעבר למה שכל אחד מהם לבד היה מייצר. E200 ו-E202 כחומרי שימור במרגרינה, נתרן 330 מ\"ג לצד שומן גבוה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה עם E200, E202 לצד חמאה. ביצים מיובשות במקום ביצים טריות. E500 ו-E470 בחומרי תפיחה."},
        {"dimension": "glycemic_quality", "score": 35, "label_he": "עומס גליקמי", "explanation_he": "נתון הסוכר לא אומת מנתון ל-100 גרם. סוכרים ברשימה — גורם מגביל."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E200, E202 במרגרינה, E500, E470 — ריבוי תוספים לקוקיס."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "13.6 גרם שומן רווי ל-100 גרם — גבוה מאוד. שוקולד חלב 19.3% מוסיף."}
    ],
    "bestUseCases": ["כיבוד נדיר — לא לצריכה שגרתית"]
},

"ck-7290106571945": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "פיטנס קקאו דגנים מלאים — 41% קמח מלא, סוכר 21 גרם.",
    "rowVerdict": "עוגיות קקאו דגנים מלאים פיטנס מגיעות ל-E. 41% קמח מלא ו-4.5% שיבולת שועל מלאים הם יתרון אמיתי, אבל 21 גרם סוכר ל-100 גרם חוצה את הסף. מלטודקסטרין, E503, E450, E500 ולציטין סויה משלימים את הפרופיל התעשייתי.",
    "bottomLine": "דגנים מלאים אמיתיים — סוכר גבוה ומלטודקסטרין ביחד.",
    "consumerTakeaway": "41% קמח מלא עם סוכר 21 גרם ומלטודקסטרין — E.",
    "consumerExplanation": "הדגנים המלאים (41%) הם אמיתיים. אבל 21 גרם סוכר ל-100 גרם, מלטודקסטרין (פחמימה פשוטה מעובדת) ושלושה חומרי תפיחה כימיים הופכים את הפרופיל ל-E — למרות התיוג הבריאותי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 35, "label_he": "איכות עיבוד", "explanation_he": "41% קמח מלא ו-8.5% שוקולד מריר הם יתרון. מלטודקסטרין, E503, E450, E500 מורידים."},
        {"dimension": "glycemic_quality", "score": 30, "label_he": "עומס גליקמי", "explanation_he": "21 גרם סוכר ל-100 גרם — גבוה. מלטודקסטרין מוסיף לעומס הגליקמי למרות שאינו 'סוכר'."},
        {"dimension": "additive_quality", "score": 32, "label_he": "תוספים", "explanation_he": "מלטודקסטרין, E503, E450, E500, לציטין סויה — חמישה תוספים בפרופיל שמציג את עצמו כבריאותי."},
        {"dimension": "calorie_density", "score": 42, "label_he": "צפיפות קלורית", "explanation_he": "שמן צמחי ושוקולד 8.5% — צפיפות קלורית בינונית לגבוהה."}
    ],
    "bestUseCases": ["חטיף לארוחת עשר בכמות קטנה"]
},

"ck-7296073453857": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קוקיס שוקולד לבן עם מרגרינה — שומן רווי 10 גרם.",
    "rowVerdict": "קוקיס שוקולד לבן מגיע ל-E. שוקולד לבן 19.9% לצד מרגרינה עם E202 ו-E200 — שילוב של שני מקורות שומן תעשייתיים. נתון הסוכר לא אומת ל-100 גרם. שומן רווי של 10 גרם מסמן E ברור.",
    "bottomLine": "שוקולד לבן ומרגרינה יחד — שומן רווי גבוה.",
    "consumerTakeaway": "שוקולד לבן 19.9% ומרגרינה — שני מקורות שומן תעשייתיים.",
    "consumerExplanation": "שוקולד לבן (מורכב בעיקר מסוכר וחמאת קקאו) ומרגרינה עם חומרי שימור E202, E200 — שני המקורות הראשיים לשומן הרווי של 10 גרם ל-100 גרם. ביצים מיובשות, E500, E470.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה עם E202, E200, ביצים מיובשות, E500, E470. שוקולד לבן 19.9% — רכיב עשיר בסוכר ושומן."},
        {"dimension": "glycemic_quality", "score": 30, "label_he": "עומס גליקמי", "explanation_he": "נתון הסוכר לא אומת ל-100 גרם. שוקולד לבן ו'סוכרים' ברשימה מסמנים עומס גליקמי גבוה."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E202, E200 במרגרינה, E500, E470 — ריבוי תוספים."},
        {"dimension": "calorie_density", "score": 22, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 10 גרם ל-100 גרם — גבוה מאוד לקוקיס."}
    ],
    "bestUseCases": ["מנת ממתק חד-פעמית"]
},

"ck-8410376037784": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות סנדוויץ שוקולד גולון — ממתיק מלטיטול E965 ושמן דקל.",
    "rowVerdict": "עוגיות סנדוויץ שוקולד של גולון מגיעות ל-E. E965 (מלטיטול) כממתיק עיקרי, שמן דקל כמקור שומן, קקאו 12% בקרם — פרופיל תעשייתי מלא. 6 גרם שומן רווי ל-100 גרם וזיגוג חלב מוסיפים לצפיפות הקלורית.",
    "bottomLine": "מלטיטול ושמן דקל — E גם ללא סוכר רגיל.",
    "consumerTakeaway": "E965 במקום סוכר, שמן דקל, זיגוג חלב — E.",
    "consumerExplanation": "E965 (מלטיטול) הוא ממתיק אלכוהול-סוכר עם אינדקס גליקמי נמוך יותר מסוכר, אבל עלול לגרום לתופעות עיכול. שמן דקל כמקור שומן ראשי, קקאו 12% בקרם, E322 ולציטין.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל כרכיב שלישי, E965, E322, זיגוג חלב — מוצר מרובד עם תוספים."},
        {"dimension": "glycemic_quality", "score": 42, "label_he": "עומס גליקמי", "explanation_he": "E965 (מלטיטול) מספק אינדקס גליקמי נמוך יחסית — אבל 5 גרם סוכר ליחידה לא תורגמו ל-100 גרם."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E965, E322, E500, E503 — ריבוי תוספים. מלטיטול עלול לגרום לאי-נוחות עיכולית."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "שמן דקל ושומן רווי 6 גרם — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["סוכרתיים שמחפשים ביסקוויט ממותק חלשה ביחידה אחת"]
},

"ck-7290019816034": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מאגדת מיני קראנץ — 33% ציפוי שוקולד לבן, סוכר 30.3 גרם.",
    "rowVerdict": "מאגדת מיני קראנץ עוגיות מגיעה ל-E. 33% ציפוי שוקולד לבן עם E476, 30.3 גרם סוכר ו-14 גרם שומן רווי ל-100 גרם — שמן קוקוס כמקור השומן הרווי העיקרי, ולא חמאת קקאו. E476 הוא פוליגליצרול.",
    "bottomLine": "שוקולד לבן עם E476 ושמן קוקוס — 30 גרם סוכר ל-100 גרם.",
    "consumerTakeaway": "33% שוקולד לבן עם E476, 14 גרם שומן רווי, 30.3 גרם סוכר.",
    "consumerExplanation": "שוקולד לבן (33%) עם E476 כמייצב הוא הרכיב הדומיננטי. שמן קוקוס בתוך המוצר מסביר את 14 גרם השומן הרווי ל-100 גרם. E471 וגואר גאם משלימים.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "ציפוי שוקולד לבן עם E476, שומן צמחי, E471, גואר גאם — מוצר מעובד מרובד."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "30.3 גרם סוכר ל-100 גרם — גבוה מאוד. שוקולד לבן מורכב בעיקרו מסוכר."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E476 בציפוי, E471, גואר גאם — שלושה תוספים עיקריים."},
        {"dimension": "calorie_density", "score": 25, "label_he": "צפיפות קלורית", "explanation_he": "14 גרם שומן רווי ל-100 גרם — גבוה מאוד. שמן קוקוס כמקור עיקרי."}
    ],
    "bestUseCases": ["מנת ממתק בודדת לעיתים נדירות"]
},

"ck-7290118426615": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "56% קמח מלא עם סוכר 22 גרם — שוקולד מריר 8%.",
    "rowVerdict": "עוגיות מיני שוקולד מגיעות ל-E. 56% קמח מלא הוא יתרון נדיר בקטגוריה — אבל 22 גרם סוכר ל-100 גרם חוצה את הסף. מלטודקסטרין, E503, E500, E450 ולציטין סויה מסמנים עיבוד תעשייתי למרות הפרופיל החלקי הטוב.",
    "bottomLine": "56% קמח מלא נגד 22 גרם סוכר ומלטודקסטרין — E.",
    "consumerTakeaway": "קמח מלא 56% לא מפצה על סוכר גבוה ומלטודקסטרין.",
    "consumerExplanation": "56% קמח מלא כרכיב ראשון הוא אמיתי. 22 גרם סוכר ל-100 גרם ומלטודקסטרין (פחמימה מהירה) יחד מבטלים את יתרון הדגנים. E503, E500, E450 מסמנים ייצור מסיבי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 38, "label_he": "איכות עיבוד", "explanation_he": "56% קמח מלא, שיבולת שועל 2.5% ושוקולד מריר 8% — בסיס טוב. מלטודקסטרין ושלושה חומרי תפיחה מורידים."},
        {"dimension": "glycemic_quality", "score": 28, "label_he": "עומס גליקמי", "explanation_he": "22 גרם סוכר ל-100 גרם. מלטודקסטרין מוסיף עומס גליקמי שלא מסווג כ'סוכר'."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "מלטודקסטרין, E503, E500, E450, לציטין — חמישה תוספים."},
        {"dimension": "calorie_density", "score": 38, "label_he": "צפיפות קלורית", "explanation_he": "שמן צמחי ושוקולד 8% — צפיפות קלורית בינונית."}
    ],
    "bestUseCases": ["כיבוד שבועי בכמות מינימלית"]
},

"ck-7290106571921": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "פיטנס חמוציות — 55% קמח מלא עם סוכר 22.4 גרם.",
    "rowVerdict": "עוגיות פיטנס חמוציות מגיעות ל-E. 55% קמח מלא אמיתי, אבל 22.4 גרם סוכר ל-100 גרם חוצה את הסף. חמוציות 6.5% אמיתיות לצד מלטודקסטרין, E503, E450, E500 ולציטין סויה — אותו מבנה כמו גרסת הקקאו.",
    "bottomLine": "קמח מלא 55% וחמוציות אמיתיות — אבל סוכר גבוה ומלטודקסטרין.",
    "consumerTakeaway": "55% קמח מלא וחמוציות 6.5%, אבל 22.4 גרם סוכר ומלטודקסטרין.",
    "consumerExplanation": "55% קמח מלא, שיבולת שועל 2.5% וחמוציות 6.5% — רכיבים אמיתיים. אבל מלטודקסטרין וסוכר גבוה (22.4 גרם) מבטלים חלק גדול מהיתרון. E503, E450, E500 — ייצור מסיבי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 38, "label_he": "איכות עיבוד", "explanation_he": "55% קמח מלא, שיבולת שועל, חמוציות 6.5% — בסיס טוב. מלטודקסטרין ושלושה חומרי תפיחה."},
        {"dimension": "glycemic_quality", "score": 27, "label_he": "עומס גליקמי", "explanation_he": "22.4 גרם סוכר ל-100 גרם — גבוה. מלטודקסטרין מוסיף עומס גליקמי נסתר."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "מלטודקסטרין, E503, E450, E500, לציטין — אותם תוספים כמו גרסת הקקאו."},
        {"dimension": "calorie_density", "score": 38, "label_he": "צפיפות קלורית", "explanation_he": "שמנים צמחיים ושומן רווי 4 גרם — בינוני לגבוה."}
    ],
    "bestUseCases": ["חטיף עם קפה בכמות קטנה"]
},

}

count = 0
for pid, copy in copy_data.items():
    for p in data['products']:
        if p['id'] == pid:
            p['confidence_label_he'] = copy['cl']
            p['confidence_tooltip_he'] = copy['ct']
            p['confidence_sub_reason'] = copy['cs']
            p['expansion']['confidenceLabel'] = copy['cl']
            p['insightLine'] = copy['insightLine']
            p['rowVerdict'] = copy['rowVerdict']
            p['expansion']['bottomLine'] = copy['bottomLine']
            p['consumerTakeaway'] = copy['consumerTakeaway']
            p['consumerExplanation'] = copy['consumerExplanation']
            p['bariInterpretation'] = copy['bariInterpretation']
            p['bestUseCases'] = copy['bestUseCases']
            count += 1
            break

remaining = sum(1 for p in data['products'] if p.get('rowVerdict') == 'PENDING_COPY')
print(f"Updated: {count}, Remaining PENDING: {remaining}")

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved batch 2.")
