import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

copy_data = {

"ck-7290119043897": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות רולדה תמרים — מרגרינה + רשימת תוספים ארוכה מאוד.",
    "rowVerdict": "עוגיות רולדה תמרים מגיעות ל-E. מרגרינה כרכיב שני, ממרח תמרים 20% שמכיל E330 ו-E202, קצפת צמחית עם שישה תוספים, ריבה שקופה עם חמישה תוספים — בסך הכל מעל עשרה תוספים שונים. 19.4 גרם סוכר ו-10.3 גרם שומן רווי ל-100 גרם.",
    "bottomLine": "תמרים ומרגרינה עם מעל עשרה תוספים — E.",
    "consumerTakeaway": "ממרח תמרים 20% אמיתי — מרגרינה ומעל עשרה תוספים מסביבו.",
    "consumerExplanation": "ממרח תמרים 20% הוא אמיתי. אבל מרגרינה כרכיב שני, קצפת צמחית עם E415, E464, E322, E481, E471, E477, E435, E475, E331, E339, E202, E160 — פרופיל תעשייתי חריג. 19.4 גרם סוכר ו-10.3 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 15, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה, קצפת צמחית עם עשרה תוספים, ריבה שקופה עם חמישה תוספים — רמת עיבוד חריגה."},
        {"dimension": "glycemic_quality", "score": 25, "label_he": "עומס גליקמי", "explanation_he": "19.4 גרם סוכר ל-100 גרם — גבוה. ממרח תמרים 20% עם סוכר טבעי גבוה."},
        {"dimension": "additive_quality", "score": 10, "label_he": "תוספים", "explanation_he": "E415, E464, E322, E481, E471, E477, E435, E475, E331, E339, E202, E160, E450, E500 — רשימה חריגה באורכה."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "מרגרינה ו-10.3 גרם שומן רווי — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי לאוהבי תמרים"]
},

"ck-8000500366073": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "ביסקוויט נוטלה — 40% ממרח קקאו, סוכר 35.8 גרם.",
    "rowVerdict": "ביסקוויט נוטלה מגיע ל-E. 40% מהמוצר הוא ממרח קקאו עם אגוזי לוז — ממרח שמכיל סוכר כרכיב ראשון ושמן צמחי שני. הביסקוויט עצמו מורכב מקמח חיטה, שמנים צמחיים, לקטוז וסובין. 35.8 גרם סוכר ו-11.5 גרם שומן רווי ל-100 גרם.",
    "bottomLine": "40% ממרח נוטלה — שמן צמחי ואגוזי לוז 13%, סוכר 35.8 גרם.",
    "consumerTakeaway": "40% ממרח נוטלה, 13% אגוזי לוז בממרח — אבל סוכר ושמן צמחי קודמים.",
    "consumerExplanation": "ממרח קקאו עם אגוזי לוז 13% הוא נוטלה הקלאסית. אבל סוכר הוא הרכיב הראשון בממרח, ושמן צמחי השני. 35.8 גרם סוכר ו-11.5 גרם שומן רווי ל-100 גרם. דבש ברשימה — נגיעה מעניינת.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "40% ממרח עם סוכר ושמן צמחי ראשונים, לציטין, מתחלבים. קמח חיטה, שמנים, לקטוז, סובין בביסקוויט."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "35.8 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר הוא הרכיב הראשון בממרח."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "לציטין סויה, מתחלבים, חומרי תפיחה מרובים, מתחלבים בממרח — ריבוי תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "515 קק\"ל ו-11.5 גרם שומן רווי ל-100 גרם — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי לאוהבי נוטלה"]
},

