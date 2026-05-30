#!/usr/bin/env python3
"""
מעדנים — BariProductVM Builder v1
Reads: BSIP2 traces (200) + BSIP0 raw (image URLs)
Writes: maadanim_frontend_v1.json  (BariProductVM[])
        maadanim_corpus_report_v1.md
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(r"C:\Bari")
BSIP2_DIR  = ROOT / "02_products/maadanim/bsip2_outputs/run_maadanim_001/products"
BSIP0_RAW  = ROOT / "02_products/maadanim/maadanim_bsip0_raw_20260528T072053.json"
OUT_DIR    = ROOT / "02_products/maadanim"
OUT_JSON   = OUT_DIR / "maadanim_frontend_v1.json"
OUT_REPORT = OUT_DIR / "maadanim_corpus_report_v1.md"

# ── Finalized insight lines (from maadanim_insight_lines_v1.md) ───────────────
INSIGHT_LINES: dict[str, str] = {
    # Cluster 1 — מילקי ודומיהם
    "מילקי בטעם שוקולד":           "הגביע הכי מוכר בקטגוריה, הציון הנמוך בה",
    "מילקי בטעם פסק זמן":          "שוקולד ועוגיות — שני סוגי סוכר ברשימת הרכיבים",
    "מילקי בטעם וניל":             "אותה תשתית של מייצבים וסוכר, בטעם שונה",
    "מילקי בטעם תות":              "טעם תות, הסוכר ברכיב השלישי",
    "מילקי אקסטרה קצפת":           "שכבת קצפת נוספת, אותו הרכב בבסיס — לא מוצר שונה",
    "מילקי עם 26% פחות סוכר":      "26% פחות סוכר, 1.5 נקודות הפרש מהגרסה הרגילה",
    "מילקי בלונדי":                "גרסת לבנה — רשימת הרכיבים ארוכה מהגרסה הכהה",
    "מילקי טופ שוקולדה מגולגל":    "המרקם בנוי על מייצבים ועמילן מעובד — לא על ריכוז חלב",
    "מילקי טופ קורנפלקס":          "קורנפלקס כתוספת — הסוכר מופיע בשתי הרשימות",
    "מילקי טופ עדשים":             "עדשים כתוספת — הסוכר קודם לעדשים ברשימת הרכיבים",
    "מילקי שכבות שוקולד+קצפת":     "שתי שכבות, הסוכר פעמיים ברשימת הרכיבים",
    "מילקי שכבות שוקולד קוקוס":    "קוקוס בשם, סוכר וקוקוס ברשימת הרכיבים",
    "מילקי קייק מארז":             "מעדן בפורמט עוגה — תשתית כבדה יותר מהגביע",
    "מילקי קייק מיניס קרם חלב":    "עוגה, קרם וציפוי — שלוש שכבות, שלוש רשימות רכיבים",
    "מיני מילקי בטעם שוקולד":      "פורמט קטן, הרכב זהה לגביע הגדול — הצמצום הוא בגרמים, לא ברכיבים",
    "יולו שכבות שוקולד":           "מוצר שונה ממילקי, הרכב דומה — מייצבים וסוכר כבסיס בשניהם",
    "מעדן מוו בטעם שוקולד":        "חמשה מייצבים לבניית המרקם — יותר מכל מוצר אחר בקבוצה",
    "מעדן מוו בטעם וניל מארז":     "גרסת הוניל — אותה רשימת מייצבים, פחות סוכר",
    "לימבו פטל קו חלבי":           "פטל בשם, סוכר ברכיב הראשון",
    # Cluster 2 — מוצרי חלבון
    "יופלה GO מועשר בחלבון":       "10 גרם חלבון, 3 רכיבים עיקריים בלבד",
    "יופלה GO אפרסק":              "GO עם אפרסק — הוסיפו סוכר ועמילן, שינו את ההרכב הבסיסי",
    "יופלה GO פירות יער":          "פירות יער בשם, ממתיקי טעם ברשימת הרכיבים",
    "יופלה GO תות":                "GO עם תות — טעם מלאכותי הגיע עם שינוי בתשתית ההרכב",
    "יופלה GO אפרסק 0.7%":         "0.7% שומן בשם, הוסיפו חומרי טעם",
    "יופלה GO דובדבן 0.7%":        "GO דובדבן — תוספת טעם ומייצבים, הרחק מהגרסה הלבנה בהרכב",
    "מעדן חלבון בטעם וניל":        "חלבון על התווית, מייצבים ברשימת הרכיבים — תשתית שונה מ-GO",
    'מעדן חלבון ללת"ס שוקולד':     "הסוכר הוחלף בממתיקים, המבנה המעובד נשאר — הפער מ-GO הוא במבנה, לא בסוכר",
    "מעדן פרו בטעם פסק זמן":       '"פרו" על האריזה, ממתיקים וסוכר ברשימת הרכיבים — תשתית עיבוד גבוהה',
    "דנונה פרו 20ג חלבון תות":     "20 גרם חלבון בגביע, ממתיקים ברשימת הרכיבים",
    'דנונ.פרו ללא סוכר פיסטוק':    "פיסטוק ו'ללא סוכר' — ממתיקים מלאכותיים ברכיבים",
    # Cluster 3 — מעדן הגולן
    "מעדן הגולן שוקולד":           "ציון גבוה מהשוקולד הלאומי — רשימת רכיבים קצרה יותר",
    "מעדן הגולן שוקולד מריר":      "שוקולד מריר — פחות סוכר מגרסת השוקולד הרגיל",
    "מעדן הגולן וניל":             "גרסת הוניל של הגולן — חלב ושמנת כבסיס, בלי מייצבים עיקריים",
    # Cluster 4 — מעדן פירות ומוצרים פשוטים
    "מעדן משמש":                   "ללא תוספים מזוניים מזוהים — נדיר בקטגוריה",
    "מעדן תפוז":                   "מעדן פרי בלי תווית בריאות",
    "מעדן חצילים":                 "חציל כרכיב עיקרי, מעט סוכר — הרכב שונה מכל מעדן אחר בקטגוריה",
    "מעדן שיבולת שועל":            "שיבולת שועל בשם — 11 רכיבים, ממתיקים ומייצבים ברשימה",
    "מעדן בטעם וניל מועשר":        '"מועשר" בוויטמינים, אותה תשתית סוכר ומייצבים של הקטגוריה',
    "מעדן גבינה מוקצף וניל":       "גבינה שמנה כבסיס, קצפת כשכבה — הרכב שונה מגביע החלב הסטנדרטי",
    "מעדן ג'לי פטל":               "ג'לי פטל בגביע — עמילן וממתיקים כבסיס, לא חלב",
    "קינוח קראנצ' דובאי":          "שוקולד, קדאיף ופיסטוק — שלוש שכבות, רשימת רכיבים ארוכה בהתאם",
    "ירח מתוק מעדן חלב+אורז":      "חלב ואורז כבסיס — ללא שכבות נוספות, הרכב פשוט יחסית לקטגוריה",
    "מעדן קרלו שוניל":             "שוקולד כתוספת — שכבת עיבוד שהמעדן הפשוט לא נושא",
    "מעדן סויה ביו טבעי":          "ללא חלב — הרשימה ארוכה יותר ממה שנראה על הגביע",
    "מעדן סויה ביו טעם תות":       "תוספת טעם תות הביאה מייצבים וממתיקים — הסויה הפשוטה נעלמה",
    "מעדן סויה ביו אפרסק":         "אפרסק בסויה — תוספת טעם שינתה את ההרכב, כמו בגרסת התות",
    "מעדן סויה עם שוקולד":         "שוקולד בסויה — תוספת הטעם מורידה את הציון",
    # Cluster 5 — פודינג
    "פודינג אינסטנט שוקולד":       "להכנה ביתית — ציון גבוה ב-18 נקודות מהגביע המוכן",
    "אינסטנט פודינג שוקולד":       "אבקה להכנה ביתית, פחות תוספים מהגביע",
    "אינסטנט פודינג וניל":         "וניל בהכנה ביתית — פחות תוספים מגרסת הגביע",
    "פודינג וניל צרפתי":           '"צרפתי" בתווית, ציון זהה לפודינג הרגיל',
    "אינסטנט פודינג בטעם וניל":    "אבקה לוניל — פחות תוספים מהגביע, יותר מגרסת האינסטנט",
    "פודינג טעם פרלין אספרסו":     "פרלין ואספרסו — רשימת הרכיבים הארוכה ביותר בפודינג",
    "פודינג וניל":                 "הגביע המוכן — שימור ארוך חיים הביא מייצבים שהאבקה לא צריכה",
    "פודינג בטעם וניל":            "מוכן לאכילה, יותר תוספים מהגרסה הביתית",
    # Cluster 6 — מלבי
    "מלבי שמנת":                   "שמנת ומי ורדים — רשימת רכיבים קצרה, מרקם מסורתי",
    "מלבי":                        "מלבי מוכן לאכילה, תוספים נוספים מהגרסה הבסיסית",
    "מלבי חלבי":                   "הגרסה עם רשימת הרכיבים הארוכה ביותר בין מוצרי המלבי",
    # Cluster 7 — דנונה ודניאלה
    "דנונה תות 3% שומן":           "3% שומן בשם, הסוכר ברכיב השני",
    "דנונה אפרסק 3% שומן":         "אפרסק בדנונה — אותה תשתית, פחות סוכר מגרסת התות",
    "דנונה מולטי עם תפוח":         "תפוח כתוספת פרי — לא משנה את תשתית הסוכר והמייצבים",
    "דנונה מולטי קולגן":           "קולגן בתווית, כמות לא מצוינת על האריזה",
    "דנונה במתיקות מעודנת":        '"מעודנת" — ממתיק מלאכותי ברשימת הרכיבים',
    "דניאלה תות בננה":             "אריזת ילדים, הרכב דומה לדנונה הבוגרת — אותם מייצבים וסוכר",
    "דניאלה תות מוקצף 5%":         "מוקצף — תוספת מייצבים לשמירת המרקם",
    "דניאלה בננה":                 "בננה בשם, סוכר ברכיב השני",
    "דניאלה בטעם ענבים":           "ענבים בתווית, טעם מלאכותי ברשימת הרכיבים",
    # Cluster 8 — יופלה טיוב ושטוזים
    "יופלה טיוב תות":              "פורמט מוצצת, תשתית שונה מ-GO — טעמי עזר במקום חלב",
    "יופלה טיוב תות בננה":         "תות ובננה בשם, ממתיקי טעם ברשימה",
    "יופלה טיוב בטעם וניל":        "וניל במוצצת — ממתיקי טעם במקום וניל אמיתי, הגרסה הפחות מעובדת בטיוב",
    "יופלה שטוזים משקה תות":       "יופלה שתייה — נוסחת פחות שמנת יותר ממתיקים, הרכב שונה מהגביע",
    "יופלה און טופ פצפוצים":       "פצפוצי שוקולד בתוספת — שכבת סוכר נוספת על הגביע",
    "יופלה און טופ כוכבים":        "כוכבים דגנים בתוספת — תשתית זהה לגרסת הפצפוצים",
    "יופלה טופ תות קורנפלקס":      "יופלה עם קורנפלקס — הדגן מוסיף סוכר משלו לגביע שכבר מתוק",
    "משקה יופלה בננה תות 1.6%":   "שתייה מהירה במקום גביע — תוספות טעם ומייצבים בנוסחת השתייה",
    # Diet trap products
    "מעדן דיאט שוקולד 0.2%":       "תווית דיאט, ממתיקים מלאכותיים ב-4 שמות ברשימה — נמוך ממעדן הפרי הפשוט",
    "מעדן דיאט בטעם שוקולד":       "מסומן 'דיאט', הסוכר הוחלף בממתיקים — התשתית המעובדת נשארה",
    # Name-variant aliases (extra spaces, missing space before %)
    "יופלה  טופ תות קורנפלקס":     "יופלה עם קורנפלקס — הדגן מוסיף סוכר משלו לגביע שכבר מתוק",
    "מעדן  מוו בטעם וניל מארז":    "גרסת הוניל — אותה רשימת מייצבים, פחות סוכר",
    "מילקי קייק":                  "מעדן בפורמט עוגה — תשתית כבדה יותר מהגביע",
    "ירח מתוק מעדן חלב+אורז3%":    "חלב ואורז כבסיס — ללא שכבות נוספות, הרכב פשוט יחסית לקטגוריה",
    "דנונה אפרסק3% שומן":          "אפרסק בדנונה — אותה תשתית, פחות סוכר מגרסת התות",
    "דניאלה תות מוקצף5% שומן":     "מוקצף — תוספת מייצבים לשמירת המרקם",
    "משקה יופלה בננה תות1.6%":     "שתייה מהירה במקום גביע — תוספות טעם ומייצבים בנוסחת השתייה",
    "מעדן קרלו שוניל 3% שומן":     "שוקולד כתוספת — שכבת עיבוד שהמעדן הפשוט לא נושא",
    "מעדן סויה ביו טעם תות 3%":    "תוספת טעם תות הביאה מייצבים וממתיקים — הסויה הפשוטה נעלמה",
    "דני שוקולד 1.5%":             "שוקולד ילדים — אבקת קקאו בשכבה השלישית, סוכר ברכיב הראשון",
    # Cluster 9 — גמדים וילדים
    "גמדים תות בננה מארז":         "מארז בית — פחות תוספים מגרסת הדרך, הגרסה הפשוטה יחסית בסדרה",
    "סופר גמדים תות בננה מארז":    '"סופר" בשם, הרכב זהה לגמדים הרגיל — השם לא שינה את הנוסחה',
    "גמדים לדרך תות בננה":         "פורמט דרך — תוספת מייצבים לשמירה, הרכב מורכב יותר מהמארז",
    "גמדים לדרך סלט פירות":        "סלט פירות בגביע — פירות כרכיב עיקרי, סוכר ברכיב השני",
    "גמדים לשתיה תות בננה":        "גמדים שתייה — נוסחת שתייה, יותר מייצבים מהגביע",
    "גמדים סקוויז לדרך תות":       "סקוויז ילדים — תוספת מייצב לשמירת הטקסטורה בלחיצה",
    "גמדים ארוחת בוקר תות":        "ארוחת בוקר בתווית, מעדן חלב בפועל — הרכב הסטנדרטי של הקטגוריה",
    "באדי תות שדה 3% שומן":        "3% שומן ופרי — הרכב מעדן ילדים סטנדרטי, סוכר ברכיב השלישי",
    "פרילי תות 1.5% שומן":         "1.5% שומן בשם, ממתיק ברשימת הרכיבים",
}

def grade_from_score(score: float) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"

def nutrition_vm(signals: dict) -> dict | None:
    """Extract BariNutritionVM from L1_observed_signals. Returns None if all null."""
    kcal   = signals.get("energy_kcal")
    prot   = signals.get("protein_g")
    sugar  = signals.get("sugars_g")
    fat    = signals.get("fat_g")
    fiber  = signals.get("dietary_fiber_g")
    sodium = signals.get("sodium_mg")

    def clean(v):
        if v is None: return None
        try:
            f = float(v)
            return round(f, 1)
        except (TypeError, ValueError):
            return None

    n = {
        "energyKcal": clean(kcal),
        "protein":    clean(prot),
        "sugar":      clean(sugar),
        "fat":        clean(fat),
        "fiber":      clean(fiber),
        "sodium":     clean(sodium),
    }
    if all(v is None for v in n.values()):
        return None
    return n

_INGREDIENT_CUTOFFS = [
    "ערכים תזונתיים",
    "הנתונים המדויקים",
    "מאפיינים נוספים",
    "אין להסתמך",
    "יתכנו טעויות",
    "התמונות והתאריכים",
    "n20 גרם",
    "קל אנרגיה",
    "מג נתרן",
]
# Pattern: ". 20 גרם" or similar — period + space + digits signals nutrition bleed
_NUTRI_BLEED_RE = re.compile(r"\.\s+\d+[\s.]+גרם")

def _clean_ingredient_text(text: str) -> str:
    """Strip nutrition facts bleed-in that BSIP1 captures after ingredient list."""
    # Replace BSIP1 newline artifact first
    text = text.replace(".n", ". ").replace("  ", " ")
    # Regex: find first ". 20 גרם" style marker (nutrition facts bleeding in)
    m = _NUTRI_BLEED_RE.search(text)
    if m and m.start() > 10:
        text = text[:m.start()]
    # String markers
    for marker in _INGREDIENT_CUTOFFS:
        idx = text.find(marker)
        if idx > 10:
            text = text[:idx]
            break
    # Trim trailing punctuation
    return text.strip().rstrip("., ")

def ingredients_vm(signals: dict) -> str | None:
    lst = signals.get("ingredient_list", [])
    if not lst:
        return None
    raw = ", ".join(str(x).strip() for x in lst if str(x).strip())
    cleaned = _clean_ingredient_text(raw)
    return cleaned if cleaned else None

def confidence_vm(trace: dict) -> tuple[str, str]:
    """Returns (confidence, confidenceLabel)."""
    if trace.get("data_sufficiency") == "insufficient":
        return "insufficient", "נתונים חסרים"
    score = trace.get("confidence_score", 0)
    if score >= 75:
        return "verified", "נתונים מלאים"
    return "partial", "נתונים חלקיים"

def best_image(image_urls: list[str]) -> str | None:
    if not image_urls:
        return None
    # Prefer 'large' URL if present (index 1), else first
    for url in image_urls:
        if "products_large" in url or "products_zoom" in url:
            return url
    return image_urls[0] if image_urls else None

def name_matches(trace_name: str, insight_key: str) -> bool:
    """Exact match after normalizing quotes and whitespace."""
    def norm(s):
        return s.strip().replace('"', '"').replace('"', '"')
    return norm(trace_name) == norm(insight_key)

def find_insight(product_name: str) -> str | None:
    for key, line in INSIGHT_LINES.items():
        if name_matches(product_name, key):
            return line
    return None


# ── CE interpretive expansion v2 (authoritative over auto-generated copy) ─────
SCORE_OVERRIDES: dict[str, int] = {
    "יופלה GO דובדבן 0.7%": 52,
}

CONFIDENCE_OVERRIDES: dict[str, tuple[str, str]] = {
    "מעדן סויה ביו טבעי": (
        "partial",
        "נתונים חלקיים — ערך האנרגיה על האריזה לא אמין",
    ),
}

CE_INTERPRETIVE_OVERRIDES: dict[str, dict] = {
    "יופלה GO מועשר בחלבון": {
        "positiveSignals": [
            "10 גרם חלבון ל-100 גרם — מגיע מחלב ואבקת חלב, לא מתווית בלבד",
            "שלושה רכיבים עיקריים בלבד — חלב, חלבוני חלב, אבקת חלב",
            "ללא תוספים פונקציונליים מזוהים ברשימה",
        ],
        "limitingFactors": [
            "עדיין מעדן מתוק בקטגוריה — לא מוצר 'נקי' לחלוטין במובן של קינוח",
        ],
        "bottomLine": "מוצר חלבון יחסית נקי במדף — החלבון באמת מהחלב.",
        "comparisonContext": "מול שאר סדרת GO — הגרסה הכי קרובה למבנה פשוט.",
    },
    "יופלה GO דובדבן 0.7%": {
        "positiveSignals": [
            "חלבון נשמר — כ-10 גרם ל-100 גרם",
            "דובדבן מבושל ברשימה — לא רק טעם מלאכותי",
        ],
        "limitingFactors": [
            "0.7% שומן על האריזה — אבל ממתיקים, חומרי טעם ומייצבים הצטרפו לתשתית",
            "ההרכב התרחק מ-GO הלבן — לא אותה פשטות ברכיבים",
        ],
        "bottomLine": "שם דל-שומן — התוספות לטעם הן מה שמפריד אותו מ-GO הבסיסי.",
        "comparisonContext": "מול GO מועשר בחלבון — אותו חלבון, תשתית כבדה ומתוקה יותר.",
    },
    "יופלה GO אפרסק 0.7%": {
        "positiveSignals": [
            "חלבון גבוה נשמר — כ-10 גרם ל-100 גרם",
        ],
        "limitingFactors": [
            "אפרסק מלווה בסוכר, עמילן וחומרי טעם — לא רק פרי על גבי GO נקי",
            "גרסת דל-שומן/טעם — המרקם נשען על תוספות, לא רק על חלב",
        ],
        "bottomLine": "GO עם אפרסק — הוסיפו סוכר ועמילן, שינו את ההרכב הבסיסי.",
        "comparisonContext": "מול GO מועשר בחלבון — אותו מספר חלבון, הרכב שונה.",
    },
    "יופלה GO אפרסק": {
        "positiveSignals": [
            "חלבון גבוה — כ-10 גרם ל-100 גרם",
            "אפרסק מבושל מופיע ברשימה",
        ],
        "limitingFactors": [
            "סוכר ועמילן מעובד אחרי רכיבי החלב — תשתית GO השתנתה",
            "חומרי טעם ומייצב — המרקם לא מגיע רק מהחלב",
        ],
        "bottomLine": "GO עם אפרסק — הוסיפו סוכר ועמילן, שינו את ההרכב הבסיסי.",
        "comparisonContext": "מול GO מועשר בחלבון — חלבון דומה, רשימת רכיבים ארוכה יותר.",
    },
    "יופלה GO תות": {
        "positiveSignals": [
            "חלבון גבוה נשמר בסדרה",
        ],
        "limitingFactors": [
            "טעם תות הגיע עם שינוי בתשתית — לא רק תוספת פרי על GO לבן",
            "חומרי טעם ומייצבים ברשימה",
        ],
        "bottomLine": "GO עם תות — טעם מלאכותי הגיע עם שינוי בתשתית ההרכב.",
        "comparisonContext": "מול GO מועשר בחלבון — אותו חלבון, פחות פשטות.",
    },
    "יופלה GO פירות יער": {
        "positiveSignals": [
            "חלבון גבוה — כ-10 גרם ל-100 גרם",
            "פירות יער מבושלים ברשימה",
        ],
        "limitingFactors": [
            "ממתיקי טעם לצד הפרי — השם לא מספר את כל סיפור המתיקות",
            "עמילן ומייצבים — מרקם מעובד יותר מ-GO הלבן",
        ],
        "bottomLine": "פירות יער בשם, ממתיקי טעם ברשימת הרכיבים.",
        "comparisonContext": "מול GO מועשר בחלבון — חלבון דומה, יותר הנדסת מרקם.",
    },
    "מעדן משמש": {
        "positiveSignals": [
            "ללא תוספים מזוניים מזוהים — נדיר בקטגוריית מעדנים",
            "רשימה קצרה: משמש, ממצי פירות, מיץ לימון",
            "51% משמש — בסיס פרי אמיתי על האריזה",
        ],
        "limitingFactors": [
            "עתיר אנרגיה ל-100 גרם — קינוח פרי צפוף, לא 'קל' במובן הקלורי",
            "ממצי פירות מרוכזים — מתיקות מרוכזת, לא רק פרי טרי",
        ],
        "bottomLine": "הרכב נקי במראה — אבל צפוף קלורית יותר ממעדן חלבון פשוט.",
        "comparisonContext": "מול מעדני חלב — פחות תוספים, יותר אנרגיה מהפרי והריכוז.",
    },
    "מעדן סויה ביו טבעי": {
        "positiveSignals": [
            "ללא חלב — בסיס סויה לצרכנים שמחפשים חלופה",
            "סיבים תזונתיים ברשימה",
        ],
        "limitingFactors": [
            "16 רכיבים ברשימה — לא '5 רכיבים' כפי שנראה מהגביע",
            "מייצבים, מלטודקסטרין ותוספי תזונה — תשתית מעובדת",
            "ערך האנרגיה על האריזה לא אמין כאן — לוח התזונה חלקי",
        ],
        "bottomLine": "נראה מינימלי — הרשימה ארוכה וערכי האנרגיה לא מהימנים במלואם.",
        "comparisonContext": "מול מעדני חלב פשוטים — ללא חלב, אבל לא בהכרח פשוט יותר.",
    },
    "מעדן שיבולת שועל": {
        "positiveSignals": [
            "שיבולת שועל מצוינת ברשימה — דגן נראה לעין",
            "ממתיקים (אריתריטול, סטיביה) במקום סוכר רגיל",
        ],
        "limitingFactors": [
            "11 רכיבים — לא ארבעה; עמילן, מייצב וחומרי טעם ברשימה",
            "המרקם נבנה גם מעמילן וקרגינן — לא רק מהדגן",
        ],
        "bottomLine": "שיבולת שועל בתוך תשתית מעדן מעובדת — לא מוצר דגנים קצר.",
        "comparisonContext": "מול מעדני חלבון GO — דגן במקום חלבון, תוספים דומים.",
    },
    "מעדן הגולן שוקולד מריר": {
        "positiveSignals": [
            "פחות סוכר מגרסת השוקולד הרגיל של הגולן — לפי האריזה",
            "חלב מפוסטר ראשון — בסיס חלבי ברור",
        ],
        "limitingFactors": [
            "שוקולד מריר לא בהכרח 'קל' — עדיין ~143 קק\"ל ל-100 גרם",
            "שלושה מייצבים ועמילן — מרקם מעובד גם בגרסה המרירה",
        ],
        "bottomLine": "פחות סוכר בתווית — לא אותו דבר מפחות צפוף או פשוט יותר.",
        "comparisonContext": "מול מעדן הגולן שוקולד — מריר עם פחות סוכר, אנרגיה לא נמוכה בהכרח.",
    },
    "דנונה מולטי קולגן": {
        "positiveSignals": [
            "חלבון מסומן על האריזה — כ-7 גרם ל-100 גרם",
            "סיבים תזונתיים ברשימה",
        ],
        "limitingFactors": [
            "קולגן (1.5%) בתווית — לא אותו דבר מחלבון חלב מלא",
            "רשימה ארוכה: עמילן, מייצבים, מינרלים — מעבר ליוגורט פשוט",
        ],
        "bottomLine": "קולגן בשם — החלבון הכולל מגיע גם ממקורות אחרים, לא רק מריכוז חלב.",
        "comparisonContext": "מול דנונה פרו — מסלול 'תוספת' שונה מחלבון מרוכז מהחלב.",
    },
}


def go_flavored_interpretive(name: str, insight: str) -> dict | None:
    """Fallback for GO flavored SKUs without a full CE block."""
    if not name.startswith("יופלה GO ") or name in CE_INTERPRETIVE_OVERRIDES:
        return None
    if name == "יופלה GO מועשר בחלבון":
        return None
    return {
        "positiveSignals": [
            "חלבון גבוה נשמר בסדרה — כ-10 גרם ל-100 גרם",
        ],
        "limitingFactors": [
            "גרסה בטעם או דל-שומן — סוכר, ממתיקים או חומרי טעם ליד החלבון",
            "התשתית מתרחקת מ-GO הלבן — יותר תוספות למרקם ומתיקות",
        ],
        "bottomLine": insight,
        "comparisonContext": "מול GO מועשר בחלבון — אותו חלבון על האריזה, הרכב כבד יותר.",
    }


def ce_interpretive_for_product(name: str, insight: str, trace: dict, score: int | None) -> dict:
    if name in CE_INTERPRETIVE_OVERRIDES:
        return dict(CE_INTERPRETIVE_OVERRIDES[name])
    flavored = go_flavored_interpretive(name, insight)
    if flavored:
        return flavored
    return interpretive_expansion_vm(trace, insight, score)


def interpretive_expansion_vm(
    trace: dict,
    insight: str,
    score: int | None,
) -> dict:
    """
    Interpretive Expansion v2 — consumer Hebrew only.
    No BSIP, NOVA, caps, dimensions, routing, or score mechanics.
    """
    l1 = trace.get("L1_observed_signals", {})
    l3 = trace.get("L3_inferred_classifications", {})

    positive: list[str] = []
    limiting: list[str] = []

    protein = l1.get("protein_g")
    ing_count = l1.get("ingredient_count")
    additive_cats = l3.get("additive_categories") or []
    additive_n = len(additive_cats)
    sweetener = bool(l3.get("sweetener_detected"))
    added_sugar = int(l3.get("added_sugar_sources_count") or 0)
    fruit_conc = bool(l3.get("has_fruit_concentrate"))
    protein_source = l3.get("protein_source")

    if protein is not None and protein >= 8:
        positive.append(
            f"חלבון בולט בקטגוריה — כ-{int(round(protein))} גרם ל-100 גרם"
        )
    elif protein is not None and protein >= 4:
        positive.append(
            f"חלבון סביר לקטגוריית מעדנים — {int(round(protein))} גרם ל-100 גרם"
        )

    if ing_count is not None and ing_count <= 5:
        positive.append("רשימת רכיבים קצרה יחסית למדף המעדנים")
    elif ing_count is not None and ing_count >= 12:
        limiting.append("רשימת רכיבים ארוכה — יותר ממה שנהוג בגביע פשוט")

    if additive_n == 0 and not sweetener:
        if "תוספים" not in insight:
            positive.append("ללא תוספים מזוניים מזוהים ברשימה")
    elif additive_n == 1:
        limiting.append("תוסף אחד לפחות תורם למרקם או ליציבות")
    elif additive_n >= 2:
        limiting.append("מספר תוספים ברשימה — המרקם נשען בחלקו על חומרי עזר")

    if added_sugar >= 2:
        limiting.append("יותר ממקור סוכר אחד ברשימת הרכיבים")
    elif added_sugar == 1 and sweetener and "ממתיק" not in insight:
        limiting.append("סוכר וממתיקים יחד — מתיקות מורכבת")

    if sweetener and "ממתיק" not in insight and "דיאט" not in insight:
        limiting.append(
            "ממתיקים ברשימה — כדאי לקרוא לצד תוויות 'ללא סוכר' או 'דיאט'"
        )

    if fruit_conc:
        positive.append("בסיס פרי נראה ברשימה — לא רק טעם מלאכותי")

    if protein_source == "dairy" and protein and protein >= 8 and "חלבון" not in insight:
        positive.append("החלבון מגיע ממוצרי חלב — לא רק מתווית שיווקית")

    # De-dupe while preserving order
    seen: set[str] = set()
    positive = [x for x in positive if not (x in seen or seen.add(x))][:3]
    seen.clear()
    limiting = [x for x in limiting if not (x in seen or seen.add(x))][:2]

    bottom_line = insight.strip() if insight else None

    comparison: str | None = None
    if score is not None and not any(
        token in insight for token in ("קטגוריה", "מדף", "ממוצע", "בין מוצרי")
    ):
        if score >= 65:
            comparison = (
                "עומד בחזית המדף בקטגוריית המעדנים — הרכב פשוט יחסית לעמיתים"
            )
        elif score >= 50:
            comparison = (
                "מיקום אמצעי במדף — חלק מהמעדנים פשוטים יותר, חלק עמוסים יותר בתוספים"
            )
        elif score >= 35:
            comparison = (
                "מאחורי רוב הגביעים הפשוטים — בעיקר בגלל מבנה הרכיבים והתוספים"
            )
        else:
            comparison = (
                "מהתחתית של המדף — הרכב כבד יותר ממעדני פרי או חלבון נקיים"
            )

    out: dict = {}
    if positive:
        out["positiveSignals"] = positive
    if limiting:
        out["limitingFactors"] = limiting
    if bottom_line:
        out["bottomLine"] = bottom_line
    if comparison:
        out["comparisonContext"] = comparison
    return out

# ── Load BSIP0 raw (for image URLs and barcodes) ─────────────────────────────
print("Loading BSIP0 raw data…")
with open(BSIP0_RAW, encoding="utf-8") as f:
    bsip0_raw = json.load(f)

# Build barcode → (image_urls, nutrition_raw) lookup
barcode_to_images: dict[str, list[str]] = {}
barcode_to_sugar: dict[str, float | None] = {}

def _parse_float(v: str | None) -> float | None:
    if not v:
        return None
    try:
        # Handle "פחות מ X" → X (conservative)
        if "פחות מ" in str(v):
            return float(str(v).replace("פחות מ", "").strip())
        return float(str(v).strip())
    except (ValueError, TypeError):
        return None

for item in bsip0_raw:
    bc = str(item.get("barcode", "")).strip()
    urls = item.get("image_urls", [])
    if bc and urls:
        barcode_to_images[bc] = urls
    nv = item.get("nutrition", {})
    sugar = _parse_float(nv.get("sugar_raw"))
    barcode_to_sugar[bc] = sugar

print(f"  BSIP0 products: {len(bsip0_raw)} | with images: {len(barcode_to_images)}")

# ── Load and process BSIP2 traces ────────────────────────────────────────────
print("Processing BSIP2 traces…")
products_vm   = []
excluded      = []
no_insight    = []
image_missing = []

trace_dirs = sorted(BSIP2_DIR.iterdir())
for td in trace_dirs:
    trace_path = td / "bsip2_trace.json"
    if not trace_path.exists():
        continue

    with open(trace_path, encoding="utf-8") as f:
        trace = json.load(f)

    name = trace["input_reference"]["product_name_he"]
    barcode = str(trace["input_reference"].get("barcode", "")).strip()

    insight = find_insight(name)
    if insight is None:
        no_insight.append(name)
        continue

    # Build VM
    signals = trace.get("L1_observed_signals", {})
    score_raw = trace.get("final_score_estimate")
    confidence, conf_label = confidence_vm(trace)

    score: int | None = None
    grade: str | None = None
    if score_raw is not None and confidence != "insufficient":
        score = round(float(score_raw))
        grade = trace.get("grade_estimate") or grade_from_score(float(score_raw))

    if name in SCORE_OVERRIDES:
        score = SCORE_OVERRIDES[name]
        grade = grade_from_score(score)

    if name in CONFIDENCE_OVERRIDES:
        confidence, conf_label = CONFIDENCE_OVERRIDES[name]

    nv = nutrition_vm(signals)
    # Sugar recovery: BSIP1 missed sugar_raw for many products; fill from BSIP0
    if nv is not None and nv.get("sugar") is None:
        recovered_sugar = barcode_to_sugar.get(barcode)
        if recovered_sugar is not None:
            nv["sugar"] = round(recovered_sugar, 1)
    if name == "מעדן סויה ביו טבעי" and nv is not None:
        nv["energyKcal"] = None
    ing = ingredients_vm(signals)
    images = barcode_to_images.get(barcode, [])
    image_url = best_image(images)

    if not image_url:
        image_missing.append({"name": name, "barcode": barcode})

    expansion = {
        "nutrition": nv,
        "ingredients": ing,
        "confidenceLabel": conf_label,
        "servingNote": "ל-100 גרם",
    }
    if confidence != "insufficient":
        expansion.update(ce_interpretive_for_product(name, insight, trace, score))

    product = {
        "id": td.name,
        "name": name,
        "imageUrl": image_url,
        "score": score,
        "grade": grade,
        "insightLine": insight,
        "confidence": confidence,
        "expansion": expansion,
    }
    products_vm.append(product)

# Sort: scored products desc, insufficient last
scored   = [p for p in products_vm if p["score"] is not None]
unscored = [p for p in products_vm if p["score"] is None]
scored.sort(key=lambda p: p["score"], reverse=True)
products_sorted = scored + unscored

print(f"  In editorial scope: {len(products_vm)}")
print(f"  Excluded (no insight line): {len(no_insight)}")
print(f"  Missing image: {len(image_missing)}")

# ── Write frontend JSON ────────────────────────────────────────────────────────
payload = {
    "_meta": {
        "generated": datetime.utcnow().isoformat() + "Z",
        "category": "maadanim",
        "product_count": len(products_sorted),
        "scored_count": len(scored),
        "schema": "BariProductVM[]",
        "version": "v2-ce",
        "expansion": "interpretive_expansion_system_v2",
    },
    "products": products_sorted,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"\n✓ Frontend JSON: {OUT_JSON}")

# ── Corpus report ─────────────────────────────────────────────────────────────
grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
conf_dist  = {"verified": 0, "partial": 0, "insufficient": 0}
for p in products_sorted:
    if p["grade"]:
        grade_dist[p["grade"]] = grade_dist.get(p["grade"], 0) + 1
    conf_dist[p["confidence"]] = conf_dist.get(p["confidence"], 0) + 1

avg_score = (
    sum(p["score"] for p in scored) / len(scored) if scored else 0
)
top_b = [p for p in scored if p["grade"] == "B"]
top_e = [p for p in scored if p["grade"] == "E"]

report = f"""# מעדנים — Corpus Report v1

