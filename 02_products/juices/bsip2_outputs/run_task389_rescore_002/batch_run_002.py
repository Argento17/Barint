# -*- coding: utf-8 -*-
"""
TASK-389 Re-run 002 — Juices 17-product rescore (CLEAN)
Purpose: Produce verified traces for the 17 display products with the EXACT live
         config flags. Replaces the contaminated run_task389_rescore_001 traces.

Env-before-import guarantee: This script is invoked as a fresh subprocess by
run_task389_launch.py after setting all env vars in the subprocess environment,
so no module has been imported with wrong flag values. We also verify at runtime
that the imported module's flag values are what we expect and ABORT if not.

Live config (juices.json):
  BARI_SHELF_RELATIVE_V1=on
  BARI_FAT_TECH_V1=on
  BARI_RECAL_P0=on
  BARI_TASK144_FIXES=off      <-- CRITICAL: must be off
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_GRAD_SODIUM_V1=off

Shelf stats (juices.json + EV-091):
  nutrient=sugars_g  median=9.5  scale=2.82  scale_type=iqr

17 display products = live juices_frontend_v3.json product set (17 barcodes).
Live run_id: run_juices_shelfrel_001 (batch_run_shelfrel_golive_001.py).
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── STEP 0: Verify env vars are set BEFORE any engine import ──────────────────
# The launcher sets these in os.environ before calling this script as subprocess.
# Belt-and-suspenders: assert them here too.
REQUIRED_FLAGS = {
    "BARI_SHELF_RELATIVE_V1": "on",
    "BARI_FAT_TECH_V1": "on",
    "BARI_RECAL_P0": "on",
    "BARI_TASK144_FIXES": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
    "BARI_GRAD_SODIUM_V1": "off",
}
for k, v in REQUIRED_FLAGS.items():
    actual = os.environ.get(k, "off").lower()
    if actual != v.lower():
        print(f"ABORT: env {k}={actual!r} but expected {v!r} — env-before-import not guaranteed", flush=True)
        sys.exit(2)

print("ENV CHECK PASS: all flags confirmed in os.environ before engine import", flush=True)
for k, v in REQUIRED_FLAGS.items():
    print(f"  {k}={os.environ.get(k, '<unset>')}", flush=True)

# ── STEP 1: Add engine src to path and import engine modules ──────────────────
import json, pathlib, logging, datetime, hashlib

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

# ── STEP 2: Runtime flag verification — confirm imported modules loaded correct values ──
print(f"\nRUNTIME FLAG VERIFICATION:", flush=True)
print(f"  signal_extractor.TASK144_FIXES_ON = {SE_TASK144}  (expected False)", flush=True)
print(f"  score_engine.TASK144_FIXES_ON     = {SE_TASK144_ENGINE}  (expected False)", flush=True)
print(f"  score_engine.RECAL_P0_ON          = {RECAL_P0_ON}  (expected True)", flush=True)

if SE_TASK144 is not False:
    print("ABORT: signal_extractor.TASK144_FIXES_ON is True — env-before-import failed!", flush=True)
    sys.exit(3)
if SE_TASK144_ENGINE is not False:
    print("ABORT: score_engine.TASK144_FIXES_ON is True — env-before-import failed!", flush=True)
    sys.exit(3)
if RECAL_P0_ON is not True:
    print("ABORT: score_engine.RECAL_P0_ON is False — BARI_RECAL_P0 not set!", flush=True)
    sys.exit(3)

print("RUNTIME FLAG CHECK PASS: all module-level flags confirmed correct after import\n", flush=True)

# ── STEP 3: Constants ─────────────────────────────────────────────────────────
BSIP1_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip1_outputs")
OUTPUT_DIR = pathlib.Path(r"C:\Bari\02_products\juices\bsip2_outputs\run_task389_rescore_002")
RUN_ID = "run_task389_rescore_002"
TASK_REF = "TASK-389"

# The 17 display barcodes from live juices_frontend_v3.json (grade_distribution A6/D7/E4)
DISPLAY_BARCODES = {
    "7290000525969",  # jc-001  מיץ תפוזים סחוט 1 ליטר                        live=85.0/A
    "7290003009640",  # jc-002  סחוט תפוז 1 ליטר                               live=85.0/A
    "7290004030100",  # jc-003  100% מיץ תפוזים ולנסיה סחוט 1 ליטר פריני      live=85.0/A  (THE BUG PRODUCT)
    "7290013153395",  # jc-005  סחוט 1 ליטר רימונים                            live=85.0/A
    "7290013608260",  # jc-006  מיץ רימונים 100%מיץ סחוט טרי מצונן 1ליט       live=85.0/A
    "7290110114886",  # jc-011  סחוט קלמנטינה 2 ליטר                           live=85.0/A
    "7290008690713",  # jc-017  מיץ חמוציות 1 ליטר                             live=49.1/D
    "7290006822192",  # jc-019  מיץ חמוציות דיאט 1 ליטר                       live=39.9/D
    "7290019056720",  # jc-018  קריסטל מיץ ענבים 2 ליטר                       live=39.8/D
    "7290000136523",  # jc-020  ג'אמפ ענבים 1.5 ליטר                          live=38.1/D
    "7290001247891",  # jc-021  ספרינג נקטר אפרסקים פחית 330 מ"ל              live=37.4/D
    "7290001247723",  # jc-022  ספרינג נקטר תות בננה פחית 330 מ"ל            live=36.9/D
    "7290001247730",  # jc-024  ספרינג נקטר מנגו פחית 330 מ"ל                live=35.4/D
    "7290019056355",  # jc-025  תפוזינה לימונענע 1.5 ליטר                     live=33.4/E
    "7290019056591",  # jc-026  ספרינג ענבים 1.5 ליטר                         live=33.3/E
    "7290019056737",  # jc-023  קריסטל מיץ אשכולית 2 ליטר                    live=30.3/E
    "7290013153418",  # jc-027  סחוט לימונענע 1 ליטר                          live=28.5/E
}

# ID mapping (from live frontend JSON)
ID_MAP = {
    "7290000525969": "jc-001", "7290003009640": "jc-002", "7290004030100": "jc-003",
    "7290013153395": "jc-005", "7290013608260": "jc-006", "7290110114886": "jc-011",
    "7290008690713": "jc-017", "7290006822192": "jc-019", "7290019056720": "jc-018",
    "7290000136523": "jc-020", "7290001247891": "jc-021", "7290001247723": "jc-022",
    "7290001247730": "jc-024", "7290019056355": "jc-025", "7290019056591": "jc-026",
    "7290019056737": "jc-023", "7290013153418": "jc-027",
}

# Live scores for delta computation (from juices_frontend_v3.json)
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

# Shelf stats (from juices.json + EV-091)
SHELF_NUTRIENT = "sugars_g"
SHELF_MEDIAN   = 9.5
SHELF_SCALE    = 2.82
SHELF_TYPE     = "iqr"

# 6 single-ingredient juices that must be 85/A with nova_proxy=1 + floor=nova1_single_ingredient
SINGLE_INGREDIENT_BARCODES = {
    "7290000525969", "7290003009640", "7290004030100",
    "7290013153395", "7290013608260", "7290110114886",
}


def run_pipeline(product: dict) -> dict:
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
    log.info("=== TASK-389 Re-run 002 — Juices 17-product rescore (CLEAN) ===")
    log.info("Run ID: %s", RUN_ID)
    log.info("BARI_TASK144_FIXES=off  BARI_SHELF_RELATIVE_V1=on  BARI_FAT_TECH_V1=on  BARI_RECAL_P0=on")
    log.info("Shelf: nutrient=%s  median=%.2f  scale=%.4f  type=%s", SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE, SHELF_TYPE)
    log.info("Products: %d barcodes in display set", len(DISPLAY_BARCODES))

    if not BSIP1_DIR.exists():
        log.error("BSIP1 source not found: %s", BSIP1_DIR)
        sys.exit(1)

    # Create output dirs (do NOT wipe — fresh run dir)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prod_dir = OUTPUT_DIR / "products"
    prod_dir.mkdir(parents=True, exist_ok=True)

    # Load all BSIP1 products, filter to display set
    all_products = load_batch(BSIP1_DIR)
    log.info("Loaded %d BSIP1 records from %s", len(all_products), BSIP1_DIR)

    products = []
    for p in all_products:
        bc = str(p.get("barcode", "") or "")
        if bc in DISPLAY_BARCODES:
            products.append(p)

    found_barcodes = {str(p.get("barcode","")) for p in products}
    missing = DISPLAY_BARCODES - found_barcodes
    if missing:
        log.error("MISSING BARCODES from BSIP1: %s", missing)
        sys.exit(1)

    log.info("Products after display-set filter: %d (expected 17)", len(products))
    assert len(products) == 17, f"Expected 17, got {len(products)}"

    # Activate shelf-relative scoring
    set_shelf_stats(SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE, SHELF_TYPE)
    log.info("shelf stats activated: %s median=%.2f scale=%.4f", SHELF_NUTRIENT, SHELF_MEDIAN, SHELF_SCALE)

    traces, errors = [], []
    run_start = datetime.datetime.now(datetime.timezone.utc)

    for product in products:
        bc  = str(product.get("barcode", ""))
        pid = product.get("canonical_product_id", f"bsip1_juice_{bc}")
        nm  = product.get("canonical_name_he", "")[:50]
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_DIR)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            nova  = trace.get("nova_proxy")
            floors = trace.get("floors_applied", [])
            log.info("  OK  %s  %s  score=%.1f/%s  nova=%s  floors=%s  %s",
                     bc, ID_MAP.get(bc,"?"), score, grade, nova, floors, nm)
            traces.append(trace)
        except Exception as e:
            import traceback as _tb
            log.error("  FAIL  %s: %s", pid, e)
            _tb.print_exc()
            errors.append({"barcode": bc, "product_id": pid, "error": str(e)})

    clear_shelf_stats(SHELF_NUTRIENT)
    log.info("shelf stats cleared")

    log.info("Processed: %d  Errors: %d", len(traces), len(errors))

    # ── Acceptance self-check: 6 single-ingredient juices must be 85/A ─────────
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
        # Check nova=1 (ingredient_count must be >=1 for this to fire)
        ing_count = (t.get("L1_observed_signals") or {}).get("ingredient_count", 0)
        nova_ok   = (nova_val == 1)
        floor_ok  = any(
            (isinstance(f, str) and "nova1" in f.lower()) or
            (isinstance(f, dict) and "nova1" in str(f).lower())
            for f in floors_a
        )
        score_ok  = (score_val == 85)
        grade_ok  = (grade_val == "A")
        nm = (ir.get("product_name_he") or "")[:45]
        status = "PASS" if (nova_ok and floor_ok and score_ok and grade_ok) else "FAIL"
        if status == "FAIL":
            si_pass = False
        print(f"  {status}  {bc}  nova={nova_val}(ok={nova_ok})  "
              f"floor={floor_ok}  score={score_val}  grade={grade_val}  ing_count={ing_count}  {nm}",
              flush=True)

    if not si_pass:
        print("ACCEPTANCE SELF-CHECK FAILED — env-before-import may not have worked; "
              "check the floor logic. Do NOT accept this run.", flush=True)
        sys.exit(4)
    else:
        print("ACCEPTANCE SELF-CHECK PASSED — all 6 single-ingredient juices: nova=1 + floor + 85/A\n",
              flush=True)

    # ── Build run record ───────────────────────────────────────────────────────
    fresh_dist: dict[str, int] = {}
    live_dist:  dict[str, int] = {}
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

        # Derive driver label
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
            score_movers.append({
                "barcode": bc, "id": jc_id, "live_score": live_s,
                "fresh_score": round(fscore, 2), "delta": delta,
            })
        if grade_moved:
            grade_movers.append({
                "barcode": bc, "id": jc_id, "name": nm_he[:50],
                "live": f"{live_s}/{live_g}", "fresh": f"{fscore}/{fgrade}",
            })

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
        })

    results_table.sort(key=lambda r: (r["fresh_score"] or 0), reverse=True)
    score_movers.sort(key=lambda r: abs(r.get("delta") or 0), reverse=True)

    run_end = datetime.datetime.now(datetime.timezone.utc)

    # SHA-256 of all trace files for artifact integrity
    trace_sha = {}
    for fp in sorted((OUTPUT_DIR / "products").glob("**/bsip2_trace.json")):
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
        trace_sha[str(fp.relative_to(OUTPUT_DIR))] = h

    run_record = {
        "run_id": RUN_ID,
        "task": TASK_REF,
        "generated": run_end.isoformat(),
        "run_start": run_start.isoformat(),
        "note": (
            "Clean re-run. env-before-import verified: BARI_TASK144_FIXES=off confirmed "
            "at os.environ level AND at module attribute level before any product scored. "
            "Replaces contaminated run_task389_rescore_001 traces (where TASK144=on was "
            "active at import time, stripping single-ingredient list -> nova_proxy=2 -> "
            "no nova1 floor -> 55/C instead of 85/A for single-ingredient juices)."
        ),
        "engine_files": {
            "score_engine": "03_operations/bsip2/proto_v0/src/score_engine.py",
            "signal_extractor": "03_operations/bsip2/proto_v0/src/signal_extractor.py",
            "nova_proxy": "03_operations/bsip2/proto_v0/src/nova_proxy.py",
            "constants": "03_operations/bsip2/proto_v0/src/constants.py",
        },
        "flags": {k: v for k, v in REQUIRED_FLAGS.items()},
        "runtime_module_checks": {
            "signal_extractor.TASK144_FIXES_ON": SE_TASK144,
            "score_engine.TASK144_FIXES_ON": SE_TASK144_ENGINE,
            "score_engine.RECAL_P0_ON": RECAL_P0_ON,
        },
        "shelf_stats": {
            "nutrient": SHELF_NUTRIENT,
            "median": SHELF_MEDIAN,
            "scale": SHELF_SCALE,
            "scale_type": SHELF_TYPE,
            "source": "juices.json + EV-091 + run_task389_rescore_001 run_record confirmed",
        },
        "live_run_id": "run_juices_shelfrel_001",
        "corpus": {
            "bsip1_dir": str(BSIP1_DIR),
            "display_barcodes": sorted(DISPLAY_BARCODES),
            "products_scored": len(traces),
            "errors": len(errors),
        },
        "live_grade_distribution": dict(sorted(live_dist.items())),
        "fresh_grade_distribution": dict(sorted(fresh_dist.items())),
        "score_movers_count": len(score_movers),
        "grade_movers_count": len(grade_movers),
        "grade_movers": grade_movers,
        "score_movers": score_movers,
        "acceptance_check": {
            "single_ingredient_barcodes": sorted(SINGLE_INGREDIENT_BARCODES),
            "pass": si_pass,
            "required": "nova_proxy=1 AND floor:nova1_single_ingredient AND score=85 AND grade=A",
        },
        "results": results_table,
        "trace_sha256": trace_sha,
        "errors": errors,
        "off_used": False,
    }

    rr_path = OUTPUT_DIR / "run_record.json"
    rr_path.write_text(json.dumps(run_record, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Run record written: %s", rr_path)

    # Print summary table
    print("\n=== 17-PRODUCT RESULTS TABLE ===", flush=True)
    print(f"{'barcode':<15} {'id':<8} {'live':>9} {'fresh':>9} {'delta':>7}  {'gm':>3}  {'driver'}", flush=True)
    for r in results_table:
        gm = "YES" if r["grade_moved"] else "no"
        print(f"{r['barcode']:<15} {r['id']:<8} {str(r['live_score'])+'/'+str(r['live_grade']):>9} "
              f"{str(r['fresh_score'])+'/'+str(r['fresh_grade']):>9} {str(r['delta']):>7}  {gm:>3}  {r['driver']}",
              flush=True)

    print(f"\nLive distribution:  {dict(sorted(live_dist.items()))}", flush=True)
    print(f"Fresh distribution: {dict(sorted(fresh_dist.items()))}", flush=True)
    print(f"Score movers: {len(score_movers)}  Grade movers: {len(grade_movers)}", flush=True)
    if grade_movers:
        print("GRADE MOVERS:", flush=True)
        for gm in grade_movers:
            print(f"  {gm}", flush=True)
    if errors:
        print(f"ERRORS ({len(errors)}):", flush=True)
        for e in errors:
            print(f"  {e}", flush=True)

    print(f"\nRun record: {rr_path}", flush=True)
    print(f"Traces: {OUTPUT_DIR / 'products'}", flush=True)

    if errors:
        log.error("Run completed with %d errors", len(errors))
        sys.exit(5)


if __name__ == "__main__":
    main()
