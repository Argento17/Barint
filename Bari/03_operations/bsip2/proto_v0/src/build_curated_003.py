"""
Build curated comparison dataset for real_bread_retail_003_v1 website handoff.

Reads:  BSIP2 per-product JSONs  + raw BSIP0 JSON (for ingredient text)
Writes: real_bread_retail_003_v1_curated_comparison_dataset.json
"""

from __future__ import annotations
import sys, json, re, pathlib, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BSIP2_DIR  = pathlib.Path(r"C:\Bari\02_products\bread_retail_003\bsip2")
RAW_JSON   = pathlib.Path(r"C:\Bari\02_products\bread_retail_003\real_bread_retail_003_v1_20260525T194532_bsip0_raw.json")
OUT_DIR    = pathlib.Path(r"C:\Bari\02_products\bread_retail_003")
TODAY      = "2026-05-26"
RUN_ID     = "real_bread_retail_003_v1"

# ── Signal keyword banks ──────────────────────────────────────────────────────
FERM_REAL_KW = ["מחמצת","שאור","תרבויות","חיידקים","חומצה לקטית","lactobacillus","sourdough"]
FERM_IND_KW  = ["שמרים"]
MATRIX_KW    = ["אינולין","inulin","psyllium","פסיליום","ציקוריה","chicory","cellulose","גואר","קסנטן"]
WG_KW        = ["קמח מלא","שיפון מלא","חיטה מלאה","כוסמין מלא","wholegrain","whole grain","whole wheat",
                 "100% כוסמין","100%שיפון","100% שיפון"]
SEED_KW      = ["שומשום","פשתן","דלעת","גרעיני","זרעי","צ'יה","chia","sunflower","sesame","pumpkin","flax"]
REFINED_KW   = ["קמח חיטה","קמח לבן","white flour","wheat flour"]

# ── Load data ─────────────────────────────────────────────────────────────────
raw_products = json.loads(RAW_JSON.read_text(encoding="utf-8"))
barcode_to_raw: dict[str, dict] = {}
for p in raw_products:
    bc = str(p.get("barcode") or "")
    if bc:
        barcode_to_raw[bc] = p

bsip2_products: list[dict] = []
for f in sorted(BSIP2_DIR.glob("bsip2_*.json")):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        bsip2_products.append(d)
    except Exception:
        pass
print(f"Loaded {len(bsip2_products)} BSIP2 products")

def _ing(p: dict) -> str:
    bc = str(p.get("barcode") or "")
    raw = barcode_to_raw.get(bc, {})
    return (raw.get("ingredients_raw") or "").lower()

def _name(p: dict) -> str:
    return (p.get("name_he") or "").strip()

# ── Signal computation ────────────────────────────────────────────────────────
def fermentation_status_he(p: dict) -> str:
    ing  = _ing(p)
    name = _name(p).lower()
    if not ing:
        return "לא ידוע — חסרים נתוני רכיבים"
    has_real  = any(kw in ing for kw in FERM_REAL_KW)
    has_ind   = any(kw in ing for kw in FERM_IND_KW)
    has_claim = "מחמצת" in name or "sourdough" in name
    if has_real and not has_ind:
        return "מחמצת אמיתית (מזוהה ברכיבים)"
    if has_claim and has_ind and not has_real:
        return "מחמצת בשם, שמרים ברכיבים"
    if has_real and has_ind and not has_claim:
        return "מחמצת אמיתית (עם שמרים עזר)"
    if has_real and has_ind and has_claim:
        return "מחמצת בשם, שמרים ברכיבים"
    if has_ind:
        return "שמרים תעשייתיים בלבד"
    return "לא זוהה תוהל"

def fiber_source_status_he(p: dict) -> str:
    ing   = _ing(p)
    fiber = (p.get("nutrition") or {}).get("dietary_fiber_g")
    if not ing:
        return "לא ידוע — חסרים נתוני רכיבים"
    has_matrix = any(kw in ing for kw in MATRIX_KW)
    has_wg     = any(kw in ing for kw in WG_KW)
    if has_matrix and fiber is not None and fiber >= 5:
        return "חלק מהסיבים מתוספים (אינולין / ציקוריה)"
    if has_wg:
        return "סיבים מדגן שלם"
    return "מקור הסיבים לא ברור"

