"""
TASK-413 — Re-derive BSIP2 traces from the authoritative BSIP1 corpus
(score_bars_task362_20260620_143230/output) at the binding config flags.

Flags (from c38bc6fad snacks.json):
  BARI_SHELF_RELATIVE_V1=off
  BARI_SODIUM_SHELF_RELATIVE_V1=off
  BARI_RECAL_P0=off
  BARI_GRAD_SODIUM_V1=off
  BARI_DAIRY_PROTEIN_REWEIGHT_V1=off
  BARI_REDLABEL_V1=off
  BARI_SODIUM_CEREAL=off
  BARI_FAT_TECH_V1=on
  BARI_D4_SCORE_V1=on

Output: C:\bari_snacks\02_products\snack_bars\bsip2_outputs\task413_rederive\products\
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

# Set flags BEFORE importing the engine (flags read at import time via os.environ.get)
os.environ["BARI_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_SODIUM_SHELF_RELATIVE_V1"] = "off"
os.environ["BARI_RECAL_P0"] = "off"
os.environ["BARI_GRAD_SODIUM_V1"] = "off"
os.environ["BARI_DAIRY_PROTEIN_REWEIGHT_V1"] = "off"
os.environ["BARI_REDLABEL_V1"] = "off"
os.environ["BARI_SODIUM_CEREAL"] = "off"
os.environ["BARI_FAT_TECH_V1"] = "on"
os.environ["BARI_D4_SCORE_V1"] = "on"

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BSIP2_SRC = pathlib.Path(r"C:\bari_snacks\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(BSIP2_SRC))
# Also add snack_bars for run_task360_phase3 imports (shared utilities)
SNACKS_DIR = pathlib.Path(r"C:\bari_snacks\02_products\snack_bars")
sys.path.insert(0, str(SNACKS_DIR))
_SHARED = pathlib.Path(r"C:\bari_snacks\03_operations\bsip0\scrape\_shared")
sys.path.insert(0, str(_SHARED))

from input_loader import load_product, validate_product
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

CORPUS_DIR = pathlib.Path(r"C:\Bari\03_operations\bsip1\score_bars_task362_20260620_143230\output")
# write_trace adds products/<pid>/ under OUT_BASE, so the generator's run_products_dir
# should point to OUT_BASE/products (where per-product subdirs live).
OUT_BASE = pathlib.Path(r"C:\bari_snacks\02_products\snack_bars\bsip2_outputs\task413_rederive")
OUT_BASE.mkdir(parents=True, exist_ok=True)
# OUT_DIR is what we pass to write_trace — it will create products/<pid>/bsip2_trace.json under it
OUT_DIR = OUT_BASE


def run_single(bsip1_path: pathlib.Path) -> dict:
    try:
        product = load_product(bsip1_path)
        product["_source_path"] = str(bsip1_path)
        errors = validate_product(product)
        product["_load_errors"] = errors

        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = score_product(product, signals, cat_result, nova_result, eval_result)
        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)

        barcode = product.get("barcode", "unknown")
        trace_dir = OUT_DIR / f"bsip1_{barcode}"
        trace_dir.mkdir(parents=True, exist_ok=True)
        write_trace(trace, trace_dir)
        return {"status": "ok", "barcode": barcode, "trace": trace}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "barcode": bsip1_path.stem}


def main():
    bsip1_files = sorted(CORPUS_DIR.glob("bsip1_*.json"))
    print(f"Corpus: {len(bsip1_files)} BSIP1 files in {CORPUS_DIR}")
    print(f"Output: {OUT_DIR}")
    print(f"Flags: FAT_TECH=on D4=on SHELF_REL=off RECAL_P0=off GRAD_SODIUM=off")
    print()

    results = []
    errors = []
    for bsip1_path in bsip1_files:
        r = run_single(bsip1_path)
        if r["status"] == "ok":
            trace = r["trace"]
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate") or trace.get("grade")
            barcode = r["barcode"]
            task405 = "CLEAN" if trace.get("_task405_clean") else ""
            # check in the bsip1 file itself
            bsip1_data = json.loads(bsip1_path.read_text(encoding="utf-8"))
            task405_flag = "CLEAN" if bsip1_data.get("_task405_clean") else ""
            results.append({
                "barcode": barcode,
                "score": round(score, 1) if score is not None else None,
                "grade": grade,
                "task405_clean": bool(task405_flag),
            })
            print(f"  OK  {barcode:16} score={score!r:6} grade={grade} {task405_flag}")
        else:
            errors.append(r)
            print(f"  ERR {r['barcode']:16} {r['error']}")

    print()
    print(f"Scored: {len(results)}, Errors: {len(errors)}")

    # Write manifest
    manifest = {
        "run_id": "task413_rederive",
        "corpus_dir": str(CORPUS_DIR),
        "flags": {
            "BARI_FAT_TECH_V1": "on",
            "BARI_D4_SCORE_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_REDLABEL_V1": "off",
        },
        "product_count": len(results),
        "error_count": len(errors),
        "products": sorted(results, key=lambda x: -(x["score"] or 0)),
        "errors": errors,
    }
    manifest_path = OUT_BASE / "task413_rederive_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
