# BSIP2 batch -- Salty Snacks x sodium SHELF-RELATIVE PILOT (run_salty_snacks_sodium_pilot)
# TASK-278 Phase-11 / EV-093 -- salty_snacks x sodium asymmetric P>B shelf-relative enrollment.
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
    SUGAR_SHELF_SCALE_GUARD, SUGAR_SHELF_SCALE_MIN,
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
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

ROOT              = pathlib.Path(r"C:\Bari")
BSIP1_SNACK_DIR  = ROOT / "02_products" / "salty_snacks" / "bsip1_outputs"
MILK_RUN005_DIR  = ROOT / "02_products" / "milk_and_alternatives" / "intelligence_bsip2" / "run_005_headpin" / "products"
BSIP1_MILK_DIR   = ROOT / "03_operations" / "bsip1" / "run_milk_002" / "output"
BSIP1_YOGURT_DIR = ROOT / "03_operations" / "bsip1" / "run_yogurt_006" / "output"
BSIP1_CHEESE_DIR = ROOT / "03_operations" / "bsip1" / "run_cheese_003" / "output"
BSIP1_HC_DIR     = ROOT / "03_operations" / "bsip1" / "run_hard_cheeses_001" / "output"
BSIP1_JUICE_DIR  = ROOT / "03_operations" / "bsip1" / "run_juices_001" / "output"
BSIP1_MAAD_DIR   = ROOT / "03_operations" / "bsip1" / "run_maadanim_001" / "output"
OUTPUT_DIR       = ROOT / "02_products" / "salty_snacks" / "bsip2_outputs" / "run_salty_snacks_sodium_pilot"
RETURN_DIR       = ROOT / "tasks" / "returns"
RUN_ID = "run_salty_snacks_sodium_pilot"

# EV-093 constants (from D7 approval)
PROPOSAL_MEDIAN           = SODIUM_SHELF_REL_SALTY_SNACK_MEDIAN       # 560.0
PROPOSAL_SCALE            = SODIUM_SHELF_REL_SALTY_SNACK_SCALE        # 140.85
PROPOSAL_IQR              = SODIUM_SHELF_REL_SALTY_SNACK_IQR          # 190.0
FLOOR_VALUE               = SODIUM_SHELF_REL_SALTY_SNACK_FLOOR        # 62
FLOOR_THRESHOLD_MG        = SODIUM_SHELF_REL_SALTY_SNACK_FLOOR_THRESHOLD_MG  # 630.0

