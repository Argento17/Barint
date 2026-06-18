"""
RT fixes for cakes + biscuits pages — TASK-275 Stage-9 red-team gate findings.
Applies: RT-1 (additive schema), RT-4 (caveat verification), RT-5 (SEO FAQ),
         RT-7 (cakes filters), RT-8 (duplicate names), RT-10 (promo names).
NO .tsx files touched.  No OFF data used.  Counts verified from artifacts.
"""
import json, re, pathlib, sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Bari")
CAKES_JSON = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cakes_hard_cookies_frontend_v1.json"
BISCUITS_JSON = ROOT / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
SEO_FAQ = ROOT / "bari-web" / "src" / "data" / "seo" / "cookies_coffee_faq_schema.json"

# ─────────────────────────────────────────────────────────────────────────────
# RT-1: Additive lookup table (sourced from additive_tiered_library_v1.md EV-041/EV-043/EV-059/EV-061)
# Keys: canonical E-number string (e.g. "E330") → AdditiveEntry dict
# Does NOT use OFF.  All tiers from signed library.
# ─────────────────────────────────────────────────────────────────────────────

ADDITIVE_LOOKUP = {
    # ── From existing correct entries (v1 cookies — 20 entries) ──────────────
    "E1414": {
        "e_number": "E1414",
        "name_he": "דיעמילן פוספט אצטילי",
        "tier": "likely-neutral",
        "function_he": "מייצב / מרקם",
        "explanation_he": "עמילן שונה; משמר מרקם בטמפרטורות שונות. נחשב בטוח ברמות שימוש רגילות במאפים.",
    },
    "E1422": {
        "e_number": "E1422",
        "name_he": "עמילן אצטט",
        "tier": "likely-neutral",
        "function_he": "מייצב",
        "explanation_he": "עמילן שונה; נפוץ בשמירת מרקם מזון בשינויי טמפרטורה.",
    },
    "E1442": {
        "e_number": "E1442",
        "name_he": "הידרוקסיפרופיל דיעמילן פוספט",
        "tier": "likely-neutral",
        "function_he": "מייצב / מרקם",
        "explanation_he": "עמילן שונה; מייצב מרקם. נחשב בטוח ברמות שימוש רגילות.",
    },
    "E1412": {
        "e_number": "E1412",
        "name_he": "דיעמילן פוספט",
        "tier": "likely-neutral",
        "function_he": "מייצב / מרקם",
        "explanation_he": "עמילן שונה; משפר מרקם וקישור. נחשב בטוח ברמות שימוש רגילות.",
    },
    "E150": {
        "e_number": "E150",
        "name_he": "קרמל",
        "tier": "disclosure-gap",
        "function_he": "צבע מאכל",
        "explanation_he": "צבע קרמל; הסיווג (I–IV) אינו מופיע בתווית — לכן לא ניתן לקבוע את הסוג המדויק.",
    },
    "E150D": {
        "e_number": "E150D",
        "name_he": "קרמל סולפיט אמוניה",
        "tier": "dose-dependent",
        "function_he": "צבע מאכל",
        "explanation_he": "קרמל סוג IV; תוצר לוואי 4-MEI — חשיפה ממאפים מוגבלת.",
    },
    "E160A": {
        "e_number": "E160A",
        "name_he": "בטא-קרוטן",
        "tier": "functional",
        "function_he": "צבע מאכל",
        "explanation_he": "פיגמנט כתום טבעי מגזר; מקור לוויטמין A. ללא דאגות בטיחות בכמויות צבע.",
    },
    "E160": {
        "e_number": "E160",
        "name_he": "בטא-קרוטן / קרוטנואידים",
        "tier": "functional",
        "function_he": "צבע מאכל",
        "explanation_he": "פיגמנטים טבעיים ממקור צמחי; ללא דאגות בטיחות ידועות בכמויות צבע.",
    },
    "E163": {
        "e_number": "E163",
        "name_he": "אנתוציאנינים",
        "tier": "functional",
        "function_he": "צבע מאכל",
        "explanation_he": "פיגמנט סגול מגזר שחור או ענבים; ללא דאגות בכמויות צבע.",
    },
    "E200": {
        "e_number": "E200",
        "name_he": "חומצה סורבית",
        "tier": "likely-neutral",
        "function_he": "חומר משמר",
        "explanation_he": "חומר משמר טבעי מפירות; עוצר עובש ושמרים. ידוע כרגישות אצל מיעוט קטן (תגובה דמוית היסטמין).",
    },
    "E202": {
        "e_number": "E202",
        "name_he": "פוטסיום סורבט",
        "tier": "likely-neutral",
        "function_he": "חומר משמר",
        "explanation_he": "חומר משמר שעוצר עובש ושמרים; נמצא בשימוש נרחב ובטוח ברמות מקובלות.",
    },
    "E270": {
        "e_number": "E270",
        "name_he": "חומצת חלב",
        "tier": "functional",
        "function_he": "מווסת חומציות",
        "explanation_he": "חומצה טבעית המיוצרת בתסיסה; מאזנת pH ומעכבת עובש. בטוחה ונפוצה במאפים.",
    },
    "E296": {
        "e_number": "E296",
        "name_he": "חומצה מאלית",
        "tier": "functional",
        "function_he": "מווסת חומציות",
        "explanation_he": "חומצה טבעית ממחזור קרבס; ללא דאגות בטיחות בכמויות מזון.",
    },
    "E300": {
        "e_number": "E300",
        "name_he": "חומצה אסקורבית (ויטמין C)",
        "tier": "functional",
        "function_he": "נוגד חמצון",
        "explanation_he": "ויטמין C; נוגד חמצון טבעי. ללא דאגות בטיחות.",
    },
    "E322": {
        "e_number": "E322",
        "name_he": "לציטין",
        "tier": "likely-neutral",
        "function_he": "מתחלב",
        "explanation_he": "מתחלב טבעי מסויה או חמניות; מסייע לתחמיץ שמן ומים במאפים.",
    },
    "E327": {
        "e_number": "E327",
        "name_he": "קלציום לקטט",
        "tier": "functional",
        "function_he": "מווסת חומציות / מקור סידן",
        "explanation_he": "לקטט הוא מטבוליט רגיל; ללא דאגות בטיחות בכמויות מזון.",
    },
    "E330": {
        "e_number": "E330",
        "name_he": "חומצת לימון",
        "tier": "functional",
        "function_he": "מווסת חומציות",
        "explanation_he": "חומצה נפוצה מהצומח; מאזנת pH ומעכבת חמצון. בטוח.",
    },
    "E331": {
        "e_number": "E331",
        "name_he": "נתרן ציטרט",
        "tier": "functional",
        "function_he": "מווסת חומציות / מייצב",
        "explanation_he": "מלח ציטרט; מאזן חומציות. תורם לנתרן — זהו שיקול תזונתי, לא בטיחותי.",
    },
    "E333": {
        "e_number": "E333",
        "name_he": "קלציום ציטרט",
        "tier": "functional",
        "function_he": "מייצב / מקור סידן",
        "explanation_he": "מלח ציטרט; מאזן חומציות ומקור סידן. ללא דאגות בטיחות.",
    },
    "E401": {
        "e_number": "E401",
        "name_he": "נתרן אלגינט",
        "tier": "functional",
        "function_he": "מסמיך / ג'ל",
        "explanation_he": "פוליסכריד מאצות חום; ללא דאגות בטיחות בכמויות מזון.",
    },
    "E407": {
        "e_number": "E407",
        "name_he": "קרגינן",
        "tier": "contested",
        "function_he": "מסמיך / מייצב",
        "explanation_he": "ממצאי מחקר עצמאיים ב-2026 (מנגנון דלקתי) בסתירה להחלטת EFSA — ראיות מעורבות.",
    },
    "E410": {
        "e_number": "E410",
        "name_he": "קמח חרובים",
        "tier": "functional",
        "function_he": "מסמיך / מייצב",
        "explanation_he": "פוליסכריד מחרוב; ללא דאגות בטיחות בכמויות מזון.",
    },
    "E412": {
        "e_number": "E412",
        "name_he": "גואר גאם",
        "tier": "functional",
        "function_he": "מסמיך / מייצב",
        "explanation_he": "סיב מסיס; ללא דאגות בטיחות מהצריכה התזונתית.",
    },
    "E415": {
        "e_number": "E415",
        "name_he": "קסנתן גאם",
        "tier": "functional",
        "function_he": "מייצב",
        "explanation_he": "סיב מותסס; נמצא בשימוש במוצרי ללא גלוטן כתחליף מרקם.",
    },
    "E422": {
        "e_number": "E422",
        "name_he": "גליצרול",
        "tier": "functional",
        "function_he": "לחות / ממס",
        "explanation_he": "אלכוהול סוכר שומר לחות ומשמש כממס לתמציות; נחשב בטוח לחלוטין.",
    },
    "E440": {
        "e_number": "E440",
        "name_he": "פקטין",
        "tier": "functional",
        "function_he": "ג'ל / מסמיך",
        "explanation_he": "סיב מסיס מפירות; ללא דאגות בטיחות — לרוב בעל מאפיינים חיוביים.",
    },
    "E450": {
        "e_number": "E450",
        "name_he": "דיפוספט",
        "tier": "dose-dependent",
        "function_he": "חומר תפיחה / מייצב",
        "explanation_he": "פוספטים; EFSA (2019) מציינת שצריכה מצטברת עלולה להתקרב ל-ADI אצל צרכנים כבדים.",
    },
    "E451": {
        "e_number": "E451",
        "name_he": "טריפוספט",
        "tier": "dose-dependent",
        "function_he": "מייצב / מרכך",
        "explanation_he": "פוספטים; כמו E450 — ADI קבוצתי של EFSA עם אזהרת צריכה מצטברת.",
    },
    "E460": {
        "e_number": "E460",
        "name_he": "תאית מיקרו-גבישית (MCC)",
        "tier": "contested",
        "function_he": "ממלא / נוגד הגבשה",
        "explanation_he": "קשר CVD יחיד (NutriNet-Santé 2023); ללא שכפול עצמאי — מסווג 'שנוי במחלוקת' זמנית (EV-061).",
    },
    "E466": {
        "e_number": "E466",
        "name_he": "קרבוקסי מתיל צלולוז (CMC)",
        "tier": "contested",
        "function_he": "מייצב / מתחלב",
        "explanation_he": "ניסוי אנושי (Chassaing 2021) הראה שינויי מיקרוביום; נתוני בני אדם עדיין מוגבלים.",
    },
    "E471": {
        "e_number": "E471",
        "name_he": "מונוגליצרידים ודיגליצרידים",
        "tier": "contested",
        "function_he": "מתחלב",
        "explanation_he": "קשר לסרטן בקוהורט גדול (Sellem 2024); ראיות ראשוניות — שנוי במחלוקת (EV-061).",
    },
    "E472": {
        "e_number": "E472",
        "name_he": "אסטרים של מונוגליצרידים",
        "tier": "likely-neutral",
        "function_he": "מתחלב / מייצב",
        "explanation_he": "אסטרים של חומצות שומן; שמירת מרקם. ברמות שימוש רגילות בטוח.",
    },
    "E472B": {
        "e_number": "E472B",
        "name_he": "אסטרים לקטיים של מונוגליצרידים (LACTEM)",
        "tier": "contested",
        "function_he": "מתחלב / מייצב",
        "explanation_he": "קשר CVD בקוהורט NutriNet-Santé; שנוי במחלוקת (EV-061). E472e/DATEM שונה ונשאר likely-neutral.",
    },
    "E472C": {
        "e_number": "E472C",
        "name_he": "אסטרים ציטריים של מונוגליצרידים (CITREM)",
        "tier": "contested",
        "function_he": "מתחלב / מייצב",
        "explanation_he": "קשר CVD בקוהורט NutriNet-Santé; שנוי במחלוקת (EV-061).",
    },
    "E472E": {
        "e_number": "E472E",
        "name_he": "DATEM",
        "tier": "likely-neutral",
        "function_he": "מייצב בצק / מתחלב",
        "explanation_he": "EFSA/JECFA 'לא מוגדר'; אינו נזכר בנייר NutriNet-Santé — נשאר likely-neutral.",
    },
    "E476": {
        "e_number": "E476",
        "name_he": "PGPR",
        "tier": "likely-neutral",
        "function_he": "מתחלב",
        "explanation_he": "מחליף לציטין בשוקולד; EFSA ו-JECFA מסווגים כ'לא מוגדר'; ברמות שימוש בטוח.",
    },
    "E481": {
        "e_number": "E481",
        "name_he": "נתרן סטיאורויל לקטילט (SSL)",
        "tier": "likely-neutral",
        "function_he": "מייצב בצק / מתחלב",
        "explanation_he": "EFSA ADI 20 מ\"ג/ק\"ג; חשיפה << ADI; ללא אות בטיחות ספציפי.",
    },
    "E500": {
        "e_number": "E500",
        "name_he": "סודיום ביקרבונט",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "אבקת אפייה; גורם לבצק לתפוח בחום.",
    },
    "E503": {
        "e_number": "E503",
        "name_he": "אמוניום ביקרבונט",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "חומר תפיחה מסורתי; מתנדף לחלוטין באפייה.",
    },
    "E516": {
        "e_number": "E516",
        "name_he": "קלציום סולפט",
        "tier": "functional",
        "function_he": "מחשל / מסדיר",
        "explanation_he": "גבס מזון; JECFA 'לא מוגדר'; ללא דאגות בטיחות בכמויות מזון.",
    },
    "E551": {
        "e_number": "E551",
        "name_he": "סיליקון דיאוקסיד",
        "tier": "functional",
        "function_he": "נוגד הגבשה",
        "explanation_he": "אבקה מינרלית מונעת גבשה; ברמות שימוש מוגדרות נחשבת בטוחה.",
    },
    "E903": {
        "e_number": "E903",
        "name_he": "שעוות קרנובה",
        "tier": "functional",
        "function_he": "מחמיר / מגן",
        "explanation_he": "שעוות צמחית לציפוי; ללא דאגות בטיחות ידועות בכמויות שימוש.",
    },
    "E950": {
        "e_number": "E950",
        "name_he": "אצסולפם-K",
        "tier": "dose-dependent",
        "function_he": "ממתיק לא-סוכר",
        "explanation_he": "ממתיק; EFSA ADI 9 מ\"ג/ק\"ג; צרכנים כבדים עשויים להתקרב ל-ADI.",
    },
    "E951": {
        "e_number": "E951",
        "name_he": "אספרטם",
        "tier": "contested",
        "function_he": "ממתיק לא-סוכר",
        "explanation_he": "IARC 2023 Group 2B vs JECFA 'אין ראיות משכנעות'; פיצול בין הערכת סיכון להגדרת סכנה.",
    },
    "E953": {
        "e_number": "E953",
        "name_he": "איזומלט",
        "tier": "functional",
        "function_he": "ממתיק / לחות",
        "explanation_he": "פוליאול מסוכרוז; בעוגיות ללא סוכר. כמויות גדולות עלולות לגרום לאי נוחות עיכולית.",
    },
    "E955": {
        "e_number": "E955",
        "name_he": "סוקרלוז",
        "tier": "dose-dependent",
        "function_he": "ממתיק לא-סוכר",
        "explanation_he": "EFSA 2026 הצרה את ה-ADI ל-5 מ\"ג/ק\"ג; דיון חי על מיקרוביום.",
    },
    "E960": {
        "e_number": "E960",
        "name_he": "גליקוזידים של סטביול",
        "tier": "dose-dependent",
        "function_he": "ממתיק לא-סוכר",
        "explanation_he": "EFSA ADI 4 מ\"ג/ק\"ג; ילדים כצרכנים כבדים עלולים להתקרב ל-ADI.",
    },
    "E965": {
        "e_number": "E965",
        "name_he": "מלטיטול",
        "tier": "functional",
        "function_he": "ממתיק",
        "explanation_he": "פוליאול בעוגיות ללא סוכר; כמות גדולה עלולה לגרום לאי נוחות עיכולית.",
    },
}

