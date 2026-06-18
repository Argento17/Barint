#!/usr/bin/env python3
"""
TASK-254 Phase 1a — Claims inventory builder
Generates yogurts_claims_input_v1.json and cereals_claims_input_v1.json
"""
import json, os, glob
from datetime import datetime, timezone

BASE = r"C:\Bari"

def read_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def trace_summary(trace):
    if trace is None:
        return None
    caps = [c["rule"] for c in trace.get("caps_applied", [])]
    penalties = [p["rule"] for p in trace.get("penalties_applied", [])]
    return {
        "final_score": trace.get("final_score_estimate"),
        "grade": trace.get("grade_estimate"),
        "nova_level": trace.get("nova_proxy"),
        "caps_applied": caps,
        "penalties_applied": penalties,
        "fermentation_bonus_applied": None,
        "explanation_drivers": trace.get("explanation_drivers", []),
        "unresolved_flags": trace.get("unresolved_flags", []),
    }

def product_strings_yogurt(p):
    s = {}
    if p.get("insightLine"):
        s["insightLine"] = p["insightLine"]
    if p.get("rowVerdict"):
        s["rowVerdict"] = p["rowVerdict"]
    exp = p.get("expansion", {})
    if exp.get("confidenceLabel"):
        s["confidenceLabel"] = exp["confidenceLabel"]
    if exp.get("unknowns"):
        s["unknowns"] = exp["unknowns"]
    pos = exp.get("positiveSignals", [])
    if pos:
        s["positiveSignals"] = pos
    lim = exp.get("limitingFactors", [])
    if lim:
        s["limitingFactors"] = lim
    cl_he = p.get("confidence_label_he")
    if cl_he:
        s["confidence_label_he"] = cl_he
    ct_he = p.get("confidence_tooltip_he")
    if ct_he:
        s["confidence_tooltip_he"] = ct_he
    return s

def product_strings_cereal(p):
    s = {}
    if p.get("insightLine"):
        s["insightLine"] = p["insightLine"]
    if p.get("rowVerdict"):
        s["rowVerdict"] = p["rowVerdict"]
    exp = p.get("expansion", {})
    if exp.get("confidenceLabel"):
        s["confidenceLabel"] = exp["confidenceLabel"]
    cl_he = p.get("confidence_label_he")
    if cl_he:
        s["confidence_label_he"] = cl_he
    ct_he = p.get("confidence_tooltip_he")
    if ct_he:
        s["confidence_tooltip_he"] = ct_he
    return s

##############################################################################
# YOGURTS
##############################################################################
yogurt_fe_path = os.path.join(BASE, r"bari-web\src\data\comparisons\yogurts_frontend_v3.json")
yogurt_fe = read_json(yogurt_fe_path)
yogurt_trace_run_shufersal = os.path.join(BASE, r"02_products\yogurt_system\bsip2_outputs\run_yogurt_006")
yogurt_trace_run_yohananof = os.path.join(BASE, r"02_products\yogurt_system\bsip2_outputs\run_yogurt_yohananof_001")

