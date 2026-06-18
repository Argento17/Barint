"""
BSIP2 Batch Runner — Bread Conform (run_bread_conform_001)
TASK-322: Bread category spine conformance.

Scores BSIP1 records from run_bread_conform_001 using the uniform engine.
Produces standard bsip2_trace.json in product subdirectories.

Flag set: grain/bread non-dairy
  BARI_RECAL_P0=on (standard for spine-conformed categories)
  BARI_SHELF_RELATIVE_V1=off (no shelf-relative for bread — same as cereals)
  BARI_FAT_TECH_V1=on (default ON as of TASK-278/284E)
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off (bread is NOT dairy)
  BARI_GRAD_SODIUM_V1=off (no graduated sodium for bread)
  BARI_REDLABEL_V1=off (de-anchor per standing directive)
  BARI_SODIUM_CEREAL=off (bread not a cereal)

Rationale: Bread is a grain product. Closest analog = cereals.
Cereals uses RECAL_P0=on, FAT_TECH=on, no shelf-rel, no dairy flags.
Bread inherits this set — sodium is factored in through standard engine
scoring (sodium_mg present for most products), no special sodium mode needed.
"""

from __future__ import annotations
import sys, json, pathlib, datetime, os

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output")
BSIP2_OUT = pathlib.Path(r"C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_001\products")
BSIP2_OUT.mkdir(parents=True, exist_ok=True)

# --- Bread flag set (grain, non-dairy, mirrors cereals) ---
BREAD_FLAGS = {
    "BARI_RECAL_P0": "on",
    "BARI_SHELF_RELATIVE_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_FAT_TECH_V1": "on",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_REDLABEL_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
}

# Apply flags before importing engine
for k, v in BREAD_FLAGS.items():
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
    return trace


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    print(f"BSIP1 files found: {len(bsip1_files)}")
    print(f"Flags: {BREAD_FLAGS}")

    scored = 0
    results = []

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
        print(f"  {barcode} | {name[:35]} | score={score} grade={grade}")
        results.append({
            "pid": pid,
            "barcode": barcode,
            "name": name,
            "score": score,
            "grade": grade,
        })

    print(f"\nScored: {scored}/{len(bsip1_files)}")

    # Write run record
    run_record = {
        "run_id": "run_bread_conform_001",
        "task": "TASK-322",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_OUT),
        "scored_count": scored,
        "flags": BREAD_FLAGS,
        "results": results,
    }
    run_record_path = BSIP2_OUT.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