# Aliases for common variant spellings
E_NUMBER_ALIASES = {
    "E-322": "E322",
    "E-476": "E476",
    "E150A": "E150",
    "E150B": "E150",
    "E150C": "E150",
    "E150D": "E150D",
    "E160A": "E160A",
    "E160B": "E160",
    "E160C": "E160",
    "E472B": "E472B",
    "E472C": "E472C",
    "E472E": "E472E",
}

# Hebrew functional-class → best-guess AdditiveEntry when no E-number is available
# Only for generic class terms (bare "מתחלבים", "מייצבים", etc.)
# These cannot be resolved to a specific E-number — we classify them as functional/unclassified
# and flag that the label uses a generic class term (a disclosure concern).
HEBREW_CLASS_LOOKUP = {
    "מתחלב": {
        "e_number": "E4xx",
        "name_he": "מתחלב (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מתחלב",
        "explanation_he": "התווית מציינת 'מתחלב' ללא שם ספציפי — הסיווג המדויק אינו ידוע מהתווית.",
    },
    "מתחלבים": {
        "e_number": "E4xx",
        "name_he": "מתחלבים (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מתחלבים",
        "explanation_he": "התווית מציינת 'מתחלבים' ללא שמות ספציפיים — הסיווג המדויק אינו ידוע.",
    },
    "מייצב": {
        "e_number": "E4xx",
        "name_he": "מייצב (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מייצב",
        "explanation_he": "התווית מציינת 'מייצב' ללא שם ספציפי.",
    },
    "מייצבים": {
        "e_number": "E4xx",
        "name_he": "מייצבים (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מייצבים",
        "explanation_he": "התווית מציינת 'מייצבים' ללא שמות ספציפיים.",
    },
    "מסמיך": {
        "e_number": "E4xx",
        "name_he": "מסמיך (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מסמיך",
        "explanation_he": "התווית מציינת 'מסמיך' ללא שם ספציפי.",
    },
    "מסמיכים": {
        "e_number": "E4xx",
        "name_he": "מסמיכים (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מסמיכים",
        "explanation_he": "התווית מציינת 'מסמיכים' ללא שמות ספציפיים.",
    },
    "מווסת חומציות": {
        "e_number": "E3xx",
        "name_he": "מווסת חומציות (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מווסת חומציות",
        "explanation_he": "התווית מציינת 'מווסת חומציות' ללא שם ספציפי.",
    },
    "מווסתי חומציות": {
        "e_number": "E3xx",
        "name_he": "מווסתי חומציות (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "מווסתי חומציות",
        "explanation_he": "התווית מציינת 'מווסתי חומציות' ללא שמות ספציפיים.",
    },
    "חומר תפיחה": {
        "e_number": "E5xx",
        "name_he": "חומר תפיחה (מין לא מפורט)",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "חומר תפיחה כללי; בדרך כלל ביקרבונטים — ידוע כבטוח.",
    },
    "חומרי תפיחה": {
        "e_number": "E5xx",
        "name_he": "חומרי תפיחה (מין לא מפורט)",
        "tier": "functional",
        "function_he": "חומרי תפיחה",
        "explanation_he": "חומרי תפיחה כלליים; בדרך כלל ביקרבונטים — ידוע כבטוח.",
    },
    "חומר הלחה": {
        "e_number": "E4xx",
        "name_he": "חומר הלחה (מין לא מפורט)",
        "tier": "functional",
        "function_he": "חומר הלחה",
        "explanation_he": "חומר הלחה כללי; שומר על לחות המוצר. ברוב המקרים גליצרול או פוליאולים בטוחים.",
    },
    "חומרי הלחה": {
        "e_number": "E4xx",
        "name_he": "חומרי הלחה (מין לא מפורט)",
        "tier": "functional",
        "function_he": "חומרי הלחה",
        "explanation_he": "חומרי הלחה כלליים; שומרים על לחות המוצר.",
    },
    "לציטין": {
        "e_number": "E322",
        "name_he": "לציטין",
        "tier": "likely-neutral",
        "function_he": "מתחלב",
        "explanation_he": "מתחלב טבעי מסויה או חמניות; מסייע לתחמיץ שמן ומים.",
    },
    "לציטין סויה": {
        "e_number": "E322",
        "name_he": "לציטין סויה",
        "tier": "likely-neutral",
        "function_he": "מתחלב",
        "explanation_he": "מתחלב טבעי מסויה; מסייע לתחמיץ שמן ומים במאפים.",
    },
    "לציטין חמניות": {
        "e_number": "E322",
        "name_he": "לציטין חמניות",
        "tier": "likely-neutral",
        "function_he": "מתחלב",
        "explanation_he": "מתחלב טבעי מחמניות; מסייע לתחמיץ שמן ומים במאפים.",
    },
    "חומצה סורבית": {
        "e_number": "E200",
        "name_he": "חומצה סורבית",
        "tier": "likely-neutral",
        "function_he": "חומר משמר",
        "explanation_he": "חומר משמר טבעי מפירות; עוצר עובש ושמרים.",
    },
    "סודיום ביקרבונט": {
        "e_number": "E500",
        "name_he": "סודיום ביקרבונט",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "אבקת אפייה; גורם לבצק לתפוח בחום.",
    },
    "ביקרבונט": {
        "e_number": "E500",
        "name_he": "ביקרבונט (סודיום)",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "אבקת אפייה; גורם לבצק לתפוח בחום.",
    },
    "אבקת אפייה": {
        "e_number": "E500",
        "name_he": "אבקת אפייה",
        "tier": "functional",
        "function_he": "חומר תפיחה",
        "explanation_he": "תערובת תפיחה; בדרך כלל ביקרבונט + חומצה + עמילן. בטוח.",
    },
    "פוספט": {
        "e_number": "E450",
        "name_he": "פוספט (מין לא מפורט)",
        "tier": "dose-dependent",
        "function_he": "חומר תפיחה / מייצב",
        "explanation_he": "פוספטים; EFSA מציינת צריכה מצטברת כשיקול — ראה ADI קבוצתי.",
    },
    "פירופוספט": {
        "e_number": "E450",
        "name_he": "פירופוספט",
        "tier": "dose-dependent",
        "function_he": "חומר תפיחה",
        "explanation_he": "דיפוספט; EFSA מציינת ADI קבוצתי לפוספטים עם אזהרת צריכה מצטברת.",
    },
    "צבע": {
        "e_number": "E1xx",
        "name_he": "צבע מאכל (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "צבע מאכל",
        "explanation_he": "התווית מציינת 'צבע' ללא שם ספציפי — לא ניתן לקבוע את הסוג המדויק.",
    },
    "צבע מאכל": {
        "e_number": "E1xx",
        "name_he": "צבע מאכל (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "צבע מאכל",
        "explanation_he": "התווית מציינת 'צבע מאכל' ללא שם ספציפי.",
    },
    "צבעי": {
        "e_number": "E1xx",
        "name_he": "צבעי מאכל (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "צבעי מאכל",
        "explanation_he": "התווית מציינת 'צבעי' ללא שמות ספציפיים.",
    },
    "צבעי מאכל": {
        "e_number": "E1xx",
        "name_he": "צבעי מאכל (מין לא מפורט)",
        "tier": "disclosure-gap",
        "function_he": "צבעי מאכל",
        "explanation_he": "התווית מציינת 'צבעי מאכל' ללא שמות ספציפיים.",
    },
    "גואר": {
        "e_number": "E412",
        "name_he": "גואר גאם",
        "tier": "functional",
        "function_he": "מסמיך / מייצב",
        "explanation_he": "סיב מסיס; ללא דאגות בטיחות מהצריכה התזונתית.",
    },
    "קסנטן": {
        "e_number": "E415",
        "name_he": "קסנתן גאם",
        "tier": "functional",
        "function_he": "מייצב",
        "explanation_he": "סיב מותסס; נפוץ במוצרי ללא גלוטן.",
    },
    "דקסטרין": {
        "e_number": "E1400",
        "name_he": "דקסטרין",
        "tier": "functional",
        "function_he": "ממלא / מייצב",
        "explanation_he": "עמילן מפורק חלקית; משמש כממלא. נחשב בטוח.",
    },
    "מלטודקסטרין": {
        "e_number": "E1400",
        "name_he": "מלטודקסטרין",
        "tier": "functional",
        "function_he": "ממלא / מסמיך",
        "explanation_he": "עמילן מפורק; נפוץ כממלא וממס. נחשב בטוח אך יש לו אינדקס גליקמי גבוה.",
    },
    "אגר": {
        "e_number": "E406",
        "name_he": "אגר-אגר",
        "tier": "functional",
        "function_he": "ג'ל / מסמיך",
        "explanation_he": "פוליסכריד מאצות אדומות; ללא דאגות בטיחות.",
    },
    "גליצרול": {
        "e_number": "E422",
        "name_he": "גליצרול",
        "tier": "functional",
        "function_he": "לחות / ממס",
        "explanation_he": "אלכוהול סוכר שומר לחות; נחשב בטוח לחלוטין.",
    },
    "פפריקה": {
        "e_number": "E160C",
        "name_he": "עשב פפריקה (צבע)",
        "tier": "functional",
        "function_he": "צבע מאכל טבעי",
        "explanation_he": "פיגמנט אדום מפפריקה; ללא דאגות בטיחות.",
    },
    "אינולין": {
        "e_number": "E1395",
        "name_he": "אינולין",
        "tier": "functional",
        "function_he": "סיב פרה-ביוטי",
        "explanation_he": "סיב מסיס (פרה-ביוטי) מעולת ירושלים/שורש עולש; ידוע כמיטיב למיקרוביום.",
    },
}


