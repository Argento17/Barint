"""
Stage 7 — Frontend packaging for breakfast cereals (run_cereals_002).

Builds a frontend_package.json from BSIP2 traces + BSIP1 governance constructs.
Marked NON-AUTHORITATIVE: the QA misroute gate (7.6% > 5%) failed and Nutrition
approval is pending, so this package is a factory artifact, NOT promoted to the
live website (run_yogurt_003 discipline: do not ship a failing orphan).

Output: 02_products/breakfast_cereals/factory_run_002/frontend_package.json
"""
from __future__ import annotations
import sys, json, glob, pathlib
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TRACES = glob.glob(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_002\products\**\bsip2_trace.json", recursive=True)
BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_002\output")
CONSTRUCTS = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_002\cereals_constructs_report.json")
OUT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\factory_run_002\frontend_package.json")

CEREAL_OK = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}

def load_bsip1(barcode):
    f = BSIP1 / f"bsip1_{barcode}.json"
    return json.load(open(f, encoding="utf-8")) if f.exists() else {}

products = []
for tf in TRACES:
    t = json.load(open(tf, encoding="utf-8"))
    ref = t.get("input_reference") or {}
    barcode = (t.get("canonical_product_id") or "").replace("bsip1_cereal_", "")
    b1 = load_bsip1(barcode)
    gov = b1.get("cereals_governance", {})
    cat = t.get("category")
    misrouted = cat not in CEREAL_OK
    nn = b1.get("normalized_nutrition_per_100g", {})
    name_he = b1.get("canonical_name_he") or ref.get("product_name_he") or ""
    # Shaped/baked/extruded cereal reading NOVA 1 -> likely under-call (QA-CER-W1)
    shaped = any(tok in name_he for tok in ["אפוי", "כוכב", "טבעות", "כריות", "פצפוצ", "מנופח"])
    nova_review = (t.get("nova_proxy") == 1 and shaped)
    products.append({
        "id": t.get("canonical_product_id"),
        "barcode": barcode,
        "name": name_he,
        "brand": b1.get("brand", ""),
        "score": t.get("final_score_estimate"),
        "grade": t.get("grade_estimate"),
        "confidence_level": "verified" if b1.get("data_sufficiency") == "sufficient" else "insufficient",
        "image_url": b1.get("image_url"),
        "ingredients_he": b1.get("ingredients_text_he", ""),
        "nutrition": {
            "energy_kcal": nn.get("energy_kcal"), "protein_g": nn.get("protein_g"),
            "carbohydrates_g": nn.get("carbohydrates_g"), "sugars_g": nn.get("sugars_g"),
            "dietary_fiber_g": nn.get("dietary_fiber_g"), "fat_g": nn.get("fat_g"),
            "fat_saturated_g": nn.get("fat_saturated_g"), "sodium_mg": nn.get("sodium_mg"),
        },
        "subtype": b1.get("bsip_cereal_subtype"),
        "subpool": (gov.get("construct_1_granola_subpool") or {}).get("subpool", "standard_cereal"),
        "is_childrens": (gov.get("construct_2_childrens") or {}).get("is_childrens_product", False),
        "whole_grain_claim": (gov.get("construct_3_whole_grain") or {}).get("whole_grain_claim_present", False),
        "marketing_divergence_finding": (gov.get("construct_3_whole_grain") or {}).get("marketing_divergence_finding", False),
        "fortified": (gov.get("construct_4_fortification_flag") or {}).get("fortified", False),
        "nova_proxy": t.get("nova_proxy"),
        "routed_category": cat,
        "_flags": {
            "misrouted": misrouted,
            "nova1_shaped_cereal_review": nova_review,
        },
        "display_approved": (not misrouted) and not nova_review,
    })

products.sort(key=lambda p: -(p["score"] or 0))
constructs = json.load(open(CONSTRUCTS, encoding="utf-8")) if CONSTRUCTS.exists() else {}
heb = sum(1 for p in products if any("א" <= c <= "ת" for c in p["name"]))
display_approved = [p for p in products if p["display_approved"]]

package = {
    "schema": "bari_frontend_package_v1",
    "category_slug": "breakfast-cereals",
    "run_id": "run_cereals_002",
    "generated": datetime.now(timezone.utc).isoformat(),
    "authoritative": False,
    "promoted_to_frontend": False,
    "non_authoritative_reason": "QA misroute gate FAILED (7.6% > 5%, QA-CER-001 router cereal-anchor gap) and Nutrition approval pending (NOVA-1 baked-flake A's). Factory artifact only; NOT shipped to live site.",
    "rtl": True,
    "language": "he",
    "counts": {
        "total": len(products),
        "display_approved": len(display_approved),
        "withheld_misrouted": sum(1 for p in products if p["_flags"]["misrouted"]),
        "withheld_nova_review": sum(1 for p in products if p["_flags"]["nova1_shaped_cereal_review"] and not p["_flags"]["misrouted"]),
        "hebrew_name_coverage": f"{heb}/{len(products)}",
    },
    "rtl_labels_he": {
        "score": "ציון", "grade": "דירוג", "ingredients": "רכיבים", "nutrition": "ערכים תזונתיים",
        "energy": "אנרגיה (קק\"ל)", "protein": "חלבון", "carbs": "פחמימות", "sugars": "מתוכן סוכרים",
        "fiber": "סיבים תזונתיים", "fat": "שומן", "saturated_fat": "מתוכו רווי", "sodium": "נתרן",
        "granola_pool": "גרנולה", "standard_pool": "דגני בוקר", "whole_grain": "דגנים מלאים",
        "fortified": "מועשר בוויטמינים ומינרלים", "childrens": "מוצר לילדים"
    },
    "category_grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
    "category_distortion_note": (constructs.get("construct_4_fortification_endemic") or {}),
    "constructs_summary": {
        "granola_subpool": constructs.get("construct_1_granola_subpool", {}).get("granola_pool_count"),
        "childrens_pool": constructs.get("construct_2_childrens", {}).get("developmental_pool_count"),
        "childrens_candidates_for_review": len((constructs.get("construct_2_childrens", {}) or {}).get("single_indicator_candidates_for_ce_review", [])),
        "whole_grain_claims": constructs.get("construct_3_whole_grain", {}).get("products_with_whole_grain_claim"),
        "marketing_divergence_findings": constructs.get("construct_3_whole_grain", {}).get("marketing_divergence_findings"),
        "fortification_pct": constructs.get("construct_4_fortification_endemic", {}).get("fortified_pct"),
        "fortification_endemic": constructs.get("construct_4_fortification_endemic", {}).get("is_endemic"),
    },
    "products": products,
}
OUT.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"total={len(products)} display_approved={len(display_approved)} "
      f"withheld_misrouted={package['counts']['withheld_misrouted']} "
      f"withheld_nova={package['counts']['withheld_nova_review']} hebrew={heb}/{len(products)}")
