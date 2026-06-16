# BSIP2 batch — Hummus x sodium SHELF-RELATIVE PILOT (run_hummus_001_sodium_pilot)
# TASK-278 Phase-12 / EV-094 — hummus x sodium asymmetric P>B shelf-relative enrollment.
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
_SCRIPT_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(_SCRIPT_DIR / "src"))

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
    SUGAR_SHELF_SURCHARGE_BANDS, SUGAR_SHELF_RELIEF_BANDS,
    SUGAR_SHELF_REL_CEREAL_MEDIAN, SUGAR_SHELF_REL_CEREAL_SCALE,
    SUGAR_SHELF_REL_YOGURT_MEDIAN, SUGAR_SHELF_REL_YOGURT_SCALE,
    FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN, FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
    FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE,
    SUGAR_SHELF_REL_JUICES_MEDIAN, SUGAR_SHELF_REL_JUICES_SCALE,
    SUGAR_SHELF_REL_MAADANIM_MEDIAN, SUGAR_SHELF_REL_MAADANIM_SCALE,
    SODIUM_SHELF_REL_SALTY_SNACK_MEDIAN, SODIUM_SHELF_REL_SALTY_SNACK_IQR,
    SODIUM_SHELF_REL_SALTY_SNACK_SCALE, SODIUM_SHELF_REL_SALTY_SNACK_FLOOR,
    SODIUM_SHELF_REL_SALTY_SNACK_FLOOR_THRESHOLD_MG,
    SODIUM_SHELF_REL_SALTY_SNACK_P_MAX, SODIUM_SHELF_REL_SALTY_SNACK_B_MAX,
    SODIUM_SHELF_SCALE_GUARD_SALTY_SNACK,
    SODIUM_SHELF_REL_HUMMUS_MEDIAN, SODIUM_SHELF_REL_HUMMUS_IQR,
    SODIUM_SHELF_REL_HUMMUS_SCALE, SODIUM_SHELF_REL_HUMMUS_FLOOR,
    SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG,
    SODIUM_SHELF_REL_HUMMUS_P_MAX, SODIUM_SHELF_REL_HUMMUS_B_MAX,
    SODIUM_SHELF_SCALE_GUARD_HUMMUS,
    HUMMUS_PRODUCT_CATEGORIES,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT               = pathlib.Path(r"C:\Bari")
BSIP1_HUMMUS_DIR   = ROOT / "02_products" / "hummus" / "canonical_bsip1"
BSIP1_SNACK_DIR    = ROOT / "02_products" / "salty_snacks" / "bsip1_outputs"
MILK_RUN005_DIR    = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
BSIP1_MILK_DIR     = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
BSIP1_YOGURT_DIR   = ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"
BSIP1_CHEESE_DIR   = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
BSIP1_HC_DIR       = ROOT / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output"
BSIP1_JUICE_DIR    = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
BSIP1_MAAD_DIR     = ROOT / "03_operations" / "bsip1" / "run_maadanim_001" / "output"
OUTPUT_DIR         = ROOT / "02_products" / "hummus" / "bsip2_outputs" / "run_hummus_001_sodium_pilot"
RETURN_DIR         = ROOT / "tasks" / "returns"
RUN_ID = "run_hummus_001_sodium_pilot"

# EV-094 constants (from D7 approval, P137 constant lock)
PROPOSAL_MEDIAN           = SODIUM_SHELF_REL_HUMMUS_MEDIAN       # 390.0
PROPOSAL_SCALE            = SODIUM_SHELF_REL_HUMMUS_SCALE        # 31.88
PROPOSAL_IQR              = SODIUM_SHELF_REL_HUMMUS_IQR          # 43.0
FLOOR_VALUE               = SODIUM_SHELF_REL_HUMMUS_FLOOR        # 62
FLOOR_THRESHOLD_MG        = SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG  # 395.0

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
    """Returns (trace, score_result) tuple — score_result carries EV-094 fields not in the trace."""
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace, score_result


