import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC = Path(r'C:\Bari\02_products\maadanim\maadanim_frontend_v1.json')
DST = Path(r'C:\Bari\02_products\maadanim\maadanim_frontend_v2.json')

with open(SRC, encoding='utf-8') as f:
    data = json.load(f)

# ─────────────────────────────────────────────
# REAL FRUIT DETECTION
# These patterns indicate actual fruit content (not monk fruit sweetener or carrot colorant)
# ─────────────────────────────────────────────
REAL_FRUIT_PATTERNS = [
    'תות מבושל', 'מחית תות', 'תות שדה (',
    'תות (', 'תות שדה מבושל',
    'בננה (', 'מחית בננה',
    'אפרסק מבושל', 'מחית אפרסק', 'אפרסק (',
    'פירות יער', 'מחיות פרי (',
    'ממיצי פירות', 'מיצי פירות',
    'פטל (', 'אוכמניות (',
    'דובדבן מבושל', 'דובדבן (',
    'קוביות תפוח', 'פרי תות שדה',
    'משמש (', 'משמש',  # The product has 51% apricot
    'רוטב פירות יער',
    'פרי תות',
]
NO_FRUIT_INDICATORS = ['לא מכיל פירות', 'אינו מכיל פרי']
FALSE_FRUIT_SIGNAL = "בסיס פרי נראה ברשימה — לא רק טעם מלאכותי"


def has_real_fruit(ingredients: str) -> bool:
    if not ingredients:
        return False
    for ind in NO_FRUIT_INDICATORS:
        if ind in ingredients:
            return False
    for pat in REAL_FRUIT_PATTERNS:
        if pat in ingredients:
            return True
    return False


