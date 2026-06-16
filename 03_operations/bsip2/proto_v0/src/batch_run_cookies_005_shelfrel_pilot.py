# BSIP2 batch -- Cookies-near-coffee SHELF-RELATIVE PILOT (run_cookies_005_shelfrel_pilot)
# TASK-278 Phase-2 / EV-085 — Biscuits x sugar asymmetric P>B shelf-relative enrollment.
# MEASURED, NOT PUBLISHED: no frontend JSON, no live-category edit, no deploy.
# Baseline: run_cookies_004 (58 products, C7/D22/E29, max 63.1/C).
# Flag config BEFORE engine imports (CRITICAL: must set BARI_SHELF_RELATIVE_V1=on).
import os, sys, json, pathlib, logging, datetime, hashlib
from collections import Counter

# --- Flag config BEFORE engine imports ---
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"     # EV-085 pilot activation (biscuit scope only)
os.environ["BARI_RECAL_P0"] = "off"             # sat-fat cliff cap 55 operative (same as run_004)
os.environ["BARI_GRAD_SODIUM_V1"] = "off"       # brined-only; cookies are not brined
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
# BARI_GLASSBOX_W4: leave at engine committed default (do NOT override; same as run_004)

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
    SUGAR_SHELF_REL_FORMULATION_FLOOR, HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD_G,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT        = pathlib.Path(r"C:\Bari")
BSIP0_FILE  = ROOT/"02_products"/"cookies_coffee"/"bsip0_outputs"/"cookies_coffee_bsip0_raw_20260613T163431.json"
CORPUS_FILE = ROOT/"02_products"/"cookies_coffee"/"factory_run_001"/"corpus_filter.json"
BSIP1_DIR   = ROOT/"03_operations"/"bsip1"/"run_cookies_001"/"output"
BSIP2_OUTPUT= ROOT/"02_products"/"cookies_coffee"/"bsip2_outputs"/"run_cookies_005_shelfrel_pilot"
BASELINE_DIR= ROOT/"02_products"/"cookies_coffee"/"bsip2_outputs"/"run_cookies_004"/"products"
RUN_ID = "run_cookies_005_shelfrel_pilot"
EXPECTED_COUNT = 58

# Spec parameters (EV-085)
PROPOSAL_MEDIAN   = 21.5   # g/100g
PROPOSAL_SCALE    = 5.115  # IQR-primary robust scale
SCALE_TOLERANCE   = 0.5    # |engine_scale - proposal_scale| <= 0.5 to proceed
MIN_N_GUARD       = 20

# Named inversion barcodes (D7 co-sign ratified)
INV_A_HIGH_SUGAR_BC = "5410126806250"   # Lotus 38.1g — baseline 18.1/E; expect -6 penalty
INV_A_LOW_SUGAR_BC  = "7290018371923"   # פתי בר אורגני 20.5g — baseline 29.0/E; expect 0 change
INV_B_LOW_SUGAR_BC  = "7290119041053"   # מרוקאי 13.5g — baseline 37.2/D; expect +2 relief
INV_B_HIGH_SUGAR_BC = "5317194"         # וניל הדר 22.0g — baseline 48.3/D; expect 0 change

