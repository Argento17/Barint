#!/usr/bin/env python3
"""
Butter — BariProductVM Builder v2 (butter_frontend_v2.json)
Based on butter_run_003 (EV-047 + EV-048 + EV-050 all active).
TASK-191 Phase B — builds corrected frontend JSON for M2 owner preview.

Do NOT copy to bari-web/src/data/comparisons/ — that requires M2 owner approval (Phase C).

Input:  BSIP2 traces from butter_run_003
Output: C:\\Bari\\02_products\\butter\\butter_frontend_v2.json
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────
BSIP2_DIR    = Path(r"C:\Bari\02_products\butter\bsip2_outputs\butter_run_003\products")
BSIP1_SOURCE = Path(r"C:\Bari\02_products\butter\bsip1_outputs\butter_bsip1_merged.json")
OUT_PATH     = Path(r"C:\Bari\02_products\butter\butter_frontend_v2.json")

# Image URLs from butter_frontend_v1 (already scraped in BSIP0; carry forward)
# Map barcode → imageUrl
BARCODE_IMAGES: dict[str, str] = {
    "3274932103802": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/TAH44_Z_P_3274932103802_1.png",
    "3274932103857": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/TAH44_Z_P_3274932103857_1.png",
    "3451790562631": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/KCU52_Z_P_3451790562631_1.png",
    "3451790562990": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/KCU52_Z_P_3451790562990_1.png",
    "4823077630057": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/UYK52_Z_P_4823077630057_1.png",
    "4823077643064": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/OER54_Z_P_4823077643064_1.png",
    "7290015039130": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/SVR40_Z_P_7290015039130_1.png",
    "7290019635130": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/FRO54_Z_P_7290019635130_1.png",
    "7290019635147": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/FRO54_Z_P_7290019635147_1.png",
    "7290108503746": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/MCP52_Z_P_7290108503746_1.png",
    "7290108507997": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/MCP52_Z_P_7290108507997_1.png",
    "7290116932033": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/OFY52_Z_P_7290116932033_1.png",
    "7290117263563": "https://res.cloudinary.com/shufersal/image/upload/f_auto,q_auto/v1551800922/prod/product_images/products_zoom/OFY52_Z_P_7290117263563_1.png",
    # Confirmed products from BSIP0 - may not have Shufersal URLs; use null for now
}

# Subtype classification: derived from name analysis during BSIP0
# salted = contains מלוח/מלח; additive_spread = known barcode; cultured = מחמצת/תרבית
# plain = everything else (unsalted)
ADDITIVE_SPREAD_BARCODES = {"7290108507997"}


def classify_subtype(name_he: str, barcode: str, ingredient_list: list) -> str:
    """Classify butter subtype for frontend display."""
    if barcode in ADDITIVE_SPREAD_BARCODES:
        return "additive_spread"
    name_lower = (name_he or "").lower()
    if "מלוח" in name_he or ("מלח" in name_he and "ללא מלח" not in name_he):
        return "salted"
    # Cultured: contains lactic culture
    ingredients_text = " ".join(ingredient_list or []).lower()
    if "מחמצת" in ingredients_text or "תרבית לקטית" in ingredients_text or "תרביות לקטיות" in ingredients_text:
        return "cultured_fermented"
    if "גהי" in name_he or "ghee" in name_lower:
        return "ghee"
    if "מתובל" in name_he:
        return "flavored"
    return "plain"


def build_insight_line(trace: dict, subtype: str) -> str:
    """
    Build the insight line for a butter product.
    Rule: composition fact + category-relevant key signal.
    Owner directive: do NOT moralize saturated fat in the insight line for plain butters.
    """
    l1    = trace.get("L1_observed_signals", {})
    sat   = l1.get("fat_saturated_g")
    fat   = l1.get("fat_g")
    sodium = l1.get("sodium_mg")
    ing_count = l1.get("ingredient_count") or 0
    ingredient_list = l1.get("ingredient_list") or []
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")

    # Additive spread: lead with ingredient complexity
    if subtype == "additive_spread":
        return f"{ing_count} רכיבים — שומן חלב {int(13)}% בלבד"

    # Flavored/spiced
    if subtype == "flavored":
        return "חמאה עם תיבול — מרכיבים נוספים לעומת חמאה בסיסית"

    # Ghee: compositional fact
    if subtype == "ghee":
        if fat:
            return f"שומן חלב {int(fat)}% — ללא מים, ללא קזאין"
        return "חמאה מזוקקת — שומן חלב נטו"

    # Salted: lead with the consumer-relevant tradeoff (sodium is the differentiator vs unsalted)
    if subtype == "salted":
        if sodium and sodium >= 700:
            return f"מלוחה — {int(sodium)} מ\"ג נתרן ל-100 גרם"
        elif sodium:
            return f"מלוחה — {int(sodium)} מ\"ג נתרן ל-100 גרם"
        else:
            return "חמאה מלוחה — תוספת מלח"

    # Cultured fermented: note the culture (it's a real compositional differentiator)
    if subtype == "cultured_fermented":
        if sat:
            return f"שמנת + תרבית לקטית בלבד — {int(sat)} גרם שומן רווי ל-100 גרם"
        return "שמנת ותרבית לקטית — חמאה מחומצת"

    # Plain unsalted: minimal ingredient count is the signal; avoid moralizing sat fat
    if ing_count and ing_count <= 2:
        ing_labels = "/".join(ingredient_list[:2]) if ingredient_list else ""
        count_word = "רכיב" if ing_count == 1 else "רכיבים"
        if ing_labels:
            return f"{ing_count} {count_word}: {ing_labels}"
        return f"{ing_count} {count_word} בלבד"
    elif ing_count and ing_count <= 3:
        return f"{ing_count} רכיבים — הרכב פשוט"

    # Fallback: fat content
    if fat:
        return f"שומן חלב {int(fat)}%"
    return "חמאה טהורה"


def build_row_verdict(trace: dict, subtype: str) -> str:
    """
    Build the row verdict (2-line interpretive standing per row_description_standard_v1 v2).
    Format: standing → why → catch (if any) → earned grade.
    Owner directive: plain butters cluster at 70/B — this is the correct finding, not a problem.
    Do NOT engineer artificial differentiation in the verdict copy.
    """
    l1    = trace.get("L1_observed_signals", {})
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")
    sat   = l1.get("fat_saturated_g")
    fat   = l1.get("fat_g")
    sodium = l1.get("sodium_mg")
    ing_count = l1.get("ingredient_count") or 0
    ingredient_list = l1.get("ingredient_list") or []
    explanation_drivers = trace.get("explanation_drivers") or []
    caps_applied = [c.get("rule") for c in (trace.get("caps_applied") or [])]
    floors_applied = trace.get("floors_applied") or []

    name_he = (trace.get("input_reference") or {}).get("product_name_he", "")

    # Additive spread
    if subtype == "additive_spread":
        return f"ממרח חמאה מועשר במתחלבים ומייצבים. {ing_count} רכיבים — הרבה מעבר לחמאה טהורה. עוצר ב-{grade}/{score} בשל ריבוי תוספים."

    # Flavored
    if subtype == "flavored":
        return f"חמאה עם תיבול — הרכב שונה מחמאה בסיסית. {grade}/{score}."

    # Ghee
    if subtype == "ghee":
        return f"חמאה מזוקקת — שומן חלב נטו, ללא מים וחלבוני חלב. {grade}/{score}."

    # Salted: sodium penalty is the honest differentiator
    if subtype == "salted":
        if sodium and sodium >= 700:
            floor_note = ""
            for fl in floors_applied:
                if fl.get("floor_value") == 50:
                    floor_note = " — רצפת קטגוריה: C/50"
                    break
            return (
                f"חמאה מלוחה: {int(sodium)} מ\"ג נתרן ל-100 גרם. "
                f"תוספת המלח מביאה תווית אדומה על נתרן{floor_note}. עוצרת ב-{grade}/{score}."
            )
        else:
            return f"חמאה מלוחה — מלח כרכיב נוסף. עוצרת ב-{grade}/{score}."

    # Cultured fermented / plain: floor at 70/B is the correct finding
    # Owner directive: "if plain butters cluster at ~70/B, that clustering is the correct finding"
    if subtype == "cultured_fermented":
        ing_desc = f"שמנת ותרבית לקטית" if ing_count <= 2 else f"{ing_count} רכיבים"
        return f"חמאה מחומצת: {ing_desc}. עיבוד מינימלי, הרכב נקי. {grade}/{score}."

    # Plain unsalted
    if ing_count and ing_count <= 2:
        ing_labels = " ו".join(ingredient_list[:2]) if ingredient_list else "שמנת"
        count_word = "רכיב" if ing_count == 1 else "רכיבים"
        return f"חמאה בסיסית: {ing_labels}. מינימום {count_word} — עיבוד נמוך. {grade}/{score}."
    elif ing_count and ing_count <= 3:
        return f"חמאה עם {ing_count} רכיבים עיקריים. עיבוד נמוך. {grade}/{score}."
    else:
        return f"חמאה טהורה. {grade}/{score}."


def build_explanation_text(trace: dict) -> str:
    """
    Build a clean human-readable explanation (no raw rule names per TASK-191 pre-launch flag).
    Use explanation_drivers but translate rule codes to plain language.
    """
    drivers = trace.get("explanation_drivers") or []
    caps    = [c.get("rule") for c in (trace.get("caps_applied") or [])]
    floors  = trace.get("floors_applied") or []
    l1      = trace.get("L1_observed_signals", {})
    sodium  = l1.get("sodium_mg")
    sat     = l1.get("fat_saturated_g")

    parts = []

    # Floor (primary driver for plain butter)
    for fl in floors:
        ftype = fl.get("floor_type", "")
        fval  = fl.get("floor_value")
        if ftype == "whole_food_fat_nova1_2":
            if fval == 70:
                parts.append("מזון שלם: חמאה טהורה מקבלת ציון בסיסי מינימלי של B/70")
            elif fval == 50:
                parts.append("מזון שלם עם עיבוד מועט: ציון בסיסי C/50 בשל נתרן גבוה")

    # Caps (only if they add information beyond floor)
    for cap in caps:
        if cap == "ADDITIVE_MARKERS_3_PLUS":
            parts.append("3 תוספים מזוניים ומעלה — כמו בממרחים מעובדים")
        elif cap == "NOVA_PROXY_3_PROCESSED":
            parts.append("הרכב רכיבים המצביע על עיבוד")
        elif cap == "HIGH_SODIUM_700MG_PLUS" and sodium:
            parts.append(f"נתרן גבוה: {int(sodium)} מ\"ג ל-100 גרם")
        elif cap == "ISRAELI_RED_LABELS_2_PLUS":
            parts.append("2 תוויות אדומות ומעלה על-פי תקינה ישראלית")

    if not parts:
        # Default from explanation_drivers if nothing else
        for d in drivers:
            if "FLOOR APPLIED" in d or "PRIMARY SIGNAL" in d:
                continue  # already handled
            if "DOMINANT" in d and "cap" in d.lower():
                parts.append("כפוף לתקרת ציון בשל הרכב תזונתי")

    return " | ".join(parts) if parts else "חמאה טהורה — ציון בסיסי של קטגוריה"


def confidence_label(band: str) -> str:
    return {
        "high":        "נתונים מלאים",
        "partial":     "נתונים חלקיים",
        "insufficient": "נתונים חלקיים",
    }.get(band, "נתונים חלקיים")


def build_product_vm(trace: dict, bsip1_lookup: dict) -> dict:
    """Build a BariProductVM object from a run_003 trace."""
    inp     = trace.get("input_reference") or {}
    pid     = inp.get("canonical_product_id", "")
    barcode = trace.get("_barcode") or inp.get("barcode", "")
    name_he = inp.get("product_name_he", "")
    brand   = inp.get("brand", "")
    retailers = inp.get("source_retailers") or ["shufersal"]
    retailer  = retailers[0] if retailers else "shufersal"

    score   = trace.get("final_score_estimate")
    grade   = trace.get("grade_estimate")
    conf_band = trace.get("confidence_band", "partial")
    conf_score = trace.get("confidence_score") or 0

    # Map confidence band to VM confidence value
    if conf_band == "high":
        confidence = "verified"
    elif conf_band == "partial" or conf_band == "sufficient":
        confidence = "partial"
    else:
        confidence = "insufficient"

    l1 = trace.get("L1_observed_signals", {})
    ingredient_list = l1.get("ingredient_list") or []

    # Subtype classification
    subtype = classify_subtype(name_he, barcode, ingredient_list)

    # Image URL
    image_url = BARCODE_IMAGES.get(barcode)
    if not image_url:
        # Attempt Shufersal CDN pattern for known barcodes
        bsip1_product = bsip1_lookup.get(barcode, {})
        image_url = bsip1_product.get("image_url") or bsip1_product.get("imageUrl")
        if not image_url and retailer == "shufersal":
            # Shufersal CDN fallback pattern (may 404 for some products)
            image_url = None  # Content Agent will source images at M2

    # Ingredient text for expansion
    ingredient_text = ", ".join(ingredient_list) if ingredient_list else None

    # Insight line + verdict
    insight_line = build_insight_line(trace, subtype)
    row_verdict  = build_row_verdict(trace, subtype)
    explanation  = build_explanation_text(trace)

    # Nutrition panel
    nutrition = {
        "energyKcal":   l1.get("energy_kcal"),
        "protein":      l1.get("protein_g"),
        "sugar":        l1.get("sugars_g"),
        "fat":          l1.get("fat_g"),
        "saturatedFat": l1.get("fat_saturated_g"),
        "fiber":        l1.get("dietary_fiber_g"),
        "sodium":       l1.get("sodium_mg"),
    }

    vm = {
        "id":         pid,
        "name":       name_he,
        "brand":      brand,
        "imageUrl":   image_url,
        "score":      score,
        "grade":      grade,
        "insightLine": insight_line,
        "confidence": confidence,
        "expansion": {
            "nutrition":       nutrition,
            "ingredients":     ingredient_text,
            "confidenceLabel": confidence_label(conf_band),
            "servingNote":     "ל-100 גרם",
            "explanation":     explanation,
        },
        "rowVerdict": row_verdict,
        "barcode":    barcode,
        "retailer":   retailer,
        "subtype":    subtype,
    }

    return vm


def main():
    print(f"[butter_frontend_v2] Reading traces from {BSIP2_DIR}")
    if not BSIP2_DIR.exists():
        print(f"ERROR: BSIP2 dir not found: {BSIP2_DIR}")
        return

    # Load BSIP1 for image URL lookup
    bsip1_lookup: dict[str, dict] = {}
    if BSIP1_SOURCE.exists():
        bsip1_raw = json.loads(BSIP1_SOURCE.read_text(encoding="utf-8"))
        for p in bsip1_raw:
            bc = p.get("barcode", "")
            if bc:
                bsip1_lookup[bc] = p

    # Load all traces
    product_dirs = [d for d in BSIP2_DIR.iterdir() if d.is_dir()]
    print(f"[butter_frontend_v2] Found {len(product_dirs)} product trace directories")

    products = []
    scored   = 0
    errors   = []

    for pd in sorted(product_dirs):
        trace_path = pd / "bsip2_trace.json"
        if not trace_path.exists():
            errors.append(f"Missing trace: {pd.name}")
            continue
        try:
            trace = json.loads(trace_path.read_text(encoding="utf-8"))
            vm = build_product_vm(trace, bsip1_lookup)
            if vm["score"] is not None:
                scored += 1
            products.append(vm)
        except Exception as e:
            errors.append(f"{pd.name}: {e}")
            print(f"  ERROR {pd.name}: {e}")

    # Sort by score descending, then alphabetically
    products.sort(key=lambda p: (-(p["score"] or -1), p["name"] or ""))

    output = {
        "_meta": {
            "generated":     datetime.now(timezone.utc).isoformat(),
            "run_id":        "butter_run_003",
            "task":          "TASK-191",
            "category":      "butter",
            "product_count": len(products),
            "scored_count":  scored,
            "schema":        "BariProductVM[]",
            "version":       "v2",
            "provenance": (
                "butter_run_003 (TASK-191 Phase B final): "
                "EV-047 + EV-048 + EV-050 all active. "
                "39 products, 16 confirmed (label-scanned) + 23 candidate (FDC/OFF enriched). "
                "No 0/E products. TRANS_FAT_VETO suppressed for all whole_food_fat products (no PHVO). "
                "DO NOT DEPLOY without M2 owner approval (Phase C decision)."
            ),
            "deployment_status": "DRAFT — M2 owner approval required before bari-web copy",
            "build_errors":  errors,
        },
        "products": products,
    }

    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n[butter_frontend_v2] Done.")
    print(f"  Products: {len(products)}  Scored: {scored}")
    print(f"  Output: {OUT_PATH}")
    if errors:
        print(f"  Errors ({len(errors)}): {errors}")

    # Grade distribution summary
    from collections import Counter
    grade_dist = Counter(p["grade"] for p in products if p["grade"])
    subtype_dist = Counter(p["subtype"] for p in products)
    print(f"\n  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print(f"  Subtype distribution: {dict(sorted(subtype_dist.items()))}")

    print("\n  Top 5 products:")
    for p in products[:5]:
        print(f"    {p['score']}/{p['grade']}  {p['name']} ({p['brand']})  [{p['subtype']}]")

    return output


if __name__ == "__main__":
    main()