def seed_halo_status_he(p: dict) -> str:
    ing  = _ing(p)
    name = _name(p).lower()
    if not ing:
        return "לא ידוע"
    seeds = [kw for kw in SEED_KW if kw in ing or kw in name]
    if not seeds:
        return "ללא זרעים בולטים"
    has_wg = any(kw in ing for kw in WG_KW)
    has_refined = any(kw in ing for kw in REFINED_KW)
    if has_wg and not has_refined:
        return "זרעים על מטריצת דגן שלם"
    if has_refined:
        return "זרעים על בסיס מזוקק (אפקט הילה אפשרי)"
    return "זרעים — בסיס לא ברור"

def structural_summary_he(p: dict) -> str:
    score  = p.get("final_score") or 0
    deg    = p.get("degradation_level","")
    cat    = p.get("category","")
    ing    = _ing(p)
    fiber  = (p.get("nutrition") or {}).get("dietary_fiber_g")
    ferm   = fermentation_status_he(p)
    seed   = seed_halo_status_he(p)

    if deg == "INSUFFICIENT":
        return "אין מספיק נתונים לתיאור מבנה מהימן"
    parts = []
    # Grain base
    if any(kw in ing for kw in WG_KW):
        parts.append("בסיס דגן שלם")
    elif any(kw in ing for kw in REFINED_KW):
        parts.append("בסיס קמח מזוקק")
    else:
        parts.append("בסיס דגן — לא ברור")
    # Fermentation
    if "אמיתית" in ferm:
        parts.append("תסיסת מחמצת")
    elif "שמרים תעשייתיים" in ferm:
        parts.append("שמרים תעשייתיים")
    # Fiber
    if fiber is not None:
        if fiber >= 10:
            parts.append(f"עשיר בסיבים ({fiber:.1f}g)")
        elif fiber >= 6:
            parts.append(f"סיבים טובים ({fiber:.1f}g)")
    # Seeds
    if "אפקט הילה" in seed:
        parts.append("זרעים (אפקט הילה אפשרי)")
    return " | ".join(parts) if parts else "מידע חלקי"

def is_displayable(p: dict) -> bool:
    return p.get("degradation_level") in ("FULL","CAUTIOUS") and bool(_ing(p))

def safe_score(p: dict) -> int | None:
    if not is_displayable(p):
        return None
    s = p.get("final_score")
    return round(s) if s is not None else None

CLUSTER_LABELS = {
    "everyday":       "לחם יומיומי — עוגן צרכני",
    "strong":         "מוצרים עם מבנה גרעיני חזק",
    "fermentation":   "ספקטרום התסיסה — מחמצת בפועל",
    "wellness_ambig": "לחמי בריאות — שאלות המבנה",
    "crackers":       "קרקרים — מגוון המבנים",
    "transparency":   "שקיפות הנתונים — מה לא ניתן לנתח",
}

# ── Product enrichment ────────────────────────────────────────────────────────
def enrich(p: dict, cluster: str, why_he: str, blurb_he: str) -> dict:
    score   = safe_score(p)
    disp    = is_displayable(p)
    nutr    = p.get("nutrition") or {}
    img     = (p.get("image_urls") or [""])[0]
    name    = _name(p)

    # sodium: BSIP2 stores in mg (already per 100g from pipeline)
    sodium_mg = nutr.get("sodium_mg")

    return {
        "product_id":             p.get("product_id",""),
        "name_he":                name,
        "brand":                  p.get("brand") or "",
        "category_display_he":    {
            "bread":          "לחם",
            "cracker":        "קרקר",
            "crispbread":     "לחמית",
            "pita":           "פיתה",
            "whole_food_fat": "לחם / מוצר שמן",
            "default":        "מאפה",
        }.get(p.get("category",""), "מוצר אפייה"),
        "website_cluster":        cluster,
        "website_cluster_label_he": CLUSTER_LABELS.get(cluster,""),
        "score":                  score,
        "grade":                  p.get("final_grade") if disp else None,
        "confidence_label_he":    p.get("confidence_label_he",""),
        "display_score_boolean":  disp,
        "safe_for_ranking_boolean":  disp and p.get("degradation_level") in ("FULL","CAUTIOUS"),
        "safe_for_blog_boolean":  disp,
        "fiber_g":                nutr.get("dietary_fiber_g"),
        "protein_g":              nutr.get("protein_g"),
        "sodium_mg":              sodium_mg,
        "fermentation_status_he": fermentation_status_he(p),
        "fiber_source_status_he": fiber_source_status_he(p),
        "seed_halo_status_he":    seed_halo_status_he(p),
        "structural_summary_he":  structural_summary_he(p),
        "why_featured_he":        why_he,
        "suggested_card_blurb_he": blurb_he,
        "image_url":              img,
        "source_url":             p.get("source_url",""),
        "degradation_level":      p.get("degradation_level",""),
        "acquisition_tier":       p.get("acquisition_tier",""),
        "_category_internal":     p.get("category",""),
    }


