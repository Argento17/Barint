import json

with open('C:/Bari/bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

PARTIAL_LABEL = "ניתוח חלקי"
PARTIAL_TOOLTIP = "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים."
PARTIAL_SUB = "missing_nutrition"

VERIFIED_LABEL = "מבוסס על נתונים מלאים"
VERIFIED_TOOLTIP = "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים."

copy_data = {

"ck-7290020030184": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות זעתר עם נתרן גבוה — ללא סוכר, עם מתחלב תעשייתי.",
    "rowVerdict": "עוגיות הזעתר של אחוה מגיעות ל-C בזכות אפס סוכר ושומן רווי נמוך. הבעיה היא נתרן גבוה — 730 מ\"ג ל-100 גרם — ו-E491, מתחלב תעשייתי שאינו מופיע בעוגיות ביתיות. הציון נגזר מהפרופיל הכולל.",
    "bottomLine": "פרופיל מלוח יחסית למראה; עדיף לצרוך במינון.",
    "consumerTakeaway": "עוגיות ללא סוכר עם נתרן גבוה ומתחלב תעשייתי.",
    "consumerExplanation": "הזעתר מציע טעם אמיתי, אבל 730 מ\"ג נתרן ל-100 גרם הופכות כל מנה לגבוהה בנתרן. שמן צמחי כללי ו-E491 מסיימים את הפרופיל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 55, "label_he": "איכות עיבוד", "explanation_he": "קמח חיטה, שמרים ושומשום — פשוט יחסית. E491 הוא מתחלב תעשייתי שאינו נחוץ בעוגייה עם שישה רכיבים."},
        {"dimension": "glycemic_quality", "score": 90, "label_he": "עומס גליקמי", "explanation_he": "אפס סוכר — הדגל הירוק הבודד. קמח לבן הוא עדיין פחמימן זמין, אבל ללא תוספת סוכר הציון טוב."},
        {"dimension": "additive_quality", "score": 45, "label_he": "תוספים", "explanation_he": "E491 משמש לייצוב מרקם; אין עדות לנזק, אבל אין לו מקום בעוגייה פשוטה."},
        {"dimension": "calorie_density", "score": 50, "label_he": "צפיפות קלורית", "explanation_he": "צפיפות קלורית בינונית לקטגוריה — הנתרן הוא הגורם המגביל יותר מהקלוריות."}
    ],
    "bestUseCases": ["כיבוד על מדף עם גבינה צהובה", "אלטרנטיבה מלוחה לעוגיות מתוקות"]
},

"ck-7290122781359": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "61% קמח מלא — שומן רווי נמוך מאוד לקטגוריה.",
    "rowVerdict": "מיני עוגיות פיטנס קלאסי מגיעות ל-C עם 61% קמח מלא וסוכר נמוך של 4.6 גרם ל-100 גרם. שומן הרווי נמוך במיוחד. גלוטן חיטה מוסף ושלושה חומרי תפיחה כימיים מסמנים עיבוד תעשייתי, לא אפייה פשוטה.",
    "bottomLine": "קמח מלא כרכיב ראשון — נדיר בקטגוריה. חומרי תפיחה מרובים.",
    "consumerTakeaway": "קמח מלא כרכיב עיקרי, סוכר נמוך מאוד, שומן רווי מינימלי.",
    "consumerExplanation": "61% קמח מלא ו-4.6 גרם סוכר יוצאי דופן בקטגוריית הביסקוויט. שומן הרווי של 0.4 גרם בלבד הוא הנמוך ביותר בין המוצרים שנסקרו. שלושה חומרי תפיחה (E503, E500, E450) הם הסייג.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 58, "label_he": "איכות עיבוד", "explanation_he": "61% קמח מלא כרכיב ראשון. גלוטן מוסף ושלושה חומרי תפיחה מורידים את הציון."},
        {"dimension": "glycemic_quality", "score": 72, "label_he": "עומס גליקמי", "explanation_he": "4.6 גרם סוכר — נמוך מאוד לעוגייה. שיבולת שועל וסיבים מוסיפים להאטת הספיגה."},
        {"dimension": "additive_quality", "score": 42, "label_he": "תוספים", "explanation_he": "שלושה חומרי תפיחה, לציטין סויה ועמילן — יותר תוספים ממה שמצופה בפרופיל זה."},
        {"dimension": "calorie_density", "score": 50, "label_he": "צפיפות קלורית", "explanation_he": "נתוני הקלוריות חסרים; שומן רווי 0.4 גרם מסמן צפיפות נמוכה יחסית לקטגוריה."}
    ],
    "bestUseCases": ["חטיף בוקר עם קפה כאלטרנטיבה לעוגייה מתוקה", "ילדים שצורכים פחות סוכר"]
},