(BSIP2_OUTPUT/"products").mkdir(parents=True, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def stdev(scores):
    if not scores: return 0.0
    n = len(scores); mean = sum(scores)/n
    return (sum((x-mean)**2 for x in scores)/n)**0.5

def extract_drivers(t):
    pens = t.get("penalties_applied",[]) or []
    caps = t.get("caps_applied",[]) or []
    drivers = []
    for p in pens[:2]: drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
    for c in caps[:2]:
        if c.get("cap"): drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
    return drivers or ["(no drivers)"]

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
    assert BARI_SHELF_RELATIVE_V1, "CRITICAL: BARI_SHELF_RELATIVE_V1 must be ON for pilot run"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    glassbox_w4 = os.environ.get("BARI_GLASSBOX_W4","engine_default(on)")
    log.info("=== BSIP2 Cookies SHELF-RELATIVE PILOT -- %s (EV-085) ===", RUN_ID)
    log.info("Flag BARI_SHELF_RELATIVE_V1=ON | scope={biscuit} | asymmetric P=6/B=3 | floor=55@20g")
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")

    # --- Load corpus ---
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"]=="IN_SCORED"}
    log.info("IN_SCORED barcodes: %d (expected %d)", len(in_scored), EXPECTED_COUNT)

    bsip1_records = []
    for p in sorted(BSIP1_DIR.glob("bsip1_cookies_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            if str(doc.get("barcode","")) in in_scored:
                bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)
    log.info("BSIP1 records loaded: %d", len(bsip1_records))

    # -----------------------------------------------------------------------
    # STEP 1: CALIBRATION RECHECK (co-sign cond 7 — BLOCKING)
    # Call compute_shelf_stats with the biscuit corpus sugars_g and report
    # the engine-computed median + robust_scale. Compare to proposal 21.5/5.115.
    # If |scale - 5.115| > 0.5 -> STOP.
    # -----------------------------------------------------------------------
    log.info("--- STEP 1: Calibration recheck (co-sign cond 7) ---")

    # Build product dicts for compute_shelf_stats: need normalized_nutrition_per_100g.sugars_g
    # The function reads normalized_nutrition_per_100g[nutrient] from each product dict.
    engine_median, engine_scale = compute_shelf_stats(
        bsip1_records,
        "sugars_g",
        scale_type="iqr",
        nutrient_min_scale=SUGAR_SHELF_SCALE_MIN,
    )
    log.info("Engine computed: median=%.3f, robust_scale=%.3f (n=%d)", engine_median or 0, engine_scale or 0, len(bsip1_records))
    log.info("Proposal expected: median=%.3f, robust_scale=%.3f", PROPOSAL_MEDIAN, PROPOSAL_SCALE)

    calibration_ok = False
    scale_divergence = None
    if engine_scale is None:
        log.error("CALIBRATION FAIL: compute_shelf_stats returned None — no sugars_g data found")
        calibration_result = "FAIL: engine returned None scale"
    else:
        scale_divergence = abs(engine_scale - PROPOSAL_SCALE)
        if scale_divergence > SCALE_TOLERANCE:
            log.error(
                "CALIBRATION FAIL (BLOCKING): |engine_scale %.3f - proposal_scale %.3f| = %.3f > %.1f tolerance",
                engine_scale, PROPOSAL_SCALE, scale_divergence, SCALE_TOLERANCE
            )
            log.error("Per co-sign cond 7: DO NOT RUN PILOT. Report divergence to orchestrator.")
            calibration_result = f"FAIL: |{engine_scale:.3f} - {PROPOSAL_SCALE:.3f}| = {scale_divergence:.3f} > {SCALE_TOLERANCE}"
            # Write a calibration failure record and exit
            fail_record = {
                "run_id": RUN_ID,
                "status": "CALIBRATION_FAIL_BLOCKED",
                "calibration": {
                    "engine_median": engine_median,
                    "engine_scale": engine_scale,
                    "proposal_median": PROPOSAL_MEDIAN,
                    "proposal_scale": PROPOSAL_SCALE,
                    "scale_divergence": scale_divergence,
                    "tolerance": SCALE_TOLERANCE,
                    "result": calibration_result,
                },
                "generated": ts,
            }
            fail_path = BSIP2_OUTPUT/"calibration_fail.json"
            fail_path.write_text(json.dumps(fail_record, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"\nCALIBRATION FAIL (BLOCKING): scale divergence {scale_divergence:.3f} > {SCALE_TOLERANCE}")
            print(f"Per co-sign cond 7: pilot NOT run. Record: {fail_path}")
            return fail_record
        else:
            calibration_ok = True
            calibration_result = f"PASS: |{engine_scale:.3f} - {PROPOSAL_SCALE:.3f}| = {scale_divergence:.3f} <= {SCALE_TOLERANCE}"
            log.info("Calibration PASS: scale divergence %.3f <= %.1f tolerance", scale_divergence, SCALE_TOLERANCE)

    log.info("Calibration result: %s", calibration_result)
    log.info("Using engine-computed scale: median=%.3f, robust_scale=%.3f", engine_median, engine_scale)

    # -----------------------------------------------------------------------
    # STEP 2: Set shelf stats for the engine (biscuit scope, sugars_g)
    # -----------------------------------------------------------------------
    clear_shelf_stats()
    set_shelf_stats(
        nutrient="sugars_g",
        median=engine_median,
        scale=engine_scale,
        scale_type="iqr",
        n=len([r for r in bsip1_records if r.get("normalized_nutrition_per_100g", {}).get("sugars_g") is not None]),
    )
    log.info("Shelf stats set: sugars_g median=%.3f scale=%.3f", engine_median, engine_scale)

    # -----------------------------------------------------------------------
    # STEP 3: Run the pilot rescore
    # -----------------------------------------------------------------------
    log.info("--- STEP 3: Pilot rescore (BARI_SHELF_RELATIVE_V1=on, scope={biscuit}) ---")

    traces, score_errors, brined_flag_fired, routing_cats = [], [], [], {}

    # Track named inversion products
    inversion_traces = {}

    for doc in bsip1_records:
        barcode = str(doc.get("barcode",""))
        name    = doc.get("canonical_name_he","")
        try:
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, BSIP2_OUTPUT)
            traces.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat   = trace.get("category")
            nova  = trace.get("nova_proxy")
            ctx_flag = trace.get("context_flag")
            routing_cats[cat] = routing_cats.get(cat,0) + 1

            if ctx_flag == "brined_food":
                brined_flag_fired.append({"barcode":barcode,"name":name,"score":score,"grade":grade})
                log.error("  CRITICAL: brined_food fired on %s (%s)!", barcode, name)

            # Track named inversion products
            if barcode in (INV_A_HIGH_SUGAR_BC, INV_A_LOW_SUGAR_BC, INV_B_LOW_SUGAR_BC, INV_B_HIGH_SUGAR_BC):
                sugar_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
                shelf_rel_pen = None
                for p in (trace.get("penalties_applied") or []):
                    if p.get("rule") == "SUGAR_SHELF_REL_V1":
                        shelf_rel_pen = p.get("amount")
                        break
                floor_applied = trace.get("ev085_formulation_floor_applied")
                inversion_traces[barcode] = {
                    "barcode": barcode, "name": name, "score": score, "grade": grade,
                    "sugars_g": sugar_val, "shelf_rel_pen": shelf_rel_pen,
                    "floor_applied": floor_applied,
                }
                log.info("  INVERSION [%s] %-40s score=%-5s grade=%-2s sugar=%-5s rel_pen=%s floor=%s",
                         barcode, name[:38], score, grade, sugar_val, shelf_rel_pen, floor_applied)
            else:
                log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-20s nova=%s",
                         name[:38], score, grade, cat, nova)
        except Exception as e:
            log.error("  BSIP2 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode":barcode,"name":name,"error":str(e)})

    # -----------------------------------------------------------------------
    # STEP 4: Compute pilot statistics
    # -----------------------------------------------------------------------
    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]
    grade_dist = {}
    for t in traces:
        g = t.get("grade_estimate","?")
        grade_dist[g] = grade_dist.get(g,0)+1

    if all_scores:
        ss = sorted(all_scores); n = len(ss)
        pilot_median   = ss[n//2] if n%2 else (ss[n//2-1]+ss[n//2])/2
        score_min      = min(all_scores); score_max = max(all_scores)
        score_stdev    = round(stdev(all_scores),2)
        score_range_v  = round(score_max - score_min, 2)
        mc = Counter(all_scores).most_common(1)[0]
        most_common_score, most_common_count = mc[0], mc[1]
    else:
        pilot_median=score_min=score_max=score_stdev=score_range_v=most_common_score=most_common_count=None

    histogram = {}
    for s in (all_scores or []):
        band = f"{int(s//10)*10}-{int(s//10)*10+9}"
        histogram[band] = histogram.get(band,0)+1

    # -----------------------------------------------------------------------
    # Load baseline scores from run_cookies_004 for delta computation
    # -----------------------------------------------------------------------
    baseline_scores = {}
    baseline_dir_products = BASELINE_DIR
    for trace_dir in sorted(baseline_dir_products.iterdir()):
        if not trace_dir.is_dir(): continue
        trace_file = trace_dir / "bsip2_trace.json"
        if not trace_file.exists(): continue
        try:
            bt = json.loads(trace_file.read_text(encoding="utf-8"))
            bc_key = str(bt.get("barcode") or (bt.get("input_reference") or {}).get("barcode") or "")
            if bc_key:
                baseline_scores[bc_key] = {
                    "score": bt.get("final_score_estimate"),
                    "grade": bt.get("grade_estimate"),
                }
        except Exception as e:
            log.warning("Baseline read error %s: %s", trace_dir.name, e)

    log.info("Baseline scores loaded: %d products", len(baseline_scores))

    # Per-product deltas
    deltas = []
    for t in traces:
        bc = str(t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or "")
        pilot_s = t.get("final_score_estimate")
        base_s  = baseline_scores.get(bc, {}).get("score")
        if pilot_s is not None and base_s is not None:
            deltas.append({"barcode": bc, "baseline": base_s, "pilot": pilot_s, "delta": round(pilot_s - base_s, 2)})

    avg_delta = round(sum(d["delta"] for d in deltas) / len(deltas), 4) if deltas else None
    log.info("Average score delta (baseline -> pilot): %.4f (criterion: <=1.5)", avg_delta or 0)

    # -----------------------------------------------------------------------
    # STEP 4: Named inversion verification
    # -----------------------------------------------------------------------
    inv_a_high = inversion_traces.get(INV_A_HIGH_SUGAR_BC, {})
    inv_a_low  = inversion_traces.get(INV_A_LOW_SUGAR_BC, {})
    inv_b_low  = inversion_traces.get(INV_B_LOW_SUGAR_BC, {})
    inv_b_high = inversion_traces.get(INV_B_HIGH_SUGAR_BC, {})

    inv_a_gap_baseline = 10.9   # 29.0 - 18.1 = 10.9 (low scores higher than high, so gap is pos)
    inv_b_gap_baseline = 11.1   # 48.3 - 37.2 = 11.1 (high scores higher than low, inversion)

    inv_a_high_score = inv_a_high.get("score")
    inv_a_low_score  = inv_a_low.get("score")
    inv_b_low_score  = inv_b_low.get("score")
    inv_b_high_score = inv_b_high.get("score")

    inv_a_gap_pilot = None
    inv_b_gap_pilot = None
    if inv_a_low_score is not None and inv_a_high_score is not None:
        inv_a_gap_pilot = round(inv_a_low_score - inv_a_high_score, 2)
    if inv_b_high_score is not None and inv_b_low_score is not None:
        inv_b_gap_pilot = round(inv_b_high_score - inv_b_low_score, 2)

    # -----------------------------------------------------------------------
    # STEP 4: Floor compliance check (cond 5 — all 51+ products with sugar>=20g must score <=55)
    # -----------------------------------------------------------------------
    floor_compliance = []
    floor_violations = []
    for t in traces:
        bc = str(t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or "")
        pilot_s = t.get("final_score_estimate")
        # Get sugar from bsip1 record
        sugar_val = None
        for doc in bsip1_records:
            if str(doc.get("barcode","")) == bc:
                sugar_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
                break
        if sugar_val is not None and sugar_val >= HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD_G:
            cat = t.get("category","")
            compliant = (pilot_s is None or pilot_s <= SUGAR_SHELF_REL_FORMULATION_FLOOR)
            entry = {"barcode": bc, "sugars_g": sugar_val, "score": pilot_s, "compliant": compliant, "category": cat}
            floor_compliance.append(entry)
            if not compliant:
                floor_violations.append(entry)
                log.error("  FLOOR VIOLATION: %s sugar=%.1f score=%.1f > floor=%d", bc, sugar_val, pilot_s, SUGAR_SHELF_REL_FORMULATION_FLOOR)

    log.info("Floor compliance: %d products with sugar>=%.0fg checked, %d violations",
             len(floor_compliance), HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD_G, len(floor_violations))

    # -----------------------------------------------------------------------
    # STEP 4: D->C via relief check (B=2 recalibration trigger)
    # Products that crossed from D (<65) to C (>=65) via the relief term
    # -----------------------------------------------------------------------
    d_to_c_crossings = []
    GRADE_C_THRESHOLD = 65.0
    GRADE_D_THRESHOLD = 40.0  # D: 40-64
    for d in deltas:
        bc = d["barcode"]
        base_s = d["baseline"]
        pilot_s = d["pilot"]
        # Check if base was D (<65) and pilot is C (>=65)
        base_grade = score_to_grade(base_s) if base_s is not None else None
        pilot_grade = score_to_grade(pilot_s) if pilot_s is not None else None
        if base_grade == "D" and pilot_grade == "C":
            # Get sugar
            sugar_val = None
            for doc in bsip1_records:
                if str(doc.get("barcode","")) == bc:
                    sugar_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
                    break
            d_to_c_crossings.append({
                "barcode": bc, "base_score": base_s, "pilot_score": pilot_s,
                "delta": d["delta"], "sugars_g": sugar_val,
            })
            log.warning("  D->C CROSSING: %s base=%.1f pilot=%.1f sugar=%s (B=2 recal trigger if present)",
                        bc, base_s, pilot_s, sugar_val)

    # -----------------------------------------------------------------------
    # STEP 4: 7 pilot success criteria evaluation
    # -----------------------------------------------------------------------
    baseline_grade_dist = {"C": 7, "D": 22, "E": 29, "B": 0, "A": 0}  # from run_cookies_004
    pilot_grade_c = grade_dist.get("C", 0)
    pilot_grade_d = grade_dist.get("D", 0)
    pilot_grade_e = grade_dist.get("E", 0)
    pilot_grade_b = grade_dist.get("B", 0)
    pilot_grade_a = grade_dist.get("A", 0)

    # Criterion 1: Resolution restored (fewer products pinned at identical cliff scores vs baseline)
    baseline_cliff_counts = Counter(baseline_scores[bc]["score"] for bc in baseline_scores)
    pilot_cliff_counts = Counter(t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None)
    baseline_max_pinned = max(baseline_cliff_counts.values()) if baseline_cliff_counts else 0
    pilot_max_pinned    = max(pilot_cliff_counts.values()) if pilot_cliff_counts else 0
    crit1_pass = pilot_max_pinned < baseline_max_pinned
    crit1_note = f"baseline max_pinned={baseline_max_pinned}, pilot max_pinned={pilot_max_pinned}"

    # Criterion 2: Rank inversions corrected (both Inv A gap widened, Inv B gap narrowed)
    inv_a_pass = (inv_a_gap_pilot is not None and inv_a_gap_pilot >= 13.0)
    inv_b_pass = (inv_b_gap_pilot is not None and inv_b_gap_pilot <= 10.0)
    crit2_pass = inv_a_pass and inv_b_pass
    crit2_note = (f"InvA gap: baseline={inv_a_gap_baseline} pilot={inv_a_gap_pilot} "
                  f"(need>=13) {'PASS' if inv_a_pass else 'FAIL'}; "
                  f"InvB gap: baseline={inv_b_gap_baseline} pilot={inv_b_gap_pilot} "
                  f"(need<=10) {'PASS' if inv_b_pass else 'FAIL'}")

    # Criterion 3: Shelf average stable (avg delta <= 1.5 pts)
    crit3_pass = avg_delta is not None and abs(avg_delta) <= 1.5
    crit3_note = f"avg_delta={avg_delta} (need<=1.5)"

    # Criterion 4: Anti-Immunity holds (no biscuit with sugar>=20g reaches grade A)
    high_sugar_a_count = sum(1 for e in floor_compliance if e.get("score") is not None and e["score"] >= 80)
    crit4_pass = high_sugar_a_count == 0
    crit4_note = f"high_sugar (>=20g) products at A (>=80): {high_sugar_a_count} (need=0)"

    # Criterion 5: Absolute floor enforced (all 51+ products with sugar>=20g score <=55)
    crit5_pass = len(floor_violations) == 0
    crit5_note = f"{len(floor_compliance)} products with sugar>=20g checked, {len(floor_violations)} violations (need=0)"

    # Criterion 6: Flag-off byte-identical (verified separately via p56_byte_identity.py pattern)
    # Reported as "requires separate check" — done in Step 5 (no-regression)
    crit6_pass = None   # set by no-regression step
    crit6_note = "Verified separately: BARI_SHELF_RELATIVE_V1=off byte-identity test (Step 5)"

    # Criterion 7: No cross-category contamination (scope guard holds for non-biscuit categories)
    # All products in this corpus should route to biscuit; non-biscuit products untouched.
    non_biscuit_with_shelf_rel = []
    for t in traces:
        cat = t.get("category","")
        if cat != "biscuit":
            for p in (t.get("penalties_applied") or []):
                if p.get("rule") == "SUGAR_SHELF_REL_V1":
                    non_biscuit_with_shelf_rel.append({"barcode": str(t.get("barcode","")), "category": cat, "penalty": p})
    crit7_pass = len(non_biscuit_with_shelf_rel) == 0
    crit7_note = (f"Non-biscuit products with SUGAR_SHELF_REL_V1 fired: {len(non_biscuit_with_shelf_rel)} (need=0). "
                  f"Cross-category contamination by external published categories verified separately in Step 5.")

    success_criteria = [
        {"criterion": 1, "name": "Resolution restored", "pass": crit1_pass, "note": crit1_note},
        {"criterion": 2, "name": "Rank inversions corrected", "pass": crit2_pass, "note": crit2_note},
        {"criterion": 3, "name": "Shelf average stable (<=1.5 pts)", "pass": crit3_pass, "note": crit3_note},
        {"criterion": 4, "name": "Anti-Immunity holds (no sugar>=20g at A)", "pass": crit4_pass, "note": crit4_note},
        {"criterion": 5, "name": "Absolute floor enforced (sugar>=20g score<=55)", "pass": crit5_pass, "note": crit5_note},
        {"criterion": 6, "name": "Flag-off byte-identical", "pass": crit6_pass, "note": crit6_note},
        {"criterion": 7, "name": "No cross-category contamination", "pass": crit7_pass, "note": crit7_note},
    ]

    all_pass = all(c["pass"] for c in success_criteria if c["pass"] is not None)
    crit_summary = {f"C{c['criterion']}": ('PASS' if c['pass'] else ('UNKNOWN' if c['pass'] is None else 'FAIL')) for c in success_criteria}

    # -----------------------------------------------------------------------
    # Write verification table
    # -----------------------------------------------------------------------
    verify_path = BSIP2_OUTPUT/"verification_table.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        vf.write("barcode,pilot_score,pilot_grade,baseline_score,baseline_grade,delta,sugars_g,shelf_rel_pen,floor_applied,binding_cap,category\n")
        for t in sorted(traces, key=lambda x: str(x.get("barcode") or "")):
            bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or ""
            bc_str = str(bc)
            pilot_s = t.get("final_score_estimate")
            pilot_g = t.get("grade_estimate")
            base_s  = baseline_scores.get(bc_str, {}).get("score")
            base_g  = baseline_scores.get(bc_str, {}).get("grade")
            delta_v = round(pilot_s - base_s, 2) if (pilot_s is not None and base_s is not None) else ""
            sugar_v = None
            for doc in bsip1_records:
                if str(doc.get("barcode","")) == bc_str:
                    sugar_v = (doc.get("normalized_nutrition_per_100g") or {}).get("sugars_g")
                    break
            rel_pen = ""
            for p in (t.get("penalties_applied") or []):
                if p.get("rule") == "SUGAR_SHELF_REL_V1":
                    rel_pen = p.get("amount","")
                    break
            floor_app = t.get("ev085_formulation_floor_applied", "")
            row = ",".join(str(x) for x in [bc_str, pilot_s, pilot_g, base_s, base_g, delta_v,
                                              sugar_v, rel_pen, floor_app, t.get("binding_cap"), t.get("category")])
            vf.write(row + "\n")

    # -----------------------------------------------------------------------
    # Write run record
    # -----------------------------------------------------------------------
    eval_scope_sha  = sha256_file(pathlib.Path(__file__).parent/"evaluation_scope.py")
    score_engine_sha = sha256_file(pathlib.Path(__file__).parent/"score_engine.py")
    constants_sha   = sha256_file(pathlib.Path(__file__).parent/"constants.py")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-2 / EV-085",
        "category_slug": "cookies-coffee",
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
            "BARI_GLASSBOX_W4": glassbox_w4,
        },
        "calibration": {
            "proposal_median_g": PROPOSAL_MEDIAN,
            "proposal_scale_g":  PROPOSAL_SCALE,
            "engine_median_g":   engine_median,
            "engine_scale_g":    engine_scale,
            "scale_divergence":  scale_divergence,
            "tolerance":         SCALE_TOLERANCE,
            "result":            calibration_result,
        },
        "shelf_stats_set": {
            "nutrient": "sugars_g",
            "median":   engine_median,
            "scale":    engine_scale,
            "scale_type": "iqr",
        },
        "off_used": False,
        "corpus_source":    str(CORPUS_FILE),
        "bsip1_source":     str(BSIP1_DIR),
        "in_scored_count":  len(in_scored),
        "bsip1": {"records_loaded": len(bsip1_records)},
        "bsip2": {"output_dir": str(BSIP2_OUTPUT), "scored": len(traces), "errors": len(score_errors)},
        "score_distribution": {
            "min": score_min, "max": score_max, "median": pilot_median,
            "stdev": score_stdev, "range": score_range_v,
            "most_common_score": most_common_score, "most_common_count": most_common_count,
            "histogram": histogram,
            "grade_dist": grade_dist,
        },
        "baseline_grade_dist": baseline_grade_dist,
        "routing_distribution": routing_cats,
        "avg_score_delta_baseline_to_pilot": avg_delta,
        "per_product_deltas": deltas,
        "named_inversions": {
            "inversion_A": {
                "description": "Lotus (38.1g sugar) vs פתי בר אורגני (20.5g sugar) — within-E resolution",
                "high_sugar_barcode": INV_A_HIGH_SUGAR_BC,
                "low_sugar_barcode":  INV_A_LOW_SUGAR_BC,
                "gap_baseline_pts":   inv_a_gap_baseline,
                "gap_pilot_pts":      inv_a_gap_pilot,
                "high_sugar_trace":   inv_a_high,
                "low_sugar_trace":    inv_a_low,
                "pass_condition":     "gap >= 13 pts",
                "pass":               inv_a_pass,
            },
            "inversion_B": {
                "description": "מרוקאי (13.5g sugar) vs וניל הדר (22g sugar) — true rank inversion",
                "low_sugar_barcode":  INV_B_LOW_SUGAR_BC,
                "high_sugar_barcode": INV_B_HIGH_SUGAR_BC,
                "gap_baseline_pts":   inv_b_gap_baseline,
                "gap_pilot_pts":      inv_b_gap_pilot,
                "low_sugar_trace":    inv_b_low,
                "high_sugar_trace":   inv_b_high,
                "pass_condition":     "gap <= 10 pts",
                "pass":               inv_b_pass,
            },
        },
        "floor_compliance": {
            "high_sugar_threshold_g": HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD_G,
            "floor_value": SUGAR_SHELF_REL_FORMULATION_FLOOR,
            "products_checked": len(floor_compliance),
            "violations": len(floor_violations),
            "violation_list": floor_violations,
            "full_list": floor_compliance,
        },
        "d_to_c_crossings": d_to_c_crossings,
        "success_criteria": success_criteria,
        "success_criteria_summary": crit_summary,
        "all_criteria_pass": all_pass,
        "brined_flag": {
            "fired_count": len(brined_flag_fired),
            "guard_pass": len(brined_flag_fired) == 0,
            "fired_products": brined_flag_fired,
        },
        "evaluation_scope_sha256": eval_scope_sha,
        "score_engine_sha256": score_engine_sha,
        "constants_sha256": constants_sha,
        "verification_table": str(verify_path),
        "errors": score_errors,
        "self_check": {
            "off_used": False,
            "flag_on": BARI_SHELF_RELATIVE_V1,
            "calibration_pass": calibration_ok,
            "brined_food_fired": len(brined_flag_fired),
            "brined_food_guard_pass": len(brined_flag_fired) == 0,
            "scored_count": len(traces),
            "expected_count": EXPECTED_COUNT,
            "count_match": len(traces) == EXPECTED_COUNT,
            "floor_violations": len(floor_violations),
            "floor_compliance_pass": len(floor_violations) == 0,
            "non_biscuit_shelf_rel_fired": len(non_biscuit_with_shelf_rel),
        },
    }

    rr_path = BSIP2_OUTPUT/"run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", rr_path)

    # -----------------------------------------------------------------------
    # Final report
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print(f"COOKIES SHELF-RELATIVE PILOT -- {RUN_ID}")
    print("="*70)
    print(f"TASK-278 Phase-2 / EV-085 | MEASURED NOT PUBLISHED")
    print(f"Flag: BARI_SHELF_RELATIVE_V1=ON | scope={{biscuit}} | P=6/B=3 | floor=55@20g")
    print()
    print(f"CALIBRATION RECHECK (co-sign cond 7):")
    print(f"  Engine:   median={engine_median:.3f}g  scale={engine_scale:.3f}g")
    print(f"  Proposal: median={PROPOSAL_MEDIAN:.3f}g  scale={PROPOSAL_SCALE:.3f}g")
    print(f"  Divergence: |{engine_scale:.3f} - {PROPOSAL_SCALE:.3f}| = {scale_divergence:.3f}  (tolerance: {SCALE_TOLERANCE})")
    print(f"  Result: {calibration_result}")
    print()
    print(f"CORPUS: {len(in_scored)} IN_SCORED | BSIP1: {len(bsip1_records)} | Scored: {len(traces)} | Errors: {len(score_errors)}")
    print()
    print(f"GRADE DISTRIBUTION:")
    print(f"  Baseline:  A={baseline_grade_dist['A']} B={baseline_grade_dist['B']} C={baseline_grade_dist['C']} D={baseline_grade_dist['D']} E={baseline_grade_dist['E']}")
    print(f"  Pilot:     A={pilot_grade_a} B={pilot_grade_b} C={pilot_grade_c} D={pilot_grade_d} E={pilot_grade_e}")
    print(f"  Delta:     A={pilot_grade_a-baseline_grade_dist['A']:+d} B={pilot_grade_b-baseline_grade_dist['B']:+d} C={pilot_grade_c-baseline_grade_dist['C']:+d} D={pilot_grade_d-baseline_grade_dist['D']:+d} E={pilot_grade_e-baseline_grade_dist['E']:+d}")
    print()
    print(f"SCORE DISTRIBUTION (pilot):")
    print(f"  Max: {score_max}  Median: {pilot_median}  Min: {score_min}  StDev: {score_stdev}")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print()
    print(f"AVERAGE SCORE DELTA (baseline->pilot): {avg_delta} pts (criterion: <=1.5)")
    print()
    print(f"NAMED INVERSIONS:")
    print(f"  Inversion A (Lotus vs פתי בר אורגני):")
    print(f"    Lotus       [{INV_A_HIGH_SUGAR_BC}]: baseline=18.1/E  pilot={inv_a_high.get('score')}/{inv_a_high.get('grade')}  rel_pen={inv_a_high.get('shelf_rel_pen')}")
    print(f"    פתי בר      [{INV_A_LOW_SUGAR_BC}]:  baseline=29.0/E  pilot={inv_a_low.get('score')}/{inv_a_low.get('grade')}   rel_pen={inv_a_low.get('shelf_rel_pen')}")
    print(f"    Gap: baseline={inv_a_gap_baseline}  pilot={inv_a_gap_pilot}  (pass: >=13)  -> {'PASS' if inv_a_pass else 'FAIL'}")
    print()
    print(f"  Inversion B (מרוקאי vs וניל הדר):")
    print(f"    מרוקאי      [{INV_B_LOW_SUGAR_BC}]:  baseline=37.2/D  pilot={inv_b_low.get('score')}/{inv_b_low.get('grade')}   rel_pen={inv_b_low.get('shelf_rel_pen')}")
    print(f"    וניל הדר    [{INV_B_HIGH_SUGAR_BC}]:    baseline=48.3/D  pilot={inv_b_high.get('score')}/{inv_b_high.get('grade')}   rel_pen={inv_b_high.get('shelf_rel_pen')}")
    print(f"    Gap: baseline={inv_b_gap_baseline}  pilot={inv_b_gap_pilot}  (pass: <=10)  -> {'PASS' if inv_b_pass else 'FAIL'}")
    print()
    print(f"FLOOR COMPLIANCE (sugar>=20g -> score<=55):")
    print(f"  Products checked: {len(floor_compliance)} | Violations: {len(floor_violations)} (pass: 0)")
    if floor_violations:
        for v in floor_violations:
            print(f"  VIOLATION: {v['barcode']} sugar={v['sugars_g']} score={v['score']}")
    print()
    print(f"D->C CROSSINGS via relief: {len(d_to_c_crossings)} (B=2 recal trigger if >0)")
    if d_to_c_crossings:
        for x in d_to_c_crossings:
            print(f"  {x['barcode']} base={x['base_score']} pilot={x['pilot_score']} sugar={x['sugars_g']}")
    print()
    print(f"7 PILOT SUCCESS CRITERIA:")
    for c in success_criteria:
        status = 'PASS' if c['pass'] else ('UNKNOWN' if c['pass'] is None else 'FAIL')
        print(f"  C{c['criterion']} [{status}]: {c['name']} — {c['note']}")
    print()
    print(f"ALL CRITERIA PASS (excl. C6 which requires separate check): {all_pass}")
    print()
    print(f"NO-REGRESSION (Step 5): run separately:")
    print(f"  1. python 03_operations/bsip2/proto_v0/src/p56_byte_identity.py  (flag-off byte-identical)")
    print(f"  2. python 03_operations/shadow/engine_invariants.py")
    print(f"  3. Non-biscuit corpus rescore with flag=on (brined or milk) -> 0 movement")
    print()
    print(f"score_engine.py SHA256: {score_engine_sha[:16]}...")
    print(f"constants.py SHA256:    {constants_sha[:16]}...")
    print(f"Run record: {rr_path}")
    print(f"Verification table: {verify_path}")
    print("="*70)
    return run_record

if __name__ == "__main__":
    main()
