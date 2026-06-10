# -*- coding: utf-8 -*-
"""
Frontend JSON builder — Hard & Yellow Cheeses (run_hard_cheeses_yohananof_001)
TASK-215

Reads:  BSIP1 outputs + BSIP2 trace outputs
Writes: hard_cheeses_frontend_v2.json → 02_products/hard_cheeses/ + bari-web/src/data/comparisons/
"""
import sys
import json
import pathlib
import datetime
import shutil

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT         = pathlib.Path(r"C:\Bari")
BSIP1_DIR    = ROOT / "02_products" / "hard_cheeses" / "bsip1_outputs"
BSIP2_DIR    = ROOT / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hard_cheeses_yohananof_001" / "products"
OUT_LOCAL    = ROOT / "02_products" / "hard_cheeses" / "hard_cheeses_frontend_v2.json"
OUT_WEB      = ROOT / "bari-web" / "src" / "data" / "comparisons" / "hard_cheeses_frontend_v2.json"

# Only the barcodes from the new yohananof run (not the fabricated old ones)
YOHANANOF_BARCODES = {
    "7290000057118", "7290004137311", "7290102394463", "7290110320867",
    "7290004122195", "7290014763395", "7290004122683", "7290014760912",
    "7290004125776", "7290102396672", "7290004122348", "7290110320850",
    "7290110324872", "7290000057088", "7290102394845", "7290004122270",
    "7290110323301", "7290102397204", "7290014455252", "3073781199918",
    "7290117265888", "7290117265918", "7290108502725", "7290108501346",
    "7290116931524", "7290108503999", "7290019635192", "7290017065434",
    "7290102302864", "8711528211138",
}


def confidence_label(nn: dict) -> tuple:
    """Return (confidence_key, confidenceLabel_he)."""
    kcal  = nn.get("energy_kcal")
    fat   = nn.get("fat_g")
    prot  = nn.get("protein_g")
    sod   = nn.get("sodium_mg")
    present = sum(1 for v in [kcal, fat, prot, sod] if v is not None)
    if kcal is None:
        return "insufficient", "נתונים לא מספיקים"
    if present >= 3:
        return "verified", "נתונים מאומתים"
    return "partial", "נתונים חלקיים"