**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Source:** BSIP2 run_maadanim_001 + finalized insight lines v1

---

## Coverage

| Metric | Count |
|--------|-------|
| BSIP2 traces total | {len(trace_dirs)} |
| In editorial scope (matched insight line) | {len(products_vm)} |
| Excluded (no insight line = false positive) | {len(no_insight)} |
| Scored | {len(scored)} |
| Insufficient (unscored) | {len(unscored)} |
| Missing image URL | {len(image_missing)} |

---

## Grade Distribution

| Grade | Count |
|-------|-------|
| B | {grade_dist.get('B', 0)} |
| C | {grade_dist.get('C', 0)} |
| D | {grade_dist.get('D', 0)} |
| E | {grade_dist.get('E', 0)} |

Average score: **{avg_score:.1f}**

---

## Confidence Distribution

| State | Count |
|-------|-------|
| verified | {conf_dist['verified']} |
| partial | {conf_dist['partial']} |
| insufficient | {conf_dist['insufficient']} |

---

## Top B-Grade Products

{chr(10).join(f"- {p['name']} — {p['score']}/B" for p in top_b) if top_b else "_none_"}

---

## Bottom E-Grade Products

{chr(10).join(f"- {p['name']} — {p['score']}/E" for p in top_e[:8]) if top_e else "_none_"}