# ── Product selection ─────────────────────────────────────────────────────────
def find(name_fragment: str, min_score: float = 0, deg: str = None,
         cat: str = None, prefer_cautious: bool = True) -> dict | None:
    """Find best-matching BSIP2 product by name fragment."""
    matches = [p for p in bsip2_products if name_fragment in (p.get("name_he") or "")]
    if not matches:
        return None
    if deg:
        dm = [p for p in matches if p.get("degradation_level") == deg]
        if dm:
            matches = dm
    if cat:
        cm = [p for p in matches if p.get("category") == cat]
        if cm:
            matches = cm
    # prefer those with ingredient text
    with_ing = [p for p in matches if _ing(p)]
    if with_ing:
        matches = with_ing
    if prefer_cautious:
        cautious = [p for p in matches if p.get("degradation_level") == "CAUTIOUS"]
        if cautious:
            matches = cautious
    # sort by score desc
    matches.sort(key=lambda x: x.get("final_score") or 0, reverse=True)
    top = [p for p in matches if (p.get("final_score") or 0) >= min_score]
    return (top or matches)[0] if matches else None


# ── Cluster A: Everyday anchors ───────────────────────────────────────────────
cluster_a_raw = [
    ("לחם אחיד פרוס",     "לחם אחיד פרוס", 60,
     "עוגן צרכני — הלחם היומיומי הנפוץ ביותר. מציג מבנה בסיסי ברור.",
     "לחם בסיסי. פחות מורכב — אבל גם פחות מהונדס. ציון הביניים משקף מבנה פשוט."),
    ("לחם אחיד פרוס קל",  "לחם אחיד פרוס קל", 70,
     "עוגן צרכני עם סיבים גבוהים יחסית. מראה שמוצר אחיד יכול להיות מוצלח.",
     "לחם אחיד עם סיבים גבוהים יחסית לקטגוריה. נקודת ייחוס טובה."),
    ("לחם ברמן לענין",    "לחם ברמן", 60,
     "מותג ברמן — המובייל-מרקט של לחם ישראלי. מבנה ממוצע עם מחמצת אמיתית.",
     "ברמן לענין — מחמצת ומלא. מותג הלחם הגדול בישראל במבנה מאוזן."),
    ("לחם ברמן אקטיב",    "לחם ברמן אקטיב", 68,
     "ברמן עם מחמצת אמיתית וסיבים גבוהים — ממצא מפתיע מהמיינסטרים.",
     "ברמן אקטיב: מחמצת ברשימת הרכיבים וסיבים גבוהים. הממצא החשוב מהמדף היומיומי."),
    ("לחם אנג'ל חיטה מלאה", "לחם אנג'ל חיטה מלאה", 65,
     "אנג'ל — מותג נפוץ בפיצ'ור 'מלא'. בפועל: זרעים, מבנה מעורב.",
     "אנג'ל חיטה מלאה — מיינסטרים עם טענת 'מלא'. מבנה מעורב, ציון בינוני-גבוה."),
    ("לחם אנג'ל חצי מלא",  "לחם אנג'ל חצי מלא", 55,
     "גרסת 'חצי מלא' של אנג'ל — שם שמניח ציפייה מנוהלת.",
     "לחם אחיד עם סיבים נמוכים יחסית. תחת שם 'חצי מלא'."),
    ("פיתה פיתה",          "פיתה פיתה", 0,
     "עוגן פיתה — מוצר פיתה ייחוסי. מבנה פשוט, מידע חלקי.",
     "פיתה — בסיס לבן. מייצגת את קטגוריית הפיתות ומבנה פשוט."),
]

