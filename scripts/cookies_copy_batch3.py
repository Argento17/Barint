import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

copy_data = {

"ck-7290119040612": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגת קראנץ קינמון — שמנים מוקשים, 30 גרם סוכר.",
    "rowVerdict": "עוגת קראנץ קינמון מגיעה ל-E. המבנה זהה לגרסת האגוזים — שמנים מוקשים, מרגרינה, סוכר 30 גרם, שומן רווי 8 גרם ורשימת תוספים ארוכה הכוללת E422, E481, E202, E282, E1414, E471. הקינמון הוא ניחוח, לא מרכיב שמשנה את הפרופיל.",
    "bottomLine": "מבנה זהה לגרסת האגוזים — E מאותן סיבות.",
    "consumerTakeaway": "קינמון לא משנה את הפרופיל — שמנים מוקשים ותוספים מרובים.",
    "consumerExplanation": "גרסת הקינמון של קראנץ שופרסל חולקת בדיוק את אותה נוסחת בסיס: מרגרינה, שמנים מוקשים, 30 גרם סוכר ל-100 גרם ויותר מעשרה תוספים. הקינמון אינו משנה את הפרופיל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה, שמנים מוקשים, E422, E481, E202, E282, E1414, E471, E322, E415 — פרופיל תעשייתי מובהק."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם — גבוה מאוד. סירופ גלוקוז ברשימה."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E422, E481, E202, E282, E1414, E471, E322, E415 — רשימה ארוכה במיוחד."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 8 גרם וסוכר גבוה — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["מנת טעימה חד-פעמית"]
},

"ck-7290119040513": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגת קראנץ שוקולד — מרגרינה, שמנים מוקשים, 30 גרם סוכר.",
    "rowVerdict": "עוגת קראנץ שוקולד מגיעה ל-E. אותה נוסחת קראנץ שופרסל — מרגרינה, שמנים מוקשים, 30 גרם סוכר, שומן רווי 8 גרם, ורשימת תוספים ארוכה. השוקולד הוא ניחוח, לא מרכיב שמשנה את הפרופיל.",
    "bottomLine": "אותה נוסחה כמו גרסות הקינמון והאגוזים — E.",
    "consumerTakeaway": "שוקולד לא משנה את הנוסחה הבסיסית — שמנים מוקשים ותוספים.",
    "consumerExplanation": "גרסת השוקולד של קראנץ שופרסל חולקת בדיוק אותה נוסחה: מרגרינה, שמנים מוקשים, 30 גרם סוכר ל-100 גרם ויותר מעשרה תוספים.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה, שמנים מוקשים, E422, E481, E202, E282, E1414, E471, E322, E415 — זהה לגרסות האחרות."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם. זהה לגרסות הקינמון והאגוזים."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E422, E481, E202, E282, E1414, E471, E322, E415 — רשימה ארוכה."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 8 גרם — זהה לגרסות האחרות."}
    ],
    "bestUseCases": ["מנת טעימה חד-פעמית"]
},

"ck-7290119040667": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגת קראנץ פרג — מרגרינה, שמנים מוקשים, 30 גרם סוכר.",
    "rowVerdict": "עוגת קראנץ פרג מגיעה ל-E. גרסה נוספת מאותה סדרת קראנץ שופרסל — מרגרינה, שמנים מוקשים, 30 גרם סוכר ל-100 גרם, שומן רווי 8 גרם, ויותר מעשרה תוספים. הפרג הוא ניחוח ומרקם, לא שינוי פרופיל.",
    "bottomLine": "גרסת הפרג של אותה נוסחה — E מאותן סיבות.",
    "consumerTakeaway": "פרג לא משנה את הנוסחה — שמנים מוקשים ותוספים מרובים.",
    "consumerExplanation": "גרסת הפרג חולקת בדיוק את אותה נוסחת בסיס כמו גרסות הקינמון, השוקולד והאגוזים. הפרג מוסיף מרקם, לא יתרון תזונתי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה, שמנים מוקשים, E422, E481, E202, E282, E1414, E471 — זהה לכל הגרסות."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם — זהה לגרסות האחרות."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E422, E481, E202, E282, E1414, E471 — רשימה ארוכה, זהה לגרסות האחרות."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 8 גרם — זהה."}
    ],
    "bestUseCases": ["מנת טעימה חד-פעמית"]
},

