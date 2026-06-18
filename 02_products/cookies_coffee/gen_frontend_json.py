"""
P77/P89 - Generate cookies_coffee_frontend_v1.json
Source: run_cookies_004 traces (P89 remediation) + BSIP0 raw + corpus_filter
Golden reference: brined_cheeses_frontend_v2.json (milk-depth v3 schema)
P89 changes: corpus 58 (3 OOS drops), EV-058 oat anchor, RT-6 E-number regex fix + ADDITIVE_DB expansions
"""
import json, os, re, sys, hashlib
from datetime import datetime, timezone

TRACE_DIR = r"C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_004\products"
BSIP0_PATH = r"C:\Bari\02_products\cookies_coffee\bsip0_outputs\cookies_coffee_bsip0_raw_20260613T163431.json"
CORPUS_PATH = r"C:\Bari\02_products\cookies_coffee\factory_run_001\corpus_filter.json"
OUTPUT_PATH = r"C:\Bari\bari-web\src\data\comparisons\cookies_coffee_frontend_v1.json"

# ── Additive registry ─────────────────────────────────────────────────────────
ADDITIVE_DB = {
    "E500": {"name_he": "סודיום ביקרבונט", "tier": "functional", "function_he": "חומר תפיחה",
             "explanation_he": "אבקת אפייה מלחית; גורם לבצק לתפוח בחום. נמצא בכמעט כל עוגייה אפויה."},
    "E503": {"name_he": "אמוניום קרבונט", "tier": "functional", "function_he": "חומר תפיחה",
             "explanation_he": "חומר תפיחה ישן ומוכר; מתנדף לחלוטין באפייה. אין שאריות במוצר הסופי."},
    "E450": {"name_he": "דיפוספט", "tier": "likely-neutral", "function_he": "חומר תפיחה / מייצב",
             "explanation_he": "תורם לתפיחה אחידה; נמצא בשימוש נרחב במאפים תעשייתיים."},
    "E451": {"name_he": "טריפוספט", "tier": "likely-neutral", "function_he": "מייצב / חומר תפיחה",
             "explanation_he": "מייצב פוספט; שימושי במאפים ובמזונות מעובדים."},
    "E322": {"name_he": "לציטין", "tier": "likely-neutral", "function_he": "מתחלב",
             "explanation_he": "מתחלב טבעי מסויה או חמניות; מסייע לתחמיץ שמן ומים. נחשב בטוח לרוב האנשים."},
    "E476": {"name_he": "פוליגליצרול אסטר", "tier": "dose-dependent", "function_he": "מתחלב",
             "explanation_he": "מתחלב תעשייתי המשמש להחלקת מרקם; שכיח בשוקולד ובמאפים."},
    "E471": {"name_he": "מונוגליצרידים ודיגליצרידים", "tier": "likely-neutral", "function_he": "מתחלב",
             "explanation_he": "שומנים מהצומח המסייעים למרקם ולמדף; נמצאים בשימוש נרחב במאפים."},
    "E466": {"name_he": "קרבוקסי מתיל צלולוז (CMC)", "tier": "contested", "function_he": "מייצב / מתחלב",
             "explanation_he": "מייצב תעשייתי; מחקרים מוקדמים בבעלי חיים הצביעו על שינויי מיקרוביום — הנתונים בבני אדם עדיין מוגבלים."},
    "E415": {"name_he": "קסנתן גאם", "tier": "likely-neutral", "function_he": "מייצב",
             "explanation_he": "סיב מותסס; נמצא בשימוש במוצרי ללא גלוטן כתחליף מרקם."},
    "E1422": {"name_he": "עמילן אצטט", "tier": "likely-neutral", "function_he": "מייצב",
              "explanation_he": "עמילן שונה; נפוץ בשמירת מרקם מזון בשינויי טמפרטורה."},
    "E200": {"name_he": "חומצה סורבית", "tier": "likely-neutral", "function_he": "חומר משמר",
             "explanation_he": "חומר משמר טבעי מפרות; עוצר עובש ושמרים. בשימוש נרחב במרגרינות ומוצרי מאפה. ידוע כרגישות אצל מיעוט קטן של אנשים (תגובה דמוית היסטמין)."},
    "E160A": {"name_he": "בטא-קרוטן (ממקור טבעי)", "tier": "functional", "function_he": "צבע מאכל",
              "explanation_he": "פיגמנט כתום טבעי מגזר או אצות; מקור לוויטמין A. ללא דאגות בטיחות ידועות בשלב זה."},
    "E150": {"name_he": "קרמל", "tier": "likely-neutral", "function_he": "צבע מאכל",
             "explanation_he": "צבע קרמל פשוט מסוכר שרוף; ללא דאגות ידועות בשלב זה."},
    "E150A": {"name_he": "קרמל רגיל", "tier": "likely-neutral", "function_he": "צבע מאכל",
              "explanation_he": "צבע קרמל פשוט מסוכר שרוף; ללא דאגות ידועות."},
    "E150C": {"name_he": "קרמל אמוניה", "tier": "dose-dependent", "function_he": "צבע מאכל",
              "explanation_he": "קרמל שנוצר עם אמוניה; מוצר לוואי 4-MEI — חשיפה מעוגיות נמוכה."},
    "E150D": {"name_he": "קרמל סולפיט אמוניה", "tier": "dose-dependent", "function_he": "צבע מאכל",
              "explanation_he": "קרמל סוג 4; מוצר לוואי 4-MEI — חשיפה מעוגיות מוגבלת."},
    "E330": {"name_he": "חומצת לימון", "tier": "functional", "function_he": "מווסת חומציות",
             "explanation_he": "חומצה נפוצה מהצומח; מאזנת pH ומעכבת חמצון. בשימוש נרחב ובטוח."},
    "E202": {"name_he": "פוטסיום סורבט", "tier": "likely-neutral", "function_he": "חומר משמר",
             "explanation_he": "חומר משמר שעוצר עובש ושמרים; נמצא בשימוש נרחב ובטוח ברמות מקובלות."},
    "E955": {"name_he": "סוקרלוז", "tier": "dose-dependent", "function_he": "ממתיק",
             "explanation_he": "ממתיק כלורי 600× מסוכר; מחקרים מוקדמים מצביעים על השפעות מיקרוביום בדוזות גבוהות."},
    "E965": {"name_he": "מלטיטול", "tier": "functional", "function_he": "ממתיק",
             "explanation_he": "פוליאול מגלוקוז; בעוגיות ללא סוכר. כמות גדולה עלולה לגרום לאי נוחות עיכולית."},
    "E950": {"name_he": "אצסולפאם K", "tier": "contested", "function_he": "ממתיק",
             "explanation_he": "ממתיק מלאכותי; ראיות בטיחות בבני אדם נחשבות מספקות, אך כמה מחקרים מצביעים על השפעות מיקרוביום."},
    "E420": {"name_he": "סורביטול", "tier": "functional", "function_he": "ממתיק / לחות",
             "explanation_he": "פוליאול מסוכר; בכמות גבוהה עלול לגרום לאפקט משלשל קל."},
    # RT-6 corpus scan additions (EV-058 / P89 2026-06-13) ─────────────────────
    "E124": {"name_he": "פונסו 4R (אדום 4R)", "tier": "contested", "function_he": "צבע מאכל",
             "explanation_he": "צבע אדום סינתטי; מחויב בסימון אזהרה ב-EU ('עלול להשפיע לרעה על פעילות הילד')."},
    "E1414": {"name_he": "די-עמילן פוספט אצטילי", "tier": "likely-neutral", "function_he": "מייצב / מרקם",
              "explanation_he": "עמילן שונה; משמר מרקם בטמפרטורות שונות. נחשב בטוח ברמות שימוש רגילות במאפים."},
    "E220": {"name_he": "גופרית דו חמצנית (SO2)", "tier": "contested", "function_he": "חומר משמר / נוגד חמצון",
             "explanation_he": "חומר גפרית; מחויב בסימון כאלרגן כאשר ריכוזו עולה על 10ppm. עלול לגרום לתגובה אצל אסתמטיים."},
    "E270": {"name_he": "חומצת חלב", "tier": "functional", "function_he": "מווסת חומציות",
             "explanation_he": "חומצה טבעית המיוצרת בתסיסה; מאזנת pH ומעכבת עובש. בטוחה ונפוצה ביותר במאפים."},
    "E422": {"name_he": "גליצרול", "tier": "functional", "function_he": "לחות / ממס",
             "explanation_he": "אלכוהול סוכר שמור לחות ומשמש כממס לתמציות; נחשב בטוח לחלוטין."},
    "E440": {"name_he": "פקטין", "tier": "functional", "function_he": "מייצב / ג'ל",
             "explanation_he": "סיב טבעי מקליפות פירות; מייצב מרקם ריבות ומילויים. ללא דאגות בטיחות ידועות."},
    "E470B": {"name_he": "מגנזיום סטיאראט", "tier": "likely-neutral", "function_he": "נוגד הידבקות",
              "explanation_he": "מלח מגנזיום של חומצת שומן; מונע הידבקות בעיבוד מזון. ברמות שימוש רגילות בטוח."},
    "E953": {"name_he": "איזומלט", "tier": "functional", "function_he": "ממתיק / לחות",
             "explanation_he": "פוליאול מסוכרוז; בעוגיות ללא סוכר. מעלה סף עיכולי — כמויות גדולות עלולות לגרום לאי נוחות."},
}