# ── Cluster B: Strong verified ────────────────────────────────────────────────
cluster_b_raw = [
    ("לחם ירוק מקמח מלא",      80, "bread",
     "ציון גבוה עם מבנה דגן שלם. אחד המוצרים המובנים ביותר במדף.",
     "מבנה שלם, ציון גבוה. קמח מלא כבסיס אמיתי."),
    ("לחם מחמצת קמח מלא",     77, "bread",
     "מחמצת אמיתית עם קמח מלא — שילוב נדיר ומבוסס נתונים.",
     "מחמצת ברכיבים, קמח מלא. ציון גבוה ומבוסס."),
    ("לחם שיפון מלא מסטמכר",  76, "bread",
     "שיפון מלא 100% — אחד ממוצרי השיפון הטהורים ביותר בניתוח.",
     "שיפון מלא. סיבים גבוהים במיוחד, מבנה קוהרנטי."),
    ("לחם דגנים מלא",          75, "bread",
     "מבנה דגן שלם מרובה. נקודת ייחוס טובה לקטגוריית 'לחם מלא'.",
     "דגנים מלאים, ציון גבוה. פשוט ומוצלח."),
    ("לחם חיטה מלא לילדים",   75, "bread",
     "לחם לילדים עם מחמצת אמיתית ומבנה דגן שלם — לא מה שמצפים.",
     "ממוקד ילדים, מחמצת ברכיבים. מבנה מרשים יחסית לקטגוריה."),
    ("לחם אחיד פרוס קל",      73, "bread",
     "לחם אחיד עם ביצועים גבוהים יחסית — מראה שמיינסטרים יכול להיות טוב.",
     "לחם אחיד עם סיבים גבוהים. נקודת ייחוס חזקה למוצר יומיומי."),
]

# ── Cluster C: Fermentation spectrum ─────────────────────────────────────────
cluster_c_raw = [
    ("לחם שיפון קל",   "bread",
     "מחמצת אמיתית, שיפון מלא, סיבים גבוהים — ייחוס מקיף לתסיסה אמיתית.",
     "המחמצת כאן היא ברשימת הרכיבים, לא רק בשם. שיפון מלא עם סיבים גבוהים."),
    ("לחם מחמצת גרעינים", "bread",
     "מחמצת אמיתית עם גרעינים — ציון גבוה ותסיסה מאומתת.",
     "מחמצת ברכיבים + גרעינים שלמים. ניתוח מאוזן."),
    ("לחם ברמן אקטיב",  "bread",
     "מחמצת אמיתית במותג מיינסטרים — הממצא המפתיע ביותר בניתוח.",
     "ברמן אקטיב: מחמצת אמיתית. ממצא יוצא דופן מהמדף היומיומי."),
    ("לחם מחמצת וחיטה מלאה קל", "bread",
     "שם מבטיח 'מחמצת', רכיבים מגלים שמרים תעשייתיים — מקרה מייצג של פערי ציפייה.",
     "מחמצת בשם. שמרים ברכיבים. פער בין המיתוג לנתון."),
    ("לחם מחמצת שיפון+אגוזים", "bread",
     "מוצר עם שם 'מחמצת' ונתוני רכיבים שמראים שמרים — דוגמת ספקטרום תסיסה.",
     "מחמצת בשם, שמרים ברכיבים. ציון ממוצע."),
    ("לחם אחיד פרוס",   "bread",
     "ייחוס — ללא מחמצת, ללא טענה, שמרים תעשייתיים. נקודת השוואה ניטרלית.",
     "ללא תסיסה. שמרים תעשייתיים בלבד. בסיס ניקיון להשוואה."),
]

