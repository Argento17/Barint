# BSIP2 batch -- Juices x sugar SHELF-RELATIVE PILOT (run_juices_002_sugar_pilot)
# TASK-278 Phase-9 / EV-091 -- Juices x sugar asymmetric P>B shelf-relative enrollment.
# MEASURED, NOT PUBLISHED: no frontend JSON, no live-category edit, no deploy.
# Flag config BEFORE engine imports (CRITICAL: must set BARI_SHELF_RELATIVE_V1=on).
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# --- Flag config BEFORE engine imports ---
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats, compute_shelf_stats,
    BARI_SHELF_RELATIVE_V1,
)
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    score_to_grade,
    SUGAR_SHELF_SCALE_GUARD, SUGAR_SHELF_SCALE_MIN,
    SUGAR_SHELF_REL_JUICES_MEDIAN, SUGAR_SHELF_REL_JUICES_IQR,
    SUGAR_SHELF_REL_JUICES_SCALE, SUGAR_SHELF_REL_JUICES_FLOOR,
    SUGAR_SHELF_REL_JUICES_FLOOR_THRESHOLD_G,
    SUGAR_SHELF_REL_JUICES_P_MAX, SUGAR_SHELF_REL_JUICES_B_MAX,
    SUGAR_SHELF_SCALE_GUARD_JUICES,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT         = pathlib.Path(r"C:\Bari")
BSIP1_JUICE_DIR = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
BSIP1_MILK_DIR  = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
MILK_RUN005_DIR = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
OUTPUT_DIR   = ROOT / "02_products" / "juices" / "bsip2_outputs" / "run_juices_002_sugar_pilot"
RETURN_DIR   = ROOT / "tasks" / "returns"
RUN_ID = "run_juices_002_sugar_pilot"

# Pilot stats from D7 co-sign (P125)
PROPOSAL_MEDIAN = 9.50
PROPOSAL_SCALE  = 2.82
PROPOSAL_IQR    = 3.80
FLOOR_VALUE     = 62
FLOOR_THRESHOLD_G = 12.2

# Gate C3 inversions (sugars_g based):
# INV-A: lemon juice (sugars_g~2.5g) vs 100% orange (sugars_g~8.4g)
# INV-B: frigat nectar peach (sugars_g~12.2g) vs apple juice 100% (sugars_g~9.6g)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RETURN_DIR.mkdir(parents=True, exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def stdev(scores):
    if not scores:
        return 0.0
    n = len(scores)
    mean = sum(scores) / n
    return (sum((x - mean) ** 2 for x in scores) / n) ** 0.5


def run_bsip2_pipeline(product):
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def run_bsip2_pipeline_flag_off(product):
    """Score with flag OFF by temporarily clearing shelf stats and forcing flag=off via env."""
    saved = os.environ.get("BARI_SHELF_RELATIVE_V1")
    os.environ["BARI_SHELF_RELATIVE_V1"] = "off"
    # Re-import flag state is module-level; we use a workaround:
    # call score_product with flag=off via monkeypatching isn't practical
    # Instead we rely on the engine reading the env var each call via module-level bool.
    # Because BARI_SHELF_RELATIVE_V1 is set at module import time, we must use
    # a different approach: score flag-off FIRST in a separate process or by
    # toggling the module attribute directly.
    import score_engine as _se
    saved_flag = _se.BARI_SHELF_RELATIVE_V1
    _se.BARI_SHELF_RELATIVE_V1 = False
    try:
        signals     = extract_signals(product)
        cat_result  = classify_category(product)
        l3          = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)
        trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    finally:
        _se.BARI_SHELF_RELATIVE_V1 = saved_flag
        if saved is not None:
            os.environ["BARI_SHELF_RELATIVE_V1"] = saved
    return trace


