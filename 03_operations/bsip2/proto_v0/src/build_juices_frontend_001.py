# -*- coding: utf-8 -*-
"""
Frontend JSON builder — Juices & Fruit Drinks (run_juices_yohananof_001)
TASK-214

Reads:  BSIP1 outputs + BSIP2 trace outputs
Writes: juices_frontend_v2.json → 02_products/juices/ + bari-web/src/data/comparisons/
"""
import sys
import json
import pathlib
import datetime
import shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT       = pathlib.Path(r"C:\Bari")
BSIP1_DIR  = ROOT / "02_products" / "juices" / "bsip1_outputs"
BSIP2_DIR  = ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_juices_yohananof_001" / "products"
OUT_LOCAL  = ROOT / "02_products" / "juices" / "juices_frontend_v2.json"
OUT_WEB    = ROOT / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v2.json"


def confidence_label(nn: dict) -> tuple:
    kcal   = nn.get("energy_kcal")
    carbs  = nn.get("carbohydrates_g")
    sugar  = nn.get("sugars_g")
    fat    = nn.get("fat_g")
    present = sum(1 for v in [kcal, carbs, sugar] if v is not None)
    if kcal is None:
        return "insufficient", "נתונים לא מספיקים"
    if present >= 3:
        return "verified", "נתונים מאומתים"
    return "partial", "נתונים חלקיים"


def build_insight_line(name: str, bsip1: dict) -> str:
    """Generate Hebrew insight line for juice/beverage."""
    sugar  = bsip1.get("sugars_g")
    kcal   = bsip1.get("energy_kcal")
    nova   = bsip1.get("nova_proxy")
    subp   = bsip1.get("juice_subpool", "fruit_drink")
    addt   = bsip1.get("detected_additives") or []
    ing    = bsip1.get("ingredients_text_he") or ""
    add_ct = len(addt)

    sugar_str = f"{sugar:.1f}" if sugar is not None else "?"
    kcal_str  = f"{kcal:.0f}" if kcal is not None else "?"

    # 100% juice — lead with honest sugar reality
    if subp == "juice_100":
        # Fresh-squeezed or cold-pressed
        if nova == 1 or ("סחוט" in name or "טרי" in name):
            return (f"מיץ סחוט טרי — {kcal_str} קלוריות ל-100 מ\"ל. "
                    f"סוכר {sugar_str}g — כולו מהפרי. ללא ריכוז, ללא תוספות.")
        # Reconstituted 100%
        if add_ct == 0:
            return (f"מיץ 100% ללא תוספות — {kcal_str} קלוריות ל-100 מ\"ל. "
                    f"סוכר {sugar_str}g — כולו מהפרי. עשוי מרכז.")
        return (f"מיץ 100% — סוכר {sugar_str}g ל-100 מ\"ל. "
                f"מכיל {add_ct} חומרים משמרים/חומציות. כולו מהפרי, ללא סוכר מוסף.")

    # Nectar — lead with fruit content and added sugar signal
    if subp == "nectar":
        has_added_sugar = "סוכר לבן" in ing
        sug_note = "עם סוכר מוסף" if has_added_sugar else "ללא סוכר מוסף מפורש"
        return (f"נקטר — מחית פרי + {sug_note}. "
                f"סוכר {sugar_str}g ל-100 מ\"ל ({kcal_str} קלוריות). "
                f"אחוז פרי נמוך מ-100%.")

    # Fruit drink — lead with sugar and low fruit content, be direct
    # Spring grape — special case
    if "ספרינג ענבים" in name:
        return ("ספרינג ענבים — 5.6% תפוח + 3.5% ענבים בקבוק. "
                "השאר: מים, סוכר לבן, ומגוון חומרים. "
                f"סיווג: משקה פירות, לא מיץ. סוכר {sugar_str}g ל-100 מ\"ל.")

    # Tapuzina
    if "תפוזינה" in name:
        return (f"תפוזינה — משקה פירות עם מחזקי טעם וצבע מאכל. "
                f"סוכר {sugar_str}g ל-100 מ\"ל, {kcal_str} קלוריות.")

    # Crystal
    if "קריסטל" in name:
        return (f"קריסטל — משקה פירות: מים, סוכר לבן, 2–6% פרי. "
                f"סוכר {sugar_str}g ל-100 מ\"ל. מכיל ממתיקים מלאכותיים.")

    # Jump
    if "ג'אמפ" in name:
        return (f"ג'אמפ ענבים — 10% פרי או יותר, סוכר מוסף, "
                f"צבע קרמל ותוספות. סוכר {sugar_str}g ל-100 מ\"ל.")

    # Cranberry drinks
    if "חמוציות" in name:
        has_added_sugar = "סוכר" in ing
        sug_note = f"עם סוכר מוסף. סוכר {sugar_str}g ל-100 מ\"ל." if has_added_sugar else f"ללא סוכר מוסף. סוכר {sugar_str}g."
        return f"מיץ חמוציות — 25% פרי מרכז. {sug_note}"

    # Lemonade/citrus fruit drink
    if "לימונענע" in name:
        return (f"לימונענע — מים, סוכר, 6% לימון מרכז. "
                f"סוכר {sugar_str}g ל-100 מ\"ל. חומרי טעם וריח.")

    # Generic fruit drink
    return (f"משקה פירות — סוכר {sugar_str}g ל-100 מ\"ל ({kcal_str} קלוריות). "
            f"מכיל {add_ct} תוספות מזוהות.")