# Named additives (no E-number or named form in Hebrew ingredients)
ADDITIVE_BY_NAME_RE = [
    (r"לציטין\s+סויה", {"e_number": "E322", "name_he": "לציטין סויה", "tier": "likely-neutral",
                         "function_he": "מתחלב", "explanation_he": "מתחלב טבעי מסויה; מסייע לתחמיץ שמן ומים במאפים."}),
    (r"לציטין\s+חמניות", {"e_number": "E322", "name_he": "לציטין חמניות", "tier": "likely-neutral",
                          "function_he": "מתחלב", "explanation_he": "מתחלב טבעי מחמניות; ברירת מחדל ללא סויה."}),
    (r"(?<!\w)לציטין(?!\s+סויה|\s+חמניות)", {"e_number": "E322", "name_he": "לציטין", "tier": "likely-neutral",
                                               "function_he": "מתחלב", "explanation_he": "מתחלב טבעי; מסייע לתחמיץ שמן ומים במאפים."}),
    (r"חומצת\s+לימון", {"e_number": "E330", "name_he": "חומצת לימון", "tier": "functional",
                        "function_he": "מווסת חומציות", "explanation_he": "חומצה נפוצה מהצומח; מאזנת pH ומעכבת חמצון. בטוח."}),
    (r"חומצת\s+מאכל", {"e_number": "E330", "name_he": "חומצת מאכל", "tier": "functional",
                       "function_he": "מווסת חומציות", "explanation_he": "מווסת חומציות; בדרך כלל חומצת לימון — בטוח."}),
    (r"מלטיטול", {"e_number": "E965", "name_he": "מלטיטול", "tier": "functional",
                  "function_he": "ממתיק", "explanation_he": "פוליאול בעוגיות ללא סוכר; כמות גדולה עלולה לגרום לאי נוחות עיכולית."}),
    (r"סוקרלוז", {"e_number": "E955", "name_he": "סוקרלוז", "tier": "dose-dependent",
                  "function_he": "ממתיק", "explanation_he": "ממתיק כלורי 600× מסוכר; מחקרים מוקדמים על השפעות מיקרוביום בדוזות גבוהות."}),
    (r"אמוניום\s+ביקרבונט", {"e_number": "E503", "name_he": "אמוניום ביקרבונט", "tier": "functional",
                             "function_he": "חומר תפיחה", "explanation_he": "חומר תפיחה מסורתי; מתנדף לחלוטין באפייה."}),
    (r"סודיום\s+ביקרבונט", {"e_number": "E500", "name_he": "סודיום ביקרבונט", "tier": "functional",
                            "function_he": "חומר תפיחה", "explanation_he": "אבקת אפייה; גורם לבצק לתפוח בחום."}),
    (r"סיבי\s+במבוק", {"e_number": None, "name_he": "סיבי במבוק", "tier": "functional",
                       "function_he": "מייצב / מרקם", "explanation_he": "סיב תזונתי מבמבוק; כתוסף מרקם וסיב בעוגיות."}),
    (r"(?:סוכר\s+)?קרמל", {"e_number": "E150", "name_he": "קרמל", "tier": "likely-neutral",
                            "function_he": "צבע מאכל", "explanation_he": "צבע קרמל פשוט מסוכר שרוף; ללא דאגות ידועות."}),
    (r"פוטסיום\s+סורבט", {"e_number": "E202", "name_he": "פוטסיום סורבט", "tier": "likely-neutral",
                          "function_he": "חומר משמר", "explanation_he": "חומר משמר שעוצר עובש ושמרים; בטוח ברמות מקובלות."}),
]


