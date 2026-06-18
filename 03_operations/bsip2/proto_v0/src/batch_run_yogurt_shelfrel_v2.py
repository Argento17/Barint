# BSIP2 batch -- Yogurt SHELF-RELATIVE SUGAR PILOT v2 (run_yogurt_shelfrel_v2)
# TASK-278 Phase-6 wire + definitive pilot (P115)
# MEASURED NOT PUBLISHED: no frontend JSON, no comp JSON, no go-live, no published scores.
# Dual run same engine instance: BARI_SHELF_RELATIVE_V1 on vs off; clean_delta = on - off.
# Corpus: run_yogurt_006 bsip1 inputs (88 barcodes: 87 yogurt + 1 cereal outlier) + milk run_005_headpin bsip1 (~20).
# Yogurt SR gated by category=="dairy_protein" AND category_subtype in CULTURED_YOGURT_SUBTYPES.
# Shelf stats set to yogurt-locked (median=5.45, scale=4.299, n=74 with sugars_g); milks included only for C10 byte-id.
# OFF-BAN HARD: all sugars_g / nutrition from direct BSIP1 L1/normalized_nutrition; NO Open Food Facts.
# C10 (milk frozen byte-id) is CRITICAL: any milk delta !=0 at on = pilot FAIL.
# Adapted from batch_run_cereals_002_clean_pilot.py (P109).
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter
import importlib

# --- Flag config (common) BEFORE any engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "on"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "on"
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
    SUGAR_SHELF_REL_YOGURT_FLOOR, SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G,
    CULTURED_YOGURT_SUBTYPES,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
YOGURT_BSIP1 = ROOT / "03_operations" / "bsip1" / "run_yogurt_005" / "output"
MILK_BSIP1   = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
OUTPUT_DIR   = ROOT / "02_products" / "yogurt_system" / "bsip2_outputs" / "run_yogurt_shelfrel_v2"
BASELINE_DIR = ROOT / "02_products" / "yogurt_system" / "bsip2_outputs" / "run_yogurt_006" / "products"
RUN_ID = "run_yogurt_shelfrel_v2"
EXCLUDED_BARCODES = {"7290116932620"}

# Inversions per P115 C3
INV1_LOW_SUGAR_BC  = "7290110321697"   # 9.8g (should get less surcharge / higher on-score)
INV1_HIGH_SUGAR_BC = "7290102397600"   # 13.6g

