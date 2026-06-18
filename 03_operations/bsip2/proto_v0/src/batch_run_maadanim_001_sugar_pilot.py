# BSIP2 batch -- Maadanim x sugar SHELF-RELATIVE PILOT (run_maadanim_001_sugar_pilot)
# TASK-278 Phase-10 / EV-092 -- Maadanim x sugar asymmetric P>B shelf-relative enrollment.
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
    SUGAR_SHELF_REL_MAADANIM_MEDIAN, SUGAR_SHELF_REL_MAADANIM_IQR,
    SUGAR_SHELF_REL_MAADANIM_SCALE, SUGAR_SHELF_REL_MAADANIM_FLOOR,
    SUGAR_SHELF_REL_MAADANIM_FLOOR_THRESHOLD_G,
    SUGAR_SHELF_REL_MAADANIM_P_MAX, SUGAR_SHELF_REL_MAADANIM_B_MAX,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT              = pathlib.Path(r"C:\Bari")
BSIP1_MAAD_DIR   = ROOT / "03_operations" / "bsip1" / "run_maadanim_001" / "output"
MILK_RUN005_DIR  = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
BSIP1_MILK_DIR   = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
BSIP1_YOGURT_DIR = ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"
BSIP1_CHEESE_DIR = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
BSIP1_HC_DIR     = ROOT / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output"
BSIP1_JUICE_DIR  = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
OUTPUT_DIR       = ROOT / "02_products" / "maadanim" / "bsip2_outputs" / "run_maadanim_001_sugar_pilot"
RETURN_DIR       = ROOT / "tasks" / "returns"
RUN_ID = "run_maadanim_001_sugar_pilot"

# Pilot stats from D7 co-sign (P129/EV-092)
PROPOSAL_MEDIAN       = SUGAR_SHELF_REL_MAADANIM_MEDIAN       # 9.70
PROPOSAL_SCALE        = SUGAR_SHELF_REL_MAADANIM_SCALE        # 8.75
PROPOSAL_IQR          = SUGAR_SHELF_REL_MAADANIM_IQR          # 11.78
FLOOR_VALUE           = SUGAR_SHELF_REL_MAADANIM_FLOOR        # 62
FLOOR_THRESHOLD_G     = SUGAR_SHELF_REL_MAADANIM_FLOOR_THRESHOLD_G  # 16.08

# Gate C3 inversions (barcodes from D7):
# INV-A: 7290110573751 (18.0g sugar) vs 7290110573737 (3.4g sugar) -- gap must narrow (high penalized more)
# INV-B: 2385455 (3.5g sugar) vs 5014271300429 (52.0g sugar) -- directional reversal
INV_A_HIGH_BC = "7290110573751"
INV_A_LOW_BC  = "7290110573737"
INV_B_LOW_BC  = "2385455"
INV_B_HIGH_BC = "5014271300429"

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
    """Score with flag OFF by temporarily toggling the module-level boolean."""
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
    return trace


def load_bsip1_dir(directory, glob_pattern="bsip1_*.json", label=""):
    records = []
    for p in sorted(pathlib.Path(directory).glob(glob_pattern)):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            records.append(doc)
        except Exception as e:
            log.error("Load error [%s] %s: %s", label, p.name, e)
    log.info("%s BSIP1 records loaded: %d", label, len(records))
    return records


def load_milk_run005():
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
    return milk_records


