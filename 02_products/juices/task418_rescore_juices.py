# -*- coding: utf-8 -*-
"""
TASK-418 Juices Re-score — after ingredient cleaning.
Run ID: run_juices_task418_clean

Same flag stack as the live run (run_task389_rescore_002 / run_juices_shelfrel_001):
  BARI_SHELF_RELATIVE_V1=on
  BARI_FAT_TECH_V1=on
  BARI_RECAL_P0=on
  BARI_D4_SCORE_V1=on
  BARI_TASK144_FIXES=off
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_GRAD_SODIUM_V1=off

Corpus: C:\\Bari\\02_products\\juices\\bsip1_outputs (TASK-418 cleaned)
"""
import os, sys

os.environ["BARI_SHELF_RELATIVE_V1"]          = "on"
os.environ["BARI_FAT_TECH_V1"]                = "on"
os.environ["BARI_RECAL_P0"]                   = "on"
os.environ["BARI_D4_SCORE_V1"]                = "on"
os.environ["BARI_TASK144_FIXES"]              = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"]   = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"]  = "off"
os.environ["BARI_REDLABEL_V1"]                = "off"
os.environ["BARI_SODIUM_CEREAL"]              = "off"
os.environ["BARI_GRAD_SODIUM_V1"]             = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Verify flags BEFORE any engine import
REQUIRED_FLAGS = {
    "BARI_SHELF_RELATIVE_V1":        "on",
    "BARI_FAT_TECH_V1":              "on",
    "BARI_RECAL_P0":                 "on",
    "BARI_D4_SCORE_V1":              "on",
    "BARI_TASK144_FIXES":            "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
    "BARI_REDLABEL_V1":              "off",
    "BARI_SODIUM_CEREAL":            "off",
    "BARI_GRAD_SODIUM_V1":           "off",
}
for k, v in REQUIRED_FLAGS.items():
    actual = os.environ.get(k, "off").lower()
    if actual != v.lower():
        print(f"ABORT: env {k}={actual!r} but expected {v!r}", flush=True)
        sys.exit(2)

print("ENV CHECK PASS: all flags confirmed before engine import", flush=True)

import json, pathlib, logging, datetime, shutil

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals, TASK144_FIXES_ON as SE_TASK144
from score_engine import (
    score_product, set_shelf_stats, clear_shelf_stats,
    TASK144_FIXES_ON as SE_TASK144_ENGINE,
    RECAL_P0_ON,
)
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# Runtime flag check
print(f"\nRUNTIME FLAG VERIFICATION:", flush=True)
print(f"  signal_extractor.TASK144_FIXES_ON = {SE_TASK144}  (expected False)", flush=True)
print(f"  score_engine.TASK144_FIXES_ON     = {SE_TASK144_ENGINE}  (expected False)", flush=True)
print(f"  score_engine.RECAL_P0_ON          = {RECAL_P0_ON}  (expected True)", flush=True)

if SE_TASK144 is not False:
    print("ABORT: signal_extractor.TASK144_FIXES_ON is True", flush=True)
    sys.exit(3)
if SE_TASK144_ENGINE is not False:
    print("ABORT: score_engine.TASK144_FIXES_ON is True", flush=True)
    sys.exit(3)
if RECAL_P0_ON is not True:
    print("ABORT: score_engine.RECAL_P0_ON is False", flush=True)
    sys.exit(3)

print("RUNTIME FLAG CHECK PASS\n", flush=True)

BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")
OUTPUT_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_juices_task418_clean")
RUN_ID     = "run_juices_task418_clean"

SHELF_NUTRIENT = "sugars_g"
SHELF_MEDIAN   = 9.5
SHELF_SCALE    = 2.82
SHELF_TYPE     = "iqr"