YOGURT_PAGE_STRINGS = {
    "hero_eyebrow": "יוגורטים · מדף ישראלי",
    "hero_title": 'יוגורט: לא כל "טבעי" נוצר שווה',
    "prologue_1": "בדקנו מחדש את מדף היוגורט על נתוני אריזה אמיתיים — רכיבים, חלבון, סוכר ושומן. התמונה התהפכה מהבדיקה הקודמת: שבעה יוגורטים על המדף מגיעים ל-A. הציון הגבוה הוא 96/A — דנונה PRO יוגורט 20 גרם חלבון, על בסיס חלבון גבוה במיוחד ותרביות חיות.",
    "prologue_2": "היוגורטים הפשוטים של תנובה — ביו 3% וביו 1.5% — וגם נטול הלקטוז מגיעים ל-80 עד 81, כולם A: בסיס חלבי, חיידקי ביפידוס, מעט מרכיבים. יוגורט עיזים נשאר ב-77/B, בעיקר כי החלבון בו נמוך יותר.",
    "prologue_3": "מכאן זה יורד. ככל שמתווספים סוכר, חומרי טעם, מייצבים או פצפוצים — הציון נופל. גרסאות הטעם וה'קראנצ'' מגיעות עד C ו-D, גם כשכמות החלבון על האריזה זהה. ושומן גבוה לא מעלה ציון: יווני 8% עם 4.8 גרם שומן רווי עוצר ב-79/B, מתחת לבסיסים הרזים.",
    "prologue_4": "במדף הזה 'הכי טוב' הוא A — אבל לא S. גם היוגורט המוביל נעצר ב-A: ציון החלבון והתרביות מרים אותו גבוה, אך לא הופך אותו ליוצא דופן. הכי טוב, לא מושלם.",
    "category_note": "הערת קטגוריה — אותה תווית, שני קצוות\n\nהציון משקלל את ההרכב כולו — חלבון, סוכר, מייצבים ורמת עיבוד — ולא תווית אחת. אותו 'עשיר בחלבון' יכול לשבת בראש המדף כשהבסיס פשוט, וליפול ל-C או D בגרסת טעמים שמוסיפה סוכר, חומרי טעם ופצפוצים על אותו חלבון בדיוק. מספר החלבון על החזית אינו מספיק כדי לקבוע את הציון.\n\nהערת קטגוריה — 'הכי טוב' כאן הוא A, לא S\n\nשבעה יוגורטים על המדף מגיעים ל-A, והגבוה הוא 96/A. אבל אף אחד לא מגיע ל-S, גם המוביל: חלבון גבוה ותרביות חיות מרימים את הציון, ואינם הופכים יוגורט ליוצא דופן. A כאן אומר יוגורט טוב באמת — לא מושלם, ולא מעבר לכך.\n\nהערת קטגוריה — סיבים תזונתיים\n\nמוצרי חלב כמעט אינם מציינים סיבים תזונתיים על התווית, ולכן ערך זה אינו נכנס לניתוח בקטגוריה זו.",
    "methodology_1": "נבדקו 19 יוגורטים מהמדף הישראלי — מחלב פשוט ועד גרסאות חלבון עם תוספים.",
    "methodology_2": "לכל מוצר נבחנו הרכב הרכיבים, רמת חלבון, תוספי מייצבים, סוכר מוסף ורמת עיבוד.",
    "methodology_3": "ציון יוגורט טבעי מבוסס גבוה יותר ממוצר בטעמים — לא בגלל שמות, אלא בגלל מה שכתוב ברשימת הרכיבים.",
    "methodology_4": "מעדני חלב — מוצרים עם שכבות שוקולד, קצפת, או מבנה קינוח — אינם נכללים בהשוואה; הם מוצרי הנאה נפרדים. יוגורט שתיה נכלל ומקבל ציון כמוצר יוגורט מעובד.",
    "metadataLine": f"{yogurt_fe['_meta']['product_count']} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari",
}

yogurt_products_out = []
yogurt_anomalies = []

for p in yogurt_fe["products"]:
    barcode = str(p.get("barcode", ""))
    pid = p.get("id", "")
    retailer = p.get("retailer", "shufersal")

    if retailer == "yohananof":
        trace_run_dir = yogurt_trace_run_yohananof
    else:
        trace_run_dir = yogurt_trace_run_shufersal

    trace_pid = f"bsip1_yogurt_{barcode}" if barcode else pid
    trace_path = os.path.join(trace_run_dir, "products", trace_pid, "bsip2_trace.json")

    trace = read_json(trace_path)
    if trace is None:
        yogurt_anomalies.append(f"NO_TRACE: product {pid} (barcode={barcode}, retailer={retailer}) not found at {trace_path}")

    strings = product_strings_yogurt(p)
    if not strings:
        yogurt_anomalies.append(f"EMPTY_STRINGS: product {pid} (barcode={barcode}) has no extractable strings")

    yogurt_products_out.append({
        "product_id": pid,
        "barcode": barcode,
        "name_he": p.get("name", ""),
        "strings": strings,
        "trace_path": trace_path,
        "trace_found": trace is not None,
        "trace_summary": trace_summary(trace),
    })

# Check duplicate barcodes
barcode_counts = {}
for p in yogurt_products_out:
    bc = p["barcode"]
    barcode_counts[bc] = barcode_counts.get(bc, 0) + 1
for bc, cnt in barcode_counts.items():
    if cnt > 1:
        yogurt_anomalies.append(f"DUPLICATE_BARCODE: barcode {bc} appears {cnt} times on page")

# Cross-check page vs run_yogurt_006
run006_products = glob.glob(os.path.join(yogurt_trace_run_shufersal, "products", "*"))
run006_ids = set(os.path.basename(d) for d in run006_products)
page_shufersal_ids = set(
    f"bsip1_yogurt_{p['barcode']}"
    for p in yogurt_fe["products"]
    if p.get("retailer", "shufersal") == "shufersal" and p.get("barcode")
)
on_page_not_in_run006 = page_shufersal_ids - run006_ids
in_run006_not_on_page = run006_ids - page_shufersal_ids
yogurt_anomalies.append(f"INFO: run_yogurt_006 has {len(run006_ids)} products; page Shufersal pool has {len(page_shufersal_ids)}; {len(in_run006_not_on_page)} in run not on page (corpus is larger, expected)")
if on_page_not_in_run006:
    yogurt_anomalies.append(f"ON_PAGE_SHUFERSAL_NOT_IN_RUN006: {sorted(on_page_not_in_run006)}")

