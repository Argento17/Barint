# -*- coding: utf-8 -*-
"""
Hard Cheeses TASK-412 — RT-4 Option B fix re-score.
Run ID: run_hc_task412_rt4_fix

RT-4 fix (TASK-412): HC_DAIRY_SATFAT_NA_CAP_600_VALUE raised from 63.0 -> 67.0
  (= HC_DAIRY_SATFAT_C_CEILING_VALUE) in constants.py.
  HC-3 no longer introduces a tighter tier than HC-2 for sodium 600-699mg range.
  Within-band differentiation comes from SODIUM_LOAD_GENERAL_GRAD penalty.

RT-5 fix applied inline: Noam 9% (HC-5079665) bsip1_trust_level=unknown AND
  ingredient_text_quality=null -> confidence reclassified full->medium.

Same flag stack as candA_003 (Candidate A, owner-approved):
  BARI_SHELF_RELATIVE_V1  = on
  BARI_FAT_TECH_V1        = on
  BARI_RECAL_P0           = on
  BARI_REDLABEL_V1        = on
  BARI_HC_DAIRY_SATFAT_V1 = on
  BARI_DAIRY_SAT_FAT_INFER= on
  BARI_HC002_NOVA1        = off
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

SRC = pathlib.Path(__file__).parent
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
    HC_DAIRY_SATFAT_NA_CAP_600_VALUE,
    HC_DAIRY_SATFAT_C_CEILING_VALUE,
)
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

WORKTREE  = pathlib.Path(r"C:\bari_hc_engine")
BSIP1_DIR = WORKTREE / "02_products" / "hard_cheeses" / "bsip1_task412"
OUTPUT_DIR = WORKTREE / "02_products" / "hard_cheeses" / "bsip2_outputs" / "run_hc_task412_rt4_fix"

RUN_ID = "run_hc_task412_rt4_fix"

# Curated 31-product barcodes (v3 corpus, same as candA_003)
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

# RT-5: barcodes with trust_level=unknown AND ingredient_text_quality=null
# -> confidence reclassified full->medium
RT5_MEDIUM_BARCODES = set()  # will be populated by inspection during run

OFF_MARKERS = ["open_food_facts", "openfoodfacts", "il_prices"]


def is_off_contaminated(doc):
    prov_str = json.dumps(doc.get("provenance", {})).lower()
    return any(m in prov_str for m in OFF_MARKERS)


def get_nnn(doc):
    return doc.get("normalized_nutrition_per_100g") or {}


def missing_data_discard(doc):
    nnn = get_nnn(doc)
    sodium = nnn.get("sodium_mg")
    fat = nnn.get("fat_g")
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


def check_rt5_condition(doc):
    """RT-5: trust_level=unknown AND ingredient_text_quality=null -> medium confidence."""
    trust_level = doc.get("bsip1_trust_level") or doc.get("trust_level")
    ing_qual = doc.get("ingredient_text_quality")
    return trust_level == "unknown" and ing_qual is None


def score_one(doc):
    signals = extract_signals(doc)
    cat = classify_category(doc)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(doc, l3)
    ev = assign_evaluation_scope(doc, cat["category"])
    sr = score_product(doc, signals, cat, nova, ev)
    tr = assemble_trace(doc, signals, cat, nova, ev, sr)
    tr["structural_class"] = classify_structural_class(tr)
    return tr


def main():
    log.info("=" * 70)
    log.info("BSIP2 Hard Cheeses — %s (TASK-412 RT-4 Option B fix)", RUN_ID)
    log.info("RT-4 fix: HC_DAIRY_SATFAT_NA_CAP_600_VALUE = %.1f (was 63.0)", HC_DAIRY_SATFAT_NA_CAP_600_VALUE)
    log.info("RT-4 verify: HC_DAIRY_SATFAT_NA_CAP_600_VALUE(%.1f) == HC_DAIRY_SATFAT_C_CEILING_VALUE(%.1f): %s",
             HC_DAIRY_SATFAT_NA_CAP_600_VALUE, HC_DAIRY_SATFAT_C_CEILING_VALUE,
             HC_DAIRY_SATFAT_NA_CAP_600_VALUE == HC_DAIRY_SATFAT_C_CEILING_VALUE)
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

    products_all = []
    products_curated = []
    off_skipped = 0
    discarded = []
    rt5_siblings = []  # RT-5: products with trust_level=unknown AND ingredient_text_quality=null

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

        # RT-5: identify products with trust_level=unknown AND ingredient_text_quality=null
        if check_rt5_condition(doc):
            rt5_siblings.append({
                "barcode": bc,
                "name": doc.get("canonical_name_he") or doc.get("product_name_he") or "",
                "bsip1_trust_level": doc.get("bsip1_trust_level") or doc.get("trust_level"),
                "ingredient_text_quality": doc.get("ingredient_text_quality"),
                "confidence_before_rt5": "full",  # will be overridden to medium
            })
            RT5_MEDIUM_BARCODES.add(bc)

        products_all.append((bc, doc))
        if bc in CURATED_31:
            products_curated.append((bc, doc))

    log.info("Total loaded (post-discard): %d", len(products_all))
    log.info("Curated 31 found: %d", len(products_curated))
    log.info("RT-5 candidates (trust=unknown + ing_qual=null): %d -> %s",
             len(rt5_siblings), [s["barcode"] for s in rt5_siblings])

    # --- Score all products ---
    all_traces = []
    curated_traces = []
    errors = []

    for bc, doc in products_all:
        try:
            tr = score_one(doc)

            # RT-5: apply confidence reclassification for trust_level=unknown + ing_qual=null
            # The score is unchanged; only the confidence field surface label changes.
            # This is a data-quality annotation, not a scoring change.
            if bc in RT5_MEDIUM_BARCODES:
                conf_result = tr.get("confidence_result") or {}
                old_band = conf_result.get("confidence_band")
                # Only reclassify if currently at full (RT-5 spec: full->medium)
                if old_band == "full":
                    conf_result["confidence_band"] = "medium"
                    conf_result["rt5_reclassification"] = (
                        "full->medium: bsip1_trust_level=unknown AND "
                        "ingredient_text_quality=null (TASK-412 RT-5)"
                    )
                    tr["confidence_result"] = conf_result
                    tr["rt5_applied"] = True
                    log.info("RT-5 reclassification applied: %s full->medium", bc)

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
    for bc, tr in sorted(curated_traces, key=lambda x: (x[1].get("final_score_estimate") or 0)):
        ref = tr.get("input_reference") or {}
        score = tr.get("final_score_estimate")
        grade = tr.get("grade_estimate")
        nova = tr.get("nova_proxy")
        conf_band = (tr.get("confidence_result") or {}).get("confidence_band")
        rt5 = tr.get("rt5_applied", False)
        curated_rows.append({
            "barcode": bc,
            "name": ref.get("product_name_he", ""),
            "score": score,
            "grade": grade,
            "nova_proxy": nova,
            "confidence_band": conf_band,
            "rt5_applied": rt5,
            "binding_cap": tr.get("binding_cap"),
            "total_penalty": tr.get("total_penalty_after_scaling"),
            "caps_fired": [c["rule"] for c in (tr.get("caps_considered") or []) if c.get("fired")],
            "caps_applied": [c["rule"] for c in (tr.get("caps_applied") or [])],
            "penalties_applied": [p["rule"] for p in (tr.get("penalties_applied") or [])],
        })

    grade_dist = dict(sorted(Counter(r["grade"] for r in curated_rows).items()))

    print()
    print("=" * 80)
    print(f"TASK-412 RT-4 Option B fix — {RUN_ID}")
    print(f"HC-3 na_cap: 63.0 -> {HC_DAIRY_SATFAT_NA_CAP_600_VALUE} (= HC-2 ceiling)")
    print("=" * 80)
    print(f"Curated 31: {len(curated_traces)} products scored")
    print(f"Grade distribution: {grade_dist}")
    print()
    print(f"{'BC':<16} {'Score':>6} {'G':>2} {'NOVA':>4} {'Conf':>7}  {'Caps/Penalties'}")
    print("-" * 80)
    for r in curated_rows:
        caps_app = "+".join(r["caps_applied"]) if r["caps_applied"] else "-"
        pens = "+".join(r["penalties_applied"]) if r["penalties_applied"] else "-"
        rt5_flag = " [RT5]" if r["rt5_applied"] else ""
        print(f"{r['barcode']:<16} {str(r['score']):>6} {r['grade']:>2} {str(r['nova_proxy']):>4} "
              f"{str(r['confidence_band'] or '?'):>7}  {caps_app[:30]} | {pens[:30]}{rt5_flag}")

    print()
    print("RT-5 siblings (trust=unknown + ing_qual=null):")
    if rt5_siblings:
        for s in rt5_siblings:
            print(f"  {s['barcode']}: {s['name'][:40]}")
    else:
        print("  None found.")

    # --- Full corpus grade distribution ---
    all_grades = Counter(tr.get("grade_estimate") for _, tr in all_traces if tr.get("grade_estimate"))
    all_grade_dist = dict(sorted(all_grades.items()))
    print()
    print(f"Full corpus (76): {all_grade_dist}")

    # Save run summary
    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "rt4_fix": {
            "description": "HC_DAIRY_SATFAT_NA_CAP_600_VALUE raised from 63.0 to 67.0 (= HC-2 ceiling)",
            "file": "03_operations/bsip2/proto_v0/src/constants.py",
            "line": "702",
            "old_value": 63.0,
            "new_value": HC_DAIRY_SATFAT_NA_CAP_600_VALUE,
            "rationale": "EV-104 inversion defect: sodium 600-699 capped tighter (63) than sodium >=700 (67 via HC-2). Option B removes HC-3 as a distinct tier; within-band differentiation from SODIUM_LOAD_GENERAL_GRAD.",
        },
        "rt5_fix": {
            "description": "Reclassify confidence full->medium for products with bsip1_trust_level=unknown AND ingredient_text_quality=null",
            "siblings_reclassified": rt5_siblings,
        },
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_HC002_NOVA1": "off",
            "BARI_DAIRY_SAT_FAT_INFER": "on",
            "BARI_REDLABEL_V1": "on",
            "BARI_HC_DAIRY_SATFAT_V1": "on",
        },
        "curated_31": {
            "found": len(curated_traces),
            "grade_distribution": grade_dist,
            "stable_table": curated_rows,
        },
        "all_products": {
            "scored": len(all_traces),
            "errors": len(errors),
            "grade_distribution": all_grade_dist,
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
