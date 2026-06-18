# BSIP2 batch -- Hard Cheeses SHELF-RELATIVE SAT_FAT PILOT v1 (run_hard_cheeses_002_satfat_pilot)
# TASK-278 Phase-8 hard_cheeses×sat_fat shelf-relative pilot (P123, 2026-06-14)
# MEASURED NOT PUBLISHED: no frontend JSON, no comp JSON, no go-live, no published scores.
# Dual run same engine instance: BARI_SHELF_RELATIVE_V1 on vs off; clean_delta = on - off.
# Corpus:
#   Hard cheeses: run_hard_cheeses_001 bsip1 (37 products)
#   Milk: run_milk_002 BSIP1 (41 products; C10 CRITICAL — all must have delta=0)
#   Yogurt: run_yogurt_006 BSIP1 (89 products; C10c CRITICAL)
#   Cheese spreads: run_cheese_003 BSIP1 (59 products; C10b CRITICAL)
# Scope guard: category=="dairy_protein" AND bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS.
# Shelf stats set to hard_cheese-locked (median=18.0, scale=1.40, n=22; D7/P123).
# OFF-BAN HARD: all fat_saturated_g / nutrition from direct BSIP1 L1/normalized_nutrition; NO Open Food Facts.
# C10 (milk frozen byte-id) is CRITICAL: any milk delta !=0 at flag-on = pilot FAIL.
# C10b (cheese_spread byte-id) is CRITICAL: cheese_spread SR branch must NOT fire on hard_cheese SR.
# C10c (yogurt byte-id) is CRITICAL: yogurt products must NOT get delta from hard_cheese SR branch.
# Adapted from batch_run_cheese_shelfrel_v1.py (P119 / TASK-278 Phase-7).
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
    FATSAT_SHELF_REL_HARDCHEESE_FLOOR,
    FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G,
    FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
    FATSAT_SHELF_REL_HARDCHEESE_SCALE,
    HARD_CHEESE_YELLOW_SUBPOOLS,
    CREAM_CHEESE_SPREAD_SUBTYPES,
    CULTURED_YOGURT_SUBTYPES,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
HARDCHEESE_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output"
MILK_BSIP1       = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
YOGURT_BSIP1     = ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"
CHEESE_BSIP1     = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
OUTPUT_DIR       = ROOT / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hard_cheeses_002_satfat_pilot"
RUN_ID           = "run_hard_cheeses_002_satfat_pilot"

# C3 inversion barcodes (hard_cheese corpus)
# INV-1: |score(7290000062426 yellow_light/5.5g) - score(7290000062433 yellow/17.5g)|
#         expect gap narrows: ~11.3 (on) < ~13.3 (off) -- yellow_light below-median gets relief
# INV-2: |score(7290000062426 yellow_light/5.5g) - score(8866972 yellow/19.5g)|
#         expect gap narrows: ~0.6 (on) < ~5.6 (off) -- 8866972 gets penalty (above median), 62426 gets relief
INV1_A_BC = "7290000062426"   # yellow_light, sat_fat=5.5g (below median 18.0g)
INV1_B_BC = "7290000062433"   # yellow, sat_fat=17.5g (below median, slight relief)
INV2_A_BC = "7290000062426"   # yellow_light, sat_fat=5.5g (below median)
INV2_B_BC = "8866972"         # yellow, sat_fat=19.5g (above median, floor)

