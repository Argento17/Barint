import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

copy_data = {

"ck-7290119040858": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות מקלות עלים — מרגרינה, סוכר 20 גרם, שומן רווי 9.5 גרם.",
    "rowVerdict": "עוגיות מקלות עלים מגיעות ל-E. מרגרינה כרכיב שלישי, 20 גרם סוכר ו-9.5 גרם שומן רווי ל-100 גרם. 'מקלות עלים' מרמז על בצק ספוג — כאן הספיגה היא של שמן דקל ומרגרינה.",
    "bottomLine": "מרגרינה בבצק, 9.5 גרם שומן רווי ל-100 גרם.",
    "consumerTakeaway": "מרגרינה כרכיב שלישי, שומן רווי 9.5 גרם, סוכר 20 גרם.",
    "consumerExplanation": "מרגרינה כרכיב שלישי בבצק הנשכן ומראה ביתי מסתיר פרופיל תעשייתי. 9.5 גרם שומן רווי ו-20 גרם סוכר ל-100 גרם. E450, E500 כחומרי תפיחה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה כרכיב שלישי — שומן מוקשה תעשייתי. E450, E500 בחומרי תפיחה."},
        {"dimension": "glycemic_quality", "score": 30, "label_he": "עומס גליקמי", "explanation_he": "20 גרם סוכר ל-100 גרם — חוצה את הסף. קמח לבן כבסיס."},
        {"dimension": "additive_quality", "score": 35, "label_he": "תוספים", "explanation_he": "E450, E500 — חומרי תפיחה נפוצים. מרגרינה עצמה מכילה תוספים."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "מרגרינה ושומן רווי 9.5 גרם — צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["כיבוד במנה קטנה"]
},

"ck-7290105364784": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "פרה קראנץ שוקולד לבן — 47 גרם סוכר ו-562 קק\"ל ל-100 גרם.",
    "rowVerdict": "פרה קראנץ שוקולד לבן מגיעה ל-E עם 47 גרם סוכר ו-16.7 גרם שומן רווי ל-100 גרם — שניהם בין הגבוהים ביותר בקטגוריה. שוקולד לבן ושוקולד חלב כציפוי כפול, 562 קק\"ל ל-100 גרם, ביסקוויט 18.5% בלבד.",
    "bottomLine": "47 גרם סוכר ו-562 קק\"ל ל-100 גרם — בין הגבוהים בקטגוריה.",
    "consumerTakeaway": "ביסקוויט 18.5% בציפוי כפול שוקולד — 47 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "שוקולד לבן ושוקולד חלב כציפוי כפול מסבירים את 47 גרם הסוכר. הביסקוויט עצמו מהווה 18.5% בלבד. 16.7 גרם שומן רווי ו-562 קק\"ל ל-100 גרם. מחית אגוזי לוז 10% — נגיעה אמיתית.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "שוקולד לבן ושוקולד חלב כציפוי כפול, שמנים, קמח סויה, עיסת קקאו, לציטין. ביסקוויט כ-18.5% בלבד."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "47 גרם סוכר ל-100 גרם — גבוה מאוד. שוקולד לבן מורכב בעיקרו מסוכר."},
        {"dimension": "additive_quality", "score": 35, "label_he": "תוספים", "explanation_he": "לציטין לפתית כמתחלב — תוסף נסבל. שאר הרכיבים הם רכיבי מזון, לא תוספים."},
        {"dimension": "calorie_density", "score": 12, "label_he": "צפיפות קלורית", "explanation_he": "562 קק\"ל ל-100 גרם ו-16.7 גרם שומן רווי — גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד נדיר — מנת ממתק קטנה"]
},