# ─────────────────────────────────────────────
# PRODUCT-SPECIFIC OVERRIDES
# Keyed by product id
# ─────────────────────────────────────────────
SPECIFIC = {
    # GO דובדבן 0.7% — score already corrected 48→52 in v1. Add _calibration audit field.
    "bsip1_maadanim_7290110323585": {
        "_calibration": {
            "score_v1": 48, "grade_v1": "D",
            "score_v2": 52, "grade_v2": "C",
            "delta": 4,
            "correction_type": "macro_profile_reassessment",
            "note": "10g protein, 60 kcal — D grade alongside 143 kcal chocolate puddings was incorrect positioning"
        }
    },

    # מלבי שמנת — no positiveSignals at all; fix
    "bsip1_maadanim_5431968": {
        "set_positive": [
            "פיסטוק וקוקוס כתוספת ממשית — לא רק תבלין",
            "בסיס שמנת וחלב — מרקם מסורתי",
        ],
        "set_limiting": [
            "חומר משמר E202 ברשימה — שימור שמנת לחיי מדף ארוכים",
            "שני מייצבים — המרקם לא מגיע רק מהשמנת",
        ],
        "set_bottom": "מלבי בסגנון מסורתי — פיסטוק וקוקוס אמיתיים, גם עם חומר משמר.",
        "set_comparison": "מבין מוצרי המלבי — פשוט יחסית, עם תוספת פרי יער.",
    },

    # מעדן הגולן וניל — no positiveSignals
    "bsip1_maadanim_7290110557133": {
        "set_positive": [
            "חלב מפוסטר (78%) — בסיס חלבי גבוה ביחס לקטגוריה",
        ],
        "set_limiting": [
            "ארבעה מייצבים ברשימה — קרגינאן, גואר גאם, סודיום פוספאט, פוליפוספאט",
            "עמילן מעובד — מרקם נוסף שלא מגיע מהחלב",
        ],
        "set_bottom": "חלב גבוה בבסיס — ארבעה מייצבים מכבידים על ציון שיכל להיות גבוה יותר.",
        "set_comparison": "מול מעדן הגולן שוקולד — הוניל עם יותר מייצבים, אותו מנגנון עיבוד.",
    },

    # מעדן חצילים — no positiveSignals
    "bsip1_maadanim_7296073725640": {
        "set_positive": [
            "חציל מטוגן (40%) — הרכב ירק שאין לו מקבילה בקטגוריה",
            "רסק עגבניות (18%) ובצל מטוגן — בסיס ירקות אמיתי",
        ],
        "set_limiting": [
            "שמן סויה מזוכך שלוש פעמים ברשימה — תשתית שמן בפועל",
            "חומר משמר (פוטסיום סורבט) ומייצב",
        ],
        "set_bottom": "מוצר שאינו מעדן חלב — ירק ושמן, לא חלב ולא קינוח.",
        "set_comparison": "הקטגוריה מוגדרת חלב — מעדן החצילים שונה לחלוטין בהרכב.",
    },

    # מילקי בטעם שוקולד — flagship but bottom of category; fix limiting
    "bsip1_maadanim_72940761": {
        "set_positive": [],
        "set_limiting": [
            "חמישה מייצבים ברשימה — קרגינאן, סודיום פוספאט, פוליפוספאט, קסנטאן גאם, ועוד",
            "שמנת לפני חלב — תשתית שומן גבוהה, חלבון נמוך מ-4 גרם",
        ],
        "set_bottom": "הגביע הכי מוכר בקטגוריה, הציון הנמוך בה — מייצבים רבים, חלבון נמוך.",
        "set_comparison": "מול GO מועשר — 30 נקודות הפרש, חלבון שליש, מייצבים פי חמישה.",
    },

    # באדי תות שדה — explicitly לא מכיל פירות; fix signals
    "bsip1_maadanim_72961544": {
        "set_positive": [],
        "set_limiting": [
            "\"לא מכיל פירות\" כתוב על האריזה — טעם מחומרי טעם בלבד",
            "עמילן מעובד ופקטין — המרקם על תוספים, לא על חלב סמיך",
        ],
        "set_bottom": "מעדן ילדים — ללא פרי, טעם תות מלאכותי לחלוטין.",
    },

    # לימבו פטל — water+sugar+stabilizers, zero protein, zero fat, no fruit
    "bsip1_maadanim_7290110565435": {
        "set_positive": [],
        "set_limiting": [
            "מים וסוכר כרכיבים הראשונים — אין בסיס חלב",
            "אין חלבון, אין שומן — לא קינוח חלב בשום מובן",
        ],
        "set_bottom": "ג'לי ממותק — מים, סוכר ומייצבים. לא חלב ולא פרי.",
        "set_comparison": "מהתחתית של המדף — המוצר הרחוק ביותר מקטגוריית מעדן החלב.",
    },

    # מעדן מוו בטעם שוקולד — only monk fruit as "fruit", remove signal
    "bsip1_maadanim_7290102396399": {
        "set_positive": [],
        "set_limiting": [
            "פרוקטוז כממתיק נוסף לצד סוכר — שני מקורות סוכר",
            "חמשה מייצבים (כולל קרגינן) — כפי שמשקף הציון",
        ],
    },

    # מעדן מוו וניל מארז — same issue
    "bsip1_maadanim_7290102396405": {
        "set_positive": [],
        "set_limiting": [
            "פרוקטוז לצד סוכר — שני מקורות ממתיקים",
            "מייצבים ועמילן — מרקם מובנה על תוספים",
        ],
    },

    # דני שוקולד 1.5% — monk fruit only, remove fruit signal
    "bsip1_maadanim_72993637": {
        "set_positive": [],
        "set_limiting": [
            "שלושה מייצבים — קרגינאן, סודיום פוספאט, פוליפוספאט",
            "סוכר ברכיב הראשון — הבסיס הוא סוכר לפני קקאו",
        ],
    },

    # מילקי בטעם תות — no real strawberry (only colors/flavors)
    "bsip1_maadanim_7290105368331": {
        "set_positive": [],
        "set_limiting": [
            "ארבעה מייצבים ברשימה",
            "טעם תות מחומרי טעם וריח — ללא פרי ממשי",
        ],
        "set_bottom": "מילקי תות — אותה תשתית מייצבים, הטעם מחומרי ריח.",
    },

    # מילקי עם 26% פחות סוכר — monk fruit only
    "bsip1_maadanim_7290112344755": {
        "set_positive": [],
        "set_limiting": [
            "\"26% פחות סוכר\" — רכז פרי המונק (ממתיק) מחליף חלק מהסוכר",
            "ארבעה מייצבים — אותה תשתית כימית של הגביע הרגיל",
        ],
        "set_bottom": "פחות סוכר — לא פחות עיבוד; הציון זהה כמעט לגרסה הרגילה.",
    },

    # מילקי בטעם פסק זמן — monk fruit only
    "bsip1_maadanim_7290110560836": {
        "set_positive": [],
        "set_limiting": [
            "חמישה מייצבים — המורכב ביותר ברשימת מילקי",
            "רכז פרי המונק (ממתיק) + קקאו + שוקולד מריר — שלוש שכבות טעם",
        ],
        "set_bottom": "שוקולד ועוגיות — מרכיב הטעם עשיר, אבל גם העיבוד.",
    },

    # מילקי שכבות שוקולד+קצפת — monk fruit only
    "bsip1_maadanim_7290110557423": {
        "set_positive": [],
        "set_limiting": [
            "ארבעה מייצבים לבסיס המעדן + מתחלב — עיבוד רב-שלבי",
            "שני מקורות סוכר + קקאו — גביע עשיר בתוספים",
        ],
        "set_bottom": "שתי שכבות — הסוכר מופיע פעמיים, המייצבים פי שניים.",
    },

    # מילקי שכבות שוקולד קוקוס — monk fruit only
    "bsip1_maadanim_7290119380558": {
        "set_positive": [],
        "set_limiting": [
            "חמישה מייצבים + מתחלב — רשימה כבדה לגביע שכבות",
            "רכז פרי המונק (ממתיק) — 'פחות סוכר' בפועל, לא פחות עיבוד",
        ],
        "set_bottom": "קוקוס בשם — סוכר, מייצבים וקוקוס ברשימת הרכיבים.",
    },

    # דניאלה תות בננה — no real fruit (only colors/flavors)
    "bsip1_maadanim_7290112349606": {
        "set_positive": [
            "חלבון 5 גרם — ממוצע סביר לקטגוריה",
        ],
        "set_comparison": "מאחורי רוב הגביעים הפשוטים — מייצבים וג'לטין מכבידים.",
    },

    # דניאלה תות מוקצף — no real fruit
    "bsip1_maadanim_8693134": {
        "set_positive": [
            "חלבון 5 גרם — ממוצע סביר לקטגוריה",
        ],
        "set_comparison": "מאחורי רוב הגביעים הפשוטים — הקצף מוסיף מייצבים, לא ערך.",
    },

    # דניאלה בננה — no real banana
    "bsip1_maadanim_7290011194215": {
        "set_positive": [
            "חלבון 5 גרם — ממוצע סביר לקטגוריה",
        ],
    },

    # דניאלה בטעם ענבים — explicitly "לא מכיל פירות"
    "bsip1_maadanim_7290112349637": {
        "set_positive": [
            "חלבון 5 גרם — ממוצע סביר לקטגוריה",
        ],
        "set_limiting": [
            "\"לא מכיל פירות\" — טעם ענבים מחומרי טעם בלבד",
            "שני מייצבים + ג'לטין + שני עמילנים ברשימה",
        ],
        "set_bottom": "ענבים בתווית, טעם מלאכותי בפועל — \"לא מכיל פירות\" כתוב על האריזה.",
    },

    # מעדן גבינה מוקצף וניל — no fruit
    "bsip1_maadanim_5838002": {
        "set_positive": [
            "חלבון 5 גרם — ממוצע סביר לקטגוריה",
        ],
    },

    # יופלה טיוב בטעם וניל — no fruit (only carrot color)
    "bsip1_maadanim_7290110325510": {
        "set_positive": [],
        "set_limiting": [
            "שני עמילנים מעובדים ושני מייצבים — נוסחת טיוב מרובת תוספים",
            "ביפידוס כתוספת — לא שווה ערך לפרוביוטי יוגורט מסורתי",
        ],
        "set_bottom": "וניל במוצצת — תשתית עיבוד כבדה, לא GO לבן בשם אחר.",
    },
}