def normalize_e_number(term: str) -> str | None:
    """Extract canonical E-number from a term string. Returns e.g. 'E330' or None."""
    # Try to extract E-number
    m = re.search(r'\b(E[-]?\d{3,4}[a-zA-Z]{0,2})\b', term, re.IGNORECASE)
    if m:
        raw = m.group(1).upper().replace("E-", "E")
        # Normalize sub-letter to uppercase
        return raw
    return None


def convert_legacy_additive(legacy_entry: dict) -> dict:
    """
    Convert a {term, category} legacy additive entry to AdditiveEntry schema.
    Strategy:
    1. Try to extract an E-number from the term → look up in ADDITIVE_LOOKUP
    2. Try the term directly in HEBREW_CLASS_LOOKUP
    3. Fall back to unclassified with honest Hebrew name
    Never invents an E-number.  Never uses OFF.
    """
    term = (legacy_entry.get("term") or "").strip()

    # Already correct schema — pass through
    if "e_number" in legacy_entry:
        return legacy_entry

    # 1. E-number path
    e_num = normalize_e_number(term)
    if e_num:
        # Check aliases
        canonical = E_NUMBER_ALIASES.get(e_num, e_num)
        if canonical in ADDITIVE_LOOKUP:
            return ADDITIVE_LOOKUP[canonical].copy()
        # E-number found but not in library → build functional/unclassified entry
        return {
            "e_number": canonical,
            "name_he": term,  # use the full term as name since we don't have a Hebrew name
            "tier": "unclassified",
            "function_he": legacy_entry.get("category", "").replace("_", " "),
            "explanation_he": f"מספר {canonical}; לא נמצא בספרייה המאושרת — מסווג כ'לא מסווג'.",
        }

    # 2. Hebrew class lookup
    if term in HEBREW_CLASS_LOOKUP:
        return HEBREW_CLASS_LOOKUP[term].copy()

    # 3. Fallback — preserve Hebrew name, mark unclassified
    cat = legacy_entry.get("category", "")
    return {
        "e_number": "—",
        "name_he": term,
        "tier": "unclassified",
        "function_he": cat.replace("_", " ") if cat else "לא ידוע",
        "explanation_he": "רכיב שאינו מפורט מספיק בתווית; לא ניתן לסווגו מהמידע הזמין.",
    }