yogurt_out = {
    "category": "yogurts",
    "role": "pilot",
    "source_frontend": r"bari-web/src/lib/comparisons/yogurts-comparison-page-data.ts",
    "source_frontend_data": r"bari-web/src/data/comparisons/yogurts_frontend_v3.json",
    "source_trace_run": {
        "shufersal_11_products": r"02_products/yogurt_system/bsip2_outputs/run_yogurt_006",
        "yohananof_8_products": r"02_products/yogurt_system/bsip2_outputs/run_yogurt_yohananof_001",
        "evidence": (
            "Frontend _meta.provenance: 'Shufersal pool (11 products): frozen from yogurts_frontend_v2.json / "
            "run_yogurt_006_recal_p0_trim. New Yohananof pool (8 products): run_yogurt_yohananof_001.' "
            "TASK-249 remediated run products live at run_yogurt_006/products/. "
            "run_yogurt_006_recal_p0_trim/run_record.json is marked _status=SUPERSEDED/REFERENCE_ONLY; "
            "it claims authoritative record at reports/ which does not exist in repo. "
            "Yohananof product traces verified to exist in run_yogurt_yohananof_001/products/."
        ),
    },
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "page_strings": YOGURT_PAGE_STRINGS,
    "products": yogurt_products_out,
    "integrity_anomalies": yogurt_anomalies,
}

out_yogurt = os.path.join(BASE, r"03_operations\claim_entailment\inputs\yogurts_claims_input_v1.json")
with open(out_yogurt, "w", encoding="utf-8") as f:
    json.dump(yogurt_out, f, ensure_ascii=False, indent=2)
print(f"Wrote {out_yogurt}")
print(f"Yogurt: {len(yogurt_products_out)} products, {len(yogurt_anomalies)} anomalies")
for a in yogurt_anomalies:
    print(f"  Y-ANOMALY: {a}")

##############################################################################
# CEREALS
##############################################################################
cereals_fe_path = os.path.join(BASE, r"bari-web\src\data\comparisons\cereals_frontend_v2.json")
cereals_fe = read_json(cereals_fe_path)
cereals_trace_run = os.path.join(BASE, r"02_products\breakfast_cereals\bsip2_outputs\run_cereals_006")

CEREALS_PAGE_STRINGS = {
    "hero_eyebrow": "דגני בוקר",
    "hero_title": "דגני בוקר: 34 מוצרים, אף אחד לא מגיע ל-A",
    "prologue_1": "בדקנו 34 מוצרי דגני בוקר מהמדף הישראלי — משופרסל וקרפור.",
    "prologue_2": "אף מוצר לא הגיע ל-A — הציון הגבוה ביותר עוצר ב-75/B.",
    "prologue_3": "החלוקה: שישה מוצרים ב-B, 11 ב-C, 16 ב-D ואחד ב-E.",
    "prologue_4": "חמישה מוצרים מיועדים לילדים; הפער בין הגבוה לנמוך הוא 43 נקודות.",
    "prologue_5": "גרנולה ומוזלי מוצגים בעמוד נפרד — משפחת מוצרים אחרת.",
    "category_note": (
        "הערת קטגוריה — העשרה בוויטמינים ומינרלים\n\n"
        "רוב דגני הבוקר מועשרים בוויטמינים ומינרלים סינתטיים — ברזל, ויטמיני B, חומצה פולית, ויטמין D. "
        "ההעשרה נגזרת מתהליך הייצור: הדגן המעובד מאבד חלק ממיקרו-הרכיבים שלו, והיצרן מחזיר אותם מבחוץ. "
        "ציון Bari מבוסס על מבנה המזון — כמות החלבון, הסיבים, רמת העיבוד ושלמות רשימת הרכיבים. "
        "הוא אינו מחשב תרומת מיקרו-רכיבים, בין אם מועשרים ובין אם מקוריים. "
        "מוצר מועשר עשוי לספק ברזל או ויטמין D שאינם משתקפים בציון.\n\n"
        "הערת קטגוריה — טענת 'דגנים מלאים' נקראת מהרשימה, לא מהמיתוג\n\n"
        "טענת 'דגנים מלאים' מופיעה על 20 מוצרים בעמוד זה, אך לא בכולם סדר הרכיבים תומך בה — "
        "לעיתים קמח לבן מופיע לפני הדגן המלא. הציון מבוסס על ההרכב בפועל, לא על הטענה שעל האריזה."
    ),
    "methodology_1": "בדקנו 34 מוצרי דגני בוקר משתי רשתות — שופרסל וקרפור — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
    "methodology_2": "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
    "methodology_3": "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
}