DISPLAY_BARCODES = {
    "7290000525969",  # jc-001  מיץ תפוזים סחוט 1 ליטר
    "7290003009640",  # jc-002  סחוט תפוז 1 ליטר
    "7290004030100",  # jc-003  100% מיץ תפוזים ולנסיה סחוט
    "7290013153395",  # jc-005  סחוט 1 ליטר רימונים
    "7290013608260",  # jc-006  מיץ רימונים 100% סחוט
    "7290110114886",  # jc-011  סחוט קלמנטינה 2 ליטר
    "7290008690713",  # jc-017  מיץ חמוציות 1 ליטר
    "7290006822192",  # jc-019  מיץ חמוציות דיאט 1 ליטר
    "7290019056720",  # jc-018  קריסטל מיץ ענבים 2 ליטר
    "7290000136523",  # jc-020  ג'אמפ ענבים 1.5 ליטר
    "7290001247891",  # jc-021  ספרינג נקטר אפרסקים
    "7290001247723",  # jc-022  ספרינג נקטר תות בננה
    "7290001247730",  # jc-024  ספרינג נקטר מנגו
    "7290019056355",  # jc-025  תפוזינה לימונענע 1.5 ליטר
    "7290019056591",  # jc-026  ספרינג ענבים 1.5 ליטר
    "7290019056737",  # jc-023  קריסטל מיץ אשכולית 2 ליטר
    "7290013153418",  # jc-027  סחוט לימונענע 1 ליטר
}

ID_MAP = {
    "7290000525969": "jc-001", "7290003009640": "jc-002", "7290004030100": "jc-003",
    "7290013153395": "jc-005", "7290013608260": "jc-006", "7290110114886": "jc-011",
    "7290008690713": "jc-017", "7290006822192": "jc-019", "7290019056720": "jc-018",
    "7290000136523": "jc-020", "7290001247891": "jc-021", "7290001247723": "jc-022",
    "7290001247730": "jc-024", "7290019056355": "jc-025", "7290019056591": "jc-026",
    "7290019056737": "jc-023", "7290013153418": "jc-027",
}

LIVE_SCORES = {
    "7290000525969": (85.0, "A"), "7290003009640": (85.0, "A"),
    "7290004030100": (85.0, "A"), "7290013153395": (85.0, "A"),
    "7290013608260": (85.0, "A"), "7290110114886": (85.0, "A"),
    "7290008690713": (49.1, "D"), "7290006822192": (39.9, "D"),
    "7290019056720": (39.8, "D"), "7290000136523": (38.1, "D"),
    "7290001247891": (37.4, "D"), "7290001247723": (36.9, "D"),
    "7290001247730": (35.4, "D"), "7290019056355": (33.4, "E"),
    "7290019056591": (33.3, "E"), "7290019056737": (30.3, "E"),
    "7290013153418": (28.5, "E"),
}

# 6 single-ingredient juices that must be 85/A
SINGLE_INGREDIENT_BARCODES = {
    "7290000525969", "7290003009640", "7290004030100",
    "7290013153395", "7290013608260", "7290110114886",
}

# 3 excluded juice barcodes (untouched by cleaning)
EXCLUDED_BARCODES = {
    "7290013153395",
    "7290110114886",
    "7290003009640",
}


def run_pipeline(product):
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace       = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    try:
        trace["structural_class"] = classify_structural_class(trace)
    except Exception:
        trace["structural_class"] = None
    return trace