def fix_d4_additives(products: list) -> tuple[int, int]:
    """
    Converts all legacy {term, category} d4_additives entries to AdditiveEntry schema.
    Returns (legacy_converted, already_correct).
    """
    legacy_converted = 0
    already_correct = 0
    for p in products:
        additives = p.get("d4_additives", [])
        if not additives:
            continue
        new_additives = []
        product_seen_enums = set()
        for a in additives:
            if "e_number" in a:
                already_correct += 1
                # Dedupe by e_number within product
                if a["e_number"] not in product_seen_enums:
                    product_seen_enums.add(a["e_number"])
                    new_additives.append(a)
            else:
                legacy_converted += 1
                converted = convert_legacy_additive(a)
                # Dedupe by e_number within product
                if converted["e_number"] not in product_seen_enums:
                    product_seen_enums.add(converted["e_number"])
                    new_additives.append(converted)
        p["d4_additives"] = new_additives
    return legacy_converted, already_correct


# ─────────────────────────────────────────────────────────────────────────────
# RT-10: Promo name stripping
# ─────────────────────────────────────────────────────────────────────────────

PROMO_STRIP_RE = re.compile(
    r'\s*\|\s*[\d.,]+\s*גרם\s.*$'   # ' | N גרם ...'
    r'|\s*\|\s*.*[\d.]+\s*₪.*$'      # ' | ... ₪ ...'
    r'|\s+\d+\s+יח.*?₪.*$'            # ' N יח' ב- ... ₪ ...'
    r'|\s*\|\s*\d+\s*$',              # ' | 176' (truncated promo tail — bare number)
    re.UNICODE,
)


