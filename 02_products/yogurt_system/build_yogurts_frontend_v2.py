# -*- coding: utf-8 -*-
"""
TASK-143 step 3c — build the run_yogurt_004 frontend package (yogurts_frontend_v2.json).

Engine UNMODIFIED. No score changes. This script only PACKAGES existing run_yogurt_004
outputs into the BariProductVM[] frontend schema (mirrors yogurts_frontend_v1.json).

Sources of truth:
  - scores/grades  -> bsip2_outputs/run_yogurt_004/products/**/bsip2_trace.json (final_score_estimate/grade_estimate)
  - macros         -> same trace, L1_observed_signals
  - insightLine    -> reports/content_reauthor_143_run_yogurt_004.md (3b re-author, verbatim)
  - prologue       -> 3b §3 (installed in the .ts page-data layer, not here)
  - soy/coconut    -> 3a ruling: DROP + DEFER (run contains zero plant products)

Expansion is TECHNICAL-ONLY this pass (Product decision 2026-06-02): clean nutrition grid only.
The ingredient_list in the traces is OCR-polluted (nutrition-panel + disclaimer bleed, and for
flavored SKUs the score-driving additives sit adjacent to that bleed), so the raw string is NOT
shipped; the ingredient narrative lives in each Content-authored insightLine. Interpretive
expansion (positiveSignals/limitingFactors/bottomLine) was explicitly deferred by 3b.
"""
import json
import os
from datetime import datetime, timezone

BASE = r"C:\Bari\02_products\yogurt_system"
TRACES = os.path.join(BASE, "bsip2_outputs", "run_yogurt_004", "products")
# Canonical BSIP1 records — source of the persisted Shufersal image URLs
# (same provenance bread/cheese/maadanim used). image step was never wired into the
# original 3c packaging pass, leaving imageUrl=null for all 11 (QA gap, TASK hygiene).
BSIP1 = os.path.join(r"C:\Bari", "03_operations", "bsip1", "run_yogurt_004", "output")
OUT = os.path.join(BASE, "yogurts_frontend_v2.json")

# Ordered, score-descending. (barcode, vm_id, display_name, cluster, insightLine)
# insightLine copied verbatim from content_reauthor_143_run_yogurt_004.md §4.
ROWS = [
    ("7290112336712", "yog-001", "דנונה פרו 21 חלבון 0%", "high-protein",
     "10.5 גרם חלבון ל-100 גרם ב-0% שומן, חמישה מרכיבים, בלי חומרי טעם או צבע. הציון הגבוה בקטגוריה — ונשאר B."),
    ("7290110328221", "yog-002", "יוגורט נטול לקטוז 3% שומן", "plain",
     "אותו בסיס חלבי של יוגורט ביו, עם חיידקי ביפידוס — ולקטוז עד 0.05%."),
    ("7290014758100", "yog-003", "יוגורט ביו תנובה 3%", "plain",
     "חלב, רכיבי חלב וחיידקי ביפידוס — 5.3 גרם חלבון, בלי טעמים מוספים. בסיס יוגורט פשוט."),
    ("7290114311069", "yog-004", "מולר אקטיב לבן 0% 25 חלבון", "high-protein",
     "12.5 גרם חלבון ל-100 גרם עם 2.5 גרם סיבים, 0% שומן — ועדיין B. חלבון גבוה לבדו לא חוצה את התקרה."),
    ("7290014758117", "yog-005", "יוגורט ביו תנובה 1.5%", "plain",
     "אותו ביו של תנובה בגרסת 1.5% שומן — אותם חיידקי ביפידוס, פחות שומן, אותו אשכול ציון."),
    ("7290012645297", "yog-006", "יוגורט עיזים ביו", "plain",
     "חלב עיזים, סיבים תזונתיים ותרבית יוגורט — שישה מרכיבים, בלי טעמים. הבסיס הפשוט של מדף העיזים."),
    ("7290107936309", "yog-007", "יוגורט בסגנון יווני 6.5%", "greek",
     "מסוי בסגנון יווני, 5.5 גרם חלבון ו-0 סוכר מוסף — אבל 6.5% שומן (3.9 גרם רווי) מחזיק אותו ב-B."),
    ("7290110321031", "yog-008", "יופלה GO מועשר בחלבון", "high-protein",
     "10 גרם חלבון, בלי סוכר מוסף ובלי תוספים — אבל החלבון מאבקת חלב, לא מתסיסה. נקודת המעבר התחתונה של ה-B."),
    ("7290014890589", "yog-009", "יוגורט יווני 8%", "greek",
     "שלושה מרכיבים בלבד — חלב, שמנת וחלבון חלב — אבל 8% שומן ו-4.8 גרם רווי ל-100 גרם מורידים אותו ל-C. נקי לא תמיד אומר רזה."),
    ("7290110321680", "yog-010", "יופלה GO תות", "flavored",
     "אותם 10 גרם חלבון של ה-GO הלבן — אבל 9.6 גרם סוכר, 16 מרכיבים, צבע מאכל ועמילן מעובד מורידים אותו ל-D. הטעם הוא ההבדל."),
    ("7290010471669", "yog-011", "יוגורט קראנצ תות קורנפלק", "flavored",
     "יוגורט עם תוסף קורנפלקס ושוקולד: 19 מרכיבים, 9.9 גרם סוכר ו-13.1 גרם פחמימות. הציון הנמוך במדף."),
]

