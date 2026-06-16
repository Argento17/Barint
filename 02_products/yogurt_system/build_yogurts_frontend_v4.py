"""
Build yogurts_frontend_v4.json from run_yogurt_005 BSIP2 traces.

run_yogurt_005 = full re-acquisition from Shufersal (Option A, owner-approved 2026-06-11).
Replaces the thin 11-product yogurts_frontend_v3.json (0 ingredient coverage) with a
full ingredient-bearing corpus. 0 OFF anywhere in the pipeline.

Engine: proto_v0 / 0.4.0 (UNMODIFIED). No manual score edits.
"""
import json, pathlib, sys, logging
from datetime import datetime, timezone

sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")
import frontend_core as FC  # noqa: E402 — grade_from_score, round_score, confidence_from_trace, select_image_url, strip_non_vm_fields

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

TRACES_DIR  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_005\products")
BSIP1_DIR   = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_005\output")
STAGING_OUT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\yogurts_frontend_v4.json")
WEB_OUT     = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v4.json")
RUN_ID      = "run_yogurt_005"

# Subtype -> cluster label (used for _cluster field)
SUBTYPE_CLUSTER = {
    "greek": "greek",
    "high_protein": "high-protein",
    "probiotic": "probiotic",
    "bio": "bio",
    "plain_lowfat": "plain",
    "plain_natural": "plain",
    "flavored": "flavored",
}


def load_trace(pid: str) -> dict:
    p = TRACES_DIR / pid / "bsip2_trace.json"
    return json.loads(p.read_text(encoding="utf-8"))


def load_bsip1(barcode: str) -> dict:
    p = BSIP1_DIR / f"bsip1_{barcode}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def classify_subtype_from_name(name: str) -> str:
    import re
    nl = name.lower() if name else ""
    if re.search(r"יווני|greek|skyr|סקיר", nl):
        return "greek"
    if re.search(r"פרו|pro|go ?20|go20|25g|20g|חלבון|protein", nl):
        return "high_protein"
    if re.search(r"אקטיביה|activia|פרוביו|probiotic", nl):
        return "probiotic"
    if re.search(r"\bביו\b|\bbio\b", nl):
        return "bio"
    if re.search(r"0%|light|free|דל|ללא שומן|נטול", nl):
        return "plain_lowfat"
    if re.search(r"פירות|תות|פטל|אוכמ|וניל|vanil|פרי|בטעם|froop|פרופ|שוקולד|פיר|לימון|אפרסק|מנגו", nl):
        return "flavored"
    return "plain_natural"


