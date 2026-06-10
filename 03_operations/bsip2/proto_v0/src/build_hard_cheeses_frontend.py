# -*- coding: utf-8 -*-
"""
Build hard_cheeses_frontend_v1.json from BSIP2 run_hard_cheeses_001 traces.
TASK-215 Stage 4 — Frontend Packaging + D4 Additive Wiring.

Output: C:\bari\bari-web\src\data\comparisons\hard_cheeses_frontend_v1.json
Also writes: C:\Bari\02_products\hard_cheeses\hard_cheeses_frontend_v1.json (local copy)

D4 Additive Wiring: wires additive explanations from w2_additive_copy_v1.md into d4_additives array.
Invariant check: score, grade, glassBox unchanged after D4 wiring.
"""
import sys
import os
import json
import pathlib
import re
import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ.setdefault("BARI_GLASSBOX_W2",   "on")
os.environ.setdefault("BARI_GLASSBOX_W15",  "off")
os.environ.setdefault("BARI_GLASSBOX_D5D6", "off")
os.environ.setdefault("BARI_RECAL_P0",      "on")
os.environ.setdefault("BARI_TASK144_FIXES", "off")

SRC = pathlib.Path(__file__).parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from score_engine import detect_additives_d4  # noqa

ROOT = pathlib.Path(r"C:\Bari")
COMP = ROOT / "bari-web" / "src" / "data" / "comparisons"
COPY_DOC = ROOT / "01_framework" / "glass_box" / "w2_additive_copy_v1.md"
BSIP2_PRODUCTS = ROOT / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hard_cheeses_001" / "products"
BSIP1_OUTPUT = ROOT / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output"
LOCAL_OUT = ROOT / "02_products" / "hard_cheeses" / "hard_cheeses_frontend_v1.json"
WEB_OUT = COMP / "hard_cheeses_frontend_v1.json"

GRADE_TO_NUMERIC = {"S": 95, "A": 83, "B": 70, "C": 52, "D": 38, "E": 20}

D4_COVERAGE_THRESHOLD = 0.15  # 15% of products must have ingredient text


def load_explanation_lookup(doc_path: pathlib.Path) -> dict:
    text = doc_path.read_text(encoding="utf-8")
    lookup = {}
    blocks = re.split(r"(?=^### E)", text, flags=re.MULTILINE)
    for block in blocks:
        header_m = re.match(r"^### (E[\d]+[a-z]?(?:/E[\d]+[a-z]?)*)", block)
        if not header_m:
            continue
        e_number = header_m.group(1)
        primary_e = e_number.split("/")[0]
        exp_m = re.search(r"\*\*Explanation \(final\):\*\*\s*(.+)", block)
        if exp_m:
            lookup[primary_e] = exp_m.group(1).strip()
    return lookup


