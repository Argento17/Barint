#!/usr/bin/env python3
"""
_build_claims_v3.py — Claims inventory v3 + v2 with display_values per rubric §9.

Generates:
  - yogurts_claims_input_v2.json  (v1 + display_values)
  - cereals_claims_input_v3.json  (v2 + display_values)

display_values block per §9: display_score/grade from live frontend JSON;
nutrition + ingredient fields from BSIP1 corpus files. No OFF, no invention.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BASE = r"C:\Bari"


def read_json(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── BSIP1 corpus helpers ────────────────────────────────────────────────

def load_bsip1_index(corpus_dir: str) -> dict[str, dict]:
    """Load all BSIP1 product files keyed by barcode."""
    index: dict[str, dict] = {}
    d = Path(corpus_dir)
    if not d.exists():
        return index
    for fpath in sorted(d.iterdir()):
        if fpath.suffix != ".json":
            continue
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            bc = data.get("barcode", "")
            if bc:
                index[bc] = data
        except Exception:
            pass
    return index


# BSIP1 corpus paths
BSIP1_YOGURT = os.path.join(BASE, r"03_operations\bsip1\run_yogurt_006\output")
BSIP1_YOGURT_YOHANANOF = os.path.join(BASE, r"03_operations\bsip1\run_yogurt_yohananof_001\output")
BSIP1_CEREALS = os.path.join(BASE, r"03_operations\bsip1\run_cereals_005\output")

# Load indexes once
_YOGURT_BSIP1 = load_bsip1_index(BSIP1_YOGURT)
_YOGURT_YOHANANOF_BSIP1 = load_bsip1_index(BSIP1_YOGURT_YOHANANOF)
_CEREALS_BSIP1 = load_bsip1_index(BSIP1_CEREALS)


def _find_bsip1(barcode: str, category: str) -> dict | None:
    """Look up a barcode in the appropriate BSIP1 corpus index."""
    if category == "yogurts":
        entry = _YOGURT_BSIP1.get(barcode)
        if entry is None:
            entry = _YOGURT_YOHANANOF_BSIP1.get(barcode)
        return entry
    elif category == "breakfast-cereals":
        return _CEREALS_BSIP1.get(barcode)
    return None


# ── Display-values builder (§9) ─────────────────────────────────────────

# BSIP1 → display_values field mapping
NUTR_MAP: list[tuple[str, str]] = [
    ("energy_kcal_per_100g",        "energy_kcal"),
    ("protein_g_per_100g",          "protein_g"),
    ("fat_g_per_100g",              "fat_g"),
    ("saturated_fat_g_per_100g",    "fat_saturated_g"),
    ("carbohydrate_g_per_100g",     "carbohydrates_g"),
    ("sugar_g_per_100g",            "sugars_g"),
    ("fiber_g_per_100g",            "dietary_fiber_g"),
    ("sodium_mg_per_100g",          "sodium_mg"),
]

# Fields displayed as integers (energy_kcal, sodium_mg)
INT_FIELDS = {"energy_kcal_per_100g", "sodium_mg_per_100g"}


def _extract_percentages(
    ingredients_list: list[str],
) -> dict[str, float]:
    """Extract {ingredient_stem: percentage} from ingredients list."""
    pct_re = re.compile(r"\((\d+\.?\d*)%\)\s*$")
    result: dict[str, float] = {}
    for entry in ingredients_list:
        entry = entry.strip()
        m = pct_re.search(entry)
        if m:
            pct = float(m.group(1))
            stem = entry[: m.start()].strip()
            # Clean trailing punctuation
            stem = stem.rstrip(" ,;.")
            if stem and pct > 0:
                result[stem] = pct
    return result


def _ingredient_stem(raw: str) -> str:
    """Clean an ingredient name — strip trailing parenthetical annotations but keep the base name."""
    s = raw.strip()
    # Remove trailing parenthetical groups like (מכיל גלוטן) or (95%) or (7.4%)
    while True:
        m = re.search(r"\s*\([^)]*\)\s*$", s)
        if m:
            s = s[: m.start()].strip()
        else:
            break
    return s


def _build_display_values(
    fe_product: dict,
    barcode: str,
    category: str,
) -> dict:
    """Build the display_values block per rubric §9."""
    bsip1 = _find_bsip1(barcode, category)

    dv: dict = {
        "display_score": fe_product.get("score"),
        "display_grade": fe_product.get("grade"),
        "energy_kcal_per_100g": None,
        "protein_g_per_100g": None,
        "fat_g_per_100g": None,
        "saturated_fat_g_per_100g": None,
        "carbohydrate_g_per_100g": None,
        "sugar_g_per_100g": None,
        "fiber_g_per_100g": None,
        "sodium_mg_per_100g": None,
        "ingredient_count": None,
        "ingredient_first": None,
        "ingredient_percentages": {},
        "ingredient_list_sha256": None,
    }

    if bsip1 is None:
        return dv

    # Nutrition fields
    nutr = bsip1.get("normalized_nutrition_per_100g", {}) or {}
    for dv_key, bsip1_key in NUTR_MAP:
        val = nutr.get(bsip1_key)
        if val is not None:
            if dv_key in INT_FIELDS:
                dv[dv_key] = round(val)
            else:
                # Round to 1dp for display consistency
                dv[dv_key] = round(float(val), 1)
        else:
            dv[dv_key] = None

    # Ingredient fields
    ingr_list = bsip1.get("ingredients_list", []) or []
    dv["ingredient_count"] = len(ingr_list) if ingr_list else None

    if ingr_list:
        dv["ingredient_first"] = _ingredient_stem(ingr_list[0])

    percentages = _extract_percentages(ingr_list)
    if percentages:
        dv["ingredient_percentages"] = percentages

    # SHA-256 of full raw ingredient text
    ingr_raw = bsip1.get("ingredients_raw", "") or ""
    if ingr_raw:
        dv["ingredient_list_sha256"] = hashlib.sha256(
            ingr_raw.encode("utf-8")
        ).hexdigest()

    return dv


# ── YOGURTS ─────────────────────────────────────────────────────────────

def _product_strings_yogurt(p: dict) -> dict:
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
    if p.get("confidence_label_he"):
        s["confidence_label_he"] = p["confidence_label_he"]
    if p.get("confidence_tooltip_he"):
        s["confidence_tooltip_he"] = p["confidence_tooltip_he"]
    return s


YOGURT_PAGE_STRINGS = {
    "hero_eyebrow": "יוגורטים · מדף ישראלי",
    "hero_title": "יוגורט: לא כל \"טבעי\" נוצר שווה",
    "prologue_1": (
        "בדקנו מחדש את מדף היוגורט על נתוני אריזה אמיתיים — רכיבים, חלבון, "
        "סוכר ושומן. התמונה התהפכה מהבדיקה הקודמת: שבעה יוגורטים על המדף "
        "מגיעים ל-A. הציון הגבוה הוא 96/A — דנונה PRO יוגורט 20 גרם חלבון, "
        "על בסיס חלבון גבוה במיוחד ותרביות חיות."
    ),
    "prologue_2": (
        "היוגורטים הפשוטים של תנובה — ביו 3% וביו 1.5% — וגם נטול הלקטוז "
        "מגיעים ל-80 עד 81, כולם A: בסיס חלבי, חיידקי ביפידוס, מעט מרכיבים. "
        "יוגורט עיזים נשאר ב-77/B, בעיקר כי החלבון בו נמוך יותר."
    ),
    "prologue_3": (
        "מכאן זה יורד. ככל שמתווספים סוכר, חומרי טעם, מייצבים או פצפוצים — "
        "הציון נופל. גרסאות הטעם וה'קראנצ' מגיעות עד C ו-D, גם כשכמות "
        "החלבון על האריזה זהה. ושומן גבוה לא מעלה ציון: יווני 8% עם 4.8 גרם "
        "שומן רווי עוצר ב-79/B, מתחת לבסיסים הרזים."
    ),
    "prologue_4": (
        "במדף הזה 'הכי טוב' הוא A — אבל לא S. גם היוגורט המוביל נעצר ב-A: "
        "ציון החלבון והתרביות מרים אותו גבוה, אך לא הופך אותו ליוצא דופן. "
        "הכי טוב, לא מושלם."
    ),
    "category_note": (
        "הערת קטגוריה — אותה תווית, שני קצוות\n\n"
        "הציון משקלל את ההרכב כולו — חלבון, סוכר, מייצבים ורמת עיבוד — "
        "ולא תווית אחת. אותו 'עשיר בחלבון' יכול לשבת בראש המדף כשהבסיס "
        "פשוט, וליפול ל-C או D בגרסת טעמים שמוסיפה סוכר, חומרי טעם ופצפוצים "
        "על אותו חלבון בדיוק. מספר החלבון על החזית אינו מספיק כדי לקבוע את "
        "הציון.\n\n"
        "הערת קטגוריה — 'הכי טוב' כאן הוא A, לא S\n\n"
        "שבעה יוגורטים על המדף מגיעים ל-A, והגבוה הוא 96/A. אבל אף אחד לא "
        "מגיע ל-S, גם המוביל: חלבון גבוה ותרביות חיות מרימים את הציון, "
        "ואינם הופכים יוגורט ליוצא דופן. A כאן אומר יוגורט טוב באמת — לא "
        "מושלם, ולא מעבר לכך.\n\n"
        "הערת קטגוריה — סיבים תזונתיים\n\n"
        "מוצרי חלב כמעט אינם מציינים סיבים תזונתיים על התווית, ולכן ערך זה "
        "אינו נכנס לניתוח בקטגוריה זו."
    ),
    "methodology_1": (
        "נבדקו 19 יוגורטים מהמדף הישראלי — מחלב פשוט ועד גרסאות חלבון עם "
        "תוספים."
    ),
    "methodology_2": (
        "לכל מוצר נבחנו הרכב הרכיבים, רמת חלבון, תוספי מייצבים, סוכר מוסף "
        "ורמת עיבוד."
    ),
    "methodology_3": (
        "ציון יוגורט טבעי מבוסס גבוה יותר ממוצר בטעמים — לא בגלל שמות, אלא "
        "בגלל מה שכתוב ברשימת הרכיבים."
    ),
    "methodology_4": (
        "מעדני חלב — מוצרים עם שכבות שוקולד, קצפת, או מבנה קינוח — אינם "
        "נכללים בהשוואה; הם מוצרי הנאה נפרדים. יוגורט שתיה נכלל ומקבל ציון "
        "כמוצר יוגורט מעובד."
    ),
}


def build_yogurts(fe_path: str) -> tuple[list[dict], list[str]]:
    fe = read_json(fe_path)
    if fe is None:
        return [], ["YOGURT_FRONTEND_NOT_FOUND"]

    trace_run_shufersal = os.path.join(
        BASE, r"02_products\yogurt_system\bsip2_outputs\run_yogurt_006_shipcfg2\products"
    )
    trace_run_yohananof = os.path.join(
        BASE, r"02_products\yogurt_system\bsip2_outputs\run_yogurt_yohananof_001"
    )

    anomalies: list[str] = []
    products_out: list[dict] = []

    for p in fe["products"]:
        barcode = str(p.get("barcode", ""))
        pid = p.get("id", "")
        retailer = p.get("retailer", "shufersal")

        if retailer == "yohananof":
            trace_run_dir = trace_run_yohananof
        else:
            trace_run_dir = trace_run_shufersal

        trace_pid = f"bsip1_yogurt_{barcode}" if barcode else pid
        trace_path = os.path.join(
            trace_run_dir, "products", trace_pid, "bsip2_trace.json"
        )
        trace = read_json(trace_path)
        if trace is None:
            anomalies.append(
                f"NO_TRACE: {pid} (barcode={barcode}, retailer={retailer})"
            )

        strings = _product_strings_yogurt(p)
        if not strings:
            anomalies.append(
                f"EMPTY_STRINGS: {pid} (barcode={barcode})"
            )

        dv = _build_display_values(p, barcode, "yogurts")

        products_out.append({
            "product_id": pid,
            "barcode": barcode,
            "name_he": p.get("name", ""),
            "strings": strings,
            "display_values": dv,
            "trace_path": trace_path,
            "trace_found": trace is not None,
            "trace_summary": _trace_summary(trace),
        })

    # Cross-check run_yogurt_006
    run006_products = glob.glob(
        os.path.join(trace_run_shufersal, "products", "*")
    )
    run006_ids = set(os.path.basename(d) for d in run006_products)
    page_shufersal_ids = {
        f"bsip1_yogurt_{p['barcode']}"
        for p in fe["products"]
        if p.get("retailer", "shufersal") == "shufersal" and p.get("barcode")
    }
    in_run006_not_on_page = run006_ids - page_shufersal_ids
    anomalies.append(
        f"INFO: run_yogurt_006 has {len(run006_ids)} products; "
        f"page Shufersal pool has {len(page_shufersal_ids)}; "
        f"{len(in_run006_not_on_page)} in run not on page (corpus is larger, expected)"
    )

    # Add metadataLine
    meta_line = (
        f"{fe['_meta']['product_count']} מוצרים נבדקו · "
        f"מדגם מדף ישראלי · ממוין לפי ציון Bari"
    )
    YOGURT_PAGE_STRINGS["metadataLine"] = meta_line

    return products_out, anomalies


# ── CEREALS ──────────────────────────────────────────────────────────────

CEREALS_PAGE_STRINGS = {
    "hero_eyebrow": "דגני בוקר",
    "hero_title": "דגני בוקר: 34 מוצרים, אף אחד לא מגיע ל-A",
    "prologue_1": (
        "בדקנו 34 מוצרי דגני בוקר מהמדף הישראלי — משופרסל וקרפור."
    ),
    "prologue_2": (
        "אף מוצר לא הגיע ל-A — הציון הגבוה ביותר עוצר ב-75/B."
    ),
    "prologue_3": (
        "החלוקה: שישה מוצרים ב-B, 11 ב-C, 16 ב-D ואחד ב-E."
    ),
    "prologue_4": (
        "חמישה מוצרים מיועדים לילדים; הפער בין הגבוה לנמוך הוא 43 נקודות."
    ),
    "prologue_5": (
        "גרנולה ומוזלי מוצגים בעמוד נפרד — משפחת מוצרים אחרת."
    ),
    "category_note": (
        "הערת קטגוריה — העשרה בוויטמינים ומינרלים\n\n"
        "רוב דגני הבוקר מועשרים בוויטמינים ומינרלים סינתטיים — ברזל, "
        "ויטמיני B, חומצה פולית, ויטמין D. ההעשרה נגזרת מתהליך הייצור: "
        "הדגן המעובד מאבד חלק ממיקרו-הרכיבים שלו, והיצרן מחזיר אותם מבחוץ. "
        "ציון Bari מבוסס על מבנה המזון — כמות החלבון, הסיבים, רמת העיבוד "
        "ושלמות רשימת הרכיבים. הוא אינו מחשב תרומת מיקרו-רכיבים, בין אם "
        "מועשרים ובין אם מקוריים. מוצר מועשר עשוי לספק ברזל או ויטמין D "
        "שאינם משתקפים בציון.\n\n"
        "הערת קטגוריה — טענת 'דגנים מלאים' נקראת מהרשימה, לא מהמיתוג\n\n"
        "טענת 'דגנים מלאים' מופיעה על 20 מוצרים בעמוד זה, אך לא בכולם סדר "
        "הרכיבים תומך בה — לעיתים קמח לבן מופיע לפני הדגן המלא. הציון מבוסס "
        "על ההרכב בפועל, לא על הטענה שעל האריזה."
    ),
    "methodology_1": (
        "בדקנו 34 מוצרי דגני בוקר משתי רשתות — שופרסל וקרפור — רכיבים, "
        "ערכי תזונה ורמת עיבוד, לא רק קלוריות."
    ),
    "methodology_2": (
        "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A."
    ),
    "methodology_3": (
        "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה "
        "שזמין."
    ),
}


def _product_strings_cereal(p: dict) -> dict:
    s = {}
    if p.get("insightLine"):
        s["insightLine"] = p["insightLine"]
    if p.get("rowVerdict"):
        s["rowVerdict"] = p["rowVerdict"]
    exp = p.get("expansion", {})
    if exp.get("confidenceLabel"):
        s["confidenceLabel"] = exp["confidenceLabel"]
    if p.get("confidence_label_he"):
        s["confidence_label_he"] = p["confidence_label_he"]
    if p.get("confidence_tooltip_he"):
        s["confidence_tooltip_he"] = p["confidence_tooltip_he"]
    return s


def build_cereals(fe_path: str) -> tuple[list[dict], list[str]]:
    fe = read_json(fe_path)
    if fe is None:
        return [], ["CEREALS_FRONTEND_NOT_FOUND"]

    run_008 = os.path.join(
        BASE,
        r"02_products\breakfast_cereals\bsip2_outputs"
        r"\run_cereals_008_reconstruction",
    )
    run_mr = os.path.join(
        BASE,
        r"02_products\breakfast_cereals\bsip2_outputs"
        r"\run_cereals_multiretailer_001_reconstruction",
    )

    trace_index: dict[str, tuple[str, str]] = {}
    for run_dir, label in [
        (run_008, "run_cereals_008_reconstruction"),
        (run_mr, "run_cereals_multiretailer_001_reconstruction"),
    ]:
        pdir = os.path.join(run_dir, "products")
        if not os.path.exists(pdir):
            continue
        for d in os.listdir(pdir):
            tp = os.path.join(pdir, d, "bsip2_trace.json")
            if os.path.exists(tp):
                trace_index[d] = (tp, label)

    anomalies: list[str] = []
    products_out: list[dict] = []

    for p in fe["products"]:
        barcode = str(p.get("barcode", ""))
        pid = p.get("id", "")
        trace_pid = f"bsip1_cereal_{barcode}" if barcode else pid

        entry = trace_index.get(trace_pid)
        if entry is None:
            trace_path = ""
            trace_found = False
            trace_obj = None
            source_run = "UNKNOWN"
            anomalies.append(
                f"NO_TRACE: {pid} (barcode={barcode}) — "
                f"not in any reconstruction dir"
            )
        else:
            trace_path, source_run = entry
            trace_obj = read_json(trace_path)
            trace_found = trace_obj is not None
            if trace_obj is None:
                anomalies.append(
                    f"TRACE_READ_FAIL: {pid} (barcode={barcode}) at {trace_path}"
                )

        strings = _product_strings_cereal(p)
        if not strings:
            anomalies.append(
                f"EMPTY_STRINGS: {pid} (barcode={barcode})"
            )

        dv = _build_display_values(p, barcode, "breakfast-cereals")

        products_out.append({
            "product_id": pid,
            "barcode": barcode,
            "name_he": p.get("name", ""),
            "strings": strings,
            "display_values": dv,
            "trace_path": trace_path,
            "trace_found": trace_found,
            "trace_summary": _trace_summary(trace_obj),
        })

    # Cross-check
    page_ids = {
        f"bsip1_cereal_{p['barcode']}"
        for p in fe["products"]
        if p.get("barcode")
    }
    in_recon_not_on_page = set(trace_index.keys()) - page_ids
    anomalies.append(
        f"INFO: reconstruction has {len(trace_index)} products total; "
        f"page has {len(products_out)} products; "
        f"{len(in_recon_not_on_page)} in recon not on page (corpus is larger, expected)"
    )

    return products_out, anomalies


# ── Shared helpers ───────────────────────────────────────────────────────

def _trace_summary(trace: dict | None) -> dict | None:
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


# ── Inventory stats ─────────────────────────────────────────────────────

def _dv_nonnull_counts(products: list[dict]) -> dict[str, int]:
    """Count non-null display_values fields."""
    fields = [
        "display_score", "display_grade", "energy_kcal_per_100g",
        "protein_g_per_100g", "fat_g_per_100g", "saturated_fat_g_per_100g",
        "carbohydrate_g_per_100g", "sugar_g_per_100g", "fiber_g_per_100g",
        "sodium_mg_per_100g", "ingredient_count", "ingredient_first",
        "ingredient_list_sha256",
    ]
    counts: dict[str, int] = {}
    for f in fields:
        counts[f] = sum(
            1 for p in products
            if p.get("display_values", {}).get(f) is not None
        )
    # ingredient_percentages: count non-empty dicts
    counts["ingredient_percentages"] = sum(
        1 for p in products
        if p.get("display_values", {}).get("ingredient_percentages", {})
    )
    return counts


# ── MAIN ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Building claims inventories v3 (display_values)")
    print("=" * 60)

    # Yogurts v2
    print("\n--- YOGURTS ---")
    yogurt_fe_path = os.path.join(
        BASE, r"bari-web\src\data\comparisons\yogurts_frontend_v4.json"
    )
    yogurt_products, yogurt_anomalies = build_yogurts(yogurt_fe_path)

    yogurt_out = {
        "category": "yogurts",
        "role": "pilot",
        "version": 3,
        "source_frontend": (
            r"bari-web/src/lib/comparisons/yogurts-comparison-page-data.ts"
        ),
        "source_frontend_data": (
            r"bari-web/src/data/comparisons/yogurts_frontend_v4.json"
        ),
        "source_bsip1": {
            "shufersal": r"03_operations/bsip1/run_yogurt_006/output",
            "yohananof": r"03_operations/bsip1/run_yogurt_yohananof_001/output",
        },
        "source_trace_run": {
            "shufersal_17_products": (
                r"02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2"
            ),
            "evidence": (
                "P15-carry-forward: repointed from v3→v4 + run_006→shipcfg2. "
                "display_score/grade from yogurts_frontend_v4.json; "
                "nutrition + ingredient fields from run_yogurt_006 BSIP1 corpus."
            ),
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "page_strings": YOGURT_PAGE_STRINGS,
        "products": yogurt_products,
        "integrity_anomalies": yogurt_anomalies,
    }

    out_yogurt = os.path.join(
        BASE,
        r"03_operations\claim_entailment\inputs"
        r"\yogurts_claims_input_v3.json",
    )
    with open(out_yogurt, "w", encoding="utf-8") as f:
        json.dump(yogurt_out, f, ensure_ascii=False, indent=2)

    y_dv = _dv_nonnull_counts(yogurt_products)
    print(f"  Products: {len(yogurt_products)}")
    print(f"  Anomalies: {len(yogurt_anomalies)}")
    print(f"  display_values non-null:")
    for k, v in sorted(y_dv.items()):
        print(f"    {k}: {v}/{len(yogurt_products)}")
    for a in yogurt_anomalies:
        print(f"  ANOMALY: {a}")
    print(f"  Wrote: {out_yogurt}")

    # Cereals v3
    print("\n--- CEREALS ---")
    cereals_fe_path = os.path.join(
        BASE, r"bari-web\src\data\comparisons\cereals_frontend_v2.json"
    )
    cereals_products, cereals_anomalies = build_cereals(cereals_fe_path)

    cereals_out = {
        "category": "breakfast-cereals",
        "role": "control",
        "version": 3,
        "source_frontend": (
            r"bari-web/src/lib/comparisons/cereals-page-data.ts"
        ),
        "source_frontend_data": (
            r"bari-web/src/data/comparisons/cereals_frontend_v2.json"
        ),
        "source_bsip1": r"03_operations/bsip1/run_cereals_005/output",
        "source_trace_run": {
            "run_008_reconstruction": (
                r"02_products/breakfast_cereals/bsip2_outputs"
                r"/run_cereals_008_reconstruction"
            ),
            "run_multiretailer_001_reconstruction": (
                r"02_products/breakfast_cereals/bsip2_outputs"
                r"/run_cereals_multiretailer_001_reconstruction"
            ),
            "note": (
                "TASK-254/F2: added display_values per rubric §9. "
                "display_score/grade from cereals_frontend_v2.json; "
                "nutrition + ingredient fields from run_cereals_005 BSIP1 corpus."
            ),
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "page_strings": CEREALS_PAGE_STRINGS,
        "products": cereals_products,
        "integrity_anomalies": cereals_anomalies,
    }

    out_cereals = os.path.join(
        BASE,
        r"03_operations\claim_entailment\inputs"
        r"\cereals_claims_input_v3.json",
    )
    with open(out_cereals, "w", encoding="utf-8") as f:
        json.dump(cereals_out, f, ensure_ascii=False, indent=2)

    c_dv = _dv_nonnull_counts(cereals_products)
    print(f"  Products: {len(cereals_products)}")
    print(f"  Anomalies: {len(cereals_anomalies)}")
    print(f"  display_values non-null:")
    for k, v in sorted(c_dv.items()):
        print(f"    {k}: {v}/{len(cereals_products)}")
    for a in cereals_anomalies:
        print(f"  ANOMALY: {a}")
    print(f"  Wrote: {out_cereals}")


if __name__ == "__main__":
    main()