def build_insight_line(trace: dict, bsip1: dict) -> str:
    """
    Auto-generate an insight line from the trace data.
    Follows the Bari Assertive Writing standard: finding-first, real driver named.
    """
    l1 = trace.get("L1_observed_signals", {})
    name = (trace.get("input_reference") or {}).get("canonical_name_he") or \
           (trace.get("input_reference") or {}).get("product_name_he") or ""
    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")
    nova = trace.get("nova_proxy")

    protein = l1.get("protein_g")
    fat = l1.get("fat_g")
    sugar = l1.get("sugars_g")
    energy = l1.get("energy_kcal")
    sodium = l1.get("sodium_mg")
    sat_fat = l1.get("fat_saturated_g")

    enrichment = bsip1.get("enrichment_summary", {})
    has_cultures = enrichment.get("has_live_cultures", False)
    additive_count = enrichment.get("additive_count", 0)
    sweetener_count = enrichment.get("sweetener_count", 0)
    ingr_count = enrichment.get("ingredient_count_parsed", 0)

    subtype = bsip1.get("bsip_yogurt_subtype") or classify_subtype_from_name(name)
    binding_cap = trace.get("binding_cap")
    caps = trace.get("caps_considered") or []
    nova4_fired = any(c.get("rule") == "NOVA_PROXY_4_ULTRA_PROCESSED" and c.get("fired") for c in caps)
    additive_cap = any(c.get("rule", "").startswith("ADDITIVE") and c.get("fired") for c in caps)
    sugar_cap = any(c.get("rule", "").startswith("HIGH_SUGAR") and c.get("fired") for c in caps)
    high_cal_sugar_cap = any("HIGH_CAL_HIGH_SUGAR" in c.get("rule", "") and c.get("fired") for c in caps)

    parts = []

    # Leading finding
    if subtype == "high_protein" and protein is not None:
        parts.append(f"{protein:.0f} גרם חלבון ל-100 גרם")
    elif subtype == "greek":
        if fat is not None:
            parts.append(f"יוגורט יווני עם {fat:.1f}% שומן")
    elif subtype in ("bio", "probiotic") and has_cultures:
        parts.append("תרביות חיות מאומתות ברכיבים")
    elif subtype == "plain_natural" or subtype == "plain_lowfat":
        if protein is not None:
            parts.append(f"{protein:.1f} גרם חלבון")

    # Positive signals
    if sugar is not None and sugar < 5 and subtype != "flavored":
        parts.append("סוכר נמוך")
    if additive_count == 0 and ingr_count > 0:
        parts.append("ללא תוספים מזוהים")
    elif additive_count > 0:
        parts.append(f"{additive_count} תוספים ברכיבים")

    # Negative / limiting
    if nova4_fired:
        parts.append("NOVA 4 — עיבוד גבוה מוריד את הציון")
    elif additive_cap:
        parts.append(f"{additive_count} תוספים מגבילים את הציון")
    if sugar is not None and sugar >= 10 and subtype == "flavored":
        parts.append(f"{sugar:.1f} גרם סוכר")
    if sat_fat is not None and sat_fat > 4:
        parts.append(f"{sat_fat:.1f} גרם שומן רווי")

    # Grade close
    if grade in ("B", "C", "D", "E"):
        grade_map = {"B": "B", "C": "C", "D": "D", "E": "E"}
        parts.append(f"ציון {grade_map[grade]}")

    if not parts:
        return f"ציון {grade} — נבדק על בסיס תזונה ורכיבים."

    return " — ".join(parts[:4]) + "."


def build_positive_signals(trace: dict, bsip1: dict) -> list:
    l1 = trace.get("L1_observed_signals", {})
    enrichment = bsip1.get("enrichment_summary", {})
    sigs = []
    protein = l1.get("protein_g")
    sugar = l1.get("sugars_g")
    fat = l1.get("fat_g")
    has_cultures = enrichment.get("has_live_cultures", False)
    additive_count = enrichment.get("additive_count", 0)
    ingr_count = enrichment.get("ingredient_count_parsed", 0)

    if protein is not None and protein >= 8:
        sigs.append(f"חלבון גבוה — {protein:.0f} גרם ל-100 גרם")
    elif protein is not None and protein >= 5:
        sigs.append(f"חלבון — {protein:.1f} גרם ל-100 גרם")
    if sugar is not None and sugar < 5:
        sigs.append(f"סוכר נמוך — {sugar:.1f} גרם ל-100 גרם")
    if has_cultures:
        sigs.append("תרביות חיות ברכיבים")
    if additive_count == 0 and ingr_count > 0:
        sigs.append("ללא תוספים מזוהים")
    if fat is not None and fat < 1:
        sigs.append("דל שומן")
    return sigs[:3]


def build_limiting_factors(trace: dict, bsip1: dict) -> list:
    l1 = trace.get("L1_observed_signals", {})
    enrichment = bsip1.get("enrichment_summary", {})
    caps = trace.get("caps_considered") or []
    lim = []
    sugar = l1.get("sugars_g")
    sat_fat = l1.get("fat_saturated_g")
    additive_count = enrichment.get("additive_count", 0)
    nova = trace.get("nova_proxy")

    nova4_fired = any(c.get("rule") == "NOVA_PROXY_4_ULTRA_PROCESSED" and c.get("fired") for c in caps)
    additive_cap_fired = any(c.get("rule", "").startswith("ADDITIVE") and c.get("fired") for c in caps)
    sugar_cap_fired = any(c.get("rule", "").startswith("HIGH_SUGAR") and c.get("fired") for c in caps)

    if nova4_fired:
        lim.append("NOVA 4 — עיבוד גבוה")
    elif nova == 4:
        lim.append("NOVA 4")
    if additive_cap_fired or additive_count >= 3:
        lim.append(f"{additive_count} תוספים מזוהים")
    if sugar is not None and sugar >= 10:
        lim.append(f"סוכר גבוה — {sugar:.1f} גרם ל-100 גרם")
    elif sugar_cap_fired and sugar is not None:
        lim.append(f"סוכר — {sugar:.1f} גרם ל-100 גרם")
    if sat_fat is not None and sat_fat > 4:
        lim.append(f"שומן רווי — {sat_fat:.1f} גרם ל-100 גרם")
    return lim[:3]


