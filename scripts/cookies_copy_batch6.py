import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

copy_data = {

"ck-7290019870463": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "סנדוויץ קרם וניל צ'וקטה — שמן דקל, 32 גרם סוכר, מלטודקסטרין.",
    "rowVerdict": "עוגיות סנדוויץ קרם וניל צ'וקטה מגיעות ל-E. שמן דקל כרכיב שני, 32 גרם סוכר ו-9 גרם שומן רווי ל-100 גרם. מלטודקסטרין, צבע מאכל קרמל, לציטין חמניות — פרופיל תעשייתי. 'קרם וניל' הוא חומרי טעם.",
    "bottomLine": "שמן דקל שני, מלטודקסטרין, 32 גרם סוכר — E.",
    "consumerTakeaway": "שמן דקל כרכיב שני, מלטודקסטרין, 32 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "שמן דקל כרכיב שני מסביר את 9 גרם השומן הרווי. מלטודקסטרין (פחמימה מהירה) ו-32 גרם סוכר — שני גורמי עומס גליקמי. צבע מאכל קרמל ולציטין חמניות.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל שני, עמילן חיטה, מלטודקסטרין, צבע מאכל קרמל, לציטין חמניות."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "32 גרם סוכר ל-100 גרם. מלטודקסטרין מוסיף עומס גליקמי שלא מסווג כ'סוכר'."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "מלטודקסטרין, צבע מאכל קרמל, לציטין חמניות, מתפיחים — ארבעה."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "9 גרם שומן רווי ו-456 קק\"ל — בינוני לגבוה."}
    ],
    "bestUseCases": ["כיבוד שגרתי במנה קטנה"]
},

"ck-7296073659969": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות חיות שוקו — שמן דקל, שלושה סוגי סוכר.",
    "rowVerdict": "עוגיות חיות שוקו מגיעות ל-E. שמן דקל כרכיב שני, שלושה מקורות סוכר (סוכר, דקסטרוז, פרוקטוז) ברשימה, אבקת קקאו 2.4% — כמות נמוכה. עמילן, מסמיך צלולוז, לציטין. נתרן חסר.",
    "bottomLine": "שמן דקל שני, שלושה מקורות סוכר, קקאו 2.4% בלבד.",
    "consumerTakeaway": "שמן דקל כרכיב שני, שלושה סוגי סוכר — קקאו מינימלי.",
    "consumerExplanation": "שמן דקל כרכיב שני, שלושה מקורות סוכר — סוכר, דקסטרוז, פרוקטוז — ברשימה. אבקת קקאו 2.4% מספקת את 'השוקו' בשם. מסמיך צלולוז ולציטין סויה. נתון הנתרן חסר.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל שני, שלושה מקורות סוכר, מסמיך צלולוז, עמילן, לציטין, גלוטן חיטה מוסף."},
        {"dimension": "glycemic_quality", "score": 28, "label_he": "עומס גליקמי", "explanation_he": "21 גרם סוכר ל-100 גרם. שלושה מקורות סוכר — סוכר, דקסטרוז, פרוקטוז."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "מסמיך (צלולוז), לציטין סויה, חומרי תפיחה, מעכב חמצון (תמצית רוזמרין) — ארבעה."},
        {"dimension": "calorie_density", "score": 22, "label_he": "צפיפות קלורית", "explanation_he": "8.6 גרם שומן רווי ו-494 קק\"ל. שמן דקל כמקור עיקרי."}
    ],
    "bestUseCases": ["כיבוד לילדים — מנה קטנה"]
},

"ck-7290119040605": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות נסיכה בטעם תות — שמן דקל, מילוי תות 38% עם שישה תוספים.",
    "rowVerdict": "עוגיות נסיכה בטעם תות מגיעות ל-E. זהה לגרסת המיקס — מילוי תות שדה 38% שמכיל 65% סוכר, E300, E440, E202, E150D ו-E124. שמן דקל בבצק, 10.8 גרם שומן רווי ל-100 גרם.",
    "bottomLine": "מילוי תות 38% עם 65% סוכר ושישה תוספים — זהה לגרסת המיקס.",
    "consumerTakeaway": "מילוי תות 65% סוכר, שישה תוספים — גרסת תות של נסיכה.",
    "consumerExplanation": "גרסת התות של נסיכה חולקת אותו מילוי עם גרסת המיקס — 65% סוכר, תפוח 20%, E300, E440, E202, E150D, E124. שמן דקל בבצק, 10.8 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 18, "label_he": "איכות עיבוד", "explanation_he": "מילוי עם 65% סוכר ושישה תוספים, ריבה שקופה עם חמישה תוספים, שמן דקל בבצק — זהה לגרסת המיקס."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "מילוי עם 65% סוכר. 23 גרם סוכר ל-100 גרם בפרופיל הכולל."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E300, E440, E202, E150D, E124 במילוי + E440, E330, E202, E900 בריבה — ריבוי תוספים."},
        {"dimension": "calorie_density", "score": 28, "label_he": "צפיפות קלורית", "explanation_he": "10.8 גרם שומן רווי ו-434 קק\"ל — זהה לגרסת המיקס."}
    ],
    "bestUseCases": ["כיבוד לילדים — מנה קטנה"]
},

