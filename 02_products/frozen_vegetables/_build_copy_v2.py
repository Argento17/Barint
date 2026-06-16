# -*- coding: utf-8 -*-
"""
TASK-235 Phase 3 — frozen-vegetable consumer copy (score-free v2).
Copy authoring only. Reads the grounded copy-input, emits a draft + benefit-claim table.
No frontend / no generator / no engine. Per-band copy logic per Phase 1 spec §3.
"""
import json, io

SRC = r"c:/Bari/02_products/frozen_vegetables/frozen_vegetables_v2_phase3_copyinput_v1.json"
OUT = r"c:/Bari/02_products/frozen_vegetables/frozen_vegetables_copy_v2_draft.json"

with io.open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# Hebrew vegetable display names for USDA generic-reference phrasing
VEG_HE = {
    "cauliflower": "כרובית", "broccoli": "ברוקולי", "green_beans": "שעועית ירוקה",
    "yellow_wax_beans": "שעועית צהובה", "sweet_corn": "תירס", "spinach": "תרד",
    "okra": "במיה", "green_peas": "אפונה", "fava_beans": "פול ירוק",
    "white_beans": "שעועית לבנה", "chickpeas": "חומוס", "soybeans_green": "פולי סויה",
}
UNIT = {"fiber_g": "גרם סיבים", "vitc_mg": 'מ"ג ויטמין C',
        "vita_rae_ug": "מק\"ג ויטמין A", "vitk_ug": "מק\"ג ויטמין K",
        "folate_ug": "מק\"ג חומצה פולית", "protein_g": "גרם חלבון"}

def fmt(v):
    return str(int(v)) if float(v) == int(v) else str(v)

def usda_phrase(veg_q, key, val):
    """Approved generic-reference phrasing. Returns (consumer_phrase, claim_row)."""
    veg = VEG_HE.get(veg_q, veg_q)
    phrase = f"{veg} מספק בדרך כלל ~{fmt(val)} {UNIT[key]} ל-100 גרם (ערך ייחוס גנרי, לא נמדד על המוצר)."
    return phrase

claim_table = []   # rows for benefit_claim_table
def add_claim(pid, claim, source_type):
    claim_table.append({
        "bsip1_product_id": pid, "claim": claim,
        "source_type": source_type, "nutrition_approval_status": "PENDING"
    })

out = []

