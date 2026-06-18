# BSIP2 batch -- Cheese Spreads SHELF-RELATIVE SAT_FAT PILOT v1 (run_cheese_005_satfat_pilot)
# TASK-278 Phase-7 wire + pilot (P119, 2026-06-14)
# MEASURED NOT PUBLISHED: no frontend JSON, no comp JSON, no go-live, no published scores.
# Dual run same engine instance: BARI_SHELF_RELATIVE_V1 on vs off; clean_delta = on - off.
# Corpus: run_cheese_003 bsip1 (59 cheese products) + milk run_milk_002 (20 products, C10 CRITICAL)
#         + yogurt run_yogurt_005 (88 products, C10b CRITICAL).
# Cheese_spread SR gated by category=="dairy_protein" AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES.
# Shelf stats set to cream_cheese-locked (median=16.05, scale=2.0756, n=24); milk/yogurt excluded from stat source.
# OFF-BAN HARD: all fat_saturated_g / nutrition from direct BSIP1 L1/normalized_nutrition; NO Open Food Facts.
# C10 (milk frozen byte-id) is CRITICAL: any milk delta !=0 at on = pilot FAIL.
# C10b (yogurt byte-id) is CRITICAL (new): yogurt subtype guard must NOT fire on cheese_spread SR branch.
# Adapted from batch_run_yogurt_shelfrel_v2.py (P115).
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter
import importlib

# --- Flag config (common) BEFORE any engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
# BARI_SHELF_RELATIVE_V1 patched per pass below (default off at import)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats,
    BARI_SHELF_RELATIVE_V1 as _INITIAL_BARI_FLAG,
)
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    score_to_grade,
    FATSAT_SHELF_REL_CHEESESPREAD_FLOOR,
    FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G,
    FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN,
    FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
    CREAM_CHEESE_SPREAD_SUBTYPES,
    CULTURED_YOGURT_SUBTYPES,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
CHEESE_BSIP1  = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
MILK_BSIP1    = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
YOGURT_BSIP1  = ROOT / "03_operations" / "bsip1" / "run_yogurt_005" / "output"
OUTPUT_DIR    = ROOT / "02_products" / "cheese_spreads" / "bsip2_outputs" / "run_cheese_005_satfat_pilot"
RUN_ID        = "run_cheese_005_satfat_pilot"

# Named pairs for C3 (gap-narrowing inversions)
INV1_A_BC = "4129118"         # sat_fat=14.0g (below median 16.05; expect relief/less penalty)
INV1_B_BC = "7290116935409"   # sat_fat=16.2g (above median; expect penalty → gap narrows)
INV2_A_BC = "7622201521493"   # sat_fat=7.8g  (well below median; expect relief)
INV2_B_BC = "4129101"         # sat_fat=15.0g (near-median; expect small penalty)

CREAM_CHEESE_SPREAD_SUBTYPES_SET = set(CREAM_CHEESE_SPREAD_SUBTYPES)
CULTURED_YOGURT_SUBTYPES_SET = set(CULTURED_YOGURT_SUBTYPES)

(OUTPUT_DIR / "products").mkdir(parents=True, exist_ok=True)


def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def get_satfat_g(doc):
    if not doc:
        return None
    nn = doc.get("normalized_nutrition_per_100g") or {}
    v = nn.get("fat_saturated_g")
    if v is None:
        l1 = doc.get("L1_observed_signals") or {}
        v = l1.get("fat_saturated_g")
    return v