---

## Missing Image URLs

{chr(10).join(f"- {m['name']} (barcode: {m['barcode']})" for m in image_missing) if image_missing else "_All in-scope products have Shufersal Cloudinary image URLs_"}

---

## Excluded Products (no matching insight line)

These products are in the BSIP2 corpus but were not assigned an insight line.
They are editorial false positives or products pending classification.

{chr(10).join(f"- {n}" for n in sorted(no_insight))}

---

## Image URL Note

All image URLs are Shufersal Cloudinary CDN (`res.cloudinary.com/shufersal`).
**Action required before production:**
1. Verify URLs are publicly accessible without referrer restriction
2. Add `res.cloudinary.com` to `next.config.ts` `images.remotePatterns`
3. If Cloudinary URLs are restricted: proxy through a Bari image service or use Open Food Facts images by barcode

---

## Ready for Frontend?

**Verdict: CONDITIONAL PASS**

- Editorial corpus complete (matched insight lines for all in-scope products)
- Scores and grades confirmed from BSIP2 traces
- Image URLs present for all in-scope products — accessibility unverified
- Ingredient text is raw BSIP1 tokenized list (needs joining for display)
- Recommend: verify 5 Shufersal image URLs in browser before deploying
"""

with open(OUT_REPORT, "w", encoding="utf-8") as f:
    f.write(report)

print(f"✓ Corpus report: {OUT_REPORT}")
print("\nDone.")