HARD_CHEESE_YELLOW_SUBPOOLS_SET = set(HARD_CHEESE_YELLOW_SUBPOOLS)
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
    log.info("=== BSIP2 Hard Cheeses SAT_FAT SHELF-RELATIVE PILOT v1 -- %s (P123 / TASK-278 Phase-8) ===", RUN_ID)
    log.info("Dual run: flag-on vs flag-off within SAME engine (patch BARI_SHELF_RELATIVE_V1)")
    log.info("Corpus: hard_cheeses run_hard_cheeses_001 (37) + milk run_milk_002 (41 C10 CRITICAL) + yogurt run_yogurt_006 (89 C10c CRITICAL) + cheese run_cheese_003 (59 C10b CRITICAL)")
    log.info("Shelf stats: fat_saturated_g locked to hard_cheese-only corpus (median=18.0, scale=1.40, n=22)")
    log.info("Scope: dairy_protein + bsip_cheese_subpool in {yellow, yellow_light, hard_grating} only")
    log.info("MEASURED NOT PUBLISHED: no frontend, no comp JSON, no go-live")
    log.info("OFF-BAN HARD: fat_saturated_g from direct label/BSIP1 only; no OFF substitution ever")
    log.info("C10 CRITICAL: milk run_milk_002 products must be byte-identical (delta=0) at flag-on vs off")
    log.info("C10b CRITICAL: cheese_spread products must NOT get delta from hard_cheese SR branch")
    log.info("C10c CRITICAL: yogurt products must NOT get delta from hard_cheese SR branch")

    # Load hard cheese bsip1 inputs
    if not HARDCHEESE_BSIP1.exists():
        log.error("Hard cheese BSIP1 source missing: %s", HARDCHEESE_BSIP1); return
    products_hc = load_batch(HARDCHEESE_BSIP1)
    log.info("Hard Cheese BSIP1 loaded: %d", len(products_hc))

    # Load milk bsip1 (for C10 frozen byte-id — CRITICAL)
    if not MILK_BSIP1.exists():
        log.error("Milk BSIP1 source missing: %s", MILK_BSIP1); return
    products_m = load_batch(MILK_BSIP1)
    log.info("Milk BSIP1 loaded: %d", len(products_m))

    # Load yogurt bsip1 (for C10c scope isolation — CRITICAL)
    if not YOGURT_BSIP1.exists():
        log.error("Yogurt BSIP1 source missing: %s", YOGURT_BSIP1); return
    products_y = load_batch(YOGURT_BSIP1)
    log.info("Yogurt BSIP1 loaded: %d", len(products_y))

    # Load cheese_spread bsip1 (for C10b scope isolation — CRITICAL)
    if not CHEESE_BSIP1.exists():
        log.error("Cheese_spread BSIP1 source missing: %s", CHEESE_BSIP1); return
    products_cs = load_batch(CHEESE_BSIP1)
    log.info("Cheese_spread BSIP1 loaded: %d", len(products_cs))

    all_products = products_hc + products_m + products_y + products_cs
    bsip1_by_bc = {}
    for doc in all_products:
        bc = str(doc.get("barcode", ""))
        if bc:
            bsip1_by_bc[bc] = doc

    hc_barcodes     = {str(p.get("barcode", "")) for p in products_hc if p.get("barcode")}
    milk_barcodes   = {str(p.get("barcode", "")) for p in products_m if p.get("barcode")}
    yogurt_barcodes = {str(p.get("barcode", "")) for p in products_y if p.get("barcode")}
    cheese_barcodes = {str(p.get("barcode", "")) for p in products_cs if p.get("barcode")}

    # Set hard_cheese-specific shelf stats for fat_saturated_g (locked per D7/P123)
    # Only the yellow/yellow_light/hard_grating subpool contributes (n=22, scope A)
    # Milk, yogurt, and cheese_spread products do NOT contribute to this stat
    log.info("--- Set shelf stats (hard_cheese-locked: median=18.0, scale=1.40, n=22) ---")
    clear_shelf_stats()
    set_shelf_stats(
        nutrient="fat_saturated_g",
        median=FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,   # 18.0
        scale=FATSAT_SHELF_REL_HARDCHEESE_SCALE,      # 1.40
        scale_type="mad",
        n=22,
    )
    log.info("Shelf stats set for fat_saturated_g (hard_cheese SR only; global for this run)")

    # Dual run via module patch
    import score_engine as _se
    log.info("Initial BARI_SHELF_RELATIVE_V1 (at import): %s", _se.BARI_SHELF_RELATIVE_V1)

    # PASS 1: flag-on
    log.info("--- PASS 1: flag-on (BARI_SHELF_RELATIVE_V1=True, hard_cheese subpool gate) ---")
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
            bsip_subpool = doc.get("bsip_cheese_subpool")
            trace = run_bsip2_pipeline(doc)
            # Only write traces for hard_cheese products (pilot artifacts)
            if barcode in hc_barcodes:
                write_trace(trace, OUTPUT_DIR)
                traces_on.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat = trace.get("category") or cat_result.get("category")
            ev090_floor = trace.get("ev090_hard_cheese_floor_applied", False)
            # Check if hard_cheese SR term fired (FATSAT_HARDCHEESE_SHELF_REL_V1)
            hc_term_fired = False
            for p in (trace.get("penalties_applied") or []):
                if "FATSAT_HARDCHEESE_SHELF_REL" in (p.get("rule") or ""):
                    hc_term_fired = True
                    break
            results_on[barcode] = {
                "score": score,
                "grade": grade,
                "category": cat,
                "subtype": subtype,
                "bsip_subpool": bsip_subpool,
                "hc_term_fired": hc_term_fired,
                "ev090_floor": ev090_floor,
            }
            log.info("  ON  %-45s score=%-5s grade=%-2s subpool=%-14s hc_term=%s floor=%s",
                     name[:41], score, grade, str(bsip_subpool), hc_term_fired, ev090_floor)
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
            log.info("  OFF %-45s score=%-5s grade=%-2s",
                     name[:41], score, grade)
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
            subpool = results_on[bc].get("bsip_subpool")
            entry = {
                "barcode": bc,
                "flag_on": on_s,
                "flag_off": off_s,
                "clean_delta": d,
                "category": results_on[bc]["category"],
                "subtype": results_on[bc].get("subtype", ""),
                "bsip_cheese_subpool": subpool,
                "is_hc": bc in hc_barcodes,
                "is_milk": bc in milk_barcodes,
                "is_yogurt": bc in yogurt_barcodes,
                "is_cheese_spread": bc in cheese_barcodes,
                "hc_term_fired": results_on[bc].get("hc_term_fired", False),
                "ev090_hard_cheese_floor_applied": results_on[bc].get("ev090_floor", False),
            }
            all_deltas.append(entry)

    log.info("Clean deltas computed: all=%d", len(all_deltas))

    # Segment by corpus
    hc_yellow_deltas = [e for e in all_deltas
                        if e["is_hc"] and e["bsip_cheese_subpool"] in HARD_CHEESE_YELLOW_SUBPOOLS_SET]
    hc_all_deltas    = [e for e in all_deltas if e["is_hc"]]
    non_hc_dairy_deltas = [
        e for e in all_deltas
        if e["category"] == "dairy_protein" and not e["is_hc"]
    ]
    milk_deltas_list   = [e for e in all_deltas if e["is_milk"]]
    yogurt_deltas_list = [e for e in all_deltas if e["is_yogurt"]]
    cheese_spread_deltas_list = [e for e in all_deltas if e["is_cheese_spread"]]

    log.info("hc_yellow_subpool: %d; hc_all: %d; non_hc_dairy: %d; milk: %d; yogurt: %d; cheese_spread: %d",
             len(hc_yellow_deltas), len(hc_all_deltas),
             len(non_hc_dairy_deltas), len(milk_deltas_list),
             len(yogurt_deltas_list), len(cheese_spread_deltas_list))

    # -----------------------------------------------------------------------
    # Gate criteria scoring (P123 / TASK-278 Phase-8)
    # -----------------------------------------------------------------------

    # C10: milk byte-id (CRITICAL)
    milk_nonzero = sum(1 for e in milk_deltas_list if abs(e["clean_delta"]) > 0.0001)
    crit10_pass = milk_nonzero == 0
    log.info("C10 milk byte-id (CRITICAL): %d milks, nonzero_delta=%d (pass=%s)",
             len(milk_deltas_list), milk_nonzero, crit10_pass)
    if not crit10_pass:
        log.error("CRITICAL FAIL: milk products have non-zero delta — PILOT FAIL")

    # C10b: cheese_spread scope isolation (CRITICAL)
    # The hard_cheese SR branch must NOT fire on cheese_spread products.
    # Note: EV-089 (cheese_spread floor) may fire on cheese_spreads when BARI_SHELF_RELATIVE_V1=True —
    # that is EXPECTED. C10b only checks that EV-090 (hard_cheese SR) does NOT contribute delta to cheese_spreads.
    # Since the scope guard is bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS, cheese_spreads
    # (which have cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES, not bsip_cheese_subpool) should be unaffected.
    # We check: any cheese_spread with hc_term_fired=True
    cheese_spread_hc_fired = [
        e for e in cheese_spread_deltas_list
        if e.get("hc_term_fired", False)
    ]
    crit10b_pass = len(cheese_spread_hc_fired) == 0
    log.info("C10b cheese_spread scope isolation (CRITICAL): %d cheese_spreads, EV-090 fired on: %d (pass=%s)",
             len(cheese_spread_deltas_list), len(cheese_spread_hc_fired), crit10b_pass)
    if not crit10b_pass:
        log.error("CRITICAL FAIL: cheese_spread products received delta from EV-090 hard_cheese SR branch — scope guard failure")

    # C10c: yogurt scope isolation (CRITICAL)
    # The hard_cheese SR branch must NOT fire on yogurt products.
    # Note: EV-088 (yogurt sugar floor) may still fire for high-sugar yogurts when BARI_SHELF_RELATIVE_V1=True.
    # That is EXPECTED behavior from EV-088, NOT a failure of C10c.
    # C10c checks: EV-090 hard_cheese SR must NOT contribute delta to yogurts.
    yogurt_hc_fired = [
        e for e in yogurt_deltas_list
        if e.get("hc_term_fired", False)
    ]
    crit10c_pass = len(yogurt_hc_fired) == 0
    log.info("C10c yogurt scope isolation (CRITICAL): %d yogurts, EV-090 fired on: %d (pass=%s)",
             len(yogurt_deltas_list), len(yogurt_hc_fired), crit10c_pass)
    if not crit10c_pass:
        log.error("CRITICAL FAIL: yogurt products received delta from EV-090 hard_cheese SR branch — scope guard failure")

    # Hard cheese yellow-subpool movers + SR-firing stats
    n_hc_movers = 0
    n_hc_grade_chg = 0
    hc_grade_chg = []
    fired_hc = 0
    absorbed_hc = 0
    for e in hc_yellow_deltas:
        bc = e["barcode"]
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        d = e["clean_delta"]
        term = e.get("hc_term_fired", False)
        if term:
            fired_hc += 1
        if abs(d) > 0.0001:
            n_hc_movers += 1
        if on_g and off_g and on_g != off_g:
            n_hc_grade_chg += 1
            hc_grade_chg.append({
                "barcode": bc,
                "from": off_g, "to": on_g,
                "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": d,
                "bsip_cheese_subpool": e["bsip_cheese_subpool"],
                "sat_fat_g": get_satfat_g(bsip1_by_bc.get(bc)),
            })
        if term and abs(d) <= 0.0001:
            absorbed_hc += 1
    absorption = round(absorbed_hc / fired_hc, 4) if fired_hc > 0 else 0.0
    log.info("HC YELLOW: movers=%d grade_chg=%d term_fired=%d absorbed=%d absorption=%.4f",
             n_hc_movers, n_hc_grade_chg, fired_hc, absorbed_hc, absorption)

    # C1: directional distribution (asymmetric: above-median penalty -> mean_delta<=0; below-median relief -> mean_delta>=0)
    above_median_deltas = []
    below_median_deltas = []
    for e in hc_yellow_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        if sfg is None:
            continue
        if sfg > FATSAT_SHELF_REL_HARDCHEESE_MEDIAN:
            above_median_deltas.append(e["clean_delta"])
        elif sfg < FATSAT_SHELF_REL_HARDCHEESE_MEDIAN:
            below_median_deltas.append(e["clean_delta"])
    mean_above = round(sum(above_median_deltas) / len(above_median_deltas), 4) if above_median_deltas else 0.0
    mean_below = round(sum(below_median_deltas) / len(below_median_deltas), 4) if below_median_deltas else 0.0
    crit1_pass = (mean_above <= 0) and (mean_below >= 0)
    log.info("C1 directional: above_median n=%d mean_delta=%.4f (<=0? %s); below_median n=%d mean_delta=%.4f (>=0? %s)",
             len(above_median_deltas), mean_above, mean_above <= 0,
             len(below_median_deltas), mean_below, mean_below >= 0)

    # C2: grade distribution and magnitude
    # (A) 0 HARD_CHEESE_YELLOW_SUBPOOLS products with sat_fat>=19.0g at grade B (score>=70) flag-on
    # (B) >=1 HARD_CHEESE_YELLOW_SUBPOOLS product with sat_fat<=10g at grade C or better (score>=52)
    # (C) mean |clean_delta| >= 0.5 among SR-firing HARD_CHEESE_YELLOW_SUBPOOLS products
    high_satfat_b_count = 0   # sat_fat>=19g at B
    low_satfat_c_plus_count = 0   # sat_fat<=10g at score>=52 (C or better)
    all_abs_d = []
    for e in hc_yellow_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        on_s = results_on.get(bc, {}).get("score")
        on_g = results_on.get(bc, {}).get("grade")
        d = e["clean_delta"]
        if abs(d) > 0.0001 or e.get("hc_term_fired", False):
            all_abs_d.append(abs(d))
        if sfg is not None and sfg >= 19.0:
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
    log.info("C2: A(0 highsat>=19g@B)=%s(%d) B(>=1 lowsat<=10g@C+)=%s(%d) C(mean|d|=%.4f>=0.5)=%s",
             crit2a, high_satfat_b_count, crit2b, low_satfat_c_plus_count, mean_abs_d, crit2c)

    # C3: gap-narrowing for BOTH named pairs
    # INV-1: |score(7290000062426/yellow_light/5.5g) - score(7290000062433/yellow/17.5g)| at flag-on < flag-off
    # INV-2: |score(7290000062426/yellow_light/5.5g) - score(8866972/yellow/19.5g)| at flag-on < flag-off
    def _pair_scores(bc_a, bc_b):
        on_a  = results_on.get(bc_a, {}).get("score")
        off_a = results_off.get(bc_a, {}).get("score")
        on_b  = results_on.get(bc_b, {}).get("score")
        off_b = results_off.get(bc_b, {}).get("score")
        gap_on  = round(abs(on_a  - on_b),  2) if (on_a  is not None and on_b  is not None) else None
        gap_off = round(abs(off_a - off_b), 2) if (off_a is not None and off_b is not None) else None
        return on_a, off_a, on_b, off_b, gap_on, gap_off

    inv1_on_a, inv1_off_a, inv1_on_b, inv1_off_b, inv1_gap_on, inv1_gap_off = _pair_scores(INV1_A_BC, INV1_B_BC)
    inv2_on_a, inv2_off_a, inv2_on_b, inv2_off_b, inv2_gap_on, inv2_gap_off = _pair_scores(INV2_A_BC, INV2_B_BC)

    inv1_narrows = (inv1_gap_on is not None and inv1_gap_off is not None and inv1_gap_on < inv1_gap_off)
    inv2_narrows = (inv2_gap_on is not None and inv2_gap_off is not None and inv2_gap_on < inv2_gap_off)
    crit3_pass = inv1_narrows and inv2_narrows
    log.info("C3 INV-1: %s(5.5g) on=%.2f off=%.2f | %s(17.5g) on=%.2f off=%.2f | gap_on=%.2f gap_off=%.2f narrows=%s",
             INV1_A_BC, inv1_on_a or 0, inv1_off_a or 0, INV1_B_BC, inv1_on_b or 0, inv1_off_b or 0,
             inv1_gap_on or 0, inv1_gap_off or 0, inv1_narrows)
    log.info("C3 INV-2: %s(5.5g) on=%.2f off=%.2f | %s(19.5g) on=%.2f off=%.2f | gap_on=%.2f gap_off=%.2f narrows=%s",
             INV2_A_BC, inv2_on_a or 0, inv2_off_a or 0, INV2_B_BC, inv2_on_b or 0, inv2_off_b or 0,
             inv2_gap_on or 0, inv2_gap_off or 0, inv2_narrows)

    # C4: min_movers
    crit4_pass = n_hc_movers >= 5
    log.info("C4 min_movers: %d (need >=5, pass=%s)", n_hc_movers, crit4_pass)

    # C5: min_grade_changes
    crit5_pass = n_hc_grade_chg >= 1
    log.info("C5 min_grade_changes: %d (need >=1, pass=%s)", n_hc_grade_chg, crit5_pass)

    # C6: max_absorption
    crit6_pass = (fired_hc == 0) or (absorption <= 0.40)
    log.info("C6 max_absorption: %d/%d=%.4f (need <=0.40, pass=%s)", absorbed_hc, fired_hc, absorption, crit6_pass)

    # C7: anti-immunity (0 yellow-subpool sat_fat>=19.0g at grade B flag-on)
    crit7_pass = high_satfat_b_count == 0
    log.info("C7 anti_immunity: sat_fat>=19g @B flag-on: %d (need=0, pass=%s)", high_satfat_b_count, crit7_pass)

    # C8: floor_compliance (all yellow-subpool sat_fat>=19.0g: flag-on score <=62)
    floor_viol_hc = 0
    floor_checked_hc = 0
    for e in hc_yellow_deltas:
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        if sfg is not None and sfg >= FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G:
            floor_checked_hc += 1
            on_s = results_on.get(bc, {}).get("score")
            if on_s is not None and on_s > FATSAT_SHELF_REL_HARDCHEESE_FLOOR:
                floor_viol_hc += 1
    crit8_pass = floor_viol_hc == 0
    log.info("C8 floor: checked=%d (sat_fat>=%.1fg) viol=%d (all <=%.0f? %s)",
             floor_checked_hc, FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G,
             floor_viol_hc, FATSAT_SHELF_REL_HARDCHEESE_FLOOR, crit8_pass)

    # C9: no_scope_bleed (non-yellow-subpool dairy_protein with nonzero hc_term_fired delta)
    # Check non-HC dairy_protein products for any EV-090 SR term firing
    non_hc_hc_term_fired = [
        e for e in non_hc_dairy_deltas
        if e.get("hc_term_fired", False)
    ]
    crit9_pass = len(non_hc_hc_term_fired) == 0
    log.info("C9 scope bleed: non-HC dairy_protein with EV-090 term: %d (pass=%s)", len(non_hc_hc_term_fired), crit9_pass)

    # C11: flag-off drift vs run_hard_cheeses_001 baseline (DOCS-ONLY)
    BASELINE_HC_DIR = ROOT / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hard_cheeses_001" / "products"
    baseline_hc = {}
    if BASELINE_HC_DIR.exists():
        for sub in sorted(BASELINE_HC_DIR.iterdir()):
            if not sub.is_dir(): continue
            tf = sub / "bsip2_trace.json"
            if tf.exists():
                try:
                    bt = json.loads(tf.read_text(encoding="utf-8"))
                    bc = str(bt.get("barcode") or (bt.get("input_reference") or {}).get("barcode", ""))
                    if bc:
                        baseline_hc[bc] = bt.get("final_score_estimate")
                except Exception:
                    pass
    drift_hc = 0
    drift_list_hc = []
    for e in hc_yellow_deltas:
        bc = e["barcode"]
        off = e["flag_off"]
        base = baseline_hc.get(bc)
        if off is not None and base is not None and abs(off - base) > 5.0:
            drift_hc += 1
            drift_list_hc.append({
                "barcode": bc,
                "flag_off": off,
                "baseline_run_hard_cheeses_001": base,
                "diff": round(off - base, 4),
            })
    log.info("C11 flag_off_drift (hc_yellow vs run_hard_cheeses_001): %d mismatches >5pts (docs-only)", drift_hc)

    # -----------------------------------------------------------------------
    # Gate results
    # -----------------------------------------------------------------------
    gate_results = [
        {"criterion": "C1",   "name": "directional_distribution",
         "pass": crit1_pass,
         "evidence": f"above_median n={len(above_median_deltas)} mean_delta={mean_above} (<=0? {mean_above<=0}); below_median n={len(below_median_deltas)} mean_delta={mean_below} (>=0? {mean_below>=0})"},
        {"criterion": "C2",   "name": "grade_dist_and_magnitude",
         "pass": crit2_pass,
         "evidence": f"(A) high_sat>=19g@B={high_satfat_b_count}==0?{crit2a}; (B) low_sat<=10g@C+={low_satfat_c_plus_count}>=1?{crit2b}; (C) mean|d|={mean_abs_d}>=0.5?{crit2c}"},
        {"criterion": "C3",   "name": "gap_narrows_inversion",
         "pass": crit3_pass,
         "evidence": f"INV-1: gap_on={inv1_gap_on} < gap_off={inv1_gap_off}? {inv1_narrows}; INV-2: gap_on={inv2_gap_on} < gap_off={inv2_gap_off}? {inv2_narrows}"},
        {"criterion": "C4",   "name": "min_movers",
         "pass": crit4_pass,
         "evidence": f"n={n_hc_movers} (need >=5)"},
        {"criterion": "C5",   "name": "min_grade_changes",
         "pass": crit5_pass,
         "evidence": f"n={n_hc_grade_chg} (need >=1)"},
        {"criterion": "C6",   "name": "max_absorption",
         "pass": crit6_pass,
         "evidence": f"{absorbed_hc}/{fired_hc}={absorption} (need <=0.40)"},
        {"criterion": "C7",   "name": "anti_immunity",
         "pass": crit7_pass,
         "evidence": f"sat_fat>=19g @B flag-on: {high_satfat_b_count} (need=0)"},
        {"criterion": "C8",   "name": "floor_compliance",
         "pass": crit8_pass,
         "evidence": f"{floor_checked_hc} checked (sat_fat>={FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G}g), {floor_viol_hc} >{FATSAT_SHELF_REL_HARDCHEESE_FLOOR} (need=0)"},
        {"criterion": "C9",   "name": "no_scope_bleed",
         "pass": crit9_pass,
         "evidence": f"non-HC dairy_protein with EV-090 term: {len(non_hc_hc_term_fired)} (need=0)"},
        {"criterion": "C10",  "name": "frozen_byte_id_milk",
         "pass": crit10_pass,
         "evidence": f"CRITICAL: milk products={len(milk_deltas_list)} all delta=0: {crit10_pass}; nonzero={milk_nonzero}"},
        {"criterion": "C10b", "name": "cheese_spread_byte_id",
         "pass": crit10b_pass,
         "evidence": f"CRITICAL: cheese_spread products={len(cheese_spread_deltas_list)} EV-090 fired on: {len(cheese_spread_hc_fired)} (need=0)"},
        {"criterion": "C10c", "name": "yogurt_byte_id",
         "pass": crit10c_pass,
         "evidence": f"CRITICAL: yogurt products={len(yogurt_deltas_list)} EV-090 fired on: {len(yogurt_hc_fired)} (need=0)"},
        {"criterion": "C11",  "name": "flag_off_drift",
         "pass": "n/a-docs-only",
         "evidence": f"{drift_hc} mismatches >5pts vs run_hard_cheeses_001 (non-blocking)"},
    ]

    gate_pass = [g["criterion"] for g in gate_results if g["pass"] is True]
    gate_fail = [g["criterion"] for g in gate_results if g["pass"] is False]
    log.info("GATE SUMMARY: PASS=%s FAIL=%s", gate_pass, gate_fail)
    all_hard_pass = len(gate_fail) == 0
    log.info("ALL HARD GATES PASS: %s", all_hard_pass)

    # Per-product table (hard_cheese yellow-subpool)
    per_hc_table = []
    for e in sorted(hc_yellow_deltas,
                    key=lambda x: (get_satfat_g(bsip1_by_bc.get(x["barcode"])) is None,
                                   get_satfat_g(bsip1_by_bc.get(x["barcode"])) or 0)):
        bc = e["barcode"]
        sfg = get_satfat_g(bsip1_by_bc.get(bc))
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        name = (bsip1_by_bc.get(bc) or {}).get("canonical_name_he", "")
        per_hc_table.append({
            "barcode": bc,
            "name": name,
            "sat_fat_g": sfg,
            "bsip_cheese_subpool": e["bsip_cheese_subpool"],
            "flag_off_score": e["flag_off"],
            "flag_on_score": e["flag_on"],
            "clean_delta": e["clean_delta"],
            "grade_off": off_g,
            "grade_on": on_g,
            "hc_term_fired": e.get("hc_term_fired", False),
            "ev090_hard_cheese_floor_applied": e.get("ev090_hard_cheese_floor_applied", False),
            "baseline_run001": baseline_hc.get(bc),
        })

    # Per-product table for non-yellow HC products (subpool check)
    per_hc_other_table = []
    for e in hc_all_deltas:
        bc = e["barcode"]
        if e["bsip_cheese_subpool"] not in HARD_CHEESE_YELLOW_SUBPOOLS_SET:
            sfg = get_satfat_g(bsip1_by_bc.get(bc))
            name = (bsip1_by_bc.get(bc) or {}).get("canonical_name_he", "")
            per_hc_other_table.append({
                "barcode": bc,
                "name": name,
                "sat_fat_g": sfg,
                "bsip_cheese_subpool": e["bsip_cheese_subpool"],
                "flag_off_score": e["flag_off"],
                "flag_on_score": e["flag_on"],
                "clean_delta": e["clean_delta"],
            })

    milk_table = [
        {"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"], "clean_delta": e["clean_delta"]}
        for e in milk_deltas_list
    ]
    yogurt_table = [
        {"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"],
         "clean_delta": e["clean_delta"], "hc_term_fired": e.get("hc_term_fired", False),
         "subtype": results_on.get(e["barcode"], {}).get("subtype", "")}
        for e in yogurt_deltas_list
    ]
    cheese_spread_table = [
        {"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"],
         "clean_delta": e["clean_delta"], "hc_term_fired": e.get("hc_term_fired", False),
         "subtype": results_on.get(e["barcode"], {}).get("subtype", "")}
        for e in cheese_spread_deltas_list
    ]

    # File hashes
    eval_sha  = sha256_file(pathlib.Path(__file__).parent / "evaluation_scope.py")
    eng_sha   = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")
    const_sha = sha256_file(pathlib.Path(__file__).parent / "constants.py")

    # run_record
    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-8 hard_cheeses×sat_fat wire + pilot (P123)",
        "pilot_type": "MEASURED_NOT_PUBLISHED",
        "generated": ts,
        "engine": "proto_v0 + EV-090 hard_cheese sat_fat SR call site + EV-090 floor (bsip_cheese_subpool guard, FATSAT_SHELF_REL_SCOPE untouched)",
        "flag_config": {
            "BARI_SHELF_RELATIVE_V1": "dual (on/off patch)",
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK250_CONF": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "other_flags": "off (grad_sodium, sodium_shelf_relative, redlabel, sodium_cereal, task144)",
        },
        "dual_run_method": "module patch on score_engine.BARI_SHELF_RELATIVE_V1 (same process, hard_cheese-locked shelf_stats for fat_saturated_g)",
        "off_used": False,
        "corpus": {
            "hardcheese_bsip1": str(HARDCHEESE_BSIP1),
            "milk_bsip1": str(MILK_BSIP1),
            "yogurt_bsip1": str(YOGURT_BSIP1),
            "cheese_spread_bsip1": str(CHEESE_BSIP1),
            "n_hardcheese_loaded": len(products_hc),
            "n_milk_loaded": len(products_m),
            "n_yogurt_loaded": len(products_y),
            "n_cheese_spread_loaded": len(products_cs),
        },
        "shelf_stats_used": {
            "nutrient": "fat_saturated_g",
            "median": FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
            "scale": FATSAT_SHELF_REL_HARDCHEESE_SCALE,
            "n": 22,
            "source": "locked D7/P123 from yellow+yellow_light+hard_grating n=22 in run_hard_cheeses_001",
        },
        "scope_guard_used": "category == dairy_protein AND bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS {yellow, yellow_light, hard_grating}",
        "constants_used": {
            "FATSAT_SHELF_REL_HARDCHEESE_MEDIAN": FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
            "FATSAT_SHELF_REL_HARDCHEESE_SCALE": FATSAT_SHELF_REL_HARDCHEESE_SCALE,
            "FATSAT_SHELF_REL_HARDCHEESE_FLOOR": FATSAT_SHELF_REL_HARDCHEESE_FLOOR,
            "FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G": FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G,
            "HARD_CHEESE_YELLOW_SUBPOOLS": sorted(HARD_CHEESE_YELLOW_SUBPOOLS),
        },
        "milk_byte_id": {
            "pass": crit10_pass,
            "milk_products_checked": len(milk_deltas_list),
            "any_nonzero_delta": not crit10_pass,
            "milk_deltas": [{"barcode": m["barcode"], "delta": m["clean_delta"]} for m in milk_table],
        },
        "cheese_spread_byte_id": {
            "pass": crit10b_pass,
            "cheese_spread_products_checked": len(cheese_spread_deltas_list),
            "ev090_fired_on_cheese_spread": len(cheese_spread_hc_fired),
            "cheese_spread_hc_fired_list": cheese_spread_hc_fired,
        },
        "yogurt_byte_id": {
            "pass": crit10c_pass,
            "yogurt_products_checked": len(yogurt_deltas_list),
            "ev090_fired_on_yogurt": len(yogurt_hc_fired),
            "yogurt_hc_fired_list": yogurt_hc_fired,
        },
        "named_pairs": {
            "inv1_a": {"barcode": INV1_A_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV1_A_BC)),
                       "flag_off": inv1_off_a, "flag_on": inv1_on_a,
                       "note": "yellow_light/5.5g below-median -> relief expected"},
            "inv1_b": {"barcode": INV1_B_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV1_B_BC)),
                       "flag_off": inv1_off_b, "flag_on": inv1_on_b,
                       "note": "yellow/17.5g below-median -> slight relief expected"},
            "inv1_gap_off": inv1_gap_off, "inv1_gap_on": inv1_gap_on, "inv1_narrows": inv1_narrows,
            "inv2_a": {"barcode": INV2_A_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV2_A_BC)),
                       "flag_off": inv2_off_a, "flag_on": inv2_on_a,
                       "note": "yellow_light/5.5g below-median -> relief expected"},
            "inv2_b": {"barcode": INV2_B_BC, "sat_fat_g": get_satfat_g(bsip1_by_bc.get(INV2_B_BC)),
                       "flag_off": inv2_off_b, "flag_on": inv2_on_b,
                       "note": "yellow/19.5g above-median >= 19g floor -> floor+penalty expected"},
            "inv2_gap_off": inv2_gap_off, "inv2_gap_on": inv2_gap_on, "inv2_narrows": inv2_narrows,
        },
        "gate_criteria": gate_results,
        "gate_summary": {
            "all_hard_pass": all_hard_pass,
            "pass": gate_pass,
            "fail": gate_fail,
        },
        "aggregate_stats": {
            "hc_yellow_subpool_n": len(hc_yellow_deltas),
            "hc_yellow_movers": n_hc_movers,
            "hc_yellow_grade_changes": n_hc_grade_chg,
            "hc_yellow_sr_term_fired": fired_hc,
            "hc_yellow_absorbed": absorbed_hc,
            "hc_yellow_absorption_rate": absorption,
            "above_median_n": len(above_median_deltas),
            "below_median_n": len(below_median_deltas),
            "mean_delta_above_median": mean_above,
            "mean_delta_below_median": mean_below,
            "mean_abs_delta_sr_products": mean_abs_d,
        },
        "grade_changes": hc_grade_chg,
        "drift_vs_baseline": {
            "baseline_dir": str(BASELINE_HC_DIR),
            "n_loaded": len(baseline_hc),
            "n_exceeding_5pts": drift_hc,
            "mismatches": drift_list_hc,
        },
        "engine_artifacts": {
            "score_engine.py": eng_sha,
            "constants.py": const_sha,
            "evaluation_scope.py": eval_sha,
        },
        "score_errors": score_errors,
        "per_product_hardcheese_yellow": per_hc_table,
        "per_product_hardcheese_other_subpool": per_hc_other_table,
        "per_product_milk": milk_table,
        "per_product_yogurt": yogurt_table,
        "per_product_cheese_spread": cheese_spread_table,
    }

    out_path = OUTPUT_DIR / "run_record.json"
    out_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record written: %s", out_path)
    run_record_sha = sha256_file(out_path)
    log.info("run_record sha256: %s", run_record_sha)

    # Console summary
    print("\n" + "="*70)
    print(f"TASK-278 Phase-8 Hard Cheese SR Pilot - {RUN_ID}")
    print("="*70)
    print(f"Hard Cheese YELLOW corpus: {len(hc_yellow_deltas)} products")
    print(f"  Movers: {n_hc_movers}  Grade changes: {n_hc_grade_chg}  SR term fired: {fired_hc}")
    print(f"  Above-median mean delta: {mean_above}  Below-median mean delta: {mean_below}")
    print(f"  Mean |delta| SR-firing: {mean_abs_d}")
    print(f"Milk C10: {len(milk_deltas_list)} products, nonzero_delta={milk_nonzero} -> PASS={crit10_pass}")
    print(f"Cheese_spread C10b: {len(cheese_spread_deltas_list)} products, EV-090 fired: {len(cheese_spread_hc_fired)} -> PASS={crit10b_pass}")
    print(f"Yogurt C10c: {len(yogurt_deltas_list)} products, EV-090 fired: {len(yogurt_hc_fired)} -> PASS={crit10c_pass}")
    print("\nPer-product table (hard_cheese YELLOW, sorted by sat_fat_g):")
    print(f"  {'BC':<15} {'Name':<35} {'sat_fat':>7} {'off':>6} {'on':>6} {'delta':>7} {'G_off':>5} {'G_on':>5} {'subpool':<14} {'floor'}")
    for r in per_hc_table:
        print(f"  {r['barcode']:<15} {(r['name'] or '')[:33]:<35} {str(r['sat_fat_g'] or ''):>7} "
              f"{str(r['flag_off_score'] or ''):>6} {str(r['flag_on_score'] or ''):>6} "
              f"{str(r['clean_delta']):>7} {str(r['grade_off'] or ''):>5} {str(r['grade_on'] or ''):>5} "
              f"{str(r['bsip_cheese_subpool'] or ''):>14} {r['ev090_hard_cheese_floor_applied']}")
    print("\nGate summary:")
    for g in gate_results:
        status = "PASS" if g["pass"] is True else ("DOCS" if g["pass"] == "n/a-docs-only" else "FAIL")
        print(f"  {status} {g['criterion']:5s} {g['name']}: {g['evidence']}")
    print(f"\nAll hard gates PASS: {all_hard_pass}")
    print(f"Run record: {out_path}")
    print("="*70 + "\n")

    return run_record


if __name__ == "__main__":
    main()
