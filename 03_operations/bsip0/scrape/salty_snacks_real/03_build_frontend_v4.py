"""
Build salty_snacks_frontend_v4.json from BSIP2 run_salty_snacks_002 traces (REAL rebuild).
TASK-228. Real EAN + real Yochananof image + OFF panel. Engine unchanged (TASK-216 extrusion
signal retained). Editorial content is DERIVED FROM THE REAL TRACE (signals/caps/penalties),
not authored from fabricated nutrition.

Keeps v3 editorial shape: insightLine (2-line verdict), expansion.{nutrition(sodium+fiber),
ingredients, confidenceLabel, servingNote, positiveSignals, limitingFactors, bottomLine,
comparisonContext}, confidence fields.
"""
import sys, json, pathlib, datetime
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TRACES_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUT_LOCAL  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\salty_snacks_frontend_v4.json")
OUT_WEB    = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\salty_snacks_frontend_v4.json")


def grade_from_score(s):
    if s is None: return "?"
    if s >= 80: return "A"
    if s >= 65: return "B"
    if s >= 50: return "C"
    if s >= 35: return "D"
    return "E"


def retailer_he(r): return {"yochananof": "יוחננוף", "shufersal": "שופרסל", "carrefour": "קרפור"}.get(r, r)


def load_bsip1():
    by = {}
    for f in BSIP1_DIR.glob("bsip1_snack_*.json"):
        d = json.loads(f.read_text("utf-8"))
        by[d["canonical_product_id"]] = d
    return by


def load_traces():
    out = []
    for pd in TRACES_DIR.iterdir():
        tp = pd / "bsip2_trace.json"
        if tp.exists():
            out.append(json.loads(tp.read_text("utf-8")))
    return out


def positive_signals(sig, nova, has_ing):
    out = []
    fib = sig.get("dietary_fiber_g"); prot = sig.get("protein_g"); sod = sig.get("sodium_mg")
    sugar = sig.get("sugars_g")
    if fib is not None and fib >= 6:
        out.append(f"{round(fib,1)} גרם סיבים ל-100 גרם")
    if prot is not None and prot >= 10:
        out.append(f"{round(prot,1)} גרם חלבון ל-100 גרם")
    if sod is not None and sod <= 200:
        out.append(f"נתרן נמוך יחסית — {round(sod)} מ\"ג ל-100 גרם")
    if sugar is not None and sugar <= 2:
        out.append("כמעט ללא סוכר")
    return out[:3]


def limiting_signals(sig, caps, pens):
    out = []
    sod = sig.get("sodium_mg"); sat = sig.get("fat_saturated_g"); fat = sig.get("fat_g")
    sugar = sig.get("sugars_g")
    if sod is not None and sod >= 500:
        out.append(f"{round(sod)} מ\"ג נתרן ל-100 גרם — גבוה")
    if sat is not None and sat >= 5:
        out.append(f"{round(sat,1)} גרם שומן רווי ל-100 גרם")
    if sugar is not None and sugar >= 15:
        out.append(f"{round(sugar,1)} גרם סוכר ל-100 גרם")
    if fat is not None and fat >= 25 and not any("שומן" in x for x in out):
        out.append(f"{round(fat)} גרם שומן ל-100 גרם")
    # NOVA 4 processing
    for c in (caps or []):
        if "NOVA" in (c.get("rule") or "") and not any("עיבוד" in x for x in out):
            out.append("מוצר אולטרה-מעובד (NOVA 4)")
    return out[:3]


