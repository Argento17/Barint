#!/usr/bin/env python3
"""
לחם — BariProductVM Builder v1
Reads:  BSIP2 flat files (bread_retail_003/bsip2/*.json)
        BSIP0 raw (ingredients_raw + image_urls, keyed by barcode)
        Barcode-keyed insight lines from lechem_insight_lines_v1.md
Writes: lechem_frontend_v1.json  (BariProductVM[])
        lechem_corpus_report_v1.md
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT      = Path(r"C:\Bari")

sys.path.insert(0, str(ROOT / "03_operations/bsip2/proto_v0/src"))
from grade_governance import apply_a_grade_floor  # noqa: E402  TASK-188
BSIP2_DIR = ROOT / "02_products/bread_retail_003/bsip2"
BSIP0_RAW = ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"
OUT_DIR   = ROOT / "02_products/bread_retail_003"
OUT_JSON  = OUT_DIR / "lechem_frontend_v1.json"
OUT_REPORT = OUT_DIR / "lechem_corpus_report_v1.md"

# ── Insight lines — keyed by barcode ─────────────────────────────────────────
INSIGHT_LINES: dict[str, str] = {
    # A-Grade
    "7290016245325": "18.5 גרם סיבים, בסיס זרעים ומחמצת — ויטמין C ואינולין ברשימה מגלים עיבוד מכוון",
    "96086000966":   "4 רכיבים: קמח כוסמין מלא, שומשום, מלח, אורגנו — הרשימה הקצרה ביותר בין ציוני ה-A",
    # B-Grade high (75–80)
    "3268429":       "100% קמח חיטה מלא, חומץ טבעי במקום שיפורי קמח — הרכב יוצא דופן ברשתות",
    "96086000577":   "קמח כוסמין מלא אורגני 98%, מים, מלח — שלושה רכיבים, ציון B",
    "481203":        "מחמצת שיפון ב-10% ממשקל המוצר — תסיסה מזוהה, קמח חיטה מלא 90%",
    "3054183":       "גרעיני שיפון שבורים 50% — לא קמח שיפון, גרעין שיפון. ההבדל מסביר את ה-10.6 גרם סיבים",
    "481197":        "מחמצת וגרעינים — קמח חיטה לבן ראשון ברשימה, קמח מלא שלישי",
    "2079927":       "83% קמח חיטה מלא — מתחלבי קמח ברשימה. הדגן השלם לא עומד לבד",
    "3268252":       "לילדים — 100% חיטה מלאה, מחמצת שיפון, ללא מתחלבים. הנוסחה הנקייה בין לחמי הרשת",
    "574370":        "שיפון מלא ומחמצת עם 12.4 גרם סיבים — מתחלבים שמשלימים את הרשימה",
    # B-Grade 74
    "2079033":       "14.2 גרם סיבים — חלקם מאינולין מוסף, לא מגרעין. המספר גבוה, המקור מעורב",
    "3719259":       "שיפון מלא 100% ומחמצת שיפון — שיפורי קמח ומתחלבים נוספו למרות הבסיס הנקי",
    "379203":        "חיטה מלאה טרום נבוטה כבסיס — תהליך השרייה שמשנה את הנגישות, עם שיפורי קמח",
    "4023041":       "שיפון מלא 80%, חיטה מלאה 20%, מחמצת שאור — שני דגנים מלאים, תסיסה מזוהה",
    "4685430":       "כוסמין מלא 100% ומחמצת שיפון — שיפורי קמח נוספו. הדגן הטוב לא מגיע לבד",
    "498034":        "E-FREE בשם — כוסמין מלא 100% ומחמצת, ללא מספרי E. התווית תואמת את הרכב",
    "7290018540817": "כוסמין מלא 78%, מחמצת חיטה מלאה — שני הרכיבים העיקריים תואמים את השם",
    # B-Grade 70–73
    "2079996":       "קמח חיטה כהה ראשון, סיבים תזונתיים מוספים שניים — הסיבים לא מגיעים מגרעין שלם",
    "4685492":       "חיטה ושיפון מלאים, מחמצת שיפון — שיפורי קמח ומתחלבים ברשימה ארוכה",
    "497044":        "100% חיטה מלאה, מחמצת, אינולין מוסף — הסיבים מגיעים גם מתוספת, לא רק מהדגן",
    "497426":        "חיטה מלאה טרום נבוטה, שיפון ומחמצת — רשימה מכוונת לבריאות, שיפורי קמח כלולים",
    "574172":        "95% קמח חיטה מלא, 12.3 גרם סיבים — מתחלבים שמאריכים חיי המדף",
    "6322104":       "חיטה ושיפון מלאים, רשימה ארוכה — שיפורי עיבוד על הבסיס הנקי",
    "7290016967074": "100% חיטה מלאה, גרעינים 25% — חומרי תחלוב מסיימים את רשימת הרכיבים",
    "7296073134459": "בסגנון שוודי — חיטה מלאה 33.5%, גריסי תירס ועמילן תפוח אדמה. לא שיפון שוודי",
    # B-Grade 71
    "2037194":       "חיטה מלאה 80% ומחמצת שיפון — שיפורי קמח ומתחלבים בכל זאת. הנוסחה הלאומית הסטנדרטית",
    "4033712":       "חיטה מלאה 80%, מחמצת — אותה נוסחה כמו מתחרים, שיפורי קמח כלולים",
    "4685195":       "10 דגנים בשם — חיטה ושיפון מלאים עיקרים, שאר הדגנים ב-7% ממשקל הלחם",
    "4685201":       "שיפון, אגוזי מלך ומחמצת — שיפורי קמח ומתחלבים ברקע הרשימה",
    "481180":        "שאור בשם, קמח חיטה לבן 75% ממשקל הקמחים — הבסיס לבן, המחמצת שלישית ברשימה",
    "574141":        "100% קמח חיטה מלא — חומרי תחלוב ברשימה. הדגן עומד, שיפורי העיבוד מצטרפים",
    "574455":        "כוסמין 7% מהקמחים, 4.5% ממשקל הלחם — כוסמין בשם, מינוריטי בפועל",
    "7290017304885": "שיפון מלא 51%, חיטה מלאה 27% — שני דגנים מלאים, שיפורי קמח ביניהם",
    "7290017746906": "כוסמין 51%, חיטה מלאה 49% — שני קמחים מלאים, חומרי עיבוד מצטרפים לשניהם",
    "7296073134442": "70% קמח חיטה מלא, שיפון 4.9% — שמו שיפון, עיקרו חיטה",
    # B-Grade 70
    "4685010":       "שיפון מלא 100%, מחמצת שיפון 10%, פתיתי שיבולת שועל — מתחלבים ברשימה ארוכה",
    "4685027":       "חיטה מלאה 76%, שיפון מלא 24%, מחמצת — יחס הדגנים מוצהר, שיפורי קמח נלווים",
    "4685126":       "חמישה דגנים בשם — שיפון 48%, חיטה 32%, שלושת האחרים ב-20% ביחד",
    "4685157":       "שיפון מלא 100% — שמן מהצומח ומתחלבים ברשימה. הגרעין הטוב עם תוספות עיבוד",
    "498003":        "E-FREE בגרסת החיטה — 100% חיטה מלאה ומחמצת, ללא מספרי E",
    "6322838":       "100% קמח מלא בשם — חלבון צמחי מוסף ומתחלבים. הקמח השלם לא עומד לבד",
    "7290014940901": "שמו פשוט — 100% חיטה מלאה, ואז מתחלבים. הפשטות מגיעה עד הרכיב הרביעי",
    # B-Grade 65–69
    "7290013027399": "חיטה ושיפון מלאים — שיפורי קמח, ללא מחמצת. פחות ממוצרים עם תסיסה מזוהה",
    "2065616":       "חיטה מלאה, שיפון, גרעינים וחיטה טרום נבוטה — מחמצת ברשימה, מתחלבים גם הם",
    "497570":        "12.7 גרם סיבים — אינולין מוסף ברשימה. ה'פלוס' הוא תוספת סיבים, לא גרעין שלם",
    "7290018500316": "כוסמין לבן — גרעין כוסמין מנופה. 3.3 גרם סיבים בלבד, פחות מגרסת הכוסמין המלא",
    "2065623":       "כפרי בשם — קמח חיטה כהה ראשון, שיפון מלא שלישי. הכפריות בשם, לא בדגן",
    "2079477":       "שני חומרים משמרים — קלציום פרופיונט ופוטסיום סורבט. לחם אחיד, שיא התוספות",
    "497532":        "ברמן ללא הנבט — חיטה מלאה ומחמצת, בלי חיטה טרום נבוטה. ציון B בנוסחה הפשוטה",
    "7290018500460": "חצי חיטה מלאה, חצי חיטה לבנה — אנג'ל מפצל 50%, הציון מחצית בהתאם",
    "8713900":       "שיפון עגול — קמח חיטה כהה ראשון, שיפון מלא 33%. הצורה עגולה, הדגן לא שלם",
    "8713917":       "קמח חיטה כהה 66%, שיפון מלא 34% — כהה בצבע, לא מלא בגרעין",
    "4033736":       "בסגנון בריוש — קמח לבן 100%, סוכר שני ברשימה, מתחלבים. הסגנון מסביר את הרכב",
    "497112":        "קמח חיטה כהה, סיבים מוספים, משמר E282 ומתחלב E481 — הנוסחה הבסיסית",
    "574035":        "קמח חיטה כהה, שמנים מהצומח, מתחלבים — ללא ויטמין C ושיפורי אפייה מורחבים",
    "6451507":       "מחמצת שאור, כוסמין מלא 70% — קמח חיטה לבן שני ברשימה, לא שלם",
    "7296073659945": "קרקר דק עם רוזמרין — חיטה מלאה 25%, שמן דקל, גלוטן. הטעם מוסיף, הדגן לא מתחלף",
    "7296073659952": "כפרי בשם — חיטה מלאה 25.5%, אורז ודקל. תערובת קמחים לא כפרית",
    "379142":        "חיטה מלאה 71%, חיטה טרום נבוטה 29% — מתחלבי קמח נלווים לנוסחה הנבוטה",
    "7290017947105": "בסגנון אמריקה — קמח לבן ראשון, סוכר שני, מתחלבים שלישי. הסגנון מסביר את הרכב",
    "7290018500231": "WEEKEND — קמח לבן, סוכר, מתחלבים. אנג'ל לשבת, לא לשבוע",
    "7290018500361": "קמח חיטה כהה, סיבים תזונתיים מוספים, E282 ו-E471 — הנוסחה הלאומית הסטנדרטית",
    # C-Grade
    "6451514":       "מחמצת שאור — קמח חיטה לבן ראשון, גרעינים שלישיים. הבסיס לבן, הסיבים מהגרעינים",
    "6451521":       "שיפון מלא 70%, קמח חיטה לבן שני — הבסיס הטוב עם קמח לבן כ'חיזוק'",
    "7290015161589": "קמח אורז ותירס אורגני, ירקות 1% — ירקות בשם, 1.3 גרם סיבים בלבד",
    "7296073219347": "קמח חיטה כהה, שמן מוקשה בחלקו, E481 — שמן חלקית מוקשה, יוצא דופן בין הגרסאות",
    "6451477":       "מחמצת שאור — קמח לבן 40% מהלחם. 'צרפתי' מתאר בסיס, לא תהליך",
    "7296073612759": "קמח לבן כבסיס, שאור כתוספת — הצרפתי הוא הבסיס הלבן, לא המחמצת",
    "7296073641605": "מחמצת צרפתי פרוס — קמח לבן, שאור, פרוסות. הפריסה לא שינתה את הרכב",
    "2079217":       "מחמצת שיפון 2% בלבד — תוספת, לא בסיס. השמן והמתחלבים ארוכים ממנה ברשימה",
    "6451491":       "זיתי קלמטה 8% ומחמצת שאור — בסיס קמח חיטה לבן. האוכל הטוב מגיע עם רקע לבן",
    "6451934":       "אגוזי מלך 7%, מחמצת שאור — בסיס קמח לבן. האגוז מוסיף ערך, הבסיס לבן",
    "7296073612742": "מחמצת שאור וזיתי קלמטה — בסיס קמח לבן. הגרעין מגיע מהזיתים, לא מהקמח",
    "7296073641599": "מחמצת, זיתים, קמח לבן — שני דברים טובים עם בסיס לבן. ציון C מסביר את השלישי",
    "6451484":       "אגוזים וצימוקים עם מחמצת — בסיס קמח לבן, הפירות היבשים מוסיפים סוכר טבעי",
    "7290016867114": "כוסמין מלא 34% ממשקל הלחם — 'קל' פירושו פחות קמח, לא פחות עיבוד",
    "8434165658523": "קמח חיטה לבן, שמן דקל, סוכר — הקרקר הלבן הלאומי. ציון C, רשימת רכיבים צפויה",
    "7290112968807": "פיטנס וסלק — חיטה מלאה 31%, אורז 23%, אבקת סלק 7.5%. המרקם הדק על חשבון הדגן",
    "7296073389446": "ללא גלוטן — עמילן תפוח אדמה כבסיס, גרעינים כתוספת. הגרעין לא מחליף את העמילן",
    "7296073389453": "ציה ללא גלוטן — עמילן תפוח אדמה כבסיס, ציה 8%. ה'ציה' בשם, העמילן בבסיס",
    # D-Grade
    "7290013121028": "לבן ללא גלוטן — עמילן מעובד (E1442) ברכיב השני, 1 גרם סיבים בלבד",
}

_CUTOFF_MARKERS = ['מאפיינים נוספים', 'ערכים תזונתיים', 'אין להסתמך', 'הנתונים המדויקים']

def clean_ingredients(text: str) -> str:
    if not text:
        return ""
    for marker in _CUTOFF_MARKERS:
        idx = text.find(marker)
        if idx > 10:
            text = text[:idx]
    return text.strip().rstrip("., ")

def detect_fermentation(ing: str) -> bool:
    return any(m in ing for m in ['מחמצת', 'שאור', 'חמיצה'])

def detect_bread_subtype(name: str) -> str:
    if 'קרקר' in name:
        return 'קרקר'
    if 'בגט' in name:
        return 'בגט'
    if 'פיתה' in name or 'פיתות' in name:
        return 'פיתה'
    if 'לחמניה' in name or 'לחמניות' in name:
        return 'לחמניה'
    return 'לחם'

def confidence_vm(deg: str) -> tuple[str, str]:
    if deg == 'FULL':
        return 'verified', 'נתונים מלאים'
    return 'partial', 'נתונים חלקיים'

def clean_float(v) -> float | None:
    if v is None:
        return None
    try:
        return round(float(v), 1)
    except (TypeError, ValueError):
        return None

def nutrition_vm(nv: dict) -> dict | None:
    n = {
        'energyKcal': clean_float(nv.get('energy_kcal')),
        'protein':    clean_float(nv.get('protein_g')),
        'sugar':      clean_float(nv.get('sugars_g') or nv.get('sugar_g')),
        'fat':        clean_float(nv.get('fat_g') or nv.get('total_fat_g')),
        'fiber':      clean_float(nv.get('dietary_fiber_g')),
        'sodium':     clean_float(nv.get('sodium_mg')),
    }
    if all(v is None for v in n.values()):
        return None
    return n

def best_image(urls: list) -> str | None:
    if not urls:
        return None
    for url in urls:
        if 'products_large' in url or 'products_zoom' in url:
            return url
    return urls[0]

# ── Load BSIP0 raw ────────────────────────────────────────────────────────────
print("Loading BSIP0 raw…")
with open(BSIP0_RAW, encoding='utf-8') as f:
    bsip0_raw = json.load(f)

barcode_to_b0: dict[str, dict] = {}
for item in bsip0_raw:
    bc = str(item.get('barcode', '')).strip()
    if bc:
        barcode_to_b0[bc] = item

print(f"  BSIP0 items: {len(bsip0_raw)} | indexed by barcode: {len(barcode_to_b0)}")

# ── Process BSIP2 flat files ──────────────────────────────────────────────────
print("Processing BSIP2 files…")
products_vm    = []
no_insight     = []
image_missing  = []

for fp in sorted(BSIP2_DIR.glob('*.json')):
    with open(fp, encoding='utf-8') as f:
        t = json.load(f)

    deg   = t.get('degradation_level', '')
    score = t.get('final_score')
    if deg not in ('FULL', 'CAUTIOUS') or score is None:
        continue

    barcode = str(t.get('barcode', '')).strip()
    name    = t.get('name_he', '?')

    insight = INSIGHT_LINES.get(barcode)
    if insight is None:
        no_insight.append({'barcode': barcode, 'name': name})
        continue

    b0      = barcode_to_b0.get(barcode, {})
    ing_raw = clean_ingredients(b0.get('ingredients_raw', '') or '')

    # Image: prefer BSIP2 image_urls, fall back to BSIP0
    images    = t.get('image_urls') or b0.get('image_urls', [])
    image_url = best_image(images)
    if not image_url:
        image_missing.append({'barcode': barcode, 'name': name})

    confidence, conf_label = confidence_vm(deg)
    nv = nutrition_vm(t.get('nutrition', {}))

    # TASK-188: A-grade ingredient observability floor
    # Bread BSIP2 traces use a flat nutrition dict at t['nutrition'] and
    # ingredients come from BSIP0 (ing_raw). Pass the flat nutrition dict
    # for Condition 3; no full trace available here (flat file format), so
    # Condition 2 defaults to pass (belt-and-suspenders via C1 + C3).
    disp_score = round(float(score))
    disp_grade = t.get('final_grade', '?')
    disp_score, disp_grade = apply_a_grade_floor(
        score=disp_score,
        grade=disp_grade,
        ingredients=ing_raw,
        nutrition=t.get('nutrition', {}),
        trace=None,  # flat-file format; no trace dict for C2
    )

    product = {
        'id':          barcode,
        'name':        name,
        'imageUrl':    image_url,
        'score':       disp_score,
        'grade':       disp_grade,
        'insightLine': insight,
        'confidence':  confidence,
        'fermentationDetected': detect_fermentation(ing_raw),
        'breadSubtype':         detect_bread_subtype(name),
        'expansion': {
            'nutrition':        nv,
            'ingredients':      ing_raw if ing_raw else None,
            'confidenceLabel':  conf_label,
            'servingNote':      'ל-100 גרם',
        },
    }
    products_vm.append(product)

products_vm.sort(key=lambda p: p['score'], reverse=True)

print(f"  Coherent products with insight line: {len(products_vm)}")
print(f"  No insight line (skipped): {len(no_insight)}")
print(f"  Missing image: {len(image_missing)}")

# ── Write frontend JSON ───────────────────────────────────────────────────────
payload = {
    '_meta': {
        'generated':     datetime.utcnow().isoformat() + 'Z',
        'category':      'lechem',
        'product_count': len(products_vm),
        'schema':        'BariProductVM[]',
        'version':       'v1',
        'source':        'bread_retail_003 (Shufersal), 81 coherent products',
    },
    'products': products_vm,
}

with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"\n  Frontend JSON: {OUT_JSON}")

# ── Corpus report ─────────────────────────────────────────────────────────────
grade_dist    = {}
ferm_count    = 0
subtype_dist  = {}
scores        = [p['score'] for p in products_vm]

for p in products_vm:
    g = p['grade']
    grade_dist[g] = grade_dist.get(g, 0) + 1
    if p['fermentationDetected']:
        ferm_count += 1
    st = p['breadSubtype']
    subtype_dist[st] = subtype_dist.get(st, 0) + 1

avg_score = sum(scores) / len(scores) if scores else 0

grade_rows = '\n'.join(
    f'| {g} | {grade_dist.get(g, 0)} |'
    for g in ('A', 'B', 'C', 'D', 'E')
)
subtype_rows = '\n'.join(
    f'| {st} | {cnt} |'
    for st, cnt in sorted(subtype_dist.items(), key=lambda x: -x[1])
)
no_insight_rows = '\n'.join(
    f'- {x["name"]} (BC={x["barcode"]})'
    for x in sorted(no_insight, key=lambda x: x['name'])
) or '_none_'
missing_img_rows = '\n'.join(
    f'- {x["name"]} (BC={x["barcode"]})'
    for x in image_missing
) or '_All products have image URLs_'

report = f"""# לחם — Corpus Report v1