"ck-8410376075915": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות ללא גלוטן עם שוקולד — שמן חמנייה 14%, סוכר 19 גרם.",
    "rowVerdict": "עוגיות שבבי שוקולד ללא גלוטן מגיעות ל-E. שמן חמנייה 14% כמקור שומן ראשי הוא בחירה סבירה יחסית, אבל 19 גרם סוכר ל-100 גרם וקמח אורז וקמח תירס כבסיס מסמנים עיבוד גבוה. 'ללא גלוטן' הוא הסרת רכיב, לא שיפור פרופיל.",
    "bottomLine": "ללא גלוטן עם שמן חמנייה — סוכר גבוה ועיבוד גבוה.",
    "consumerTakeaway": "ללא גלוטן לא מסמל פרופיל בריא — 19 גרם סוכר ועיבוד גבוה.",
    "consumerExplanation": "קמח אורז, קמח תירס ושמן חמנייה 14% — בסיס טוב יחסית ל'ללא גלוטן'. אבל 19 גרם סוכר ל-100 גרם, קקאו 3% (נמוך) ו-E500, E503 מסמנים E. שבבי שוקולד 22% כוללים חמאת קקאו — יתרון קטן.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 32, "label_he": "איכות עיבוד", "explanation_he": "קמח אורז, קמח תירס, שמן חמנייה — בסיס נסבל. אוליגופרוקטוז, E500, E503 ולציטין מסמנים עיבוד תעשייתי."},
        {"dimension": "glycemic_quality", "score": 30, "label_he": "עומס גליקמי", "explanation_he": "19 גרם סוכר ל-100 גרם. קמח אורז ותירס הם פחמימות זמינות — עומס גליקמי גבוה."},
        {"dimension": "additive_quality", "score": 35, "label_he": "תוספים", "explanation_he": "אוליגופרוקטוז (פרה-ביוטי — פלוס קטן), E500, E503, לציטין — בינוני."},
        {"dimension": "calorie_density", "score": 38, "label_he": "צפיפות קלורית", "explanation_he": "שמן חמנייה 14% ושבבי שוקולד 22% — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["צליאקים שמחפשים חטיף מתוק", "אחד בשבוע כעוגיית שוקולד"]
},

"ck-7290019870470": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות סנדוויץ שוקו צ'וקטה — שמן דקל, סוכר 29 גרם, קקאו 3.5%.",
    "rowVerdict": "עוגיות סנדוויץ שוקו צ'וקטה מגיעות ל-E. שומן צמחי דקלים כרכיב שלישי, 29 גרם סוכר ו-8.6 גרם שומן רווי ל-100 גרם. קקאו 3.5% בלבד — לא מספיק כדי לצדיק 'שוקו' במלוא המשמעות.",
    "bottomLine": "שמן דקל, סוכר 29 גרם, קקאו 3.5% בלבד — E.",
    "consumerTakeaway": "שמן דקל כרכיב שלישי, סוכר גבוה, קקאו מינימלי.",
    "consumerExplanation": "שומן צמחי דקלים כרכיב שלישי מסביר את 8.6 גרם השומן הרווי. 29 גרם סוכר ל-100 גרם וקקאו 3.5% — הפרופיל של ממתק, לא של עוגיית שוקולד עם ערך.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "שומן דקל כרכיב שלישי, עמילן חיטה, מלטודקסטרין, קרמל כצבע מאכל, לציטין חמניות."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "29 גרם סוכר ל-100 גרם — גבוה מאוד. עמילן חיטה ומלטודקסטרין מוסיפים."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "קרמל כצבע מאכל, מלטודקסטרין, לציטין חמניות, מתפיחים — בינוני."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "שמן דקל ושומן רווי 8.6 גרם — צפיפות גבוהה."}
    ],
    "bestUseCases": ["כיבוד שגרתי בכמות קטנה"]
},