def build_insight(name, score, grade, sig, caps, total):
    """2-line interpretive verdict derived from real signals."""
    sod = sig.get("sodium_mg"); fib = sig.get("dietary_fiber_g"); prot = sig.get("protein_g")
    sugar = sig.get("sugars_g"); fat = sig.get("fat_g")
    # Line 1: standing + primary positive/character
    if grade in ("A", "B"):
        if fib is not None and fib >= 6:
            l1 = f"מבין {total} חטיפים שנסרקו, זה אחד הבודדים עם {round(fib,1)} גרם סיבים ל-100 גרם."
        elif prot is not None and prot >= 9:
            l1 = f"מבין {total} חטיפים, בולט עם {round(prot,1)} גרם חלבון ל-100 גרם."
        elif sod is not None and sod <= 250:
            l1 = f"מבין {total} חטיפים, פרופיל נקי יחסית — נתרן נמוך ({round(sod)} מ\"ג ל-100 גרם)."
        else:
            l1 = f"מבין {total} חטיפים, פרופיל סביר שמציב אותו בחלק העליון של המדף."
    elif grade == "C":
        l1 = f"חטיף ממוצע למדף — לא בולט לטובה ולא נופל בבירור."
    else:
        if sugar is not None and sugar >= 15:
            l1 = f"חטיף ממותק יותר מאשר מלוח — {round(sugar,1)} גרם סוכר ל-100 גרם."
        else:
            l1 = f"מהחלק התחתון של המדף — פרופיל תזונתי חלש."
    # Line 2: the catch / grade qualifier
    catch = []
    if sod is not None and sod >= 500:
        catch.append(f"שקית שלמה תתרום נתרן יומי משמעותי — {round(sod)} מ\"ג ל-100 גרם")
    if fat is not None and fat >= 30:
        catch.append(f"{round(fat)} גרם שומן ל-100 גרם")
    if catch:
        l2 = f"{grade} עם הסתייגות: " + "; ".join(catch[:2]) + "."
    else:
        l2 = f"הציון {round(score)}/{grade} משקף את האיזון הכולל בין הרכיב לעיבוד."
    return l1 + "\n" + l2


def bottom_line(name, score, grade, sig, total):
    sod = sig.get("sodium_mg"); fib = sig.get("dietary_fiber_g")
    if grade in ("A", "B"):
        return f"מהטובים במדף ({round(score)}/{grade}) — אבל \"הטוב ביותר\" אינו \"מצוין\": עדיין חטיף מעובד."
    if grade == "C":
        return f"בחירה סבירה אם רוצים חטיף — {round(score)}/{grade}, ללא יתרון תזונתי בולט."
    return f"מהחלשים במדף ({round(score)}/{grade}); עדיף לבחור חטיף עם פרופיל נקי יותר."