"ck-8710502405204": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מרבה ממולאות קרם שוקולד — סוכר 39.8 גרם, שמן דקל ראשון.",
    "rowVerdict": "מרבה ממולאות קרם שוקולד מגיעות ל-E. סוכר כרכיב ראשון, שמן דקל+חמניות כרכיב שני, 39.8 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם. 516 קק\"ל. שיבולת שועל ברשימה — נוכח אבל לא משנה את הפרופיל.",
    "bottomLine": "סוכר ראשון, שמן דקל שני — 39.8 גרם סוכר ל-100 גרם.",
    "consumerTakeaway": "סוכר כרכיב ראשון, שמן דקל שני, 39.8 גרם סוכר, 516 קק\"ל.",
    "consumerExplanation": "סוכר ושמן דקל הם שני הרכיבים הראשיים — מבנה קלאסי של עוגיית מילוי תעשייתית. שיבולת שועל ברשימה (רכיב 5-6) — נוכח אבל מינורי. 13 גרם שומן רווי מסמן E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן דקל כשני הרכיבים הראשיים. E450, E500, לציטין סויה. שיבולת שועל כרכיב מינורי."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "39.8 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר כרכיב ראשון."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E450, E500, לציטין סויה — שלושה תוספים נפוצים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "516 קק\"ל ל-100 גרם. שמן דקל ו-13 גרם שומן רווי."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-8710502139017": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מרבה טריפל שוקולד — סוכר 36.4 גרם, שמן דקל+חמניות.",
    "rowVerdict": "מרבה טריפל שוקולד מגיעה ל-E. סוכר כרכיב ראשון, שמן דקל+חמניות שני, 36.4 גרם סוכר ו-13.1 גרם שומן רווי ל-100 גרם. 'טריפל שוקולד' — עיסת קקאו, חמאת קקאו ושוקולד — לא מפצה על הבסיס.",
    "bottomLine": "סוכר ושמן דקל ראשונים — 36.4 גרם סוכר, 13 גרם שומן רווי.",
    "consumerTakeaway": "טריפל שוקולד אמיתי, אבל סוכר ושמן דקל קודמים לו ברשימה.",
    "consumerExplanation": "עיסת קקאו, חמאת קקאו ואבקת חלב — שלושת מרכיבי 'טריפל' — נמצאים ברשימה. אבל סוכר ושמן דקל הם הרכיבים הראשיים. 36.4 גרם סוכר ו-13.1 גרם שומן רווי ל-100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן דקל כרכיבים הראשיים. E450, E500, לציטין סויה. מרכיבי הקאקאו אמיתיים אבל מינוריים."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "36.4 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר ראשון ברשימה."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E450, E500, לציטין סויה — שלושה תוספים נפוצים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "13.1 גרם שומן רווי. שמן דקל כרכיב שני."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-8710502279010": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות שוקולד מצופות — סוכר 38.1 גרם, שמן דקל, 525 קק\"ל.",
    "rowVerdict": "עוגיות שוקולד צ'יפס מצופות מגיעות ל-E עם 38.1 גרם סוכר, 14.9 גרם שומן רווי ו-525 קק\"ל ל-100 גרם. סוכר כרכיב ראשון, שמן דקל+חמניות שני. מסת קקאו וחמאת קקאו — נוכחים אבל נחנקים בסוכר ובשמן.",
    "bottomLine": "38.1 גרם סוכר ו-525 קק\"ל — סוכר ושמן דקל ראשונים.",
    "consumerTakeaway": "סוכר ראשון, שמן דקל שני — 38 גרם סוכר ו-525 קק\"ל ל-100 גרם.",
    "consumerExplanation": "מסת קקאו וחמאת קקאו מציעים טעם שוקולד אמיתי, אבל הסוכר (38.1 גרם) ושמן הדקל (14.9 גרם שומן רווי) הם הגורמים הדומיננטיים. 525 קק\"ל ל-100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן דקל+חמניות ראשונים. E450, E500, לציטין סויה וחמניות."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "38.1 גרם סוכר ל-100 גרם — גבוה מאוד."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E450, E500, לציטין סויה וחמניות — שלושה תוספים."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "525 קק\"ל ל-100 גרם, 14.9 גרם שומן רווי — גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290112961754": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקוציפס קרם אגוז — 36% מילוי, סוכר 36 גרם, 508 קק\"ל.",
    "rowVerdict": "שוקוציפס קרם אגוז מגיע ל-E עם 36 גרם סוכר, 9 גרם שומן רווי ו-508 קק\"ל ל-100 גרם. 36% מילוי — קרם אגוז תעשייתי עם עמילן תירס, קמח סויה ולציטין. אגוזי לוז ברשימה — נוכחים, כמות לא ידועה.",
    "bottomLine": "36% מילוי קרם אגוז תעשייתי, 36 גרם סוכר, 508 קק\"ל.",
    "consumerTakeaway": "36% מילוי קרם אגוז תעשייתי, 36 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "אגוזי לוז ברשימה מאמינים על טעם — אבל 36% קרם תעשייתי שמכיל עמילן תירס, קמח סויה ולציטין, לצד 36 גרם סוכר ל-100 גרם. סוכר כרכיב ראשון. 508 קק\"ל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "סוכר ראשון, שמנים צמחיים, עמילן תירס, קמח סויה, לציטין, E503, E500 — מוצר תעשייתי."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "36 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר ראשון ברשימה."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E503, E500, לציטין סויה — שלושה תוספים. עמילן תירס וקמח סויה כממלאים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "508 קק\"ל ל-100 גרם, 9 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-4017100364112": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "היט שוקולד בלזן — שמן דקל, נתרן 510 מ\"ג, שומן רווי 17 גרם.",
    "rowVerdict": "היט שוקולד בלזן מגיע ל-E עם שמן דקל כרכיב שלישי, 17 גרם שומן רווי ו-510 מ\"ג נתרן ל-100 גרם — גבוה מאוד גם עבור ביסקוויט. 29 גרם סוכר לצד נתרן גבוה הם שני גורמים מגבילים יוצאי דופן בשילוב.",
    "bottomLine": "17 גרם שומן רווי ו-510 מ\"ג נתרן — שילוב יוצא דופן.",
    "consumerTakeaway": "שמן דקל, שומן רווי 17 גרם ונתרן 510 מ\"ג — שניהם גבוהים.",
    "consumerExplanation": "שמן דקל כרכיב שלישי מסביר את 17 גרם השומן הרווי הגבוהים. 510 מ\"ג נתרן ל-100 גרם גבוה במיוחד לעוגייה מתוקה. גלוקוז-פרוקטוז, מי גבינה, E503, E500 ועיסת קקאו.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל כרכיב שלישי, גלוקוז-פרוקטוז, מי גבינה, E503, E500 — פרופיל תעשייתי מובהק."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "29 גרם סוכר ל-100 גרם — גבוה. גלוקוז-פרוקטוז מוסיף לעומס."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E503, E500, חומצה ציטרית, לציטין — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "17 גרם שומן רווי — גבוה מאוד. שמן דקל כמקור ראשי."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7622300489427": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "אוראו ציפוי שוקולד לבן — סוכר 49 גרם, שמן דקל+שיאה+לפתית.",
    "rowVerdict": "אוראו בציפוי שוקולד לבן מגיע ל-E עם 49 גרם סוכר ל-100 גרם — הגבוה ביותר שנמדד בקטגוריה. ציפוי שוקולד לבן על אוראו קלאסי הוסיף שכבת סוכר נוספת לפרופיל שכבר היה גבוה. E492 ו-E476 בציפוי.",
    "bottomLine": "49 גרם סוכר ל-100 גרם — הגבוה ביותר בקטגוריה.",
    "consumerTakeaway": "ציפוי שוקולד לבן הביא את הסוכר ל-49 גרם ל-100 גרם.",
    "consumerExplanation": "אוראו קלאסי כבר לא פרופיל פשוט — הוספת ציפוי שוקולד לבן (שמורכב בעיקרו מסוכר) מעלה את הסוכר ל-49 גרם ל-100 גרם. שמן דקל, שיאה ולפתית בציפוי, E492 ו-E476.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "ציפוי שוקולד לבן עם E492, E476, שמן דקל+שיאה+לפתית — מרובד ומורכב. בסיס אוראו עם E500, E503."},
        {"dimension": "glycemic_quality", "score": 10, "label_he": "עומס גליקמי", "explanation_he": "49 גרם סוכר ל-100 גרם — הגבוה ביותר בקטגוריה. שוקולד לבן מורכב בעיקרו מסוכר."},
        {"dimension": "additive_quality", "score": 20, "label_he": "תוספים", "explanation_he": "E492, E476 בציפוי, E500, E503 בבסיס, לקטוז, לציטין — ריבוי תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "שמן דקל ושומן רווי 11 גרם — גבוה. ציפוי כפול מוסיף צפיפות."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי — לא לצריכה שגרתית"]
},