"ck-7622210137234": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "אוראו דאבל קרם וניל — סוכר 43 גרם, שמן דקל+גרעיני דקל.",
    "rowVerdict": "אוראו דאבל קרם וניל מגיע ל-E עם 43 גרם סוכר ו-12 גרם שומן רווי ל-100 גרם. 'דאבל' — כמות קרם כפולה מהאוראו הרגיל — מסביר את הסוכר הגבוה. שמן דקל וגרעיני דקל בציפוי, E450, E500, E503, לציטין.",
    "bottomLine": "קרם כפול — 43 גרם סוכר ושמן דקל+גרעיני דקל.",
    "consumerTakeaway": "קרם כפול הביא 43 גרם סוכר ל-100 גרם — שמן דקל ושמן גרעיני דקל.",
    "consumerExplanation": "קרם כפול מהאוראו הרגיל מסביר את 43 גרם הסוכר — שמן דקל ושמן גרעיני דקל הם מקורות השומן הרווי בקרם. E450, E500, E503, לציטין חמניות ולציטין סויה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן דקל+גרעיני דקל ראשונים. E450, E500, E503, מתחלבים — מוצר תעשייתי מובהק."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "43 גרם סוכר ל-100 גרם — גבוה מאוד. קרם כפול כמות סוכר כפולה."},
        {"dimension": "additive_quality", "score": 22, "label_he": "תוספים", "explanation_he": "E450, E500, E503, לציטין חמניות, לציטין סויה, מתחלבים — ריבוי תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "500 קק\"ל ו-12 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-5901414200411": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "היט מיניס עם שוקולד בלזן — שמן דקל, שומן רווי 15 גרם.",
    "rowVerdict": "היט מיניס עם שוקולד בלזן מגיעות ל-E. שומן צמחי דקלים כרכיב שני, 15 גרם שומן רווי ו-28 גרם סוכר ל-100 גרם. עיסת קקאו וחמאת קקאו — קקאו אמיתי בכמות קטנה. סירופ סוכר אינוורטי ומי גבינה משלימים.",
    "bottomLine": "שמן דקל שני, שומן רווי 15 גרם ל-100 גרם — E.",
    "consumerTakeaway": "שמן דקל כרכיב שני, 15 גרם שומן רווי, 28 גרם סוכר.",
    "consumerExplanation": "שומן צמחי דקלים כרכיב שני מסביר את 15 גרם השומן הרווי. 28 גרם סוכר ל-100 גרם. עיסת קקאו וחמאת קקאו — קקאו אמיתי אבל בכמות קטנה (2.3% קקאו דלת שומן). מי גבינה ואבקת מי גבינה כמרכיבי חלב.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל שני, סירופ סוכר אינוורטי, מי גבינה, דיסודיום דיפוספט, E503, לציטין."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "28 גרם סוכר ל-100 גרם. סירופ סוכר אינוורטי מוסיף לעומס."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "דיסודיום דיפוספט, E503, חומצה ציטרית, לציטין — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "503 קק\"ל ו-15 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7296073161981": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות קרם שוקולד — 40% קרם, 544 קק\"ל, שומן רווי 14 גרם.",
    "rowVerdict": "עוגיות במילוי קרם שוקולד מגיעות ל-E עם 40% קרם תעשייתי, 30 גרם סוכר, 14 גרם שומן רווי ו-544 קק\"ל ל-100 גרם. מחית אגוז לוז 6.5% בקרם — אמיתי אבל מינורי. חמאה ושוקולד מריר 1% — נגיעות אמיתיות בפרופיל ביסקוויט שמרוב קרם.",
    "bottomLine": "40% קרם שוקולד תעשייתי — 544 קק\"ל, שומן רווי 14 גרם.",
    "consumerTakeaway": "40% קרם שוקולד עם שמנים צמחיים — 30 גרם סוכר, 544 קק\"ל.",
    "consumerExplanation": "40% קרם שמכיל שמנים ושומנים צמחיים, מחית אגוז לוז 6.5%, אבקת חלב ועיסת קקאו — מרוכב. חמאה ושוקולד מריר 1% נוכחים. 30 גרם סוכר ו-544 קק\"ל ל-100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "40% קרם עם שמנים ושומנים, מחית אגוז לוז, אבקת חלב, עיסת קקאו. E500, E503 בבסיס, לציטין בקרם."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם. גלוקוז ברשימה מוסיף לעומס."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E500, E503, לציטין סויה — שלושה תוספים."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "544 קק\"ל ו-14 גרם שומן רווי — גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-4017100198151": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "היט וניל בלזן — שמן דקל, שומן רווי 17 גרם, סוכר 31 גרם.",
    "rowVerdict": "עוגיות היט בטעם וניל של בלזן מגיעות ל-E עם שמן דקל כרכיב שני, 17 גרם שומן רווי ו-31 גרם סוכר ל-100 גרם. אבקת מי גבינה ואבקת חלב דל שומן — נגיעת חלב. 'בטעם וניל' הוא חומר טעם וריח, לא וניל אמיתי.",
    "bottomLine": "שמן דקל שני, 17 גרם שומן רווי — E ברור.",
    "consumerTakeaway": "שמן דקל כרכיב שני, שומן רווי 17 גרם, 31 גרם סוכר.",
    "consumerExplanation": "שמן דקל כרכיב שני מסביר את 17 גרם השומן הרווי — גבוה מאוד. 31 גרם סוכר ל-100 גרם. 'בטעם וניל' הוא חומר טעם, לא תרמיל וניל. אבקת מי גבינה ואבקת חלב דל שומן — נגיעת חלב.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל שני, אבקת מי גבינה, אמוניום קרבונט, E503, חומצה ציטרית, חומרי טעם — מוצר תעשייתי."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "31 גרם סוכר ל-100 גרם — גבוה. סירופ סוכר אינוורטי ברשימה."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "אמוניום קרבונט, E503, חומצה ציטרית — שלושה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "17 גרם שומן רווי ו-508 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290106656727": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "חיוכים שוקולד — שמנים צמחיים, סוכר 40 גרם, שלושה סוכרים.",
    "rowVerdict": "עוגיות חיוכים שוקולד מגיעות ל-E עם 40 גרם סוכר ל-100 גרם. ברשימת הרכיבים מצוינים שלושה סוגי סוכר — 'סוכרים (סוכר לבן, דקסטרוזה, סוכר אינברטי)'. 10.7 גרם שומן רווי ושמנים ושומנים צמחיים כלליים.",
    "bottomLine": "שלושה סוגי סוכר ברשימה — 40 גרם סוכר ל-100 גרם.",
    "consumerTakeaway": "שלושה סוגי סוכר (לבן, דקסטרוזה, אינברטי) — 40 גרם ל-100 גרם.",
    "consumerExplanation": "ריכוז שלושה סוגי סוכר ברשימת הרכיבים — סוכר לבן, דקסטרוזה וסוכר אינברטי — מסמן מוצר שמנסה לפזר את ה'סוכר' על פני מספר רכיבים. 40 גרם ל-100 גרם. ציפוי אבקת קקאו 2.4%.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שלושה סוגי סוכר, שמנים ושומנים צמחיים כלליים, מייצב (צלולוזה), עמילן תירס, לציטין, E500, E503."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "40 גרם סוכר ל-100 גרם — גבוה מאוד. שלושה מקורות סוכר."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "מייצב (צלולוזה), לציטין סויה, E500, E503 — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "10.7 גרם שומן רווי ו-497 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-46214930207": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקולד צ'יפס עם ציפוי סוכר צבעוני — סוכר 41.2 גרם, שמן דקל.",
    "rowVerdict": "עוגיות שוקולד צ'יפס מגיעות ל-E עם 41.2 גרם סוכר ו-12.4 גרם שומן רווי ל-100 גרם. ציפוי סוכר צבעוני על שוקולד חלב הוסיף שישה צבעי מאכל (אנטוציאנין, כורכומין, קופר כלורופיל, מיצוי סלק, קארוטין, ווקס) ו-E903 כחומר הזגה. שמן דקל+חמניות.",
    "bottomLine": "ציפוי סוכר צבעוני על שוקולד — שישה צבעי מאכל וסוכר גבוה.",
    "consumerTakeaway": "שישה צבעי מאכל בציפוי הסוכר הצבעוני — 41 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "ציפוי הסוכר הצבעוני מכיל אנטוציאנין, כורכומין, קופר כלורופיל, מיצוי סלק, קארוטין וווקס קרנבורה — שישה צבעי מאכל. שוקולד מריר 14% ושוקולד חלב 22% אמיתיים, אבל 41.2 גרם סוכר ו-E903 משלימים.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "שישה צבעי מאכל בציפוי, E903 כחומר הזגה, גאם ערביק, E450, E500, לציטין — מוצר מורכב."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "41.2 גרם סוכר ל-100 גרם — גבוה מאוד. גלוקוז-פרוקטוז ברשימה."},
        {"dimension": "additive_quality", "score": 18, "label_he": "תוספים", "explanation_he": "שישה צבעי מאכל, E903 (ווקס קרנבורה), גאם ערביק, E450, E500, לציטין — ריבוי תוספים חריג."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "12.4 גרם שומן רווי ו-496 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד לילדים — מנה קטנה"]
},

