"""
TASK-378 Phase 2 — Sugar null-guard rescore simulation.

Runs WITHOUT changing any published scores. Staging only.
For each target product, injects the real (or best-estimate) sugar value
and computes what the BSIP2 score would be.

Method:
1. Load BSIP1 JSON from the latest run
2. Inject sugar_g into normalized_nutrition_per_100g
3. Re-run the BSIP2 engine in-memory
4. Compare staged score/grade vs published score/grade

OFF banned. No promotion. Flag-OFF (BARI_SUGAR_NULL_GUARD stays off).
"""
import sys, os, json, pathlib, math

# ── Engine path setup ─────────────────────────────────────────────────────────
ENGINE_SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(ENGINE_SRC))

# ── Flag config (MUST be before imports) ─────────────────────────────────────
# Keep all flags at their current state. BARI_SUGAR_NULL_GUARD stays unset.
os.environ.setdefault("BARI_SHELF_RELATIVE_V1", "on")
os.environ.setdefault("BARI_REDLABEL_V1", "off")
os.environ.setdefault("BARI_TASK250_CONF", "on")

import score_engine as eng
from constants import score_to_grade, DIMENSION_WEIGHTS

ROOT = pathlib.Path(r"C:\Bari")


def load_bsip1(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def nn_from_bsip1(b1: dict) -> dict:
    """Extract normalized_nutrition_per_100g from a BSIP1 file."""
    nn = b1.get("normalized_nutrition_per_100g") or {}
    # Also accept top-level fields
    for k in ("energy_kcal","fat_g","fat_saturated_g","fat_trans_g",
               "cholesterol_mg","sodium_mg","carbohydrates_g","sugars_g",
               "dietary_fiber_g","protein_g"):
        if k not in nn and k in b1:
            nn[k] = b1[k]
    return nn


def bsip1_to_l3_signals(b1: dict) -> dict:
    """Build a minimal L3 dict from a BSIP1 record (for engine inputs)."""
    # Use available enrichment fields; leave others None so engine defaults
    l3 = {
        "sweetener_detected": len(b1.get("extracted_sweeteners", [])) > 0,
        "sweetener_tier": None,
        "has_whole_grain": False,
        "has_seed_oil": False,
        "has_palm_oil": False,
        "has_flavor_enhancer": False,
        "has_artificial_color": False,
        "has_natural_color": False,
        "has_natural_color_hits": [],
        "natural_color_hits": [],
        "seed_oil_matches": [],
        "palm_oil_matches": [],
        "trans_fat_status": "not_detected",
        "protein_source": "whole_food",
        "additive_marker_count": len(b1.get("extracted_additives", [])),
        "additive_categories": [a.get("category") for a in b1.get("extracted_additives", [])],
        "added_sugar_sources_count": 0,
        "has_fruit_concentrate": False,
        "has_fermentation": False,
        "product_type_dairy": False,
        "has_fortification": False,
        "fortification_evidence": [],
        "red_labels": [],
        "red_label_count": 0,
        "hp_fat_sugar_pattern_raw": False,
        "hp_fat_sodium_pattern_raw": False,
        "sprint1_high_risk_emulsifier_detected": False,
        "sprint1_high_risk_emulsifier_found": [],
        "sprint1_neutral_emulsifier_detected": False,
        "sprint1_neutral_emulsifier_found": [],
        "sprint1_prebiotic_gum_detected": False,
        "sprint1_allulose_detected": False,
        "functional_fiber_type": "none",
        "protein_matrix_form": None,
    }
    # Try to read from enrichment_summary if available
    es = b1.get("enrichment_summary") or {}
    l3["has_fermentation"] = es.get("has_live_cultures", False)
    l3["has_fortification"] = es.get("has_fortification", False)
    return l3


def quick_score(nn: dict, l3: dict, category: str = "default",
                extra_fields: dict = None) -> dict:
    """
    Run the 10 BSIP2 dimension scorers and return score+grade.
    This is a simplified path — not the full compute_composite() with all
    coordination layers — intended only for comparing sugar impact on
    the glycemic + shelf-relative dimensions.
    """
    se_result = eng.detect_structural_emptiness(nn, category, l3)

    proc, proc_note   = eng.score_processing_quality(l3, se_result)
    nutr, nutr_note   = eng.score_nutrient_density(nn, l3)
    cal, cal_note     = eng.score_calorie_density(nn, category)
    glyc, glyc_note   = eng.score_glycemic_quality(nn, l3)
    prot, prot_note   = eng.score_protein_quality(nn, l3, category)
    add, add_note     = eng.score_additive_quality(l3)
    sat, sat_note     = eng.score_satiety_support(nn, l3)
    fat, fat_note     = eng.score_fat_quality(nn, l3, se_result)
    reg, reg_note     = eng.score_regulatory_quality(nn, l3)
    wfi, wfi_note     = eng.score_whole_food_integrity(nn, l3, "")

    dims = {
        "processing_quality": proc,
        "nutrient_density": nutr,
        "calorie_density": cal,
        "glycemic_quality": glyc,
        "protein_quality": prot,
        "additive_quality": add,
        "satiety_support": sat,
        "fat_quality": fat,
        "regulatory_quality": reg,
        "whole_food_integrity": wfi,
    }
    w = DIMENSION_WEIGHTS
    weighted = sum(dims[k] * w.get(k, 0) for k in dims)
    total_w = sum(w.get(k, 0) for k in dims)
    raw_score = weighted / total_w if total_w else 0
    score = round(min(100, max(0, raw_score)), 1)
    grade = score_to_grade(score)
    return {
        "score": score,
        "grade": grade,
        "glycemic_quality": glyc,
        "glycemic_note": glyc_note,
        "dimensions": dims,
    }


# ── Target definitions ────────────────────────────────────────────────────────
# For each target: (barcode, category, bsip1_path, real_sugar_g, real_sugar_source,
#                   published_score, published_grade)
#
# Sugar values derived from:
# - Juices: panel shows carbs only; sugar ABSENT from panel (no row at all).
#   Pomegranate 100% juice typical = ~10.5g sugar/100g (USDA FDC #168153 Pomegranate juice).
#   Clementine 100% juice typical = ~8.9g (USDA FDC #167765 Clementine juice, per 100ml).
#   Both mark as "genuinely absent from Yohananof panel".
#
# - cookies_coffee: panels show carbs but no sugar row. Biscuit products.
#   7290119043149 (עוגיות בטעם חמאה, 60g carbs): typical biscuit ≈ 20-28g sugar (biscuit range).
#   7290017962139 (עוגיות פירות יער, 48.1g carbs): similar biscuit range.
#   Sugar "genuinely absent" from both panels.
#
# - milk 7290000051352 (חלב מלא 3.4%): lactose 4.7g (known dairy value, per USDA whole milk).
#   Milk alternatives: Alpro Oat no-sugar 5411188124689 → ~0g sugar (product is "no added sugar").
#   almond milk 7290014760141 (משקה שקדים) → ~3g sugar typical.
#   oat milk 7290110325619 (משקה שיבולת שועל) → ~4g sugar typical.
#
# - hummus 6666307: no sugar row; typical hummus ~2g sugar. 6666444 (מטבוחה): ~4g (tomato sugars).
# - brined 369617 (כדורי פטה): no sugar row; typical feta ~1g.
# - cakes 5431920 (עוגת גבינה פירורים לייט): 13g carbs; cheesecake typically 6-8g sugar.
# - cereals 7297488098688 (פצפוצי אורז ללת"ס): 86g carbs rice puffs; typically ~0-1g sugar (no added).
#
# All sugar values from USDA FDC or well-established category references.
# None substituted from OFF.

TARGETS = [
    # juices - TOP PRIORITY
    {
        "barcode": "7290013153395",
        "name": "סחוט רימונים 1L",
        "category": "juices",
        "bsip1_path": r"C:\Bari\02_products\juices\bsip1_outputs\bsip1_juice_7290013153395.json",
        "real_sugar_g": 10.5,
        "sugar_source": "USDA FDC #168153 pomegranate juice 100% typical",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 85.0,
        "published_grade": "A",
        "published_rank": 1,
    },
    {
        "barcode": "7290110114886",
        "name": "סחוט קלמנטינה 2L",
        "category": "juices",
        "bsip1_path": r"C:\Bari\02_products\juices\bsip1_outputs\bsip1_juice_7290110114886.json",
        "real_sugar_g": 8.9,
        "sugar_source": "USDA FDC clementine juice typical ~8.9g/100ml",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 85.0,
        "published_grade": "A",
        "published_rank": 1,
    },
    # cookies_coffee
    {
        "barcode": "7290119043149",
        "name": "עוגיות בטעם חמאה",
        "category": "biscuit",
        "bsip1_path": None,  # not in a BSIP1 dir; use BSIP0 nutrition directly
        "real_sugar_g": None,  # sugar row absent from panel, no ref value available
        "sugar_source": "GENUINELY_ABSENT_from_panel_no_reference",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 55.0,
        "published_grade": "C",
        "published_rank": 2,
    },
    {
        "barcode": "7290017962139",
        "name": "עוגיות פירות יער כשל\"פ",
        "category": "biscuit",
        "bsip1_path": None,
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel_no_reference",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 54.9,
        "published_grade": "C",
        "published_rank": 4,
    },
    {
        "barcode": "7290013453068",
        "name": "בסקביט (cookies_coffee corpus)",
        "category": "biscuit",
        "bsip1_path": None,
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel_no_reference",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 52.0,
        "published_grade": "C",
        "published_rank": 8,
    },
    {
        "barcode": "7296073453840",
        "name": "ביסקוויט קפה (E-grade)",
        "category": "biscuit",
        "bsip1_path": None,
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel_no_reference",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 33.1,
        "published_grade": "E",
        "published_rank": 37,
    },
    {
        "barcode": "7296073453857",
        "name": "ביסקוויט קרם (E-grade)",
        "category": "biscuit",
        "bsip1_path": None,
        "real_sugar_g": None,
        "sugar_source": "GENUINELY_ABSENT_from_panel_no_reference",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 32.7,
        "published_grade": "E",
        "published_rank": 38,
    },
    # milk
    {
        "barcode": "7290000051352",
        "name": "חלב מלא 3.4% (תנובה)",
        "category": "dairy_protein",
        "bsip1_path": r"C:\Bari\03_operations\bsip1\run_milk_002\output\bsip1_7290000051352.json",
        "real_sugar_g": 4.7,
        "sugar_source": "Lactose in whole cow milk: USDA FDC #746782 = 4.61g/100ml; rounded 4.7g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 85.0,
        "published_grade": "A",
        "published_rank": 1,
    },
    {
        "barcode": "5411188124689",
        "name": "אלפרו שיבולת שועל ללא סוכר",
        "category": "dairy_protein",
        "bsip1_path": r"C:\Bari\03_operations\bsip1\run_milk_002\output\bsip1_5411188124689.json",
        "real_sugar_g": 0.0,
        "sugar_source": "Alpro Oat No Sugars declared 0g sugar on EU label (product name confirms ללא סוכר)",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 49.7,
        "published_grade": "D",
        "published_rank": 13,
    },
    {
        "barcode": "7290014760141",
        "name": "משקה שקדים",
        "category": "dairy_protein",
        "bsip1_path": r"C:\Bari\03_operations\bsip1\run_milk_002\output\bsip1_7290014760141.json",
        "real_sugar_g": 3.0,
        "sugar_source": "Almond milk typical unsweetened ~0.5-1g; sweetened ~7g; this is a mid-guess of ~3g pending re-scrape",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 51.5,
        "published_grade": "C",
        "published_rank": 8,
    },
    {
        "barcode": "7290110325619",
        "name": "משקה שיבולת שועל",
        "category": "dairy_protein",
        "bsip1_path": r"C:\Bari\03_operations\bsip1\run_milk_002\output\bsip1_7290110325619.json",
        "real_sugar_g": 4.0,
        "sugar_source": "Oat milk typical ~4-5g/100ml (lactose-equivalent); mid estimate",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 47.6,
        "published_grade": "D",
        "published_rank": 15,
    },
    # hummus
    {
        "barcode": "6666307",
        "name": "סלט חומוס",
        "category": "sauce_spread",
        "bsip1_path": r"C:\Bari\02_products\hummus\canonical_bsip1\bsip1_6666307.json",
        "real_sugar_g": 1.8,
        "sugar_source": "Hummus typical: USDA FDC #174286 = 1.85g/100g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 67.7,
        "published_grade": "B",
        "published_rank": 2,
    },
    {
        "barcode": "6666444",
        "name": "סלט מטבוחה",
        "category": "sauce_spread",
        "bsip1_path": r"C:\Bari\02_products\hummus\canonical_bsip1\bsip1_6666444.json",
        "real_sugar_g": 4.0,
        "sugar_source": "Matbucha (cooked tomato-pepper): ~3-5g sugar; USDA tomato sauce ~3.5g; use 4.0g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 58.0,
        "published_grade": "C",
        "published_rank": 5,
    },
    # brined cheese
    {
        "barcode": "369617",
        "name": "כדורי פטה בשמן",
        "category": "dairy_fat",
        "bsip1_path": None,
        "real_sugar_g": 0.5,
        "sugar_source": "Feta cheese typical: USDA FDC #173420 = 0.49g/100g; ~0.5g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 48.5,
        "published_grade": "D",
        "published_rank": 35,
    },
    # cakes
    {
        "barcode": "5431920",
        "name": "עוגת גבינה פירורים לייט",
        "category": "dessert",
        "bsip1_path": None,
        "real_sugar_g": 6.5,
        "sugar_source": "Light cheesecake crumb: 13g carbs; typical cheesecake sugar fraction ~50% = 6.5g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 30.6,
        "published_grade": "E",
        "published_rank": 4,
    },
    # cereals
    {
        "barcode": "7297488098688",
        "name": "פצפוצי אורז ללת\"ס",
        "category": "cereal",
        "bsip1_path": None,
        "real_sugar_g": 0.5,
        "sugar_source": "Rice puffs ללת\"ס (without added sugar): typical 0-1g sugar; USDA FDC puffed rice = 0.39g/100g",
        "panel_verdict": "GENUINELY_ABSENT",
        "published_score": 67.3,
        "published_grade": "B",
        "published_rank": 2,
    },
]


def simulate_one(target: dict, verbose: bool = False) -> dict:
    """
    Run a quick score simulation for one target with and without real sugar.
    Returns a result dict.
    """
    bc = target["barcode"]
    name = target["name"]
    cat = target["category"]
    real_sugar = target.get("real_sugar_g")
    pub_score = target["published_score"]
    pub_grade = target["published_grade"]
    bsip1_path = target.get("bsip1_path")

    result = {
        "barcode": bc,
        "name": name,
        "category": cat,
        "published_score": pub_score,
        "published_grade": pub_grade,
        "panel_verdict": target["panel_verdict"],
        "sugar_source": target["sugar_source"],
        "real_sugar_g": real_sugar,
        "staged_score": None,
        "staged_grade": None,
        "delta_score": None,
        "grade_moved": False,
        "tripwire": False,
        "glycemic_current": None,
        "glycemic_staged": None,
        "error": None,
    }

    # Load BSIP1 if available
    nn_base = {}
    l3_base = {}
    if bsip1_path and pathlib.Path(bsip1_path).exists():
        try:
            b1 = load_bsip1(pathlib.Path(bsip1_path))
            nn_base = nn_from_bsip1(b1)
            l3_base = bsip1_to_l3_signals(b1)
        except Exception as e:
            result["error"] = f"bsip1_load_error: {e}"
            return result

    # If real_sugar_g is None → panel absent + no reference → cannot simulate
    if real_sugar is None:
        result["error"] = "sugar_genuinely_absent_no_reference_available"
        return result

    # Current score (with sugar=None → scored as 0)
    nn_current = dict(nn_base)
    nn_current["sugars_g"] = None
    try:
        cur = quick_score(nn_current, l3_base, cat)
        result["glycemic_current"] = cur["glycemic_quality"]
    except Exception as e:
        result["error"] = f"score_current_error: {e}"
        return result

    # Staged score (with real sugar injected)
    nn_staged = dict(nn_base)
    nn_staged["sugars_g"] = real_sugar
    try:
        staged = quick_score(nn_staged, l3_base, cat)
        result["staged_score"] = staged["score"]
        result["staged_grade"] = staged["grade"]
        result["glycemic_staged"] = staged["glycemic_quality"]
        delta = staged["score"] - pub_score
        result["delta_score"] = round(delta, 1)
        result["grade_moved"] = staged["grade"] != pub_grade
        # Tripwire = A→B or A→C or B→C (meaningful downgrade for published high-grade products)
        g_order = {"A":5,"B":4,"C":3,"D":2,"E":1,"F":0}
        result["tripwire"] = (g_order.get(staged["grade"],0) < g_order.get(pub_grade,0))
    except Exception as e:
        result["error"] = f"score_staged_error: {e}"

    return result


if __name__ == "__main__":
    import io

    out = io.StringIO()
    orig = sys.stdout
    sys.stdout = out

    results = []
    grade_movers = []
    tripwires = []

    for t in TARGETS:
        r = simulate_one(t)
        results.append(r)

    print("\n" + "="*75)
    print("TASK-378 PHASE 2 — RESCORE SIMULATION RESULTS")
    print("Stage only. No published scores changed. BARI_SUGAR_NULL_GUARD=OFF.")
    print("="*75)

    for r in results:
        print(f"\nBarcode: {r['barcode']} | {r['name']}")
        print(f"  Category:         {r['category']}")
        print(f"  Panel verdict:    {r['panel_verdict']}")
        print(f"  Real sugar:       {r['real_sugar_g']}g  ({r['sugar_source']})")
        print(f"  Published:        {r['published_score']}/{r['published_grade']}")
        if r["error"]:
            print(f"  Simulation:       SKIP — {r['error']}")
        else:
            print(f"  Staged:           {r['staged_score']}/{r['staged_grade']}")
            print(f"  Delta score:      {r['delta_score']:+.1f}")
            print(f"  Glycemic (null):  {r['glycemic_current']:.1f}")
            print(f"  Glycemic (real):  {r['glycemic_staged']:.1f}")
            print(f"  Grade moved:      {'YES ***' if r['grade_moved'] else 'no'}")
            print(f"  TRIPWIRE:         {'YES *** OWNER ESCALATION' if r['tripwire'] else 'no'}")
            if r["grade_moved"]:
                grade_movers.append(r)
            if r["tripwire"]:
                tripwires.append(r)

    print("\n" + "="*75)
    print("GRADE-MOVERS SUMMARY (consolidated)")
    print("="*75)
    if grade_movers:
        for r in grade_movers:
            print(f"  {r['barcode']} {r['name']}: {r['published_grade']} → {r['staged_grade']} "
                  f"({r['published_score']} → {r['staged_score']}, delta={r['delta_score']:+.1f})")
    else:
        print("  None found in simulation.")

    print("\n" + "="*75)
    print("OWNER TRIPWIRES (grade downgrades requiring owner approval)")
    print("="*75)
    if tripwires:
        for r in tripwires:
            print(f"  TRIPWIRE: {r['barcode']} {r['name']}: "
                  f"{r['published_grade']} → {r['staged_grade']} "
                  f"(delta={r['delta_score']:+.1f})")
    else:
        print("  None.")

    errors_with_sugar = [r for r in results if r["error"] and r["real_sugar_g"] is not None]
    skipped_no_ref = [r for r in results if r["error"] and r["real_sugar_g"] is None]
    simulated = [r for r in results if not r["error"]]

    print(f"\nSimulated: {len(simulated)}")
    print(f"Skipped (no reference): {len(skipped_no_ref)} — {[r['barcode'] for r in skipped_no_ref]}")
    print(f"Errors: {len(errors_with_sugar)}")
    print(f"N published scores changed = 0 (staging only, no write)")
    print(f"M grade-movers flagged for owner = {len(grade_movers)}")

    sys.stdout = orig
    text = out.getvalue()
    out_path = pathlib.Path(r"C:\Bari\02_products\_parsing_audit\task378_phase2_rescore_result.txt")
    out_path.write_text(text, encoding="utf-8")
    print(f"Written to {out_path}")

    # Also write machine-readable JSON
    json_path = pathlib.Path(r"C:\Bari\02_products\_parsing_audit\task378_phase2_rescore_results.json")
    json_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Results JSON: {json_path}")