# Gate C3 named pair: Pringles Original (480mg) vs Bisli Spaghetti (800mg)
PRINGLES_ORIGINAL_BC = "7290005204001"   # sodium=480mg — low-sodium reference
BISLI_SPAGHETTI_BC   = "7290009900003"  # sodium=800mg — high-sodium reference

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
        barcode = str(doc.get("barcode", ""))
        name    = doc.get("canonical_name_he", "") or doc.get("product_name_he", "") or doc.get("canonical_name_en", "")
        nn      = doc.get("normalized_nutrition_per_100g") or {}
        sodium_mg = nn.get("sodium_mg")
        try:
            trace_on  = run_bsip2_pipeline(doc)
            trace_off = run_bsip2_pipeline_flag_off(doc)
            score_on  = trace_on.get("final_score_estimate")
            score_off = trace_off.get("final_score_estimate")
            grade_on  = trace_on.get("grade_estimate")
            grade_off = trace_off.get("grade_estimate")
            delta     = round(score_on - score_off, 2) if (score_on is not None and score_off is not None) else None
            category  = trace_on.get("category")
            floor_app = trace_on.get("ev093_salty_snack_floor_applied")
            sr_pen_on = None
            for p in (trace_on.get("penalties_applied") or []):
                if p.get("rule") == "SODIUM_SALTY_SNACK_SHELF_REL_V1":
                    sr_pen_on = p.get("amount")
                    break
            ev093_fired = (sr_pen_on is not None and sr_pen_on != 0) or (floor_app is True)
            rows.append({
                "barcode": barcode,
                "name": name,
                "corpus": corpus_label,
                "sodium_mg": sodium_mg,
                "flag_off_score": score_off,
                "flag_off_grade": grade_off,
                "flag_on_score": score_on,
                "flag_on_grade": grade_on,
                "delta": delta,
                "ev093_fired": ev093_fired,
                "ev093_salty_snack_floor_applied": floor_app,
                "sr_penalty": sr_pen_on,
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
    log.info("=== TASK-278 Phase-11 EV-093: Salty Snacks x Sodium SR Pilot -- %s ===", RUN_ID)
    log.info("MEASURED NOT PUBLISHED: no frontend JSON, no live category, no deploy")

    # -----------------------------------------------------------------------
    # STEP 1: Load all corpora
    # -----------------------------------------------------------------------
    snack_records  = load_bsip1_dir(BSIP1_SNACK_DIR, "bsip1_snack_*.json", "salty_snack")
    milk_records   = load_milk_run005()
    yogurt_records = load_bsip1_dir(BSIP1_YOGURT_DIR, "bsip1_*.json", "yogurt")
    cheese_records = load_bsip1_dir(BSIP1_CHEESE_DIR, "bsip1_*.json", "cheese_spread")
    hc_records     = load_bsip1_dir(BSIP1_HC_DIR, "bsip1_hardcheese_*.json", "hard_cheese")
    juice_records  = load_bsip1_dir(BSIP1_JUICE_DIR, "bsip1_*.json", "juice")
    maad_records   = load_bsip1_dir(BSIP1_MAAD_DIR, "bsip1_*.json", "maadanim")

    log.info("Salty snacks loaded: %d (expected 54)", len(snack_records))

    # -----------------------------------------------------------------------
    # STEP 2: Verify sodium data coverage
    # -----------------------------------------------------------------------
    snack_with_sodium = [r for r in snack_records
                         if (r.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") is not None]
    sodium_vals = [(r.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") for r in snack_with_sodium]
    log.info("Salty snacks with sodium_mg: %d/%d", len(snack_with_sodium), len(snack_records))

    # -----------------------------------------------------------------------
    # STEP 3: Set shelf stats
    # Set salty_snack sodium shelf stats (D7-approved constants)
    # Set prior enrolled category stats
    # -----------------------------------------------------------------------
    clear_shelf_stats()

    # EV-093: salty_snack × sodium
    engine_median, engine_scale = compute_shelf_stats(
        snack_with_sodium,
        "sodium_mg",
        scale_type="iqr",
        nutrient_min_scale=10.0,
    )
    log.info("Engine computed sodium_mg: median=%.3f, scale=%.3f (proposal: median=%.3f, scale=%.3f)",
             engine_median or 0, engine_scale or 0, PROPOSAL_MEDIAN, PROPOSAL_SCALE)

    set_shelf_stats(
        nutrient="sodium_mg",
        median=engine_median if engine_median is not None else PROPOSAL_MEDIAN,
        scale=engine_scale if engine_scale is not None else PROPOSAL_SCALE,
        scale_type="iqr",
        n=len(snack_with_sodium),
    )
    used_median = engine_median if engine_median is not None else PROPOSAL_MEDIAN
    used_scale  = engine_scale if engine_scale is not None else PROPOSAL_SCALE
    log.info("Shelf stats set: sodium_mg median=%.3f scale=%.3f n=%d", used_median, used_scale, len(snack_with_sodium))

    # Prior enrolled categories — set their shelf stats as in prior pilots
    # EV-087 cereals × sugars_g
    set_shelf_stats(nutrient="sugars_g",
                    median=SUGAR_SHELF_REL_CEREAL_MEDIAN, scale=SUGAR_SHELF_REL_CEREAL_SCALE,
                    scale_type="iqr", n=34)
    # EV-088 yogurt × sugars_g (will OVERWRITE cereal; engine uses same nutrient key)
    # NOTE: sugars_g is a shared key — only one nutrient entry per key.
    # The engine scope guards (category_subtype, juice_sub_pool, maadanim_subtype) separate them.
    # For this pilot we set the most recent approved sugars_g stats (maadanim is latest).
    # Each pilot sets stats for its own nutrient; maadanim overrides yogurt/cereal for sugars_g.
    # Correct approach: set all sugars_g enrolled stats — the engine guards handle scoping.
    # We use maadanim stats (last enrolled, broadest scope) as the stat for sugars_g.
    # This matches prior pilot pattern (maadanim pilot set sugars_g to its stats).
    set_shelf_stats(nutrient="sugars_g",
                    median=SUGAR_SHELF_REL_MAADANIM_MEDIAN, scale=SUGAR_SHELF_REL_MAADANIM_SCALE,
                    scale_type="iqr", n=146)
    # EV-089 cheese_spread × fat_saturated_g
    set_shelf_stats(nutrient="fat_saturated_g",
                    median=FATSAT_SHELF_REL_CHEESESPREAD_MEDIAN, scale=FATSAT_SHELF_REL_CHEESESPREAD_SCALE,
                    scale_type="iqr", n=24)
    # EV-090 hard_cheese × fat_saturated_g (shares key with cheese_spread)
    # Hard cheese uses same fat_saturated_g key — last write wins.
    # For scope bleed test: neither hard_cheese nor cheese_spread should see EV-093.
    # Keep fat_saturated_g stats as last set (cheese_spread or hard_cheese — same nutrient key).
    # Set to hard_cheese stats (higher n, more conservative).
    set_shelf_stats(nutrient="fat_saturated_g",
                    median=FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, scale=FATSAT_SHELF_REL_HARDCHEESE_SCALE,
                    scale_type="iqr", n=37)

    log.info("Shelf stats set for all enrolled nutrients.")

    # -----------------------------------------------------------------------
    # STEP 4: Score all corpora
    # -----------------------------------------------------------------------
    errors = []
    log.info("--- Scoring salty_snack corpus (%d products) ---", len(snack_records))
    snack_rows  = score_corpus(snack_records, "salty_snack", errors)
    log.info("--- Scoring milk corpus (%d products) C10 check ---", len(milk_records))
    milk_rows   = score_corpus(milk_records, "milk", errors)
    log.info("--- Scoring yogurt corpus (%d products) ---", len(yogurt_records))
    yogurt_rows = score_corpus(yogurt_records, "yogurt", errors)
    log.info("--- Scoring cheese_spread corpus (%d products) ---", len(cheese_records))
    cheese_rows = score_corpus(cheese_records, "cheese_spread", errors)
    log.info("--- Scoring hard_cheese corpus (%d products) ---", len(hc_records))
    hc_rows     = score_corpus(hc_records, "hard_cheese", errors)
    log.info("--- Scoring juice corpus (%d products) ---", len(juice_records))
    juice_rows  = score_corpus(juice_records, "juice", errors)
    log.info("--- Scoring maadanim corpus (%d products) ---", len(maad_records))
    maad_rows   = score_corpus(maad_records, "maadanim", errors)

    # -----------------------------------------------------------------------
    # STEP 5: Gate criteria evaluation
    # -----------------------------------------------------------------------
    log.info("--- Evaluating gate criteria ---")

    # Salty snack rows that are in EV-093 scope (have sodium_mg > 0)
    snack_sodium_rows = [r for r in snack_rows if r["sodium_mg"] is not None and r["sodium_mg"] > 0]
    log.info("EV-093 sodium scope: %d salty_snack products with sodium_mg", len(snack_sodium_rows))

    # C1: directional_distribution — ≥70% of movers move in correct direction
    # high-sodium (>median) → negative delta; low-sodium (<median) → positive delta
    above_median = [r for r in snack_sodium_rows if r["sodium_mg"] is not None and r["sodium_mg"] > PROPOSAL_MEDIAN]
    below_median = [r for r in snack_sodium_rows if r["sodium_mg"] is not None and r["sodium_mg"] < PROPOSAL_MEDIAN]
    above_movers = [r for r in above_median if r["delta"] is not None and r["delta"] != 0]
    below_movers = [r for r in below_median if r["delta"] is not None and r["delta"] != 0]
    above_correct = [r for r in above_movers if r["delta"] < 0]
    below_correct = [r for r in below_movers if r["delta"] > 0]
    all_movers_directional = above_movers + below_movers
    all_correct_directional = above_correct + below_correct
    c1_pct = (len(all_correct_directional) / len(all_movers_directional) * 100) if all_movers_directional else 0
    c1_pass = c1_pct >= 70.0
    c1_note = (f"above_median(>{PROPOSAL_MEDIAN}mg, n={len(above_median)}, movers={len(above_movers)}, "
               f"correct_dir={len(above_correct)}); below_median(<{PROPOSAL_MEDIAN}mg, n={len(below_median)}, "
               f"movers={len(below_movers)}, correct_dir={len(below_correct)}); "
               f"directional_correct={len(all_correct_directional)}/{len(all_movers_directional)}={c1_pct:.1f}% (need>=70%)")

    # C2a: grade dist at flag-off is plausible (not degenerate — has at least 2 distinct grades)
    grade_off_dist = Counter(r["flag_off_grade"] for r in snack_sodium_rows if r["flag_off_grade"])
    grade_on_dist  = Counter(r["flag_on_grade"] for r in snack_sodium_rows if r["flag_on_grade"])
    c2a_pass = len(grade_off_dist) >= 2
    c2a_note = f"Grade dists: off={dict(grade_off_dist)} on={dict(grade_on_dist)} (need >=2 distinct grades at flag-off)"

    # C2b: grade absorption ≤50% (movers that DON'T change grade / total movers)
    movers = [r for r in snack_sodium_rows if r["delta"] is not None and r["delta"] != 0]
    non_grade_changers = [r for r in movers if r["flag_off_grade"] == r["flag_on_grade"]]
    grade_absorption_pct = (len(non_grade_changers) / len(movers) * 100) if movers else 0
    c2b_pass = grade_absorption_pct <= 50.0
    c2b_note = f"Grade absorption (movers without grade change): {len(non_grade_changers)}/{len(movers)}={grade_absorption_pct:.1f}% (need<=50%)"

    # C2c: mean abs delta for movers ≥0.5 pts
    mover_abs_deltas = [abs(r["delta"]) for r in movers if r["delta"] is not None]
    c2c_mean_abs = sum(mover_abs_deltas) / len(mover_abs_deltas) if mover_abs_deltas else 0
    c2c_pass = len(movers) > 0 and c2c_mean_abs >= 0.5
    c2c_note = f"movers={len(movers)}, mean|delta|={c2c_mean_abs:.3f} (need>=0.5)"

    # C3: named inversion pair — Pringles Original (480mg) vs Bisli Spaghetti (800mg)
    def find_by_barcode(rows, bc):
        for r in rows:
            if str(r["barcode"]) == str(bc):
                return r
        return None

    pringles = find_by_barcode(snack_rows, PRINGLES_ORIGINAL_BC)
    bisli_sp = find_by_barcode(snack_rows, BISLI_SPAGHETTI_BC)

    c3_pass = False
    c3_note = f"Pringles({PRINGLES_ORIGINAL_BC}) vs Bisli_Spaghetti({BISLI_SPAGHETTI_BC}): "
    if pringles and bisli_sp:
        p_off = pringles.get("flag_off_score")
        p_on  = pringles.get("flag_on_score")
        b_off = bisli_sp.get("flag_off_score")
        b_on  = bisli_sp.get("flag_on_score")
        if all(x is not None for x in [p_off, p_on, b_off, b_on]):
            gap_off = round(p_off - b_off, 2)  # Pringles - Bisli at flag-off
            gap_on  = round(p_on - b_on, 2)    # Pringles - Bisli at flag-on
            # Correct: Pringles (low sodium=480mg) should score above Bisli (high sodium=800mg)
            # At flag-on, the gap should widen (or rank should be correct)
            correct_rank = p_on >= b_on  # Pringles ≥ Bisli at flag-on
            gap_widened  = gap_on > gap_off   # gap widened in Pringles' favor
            c3_pass = correct_rank or gap_widened
            c3_note += (f"flag_off: Pringles={p_off} Bisli={b_off} gap={gap_off}; "
                        f"flag_on: Pringles={p_on} Bisli={b_on} gap={gap_on}; "
                        f"correct_rank_at_on={correct_rank} gap_widened={gap_widened} -> {'PASS' if c3_pass else 'FAIL'}")
        else:
            c3_note += "one or both products have None score — FAIL"
    else:
        missing = []
        if not pringles: missing.append(f"Pringles({PRINGLES_ORIGINAL_BC})")
        if not bisli_sp: missing.append(f"Bisli({BISLI_SPAGHETTI_BC})")
        c3_note += f"NOT FOUND in corpus: {missing}"

    # C4: movers_n ≥5
    c4_pass = len(movers) >= 5
    c4_note = f"{len(movers)} salty_snack products with |delta|>0 (need>=5)"

    # C5: grade_changes_n ≥1
    grade_changers = [r for r in snack_sodium_rows if r["flag_off_grade"] != r["flag_on_grade"]]
    c5_pass = len(grade_changers) >= 1
    c5_note = (f"{len(grade_changers)} salty_snack products with grade change (need>=1). "
               f"Examples: {[{'bc': r['barcode'], 'off': r['flag_off_grade'], 'on': r['flag_on_grade']} for r in grade_changers[:3]]}")

    # C6: dead_zone_pct ≤55% (products with |delta| < 0.1 / total salty_snacks)
    dead_zone = [r for r in snack_sodium_rows if r["delta"] is None or abs(r["delta"]) < 0.1]
    dead_zone_pct = (len(dead_zone) / len(snack_sodium_rows) * 100) if snack_sodium_rows else 0
    c6_pass = dead_zone_pct <= 55.0
    c6_note = f"Dead zone (|delta|<0.1): {len(dead_zone)}/{len(snack_sodium_rows)}={dead_zone_pct:.1f}% (need<=55%)"

    # C7: anti-immunity — no salty_snack reaches grade B (70+) solely via SR
    # Check: products that moved UP via SR and now score ≥70 — flag if delta>0 and score_on>=70
    sr_boosted_to_b = [r for r in snack_sodium_rows
                       if r["delta"] is not None and r["delta"] > 0
                       and r["flag_on_score"] is not None and r["flag_on_score"] >= 70]
    c7_pass = len(sr_boosted_to_b) == 0
    c7_note = (f"{len(sr_boosted_to_b)} salty_snack products boosted by SR to grade B (score>=70). "
               f"Violators: {[r['barcode'] for r in sr_boosted_to_b]}")

    # C8: floor compliance — all products with sodium ≥630mg score ≥62 at flag-on
    # (EV-093 floor CLAMPS at ≤62, so this verifies the floor fires correctly)
    above_floor_threshold = [r for r in snack_sodium_rows
                             if r["sodium_mg"] is not None and r["sodium_mg"] >= FLOOR_THRESHOLD_MG]
    floor_violations = [r for r in above_floor_threshold
                        if r["flag_on_score"] is not None and r["flag_on_score"] > FLOOR_VALUE]
    c8_pass = len(floor_violations) == 0
    c8_note = (f"{len(above_floor_threshold)} products with sodium>={FLOOR_THRESHOLD_MG}mg, "
               f"{len(floor_violations)} floor violations (score>{FLOOR_VALUE}). "
               f"Violators: {[r['barcode'] for r in floor_violations]}")

    # C9: scope bleed = 0 (no non-salty_snack product has delta ≠ 0.0 from EV-093)
    non_snack_rows = milk_rows + yogurt_rows + cheese_rows + hc_rows + juice_rows + maad_rows
    bleed_products = [r for r in non_snack_rows if r.get("ev093_fired") or r.get("ev093_salty_snack_floor_applied")]
    c9_pass = len(bleed_products) == 0
    c9_note = (f"{len(bleed_products)} non-salty_snack products with EV-093 fired (need=0). "
               f"Examples: {[r['barcode'] for r in bleed_products[:3]]}")

    # C10: CRITICAL — all 20 milk products delta = 0.0
    milk_movers = [r for r in milk_rows if r["delta"] is not None and r["delta"] != 0]
    c10_pass = len(milk_rows) == 20 and len(milk_movers) == 0
    if not c10_pass:
        log.error("CRITICAL FAIL C10: milk delta != 0 for %d products! STOP.", len(milk_movers))
        if len(milk_rows) != 20:
            log.error("CRITICAL: Expected 20 milk products, got %d", len(milk_rows))
    c10_note = (f"{len(milk_rows)} milk products loaded, "
                f"{len(milk_rows) - len(milk_movers)}/20 with delta=0.0 (need 20/20). "
                f"Movers: {[{'bc': r['barcode'], 'delta': r['delta']} for r in milk_movers]}")

    # C10 HALT if milk products moved
    if not c10_pass:
        print("\n" + "=" * 70)
        print("CRITICAL FAIL C10: MILK PRODUCTS MOVED — HALT")
        print(f"milk_movers={len(milk_movers)}: {[{'bc': r['barcode'], 'delta': r['delta']} for r in milk_movers]}")
        print("=" * 70)
        import sys; sys.exit(1)

    gate_criteria = [
        {"criterion": "C1",  "name": "directional_distribution",  "pass": c1_pass,  "note": c1_note},
        {"criterion": "C2a", "name": "grade_dist_plausible",       "pass": c2a_pass, "note": c2a_note},
        {"criterion": "C2b", "name": "grade_absorption",           "pass": c2b_pass, "note": c2b_note},
        {"criterion": "C2c", "name": "magnitude",                  "pass": c2c_pass, "note": c2c_note},
        {"criterion": "C3",  "name": "inversion_pair",             "pass": c3_pass,  "note": c3_note},
        {"criterion": "C4",  "name": "movers_n",                   "pass": c4_pass,  "note": c4_note},
        {"criterion": "C5",  "name": "grade_changes_n",            "pass": c5_pass,  "note": c5_note},
        {"criterion": "C6",  "name": "dead_zone_pct",              "pass": c6_pass,  "note": c6_note},
        {"criterion": "C7",  "name": "anti_immunity",              "pass": c7_pass,  "note": c7_note},
        {"criterion": "C8",  "name": "floor_compliance",           "pass": c8_pass,  "note": c8_note},
        {"criterion": "C9",  "name": "no_scope_bleed",             "pass": c9_pass,  "note": c9_note},
        {"criterion": "C10", "name": "milk_frozen_byte_id",        "pass": c10_pass, "note": c10_note},
    ]

    criteria_pass = [c["criterion"] for c in gate_criteria if c["pass"]]
    criteria_fail = [c["criterion"] for c in gate_criteria if not c["pass"]]
    all_pass = len(criteria_fail) == 0

    # -----------------------------------------------------------------------
    # STEP 6: Write score table CSV
    # -----------------------------------------------------------------------
    table_path = OUTPUT_DIR / "salty_snack_pilot_table.csv"
    with table_path.open("w", encoding="utf-8", newline="") as f:
        f.write("barcode,name,sodium_mg,flag_off_score,flag_off_grade,"
                "flag_on_score,flag_on_grade,delta,ev093_fired,ev093_floor_applied,category\n")
        for r in sorted(snack_rows, key=lambda x: -(x["sodium_mg"] or 0)):
            f.write(",".join(str(r.get(k, "")) for k in [
                "barcode", "name", "sodium_mg",
                "flag_off_score", "flag_off_grade",
                "flag_on_score", "flag_on_grade",
                "delta", "ev093_fired", "ev093_salty_snack_floor_applied", "category"
            ]) + "\n")

    # -----------------------------------------------------------------------
    # STEP 7: Write run_record.json
    # -----------------------------------------------------------------------
    score_engine_sha = sha256_file(_SCRIPT_DIR / "src" / "score_engine.py")
    constants_sha    = sha256_file(_SCRIPT_DIR / "src" / "constants.py")

    on_scores  = [r["flag_on_score"] for r in snack_sodium_rows if r["flag_on_score"] is not None]
    off_scores = [r["flag_off_score"] for r in snack_sodium_rows if r["flag_off_score"] is not None]

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-278 Phase-11 / EV-093",
        "category_slug": "salty_snack",
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
            "salty_snack_total": len(snack_records),
            "salty_snack_with_sodium": len(snack_with_sodium),
            "ev093_sodium_scope_n": len(snack_sodium_rows),
        },
        "shelf_stats": {
            "nutrient": "sodium_mg",
            "proposal_median": PROPOSAL_MEDIAN,
            "proposal_scale": PROPOSAL_SCALE,
            "proposal_iqr": PROPOSAL_IQR,
            "engine_median": engine_median,
            "engine_scale": engine_scale,
            "used_median": used_median,
            "used_scale": used_scale,
            "n_for_stats": len(snack_with_sodium),
        },
        "corpus": {
            "salty_snack_loaded": len(snack_records),
            "salty_snack_sodium_scope_n": len(snack_sodium_rows),
            "milk_loaded": len(milk_records),
            "yogurt_loaded": len(yogurt_records),
            "cheese_spread_loaded": len(cheese_records),
            "hard_cheese_loaded": len(hc_records),
            "juice_loaded": len(juice_records),
            "maadanim_loaded": len(maad_records),
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
        "grade_changes_n": len(grade_changers),
        "mean_abs_delta_movers": round(c2c_mean_abs, 3),
        "dead_zone_pct": round(dead_zone_pct, 1),
        "floor_applied_count": len([r for r in snack_rows if r.get("ev093_salty_snack_floor_applied")]),
        "milk_delta_zero_count": len(milk_rows) - len(milk_movers),
        "milk_total": len(milk_rows),
        "gate_criteria": gate_criteria,
        "criteria_pass": criteria_pass,
        "criteria_fail": criteria_fail,
        "all_criteria_pass": all_pass,
        "salty_snack_product_table": sorted(snack_rows, key=lambda x: -(x["sodium_mg"] or 0)),
        "milk_rows": milk_rows,
        "pringles_row": pringles,
        "bisli_spaghetti_row": bisli_sp,
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
    print(f"SALTY SNACKS SODIUM SR PILOT -- {RUN_ID}")
    print("=" * 70)
    print(f"TASK-278 Phase-11 / EV-093 | MEASURED NOT PUBLISHED")
    print(f"Flag: BARI_SHELF_RELATIVE_V1=ON | scope=salty_snack | P=6/B=3 | floor=62@{FLOOR_THRESHOLD_MG}mg")
    print()
    print(f"PRECHECK: salty_snack_total={len(snack_records)} with_sodium={len(snack_with_sodium)} scope={len(snack_sodium_rows)}")
    print()
    print(f"SHELF STATS: engine median={engine_median}, scale={engine_scale}")
    print(f"  Proposal: median={PROPOSAL_MEDIAN}, scale={PROPOSAL_SCALE}")
    print()
    print(f"CORPUS: salty_snack={len(snack_records)} | milk={len(milk_records)} | yogurt={len(yogurt_records)} | "
          f"cheese_spread={len(cheese_records)} | hard_cheese={len(hc_records)} | juice={len(juice_records)} | maadanim={len(maad_records)}")
    print(f"Errors: {len(errors)}")
    print()
    print(f"GRADE DISTRIBUTION (salty_snack sodium scope, n={len(snack_sodium_rows)}):")
    for g in ["S", "A", "B", "C", "D", "E"]:
        print(f"  {g}: off={grade_off_dist.get(g,0)} on={grade_on_dist.get(g,0)}")
    print()
    print(f"MOVERS (|delta|>0): {len(movers)}/{len(snack_sodium_rows)}")
    print(f"GRADE CHANGES: {len(grade_changers)}")
    print(f"MEAN |DELTA| (movers): {c2c_mean_abs:.3f}")
    print(f"DEAD ZONE (|delta|<0.1): {dead_zone_pct:.1f}%")
    print(f"FLOOR APPLIED: {run_record['floor_applied_count']}")
    print()
    print(f"C3 INVERSION CHECK:")
    if pringles:
        print(f"  Pringles Original ({PRINGLES_ORIGINAL_BC}, 480mg): off={pringles.get('flag_off_score')} on={pringles.get('flag_on_score')} delta={pringles.get('delta')}")
    else:
        print(f"  Pringles Original ({PRINGLES_ORIGINAL_BC}): NOT FOUND")
    if bisli_sp:
        print(f"  Bisli Spaghetti   ({BISLI_SPAGHETTI_BC}, 800mg): off={bisli_sp.get('flag_off_score')} on={bisli_sp.get('flag_on_score')} delta={bisli_sp.get('delta')}")
    else:
        print(f"  Bisli Spaghetti   ({BISLI_SPAGHETTI_BC}): NOT FOUND")
    print()
    print(f"{len(gate_criteria)} GATE CRITERIA:")
    for c in gate_criteria:
        status = "PASS" if c["pass"] else "FAIL"
        print(f"  {c['criterion']:4s} [{status}]: {c['name']}")
        print(f"        {c['note']}")
    print()
    print(f"ALL CRITERIA PASS: {all_pass}")
    print(f"PASS: {criteria_pass}")
    print(f"FAIL: {criteria_fail}")
    print()
    print(f"C10 MILK: {len(milk_rows) - len(milk_movers)}/{len(milk_rows)} delta=0")
    print()
    print(f"SODIUM DISTRIBUTION (key products, sorted by sodium desc):")
    for r in sorted(snack_rows, key=lambda x: -(x["sodium_mg"] or 0))[:10]:
        print(f"  {r['barcode']} sodium={r['sodium_mg']}mg off={r['flag_off_score']}/{r['flag_off_grade']} on={r['flag_on_score']}/{r['flag_on_grade']} delta={r['delta']}")
    print()
    print(f"score_engine.py SHA256: {score_engine_sha[:16]}...")
    print(f"constants.py SHA256:    {constants_sha[:16]}...")
    print(f"Run record: {rr_path}")
    print(f"Table: {table_path}")
    print("=" * 70)

    return run_record


if __name__ == "__main__":
    main()
