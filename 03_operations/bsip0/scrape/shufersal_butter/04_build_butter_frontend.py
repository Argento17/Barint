"""
Stage D — Frontend JSON builder for Butter (TASK-191).

Reads:   C:\\Bari\\02_products\\butter\\bsip2_outputs\\butter_run_001\\products\\*\\bsip2_trace.json
         + C:\\Bari\\02_products\\butter\\bsip1_outputs\\butter_bsip1_merged.json (for enrichment data)

Writes:  C:\\Bari\\02_products\\butter\\butter_frontend_v1.json
         C:\\bari\\bari-web\\src\\data\\comparisons\\butter_frontend_v1.json

Schema matches cereals_frontend_v1.json (BariProductVM[] v2).
Products with score=null (INSUFFICIENT) are included with grade="INSUFFICIENT".

Insight line rules (per row_description_standard_v1 + bari_insight_line_spec_v1):
  - T1 (composition fact): fat%, sat-fat, ingredients count
  - T2 (contradiction): cultured vs salted tension, reduced fat paradox
  - T3 (position): rank in category

Verdict rules (per comparison_row_verdict_model + editorial standard):
  - standing → why → catch → grade
  - Hebrew, assertive, insight-first
  - For INSUFFICIENT: note the missing panel, state what we know from identity
"""
from __future__ import annotations

import json
import pathlib
import logging
import shutil
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

TRACE_ROOT    = pathlib.Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_001\products")
BSIP1_PATH    = pathlib.Path(r"C:\Bari\02_products\butter\bsip1_outputs\butter_bsip1_merged.json")
OUT_LOCAL     = pathlib.Path(r"C:\Bari\02_products\butter\butter_frontend_v1.json")
OUT_WEBSITE   = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\butter_frontend_v1.json")


