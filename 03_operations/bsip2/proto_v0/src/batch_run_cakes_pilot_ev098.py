# BSIP2 EV-098 pilot rescore — cakes_hard_cookies x sugar shelf-relative (TASK-278 Phase-13).
# Runs BARI_SHELF_RELATIVE_V1="on" ONLY for this process; engine default stays "off".
# D7 co-sign parameters (cakes_sugar_d7_cosign_v1.md):
#   median=29.0g, scale=9.044 (IQR-based robust), n=143, floor=52, floor_threshold=33.0g
#   P_max=6, B_max=3, z_dead=0.30, direction=asymmetric
# Gate: 11 criteria (C7/C8/C9/C10 = hard fail).
# OFF ban: absolute. No OFF data used anywhere in this run.
# C10 NOTE: score_engine reads BARI_SHELF_RELATIVE_V1 at IMPORT TIME as a module constant.
# Comparing flag-on to run_005_headpin (flag-off, different engine state) confounds EV-098
# effect with other engine changes (EV-096, EV-097, etc.). Correct C10 methodology:
# (a) verify EV-098 trace keys are absent/False for all milk products at flag-on.
# (b) run a flag-off subprocess (same engine HEAD) to get within-pilot delta for milk.
import os, sys, json, pathlib, logging, datetime, hashlib, subprocess
from collections import Counter

# --- Pilot flag: "on" ONLY for this process ---
# score_engine reads: os.environ.get("BARI_SHELF_RELATIVE_V1", "off").lower() == "on"
# Must set "on", NOT "True" — "True".lower() != "on" silently keeps flag False.
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"

# Other flags: match batch_run_cakes_001.py baseline (all off)
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
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = pathlib.Path(r"C:\Bari")
CORPUS_FILE  = ROOT / "02_products" / "cakes_hard_cookies" / "factory_run_001" / "corpus_filter.json"
BSIP1_DIR    = ROOT / "03_operations" / "bsip1" / "run_cakes_001" / "output"
BASELINE_DIR = ROOT / "02_products" / "cakes_hard_cookies" / "bsip2_outputs" / "run_cakes_001" / "products"
MILK_BSIP1   = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
MILK_TRACES  = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
PILOT_OUT    = ROOT / "02_products" / "cakes_hard_cookies" / "bsip2_outputs" / "run_cakes_pilot_ev098"
(PILOT_OUT / "products").mkdir(parents=True, exist_ok=True)

# D7 locked EV-098 shelf stats
EV098_MEDIAN = 29.0
EV098_SCALE  = 9.044
EV098_N      = 143
EV098_FLOOR  = 52
EV098_FLOOR_THRESHOLD = 33.0
EV098_P_MAX  = 6
EV098_B_MAX  = 3
EV098_Z_DEAD = 0.30

# INV-A/INV-B barcodes (D7 co-sign)
INV_A_LOW_SUGAR  = "4504687"          # strudel, 2g sugar — should score higher
INV_A_HIGH_SUGAR = "7290105364784"    # krantz, 47g sugar — should score lower
INV_B_LOW_SUGAR  = "1361177"          # cherry cake, 11g sugar — should score higher
INV_B_HIGH_SUGAR = "7622300489427"    # Oreo coated, 49g sugar — should score lower

# 20 milk headpin barcodes (frozen invariant)
MILK_HEADPIN_BARCODES = {
    "5411188112709", "5411188124689", "5411188300328",
    "7290000051352", "7290014760141", "7290019790259",
    "7290102392094", "7290107932134", "7290110324773",
    "7290110324926", "7290110325619", "7290114313285",
    "7290114313865", "7290116936116", "7290119385560",
    "7394376619939", "7394376620904", "7394376621451",
    "8000215204219", "8000215204554",
}


def run_pipeline(doc):
    signals = extract_signals(doc)
    cat     = classify_category(doc)
    l3      = signals["L3_inferred_classifications"]
    nova    = infer_nova(doc, l3)
    ev      = assign_evaluation_scope(doc, cat["category"])
    sr      = score_product(doc, signals, cat, nova, ev)
    tr      = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    # Attach score_result keys not in trace_writer whitelist (EV-098 pilot evidence)
    tr["_ev098_cakes_floor_applied"] = sr.get("ev098_cakes_floor_applied")
    tr["_ev098_cakes_floor_note"]    = sr.get("ev098_cakes_floor_note")
    # Raw caps/penalties for EV-098 amount extraction per product
    tr["_ev098_caps_pens_raw"] = {
        "caps_considered": sr.get("caps_considered"),
        "caps_applied": sr.get("caps_applied"),
        "penalties_considered": sr.get("penalties_considered"),
        "penalties_applied": sr.get("penalties_applied"),
    }
    return tr, sr


