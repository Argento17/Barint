"""
BSIP2 Batch Runner — Rice/Corn/Buckwheat Cakes (run_ricecakes_conform_001)
TASK-516: crackers shelf expansion (Nutrition + Product Agent sign-off 2026-07-05).

Scores BSIP1 records from run_ricecakes_conform_001 using the uniform engine.
Same flag set as the existing crackers run (identical grain/non-dairy vector,
no shelf-relative signal, no dairy/cereal-sodium modes) -- these are the same
grain-snack product family, sharing a comparison pool per the Constitution.

Category routing: router_v2.classify_category has a live HARD_ANCHOR
("פריכיות", "cracker", "puffed_cracker", 0.88) confirmed by Nutrition Agent
(2026-07-05) -- no caller override needed, same mechanism as run_crackers_
conform_001.
"""

from __future__ import annotations
import sys, json, pathlib, datetime, os

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_ricecakes_conform_001\output")
BSIP2_OUT = pathlib.Path(r"C:\Bari\02_products\crackers\bsip2_outputs\run_ricecakes_conform_001\products")
BSIP2_OUT.mkdir(parents=True, exist_ok=True)

CRACKERS_FLAGS = {
    "BARI_RECAL_P0": "on",
    "BARI_SHELF_RELATIVE_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_FAT_TECH_V1": "on",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
}

for k, v in CRACKERS_FLAGS.items():
    os.environ[k] = v

from input_loader import load_product, validate_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, compute_confidence
from trace_writer import assemble_trace
from structural_classifier import classify_structural_class


def score_one(product: dict) -> dict:
    prod = {k: v for k, v in product.items() if not k.startswith("_")}
    signals = extract_signals(prod)
    cat_result = classify_category(prod)
    l3 = signals["L3_inferred_classifications"]
    nova_result = infer_nova(prod, l3)
    eval_result = assign_evaluation_scope(prod, cat_result["category"])
    score_result = score_product(prod, signals, cat_result, nova_result, eval_result)
    trace = assemble_trace(prod, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    trace["_router_category"] = cat_result["category"]
    trace["_router_confidence"] = cat_result["category_confidence"]
    return trace


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    print(f"BSIP1 files found: {len(bsip1_files)}")
    print(f"Flags: {CRACKERS_FLAGS}")

    scored = 0
    results = []
    router_mismatches = []

    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        errors = validate_product(product)
        product["_load_errors"] = errors

        pid = product.get("canonical_product_id", fpath.stem)
        barcode = product.get("barcode", "")

        try:
            trace = score_one(product)
        except Exception as e:
            print(f"  ERROR scoring {pid}: {e}")
            results.append({"pid": pid, "barcode": barcode, "error": str(e)})
            continue

        product_dir = BSIP2_OUT / str(pid)
        product_dir.mkdir(parents=True, exist_ok=True)
        trace_path = product_dir / "bsip2_trace.json"
        trace_path.write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        scored += 1

        score = trace.get("final_score_estimate")
        grade = trace.get("grade_estimate")
        name = product.get("canonical_name_he", "?")
        router_cat = trace.get("_router_category")
        router_conf = trace.get("_router_confidence")
        if router_cat != "cracker":
            router_mismatches.append({"barcode": barcode, "name": name, "router_category": router_cat})
        print(f"  {barcode} | {name[:35]:35s} | score={score} grade={grade} | router={router_cat}@{router_conf}")
        results.append({
            "pid": pid, "barcode": barcode, "name": name,
            "score": score, "grade": grade,
            "router_category": router_cat, "router_confidence": router_conf,
        })

    print(f"\nScored: {scored}/{len(bsip1_files)}")
    print(f"Router mismatches (not routed to 'cracker'): {len(router_mismatches)}")
    for m in router_mismatches:
        print(f"  {m}")

    run_record = {
        "run_id": "run_ricecakes_conform_001",
        "task": "TASK-516",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_OUT),
        "scored_count": scored,
        "flags": CRACKERS_FLAGS,
        "results": results,
        "router_mismatches": router_mismatches,
    }
    run_record_path = BSIP2_OUT.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
