"""
Stage 7 — Frontend packaging for cottage / white cheese (run_cheese_001).

Builds a frontend_package.json from BSIP2 traces + BSIP1 cheese governance constructs.
Marked NON-AUTHORITATIVE: the QA misroute gate (47.4% > 5%, QA-CHS-001 router cream-cheese-anchor
gap) failed and Nutrition approval is pending, so this package is a factory artifact, NOT promoted
to the live website (run_cereals_002 / run_yogurt_003 discipline: do not ship a failing orphan).

Wires the TWO Product-Owner-approved Sec 6.4 disclosure texts (TASK-141 Resolution 3):
  - category-wide sodium / saturated-fat note (DISTORTION-010) — all pools
  - pool-specific reduced-fat reformulation note (DISTORTION-006/009) — cream + light products only

Output: 02_products/cheese_spreads/factory_run_001/frontend_package.json
"""
from __future__ import annotations
import sys, json, glob, pathlib
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TRACES = glob.glob(r"C:\Bari\02_products\cheese_spreads\bsip2_outputs\run_cheese_003\products\**\bsip2_trace.json", recursive=True)
BSIP1  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_003\output")
CONSTRUCTS = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cheese_003\cheese_constructs_report.json")
OUT = pathlib.Path(r"C:\Bari\02_products\cheese_spreads\factory_run_003\frontend_package.json")

DAIRY_OK = {"dairy_protein", "dairy", "dairy_system", "cheese", "cheese_spreads"}

def load_bsip1(barcode):
    f = BSIP1 / f"bsip1_{barcode}.json"
    return json.load(open(f, encoding="utf-8")) if f.exists() else {}

products = []
for tf in TRACES:
    t = json.load(open(tf, encoding="utf-8"))
    ref = t.get("input_reference") or {}
    barcode = ref.get("barcode") or (ref.get("canonical_product_id") or "").replace("bsip1_cheese_", "")
    b1 = load_bsip1(barcode)
    gov = b1.get("cheese_governance", {})
    cat = t.get("category")
    misrouted = cat not in DAIRY_OK
    nn = b1.get("normalized_nutrition_per_100g", {})
    name_he = b1.get("canonical_name_he") or ref.get("product_name_he") or ""
    grade = t.get("grade_estimate")
    ac = (gov.get("construct_5_a_ceiling") or {})
    light = (gov.get("construct_3_light") or {})
    ferment = (gov.get("construct_4_fermentation") or {})
    # A-ceiling withhold: a grade-A product that is NOT A-eligible (C1-C6) must be withheld.
    a_ceiling_withhold = (grade == "A" and ac.get("a_eligible_pre_routing") is False)
    insufficient = (t.get("data_sufficiency") == "insufficient" or t.get("final_score_estimate") is None)
    pool = b1.get("bsip_cheese_subpool", "unknown")
    products.append({
        "id": ref.get("canonical_product_id"),
        "barcode": barcode,
        "name": name_he,
        "brand": b1.get("brand", ""),
        "score": t.get("final_score_estimate"),
        "grade": grade,
        "confidence_level": "verified" if (b1.get("data_sufficiency") == "sufficient" and not insufficient) else "insufficient",
        "image_url": b1.get("image_url"),
        "ingredients_he": b1.get("ingredients_text_he", ""),
        "nutrition": {
            "energy_kcal": nn.get("energy_kcal"), "protein_g": nn.get("protein_g"),
            "carbohydrates_g": nn.get("carbohydrates_g"), "sugars_g": nn.get("sugars_g"),
            "dietary_fiber_g": nn.get("dietary_fiber_g"), "fat_g": nn.get("fat_g"),
            "fat_saturated_g": nn.get("fat_saturated_g"), "sodium_mg": nn.get("sodium_mg"),
        },
        "subpool": pool,
        "light_claim": light.get("light_claim_present", False),
        "light_supported": light.get("reduced_fat_threshold_met_ge25pct"),
        "marketing_divergence_finding": light.get("marketing_divergence_finding", False),
        "culture_credited": ferment.get("fermentation_credit_applied", False),
        "a_eligible_pre_routing": ac.get("a_eligible_pre_routing"),
        "nova_proxy": t.get("nova_proxy"),
        "routed_category": cat,
        "_flags": {
            "misrouted": misrouted,
            "a_ceiling_withhold": a_ceiling_withhold,
            "insufficient": insufficient,
        },
        "display_approved": (not misrouted) and (not a_ceiling_withhold) and (not insufficient),
    })

products.sort(key=lambda p: (p["subpool"], -(p["score"] or 0)))
constructs = json.load(open(CONSTRUCTS, encoding="utf-8")) if CONSTRUCTS.exists() else {}
heb = sum(1 for p in products if any("א" <= c <= "ת" for c in p["name"]))
display_approved = [p for p in products if p["display_approved"]]
endemic = (constructs.get("construct_6_endemic_distortion") or {})