"ck-8710502470028": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקוצ'יפס נוגטלי — סוכר 40.2 גרם, חמאה ואגוזי מלך.",
    "rowVerdict": "עוגיות שוקוצ'יפס נוגטלי מגיעות ל-E עם 40.2 גרם סוכר ו-12.6 גרם שומן רווי ל-100 גרם. חמאה ברשימה — יתרון על שמן צמחי. אגוזי מלך 2.4% — נוכחים. אבל סוכר ושמן צמחי קודמים לחמאה ברשימה. 513 קק\"ל.",
    "bottomLine": "חמאה ואגוזים אמיתיים — אבל סוכר 40 גרם ושמן צמחי ראשונים.",
    "consumerTakeaway": "חמאה ואגוזי מלך אמיתיים — אבל 40 גרם סוכר ושמן צמחי קודמים.",
    "consumerExplanation": "חמאה ואגוזי מלך 2.4% מבדילים את המוצר הזה ממרבית הקטגוריה. אבל סוכר כרכיב ראשון ושמן צמחי שני, 40.2 גרם סוכר ו-12.6 גרם שומן רווי ל-100 גרם — E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן צמחי ראשונים. חמאה, אגוזי מלך — נגיעות איכות. E450, E500, לציטין."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "40.2 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר החלב ברשימה מוסיף."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E450, E500, לציטין סויה — שלושה תוספים. רשימה יחסית קצרה."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "513 קק\"ל ו-12.6 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290119040650": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות נסיכה מיקס — שמן דקל, מילוי תות 38% עם שישה תוספים.",
    "rowVerdict": "עוגיות נסיכה מיקס מגיעות ל-E. מילוי תות שדה 38% שמכיל 65% סוכר, תפוח 20%, E300, E440, E202, E150D ו-E124 — שישה תוספים במילוי בלבד. שמן דקל בבצק, ריבה שקופה 3.4% עם עוד חמישה תוספים.",
    "bottomLine": "מילוי תות 38% שמורכב מ-65% סוכר ושישה תוספים.",
    "consumerTakeaway": "מילוי תות 38% — 65% ממנו סוכר, שישה תוספים.",
    "consumerExplanation": "מילוי לאפייה 'בטעם תות' מכיל 65% סוכר — כלומר 65 גרם מתוך 100 גרם של המילוי הם סוכר. תפוח 20% נותן גוף, E300, E440, E202, E150D, E124 — שישה תוספים. 10.8 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 18, "label_he": "איכות עיבוד", "explanation_he": "מילוי עם 65% סוכר ושישה תוספים, ריבה שקופה עם חמישה תוספים, שמן דקל בבצק. רמת עיבוד חריגה."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "מילוי עם 65% סוכר — גבוה מאוד. 23 גרם סוכר ל-100 גרם בפרופיל הכולל."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E300, E440, E202, E150D, E124 במילוי + E440, E330, E202, E900 בריבה — ריבוי תוספים חריג."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "10.8 גרם שומן רווי ו-434 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד לילדים — מנה קטנה"]
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
print("Saved batch 5.")