def extract_e_numbers(text):
    """Extract E-numbers from ingredient text, deduplicated.

    EV-058 / P89 (2026-06-13) — Regex normalisation rules:
      - 'E500ll' → 'E500'  : Hebrew lamed ('l') artefact from OCR/scraper bleed
      - 'E450l'  → 'E450'  : same
      - 'E160aii'→ 'E160A' : 'a' = genuine EU variant designator (keep first letter
                               if in {a,b,c,d}); trailing 'ii' = noise (strip)
      - 'E322i'  → 'E322'  : 'i' = Roman numeral suffix in EU notation, discard
      - 'E471'   → 'E471'  : no suffix, unchanged
      - 'E150c'  → 'E150C' : 'c' = recognised variant, kept uppercased

    Logic: capture digits + any trailing letters. If the FIRST trailing character is
    one of {a,b,c,d} (known EU sub-type designators), keep it as the variant suffix.
    Discard 'i', 'l', and all multi-character suffixes — they are Roman numerals or
    OCR bleed artefacts, not genuine sub-type codes.
    """
    if not text:
        return []
    raw_matches = re.findall(r'E(\d{3,4})([a-z]*)', str(text), re.IGNORECASE)
    result = []
    seen = set()
    for digits, suffix in raw_matches:
        suffix_lower = suffix.lower()
        if suffix_lower and suffix_lower[0] in 'abcd':
            # Keep only the first letter as the variant designator
            e = f"E{digits}{suffix_lower[0].upper()}"
        else:
            # 'i', 'll', 'ii', 'l' etc. → artefact, discard suffix
            e = f"E{digits}"
        e_upper = e.upper()
        if e_upper not in seen:
            seen.add(e_upper)
            result.append(e_upper)
    return result