"ck-46214731552": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות שוקולד צ'יפס — סוכר 38.2 גרם, שומן רווי 16.4 גרם.",
    "rowVerdict": "עוגיות שוקולד צ'יפס מגיעות ל-E עם 38.2 גרם סוכר ו-16.4 גרם שומן רווי ל-100 גרם — שניהם גבוהים מאוד. 503 קק\"ל. סוכר כרכיב ראשון, שמן צמחי שני. עיסת קקאו וחמאת קקאו נוכחים — אבל נחנקים.",
    "bottomLine": "38 גרם סוכר ו-16 גרם שומן רווי — שניהם גבוהים מאוד.",
    "consumerTakeaway": "סוכר ושמן צמחי ראשונים — 38 גרם סוכר, 16 גרם שומן רווי.",
    "consumerExplanation": "עיסת קקאו וחמאת קקאו ברשימה מסמנים שוקולד אמיתי לכאורה — אבל סוכר ושמן צמחי הם הרכיבים הדומיננטיים. 38.2 גרם סוכר ל-100 גרם, 16.4 גרם שומן רווי, 503 קק\"ל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "סוכר ושמן צמחי ראשונים. E500, E450, לציטין סויה. עיסת קקאו מינורית."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "38.2 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר כרכיב ראשון."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E500, E450, לציטין סויה — שלושה תוספים."},
        {"dimension": "calorie_density", "score": 15, "label_he": "צפיפות קלורית", "explanation_he": "503 קק\"ל ו-16.4 גרם שומן רווי — גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7296073529019": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קוקיס שוקולד מריר עם חמאה ומרגרינה — סוכר 36.2 גרם.",
    "rowVerdict": "קוקיס שוקולד מריר מגיע ל-E. שוקולד מריר 19.3% — זה יתרון. אבל חמאה ומרגרינה יחד (עם E200, E202) מסבירים את 13.3 גרם השומן הרווי. 36.2 גרם סוכר ל-100 גרם. 'מריר' לא מחזיר את הפרופיל לD.",
    "bottomLine": "שוקולד מריר 19.3% אמיתי — חמאה ומרגרינה יחד מוחקים את היתרון.",
    "consumerTakeaway": "שוקולד מריר 19.3% עם חמאה ומרגרינה — 36 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "שוקולד מריר 19.3% הוא שיעור גבוה יחסית לקטגוריה. אבל חמאה ומרגרינה (עם E200, E202) יחד מייצרים 13.3 גרם שומן רווי. 36.2 גרם סוכר ל-100 גרם. E500, E470 בחומרי תפיחה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה עם E200, E202, ביצים מיובשות, E500, E470. שוקולד מריר 19.3% — נקודה חיובית."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "36.2 גרם סוכר ל-100 גרם — גבוה מאוד. 'סוכרים' ברשימה."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E200, E202 במרגרינה, E500, E470 — ארבעה תוספים עיקריים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "חמאה ומרגרינה יחד — 13.3 גרם שומן רווי. גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד עם קפה — מנה קטנה"]
},

