# -*- coding: utf-8 -*-
"""
TASK-169B — Transform run_cheese_004 (BARI_RECAL_P0=ON) frontend_package.json into
the bari-web comparison schema → cheese_frontend_v2.json (STAGED, NOT live-pointed).

Mirrors build_cheese_frontend.py (run_003 → cheese_frontend_v1.json) exactly, with
ONE deliberate, flagged difference handled at the display-set boundary:

  GOVERNANCE CONFLICT (surfaced, NOT silently resolved):
  The run_003 A-ceiling construct (EV-021 / RULING-DAIRY-A-01 C1-C6) marks
  a_eligible_pre_routing=False for ALL cheese, so the package withholds every
  grade-A product. But TASK-169 v1.1 (owner ruling 2026-06-02) RETIRES the hard
  grade cap and explicitly intends cottage 1% to LAND at ~90/A as the shelf leader.
  These two owner-approved decisions conflict.

  This builder STAGES the recalibrated A's for the owner look (the recal's stated
  purpose), i.e. it applies the routing + data-sufficiency withholds (misroute,
  insufficient) but DOES NOT apply the EV-021 A-ceiling withhold. The conflict is
  recorded verbatim in _meta.recal_governance_conflict for Nutrition/Product/owner
  to settle before any live repoint. NO live file is overwritten by this script.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "frontend_package.json")
# STAGED alongside the live file — a NEW versioned filename; the page import is NOT changed.
OUT = os.path.abspath(
    os.path.join(
        HERE, "..", "..", "..", "bari-web", "src", "data", "comparisons", "cheese_frontend_v2.json"
    )
)

SUBPOOL_TO_CLUSTER = {
    "cottage": "cottage",
    "white_cheese_quark": "white-cheese-quark",
    "cream_cheese_spread": "cream-cheese-spread",
    "labaneh": "labaneh",
}


def vm_id(barcode):
    return "che-" + str(barcode)


def round_half_up(x):
    import math
    return int(math.floor(x + 0.5))


def n(v):
    return None if v is None else v


def fmt_num(v):
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
    """Deterministic Hebrew placeholder insight line from package data.
    *** Content Agent WILL REWRITE these against the NEW scores. *** Many run_003
    insight lines are now stale (see TASK-169B report deliverable (b))."""
    nut = p["nutrition"]
    protein = nut.get("protein_g")
    fat = nut.get("fat_g")
    subpool = p["subpool"]

    protein_s = fmt_num(protein)
    fat_s = fmt_num(fat)

    if p.get("marketing_divergence_finding"):
        return "מסומן 'לייט', אך הפחתת השומן אינה נתמכת בנתוני האריזה."

    if subpool == "cream_cheese_spread":
        if fat is not None and protein is not None:
            if fat >= 20:
                return f"{fat_s} גרם שומן ל-100 גרם מול {protein_s} גרם חלבון — ממרח עתיר שומן, לא מקור חלבון."
            return f"{fat_s} גרם שומן ו-{protein_s} גרם חלבון ל-100 גרם — ממרח, לא גבינה לבנה."
        if fat is not None:
            return f"{fat_s} גרם שומן ל-100 גרם — ממרח גבינה עתיר שומן."

    if subpool in ("cottage", "white_cheese_quark"):
        if protein is not None and fat is not None:
            return f"{protein_s} גרם חלבון ל-100 גרם ב-{fat_s} גרם שומן — גבינה לבנה על בסיס חלבי פשוט."
        if protein is not None:
            return f"{protein_s} גרם חלבון ל-100 גרם — גבינה לבנה על בסיס חלבי פשוט."

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

    if protein is not None:
        return f"{protein_s} גרם חלבון ל-100 גרם."
    return ""


def build_product(p):
    nut = p["nutrition"]
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
            "ingredients": None,
            "confidenceLabel": confidence_label(p["confidence_level"]),
            "servingNote": "ל-100 גרם",
        },
    }


def main():
    pkg = json.load(io.open(PKG, encoding="utf-8"))
    # Display set: apply routing + data withholds; STAGE the recal A's (do NOT apply
    # the EV-021 A-ceiling withhold — see module docstring; conflict recorded in _meta).
    disp = [x for x in pkg["products"]
            if not x["_flags"]["misrouted"] and not x["_flags"]["insufficient"]]
    disp.sort(key=lambda d: (-d["score"], str(d["barcode"])))
    products = [build_product(p) for p in disp]

    a_ceiling_withheld = [
        {"name": x["name"], "score": round_half_up(x["score"]), "grade": x["grade"], "pool": x["subpool"]}
        for x in pkg["products"]
        if x["_flags"]["a_ceiling_withhold"]
    ]

    meta = {
        "generated": pkg["generated"],
        "category": "cheese-spreads",
        "product_count": len(products),
        "scored_count": sum(1 for p in products if p["score"] is not None),
        "schema": "BariProductVM[]",
        "version": "v2-run_cheese_004-recal_p0",
        "expansion": "technical_only_v1",
        "staged_not_live": True,
        "scope_note": (
            "מדף גבינות לבנות וממרחים אמיתי (Shufersal) — ציוני מנוע Bari 0.4.1 עם כיול מחדש "
            "BARI_RECAL_P0 (run_cheese_004, TASK-169B). גרסה מבוימת לבדיקת בעלים — טרם הוחלף קובץ חי."
        ),
        "provenance": {
            "run_id": "run_cheese_004",
            "engine": "proto_v0 / 0.4.1 + BARI_RECAL_P0=on",
            "recal_p0": "on",
            "scores_from": "run_cheese_004 frontend_package.json product.score (recalibrated; rounded half-up for display)",
            "insight_lines_from": "DRAFT placeholders from package data — Content Agent MUST rewrite vs new scores (TASK-169B report (b))",
            "withheld": {
                "misrouted": pkg["counts"]["withheld_misrouted"],
                "insufficient": pkg["counts"]["withheld_insufficient"],
                "a_ceiling_NOT_applied": pkg["counts"]["withheld_a_ceiling"],
            },
            "governance_ref": pkg["governance_ref"],
            "task": "TASK-169B",
        },
        "recal_governance_conflict": {
            "issue": (
                "The run_003 A-ceiling construct (EV-021 / RULING-DAIRY-A-01 C1-C6) sets "
                "a_eligible_pre_routing=False for ALL cheese, which would withhold every recalibrated "
                "grade-A product (including the flagship cottage 1% at 90/A). TASK-169 v1.1 (owner ruling "
                "2026-06-02) retires the hard grade cap and intends cottage 1% to LAND at ~90/A as the "
                "shelf leader. These two owner-approved decisions conflict."
            ),
            "resolution_pending": "Nutrition + Product + owner must reconcile EV-021 vs TASK-169 v1.1 before any live repoint.",
            "this_file_behavior": "STAGES the recal A's (A-ceiling withhold NOT applied) so the owner can see the intended shelf. NOT live.",
            "a_ceiling_would_withhold": a_ceiling_withheld,
        },
        "subpools": {
            "cottage": pkg["subpools"]["cottage"]["name_he"],
            "white-cheese-quark": pkg["subpools"]["white_cheese_quark"]["name_he"],
            "cream-cheese-spread": pkg["subpools"]["cream_cheese_spread"]["name_he"],
            "labaneh": pkg["subpools"]["labaneh"]["name_he"],
        },
        "disclosures": {
            "category_wide_sodium_satfat": pkg["disclosures_sec_6_4"]["category_wide_sodium_satfat"]["text_he"],
            "pool_specific_light_reformulation": pkg["disclosures_sec_6_4"]["pool_specific_light_reformulation"]["text_he"],
            "labaneh_n1_condition": (
                "לבנה — קבוצת מוצר יחידה. מוצג מוצר אחד בלבד, על מאפייניו, ללא דירוג פנימי בתוך הקבוצה."
            ),
        },
    }

    out = {"_meta": meta, "products": products}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("WROTE", OUT)
    print("products:", len(products), "| a_ceiling would withhold:", len(a_ceiling_withheld))


if __name__ == "__main__":
    main()