# ── Cluster D: Wellness ambiguity ─────────────────────────────────────────────
cluster_d_raw = [
    ("לחם טחינה פרוס",       "whole_food_fat",
     "ציון הגבוה ביותר — אבל הסיבים הגבוהים מגיעים מהטחינה, לא מהדגן. מקרה לימודי.",
     "ציון 82 — אבל כדאי לדעת: הסיבים כאן מגיעים מהטחינה. מנגנון שונה מלחם דגן שלם."),
    ("לחם לס פרוס קיטו",    "bread",
     "קיטו עם סיבים גבוהים מאוד — מקור הסיבים לא לגמרי ברור. מיצוב פרימיום, נתונים חלקיים.",
     "לחם קיטו עם 17.4g סיבים. מקור הסיבים לא ברור. ציון ממוצע."),
    ("לחם כוסמין לבן",      "bread",
     "כוסמין לבן — המילה 'כוסמין' מציינת סוג דגן, לא מלאות. מבנה ממוצע.",
     "כוסמין לבן — לא כוסמין מלא. שם מציג ציפייה שונה מהמציאות."),
    ("לחם מחמצת מכוסמין",   "bread",
     "מחמצת + כוסמין בשם. נתוני רכיבים: שמרים תעשייתיים. כלי להבנת פערי שיווק.",
     "מחמצת וכוסמין בשם — שמרים ברכיבים. ציון בינוני."),
    ("לחם מחמצת אגוזים צימוקים", "bread",
     "מוצר פרימיום עם שם מחמצת — נתונים חלקיים, לא ניתן לציון מלא.",
     "מחמצת, אגוזים, צימוקים — נשמע מעולה. אין מספיק נתונים לניתוח מלא."),
    ("לחם דגנים לייט",      "bread",
     "לייט עם סיבים גבוהים מאוד מדגן שלם — דוגמת מוצר שמיצובו ותכונותיו מתאימות.",
     "לייט עם 14.2g סיבים מדגן שלם. מתאים בין השם לנתון."),
]

# ── Cluster E: Crackers ────────────────────────────────────────────────────────
cluster_e_raw = [
    ("קרקר כוסמין מלא ושומשום", "cracker",
     "הקרקר עם הציון הגבוה ביותר — כוסמין מלא, שומשום, מבנה קוהרנטי.",
     "ציון 82. כוסמין מלא כבסיס. השומשום על גבי דגן שלם."),
    ("קרקר כוסמין אורגני",     "cracker",
     "קרקר אורגני עם ביצועים חזקים — אורגני ומבנה טוב.",
     "קרקר אורגני עם ציון 78. בסיס כוסמין שלם."),
    ("קרקר פריך בסגנון שוודי", "cracker",
     "קרקר שוודי — מבנה טוב אבל זרעים על בסיס לא ברור.",
     "קרקר שוודי, ציון 72. מבנה סביר, בסיס לא לגמרי ברור."),
    ("קרקר פריך עם קמח שיפון", "cracker",
     "קרקר שיפון — אחד הקרקרים המובנים יותר עם דגן בסיס ברור.",
     "שיפון כבסיס, ציון 71. מבנה פשוט ומוצלח."),
    ("קרם קרקר",               "cracker",
     "קרם קרקר — קרקר קלאסי עם סוכרים מרובים. נקודת ייחוס להנדסת מרקם.",
     "קרם קרקר: שלושה מקורות סוכר. קרקר מהונדס קלאסי."),
    ("קרקר שומשום אסם",       "cracker",
     "קרקר מסחרי עם שומשום — שומשום על בסיס לא שלם, רמת עיבוד גבוהה.",
     "שומשום על בסיס מזוקק. שלושה מקורות סוכר. ציון 52."),
]

# ── Cluster F: Transparency ───────────────────────────────────────────────────
cluster_f_raw = [
    ("מארז פיתות אסליות",      "נציג פיתה קלאסית — ללא נתוני תזונה ורכיבים מספיקים לניתוח.",
     "פיתות אסליות — נפוצות מאוד, אבל אין לנו מספיק נתונים לציון."),
    ("לחם מחמצת אגוזים פרוס", "לחם פרימיום — שם מרשים, אבל נתוני רכיבים חסרים.",
     "מחמצת ואגוזים — נשמע מצוין. אך הנתונים לא מספיקים לציון."),
    ("לחם אחיד",               "לחם אחיד בסיסי — הכי נפוץ, הכי קשה לנתח ללא נתוני רכיבים.",
     "לחם אחיד ללא תזונה מלאה. אנחנו לא מציגים ציון בלי מידע מספיק."),
    ("חלה קלועה",              "חלה — קטגוריה שלמה שנעדרה נתוני רכיבים בניתוח זה.",
     "חלה קלועה — ייצגת, אבל חסרים הנתונים. לא נציג ציון."),
]


# ── Build curated list ────────────────────────────────────────────────────────
curated: list[dict] = []
used_ids: set[str] = set()

def add(p: dict | None, cluster: str, why: str, blurb: str) -> None:
    if p is None:
        print(f"  [skip] not found for cluster={cluster}")
        return
    pid = p.get("product_id","")
    if pid in used_ids:
        print(f"  [dup] {p.get('name_he','')} already added")
        return
    used_ids.add(pid)
    curated.append(enrich(p, cluster, why, blurb))
    score = p.get("final_score")
    deg   = p.get("degradation_level","")
    print(f"  + [{cluster}] {p.get('name_he',''):40s} score={score} deg={deg}")