CONF_LABEL = {"verified": "נתונים מלאים", "partial": "נתונים חלקיים", "insufficient": "נתונים חסרים"}
# NutritionGrid renders exactly these 5 cells:
GRID_KEYS = ["energyKcal", "protein", "sugar", "fat", "sodium"]


def load_trace(barcode):
    folder = os.path.join(TRACES, f"bsip1_yogurt_{barcode}")
    with open(os.path.join(folder, "bsip2_trace.json"), encoding="utf-8") as f:
        return json.load(f)


def load_image_url(barcode):
    """Read the persisted Shufersal image_url from the canonical BSIP1 record.
    Returns None (never fabricates) if the record or field is missing; the
    builder asserts non-null below so a missing image fails loudly."""
    path = os.path.join(BSIP1, f"bsip1_{barcode}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    url = rec.get("image_url")
    # Sanity: the persisted URL must embed this product's barcode (no cross-wiring).
    if url and barcode in url:
        return url
    return None


def round_score(x):
    return int(x + 0.5)  # round-half-up for positive scores


products = []
audit = []
for barcode, vid, name, cluster, insight in ROWS:
    t = load_trace(barcode)
    L = t["L1_observed_signals"]
    raw_score = t["final_score_estimate"]
    grade = t["grade_estimate"]
    nutrition = {
        "energyKcal": L.get("energy_kcal"),
        "protein": L.get("protein_g"),
        "sugar": L.get("sugars_g"),
        "fat": L.get("fat_g"),
        "fiber": L.get("dietary_fiber_g"),
        "sodium": L.get("sodium_mg"),
    }
    # confidence = verified iff all 5 grid macros present, else partial
    all_grid = all(nutrition[k] is not None for k in GRID_KEYS)
    confidence = "verified" if all_grid else "partial"
    image_url = load_image_url(barcode)
    if image_url is None:
        raise SystemExit(
            f"MISSING IMAGE: {vid} ({barcode}) has no persisted Shufersal image_url "
            f"in {BSIP1}. Refusing to fabricate a URL."
        )
    products.append({
        "id": vid,
        "name": name,
        "imageUrl": image_url,
        "score": round_score(raw_score),
        "grade": grade,
        "confidence": confidence,
        "insightLine": insight,
        "_cluster": cluster,
        "expansion": {
            "nutrition": nutrition,
            "ingredients": None,
            "confidenceLabel": CONF_LABEL[confidence],
            "servingNote": "ל-100 גרם",
        },
    })
    audit.append({
        "id": vid, "barcode": barcode, "name": name, "cluster": cluster,
        "raw_score": raw_score, "displayed_score": round_score(raw_score), "grade": grade,
        "confidence": confidence,
        "trace_name": t["input_reference"]["product_name_he"],
        "missing_grid_macros": [k for k in GRID_KEYS if nutrition[k] is None],
        "image_file": image_url.split("/")[-1],
    })

payload = {
    "_meta": {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "category": "yogurts",
        "product_count": len(products),
        "scored_count": len(products),
        "schema": "BariProductVM[]",
        "version": "v2-run_yogurt_004",
        "expansion": "technical_only_v1",
        "scope_note": "מדף יוגורט אמיתי (Shufersal) — ציוני מנוע Bari 0.4.0 (run_yogurt_004); מחליף את DEC-005 הידני",
        "provenance": {
            "run_id": "run_yogurt_004",
            "engine": "proto_v0 / 0.4.0 (UNMODIFIED)",
            "scores_from": "bsip2_trace.json final_score_estimate (rounded half-up for display)",
            "insight_lines_from": "content_reauthor_143_run_yogurt_004.md (3b)",
            "soy_coconut": "DROP+DEFER per 3a ruling (run contains zero plant-base products)",
            "expansion_note": "technical-only: clean nutrition grid; raw ingredient strings withheld (OCR/disclaimer bleed); interpretive expansion deferred by 3b",
            "retires": "DEC-005 (yogurts_frontend_v1.json, 13 manual products, A-heavy)",
            "task": "TASK-143",
        },
    },
    "products": products,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# Audit / reconcile-check summary to stdout
print(f"WROTE {OUT}")
print(f"products: {len(products)}  | grades: " +
      ", ".join(f"{p['grade']}" for p in products))
print("id   barcode        disp(raw)    grade conf      name")
for a in audit:
    print(f"{a['id']} {a['barcode']:>13} {a['displayed_score']:>3}({a['raw_score']:>5})  "
          f"{a['grade']:<2}   {a['confidence']:<8} {a['name']}  "
          f"{'MISSING:'+','.join(a['missing_grid_macros']) if a['missing_grid_macros'] else ''}")