# Check available barcodes in run_cereals_006
run006c_products = set(os.path.basename(d) for d in glob.glob(os.path.join(cereals_trace_run, "products", "*")))

cereals_products_out = []
cereals_anomalies = []

for p in cereals_fe["products"]:
    barcode = str(p.get("barcode", ""))
    pid = p.get("id", "")

    trace_pid = f"bsip1_cereal_{barcode}" if barcode else pid
    trace_path = os.path.join(cereals_trace_run, "products", trace_pid, "bsip2_trace.json")

    trace = read_json(trace_path)
    if trace is None:
        cereals_anomalies.append(f"NO_TRACE: product {pid} (barcode={barcode}) not found in run_cereals_006")

    strings = product_strings_cereal(p)
    if not strings:
        cereals_anomalies.append(f"EMPTY_STRINGS: product {pid} (barcode={barcode}) has no extractable strings")

    cereals_products_out.append({
        "product_id": pid,
        "barcode": barcode,
        "name_he": p.get("name", ""),
        "strings": strings,
        "trace_path": trace_path,
        "trace_found": trace is not None,
        "trace_summary": trace_summary(trace),
    })

# Products on page not in run_cereals_006
page_cereal_ids = set(f"bsip1_cereal_{p['barcode']}" for p in cereals_fe["products"] if p.get("barcode"))
on_page_not_in_run006c = page_cereal_ids - run006c_products
in_run006c_not_on_page = run006c_products - page_cereal_ids
cereals_anomalies.append(
    f"INFO: run_cereals_006 has {len(run006c_products)} products; "
    f"page has {len(cereals_products_out)} products; "
    f"{len(in_run006c_not_on_page)} in run not on page"
)
if on_page_not_in_run006c:
    cereals_anomalies.append(
        f"ON_PAGE_NOT_IN_RUN006 (authoritative run_cereals_008 missing from repo): "
        f"{sorted(on_page_not_in_run006c)}"
    )

# page count vs JSON product_count mismatch
json_product_count = cereals_fe.get("_meta", {}).get("product_count", 0)
page_actual_count = len(cereals_products_out)
if json_product_count != page_actual_count:
    cereals_anomalies.append(
        f"COUNT_MISMATCH: _meta.product_count={json_product_count} but actual products array length={page_actual_count}"
    )

# route description says 37 products
cereals_anomalies.append(
    "INFO: bari-web/src/app/hashvaot/breakfast-cereals/page.tsx metadata description says '37 מוצרי דגני בוקר' "
    "but _meta.product_count=34 and products array has 34 entries — metadata description is stale"
)

cereals_out = {
    "category": "breakfast-cereals",
    "role": "control",
    "source_frontend": r"bari-web/src/lib/comparisons/cereals-page-data.ts",
    "source_frontend_data": r"bari-web/src/data/comparisons/cereals_frontend_v2.json",
    "source_trace_run": {
        "run": r"02_products/breakfast_cereals/bsip2_outputs/run_cereals_006",
        "note": "BEST AVAILABLE — authoritative run_cereals_008 not present in repo",
        "evidence": (
            "Frontend _meta.provenance: 'Shufersal pool (37 products): frozen from cereals_frontend_v1.json / run_cereals_008. "
            "Baseline: run_cereals_005 / run_cereals_008 (66 Shufersal barcodes).' "
            "run_cereals_007 and run_cereals_008 directories do not exist in "
            "02_products/breakfast_cereals/bsip2_outputs/. "
            "Highest available run with matching bsip1_cereal_BARCODE ID format is run_cereals_006 (63 products). "
            "7 frontend barcodes absent from run_cereals_006 — added between run_006 and missing run_008."
        ),
    },
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "page_strings": CEREALS_PAGE_STRINGS,
    "products": cereals_products_out,
    "integrity_anomalies": cereals_anomalies,
}

out_cereals = os.path.join(BASE, r"03_operations\claim_entailment\inputs\cereals_claims_input_v1.json")
with open(out_cereals, "w", encoding="utf-8") as f:
    json.dump(cereals_out, f, ensure_ascii=False, indent=2)
print(f"\nWrote {out_cereals}")
print(f"Cereals: {len(cereals_products_out)} products, {len(cereals_anomalies)} anomalies")
for a in cereals_anomalies:
    print(f"  C-ANOMALY: {a}")
