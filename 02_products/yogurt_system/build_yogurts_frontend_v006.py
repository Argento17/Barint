"""
Build yogurts_frontend_v006_staging.json from run_yogurt_006 BSIP2 traces.

run_yogurt_006 = TASK-250 rulings applied on top of run_yogurt_005 corpus:
  - Ruling 1: null sugar_g → confidence −10 (confidence_band → partial for null-sugar A products)
  - Ruling 2: null fat_saturated_g → confidence −5
  - Ruling 3: grade-before-round FIX — grade assigned from raw score, display score is rounded
  - Ruling 4: NOT APPLICABLE — "sweeteners" in BSIP1 are added sugars (honey/table sugar),
              not non-nutritive; sweetener cap correctly does not fire; no cap change
  - Ruling 5: barcode 7290116932620 excluded (protein=190 corruption); caveat copy update
              is Content Agent scope

GRADE-BEFORE-ROUND FIX (Ruling 3):
  The run_005 builder used grade_from_score(round(raw)) which caused two grade promotions:
    - 7290114313070 (יוגורט מוקצף אפרסק): raw=34.8 → round=35 → grade D (wrong: should be E)
    - 7290102399819 (מולר פרוטאין יוגור.פירות): raw=49.6 → round=50 → grade C (wrong: should be D)
  Fix: grade_from_score(raw) THEN round_score(raw). Display score is still 35 or 50.

STAGING NOTE (OWNER TRIPWIRE — Ruling 3):
  The run_006 frontend JSON is written to a STAGING path only.
  It must NOT be written to bari-web/src/data/ until the owner signs off on the grade
  corrections (two products change grade: 35/D→35/E and 50/C→50/D).
  Staging path: C:\\Bari\\02_products\\yogurt_system\\yogurts_frontend_v006_staging.json
  Live path (locked, do not write until owner sign-off):
    C:\\Bari\\bari-web\\src\\data\\comparisons\\yogurts_frontend_v006.json

0 OFF anywhere in this pipeline.
"""
import json, pathlib, sys, logging
from datetime import datetime, timezone

_SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(_SRC))

# frontend_core is distributed as a compiled .pyc only (no .py source).
# Use importlib to load it directly from the __pycache__ file.
import importlib.util as _ilu
_fc_pyc = _SRC / "__pycache__" / "frontend_core.cpython-314.pyc"
_fc_spec = _ilu.spec_from_file_location("frontend_core", str(_fc_pyc))
FC = _ilu.module_from_spec(_fc_spec)
_fc_spec.loader.exec_module(FC)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

TRACES_DIR   = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006\products")
BSIP1_DIR    = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_005\output")
# STAGING ONLY — do not write to bari-web until owner sign-off on Ruling 3 grade corrections
STAGING_OUT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\yogurts_frontend_v006_staging.json")
# LIVE path — locked pending owner sign-off on Ruling 3
# WEB_OUT = pathlib.Path(r"C:\Bari\bari-web\src\data\comparisons\yogurts_frontend_v006.json")
RUN_ID = "run_yogurt_006"

# Subtype -> cluster label
SUBTYPE_CLUSTER = {
    "greek": "greek",
    "high_protein": "high-protein",
    "probiotic": "probiotic",
    "bio": "bio",
    "plain_lowfat": "plain",
    "plain_natural": "plain",
    "flavored": "flavored",
}