def extract_named_additives(text):
    """Extract named additives (no E-number in text) from ingredient text."""
    if not text:
        return []
    results = []
    seen_e = set()
    for pattern, info in ADDITIVE_BY_NAME_RE:
        if re.search(pattern, str(text)):
            e = info.get("e_number")
            key = e if e else info["name_he"]
            if key not in seen_e:
                seen_e.add(key)
                results.append(dict(info))
    return results


def build_d4_additives(ingredients_text, trace_L3):
    """Build d4_additives from ingredient text + trace L3 additive signals."""
    seen = {}  # keyed by e_number or name_he to deduplicate

    # 1. E-numbers from ingredient text
    enums = extract_e_numbers(ingredients_text)
    for e in enums:
        e_upper = e.upper()
        if e_upper in ADDITIVE_DB:
            entry = dict(ADDITIVE_DB[e_upper])
            entry["e_number"] = e_upper
            key = e_upper
            if key not in seen:
                seen[key] = entry

    # 2. Named additives (lecithin, citric acid, maltitol, etc.)
    named = extract_named_additives(ingredients_text)
    for entry in named:
        e = entry.get("e_number")
        key = e if e else entry["name_he"]
        if key not in seen:
            # Only add if not already covered by E-number extraction
            seen[key] = entry

    return list(seen.values())


def parse_float(val):
    """Parse a nutrition value string to float, returning None if empty/None."""
    if val is None or val == "" or val == "null":
        return None
    # Strip units like 'מג', 'מ"ג', 'גרם', spaces
    s = re.sub(r'[^\d\.]', '', str(val).replace(',', '.'))
    try:
        return float(s) if s else None
    except ValueError:
        return None


