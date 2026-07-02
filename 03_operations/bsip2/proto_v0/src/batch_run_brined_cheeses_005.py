"""
BSIP1 Enrichment + BSIP2 Scoring — Brined Cheeses (run_brined_005)
Red-team remediation run. Fixes:
  RT-1  (CRITICAL) bc-048 brined_food vocabulary gap — evaluation_scope.py now
         includes construct forms ("גבינת מלוחה", "גבינת עזים", "גבינת כבשים"),
         EV-052 addendum.
  RT-2/RT-6/RT-13 (CRITICAL) bc-035 + bc-045 marketing-copy ingredients — nulled
         in BSIP1 run_brined_002, ingredient_text_quality="marketing_bleed".
  RT-9/RT-10/RT-11 (MED) scrape artifacts stripped, typo fixed, name fixed —
         in BSIP1 run_brined_002.

Changes from run_brined_003:
  1. BSIP1 source: run_brined_cheeses_002 (hygiene-cleaned corpus).
  2. evaluation_scope.py: brined_food keyword list extended with Hebrew construct
     forms ("גבינת מלוחה", "גבינת עזים", "גבינת כבשים") — vocabulary extension only,
     no new scoring rule, no D7 required (Nutrition ruling per cap45_ruling §9 addendum).
  3. bc-048 (גבינת טמרה מלוחה בקר 17%, barcode 3075805) now receives context_flag=brined_food,
     EV-053/054/055 all fire. Score expected to rise from 39/D to mid-B or higher.

Flag config (identical to run_brined_003 + TASK-449 brined fix for candidate):
  BARI_RECAL_P0=on
  BARI_RECAL_P0_YOGURT_TRIM=off
  BARI_GRAD_SODIUM_V1=on          — EV-055 graduated sodium (brined_food scope only)
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_TASK144_FIXES=off
  BARI_TASK250_CONF=off
  BARI_GLASSBOX_W4=on (default)
  BARI_FERMENT_MARKER_BRINED_FIX_V1=on  — TASK-449 Option A (restricts Path B +8 for brined_food)

OFF ban: absolute. off_used=0.
"""
import os
import sys
import json
import re
import pathlib
import logging
import datetime
import hashlib