def load_trace(trace_dir: pathlib.Path) -> dict:
    p = trace_dir / "bsip2_trace.json"
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
    l1 = trace.get("L1_observed_signals", {})
    name = (trace.get("input_reference") or {}).get("canonical_name_he") or \
           (trace.get("input_reference") or {}).get("product_name_he") or ""
    grade = trace.get("grade_estimate")
    nova = trace.get("nova_proxy")

    protein = l1.get("protein_g")
    fat = l1.get("fat_g")
    sugar = l1.get("sugars_g")
    sat_fat = l1.get("fat_saturated_g")

    enrichment = bsip1.get("enrichment_summary", {})
    has_cultures = enrichment.get("has_live_cultures", False)
    additive_count = enrichment.get("additive_count", 0)
    ingr_count = enrichment.get("ingredient_count_parsed", 0)

    subtype = bsip1.get("bsip_yogurt_subtype") or classify_subtype_from_name(name)
    binding_cap = trace.get("binding_cap")
    caps = trace.get("caps_considered") or []
    nova4_fired = any(c.get("rule") == "NOVA_PROXY_4_ULTRA_PROCESSED" and c.get("fired") for c in caps)
    additive_cap = any(c.get("rule", "").startswith("ADDITIVE") and c.get("fired") for c in caps)
    sugar_cap = any(c.get("rule", "").startswith("HIGH_SUGAR") and c.get("fired") for c in caps)

    parts = []

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

    if sugar is not None and sugar < 5 and subtype != "flavored":
        parts.append("סוכר נמוך")
    if additive_count == 0 and ingr_count > 0:
        parts.append("ללא תוספים מזוהים")
    elif additive_count > 0:
        parts.append(f"{additive_count} תוספים ברכיבים")

    if nova4_fired:
        parts.append("NOVA 4 — עיבוד גבוה מוריד את הציון")
    elif additive_cap:
        parts.append(f"{additive_count} תוספים מגבילים את הציון")
    if sugar is not None and sugar >= 10 and subtype == "flavored":
        parts.append(f"{sugar:.1f} גרם סוכר")
    if sat_fat is not None and sat_fat > 4:
        parts.append(f"{sat_fat:.1f} גרם שומן רווי")

    if grade in ("B", "C", "D", "E"):
        parts.append(f"ציון {grade}")

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
    if not TRACES_DIR.exists():
        log.error("run_006 traces dir not found: %s", TRACES_DIR)
        log.error("Run batch_run_yogurt_006.py first to generate traces.")
        return

    trace_dirs = [d for d in TRACES_DIR.iterdir() if d.is_dir()]
    log.info("Found %d run_006 trace directories", len(trace_dirs))

    products_raw = []
    errors = []
    grade_corrections = []   # track Ruling 3 corrections for the return block

    for td in trace_dirs:
        trace_file = td / "bsip2_trace.json"
        if not trace_file.exists():
            continue
        try:
            trace = json.loads(trace_file.read_text(encoding="utf-8"))
            pid = td.name
            barcode = (trace.get("input_reference") or {}).get("barcode") or \
                      pid.replace("bsip1_yogurt_", "").replace("bsip1_", "")
            barcode = str(barcode).strip()
            name = (trace.get("input_reference") or {}).get("canonical_name_he") or \
                   (trace.get("input_reference") or {}).get("product_name_he") or barcode

            bsip1 = load_bsip1(barcode)

            raw_score = trace.get("final_score_estimate")

            # "No S grades" policy (TASK-169D, frozen): any yogurt score > 89.9 → 89.9.
            if raw_score is not None and raw_score > 89.9:
                raw_score = 89.9

            # RULING 3 (TASK-250): grade-before-round.
            # Grade is derived from raw_score BEFORE rounding. Display score is rounded.
            # This corrects the run_005 builder error (grade_from_score(round(raw))).
            grade_raw_would_be = FC.grade_from_score(FC.round_score(raw_score))  # old (buggy) method
            grade = FC.grade_from_score(raw_score)                               # new (correct) method
            score = FC.round_score(raw_score)

            if grade != grade_raw_would_be:
                grade_corrections.append({
                    "barcode": barcode, "name": name,
                    "raw_score": raw_score, "display_score": score,
                    "grade_run005_buggy": grade_raw_would_be,
                    "grade_run006_correct": grade,
                })
                log.warning("  RULING3 GRADE CORRECTION: %s (%s) raw=%.1f display=%s "
                            "grade: %s → %s",
                            barcode, name, raw_score, score,
                            grade_raw_would_be, grade)

            # Confidence from trace
            conf_fields = FC.confidence_from_trace(trace)

            # Image URL
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

            # Ingredients
            ingr_text = bsip1.get("ingredients_text_he") or None

            positive_signals = build_positive_signals(trace, bsip1)
            limiting_factors = build_limiting_factors(trace, bsip1)
            unknowns = build_unknowns(l1)
            insight_line = build_insight_line(trace, bsip1)

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

    products_raw.sort(key=lambda x: -x[0])
    products = [p for _, p in products_raw]

    log.info("Built %d products, %d errors", len(products), len(errors))
    if grade_corrections:
        log.info("Ruling 3 grade corrections (%d):", len(grade_corrections))
        for c in grade_corrections:
            log.info("  %s (%s): raw=%.1f display=%s %s → %s",
                     c["barcode"], c["name"], c["raw_score"], c["display_score"],
                     c["grade_run005_buggy"], c["grade_run006_correct"])

    grade_dist = {}
    for p in products:
        g = p.get("grade", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    retailer_dist = {}
    for p in products:
        r = p.get("retailer", "unknown")
        retailer_dist[r] = retailer_dist.get(r, 0) + 1

    n_with_ingr = sum(1 for p in products if p.get("expansion", {}).get("ingredients"))

    payload = {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "category": "yogurts",
            "product_count": len(products),
            "scored_count": len(products),
            "schema": "BariProductVM[]",
            "version": "v006",
            "run_id": RUN_ID,
            "staging": True,
            "staging_note": (
                "STAGED — NOT LIVE. Owner sign-off required before publishing to bari-web "
                "(Ruling 3 changes two product grades: 35/D→35/E and 50/C→50/D). "
                "See TASK-250 Ruling 3 and TASK-249 pre-conditions."
            ),
            "owner_tripwire_pending": "Ruling 3 grade corrections require owner sign-off",
            "grade_corrections_ruling3": grade_corrections,
            "provenance": (
                "run_yogurt_006: TASK-250 rulings on top of run_yogurt_005 corpus. "
                "Ruling 1: null sugar_g −10 confidence. "
                "Ruling 2: null satFat −5 confidence. "
                "Ruling 3: grade-before-round (builder fix). "
                "Ruling 4: not applicable (products contain added sugars, not non-nutritive sweeteners). "
                "Ruling 5: barcode 7290116932620 excluded (protein=190 corruption). "
                "0 OFF anywhere in pipeline."
            ),
            "engine": "proto_v0 / 0.4.0 + BARI_RECAL_P0_YOGURT_TRIM + BARI_TASK250_CONF",
            "s_grade_cap_applied": True,
            "retailer_breakdown": retailer_dist,
            "grade_distribution": grade_dist,
            "ingredient_coverage": f"{n_with_ingr}/{len(products)}",
            "off_in_pipeline": False,
        },
        "products": products,
    }

    payload["products"] = [FC.strip_non_vm_fields(p, keep=("_cluster",)) for p in products]

    STAGING_OUT.parent.mkdir(parents=True, exist_ok=True)
    STAGING_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Staging: %s", STAGING_OUT)
    log.info("OWNER SIGN-OFF REQUIRED before writing to bari-web (Ruling 3 grade corrections).")

    print("\n=== yogurts_frontend_v006_staging.json build complete ===")
    print(f"Products: {len(products)}")
    print(f"Grade distribution: {grade_dist}")
    print(f"Ingredient coverage: {n_with_ingr}/{len(products)}")
    print(f"Errors: {errors}")
    if grade_corrections:
        print(f"\nRuling 3 grade corrections ({len(grade_corrections)}):")
        for c in grade_corrections:
            print(f"  {c['barcode']} ({c['name']}): "
                  f"raw={c['raw_score']:.1f} display={c['display_score']} "
                  f"{c['grade_run005_buggy']} → {c['grade_run006_correct']}")
    print(f"\nSTAGING: {STAGING_OUT}")
    print("LIVE PATH (LOCKED): requires owner sign-off on Ruling 3.")


if __name__ == "__main__":
    main()
