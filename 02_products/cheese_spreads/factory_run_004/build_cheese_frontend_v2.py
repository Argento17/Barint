# -*- coding: utf-8 -*-
"""
TASK-169B — Transform run_cheese_004 (BARI_RECAL_P0=ON) frontend_package.json into
the bari-web comparison schema → cheese_frontend_v2.json (STAGED, NOT live-pointed).

GOVERNANCE CONFLICT RESOLVED (EV-021 AMENDMENT A1, owner-approved 2026-06-02):
  The prior run_003 A-ceiling construct collapsed RULING-DAIRY-A-01 C1-C6 into a
  blanket a_eligible_pre_routing=False for ALL cheese, which would have withheld
  every recalibrated grade-A cheese (incl. cottage 1% ~90/A). EV-021 Amendment A1
  RETIRES that blanket cap for cheese and replaces it with a CONDITIONAL
  A-ELIGIBILITY GATE: a cheese may DISPLAY grade A only if genuinely clean on the
  two axes the composite under-weights for cheese — sodium AND saturated fat.

  Mechanism is a CAP, not a withhold. A product that earns an A/S-band score but
  fails the gate keeps its numeric score and stays on the shelf, but its DISPLAYED
  grade is capped to B (e.g. 81/B). The misroute + insufficient + transparency
  withholds are UNCHANGED. The gate is active only with BARI_RECAL_P0=ON; flag-OFF
  behavior is unchanged. Cheese-scoped only (does not touch yogurt/milk/hummus).

  Predicate fields = L1_observed_signals.sodium_mg / .fat_saturated_g, which the
  package faithfully carries as nutrition.sodium_mg / nutrition.fat_saturated_g
  (verified identical against the run_cheese_004 BSIP2 traces).
"""
import io
import json
import os
import sys

# TASK-188: A-grade ingredient observability floor
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
from grade_governance import apply_a_grade_floor  # noqa: E402  TASK-188

# --- EV-021 AMENDMENT A1 — conditional cheese A-eligibility gate (BARI_RECAL_P0) ---
# Thresholds grounded in Israeli MoH red-label lines (sodium 600 / sat-fat 5.0 per
# 100g) held meaningfully below the red line per the "best != excellent" doctrine.
RECAL_P0_ON = os.environ.get("BARI_RECAL_P0", "").lower() in ("1", "on", "true", "yes")
CHEESE_A_SODIUM_MAX = 400.0  # mg/100g  (67% of the 600 red line; = shelf Q3)
CHEESE_A_SATFAT_MAX = 4.0    # g/100g   (80% of the 5.0 red line; excludes 9% tier @5.4)


def cheese_a_eligible(sodium_mg, sat_fat_g):
    """True only if genuinely clean on BOTH axes. Missing data fails closed."""
    if sodium_mg is None or sat_fat_g is None:
        return False  # fail-closed: gate cannot be evaluated -> cap to B
    return sodium_mg <= CHEESE_A_SODIUM_MAX and sat_fat_g <= CHEESE_A_SATFAT_MAX


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


def displayed_grade(p):
    """Apply the EV-021 Amendment A1 conditional A-eligibility gate (cheese, RECAL_P0).
    Returns (grade_to_show, a_capped_to_b: bool). Score is NEVER changed."""
    grade = p["grade"]
    if not RECAL_P0_ON:
        return grade, False
    if grade in ("A", "S"):
        nut = p["nutrition"]
        if not cheese_a_eligible(nut.get("sodium_mg"), nut.get("fat_saturated_g")):
            return "B", True  # CAP displayed grade to B; keep numeric score; stays visible
    return grade, False