"ck-7290013453068": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "34% כוסמין מלא עם פירות יער 8% — שומן רווי 6.1 גרם.",
    "rowVerdict": "עוגיות הכוסמין פירות יער מגיעות ל-C עם בסיס קמח מלא ופירות יער אמיתיים ב-8%. שמן קנולה כמקור השומן הראשי הוא בחירה סבירה. הסייג: שומן רווי של 6.1 גרם ל-100 גרם — גבוה יחסית לפרופיל הכולל. נתון הסוכר לא אומת.",
    "bottomLine": "כוסמין מלא ופירות יער בפועל — שומן רווי גבוה מהמצופה.",
    "consumerTakeaway": "כוסמין מלא ופירות יער אמיתיים, שומן רווי גבוה יחסית.",
    "consumerExplanation": "34% קמח כוסמין מלא ו-8% פירות יער הם יתרון אמיתי. שמן קנולה כמקור שומן ראשי הוא בחירה נסבלת. 6.1 גרם שומן רווי ל-100 גרם גבוה לפרופיל שמציג את עצמו כ'בריאותי'. נתון הסוכר חסר.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 60, "label_he": "איכות עיבוד", "explanation_he": "כוסמין מלא, שיבולת שועל ופירות יער עם ממתיקים טבעיים (אגבה, מונק פרוט). מעובד אך לא תעשייתי קיצוני."},
        {"dimension": "glycemic_quality", "score": 65, "label_he": "עומס גליקמי", "explanation_he": "ממתיקים אגבה ומונק פרוט מגיעים עם אינדקס גליקמי נמוך יותר מסוכר. נתון הסוכר חסר לאימות מלא."},
        {"dimension": "additive_quality", "score": 55, "label_he": "תוספים", "explanation_he": "רשימת רכיבים נקייה יחסית — ללא מתחלבים תעשייתיים מיותרים."},
        {"dimension": "calorie_density", "score": 42, "label_he": "צפיפות קלורית", "explanation_he": "24.4 גרם שומן כולל עם שומן רווי 6.1 גרם מעלים את הצפיפות הקלורית."}
    ],
    "bestUseCases": ["חטיף לארוחת עשר", "כיבוד לאוהבי מוצרים עם דגנים מלאים"]
},

"ck-7290119043149": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "שמנים מוקשים חלקית — שומן רווי 8 גרם ל-100 גרם.",
    "rowVerdict": "עוגיות בטעם חמאה מגיעות ל-D עם שומן רווי של 8 גרם ל-100 גרם ורכיבים שמצהירים במפורש על 'שמנים ושומנים מהצומח, חלקם מוקשים'. 'בטעם חמאה' בשם הוא תיאור ריח, לא חמאה בפועל.",
    "bottomLine": "שמנים מוקשים חלקית ושומן רווי גבוה — ללא חמאה אמיתית.",
    "consumerTakeaway": "שמנים מוקשים חלקית ושומן רווי גבוה. בלי חמאה אמיתית.",
    "consumerExplanation": "הכיתוב 'בטעם חמאה' מסווה שמנים צמחיים מוקשים חלקית כמקור שומן. 8 גרם שומן רווי ל-100 גרם גבוה לביסקוויט פשוט. גלוקוזה וחומרי תפיחה כימיים משלימים את הפרופיל התעשייתי.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 35, "label_he": "איכות עיבוד", "explanation_he": "שמנים מוקשים חלקית — מסמן עיבוד תעשייתי גבוה. קמח לבן, גלוקוזה וחומרי תפיחה."},
        {"dimension": "glycemic_quality", "score": 55, "label_he": "עומס גליקמי", "explanation_he": "נתון הסוכר חסר. גלוקוזה ברכיבים מסמנת תוספת סוכר מהיר."},
        {"dimension": "additive_quality", "score": 40, "label_he": "תוספים", "explanation_he": "E450 ו-E500 — חומרי תפיחה נפוצים. מאפיינים עיבוד תעשייתי."},
        {"dimension": "calorie_density", "score": 40, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 8 גרם מסמן צפיפות קלורית גבוהה לקטגוריה."}
    ],
    "bestUseCases": ["מנת חטיף קטנה כשאין אלטרנטיבה"]
},

