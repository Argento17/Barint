"""
TASK-231 — Correct the beet-cracker (7290112968807) trans-fat artifact and re-score.

Finding: OFF panel for 7290112968807 declared trans-fat_serving = 0.5 g on a 21.5 g
serving, then computed trans-fat_100g by dividing by 0.215 -> 2.326 g/100g. The whole
_100g block is corrupted by that bad serving division (nova-group_100g = 18.6, etc.).
0.5 g on the serving panel is the Israeli "<1 g" threshold declaration (see
score_engine.py ~L3051), NOT a measured value. Ingredients list "vegetable oils" +
rosemary extract, no PHVO/hydrogenated oil -> no real industrial trans source. A whole-
grain beet cracker with 1.86 g saturated/100g cannot carry 2.33 g trans/100g.

Fix: set fat_trans_g = 0.0 (honest: no measured trans; OFF value is a serving-scaling
artifact) and re-run this single product through the UNCHANGED engine. Scoring logic,
caps, vetoes, thresholds untouched. Result: trans-fat veto no longer (mis)fires.
"""
import json, sys, os, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ["BARI_RECAL_P0"] = "on"
sys.path.insert(0, r"C:\Bari\03_operations\bsip2\proto_v0\src")

from input_loader import load_batch  # noqa: E402
from signal_extractor import extract_signals  # noqa: E402
from router_v2 import classify_category  # noqa: E402
from nova_proxy import infer_nova  # noqa: E402
from evaluation_scope import assign_evaluation_scope  # noqa: E402
from score_engine import score_product  # noqa: E402
from trace_writer import assemble_trace, write_trace  # noqa: E402
from structural_classifier import classify_structural_class  # noqa: E402

BARCODE = "7290112968807"
BSIP1 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs\bsip1_snack_7290112968807.json")
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002")


def main():
    rec = json.loads(BSIP1.read_text("utf-8"))
    old = rec["normalized_nutrition_per_100g"].get("fat_trans_g")
    rec["normalized_nutrition_per_100g"]["fat_trans_g"] = 0.0
    rec.setdefault("data_corrections", []).append({
        "field": "normalized_nutrition_per_100g.fat_trans_g",
        "old_value": old,
        "new_value": 0.0,
        "reason": ("OFF trans-fat_100g (2.326) was a serving-scaling artifact: serving "
                   "panel 0.5 g / 0.215 serving fraction. 0.5 g serving = Israeli '<1g' "
                   "threshold declaration, not measured. No PHVO/hydrogenated oil in "
                   "ingredients. Corrected to 0.0 (no measured trans). TASK-231."),
        "task": "TASK-231",
        "corrected_at_source": "open_food_facts (serving-scaling artifact)",
    })
    BSIP1.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"BSIP1 corrected: fat_trans_g {old} -> 0.0")

    # Re-run this single product through the unchanged engine
    product = None
    for p in load_batch(BSIP1.parent):
        if p.get("barcode") == BARCODE or p.get("canonical_product_id") == "bsip1_snack_" + BARCODE:
            product = p
            break
    if product is None:
        print("ERROR: product not found in batch load"); sys.exit(1)

    signals = extract_signals(product)
    cat = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(product, l3)
    scope = assign_evaluation_scope(product, cat["category"])
    score = score_product(product, signals, cat, nova, scope)
    trace = assemble_trace(product, signals, cat, nova, scope, score)
    trace["structural_class"] = classify_structural_class(trace)
    write_trace(trace, OUTPUT_ROOT)
    print(f"Re-scored {BARCODE}: final={trace.get('final_score_estimate')} "
          f"grade={trace.get('grade_estimate')} trans_veto={score.get('trans_fat_veto')}")


if __name__ == "__main__":
    main()