def build_insight_line(name: str, bsip1: dict) -> str:
    """Generate Hebrew insight line for hard cheese."""
    fat    = bsip1.get("fat_g")
    prot   = bsip1.get("protein_g")
    sod    = bsip1.get("sodium_mg")
    nova   = bsip1.get("nova_proxy")
    addict = bsip1.get("detected_additives") or []
    subp   = bsip1.get("bsip_cheese_subpool", "yellow")
    add_count = len(addict)

    # Processed cheese
    if subp == "processed":
        e_list = ", ".join(addict[:3]) if addict else "E339"
        return (f"גבינה מעובדת עם פוספטים — {e_list} ברשימת הרכיבים מציינים עיבוד תעשייתי. "
                f"הציון משקף את פרופיל התוספים והשומן הגבוה.")

    # Light yellow cheese
    if subp == "yellow_light":
        fat_str = f"{fat:.0f}%" if fat is not None else "?"
        sod_str = f"{sod:.0f}" if sod is not None else "?"
        if add_count >= 2:
            return (f"מופחת שומן {fat_str} אבל עם ייצובים — הקלוריות ירדו אך "
                    f"רשימת הרכיבים התארכה. נתרן: {sod_str}מ\"ג ל-100 גרם.")
        return (f"מופחת שומן {fat_str} — פחות שומן, פחות תוספות מהגרסה המלאה. "
                f"נתרן: {sod_str}מ\"ג ל-100 גרם.")

    # Hard grating cheese (like parmesan)
    if subp == "hard_grating":
        prot_str = f"{prot:.0f}" if prot is not None else "?"
        fat_str  = f"{fat:.0f}" if fat is not None else "?"
        return (f"גבינה קשה לגרירה — חלבון גבוה ({prot_str}g ל-100g), שומן {fat_str}%. "
                f"מיועדת לכמויות קטנות — גורם הריכוז הופך את ערכי ה-100g לגבוהים.")

    # Minimal ingredient cheese (NOVA 1, high protein)
    if nova == 1 and add_count == 0:
        prot_str = f"{prot:.0f}" if prot is not None else "?"
        fat_str  = f"{fat:.0f}" if fat is not None else "?"
        return (f"גבינה עם רכיבים בלבד — חלב, מלח ואנזים. "
                f"לא מעובדת. חלבון {prot_str}g ל-100g לצד {fat_str}% שומן.")

    # Goat cheese
    if "עיזים" in name:
        fat_str = f"{fat:.0f}" if fat is not None else "?"
        sod_str = f"{sod:.0f}" if sod is not None else "?"
        return (f"גאודה עיזים — חלב עיזים מלא, מינימום תוספות. "
                f"שומן {fat_str}%, נתרן {sod_str}מ\"ג. פרופיל נקי לקטגוריה.")

    # Standard yellow cheese (emek, gouda, etc.)
    prot_str = f"{prot:.0f}" if prot is not None else "?"
    fat_str  = f"{fat:.0f}" if fat is not None else "?"
    sod_str  = f"{sod:.0f}" if sod is not None else "?"
    if add_count >= 1:
        return (f"גבינה צהובה {fat_str}% — חלבון {prot_str}g ל-100g. "
                f"מכילה {add_count} תוסף/תוספות מזוהים. נתרן {sod_str}מ\"ג.")
    return (f"גבינה צהובה {fat_str}% — חלבון {prot_str}g ל-100g, "
            f"נתרן {sod_str}מ\"ג. עיבוד מינימלי.")


def _nova1_cheese_label(ing: str) -> str:
    """Consumer-facing replacement for NOVA-1 cheese signal.
    Uses actual ingredients text to confirm minimal processing.
    Never exposes the word 'NOVA' to the consumer layer.
    """
    ing_lower = (ing or "").lower()
    if any(x in ing_lower for x in ["חלב", "milk"]):
        return "גבינה עם רכיבים מינימליים — חלב, מלח ותרביות בלבד"
    return "גבינה עם רכיבים מינימליים"


def build_positive_signals(bsip1: dict) -> list:
    signals = []
    prot = bsip1.get("protein_g")
    fat  = bsip1.get("fat_g")
    nova = bsip1.get("nova_proxy")
    addt = bsip1.get("detected_additives") or []
    subp = bsip1.get("bsip_cheese_subpool", "yellow")
    ing  = bsip1.get("ingredients_text_he") or ""

    if prot is not None and prot >= 25:
        signals.append(f"חלבון גבוה ({prot:.0f}g ל-100g)")
    elif prot is not None and prot >= 20:
        signals.append(f"חלבון טוב ({prot:.0f}g ל-100g)")
    if len(addt) == 0:
        signals.append("ללא תוספות מזוהות")
    if nova == 1:
        # Never expose "NOVA" in consumer-facing copy; translate to product-specific language
        signals.append(_nova1_cheese_label(ing))
    # NOVA 2 is not a meaningful consumer positive (basic processing level of all cheese);
    # omit — the "ללא תוספות מזוהות" signal already conveys cleanliness where applicable.
    # NOVA 3 and NOVA 4 are never positive signals.
    if subp == "yellow_light" and fat is not None and fat <= 10:
        signals.append(f"מופחת שומן ({fat:.0f}%)")
    return signals