"ck-7290013156921": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "ללא סוכר עם מרגרינה — שומן רווי 9.5 גרם ל-100 גרם.",
    "rowVerdict": "עוגיות גאקובס ללא סוכר מגיעות ל-D. מרגרינה כרכיב שני ושומן רווי של 9.5 גרם ל-100 גרם מוחקים את היתרון של הסרת הסוכר. מלטיטול (E965) ידוע בתופעות עיכול במינון גבוה.",
    "bottomLine": "אפס סוכר לא מפצה על מרגרינה כמקור שומן ושומן רווי גבוה.",
    "consumerTakeaway": "הסרת סוכר הוסיפה מרגרינה — הציון משקף את העסקה הזו.",
    "consumerExplanation": "מרגרינה כרכיב שני עם שומן רווי של 9.5 גרם ל-100 גרם הופכת את הפיצוי לאשלייתי. מלטיטול עלול לגרום לאי-נוחות עיכולית בצריכה גבוהה.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה כרכיב שני — שומן תעשייתי מוקשה. E965, E450, E500 — רמת עיבוד גבוהה."},
        {"dimension": "glycemic_quality", "score": 70, "label_he": "עומס גליקמי", "explanation_he": "אפס סוכר — יתרון מדיד. מלטיטול מגיע עם אינדקס גליקמי נמוך יותר מסוכר."},
        {"dimension": "additive_quality", "score": 35, "label_he": "תוספים", "explanation_he": "E965 (מלטיטול), E450, E500. מלטיטול במינון גבוה ידוע בתופעות עיכול."},
        {"dimension": "calorie_density", "score": 30, "label_he": "צפיפות קלורית", "explanation_he": "שומן רווי 9.5 גרם מסמן צפיפות קלורית גבוהה — מרגרינה צפופה כמו חמאה."}
    ],
    "bestUseCases": ["סוכרתיים שמחפשים אפשרות מוגבלת ביחידה אחת"]
},

"ck-7290000061245": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "8% שוקולד מריר, סוכר כרכיב ראשון, 36% מילוי.",
    "rowVerdict": "עוגיות שוקוצ'יפס ממולאות אסם מגיעות ל-D. סוכר הוא הרכיב הראשון, לפני הקמח. 36% מהמוצר הוא מילוי. נתוני 6.2 גרם סוכר ו-2.2 גרם שומן רווי נמדדו ליחידה, לא ל-100 גרם — מה שמעמעם את הפרופיל האמיתי.",
    "bottomLine": "סוכר לפני קמח ברשימה; 36% מילוי; נתונים ליחידה בלבד.",
    "consumerTakeaway": "סוכר כרכיב ראשון; 36% מילוי; נתוני תזונה ליחידה.",
    "consumerExplanation": "כש-36% מהמוצר הוא מילוי וסוכר עומד ראשון ברשימת הרכיבים, הפרופיל הוא של ממתק. הנתונים הנמוכים לכאורה (6.2 גרם סוכר) משקפים יחידה בודדת, לא 100 גרם.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 32, "label_he": "איכות עיבוד", "explanation_he": "סוכר כרכיב ראשון; E500, E503, לציטין סויה — מוצר ייצור מסיבי."},
        {"dimension": "glycemic_quality", "score": 40, "label_he": "עומס גליקמי", "explanation_he": "סוכר ראשון ועמילנים ברשימה — עומס גליקמי גבוה גם אם הנתון ליחידה נראה נמוך."},
        {"dimension": "additive_quality", "score": 42, "label_he": "תוספים", "explanation_he": "E500 ו-E503, לציטין כמתחלב — מסמן עיבוד תעשייתי."},
        {"dimension": "calorie_density", "score": 40, "label_he": "צפיפות קלורית", "explanation_he": "נתוני 100 גרם לא אומתו; 97 קק\"ל ליחידה מסמן צפיפות לא נמוכה."}
    ],
    "bestUseCases": ["כיבוד לילדים במנה מוגבלת"]
},

"ck-7290013740014": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "11% שוקולד מריר — סוכר 23.6 גרם ושומן רווי 9.5 גרם ל-100 גרם.",
    "rowVerdict": "עוגיות שוקוצ'יפס של שופרסל מגיעות ל-D עם 23.6 גרם סוכר ו-9.5 גרם שומן רווי ל-100 גרם. שניהם חוצים סף משמעותי. 11% שוקולד מריר אמיתי הוא יתרון שלא מכסה על הפרופיל הכולל.",
    "bottomLine": "סוכר ושומן רווי גבוהים — גם עם שוקולד מריר בפועל.",
    "consumerTakeaway": "שוקולד מריר 11% אמיתי, אבל סוכר ושומן רווי גבוהים.",
    "consumerExplanation": "11% שוקולד מריר מציע גוון קקאו אמיתי. 23.6 גרם סוכר ו-9.5 גרם שומן רווי ל-100 גרם הם שני גורמים מגבילים. ביצים כרכיב שלישי — אינדיקטור לאיכות בצק.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 40, "label_he": "איכות עיבוד", "explanation_he": "קמח חיטה, ביצים ושוקולד מריר — רכיבים מוכרים ורשימה קצרה יחסית."},
        {"dimension": "glycemic_quality", "score": 35, "label_he": "עומס גליקמי", "explanation_he": "23.6 גרם סוכר ל-100 גרם גבוה. קמח לבן כבסיס מחמיר את הפרופיל."},
        {"dimension": "additive_quality", "score": 55, "label_he": "תוספים", "explanation_he": "רשימה קצרה יחסית ללא מתחלבים מרובים."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "9.5 גרם שומן רווי מסמן עושר קלורי גבוה."}
    ],
    "bestUseCases": ["כיבוד בכמות מוגבלת עם קפה"]
},

