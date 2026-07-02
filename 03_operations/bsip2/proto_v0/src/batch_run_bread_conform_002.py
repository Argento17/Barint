"""
BSIP2 Batch Runner — Bread Conform v2 (run_bread_conform_002)
TASK-433: Bread re-derive after crackers split. SCORES PROTECTED.

Scores BSIP1 records from run_bread_conform_002 (23 scoreable + 2
config-excluded, same 2 as v1) using the EXACT SAME canonical bread flag
vector as batch_run_bread_conform_001.py / bread.json — this run must
byte-reproduce every one of the 23 survivors' published scores in
bread_frontend_v3.json (0.000 drift required; if any drifts, STOP, do not
ship, return BLOCKED per task instructions).

Flag set: grain/bread non-dairy (UNCHANGED from v1):
  BARI_RECAL_P0=on
  BARI_SHELF_RELATIVE_V1=off
  BARI_FAT_TECH_V1=on
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_GRAD_SODIUM_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
"""

from __future__ import annotations
import sys, json, pathlib, datetime, os

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP1_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_conform_002\output")
BSIP2_OUT = pathlib.Path(r"C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_002\products")
BSIP2_OUT.mkdir(parents=True, exist_ok=True)

# --- Bread flag set — IDENTICAL to run_bread_conform_001 (canonical, unchanged) ---
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


# Published bread_frontend_v3.json scores for the 23 survivors — used ONLY
# for the byte-identical verification diff (Step 6), never consulted by
# scoring itself.
PUBLISHED_23 = {
    "7290016245325": 94.8, "3268429": 92.7, "3268252": 89.7, "481203": 89.3,
    "481197": 88.2, "574370": 86.9, "3054183": 86.8, "2079033": 83.1,
    "2079927": 83.0, "497044": 83.0, "2079996": 82.0, "7290018500316": 81.6,
    "7290018540329": 79.2, "2079477": 75.2, "9398281": 75.0, "2079217": 70.1,
    "7290014321168": 70.0, "6451484": 69.0, "6451507": 69.0,
    "7290018500460": 69.0, "4685027": 68.0, "7290016967074": 66.0,
    "1902325": 57.7,
}


def main():
    bsip1_files = sorted(BSIP1_DIR.glob("bsip1_*.json"))
    print(f"BSIP1 files found: {len(bsip1_files)}")
    print(f"Flags: {BREAD_FLAGS}")

    scored = 0
    results = []
    drift_report = []

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

        if barcode in PUBLISHED_23:
            published = PUBLISHED_23[barcode]
            drift = None if score is None else round(score - published, 3)
            drift_report.append({
                "barcode": barcode,
                "name": name,
                "published_v3_score": published,
                "new_v2_score": score,
                "drift": drift,
            })

    print(f"\nScored: {scored}/{len(bsip1_files)}")
    print("\n=== 23-survivor byte-identical drift report (published v3 vs re-derived v2) ===")
    max_abs_drift = 0.0
    for d in drift_report:
        drift_val = abs(d["drift"]) if d["drift"] is not None else None
        if drift_val is not None:
            max_abs_drift = max(max_abs_drift, drift_val)
        print(f"  {d['barcode']} | {d['name'][:30]:30s} | published={d['published_v3_score']} new={d['new_v2_score']} drift={d['drift']}")
    print(f"\nSurvivors checked: {len(drift_report)}/23")
    print(f"Max abs drift: {max_abs_drift}")
    print(f"VERDICT: {'PASS — 0.000 drift on all 23' if max_abs_drift == 0.0 and len(drift_report) == 23 else 'BLOCKED — drift or missing survivor detected'}")

    run_record = {
        "run_id": "run_bread_conform_002",
        "task": "TASK-433",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "bsip1_dir": str(BSIP1_DIR),
        "bsip2_dir": str(BSIP2_OUT),
        "scored_count": scored,
        "flags": BREAD_FLAGS,
        "results": results,
        "survivor_23_drift_report": drift_report,
        "max_abs_drift": max_abs_drift,
        "survivors_checked": len(drift_report),
    }
    run_record_path = BSIP2_OUT.parent / "run_record.json"
    with open(run_record_path, "w", encoding="utf-8") as f:
        json.dump(run_record, f, ensure_ascii=False, indent=2)
    print(f"Run record: {run_record_path}")


if __name__ == "__main__":
    main()