"ck-4823077633317": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "LOVITA שוקולד — סוכר 35.8 גרם ושמן דקל גם בשבבים.",
    "rowVerdict": "LOVITA שוקולד מגיעה ל-E עם 35.8 גרם סוכר ו-14.2 גרם שומן רווי ל-100 גרם. שמן דקל ושמן זרעי דקל נמצאים בשבבי השוקולד עצמם — לא רק בבסיס. E503, E500 ולציטין סויה משלימים.",
    "bottomLine": "שמן דקל גם בשבבי השוקולד — 35.8 גרם סוכר ו-14 גרם שומן רווי.",
    "consumerTakeaway": "שמן דקל בשבבים ובבסיס, סוכר 35.8 גרם, שומן רווי 14.2 גרם.",
    "consumerExplanation": "שבבי שוקולד עם שמן דקל ושמן זרעי דקל הם מה שמסביר את 14.2 גרם השומן הרווי. 35.8 גרם סוכר ל-100 גרם — גבוה מאוד. נוזל ביצים ואבקת חלב — נגיעה בסיס טובה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל ושמן זרעי דקל בשבבי השוקולד, E503, E500, לציטין סויה. ריבוי מקורות שומן עם עיבוד גבוה."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "35.8 גרם סוכר ל-100 גרם — גבוה מאוד. שוקולד בצד הנמוך של מוצקי הקקאו."},
        {"dimension": "additive_quality", "score": 32, "label_he": "תוספים", "explanation_he": "E503, E500, דיסודיום דיפוספט, לציטין סויה — בינוני לגבוה."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "14.2 גרם שומן רווי — גבוה מאוד. שמן דקל הוא שומן רווי ביחס גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290017724171": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "אקלר סנדוויץ ריבה ללא סוכר הללס — מרגרינה ומילוי עם עשרה תוספים.",
    "rowVerdict": "אקלר סנדוויץ ריבה ללא סוכר הללס מגיע ל-E. הסרת הסוכר הוחלפה במלטיטול, סורביטול, E440, E330, E124, E150d, E202, E341, E450 — עשרה תוספים במילוי הריבה בלבד. מרגרינה בבסיס. 6.2 גרם שומן רווי ל-100 גרם.",
    "bottomLine": "עשרה תוספים במילוי הריבה בלבד — מרגרינה בבסיס.",
    "consumerTakeaway": "ריבה ללא סוכר עם עשרה תוספים; מרגרינה בבצק.",
    "consumerExplanation": "מלטיטול וסורביטול כממתיקים, E440 (פקטין), E330, E124 (צבע אדום), E150d, E202, E341, E450 — כל אלה במילוי הריבה בלבד. בצק עם מרגרינה ושומן רווי 6.2 גרם ל-100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 18, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה בבצק, יותר מעשרה תוספים במילוי הריבה — רמת עיבוד חריגה גם לפי תקני הקטגוריה."},
        {"dimension": "glycemic_quality", "score": 48, "label_he": "עומס גליקמי", "explanation_he": "1.2 גרם סוכר — נמוך. מלטיטול וסורביטול עם אינדקס גליקמי נמוך יחסית, אך עלולים לגרום לאי-נוחות עיכולית."},
        {"dimension": "additive_quality", "score": 12, "label_he": "תוספים", "explanation_he": "E440, E330, E124, E150d, E202, E341, E450, מלטיטול, סורביטול, לציטין — רשימה ארוכה במיוחד."},
        {"dimension": "calorie_density", "score": 32, "label_he": "צפיפות קלורית", "explanation_he": "מרגרינה ושומן רווי 6.2 גרם — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["סוכרתיים שצריכים ממתיק חלש — יחידה אחת בלבד"]
},

"ck-4006529002170": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "גולד רינג — 541 קק\"ל ל-100 גרם, שמן דקל, סוכר 23 גרם.",
    "rowVerdict": "עוגיות גולד רינג מגיעות ל-E עם 541 קק\"ל ל-100 גרם — הצפיפות הקלורית הגבוהה ביותר בין המוצרים שנסקרו. שמן דקל כרכיב שני, שומן רווי 15 גרם ו-23 גרם סוכר ל-100 גרם. רשימת רכיבים קצרה, אבל שמן דקל הוא גורם מגביל משמעותי.",
    "bottomLine": "541 קק\"ל ל-100 גרם — הצפיפות הגבוהה ביותר בקטגוריה, שמן דקל שני.",
    "consumerTakeaway": "שמן דקל כרכיב שני, 541 קק\"ל ל-100 גרם, 15 גרם שומן רווי.",
    "consumerExplanation": "שמן דקל כרכיב שני מסביר את 15 גרם השומן הרווי — כמעט פי שלושה מהסף. 541 קק\"ל ל-100 גרם הוא הגבוה ביותר שנמדד בקטגוריה זו. הרכיבים מועטים אך כבדים.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 30, "label_he": "איכות עיבוד", "explanation_he": "קמח חיטה, שמן דקל, סוכר, ביצים, מלח, חומרי טעם — רשימה קצרה יחסית. שמן דקל כמקור שומן ראשי."},
        {"dimension": "glycemic_quality", "score": 28, "label_he": "עומס גליקמי", "explanation_he": "23 גרם סוכר ל-100 גרם — גבוה. קמח לבן כבסיס."},
        {"dimension": "additive_quality", "score": 45, "label_he": "תוספים", "explanation_he": "רשימה קצרה — חומרי טעם בלבד. פחות תוספים מרוב הקטגוריה."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "541 קק\"ל ל-100 גרם — הגבוה ביותר שנמדד. שמן דקל ו-15 גרם שומן רווי."}
    ],
    "bestUseCases": ["כיבוד נדיר — יחידה אחת"]
},

