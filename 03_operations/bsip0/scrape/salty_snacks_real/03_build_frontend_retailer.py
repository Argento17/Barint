"""
Build salty_snacks_frontend_v4.json from BSIP2 run_salty_snacks_002 traces — REAL RETAILER
PANELS (TASK-237). NO Open Food Facts anywhere in this build.

Source: 02_products/salty_snacks/bsip2_outputs/run_salty_snacks_002 traces, scored on the
UNCHANGED engine (engine-baseline-2026-06-04 + TASK-216) over BSIP1 records whose nutrition
and Hebrew ingredients were re-sourced from the Yochananof storefront product modal
(panel_source = retailer_product_page). Trans "<0.5"/"L 0.5" declarations carried as
fat_trans_g == 0.5 -> engine threshold_declaration convention (no penalty); NO manual
trans data_corrections, NO basis-error excludes, NO OFF ingredient omits.

PRESERVED from the shipped quality work (TASK-230/231/232/233/234):
  - copy spec generators (no NOVA/score/recommendation leak, integer grams)
  - is_clean HARD GATE on every consumer string
  - confidence-label <-> ingredient consistency HARD GATE
  - brand normalization (one canonical per maker)
  - real Yochananof images (never a synthesized prefix)
  - BariProductVM emission strip
Editorial content is DERIVED FROM THE REAL TRACE (signals/caps/penalties).
"""
import sys, json, pathlib, datetime, re
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Bari\integrations\clients")
import hebrew_readability as hr  # noqa: E402
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
import frontend_core as FC  # noqa: E402

TRACES_DIR = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\products")
BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs")
OUT_LOCAL  = pathlib.Path(r"C:\Bari\02_products\salty_snacks\salty_snacks_frontend_v4.json")
OUT_WEB    = pathlib.Path(r"C:\bari\bari-web\src\data\comparisons\salty_snacks_frontend_v4.json")

# ── Brand normalization: one canonical string per maker (identity work, kept) ──
# Brands are NOT in the retailer panel, so we derive them from the product name as before.
BRAND_CANONICAL = {
    "osem": "אסם", "אסם": "אסם", "fitness": "פיטנס", "פיטנס": "פיטנס",
    "click": "קליק", "קליק": "קליק", "nestlé": "נסטלה", "nestle": "נסטלה",
}
BRAND_BY_BARCODE = {
    "7290111564291": "נסטלה", "7290111564277": "נסטלה",
    "7290017928661": "סמאש", "4011800528416": "Corny",
    "7290018893654": "צ'וקטה",
    "7290110551926": "תפוצ'יפס", "7290008745239": "תפוצ'יפס",
    "7290104500572": "אפרופו", "7290118421603": "אפרופו",
    "7290000066332": "אפרופו",
    "7290000066318": "אסם", "7290000066295": "אסם", "7290000066141": "אסם",
    "7290100850916": "עלית", "7290116537375": "קליק", "7290112494313": "קליק",
}


def grade_from_score(s):
    return FC.grade_from_score(s)


def retailer_he(r):
    return {"yochananof": "יוחננוף", "shufersal": "שופרסל"}.get(r, r)


def clean_ingredient_text(text):
    """Meaning-preserving cleanup for a real Hebrew ingredient list: European decimal
    commas in percentages (70,5% -> 70.5%) and a trailing standalone English token."""
    if not text:
        return text
    text = re.sub(r"(\d),(\d)", r"\1.\2", text)
    text = re.sub(r"[,\s]+[A-Za-z]{3,}\s*$", "", text)
    return text.strip().rstrip(",").strip()


def canonical_brand(raw_brand, barcode):
    if barcode in BRAND_BY_BARCODE:
        return BRAND_BY_BARCODE[barcode]
    key = (raw_brand or "").strip().lower()
    if key in BRAND_CANONICAL:
        return BRAND_CANONICAL[key]
    return (raw_brand or "").strip()


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


# ── Copy generation (COPY_SPEC_v4_TASK230) — unchanged from the shipped build ──

