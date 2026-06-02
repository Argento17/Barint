# -*- coding: utf-8 -*-
"""
TASK-152 — Transform run_cheese_003 frontend_package.json into the live
bari-web comparison schema (cheese_frontend_v1.json).

FRONTEND-ONLY. Does NOT touch scores, grades, or scoring logic — it only
re-shapes the already-signed package into the BariProductVM[] contract the
website renders (id/name/imageUrl/score/grade/confidence/insightLine/_cluster/
expansion + _meta), matching yogurts_frontend_v2.json / maadanim_frontend_v2.json.

Display set = the 52 display_approved products (Nutrition sign-off keeps all 7
withheld OFF display: 1 misrouted, 1 A-ceiling, 5 transparency-tier partial-panel).
Insight lines are drafted faithfully from package data per the canonical insight-line
spec (composition fact / contradiction / position) and are flagged for Content review.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "frontend_package.json")
OUT = os.path.abspath(
    os.path.join(
        HERE, "..", "..", "..", "bari-web", "src", "data", "comparisons", "cheese_frontend_v1.json"
    )
)

SUBPOOL_TO_CLUSTER = {
    "cottage": "cottage",
    "white_cheese_quark": "white-cheese-quark",
    "cream_cheese_spread": "cream-cheese-spread",
    "labaneh": "labaneh",
}

# Stable, short id prefix for the category (mirrors yog-/snk- convention).
def vm_id(barcode):
    return "che-" + str(barcode)


def round_half_up(x):
    # ScoreChip renders Math.round (round-half-up on .5). Mirror it so the
    # stored display score matches the rendered chip; never re-derives a score.
    import math
    return int(math.floor(x + 0.5))


def n(v):
    return None if v is None else v


def fmt_num(v):
    """Render a number without a trailing .0 for whole values (Hebrew copy)."""
    if v is None:
        return None
    if float(v).is_integer():
        return str(int(v))
    return ("%g" % v)


def confidence_label(conf):
    return {
        "verified": "נתונים מלאים",
        "partial": "נתונים חלקיים",
        "insufficient": "נתונים חלקיים",
    }[conf]


def draft_insight_line(p):
    """
    Faithful, deterministic Hebrew insight line from package data.
    Canonical spec: composition fact / contradiction / position — restrained
    but fearless, no framework vocabulary. CONTENT AGENT WILL REVIEW/REFINE.
    """
    nut = p["nutrition"]
    protein = nut.get("protein_g")
    fat = nut.get("fat_g")
    sat = nut.get("fat_saturated_g")
    subpool = p["subpool"]
    grade = p["grade"]

    protein_s = fmt_num(protein)
    fat_s = fmt_num(fat)
    sat_s = fmt_num(sat)

    # Contradiction: an unsupported "light" marketing claim (divergence finding).
    if p.get("marketing_divergence_finding"):
        return f"מסומן 'לייט', אך הפחתת השומן אינה נתמכת בנתוני האריזה."

    # Cream-cheese / spreads: fat is the defining fact of the pool.
    if subpool == "cream_cheese_spread":
        if fat is not None and protein is not None:
            if fat >= 20:
                return f"{fat_s} גרם שומן ל-100 גרם מול {protein_s} גרם חלבון — ממרח עתיר שומן, לא מקור חלבון."
            return f"{fat_s} גרם שומן ו-{protein_s} גרם חלבון ל-100 גרם — ממרח, לא גבינה לבנה."
        if fat is not None:
            return f"{fat_s} גרם שומן ל-100 גרם — ממרח גבינה עתיר שומן."

    # Cottage / white-cheese / quark: protein staple — protein is the headline.
    if subpool in ("cottage", "white_cheese_quark"):
        if protein is not None and fat is not None:
            return f"{protein_s} גרם חלבון ל-100 גרם ב-{fat_s} גרם שומן — גבינה לבנה על בסיס חלבי פשוט."
        if protein is not None:
            return f"{protein_s} גרם חלבון ל-100 גרם — גבינה לבנה על בסיס חלבי פשוט."

    # Labaneh (n=1): present on its own merits, no intra-pool ranking.
    if subpool == "labaneh":
        parts = []
        if protein is not None:
            parts.append(f"{protein_s} גרם חלבון")
        if fat is not None:
            parts.append(f"{fat_s} גרם שומן")
        body = " ו-".join(parts) if parts else ""
        if body:
            return f"לבנה מסורתית — {body} ל-100 גרם. מוצג כמוצר יחיד בקבוצתו, ללא דירוג פנימי."
        return "לבנה מסורתית — מוצג כמוצר יחיד בקבוצתו, ללא דירוג פנימי."

    # Fallback (should not hit for display set).
    if protein is not None:
        return f"{protein_s} גרם חלבון ל-100 גרם."
    return ""


def build_product(p):
    nut = p["nutrition"]
    # Technical-only expansion (matches yogurts_frontend_v2 / bread_frontend_v2):
    # the package's ingredients_he carries Shufersal nutrition-panel + legal-disclaimer
    # bleed appended to the real ingredient list, so the raw string is withheld from
    # display. The clean structured nutrition grid below is what renders.
    ingredients = None
    return {
        "id": vm_id(p["barcode"]),
        "name": p["name"].strip(),
        "imageUrl": p.get("image_url") or None,
        "score": round_half_up(p["score"]),
        "grade": p["grade"],
        "confidence": p["confidence_level"],
        "insightLine": draft_insight_line(p),
        "_cluster": SUBPOOL_TO_CLUSTER[p["subpool"]],
        "expansion": {
            "nutrition": {
                "energyKcal": n(nut.get("energy_kcal")),
                "protein": n(nut.get("protein_g")),
                "sugar": n(nut.get("sugars_g")),
                "fat": n(nut.get("fat_g")),
                "fiber": n(nut.get("dietary_fiber_g")),
                "sodium": n(nut.get("sodium_mg")),
            },
            "ingredients": ingredients,
            "confidenceLabel": confidence_label(p["confidence_level"]),
            "servingNote": "ל-100 גרם",
        },
    }


def main():
    pkg = json.load(io.open(PKG, encoding="utf-8"))
    disp = [x for x in pkg["products"] if x["display_approved"]]
    # VM contract: pre-ordered scored-desc; UI never sorts. Stable secondary key
    # on barcode so equal scores keep a deterministic order across rebuilds.
    disp.sort(key=lambda d: (-d["score"], str(d["barcode"])))

    products = [build_product(p) for p in disp]

    meta = {
        "generated": pkg["generated"],
        "category": "cheese-spreads",
        "product_count": len(products),
        "scored_count": sum(1 for p in products if p["score"] is not None),
        "schema": "BariProductVM[]",
        "version": "v1-run_cheese_003",
        "expansion": "technical_only_v1",
        "scope_note": (
            "מדף גבינות לבנות וממרחים אמיתי (Shufersal) — ציוני מנוע Bari 0.4.1 "
            "(run_cheese_003); 52 מוצרים מוצגים מתוך 59 (7 הוסתרו: ניתוב שגוי, תקרת A, "
            "ופאנל מקור חלקי)."
        ),
        "provenance": {
            "run_id": "run_cheese_003",
            "engine": "proto_v0 / 0.4.1 (unmodified)",
            "scores_from": "frontend_package.json product.score (rounded half-up for display)",
            "expansion_note": "technical-only: clean nutrition grid; raw ingredient strings withheld (Shufersal panel/disclaimer bleed) — matches yogurt/bread precedent",
            "insight_lines_from": "drafted from package data (TASK-152) — pending Content Agent review",
            "withheld": {
                "misrouted": pkg["counts"]["withheld_misrouted"],
                "a_ceiling": pkg["counts"]["withheld_a_ceiling"],
                "transparency_tier_insufficient": pkg["counts"]["withheld_insufficient"],
                "note": "Nutrition sign-off (NUTRITION_SIGNOFF_VERDICT.md) keeps all 7 off display.",
            },
            "governance_ref": pkg["governance_ref"],
            "task": "TASK-152",
        },
        "subpools": {
            "cottage": pkg["subpools"]["cottage"]["name_he"],
            "white-cheese-quark": pkg["subpools"]["white_cheese_quark"]["name_he"],
            "cream-cheese-spread": pkg["subpools"]["cream_cheese_spread"]["name_he"],
            "labaneh": pkg["subpools"]["labaneh"]["name_he"],
        },
        # The 2 PO-approved Sec 6.4 disclosures carried verbatim from the package,
        # plus the labaneh n=1 standalone display condition.
        "disclosures": {
            "category_wide_sodium_satfat": pkg["disclosures_sec_6_4"][
                "category_wide_sodium_satfat"
            ]["text_he"],
            "pool_specific_light_reformulation": pkg["disclosures_sec_6_4"][
                "pool_specific_light_reformulation"
            ]["text_he"],
            "labaneh_n1_condition": (
                "לבנה — קבוצת מוצר יחידה. מוצג מוצר אחד בלבד, על מאפייניו, ללא דירוג "
                "פנימי בתוך הקבוצה."
            ),
        },
    }

    out = {"_meta": meta, "products": products}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("WROTE", OUT)
    print("products:", len(products))


if __name__ == "__main__":
    main()
