#!/usr/bin/env python3
"""
TASK-254/F1 — Claims inventory v2 (reconstructed traces)
Generates cereals_claims_input_v2.json pointing to reconstruction dirs.
Resolves all 8 NO_TRACE from v1.
"""
import json, os
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

cereals_fe_path = os.path.join(BASE, r"bari-web\src\data\comparisons\cereals_frontend_v2.json")
cereals_fe = read_json(cereals_fe_path)

RUN_008  = os.path.join(BASE, r"02_products\breakfast_cereals\bsip2_outputs\run_cereals_008_reconstruction")
RUN_MR   = os.path.join(BASE, r"02_products\breakfast_cereals\bsip2_outputs\run_cereals_multiretailer_001_reconstruction")

# Build lookup dicts
trace_index = {}
for run_dir, label in [(RUN_008, "run_cereals_008_reconstruction"), (RUN_MR, "run_cereals_multiretailer_001_reconstruction")]:
    pdir = os.path.join(run_dir, "products")
    if not os.path.exists(pdir):
        continue
    for d in os.listdir(pdir):
        tp = os.path.join(pdir, d, "bsip2_trace.json")
        if os.path.exists(tp):
            trace_index[d] = (tp, label)

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

products_out = []
anomalies = []

for p in cereals_fe["products"]:
    barcode = str(p.get("barcode", ""))
    pid = p.get("id", "")
    trace_pid = f"bsip1_cereal_{barcode}" if barcode else pid

    entry = trace_index.get(trace_pid)
    if entry is None:
        trace_path = ""
        trace_found = False
        trace_obj = None
        source_run = "UNKNOWN"
        anomalies.append(f"NO_TRACE: {pid} (barcode={barcode}) — not in any reconstruction dir")
    else:
        trace_path, source_run = entry
        trace_obj = read_json(trace_path)
        trace_found = trace_obj is not None
        if trace_obj is None:
            anomalies.append(f"TRACE_READ_FAIL: {pid} (barcode={barcode}) at {trace_path}")

    strings = product_strings_cereal(p)
    if not strings:
        anomalies.append(f"EMPTY_STRINGS: product {pid} (barcode={barcode}) has no extractable strings")

    products_out.append({
        "product_id": pid,
        "barcode": barcode,
        "name_he": p.get("name", ""),
        "strings": strings,
        "trace_path": trace_path,
        "trace_found": trace_found,
        "trace_summary": trace_summary(trace_obj),
    })

# Cross-check
page_ids = set(f"bsip1_cereal_{p['barcode']}" for p in cereals_fe["products"] if p.get("barcode"))
in_recon_not_on_page = set(trace_index.keys()) - page_ids
anomalies.append(
    f"INFO: reconstruction has {len(trace_index)} products total; "
    f"page has {len(products_out)} products; "
    f"{len(in_recon_not_on_page)} in recon not on page (corpus is larger, expected)"
)

out = {
    "category": "breakfast-cereals",
    "role": "control",
    "version": 2,
    "source_frontend": r"bari-web/src/lib/comparisons/cereals-page-data.ts",
    "source_frontend_data": r"bari-web/src/data/comparisons/cereals_frontend_v2.json",
    "source_trace_run": {
        "run_008_reconstruction": r"02_products/breakfast_cereals/bsip2_outputs/run_cereals_008_reconstruction",
        "run_multiretailer_001_reconstruction": r"02_products/breakfast_cereals/bsip2_outputs/run_cereals_multiretailer_001_reconstruction",
        "note": (
            "TASK-254/F1: Reconstructed traces for run_cereals_008 and run_cereals_multiretailer_001. "
            "v1 pointed to run_cereals_006 (BEST AVAILABLE) but 8 products had NO_TRACE. "
            "v2 resolves all 8 via reconstruction. Original run_cereals_008/run_cereals_multiretailer_001 "
            "directories do not exist in repo — reconstruction is the best available."
        ),
    },
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "page_strings": CEREALS_PAGE_STRINGS,
    "products": products_out,
    "integrity_anomalies": anomalies,
}

out_path = os.path.join(BASE, r"03_operations\claim_entailment\inputs\cereals_claims_input_v2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Wrote {out_path}")
print(f"Products: {len(products_out)}, Anomalies: {len(anomalies)}")
for a in anomalies:
    print(f"  ANOMALY: {a}")