"ck-7296073529026": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קוקיס שוקו+שבבי שוקולד — חמאה ומרגרינה, סוכר 39.1 גרם.",
    "rowVerdict": "קוקיס שוקו ושבבי שוקולד מגיע ל-E — גרסת הקקאו של הקוקיס מריר. אותה נוסחה: חמאה ומרגרינה (E200, E202) יחד, 39.1 גרם סוכר ו-13.6 גרם שומן רווי ל-100 גרם. הוספת קקאו לא שינתה את הפרופיל.",
    "bottomLine": "גרסת קקאו של אותה נוסחה — E מאותן סיבות.",
    "consumerTakeaway": "קקאו לא שינה את הנוסחה — חמאה, מרגרינה, 39 גרם סוכר.",
    "consumerExplanation": "הוספת קקאו לגרסת השוקולד המריר יצרה קוקיס עם 39.1 גרם סוכר ל-100 גרם — יותר מהגרסה המריר. אותם חמאה ומרגרינה (E200, E202) ו-13.6 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה עם E200, E202, ביצים מיובשות, E500, E470 — זהה לגרסת השוקולד המריר."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "39.1 גרם סוכר ל-100 גרם — גבוה מהגרסה המריר."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E200, E202 במרגרינה, E500, E470 — זהה לגרסה המריר."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "13.6 גרם שומן רווי — גבוה מאוד. זהה לגרסה המריר."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
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
print("Saved batch 4.")