def build_product(p):
    nut = p["nutrition"]
    grade, a_capped = displayed_grade(p)
    disp_score = round_half_up(p["score"])

    # TASK-188: A-grade ingredient observability floor — applied after EV-021 cheese gate.
    # Cheese builder withholds ingredients (ingredients=None in expansion), so Condition 1
    # fires for any A-grade product without a resolved ingredient list here. Pass the
    # normalized nutrition dict from the package for Condition 3; no BSIP2 trace dict
    # available at this layer (trace=None; Condition 2 defaults to pass).
    disp_score, grade = apply_a_grade_floor(
        score=disp_score,
        grade=grade,
        ingredients=None,   # cheese builder ships no ingredient text (not yet wired)
        nutrition=nut,      # package nutrition dict: keys energy_kcal, protein_g, fat_g, carbohydrates_g
        trace=None,
    )

    return {
        "id": vm_id(p["barcode"]),
        "name": p["name"].strip(),
        "imageUrl": p.get("image_url") or None,
        "score": disp_score,
        "grade": grade,
        "_aCappedToB": a_capped,
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
    # Display set: apply routing + data withholds. The EV-021 blanket A-ceiling
    # withhold is RETIRED for cheese (Amendment A1); A-eligibility is now a per-product
    # DISPLAY CAP applied inside build_product (visible product, score kept, grade->B).
    disp = [x for x in pkg["products"]
            if not x["_flags"]["misrouted"] and not x["_flags"]["insufficient"]]
    disp.sort(key=lambda d: (-d["score"], str(d["barcode"])))
    products = [build_product(p) for p in disp]

    # Products whose DISPLAYED grade was capped A/S -> B by the Amendment A1 gate.
    # They remain on the shelf (visible) with their numeric score intact.
    a_capped_to_b = [
        {"id": q["id"], "name": q["name"], "score": q["score"], "displayed_grade": q["grade"]}
        for q in products
        if q.get("_aCappedToB")
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
            },
            "a_eligibility_gate": {
                "mechanism": "DISPLAY CAP (not a withhold): A/S-band score that fails the gate keeps its numeric score, stays visible, displays grade B.",
                "predicate": "sodium_mg <= 400 AND fat_saturated_g <= 4.0 (both required; missing data fails closed -> cap to B)",
                "fields": "L1_observed_signals.sodium_mg / L1_observed_signals.fat_saturated_g (carried as nutrition.sodium_mg / nutrition.fat_saturated_g)",
                "scope": "dairy_protein cheese ONLY; gated by BARI_RECAL_P0",
                "capped_count": len(a_capped_to_b),
                "capped_products": a_capped_to_b,
            },
            "governance_ref": pkg["governance_ref"],
            "task": "TASK-169B",
        },
        "recal_governance_note": {
            "status": "RESOLVED",
            "resolution": (
                "Conflict between the run_003 blanket cheese A-ceiling (EV-021 / RULING-DAIRY-A-01 "
                "C1-C6, which set a_eligible_pre_routing=False for ALL cheese) and TASK-169 v1.1 "
                "(owner ruling intending cottage 1% to land at ~90/A) is RESOLVED via EV-021 "
                "AMENDMENT A1 (owner-approved 2026-06-02). The blanket no-A cap for cheese is retired "
                "and replaced by a conditional A-eligibility gate (sodium <= 400 AND sat-fat <= 4.0, "
                "fail-closed on missing data). The gate is a DISPLAY CAP, not a withhold: a failing "
                "product keeps its numeric score and stays on the shelf showing grade B."
            ),
            "evidence_ref": "EV-021 AMENDMENT A1 (03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md)",
            "scope": "dairy_protein (cheese) ONLY; gated by BARI_RECAL_P0; yogurt C1-C6 unchanged.",
            "outcome": "11 A-band products keep A (cottage 1% leads ~90/A); 2 capped to B (9% cottage tier, sat-fat 5.4 > 4.0).",
            "still_staged": "File remains STAGED (page imports unchanged). Product Agent D7 co-sign required before live repoint.",
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
    from collections import Counter
    dist = Counter(q["grade"] for q in products)
    print("WROTE", OUT)
    print("RECAL_P0:", "ON" if RECAL_P0_ON else "OFF", "| products:", len(products),
          "| A->B capped:", len(a_capped_to_b))
    print("displayed grade distribution:", dict(sorted(dist.items())))


if __name__ == "__main__":
    main()
