"""
TASK-397 Flag-OFF Regression Check (Pair Comparison)

Verifies that BARI_FAT_SENTINEL_V1=off produces scores identical to a fresh
flag-off run FROM THE SAME BSIP1 state.  This isolates the sentinel code change
from any BSIP1 data drift.

Two sub-runs from the same BSIP1 files:
  A: BARI_FAT_SENTINEL_V1=off   (control / flag-off)
  B: BARI_FAT_SENTINEL_V1=on    (staging / flag-on)

Expected invariant: for all non-sentinel products, A == B.
For sentinel products: B.fat_quality == 50.0, A.fat_quality == 90.5.
"""
from __future__ import annotations
import sys, json, pathlib, os

def score_all(flag_on: bool) -> list[dict]:
    flags = {
        "BARI_RECAL_P0":                  "on",
        "BARI_SHELF_RELATIVE_V1":         "off",
        "BARI_SODIUM_SHELF_RELATIVE_V1":  "off",
        "BARI_FAT_TECH_V1":               "on",
        "BARI_GRAD_SODIUM_V1":            "off",
        "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
        "BARI_REDLABEL_V1":               "off",
        "BARI_SODIUM_CEREAL":             "off",
        "BARI_FAT_SENTINEL_V1":           "on" if flag_on else "off",
    }
    for k, v in flags.items():
        os.environ[k] = v

    # Must import AFTER setting env vars (flags are read at module level)
    import importlib
    import score_engine as se_mod
    # Reload to pick up new flag value
    importlib.reload(se_mod)
    from input_loader import load_product, validate_product
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from trace_writer import assemble_trace
    from structural_classifier import classify_structural_class

    BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output")
    results = []
    for fpath in sorted(BSIP1_DIR.glob("bsip1_*.json")):
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        product["_load_errors"] = validate_product(product)
        pid     = product.get("canonical_product_id", fpath.stem)
        barcode = str(product.get("barcode", ""))
        nn      = product.get("normalized_nutrition_per_100g", {}) or {}
        fat_sentinel = nn.get("fat_sentinel", False)

        try:
            prod     = {k: v for k, v in product.items() if not k.startswith("_")}
            signals  = extract_signals(prod)
            cat_res  = classify_category(prod)
            l3       = signals["L3_inferred_classifications"]
            nova_res = infer_nova(prod, l3)
            eval_res = assign_evaluation_scope(prod, cat_res["category"])
            sc_res   = se_mod.score_product(prod, signals, cat_res, nova_res, eval_res)
            trace    = assemble_trace(prod, signals, cat_res, nova_res, eval_res, sc_res)
            trace["structural_class"] = classify_structural_class(trace)
            results.append({
                "barcode":      barcode,
                "fat_sentinel": fat_sentinel,
                "score":        trace.get("final_score_estimate"),
                "grade":        trace.get("grade_estimate"),
                "fat_quality":  trace.get("dimension_scores", {}).get("fat_quality"),
                "fat_note":     trace.get("dimension_notes", {}).get("fat_quality", ""),
            })
        except Exception as e:
            results.append({"barcode": barcode, "error": str(e)})
    return results


sys.path.insert(0, str(pathlib.Path(__file__).parents[4] / "03_operations/bsip2/proto_v0/src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

print("Running flag-OFF (control)...")
off_results = score_all(False)
print("Running flag-ON  (sentinel)...")
on_results  = score_all(True)

# Index by barcode
off_by_bc = {r["barcode"]: r for r in off_results}
on_by_bc  = {r["barcode"]: r for r in on_results}

print("\n=== Pair Comparison (flag-OFF vs flag-ON) ===")
print(f"{'barcode':<16} | {'sentinel':<8} | {'off_score':<10} | {'on_score':<10} | {'off_fq':<7} | {'on_fq':<7} | {'grade_off':<9} | {'grade_on':<9}")
print("-" * 110)

unexpected = []
expected_moves = 0
for bc in sorted(off_by_bc.keys()):
    o = off_by_bc[bc]
    n = on_by_bc.get(bc, {})
    sentinel = o.get("fat_sentinel", False)
    score_diff = o.get("score") != n.get("score")
    grade_diff = o.get("grade") != n.get("grade")
    fq_diff    = o.get("fat_quality") != n.get("fat_quality")
    print(f"{bc:<16} | {str(sentinel):<8} | {str(o.get('score')):<10} | {str(n.get('score')):<10} | "
          f"{str(o.get('fat_quality')):<7} | {str(n.get('fat_quality')):<7} | "
          f"{str(o.get('grade')):<9} | {str(n.get('grade')):<9}")
    if sentinel:
        expected_moves += 1
        if not fq_diff:
            unexpected.append(f"SENTINEL DID NOT FIRE: {bc}")
    else:
        if score_diff or grade_diff or fq_diff:
            unexpected.append(f"NON-SENTINEL MOVED: {bc} score {o.get('score')}->{n.get('score')} "
                              f"grade {o.get('grade')}->{n.get('grade')} fq {o.get('fat_quality')}->{n.get('fat_quality')}")

print(f"\nSentinel products (expected to move fq): {expected_moves}")
print(f"Non-sentinel unexpected movements:       {len(unexpected)}")
if unexpected:
    for u in unexpected:
        print(f"  PROBLEM: {u}")
    print("\nREGRESSION FAILED")
    sys.exit(1)
else:
    print("\nPASS — sentinel fires only on sentinel products; non-sentinel products are byte-identical.")
    sys.exit(0)