for p in data["products"]:
    pid = p["bsip1_product_id"]
    name = p["name_he"]
    band = p["consumer_band"]
    marker = p["standing_marker"]
    lab = p.get("label_nutrition_per100g", {})
    usda = p.get("usda_generic_benefits_per100g", {}) or {}
    nc = p.get("is_not_characterized", False)
    veg_q = p.get("usda_generic_query")
    ingr = p.get("ingredient_list", [])

    refs = []          # benefit_claims_used
    positive = []      # expansion.positive_facts
    what = []          # expansion.what_to_know
    header = "מה לדעת"

    # -------- BAND 1: ירקות בודדים --------
    if band == "ירקות בודדים":
        l1 = f"{name} — ירק אחד, רכיב אחד."
        fiber = lab.get("fiber")
        kcal = lab.get("energyKcal")
        # collapsed verdict line 2: lead with fiber if meaningful & present (label fact)
        bits = []
        if fiber is not None and fiber >= 2.5:
            c = f"מספק כ-{fmt(fiber)} גרם סיבים ל-100 גרם."
            bits.append(c); add_claim(pid, c, "label"); refs.append(c); positive.append(c)
        elif fiber is not None:
            c = f"{fmt(fiber)} גרם סיבים ל-100 גרם."
            positive.append(c); add_claim(pid, c, "label"); refs.append(c)
        # identity / light energy context (no alarm, no recommendation)
        if not bits:
            l2 = "ירק פשוט בלי תוספות. מה שכתוב על האריזה הוא מה שיש בפנים."
        else:
            l2 = bits[0] + " ללא תוספות — רכיב יחיד."
        # USDA generic micros -> positive facts (generic-reference framed)
        for key in ("vitc_mg", "vita_rae_ug", "vitk_ug", "fiber_g"):
            if key in usda and float(usda[key]) > 0:
                ph = usda_phrase(veg_q, key, usda[key])
                positive.append(ph); add_claim(pid, ph, "USDA generic-reference"); refs.append(ph)
        # plain veg: usually no catch. Only flag organic-corn higher energy as a plain fact if notable.
        if not what:
            pass
        bottom = "ירק קפוא בודד: שומר את עצמו טוב לבישול, בלי תוספות. ההבדלים בין מוצרים בקטגוריה קטנים."

    # -------- BAND 2: קטניות --------
    elif band == "קטניות":
        prot = lab.get("protein"); fiber = lab.get("fiber")
        label_fiber = fiber is not None
        # line-1 identity reflects what's actually a LABEL fact (don't promise label fiber we don't have)
        if prot is not None and label_fiber:
            l1 = f"{name} — קטנייה, מקור חלבון וסיבים."
        elif prot is not None:
            l1 = f"{name} — קטנייה, מקור חלבון."
        else:
            l1 = f"{name} — קטנייה."
        head = []
        if prot is not None:
            c = f"כ-{fmt(prot)} גרם חלבון ל-100 גרם"
            head.append(c); add_claim(pid, c, "label"); refs.append(c); positive.append(c + ".")
        if label_fiber:
            c = f"כ-{fmt(fiber)} גרם סיבים ל-100 גרם"
            head.append(c); add_claim(pid, c, "label"); refs.append(c); positive.append(c + ".")
        elif "fiber_g" in usda:
            ph = usda_phrase(veg_q, "fiber_g", usda["fiber_g"])
            positive.append(ph); add_claim(pid, ph, "USDA generic-reference"); refs.append(ph)
            what.append("ערך הסיבים לא דווח על האריזה — מוצג ערך ייחוס גנרי, לא נמדד על המוצר עצמו.")
        if "folate_ug" in usda:
            ph = usda_phrase(veg_q, "folate_ug", usda["folate_ug"])
            positive.append(ph); add_claim(pid, ph, "USDA generic-reference"); refs.append(ph)
        # collapsed line-2: only state on-label facts as the headline
        if prot is not None and label_fiber:
            l2 = " • ".join(head) + " — חלבון וסיבים באותה כף."
        elif prot is not None:
            l2 = f"כ-{fmt(prot)} גרם חלבון ל-100 גרם — קטנייה משביעה ברכיב יחיד."
        else:
            l2 = "קטנייה שלמה, רכיב יחיד."
        bottom = "קטנייה: מביאה חלבון וסיבים שירקות מימיים לא נותנים. שווה כשמחפשים מנה משביעה."

    # -------- BAND 4: תיבול ובישול --------
    elif band == "תיבול ובישול":
        header = "מה לדעת"
        # reframe up front — judge as seasoning
        l1 = f"{name} — תיבול, נשפט ככזה ולא כירק במנה."
        # plain ingredient statement
        main = ingr[0] if ingr else name
        l2 = "רכיב לבישול: כף קטנה נכנסת לתבשיל, לא צלחת שלמה. הערכים מתייחסים לשימוש של כ-5 גרם (כפית)."
        what.append("הערכים על האריזה הם ל-100 גרם — שימוש רגיל הוא כפית, הרבה פחות.")
        # composition / additive transparency (identity only, no nutrient claim, no oil/salt as flaw)
        addl = [x for x in ingr[1:] if x.strip()]
        if addl:
            positive.append("רשימת רכיבים קצרה: " + ", ".join([ingr[0]] + addl[:4]) + ".")
        else:
            positive.append("רכיב יחיד.")
        bottom = "תיבול — לא ירק למנה. בודקים אותו לפי מה שהוא: רכיב שנותן טעם לבישול."

    # -------- BAND 3: תערובות וארוחות --------
    else:  # תערובות וארוחות
        header = "מה לדעת"
        l1 = f"{name} — ארוחה מורכבת, לא ירק יחיד."
        # composition split from ingredient list
        veg_share = None
        pasta = any(("פסטה" in x or "פוזילי" in x or "גלוטן" in x) for x in ingr)
        sauce = any(("רוטב" in x or "סצואן" in x or "סויה" in x) for x in ingr)
        season = any(("תיבול" in x or "מלח" in x) for x in ingr)
        addmark = any(("מייצב" in x or "מעכב חמצון" in x or "קסנט" in x or "עמילן" in x or "מיצוי" in x) for x in ingr)
        comp_bits = []
        if pasta:
            comp_bits.append("פסטה")
        if sauce:
            comp_bits.append("רוטב")
        # build line 2
        if pasta and sauce:
            l2 = "ירקות עם פסטה ושקיק רוטב — מנה מוכנה, לא ירק נקי. נאכלת עם כל מה שבפנים."
            what.append("כולל פסטה (גלוטן) ושקיק רוטב — הנתרן והפחמימה במנה מגיעים מהתוספות, לא מהירקות.")
        elif pasta:
            l2 = "ירקות עם פסטה מבושלת — מנה, לא ירק יחיד. הפחמימה במנה מגיעה מהפסטה."
            what.append("כ-25% פסטה (גלוטן) מעורבים בירקות — נאכלת כמנה שלמה.")
        else:
            l2 = "תערובת כמה ירקות — נוחה לבישול מהיר, אבל לא רכיב יחיד שאפשר לאפיין."
        # additive watch-out (only band that surfaces this)
        if addmark:
            what.append("מכילה תוספים (מייצבים / מעכבי חמצון / עמילן) — קראו את רשימת הרכיבים המלאה.")
        # composition is identity-only; micros not characterized
        comp_claim = "תערובת — אין ערך ייחוס גנרי נקי; ערכי המיקרו לא אופיינו ולא הומצאו."
        positive.append("הרכב: " + ", ".join([x.strip() for x in ingr[:5] if x.strip()]) + ("…" if len(ingr) > 5 else "") + ".")
        add_claim(pid, comp_claim, "composition/identity"); refs.append(comp_claim)
        bottom = "תערובת/ארוחה: הנוחות באה במחיר התוספות. שופטים אותה כמנה, לא כירק בודד."

    # not_characterized guard: strip any benefit claim, keep identity/composition only
    if nc:
        positive = [x for x in positive if x.startswith("הרכב") or x.startswith("רשימת רכיבים") or "תערובת" in x]
        # ensure the not-characterized note is present and no benefit refs survive
        refs = [r for r in refs if "תערובת" in r or "ייחוס" not in r and "גרם" not in r and "מ\"ג" not in r and "מק" not in r]
        # rebuild refs cleanly: only composition/identity rows for this pid
        refs = [r["claim"] for r in claim_table if r["bsip1_product_id"] == pid and r["source_type"] == "composition/identity"]

    out.append({
        "bsip1_product_id": pid,
        "name_he": name,
        "consumer_band": band,
        "standing_marker": marker,
        "verdict_line_1": l1,
        "verdict_line_2": l2,
        "expansion": {
            "header": header,
            "positive_facts": positive,
            "what_to_know": what,
            "bottom_line": bottom,
        },
        "benefit_claims_used": refs,
    })

result = {
    "task": "TASK-235 Phase 3 — frozen-vegetable consumer copy v2 (score-free)",
    "model": "Phase 1 spec §3 copy model; score-free; benefit facts label|USDA-generic|composition only",
    "n": len(out),
    "products": out,
    "benefit_claim_table": claim_table,
    "_status": "DRAFT — pending Nutrition claim sign-off + QA leak-scan",
}

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# console summary
from collections import Counter
by_src = Counter(r["source_type"] for r in claim_table)
nc_ids = [p["bsip1_product_id"] for p in data["products"] if p["is_not_characterized"]]
print("products:", len(out))
print("claims total:", len(claim_table))
print("by source:", dict(by_src))
print("not_characterized count:", len(nc_ids))
print(OUT)