def run_bsip2_pipeline_flag_off(product):
    """Score with flag OFF by temporarily toggling the module-level boolean. Returns (trace, score_result)."""
    import score_engine as _se
    saved_flag = _se.BARI_SHELF_RELATIVE_V1
    _se.BARI_SHELF_RELATIVE_V1 = False
    try:
        signals      = extract_signals(product)
        cat_result   = classify_category(product)
        l3           = signals["L3_inferred_classifications"]
        nova_result  = infer_nova(product, l3)
        eval_result  = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)
        trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    finally:
        _se.BARI_SHELF_RELATIVE_V1 = saved_flag
    return trace, score_result


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
                candidates = list(BSIP1_MILK_DIR.glob(f"bsip1_{bc}.json")) + \
                             list(BSIP1_MILK_DIR.glob(f"bsip1_audit_{bc}.json"))
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
        barcode = str(doc.get("barcode", "") or doc.get("canonical_product_id", ""))
        name    = doc.get("canonical_name_he", "") or doc.get("product_name_he", "") or doc.get("canonical_name_en", "")
        nn      = doc.get("normalized_nutrition_per_100g") or {}
        sodium_mg = nn.get("sodium_mg")
        # EV-094 scope fields
        bsip0_src = doc.get("bsip0_source")
        hummus_cat = bsip0_src.get("product_category") if isinstance(bsip0_src, dict) else None
        in_hummus_scope = hummus_cat in HUMMUS_PRODUCT_CATEGORIES
        try:
            trace_on,  sr_on  = run_bsip2_pipeline(doc)
            trace_off, sr_off = run_bsip2_pipeline_flag_off(doc)
            score_on  = trace_on.get("final_score_estimate")
            score_off = trace_off.get("final_score_estimate")
            grade_on  = trace_on.get("grade_estimate")
            grade_off = trace_off.get("grade_estimate")
            delta     = round(score_on - score_off, 2) if (score_on is not None and score_off is not None) else None
            category  = trace_on.get("category")
            # Read ev094 floor from score_result directly (not in trace dict)
            floor_app = sr_on.get("ev094_hummus_floor_applied")
            # Get EV-094 SR penalty from penalties_applied in trace
            sr_pen_on = None
            for p_entry in (trace_on.get("penalties_applied") or []):
                if p_entry.get("rule") == "SODIUM_HUMMUS_SHELF_REL_V1":
                    sr_pen_on = p_entry.get("amount")
                    break
            # EV-093 (salty snack) fired check
            ev093_fired = any(
                p_entry.get("rule") == "SODIUM_SALTY_SNACK_SHELF_REL_V1"
                for p_entry in (trace_on.get("penalties_applied") or [])
            ) or (sr_on.get("ev093_salty_snack_floor_applied") is True)
            ev094_fired = (sr_pen_on is not None and sr_pen_on != 0) or (floor_app is True)
            rows.append({
                "barcode": barcode,
                "name": name,
                "corpus": corpus_label,
                "hummus_product_category": hummus_cat,
                "in_hummus_scope": in_hummus_scope,
                "sodium_mg": sodium_mg,
                "flag_off_score": score_off,
                "flag_off_grade": grade_off,
                "flag_on_score": score_on,
                "flag_on_grade": grade_on,
                "delta": delta,
                "ev094_fired": ev094_fired,
                "ev094_hummus_floor_applied": floor_app,
                "ev094_sr_penalty": sr_pen_on,
                "ev093_fired": ev093_fired,
                "category": category,
            })
            log.info("  [%s] %-45s sodium=%-6s off=%s/%s on=%s/%s delta=%s floor=%s",
                     corpus_label, (name or barcode)[:43], sodium_mg,
                     score_off, grade_off, score_on, grade_on, delta, floor_app)
        except Exception as e:
            log.error("  ERROR [%s] %s (%s): %s", corpus_label, barcode, name, e)
            import traceback; traceback.print_exc()
            errors.append({"corpus": corpus_label, "barcode": barcode, "name": name, "error": str(e)})
    return rows