def positive_signals(sig):
    out = []
    fib = sig.get("dietary_fiber_g"); prot = sig.get("protein_g")
    sod = sig.get("sodium_mg"); sugar = sig.get("sugars_g")
    if fib is not None and fib >= 6:
        out.append(f"{round(fib)} גרם סיבים ל-100 גרם")
    if prot is not None and prot >= 10:
        out.append(f"{round(prot)} גרם חלבון ל-100 גרם")
    if sod is not None and sod <= 120:
        out.append(f"נתרן נמוך: {round(sod)} מ\"ג ל-100 גרם")
    if sugar is not None and sugar <= 2:
        out.append("כמעט בלי סוכר")
    return out[:3]


def processing_line(nova_group):
    if nova_group == 4:
        return "מעובד מאוד, עם רשימת רכיבים ארוכה ורחוקה מהחומר הגלם."
    return None


def limiting_signals(sig, nova_group):
    out = []
    sod = sig.get("sodium_mg"); sat = sig.get("fat_saturated_g")
    fat = sig.get("fat_g"); sugar = sig.get("sugars_g")
    if sod is not None and sod >= 500:
        out.append(f"{round(sod)} מ\"ג נתרן ל-100 גרם")
    if sat is not None and sat >= 5:
        out.append(f"{round(sat)} גרם שומן רווי ל-100 גרם")
    if sugar is not None and sugar >= 15:
        out.append(f"{round(sugar)} גרם סוכר ל-100 גרם")
    if fat is not None and fat >= 25 and not any("שומן" in x for x in out):
        out.append(f"{round(fat)} גרם שומן ל-100 גרם")
    if len(out) < 3:
        pl = processing_line(nova_group)
        if pl:
            out.append(pl)
    return out[:3]


def build_insight(score, grade, sig):
    sod = sig.get("sodium_mg"); fib = sig.get("dietary_fiber_g")
    prot = sig.get("protein_g"); sugar = sig.get("sugars_g"); fat = sig.get("fat_g")
    sat = sig.get("fat_saturated_g")

    l1 = None
    if (fib is not None and fib >= 6) or (prot is not None and prot >= 9):
        if fib is not None and fib >= 6 and prot is not None and prot >= 9:
            l1 = (f"אחד החטיפים הבודדים במדף עם {round(fib)} גרם סיבים "
                  f"ו-{round(prot)} גרם חלבון ל-100 גרם.")
        elif fib is not None and fib >= 6:
            l1 = f"אחד החטיפים הבודדים במדף עם {round(fib)} גרם סיבים ל-100 גרם."
        else:
            l1 = f"אחד החטיפים הבודדים במדף עם {round(prot)} גרם חלבון ל-100 גרם."
    elif sod is not None and sod <= 120:
        l1 = f"מהפרופילים הנקיים במדף: רק {round(sod)} מ\"ג נתרן ל-100 גרם."
    elif sugar is not None and sugar >= 15:
        l1 = f"חטיף מתוק שמתחזה למלוח: {round(sugar)} גרם סוכר ל-100 גרם."
    elif sod is not None and sod >= 600:
        l1 = f"חטיף מלוח מאוד: {round(sod)} מ\"ג נתרן ל-100 גרם."
    elif fat is not None and fat >= 28:
        l1 = f"חטיף עתיר שומן: {round(fat)} גרם שומן ל-100 גרם, רובו מהטיגון והשמן."
    elif grade in ("A", "B"):
        l1 = "נשאר בין הטובים במדף, גם בלי תכונה אחת שבולטת."
    elif grade == "C":
        l1 = "פרופיל ממוצע: לא בולט לטובה אבל גם לא נופל."
    else:
        l1 = "מהחלק התחתון של המדף, עם פרופיל תזונתי חלש."

    sweet_in_l1 = l1.startswith("חטיף מתוק")
    salty_in_l1 = l1.startswith("חטיף מלוח")
    fat_in_l1 = l1.startswith("חטיף עתיר שומן")

    l2 = None
    if sod is not None and sod >= 600 and not salty_in_l1:
        l2 = "שקית שלמה לבדה מכסה חלק ניכר מהנתרן היומי."
    elif fat is not None and fat >= 28 and not fat_in_l1:
        l2 = "רוב הקלוריות כאן מגיעות מהשומן."
    elif sat is not None and sat >= 7:
        l2 = f"כולל {round(sat)} גרם שומן רווי ל-100 גרם."
    elif sugar is not None and sugar >= 15 and not sweet_in_l1:
        l2 = "הסוכר הוא הסיפור כאן, לא המליחות."
    elif grade in ("A", "B"):
        l2 = "נשאר חטיף מעובד, אבל מהפרופילים הסבירים שתמצאו על המדף הזה."
    elif grade == "C":
        l2 = "נתרן וקלוריות במרכז הטווח של המדף, בלי יתרון תזונתי שמושך תשומת לב."
    else:
        l2 = "פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן."

    return l1 + "\n" + l2


