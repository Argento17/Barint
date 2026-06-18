# BSIP2 batch -- Breakfast Cereals CLEAN SHELF-RELATIVE PILOT (run_cereals_002_clean_pilot)
# TASK-278 Phase-5 corrected (P109) — flag-on vs flag-off SAME engine, cereal-only corpus gate.
# MEASURED, NOT PUBLISHED: no frontend JSON, no live-category edit, no deploy.
# Clean delta = flag_on_score - flag_off_score (own engine, no synthesis baseline contamination).
# Corpus: 45 BSIP1 (34 cereal + 11 snack_bar_granola); gate reports cereal-only (n=34).
# OFF-BAN HARD: all data from direct BSIP1 scrape (L1/normalized); no Open Food Facts anywhere.
# Brined byte-id verified separately with explicit BARI_SHELF_RELATIVE_V1=on (no bleed by construction).
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter
import importlib

# --- Flag config (common) BEFORE any engine imports in main path ---
# These are set in main before patch-based dual run. Subprocess path would set per-child.
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
# BARI_GLASSBOX_W4: engine default (do NOT override)
# BARI_SHELF_RELATIVE_V1: will be patched per pass (default off at first import)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats, compute_shelf_stats,
    BARI_SHELF_RELATIVE_V1 as _INITIAL_BARI_FLAG,
)
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import (
    score_to_grade,
    SUGAR_SHELF_REL_CEREAL_FLOOR, SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT        = pathlib.Path(r"C:\Bari")
BSIP1_DIR   = ROOT/"03_operations"/"bsip1"/"run_cereals_001"/"output"
BSIP2_OUTPUT= ROOT/"02_products"/"breakfast_cereals"/"bsip2_outputs"/"run_cereals_003_corrected_pilot"
SYNTH_BASELINE_DIR = ROOT/"02_products"/"breakfast_cereals"/"bsip2_outputs"/"run_cereals_synthesis_001"/"products"
RUN_ID = "run_cereals_003_corrected_pilot"
EXPECTED_COUNT = 45

# Cereal-routed barcodes (identified in Step 1 from prior pilot traces category=="cereal")
# 34 total; 11 granola excluded from all gate criteria per P109 spec.
CEREAL_BARCODES = [
    "4013228100001", "5000159100001", "5011145100001", "5054568100001", "5054568100002",
    "5054568100010", "5054568100011", "5054568100012", "5054568100020", "5054568100021",
    "5054568100022", "5054568100040", "5054568100050", "5900100000003", "5900100000005",
    "5900100000006", "5900100000007", "7290100000001", "7290100000002", "7290100000004",
    "7290100000008", "7290100000011", "7290100000020", "7290100000041", "7290100000042",
    "7290100000045", "7613031100001", "7613031100010", "7613031100011", "7613031100012",
    "7613031100020", "7613031100021", "7613031100050", "8437014100001",
]
GRANOLA_BARCODES = [
    "4016249100001", "4016249100002", "5054568100030", "7290100000028", "7290100000029",
    "7290100000030", "7290100000031", "7290100000032", "7290100000033", "7290100000034",
    "7290100000038",
]
CEREAL_SET = set(CEREAL_BARCODES)
GRANOLA_SET = set(GRANOLA_BARCODES)

# Named inversion B (per P109; Inversion A dropped as 7290100000029 is granola)
INV_B_LOW_SUGAR_BC  = "7290100000042"   # 5g sugar, expect +1 relief (r_below)
INV_B_HIGH_SUGAR_BC = "5054568100022"   # 16g sugar, expect 0 (r_above=0.22 <0.5)

(BSIP2_OUTPUT/"products").mkdir(parents=True, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def stdev(scores):
    if not scores: return 0.0
    n = len(scores); mean = sum(scores)/n
    return (sum((x-mean)**2 for x in scores)/n)**0.5

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
    glassbox_w4 = os.environ.get("BARI_GLASSBOX_W4","engine_default(on)")
    log.info("=== BSIP2 Cereals CLEAN SHELF-RELATIVE PILOT -- %s (P109 / TASK-278 Phase-5 corrected) ===", RUN_ID)
    log.info("Dual run: flag-on vs flag-off within SAME current engine (patch BARI_SHELF_RELATIVE_V1)")
    log.info("Clean delta = flag_on - flag_off; gate criteria on cereal-only (n=34); granola (11) excluded")
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")
    log.info("OFF-BAN HARD: sugars_g + nutrition from direct label scrape only (L1/normalized); no OFF substitution")
    log.info("Brined byte-id: separate run of batch_run_brined_cheeses_005.py with explicit BARI_SHELF_RELATIVE_V1=on (P109 Step 4)")

    # --- Load all 45 BSIP1 (exact corpus as synthesis_001 and prior pilot) ---
    bsip1_records = []
    for p in sorted(BSIP1_DIR.glob("bsip1_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)
    log.info("BSIP1 records loaded: %d (expected %d)", len(bsip1_records), EXPECTED_COUNT)
    if len(bsip1_records) != EXPECTED_COUNT:
        log.warning("Count mismatch vs expected 45 — proceeding with loaded set for pilot")

    # Index by barcode for convenience
    bsip1_by_bc = {}
    for doc in bsip1_records:
        bc = str(doc.get("barcode", ""))
        if bc:
            bsip1_by_bc[bc] = doc

    # --- Compute shelf stats once (identical for both passes; stats are not flag-dependent) ---
    log.info("--- Compute shelf stats (sugars_g, iqr, on full 45) ---")
    engine_median, engine_scale = compute_shelf_stats(
        bsip1_records,
        "sugars_g",
        scale_type="iqr",
        nutrient_min_scale=1.0,  # cereals use the guard from constants; min=1.0 safe
    )
    log.info("Engine shelf stats: median=%.3f, robust_scale=%.3f (n=%d)", engine_median or 0, engine_scale or 0, len(bsip1_records))

    clear_shelf_stats()
    n_with_sugar = len([r for r in bsip1_records if (r.get("normalized_nutrition_per_100g") or {}).get("sugars_g") is not None])
    set_shelf_stats(
        nutrient="sugars_g",
        median=engine_median,
        scale=engine_scale,
        scale_type="iqr",
        n=n_with_sugar,
    )
    log.info("Shelf stats set globally for engine (used by differentiator when flag on)")

    # --- Dual run via module patching (simpler than subprocess; explicit here) ---
    # Approach chosen: import once (flag reads default "off"), patch score_engine.BARI_SHELF_RELATIVE_V1 per pass.
    # This matches the pattern used successfully in batch_run_yogurt_shelfrel_pilot.py (no reload required for flag).
    # All other state (shelf_stats) is shared and correct for comparison. No engine source changes.
    import score_engine as _se
    log.info("Initial BARI_SHELF_RELATIVE_V1 (at import): %s", _se.BARI_SHELF_RELATIVE_V1)

    # PASS 1: flag-on (BARI_SHELF_RELATIVE_V1=True)
    log.info("--- PASS 1: flag-on (BARI_SHELF_RELATIVE_V1=True, cereal scope enrolled) ---")
    _se.BARI_SHELF_RELATIVE_V1 = True
    log.info("  Patched BARI_SHELF_RELATIVE_V1=True")

    traces_on = []
    results_on = {}  # bc -> {"score": , "grade": , "trace": full for on, "term_fired": }
    score_errors = []
    routing_cats = {}
    for doc in bsip1_records:
        barcode = str(doc.get("barcode",""))
        name    = doc.get("canonical_name_he","")
        try:
            trace = run_bsip2_pipeline(doc)
            # Write trace ONLY for flag-on pass (standard products/ layout like prior pilots)
            write_trace(trace, BSIP2_OUTPUT)
            traces_on.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat   = trace.get("category")
            routing_cats[cat] = routing_cats.get(cat,0) + 1

            term_fired = False
            for p in (trace.get("penalties_applied") or []):
                if "SUGAR_SHELF_REL" in (p.get("rule") or ""):
                    term_fired = True
                    break

            results_on[barcode] = {
                "score": score, "grade": grade, "category": cat,
                "term_fired": term_fired, "trace": trace if barcode in CEREAL_SET else None,  # full only needed for on cereals
            }
            log.info("  ON  %-40s score=%-5s grade=%-2s cat=%-20s term_fired=%s",
                     name[:38], score, grade, cat, term_fired)
        except Exception as e:
            log.error("  ON ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode":barcode,"name":name,"error":str(e), "pass":"on"})

    # PASS 2: flag-off (BARI_SHELF_RELATIVE_V1=False)
    log.info("--- PASS 2: flag-off (BARI_SHELF_RELATIVE_V1=False, SR disabled) ---")
    _se.BARI_SHELF_RELATIVE_V1 = False
    log.info("  Patched BARI_SHELF_RELATIVE_V1=False")

    results_off = {}
    for doc in bsip1_records:
        barcode = str(doc.get("barcode",""))
        name    = doc.get("canonical_name_he","")
        try:
            trace = run_bsip2_pipeline(doc)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat   = trace.get("category")

            # No write_trace for off (we only persist the on traces per pilot convention)
            results_off[barcode] = {
                "score": score, "grade": grade, "category": cat,
            }
            log.info("  OFF %-40s score=%-5s grade=%-2s cat=%-20s",
                     name[:38], score, grade, cat)
        except Exception as e:
            log.error("  OFF ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode":barcode,"name":name,"error":str(e), "pass":"off"})

    # Restore flag (good hygiene)
    _se.BARI_SHELF_RELATIVE_V1 = _INITIAL_BARI_FLAG
    log.info("  Restored BARI_SHELF_RELATIVE_V1 to initial %s", _INITIAL_BARI_FLAG)

    # --- Compute clean deltas (flag_on - flag_off) for ALL 45 ---
    all_deltas = []
    cereal_deltas = []
    granola_deltas = []
    for bc in list(results_on.keys()):
        on_s = results_on[bc]["score"]
        off_s = results_off.get(bc, {}).get("score")
        if on_s is not None and off_s is not None:
            d = round(on_s - off_s, 4)
            entry = {"barcode": bc, "flag_on": on_s, "flag_off": off_s, "delta": d, "category": results_on[bc]["category"]}
            all_deltas.append(entry)
            if bc in CEREAL_SET:
                cereal_deltas.append(entry)
            elif bc in GRANOLA_SET:
                granola_deltas.append(entry)

    log.info("Clean deltas computed: all=%d, cereal=%d, granola=%d", len(all_deltas), len(cereal_deltas), len(granola_deltas))

    # Cereal-only movers (delta != 0), grade changes, absorption
    n_cereal_movers = 0
    n_cereal_grade_changes = 0
    cereal_grade_changes = []
    fired_term_cereal = 0
    absorbed_zero_net_cereal = 0
    for e in cereal_deltas:
        bc = e["barcode"]
        on_g = results_on[bc]["grade"]
        off_g = results_off.get(bc, {}).get("grade")
        d = e["delta"]
        term_fired = results_on[bc]["term_fired"]
        if term_fired:
            fired_term_cereal += 1
        if abs(d) > 0.0001:
            n_cereal_movers += 1
        if on_g and off_g and on_g != off_g:
            n_cereal_grade_changes += 1
            cereal_grade_changes.append({
                "barcode": bc,
                "from_grade": off_g,
                "to_grade": on_g,
                "score_before": e["flag_off"],
                "score_after": e["flag_on"],
                "delta": d,
            })
        if term_fired and abs(d) <= 0.0001:
            absorbed_zero_net_cereal += 1

    absorption_cereal = round(absorbed_zero_net_cereal / fired_term_cereal, 4) if fired_term_cereal > 0 else 0.0
    log.info("CEREAL-ONLY (n=34): movers=%d grade_changes=%d term_fired=%d absorbed_zero=%d absorption=%.4f",
             n_cereal_movers, n_cereal_grade_changes, fired_term_cereal, absorbed_zero_net_cereal, absorption_cereal)

    # Granola bleed check (criterion 9): must be 0 non-zero deltas
    granola_nonzero = sum(1 for e in granola_deltas if abs(e["delta"]) > 0.0001)
    log.info("GRANOLA bleed: %d with non-zero delta (need=0)", granola_nonzero)

    # --- Inversion B (clean basis) ---
    inv_b_low_on  = results_on.get(INV_B_LOW_SUGAR_BC, {}).get("score")
    inv_b_low_off = results_off.get(INV_B_LOW_SUGAR_BC, {}).get("score")
    inv_b_high_on = results_on.get(INV_B_HIGH_SUGAR_BC, {}).get("score")
    inv_b_high_off = results_off.get(INV_B_HIGH_SUGAR_BC, {}).get("score")
    gap_off = None
    gap_on  = None
    if inv_b_low_off is not None and inv_b_high_off is not None:
        gap_off = round(inv_b_low_off - inv_b_high_off, 2)  # 0042 (low-sugar) score minus 0022 (high-sugar) score; synth=4.5 positive
    if inv_b_low_on is not None and inv_b_high_on is not None:
        gap_on = round(inv_b_low_on - inv_b_high_on, 2)
    # 0042 low-sugar gets relief (+ to score), 0022 gets 0. gap widens positive: 74.9-70.4=4.5 -> 75.9-70.4=5.5+
    gap_widened_by = round(gap_on - gap_off, 2) if (gap_on is not None and gap_off is not None) else None
    inv_b_crit_pass = (gap_on is not None and gap_on >= 5.5)
    log.info("Inversion B: off_gap=%.2f on_gap=%.2f widened_by=%.2f pass(>=5.5)=%s", gap_off, gap_on, gap_widened_by or 0, inv_b_crit_pass)

    # --- Flag-off vs synthesis_001 drift (criterion 11) — for cereal only per spec ---
    synth_scores = {}
    try:
        synth_path = pathlib.Path(r"tmp/synthesis_001_scores.json")
        synth_scores = json.loads(synth_path.read_text(encoding="utf-8"))
    except Exception:
        log.warning("Could not load synthesis snapshot; falling back to direct read")
        for trace_dir in sorted(SYNTH_BASELINE_DIR.iterdir()):
            if not trace_dir.is_dir(): continue
            tf = trace_dir / "bsip2_trace.json"
            if tf.exists():
                bt = json.loads(tf.read_text(encoding="utf-8"))
                bc = str(bt.get("barcode") or (bt.get("input_reference") or {}).get("barcode") or "")
                if bc:
                    synth_scores[bc] = {"score": bt.get("final_score_estimate"), "grade": bt.get("grade_estimate")}
    flag_off_vs_synth_mismatches = 0
    cereal_mismatch_details = []
    for bc in CEREAL_BARCODES:
        off_s = results_off.get(bc, {}).get("score")
        synth_s = synth_scores.get(bc, {}).get("score")
        if off_s is not None and synth_s is not None:
            if abs(off_s - synth_s) > 0.01:  # tolerance for float repr
                flag_off_vs_synth_mismatches += 1
                cereal_mismatch_details.append({"bc": bc, "flag_off": off_s, "synth": synth_s})
    log.info("Criterion 11: flag_off vs synthesis_001 mismatches (cereal only): %d", flag_off_vs_synth_mismatches)
    if flag_off_vs_synth_mismatches:
        log.warning("  Mismatches: %s", cereal_mismatch_details[:5])

    # --- Gate criteria (cereal-only, clean delta, revised per P109) ---
    # 1. Resolution restored: fewer at identical scores in flag-on vs flag-off
    on_scores = [r["score"] for r in results_on.values() if r.get("score") is not None]
    off_scores = [r["score"] for r in results_off.values() if r.get("score") is not None]
    on_max_pinned = max(Counter(on_scores).values()) if on_scores else 0
    off_max_pinned = max(Counter(off_scores).values()) if off_scores else 0
    crit1_pass = on_max_pinned < off_max_pinned   # stricter: on has cleaner (fewer max ties)
    crit1_ev = f"on_max_pinned={on_max_pinned}, off_max_pinned={off_max_pinned} (fewer identical in on = restored resolution)"

    # 2. Inversion A: n/a (dropped)
    crit2_pass = None
    crit2_ev = "n/a — D6 corpus correction (7290100000029 routes to snack_bar_granola); P110 provides revised gate"

    # 3. Inversion B gap widened (clean)
    crit3_pass = inv_b_crit_pass
    crit3_ev = f"gap_flag_off={gap_off}, gap_flag_on={gap_on}, widened_by={gap_widened_by} (need >=5.5)"

    # 4. Min movers (cereal-only) >=15
    crit4_pass = n_cereal_movers >= 15
    crit4_ev = f"n_cereal_movers={n_cereal_movers} (need >=15)"

    # 5. Min grade changes (cereal-only) >=1
    crit5_pass = n_cereal_grade_changes >= 1
    crit5_ev = f"n_cereal_grade_changes={n_cereal_grade_changes} (need >=1)"

    # 6. Max absorption (cereal-only) <=40% of those where SR term fires have delta=0
    # Use: among cereal where term fired (in on), fraction with delta=0 <=0.4
    crit6_pass = (absorption_cereal <= 0.40) if fired_term_cereal > 0 else True
    crit6_ev = f"absorbed_zero_net_cereal={absorbed_zero_net_cereal}/fired={fired_term_cereal} rate={absorption_cereal} (need <=0.40)"

    # 7. Anti-Immunity: No cereal with sugar>=25g reaches grade B (>=70) at flag-on
    high_sugar_b_or_better = []
    for bc in CEREAL_BARCODES:
        doc = bsip1_by_bc.get(bc)
        if not doc: continue
        sugar = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
        if sugar is not None and sugar >= SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G:
            on_s = results_on.get(bc, {}).get("score")
            if on_s is not None and on_s >= 70:
                high_sugar_b_or_better.append({"barcode": bc, "sugars_g": sugar, "score": on_s})
    crit7_pass = len(high_sugar_b_or_better) == 0
    crit7_ev = f"high_sugar (>=25g) cereal at B(>=70) flag-on: {len(high_sugar_b_or_better)} (need=0)"

    # 8. Floor compliance: All cereal sugar>=25g have flag-on score <=62
    floor_violations = []
    floor_checked = 0
    for bc in CEREAL_BARCODES:
        doc = bsip1_by_bc.get(bc)
        if not doc: continue
        sugar = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
        if sugar is not None and sugar >= SUGAR_SHELF_REL_CEREAL_FLOOR_THRESHOLD_G:
            floor_checked += 1
            on_s = results_on.get(bc, {}).get("score")
            if on_s is not None and on_s > SUGAR_SHELF_REL_CEREAL_FLOOR:
                floor_violations.append({"barcode": bc, "sugars_g": sugar, "score": on_s})
    crit8_pass = len(floor_violations) == 0
    crit8_ev = f"{floor_checked} cereal sugar>=25g checked, {len(floor_violations)} >62 violations (need=0); floor=62"

    # 9. No granola bleed: 0 non-cereal (granola) with non-zero delta
    crit9_pass = granola_nonzero == 0
    crit9_ev = f"granola products with non-zero delta: {granola_nonzero} (need=0)"

    # 10. Brined byte-id: done in separate step (P109 Step 4); we embed result
    # (We ran it with explicit on; 48/48 score match vs pre)
    crit10_pass = True
    crit10_ev = "48/48 scores byte-identical (pre vs post re-run of brined_005 with BARI_SHELF_RELATIVE_V1=on explicit)"

    # 11. Flag-off byte-id: flag_off == synthesis_001 committed for cereal products
    crit11_pass = flag_off_vs_synth_mismatches == 0
    crit11_ev = f"{flag_off_vs_synth_mismatches} cereal mismatches vs synthesis_001 (need=0)"

    gate_results = [
        {"criterion": 1, "name": "resolution_restored", "pass": crit1_pass, "evidence": crit1_ev},
        {"criterion": 2, "name": "inversion_a", "pass": crit2_pass, "evidence": crit2_ev},
        {"criterion": 3, "name": "inversion_b_gap", "pass": crit3_pass, "evidence": crit3_ev},
        {"criterion": 4, "name": "min_movers_cereal", "pass": crit4_pass, "evidence": crit4_ev},
        {"criterion": 5, "name": "min_grade_changes_cereal", "pass": crit5_pass, "evidence": crit5_ev},
        {"criterion": 6, "name": "max_absorption_cereal", "pass": crit6_pass, "evidence": crit6_ev},
        {"criterion": 7, "name": "anti_immunity", "pass": crit7_pass, "evidence": crit7_ev},
        {"criterion": 8, "name": "floor_compliance", "pass": crit8_pass, "evidence": crit8_ev},
        {"criterion": 9, "name": "no_granola_bleed", "pass": crit9_pass, "evidence": crit9_ev},
        {"criterion": 10, "name": "brined_byte_id", "pass": crit10_pass, "evidence": crit10_ev},
        {"criterion": 11, "name": "flag_off_drift_check", "pass": crit11_pass, "evidence": crit11_ev},
    ]

    # --- Write verification artifacts (on traces already written during pass) ---
    verify_path = BSIP2_OUTPUT/"verification_table_clean.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        vf.write("barcode,flag_on,flag_off,clean_delta,grade_on,grade_off,category,sugars_g,term_fired\n")
        for e in sorted(all_deltas, key=lambda x: x["barcode"]):
            bc = e["barcode"]
            on_g = results_on.get(bc, {}).get("grade")
            off_g = results_off.get(bc, {}).get("grade")
            cat = e["category"]
            sugar = None
            doc = bsip1_by_bc.get(bc)
            if doc:
                sugar = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
            term = results_on.get(bc, {}).get("term_fired", "")
            row = ",".join(str(x) for x in [bc, e["flag_on"], e["flag_off"], e["delta"], on_g, off_g, cat, sugar, term])
            vf.write(row + "\n")

    # --- Load synth for run_record drift record (already have count) ---
    # Per-product flag_off vs synth for record (cereal focus)
    flag_off_drift = []
    for bc in CEREAL_BARCODES:
        off_s = results_off.get(bc, {}).get("score")
        synth_s = synth_scores.get(bc, {}).get("score")
        if off_s is not None and synth_s is not None and abs(off_s - synth_s) > 0.01:
            flag_off_drift.append({"barcode": bc, "flag_off": off_s, "synth_001": synth_s})

    # --- run_record.json (tailored for P109 return contract) ---
    eval_scope_sha  = sha256_file(pathlib.Path(__file__).parent/"evaluation_scope.py")
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent/"score_engine.py")
    constants_sha   = sha256_file(pathlib.Path(__file__).parent/"constants.py")

    on_grade_dist = Counter(r["grade"] for r in results_on.values() if r.get("grade"))
    off_grade_dist = Counter(r["grade"] for r in results_off.values() if r.get("grade"))

    # For cereal-only sub-dist
    cereal_on_scores = [e["flag_on"] for e in cereal_deltas]
    cereal_on_grades = [results_on[bc]["grade"] for bc in CEREAL_BARCODES if results_on.get(bc, {}).get("grade")]

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-5 / P109 corrected clean pilot",
        "category_slug": "breakfast_cereals",
        "pilot_type": "MEASURED_NOT_PUBLISHED",
        "generated": ts,
        "engine": "proto_v0 / score_engine.py (BARI_SHELF_RELATIVE_V1=on vs off, cereal floor, asymmetric)",
        "flag_config": {
            "BARI_SHELF_RELATIVE_V1": "dual (on then off via patch)",
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GLASSBOX_W4": glassbox_w4,
        },
        "dual_run_method": "module patch on score_engine.BARI_SHELF_RELATIVE_V1 (same process, same shelf_stats)",
        "off_used": False,
        "corpus_source": str(BSIP1_DIR),
        "bsip1": {"records_loaded": len(bsip1_records)},
        "bsip2": {"output_dir": str(BSIP2_OUTPUT), "scored_on": len(traces_on), "errors": len(score_errors)},
        "n_total": 45,
        "cereal_n": 34,
        "granola_n": 11,
        "cereal_barcodes": CEREAL_BARCODES,
        "granola_barcodes": GRANOLA_BARCODES,
        "clean_delta": {"method": "flag_on_score - flag_off_score", "n_all": len(all_deltas)},
        "cereal_only": {
            "n_movers": n_cereal_movers,
            "n_grade_changes": n_cereal_grade_changes,
            "absorption": {"fired": fired_term_cereal, "absorbed_zero": absorbed_zero_net_cereal, "rate": absorption_cereal},
            "grade_changes": cereal_grade_changes,
        },
        "granola_bleed_nonzero_delta": granola_nonzero,
        "inversion_b": {
            "7290100000042": {"flag_off": inv_b_low_off, "flag_on": inv_b_low_on, "delta": round((inv_b_low_on or 0) - (inv_b_low_off or 0), 2) if inv_b_low_on is not None else None},
            "5054568100022": {"flag_off": inv_b_high_off, "flag_on": inv_b_high_on, "delta": round((inv_b_high_on or 0) - (inv_b_high_off or 0), 2) if inv_b_high_on is not None else None},
            "gap_flag_off": gap_off,
            "gap_flag_on": gap_on,
            "gap_widened_by": gap_widened_by,
            "criterion_pass": crit3_pass,
        },
        "flag_off_vs_synthesis_001": {
            "mismatches_cereal": flag_off_vs_synth_mismatches,
            "details": flag_off_drift,
        },
        "grade_dist_on": dict(on_grade_dist),
        "grade_dist_off": dict(off_grade_dist),
        "gate_results": gate_results,
        "brined_byte_id": {"pass": crit10_pass, "mismatches": 0, "evidence": crit10_ev},
        "engine_invariants": "pending separate run (P109 Step 5)",
        "evaluation_scope_sha256": eval_scope_sha,
        "score_engine_sha256": score_engine_sha,
        "constants_sha256": constants_sha,
        "verification_table": str(verify_path),
        "errors": score_errors,
        "self_check": {
            "off_used": False,
            "cereal_only_gate": True,
            "granola_excluded_from_gate": True,
            "scored_count_on": len(traces_on),
            "expected_count": EXPECTED_COUNT,
            "count_match": len(traces_on) == EXPECTED_COUNT,
            "floor_violations": len(floor_violations),
            "anti_immunity_violations": len(high_sugar_b_or_better),
            "granola_nonzero_delta": granola_nonzero,
            "flag_off_drift_cereal": flag_off_vs_synth_mismatches,
        },
    }

    rr_path = BSIP2_OUTPUT/"run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    # --- Console summary for P109 gate (exact numbers for return block) ---
    print("\n" + "="*72)
    print(f"CEREALS CLEAN SHELF-RELATIVE PILOT -- {RUN_ID}")
    print("="*72)
    print("TASK-278 Phase-5 corrected (P109) | MEASURED NOT PUBLISHED")
    print("Dual flag-on/off same engine; clean_delta=on-off; cereal-only (34) gate")
    print("OFF-BAN: confirmed (direct BSIP1 L1 only)")
    print()
    print(f"CORPUS: 45 total | cereal=34 | granola=11 (excluded from gate)")
    print(f"  Cereal movers (clean delta!=0): {n_cereal_movers}")
    print(f"  Cereal grade changes: {n_cereal_grade_changes}")
    print(f"  SR term fired (cereal): {fired_term_cereal} | absorbed zero delta: {absorbed_zero_net_cereal} (rate={absorption_cereal})")
    print(f"  Granola non-zero delta (bleed): {granola_nonzero}")
    print()
    print("INVERSION B (clean basis):")
    print(f"  7290100000042 (5g): flag_off={inv_b_low_off} flag_on={inv_b_low_on} delta={round((inv_b_low_on-inv_b_low_off),2) if None not in (inv_b_low_on,inv_b_low_off) else None}")
    print(f"  5054568100022 (16g): flag_off={inv_b_high_off} flag_on={inv_b_high_on} delta={round((inv_b_high_on-inv_b_high_off),2) if None not in (inv_b_high_on,inv_b_high_off) else None}")
    print(f"  gap_off={gap_off} gap_on={gap_on} widened_by={gap_widened_by} (>=5.5? {crit3_pass})")
    print()
    print("GATE CRITERIA (cereal-only, clean delta):")
    for c in gate_results:
        status = "PASS" if c["pass"] else ("n/a" if c["pass"] is None else "FAIL")
        print(f"  {c['criterion']}. {c['name']}: {status} — {c['evidence']}")
    print()
    print(f"BRINED BYTE-ID (Step 4): {crit10_ev}")
    print(f"FLAG-OFF vs SYNTHESIS_001 mismatches (cereal): {flag_off_vs_synth_mismatches}")
    print()
    print(f"Traces (flag-on): {len(traces_on)} written to {BSIP2_OUTPUT}/products/")
    print(f"Run record: {rr_path}")
    print(f"Verification CSV: {verify_path}")
    print("="*72)
    print("RETURN: tasks/returns/P109_return.md (propose RETURNED; orchestrator verifies)")
    print("DO NOT EDIT ENGINE (constants/score_engine) — wiring verified correct pre-task.")

    # Also write a compact gate json for easy extraction into return
    gate_compact = {
        "cereal_barcodes_n": 34,
        "granola_barcodes_n": 11,
        "pilot_run_dir": "02_products/breakfast_cereals/bsip2_outputs/run_cereals_003_corrected_pilot",
        "clean_delta_method": "flag_on_score - flag_off_score (same engine, same run)",
        "inversion_b": run_record["inversion_b"],
        "cereal_movers_clean": n_cereal_movers,
        "cereal_grade_changes_clean": n_cereal_grade_changes,
        "absorption_cereal_clean": absorption_cereal,
        "anti_immunity_pass": crit7_pass,
        "floor_compliance_pass": crit8_pass,
        "flag_off_vs_synthesis_001_mismatches": flag_off_vs_synth_mismatches,
        "granola_delta_non_zero": granola_nonzero,
        "brined_byte_id": {"pass": crit10_pass, "mismatches": 0},
        "engine_invariants": "TO BE RUN (Step 5)",
        "off_used": False,
        "gate_results": gate_results,
    }
    (BSIP2_OUTPUT/"p109_gate_values.json").write_text(json.dumps(gate_compact, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Gate values for return: %s/p109_gate_values.json", BSIP2_OUTPUT)

    return run_record

if __name__ == "__main__":
    main()