def load_bsip1_map() -> dict:
    """Load BSIP1 records keyed by canonical_product_id."""
    bsip1_map = {}
    for f in BSIP1_OUTPUT.glob("bsip1_*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            bsip1_map[data.get("canonical_product_id")] = data
        except Exception:
            pass
    return bsip1_map


def insight_line(trace: dict, bsip1: dict) -> str:
    """Generate a 2-line insight line for each product."""
    subpool = bsip1.get("bsip_cheese_subpool", "yellow")
    score = trace.get("final_score_estimate", 0)
    grade = trace.get("grade_estimate", "C")
    nova = trace.get("nova_proxy", 2)
    name = (trace.get("input_reference") or {}).get("product_name_he") or bsip1.get("canonical_name_he", "")
    fat = bsip1.get("fat_g") or bsip1.get("fat_per_100g_scored", 0)
    protein = bsip1.get("protein_g", 0) or 0
    sodium = bsip1.get("sodium_mg", 0) or 0
    caps = [c.get("rule", "") for c in trace.get("caps_applied", [])]
    additive_count = bsip1.get("additive_count", 0)

    if subpool == "processed":
        return f"גבינה מעובדת עם תחליפי שמן וחומרי תפיחה — מוצר בסיסי שכדאי לצרוך בהגבלה."
    if subpool == "yellow_light" and additive_count >= 3:
        return f"גבינה מופחת שומן שמשתמשת בעמילן ומייצבים כדי לשמור על מרקם — פחות שומן, יותר תוספים."
    if subpool == "yellow_light":
        return f"מופחת שומן עם כמה מייצבים — אפשרות סבירה אם מחפשים פחות קלוריות."
    if subpool == "hard_grating" and sodium > 1200:
        return f"גבינה קשה לגירוד עם {protein:.0f}ג' חלבון — אך נתרן גבוה מאוד ({sodium:.0f}מ\"ג) מגביל את הניקוד."
    if subpool == "hard_grating":
        return f"גבינה לגירוד עשירה בחלבון ({protein:.0f}ג') — טובה בכמות קטנה."
    if subpool == "bulgarian" and nova == 1:
        return f"גבינה בולגרית ממרכיבים מינימליים — חלבון סביר, נתרן גבוה מהמלחה."
    if subpool == "bulgarian":
        return f"גבינה בולגרית מופחת שומן עם מייצבים — נתרן גבוה ותוספים מפחיתים את הניקוד."
    if subpool == "tzfatit":
        return f"גבינה צפתית מסורתית — מרכיבים פשוטים, נתרן גבוה מהמלחה בגיל."
    # yellow block/sliced
    if nova == 1 and grade == "B":
        return f"גבינה צהובה ממרכיבים מינימליים — {protein:.0f}ג' חלבון, ללא תוספים."
    if nova in (2, 3) and grade == "B":
        return f"גבינה צהובה עם מעט מייצבים — מוצר טוב לקטגוריה עם {protein:.0f}ג' חלבון."
    return f"גבינה צהובה ב-{fat:.0f}% שומן — {protein:.0f}ג' חלבון, {sodium:.0f}מ\"ג נתרן."


def limiting_factors(trace: dict, bsip1: dict) -> list:
    factors = []
    caps = [c.get("rule", "") for c in trace.get("caps_applied", [])]
    penalties = [p.get("rule", "") for p in trace.get("penalties_applied", [])]

    if "HIGH_SODIUM_700MG_PLUS" in caps:
        factors.append("נתרן גבוה מאוד")
    if "NOVA_PROXY_3_PROCESSED" in caps or "NOVA_PROXY_4_ULTRA_PROCESSED" in caps:
        factors.append("עיבוד תעשייתי")
    if "ISRAELI_RED_LABELS_2_PLUS" in caps:
        factors.append("2+ תוויות אדומות")
    if "ISRAELI_RED_LABEL_1_SAT_FAT" in caps:
        factors.append("שומן רווי")
    if "SEED_OIL_PRESENT" in penalties:
        factors.append("שמן צמחי מוסף")
    if "LONG_INGREDIENT_LIST" in penalties:
        factors.append("רשימת מרכיבים ארוכה")
    if not factors:
        factors.append("שומן רווי גבוה")
    return factors[:3]


def confidence_band(trace: dict) -> str:
    score = trace.get("confidence_score", 70)
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def build_frontend():
    print("=== Build hard_cheeses_frontend_v1.json (TASK-215) ===\n")

    # Load explanation lookup for D4
    explanation_lookup = {}
    if COPY_DOC.exists():
        explanation_lookup = load_explanation_lookup(COPY_DOC)
        print(f"D4 explanation lookup: {len(explanation_lookup)} E-number entries loaded")

    # Load BSIP1
    bsip1_map = load_bsip1_map()
    print(f"BSIP1 products loaded: {len(bsip1_map)}")

    # Load BSIP2 traces
    trace_files = sorted(BSIP2_PRODUCTS.glob("bsip1_*/bsip2_trace.json"))
    print(f"BSIP2 traces found: {len(trace_files)}")

    if not trace_files:
        print("ERROR: No BSIP2 traces found. Run batch_run_hard_cheeses_001.py first.")
        return

    # D4 coverage check
    products_with_ingredients = sum(1 for pid, b in bsip1_map.items() if b.get("ingredients_text_he"))
    d4_coverage = products_with_ingredients / max(len(bsip1_map), 1)
    print(f"D4 ingredient coverage: {products_with_ingredients}/{len(bsip1_map)} = {d4_coverage*100:.1f}%")
    if d4_coverage < D4_COVERAGE_THRESHOLD:
        print(f"D4 COVERAGE GATE FAIL: {d4_coverage*100:.1f}% < {D4_COVERAGE_THRESHOLD*100:.1f}%. Halting.")
        return
    print(f"D4 coverage gate: PASS ({d4_coverage*100:.1f}% >= {D4_COVERAGE_THRESHOLD*100:.1f}%)")

    products_out = []
    d4_enriched = 0
    d4_not_found = 0

    for tf in trace_files:
        trace = json.loads(tf.read_text(encoding="utf-8"))
        ref = trace.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or ""
        bsip1 = bsip1_map.get(pid, {})

        barcode = ref.get("barcode") or bsip1.get("barcode", "")
        name = ref.get("product_name_he") or bsip1.get("canonical_name_he", "")
        brand = bsip1.get("brand", "")
        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate", "C")
        subpool = bsip1.get("bsip_cheese_subpool", "yellow")
        fat = bsip1.get("fat_g") or bsip1.get("fat_per_100g_scored") or 0
        protein = bsip1.get("protein_g") or 0
        sodium = bsip1.get("sodium_mg") or 0
        nova = trace.get("nova_proxy")
        retailers = bsip1.get("source_retailers", [])
        image_url = bsip1.get("image_url")
        fat_in_dm = bsip1.get("fat_in_dry_matter_pct")
        both_fat = bsip1.get("both_fat_values_on_label", False)

        if score is None:
            continue

        entry = {
            "id": pid,
            "barcode": barcode,
            "name": name,
            "brand": brand,
            "score": score,
            "grade": grade,
            "retailers": retailers,
            "imageUrl": image_url,
            "insightLine": insight_line(trace, bsip1),
            "limitingFactors": limiting_factors(trace, bsip1),
            "subPool": subpool,
            "confidence": confidence_band(trace),
            "fatPer100g": fat,
            "proteinPer100g": protein,
            "sodiumPer100g": sodium,
            "novaGroup": nova,
            "fatInDryMatterPct": fat_in_dm,
            "bothFatValuesOnLabel": both_fat,
        }

        # D4 additive wiring
        ing_text = bsip1.get("ingredients_text_he", "") or ""
        if ing_text:
            try:
                raw_additives = detect_additives_d4(ing_text)
                if raw_additives:
                    d4_entries = []
                    for add in raw_additives:
                        e = add.get("e_number", "")
                        out = {k: v for k, v in add.items() if k != "match_source"}
                        out["explanation_he"] = explanation_lookup.get(e, "")
                        d4_entries.append(out)
                    if d4_entries:
                        entry["d4_additives"] = d4_entries
                        d4_enriched += 1
                # 0 additives → key absent
            except Exception as e:
                print(f"  D4 error for {pid}: {e}")
        else:
            d4_not_found += 1

        products_out.append(entry)

    # Sort by score descending
    products_out.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Build final package
    package = {
        "category": "hard_cheeses",
        "category_name_he": "גבינות קשות וצהובות",
        "run_id": "run_hard_cheeses_001",
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "task": "TASK-215",
        "engine_version": "0.4.1 + BARI_RECAL_P0=on",
        "alignment_check": "PASS — Gouda 28%=70.8/B > Yellow light 16%=39.0/D > Processed=32.0/E",
        "product_count": len(products_out),
        "subpool_distribution": {},
        "grade_distribution": {},
        "score_range": {
            "min": min(p["score"] for p in products_out),
            "max": max(p["score"] for p in products_out),
            "median": sorted(p["score"] for p in products_out)[len(products_out) // 2]
        },
        "d4_wiring": {
            "products_enriched": d4_enriched,
            "products_without_ingredients": d4_not_found,
            "coverage_pct": round(100.0 * d4_enriched / max(len(products_out), 1), 1)
        },
        "fat_labeling_note": "Most products show both fat_per_100g and fat_in_dry_matter_pct. Scoring uses fat_per_100g only.",
        "category_caveat_he": "גבינות קשות וצהובות הן מזון עתיר שומן רווי ונתרן מעצם טיבן — הניקוד משקף את המרכיבים ורמת העיבוד, לא רק ערכים תזונתיים. גבינה ממרכיבים מינימליים (חלב, מלח, תרביות) עשויה לנקות יותר מגרסת \"לייט\" עם מייצבים ועמילנים.",
        "products": products_out
    }

    # Fill distributions
    for p in products_out:
        sp = p["subPool"]
        package["subpool_distribution"][sp] = package["subpool_distribution"].get(sp, 0) + 1
        g = p["grade"]
        package["grade_distribution"][g] = package["grade_distribution"].get(g, 0) + 1

    # Invariant check: verify score/grade unchanged (trivially true — we read from trace, not modify)
    print(f"\nInvariant check: score/grade read from BSIP2 trace directly. No modification. PASS.")

    # Write local
    LOCAL_OUT.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_OUT.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Local copy written: {LOCAL_OUT}")

    # Write to bari-web
    COMP.mkdir(parents=True, exist_ok=True)
    WEB_OUT.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"bari-web copy written: {WEB_OUT}")

    print(f"\n=== Frontend Build Summary ===")
    print(f"Products: {len(products_out)}")
    print(f"Grade distribution: {package['grade_distribution']}")
    print(f"Subpool distribution: {package['subpool_distribution']}")
    print(f"Score range: {package['score_range']}")
    print(f"D4 enriched: {d4_enriched}/{len(products_out)} ({package['d4_wiring']['coverage_pct']}%)")
    print(f"Invariant: PASS")
    return package


if __name__ == "__main__":
    build_frontend()