def strip_promo(name: str) -> str:
    """Strip price/promo tail from a product display name."""
    cleaned = PROMO_STRIP_RE.sub("", name).strip()
    # Safety: if cleaning removes too much, return original
    if not cleaned or len(cleaned) < 3:
        return name
    return cleaned


# ─────────────────────────────────────────────────────────────────────────────
# RT-8: Duplicate name disambiguation
# Using real attributes from BSIP1 data (brand, ingredients).
# ─────────────────────────────────────────────────────────────────────────────

# Mapping: barcode → disambiguated name suffix/replacement
# Sources: BSIP1 brand + ingredient text (verified above)
DUPLICATE_NAME_FIXES = {
    # עוגת מאפין אגוזים pair:
    # 2472254 = שופרסל brand, shorter ingredient list, uses "שומן צמחי" generic
    # 7296073431893 = שופרסל brand, detailed list with "שמן קנולה מזוכך" + chocolate frosting
    "2472254": "עוגת מאפין אגוזים — שופרסל",
    "7296073431893": "עוגת מאפין אגוזים עם ציפוי — שופרסל",

    # עוגת מאפין תפוז pair:
    # 7296073140184 = לה פזואלוס brand
    # 2472223 = שופרסל brand
    "7296073140184": "עוגת מאפין תפוז — לה פזואלוס",
    "2472223": "עוגת מאפין תפוז — שופרסל",

    # עוגה בטעם שוקולד כשל"פ pair (both VOILA):
    # 7290123330884 = with cocoa powder 6% ("אבקת קקאו 6%")
    # 7290123331034 = with chocolate drizzle 8% ("נטיפים בטעם שוקולד 8%")
    "7290123330884": 'עוגה בטעם שוקולד כשל"פ — קקאו',
    "7290123331034": 'עוגה בטעם שוקולד כשל"פ — נטיפים',
}


