"""
TASK-229 — Correct the אפרופו קרמל (7290118421603) trans-fat artifact and re-score.

Finding (same artifact class as the beet cracker, TASK-231): the OFF panel for
7290118421603 carries trans-fat_serving = 0.5 g on a 40 g serving (serving fraction 0.4,
confirmed by every other macro scaling cleanly: energy 219/547.5, fat 12.6/31.5, sat
5.2/13, sugar 14/35, carbs 24.4/61 — all => 0.4). OFF then computed trans-fat_100g by
dividing: 0.5 / 0.4 = 1.25 g/100g, which trips the >1.0 g hard trans veto.

0.5 g on the serving panel is the Israeli "<1 g" threshold declaration (the exact value
the engine itself classifies as `threshold_declaration`, signal_extractor.py ~L1104),
NOT a measured value. It is the identical canned 0.5 g declaration found in the beet
cracker panel. The sat/fat profile (13/31.5 = 41%) is consistent with palm oil (Osem's
post-PHVO-phaseout frying fat) + caramel (sugar+palm), no industrial PHVO trans source.
A 1.25 g/100g measured trans is implausible and is a serving-scaling artifact.

Fix: set fat_trans_g = 0.0 (honest: no measured trans; OFF value is a serving-scaling
artifact) and re-run this single product through the UNCHANGED engine. Scoring logic,
caps, vetoes, thresholds untouched. Result: trans-fat veto no longer (mis)fires.
"""
import json, sys, os, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# TASK-238: Open Food Facts is BANNED. This product's nutrition panel is OFF-derived; the
# trans correction here reasons over an OFF panel. DISABLED — handled by the OFF removal.
raise RuntimeError(
    "OFF is banned (TASK-238): fix_apropo_caramel_trans.py corrects an Open Food Facts "
    "panel and is disabled. OFF-derived nutrition is NULLed by the TASK-238 remediation."
)

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

BARCODE = "7290118421603"
BSIP1 = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip1_outputs\bsip1_snack_7290118421603.json")
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002")


def main():
    rec = json.loads(BSIP1.read_text("utf-8"))
    old = rec["normalized_nutrition_per_100g"].get("fat_trans_g")
    rec["normalized_nutrition_per_100g"]["fat_trans_g"] = 0.0
    rec.setdefault("data_corrections", []).append({
        "field": "normalized_nutrition_per_100g.fat_trans_g",
        "old_value": old,
        "new_value": 0.0,
        "reason": ("OFF trans-fat_100g (1.25) was a serving-scaling artifact: serving "
                   "panel 0.5 g / 0.40 serving fraction (40 g serving, confirmed by all "
                   "other macros scaling at 0.40). 0.5 g serving = Israeli '<1g' threshold "
                   "declaration (identical canned value to the beet cracker), not measured. "
                   "Sat/fat 41% consistent with palm oil + caramel, no PHVO trans source. "
                   "Corrected to 0.0 (no measured trans). TASK-229."),
        "task": "TASK-229",
        "corrected_at_source": "open_food_facts (serving-scaling artifact)",
    })
    BSIP1.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"BSIP1 corrected: fat_trans_g {old} -> 0.0")

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