def score_corpus(records, corpus_label, errors):
    rows = []
    for doc in records:
        barcode = str(doc.get("barcode", ""))
        name    = doc.get("canonical_name_he", "") or doc.get("product_name_he", "")
        nn      = doc.get("normalized_nutrition_per_100g") or {}
        sugars_g = nn.get("sugars_g")
        maad_subtype = doc.get("bsip_maadanim_subtype")
        try:
            trace_on  = run_bsip2_pipeline(doc)
            trace_off = run_bsip2_pipeline_flag_off(doc)
            score_on  = trace_on.get("final_score_estimate")
            score_off = trace_off.get("final_score_estimate")
            grade_on  = trace_on.get("grade_estimate")
            grade_off = trace_off.get("grade_estimate")
            delta     = round(score_on - score_off, 2) if (score_on is not None and score_off is not None) else None
            category  = trace_on.get("category")
            floor_app = trace_on.get("ev092_maadanim_floor_applied")
            sr_pen_on = None
            for p in (trace_on.get("penalties_applied") or []):
                if p.get("rule") == "SUGAR_MAADANIM_SHELF_REL_V1":
                    sr_pen_on = p.get("amount")
                    break
            ev092_fired = (sr_pen_on is not None and sr_pen_on != 0) or (floor_app is True)
            rows.append({
                "barcode": barcode,
                "name": name,
                "corpus": corpus_label,
                "bsip_maadanim_subtype": maad_subtype,
                "sugars_g": sugars_g,
                "flag_off_score": score_off,
                "flag_off_grade": grade_off,
                "flag_on_score": score_on,
                "flag_on_grade": grade_on,
                "delta": delta,
                "ev092_fired": ev092_fired,
                "ev092_maadanim_floor_applied": floor_app,
                "sr_penalty": sr_pen_on,
                "category": category,
            })
            log.info("  [%s] %-45s sugar=%-5s off=%s/%s on=%s/%s delta=%s floor=%s",
                     corpus_label, name[:43], sugars_g, score_off, grade_off, score_on, grade_on, delta, floor_app)
        except Exception as e:
            log.error("  ERROR [%s] %s (%s): %s", corpus_label, barcode, name, e)
            import traceback; traceback.print_exc()
            errors.append({"corpus": corpus_label, "barcode": barcode, "name": name, "error": str(e)})
    return rows