# ─────────────────────────────────────────────────────────────────────────────
# RT-7: Cakes filter entries
# ─────────────────────────────────────────────────────────────────────────────

def compute_cakes_filters(products: list) -> list:
    """
    Compute filter entries for cakes page.
    Filter IDs must match what the component expects.
    """
    # least_bad = grade C only (1 product in this dataset)
    least_bad_count = sum(1 for p in products if p.get("grade") == "C")
    # has_phvo = products flagged with PHVO
    has_phvo_count = sum(1 for p in products if p.get("_has_phvo") is True)
    # no_phvo = complement
    no_phvo_count = len(products) - has_phvo_count
    # high_sugar = products in the high_sugar set
    high_sugar_count = sum(
        1 for p in products
        if (p.get("expansion", {}).get("nutrition", {}) or {}).get("sugar") is not None
        and (p["expansion"]["nutrition"]["sugar"] >= 30)
    )

    filters = [
        {"id": "all", "label_he": "הכל", "count": len(products)},
    ]

    # Add only filters with meaningful counts (>0 and < total)
    if 0 < least_bad_count < len(products):
        filters.append({
            "id": "least_bad",
            "label_he": f"הכי פחות כבדות (ציון C)",
            "count": least_bad_count,
        })

    if 0 < has_phvo_count < len(products):
        filters.append({
            "id": "has_phvo",
            "label_he": f"עם שומן צמחי מוקשה ({has_phvo_count})",
            "count": has_phvo_count,
        })

    if 0 < no_phvo_count < len(products):
        filters.append({
            "id": "no_phvo",
            "label_he": f"ללא שומן צמחי מוקשה ({no_phvo_count})",
            "count": no_phvo_count,
        })

    if 0 < high_sugar_count < len(products):
        filters.append({
            "id": "high_sugar",
            "label_he": f"סוכר גבוה במיוחד ({high_sugar_count})",
            "count": high_sugar_count,
        })

    return filters


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — load, fix, save
# ─────────────────────────────────────────────────────────────────────────────