def build_positive_signals(bsip1: dict) -> list:
    signals = []
    sugar  = bsip1.get("sugars_g")
    nova   = bsip1.get("nova_proxy")
    subp   = bsip1.get("juice_subpool", "fruit_drink")
    addt   = bsip1.get("detected_additives") or []
    ing    = bsip1.get("ingredients_text_he") or ""

    if subp == "juice_100":
        signals.append("100% פרי ללא תוספות" if len(addt) == 0 else "100% פרי")
    has_added_sugar = "סוכר לבן" in ing or ("סוכר" in ing and subp != "juice_100")
    if not has_added_sugar:
        signals.append("ללא סוכר מוסף זוהה")
    if sugar is not None and sugar < 8:
        signals.append(f"סוכר נמוך ({sugar:.1f}g ל-100מ\"ל)")
    if nova == 1:
        signals.append("NOVA 1 — מיץ סחוט טרי")
    return signals


def build_limiting_factors(bsip1: dict) -> list:
    factors = []
    sugar  = bsip1.get("sugars_g")
    nova   = bsip1.get("nova_proxy")
    subp   = bsip1.get("juice_subpool", "fruit_drink")
    addt   = bsip1.get("detected_additives") or []
    ing    = bsip1.get("ingredients_text_he") or ""

    if sugar is not None and sugar > 10:
        factors.append(f"סוכר גבוה ({sugar:.1f}g ל-100מ\"ל)")
    elif sugar is not None and sugar > 6:
        factors.append(f"סוכר בינוני ({sugar:.1f}g ל-100מ\"ל)")

    if subp == "fruit_drink":
        factors.append("תוכן פרי נמוך (<25%)")

    has_added_sugar = "סוכר לבן" in ing
    if has_added_sugar:
        factors.append("סוכר מוסף")

    if nova == 4:
        factors.append("NOVA 4 — משקה מעובד")
    elif nova == 3 and subp != "juice_100":
        factors.append("NOVA 3 — מעובד/מרוכז")

    if addt:
        has_color_flavor = any(re.search(r"E1[0-9]{2}|E6[0-9]{2}|E4[0-9]{2}", a, re.I) for a in addt)
        if has_color_flavor or len(addt) >= 3:
            factors.append(f"תוספות צבע/טעם ({', '.join(addt[:3])})")

    return factors