def main():
    b1 = load_bsip1()
    traces = load_traces()
    products = []
    skipped = {}
    total_scored = sum(1 for t in traces
                       if t.get("final_score_estimate") is not None
                       and t.get("data_sufficiency") != "insufficient")

    for t in traces:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id") or ""
        score = t.get("final_score_estimate")
        if score is None or t.get("data_sufficiency") == "insufficient":
            skipped[pid] = "insufficient"; continue
        rec1 = b1.get(pid, {})
        sig = t.get("L1_observed_signals") or {}
        grade = grade_from_score(score)
        nova = t.get("nova_proxy")
        caps = t.get("caps_applied") or []
        pens = t.get("penalties_applied") or []
        has_ing = rec1.get("ingredient_text_quality") == "clean"

        name = rec1.get("canonical_name_he") or ref.get("product_name_he") or ""
        brand = rec1.get("brand") or ""
        retailer = (rec1.get("source_retailers") or ["yochananof"])[0]
        nutrition = {
            "energyKcal": sig.get("energy_kcal"),
            "protein": sig.get("protein_g"),
            "fat": sig.get("fat_g"),
            "carbs": sig.get("carbohydrates_g"),
            "fiber": sig.get("dietary_fiber_g"),
            "sodium": sig.get("sodium_mg"),
            "sugar": sig.get("sugars_g"),
            "saturatedFat": sig.get("fat_saturated_g"),
        }
        pos = positive_signals(sig, nova, has_ing)
        lim_text = limiting_signals(sig, caps, pens)
        insight = build_insight(name, score, grade, sig, caps, total_scored)
        # limitingFactors token list (for row chips) from caps/penalties
        lim_tokens = []
        for c in caps:
            r = c.get("rule", "")
            if "SODIUM" in r: lim_tokens.append("sodium")
            elif "SUGAR" in r: lim_tokens.append("sugar")
            elif "NOVA" in r: lim_tokens.append("processing")
            elif "SAT" in r: lim_tokens.append("saturated_fat")
        for p in pens:
            r = p.get("rule", "")
            if "SEED_OIL" in r: lim_tokens.append("seed_oil")
            elif "FAT" in r: lim_tokens.append("fat")
        lim_tokens = list(dict.fromkeys(lim_tokens))[:4]

        conf = "verified" if has_ing else "partial"
        conf_label = "נתונים מלאים" if has_ing else "נתונים חלקיים"
        record = {
            "id": pid,
            "name": name,
            "brand": brand,
            "imageUrl": rec1.get("image_url") or "",
            "score": round(score),
            "grade": grade,
            "insightLine": insight,
            "confidence": conf,
            "subPool": rec1.get("sub_pool") or "chips",
            "novaGroup": nova,
            "retailer": retailer,
            "retailer_he": retailer_he(retailer),
            "limitingFactors": lim_tokens,
            "ingredientCount": rec1.get("ingredient_count") or 0,
            "expansion": {
                "nutrition": nutrition,
                "ingredients": rec1.get("ingredients_text_he") or "",
                "confidenceLabel": conf_label,
                "servingNote": "ל-100 גרם",
                "positiveSignals": pos,
                "limitingFactors": lim_text,
                "bottomLine": bottom_line(name, score, grade, sig, total_scored),
                "comparisonContext": "",
            },
            "provenance": "bsip0_yochananof_real_scrape + off_panel",
            "barcode": rec1.get("barcode") or "",
            "source_traceability_status": "resolved" if has_ing else "panel_only",
            "confidence_label_he": "מבוסס על נתונים מלאים" if has_ing else "מבוסס על נתוני תזונה בלבד",
            "confidence_tooltip_he": ("הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים."
                                       if has_ing else
                                       "הציון מבוסס על לוח התזונה; רשימת הרכיבים אינה זמינה במקור."),
            "confidence_sub_reason": None if has_ing else "ingredients_unavailable",
        }
        products.append(record)

    products.sort(key=lambda p: -(p.get("score") or 0))

    grade_dist = dict(Counter(p["grade"] for p in products))
    subpool_dist = dict(Counter(p["subPool"] for p in products))
    nova_dist = dict(Counter(str(p["novaGroup"]) for p in products))
    retailer_dist = dict(Counter(p["retailer"] for p in products))
    ing_cov = sum(1 for p in products if p["source_traceability_status"] == "resolved")

    output = {
        "_meta": {
            "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "category": "salty-snacks",
            "category_he": "חטיפים מלוחים",
            "run_id": "run_salty_snacks_002",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v4",
            "change_note": (
                "v4 REAL rebuild (TASK-228): corpus rebuilt from real Yochananof storefront "
                "catalog (real EAN + real api.yochananof.co.il image URL, HTTP-200 verified) + "
                "Open Food Facts nutrition panels by real EAN (EDPG candidate→verified via "
                "BSIP0/QA). Replaces the fabricated-barcode / fake-image-host v3. Engine "
                "unchanged (engine-baseline-2026-06-04 + TASK-216 extrusion signal). Editorial "
                "content derived from real traces. sodium + fiber retained for metric bars."
            ),
            "sub_pools": ["chips", "popcorn", "puffed", "baked", "rice_cakes", "pretzels"],
            "provenance": (
                "TASK-228 real rebuild. Identity+image: Yochananof catalog harvest (real EAN). "
                f"Panel: Open Food Facts by real EAN. Corpus: {len(products)} products. "
                f"Ingredient coverage: {ing_cov}/{len(products)}. "
                f"Grade dist: {grade_dist}. NOVA dist: {nova_dist}."
            ),
            "grade_distribution": grade_dist,
            "subpool_distribution": subpool_dist,
            "nova_distribution": nova_dist,
            "retailer_breakdown": retailer_dist,
            "ingredient_coverage": f"{ing_cov}/{len(products)}",
        },
        "products": products,
    }
    OUT_LOCAL.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_LOCAL}")
    print(f"Written: {OUT_WEB}")
    print(f"Products: {len(products)}  grades: {grade_dist}")
    print(f"Ingredient coverage: {ing_cov}/{len(products)}")
    print(f"Skipped insufficient: {len(skipped)} -> {list(skipped)}")

if __name__ == "__main__":
    main()
