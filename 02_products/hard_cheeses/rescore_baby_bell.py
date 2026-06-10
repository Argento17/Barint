"""
Re-score Baby Bell (3073781199918) using the production pipeline.
Uses the corrected BSIP1 record and runs through the full score_engine pipeline.
"""
import sys, json, pathlib, os, logging

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PIPELINE_SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
BSIP1_PATH = pathlib.Path(
    r"C:\Bari\02_products\hard_cheeses\bsip1_outputs\bsip1_hardcheese_3073781199918.json"
)
BSIP2_OUTPUT_ROOT = pathlib.Path(
    r"C:\Bari\02_products\hard_cheeses\bsip2_outputs\run_hard_cheeses_yohananof_001"
)
TRACE_PATH = BSIP2_OUTPUT_ROOT / "products" / "bsip1_hardcheese_3073781199918" / "bsip2_trace.json"

sys.path.insert(0, str(PIPELINE_SRC))

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)


def run_pipeline(product: dict) -> dict:
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    from trace_writer import assemble_trace, write_trace
    from structural_classifier import classify_structural_class

    signals = extract_signals(product)
    cat_result = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    write_trace(trace, BSIP2_OUTPUT_ROOT)
    return trace


def main():
    product = json.loads(BSIP1_PATH.read_text(encoding="utf-8"))
    log.info("Re-scoring: %s", product.get("canonical_product_id"))
    log.info("Ingredients: %s", product.get("ingredients_text_he"))
    log.info("Nutrition fat=%.1f protein=%.1f sodium=%.1f",
             product.get("fat_g", 0), product.get("protein_g", 0), product.get("sodium_mg", 0))

    trace = run_pipeline(product)

    score = trace.get("final_score_estimate")
    grade = trace.get("grade_estimate")
    log.info("=== RESULT: score=%s grade=%s ===", score, grade)
    log.info("Trace written to: %s", TRACE_PATH)

    print(f"\nFinal score: {score}")
    print(f"Grade: {grade}")
    print(f"Category: {trace.get('category')}")

    # Print key trace sections
    for section in ["confidence_ceiling", "glass_box_flags", "limiting_factors_resolved"]:
        if section in trace:
            print(f"{section}: {json.dumps(trace[section], ensure_ascii=False)}")

    return trace


if __name__ == "__main__":
    main()
