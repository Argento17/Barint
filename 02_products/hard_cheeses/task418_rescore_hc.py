# -*- coding: utf-8 -*-
"""
Hard Cheeses TASK-418 — Re-score after ingredient cleaning.
Run ID: run_hc_task418_clean

Purpose: Re-score the 31-product curated HC corpus from the CLEANED bsip1_task412 files.
Same flag stack as task412_rt4_fix (the previous live run):
  BARI_SHELF_RELATIVE_V1  = on
  BARI_FAT_TECH_V1        = on
  BARI_RECAL_P0           = on
  BARI_REDLABEL_V1        = on
  BARI_HC_DAIRY_SATFAT_V1 = on
  BARI_DAIRY_SAT_FAT_INFER= on
  BARI_HC002_NOVA1        = off

Source corpus: C:\\Bari\\02_products\\hard_cheeses\\bsip1_task412 (TASK-418 cleaned)
"""

import os, sys

os.environ["BARI_SHELF_RELATIVE_V1"]        = "on"
os.environ["BARI_FAT_TECH_V1"]              = "on"
os.environ["BARI_RECAL_P0"]                 = "on"
os.environ["BARI_REDLABEL_V1"]              = "on"
os.environ["BARI_HC_DAIRY_SATFAT_V1"]       = "on"
os.environ["BARI_DAIRY_SAT_FAT_INFER"]      = "on"
os.environ["BARI_HC002_NOVA1"]              = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"]= "off"
os.environ["BARI_SODIUM_CEREAL"]            = "off"
os.environ["BARI_GRAD_SODIUM_V1"]           = "off"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json, pathlib, logging, datetime, shutil
from collections import Counter

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, set_shelf_stats, clear_shelf_stats
from trace_writer import assemble_trace, write_trace
from constants import (
    score_to_grade,
    FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
    FATSAT_SHELF_REL_HARDCHEESE_SCALE,
)
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_DIR  = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip1_task412")
OUTPUT_DIR = pathlib.Path(r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hc_task418_clean")
RUN_ID     = "run_hc_task418_clean"

# Curated 31-product barcodes (v3 corpus)
CURATED_31 = {
    "7290110324872", "7290004122348", "5384356", "52311", "4137311",
    "7290117265888", "7290116931524", "7290114312813", "7290114311601",
    "9150162", "7296073731856", "7290019635192", "5079665",
    "3073781199918", "7290004122195", "7290017065434", "8711528211138",
    "7290014760448", "7290014760912",
    "7290020467393", "7296073735151", "8606608", "8606974",
    "4122270", "7290110320850", "53219", "7290110323301", "7296073453482",
    "5079672", "5079658", "7290014455245",
}

# Live scores from hard_cheeses_frontend_v4.json for delta computation
# (curated 31 only — pulled from live frontend)
LIVE_SCORES = {
    "7290110324872": (93.2, "S"),
    "7290004122348": (78.5, "B"),
    "5384356":       (76.1, "B"),
    "52311":         (74.9, "B"),
    "4137311":       (74.8, "B"),
    "7290117265888": (74.5, "B"),
    "7290116931524": (73.5, "B"),
    "7290114312813": (73.2, "B"),
    "7290114311601": (72.8, "B"),
    "9150162":       (72.2, "B"),
    "7296073731856": (72.2, "B"),
    "7290019635192": (71.2, "B"),
    "5079665":       (70.8, "B"),
    "3073781199918": (70.0, "B"),
    "7290004122195": (69.9, "B"),
    "7290017065434": (69.7, "B"),
    "8711528211138": (69.3, "B"),
    "7290014760448": (68.8, "B"),
    "7290014760912": (68.4, "B"),
    "7290020467393": (67.5, "B"),
    "7296073735151": (66.9, "B"),
    "8606608":       (63.0, "C"),
    "8606974":       (63.0, "C"),
    "4122270":       (62.6, "C"),
    "7290110320850": (62.6, "C"),
    "53219":         (62.6, "C"),
    "7290110323301": (62.5, "C"),
    "7296073453482": (62.4, "C"),
    "5079672":       (62.2, "C"),
    "5079658":       (62.2, "C"),
    "7290014455245": (62.2, "C"),
}

OFF_MARKERS = ["open_food_facts", "openfoodfacts", "il_prices"]


def is_off_contaminated(doc):
    prov_str = json.dumps(doc.get("provenance", {})).lower()
    return any(m in prov_str for m in OFF_MARKERS)


def missing_data_discard(doc):
    nnn = doc.get("normalized_nutrition_per_100g") or {}
    sodium  = nnn.get("sodium_mg")
    fat     = nnn.get("fat_g")
    protein = nnn.get("protein_g")
    reasons = []
    if sodium is not None and float(sodium) < 100:
        reasons.append(f"R1_sodium_lt100 (sodium={sodium})")
    if sodium is None:
        reasons.append("R2_sodium_null")
    if fat is None:
        reasons.append("R3_fat_null")
    if protein is None:
        reasons.append("R4_protein_null")
    return bool(reasons), reasons


def score_one(doc):
    signals = extract_signals(doc)
    cat     = classify_category(doc)
    l3      = signals["L3_inferred_classifications"]
    nova    = infer_nova(doc, l3)
    ev      = assign_evaluation_scope(doc, cat["category"])
    sr      = score_product(doc, signals, cat, nova, ev)
    tr      = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    return tr


def main():
    log.info("=" * 70)
    log.info("BSIP2 Hard Cheeses — %s (TASK-418 clean corpus re-score)", RUN_ID)
    log.info("Flag stack: BARI_SHELF_RELATIVE_V1=on BARI_FAT_TECH_V1=on "
             "BARI_RECAL_P0=on BARI_REDLABEL_V1=on "
             "BARI_HC_DAIRY_SATFAT_V1=on BARI_DAIRY_SAT_FAT_INFER=on "
             "BARI_HC002_NOVA1=off")
    log.info("fat_sat shelf stats: median=%.1f scale=%.4f type=iqr",
             FATSAT_SHELF_REL_HARDCHEESE_MEDIAN, FATSAT_SHELF_REL_HARDCHEESE_SCALE)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    set_shelf_stats(
        "fat_saturated_g",
        FATSAT_SHELF_REL_HARDCHEESE_MEDIAN,
        FATSAT_SHELF_REL_HARDCHEESE_SCALE,
        "iqr"
    )

    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_hardcheese_*.json"))
    log.info("BSIP1 files found: %d", len(bsip1_files))

    products_all     = []
    products_curated = []
    off_skipped      = 0
    discarded        = []

    for p in bsip1_files:
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            log.error("Failed to read %s: %s", p, e)
            continue

        if is_off_contaminated(doc):
            log.warning("OFF-CONTAMINATED — skip: %s", doc.get("barcode", ""))
            off_skipped += 1
            continue

        should_discard, reasons = missing_data_discard(doc)
        if should_discard:
            discarded.append({"barcode": doc.get("barcode"), "reasons": reasons})
            continue

        bc = str(doc.get("barcode", ""))
        products_all.append((bc, doc))
        if bc in CURATED_31:
            products_curated.append((bc, doc))

    log.info("Total loaded (post-discard): %d", len(products_all))
    log.info("Curated 31 found: %d", len(products_curated))

    # --- Score all products ---
    all_traces     = []
    curated_traces = []
    errors         = []

    for bc, doc in products_all:
        try:
            tr = score_one(doc)
            all_traces.append((bc, tr))
            if bc in CURATED_31:
                curated_traces.append((bc, tr))
            write_trace(tr, OUTPUT_DIR)
        except Exception as e:
            log.error("PIPELINE ERROR [%s]: %s", bc, e)
            import traceback
            traceback.print_exc()
            errors.append({"barcode": bc, "error": str(e)})

    clear_shelf_stats("fat_saturated_g")
    log.info("Scored: %d  errors: %d", len(all_traces), len(errors))

    # --- Build curated 31 summary ---
    curated_rows = []
    score_movers = []
    grade_movers = []

    for bc, tr in sorted(curated_traces, key=lambda x: (x[1].get("final_score_estimate") or 0)):
        ref   = tr.get("input_reference") or {}
        score = tr.get("final_score_estimate")
        grade = tr.get("grade_estimate")
        nova  = tr.get("nova_proxy")
        nnn   = (tr.get("L1_observed_signals") or {})
        fat_sat  = nnn.get("fat_saturated_g")
        sodium   = nnn.get("sodium_mg")
        binding_cap = tr.get("binding_cap")
        conf_band   = (tr.get("confidence_result") or {}).get("confidence_band")

        live_s, live_g = LIVE_SCORES.get(bc, (None, None))
        delta = round(score - live_s, 2) if (score is not None and live_s is not None) else None
        grade_moved = (grade != live_g) if (grade and live_g) else False

        row = {
            "barcode": bc,
            "name": ref.get("product_name_he", ""),
            "score": score,
            "grade": grade,
            "nova_proxy": nova,
            "confidence_band": conf_band,
            "binding_cap": binding_cap,
            "fat_saturated_g": fat_sat,
            "sodium_mg": sodium,
            "context_flag": tr.get("context_flag"),
            "live_score": live_s,
            "live_grade": live_g,
            "delta": delta,
            "grade_moved": grade_moved,
            "caps_applied": [c["rule"] for c in (tr.get("caps_applied") or [])],
            "penalties_applied": [p["rule"] for p in (tr.get("penalties_applied") or [])],
        }
        curated_rows.append(row)

        if delta is not None and abs(delta) >= 0.05:
            score_movers.append(row)
        if grade_moved:
            grade_movers.append(row)

    grade_dist = dict(sorted(Counter(r["grade"] for r in curated_rows).items()))

    print()
    print("=" * 80)
    print(f"TASK-418 Clean Corpus Re-score — {RUN_ID}")
    print("=" * 80)
    print(f"Curated 31: {len(curated_traces)} products scored")
    print(f"Grade distribution: {grade_dist}")
    print()
    print(f"{'BC':<16} {'Old':>8} {'New':>8} {'Delta':>7} {'GM':>3}  {'Conf':>7}")
    print("-" * 65)
    for r in sorted(curated_rows, key=lambda x: (x["score"] or 0), reverse=True):
        gm = "YES" if r["grade_moved"] else "no"
        delta_s = f"{r['delta']:+.2f}" if r["delta"] is not None else "?"
        live_str = f"{r['live_score']}/{r['live_grade']}" if r["live_score"] else "?"
        new_str  = f"{r['score']}/{r['grade']}" if r["score"] else "?"
        print(f"{r['barcode']:<16} {live_str:>8} {new_str:>8} {delta_s:>7} {gm:>3}  {str(r['confidence_band'] or '?'):>7}")

    print()
    print(f"Score movers (|delta| >= 0.05): {len(score_movers)}")
    print(f"Grade movers: {len(grade_movers)}")
    if grade_movers:
        print("GRADE MOVERS:")
        for r in grade_movers:
            print(f"  {r['barcode']}  {r['live_score']}/{r['live_grade']} -> {r['score']}/{r['grade']}  delta={r['delta']}")

    # Full corpus grade distribution
    all_grades = Counter(tr.get("grade_estimate") for _, tr in all_traces if tr.get("grade_estimate"))
    print()
    print(f"Full corpus: {dict(sorted(all_grades.items()))}")

    # Verification table (flat)
    vt = [{
        "barcode":        r["barcode"],
        "name":           r["name"],
        "score":          r["score"],
        "grade":          r["grade"],
        "binding_cap":    r["binding_cap"],
        "nova":           r["nova_proxy"],
        "fat_saturated_g": r["fat_saturated_g"],
        "sodium_mg":      r["sodium_mg"],
        "context_flag":   r["context_flag"],
        "live_score":     r["live_score"],
        "live_grade":     r["live_grade"],
        "delta":          r["delta"],
        "grade_moved":    r["grade_moved"],
    } for r in sorted(curated_rows, key=lambda x: (x["score"] or 0), reverse=True)]

    vt_path = OUTPUT_DIR / "verification_table.json"
    vt_path.write_text(json.dumps(vt, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Verification table: %s", vt_path)

    # Save run summary
    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "task": "TASK-418",
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_HC002_NOVA1": "off",
            "BARI_DAIRY_SAT_FAT_INFER": "on",
            "BARI_REDLABEL_V1": "on",
            "BARI_HC_DAIRY_SATFAT_V1": "on",
        },
        "corpus_dir": str(BSIP1_DIR),
        "curated_31": {
            "found": len(curated_traces),
            "grade_distribution": grade_dist,
            "stable_table": curated_rows,
            "score_movers_count": len(score_movers),
            "grade_movers_count": len(grade_movers),
            "grade_movers": grade_movers,
        },
        "all_products": {
            "scored": len(all_traces),
            "errors": len(errors),
            "grade_distribution": dict(sorted(all_grades.items())),
        },
        "off_skipped": off_skipped,
        "discarded": discarded,
        "error_list": errors,
    }

    summary_path = OUTPUT_DIR / "run_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Summary written: %s", summary_path)

    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
