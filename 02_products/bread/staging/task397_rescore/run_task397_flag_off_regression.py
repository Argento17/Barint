"""
TASK-397 Flag-OFF Regression Check
Verifies that BARI_FAT_SENTINEL_V1=off produces byte-identical scores to
the live run_bread_conform_001 baseline.
"""
from __future__ import annotations
import sys, json, pathlib, os

# Sentinel flag MUST be off; all other flags identical to run_bread_conform_001
FLAGS = {
    "BARI_RECAL_P0":                  "on",
    "BARI_SHELF_RELATIVE_V1":         "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1":  "off",
    "BARI_FAT_TECH_V1":               "on",
    "BARI_GRAD_SODIUM_V1":            "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1":               "off",
    "BARI_SODIUM_CEREAL":             "off",
    "BARI_FAT_SENTINEL_V1":           "off",   # ← must be OFF
}
for k, v in FLAGS.items():
    os.environ[k] = v

sys.path.insert(0, str(pathlib.Path(__file__).parents[4] / "03_operations/bsip2/proto_v0/src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from input_loader     import load_product, validate_product
from signal_extractor import extract_signals
from router_v2        import classify_category
from nova_proxy       import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine     import score_product
from trace_writer     import assemble_trace
from structural_classifier import classify_structural_class

BSIP1_DIR    = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output")
BASELINE_DIR = pathlib.Path(r"C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_001\products")


def score_one(product: dict) -> dict:
    prod     = {k: v for k, v in product.items() if not k.startswith("_")}
    signals  = extract_signals(prod)
    cat_res  = classify_category(prod)
    l3       = signals["L3_inferred_classifications"]
    nova_res = infer_nova(prod, l3)
    eval_res = assign_evaluation_scope(prod, cat_res["category"])
    sc_res   = score_product(prod, signals, cat_res, nova_res, eval_res)
    trace    = assemble_trace(prod, signals, cat_res, nova_res, eval_res, sc_res)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    mismatches = []
    matches    = 0

    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        product["_load_errors"] = validate_product(product)

        pid     = product.get("canonical_product_id", fpath.stem)
        barcode = str(product.get("barcode", ""))

        try:
            trace = score_one(product)
        except Exception as e:
            print(f"  ERROR {pid}: {e}")
            mismatches.append({"barcode": barcode, "diff": f"ERROR: {e}"})
            continue

        # Load baseline
        baseline_path = BASELINE_DIR / str(pid) / "bsip2_trace.json"
        if not baseline_path.exists():
            mismatches.append({"barcode": barcode, "diff": "baseline missing"})
            continue

        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))

        # Compare final_score_estimate, grade_estimate, fat_quality
        new_score  = trace.get("final_score_estimate")
        base_score = baseline.get("final_score_estimate")
        new_grade  = trace.get("grade_estimate")
        base_grade = baseline.get("grade_estimate")
        new_fq     = trace.get("dimension_scores", {}).get("fat_quality")
        base_fq    = baseline.get("dimension_scores", {}).get("fat_quality")

        if new_score != base_score or new_grade != base_grade or new_fq != base_fq:
            mismatches.append({
                "barcode": barcode,
                "diff": f"score {base_score}->{new_score} grade {base_grade}->{new_grade} fq {base_fq}->{new_fq}",
            })
        else:
            matches += 1

    print(f"\n=== Flag-OFF Regression Result ===")
    print(f"Matches:    {matches}/{len(bsip1_files)}")
    print(f"Mismatches: {len(mismatches)}")
    if mismatches:
        for m in mismatches:
            print(f"  MISMATCH {m['barcode']}: {m['diff']}")
        print("\nREGRESSION FAILED — flag-off is NOT byte-identical to baseline!")
        sys.exit(1)
    else:
        print("\nPASS — flag-off is byte-identical to run_bread_conform_001 baseline.")
        sys.exit(0)


if __name__ == "__main__":
    main()
