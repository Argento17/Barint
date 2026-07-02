"""
TASK-385 / EV-105 — Cross-category isolation proof for BARI_GRAN_SUGAR_25G_V1.
Scope guard in score_engine.py: category in SODIUM_CEREAL_CATEGORIES = {"snack_bar_granola", "cereal"}.
Test: run 5 milk products (dairy_protein category) with flag OFF vs ON — expect 0 score movers.
"""
import sys, io, json, pathlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "03_operations" / "bsip2" / "proto_v0" / "src"))

MILK_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output")
N_CONTROL = 5   # number of control products

def score_product_pair(product, gran_on):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from score_engine import score_product
    import score_engine as se

    se.BARI_SODIUM_CEREAL = False
    se.BARI_RECAL_P0 = True
    se.BARI_FAT_TECH_V1 = True
    se.BARI_REDLABEL_V1 = False
    se.BARI_SHELF_RELATIVE_V1 = False
    se.BARI_GRAN_SUGAR_25G_V1 = gran_on

    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    result      = score_product(product, signals, cat_result, nova_result, eval_result)
    return {
        "score": result.get("final_score_estimate"),
        "grade": result.get("grade_estimate"),
        "category": cat_result.get("category"),
    }


def main():
    from input_loader import load_batch
    all_products = load_batch(MILK_DIR)
    control = all_products[:N_CONTROL]
    print(f"Cross-category isolation test — {len(control)} milk/dairy products")
    print(f"Scope guard: SODIUM_CEREAL_CATEGORIES = {{snack_bar_granola, cereal}}")
    print()

    movers = []
    rows = []
    for p in control:
        bc = str(p.get("barcode", "?"))
        name = p.get("product_name_he", "?")
        r_off = score_product_pair(p, False)
        r_on  = score_product_pair(p, True)
        delta = round((r_on["score"] or 0) - (r_off["score"] or 0), 4)
        moved = abs(delta) > 0.001
        rows.append({
            "barcode": bc,
            "name": name,
            "category": r_off["category"],
            "score_off": r_off["score"],
            "score_on": r_on["score"],
            "delta": delta,
            "moved": moved,
        })
        if moved:
            movers.append(bc)

    print(f"{'barcode':15s} | {'category':20s} | {'score_off':9s} | {'score_on':9s} | {'delta':6s} | moved?")
    print("-" * 80)
    for r in rows:
        print(f"{r['barcode']:15s} | {r['category']:20s} | {str(r['score_off']):9s} | {str(r['score_on']):9s} | {str(r['delta']):6s} | {'YES — FAIL' if r['moved'] else 'no'}")

    print()
    if movers:
        print(f"ISOLATION FAIL: {len(movers)} non-granola products moved: {movers}")
    else:
        print(f"ISOLATION PASS: 0/{len(control)} non-granola/cereal products moved when flag flipped OFF->ON")
        print(f"Category guard confirmed: SODIUM_CEREAL_CATEGORIES scope prevents any dairy_protein score change.")
    print(f"Exit: {'1' if movers else '0'}")
    return 1 if movers else 0


if __name__ == "__main__":
    sys.exit(main())