def bottom_line(grade, sig):
    if grade in ("A", "B"):
        return ("מהטובים שתמצאו על המדף הזה, וזה עדיין חטיף מעובד. "
                "\"הכי טוב\" כאן לא אומר \"מצוין\".")
    if grade == "C":
        return "חטיף סביר בלי יתרון תזונתי בולט. נמצא בדיוק במרכז המדף."
    return "מהחלשים במדף: פרופיל עתיר שומן, נתרן או סוכר, בלי צד מאזן."


def confidence_fields(trace):
    f = FC.confidence_from_trace(trace)
    return {
        "confidence": f["confidence"],
        "confidenceLabel": f["confidence_label_he"],
        "confidence_label_he": f["confidence_label_he"],
        "confidence_tooltip_he": f["confidence_tooltip_he"],
        "confidence_sub_reason": f["confidence_sub_reason"],
    }


def load_drops():
    p = pathlib.Path(r"C:\Bari\02_products\salty_snacks\reports\salty_snacks_retailer_drops.json")
    if p.exists():
        return json.loads(p.read_text("utf-8"))
    return []


def main():
    b1 = load_bsip1()
    traces = load_traces()
    drops = load_drops()
    products = []
    skipped = {}

    for t in traces:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id") or ""
        score = t.get("final_score_estimate")
        if score is None or t.get("data_sufficiency") == "insufficient":
            skipped[pid] = "insufficient"; continue

        rec1 = b1.get(pid, {})
        sig = t.get("L1_observed_signals") or {}
        score_int = FC.round_score(score)
        grade = grade_from_score(score_int)
        nova = t.get("nova_proxy")
        barcode = rec1.get("barcode") or ""

        name = rec1.get("canonical_name_he") or ref.get("product_name_he") or ""
        brand = canonical_brand(rec1.get("brand"), barcode)
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
        sodium_unavailable = sig.get("sodium_mg") is None

        # Real Hebrew ingredients straight from the retailer panel; light cleanup only.
        raw_ing = rec1.get("ingredients_text_he") or ""
        ingredients = clean_ingredient_text(raw_ing)
        has_ing = (rec1.get("ingredient_text_quality") == "clean") and bool(ingredients)

        # novaGroup published only when the consumer can see the composition it summarizes
        # (ingredientCount > 0). For real-panel products this is the common case.
        ingredient_count_pub = rec1.get("ingredient_count") or 0
        nova_pub = nova if ingredient_count_pub > 0 else None
        nova_suppressed_reason = None if nova_pub is not None else (
            "ingredients_unavailable" if not has_ing else None)

        pos = positive_signals(sig)
        lim_text = limiting_signals(sig, nova)
        insight = build_insight(score, grade, sig)
        conf_fields = confidence_fields(t)

        lim_tokens = []
        for c in (t.get("caps_applied") or []):
            r = c.get("rule", "")
            if "SODIUM" in r: lim_tokens.append("sodium")
            elif "SUGAR" in r: lim_tokens.append("sugar")
            elif "NOVA" in r: lim_tokens.append("processing")
            elif "SAT" in r: lim_tokens.append("saturated_fat")
        for p in (t.get("penalties_applied") or []):
            r = p.get("rule", "")
            if "SEED_OIL" in r: lim_tokens.append("seed_oil")
            elif "FAT" in r: lim_tokens.append("fat")
        lim_tokens = list(dict.fromkeys(lim_tokens))[:4]

        record = {
            "id": pid,
            "name": name,
            "brand": brand,
            "imageUrl": FC.select_image_url(rec1) or "",
            "score": FC.round_score(score),
            "grade": grade,
            "insightLine": insight,
            "confidence": conf_fields["confidence"],
            "subPool": rec1.get("sub_pool") or "chips",
            "novaGroup": nova_pub,
            "retailer": retailer,
            "retailer_he": retailer_he(retailer),
            "limitingFactors": lim_tokens,
            "ingredientCount": ingredient_count_pub,
            "expansion": {
                "nutrition": nutrition,
                "sodiumUnavailable": sodium_unavailable,
                "ingredients": ingredients,
                "confidenceLabel": conf_fields["confidenceLabel"],
                "servingNote": "ל-100 גרם",
                "positiveSignals": pos,
                "limitingFactors": lim_text,
                "bottomLine": bottom_line(grade, sig),
                "comparisonContext": "",
            },
            "provenance": "bsip0_yochananof_retailer_product_page_panel",
            "barcode": barcode,
            "source_traceability_status": "resolved" if has_ing else "panel_only",
            "confidence_label_he": conf_fields["confidence_label_he"],
            "confidence_tooltip_he": conf_fields["confidence_tooltip_he"],
            "confidence_sub_reason": conf_fields["confidence_sub_reason"],
            "nova_suppressed_reason": nova_suppressed_reason,
        }
        if sodium_unavailable:
            record["sodium_note_he"] = "ערך הנתרן לא דווח במקור עבור מוצר זה."
        products.append(record)

    products.sort(key=lambda p: -(p.get("score") or 0))

    # ── HARD GATE: every consumer string is_clean + no raw multi-decimal text ──
    leak_failures, decimal_failures = [], []
    raw_dec = re.compile(r"\d+\.\d{2,}")
    for p in products:
        strings = {
            "insightLine": p["insightLine"],
            "bottomLine": p["expansion"]["bottomLine"],
            "confidence_label_he": p["confidence_label_he"],
            "confidence_tooltip_he": p["confidence_tooltip_he"],
            "confidenceLabel": p["expansion"]["confidenceLabel"],
        }
        for i, s in enumerate(p["expansion"]["positiveSignals"]):
            strings[f"positiveSignals[{i}]"] = s
        for i, s in enumerate(p["expansion"]["limitingFactors"]):
            strings[f"limitingFactors[{i}]"] = s
        if p.get("sodium_note_he"):
            strings["sodium_note_he"] = p["sodium_note_he"]
        for key, s in strings.items():
            rep = hr.analyze(s)
            if not rep.is_clean:
                leak_failures.append((p["id"], key, s, [l.kind + ":" + l.term for l in rep.leaks
                                                        if l.kind != "english"]))
            if raw_dec.search(s):
                decimal_failures.append((p["id"], key, s))

    # ── HARD GATE: confidence-label <-> ingredient consistency ──
    confidence_failures = []
    for p in products:
        ing = (p["expansion"].get("ingredients") or "").strip()
        label = (p.get("confidence_label_he") or "") + " " + \
                (p.get("confidence_tooltip_he") or "") + " " + \
                (p["expansion"].get("confidenceLabel") or "")
        claims_full = (p.get("confidence") == "verified") or \
                      ("מלאים" in label) or ("רשימת הרכיבים" in label and "לא הי" not in label)
        if claims_full and not ing:
            confidence_failures.append((p["id"], p.get("confidence"), p.get("confidence_label_he")))

    if leak_failures or decimal_failures or confidence_failures:
        print("!!! GATE FAILURES !!!")
        for f in leak_failures: print("  LEAK", f)
        for f in decimal_failures: print("  RAW DECIMAL", f)
        for f in confidence_failures: print("  CONFIDENCE/INGREDIENT MISMATCH", f)
        sys.exit(1)
    print(f"GATE PASS: all consumer strings clean across {len(products)} products.")

    grade_dist = dict(Counter(p["grade"] for p in products))
    subpool_dist = dict(Counter(p["subPool"] for p in products))
    nova_dist = dict(Counter(str(p["novaGroup"]) for p in products))
    retailer_dist = dict(Counter(p["retailer"] for p in products))
    ing_cov = sum(1 for p in products if p["source_traceability_status"] == "resolved")
    sodium_unavail_ids = [p["id"] for p in products if p["expansion"].get("sodiumUnavailable")]
    panel_only_ids = [p["id"] for p in products if p["source_traceability_status"] == "panel_only"]

    # ── BariProductVM emission strip ──
    products = [FC.strip_non_vm_fields(p, keep={"subPool"}) for p in products]

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
                "v4 REAL RETAILER-PANEL re-source (TASK-237). Open Food Facts REMOVED from the "
                "salty pipeline entirely. Nutrition + Hebrew ingredients re-sourced per product "
                "from the Yochananof storefront product modal (panel_source=retailer_product_page). "
                "Engine UNCHANGED (engine-baseline-2026-06-04 + TASK-216); re-scored on real data "
                "(scores moved — authorized data re-source, not a scoring change). Trans \"<0.5\"/"
                "\"L 0.5\" declarations carried as fat_trans_g==0.5 -> engine threshold_declaration "
                "convention (no penalty); NO manual trans data_corrections, NO OFF ingredient omits. "
                "Identity+image unchanged (Yochananof catalog, real EAN, HTTP-200). "
                f"{len(drops)} products dropped: 1 Calbee import (no retailer panel) + "
                f"{sum(1 for d in drops if d.get('drop_class')=='basis_error')} whose Yochananof panel "
                "declares 'ל100 גרם' but is on a per-serving basis (kcal<200, Atwater-consistent; "
                "unrecoverable, TASK-234 basis-error precedent). NONE backfilled from OFF. "
                "PRESERVED: is_clean gate, confidence<->ingredient gate, no recommendation language, "
                "reworded confidence labels, brand normalization."
            ),
            "sub_pools": ["chips", "popcorn", "puffed", "baked", "rice_cakes", "pretzels"],
            "provenance": (
                "TASK-237 real retailer re-source. Identity+image: Yochananof catalog (real EAN). "
                "Panel: Yochananof product-page modal (real Hebrew nutrition + ingredients). "
                "NO Open Food Facts. "
                f"Corpus: {len(products)} products ({len(drops)} dropped: 1 no-panel + "
                f"{sum(1 for d in drops if d.get('drop_class')=='basis_error')} per-serving-basis error). "
                f"Ingredient coverage: {ing_cov}/{len(products)} (real Hebrew). "
                f"Grade dist: {grade_dist}. NOVA dist: {nova_dist}."
            ),
            "grade_distribution": grade_dist,
            "subpool_distribution": subpool_dist,
            "nova_distribution": nova_dist,
            "retailer_breakdown": retailer_dist,
            "ingredient_coverage": f"{ing_cov}/{len(products)}",
            "panel_only_ids": panel_only_ids,
            "sodium_unavailable_marked": sodium_unavail_ids,
            "off_removed": True,
            "panel_source": "retailer_product_page (yochananof storefront modal)",
            "dropped_products": drops,
            "dropped_count": len(drops),
        },
        "products": products,
    }
    OUT_LOCAL.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written: {OUT_LOCAL}")
    print(f"Written: {OUT_WEB}")
    print(f"Products: {len(products)}  grades: {grade_dist}")
    print(f"Ingredient coverage (real Hebrew): {ing_cov}/{len(products)}")
    print(f"Panel-only: {len(panel_only_ids)} {panel_only_ids}")
    print(f"Skipped insufficient: {len(skipped)} -> {list(skipped)}")


if __name__ == "__main__":
    main()