def build_unknowns(l1: dict) -> list:
    unknowns = []
    if l1.get("sugars_g") is None:
        unknowns.append("ערכי הסוכר לא היו זמינים במקור הנתונים — מדד זה לא נכלל בניתוח.")
    if l1.get("fat_saturated_g") is None:
        unknowns.append("ערכי שומן הרווי לא היו זמינים במקור הנתונים.")
    if l1.get("dietary_fiber_g") is None:
        unknowns.append("ערכי הסיבים לא היו זמינים במקור הנתונים.")
    return unknowns[:2]


def main():
    # Discover all trace directories
    if not TRACES_DIR.exists():
        log.error("Traces dir not found: %s", TRACES_DIR)
        return

    trace_dirs = [d for d in TRACES_DIR.iterdir() if d.is_dir()]
    log.info("Found %d trace directories", len(trace_dirs))

    products_raw = []
    errors = []
    for td in trace_dirs:
        trace_file = td / "bsip2_trace.json"
        if not trace_file.exists():
            continue
        try:
            trace = json.loads(trace_file.read_text(encoding="utf-8"))
            pid = td.name  # e.g. bsip1_yogurt_7290112336712
            barcode = (trace.get("input_reference") or {}).get("barcode") or pid.replace("bsip1_yogurt_", "").replace("bsip1_", "")
            barcode = str(barcode).strip()
            name = (trace.get("input_reference") or {}).get("canonical_name_he") or \
                   (trace.get("input_reference") or {}).get("product_name_he") or barcode

            bsip1 = load_bsip1(barcode)

            raw_score = trace.get("final_score_estimate")
            grade_engine = trace.get("grade_estimate")

            # "No S grades" policy (TASK-169D, frozen): any yogurt score > 89.9 → 89.9.
            # BARI_RECAL_P0_YOGURT_TRIM has a Path A gap (ingredient-keyword fermentation
            # bonus not capped at engine level). Post-processing cap applied here before
            # grade derivation so the grade always derives from the capped score.
            if raw_score is not None and raw_score > 89.9:
                raw_score = 89.9

            score = FC.round_score(raw_score)
            grade = FC.grade_from_score(score)

            # Confidence from trace
            conf_fields = FC.confidence_from_trace(trace)

            # Image URL — from BSIP1 record (scraped directly from Shufersal)
            image_url = FC.select_image_url(bsip1, trace)

            # Nutrition
            l1 = trace.get("L1_observed_signals", {})
            nutrition = {
                "energyKcal": l1.get("energy_kcal"),
                "protein": l1.get("protein_g"),
                "sugar": l1.get("sugars_g"),
                "fat": l1.get("fat_g"),
                "satFat": l1.get("fat_saturated_g"),
                "fiber": l1.get("dietary_fiber_g"),
                "sodium": l1.get("sodium_mg"),
            }

            # Ingredients — real Hebrew text from BSIP1 (run_yogurt_005 has real ingredient panels)
            ingr_text = bsip1.get("ingredients_text_he") or None

            # Signals
            positive_signals = build_positive_signals(trace, bsip1)
            limiting_factors = build_limiting_factors(trace, bsip1)
            unknowns = build_unknowns(l1)
            insight_line = build_insight_line(trace, bsip1)

            # Subtype -> cluster
            subtype = bsip1.get("bsip_yogurt_subtype") or classify_subtype_from_name(name)
            cluster = SUBTYPE_CLUSTER.get(subtype, "plain")

            product = {
                "id": pid,
                "name": name,
                "imageUrl": image_url,
                "score": score,
                "grade": grade,
                "confidence": conf_fields["confidence"],
                "confidence_label_he": conf_fields["confidence_label_he"],
                "confidence_tooltip_he": conf_fields["confidence_tooltip_he"],
                "confidence_sub_reason": conf_fields["confidence_sub_reason"],
                "insightLine": insight_line,
                "_cluster": cluster,
                "barcode": barcode,
                "retailer": "shufersal",
                "expansion": {
                    "nutrition": nutrition,
                    "ingredients": ingr_text,
                    "confidenceLabel": conf_fields["confidence_label_he"],
                    "servingNote": "ל-100 גרם",
                    "positiveSignals": positive_signals,
                    "limitingFactors": limiting_factors,
                    "unknowns": unknowns,
                    "bottomLine": None,
                    "comparisonContext": None,
                },
            }

            products_raw.append((score or 0, product))

        except Exception as e:
            log.error("Error processing %s: %s", td.name, e)
            import traceback; traceback.print_exc()
            errors.append(str(td.name))

    # Sort by score descending
    products_raw.sort(key=lambda x: -x[0])
    products = [p for _, p in products_raw]

    log.info("Built %d products, %d errors", len(products), len(errors))

    # Grade distribution
    grade_dist = {}
    for p in products:
        g = p.get("grade", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    # Retailer breakdown
    retailer_dist = {}
    for p in products:
        r = p.get("retailer", "unknown")
        retailer_dist[r] = retailer_dist.get(r, 0) + 1

    # Ingredient coverage
    n_with_ingr = sum(1 for p in products if p.get("expansion", {}).get("ingredients"))

    payload = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "category": "yogurts",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v4",
            "run_id": RUN_ID,
            "provenance": (
                "run_yogurt_005: Shufersal direct scrape (html_parse), real Hebrew ingredients, "
                "BARI_RECAL_P0_YOGURT_TRIM + 89.9 post-cap applied. "
                "Full re-acquisition per owner Option A + recal approval 2026-06-11. "
                "0 OFF anywhere in pipeline."
            ),
            "engine": "proto_v0 / 0.4.0 (unmodified)",
            "s_grade_cap_applied": True,
            "s_grade_cap_note": (
                "Hard 89.9 cap applied post-processing per TASK-169D 'no S grades' policy. "
                "BARI_RECAL_P0_YOGURT_TRIM has a Path A gap (ingredient-keyword fermentation "
                "bonus not capped at engine level). 1 product affected: 7290112336712 "
                "(90.4→89.9/A). Engine fix tracked separately."
            ),
            "retailer_breakdown": retailer_dist,
            "grade_distribution": grade_dist,
            "ingredient_coverage": f"{n_with_ingr}/{len(products)}",
            "bsip0_gate": "PASS (96 products scraped, 92% nutrition, 92% ingredients)",
            "bsip1_included": len(products),
            "bsip1_excluded": 7,
            "bsip1_exclusion_reason": "no_usable_nutrition (all 7)",
            "off_in_pipeline": False,
        },
        "products": products,
    }

    # Apply the VM field allowlist strip (keeps _cluster as load-bearing field)
    payload["products"] = [FC.strip_non_vm_fields(p, keep=("_cluster",)) for p in products]
    # Restore retailer (in allowlist) and barcode (in allowlist)

    # Write staging
    STAGING_OUT.parent.mkdir(parents=True, exist_ok=True)
    STAGING_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Staging: %s", STAGING_OUT)

    # Write web staging (v4 — does NOT overwrite v3)
    WEB_OUT.parent.mkdir(parents=True, exist_ok=True)
    WEB_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Web staging: %s", WEB_OUT)

    # Summary
    print("\n=== yogurts_frontend_v4.json build complete ===")
    print(f"Products: {len(products)}")
    print(f"Grade distribution: {grade_dist}")
    print(f"Ingredient coverage: {n_with_ingr}/{len(products)}")
    print(f"Errors: {len(errors)}")
    if errors:
        print(f"  Error list: {errors}")
    print(f"Staging: {STAGING_OUT}")
    print(f"Web:     {WEB_OUT}")


if __name__ == "__main__":
    main()