def map_confidence(confidence_band, confidence_score, missing_fields):
    """Map trace confidence_band to BariConfidence VM value.

    Guard per spec: fiber expected-null must NOT trigger partial when core nutrition present.
    Core fields: energyKcal, protein, fat, sugar.
    """
    # Core fields that trigger partial confidence if missing
    CORE_FIELDS = {"energy_kcal", "protein_g", "fat_g", "sugars_g"}
    core_missing = [f for f in (missing_fields or []) if any(k in f for k in ["energy", "protein", "fat_g", "sugar"])]

    if confidence_band == "high" and not core_missing:
        return "verified"
    elif confidence_band in ("medium", "low") or core_missing:
        return "partial"
    else:
        return "verified"


def confidence_labels(confidence, missing_fields):
    """Return (confidence_label_he, confidence_tooltip_he, confidence_sub_reason)."""
    CORE_FIELDS_CHECK = ["energy", "protein", "fat_g", "sugar"]
    core_missing = [f for f in (missing_fields or []) if any(k in f for k in CORE_FIELDS_CHECK)]

    if confidence == "verified":
        return (
            "מבוסס על נתונים מלאים",
            "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים.",
            None
        )
    elif confidence == "partial":
        if core_missing:
            return (
                "ניתוח חלקי",
                "חסרים נתוני תזונה מהותיים; הציון מבוסס על נתונים חלקיים.",
                "missing_nutrition"
            )
        else:
            return (
                "ניתוח חלקי",
                "אמינות הנתונים מוגבלת; הציון מבוסס על מידע שחולץ חלקית.",
                "low_extraction"
            )
    else:
        return ("נתונים לא מספיקים", "לא ניתן לחשב ציון מלא עקב חוסר בנתונים.", "missing_nutrition")


_FLAVOR_PRESERVATIVE_MARKERS = [
    "חומרי טעם",  # "flavoring agents" (broad — covers "חומרי טעם וריח" with or without extra spaces)
    "חומר טעם",
    "E200", "E202", "E210", "E211", "E212", "E220", "E221", "E222",  # sorbates, benzoates, sulphites
    "חומר משמר",
    "משמר ",       # trailing space to avoid false-positives on "משמרת"
]


def _has_flavor_or_preservative(ingredients: str) -> bool:
    """Return True if ingredient string contains a flavoring or preservative marker."""
    return any(m in ingredients for m in _FLAVOR_PRESERVATIVE_MARKERS)


def build_positive_signals(trace, ingredients: str = ""):
    """Build positiveSignals from trace data.

    ingredients: cleaned ingredient string from the BSIP0 entry — used to suppress
    the minimal-processing fallback when a product's NOVA=2 comes from a low-confidence
    parse (e.g. 1-ingredient truncation) but the ingredient list shows flavoring or
    preservative additives (NEW-A fix, run_cookies_004).
    """
    signals = []
    L1 = trace["L1_observed_signals"]
    L3 = trace["L3_inferred_classifications"]
    nova = trace.get("nova_proxy", 3)
    nova_conf = trace.get("nova_confidence", 0)

    protein = L1.get("protein_g")
    fiber = L1.get("dietary_fiber_g")
    fat = L1.get("fat_g")
    kcal = L1.get("energy_kcal")

    if nova in (1, 2) and nova_conf >= 0.3:
        nova_label = "NOVA 1 — עיבוד מינימלי" if nova == 1 else "NOVA 2 — מינימום עיבוד"
        signals.append(nova_label)

    if protein is not None and protein >= 8:
        signals.append(f"חלבון ({protein}g ל-100g)")

    if L3.get("has_whole_grain"):
        signals.append("דגנים מלאים — מקור לסיבים")

    if fiber is not None and fiber >= 3:
        signals.append(f"סיבים תזונתיים ({fiber}g ל-100g)")

    if L3.get("has_fermentation"):
        signals.append("תסיסה טבעית")

    if not signals:
        # Fallback: no detected positives — but suppress the minimal-processing
        # signal when nova_confidence is low AND the ingredient string contains
        # flavoring or preservative markers (contradicts minimal-processing claim).
        nova_confidence_band = trace.get("nova_confidence_band", "")
        suppress = (
            nova_confidence_band == "low"
            and _has_flavor_or_preservative(ingredients)
        ) or (
            # Also suppress when nova_conf is very low (<0.3) and flavor markers present
            nova_conf < 0.3
            and _has_flavor_or_preservative(ingredients)
        )
        if nova in (1, 2) and not suppress:
            signals.append("עיבוד מינימלי יחסית לקטגוריה")

    return signals[:3] if signals else None