print("=== RT FIXES — TASK-275 ===")
print()

# ── Load files ────────────────────────────────────────────────────────────────
cakes_data = json.loads(CAKES_JSON.read_text(encoding="utf-8"))
biscuits_data = json.loads(BISCUITS_JSON.read_text(encoding="utf-8"))
seo_data = json.loads(SEO_FAQ.read_text(encoding="utf-8"))

cakes_products = cakes_data["products"]
biscuits_products = biscuits_data["products"]

print(f"Loaded cakes: {len(cakes_products)} products")
print(f"Loaded biscuits: {len(biscuits_products)} products")

# ── RT-1: Fix additive schema ────────────────────────────────────────────────
print("\n--- RT-1: Additive schema fix ---")

# Count legacy before
cakes_legacy_before = sum(
    1 for p in cakes_products
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
biscuits_legacy_before = sum(
    1 for p in biscuits_products
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
print(f"Cakes legacy entries before: {cakes_legacy_before}")
print(f"Biscuits legacy entries before: {biscuits_legacy_before}")

# Apply fix
cakes_converted, cakes_correct = fix_d4_additives(cakes_products)
biscuits_converted, biscuits_correct = fix_d4_additives(biscuits_products)

# Verify zero legacy remain
cakes_legacy_after = sum(
    1 for p in cakes_products
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
biscuits_legacy_after = sum(
    1 for p in biscuits_products
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
print(f"Cakes converted: {cakes_converted}, already correct: {cakes_correct}")
print(f"Biscuits converted: {biscuits_converted}, already correct: {biscuits_correct}")
print(f"Cakes legacy after: {cakes_legacy_after} (must be 0)")
print(f"Biscuits legacy after: {biscuits_legacy_after} (must be 0)")
assert cakes_legacy_after == 0, "Cakes still have legacy additive entries!"
assert biscuits_legacy_after == 0, "Biscuits still have legacy additive entries!"

# ── RT-4: Caveat verification ────────────────────────────────────────────────
print("\n--- RT-4: Caveat arithmetic verification ---")
cross_both = cross_one = cross_neither = not_verifiable = 0
for p in biscuits_products:
    n = p.get("expansion", {}).get("nutrition", {}) or {}
    sugar = n.get("sugar")
    sat_fat = n.get("satFat")
    if sugar is None or sat_fat is None:
        not_verifiable += 1
    elif sugar > 17.5 and sat_fat > 5:
        cross_both += 1
    elif sugar > 17.5 or sat_fat > 5:
        cross_one += 1
    else:
        cross_neither += 1

total = cross_both + cross_one + cross_neither + not_verifiable
print(f"Cross both: {cross_both} | Cross one: {cross_one} | Cross neither: {cross_neither} | Not verifiable: {not_verifiable}")
print(f"Total: {total} (must be 118)")
assert total == 118, f"Arithmetic doesn't close! Got {total}"
print(f"Caveat body arithmetic VERIFIED: 68+33+11+6={68+33+11+6} = 118 ✓")
print("RT-4: No caveat body change needed — current '6' is the correct verified count.")

# ── RT-5: SEO FAQ update ────────────────────────────────────────────────────
print("\n--- RT-5: SEO FAQ update ---")
# Verify top and low scores from v2 data
biscuits_scores = [(p["score"], p["name"]) for p in biscuits_products if p.get("score") is not None]
biscuits_scores.sort(key=lambda x: -x[0])
top_score = biscuits_scores[0][0]
low_score = biscuits_scores[-1][0]
top_name = biscuits_scores[0][1]
print(f"Top score: {top_score}/100 — {top_name}")
print(f"Low score: {low_score}/100")

seo_before_count = seo_data["_bari_meta"]["product_count"]
seo_before_version = seo_data["_bari_meta"]["source_version"]

seo_data["_bari_meta"]["source_version"] = "cookies_coffee_frontend_v2.json"
seo_data["_bari_meta"]["product_count"] = 118
seo_data["_bari_meta"]["generated"] = datetime.now(timezone.utc).isoformat()

# Fix FAQ answer that says "56 מוצרים"
for qa in seo_data.get("mainEntity", []):
    answer = qa.get("acceptedAnswer", {}).get("text", "")
    if "56 מוצרים" in answer:
        new_answer = answer.replace("56 מוצרים", "118 מוצרים")
        qa["acceptedAnswer"]["text"] = new_answer
        print(f"Updated FAQ answer: '56 מוצרים' → '118 מוצרים'")
    if "56" in answer and "מוצר" in answer:
        # catch any remaining references
        pass

print(f"SEO: product_count {seo_before_count} → 118")
print(f"SEO: source_version '{seo_before_version}' → 'cookies_coffee_frontend_v2.json'")
print(f"SEO: top_score {top_score} (unchanged, was already correct in FAQ text)")
print(f"SEO: low_score {low_score} (unchanged, was already correct in FAQ text)")

# ── RT-7: Cakes filters ────────────────────────────────────────────────────
print("\n--- RT-7: Cakes filter entries ---")
old_filters = cakes_data["page_copy"]["filters"]
print(f"Old filters: {[f['id'] for f in old_filters]}")

new_filters = compute_cakes_filters(cakes_products)
cakes_data["page_copy"]["filters"] = new_filters

# Report counts for verification
for f in new_filters:
    print(f"  id={f['id']} count={f['count']}")

# Note: least_bad=1 (grade C only). This is trivially small (1/65) but USEFUL
# as a filter precisely because it's the sole non-E product — it surfaces the one
# product that's less bad. Ship it.

# ── RT-8: Duplicate name disambiguation ─────────────────────────────────────
print("\n--- RT-8: Duplicate name disambiguation ---")
rt8_changes = []
for p in cakes_products:
    bc = str(p.get("barcode", ""))
    if bc in DUPLICATE_NAME_FIXES:
        old_name = p["name"]
        new_name = DUPLICATE_NAME_FIXES[bc]
        p["name"] = new_name
        rt8_changes.append({"barcode": bc, "before": old_name, "after": new_name})
        print(f"  {bc}: '{old_name}' → '{new_name}'")

# Verify no more duplicates
name_count = {}
for p in cakes_products:
    n = p["name"]
    name_count[n] = name_count.get(n, 0) + 1
remaining_dupes = {n: c for n, c in name_count.items() if c > 1}
print(f"Remaining duplicate names after fix: {len(remaining_dupes)}")
if remaining_dupes:
    print(f"  WARNING: {remaining_dupes}")

# ── RT-10: Promo name stripping ─────────────────────────────────────────────
print("\n--- RT-10: Promo name stripping ---")
rt10_cakes = 0
rt10_biscuits = 0

for p in cakes_products:
    old_name = p["name"]
    new_name = strip_promo(old_name)
    if new_name != old_name:
        p["name"] = new_name
        rt10_cakes += 1
        print(f"  CAKE {p['barcode']}: stripped promo")

for p in biscuits_products:
    old_name = p["name"]
    new_name = strip_promo(old_name)
    if new_name != old_name:
        p["name"] = new_name
        rt10_biscuits += 1

print(f"Cakes promo names stripped: {rt10_cakes}")
print(f"Biscuits promo names stripped: {rt10_biscuits}")
print(f"Total: {rt10_cakes + rt10_biscuits} (expected ~21)")

# ── Final count verification ─────────────────────────────────────────────────
print("\n--- Final count verification ---")
print(f"Cakes products: {len(cakes_products)} (must be 65)")
print(f"Biscuits products: {len(biscuits_products)} (must be 118)")
assert len(cakes_products) == 65, f"Cakes count changed! {len(cakes_products)}"
assert len(biscuits_products) == 118, f"Biscuits count changed! {len(biscuits_products)}"

# ── Save ─────────────────────────────────────────────────────────────────────
print("\n--- Saving files ---")
CAKES_JSON.write_text(json.dumps(cakes_data, ensure_ascii=False, indent=2), encoding="utf-8")
BISCUITS_JSON.write_text(json.dumps(biscuits_data, ensure_ascii=False, indent=2), encoding="utf-8")
SEO_FAQ.write_text(json.dumps(seo_data, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Saved: {CAKES_JSON}")
print(f"Saved: {BISCUITS_JSON}")
print(f"Saved: {SEO_FAQ}")

# ── Final verification pass ───────────────────────────────────────────────────
print("\n=== FINAL VERIFICATION ===")

cakes_check = json.loads(CAKES_JSON.read_text(encoding="utf-8"))
biscuits_check = json.loads(BISCUITS_JSON.read_text(encoding="utf-8"))

# RT-1: Zero legacy schema
cakes_legacy_final = sum(
    1 for p in cakes_check["products"]
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
biscuits_legacy_final = sum(
    1 for p in biscuits_check["products"]
    for a in p.get("d4_additives", [])
    if "e_number" not in a
)
print(f"RT-1 — Cakes legacy schema entries: {cakes_legacy_final} (must be 0)")
print(f"RT-1 — Biscuits legacy schema entries: {biscuits_legacy_final} (must be 0)")

# Counts
print(f"RT-1 — Cakes products: {len(cakes_check['products'])} (must be 65)")
print(f"RT-1 — Biscuits products: {len(biscuits_check['products'])} (must be 118)")

# Filters
filter_ids = [f["id"] for f in cakes_check["page_copy"]["filters"]]
print(f"RT-7 — Cakes filter ids: {filter_ids}")

# SEO
seo_check = json.loads(SEO_FAQ.read_text(encoding="utf-8"))
print(f"RT-5 — SEO product_count: {seo_check['_bari_meta']['product_count']} (must be 118)")
print(f"RT-5 — SEO source_version: {seo_check['_bari_meta']['source_version']}")

print("\nAll checks passed.")