package = {
    "schema": "bari_frontend_package_v1",
    "category_slug": "cheese-spreads",
    "name_he": "גבינות לבנות וממרחים",
    "run_id": "run_cheese_003",
    "generated": datetime.now(timezone.utc).isoformat(),
    "authoritative": False,
    "promoted_to_frontend": False,
    "non_authoritative_reason": "run_cheese_003 = re-scrape + re-build + re-score on EV-029-CORRECTED fat/saturated data (TASK-142A parser fix; engine 0.4.0 UNMODIFIED). Data/routing/plausibility gates GREEN: misroute 1.7% (<5%), COV-006 plausibility 0.0% implausible (was 31.9% on the corrupt corpus), fat sane across all 4 sub-pools. NON-AUTHORITATIVE pending Nutrition/Product grade-publication sign-off. NOTE: scores shifted materially vs run_002 — cream-cheese now scores on REAL high fat (25-32%, was falsely 0.5g) so the pool grades lower/truthfully; and 5 products are withheld as transparency-tier on GENUINE partial Shufersal panels (total fat/protein/carbs omitted at source). run_002's literal '0/57 insufficient' was itself an artifact of the EV-029 bug injecting fake fat that made partial panels look complete.",
    "rtl": True,
    "language": "he",
    "engine": "proto_v0 / 0.4.0 (unmodified)",
    "governance_ref": "cheese_spreads_stress_test_001 (TASK-141, verdict B); dairy calibration TASK-139A/B/D",
    "counts": {
        "total": len(products),
        "display_approved": len(display_approved),
        "withheld_misrouted": sum(1 for p in products if p["_flags"]["misrouted"]),
        "withheld_a_ceiling": sum(1 for p in products if p["_flags"]["a_ceiling_withhold"]),
        "withheld_insufficient": sum(1 for p in products if p["_flags"]["insufficient"] and not p["_flags"]["misrouted"]),
        "hebrew_name_coverage": f"{heb}/{len(products)}",
    },
    "subpools": {
        "cottage": {"name_he": "גבינת קוטג'"},
        "white_cheese_quark": {"name_he": "גבינה לבנה / קוורק"},
        "labaneh": {"name_he": "לבנה"},
        "cream_cheese_spread": {"name_he": "גבינת שמנת / ממרח גבינה"},
    },
    "rtl_labels_he": {
        "score": "ציון", "grade": "דירוג", "ingredients": "רכיבים", "nutrition": "ערכים תזונתיים",
        "energy": "אנרגיה (קק\"ל)", "protein": "חלבון", "carbs": "פחמימות", "sugars": "מתוכן סוכרים",
        "fiber": "סיבים תזונתיים", "fat": "שומן", "saturated_fat": "מתוכו רווי", "sodium": "נתרן",
        "cottage": "קוטג'", "white_cheese_quark": "גבינה לבנה / קוורק", "labaneh": "לבנה",
        "cream_cheese_spread": "גבינת שמנת / ממרח גבינה",
        "light_claim": "דל שומן / לייט", "reduced_fat_supported": "הפחתת שומן מאומתת (>=25%)",
        "marketing_divergence": "טענת שיווק שאינה נתמכת", "live_culture": "תרבית חיה"
    },
    "category_grade_thresholds_engine": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
    "disclosures_sec_6_4": {
        "category_wide_sodium_satfat": {
            "scope": "all pools (DISTORTION-010, endemic)",
            "approved": "Product Owner 2026-06-01 (TASK-141 Resolution 3)",
            "text_he": (endemic.get("category_wide_sodium_satfat") or {}).get("category_note_he"),
        },
        "pool_specific_light_reformulation": {
            "scope": "cream-cheese + light products only (DISTORTION-006/009); must NOT appear on plain cottage/labaneh cards",
            "approved": "Product Owner 2026-06-01 (TASK-141 Resolution 3)",
            "applies_to_pools": ["cream_cheese_spread"],
            "text_he": (endemic.get("pool_specific_light_reformulation") or {}).get("category_note_he"),
        },
    },
    "constructs_summary": {
        "subpool_counts": (constructs.get("construct_1_subpools") or {}).get("pool_counts"),
        "developmental_pool": (constructs.get("construct_2_developmental") or {}).get("developmental_pool_count"),
        "light_claims": (constructs.get("construct_3_light") or {}).get("light_claims_count"),
        "marketing_divergence_findings": (constructs.get("construct_3_light") or {}).get("marketing_divergence_findings"),
        "culture_credited": (constructs.get("construct_4_fermentation") or {}).get("culture_credited_count"),
        "ev015_violations": (constructs.get("construct_4_fermentation") or {}).get("ev015_flavor_vs_marker_violations"),
        "a_eligible_pre_routing": (constructs.get("construct_5_a_ceiling") or {}).get("a_eligible_pre_routing_count"),
    },
    "products": products,
}
OUT.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {OUT}")
print(f"total={len(products)} display_approved={len(display_approved)} "
      f"withheld_misrouted={package['counts']['withheld_misrouted']} "
      f"withheld_a_ceiling={package['counts']['withheld_a_ceiling']} "
      f"withheld_insufficient={package['counts']['withheld_insufficient']} hebrew={heb}/{len(products)}")