"ck-7290112340276": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות קרם קפה נמס — שמן צמחי, שומן רווי 14.7 גרם, קפה 0.6%.",
    "rowVerdict": "עוגיות קרם קפה נמס של עלית מגיעות ל-E. שמנים ושומנים צמחיים כרכיב שני, 14.7 גרם שומן רווי ו-30 גרם סוכר ל-100 גרם. קפה נמס 0.6% — כמות זניחה שמוסיפה ניחוח, לא מאפיין קפה. 523 קק\"ל.",
    "bottomLine": "קפה נמס 0.6% — שמן צמחי ושומן רווי 14.7 גרם דומיננטיים.",
    "consumerTakeaway": "קפה 0.6% לא משנה את הפרופיל — שמן צמחי ושומן רווי גבוה.",
    "consumerExplanation": "קפה נמס 0.6% מוסיף ניחוח, לא מהות. שמנים ושומנים צמחיים כרכיב שני, 14.7 גרם שומן רווי ו-30 גרם סוכר ל-100 גרם — פרופיל E מוחלט. שבבי שוקולד מריר 5.2% — נוכחים.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "שמנים ושומנים צמחיים שניים, לציטין סויה, E450, E500, מעכב חמצון (רוזמרין)."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "30 גרם סוכר ל-100 גרם — גבוה."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "לציטין סויה, E450, E500, מעכב חמצון — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "523 קק\"ל ו-14.7 גרם שומן רווי — גבוה מאוד."}
    ],
    "bestUseCases": ["כיבוד עם קפה — מנה קטנה"]
},