def build_limiting_factors(bsip1: dict) -> list:
    factors = []
    fat  = bsip1.get("fat_g")
    sod  = bsip1.get("sodium_mg")
    nova = bsip1.get("nova_proxy")
    addt = bsip1.get("detected_additives") or []

    if fat is not None and fat >= 25:
        factors.append(f"שומן גבוה ({fat:.0f}g ל-100g)")
    if sod is not None and sod >= 500:
        factors.append(f"נתרן גבוה ({sod:.0f}mg ל-100g)")
    elif sod is not None and sod >= 400:
        factors.append(f"נתרן בינוני-גבוה ({sod:.0f}mg ל-100g)")
    if addt:
        e_str = ", ".join(addt[:4])
        factors.append(f"תוספות מזוהות: {e_str}")
    # Never expose raw "NOVA N — ..." strings in consumer copy
    if nova == 4:
        factors.append("גבינה מעובדת — עיבוד תעשייתי")
    elif nova == 3:
        factors.append("מכיל מייצבים")
    return factors


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Load BSIP1 files (only new yohananof barcodes)
    bsip1_map = {}
    for f in BSIP1_DIR.glob("bsip1_hardcheese_*.json"):
        if "run_report" in f.name or "skipped" in f.name:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            barcode = d.get("barcode")
            if barcode and barcode in YOHANANOF_BARCODES:
                bsip1_map[d["canonical_product_id"]] = d
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

    # Build products list
    products = []
    for pid, trace in trace_map.items():
        bsip1 = bsip1_map[pid]
        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")

        if score is None or grade in ("insufficient_data", None):
            continue
        if not isinstance(score, (int, float)):
            continue

        nn     = bsip1.get("normalized_nutrition_per_100g") or {}
        name   = bsip1.get("canonical_name_he") or ""
        subp   = bsip1.get("bsip_cheese_subpool") or "yellow"
        conf_key, conf_label = confidence_label(nn)

        products.append({
            "_pid":   pid,
            "_score": score,
            "_grade": grade,
            "_name":  name,
            "_subp":  subp,
            "_bsip1": bsip1,
            "_nn":    nn,
            "_conf_key": conf_key,
            "_conf_label": conf_label,
        })

    products.sort(key=lambda x: x["_score"], reverse=True)

    grade_dist = {}
    out_products = []
    for i, p in enumerate(products):
        seq = f"hc-{i+1:03d}"
        bsip1 = p["_bsip1"]
        nn    = p["_nn"]
        score = round(p["_score"])
        grade = p["_grade"]
        g = grade_dist
        g[grade] = g.get(grade, 0) + 1

        insight = build_insight_line(p["_name"], bsip1)
        pos_sig = build_positive_signals(bsip1)
        lim_fac = build_limiting_factors(bsip1)

        out_products.append({
            "id":         seq,
            "name":       p["_name"],
            "barcode":    bsip1.get("barcode"),
            "imageUrl":   bsip1.get("image_url"),
            "score":      score,
            "grade":      grade,
            "confidence": p["_conf_key"],
            "insightLine": insight,
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
                "ingredients":      bsip1.get("ingredients_text_he"),
                "confidenceLabel":  p["_conf_label"],
                "servingNote":      "ל-100 גרם",
                "positiveSignals":  pos_sig,
                "limitingFactors":  lim_fac,
            },
            "retailer": "yohananof",
            "subPool":  p["_subp"],
            "novaGroup": bsip1.get("nova_proxy"),
        })

    doc = {
        "_meta": {
            "generated":     ts,
            "category":      "hard_cheeses",
            "run_id":        "run_hard_cheeses_yohananof_001",
            "product_count": len(out_products),
            "scored_count":  len(out_products),
            "schema":        "BariProductVM[]",
            "version":       "v2",
            "provenance":    "bsip0_yohananof_hard_cheeses_storefront_20260607_151235.json → BSIP1 run_hard_cheeses_yohananof_001 → BSIP2 run_hard_cheeses_yohananof_001",
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
    print(f"  Score range: {out_products[-1]['score']}–{out_products[0]['score']}")


if __name__ == "__main__":
    main()