def main():
    assert BARI_SHELF_RELATIVE_V1, "CRITICAL: BARI_SHELF_RELATIVE_V1 must be ON for pilot run"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-278 Phase-10 EV-092: Maadanim x Sugar SR Pilot -- %s ===", RUN_ID)
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")

    # -----------------------------------------------------------------------
    # STEP 1: Load all corpora
    # -----------------------------------------------------------------------
    maad_records   = load_bsip1_dir(BSIP1_MAAD_DIR, "bsip1_*.json", "maadanim")
    milk_records   = load_milk_run005()
    yogurt_records = load_bsip1_dir(BSIP1_YOGURT_DIR, "bsip1_*.json", "yogurt")
    cheese_records = load_bsip1_dir(BSIP1_CHEESE_DIR, "bsip1_*.json", "cheese_spread")
    hc_records     = load_bsip1_dir(BSIP1_HC_DIR, "bsip1_hardcheese_*.json", "hard_cheese")
    juice_records  = load_bsip1_dir(BSIP1_JUICE_DIR, "bsip1_*.json", "juice")

    # -----------------------------------------------------------------------
    # STEP 2: Precheck bsip_maadanim_subtype coverage
    # -----------------------------------------------------------------------
    maad_with_subtype = [r for r in maad_records if r.get("bsip_maadanim_subtype") is not None]
    maad_with_sugars  = [r for r in maad_records if (r.get("normalized_nutrition_per_100g") or {}).get("sugars_g") is not None]
    maad_sugar_scope  = [r for r in maad_records
                         if r.get("bsip_maadanim_subtype") is not None
                         and (r.get("normalized_nutrition_per_100g") or {}).get("sugars_g") is not None]
    subtype_dist = Counter(r.get("bsip_maadanim_subtype") for r in maad_records if r.get("bsip_maadanim_subtype"))
    log.info("Maadanim: total=%d, with_subtype=%d/200, with_sugars_g=%d/200, EV-092 scope (both)=%d",
             len(maad_records), len(maad_with_subtype), len(maad_with_sugars), len(maad_sugar_scope))
    log.info("Subtype distribution: %s", dict(subtype_dist))

    # -----------------------------------------------------------------------
    # STEP 3: Set shelf stats from D7 (n=146 approved; use proposal stats)
    # -----------------------------------------------------------------------
    # Compute from actual corpus for verification vs proposal
    engine_median, engine_scale = compute_shelf_stats(
        maad_sugar_scope,
        "sugars_g",
        scale_type="iqr",
        nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
    )
    log.info("Engine computed: median=%.3f, scale=%.3f (proposal: median=%.3f, scale=%.3f)",
             engine_median or 0, engine_scale or 0, PROPOSAL_MEDIAN, PROPOSAL_SCALE)

    clear_shelf_stats()
    set_shelf_stats(
        nutrient="sugars_g",
        median=engine_median if engine_median is not None else PROPOSAL_MEDIAN,
        scale=engine_scale if engine_scale is not None else PROPOSAL_SCALE,
        scale_type="iqr",
        n=len(maad_sugar_scope),
    )
    used_median = engine_median if engine_median is not None else PROPOSAL_MEDIAN
    used_scale  = engine_scale if engine_scale is not None else PROPOSAL_SCALE
    log.info("Shelf stats set: sugars_g median=%.3f scale=%.3f", used_median, used_scale)

    # -----------------------------------------------------------------------
    # STEP 4: Score all corpora
    # -----------------------------------------------------------------------
    errors = []
    log.info("--- Scoring maadanim corpus (%d products) ---", len(maad_records))
    maad_rows   = score_corpus(maad_records, "maadanim", errors)
    log.info("--- Scoring milk corpus (%d products) C10 check ---", len(milk_records))
    milk_rows   = score_corpus(milk_records, "milk", errors)
    log.info("--- Scoring yogurt corpus (%d products) C10b ---", len(yogurt_records))
    yogurt_rows = score_corpus(yogurt_records, "yogurt", errors)
    log.info("--- Scoring cheese_spread corpus (%d products) C10c ---", len(cheese_records))
    cheese_rows = score_corpus(cheese_records, "cheese_spread", errors)
    log.info("--- Scoring hard_cheese corpus (%d products) C10d ---", len(hc_records))
    hc_rows     = score_corpus(hc_records, "hard_cheese", errors)
    log.info("--- Scoring juice corpus (%d products) C10e ---", len(juice_records))
    juice_rows  = score_corpus(juice_records, "juice", errors)

    # Filter to EV-092 sugar scope (146): bsip_maadanim_subtype not None AND sugars_g not None
    maad_sugar_rows = [r for r in maad_rows
                       if r["bsip_maadanim_subtype"] is not None and r["sugars_g"] is not None]
    log.info("EV-092 sugar scope (both guards): %d maadanim products", len(maad_sugar_rows))

    # -----------------------------------------------------------------------
    # STEP 5: Gate criteria evaluation
    # -----------------------------------------------------------------------
    log.info("--- Evaluating gate criteria ---")

    # C1: directional_distribution
    above_median = [r for r in maad_sugar_rows if r["sugars_g"] is not None and r["sugars_g"] > PROPOSAL_MEDIAN]
    below_median = [r for r in maad_sugar_rows if r["sugars_g"] is not None and r["sugars_g"] < PROPOSAL_MEDIAN]
    above_deltas = [r["delta"] for r in above_median if r["delta"] is not None]
    below_deltas = [r["delta"] for r in below_median if r["delta"] is not None]
    c1_above_mean = sum(above_deltas) / len(above_deltas) if above_deltas else None
    c1_below_mean = sum(below_deltas) / len(below_deltas) if below_deltas else None
    c1_pass = (c1_above_mean is not None and c1_above_mean <= 0) and (c1_below_mean is not None and c1_below_mean >= 0)
    c1_above_str = f"{c1_above_mean:.3f}" if c1_above_mean is not None else "N/A"
    c1_below_str = f"{c1_below_mean:.3f}" if c1_below_mean is not None else "N/A"
    c1_note = (f"above_median(sugars_g>{PROPOSAL_MEDIAN}g, n={len(above_median)}) mean_delta={c1_above_str} (need<=0); "
               f"below_median(n={len(below_median)}) mean_delta={c1_below_str} (need>=0)")

    # C2a: grade_dist — net A+B+C count not degraded overall
    grade_off_dist = Counter(r["flag_off_grade"] for r in maad_sugar_rows if r["flag_off_grade"])
    grade_on_dist  = Counter(r["flag_on_grade"] for r in maad_sugar_rows if r["flag_on_grade"])
    abc_off = sum(grade_off_dist.get(g, 0) for g in ["A", "B", "C"])
    abc_on  = sum(grade_on_dist.get(g, 0) for g in ["A", "B", "C"])
    c2a_pass = abc_on >= abc_off
    c2a_note = f"A+B+C: off={abc_off} on={abc_on} (need on>=off). Grade dists: off={dict(grade_off_dist)} on={dict(grade_on_dist)}"

    # C2b: grade absorption — no single grade absorbs >40% of movers
    movers = [r for r in maad_sugar_rows if r["delta"] is not None and r["delta"] != 0]
    if movers:
        mover_grades_on = Counter(r["flag_on_grade"] for r in movers if r["flag_on_grade"])
        max_grade_count = max(mover_grades_on.values()) if mover_grades_on else 0
        max_grade_pct   = max_grade_count / len(movers) * 100
        max_grade_name  = max(mover_grades_on, key=mover_grades_on.get) if mover_grades_on else "N/A"
        c2b_pass = max_grade_pct <= 40.0
        c2b_note = f"Max grade absorption among movers: {max_grade_name}={max_grade_count}/{len(movers)}={max_grade_pct:.1f}% (need<=40%)"
    else:
        c2b_pass = True
        c2b_note = "No movers — absorption N/A"

    # C2c: magnitude — mean |delta| for movers in [0.5, P_max=6]
    mover_abs_deltas = [abs(r["delta"]) for r in movers if r["delta"] is not None]
    c2c_mean_abs = sum(mover_abs_deltas) / len(mover_abs_deltas) if mover_abs_deltas else 0
    c2c_pass = len(movers) > 0 and 0.5 <= c2c_mean_abs <= SUGAR_SHELF_REL_MAADANIM_P_MAX
    c2c_note = f"movers={len(movers)}, mean|delta|={c2c_mean_abs:.3f} (need in [0.5, {SUGAR_SHELF_REL_MAADANIM_P_MAX}])"

    # C3: gap_narrows_inversion
    def find_by_barcode(rows, bc):
        for r in rows:
            if str(r["barcode"]) == str(bc):
                return r
        return None

    inv_a_high = find_by_barcode(maad_rows, INV_A_HIGH_BC)
    inv_a_low  = find_by_barcode(maad_rows, INV_A_LOW_BC)
    inv_b_low  = find_by_barcode(maad_rows, INV_B_LOW_BC)
    inv_b_high = find_by_barcode(maad_rows, INV_B_HIGH_BC)

    c3_inv_a_gap_off = c3_inv_a_gap_on = c3_inv_a_pass = None
    if inv_a_high and inv_a_low:
        # INV-A: high-sugar (18g) should be penalized more than low-sugar (3.4g) at flag-on
        # gap = high_score - low_score; should NARROW (high penalized more) at flag-on
        c3_inv_a_gap_off = round((inv_a_high["flag_off_score"] or 0) - (inv_a_low["flag_off_score"] or 0), 2)
        c3_inv_a_gap_on  = round((inv_a_high["flag_on_score"] or 0) - (inv_a_low["flag_on_score"] or 0), 2)
        # gap should narrow (or reverse) -- high penalized more, so gap should be more negative or smaller
        c3_inv_a_pass = c3_inv_a_gap_on < c3_inv_a_gap_off

    c3_inv_b_gap_off = c3_inv_b_gap_on = c3_inv_b_pass = None
    if inv_b_low and inv_b_high:
        # INV-B: 2385455 (3.5g) vs 5014271300429 (52g)
        # |gap| flag-on < flag-off AND directional reversal (low-sugar scores >= high-sugar)
        gap_off = round(abs((inv_b_low["flag_off_score"] or 0) - (inv_b_high["flag_off_score"] or 0)), 2)
        gap_on  = round(abs((inv_b_low["flag_on_score"] or 0) - (inv_b_high["flag_on_score"] or 0)), 2)
        c3_inv_b_gap_off = gap_off
        c3_inv_b_gap_on  = gap_on
        # directional reversal: at flag-on low-sugar should score >= high-sugar
        reversal = (inv_b_low["flag_on_score"] or 0) >= (inv_b_high["flag_on_score"] or 0)
        c3_inv_b_pass = gap_on < gap_off and reversal

    c3_pass = (c3_inv_a_pass is True) and (c3_inv_b_pass is True)
    c3_note = (
        f"INV-A ({INV_A_HIGH_BC} 18g vs {INV_A_LOW_BC} 3.4g): "
        f"gap_off={c3_inv_a_gap_off} gap_on={c3_inv_a_gap_on} -> {'PASS' if c3_inv_a_pass else 'FAIL'}; "
        f"INV-B ({INV_B_LOW_BC} 3.5g vs {INV_B_HIGH_BC} 52g): "
        f"|gap|_off={c3_inv_b_gap_off} |gap|_on={c3_inv_b_gap_on} -> {'PASS' if c3_inv_b_pass else 'FAIL'}"
    )

    # C4: min_movers — >= 5 maadanim products with |delta| >= 1pt
    big_movers = [r for r in maad_sugar_rows if r["delta"] is not None and abs(r["delta"]) >= 1.0]
    c4_pass = len(big_movers) >= 5
    c4_note = f"{len(big_movers)} maadanim products with |delta|>=1pt (need>=5)"

    # C5: min_grade_changes — >= 1 maadanim product with grade change
    grade_changers = [r for r in maad_sugar_rows if r["flag_off_grade"] != r["flag_on_grade"]]
    c5_pass = len(grade_changers) >= 1
    c5_note = (f"{len(grade_changers)} maadanim products with grade change (need>=1). "
               f"Examples: {[{'bc': r['barcode'], 'off': r['flag_off_grade'], 'on': r['flag_on_grade']} for r in grade_changers[:3]]}")

    # C6: max_absorption — dead zone <= 40% of scored maadanim products
    # Dead zone = bsip_maadanim_subtype not None AND sugars_g not None but delta=0
    in_dead_zone = [r for r in maad_sugar_rows if r["delta"] == 0 or r["delta"] is None]
    dead_zone_pct = (len(in_dead_zone) / len(maad_sugar_rows) * 100) if maad_sugar_rows else 0
    c6_pass = dead_zone_pct <= 40.0
    c6_note = f"Dead zone (delta=0): {len(in_dead_zone)}/{len(maad_sugar_rows)}={dead_zone_pct:.1f}% (need<=40%)"

    # C7: anti_immunity — 0 maadanim products with sugars_g >= 16.08g at grade B (score>=70) at flag-on
    high_sugar_b = [r for r in maad_sugar_rows
                    if r["sugars_g"] is not None and r["sugars_g"] >= FLOOR_THRESHOLD_G
                    and r["flag_on_score"] is not None and r["flag_on_score"] >= 70]
    c7_pass = len(high_sugar_b) == 0
    c7_note = (f"{len(high_sugar_b)} maadanim products with sugars_g>={FLOOR_THRESHOLD_G}g at grade B at flag-on "
               f"(need=0). Violators: {[r['barcode'] for r in high_sugar_b]}")

    # C8: floor_compliance — all maadanim products with sugars_g >= 16.08g: flag-on score <= 62
    above_threshold  = [r for r in maad_sugar_rows if r["sugars_g"] is not None and r["sugars_g"] >= FLOOR_THRESHOLD_G]
    floor_violators  = [r for r in above_threshold if r["flag_on_score"] is not None and r["flag_on_score"] > FLOOR_VALUE]
    c8_pass = len(floor_violators) == 0
    c8_note = (f"{len(above_threshold)} products with sugars_g>={FLOOR_THRESHOLD_G}g, "
               f"{len(floor_violators)} floor violations (score>{FLOOR_VALUE}). "
               f"Violators: {[r['barcode'] for r in floor_violators]}")

    # C9: no_scope_bleed — 0 non-maadanim products show EV-092 fired
    non_maad_rows = milk_rows + yogurt_rows + cheese_rows + hc_rows + juice_rows
    bleed_products = [r for r in non_maad_rows if r.get("ev092_fired") or r.get("ev092_maadanim_floor_applied")]
    c9_pass = len(bleed_products) == 0
    c9_note = f"{len(bleed_products)} non-maadanim products with EV-092 fired (need=0). Examples: {[r['barcode'] for r in bleed_products[:3]]}"

    # C10: frozen_byte_id_milk — 20/20 milk delta=0 CRITICAL
    milk_movers = [r for r in milk_rows if r["delta"] is not None and r["delta"] != 0]
    c10_pass = len(milk_rows) == 20 and len(milk_movers) == 0
    if not c10_pass:
        log.error("CRITICAL FAIL C10: milk delta != 0 for %d products! STOP.", len(milk_movers))
    c10_note = (f"{len(milk_rows)} milk products loaded, "
                f"{len(milk_rows) - len(milk_movers)}/20 with delta=0.0 (need 20/20). "
                f"Movers: {[{'bc': r['barcode'], 'delta': r['delta']} for r in milk_movers]}")

    # C10b: yogurt_isolation — 0 yogurt products show SUGAR_MAADANIM_SHELF_REL_V1 fired
    yogurt_ev092 = [r for r in yogurt_rows if r.get("ev092_fired") or r.get("ev092_maadanim_floor_applied")]
    c10b_pass = len(yogurt_ev092) == 0
    c10b_note = f"{len(yogurt_ev092)} yogurt products with EV-092 fired (need=0)"

    # C10c: cheese_spread_isolation — 0 cheese_spread products show SUGAR_MAADANIM_SHELF_REL_V1 fired
    cheese_ev092 = [r for r in cheese_rows if r.get("ev092_fired") or r.get("ev092_maadanim_floor_applied")]
    c10c_pass = len(cheese_ev092) == 0
    c10c_note = f"{len(cheese_ev092)} cheese_spread products with EV-092 fired (need=0)"

    # C10d: hard_cheese_isolation
    hc_ev092 = [r for r in hc_rows if r.get("ev092_fired") or r.get("ev092_maadanim_floor_applied")]
    c10d_pass = len(hc_ev092) == 0
    c10d_note = f"{len(hc_ev092)} hard_cheese products with EV-092 fired (need=0)"

    # C10e: juice_isolation
    juice_ev092 = [r for r in juice_rows if r.get("ev092_fired") or r.get("ev092_maadanim_floor_applied")]
    c10e_pass = len(juice_ev092) == 0
    c10e_note = f"{len(juice_ev092)} juice products with EV-092 fired (need=0)"

    # C11: flag_off_drift — docs only, non-blocking
    # Check that flag-off scores are stable vs prior run (we don't have a prior run_record; note as N/A)
    c11_pass = True
    c11_note = "flag_off_drift: non-blocking informational only (no prior baseline to compare)"

    gate_criteria = [
        {"criterion": "C1",   "name": "directional_distribution",    "pass": c1_pass,   "note": c1_note},
        {"criterion": "C2a",  "name": "grade_dist",                  "pass": c2a_pass,  "note": c2a_note},
        {"criterion": "C2b",  "name": "grade_absorption",            "pass": c2b_pass,  "note": c2b_note},
        {"criterion": "C2c",  "name": "magnitude",                   "pass": c2c_pass,  "note": c2c_note},
        {"criterion": "C3",   "name": "gap_narrows_inversion",       "pass": c3_pass,   "note": c3_note},
        {"criterion": "C4",   "name": "min_movers",                  "pass": c4_pass,   "note": c4_note},
        {"criterion": "C5",   "name": "min_grade_changes",           "pass": c5_pass,   "note": c5_note},
        {"criterion": "C6",   "name": "max_absorption",              "pass": c6_pass,   "note": c6_note},
        {"criterion": "C7",   "name": "anti_immunity",               "pass": c7_pass,   "note": c7_note},
        {"criterion": "C8",   "name": "floor_compliance",            "pass": c8_pass,   "note": c8_note},
        {"criterion": "C9",   "name": "no_scope_bleed",              "pass": c9_pass,   "note": c9_note},
        {"criterion": "C10",  "name": "frozen_byte_id_milk",         "pass": c10_pass,  "note": c10_note},
        {"criterion": "C10b", "name": "yogurt_isolation",            "pass": c10b_pass, "note": c10b_note},
        {"criterion": "C10c", "name": "cheese_spread_isolation",     "pass": c10c_pass, "note": c10c_note},
        {"criterion": "C10d", "name": "hard_cheese_isolation",       "pass": c10d_pass, "note": c10d_note},
        {"criterion": "C10e", "name": "juice_isolation",             "pass": c10e_pass, "note": c10e_note},
        {"criterion": "C11",  "name": "flag_off_drift",              "pass": c11_pass,  "note": c11_note},
    ]

    criteria_pass = [c["criterion"] for c in gate_criteria if c["pass"]]
    criteria_fail = [c["criterion"] for c in gate_criteria if not c["pass"]]
    all_pass = len(criteria_fail) == 0
    hard_criteria = ["C1","C2a","C2b","C2c","C3","C4","C5","C6","C7","C8","C9","C10","C10b","C10c","C10d","C10e"]
    hard_pass = all(c["pass"] for c in gate_criteria if c["criterion"] in hard_criteria)

    # -----------------------------------------------------------------------
    # STEP 6: Per-product table
    # -----------------------------------------------------------------------
    table_path = OUTPUT_DIR / "maadanim_pilot_table.csv"
    with table_path.open("w", encoding="utf-8", newline="") as f:
        f.write("barcode,bsip_maadanim_subtype,sugars_g,flag_off_score,flag_off_grade,"
                "flag_on_score,flag_on_grade,delta,ev092_fired,ev092_maadanim_floor_applied,category\n")
        for r in sorted(maad_rows, key=lambda x: -(x["sugars_g"] or 0)):
            f.write(",".join(str(r.get(k, "")) for k in [
                "barcode", "bsip_maadanim_subtype", "sugars_g",
                "flag_off_score", "flag_off_grade",
                "flag_on_score", "flag_on_grade",
                "delta", "ev092_fired", "ev092_maadanim_floor_applied", "category"
            ]) + "\n")

    # -----------------------------------------------------------------------
    # STEP 7: Write run_record.json
    # -----------------------------------------------------------------------
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")
    constants_sha    = sha256_file(pathlib.Path(__file__).parent / "constants.py")

    # biscuit/cereal routing for EV-085 interaction note
    biscuit_cereal_products = [r for r in maad_rows if r.get("category") in ("biscuit", "cereal")]

    on_scores  = [r["flag_on_score"] for r in maad_sugar_rows if r["flag_on_score"] is not None]
    off_scores = [r["flag_off_score"] for r in maad_sugar_rows if r["flag_off_score"] is not None]

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-10 / EV-092",
        "category_slug": "maadanim",
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
            "maadanim_total": len(maad_records),
            "maadanim_with_subtype": len(maad_with_subtype),
            "maadanim_with_sugars_g": len(maad_with_sugars),
            "ev092_sugar_scope_n": len(maad_sugar_scope),
            "subtype_distribution": dict(subtype_dist),
        },
        "shelf_stats": {
            "nutrient": "sugars_g",
            "proposal_median": PROPOSAL_MEDIAN,
            "proposal_scale": PROPOSAL_SCALE,
            "proposal_iqr": PROPOSAL_IQR,
            "engine_median": engine_median,
            "engine_scale": engine_scale,
            "used_median": used_median,
            "used_scale": used_scale,
            "n_for_stats": len(maad_sugar_scope),
        },
        "corpus": {
            "maadanim_loaded": len(maad_records),
            "maadanim_sugar_scope_n": len(maad_sugar_rows),
            "milk_loaded": len(milk_records),
            "yogurt_loaded": len(yogurt_records),
            "cheese_spread_loaded": len(cheese_records),
            "hard_cheese_loaded": len(hc_records),
            "juice_loaded": len(juice_records),
            "errors": len(errors),
        },
        "score_distribution": {
            "flag_on": {
                "min": min(on_scores) if on_scores else None,
                "max": max(on_scores) if on_scores else None,
                "median": sorted(on_scores)[len(on_scores)//2] if on_scores else None,
                "stdev": round(stdev(on_scores), 2),
                "grade_dist": dict(grade_on_dist),
            },
            "flag_off": {
                "min": min(off_scores) if off_scores else None,
                "max": max(off_scores) if off_scores else None,
                "median": sorted(off_scores)[len(off_scores)//2] if off_scores else None,
                "stdev": round(stdev(off_scores), 2),
                "grade_dist": dict(grade_off_dist),
            },
        },
        "movers_n": len(movers),
        "big_movers_n": len(big_movers),
        "grade_changes_n": len(grade_changers),
        "mean_abs_delta_movers": round(c2c_mean_abs, 3),
        "dead_zone_pct": round(dead_zone_pct, 1),
        "floor_applied_count": len([r for r in maad_rows if r.get("ev092_maadanim_floor_applied")]),
        "c10_milk_delta_zero_count": len(milk_rows) - len(milk_movers),
        "c10_milk_total": len(milk_rows),
        "biscuit_cereal_routing_n": len(biscuit_cereal_products),
        "biscuit_cereal_products": [{"barcode": r["barcode"], "name": r["name"], "category": r["category"],
                                      "sugars_g": r["sugars_g"], "delta": r["delta"]}
                                     for r in biscuit_cereal_products],
        "gate_criteria": gate_criteria,
        "criteria_pass": criteria_pass,
        "criteria_fail": criteria_fail,
        "all_criteria_pass": all_pass,
        "hard_criteria_pass": hard_pass,
        "maadanim_product_table": sorted(maad_rows, key=lambda x: -(x["sugars_g"] or 0)),
        "milk_rows": milk_rows,
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
    print(f"MAADANIM SR PILOT -- {RUN_ID}")
    print("=" * 70)
    print(f"TASK-278 Phase-10 / EV-092 | MEASURED NOT PUBLISHED")
    print(f"Flag: BARI_SHELF_RELATIVE_V1=ON | scope=bsip_maadanim_subtype | P=6/B=3 | floor=62@{FLOOR_THRESHOLD_G}g")
    print()
    print(f"PRECHECK: maadanim_total={len(maad_records)} with_subtype={len(maad_with_subtype)} with_sugars={len(maad_with_sugars)} scope={len(maad_sugar_rows)}")
    print(f"  Subtype dist: {dict(subtype_dist)}")
    print()
    print(f"SHELF STATS: engine median={engine_median}, scale={engine_scale}")
    print(f"  Proposal: median={PROPOSAL_MEDIAN}, scale={PROPOSAL_SCALE}")
    print()
    print(f"CORPUS: maadanim={len(maad_records)} | milk={len(milk_records)} | yogurt={len(yogurt_records)} | "
          f"cheese_spread={len(cheese_records)} | hard_cheese={len(hc_records)} | juice={len(juice_records)}")
    print(f"Errors: {len(errors)}")
    print()
    print(f"GRADE DISTRIBUTION (maadanim sugar scope, n={len(maad_sugar_rows)}):")
    for g in ["S", "A", "B", "C", "D", "E"]:
        print(f"  {g}: off={grade_off_dist.get(g,0)} on={grade_on_dist.get(g,0)}")
    print()
    print(f"MOVERS (|delta|>0): {len(movers)}/{len(maad_sugar_rows)}")
    print(f"BIG MOVERS (|delta|>=1): {len(big_movers)}/{len(maad_sugar_rows)}")
    print(f"GRADE CHANGES: {len(grade_changers)}")
    print(f"MEAN |DELTA| (movers): {c2c_mean_abs:.3f}")
    print(f"DEAD ZONE: {dead_zone_pct:.1f}%")
    print(f"FLOOR APPLIED: {run_record['floor_applied_count']}")
    print()
    if biscuit_cereal_products:
        print(f"BISCUIT/CEREAL-ROUTED (EV-085 interaction possible): {len(biscuit_cereal_products)}")
        for r in biscuit_cereal_products[:5]:
            print(f"  [{r['category']}] {r['barcode']} sugar={r['sugars_g']} delta={r['delta']}")
    print()
    print(f"{len(gate_criteria)} GATE CRITERIA:")
    for c in gate_criteria:
        status = "PASS" if c["pass"] else "FAIL"
        print(f"  {c['criterion']:4s} [{status}]: {c['name']}")
        print(f"        {c['note']}")
    print()
    print(f"ALL CRITERIA PASS: {all_pass}")
    print(f"HARD CRITERIA PASS: {hard_pass}")
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