def main():
    log.info("=== TASK-418 Juices Re-score after ingredient cleaning ===")
    log.info("Run ID: %s", RUN_ID)

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source not found: %s", BSIP1_DIR)
        sys.exit(1)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "products").mkdir(parents=True, exist_ok=True)

    # Load BSIP1, filter to display set
    all_products = load_batch(BSIP1_DIR)
    log.info("Loaded %d BSIP1 records", len(all_products))

    products = [p for p in all_products if str(p.get("barcode", "")) in DISPLAY_BARCODES]
    found_barcodes = {str(p.get("barcode","")) for p in products}
    missing = DISPLAY_BARCODES - found_barcodes
    if missing:
        log.error("MISSING BARCODES from BSIP1: %s", missing)
        sys.exit(1)

    log.info("Products after display-set filter: %d (expected 17)", len(products))
    assert len(products) == 17, f"Expected 17, got {len(products)}"

    set_shelf_stats(SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE, SHELF_TYPE)
    log.info("shelf stats activated: %s median=%.2f scale=%.4f", SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE)

    traces, errors = [], []
    run_start = datetime.datetime.now(datetime.timezone.utc)

    for product in products:
        bc  = str(product.get("barcode", ""))
        nm  = product.get("canonical_name_he", "")[:50]
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_DIR)
            score  = trace.get("final_score_estimate")
            grade  = trace.get("grade_estimate")
            nova   = trace.get("nova_proxy")
            floors = trace.get("floors_applied", [])
            log.info("  OK  %s  %s  score=%.1f/%s  nova=%s  floors=%s  %s",
                     bc, ID_MAP.get(bc,"?"), score, grade, nova, floors, nm)
            traces.append(trace)
        except Exception as e:
            import traceback as _tb
            log.error("  FAIL  %s: %s", bc, e)
            _tb.print_exc()
            errors.append({"barcode": bc, "error": str(e)})

    clear_shelf_stats(SHELF_NUTRIENT)
    log.info("shelf stats cleared")
    log.info("Processed: %d  Errors: %d", len(traces), len(errors))

    # Acceptance self-check: 6 single-ingredient juices must be 85/A
    print("\n=== ACCEPTANCE SELF-CHECK: 6 single-ingredient juices ===", flush=True)
    si_pass = True
    for t in traces:
        ir  = t.get("input_reference") or {}
        bc  = str(ir.get("barcode", "") or "")
        if bc not in SINGLE_INGREDIENT_BARCODES:
            continue
        nova_val  = t.get("nova_proxy")
        floors_a  = t.get("floors_applied", [])
        score_val = t.get("final_score_estimate")
        grade_val = t.get("grade_estimate")
        nova_ok   = (nova_val == 1)
        floor_ok  = any(
            (isinstance(f, str) and "nova1" in f.lower()) or
            (isinstance(f, dict) and "nova1" in str(f).lower())
            for f in floors_a
        )
        score_ok = (score_val == 85)
        grade_ok = (grade_val == "A")
        status = "PASS" if (nova_ok and floor_ok and score_ok and grade_ok) else "FAIL"
        if status == "FAIL":
            si_pass = False
        excl = " [excluded-from-cleaning]" if bc in EXCLUDED_BARCODES else ""
        nm = (ir.get("product_name_he") or "")[:45]
        print(f"  {status}  {bc}  nova={nova_val}(ok={nova_ok})  floor={floor_ok}  "
              f"score={score_val}  grade={grade_val}{excl}  {nm}", flush=True)

    if not si_pass:
        print("ACCEPTANCE SELF-CHECK FAILED — check nova/floor logic.", flush=True)
        sys.exit(4)
    else:
        print("ACCEPTANCE SELF-CHECK PASSED — all 6 single-ingredient juices: 85/A\n", flush=True)

    # Build results table
    fresh_dist: dict = {}
    live_dist:  dict = {}
    score_movers, grade_movers = [], []
    results_table = []

    for t in traces:
        ir      = t.get("input_reference") or {}
        bc      = str(ir.get("barcode", "") or "")
        jc_id   = ID_MAP.get(bc, "?")
        nm_he   = (ir.get("product_name_he") or "")
        fscore  = t.get("final_score_estimate")
        fgrade  = t.get("grade_estimate")
        nova_v  = t.get("nova_proxy")
        floors_a= t.get("floors_applied", [])
        live_s, live_g = LIVE_SCORES.get(bc, (None, None))

        if any(
            (isinstance(f, str) and "nova1" in f.lower()) or
            (isinstance(f, dict) and "nova1" in str(f).lower())
            for f in floors_a
        ):
            driver = "floor:nova1_single_ingredient"
        else:
            driver = "weighted_dims_only"

        delta = round(fscore - live_s, 2) if (fscore is not None and live_s is not None) else None
        grade_moved = (fgrade != live_g) if (fgrade and live_g) else False

        fresh_dist[fgrade] = fresh_dist.get(fgrade, 0) + 1
        live_dist[live_g]  = live_dist.get(live_g, 0) + 1

        if delta is not None and abs(delta) >= 0.05:
            score_movers.append({"barcode": bc, "id": jc_id, "live_score": live_s,
                                  "fresh_score": round(fscore, 2), "delta": delta})
        if grade_moved:
            grade_movers.append({"barcode": bc, "id": jc_id, "name": nm_he[:50],
                                  "live": f"{live_s}/{live_g}", "fresh": f"{fscore}/{fgrade}"})

        excluded_from_cleaning = bc in EXCLUDED_BARCODES
        results_table.append({
            "barcode": bc, "id": jc_id, "name": nm_he,
            "live_score": live_s, "live_grade": live_g,
            "fresh_score": round(fscore, 2) if fscore is not None else None,
            "fresh_grade": fgrade,
            "delta": delta,
            "grade_moved": grade_moved,
            "nova_proxy": nova_v,
            "floors_applied": floors_a,
            "driver": driver,
            "excluded_from_cleaning": excluded_from_cleaning,
        })

    results_table.sort(key=lambda r: (r["fresh_score"] or 0), reverse=True)
    run_end = datetime.datetime.now(datetime.timezone.utc)

    print("\n=== 17-PRODUCT RESULTS TABLE ===", flush=True)
    print(f"{'barcode':<15} {'id':<8} {'live':>9} {'fresh':>9} {'delta':>7}  {'gm':>3}  {'driver'}", flush=True)
    for r in results_table:
        gm = "YES" if r["grade_moved"] else "no"
        excl = "*" if r["excluded_from_cleaning"] else " "
        print(f"{r['barcode']:<15}{excl}{r['id']:<8} {str(r['live_score'])+'/'+str(r['live_grade']):>9} "
              f"{str(r['fresh_score'])+'/'+str(r['fresh_grade']):>9} {str(r['delta']):>7}  {gm:>3}  {r['driver']}", flush=True)

    print(f"\nLive distribution:  {dict(sorted(live_dist.items()))}", flush=True)
    print(f"Fresh distribution: {dict(sorted(fresh_dist.items()))}", flush=True)
    print(f"Score movers: {len(score_movers)}  Grade movers: {len(grade_movers)}", flush=True)
    if grade_movers:
        print("GRADE MOVERS:", flush=True)
        for gm in grade_movers:
            print(f"  {gm}", flush=True)

    # Verification table
    vt = [{
        "barcode": r["barcode"], "id": r["id"], "name": r["name"],
        "live_score": r["live_score"], "live_grade": r["live_grade"],
        "fresh_score": r["fresh_score"], "fresh_grade": r["fresh_grade"],
        "delta": r["delta"], "grade_moved": r["grade_moved"],
        "excluded_from_cleaning": r["excluded_from_cleaning"],
    } for r in results_table]

    vt_path = OUTPUT_DIR / "verification_table.json"
    vt_path.write_text(json.dumps(vt, ensure_ascii=False, indent=2), encoding="utf-8")

    run_record = {
        "run_id": RUN_ID,
        "task": "TASK-418",
        "generated": run_end.isoformat(),
        "run_start": run_start.isoformat(),
        "flags": {k: v for k, v in REQUIRED_FLAGS.items()},
        "shelf_stats": {"nutrient": SHELF_NUTRIENT, "median": SHELF_MEDIAN,
                        "scale": SHELF_SCALE, "scale_type": SHELF_TYPE},
        "corpus": {"bsip1_dir": str(BSIP1_DIR), "display_barcodes": sorted(DISPLAY_BARCODES),
                   "products_scored": len(traces), "errors": len(errors)},
        "live_grade_distribution": dict(sorted(live_dist.items())),
        "fresh_grade_distribution": dict(sorted(fresh_dist.items())),
        "score_movers_count": len(score_movers),
        "grade_movers_count": len(grade_movers),
        "grade_movers": grade_movers,
        "score_movers": score_movers,
        "acceptance_check": {
            "single_ingredient_barcodes": sorted(SINGLE_INGREDIENT_BARCODES),
            "pass": si_pass,
            "excluded_from_cleaning": sorted(EXCLUDED_BARCODES),
        },
        "results": results_table,
        "errors": errors,
        "off_used": False,
    }

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record written: %s", rr_path)

    if errors:
        log.error("Run completed with %d errors", len(errors))
        sys.exit(5)


if __name__ == "__main__":
    main()