import re


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Load BSIP1 files
    bsip1_map = {}
    for f in BSIP1_DIR.glob("bsip1_juice_*.json"):
        if "run_report" in f.name or "skipped" in f.name:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            pid = d.get("canonical_product_id")
            if pid:
                bsip1_map[pid] = d
        except Exception:
            pass

    print(f"BSIP1 loaded: {len(bsip1_map)}")

    # Load BSIP2 traces
    trace_map = {}
    for trace_path in BSIP2_DIR.glob("*/bsip2_trace.json"):
        pid = trace_path.parent.name
        try:
            t = json.loads(trace_path.read_text(encoding="utf-8"))
            if pid in bsip1_map:
                trace_map[pid] = t
        except Exception:
            pass

    print(f"BSIP2 traces matched: {len(trace_map)}")

    # Build products
    products = []
    for pid, trace in trace_map.items():
        bsip1 = bsip1_map[pid]
        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")

        if score is None or grade in ("insufficient_data", None):
            continue

        nn     = bsip1.get("normalized_nutrition_per_100g") or {}
        name   = bsip1.get("canonical_name_he") or ""
        subp   = bsip1.get("juice_subpool") or "fruit_drink"
        conf_key, conf_label = confidence_label(nn)

        products.append({
            "_pid":        pid,
            "_score":      score,
            "_grade":      grade,
            "_name":       name,
            "_subp":       subp,
            "_bsip1":      bsip1,
            "_nn":         nn,
            "_conf_key":   conf_key,
            "_conf_label": conf_label,
        })

    products.sort(key=lambda x: x["_score"], reverse=True)

    grade_dist   = {}
    out_products = []
    for i, p in enumerate(products):
        seq   = f"jc-{i+1:03d}"
        bsip1 = p["_bsip1"]
        nn    = p["_nn"]
        score = round(p["_score"])
        grade = p["_grade"]
        grade_dist[grade] = grade_dist.get(grade, 0) + 1

        insight = build_insight_line(p["_name"], bsip1)
        pos_sig = build_positive_signals(bsip1)
        lim_fac = build_limiting_factors(bsip1)

        out_products.append({
            "id":           seq,
            "name":         p["_name"],
            "imageUrl":     bsip1.get("image_url"),
            "score":        score,
            "grade":        grade,
            "confidence":   p["_conf_key"],
            "insightLine":  insight,
            "expansion": {
                "nutrition": {
                    "energyKcal": nn.get("energy_kcal"),
                    "protein":    nn.get("protein_g"),
                    "sugar":      nn.get("sugars_g"),
                    "fat":        nn.get("fat_g"),
                    "satFat":     nn.get("fat_saturated_g"),
                    "fiber":      nn.get("dietary_fiber_g"),
                    "sodium":     nn.get("sodium_mg"),
                },
                "ingredients":     bsip1.get("ingredients_text_he"),
                "confidenceLabel": p["_conf_label"],
                "servingNote":     "ל-100 מ\"ל",
                "positiveSignals": pos_sig,
                "limitingFactors": lim_fac,
            },
            "retailer": "yohananof",
            "subPool":  p["_subp"],
            "novaGroup": bsip1.get("nova_proxy"),
        })

    doc = {
        "_meta": {
            "generated":      ts,
            "category":       "juices",
            "run_id":         "run_juices_yohananof_001",
            "product_count":  len(out_products),
            "scored_count":   len(out_products),
            "schema":         "BariProductVM[]",
            "version":        "v2",
            "provenance":     "bsip0_yohananof_juices_storefront_20260607_151232.json → BSIP1 run_juices_yohananof_001 → BSIP2 run_juices_yohananof_001",
            "grade_distribution": grade_dist,
        },
        "products": out_products,
    }

    OUT_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    OUT_LOCAL.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_LOCAL}")

    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_LOCAL, OUT_WEB)
    print(f"Copied to: {OUT_WEB}")

    print(f"\nFrontend summary:")
    print(f"  Products: {len(out_products)}")
    print(f"  Grade distribution: {grade_dist}")
    scores = [p["_score"] for p in products]
    if scores:
        print(f"  Score range: {min(scores):.1f}–{max(scores):.1f}")


if __name__ == "__main__":
    main()
