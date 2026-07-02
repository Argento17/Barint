"""
BSIP2 Batch Runner — Crackers Conform (run_crackers_conform_001)
TASK-433: Crackers category split from bread (Crackers Category Constitution v1).

Scores BSIP1 records from run_crackers_conform_001 using the uniform engine.
Produces standard bsip2_trace.json in product subdirectories.

Flag set: IDENTICAL to the pinned canonical bread invocation (grain/non-dairy
vector — TASK-429 canonical invocation pattern), since crackers is a grain
product family with no dairy/shelf-relative signal:
  BARI_RECAL_P0=on
  BARI_SHELF_RELATIVE_V1=off
  BARI_FAT_TECH_V1=on
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_GRAD_SODIUM_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off

Category routing: the router (router_v2.classify_category) ALREADY routes
any product with "קרקר" in canonical_name_he to category="cracker" at
confidence 0.93 (see router_v2.py HARD_ANCHORS). score_engine.py line 3636
sets cd_table_key = category, so score_calorie_density() automatically uses
CALORIE_DENSITY_TABLES["cracker"] for these records with NO caller override
needed — this is routing correctness, not a new rule (Constitution Sec 2.3).
No explicit category= caller arg exists in this pipeline; the value is
derived from the product name via the standard router, same mechanism used
for every other category.
"""

from __future__ import annotations
import sys, json, pathlib, datetime, os

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_crackers_conform_001\output")
BSIP2_OUT = pathlib.Path(r"C:\Bari\02_products\crackers\bsip2_outputs\run_crackers_conform_001\products")
BSIP2_OUT.mkdir(parents=True, exist_ok=True)

# --- Crackers flag set — identical to canonical bread invocation (grain, non-dairy) ---
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


# Legacy (published bread_frontend_v3.json) scores for the 6 products that
# were already living in the bread page under _website_cluster == "crackers".
# Used only to compute the delta report in Step 4c — NOT consulted by scoring.
LEGACY_PUBLISHED_SCORES = {
    "96086000966": 81.6,
    "96086000577": 79.6,
    "7296073134459": 74.1,
    "7296073134442": 73.3,
    "8434165658523": 69.3,
    "74252": 59.6,
}


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    print(f"BSIP1 files found: {len(bsip1_files)}")
    print(f"Flags: {CRACKERS_FLAGS}")

    scored = 0
    results = []
    deltas = []

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
        print(f"  {barcode} | {name[:35]} | score={score} grade={grade} | router_category={router_cat}")
        results.append({
            "pid": pid,
            "barcode": barcode,
            "name": name,
            "score": score,
            "grade": grade,
            "router_category": router_cat,
        })

        if barcode in LEGACY_PUBLISHED_SCORES:
            legacy = LEGACY_PUBLISHED_SCORES[barcode]
            delta = None if score is None else round(score - legacy, 3)
            deltas.append({
                "barcode": barcode,
                "name": name,
                "legacy_published_score": legacy,
                "new_crackers_table_score": score,
                "delta": delta,
            })

    print(f"\nScored: {scored}/{len(bsip1_files)}")
    print("\n=== Legacy-6 delta report (published bread_frontend_v3 vs fresh crackers run) ===")
    for d in deltas:
        print(f"  {d['barcode']} | {d['name'][:30]:30s} | legacy={d['legacy_published_score']} new={d['new_crackers_table_score']} delta={d['delta']}")

    run_record = {
        "run_id": "run_crackers_conform_001",
        "task": "TASK-433",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_OUT),
        "scored_count": scored,
        "flags": CRACKERS_FLAGS,
        "results": results,
        "legacy_6_delta_report": deltas,
    }
    run_record_path = BSIP2_OUT.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