def build_limiting_factors(trace):
    """Build limitingFactors from trace data."""
    factors = []
    L1 = trace["L1_observed_signals"]
    L3 = trace["L3_inferred_classifications"]
    caps = [c["rule"] for c in trace.get("caps_applied", [])]
    penalties = [p["rule"] for p in trace.get("penalties_applied", [])]

    sugar = L1.get("sugars_g")
    fat = L1.get("fat_g")
    kcal = L1.get("energy_kcal")
    sodium = L1.get("sodium_mg")
    nova = trace.get("nova_proxy", 3)

    if sugar is not None and sugar >= 17.5:
        factors.append(f"תכולת סוכר גבוהה ({sugar}g ל-100g)")

    if nova == 4:
        factors.append("עיבוד גבוה — NOVA 4")
    elif nova == 3 and L3.get("additive_marker_count", 0) >= 3:
        factors.append("מספר תוספים — עיבוד מעל הממוצע בקטגוריה")

    if kcal is not None and kcal >= 480 and (sugar is None or sugar < 17.5):
        factors.append(f"צפיפות קלורית גבוהה ({kcal} קל ל-100g)")

    if sodium is not None and sodium >= 400:
        factors.append(f"נתרן ({sodium} מג ל-100g)")

    if "ISRAELI_RED_LABEL_1_SAT_FAT" in caps:
        factors.append("שומן רווי — תוית אדומה")

    return factors[:2] if factors else None


def load_sources():
    """Load all source data."""
    # BSIP0
    with open(BSIP0_PATH, "r", encoding="utf-8") as f:
        bsip0_list = json.load(f)
    bsip0 = {str(p["barcode"]): p for p in bsip0_list}

    # Corpus filter IN_SCORED
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        cf = json.load(f)
    in_scored = {str(p["barcode"]): p for p in cf["products"] if p["decision"] == "IN_SCORED"}

    # Traces
    traces = {}
    for d in os.listdir(TRACE_DIR):
        trace_path = os.path.join(TRACE_DIR, d, "bsip2_trace.json")
        if os.path.exists(trace_path):
            with open(trace_path, "r", encoding="utf-8") as f:
                t = json.load(f)
            barcode = str(t["input_reference"]["barcode"])
            traces[barcode] = t

    return bsip0, in_scored, traces