# ─────────────────────────────────────────────
# APPLY CHANGES
# ─────────────────────────────────────────────
changes_log = []

for product in data['products']:
    pid = product['id']
    expansion = product.get('expansion', {})
    ingredients = expansion.get('ingredients', '') or ''

    # 1. Apply product-specific overrides
    if pid in SPECIFIC:
        fix = SPECIFIC[pid]

        if '_calibration' in fix:
            product['_calibration'] = fix['_calibration']
            changes_log.append(f"[calibration] {product['name']}")

        if 'set_positive' in fix:
            expansion['positiveSignals'] = fix['set_positive']
            changes_log.append(f"[set_positive] {product['name']}")

        if 'set_limiting' in fix:
            expansion['limitingFactors'] = fix['set_limiting']

        if 'set_bottom' in fix:
            expansion['bottomLine'] = fix['set_bottom']

        if 'set_comparison' in fix:
            expansion['comparisonContext'] = fix['set_comparison']

        product['expansion'] = expansion

    # 2. Systematic false-fruit signal removal (for products NOT in SPECIFIC_FIXES)
    else:
        pos = list(expansion.get('positiveSignals', []))
        if FALSE_FRUIT_SIGNAL in pos and not has_real_fruit(ingredients):
            pos.remove(FALSE_FRUIT_SIGNAL)
            expansion['positiveSignals'] = pos
            changes_log.append(f"[false_fruit_removed] {product['name']}")
            product['expansion'] = expansion

# ─────────────────────────────────────────────
# UPDATE METADATA
# ─────────────────────────────────────────────
data['_meta']['version'] = 'v2'
data['_meta']['generated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
data['_meta']['v2_changes'] = {
    'false_fruit_signals_removed': sum(1 for c in changes_log if 'false_fruit' in c),
    'specific_product_fixes': sum(1 for c in changes_log if 'set_positive' in c or 'calibration' in c),
    'score_corrections': '1 (GO דובדבן: 48→52, applied in v1, _calibration field added in v2)',
}

# ─────────────────────────────────────────────
# WRITE OUTPUT
# ─────────────────────────────────────────────
with open(DST, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Written: {DST}")
print(f"\n{len(changes_log)} changes:")
for c in changes_log:
    print(f"  {c}")