print("\n=== Cluster A: Everyday anchors ===")
for fragment, search_frag, min_s, why, blurb in cluster_a_raw:
    p = find(fragment if fragment == search_frag else search_frag, min_score=min_s)
    if p is None:
        p = find(fragment, min_score=min_s)
    add(p, "everyday", why, blurb)

print("\n=== Cluster B: Strong verified ===")
for fragment, min_s, cat, why, blurb in cluster_b_raw:
    p = find(fragment, min_score=min_s, cat=cat)
    if p and p.get("product_id","") in used_ids:
        # try lower-scored duplicate
        matches = [x for x in bsip2_products
                   if fragment in (x.get("name_he") or "")
                   and x.get("product_id","") not in used_ids
                   and _ing(x)]
        p = matches[0] if matches else None
    add(p, "strong", why, blurb)

print("\n=== Cluster C: Fermentation spectrum ===")
for fragment, cat, why, blurb in cluster_c_raw:
    p = find(fragment, cat=cat)
    if p and p.get("product_id","") in used_ids:
        matches = [x for x in bsip2_products
                   if fragment in (x.get("name_he") or "")
                   and x.get("product_id","") not in used_ids]
        p = matches[0] if matches else None
    add(p, "fermentation", why, blurb)

print("\n=== Cluster D: Wellness ambiguity ===")
for fragment, cat, why, blurb in cluster_d_raw:
    p = find(fragment, cat=cat)
    if p and p.get("product_id","") in used_ids:
        matches = [x for x in bsip2_products
                   if fragment in (x.get("name_he") or "")
                   and x.get("product_id","") not in used_ids]
        p = matches[0] if matches else None
    add(p, "wellness_ambig", why, blurb)

print("\n=== Cluster E: Crackers ===")
for fragment, cat, why, blurb in cluster_e_raw:
    p = find(fragment, cat=cat)
    if p and p.get("product_id","") in used_ids:
        matches = [x for x in bsip2_products
                   if fragment in (x.get("name_he") or "")
                   and x.get("product_id","") not in used_ids]
        p = matches[0] if matches else None
    add(p, "crackers", why, blurb)

print("\n=== Cluster F: Transparency ===")
for fragment, why, blurb in cluster_f_raw:
    p = find(fragment, prefer_cautious=False)
    if p and p.get("product_id","") in used_ids:
        matches = [x for x in bsip2_products
                   if fragment in (x.get("name_he") or "")
                   and x.get("product_id","") not in used_ids]
        p = matches[0] if matches else None
    add(p, "transparency", why, blurb)

# ── Output ─────────────────────────────────────────────────────────────────────
print(f"\n=== Total curated: {len(curated)} products ===")
by_cluster: dict[str, int] = {}
for e in curated:
    c = e["website_cluster"]
    by_cluster[c] = by_cluster.get(c, 0) + 1
for c, n in by_cluster.items():
    print(f"  {c}: {n}")

output = {
    "meta": {
        "run_id":          RUN_ID,
        "generated":       TODAY,
        "total_curated":   len(curated),
        "source":          "Shufersal representative shelf — acquisition v3",
        "scope_note":      "ניתוח מדף שופרסל בלבד — לא סקר שוק ישראלי",
        "cluster_labels":  CLUSTER_LABELS,
        "cluster_counts":  by_cluster,
        "signal_notes": {
            "fermentation": "מחמצת אמיתית = מחמצת/שאור ברשימת הרכיבים. שמרים תעשייתיים = שמרים כמרכיב עיקרי.",
            "fiber_source": "סיבים מדגן שלם = קמח מלא/שיפון מלא/כוסמין מלא כרכיב ראשי. תוספים = אינולין/ציקוריה/פסיליום.",
            "seed_halo":    "אפקט הילה = זרעים על בסיס קמח מזוקק. ללא אפקט הילה = זרעים על דגן שלם.",
        },
    },
    "clusters": [
        {"cluster_id": k, "label_he": v, "products": [e for e in curated if e["website_cluster"] == k]}
        for k, v in CLUSTER_LABELS.items()
    ],
    "all_products": curated,
}

out_path = OUT_DIR / f"{RUN_ID}_curated_comparison_dataset.json"
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}")