def _load_bsip1_by_pid(path: pathlib.Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {r["canonical_product_id"]: r for r in data}


def _load_traces(root: pathlib.Path) -> list[dict]:
    traces = []
    for product_dir in sorted(root.iterdir()):
        tf = product_dir / "bsip2_trace.json"
        if tf.exists():
            traces.append(json.loads(tf.read_text(encoding="utf-8")))
    return traces


def _confidence_label(trace: dict) -> str:
    ds = trace.get("data_sufficiency") or ""
    if ds == "insufficient":
        return "INSUFFICIENT"
    trust = trace.get("input_reference", {})
    # Use bsip1 trust level via source
    grade = trace.get("grade_estimate") or ""
    if grade == "INSUFFICIENT" or grade == "insufficient_data":
        return "INSUFFICIENT"
    conf = trace.get("confidence_band") or trace.get("nova_confidence_band") or ""
    if conf == "high":
        return "verified"
    if conf == "medium":
        return "partial"
    return "partial"


def _insight_line(trace: dict, bsip1: dict) -> str:
    """Build a T1/T2 insight line for a scored product."""
    nn = bsip1.get("normalized_nutrition_per_100g", {}) or {}
    fat = nn.get("fat_g")
    sat_fat = nn.get("fat_saturated_g")
    sodium_mg = nn.get("sodium_mg")
    name = bsip1.get("canonical_name_he", "")
    subtype = bsip1.get("bsip_butter_subtype", "")
    ingr_list = bsip1.get("ingredients_list") or []

    grade = trace.get("grade_estimate") or ""
    if grade in ("INSUFFICIENT", "insufficient_data"):
        return "פאנל תזונתי לא זמין — מוצר מזוהה, ציון לא ניתן לאימות"

    # Insight priority: sat fat fraction → sodium (if salted) → ingredients simplicity
    if sat_fat is not None and fat is not None and fat > 0:
        sat_pct = round(100 * sat_fat / fat)
        if sodium_mg and sodium_mg > 500:
            sodium_display = int(sodium_mg)
            return f"{sat_fat:.0f} גרם שומן רווי ל-100 גרם, נתרן {sodium_display} מ\"ג"
        if subtype == "reduced_fat":
            fat_display = int(fat)
            return f"חמאה מופחת שומן: {fat_display} גרם שומן ל-100 גרם ({sat_fat:.0f} גרם רווי)"
        if subtype == "cultured_fermented" and len(ingr_list) <= 2:
            return f"שמנת + תרבית לקטית בלבד — {sat_fat:.0f} גרם שומן רווי ל-100 גרם"
        return f"{sat_fat:.0f} גרם שומן רווי ל-100 גרם"
    if fat is not None:
        return f"{fat:.0f} גרם שומן ל-100 גרם"
    return "נתונים חלקיים"


def _row_verdict(trace: dict, bsip1: dict) -> str:
    """Build a 2-line Hebrew row verdict per the editorial standard."""
    nn = bsip1.get("normalized_nutrition_per_100g", {}) or {}
    fat = nn.get("fat_g")
    sat_fat = nn.get("fat_saturated_g")
    sodium_mg = nn.get("sodium_mg")
    name = bsip1.get("canonical_name_he", "")
    brand = bsip1.get("brand", "")
    subtype = bsip1.get("bsip_butter_subtype", "")
    ingr_list = bsip1.get("ingredients_list") or []
    additives = bsip1.get("extracted_additives") or []
    fermentation = bsip1.get("extracted_fermentation_markers") or []

    grade = trace.get("grade_estimate") or ""
    score = trace.get("final_score_estimate")

    if grade in ("INSUFFICIENT", "insufficient_data"):
        additive_note = ""
        if additives:
            additive_names = [a.get("term", "") for a in additives[:2]]
            additive_note = f" המוצר מכיל {', '.join(additive_names)}."
        return (
            f"מוצר מזוהה — פאנל תזונתי לא נמצא במאגרי הנתונים הציבוריים."
            f"{additive_note} ציון לא ניתן להפקה ללא נתוני תזונה."
        )

    score_display = int(score) if score is not None else "?"
    grade_display = grade or "?"

    # Determine the dominant story
    has_additive = len(additives) > 0
    is_cultured = subtype == "cultured_fermented" or bool(fermentation)
    is_salted = subtype == "salted" or (sodium_mg and sodium_mg > 400)
    is_reduced = subtype == "reduced_fat"
    is_herbed = subtype == "flavored_herbed"

    if is_herbed:
        additive_names = [a.get("term", "") for a in additives[:3]]
        additive_str = " + ".join(additive_names) if additive_names else "חומרים משמרים"
        return (
            f"חמאה מתובלת — מרכיבים נוספים מעבר לשמנת. "
            f"עוצרת ב-{grade_display} בשל {additive_str}."
        )

    if is_reduced:
        fat_display = int(fat) if fat else "?"
        return (
            f"חמאה מופחת שומן: {fat_display} גרם שומן ל-100 גרם — הנמוך ביותר בקטגוריה. "
            f"עוצרת ב-{grade_display}/{score_display} כי שומן חלבי נמוך לא הופך אותה לחמאה בריאה יותר — הרכב אחר."
        )

    if is_cultured and len(ingr_list) <= 2:
        sat_display = int(sat_fat) if sat_fat else "?"
        return (
            f"שני מרכיבים בלבד: שמנת ותרבית לקטית. מינימום עיבוד, מקסימום שמנת."
            f" {sat_display} גרם שומן רווי ל-100 גרם — עוצרת ב-{grade_display}/{score_display} בשל רמת שומן רווי גבוהה."
        )

    if is_salted and sodium_mg and sodium_mg > 800:
        return (
            f"מלוחה עם {int(sodium_mg)} מ\"ג נתרן ל-100 גרם — גבוה לקטגוריה. "
            f"עוצרת ב-{grade_display}/{score_display}."
        )

    # Default: plain/standard butter
    sat_display = int(sat_fat) if sat_fat else "?"
    return (
        f"חמאה בסיסית: שמנת ו{'מלח' if is_salted else 'תרבית לקטית' if is_cultured else 'מינימום מרכיבים'}. "
        f"{sat_display} גרם שומן רווי — עוצרת ב-{grade_display}/{score_display} בשל ריכוז השומן הרווי."
    )


def _subpool(trace: dict, bsip1: dict) -> str:
    subtype = bsip1.get("bsip_butter_subtype", "plain")
    return subtype


def _build_product(trace: dict, bsip1: dict | None) -> dict:
    ref = trace.get("input_reference", {}) or {}
    pid = ref.get("canonical_product_id", "")
    barcode = ref.get("barcode", "")
    name = ref.get("product_name_he", "")
    brand = ref.get("brand", "")
    retailers = ref.get("source_retailers", [])
    retailer = retailers[0] if retailers else "unknown"

    if bsip1 is None:
        bsip1 = {}

    nn = bsip1.get("normalized_nutrition_per_100g", {}) or {}
    score_raw = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate") or "INSUFFICIENT"

    # Normalize grade
    if grade in ("insufficient_data", "INSUFFICIENT"):
        grade = "INSUFFICIENT"
        score_display = None
    else:
        score_display = int(score_raw) if score_raw is not None else None

    image_url = bsip1.get("image_url") or (bsip1.get("image_urls") or [None])[0]
    ingredients_raw = bsip1.get("ingredients_text_he") or bsip1.get("ingredients_raw") or ""
    subtype = bsip1.get("bsip_butter_subtype", "plain")

    # Nutrition for expansion
    nutrition_obj = {
        "energyKcal": nn.get("energy_kcal"),
        "protein":    nn.get("protein_g"),
        "sugar":      nn.get("sugars_g"),
        "fat":        nn.get("fat_g"),
        "saturatedFat": nn.get("fat_saturated_g"),
        "fiber":      nn.get("dietary_fiber_g"),
        "sodium":     nn.get("sodium_mg"),
    }

    conf_label = _confidence_label(trace)
    insight = _insight_line(trace, bsip1)
    verdict = _row_verdict(trace, bsip1)

    # Explanation from trace
    drivers = trace.get("explanation_drivers") or []
    explanation_text = " | ".join(drivers[:2]) if drivers else ""

    return {
        "id": pid,
        "name": name,
        "brand": brand,
        "imageUrl": image_url,
        "score": score_display,
        "grade": grade,
        "insightLine": insight,
        "confidence": conf_label,
        "expansion": {
            "nutrition": nutrition_obj,
            "ingredients": ingredients_raw,
            "confidenceLabel": (
                "נתונים מלאים" if conf_label == "verified"
                else "נתונים חלקיים" if conf_label == "partial"
                else "פאנל לא זמין"
            ),
            "servingNote": "ל-100 גרם",
            "explanation": explanation_text,
        },
        "rowVerdict": verdict,
        "barcode": barcode,
        "retailer": retailer,
        "subtype": subtype,
    }


def main():
    if not TRACE_ROOT.exists():
        log.error("Trace directory not found: %s", TRACE_ROOT)
        log.error("Run batch_run_butter_001.py first.")
        return

    bsip1_map = _load_bsip1_by_pid(BSIP1_PATH)
    traces = _load_traces(TRACE_ROOT)
    log.info("Loaded %d traces", len(traces))

    products = []
    n_scored = 0
    n_insuff = 0

    for trace in traces:
        ref = trace.get("input_reference", {}) or {}
        pid = ref.get("canonical_product_id", "")
        bsip1 = bsip1_map.get(pid)

        if bsip1 is None:
            log.warning("No BSIP1 record for %s — using trace only", pid)

        p = _build_product(trace, bsip1)
        if p["grade"] == "INSUFFICIENT":
            n_insuff += 1
        else:
            n_scored += 1
        products.append(p)

    # Sort: scored products first (by score desc), then INSUFFICIENT alphabetically
    scored_products = [p for p in products if p["grade"] != "INSUFFICIENT"]
    insuff_products = [p for p in products if p["grade"] == "INSUFFICIENT"]
    scored_products.sort(key=lambda x: (-(x["score"] or 0)))
    insuff_products.sort(key=lambda x: x.get("name", ""))

    all_products = scored_products + insuff_products

    frontend = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "category": "butter",
            "product_count": len(all_products),
            "scored_count": n_scored,
            "schema": "BariProductVM[]",
            "version": "v2",
            "provenance": (
                "butter_run_001 (TASK-191): multi-retailer corpus "
                "(Shufersal 18 + Yohananof 17 seed + Carrefour 4). "
                "BSIP2 engine standard baseline, BARI_GLASSBOX_W4=on. "
                "Router: חמאה hard anchor added (TASK-191). "
                "23 INSUFFICIENT products: barcodes confirmed, no OFF panel available."
            ),
        },
        "products": all_products,
    }

    # Write local
    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.write_text(json.dumps(frontend, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Frontend JSON written: %s", OUT_LOCAL)

    # Copy to website
    OUT_WEBSITE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_LOCAL, OUT_WEBSITE)
    log.info("Copied to website: %s", OUT_WEBSITE)

    # Summary
    grade_dist: dict[str, int] = {}
    for p in all_products:
        g = p["grade"]
        grade_dist[g] = grade_dist.get(g, 0) + 1

    log.info("=== Frontend JSON Summary ===")
    log.info("  Total: %d  Scored: %d  INSUFFICIENT: %d", len(all_products), n_scored, n_insuff)
    log.info("  Grade distribution: %s", grade_dist)
    log.info("  Local:   %s", OUT_LOCAL)
    log.info("  Website: %s", OUT_WEBSITE)

    return frontend


if __name__ == "__main__":
    main()