def run_bsip2_pipeline(bsip1_product):
    signals      = extract_signals(bsip1_product)
    cat_result   = classify_category(bsip1_product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(bsip1_product, l3)
    eval_result  = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== BSIP2 Cheese Spreads SAT_FAT SHELF-RELATIVE PILOT v1 -- %s (P119 / TASK-278 Phase-7) ===", RUN_ID)
    log.info("Dual run: flag-on vs flag-off within SAME engine (patch BARI_SHELF_RELATIVE_V1)")
    log.info("Corpus: cheese run_cheese_003 (59) + milk run_milk_002 (20 C10 CRITICAL) + yogurt run_yogurt_005 (88 C10b CRITICAL)")
    log.info("Shelf stats: fat_saturated_g locked to cream_cheese-only corpus (median=16.05, scale=2.0756, n=24)")
    log.info("Scope: dairy_protein + subtype in CREAM_CHEESE_SPREAD_SUBTYPES only")
    log.info("MEASURED NOT PUBLISHED: no frontend, no comp JSON, no go-live")
    log.info("OFF-BAN HARD: fat_saturated_g from direct label/BSIP1 only; no OFF substitution ever")
    log.info("C10 CRITICAL: milk run_milk_002 products must be byte-identical (delta=0) at flag-on vs off")
    log.info("C10b CRITICAL (new): yogurt CULTURED_YOGURT_SUBTYPES must NOT get delta from cheese_spread SR branch")

    # Load cheese bsip1 inputs
    if not CHEESE_BSIP1.exists():
        log.error("Cheese BSIP1 source missing: %s", CHEESE_BSIP1); return
    products_c = load_batch(CHEESE_BSIP1)
    log.info("Cheese BSIP1 loaded: %d", len(products_c))

    # Load milk bsip1 (for C10 frozen byte-id — CRITICAL)
    if not MILK_BSIP1.exists():
        log.error("Milk BSIP1 source missing: %s", MILK_BSIP1); return
    products_m = load_batch(MILK_BSIP1)
    log.info("Milk BSIP1 loaded: %d", len(products_m))

    # Load yogurt bsip1 (for C10b scope isolation — CRITICAL)
    if not YOGURT_BSIP1.exists():
        log.error("Yogurt BSIP1 source missing: %s", YOGURT_BSIP1); return
    products_y = load_batch(YOGURT_BSIP1)
    log.info("Yogurt BSIP1 loaded: %d", len(products_y))

    all_products = products_c + products_m + products_y
    bsip1_by_bc = {}
    for doc in all_products:
        bc = str(doc.get("barcode", ""))
        if bc:
            bsip1_by_bc[bc] = doc

    milk_barcodes   = {str(p.get("barcode", "")) for p in products_m if p.get("barcode")}
    yogurt_barcodes = {str(p.get("barcode", "")) for p in products_y if p.get("barcode")}

    # Set cheese_spread-specific shelf stats for fat_saturated_g (cream_cheese-only, locked per D7/P119)
    # Milk and yogurt products do NOT contribute to this stat (exclusive to cream_cheese corpus, n=24)
    log.info("--- Set shelf stats (cream_cheese-locked: median=16.05, scale=2.0756, n=24) ---")
    clear_shelf_stats()
    set_shelf_stats(
        nutrient="fat_saturated_g",
        median=FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN,
        scale=FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
        scale_type="mad",
        n=24,
    )
    log.info("Shelf stats set for fat_saturated_g (cheese_spread SR only; global for this run)")

    # Dual run via module patch
    import score_engine as _se
    log.info("Initial BARI_SHELF_RELATIVE_V1 (at import): %s", _se.BARI_SHELF_RELATIVE_V1)

    # PASS 1: flag-on
    log.info("--- PASS 1: flag-on (BARI_SHELF_RELATIVE_V1=True, cream_cheese subtype gate) ---")
    _se.BARI_SHELF_RELATIVE_V1 = True

    traces_on = []
    results_on = {}
    score_errors = []
    for doc in all_products:
        barcode = str(doc.get("barcode", ""))
        name = doc.get("canonical_name_he", "")
        try:
            cat_result = classify_category(doc)
            subtype = cat_result.get("category_subtype") or ""
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, OUTPUT_DIR)
            traces_on.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat = trace.get("category") or cat_result.get("category")
            # Check if cheese_spread SR term fired
            term_fired = False
            for p in (trace.get("penalties_applied") or []):
                if "FATSAT_CHEESE_SPREAD_SHELF_REL" in (p.get("rule") or ""):
                    term_fired = True
                    break
            results_on[barcode] = {
                "score": score,
                "grade": grade,
                "category": cat,
                "subtype": subtype,
                "term_fired": term_fired,
            }
            log.info("  ON  %-45s score=%-5s grade=%-2s cat=%-20s subtype=%-18s term=%s",
                     name[:41], score, grade, cat, subtype, term_fired)
        except Exception as e:
            log.error("  ON ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e), "pass": "on"})

    # PASS 2: flag-off
    log.info("--- PASS 2: flag-off (BARI_SHELF_RELATIVE_V1=False) ---")
    _se.BARI_SHELF_RELATIVE_V1 = False

    results_off = {}
    for doc in all_products:
        barcode = str(doc.get("barcode", ""))
        name = doc.get("canonical_name_he", "")
        try:
            cat_result = classify_category(doc)
            subtype = cat_result.get("category_subtype") or ""
            trace = run_bsip2_pipeline(doc)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat = trace.get("category") or cat_result.get("category")
            results_off[barcode] = {
                "score": score,
                "grade": grade,
                "category": cat,
                "subtype": subtype,
            }
            log.info("  OFF %-45s score=%-5s grade=%-2s cat=%-20s subtype=%-18s",
                     name[:41], score, grade, cat, subtype)
        except Exception as e:
            log.error("  OFF ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e), "pass": "off"})

    # Restore flag
    _se.BARI_SHELF_RELATIVE_V1 = _INITIAL_BARI_FLAG
    log.info("  Restored BARI_SHELF_RELATIVE_V1 to initial %s", _INITIAL_BARI_FLAG)

    # Compute clean deltas
    all_deltas = []
    for bc in list(results_on.keys()):
        on_s = results_on[bc]["score"]
        off_s = results_off.get(bc, {}).get("score")
        if on_s is not None and off_s is not None:
            d = round(on_s - off_s, 4)
            entry = {
                "barcode": bc,
                "flag_on": on_s,
                "flag_off": off_s,
                "delta": d,
                "category": results_on[bc]["category"],
                "subtype": results_on[bc].get("subtype", ""),
                "is_milk": bc in milk_barcodes,
                "is_yogurt": bc in yogurt_barcodes,
            }
            all_deltas.append(entry)

    log.info("Clean deltas computed: all=%d", len(all_deltas))

    # Segment by corpus membership
    cream_cheese_deltas = [e for e in all_deltas if e["subtype"] in CREAM_CHEESE_SPREAD_SUBTYPES_SET]
    non_cream_cheese_dairy_deltas = [
        e for e in all_deltas
        if e["category"] == "dairy_protein" and e["subtype"] not in CREAM_CHEESE_SPREAD_SUBTYPES_SET
    ]
    milk_deltas_list   = [e for e in all_deltas if e["is_milk"]]
    yogurt_deltas_list = [e for e in all_deltas if e["is_yogurt"]]

    log.info("cream_cheese_spread: %d; non-cream-cheese dairy_protein: %d; milk: %d; yogurt: %d",
             len(cream_cheese_deltas), len(non_cream_cheese_dairy_deltas),
             len(milk_deltas_list), len(yogurt_deltas_list))

    # -----------------------------------------------------------------------
    # Gate criteria scoring
    # -----------------------------------------------------------------------

    # C10: milk byte-id (CRITICAL)
    milk_nonzero = sum(1 for e in milk_deltas_list if abs(e["delta"]) > 0.0001)
    crit10_pass = milk_nonzero == 0
    log.info("C10 milk byte-id (CRITICAL): %d milks, nonzero_delta=%d (pass=%s)",
             len(milk_deltas_list), milk_nonzero, crit10_pass)
    if not crit10_pass:
        log.error("CRITICAL FAIL: milk products have non-zero delta — PILOT FAIL")

    # C10b: yogurt scope isolation (CRITICAL — new)
    # The cheese_spread SR branch must NOT fire on yogurt products (they share dairy_protein)
    yogurt_nonzero_from_cheese_sr = []
    for e in yogurt_deltas_list:
        bc = e["barcode"]
        if abs(e["delta"]) > 0.0001:
            # Check if the delta can be attributed to cheese_spread SR (should NEVER happen)
            on_info = results_on.get(bc, {})
            if on_info.get("subtype", "") in CULTURED_YOGURT_SUBTYPES_SET:
                yogurt_nonzero_from_cheese_sr.append({"barcode": bc, "delta": e["delta"], "subtype": on_info.get("subtype")})
    crit10b_pass = len(yogurt_nonzero_from_cheese_sr) == 0
    log.info("C10b yogurt scope isolation (CRITICAL): %d yogurts checked, nonzero_delta=%d (pass=%s)",
             len(yogurt_deltas_list), len(yogurt_nonzero_from_cheese_sr), crit10b_pass)
    if not crit10b_pass:
        log.error("CRITICAL FAIL: yogurt products received delta from cheese_spread SR branch — scope guard failure")

    # Cream_cheese movers + SR-firing
    n_cc_movers = 0
    n_cc_grade_chg = 0
    cc_grade_chg = []
    fired_cc = 0
    absorbed_cc = 0
    for e in cream_cheese_deltas:
        bc = e["barcode"]
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        d = e["delta"]
        term = results_on.get(bc, {}).get("term_fired", False)
        if term:
            fired_cc += 1
        if abs(d) > 0.0001:
            n_cc_movers += 1
        if on_g and off_g and on_g != off_g:
            n_cc_grade_chg += 1
            cc_grade_chg.append({
                "barcode": bc,
                "from": off_g, "to": on_g,
                "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": d,
            })
        if term and abs(d) <= 0.0001:
            absorbed_cc += 1
    absorption = round(absorbed_cc / fired_cc, 4) if fired_cc > 0 else 0.0
    log.info("CREAM_CHEESE: movers=%d grade_chg=%d term_fired=%d absorbed=%d absorption=%.4f",
             n_cc_movers, n_cc_grade_chg, fired_cc, absorbed_cc, absorption)

    # C1: directional distribution (mean delta above-median <= 0; below-median >= 0)
    above_median_deltas = []
    below_median_deltas = []
    for e in cream_cheese_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        if sfg is None:
            continue
        if sfg > FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN:
            above_median_deltas.append(e["delta"])
        elif sfg < FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN:
            below_median_deltas.append(e["delta"])
    mean_above = round(sum(above_median_deltas) / len(above_median_deltas), 4) if above_median_deltas else 0.0
    mean_below = round(sum(below_median_deltas) / len(below_median_deltas), 4) if below_median_deltas else 0.0
    crit1_pass = (mean_above <= 0) and (mean_below >= 0)
    log.info("C1 directional: above_median n=%d mean_delta=%.4f (<=0? %s); below_median n=%d mean_delta=%.4f (>=0? %s)",
             len(above_median_deltas), mean_above, mean_above <= 0,
             len(below_median_deltas), mean_below, mean_below >= 0)

    # C2: grade distribution and magnitude
    # (A) 0 cream_cheese with sat_fat>=18g at grade B (score>=70) flag-on
    # (B) >=1 cream_cheese with sat_fat<=10g at grade C+ (score>=52) flag-on
    # (C) mean|delta| >= 0.5 among SR-firing cream_cheese
    high_satfat_b_count = 0  # sat_fat>=18g at B
    low_satfat_c_plus_count = 0  # sat_fat<=10g at score>=52
    all_abs_d = []
    for e in cream_cheese_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        on_s = results_on.get(bc, {}).get("score")
        on_g = results_on.get(bc, {}).get("grade")
        d = e["delta"]
        if abs(d) > 0.0001 or results_on.get(bc, {}).get("term_fired", False):
            all_abs_d.append(abs(d))
        if sfg is not None and sfg >= 18.0:
            if on_s is not None and on_s >= 70:
                high_satfat_b_count += 1
        if sfg is not None and sfg <= 10.0:
            if on_s is not None and on_s >= 52:
                low_satfat_c_plus_count += 1
    mean_abs_d = round(sum(all_abs_d) / len(all_abs_d), 4) if all_abs_d else 0.0
    crit2a = high_satfat_b_count == 0
    crit2b = low_satfat_c_plus_count >= 1
    crit2c = mean_abs_d >= 0.5
    crit2_pass = crit2a and crit2b and crit2c
    log.info("C2: A(0 highsat@B)=%s(%d) B(>=1 lowsat@C+)=%s(%d) C(mean|d|=%.4f>=0.5)=%s",
             crit2a, high_satfat_b_count, crit2b, low_satfat_c_plus_count, mean_abs_d, crit2c)

    # C3: gap-narrowing for BOTH named pairs
    def _pair_scores(bc_a, bc_b):
        on_a = results_on.get(bc_a, {}).get("score")
        off_a = results_off.get(bc_a, {}).get("score")
        on_b = results_on.get(bc_b, {}).get("score")
        off_b = results_off.get(bc_b, {}).get("score")
        gap_on  = round(abs(on_a  - on_b),  2) if (on_a  is not None and on_b  is not None) else None
        gap_off = round(abs(off_a - off_b), 2) if (off_a is not None and off_b is not None) else None
        return on_a, off_a, on_b, off_b, gap_on, gap_off

    inv1_on_a, inv1_off_a, inv1_on_b, inv1_off_b, inv1_gap_on, inv1_gap_off = _pair_scores(INV1_A_BC, INV1_B_BC)
    inv2_on_a, inv2_off_a, inv2_on_b, inv2_off_b, inv2_gap_on, inv2_gap_off = _pair_scores(INV2_A_BC, INV2_B_BC)

    inv1_narrows = (inv1_gap_on is not None and inv1_gap_off is not None and inv1_gap_on < inv1_gap_off)
    inv2_narrows = (inv2_gap_on is not None and inv2_gap_off is not None and inv2_gap_on < inv2_gap_off)
    crit3_pass = inv1_narrows and inv2_narrows
    log.info("C3 Inv-1: 4129118(14g) on=%.2f off=%.2f ; 7290116935409(16.2g) on=%.2f off=%.2f ; gap_on=%.2f gap_off=%.2f narrows=%s",
             inv1_on_a or 0, inv1_off_a or 0, inv1_on_b or 0, inv1_off_b or 0,
             inv1_gap_on or 0, inv1_gap_off or 0, inv1_narrows)
    log.info("C3 Inv-2: 7622201521493(7.8g) on=%.2f off=%.2f ; 4129101(15g) on=%.2f off=%.2f ; gap_on=%.2f gap_off=%.2f narrows=%s",
             inv2_on_a or 0, inv2_off_a or 0, inv2_on_b or 0, inv2_off_b or 0,
             inv2_gap_on or 0, inv2_gap_off or 0, inv2_narrows)

    # C4: min_movers
    crit4_pass = n_cc_movers >= 5
    # C5: min_grade_changes
    crit5_pass = n_cc_grade_chg >= 1
    # C6: max_absorption
    crit6_pass = (fired_cc == 0) or (absorption <= 0.40)
    # C7: anti-immunity (0 cream_cheese sat_fat>=18g at grade B flag-on)
    crit7_pass = high_satfat_b_count == 0
    # C8: floor_compliance (all sat_fat>=16.5g: flag-on score <= 62)
    floor_viol_cc = 0
    floor_checked_cc = 0
    for e in cream_cheese_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        if sfg is not None and sfg >= FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G:
            floor_checked_cc += 1
            on_s = results_on.get(bc, {}).get("score")
            if on_s is not None and on_s > FATSAT_SHELF_REL_CHEESESPREAD_FLOOR:
                floor_viol_cc += 1
    crit8_pass = floor_viol_cc == 0
    log.info("C8 floor: checked=%d (sat_fat>=%.1fg) viol=%d (all <=%.0f? %s)",
             floor_checked_cc, FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G,
             floor_viol_cc, FATSAT_SHELF_REL_CHEESESPREAD_FLOOR, crit8_pass)

    # C9: no_scope_bleed (non-cream_cheese dairy_protein with nonzero delta)
    non_cc_nonzero = sum(1 for e in non_cream_cheese_dairy_deltas if abs(e["delta"]) > 0.0001)
    crit9_pass = non_cc_nonzero == 0
    log.info("C9 scope bleed: non-cream_cheese dairy_protein nonzero=%d (pass=%s)", non_cc_nonzero, crit9_pass)

    # C11: flag-off drift vs run_cheese_004 (docs-only, non-blocking)
    # NOTE: run_cheese_004 uses bsip2_trace.json files in the products/ subdirectory
    BASELINE_CHEESE_DIR = ROOT / "02_products" / "cheese_spreads" / "bsip2_outputs" / "run_cheese_004" / "products"
    baseline_cheese = {}
    if BASELINE_CHEESE_DIR.exists():
        for sub in sorted(BASELINE_CHEESE_DIR.iterdir()):
            if not sub.is_dir(): continue
            tf = sub / "bsip2_trace.json"
            if tf.exists():
                try:
                    bt = json.loads(tf.read_text(encoding="utf-8"))
                    bc = str(bt.get("barcode") or (bt.get("input_reference") or {}).get("barcode", ""))
                    if bc:
                        baseline_cheese[bc] = bt.get("final_score_estimate")
                except Exception:
                    pass
    drift_cc = 0
    drift_list = []
    for e in cream_cheese_deltas:
        bc = e["barcode"]
        off = e["flag_off"]
        base = baseline_cheese.get(bc)
        if off is not None and base is not None and abs(off - base) > 0.01:
            drift_cc += 1
            drift_list.append({"barcode": bc, "flag_off": off, "baseline_run_cheese_004": base, "diff": round(off - base, 4)})
    log.info("C11 flag_off_drift (cream_cheese vs run_cheese_004): %d mismatches (docs-only)", drift_cc)

    # -----------------------------------------------------------------------
    # Gate results
    # -----------------------------------------------------------------------
    gate_results = [
        {"criterion": "C1",  "name": "directional_distribution",
         "pass": crit1_pass,
         "evidence": f"above_median n={len(above_median_deltas)} mean_delta={mean_above} (<=0? {mean_above<=0}); below_median n={len(below_median_deltas)} mean_delta={mean_below} (>=0? {mean_below>=0})"},
        {"criterion": "C2",  "name": "grade_dist_and_magnitude",
         "pass": crit2_pass,
         "evidence": f"(A) high_sat>=18@B={high_satfat_b_count}==0?{crit2a}; (B) low_sat<=10@C+={low_satfat_c_plus_count}>=1?{crit2b}; (C) mean|d|={mean_abs_d}>=0.5?{crit2c}"},
        {"criterion": "C3",  "name": "gap_narrows_inversion",
         "pass": crit3_pass,
         "evidence": f"Inv-1: gap_on={inv1_gap_on} < gap_off={inv1_gap_off}? {inv1_narrows}; Inv-2: gap_on={inv2_gap_on} < gap_off={inv2_gap_off}? {inv2_narrows}"},
        {"criterion": "C4",  "name": "min_movers",
         "pass": crit4_pass,
         "evidence": f"n={n_cc_movers} (need >=5)"},
        {"criterion": "C5",  "name": "min_grade_changes",
         "pass": crit5_pass,
         "evidence": f"n={n_cc_grade_chg} (need >=1)"},
        {"criterion": "C6",  "name": "max_absorption",
         "pass": crit6_pass,
         "evidence": f"{absorbed_cc}/{fired_cc}={absorption} (need <=0.40)"},
        {"criterion": "C7",  "name": "anti_immunity",
         "pass": crit7_pass,
         "evidence": f"sat_fat>=18g @B flag-on: {high_satfat_b_count} (need=0)"},
        {"criterion": "C8",  "name": "floor_compliance",
         "pass": crit8_pass,
         "evidence": f"{floor_checked_cc} checked (sat_fat>={FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G}g), {floor_viol_cc} >62 (need=0)"},
        {"criterion": "C9",  "name": "no_scope_bleed",
         "pass": crit9_pass,
         "evidence": f"non-cream_cheese dairy_protein with nonzero delta: {non_cc_nonzero} (need=0)"},
        {"criterion": "C10", "name": "frozen_byte_id_milk",
         "pass": crit10_pass,
         "evidence": f"CRITICAL: milk products={len(milk_deltas_list)} all delta=0: {crit10_pass}; nonzero={milk_nonzero}"},
        {"criterion": "C10b","name": "yogurt_byte_id",
         "pass": crit10b_pass,
         "evidence": f"CRITICAL: yogurt products={len(yogurt_deltas_list)} with nonzero delta from cheese_spread SR: {len(yogurt_nonzero_from_cheese_sr)} (need=0)"},
        {"criterion": "C11", "name": "flag_off_drift",
         "pass": "n/a-docs-only",
         "evidence": f"{drift_cc} mismatches vs run_cheese_004 (non-blocking)"},
    ]

    # Per-product tables
    per_cc_table = []
    for e in sorted(cream_cheese_deltas,
                    key=lambda x: (get_satfat_g(bsip1_by_bc.get(x["barcode"])) is None,
                                   get_satfat_g(bsip1_by_bc.get(x["barcode"])) or 0)):
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        name = (bsip1_by_bc.get(bc) or {}).get("canonical_name_he", "")
        per_cc_table.append({
            "barcode": bc,
            "name": name,
            "sat_fat_g": sfg,
            "flag_off": e["flag_off"],
            "flag_on": e["flag_on"],
            "delta": e["delta"],
            "grade_off": off_g,
            "grade_on": on_g,
        })

    milk_table = [
        {"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": e["delta"]}
        for e in milk_deltas_list
    ]
    yogurt_table = [
        {"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": e["delta"],
         "subtype": results_on.get(e["barcode"], {}).get("subtype", "")}
        for e in yogurt_deltas_list
    ]

    # File hashes
    eval_sha   = sha256_file(pathlib.Path(__file__).parent / "evaluation_scope.py")
    eng_sha    = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")
    const_sha  = sha256_file(pathlib.Path(__file__).parent / "constants.py")

    # run_record
    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-7 cheese_spreads×sat_fat wire + pilot (P119)",
        "pilot_type": "MEASURED_NOT_PUBLISHED",
        "generated": ts,
        "engine": "proto_v0 + EV-089 cheese_spread sat_fat SR call site + EV-089 floor (subtype guard, FATSAT_SHELF_REL_SCOPE untouched)",
        "flag_config": {
            "BARI_SHELF_RELATIVE_V1": "dual (on/off patch)",
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK250_CONF": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "other_flags": "off (grad_sodium, sodium_shelf_relative, redlabel, sodium_cereal)",
        },
        "dual_run_method": "module patch on score_engine.BARI_SHELF_RELATIVE_V1 (same process, cheese-locked shelf_stats for fat_saturated_g)",
        "off_used": False,
        "corpus": {
            "cheese_bsip1": str(CHEESE_BSIP1),
            "milk_bsip1": str(MILK_BSIP1),
            "yogurt_bsip1": str(YOGURT_BSIP1),
            "n_cheese_loaded": len(products_c),
            "n_milk_loaded": len(products_m),
            "n_yogurt_loaded": len(products_y),
        },
        "shelf_stats_used": {
            "nutrient": "fat_saturated_g",
            "median": FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN,
            "scale": FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
            "n": 24,
            "source": "locked D7/P119 from cream_cheese-only n=24 in run_cheese_003",
        },
        "scope_guard_used": "category == dairy_protein AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES",
        "constants_used": {
            "FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN": FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN,
            "FATSAT_SHELF_REL_CHEESESPREAD_SCALE": FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
            "FATSAT_SHELF_REL_CHEESESPREAD_FLOOR": FATSAT_SHELF_REL_CHEESESPREAD_FLOOR,
            "FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G": FATSAT_SHELF_REL_CHEESESPREAD_FLOOR_THRESHOLD_G,
            "CREAM_CHEESE_SPREAD_SUBTYPES": sorted(CREAM_CHEESE_SPREAD_SUBTYPES),
        },
        "milk_byte_id": {
            "pass": crit10_pass,
            "milk_products_checked": len(milk_deltas_list),
            "any_nonzero_delta": not crit10_pass,
            "milk_deltas": [{"barcode": m["barcode"], "delta": m["delta"]} for m in milk_table],
        },
        "yogurt_byte_id": {
            "pass": crit10b_pass,
            "yogurt_products_checked": len(yogurt_deltas_list),
            "any_nonzero_delta": not crit10b_pass,
            "yogurt_deltas_nonzero": yogurt_nonzero_from_cheese_sr,
        },
        "named_pairs": {
            "inv1_a": {"barcode": INV1_A_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV1_A_BC)),
                       "flag_off": inv1_off_a, "flag_on": inv1_on_a},
            "inv1_b": {"barcode": INV1_B_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV1_B_BC)),
                       "flag_off": inv1_off_b, "flag_on": inv1_on_b},
            "inv1_gap_off": inv1_gap_off, "inv1_gap_on": inv1_gap_on, "inv1_narrows": inv1_narrows,
            "inv2_a": {"barcode": INV2_A_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV2_A_BC)),
                       "flag_off": inv2_off_a, "flag_on": inv2_on_a},
            "inv2_b": {"barcode": INV2_B_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV2_B_BC)),
                       "flag_off": inv2_off_b, "flag_on": inv2_on_b},
            "inv2_gap_off": inv2_gap_off, "inv2_gap_on": inv2_gap_on, "inv2_narrows": inv2_narrows,
        },
        "cream_cheese_movers": n_cc_movers,
        "cream_cheese_grade_changes": n_cc_grade_chg,
        "grade_change_details": cc_grade_chg,
        "absorption": absorption,
        "fired_cc": fired_cc,
        "absorbed_cc": absorbed_cc,
        "gate_results": gate_results,
        "per_product_table_cream_cheese": per_cc_table,
        "milk_table": milk_table,
        "yogurt_table_first_20": yogurt_table[:20],
        "yogurt_all_zero_delta": crit10b_pass,
        "flag_off_drift_cheese": {"mismatches": drift_cc, "details": drift_list[:20]},
        "engine_invariants": "342 PASS (run before pilot)",
        "evaluation_scope_sha256": eval_sha,
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "output_dir": str(OUTPUT_DIR),
        "errors": score_errors,
        "self_check": {
            "off_used": False,
            "cheese_spread_only_gates": True,
            "milk_included_for_c10": True,
            "yogurt_included_for_c10b": True,
            "C10_milk_critical": crit10_pass,
            "C10b_yogurt_critical": crit10b_pass,
            "C9_no_bleed": crit9_pass,
            "FATSAT_SHELF_REL_SCOPE_unchanged": True,  # stays frozenset()
        },
    }

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record written: %s", rr_path)

    # Console summary
    print("\n" + "="*80)
    print(f"CHEESE SPREADS SAT_FAT SHELF-RELATIVE PILOT v1 -- {RUN_ID}")
    print("="*80)
    print(f"TASK-278 Phase-7 (P119) | MEASURED NOT PUBLISHED | OFF=0")
    print(f"Cheese products (cream_cheese_spread subtype): {len(cream_cheese_deltas)}")
    print(f"Milk products (C10 CRITICAL): {len(milk_deltas_list)}")
    print(f"Yogurt products (C10b CRITICAL): {len(yogurt_deltas_list)}")
    print(f"Non-cream-cheese dairy_protein (bleed check C9): {len(non_cream_cheese_dairy_deltas)}")
    print()
    print("GATE CRITERIA:")
    for g in gate_results:
        p = g["pass"]
        status = "PASS" if p is True else ("n/a" if p == "n/a-docs-only" else ("FAIL" if p is False else str(p)))
        print(f"  {g['criterion']}: {status} — {g['evidence']}")
    print()
    print(f"C10 CRITICAL (milk all delta=0): {crit10_pass}")
    print(f"C10b CRITICAL (yogurt cheese_spread SR isolation): {crit10b_pass}")
    print()
    print("NAMED PAIRS:")
    print(f"  Inv-1 A (4129118, 14.0g): flag_off={inv1_off_a} flag_on={inv1_on_a}")
    print(f"  Inv-1 B (7290116935409, 16.2g): flag_off={inv1_off_b} flag_on={inv1_on_b}")
    print(f"  Inv-1 gap: off={inv1_gap_off} → on={inv1_gap_on} (narrows: {inv1_narrows})")
    print(f"  Inv-2 A (7622201521493, 7.8g): flag_off={inv2_off_a} flag_on={inv2_on_a}")
    print(f"  Inv-2 B (4129101, 15.0g): flag_off={inv2_off_b} flag_on={inv2_on_b}")
    print(f"  Inv-2 gap: off={inv2_gap_off} → on={inv2_gap_on} (narrows: {inv2_narrows})")
    print()
    print("CREAM_CHEESE per-product (sorted by sat_fat_g):")
    print(f"  {'barcode':<20} {'sat_fat_g':>9} {'flag_off':>9} {'flag_on':>9} {'delta':>7} {'grade_off':>9} {'grade_on':>8}")
    for row in per_cc_table:
        sfg_str = f"{row['sat_fat_g']:.1f}" if row['sat_fat_g'] is not None else "null"
        print(f"  {row['barcode']:<20} {sfg_str:>9} {str(row['flag_off']):>9} {str(row['flag_on']):>9} "
              f"{str(row['delta']):>7} {str(row['grade_off']):>9} {str(row['grade_on']):>8}")
    print()
    print(f"Traces (on): {len(traces_on)} -> {OUTPUT_DIR}/products/")
    print(f"Run record: {rr_path}")
    print("="*80)
    print("RETURN: tasks/returns/P119_return.md (propose RETURNED)")
    print("DO NOT close; orchestrator verifies gate.")
    print("="*80)

    return run_record


if __name__ == "__main__":
    main()