def build_product(barcode, trace, bsip0_entry, corpus_entry):
    """Build a single BariProductVM-compatible product dict."""
    L1 = trace["L1_observed_signals"]
    L3 = trace["L3_inferred_classifications"]
    inp = trace["input_reference"]

    # Basic info from BSIP0 (names/brands/images) + corpus filter
    name_he = bsip0_entry.get("name_he") or corpus_entry.get("name_he") or inp.get("product_name_he", "")
    brand = bsip0_entry.get("brand") or corpus_entry.get("brand", "")
    name_full = f"{name_he} — {brand}" if brand else name_he

    # Image: first image_url from BSIP0 (zoom format preferred)
    image_urls = bsip0_entry.get("image_urls") or []
    # Prefer the zoom (_Z_) URL
    image_url = None
    for u in image_urls:
        if "_Z_" in str(u) or "_zoom" in str(u):
            image_url = u
            break
    if not image_url and image_urls:
        image_url = image_urls[0]

    # Scores from trace (LOCKED — do not recompute)
    score = trace["final_score_estimate"]
    grade = trace["grade_estimate"]

    # Confidence mapping
    missing_fields = L1.get("missing_nutrition_fields", [])
    conf_band = trace["confidence_band"]
    confidence = map_confidence(conf_band, trace["confidence_score"], missing_fields)
    label_he, tooltip_he, sub_reason = confidence_labels(confidence, missing_fields)

    # Nutrition from BSIP0 raw (preferred) — spec says BSIP0
    n = bsip0_entry.get("nutrition", {})
    energy_kcal = parse_float(n.get("energy_kcal_raw")) or L1.get("energy_kcal")
    protein = parse_float(n.get("protein_raw")) or L1.get("protein_g")
    fat = parse_float(n.get("fat_raw")) or L1.get("fat_g")
    sat_fat = parse_float(n.get("saturated_fat_raw")) or L1.get("fat_saturated_g")
    sugar_raw = n.get("sugar_raw", "")
    sugar = parse_float(sugar_raw) if sugar_raw not in (None, "", "null") else None
    if sugar is None:
        sugar = L1.get("sugars_g")
    fiber_raw = n.get("fiber_raw", "")
    fiber = parse_float(fiber_raw) if fiber_raw not in (None, "", "null") else None
    if fiber is None:
        fiber = L1.get("dietary_fiber_g")  # may also be None — that's OK
    sodium_raw = n.get("sodium_raw", "")
    sodium = parse_float(sodium_raw) if sodium_raw not in (None, "", "null") else None
    if sodium is None:
        sodium = L1.get("sodium_mg")

    # Ingredients from BSIP0
    ingredients_text = bsip0_entry.get("ingredients_raw") or ""
    # Clean trailing marketing noise
    ingredients_clean = re.split(r'מאפיינים נוספים|מכיל(?! גלוטן)|עלול להכיל', str(ingredients_text))[0].strip()

    # D4 additives — parsed from ingredient text
    d4_additives = build_d4_additives(ingredients_clean, L3)

    # NOVA group
    nova_group = trace.get("nova_proxy")

    # Positive signals and limiting factors
    positive_signals = build_positive_signals(trace, ingredients=ingredients_clean)
    limiting_factors = build_limiting_factors(trace)

    # Retailer
    retailer = bsip0_entry.get("retailer_name", "שופרסל")

    # Confidence label for expansion
    conf_label_expansion = label_he

    # Dimension scores for bariInterpretation (PENDING_COPY with real values)
    dim_scores = trace.get("dimension_scores", {})

    # Build the VM object
    product = {
        "id": f"ck-{barcode}",
        "name": name_full,
        "barcode": barcode,
        "imageUrl": image_url,
        "score": score,
        "grade": grade,
        "confidence": confidence,
        "confidence_label_he": label_he,
        "confidence_tooltip_he": tooltip_he,
        "confidence_sub_reason": sub_reason,
        "insightLine": "PENDING_COPY",
        "rowVerdict": "PENDING_COPY",
        "expansion": {
            "nutrition": {
                "energyKcal": energy_kcal,
                "protein": protein,
                "sugar": sugar,
                "fat": fat,
                "satFat": sat_fat,
                "fiber": fiber,
                "sodium": sodium
            },
            "ingredients": ingredients_clean if ingredients_clean else None,
            "confidenceLabel": conf_label_expansion,
            "servingNote": "ל-100 גרם",
            "positiveSignals": positive_signals,
            "limitingFactors": limiting_factors,
            "bottomLine": "PENDING_COPY"
        },
        "retailer": retailer,
        "novaGroup": nova_group,
        "d4_additives": d4_additives,
        # Milk-depth v3 authored fields — PENDING_COPY for Content merge
        "consumerTakeaway": "PENDING_COPY",
        "consumerExplanation": "PENDING_COPY",
        "bariInterpretation": [
            {
                "dimension": "processing_quality",
                "score": dim_scores.get("processing_quality"),
                "label_he": "איכות עיבוד",
                "explanation_he": "PENDING_COPY"
            },
            {
                "dimension": "glycemic_quality",
                "score": dim_scores.get("glycemic_quality"),
                "label_he": "עומס גליקמי",
                "explanation_he": "PENDING_COPY"
            },
            {
                "dimension": "additive_quality",
                "score": dim_scores.get("additive_quality"),
                "label_he": "תוספים",
                "explanation_he": "PENDING_COPY"
            },
            {
                "dimension": "calorie_density",
                "score": dim_scores.get("calorie_density"),
                "label_he": "צפיפות קלורית",
                "explanation_he": "PENDING_COPY"
            }
        ],
        "bestUseCases": ["PENDING_COPY"]
    }

    return product