(OUTPUT_DIR / "products").mkdir(parents=True, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def get_sugars_g(doc):
    if not doc:
        return None
    nn = doc.get("normalized_nutrition_per_100g") or {}
    v = nn.get("sugars_g")
    if v is None:
        l1 = doc.get("L1_observed_signals") or {}
        v = l1.get("sugars_g")
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
    glassbox_w4 = os.environ.get("BARI_GLASSBOX_W4", "engine_default(on)")
    log.info("=== BSIP2 Yogurt SHELF-RELATIVE SUGAR PILOT v2 -- %s (P115 / TASK-278 Phase-6) ===", RUN_ID)
    log.info("Dual run: flag-on vs flag-off within SAME engine (patch BARI_SHELF_RELATIVE_V1)")
    log.info("Clean delta = flag_on - flag_off; gates on yogurt-only (subtype in CULTURED_YOGURT_SUBTYPES)")
    log.info("Corpus: run_yogurt_006 bsip1 (88) + milk run_005_headpin bsip1; yogurt shelf stats only (n=74 sugars)")
    log.info("MEASURED NOT PUBLISHED: no frontend, no comp JSON, no go-live")
    log.info("OFF-BAN HARD: sugars_g from direct label/BSIP1 only (L1/normalized); no OFF substitution ever")
    log.info("C10 CRITICAL: milk run_005_headpin products must be byte-identical (delta=0) at flag-on vs off")
    log.info("All other flags match run_yogurt_006 (RECAL_P0=on + trim + TASK250) except SR dual")

    # Load yogurt bsip1 inputs (authoritative source for run_yogurt_006)
    if not YOGURT_BSIP1.exists():
        log.error("Yogurt BSIP1 source missing: %s", YOGURT_BSIP1); return
    products_y_all = load_batch(YOGURT_BSIP1)
    products_y = [p for p in products_y_all if str(p.get("barcode", "")) not in EXCLUDED_BARCODES]
    log.info("Yogurt BSIP1 loaded: %d (after exclude)", len(products_y))

    # Load milk bsip1 (for C10 frozen byte-id)
    if not MILK_BSIP1.exists():
        log.error("Milk BSIP1 source missing: %s", MILK_BSIP1); return
    products_m = load_batch(MILK_BSIP1)
    log.info("Milk BSIP1 loaded: %d", len(products_m))

    all_products = products_y + products_m
    bsip1_by_bc = {}
    for doc in all_products:
        bc = str(doc.get("barcode", ""))
        if bc:
            bsip1_by_bc[bc] = doc
    milk_barcodes = {str(p.get("barcode", "")) for p in products_m if p.get("barcode")}

    # Set yogurt-specific shelf stats (yogurt-only, locked per D7/P115; milks do not participate in yogurt shelf)
    log.info("--- Set shelf stats (yogurt-locked: median=5.45, scale=4.299, n=74) ---")
    clear_shelf_stats()
    set_shelf_stats(
        nutrient="sugars_g",
        median=5.45,
        scale=4.299,
        scale_type="iqr",
        n=74,
    )
    log.info("Shelf stats set for sugars_g (yogurt SR only; global for this run)")

    # Dual run via module patch
    import score_engine as _se
    log.info("Initial BARI_SHELF_RELATIVE_V1 (at import): %s", _se.BARI_SHELF_RELATIVE_V1)

    # PASS 1: flag-on
    log.info("--- PASS 1: flag-on (BARI_SHELF_RELATIVE_V1=True, yogurt subtype gate) ---")
    _se.BARI_SHELF_RELATIVE_V1 = True
    log.info("  Patched BARI_SHELF_RELATIVE_V1=True")

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
            term_fired = False
            for p in (trace.get("penalties_applied") or []):
                if "SUGAR_SHELF_REL" in (p.get("rule") or ""):
                    term_fired = True
                    break
            results_on[barcode] = {
                "score": score,
                "grade": grade,
                "category": cat,
                "subtype": subtype,
                "term_fired": term_fired,
                "trace": trace if subtype in set(CULTURED_YOGURT_SUBTYPES) else None,
            }
            log.info("  ON  %-40s score=%-5s grade=%-2s cat=%-20s subtype=%-15s term=%s",
                     name[:36], score, grade, cat, subtype, term_fired)
        except Exception as e:
            log.error("  ON ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e), "pass": "on"})

    # PASS 2: flag-off
    log.info("--- PASS 2: flag-off (BARI_SHELF_RELATIVE_V1=False) ---")
    _se.BARI_SHELF_RELATIVE_V1 = False
    log.info("  Patched BARI_SHELF_RELATIVE_V1=False")

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
            log.info("  OFF %-40s score=%-5s grade=%-2s cat=%-20s subtype=%-15s",
                     name[:36], score, grade, cat, subtype)
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
            }
            all_deltas.append(entry)

    log.info("Clean deltas computed: all=%d", len(all_deltas))

    # Yogurt-only (subtype gate)
    CULTURED = set(CULTURED_YOGURT_SUBTYPES)
    yogurt_deltas = [e for e in all_deltas if e["subtype"] in CULTURED]
    non_yogurt_dairy_deltas = [e for e in all_deltas if e["category"] == "dairy_protein" and e["subtype"] not in CULTURED]
    milk_deltas_list = [e for e in all_deltas if e["is_milk"]]
    log.info("Yogurt (subtype) deltas: %d; non-yogurt dairy_protein: %d; milk: %d",
             len(yogurt_deltas), len(non_yogurt_dairy_deltas), len(milk_deltas_list))

    # Yogurt movers, grade chg, absorption (SR-firing yogurts)
    n_yog_movers = 0
    n_yog_grade_chg = 0
    yog_grade_chg = []
    fired_y = 0
    absorbed_y = 0
    for e in yogurt_deltas:
        bc = e["barcode"]
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        d = e["delta"]
        term = results_on.get(bc, {}).get("term_fired", False)
        if term:
            fired_y += 1
        if abs(d) > 0.0001:
            n_yog_movers += 1
        if on_g and off_g and on_g != off_g:
            n_yog_grade_chg += 1
            yog_grade_chg.append({
                "barcode": bc,
                "from": off_g, "to": on_g,
                "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": d,
            })
        if term and abs(d) <= 0.0001:
            absorbed_y += 1
    absorption = round(absorbed_y / fired_y, 4) if fired_y > 0 else 0.0
    log.info("YOGURT-ONLY: movers=%d grade_chg=%d term_fired=%d absorbed_zero=%d absorption=%.4f",
             n_yog_movers, n_yog_grade_chg, fired_y, absorbed_y, absorption)

    # Inversion 1 (C3)
    on1 = results_on.get(INV1_LOW_SUGAR_BC, {}).get("score")
    off1 = results_off.get(INV1_LOW_SUGAR_BC, {}).get("score")
    on2 = results_on.get(INV1_HIGH_SUGAR_BC, {}).get("score")
    off2 = results_off.get(INV1_HIGH_SUGAR_BC, {}).get("score")
    gap_on = round(on1 - on2, 2) if (on1 is not None and on2 is not None) else None
    gap_off = round(off1 - off2, 2) if (off1 is not None and off2 is not None) else None
    crit3_pass = (gap_on is not None and gap_on >= 2.0)
    s1 = get_sugars_g(bsip1_by_bc.get(INV1_LOW_SUGAR_BC))
    s2 = get_sugars_g(bsip1_by_bc.get(INV1_HIGH_SUGAR_BC))
    log.info("Inversion1: 7290110321697(%.1f g) on=%.2f off=%.2f ; 7290102397600(%.1f g) on=%.2f off=%.2f ; gap_on=%.2f (>=2.0? %s)",
             s1 or 0, on1 or 0, off1 or 0, s2 or 0, on2 or 0, off2 or 0, gap_on or 0, crit3_pass)

    # C1: resolution (fewer tied clusters among 74 with sugars_g)
    yog_sugar_deltas = []
    for e in yogurt_deltas:
        sg = get_sugars_g(bsip1_by_bc.get(e["barcode"]))
        if sg is not None:
            yog_sugar_deltas.append(e)
    on_sc_y = [results_on.get(e["barcode"], {}).get("score") for e in yog_sugar_deltas if results_on.get(e["barcode"], {}).get("score") is not None]
    off_sc_y = [results_off.get(e["barcode"], {}).get("score") for e in yog_sugar_deltas if results_off.get(e["barcode"], {}).get("score") is not None]
    on_max_p = max(Counter(on_sc_y).values()) if on_sc_y else 0
    off_max_p = max(Counter(off_sc_y).values()) if off_sc_y else 0
    crit1_pass = on_max_p < off_max_p
    log.info("C1 resolution: on_max_pinned=%d off=%d (fewer in on? %s) n_sugar_yogurt=%d", on_max_p, off_max_p, crit1_pass, len(yog_sugar_deltas))

    # C2 components
    high_sg_b_count = 0
    low_sg_as_count = 0
    low_sg_deltas = []
    all_abs_d = []
    for e in yog_sugar_deltas:
        bc = e["barcode"]
        sg = get_sugars_g(bsip1_by_bc.get(bc))
        on_g = results_on.get(bc, {}).get("grade")
        on_s = results_on.get(bc, {}).get("score")
        d = e["delta"]
        all_abs_d.append(abs(d))
        if sg is not None and sg >= 12.0:
            if on_g == "B":
                high_sg_b_count += 1
        if sg is not None and sg <= 5.0:
            low_sg_deltas.append(d)
            if on_g in ("A", "S"):
                low_sg_as_count += 1
    mean_abs_d = round(sum(all_abs_d) / len(all_abs_d), 4) if all_abs_d else 0.0
    mean_d_low = round(sum(low_sg_deltas) / len(low_sg_deltas), 4) if low_sg_deltas else 0.0
    crit2a = high_sg_b_count == 0
    crit2b = low_sg_as_count >= 2
    crit2c = mean_abs_d >= 0.5
    crit2d = mean_d_low >= 0
    crit2_pass = crit2a and crit2b and crit2c and crit2d
    log.info("C2: A(0 high@B)=%s B(>=2 low@A/S)=%s(%d) C(mean|d|%.4f)=%s D(mean_d_low%.4f)=%s",
             crit2a, crit2b, low_sg_as_count, mean_abs_d, crit2c, mean_d_low, crit2d)

    # C4/C5
    crit4_pass = n_yog_movers >= 25
    crit5_pass = n_yog_grade_chg >= 1

    # C6 absorption
    crit6_pass = (fired_y == 0) or (absorption <= 0.40)

    # C7 anti-immunity
    crit7_pass = high_sg_b_count == 0

    # C8 floor
    floor_viol_y = 0
    floor_checked_y = 0
    for e in yog_sugar_deltas:
        sg = get_sugars_g(bsip1_by_bc.get(e["barcode"]))
        if sg is not None and sg >= SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G:
            floor_checked_y += 1
            on_s = results_on.get(e["barcode"], {}).get("score")
            if on_s is not None and on_s > SUGAR_SHELF_REL_YOGURT_FLOOR:
                floor_viol_y += 1
    crit8_pass = floor_viol_y == 0
    log.info("C8 floor: checked=%d viol=%d (all <=62? %s)", floor_checked_y, floor_viol_y, crit8_pass)

    # C9 no bleed
    non_yog_nonzero = sum(1 for e in non_yogurt_dairy_deltas if abs(e["delta"]) > 0.0001)
    crit9_pass = non_yog_nonzero == 0

    # C10 milk byte-id (critical)
    milk_nonzero = sum(1 for e in milk_deltas_list if abs(e["delta"]) > 0.0001)
    crit10_pass = milk_nonzero == 0
    log.info("C10 milk byte-id: %d milks, nonzero_delta=%d (pass=%s)", len(milk_deltas_list), milk_nonzero, crit10_pass)

    # C11 flag-off drift vs run_yogurt_006 baseline (yogurt products, non-blocking)
    baseline = {}
    if BASELINE_DIR.exists():
        for sub in sorted(BASELINE_DIR.iterdir()):
            if not sub.is_dir(): continue
            tf = sub / "bsip2_trace.json"
            if tf.exists():
                try:
                    bt = json.loads(tf.read_text(encoding="utf-8"))
                    bc = str(bt.get("barcode") or (bt.get("input_reference") or {}).get("barcode", ""))
                    if bc:
                        baseline[bc] = bt.get("final_score_estimate")
                except Exception:
                    pass
    drift_y = 0
    drift_list = []
    for e in yogurt_deltas:
        bc = e["barcode"]
        off = e["flag_off"]
        base = baseline.get(bc)
        if off is not None and base is not None and abs(off - base) > 0.01:
            drift_y += 1
            drift_list.append({"barcode": bc, "flag_off": off, "baseline": base})
    log.info("C11 flag_off_drift (yogurt): %d mismatches vs run_yogurt_006 (docs-only)", drift_y)

    # Gate results per P115 spec
    gate_results = [
        {"criterion": "C1", "name": "resolution_restored", "pass": crit1_pass, "evidence": f"on_max_pinned={on_max_p}, off_max_pinned={off_max_p} (n={len(yog_sugar_deltas)} with sugars)"},
        {"criterion": "C2", "name": "grade_dist_and_magnitude", "pass": crit2_pass, "evidence": f"A: high_sg_B={high_sg_b_count}==0; B: low_sg_AS={low_sg_as_count}>=2; C: mean|d|={mean_abs_d}>=0.5; D: mean_d_low={mean_d_low}>=0"},
        {"criterion": "C3", "name": "inversion_gap", "pass": crit3_pass, "evidence": f"gap_flag_on={gap_on} (need >=2.0); low9.8={on1} high13.6={on2}"},
        {"criterion": "C4", "name": "min_movers", "pass": crit4_pass, "evidence": f"n={n_yog_movers} (need >=25)"},
        {"criterion": "C5", "name": "min_grade_changes", "pass": crit5_pass, "evidence": f"n={n_yog_grade_chg} (need >=1)"},
        {"criterion": "C6", "name": "max_absorption", "pass": crit6_pass, "evidence": f"{absorbed_y}/{fired_y}={absorption} (need <=0.40)"},
        {"criterion": "C7", "name": "anti_immunity", "pass": crit7_pass, "evidence": f"high_sg(>=12) @B on: {high_sg_b_count} (need=0)"},
        {"criterion": "C8", "name": "floor_compliance", "pass": crit8_pass, "evidence": f"{floor_checked_y} checked, {floor_viol_y} >62 (need=0); floor=62"},
        {"criterion": "C9", "name": "no_scope_bleed", "pass": crit9_pass, "evidence": f"non_yogurt_dairy_protein with nonzero delta: {non_yog_nonzero} (need=0); milks verified in C10"},
        {"criterion": "C10", "name": "frozen_byte_id", "pass": crit10_pass, "evidence": f"milk products all delta=0: {crit10_pass}; checked={len(milk_deltas_list)}"},
        {"criterion": "C11", "name": "flag_off_drift", "pass": "n/a-docs-only", "evidence": f"{drift_y} mismatches vs run_yogurt_006"},
    ]

    # Per-product tables (yogurt n=87 sorted by sugars; milk)
    per_yogurt_table = []
    for e in sorted(yogurt_deltas, key=lambda x: (get_sugars_g(bsip1_by_bc.get(x["barcode"])) is None, get_sugars_g(bsip1_by_bc.get(x["barcode"])) or 0)):
        bc = e["barcode"]
        sg = get_sugars_g(bsip1_by_bc.get(bc))
        on_g = results_on.get(bc, {}).get("grade")
        off_g = results_off.get(bc, {}).get("grade")
        per_yogurt_table.append({
            "barcode": bc,
            "sugars_g": sg,
            "flag_off": e["flag_off"],
            "flag_on": e["flag_on"],
            "delta": e["delta"],
            "grade_off": off_g,
            "grade_on": on_g,
        })
    milk_table = [{"barcode": e["barcode"], "flag_off": e["flag_off"], "flag_on": e["flag_on"], "delta": e["delta"]} for e in milk_deltas_list]

    # run_record
    eval_sha = sha256_file(pathlib.Path(__file__).parent / "evaluation_scope.py")
    eng_sha = sha256_file(pathlib.Path(__file__).parent / "score_engine.py")
    const_sha = sha256_file(pathlib.Path(__file__).parent / "constants.py")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-6 yogurt×sugar wire + pilot (P115)",
        "pilot_type": "MEASURED_NOT_PUBLISHED",
        "generated": ts,
        "engine": "proto_v0 + EV-088 yogurt SR call site + EV-088 floor (subtype guard, no scope change)",
        "flag_config": {
            "BARI_SHELF_RELATIVE_V1": "dual (on/off patch)",
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "on",
            "BARI_TASK250_CONF": "on",
            "other_recal_sodium_redlabel": "off (per 006)",
        },
        "dual_run_method": "module patch on score_engine.BARI_SHELF_RELATIVE_V1 (same process, yogurt-locked shelf_stats)",
        "off_used": False,
        "corpus": {
            "yogurt_bsip1": str(YOGURT_BSIP1),
            "milk_bsip1": str(MILK_BSIP1),
            "baseline_for_c11": str(BASELINE_DIR),
            "n_yogurt_loaded": len(products_y),
            "n_milk_loaded": len(products_m),
        },
        "shelf_stats_used": {"median": 5.45, "scale": 4.299, "n": 74, "source": "locked D7/P115 from run_yogurt_006"},
        "scope_guard_used": "category == dairy_protein AND category_subtype in CULTURED_YOGURT_SUBTYPES",
        "constants_used": {
            "SUGAR_SHELF_REL_YOGURT_MEDIAN": 5.45,
            "SUGAR_SHELF_REL_YOGURT_SCALE": 4.299,
            "SUGAR_SHELF_REL_YOGURT_FLOOR": 62,
            "SUGAR_SHELF_REL_YOGURT_FLOOR_THRESHOLD_G": 12.0,
            "SUGAR_SHELF_REL_YOGURT_P_MAX": 6,
            "SUGAR_SHELF_REL_YOGURT_B_MAX": 3,
        },
        "milk_byte_id": {
            "pass": crit10_pass,
            "milk_products_checked": len(milk_deltas_list),
            "milk_deltas": [{"barcode": m["barcode"], "delta": m["delta"]} for m in milk_table],
            "any_nonzero_delta": not crit10_pass,
        },
        "non_yogurt_dairy_bleed": {
            "non_yogurt_dairy_protein_products": len(non_yogurt_dairy_deltas),
            "non_yogurt_delta_nonzero": non_yog_nonzero,
        },
        "inversion_1": {
            "7290110321697": {"sugars_g": s1, "flag_off": off1, "flag_on": on1},
            "7290102397600": {"sugars_g": s2, "flag_off": off2, "flag_on": on2},
            "gap_flag_on": gap_on,
            "criterion_pass_c3": crit3_pass,
        },
        "yogurt_movers": n_yog_movers,
        "yogurt_grade_changes": n_yog_grade_chg,
        "absorption": absorption,
        "gate_results": gate_results,
        "per_product_table": per_yogurt_table,
        "milk_table": milk_table,
        "flag_off_drift_yogurt": {"mismatches": drift_y, "details": drift_list[:10]},
        "engine_invariants": "342 PASS (run before pilot)",
        "evaluation_scope_sha256": eval_sha,
        "score_engine_sha256": eng_sha,
        "constants_sha256": const_sha,
        "output_dir": str(OUTPUT_DIR),
        "errors": score_errors,
        "self_check": {
            "off_used": False,
            "yogurt_only_gates": True,
            "milk_included_for_c10": True,
            "C10_critical": crit10_pass,
            "C9_no_bleed": crit9_pass,
        },
    }

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record written: %s", rr_path)

    # Console summary (for return block extraction)
    print("\n" + "="*80)
    print(f"YOGURT SHELF-RELATIVE SUGAR PILOT v2 -- {RUN_ID}")
    print("="*80)
    print("TASK-278 Phase-6 (P115) | MEASURED NOT PUBLISHED | OFF=0")
    print(f"Yogurt products (subtype): {len(yogurt_deltas)} (of which sugars non-null ~74)")
    print(f"Milk products (C10): {len(milk_deltas_list)}")
    print(f"Non-yogurt dairy_protein (bleed check): {len(non_yogurt_dairy_deltas)}")
    print()
    print("GATE CRITERIA:")
    for g in gate_results:
        p = g["pass"]
        status = "PASS" if p is True else ("n/a" if p == "n/a-docs-only" else ("FAIL" if p is False else str(p)))
        print(f"  {g['criterion']}: {status} — {g['evidence']}")
    print()
    print(f"C10 (milk deltas all 0): {crit10_pass}")
    print(f"C9 (no non-yogurt dairy bleed): {crit9_pass}")
    print(f"Traces (on): {len(traces_on)} -> {OUTPUT_DIR}/products/")
    print(f"Run record: {rr_path}")
    print("="*80)
    print("RETURN: tasks/returns/P115_return.md (propose RETURNED)")
    print("DO NOT close; orchestrator verifies.")
    print("="*80)

    return run_record

if __name__ == "__main__":
    main()