"ck-7290013156006": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "מרגרינה כרכיב שני — סוכר 18 גרם ושומן רווי 8.8 גרם.",
    "rowVerdict": "עוגיות מיני מרוקאיות של בקה מגיעות ל-D. מרגרינה עומדת כרכיב שני — שומן תעשייתי לפני ביצים וסוכר. 8.8 גרם שומן רווי ו-18 גרם סוכר ל-100 גרם מסמנים D ברור. המראה הביתי-מרוקאי לא משנה את הרכב הרכיבים.",
    "bottomLine": "מרגרינה כרכיב שני — הפרופיל הכולל הוא D.",
    "consumerTakeaway": "מרגרינה כרכיב שני, סוכר גבוה — עוגייה מרוקאית תעשייתית.",
    "consumerExplanation": "מרגרינה כרכיב שני (לפני ביצים) היא גורם מגביל. 18 גרם סוכר ו-8.8 גרם שומן רווי ל-100 גרם חוצים שני ספים. E450 ו-E500 מסיימים את הפרופיל.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 28, "label_he": "איכות עיבוד", "explanation_he": "מרגרינה כרכיב שני — שומן צמחי מוקשה שעבר עיבוד תעשייתי."},
        {"dimension": "glycemic_quality", "score": 38, "label_he": "עומס גליקמי", "explanation_he": "18 גרם סוכר ל-100 גרם — חוצה את הסף. קמח לבן כבסיס."},
        {"dimension": "additive_quality", "score": 38, "label_he": "תוספים", "explanation_he": "E450 ו-E500 — חומרי תפיחה נפוצים. מאפיינים ייצור תעשייתי."},
        {"dimension": "calorie_density", "score": 35, "label_he": "צפיפות קלורית", "explanation_he": "מרגרינה ושומן רווי 8.8 גרם מסמנים צפיפות קלורית גבוהה."}
    ],
    "bestUseCases": ["כיבוד קפה במנה קטנה"]
},

"ck-313184": {
    "cl": PARTIAL_LABEL, "ct": PARTIAL_TOOLTIP, "cs": PARTIAL_SUB,
    "insightLine": "עוגיות חיות ילדים — 17.5 גרם סוכר ורכיבים תעשייתיים.",
    "rowVerdict": "עוגיות גן חיות מגיעות ל-E. הצורות מושכות אבל הפרופיל תעשייתי: שמנים צמחיים כלליים, סוכר אינברטי, E500, E503, לציטין סויה, מיצוי רוזמרין וסולפיט — ו-17.5 גרם סוכר ל-100 גרם, ממש על הסף.",
    "bottomLine": "עיצוב ילדים לא משנה את הפרופיל — E לכל הדעות.",
    "consumerTakeaway": "עוגיית ילדים תעשייתית עם 17.5 גרם סוכר וסולפיט ברשימה.",
    "consumerExplanation": "סוכר אינברטי לצד סוכר רגיל, שמנים צמחיים כלליים וסולפיט — פרופיל של מוצר ייצור מסיבי. 17.5 גרם סוכר ל-100 גרם בדיוק על הסף.",
    "bariInterpretation": [
        {"dimension": "processing_quality", "score": 30, "label_he": "איכות עיבוד", "explanation_he": "שמנים צמחיים לא מפורטים, סוכר אינברטי, מיצוי רוזמרין כאנטי-חמצון, סולפיט — פרופיל תעשייתי מובהק."},
        {"dimension": "glycemic_quality", "score": 38, "label_he": "עומס גליקמי", "explanation_he": "17.5 גרם סוכר ל-100 גרם — על הגבול. שילוב סוכר רגיל וסוכר אינברטי מגביר את העומס הגליקמי."},
        {"dimension": "additive_quality", "score": 30, "label_he": "תוספים", "explanation_he": "E500, E503, לציטין, מיצוי רוזמרין וסולפיט — חמישה תוספים. הסולפיט מסומן כאלרגן."},
        {"dimension": "calorie_density", "score": 40, "label_he": "צפיפות קלורית", "explanation_he": "שמנים צמחיים ושומן רווי 2.9 גרם — צפיפות קלורית בינונית."}
    ],
    "bestUseCases": ["כיבוד לילדים פעם בשבוע במנה מוגבלת"]
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
print("Saved batch 1.")