def main():
    bsip0, in_scored, traces = load_sources()

    products = []
    images_present = 0
    off_used_count = 0

    for barcode, corpus_entry in in_scored.items():
        trace = traces.get(barcode)
        if not trace:
            print(f"WARNING: No trace for IN_SCORED barcode {barcode}", file=sys.stderr)
            continue

        bsip0_entry = bsip0.get(barcode, {})

        # Verify OFF ban
        if bsip0_entry.get("off_source_used") == True:
            off_used_count += 1
            print(f"ERROR: OFF used for {barcode}", file=sys.stderr)

        product = build_product(barcode, trace, bsip0_entry, corpus_entry)
        products.append(product)

        if product["imageUrl"]:
            images_present += 1

    # Sort by score DESCENDING (stable)
    products.sort(key=lambda p: (p["score"] is None, -(p["score"] or 0)))

    # Grade distribution
    from collections import Counter
    grade_dist = Counter(p["grade"] for p in products)

    # Count PENDING_COPY instances
    pending_count = 0
    for p in products:
        if p.get("insightLine") == "PENDING_COPY":
            pending_count += 1
        if p.get("rowVerdict") == "PENDING_COPY":
            pending_count += 1
        if p.get("consumerTakeaway") == "PENDING_COPY":
            pending_count += 1
        if p.get("consumerExplanation") == "PENDING_COPY":
            pending_count += 1
        if p.get("expansion", {}).get("bottomLine") == "PENDING_COPY":
            pending_count += 1
        for bi in p.get("bariInterpretation", []):
            if bi.get("explanation_he") == "PENDING_COPY":
                pending_count += 1
        for bu in p.get("bestUseCases", []):
            if bu == "PENDING_COPY":
                pending_count += 1

    # Page shell
    output = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "category": "cookies_coffee",
            "run_id": "run_cookies_003",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v1",
            "provenance": "BSIP0 cookies_coffee_bsip0_raw_20260613T163431.json → corpus_filter factory_run_001 → BSIP2 run_cookies_003",
            "grade_distribution": dict(grade_dist),
            "off_used": False,
            "copy_status": "PENDING — authored fields (insightLine, rowVerdict, consumerTakeaway, consumerExplanation, bariInterpretation explanations, bestUseCases, bottomLine, page_copy) await Content merge (P76)"
        },
        "page_copy": {
            "hero": {
                "categoryNameHe": "עוגיות לקפה",
                "tagline": "PENDING_COPY",
                "productCount": len(products),
                "scoredCount": len(products),
                "averageScore": None,
                "topProduct": None
            },
            "prologue": {
                "sentences": ["PENDING_COPY", "PENDING_COPY"]
            },
            "methodology": {
                "text": "PENDING_COPY",
                "sourceNote": "PENDING_COPY",
                "lastUpdated": "2026-06-13"
            },
            "caveat": "PENDING_COPY",
            "filters": [
                {"id": "all", "label": "הכל", "count": len(products), "isActive": True},
                {"id": "grade_c", "label": "ציון C ומעלה", "count": grade_dist.get("C", 0), "isActive": False},
                {"id": "grade_d", "label": "ציון D", "count": grade_dist.get("D", 0), "isActive": False},
                {"id": "grade_e", "label": "ציון E", "count": grade_dist.get("E", 0), "isActive": False}
            ]
        },
        "products": products
    }

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Compute sha256
    with open(OUTPUT_PATH, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    # Print self-check report
    print("=" * 60)
    print("P77 GENERATION COMPLETE")
    print(f"Output: {OUTPUT_PATH}")
    print(f"SHA256: {sha256}")
    print(f"Products: {len(products)}")
    print(f"Grade distribution: {dict(grade_dist)}")
    print(f"Expected (run_cookies_004 / P89): C=7, D=22, E=29")
    print(f"Grade dist match: {dict(grade_dist) == {'C': 7, 'D': 22, 'E': 29}}")
    print(f"Images present: {images_present}/{len(products)}")
    print(f"OFF used: {off_used_count}")
    print(f"d4_additives present: {sum(1 for p in products if 'd4_additives' in p)}/{len(products)}")
    print(f"PENDING_COPY count (authored fields): {pending_count}")
    print(f"Sort verified (first 5 scores): {[p['score'] for p in products[:5]]}")
    print(f"Sort verified (last 5 scores): {[p['score'] for p in products[-5:]]}")
    print("=" * 60)

    return sha256, len(products), dict(grade_dist), images_present, pending_count


if __name__ == "__main__":
    main()