"ck-7296073162001": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות קרם אגוזים — 40% קרם, 540 קק\"ל, סוכר 30 גרם.",
    "rowVerdict": "עוגיות במילוי קרם אגוזים מגיעות ל-E עם 40% קרם, 30 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם. מחית אגוז לוז 6.5% — נוכחת אבל מינורית. סירופ גלוקוז כרכיב שביעי, 540 קק\"ל ל-100 גרם.",
    "bottomLine": "40% קרם אגוזים עם סירופ גלוקוז — 540 קק\"ל ל-100 גרם.",
    "consumerTakeaway": "40% קרם אגוזים תעשייתי, 30 גרם סוכר, 13 גרם שומן רווי.",
    "consumerExplanation": "מחית אגוז לוז 6.5% — אמיתי אבל קטן. 40% קרם מכיל שמנים ושומנים צמחיים, סירופ גלוקוז, אבקת חלב, חמאה ולציטין. 30 גרם סוכר ו-540 קק\"ל ל-100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "40% קרם תעשייתי עם שמנים ושומנים, סירופ גלוקוז, חמאה, אבקת חלב, לציטין. E500, E503 בבסיס."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם. סירופ גלוקוז ברשימה מוסיף לעומס הגליקמי."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E500, E503 בבסיס, לציטין סויה בקרם — בינוני."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "540 קק\"ל ל-100 גרם — גבוה מאוד. שמנים ושומנים בקרם הם הגורם העיקרי."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290018893036": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות סנדוויץ שוקולד — שמן דקל ראשון, סוכר 33 גרם.",
    "rowVerdict": "עוגיות סנדוויץ שוקולד מגיעות ל-E עם שמן דקל כרכיב שלישי (לאחר קמח ח וסוכר), 33 גרם סוכר ו-10 גרם שומן רווי ל-100 גרם. קקאו 5%, גלוקוז-פרוקטוז ומלטודקסטרין — פרופיל תעשייתי מובהק.",
    "bottomLine": "שמן דקל, גלוקוז-פרוקטוז ומלטודקסטרין — 33 גרם סוכר.",
    "consumerTakeaway": "שמן דקל, גלוקוז-פרוקטוז, מלטודקסטרין, 33 גרם סוכר — E.",
    "consumerExplanation": "שמן דקל כרכיב שלישי, גלוקוז-פרוקטוז ומלטודקסטרין יחד מסמנים עיבוד תעשייתי גבוה. 33 גרם סוכר ל-100 גרם. לציטין חמניות — תוסף נסבל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל, גלוקוז-פרוקטוז, מלטודקסטרין, לציטין חמניות — מוצר תעשייתי מובהק."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "33 גרם סוכר ל-100 גרם. גלוקוז-פרוקטוז ומלטודקסטרין — שלושה מקורות פחמימה מהירה."},
        {"dimension": "additive_quality", "score": 35, "label_he": "תוספים", "explanation_he": "לציטין חמניות — תוסף נסבל. מלטודקסטרין, גלוקוז-פרוקטוז — לא תוספים בהגדרה, אבל מסמנים עיבוד."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "שמן דקל ושומן רווי 10 גרם — צפיפות גבוהה."}
    ],
    "bestUseCases": ["כיבוד שגרתי במנה קטנה"]
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
print("Saved batch 3.")