def main():
    assert BARI_SHELF_RELATIVE_V1, "CRITICAL: BARI_SHELF_RELATIVE_V1 must be ON for pilot run"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-278 Phase-9 EV-091: Juices x Sugar SR Pilot -- %s ===", RUN_ID)
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")

    # -----------------------------------------------------------------------
    # STEP 1: Load juice corpus (65 products)
    # -----------------------------------------------------------------------
    juice_records = []
    for p in sorted(BSIP1_JUICE_DIR.glob("bsip1_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            juice_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)
    log.info("Juice BSIP1 records loaded: %d (expected 65)", len(juice_records))

    # -----------------------------------------------------------------------
    # STEP 2: Verify juice_sub_pool (precheck)
    # -----------------------------------------------------------------------
    null_pool_count = sum(1 for r in juice_records if r.get("juice_sub_pool") is None)
    pool_dist = Counter(r.get("juice_sub_pool") for r in juice_records if r.get("juice_sub_pool") is not None)
    log.info("juice_sub_pool: null=%d, dist=%s", null_pool_count, dict(pool_dist))
    if null_pool_count > 0:
        log.error("PRECHECK FAIL: %d juice products have null juice_sub_pool — STOP", null_pool_count)
        return {"status": "PRECHECK_FAIL", "null_pool_count": null_pool_count}

    # -----------------------------------------------------------------------
    # STEP 3: Load milk corpus (20 products from run_005_headpin bsip1 source)
    # -----------------------------------------------------------------------
    milk_records = []
    for prod_dir in sorted(MILK_RUN005_DIR.iterdir()):
        if not prod_dir.is_dir():
            continue
        trace_file = prod_dir / "bsip2_trace.json"
        if not trace_file.exists():
            continue
        try:
            trace = json.loads(trace_file.read_text(encoding="utf-8"))
            bsip1_path = (trace.get("input_reference") or {}).get("bsip1_source_path")
            if bsip1_path and pathlib.Path(bsip1_path).exists():
                doc = json.loads(pathlib.Path(bsip1_path).read_text(encoding="utf-8"))
                milk_records.append(doc)
            else:
                # Fall back: look in BSIP1_MILK_DIR by barcode
                bc = str((trace.get("input_reference") or {}).get("barcode") or "")
                candidates = list(BSIP1_MILK_DIR.glob(f"bsip1_{bc}.json"))
                if candidates:
                    doc = json.loads(candidates[0].read_text(encoding="utf-8"))
                    milk_records.append(doc)
                else:
                    log.warning("No BSIP1 found for milk product %s", prod_dir.name)
        except Exception as e:
            log.error("Milk load error %s: %s", prod_dir.name, e)
    log.info("Milk BSIP1 records loaded: %d (expected 20)", len(milk_records))

    # -----------------------------------------------------------------------
    # STEP 4: Compute shelf stats from juice corpus
    # -----------------------------------------------------------------------
    engine_median, engine_scale = compute_shelf_stats(
        juice_records,
        "sugars_g",
        scale_type="iqr",
        nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
    )
    log.info("Engine computed: median=%.3f, scale=%.3f (proposal: median=%.3f, scale=%.3f)",
             engine_median or 0, engine_scale or 0, PROPOSAL_MEDIAN, PROPOSAL_SCALE)

    # Set shelf stats for flag-on scoring
    clear_shelf_stats()
    set_shelf_stats(
        nutrient="sugars_g",
        median=engine_median if engine_median is not None else PROPOSAL_MEDIAN,
        scale=engine_scale if engine_scale is not None else PROPOSAL_SCALE,
        scale_type="iqr",
        n=len([r for r in juice_records if (r.get("normalized_nutrition_per_100g") or {}).get("sugars_g") is not None]),
    )
    used_median = engine_median if engine_median is not None else PROPOSAL_MEDIAN
    used_scale  = engine_scale if engine_scale is not None else PROPOSAL_SCALE
    log.info("Shelf stats set: sugars_g median=%.3f scale=%.3f", used_median, used_scale)

    # -----------------------------------------------------------------------
    # STEP 5: Score all products flag-on AND flag-off
    # -----------------------------------------------------------------------
    juice_rows = []
    milk_rows = []
    errors = []

    log.info("--- Scoring juice corpus (65 products) flag-on ---")
    for doc in juice_records:
        barcode = str(doc.get("barcode", ""))
        name    = doc.get("canonical_name_he", "")
        nn      = doc.get("normalized_nutrition_per_100g") or {}
        sugars_g = nn.get("sugars_g")
        sub_pool = doc.get("juice_sub_pool")
        try:
            trace_on  = run_bsip2_pipeline(doc)
            trace_off = run_bsip2_pipeline_flag_off(doc)
            score_on  = trace_on.get("final_score_estimate")
            score_off = trace_off.get("final_score_estimate")
            grade_on  = trace_on.get("grade_estimate")
            grade_off = trace_off.get("grade_estimate")
            delta     = round(score_on - score_off, 2) if (score_on is not None and score_off is not None) else None
            category  = trace_on.get("category")
            floor_app = trace_on.get("ev091_juice_floor_applied")
            sr_pen_on = None
            for p in (trace_on.get("penalties_applied") or []):
                if p.get("rule") == "SUGAR_JUICES_SHELF_REL_V1":
                    sr_pen_on = p.get("amount")
                    break
            juice_rows.append({
                "barcode": barcode,
                "name": name,
                "sub_pool": sub_pool,
                "sugars_g": sugars_g,
                "flag_off_score": score_off,
                "flag_off_grade": grade_off,
                "flag_on_score": score_on,
                "flag_on_grade": grade_on,
                "clean_delta": delta,
                "ev091_floor_applied": floor_app,
                "sr_penalty": sr_pen_on,
                "category": category,
            })
            log.info("  [%s] %-45s sugar=%-5s off=%s/%s on=%s/%s delta=%s floor=%s",
                     sub_pool, name[:43], sugars_g, score_off, grade_off, score_on, grade_on, delta, floor_app)
        except Exception as e:
            log.error("  ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            errors.append({"corpus": "juice", "barcode": barcode, "name": name, "error": str(e)})

    log.info("--- Scoring milk corpus (20 products) flag-on ---")
    for doc in milk_records:
        barcode = str(doc.get("barcode", ""))
        name    = doc.get("canonical_name_he", "") or doc.get("product_name_he", "")
        nn      = doc.get("normalized_nutrition_per_100g") or {}
        try:
            trace_on  = run_bsip2_pipeline(doc)
            trace_off = run_bsip2_pipeline_flag_off(doc)
            score_on  = trace_on.get("final_score_estimate")
            score_off = trace_off.get("final_score_estimate")
            grade_on  = trace_on.get("grade_estimate")
            grade_off = trace_off.get("grade_estimate")
            delta     = round(score_on - score_off, 2) if (score_on is not None and score_off is not None) else None
            category  = trace_on.get("category")
            milk_rows.append({
                "barcode": barcode,
                "name": name,
                "corpus": "milk",
                "flag_off_score": score_off,
                "flag_on_score": score_on,
                "flag_off_grade": grade_off,
                "flag_on_grade": grade_on,
                "clean_delta": delta,
                "category": category,
            })
            log.info("  MILK %-45s off=%s/%s on=%s/%s delta=%s", name[:43], score_off, grade_off, score_on, grade_on, delta)
        except Exception as e:
            log.error("  MILK ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            errors.append({"corpus": "milk", "barcode": barcode, "name": name, "error": str(e)})

    # -----------------------------------------------------------------------
    # STEP 6: Score 12 gate criteria
    # -----------------------------------------------------------------------
    log.info("--- Evaluating 12 gate criteria ---")

    # C1 directional_distribution
    above_median = [r for r in juice_rows if r["sugars_g"] is not None and r["sugars_g"] > PROPOSAL_MEDIAN]
    below_median = [r for r in juice_rows if r["sugars_g"] is not None and r["sugars_g"] < PROPOSAL_MEDIAN]
    above_deltas = [r["clean_delta"] for r in above_median if r["clean_delta"] is not None]
    below_deltas = [r["clean_delta"] for r in below_median if r["clean_delta"] is not None]
    c1_above_mean = sum(above_deltas) / len(above_deltas) if above_deltas else None
    c1_below_mean = sum(below_deltas) / len(below_deltas) if below_deltas else None
    c1_pass = (c1_above_mean is not None and c1_above_mean <= 0) and (c1_below_mean is not None and c1_below_mean >= 0)
    c1_note = (f"above_median(n={len(above_median)}) mean_delta={c1_above_mean:.3f} (need<=0); "
               f"below_median(n={len(below_median)}) mean_delta={c1_below_mean:.3f} (need>=0)")

    # C2a: 0 juice products with sugars_g >= 12.2g at grade B (score>=70) at flag-on
    high_sugar_b = [r for r in juice_rows if (r["sugars_g"] is not None and r["sugars_g"] >= FLOOR_THRESHOLD_G
                                              and r["flag_on_score"] is not None and r["flag_on_score"] >= 70)]
    c2a_pass = len(high_sugar_b) == 0
    c2a_note = (f"{len(high_sugar_b)} juice products with sugars_g>={FLOOR_THRESHOLD_G}g at grade B at flag-on "
                f"(need=0). Violators: {[r['barcode'] for r in high_sugar_b]}")

    # C2b: >= 1 low-sugar (sugars_g <= 4g) juice product at grade C or better at flag-on
    # Grade C threshold = 50 (from GRADE_THRESHOLDS: C=50, B=65, A=80, S=90)
    low_sugar_c_or_better = [r for r in juice_rows if (r["sugars_g"] is not None and r["sugars_g"] <= 4.0
                                                        and r["flag_on_score"] is not None and r["flag_on_score"] >= 50)]
    c2b_pass = len(low_sugar_c_or_better) >= 1
    c2b_note = (f"{len(low_sugar_c_or_better)} low-sugar (<=4g) juice products at grade C+ at flag-on "
                f"(need>=1)")

    # C2c magnitude: mean |clean_delta| >= 0.5 among SR-firing juice products
    sr_firing = [r for r in juice_rows if r["clean_delta"] is not None and r["clean_delta"] != 0]
    c2c_mean_abs_delta = (sum(abs(r["clean_delta"]) for r in sr_firing) / len(sr_firing)) if sr_firing else 0
    c2c_pass = len(sr_firing) > 0 and c2c_mean_abs_delta >= 0.5
    c2c_note = f"SR-firing products: {len(sr_firing)}, mean |delta|={c2c_mean_abs_delta:.3f} (need>=0.5)"

    # C3 gap_narrows_inversion
    # INV-A: lemon juice (sugars_g~2.5g) vs 100% orange (sugars_g~8.4g)
    # INV-B: frigat nectar peach (sugars_g~12.2g) vs apple juice 100% (sugars_g~9.6g)
    # Find by sugars_g matching (closest match)
    def find_closest(rows, target_sugar, tolerance=0.5):
        candidates = [r for r in rows if r["sugars_g"] is not None and abs(r["sugars_g"] - target_sugar) <= tolerance]
        if not candidates:
            return None
        return min(candidates, key=lambda r: abs(r["sugars_g"] - target_sugar))

    inv_a_low  = find_closest(juice_rows, 2.5)   # lemon juice
    inv_a_high = find_closest(juice_rows, 8.4)   # 100% orange
    inv_b_high = find_closest(juice_rows, 12.2)  # frigat nectar peach (high sugar, should be penalized)
    inv_b_low  = find_closest(juice_rows, 9.6)   # apple juice 100% (lower sugar)

    c3_inv_a_gap_off = None
    c3_inv_a_gap_on  = None
    c3_inv_a_pass    = None
    if inv_a_low and inv_a_high:
        c3_inv_a_gap_off = round((inv_a_low["flag_off_score"] or 0) - (inv_a_high["flag_off_score"] or 0), 2)
        c3_inv_a_gap_on  = round((inv_a_low["flag_on_score"] or 0) - (inv_a_high["flag_on_score"] or 0), 2)
        c3_inv_a_pass    = c3_inv_a_gap_on > c3_inv_a_gap_off  # low-sugar should score higher vs high-sugar (bigger gap)

    c3_inv_b_gap_off = None
    c3_inv_b_gap_on  = None
    c3_inv_b_pass    = None
    if inv_b_high and inv_b_low:
        # gap = high_sugar score - low_sugar score; should NARROW (high penalized more) at flag-on
        c3_inv_b_gap_off = round((inv_b_high["flag_off_score"] or 0) - (inv_b_low["flag_off_score"] or 0), 2)
        c3_inv_b_gap_on  = round((inv_b_high["flag_on_score"] or 0) - (inv_b_low["flag_on_score"] or 0), 2)
        c3_inv_b_pass    = c3_inv_b_gap_on < c3_inv_b_gap_off  # gap narrows (high penalized more)

    c3_pass = (c3_inv_a_pass is True) and (c3_inv_b_pass is True)
    c3_note = (
        f"INV-A (lemon {inv_a_low['sugars_g'] if inv_a_low else 'N/F'}g vs OJ {inv_a_high['sugars_g'] if inv_a_high else 'N/F'}g): "
        f"gap_off={c3_inv_a_gap_off} gap_on={c3_inv_a_gap_on} -> {'PASS' if c3_inv_a_pass else 'FAIL'}; "
        f"INV-B (nectar {inv_b_high['sugars_g'] if inv_b_high else 'N/F'}g vs apple {inv_b_low['sugars_g'] if inv_b_low else 'N/F'}g): "
        f"gap_off={c3_inv_b_gap_off} gap_on={c3_inv_b_gap_on} -> {'PASS' if c3_inv_b_pass else 'FAIL'}"
    )

    # C4 min_movers: >= 5 juice products with clean_delta != 0
    movers = [r for r in juice_rows if r["clean_delta"] is not None and r["clean_delta"] != 0]
    c4_pass = len(movers) >= 5
    c4_note = f"{len(movers)} juice products with clean_delta!=0 (need>=5)"

    # C5 min_grade_changes: >= 1 juice product with grade change at flag-on
    grade_changers = [r for r in juice_rows if r["flag_off_grade"] != r["flag_on_grade"]]
    c5_pass = len(grade_changers) >= 1
    c5_note = (f"{len(grade_changers)} juice products with grade change at flag-on (need>=1). "
               f"Examples: {[{'bc': r['barcode'], 'off': r['flag_off_grade'], 'on': r['flag_on_grade']} for r in grade_changers[:3]]}")

    # C6 max_absorption: <= 40% of SR-firing products with clean_delta=0 despite non-zero SR term
    sr_term_nonzero = [r for r in juice_rows if r["sr_penalty"] is not None and r["sr_penalty"] != 0]
    absorbed = [r for r in sr_term_nonzero if r["clean_delta"] == 0]
    c6_absorption_pct = (len(absorbed) / len(sr_term_nonzero) * 100) if sr_term_nonzero else 0
    c6_pass = c6_absorption_pct <= 40.0
    c6_note = (f"SR-term nonzero: {len(sr_term_nonzero)}, absorbed (delta=0): {len(absorbed)}, "
               f"absorption={c6_absorption_pct:.1f}% (need<=40%)")

    # C7 anti_immunity: 0 juice products with sugars_g >= 12.2g at grade B (score>=70) at flag-on
    c7_pass = c2a_pass  # same condition
    c7_note = f"Same as C2a: {len(high_sugar_b)} products with sugar>={FLOOR_THRESHOLD_G}g at grade B (need=0)"

    # C8 floor_compliance: all juice products with sugars_g >= 12.2g: flag-on score <= 62
    floor_violators = [r for r in juice_rows if (r["sugars_g"] is not None and r["sugars_g"] >= FLOOR_THRESHOLD_G
                                                  and r["flag_on_score"] is not None and r["flag_on_score"] > FLOOR_VALUE)]
    above_threshold = [r for r in juice_rows if r["sugars_g"] is not None and r["sugars_g"] >= FLOOR_THRESHOLD_G]
    c8_pass = len(floor_violators) == 0
    c8_note = (f"{len(above_threshold)} products with sugars_g>={FLOOR_THRESHOLD_G}g, "
               f"{len(floor_violators)} floor violations (score>{FLOOR_VALUE}). "
               f"Violators: {[r['barcode'] for r in floor_violators]}")

    # C9 no_scope_bleed: 0 non-juice products (juice_sub_pool IS None) with non-zero clean_delta from EV-091
    # Non-juice products = milk corpus (no juice_sub_pool)
    milk_movers = [r for r in milk_rows if r["clean_delta"] is not None and r["clean_delta"] != 0]
    c9_pass = len(milk_movers) == 0
    c9_note = (f"{len(milk_movers)} non-juice (milk) products with non-zero delta (need=0). "
               f"Movers: {[r['barcode'] for r in milk_movers]}")

    # C10 frozen_byte_id_milk: ALL 20 milk products clean_delta=0.0
    milk_zero_delta = [r for r in milk_rows if r["clean_delta"] == 0.0 or r["clean_delta"] is None]
    c10_pass = len(milk_rows) == 20 and len(milk_movers) == 0
    c10_note = (f"{len(milk_rows)} milk products loaded, "
                f"{len(milk_rows) - len(milk_movers)}/20 with delta=0 (need 20/20)")

    # C11 routing_agnostic: for any pairs with same sugars_g, delta must be identical
    same_sugar_groups = {}
    for r in juice_rows:
        if r["sugars_g"] is not None:
            key = round(r["sugars_g"], 1)
            same_sugar_groups.setdefault(key, []).append(r)
    routing_violations = []
    for sg, group in same_sugar_groups.items():
        if len(group) >= 2:
            deltas = set(r["clean_delta"] for r in group)
            if len(deltas) > 1:
                routing_violations.append({"sugars_g": sg, "deltas": list(deltas), "barcodes": [r["barcode"] for r in group]})
    c11_pass = len(routing_violations) == 0
    c11_note = (f"{len(routing_violations)} routing violations (same sugars_g, different delta). "
                f"Violations: {routing_violations[:3]}")

    gate_criteria = [
        {"criterion": "C1",  "name": "directional_distribution",  "pass": c1_pass,  "note": c1_note},
        {"criterion": "C2a", "name": "grade_dist_no_high_sugar_B", "pass": c2a_pass, "note": c2a_note},
        {"criterion": "C2b", "name": "grade_dist_low_sugar_C_plus","pass": c2b_pass, "note": c2b_note},
        {"criterion": "C2c", "name": "magnitude_mean_abs_delta",   "pass": c2c_pass, "note": c2c_note},
        {"criterion": "C3",  "name": "gap_narrows_inversion",      "pass": c3_pass,  "note": c3_note},
        {"criterion": "C4",  "name": "min_movers",                 "pass": c4_pass,  "note": c4_note},
        {"criterion": "C5",  "name": "min_grade_changes",          "pass": c5_pass,  "note": c5_note},
        {"criterion": "C6",  "name": "max_absorption",             "pass": c6_pass,  "note": c6_note},
        {"criterion": "C7",  "name": "anti_immunity",              "pass": c7_pass,  "note": c7_note},
        {"criterion": "C8",  "name": "floor_compliance",           "pass": c8_pass,  "note": c8_note},
        {"criterion": "C9",  "name": "no_scope_bleed",             "pass": c9_pass,  "note": c9_note},
        {"criterion": "C10", "name": "frozen_byte_id_milk",        "pass": c10_pass, "note": c10_note},
        {"criterion": "C11", "name": "routing_agnostic",           "pass": c11_pass, "note": c11_note},
    ]

    criteria_pass = [c["criterion"] for c in gate_criteria if c["pass"]]
    criteria_fail = [c["criterion"] for c in gate_criteria if not c["pass"]]
    all_pass = len(criteria_fail) == 0

    # -----------------------------------------------------------------------
    # STEP 7: Compute score statistics
    # -----------------------------------------------------------------------
    juice_on_scores  = [r["flag_on_score"] for r in juice_rows if r["flag_on_score"] is not None]
    juice_off_scores = [r["flag_off_score"] for r in juice_rows if r["flag_off_score"] is not None]
    grade_dist_on  = Counter(r["flag_on_grade"] for r in juice_rows if r["flag_on_grade"])
    grade_dist_off = Counter(r["flag_off_grade"] for r in juice_rows if r["flag_off_grade"])

    # -----------------------------------------------------------------------
    # STEP 8: Write per-product table (CSV)
    # -----------------------------------------------------------------------
    table_path = OUTPUT_DIR / "juice_pilot_table.csv"
    with table_path.open("w", encoding="utf-8", newline="") as f:
        f.write("barcode,sub_pool,sugars_g,flag_off_score,flag_off_grade,flag_on_score,flag_on_grade,"
                "clean_delta,ev091_floor_applied,sr_penalty,category\n")
        for r in sorted(juice_rows, key=lambda x: -(x["sugars_g"] or 0)):
            f.write(",".join(str(r[k]) for k in [
                "barcode", "sub_pool", "sugars_g", "flag_off_score", "flag_off_grade",
                "flag_on_score", "flag_on_grade", "clean_delta", "ev091_floor_applied",
                "sr_penalty", "category"
            ]) + "\n")

    # -----------------------------------------------------------------------
    # STEP 9: Write run record
    # -----------------------------------------------------------------------
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")
    constants_sha    = sha256_file(pathlib.Path(__file__).parent / "constants.py")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-9 / EV-091",
        "category_slug": "juices",
        "pilot_type": "MEASURED_NOT_PUBLISHED",
        "generated": ts,
        "engine": "proto_v0 / score_engine.py (BARI_SHELF_RELATIVE_V1=on, asymmetric P=6/B=3)",
        "flag_config": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
        },
        "precheck": {
            "juice_sub_pool_null_count": null_pool_count,
            "juice_sub_pool_distribution": dict(pool_dist),
            "result": "PASS" if null_pool_count == 0 else "FAIL",
        },
        "shelf_stats": {
            "nutrient": "sugars_g",
            "proposal_median": PROPOSAL_MEDIAN,
            "proposal_scale": PROPOSAL_SCALE,
            "engine_median": engine_median,
            "engine_scale": engine_scale,
            "used_median": used_median,
            "used_scale": used_scale,
        },
        "corpus": {
            "juice_records_loaded": len(juice_records),
            "milk_records_loaded": len(milk_records),
            "juice_scored": len(juice_rows),
            "milk_scored": len(milk_rows),
            "errors": len(errors),
        },
        "juice_score_distribution": {
            "flag_on": {
                "min": min(juice_on_scores) if juice_on_scores else None,
                "max": max(juice_on_scores) if juice_on_scores else None,
                "median": sorted(juice_on_scores)[len(juice_on_scores)//2] if juice_on_scores else None,
                "stdev": round(stdev(juice_on_scores), 2),
                "grade_dist": dict(grade_dist_on),
            },
            "flag_off": {
                "min": min(juice_off_scores) if juice_off_scores else None,
                "max": max(juice_off_scores) if juice_off_scores else None,
                "median": sorted(juice_off_scores)[len(juice_off_scores)//2] if juice_off_scores else None,
                "stdev": round(stdev(juice_off_scores), 2),
                "grade_dist": dict(grade_dist_off),
            },
        },
        "gate_criteria": gate_criteria,
        "criteria_pass": criteria_pass,
        "criteria_fail": criteria_fail,
        "all_criteria_pass": all_pass,
        "c10_milk_delta_zero_count": len(milk_rows) - len(milk_movers),
        "c10_milk_total": len(milk_rows),
        "milk_rows": milk_rows,
        "juice_rows": juice_rows,
        "off_used": False,
        "score_engine_sha256": score_engine_sha,
        "constants_sha256": constants_sha,
        "errors": errors,
    }

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    # -----------------------------------------------------------------------
    # Print summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(f"JUICES SR PILOT -- {RUN_ID}")
    print("=" * 70)
    print(f"TASK-278 Phase-9 / EV-091 | MEASURED NOT PUBLISHED")
    print(f"Flag: BARI_SHELF_RELATIVE_V1=ON | scope=juice_sub_pool | P=6/B=3 | floor=62@12.2g")
    print()
    print(f"PRECHECK: juice_sub_pool null={null_pool_count}/65 -> {'PASS' if null_pool_count==0 else 'FAIL'}")
    print(f"  Distribution: {dict(pool_dist)}")
    print()
    print(f"SHELF STATS: engine median={engine_median}, scale={engine_scale}")
    print(f"  Proposal: median={PROPOSAL_MEDIAN}, scale={PROPOSAL_SCALE}")
    print()
    print(f"CORPUS: {len(juice_records)} juice | {len(milk_records)} milk | Errors: {len(errors)}")
    print()
    print(f"GRADE DISTRIBUTION (juice):")
    for g in ["A", "B", "C", "D", "E"]:
        print(f"  {g}: off={grade_dist_off.get(g,0)} on={grade_dist_on.get(g,0)}")
    print()
    print(f"12 GATE CRITERIA:")
    for c in gate_criteria:
        status = "PASS" if c["pass"] else "FAIL"
        print(f"  {c['criterion']} [{status}]: {c['name']}")
        print(f"         {c['note']}")
    print()
    print(f"ALL CRITERIA PASS: {all_pass}")
    print(f"PASS: {criteria_pass}")
    print(f"FAIL: {criteria_fail}")
    print()
    print(f"C10 MILK: {len(milk_rows) - len(milk_movers)}/{len(milk_rows)} delta=0")
    print()
    print(f"score_engine.py SHA256: {score_engine_sha[:16]}...")
    print(f"constants.py SHA256:    {constants_sha[:16]}...")
    print(f"Run record: {rr_path}")
    print(f"Table: {table_path}")
    print("=" * 70)

    return run_record


if __name__ == "__main__":
    main()