# --- Flag config BEFORE engine imports ---
os.environ["BARI_RECAL_P0"] = "on"
os.environ["BARI_RECAL_P0_YOGURT_TRIM"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "on"   # EV-055
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_TASK144_FIXES"] = "off"
os.environ["BARI_TASK250_CONF"] = "off"
os.environ["BARI_GLASSBOX_D5D6"] = "off"
os.environ["BARI_GLASSBOX_W15"] = "off"
os.environ["BARI_GLASSBOX_W2"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "on"   # EV-056
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "on"   # EV-057
os.environ["BARI_SHELF_RELATIVE_V1"] = "on"           # P109 Step-4: explicit on for brined byte-id check (must be no-op for non-cereal/biscuit)
os.environ["BARI_FERMENT_MARKER_BRINED_FIX_V1"] = "on"  # TASK-449 Option A (P459)
# BARI_GLASSBOX_W4 defaults to on (module-level default)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_sodium_stats, compute_shelf_sodium_stats, clear_shelf_sodium_stats
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# --- Paths ---
# Worktree-safe (P459): compute repo root relative to this file (in src/) so runs
# stay inside the worktree and never touch C:\Bari . Use distinct output dir for
# the TASK-449 brined-fix candidate so committed baseline run_brined_005 traces are untouched.
ROOT = pathlib.Path(__file__).resolve().parents[4]
BSIP0_FILE  = ROOT / "02_products" / "brined_cheeses" / "bsip0_outputs" / \
              "brined_cheese_bsip0_raw_20260613T065721.json"
CORPUS_FILE = ROOT / "02_products" / "brined_cheeses" / "factory_run_001" / "corpus_filter.json"
# run_brined_005 uses the hygiene-cleaned BSIP1 run_002
BSIP1_REUSE_DIR = ROOT / "03_operations" / "bsip1" / "run_brined_cheeses_002" / "output"
BSIP2_OUTPUT    = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_005_brinedfix_on"
REPORT_ROOT     = ROOT / "02_products" / "brined_cheeses" / "reports"
# Baseline for before/after comparison (committed, not overwritten)
BSIP2_PREV_DIR  = ROOT / "02_products" / "brined_cheeses" / "bsip2_outputs" / "run_brined_003"
RUN_ID = "run_brined_005_brinedfix_on"

(BSIP2_OUTPUT / "products").mkdir(parents=True, exist_ok=True)
REPORT_ROOT.mkdir(parents=True, exist_ok=True)


def run_bsip2_pipeline(bsip1_product: dict) -> dict:
    signals     = extract_signals(bsip1_product)
    cat_result  = classify_category(bsip1_product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(bsip1_product, l3)
    eval_result = assign_evaluation_scope(bsip1_product, cat_result["category"])
    score_result = score_product(bsip1_product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(bsip1_product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def stdev(scores: list) -> float:
    if not scores:
        return 0.0
    n = len(scores)
    mean = sum(scores) / n
    return (sum((x - mean) ** 2 for x in scores) / n) ** 0.5


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    log.info("=== BSIP2 Brined Cheeses — %s (EV-056 shelf-relative sodium + EV-057 dairy_protein reweight) ===", RUN_ID)
    log.info("Flags: RECAL_P0=on | GRAD_SODIUM_V1=on | REDLABEL_V1=off | SODIUM_CEREAL=off")
    log.info("BSIP1 source: run_brined_cheeses_002 (hygiene-cleaned)")

    # Load corpus filter — build IN_SCORED barcode set
    corpus = json.loads(CORPUS_FILE.read_text(encoding="utf-8"))
    in_scored_barcodes = {
        str(p["barcode"]) for p in corpus["products"]
        if p["decision"] == "IN_SCORED"
    }
    log.info("IN_SCORED barcodes: %d", len(in_scored_barcodes))

    # Load BSIP1 records from run_brined_002 (hygiene-cleaned)
    bsip1_records = []
    for p in sorted(BSIP1_REUSE_DIR.glob("bsip1_brinedcheese_*.json")):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            barcode = str(doc.get("barcode", ""))
            if barcode in in_scored_barcodes:
                bsip1_records.append(doc)
        except Exception as e:
            log.error("Load error %s: %s", p.name, e)

    log.info("BSIP1 records loaded: %d (from run_brined_cheeses_002)", len(bsip1_records))

    if len(bsip1_records) != 48:
        log.warning("Expected 48 BSIP1 records, got %d", len(bsip1_records))

    # -----------------------------------------------------------------------
    # Shelf sodium stats (EV-056) — computed before scoring loop
    # -----------------------------------------------------------------------
    shelf_median, shelf_stdev = compute_shelf_sodium_stats(bsip1_records)
    set_shelf_sodium_stats(shelf_median, shelf_stdev)
    log.info("SHELF_SODIUM_MEDIAN_MG=%s  shelf_stdev=%s", shelf_median, shelf_stdev)

    # -----------------------------------------------------------------------
    # BSIP2 Scoring
    # -----------------------------------------------------------------------
    traces = []
    score_errors = []
    brined_flag_fired = []
    brined_flag_not_fired = []
    sodium_grad_fired = []
    routing_cats = {}

    bc048_barcode = "3075805"   # bc-048 — the critical RT-1 product
    bc048_trace = None

    for doc in bsip1_records:
        barcode = str(doc.get("barcode", ""))
        name    = doc.get("canonical_name_he", "")
        try:
            trace = run_bsip2_pipeline(doc)
            write_trace(trace, BSIP2_OUTPUT)
            traces.append(trace)

            score    = trace.get("final_score_estimate")
            grade    = trace.get("grade_estimate")
            cat      = trace.get("category")
            nova     = trace.get("nova_proxy")
            ctx_flag = trace.get("context_flag")
            sodium_val = (doc.get("normalized_nutrition_per_100g") or {}).get("sodium_mg") or 0

            if barcode == bc048_barcode:
                bc048_trace = trace
                log.info("  *** bc-048 RT-1 CHECK: ctx_flag=%s score=%s grade=%s ***",
                         ctx_flag, score, grade)

            routing_cats[cat] = routing_cats.get(cat, 0) + 1

            if ctx_flag == "brined_food":
                brined_flag_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val, "score": score, "grade": grade,
                })
            else:
                brined_flag_not_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val,
                    "ctx_flag": ctx_flag,
                    "score": score, "grade": grade,
                    "note": "sodium<=500 or name not matched",
                })

            pens_applied = trace.get("penalties_applied", []) or []
            grad_fired = any(x.get("rule") == "SODIUM_LOAD_GENERAL_GRAD" for x in pens_applied)
            if grad_fired:
                pen_entry = next((x for x in pens_applied if x.get("rule") == "SODIUM_LOAD_GENERAL_GRAD"), {})
                sodium_grad_fired.append({
                    "barcode": barcode, "name": name,
                    "sodium_mg": sodium_val, "score": score, "grade": grade,
                    "penalty": pen_entry.get("amount"),
                    "note": pen_entry.get("note", ""),
                })

            log.info("  BSIP2 %-40s score=%-5s grade=%-2s cat=%-14s nova=%s ctx=%s",
                     name[:38], score, grade, cat, nova, ctx_flag or "standard")
        except Exception as e:
            log.error("  BSIP2 ERROR %s (%s): %s", barcode, name, e)
            import traceback; traceback.print_exc()
            score_errors.append({"barcode": barcode, "name": name, "error": str(e)})

    # -----------------------------------------------------------------------
    # Score distribution
    # -----------------------------------------------------------------------
    all_scores = [t.get("final_score_estimate") for t in traces if t.get("final_score_estimate") is not None]
    grade_dist = {}
    for t in traces:
        g = t.get("grade_estimate", "?")
        grade_dist[g] = grade_dist.get(g, 0) + 1

    if all_scores:
        scores_sorted = sorted(all_scores)
        n = len(scores_sorted)
        median = scores_sorted[n // 2] if n % 2 else (scores_sorted[n//2 - 1] + scores_sorted[n//2]) / 2
        score_min = min(all_scores)
        score_max = max(all_scores)
        score_stdev = round(stdev(all_scores), 2)
    else:
        median = score_min = score_max = score_stdev = None

    histogram = {}
    for s in all_scores:
        band = f"{int(s // 10) * 10}-{int(s // 10) * 10 + 9}"
        histogram[band] = histogram.get(band, 0) + 1

    score_range = (score_max - score_min) if (score_max is not None and score_min is not None) else 0

    # -----------------------------------------------------------------------
    # RT-1 acceptance check: bc-048 must now have context_flag=brined_food
    # -----------------------------------------------------------------------
    rt1_fixed = False
    bc048_summary = {}
    if bc048_trace:
        bc048_ctx = bc048_trace.get("context_flag")
        bc048_score = bc048_trace.get("final_score_estimate")
        bc048_grade = bc048_trace.get("grade_estimate")
        bc048_drivers = []
        for pen in (bc048_trace.get("penalties_applied") or []):
            bc048_drivers.append(f"-{pen.get('amount','?')} {pen.get('rule','?')}")
        for cap in (bc048_trace.get("caps_applied") or []):
            bc048_drivers.append(f"cap={cap.get('cap','?')} {cap.get('rule','?')}")
        rt1_fixed = (bc048_ctx == "brined_food")
        bc048_summary = {
            "barcode": bc048_barcode,
            "name": "גבינת טמרה מלוחה בקר 17%",
            "context_flag": bc048_ctx,
            "score_run003": 39.0,
            "score_run004": bc048_score,
            "grade_run003": "D",
            "grade_run004": bc048_grade,
            "rt1_fixed": rt1_fixed,
            "drivers": bc048_drivers,
        }

    # -----------------------------------------------------------------------
    # Before/after vs run_brined_003
    # -----------------------------------------------------------------------
    trace_by_barcode = {
        (t.get("barcode") or (t.get("input_reference") or {}).get("barcode", "")): t
        for t in traces
    }
    before_after = []
    for bc, trace in trace_by_barcode.items():
        prev_trace_path = BSIP2_PREV_DIR / "products" / f"bsip1_brinedcheese_{bc}" / "bsip2_trace.json"
        if prev_trace_path.exists():
            old = json.loads(prev_trace_path.read_text(encoding="utf-8"))
            old_score = old.get("final_score_estimate")
            old_grade = old.get("grade_estimate")
            new_score = trace.get("final_score_estimate")
            new_grade = trace.get("grade_estimate")
            if old_score != new_score or old_grade != new_grade:
                bsip1_f = BSIP1_REUSE_DIR / f"bsip1_brinedcheese_{bc}.json"
                fat_val = None
                sodium_val = None
                if bsip1_f.exists():
                    b1 = json.loads(bsip1_f.read_text(encoding="utf-8"))
                    fat_val = (b1.get("normalized_nutrition_per_100g") or {}).get("fat_g")
                    sodium_val = (b1.get("normalized_nutrition_per_100g") or {}).get("sodium_mg")
                nova_val = trace.get("nova_proxy")
                name_val = (trace.get("input_reference") or {}).get("product_name_he") or trace.get("canonical_name_he", "")
                before_after.append({
                    "barcode": bc,
                    "name": name_val,
                    "nova": nova_val,
                    "fat_g": fat_val,
                    "sodium_mg": sodium_val,
                    "context_flag": trace.get("context_flag"),
                    "run003_score": old_score, "run003_grade": old_grade,
                    "run004_score": new_score, "run004_grade": new_grade,
                    "delta": round((new_score or 0) - (old_score or 0), 2),
                })
    before_after.sort(key=lambda x: abs(x.get("delta", 0)), reverse=True)

    # -----------------------------------------------------------------------
    # Acceptance tests: same pairs as run_003
    # -----------------------------------------------------------------------
    acceptance_pairs = []

    def ap(bc_clean, bc_processed, label):
        t_clean = trace_by_barcode.get(bc_clean)
        t_proc  = trace_by_barcode.get(bc_processed)
        if t_clean and t_proc:
            s_clean = t_clean.get("final_score_estimate")
            s_proc  = t_proc.get("final_score_estimate")
            g_clean = t_clean.get("grade_estimate")
            g_proc  = t_proc.get("grade_estimate")
            nova_clean = t_clean.get("nova_proxy")
            nova_proc  = t_proc.get("nova_proxy")
            passes = (s_clean is not None and s_proc is not None and s_clean > s_proc)
            acceptance_pairs.append({
                "label": label,
                "clean_bc": bc_clean, "clean_score": s_clean, "clean_grade": g_clean, "clean_nova": nova_clean,
                "processed_bc": bc_processed, "processed_score": s_proc, "processed_grade": g_proc, "processed_nova": nova_proc,
                "nova1_above_nova3": passes,
                "delta": round((s_clean - s_proc), 2) if (s_clean and s_proc) else None,
            })
        else:
            acceptance_pairs.append({"label": label, "error": "barcode not found"})

    ap("2107798", "7290114312707", "NOVA1_5pct_bulgarian_vs_NOVA3_16pct_bulgarian_pin_break")
    ap("7290108509106", "369617", "NOVA1_13pct_bulgarian_vs_NOVA3_feta_oil")
    ap("2107798", "2385455", "NOVA3_5pct_bulgarian_vs_NOVA3_24pct_bulgarian_sodium_effect")
    ap("7290108509106", "7290017065236", "NOVA1_13pct_low_sodium_vs_NOVA1_24pct_high_sodium")

    all_acceptance_pass = all(p.get("nova1_above_nova3", False) for p in acceptance_pairs if "error" not in p)

    # Top/bottom
    traces_scored = [t for t in traces if t.get("final_score_estimate") is not None]
    traces_sorted_desc = sorted(traces_scored, key=lambda t: t.get("final_score_estimate", 0), reverse=True)

    def extract_drivers(t):
        pens = t.get("penalties_applied", []) or []
        caps = t.get("caps_applied", []) or []
        drivers = []
        for p in pens[:2]:
            drivers.append(f"-{p.get('amount','?')} {p.get('rule','?')}")
        for c in caps[:2]:
            if c.get("cap"):
                drivers.append(f"cap={c.get('cap','?')} {c.get('rule','?')}")
        return drivers or ["(no drivers)"]

    def trace_summary(t):
        bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode")
        name = (t.get("input_reference") or {}).get("product_name_he") or t.get("canonical_name_he")
        return {
            "barcode": bc, "name": name,
            "score": t.get("final_score_estimate"),
            "grade": t.get("grade_estimate"),
            "nova": t.get("nova_proxy"),
            "context_flag": t.get("context_flag"),
            "binding_cap": t.get("binding_cap"),
            "drivers": extract_drivers(t),
        }

    top3    = [trace_summary(t) for t in traces_sorted_desc[:3]]
    bottom3 = [trace_summary(t) for t in traces_sorted_desc[-3:]]

    # -----------------------------------------------------------------------
    # RT-2 / RT-6 check: bc-035 and bc-045 marketing copy removed
    # -----------------------------------------------------------------------
    rt2_fixed_count = 0
    rt2_products = []
    for bc in ["7290114310550", "2107071"]:
        t = trace_by_barcode.get(bc)
        if t:
            bsip1_f = BSIP1_REUSE_DIR / f"bsip1_brinedcheese_{bc}.json"
            b1 = json.loads(bsip1_f.read_text(encoding="utf-8")) if bsip1_f.exists() else {}
            quality = b1.get("ingredient_text_quality", "unknown")
            ing_null = b1.get("ingredients_text_he") is None
            if quality == "marketing_bleed" and ing_null:
                rt2_fixed_count += 1
            rt2_products.append({
                "barcode": bc,
                "ingredient_text_quality": quality,
                "ingredients_null": ing_null,
                "score": t.get("final_score_estimate"),
                "grade": t.get("grade_estimate"),
            })

    # -----------------------------------------------------------------------
    # Run record
    # -----------------------------------------------------------------------
    eval_scope_sha = sha256_file(pathlib.Path(__file__).parent / "evaluation_scope.py")

    run_record = {
        "run_id":           RUN_ID,
        "task":             "brined-sodium-protein-run005",
        "category_slug":    "brined-cheeses",
        "category_context": "dairy_protein",
        "generated":        ts,
        "engine":           "proto_v0 / score_engine.py — EV-052addendum + EV-053 + EV-054 + EV-055 + EV-056 + EV-057",
        "ev_applied":       ["EV-052_addendum", "EV-053", "EV-054", "EV-055", "EV-056", "EV-057"],
        "flag_config": {
            "BARI_RECAL_P0":             "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "off",
            "BARI_GRAD_SODIUM_V1":       "on",
            "BARI_REDLABEL_V1":          "off",
            "BARI_SODIUM_CEREAL":        "off",
            "BARI_TASK144_FIXES":        "off",
            "BARI_TASK250_CONF":         "off",
            "BARI_GLASSBOX_D5D6":        "off",
            "BARI_GLASSBOX_W15":         "off",
            "BARI_GLASSBOX_W2":          "off",
            "BARI_GLASSBOX_W4":          "on (default)",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "on",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "on",
        },
        "changes_from_run003": [
            "BSIP1 source: run_brined_cheeses_002 (hygiene-cleaned — marketing copy nulled for bc-035/bc-045; scrape artifacts stripped; typos fixed; bc-001 name corrected)",
            "evaluation_scope.py: brined_food keyword list extended with construct forms 'גבינת מלוחה', 'גבינת עזים', 'גבינת כבשים' (EV-052 addendum, RT-1 vocabulary fix)",
        ],
        "evaluation_scope_sha256": eval_scope_sha,
        "off_used":         False,
        "corpus_source":    str(CORPUS_FILE),
        "bsip0_source":     str(BSIP0_FILE),
        "in_scored_count":  len(in_scored_barcodes),
        "bsip1_source":     str(BSIP1_REUSE_DIR),
        "bsip1": {
            "records_loaded": len(bsip1_records),
            "note": "run_brined_cheeses_002 — hygiene-cleaned corpus (RT-1/2/6/9/10/11 fixes)",
        },
        "bsip2": {
            "output_dir": str(BSIP2_OUTPUT),
            "scored":     len(traces),
            "errors":     len(score_errors),
        },
        "score_distribution": {
            "min":       score_min,
            "max":       score_max,
            "median":    median,
            "stdev":     score_stdev,
            "range":     round(score_range, 2) if score_range else None,
            "histogram": histogram,
            "grade_dist": grade_dist,
        },
        "routing_distribution": routing_cats,
        "rt1_bc048": bc048_summary,
        "rt2_marketing_fix": {
            "fixed_count": rt2_fixed_count,
            "products": rt2_products,
        },
        "brined_flag": {
            "fired_count":     len(brined_flag_fired),
            "not_fired_count": len(brined_flag_not_fired),
            "not_fired_list":  brined_flag_not_fired,
        },
        "sodium_grad_fired": {
            "count": len(sodium_grad_fired),
            "list":  sodium_grad_fired[:10],
        },
        "acceptance_test": {
            "all_pass": all_acceptance_pass,
            "pairs":    acceptance_pairs,
        },
        "before_after_run003": before_after,
        "top3":    top3,
        "bottom3": bottom3,
        "errors":  score_errors,
        "self_check": {
            "rt1_bc048_fixed": rt1_fixed,
            "rt2_marketing_nulled": rt2_fixed_count,
            "off_used": False,
        },
    }


    # Verification table (return contract rule 7)
    verify_path = BSIP2_OUTPUT / "verification_table.csv"
    with verify_path.open("w", encoding="utf-8", newline="") as vf:
        vf.write("barcode,score,grade,binding_caps,nova,fat,sodium,context_flag" + chr(10))
        for t in sorted(traces, key=lambda x: str(x.get("barcode") or "")):
            bc = t.get("barcode") or (t.get("input_reference") or {}).get("barcode") or ""
            nn = (t.get("input_reference") or {}).get("normalized_nutrition_per_100g") or {}
            if not nn:
                for doc in bsip1_records:
                    if str(doc.get("barcode")) == str(bc):
                        nn = doc.get("normalized_nutrition_per_100g") or {}
                        break
            fat = nn.get("fat_g")
            sod = nn.get("sodium_mg")
            caps = t.get("binding_cap")
            vf.write(
                f"{bc},{t.get('final_score_estimate')},{t.get('grade_estimate')},"
                f"{caps},{t.get('nova_proxy')},{fat},{sod},{t.get('context_flag')}" + chr(10)
            )
    run_record["SHELF_SODIUM_MEDIAN_MG"] = shelf_median
    run_record["SHELF_SODIUM_STDEV_MG"] = shelf_stdev
    run_record["verification_table"] = str(verify_path)

    run_record_path = BSIP2_OUTPUT / "run_record.json"
    run_record_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record: %s", run_record_path)

    # -----------------------------------------------------------------------
    # Console report
    # -----------------------------------------------------------------------
    print("\n" + "="*70)
    print(f"BRINED CHEESES BSIP2 RUN — {RUN_ID}")
    print("EV-056 shelf-relative sodium + EV-057 dairy_protein reweight (run_brined_cheeses_002)")
    print("="*70)
    print()
    print(f"Corpus: {len(in_scored_barcodes)} IN_SCORED | BSIP1: {len(bsip1_records)}")
    print(f"BSIP2 scored: {len(traces)} | errors: {len(score_errors)}")
    print()
    print("ROUTING DISTRIBUTION:")
    for cat, cnt in sorted(routing_cats.items()):
        print(f"  {cat}: {cnt}")
    print()
    print("SCORE DISTRIBUTION:")
    print(f"  Min: {score_min}  Max: {score_max}  Median: {median}  StDev: {score_stdev}")
    print(f"  Range: {score_range:.1f} pts")
    print(f"  Histogram: {dict(sorted(histogram.items()))}")
    print(f"  Grade distribution: {dict(sorted(grade_dist.items()))}")
    print()
    print("RT-1 FIX CHECK (bc-048, barcode 3075805):")
    if bc048_trace:
        print(f"  context_flag: {bc048_summary.get('context_flag')} (was: null)")
        print(f"  score: {bc048_summary.get('score_run004')} (was: 39.0)")
        print(f"  grade: {bc048_summary.get('grade_run004')} (was: D)")
        print(f"  drivers: {bc048_summary.get('drivers')}")
        print(f"  RT-1 FIXED: {bc048_summary.get('rt1_fixed')}")
    else:
        print("  ERROR: bc-048 trace not found")
    print()
    print("RT-2/RT-6 FIX CHECK (bc-035 7290114310550, bc-045 2107071):")
    for rp in rt2_products:
        print(f"  {rp['barcode']}: quality={rp['ingredient_text_quality']} null={rp['ingredients_null']} score={rp['score']}/{rp['grade']}")
    print()
    print("ACCEPTANCE TESTS:")
    for ap_r in acceptance_pairs:
        if "error" in ap_r:
            print(f"  ERROR [{ap_r['label']}]: {ap_r['error']}")
        else:
            status = "PASS" if ap_r.get("nova1_above_nova3") else "FAIL"
            print(f"  [{status}] {ap_r['label']} delta={ap_r.get('delta','?')}")
    print(f"  OVERALL: {'PASS' if all_acceptance_pass else 'FAIL'}")
    print()
    print("BEFORE/AFTER run_003 vs run_004 (changed products):")
    for ba in before_after[:10]:
        print(f"  {ba['barcode']} {ba['run003_score']}/{ba['run003_grade']} -> {ba['run004_score']}/{ba['run004_grade']}  delta={ba.get('delta',0):+.2f}")
    print()
    print("TOP 3:")
    for i, p in enumerate(top3, 1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {p.get('name','?')[:50]}")
    print()
    print("BOTTOM 3:")
    for i, p in enumerate(bottom3, 1):
        print(f"  {i}. [{p['score']}/{p['grade']}] {p.get('name','?')[:50]}")
    print()
    print(f"evaluation_scope.py SHA256: {eval_scope_sha[:16]}...")
    print(f"Run record: {run_record_path}")
    print(f"BSIP2 dir:  {BSIP2_OUTPUT}")
    print("="*70)

    return run_record


if __name__ == "__main__":
    main()