"ck-7622300356767": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקולד צ'יפס עם ביצים — שמן דקל, סוכר 34 גרם, נתרן 330 מ\"ג.",
    "rowVerdict": "עוגיות שוקולד צ'יפס (מונדלז) מגיעות ל-E. שמן דקל כרכיב שלישי, 34 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם. ביצים ואבקת חלב מלא — נגיעות איכות. נתרן 330 מ\"ג ל-100 גרם גבוה לעוגייה מתוקה.",
    "bottomLine": "שמן דקל, ביצים ואבקת חלב — 34 גרם סוכר ונתרן גבוה.",
    "consumerTakeaway": "ביצים ואבקת חלב מלא בצד שמן דקל — 34 גרם סוכר, נתרן 330 מ\"ג.",
    "consumerExplanation": "ביצים ואבקת חלב מלא הם נגיעות איכות אמיתיות. אבל שמן דקל כרכיב שלישי, 34 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם, ונתרן 330 מ\"ג — E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "קמח חיטה 34%, שמן דקל שלישי, ביצים, אבקת חלב — נגיעות טובות. E450, E500, לציטין."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "34 גרם סוכר ל-100 גרם — גבוה מאוד. סירופ גלוקוז ברשימה."},
        {"dimension": "additive_quality", "score": 28, "label_he": "תוספים", "explanation_he": "E450, E500, לציטין סויה — שלושה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "13 גרם שומן רווי ו-494 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7622300489434": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "אוראו בציפוי שוקולד חלב — סוכר 47 גרם, שמן דקל, E501.",
    "rowVerdict": "אוראו בציפוי שוקולד חלב מגיע ל-E עם 47 גרם סוכר ו-14.5 גרם שומן רווי ל-100 גרם. ציפוי שוקולד חלב על אוראו קלאסי — כמו גרסת השוקולד הלבן, הסוכר קפץ ל-47 גרם. E500, E503, E501 בחומרי תפיחה, E322 כמתחלב.",
    "bottomLine": "ציפוי שוקולד חלב — 47 גרם סוכר ל-100 גרם. שמן דקל.",
    "consumerTakeaway": "ציפוי שוקולד חלב על אוראו — 47 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "ציפוי שוקולד חלב (שמורכב מסוכר, חמאת קקאו ואבקת חלב) מוסיף שכבת סוכר על האוראו הקלאסי. 47 גרם סוכר ל-100 גרם. שמן דקל, לקטוז ושומן חלב. E500, E503, E501, E322.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "ציפוי שוקולד חלב עם שמן דקל, לקטוז, שומן חלב. E500, E503, E501, E322 — מוצר מורכב."},
        {"dimension": "glycemic_quality", "score": 10, "label_he": "עומס גליקמי", "explanation_he": "47 גרם סוכר ל-100 גרם — גבוה מאוד. סירופ גלוקוז-פרוקטוז ברשימה."},
        {"dimension": "additive_quality", "score": 22, "label_he": "תוספים", "explanation_he": "E500, E503, E501 כחומרי תפיחה, E322 כמתחלב — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "14.5 גרם שומן רווי ו-510 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290019816232": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קראנץ סנדוויץ שוקולד — ציפוי שוקולד חלב 14%, 25 גרם סוכר.",
    "rowVerdict": "קראנץ סנדוויץ שוקולד מגיע ל-E. מורכב ממרכיבים רבים: 17.8% ביסקוויטים, 14.1% ציפוי שוקולד חלב, 3.3% חטיפי אורז, ועוד חלב רזה, קוקוס, חמאת קקאו, פסטת אגוזי לוז ו-E476, E471, לציטין, גואר גאם. 25.3 גרם סוכר ו-8.9 גרם שומן רווי.",
    "bottomLine": "מוצר מרובד ממרכיבים רבים — E476, E471, 25 גרם סוכר, 8.9 גרם שומן רווי.",
    "consumerTakeaway": "17.8% ביסקוויט ו-14.1% שוקולד חלב בתוך מוצר עם E476 ו-E471.",
    "consumerExplanation": "קראנץ סנדוויץ הוא מוצר מרובד: חלב רזה, ביסקוויטים 17.8%, שוקולד חלב 14.1%, חטיפי אורז 3.3%, קוקוס, פסטת אגוזי לוז ועוד. E476 (פוליגליצרול), E471, לציטין, גואר גאם. 25.3 גרם סוכר ו-8.9 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "E476, E471, לציטין סויה, גואר גאם, גאם גרעיני חרובים — ריבוי ממייצבים. חלב רזה משוחזר בסיס."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "25.3 גרם סוכר ל-100 גרם. סירופ גלוקוז ברשימה. חטיפי אורז תפוח מוסיפים פחמימות מהירות."},
        {"dimension": "additive_quality", "score": 20, "label_he": "תוספים", "explanation_he": "E476, E471, לציטין סויה, גואר גאם, גאם גרעיני חרובים — חמישה מייצבים."},
        {"dimension": "calorie_density", "score": 45, "label_he": "צפיפות קלורית", "explanation_he": "287 קק\"ל ל-100 גרם — נמוך יחסית לקטגוריה. 8.9 גרם שומן רווי."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7622201401900": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מילקה סנסיישן אוראו — שמן חמניות+לפתית+דקל, סוכר 38 גרם.",
    "rowVerdict": "עוגיות מילקה סנסיישן אוראו מגיעות ל-E עם 38 גרם סוכר ו-9.8 גרם שומן רווי ל-100 גרם. שמן חמניות, שמן לפתית ושמן דקל יחד — מגוון מקורות שומן. עיסת קקאו וחמאת קקאו — קקאו אמיתי בכמות קטנה. 514 קק\"ל.",
    "bottomLine": "שלושה שמנים יחד, 38 גרם סוכר — E של מילקה.",
    "consumerTakeaway": "שלושה שמנים (חמניות, לפתית, דקל) + 38 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "שמן חמניות, לפתית ודקל יחד — שלושה מקורות שומן שנפוץ לשלבם כדי לנהל עלות ותזונה. עיסת קקאו וחמאת קקאו אמיתיים אבל בכמות קטנה. 38 גרם סוכר ל-100 גרם. E450, E500, E503.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "שלושה שמנים, שומן חלב, E450, E500, E503, לציטין סויה, לקטוז. עיסת קקאו וחמאת קקאו — נגיעות חיוביות."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "38 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר כרכיב ראשון."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "E450, E500, E503, לציטין סויה, לקטוז — חמישה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "514 קק\"ל ו-9.8 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7622201809188": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "ביסקוויט מילקה — שמן דקל, חמאת קקאו, סוכר 41 גרם.",
    "rowVerdict": "ביסקוויט מילקה מגיע ל-E עם 41 גרם סוכר ו-12 גרם שומן רווי ל-100 גרם. שמן דקל כרכיב שני, חמאת קקאו ועיסת קקאו — קקאו אמיתי. E476 כמתחלב נוסף על לציטין סויה. E450, E500, E503.",
    "bottomLine": "שמן דקל שני, חמאת קקאו — 41 גרם סוכר ו-12 גרם שומן רווי.",
    "consumerTakeaway": "שמן דקל, חמאת קקאו ועיסת קקאו — 41 גרם סוכר, E476.",
    "consumerExplanation": "חמאת קקאו ועיסת קקאו הם קקאו אמיתי — נקודת פתיחה טובה יחסית לקטגוריה. אבל שמן דקל כרכיב שני, 41 גרם סוכר ו-E476 כמתחלב בנוסף ללציטין — E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 25, "label_he": "איכות עיבוד", "explanation_he": "שמן דקל שני, E476 ולציטין סויה כמתחלבים כפולים, E450, E500, E503, חומצה ציטרית."},
        {"dimension": "glycemic_quality", "score": 12, "label_he": "עומס גליקמי", "explanation_he": "41 גרם סוכר ל-100 גרם — גבוה מאוד. סוכר כרכיב ראשון."},
        {"dimension": "additive_quality", "score": 22, "label_he": "תוספים", "explanation_he": "E476, לציטין סויה, E450, E500, E503, חומצה ציטרית — שישה תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "12 גרם שומן רווי ו-488 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290115206333": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מיני שוקוצ'יפס — 22% שוקולד מריר, שומן רווי 12.2 גרם.",
    "rowVerdict": "עוגיות מיני שוקוצ'יפס מגיעות ל-E עם 12.2 גרם שומן רווי ו-31 גרם סוכר ל-100 גרם. שוקולד מריר 22% — גבוה יחסית, עם 44% מוצקי קקאו. שמן צמחי כלא-מפורט, E503, E500, לציטין סויה.",
    "bottomLine": "שוקולד מריר 22% לצד שמן צמחי לא-מפורט ו-31 גרם סוכר.",
    "consumerTakeaway": "22% שוקולד מריר עם 44% קקאו — 31 גרם סוכר, שמן צמחי לא-מפורט.",
    "consumerExplanation": "שוקולד מריר 22% עם 44% מוצקי קקאו הוא הרכיב הבולט לטובה. אבל שמן צמחי (לא מפורט) כרכיב שני, 31 גרם סוכר ו-12.2 גרם שומן רווי ל-100 גרם — E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "שוקולד מריר 22% עם 44% קקאו — נוכח. שמן צמחי לא-מפורט, E503, E500, לציטין."},
        {"dimension": "glycemic_quality", "score": 20, "label_he": "עומס גליקמי", "explanation_he": "31 גרם סוכר ל-100 גרם. שוקולד מריר 22% מוסיף אבל לא שולט."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E503, E500, לציטין סויה, חומצת לימון — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 20, "label_he": "צפיפות קלורית", "explanation_he": "12.2 גרם שומן רווי ו-501 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי עם שוקולד מריר אמיתי"]
},

"ck-7290000075143": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקוצ'יפס קלאסי אסם — 30% שוקולד מריר, 34 גרם סוכר.",
    "rowVerdict": "שוקוצ'יפס קלאסי של אסם מגיע ל-E. שוקולד מריר 30% — הגבוה ביותר שנמדד בקטגוריה, עם 44% מוצקי קקאו. אבל 34 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם, ושמנים צמחיים לא מפורטים — E.",
    "bottomLine": "30% שוקולד מריר עם 44% קקאו — 34 גרם סוכר ל-100 גרם.",
    "consumerTakeaway": "30% שוקולד מריר אמיתי — אבל 34 גרם סוכר ושמן צמחי לא-מפורט.",
    "consumerExplanation": "שוקולד מריר 30% עם 44% מוצקי קקאו הוא הרכיב הדומיננטי — גבוה יחסית לקטגוריה. אבל שמנים צמחיים לא מפורטים, 34 גרם סוכר ו-13 גרם שומן רווי ל-100 גרם — E.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 30, "label_he": "איכות עיבוד", "explanation_he": "שוקולד מריר 30% כרכיב ראשון — יוצא דופן חיובי. שמנים צמחיים לא מפורטים, E503, E500, לציטין."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "34 גרם סוכר ל-100 גרם — גבוה. שוקולד מריר מכיל סוכר גם הוא."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E503, E500, לציטין סויה, חומצת לימון — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "13 גרם שומן רווי ו-514 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["מבין ה-E — הבחירה הטובה יחסית לאוהבי שוקוצ'יפס"]
},

"ck-7290019816058": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "קראנץ מיני אלפחורס — ציפוי שוקולד לבן עם E476, ריבת חלב 10%.",
    "rowVerdict": "קראנץ מיני אלפחורס מגיע ל-E. ציפוי שוקולד לבן 32% עם E476, ריבת חלב 10% שמכילה E500 ו-E202, שוקולד לבן כרכיב ראשון — 32 גרם סוכר ו-12 גרם שומן רווי ל-100 גרם. E471, גואר גאם, גאם גרעיני חרובים ויותר מעשרה צבעי מאכל.",
    "bottomLine": "שוקולד לבן 32% עם E476, ריבת חלב 10%, ויותר מעשרה צבעי מאכל.",
    "consumerTakeaway": "ציפוי שוקולד לבן עם E476, ריבת חלב 10%, 32 גרם סוכר — E.",
    "consumerExplanation": "שוקולד לבן 32% כציפוי עם E476 הוא הרכיב הדומיננטי. ריבת חלב 10% עם E500 ו-E202. עוגיות בטעם חמאה בבסיס. יותר מעשרה צבעי מאכל בשכבות השונות. 32 גרם סוכר ו-12 גרם שומן רווי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 18, "label_he": "איכות עיבוד", "explanation_he": "שוקולד לבן עם E476, ריבת חלב עם E202, E471, גואר גאם, גאם גרעיני חרובים, E-476, יותר מעשרה צבעי מאכל."},
        {"dimension": "glycemic_quality", "score": 18, "label_he": "עומס גליקמי", "explanation_he": "32 גרם סוכר ל-100 גרם. שוקולד לבן מורכב בעיקרו מסוכר. ריבת חלב מוסיפה."},
        {"dimension": "additive_quality", "score": 15, "label_he": "תוספים", "explanation_he": "E476, E202, E500 בריבה, E471, גואר גאם, גאם חרובים, צבעי מאכל מרובים — רשימה ארוכה."},
        {"dimension": "calorie_density", "score": 30, "label_he": "צפיפות קלורית", "explanation_he": "351 קק\"ל ל-100 גרם — בינוני. 12 גרם שומן רווי."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-8710502064814": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שוקוצ'יפס מרקם רך — גליצרין, סורביטול, שמן דקל, 29.7 גרם סוכר.",
    "rowVerdict": "שוקוצ'יפס מרקם רך מגיע ל-E. המרקם הרך נגרם על-ידי גליצרין (E422) וסירופ סורביטול — שניהם חומרי לחות שמשמרים רכות. שמן דקל+חמניות, 29.7 גרם סוכר ו-11.4 גרם שומן רווי ל-100 גרם. צימוקים — נגיעת פרי.",
    "bottomLine": "גליצרין וסורביטול מסבירים את הרכות — 29.7 גרם סוכר, שמן דקל.",
    "consumerTakeaway": "גליצרין וסורביטול לרכות, שמן דקל לשומן, 30 גרם סוכר ל-100 גרם.",
    "consumerExplanation": "עוגייה רכה בגלל גליצרין (חומר הלחה) וסירופ סורביטול — לא אפייה. שמן דקל+חמניות, 29.7 גרם סוכר, 11.4 גרם שומן רווי. צימוקים כנגיעה. E450, E500.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "גליצרין (E422) וסירופ סורביטול כחומרי לחות — מה שמסביר את המרקם. שמן דקל+חמניות, E450, E500."},
        {"dimension": "glycemic_quality", "score": 20, "label_he": "עומס גליקמי", "explanation_he": "29.7 גרם סוכר ל-100 גרם. סירופ גלוקוז, דקסטרוז ברשימה — שלושה מקורות פחמימה מהירה."},
        {"dimension": "additive_quality", "score": 25, "label_he": "תוספים", "explanation_he": "גליצרין, סורביטול, E450, E500 — ארבעה תוספים."},
        {"dimension": "calorie_density", "score": 25, "label_he": "צפיפות קלורית", "explanation_he": "481 קק\"ל ו-11.4 גרם שומן רווי — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7622210453327": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מילקה סנסיישן — E1414, נתרן 352 מ\"ג, סוכר 39 גרם.",
    "rowVerdict": "עוגיות מילקה סנסיישן מגיעות ל-E עם 39 גרם סוכר, 9 גרם שומן רווי ו-352 מ\"ג נתרן ל-100 גרם — גבוה מאוד לעוגייה מתוקה. E1414 (עמילן מפורק) הוא עמילן מטופל שמשמש לשיפור מרקם. שומן חלב, עיסת קקאו, חמאת קקאו — קקאו אמיתי.",
    "bottomLine": "נתרן 352 מ\"ג וסוכר 39 גרם — שניהם גבוהים לעוגייה.",
    "consumerTakeaway": "E1414, נתרן 352 מ\"ג וסוכר 39 גרם — שניים גבוהים בשילוב.",
    "consumerExplanation": "נתרן 352 מ\"ג ל-100 גרם גבוה לעוגייה מתוקה. E1414 (עמילן מפורק) משמש לשיפור מרקם ותחושת פה. עיסת קקאו וחמאת קקאו — קקאו אמיתי בכמות לא ידועה. E450, E500, E503, לציטין.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 22, "label_he": "איכות עיבוד", "explanation_he": "E1414 (עמילן מטופל), E450, E500, E503, לציטין, צבע מאכל E160a. שומן חלב, עיסת קקאו."},
        {"dimension": "glycemic_quality", "score": 15, "label_he": "עומס גליקמי", "explanation_he": "39 גרם סוכר ל-100 גרם — גבוה מאוד. E1414 מוסיף לעומס."},
        {"dimension": "additive_quality", "score": 22, "label_he": "תוספים", "explanation_he": "E1414, E450, E500, E503, לציטין, E160a — שישה תוספים."},
        {"dimension": "calorie_density", "score": 18, "label_he": "צפיפות קלורית", "explanation_he": "9 גרם שומן רווי ו-510 קק\"ל — גבוה."}
    ],
    "bestUseCases": ["כיבוד חד-פעמי"]
},

"ck-7290101111986": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עינוגים קוקיס — ביסקוויט 41% בקרם קפוא, שמן קוקוס מוקשה.",
    "rowVerdict": "עינוגים קוקיס מגיעות ל-E. הביסקוויט 41% מוטבע בקרם שמכיל שמן קוקוס מוקשה וקוקוס מוקשה — שניהם שומן רווי גבוה. 8.7 גרם שומן רווי, 25.2 גרם סוכר ו-E471, E410, E412. 281 קק\"ל ל-100 גרם — נמוך יחסית בגלל תכולת מים.",
    "bottomLine": "שמן קוקוס מוקשה בקרם — 8.7 גרם שומן רווי, 25 גרם סוכר.",
    "consumerTakeaway": "ביסקוויט בקרם עם שמן קוקוס מוקשה — 25 גרם סוכר, שומן רווי גבוה.",
    "consumerExplanation": "ביסקוויט 41% עם שוקולד מכיל E503, E500, לציטין סויה. הקרם מכיל מים, שמן קוקוס מוקשה, חמאה, שומן חלב, E471, E410, E412. שמן קוקוס מוקשה הוא מקור לשומן רווי גבוה. 25.2 גרם סוכר.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 20, "label_he": "איכות עיבוד", "explanation_he": "שמן קוקוס מוקשה וקוקוס מוקשה בקרם, E471, E410, E412 כמייצבים. ביסקוויט עם E503, E500."},
        {"dimension": "glycemic_quality", "score": 22, "label_he": "עומס גליקמי", "explanation_he": "25.2 גרם סוכר ל-100 גרם. 'סוכרים' כרכיב שלישי בביסקוויט."},
        {"dimension": "additive_quality", "score": 20, "label_he": "תוספים", "explanation_he": "E471, E410, E412 בקרם + E503, E500, לציטין בביסקוויט — שישה תוספים."},
        {"dimension": "calorie_density", "score": 40, "label_he": "צפיפות קלורית", "explanation_he": "281 קק\"ל ל-100 גרם — בינוני בגלל תכולת מים בקרם. 8.7 גרם שומן רווי."}
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
print("Saved batch 6.")