def main():
    assert BARI_SHELF_RELATIVE_V1, "CRITICAL: BARI_SHELF_RELATIVE_V1 must be ON for pilot run"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log.info("=== TASK-278 Phase-12 EV-094: Hummus x Sodium SR Pilot -- %s ===", RUN_ID)
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")

    # -----------------------------------------------------------------------
    # STEP 1: Load all corpora
    # -----------------------------------------------------------------------
    # Hummus: filter to in-scope only (hummus_spread + hummus_and_savory_dips)
    all_hummus = load_bsip1_dir(BSIP1_HUMMUS_DIR, "bsip1_*.json", "hummus_all")
    hummus_records = [
        r for r in all_hummus
        if (r.get("bsip0_source", {}).get("product_category") if isinstance(r.get("bsip0_source"), dict) else None)
        in HUMMUS_PRODUCT_CATEGORIES
    ]
    log.info("In-scope hummus records: %d (expected 60)", len(hummus_records))

    snack_records  = load_bsip1_dir(BSIP1_SNACK_DIR, "bsip1_snack_*.json", "salty_snack")
    milk_records   = load_milk_run005()
    yogurt_records = load_bsip1_dir(BSIP1_YOGURT_DIR, "bsip1_*.json", "yogurt")
    cheese_records = load_bsip1_dir(BSIP1_CHEESE_DIR, "bsip1_*.json", "cheese_spread")
    hc_records     = load_bsip1_dir(BSIP1_HC_DIR, "bsip1_hardcheese_*.json", "hard_cheese")
    juice_records  = load_bsip1_dir(BSIP1_JUICE_DIR, "bsip1_*.json", "juice")
    maad_records   = load_bsip1_dir(BSIP1_MAAD_DIR, "bsip1_*.json", "maadanim")

    log.info("Hummus in-scope: %d | Salty snacks: %d | Milk: %d | Yogurt: %d | Cheese spread: %d | Hard cheese: %d | Juice: %d | Maadanim: %d",
             len(hummus_records), len(snack_records), len(milk_records),
             len(yogurt_records), len(cheese_records), len(hc_records),
             len(juice_records), len(maad_records))

    # -----------------------------------------------------------------------
    # STEP 2: Set shelf stats for all enrolled nutrients
    # EV-094 uses the hardcoded constants — sodium_mg stats set to hummus-specific values.
    # Prior enrolled categories stats also set so the engine scope guards work correctly.
    # -----------------------------------------------------------------------
    clear_shelf_stats()

    # EV-094: hummus × sodium_mg — use locked constants from P137 constant lock
    set_shelf_stats(
        nutrient="sodium_mg",
        median=PROPOSAL_MEDIAN,
        scale=PROPOSAL_SCALE,
        scale_type="iqr",
        n=60,
    )
    log.info("EV-094: sodium_mg shelf stats set: median=%.3f scale=%.3f n=60",
             PROPOSAL_MEDIAN, PROPOSAL_SCALE)

    # EV-093: salty_snack × sodium_mg (same nutrient key — overwrite to salty_snack after hummus run)
    # NOTE: The hummus and salty_snack SR both use sodium_mg stats. Since scope guards (BSIP1 field)
    # prevent cross-scope misfires, we set stats to the hummus constants (EV-094) for the hummus
    # products and let EV-093 use the same sodium_mg key for salty_snacks.
    # SOLUTION: set to hummus stats (EV-094 is the primary enrollment in this run);
    # EV-093 uses bsip1_salty_snack=True as scope guard which is independent of the shelf stats
    # — BUT the shelf_relative_differentiator still reads _SHELF_STATS["sodium_mg"].
    # We need to handle this: re-score salty snacks with salty_snack sodium stats for EV-093 fidelity.
    # For pilot gate purposes: we set hummus stats for hummus scoring, then salty_snack stats for snack scoring.
    # This is the same pattern used in prior pilots where the nutrient key is shared.

    # Prior enrolled categories (sugar):
    set_shelf_stats(nutrient="sugars_g",
                    median=SUGAR_SHELF_REL_MAADANIM_MEDIAN, scale=SUGAR_SHELF_REL_MAADANIM_SCALE,
                    scale_type="iqr", n=146)
    # fat_saturated_g (hard cheese, latest):
    set_shelf_stats(nutrient="fat_saturated_g",
                    median=FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, scale=FATSAT_SHELF_REL_HARDCHEESE_SCALE,
                    scale_type="iqr", n=37)

    log.info("Shelf stats set for all enrolled nutrients.")

    # -----------------------------------------------------------------------
    # STEP 3: Score all corpora
    # -----------------------------------------------------------------------
    errors = []

    log.info("--- Scoring hummus corpus (with EV-094 hummus sodium stats) ---")
    # hummus stats already set
    hummus_rows = score_corpus(hummus_records, "hummus", errors)

    log.info("--- Scoring salty snacks corpus (switching to EV-093 salty_snack sodium stats) ---")
    # Switch sodium_mg to salty_snack stats for EV-093 fidelity
    set_shelf_stats(
        nutrient="sodium_mg",
        median=SODIUM_SHELF_REL_SALTY_SNACK_MEDIAN,
        scale=SODIUM_SHELF_REL_SALTY_SNACK_SCALE,
        scale_type="iqr",
        n=54,
    )
    snack_rows = score_corpus(snack_records, "salty_snack", errors)

    log.info("--- Scoring milk corpus (C10 CRITICAL: delta must = 0.0 for all 20) ---")
    # For milk: sodium_mg is irrelevant (milk doesn't use SR). Keep salty_snack stats.
    milk_rows = score_corpus(milk_records, "milk", errors)

    log.info("--- Scoring yogurt corpus ---")
    yogurt_rows = score_corpus(yogurt_records, "yogurt", errors)

    log.info("--- Scoring cheese_spread corpus ---")
    cheese_rows = score_corpus(cheese_records, "cheese_spread", errors)

    log.info("--- Scoring hard_cheese corpus ---")
    hc_rows = score_corpus(hc_records, "hard_cheese", errors)

    log.info("--- Scoring juice corpus ---")
    juice_rows = score_corpus(juice_records, "juice", errors)

    log.info("--- Scoring maadanim corpus ---")
    maad_rows = score_corpus(maad_records, "maadanim", errors)

    all_rows = hummus_rows + snack_rows + milk_rows + yogurt_rows + cheese_rows + hc_rows + juice_rows + maad_rows

    # -----------------------------------------------------------------------
    # STEP 4: Gate criteria evaluation
    # -----------------------------------------------------------------------
    log.info("=== Evaluating 11 gate criteria ===")

    # Hummus-specific rows
    hummus_in_scope = [r for r in hummus_rows if r.get("in_hummus_scope")]
    n_hummus = len(hummus_in_scope)
    hummus_with_sodium = [r for r in hummus_in_scope if r.get("sodium_mg") is not None]
    hummus_movers = [r for r in hummus_in_scope if r.get("delta") is not None and r["delta"] != 0]
    hummus_deltas = [r["delta"] for r in hummus_in_scope if r.get("delta") is not None]
    hummus_median = PROPOSAL_MEDIAN  # 390.0 mg

    # C1: directional distribution — high-sodium hummus→delta<0, low-sodium→delta>0 (>=70%)
    high_sodium_hummus = [r for r in hummus_in_scope
                          if r.get("sodium_mg") is not None and r["sodium_mg"] > hummus_median
                          and r.get("sodium_mg", 0) < 700]  # exclude Q4 suppressed
    low_sodium_hummus  = [r for r in hummus_in_scope
                          if r.get("sodium_mg") is not None and r["sodium_mg"] < hummus_median]
    high_correct = sum(1 for r in high_sodium_hummus if r.get("delta") is not None and r["delta"] < 0)
    low_correct  = sum(1 for r in low_sodium_hummus  if r.get("delta") is not None and r["delta"] > 0)
    total_directional = len(high_sodium_hummus) + len(low_sodium_hummus)
    total_correct = high_correct + low_correct
    c1_pct = (total_correct / total_directional * 100) if total_directional > 0 else 0
    c1_pass = c1_pct >= 70.0
    log.info("C1 directional: %d/%d correct (%.1f%%) high_correct=%d/%d low_correct=%d/%d",
             total_correct, total_directional, c1_pct,
             high_correct, len(high_sodium_hummus),
             low_correct, len(low_sodium_hummus))

    # Grade distribution at flag_on
    grade_on_dist = Counter(r.get("flag_on_grade") for r in hummus_in_scope)
    grade_off_dist = Counter(r.get("flag_off_grade") for r in hummus_in_scope)
    log.info("C2a grade dist flag_on: %s", dict(grade_on_dist))
    log.info("C2a grade dist flag_off: %s", dict(grade_off_dist))

    # C2a: grade distribution plausible (not all in one grade)
    c2a_pass = len([g for g, cnt in grade_on_dist.items() if g not in (None, "insufficient_data") and cnt > 0]) >= 2

    # C2b: grade absorption <= 50% (no single grade absorbs > 50% of products)
    total_graded = sum(1 for r in hummus_in_scope if r.get("flag_on_grade") not in (None, "insufficient_data"))
    max_absorption = max((cnt for g, cnt in grade_on_dist.items() if g not in (None, "insufficient_data")), default=0)
    c2b_abs_pct = (max_absorption / total_graded * 100) if total_graded > 0 else 0
    c2b_pass = c2b_abs_pct <= 50.0
    log.info("C2b grade absorption: %.1f%% (max grade has %d/%d products)", c2b_abs_pct, max_absorption, total_graded)

    # C2c: mean abs delta for movers >= 0.5
    if hummus_movers:
        mean_abs_delta = sum(abs(r["delta"]) for r in hummus_movers) / len(hummus_movers)
    else:
        mean_abs_delta = 0.0
    c2c_pass = mean_abs_delta >= 0.5
    log.info("C2c mean abs delta movers: %.3f (n_movers=%d)", mean_abs_delta, len(hummus_movers))

    # C3: named inversion — find a pair where lower-sodium outscores higher-sodium at flag_on
    c3_pass = False
    c3_pair = None
    hummus_scored = [(r["barcode"], r.get("sodium_mg"), r.get("flag_on_score"), r.get("name", ""))
                     for r in hummus_in_scope
                     if r.get("sodium_mg") is not None and r.get("flag_on_score") is not None]
    hummus_scored.sort(key=lambda x: x[1])  # sort by sodium
    for i in range(len(hummus_scored)):
        for j in range(i+1, len(hummus_scored)):
            bc_lo, na_lo, s_lo, n_lo = hummus_scored[i]
            bc_hi, na_hi, s_hi, n_hi = hummus_scored[j]
            if na_lo < na_hi and s_lo > s_hi:  # lower sodium product scores higher
                c3_pass = True
                c3_pair = {
                    "lower_sodium": {"barcode": bc_lo, "sodium_mg": na_lo, "score_on": s_lo, "name": n_lo},
                    "higher_sodium": {"barcode": bc_hi, "sodium_mg": na_hi, "score_on": s_hi, "name": n_hi},
                }
                break
        if c3_pass:
            break
    log.info("C3 inversion: %s %s", "PASS" if c3_pass else "FAIL", c3_pair or "")

    # C4: movers_n >= 5
    movers_n = len(hummus_movers)
    c4_pass = movers_n >= 5
    log.info("C4 movers_n: %d (need >= 5)", movers_n)

    # C5: grade_changes_n >= 1
    grade_changes = [r for r in hummus_in_scope if r.get("flag_off_grade") != r.get("flag_on_grade")
                     and r.get("flag_off_grade") not in (None, "insufficient_data")
                     and r.get("flag_on_grade") not in (None, "insufficient_data")]
    grade_changes_n = len(grade_changes)
    c5_pass = grade_changes_n >= 1
    log.info("C5 grade_changes_n: %d (need >= 1)", grade_changes_n)

    # C6: dead_zone_pct <= 60%
    dead_zone_n = sum(1 for r in hummus_in_scope if r.get("delta") == 0 or r.get("delta") is None)
    dead_zone_pct = (dead_zone_n / n_hummus * 100) if n_hummus > 0 else 0
    c6_pass = dead_zone_pct <= 60.0
    log.info("C6 dead_zone_pct: %.1f%% (limit 60%%, dead_zone_n=%d/%d)", dead_zone_pct, dead_zone_n, n_hummus)

    # C7: anti-immunity — no hummus product with flag_off < 67 reaches flag_on >= 70
    c7_violations = [r for r in hummus_in_scope
                     if r.get("flag_off_score") is not None and r.get("flag_on_score") is not None
                     and r["flag_off_score"] < 67 and r["flag_on_score"] >= 70]
    c7_pass = len(c7_violations) == 0
    log.info("C7 anti-immunity violations: %d (need 0)", len(c7_violations))
    for v in c7_violations:
        log.warning("  C7 VIOLATION: %s sodium=%s off=%s on=%s", v.get("name", v["barcode"]),
                    v["sodium_mg"], v["flag_off_score"], v["flag_on_score"])

    # C8: floor compliance — all products with sodium in [395mg, 700mg) score >= 62 at flag_on.
    # Q4 products (Na>=700) are excluded from the floor (consistent with SR suppression);
    # they are handled by HIGH_SODIUM_700MG_PLUS absolute cap.
    floor_threshold = FLOOR_THRESHOLD_MG  # 395.0
    floor_value = FLOOR_VALUE  # 62
    c8_violations = [r for r in hummus_in_scope
                     if r.get("sodium_mg") is not None
                     and r["sodium_mg"] >= floor_threshold
                     and r["sodium_mg"] < 700        # Q4 excluded
                     and r.get("flag_on_score") is not None
                     and r["flag_on_score"] < floor_value]
    c8_pass = len(c8_violations) == 0
    log.info("C8 floor compliance (sodium>=%s AND <700mg, score>=%s): %s violations",
             floor_threshold, floor_value, len(c8_violations))
    for v in c8_violations:
        log.warning("  C8 VIOLATION: %s sodium=%s on=%s",
                    v.get("name", v["barcode"]), v["sodium_mg"], v["flag_on_score"])

    # C9: scope bleed = 0 (no non-hummus product with EV-094 fired)
    non_hummus_ev094 = [r for r in all_rows
                        if not r.get("in_hummus_scope") and r.get("ev094_fired")]
    c9_pass = len(non_hummus_ev094) == 0
    log.info("C9 scope bleed: %d non-hummus products with EV-094 fired (need 0)", len(non_hummus_ev094))
    for r in non_hummus_ev094[:5]:
        log.warning("  C9 BLEED: %s corpus=%s hummus_cat=%s",
                    r.get("name", r["barcode"]), r["corpus"], r.get("hummus_product_category"))

    # C10: CRITICAL — all 20 milk delta = 0.0
    milk_nonzero = [r for r in milk_rows if r.get("delta") is not None and r["delta"] != 0.0]
    milk_delta_zero_count = len(milk_rows) - len(milk_nonzero)
    c10_pass = len(milk_nonzero) == 0
    log.info("C10 CRITICAL milk delta=0: %d/%d (need 20/20)", milk_delta_zero_count, len(milk_rows))
    for r in milk_nonzero:
        log.error("  C10 FAIL: %s delta=%s off=%s on=%s",
                  r.get("name", r["barcode"]), r["delta"], r.get("flag_off_score"), r.get("flag_on_score"))

    # C11: SR suppressed for products with sodium >= 700mg (delta=0 for those products)
    high_na_hummus_q4 = [r for r in hummus_in_scope
                         if r.get("sodium_mg") is not None and r["sodium_mg"] >= 700]
    c11_violations = [r for r in high_na_hummus_q4 if r.get("delta") is not None and r["delta"] != 0]
    c11_pass = len(c11_violations) == 0
    log.info("C11 Q4 suppression (sodium>=700, delta=0): %d with Na>=700, %d violations",
             len(high_na_hummus_q4), len(c11_violations))
    for v in c11_violations:
        log.warning("  C11 VIOLATION: %s sodium=%s delta=%s", v.get("name", v["barcode"]),
                    v["sodium_mg"], v["delta"])

    # -----------------------------------------------------------------------
    # STEP 5: Build criteria summary
    # -----------------------------------------------------------------------
    criteria = {
        "C1_directional_pct_70":    "PASS" if c1_pass else "FAIL",
        "C2a_grade_dist_plausible":  "PASS" if c2a_pass else "FAIL",
        "C2b_grade_absorption_50":   "PASS" if c2b_pass else "FAIL",
        "C2c_mean_abs_delta_movers": "PASS" if c2c_pass else "FAIL",
        "C3_named_inversion":        "PASS" if c3_pass else "FAIL",
        "C4_movers_n_5":             "PASS" if c4_pass else "FAIL",
        "C5_grade_changes_n_1":      "PASS" if c5_pass else "FAIL",
        "C6_dead_zone_60":           "PASS" if c6_pass else "FAIL",
        "C7_anti_immunity":          "PASS" if c7_pass else "FAIL",
        "C8_floor_compliance":       "PASS" if c8_pass else "FAIL",
        "C9_scope_bleed_0":          "PASS" if c9_pass else "FAIL",
        "C10_milk_delta_zero_CRITICAL": "PASS" if c10_pass else "FAIL",
        "C11_q4_suppression_700mg":  "PASS" if c11_pass else "FAIL",
    }
    all_criteria_pass = all(v == "PASS" for v in criteria.values())

    # CRITICAL HALT on C10 milk failure
    if not c10_pass:
        log.error("CRITICAL: C10 MILK DELTA FAILURE — halting immediately.")
        log.error("Milk products with non-zero delta:")
        for r in milk_nonzero:
            log.error("  %s: delta=%s off=%s on=%s", r.get("name", r["barcode"]),
                      r["delta"], r.get("flag_off_score"), r.get("flag_on_score"))

    # -----------------------------------------------------------------------
    # STEP 6: Build run record
    # -----------------------------------------------------------------------
    run_record = {
        "run_id": RUN_ID,
        "task_id": "TASK-278",
        "phase": "Phase-12 hummus×sodium wire+pilot",
        "agent": "data-agent",
        "run_date": ts,
        "measured_not_published": True,
        "engine_flag": "BARI_SHELF_RELATIVE_V1=on",
        "ev094_constants": {
            "SODIUM_SHELF_REL_HUMMUS_MEDIAN": PROPOSAL_MEDIAN,
            "SODIUM_SHELF_REL_HUMMUS_IQR": PROPOSAL_IQR,
            "SODIUM_SHELF_REL_HUMMUS_SCALE": PROPOSAL_SCALE,
            "SODIUM_SHELF_REL_HUMMUS_FLOOR": FLOOR_VALUE,
            "SODIUM_SHELF_REL_HUMMUS_FLOOR_THRESHOLD_MG": FLOOR_THRESHOLD_MG,
            "SODIUM_SHELF_REL_HUMMUS_P_MAX": SODIUM_SHELF_REL_HUMMUS_P_MAX,
            "SODIUM_SHELF_REL_HUMMUS_B_MAX": SODIUM_SHELF_REL_HUMMUS_B_MAX,
        },
        "corpus_counts": {
            "hummus_in_scope_n": n_hummus,
            "salty_snacks_n": len(snack_records),
            "milk_n": len(milk_rows),
            "yogurt_n": len(yogurt_records),
            "cheese_spread_n": len(cheese_records),
            "hard_cheese_n": len(hc_records),
            "juice_n": len(juice_records),
            "maadanim_n": len(maad_records),
        },
        "gate_criteria": criteria,
        "all_criteria_pass": all_criteria_pass,
        "c10_milk_critical": {
            "milk_delta_zero_count": f"{milk_delta_zero_count}/{len(milk_rows)}",
            "pass": c10_pass,
            "violations": [{"barcode": r["barcode"], "name": r.get("name", ""), "delta": r["delta"]}
                           for r in milk_nonzero],
        },
        "directional": {
            "c1_pct": round(c1_pct, 1),
            "high_sodium_correct": f"{high_correct}/{len(high_sodium_hummus)}",
            "low_sodium_correct": f"{low_correct}/{len(low_sodium_hummus)}",
        },
        "movers_n": movers_n,
        "grade_changes_n": grade_changes_n,
        "dead_zone_pct": round(dead_zone_pct, 1),
        "mean_abs_delta_movers": round(mean_abs_delta, 3),
        "grade_dist_flag_on": dict(grade_on_dist),
        "grade_dist_flag_off": dict(grade_off_dist),
        "c3_named_inversion": c3_pair,
        "q4_suppressed_count": len(high_na_hummus_q4),
        "floor_threshold_mg": FLOOR_THRESHOLD_MG,
        "floor_value": FLOOR_VALUE,
        "off_used": False,
        "errors": errors,
        "score_table_hummus": [
            {
                "barcode": r["barcode"],
                "sodium_mg": r["sodium_mg"],
                "flag_off_score": r["flag_off_score"],
                "flag_off_grade": r["flag_off_grade"],
                "flag_on_score": r["flag_on_score"],
                "flag_on_grade": r["flag_on_grade"],
                "delta": r["delta"],
                "ev094_fired": r["ev094_fired"],
            }
            for r in sorted(hummus_in_scope, key=lambda x: (x.get("sodium_mg") or 0))
        ],
    }

    # Save run record
    run_record_path = OUTPUT_DIR / "run_record.json"
    run_record_path.write_text(
        json.dumps(run_record, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    log.info("Run record saved: %s", run_record_path)

    # Save full score table
    score_table_path = OUTPUT_DIR / "score_table_all.json"
    score_table_path.write_text(
        json.dumps(all_rows, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    log.info("Full score table saved: %s", score_table_path)

    # -----------------------------------------------------------------------
    # STEP 7: Print summary
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("TASK-278 Phase-12 / EV-094: Hummus x Sodium SR Pilot — Results")
    print("=" * 70)
    print(f"Run ID:       {RUN_ID}")
    print(f"Timestamp:    {ts}")
    print(f"Hummus in-scope (n): {n_hummus} (expected 60)")
    print(f"Salty snacks (n):    {len(snack_records)}")
    print(f"Milk (n):            {len(milk_rows)} (expected 20)")
    print()
    print("Gate Criteria:")
    for crit, result in criteria.items():
        print(f"  {crit:40s}: {result}")
    print()
    print(f"Movers (n):          {movers_n}")
    print(f"Grade changes (n):   {grade_changes_n}")
    print(f"Dead zone (%):       {dead_zone_pct:.1f}%")
    print(f"Mean abs delta:      {mean_abs_delta:.3f}")
    print(f"C1 directional:      {c1_pct:.1f}%")
    print(f"C10 milk delta=0:    {milk_delta_zero_count}/{len(milk_rows)}")
    print()
    print(f"OVERALL: {'ALL PASS' if all_criteria_pass else 'CRITERIA FAILURES — see above'}")
    print("=" * 70)

    return all_criteria_pass and c10_pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