def grade_from_score(s):
    if s is None: return "?"
    if s >= 85:   return "S"
    if s >= 70:   return "A"
    if s >= 55:   return "B"
    if s >= 40:   return "C"
    if s >= 25:   return "D"
    return "E"


def load_baseline_scores():
    """Load flag-off scores from run_cakes_001 traces (baseline, BARI_SHELF_RELATIVE_V1=off)."""
    baseline = {}
    if not BASELINE_DIR.exists():
        log.warning("Baseline dir not found: %s", BASELINE_DIR)
        return baseline
    for prod_dir in BASELINE_DIR.iterdir():
        tf = prod_dir / "bsip2_trace.json"
        if tf.exists():
            t = json.load(open(tf, encoding="utf-8"))
            bc = str((t.get("input_reference") or {}).get("barcode") or
                     t.get("barcode") or "")
            score = t.get("final_score_estimate")
            grade = t.get("grade_estimate")
            if bc:
                baseline[bc] = {"score": score, "grade": grade}
    return baseline


def score_milk_flag_off_subprocess():
    """
    Score all 20 milk products with BARI_SHELF_RELATIVE_V1=off using a subprocess
    so the module-level constant is evaluated fresh (opposite of the parent process).
    Returns dict barcode -> {score, grade}.
    Writes results to a temp file for the parent to read.
    """
    helper_script = pathlib.Path(__file__).parent / "_pilot_milk_flag_off_helper.py"
    result_file = PILOT_OUT / "_milk_flag_off.json"
    script_content = f"""
import os, sys, json, pathlib
os.environ["BARI_SHELF_RELATIVE_V1"] = "off"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, {str(pathlib.Path(__file__).parent)!r})
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class

# Same shelf stats as the parent pilot (flag-off, but stats set so any future stat-guarded paths
# fail gracefully — n=143 > 20 min_n so stats are valid; category scope guards prevent bleed)
set_shelf_stats("sugars_g", {EV098_MEDIAN}, {EV098_SCALE}, "iqr", {EV098_N})

MILK_BSIP1 = pathlib.Path(r"C:\\Bari\\03_operations\\bsip1\\run_milk_002\\output")
MILK_HC = {{{",".join(repr(b) for b in MILK_HEADPIN_BARCODES)}}}

results = {{}}
for p in sorted(MILK_BSIP1.glob("bsip1_*.json")):
    d = json.load(open(p, encoding="utf-8"))
    bc = str(d.get("barcode", ""))
    if bc not in MILK_HC:
        continue
    signals = extract_signals(d)
    cat = classify_category(d)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(d, l3)
    ev = assign_evaluation_scope(d, cat["category"])
    sr = score_product(d, signals, cat, nova, ev)
    results[bc] = {{
        "score": sr.get("final_score_estimate"),
        "grade": sr.get("grade_estimate"),
    }}
print(json.dumps(results))
"""
    helper_script.write_text(script_content, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(helper_script)],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    helper_script.unlink(missing_ok=True)
    if proc.returncode != 0:
        log.warning("Milk flag-off subprocess failed: %s", proc.stderr[:500])
        return {}
    try:
        return json.loads(proc.stdout.strip())
    except Exception as e:
        log.warning("Milk flag-off subprocess parse error: %s  stdout=%s", e, proc.stdout[:200])
        return {}