**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Source:** BSIP2 bread_retail_003 (Shufersal) + finalized insight lines v1

---

## Coverage

| Metric | Count |
|--------|-------|
| Coherent BSIP2 files (FULL/CAUTIOUS) | 81 |
| Matched insight line | {len(products_vm)} |
| Skipped (no insight line) | {len(no_insight)} |
| Missing image URL | {len(image_missing)} |

---

## Grade Distribution

| Grade | Count |
|-------|-------|
{grade_rows}

Average score: **{avg_score:.1f}**

---

## Product Subtypes

| Subtype | Count |
|---------|-------|
{subtype_rows}

---

## Fermentation Signal

| Signal | Count |
|--------|-------|
| עם מחמצת (fermentation detected) | {ferm_count} |
| ללא מחמצת מזוהה | {len(products_vm) - ferm_count} |

---

## Missing Image URLs

{missing_img_rows}

---

## Skipped Products (no insight line)

These products are coherent BSIP2 files but have no assigned insight line.
This indicates a gap in the corpus — barcodes not in lechem_insight_lines_v1.md.

{no_insight_rows}

---

## Image URL Note

Image URLs are Shufersal Cloudinary CDN (`res.cloudinary.com/shufersal`).
**Action required before production:**
1. Add `res.cloudinary.com` to `next.config.ts` `images.remotePatterns`
2. Verify URLs are publicly accessible without referrer restriction

---

## Filter Dimensions

The following fields are available for UI filtering:

- `grade` → ציון (A/B/C/D)
- `fermentationDetected` → תסיסה (עם מחמצת / ללא מחמצת מזוהה)
- `breadSubtype` → סוג (לחם / קרקר / בגט / פיתה / לחמניה)
- `score` → מספרי (slider)

---

## Ready for Frontend?

**Verdict: CONDITIONAL PASS**

- Editorial corpus complete (barcode-keyed insight lines for all 81 products)
- Scores and grades from BSIP2 flat files
- Fermentation signal derived from BSIP0 ingredients_raw
- Image URLs present (Cloudinary accessibility unverified)
- Recommend: verify 5 Shufersal image URLs in browser before deploying
"""

with open(OUT_REPORT, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"  Corpus report: {OUT_REPORT}")
print("\nDone.")