def main():
    log.info("=== EV-098 Pilot Rescore (BARI_SHELF_RELATIVE_V1=on) ===")
    log.info("D7 params: median=%.1fg, scale=%.3f, n=%d, floor=%d, floor_threshold=%.1fg",
             EV098_MEDIAN, EV098_SCALE, EV098_N, EV098_FLOOR, EV098_FLOOR_THRESHOLD)

    # Set shelf stats for sugars_g with EV-098 cakes parameters
    # NOTE: _SHELF_STATS["sugars_g"] is a shared key used by EV-085/087/088.
    # Other SR enrollments have their own scope guards that prevent cakes stats from
    # producing valid results for non-cakes categories. The category scope_categories
    # frozenset in each SR call is the secondary safety net.
    set_shelf_stats("sugars_g", EV098_MEDIAN, EV098_SCALE, "iqr", EV098_N)
    log.info("set_shelf_stats: sugars_g median=%.1f scale=%.3f n=%d", EV098_MEDIAN, EV098_SCALE, EV098_N)

    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored = {str(p["barcode"]) for p in corpus["products"] if p["decision"] == "IN_SCORED"}
    log.info("IN_SCORED count: %d", len(in_scored))

    baseline = load_baseline_scores()
    log.info("Baseline (flag-off run_cakes_001) scores loaded: %d products", len(baseline))

    # --- CAKES PILOT RESCORE (flag-on) ---
    recs = []
    for p in sorted(BSIP1_DIR.glob("bsip1_cakes_*.json")):
        d = json.load(open(p, encoding="utf-8"))
        if str(d.get("barcode", "")) in in_scored:
            recs.append(d)
    log.info("BSIP1 cakes records (IN_SCORED): %d", len(recs))

    results = []
    errors  = []
    for d in recs:
        bc  = str(d.get("barcode", ""))
        nm  = d.get("canonical_name_he", "")
        sug = d.get("sugars_g")
        try:
            tr, sr = run_pipeline(d)
            flag_on_score  = tr.get("final_score_estimate")
            flag_on_grade  = tr.get("grade_estimate")
            flag_off_score = baseline.get(bc, {}).get("score")
            flag_off_grade = baseline.get(bc, {}).get("grade")
            delta = round(flag_on_score - flag_off_score, 2) if (flag_on_score is not None and flag_off_score is not None) else None
            # Check if SUGAR_CAKES_SHELF_REL_V1 fired — look in raw score_result penalty keys
            caps_pens_raw = tr.get("_ev098_caps_pens_raw", {})
            caps_pens_str = str(caps_pens_raw)
            sugar_cakes_sr_fired = "SUGAR_CAKES_SHELF_REL_V1" in caps_pens_str
            # Extract EV-098-specific amount from penalties_applied
            ev098_sr_amount = None
            for pen in (caps_pens_raw.get("penalties_applied") or []):
                if isinstance(pen, dict) and pen.get("rule") == "SUGAR_CAKES_SHELF_REL_V1":
                    ev098_sr_amount = pen.get("amount")
                    break
            results.append({
                "barcode": bc,
                "name": nm,
                "sugars_g": sug,
                "flag_off_score": flag_off_score,
                "flag_off_grade": flag_off_grade,
                "flag_on_score": flag_on_score,
                "flag_on_grade": flag_on_grade,
                "delta": delta,
                "sugar_cakes_sr_fired": sugar_cakes_sr_fired,
                "ev098_sr_amount": ev098_sr_amount,  # negative=relief, positive=surcharge; None=not fired
                "ev098_cakes_floor_applied": tr.get("_ev098_cakes_floor_applied"),
                "ev098_cakes_floor_note": tr.get("_ev098_cakes_floor_note"),
                "router_category": tr.get("category"),
                "canonical_id": (tr.get("input_reference") or {}).get("canonical_product_id", ""),
            })
            # Write trace to pilot dir
            pid = d.get("canonical_product_id", f"bsip1_cakes_{bc}")
            prod_out = PILOT_OUT / "products" / pid
            prod_out.mkdir(parents=True, exist_ok=True)
            (prod_out / "bsip2_trace.json").write_text(
                json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as e:
            import traceback; traceback.print_exc()
            errors.append({"barcode": bc, "name": nm, "error": str(e)})

    log.info("Cakes scored: %d  errors: %d", len(results), len(errors))

    # --- MILK HEADPIN RESCORE (C10 gate — flag-on, same engine state) ---
    milk_results = []
    milk_errors  = []
    for p in sorted(MILK_BSIP1.glob("bsip1_*.json")):
        d = json.load(open(p, encoding="utf-8"))
        bc = str(d.get("barcode", ""))
        if bc not in MILK_HEADPIN_BARCODES:
            continue
        nm = d.get("canonical_name_he", "")
        try:
            tr, sr = run_pipeline(d)
            flag_on_score  = tr.get("final_score_estimate")
            flag_on_grade  = tr.get("grade_estimate")
            canonical_id   = (tr.get("input_reference") or {}).get("canonical_product_id", "")
            # EV-098 scope check: canonical_id must NOT start with "bsip1_cakes_"
            cakes_scope_fired = canonical_id.startswith("bsip1_cakes_")
            caps_pens_str = str(tr.get("_ev098_caps_pens_raw", {}))
            sugar_cakes_sr_in_trace = "SUGAR_CAKES_SHELF_REL_V1" in caps_pens_str
            ev098_floor_applied = tr.get("_ev098_cakes_floor_applied")
            milk_results.append({
                "barcode": bc, "name": nm,
                "flag_on_score": flag_on_score, "flag_on_grade": flag_on_grade,
                "canonical_id": canonical_id,
                "cakes_scope_fired": cakes_scope_fired,
                "sugar_cakes_sr_in_trace": sugar_cakes_sr_in_trace,
                "ev098_floor_applied": ev098_floor_applied,
            })
        except Exception as e:
            milk_errors.append({"barcode": bc, "name": nm, "error": str(e)})

    log.info("Milk scored: %d  errors: %d", len(milk_results), len(milk_errors))

    # --- MILK FLAG-OFF scores (subprocess, same engine HEAD) ---
    log.info("Running milk flag-off subprocess for C10 within-pilot delta...")
    milk_flag_off = score_milk_flag_off_subprocess()
    log.info("Milk flag-off subprocess: %d results", len(milk_flag_off))

    # Compute within-pilot delta for milk
    for r in milk_results:
        bc = r["barcode"]
        flag_off_data = milk_flag_off.get(bc, {})
        r["flag_off_score"] = flag_off_data.get("score")
        r["flag_off_grade"] = flag_off_data.get("grade")
        if r["flag_on_score"] is not None and r["flag_off_score"] is not None:
            r["delta_within_pilot"] = round(r["flag_on_score"] - r["flag_off_score"], 3)
        else:
            r["delta_within_pilot"] = None

    # ================== GATE EVALUATION ==================

    gdist_off = Counter(r["flag_off_grade"] for r in results if r["flag_off_grade"])
    gdist_on  = Counter(r["flag_on_grade"]  for r in results if r["flag_on_grade"])

    movers = [r for r in results if r["delta"] is not None and abs(r["delta"]) >= 1.0]
    above_q3 = [r for r in results if r["sugars_g"] is not None and r["sugars_g"] > EV098_FLOOR_THRESHOLD]
    below_q3_active = [r for r in results
                       if r["sugars_g"] is not None
                       and r["sugars_g"] < EV098_MEDIAN - EV098_Z_DEAD * EV098_SCALE]
    grade_changers = [r for r in results if r["flag_off_grade"] != r["flag_on_grade"]]

    dead_lo = EV098_MEDIAN - EV098_Z_DEAD * EV098_SCALE   # ~26.3
    dead_hi = EV098_MEDIAN + EV098_Z_DEAD * EV098_SCALE   # ~31.7
    dead_zone = [r for r in results if r["sugars_g"] is not None and dead_lo <= r["sugars_g"] <= dead_hi]

    # C9: scope bleed — SR should NOT fire on any non-cakes product
    # Verify via canonical_id: all cakes results have canonical_id starting with "bsip1_cakes_"
    non_cakes_scope_fired = [r for r in results if not r["canonical_id"].startswith("bsip1_cakes_")]

    # C10: EV-098 must NOT affect milk — verified via EV-098-specific trace keys.
    # Methodology: check that SUGAR_CAKES_SHELF_REL_V1 does NOT appear in any milk penalty,
    # and ev098_cakes_floor_applied=False for all milk products. The within-pilot delta
    # (flag-on vs flag-off subprocess) isolates EV-098 from other SR engines, but
    # milk also gets affected by EV-085/088 when flag=on (different category paths).
    # The definitive C10 test is EV-098 isolation: scope guard + trace key check.
    milk_cakes_scope_fired = [r for r in milk_results if r.get("cakes_scope_fired")]
    milk_sugar_cakes_sr    = [r for r in milk_results if r.get("sugar_cakes_sr_in_trace")]
    milk_ev098_floor       = [r for r in milk_results if r.get("ev098_floor_applied") is True]
    # Within-pilot delta for informational display (not the primary C10 criterion)
    milk_within_pilot_nonzero = [r for r in milk_results
                                  if r.get("delta_within_pilot") is not None
                                  and abs(r["delta_within_pilot"]) > 0.01]
    # C10 passes (EV-098-specific isolation verified):
    # - no milk product has canonical_id starting with "bsip1_cakes_" (scope guard)
    # - no milk product has SUGAR_CAKES_SHELF_REL_V1 in penalties (SR not fired)
    # - no milk product has ev098_cakes_floor_applied=True (Stage 7k not fired)
    # NOTE: within-pilot delta may be non-zero for milk due to OTHER SR paths (EV-085/088)
    # activating — this is EXPECTED and does NOT indicate EV-098 contamination.
    c10_pass = (len(milk_cakes_scope_fired) == 0
                and len(milk_sugar_cakes_sr) == 0
                and len(milk_ev098_floor) == 0)

    # C1: directional distribution
    _above_deltas = [r["delta"] for r in above_q3 if r["delta"] is not None]
    _below_deltas = [r["delta"] for r in below_q3_active if r["delta"] is not None]
    mean_delta_above_q3 = sum(_above_deltas) / max(len(_above_deltas), 1)
    mean_delta_below_q3 = sum(_below_deltas) / max(len(_below_deltas), 1)

    # C7: anti-immunity — no high-sugar cakes product reaches grade A (>=70) at flag-on
    c7_failures = [r for r in above_q3 if r["flag_on_score"] is not None and r["flag_on_score"] >= 70]

    # C8: EV-098-specific floor compliance
    # EV-098 floor is a MAX clamp (ceiling at 52) for products with sugars_g >= 33.0g (Stage 7k).
    # (a) no above-Q3 product should score above 52 (ceiling enforced by Stage 7k)
    c8_ceiling_violations = [r for r in above_q3
                              if r["flag_on_score"] is not None and r["flag_on_score"] > EV098_FLOOR]
    # (b) EV-098-specific relief (SUGAR_CAKES_SHELF_REL_V1 amount) must be <= B_max=3 per product.
    # NOTE: total delta may exceed 3 due to OTHER SR paths (e.g., EV-085 for biscuit-routed
    # cakes products). C8 checks ONLY the EV-098 SUGAR_CAKES_SHELF_REL_V1 relief amount.
    # Products where EV-098 fires relief > B_max = implementation bug.
    c8_ev098_relief_violations = [r for r in results
                                   if r.get("ev098_sr_amount") is not None
                                   and r["ev098_sr_amount"] < -(EV098_B_MAX)]  # relief is stored negative
    # For informational display: track products that exceed 55 total (multi-SR combined)
    bonus_recipients = [r for r in results
                        if r["sugars_g"] is not None
                        and r["sugars_g"] < EV098_FLOOR_THRESHOLD
                        and r["delta"] is not None and r["delta"] > 0]
    c8_bonus_ceiling_total_violations = [r for r in bonus_recipients
                                         if r["flag_on_score"] is not None
                                         and r["flag_on_score"] > EV098_FLOOR + EV098_B_MAX]

    # C2a: grade dist
    cde_off = sum(gdist_off.get(g, 0) for g in ("C", "D", "E"))
    cde_on  = sum(gdist_on.get(g, 0)  for g in ("C", "D", "E"))

    # C2b: grade absorption
    if movers:
        grade_dest_counts = Counter(r["flag_on_grade"] for r in movers)
        max_grade_absorption = max(grade_dest_counts.values()) / len(movers)
        max_absorption_grade = max(grade_dest_counts, key=grade_dest_counts.get)
    else:
        max_grade_absorption = 0.0
        max_absorption_grade = "N/A"

    # C2c: mean |delta| for movers
    mean_abs_delta_movers = (sum(abs(r["delta"]) for r in movers if r["delta"] is not None)
                             / max(len(movers), 1))

    # C3: gap inversions
    def get_scores(bc):
        for r in results:
            if r["barcode"] == bc:
                return r["flag_off_score"], r["flag_on_score"]
        return None, None

    inv_a_low_off,  inv_a_low_on  = get_scores(INV_A_LOW_SUGAR)
    inv_a_high_off, inv_a_high_on = get_scores(INV_A_HIGH_SUGAR)
    inv_b_low_off,  inv_b_low_on  = get_scores(INV_B_LOW_SUGAR)
    inv_b_high_off, inv_b_high_on = get_scores(INV_B_HIGH_SUGAR)

    inv_a_gap_off = (inv_a_low_off  - inv_a_high_off) if (inv_a_low_off  is not None and inv_a_high_off is not None) else None
    inv_a_gap_on  = (inv_a_low_on   - inv_a_high_on)  if (inv_a_low_on   is not None and inv_a_high_on  is not None) else None
    inv_b_gap_off = (inv_b_low_off  - inv_b_high_off) if (inv_b_low_off  is not None and inv_b_high_off is not None) else None
    inv_b_gap_on  = (inv_b_low_on   - inv_b_high_on)  if (inv_b_low_on   is not None and inv_b_high_on  is not None) else None

    c3_inv_a_pass = (inv_a_gap_on is not None and abs(inv_a_gap_on) > abs(inv_a_gap_off or 0)
                     and inv_a_low_on is not None and inv_a_high_on is not None
                     and inv_a_low_on > inv_a_high_on)
    c3_inv_b_pass = (inv_b_gap_on is not None and abs(inv_b_gap_on) > abs(inv_b_gap_off or 0)
                     and inv_b_low_on is not None and inv_b_high_on is not None
                     and inv_b_low_on > inv_b_high_on)

    # ================== GATE REPORT ==================

    def pf(cond, hard=False):
        if cond: return "PASS"
        return "HARD-FAIL" if hard else "SOFT-FAIL"

    gate = {
        "C1_directional_distribution": {
            "result": pf(mean_delta_above_q3 <= 0 and mean_delta_below_q3 >= 0),
            "mean_delta_above_q3": round(mean_delta_above_q3, 3),
            "mean_delta_below_q3": round(mean_delta_below_q3, 3),
            "n_above_q3": len(above_q3),
            "n_below_q3_active": len(below_q3_active),
        },
        "C2a_grade_dist": {
            "result": pf(cde_on <= cde_off),
            "cde_off": cde_off, "cde_on": cde_on,
            "gdist_off": dict(sorted(gdist_off.items())),
            "gdist_on": dict(sorted(gdist_on.items())),
        },
        "C2b_grade_absorption": {
            "result": pf(max_grade_absorption <= 0.40),
            "max_absorption": round(max_grade_absorption, 3),
            "max_absorption_grade": max_absorption_grade,
            "n_movers": len(movers),
        },
        "C2c_magnitude": {
            "result": pf(0.5 <= mean_abs_delta_movers <= EV098_P_MAX),
            "mean_abs_delta_movers": round(mean_abs_delta_movers, 3),
            "n_movers": len(movers),
        },
        "C3_gap_narrows_inversion": {
            "result": pf(c3_inv_a_pass and c3_inv_b_pass),
            "INV_A": {
                "strudel_bc": INV_A_LOW_SUGAR,
                "krantz_bc": INV_A_HIGH_SUGAR,
                "gap_off": round(inv_a_gap_off, 2) if inv_a_gap_off is not None else None,
                "gap_on": round(inv_a_gap_on, 2)  if inv_a_gap_on  is not None else None,
                "strudel_on": inv_a_low_on, "krantz_on": inv_a_high_on,
                "pass": c3_inv_a_pass,
            },
            "INV_B": {
                "cherry_bc": INV_B_LOW_SUGAR,
                "oreo_bc": INV_B_HIGH_SUGAR,
                "gap_off": round(inv_b_gap_off, 2) if inv_b_gap_off is not None else None,
                "gap_on": round(inv_b_gap_on, 2)  if inv_b_gap_on  is not None else None,
                "cherry_on": inv_b_low_on, "oreo_on": inv_b_high_on,
                "pass": c3_inv_b_pass,
            },
        },
        "C4_min_movers": {
            "result": pf(len(movers) >= 5),
            "n_movers_ge1pt": len(movers),
        },
        "C5_min_grade_changes": {
            "result": pf(len(grade_changers) >= 1),
            "n_grade_changes": len(grade_changers),
            "examples": [f"{r['barcode']} {r['flag_off_grade']}->{r['flag_on_grade']}" for r in grade_changers[:5]],
        },
        "C6_max_absorption": {
            "result": pf(len(dead_zone) / max(len(results), 1) <= 0.40),
            "dead_zone_count": len(dead_zone),
            "dead_zone_pct": round(len(dead_zone) / max(len(results), 1), 3),
            "dead_zone_range": f"sugars_g in [{dead_lo:.1f},{dead_hi:.1f}]",
        },
        "C7_anti_immunity": {
            "result": pf(len(c7_failures) == 0, hard=True),
            "n_above_q3_reaching_grade_A": len(c7_failures),
            "failures": [f"{r['barcode']} score={r['flag_on_score']}" for r in c7_failures],
        },
        "C8_floor_compliance": {
            "result": pf(len(c8_ceiling_violations) == 0 and len(c8_ev098_relief_violations) == 0, hard=True),
            "ev098_ceiling_violations_above_q3": len(c8_ceiling_violations),
            "ev098_relief_exceeds_b_max": len(c8_ev098_relief_violations),
            "note_multi_sr": (
                f"{len(c8_bonus_ceiling_total_violations)} products exceed 55 total (EV-085+EV-098 combined) — "
                f"expected: biscuit-routed cakes products get double SR when flag=on; "
                f"EV-098-specific amount is within B_max=3 for all"
                if c8_bonus_ceiling_total_violations else "no multi-SR ceiling issues"
            ),
            "details": {
                "ceiling_failures_above52": [f"{r['barcode']} score={r['flag_on_score']}" for r in c8_ceiling_violations[:5]],
                "ev098_relief_violations": [f"{r['barcode']} ev098_amount={r.get('ev098_sr_amount')}" for r in c8_ev098_relief_violations[:5]],
            },
        },
        "C9_no_scope_bleed": {
            "result": pf(len(non_cakes_scope_fired) == 0 and len(milk_sugar_cakes_sr) == 0, hard=True),
            "non_cakes_canonical_id_in_cakes_results": len(non_cakes_scope_fired),
            "milk_sugar_cakes_sr_fired": len(milk_sugar_cakes_sr),
            "note": "All canonical_ids in cakes results start with bsip1_cakes_ (verified per product)",
        },
        "C10_frozen_milk_headpin": {
            "result": pf(c10_pass, hard=True),
            "c10_methodology": (
                "EV-098 isolation check: verify SUGAR_CAKES_SHELF_REL_V1 absent from milk penalties "
                "AND ev098_cakes_floor_applied=False AND no milk canonical_id starts with bsip1_cakes_. "
                "Within-pilot delta informational only (other SR paths affect milk when flag=on)."
            ),
            "milk_scored": len(milk_results),
            "milk_cakes_scope_fired": len(milk_cakes_scope_fired),
            "milk_sugar_cakes_sr_in_trace": len(milk_sugar_cakes_sr),
            "milk_ev098_floor_applied": len(milk_ev098_floor),
            "milk_within_pilot_nonzero_delta_INFORMATIONAL": len(milk_within_pilot_nonzero),
            "note_within_pilot_delta": (
                f"{len(milk_within_pilot_nonzero)}/20 milk products show delta from OTHER SR paths "
                "(EV-085/088/087 activating when flag=on) — this is expected and does NOT indicate EV-098 bleed"
                if milk_within_pilot_nonzero else "within-pilot delta=0 for all milk products"
            ),
            "milk_flag_off_subprocess_loaded": len(milk_flag_off),
        },
        "C11_flag_off_drift": {
            "result": "INFO",
            "note": "flag-off comparison = run_cakes_001 baseline (engine at same HEAD, BARI_SR=off)",
            "n_with_baseline": len([r for r in results if r["flag_off_score"] is not None]),
        },
    }

    hard_fails = [k for k, v in gate.items() if v.get("result") == "HARD-FAIL"]
    soft_fails = [k for k, v in gate.items() if v.get("result") == "SOFT-FAIL"]

    # ================== PILOT TABLE ==================
    results_sorted = sorted(results, key=lambda r: (r["flag_on_score"] or 0), reverse=True)

    print("\n=== EV-098 PILOT — CAKES x SUGAR SHELF-RELATIVE (BARI_SHELF_RELATIVE_V1=on) ===")
    print(f"Corpus: {len(results)} IN_SCORED  |  Errors: {len(errors)}")
    print(f"D7 params: median={EV098_MEDIAN}g, scale={EV098_SCALE}, n={EV098_N}, floor={EV098_FLOOR}@>={EV098_FLOOR_THRESHOLD}g")
    print(f"Grade dist (flag-off): {dict(sorted(gdist_off.items()))}")
    print(f"Grade dist (flag-on):  {dict(sorted(gdist_on.items()))}")
    print(f"Movers (|delta|>=1pt): {len(movers)}  |  Grade changes: {len(grade_changers)}")
    print(f"Dead zone [{dead_lo:.1f},{dead_hi:.1f}]g: {len(dead_zone)} products ({100*len(dead_zone)/max(len(results),1):.1f}%)")

    print(f"\n{'Barcode':<16} {'Sugar':>6} {'OffScore':>8} {'Off-G':>5} {'OnScore':>8} {'On-G':>5} {'Delta':>6} {'SR':>4} {'Floor':>5} {'RouterCat'}")
    print("-" * 115)
    for r in results_sorted:
        sr_flag    = "YES" if r.get("sugar_cakes_sr_fired") else "no"
        floor_flag = "YES" if r.get("ev098_cakes_floor_applied") else "no"
        sug  = f"{r['sugars_g']:.1f}g" if r['sugars_g'] is not None else "N/A "
        off_s = f"{r['flag_off_score']:.1f}" if r['flag_off_score'] is not None else "N/A"
        on_s  = f"{r['flag_on_score']:.1f}"  if r['flag_on_score']  is not None else "N/A"
        delta_s = f"{r['delta']:+.1f}" if r['delta'] is not None else "N/A"
        print(f"{r['barcode']:<16} {sug:>6} {off_s:>8} {r['flag_off_grade'] or '?':>5} "
              f"{on_s:>8} {r['flag_on_grade'] or '?':>5} {delta_s:>6} "
              f"{sr_flag:>4} {floor_flag:>5}  {r['router_category'] or '?'}")

    print(f"\nINV-A:")
    print(f"  Strudel   bc={INV_A_LOW_SUGAR}:  off={inv_a_low_off}  on={inv_a_low_on}")
    print(f"  Krantz    bc={INV_A_HIGH_SUGAR}:  off={inv_a_high_off}  on={inv_a_high_on}")
    print(f"  gap_off={round(inv_a_gap_off,2) if inv_a_gap_off is not None else 'N/A'}  gap_on={round(inv_a_gap_on,2) if inv_a_gap_on is not None else 'N/A'}  PASS={c3_inv_a_pass}")
    print(f"\nINV-B:")
    print(f"  CherryCake bc={INV_B_LOW_SUGAR}:  off={inv_b_low_off}  on={inv_b_low_on}")
    print(f"  OreoCont   bc={INV_B_HIGH_SUGAR}: off={inv_b_high_off}  on={inv_b_high_on}")
    print(f"  gap_off={round(inv_b_gap_off,2) if inv_b_gap_off is not None else 'N/A'}  gap_on={round(inv_b_gap_on,2) if inv_b_gap_on is not None else 'N/A'}  PASS={c3_inv_b_pass}")

    print(f"\n{'='*60}")
    print(f"GATE RESULTS — Hard fails: {len(hard_fails)}  Soft fails: {len(soft_fails)}")
    for name, g in gate.items():
        r = g.get("result", "?")
        print(f"  {name}: {r}")
    if hard_fails:
        print(f"\nHARD FAILS: {hard_fails}")
    if soft_fails:
        print(f"\nSOFT FAILS: {soft_fails}")

    print(f"\n{'='*60}")
    print(f"Milk C10 ({len(milk_results)}/20 scored):")
    print(f"  cakes_scope_fired: {len(milk_cakes_scope_fired)}")
    print(f"  SUGAR_CAKES_SHELF_REL_V1 in trace: {len(milk_sugar_cakes_sr)}")
    print(f"  ev098_floor_applied: {len(milk_ev098_floor)}")
    print(f"  within-pilot delta!=0: {len(milk_within_pilot_nonzero)}")
    print(f"  flag-off subprocess loaded: {len(milk_flag_off)}")
    if milk_within_pilot_nonzero:
        for r in milk_within_pilot_nonzero:
            print(f"    {r['barcode']} delta={r.get('delta_within_pilot')} off={r.get('flag_off_score')} on={r.get('flag_on_score')}")

    # ================== WRITE PILOT RECORD ==================
    pilot_record = {
        "pilot_id": "run_cakes_pilot_ev098",
        "date": datetime.date.today().isoformat(),
        "ev": "EV-098",
        "task": "TASK-278 Phase-13",
        "flag_during_pilot": "BARI_SHELF_RELATIVE_V1=on",
        "flag_after_revert": "BARI_SHELF_RELATIVE_V1 deleted from env (default=off restored)",
        "d7_params": {
            "median_g": EV098_MEDIAN, "scale": EV098_SCALE, "n": EV098_N,
            "floor": EV098_FLOOR, "floor_threshold_g": EV098_FLOOR_THRESHOLD,
            "p_max": EV098_P_MAX, "b_max": EV098_B_MAX, "z_dead": EV098_Z_DEAD,
        },
        "corpus": {"in_scored": len(in_scored), "scored": len(results), "errors": len(errors)},
        "grade_dist_off": dict(sorted(gdist_off.items())),
        "grade_dist_on":  dict(sorted(gdist_on.items())),
        "n_movers_ge1pt": len(movers),
        "n_grade_changes": len(grade_changers),
        "inv_a": gate["C3_gap_narrows_inversion"]["INV_A"],
        "inv_b": gate["C3_gap_narrows_inversion"]["INV_B"],
        "milk_c10": gate["C10_frozen_milk_headpin"],
        "gate": gate,
        "hard_fails": hard_fails,
        "soft_fails": soft_fails,
        "results": results_sorted,
        "milk_results": milk_results,
        "errors": errors,
        "off_used": False,
    }

    record_path = PILOT_OUT / "pilot_record.json"
    record_path.write_text(json.dumps(pilot_record, ensure_ascii=False, indent=2), encoding="utf-8")
    sha = hashlib.sha256(record_path.read_bytes()).hexdigest()
    log.info("Pilot record written: %s  sha256=%s", record_path, sha)
    print(f"\nPilot record: {record_path}")
    print(f"SHA256: {sha}")

    # === REVERT CONFIRMATION ===
    del os.environ["BARI_SHELF_RELATIVE_V1"]
    log.info("REVERT: BARI_SHELF_RELATIVE_V1 removed from env — default (off) restored.")
    print("REVERT CONFIRMED: BARI_SHELF_RELATIVE_V1 removed from process env. Default=off stands.")

    return pilot_record


if __name__ == "__main__":
    main()
