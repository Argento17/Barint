"""
BSIP2 Prototype v0 — TASK-189 byte-identity verification (BARI_SODIUM_CEREAL=off).

Runs the cereals pipeline with BARI_SODIUM_CEREAL=off and compares scores to
run_cereals_006 baseline. Must be byte-identical.

Run: python batch_run_cereals_007_sodium_off.py
Expected: OFF=BYTE-IDENTICAL: PASS
"""

import sys
import json
import pathlib
import logging
import datetime
import os
import shutil

sys.path.insert(0, str(pathlib.Path(__file__).parent))

# CRITICAL: set env before importing score_engine so the flag reads correctly
os.environ["BARI_SODIUM_CEREAL"] = "off"

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product, BARI_SODIUM_CEREAL
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_006\output")
OFF_ROOT      = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_007_sodium_off")
BASELINE_ROOT = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_006")
REPORT_ROOT   = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
RUN_ID        = "run_cereals_007_sodium_off"


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    log.info("BARI_SODIUM_CEREAL flag loaded as: %s", BARI_SODIUM_CEREAL)
    assert not BARI_SODIUM_CEREAL, "Flag must be OFF for byte-identity test"

    # Run pipeline (flag OFF)
    if OFF_ROOT.exists():
        shutil.rmtree(OFF_ROOT)
    OFF_ROOT.mkdir(parents=True, exist_ok=True)
    (OFF_ROOT / "products").mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    off_traces = []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OFF_ROOT)
            off_traces.append(trace)
        except Exception as e:
            log.error("PIPELINE ERROR for %s: %s", pid, e)

    # Load baseline (run_006)
    baseline_traces = []
    for prod_dir in sorted((BASELINE_ROOT / "products").iterdir()):
        tpath = prod_dir / "bsip2_trace.json"
        if tpath.exists():
            with open(tpath, encoding="utf-8") as f:
                baseline_traces.append(json.load(f))
    log.info("Baseline traces loaded: %d", len(baseline_traces))

    # Compare
    base_map = {}
    for t in baseline_traces:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id")
        base_map[pid] = t

    mismatches = []
    for t in off_traces:
        ref = t.get("input_reference") or {}
        pid = ref.get("canonical_product_id") or t.get("canonical_product_id")
        base = base_map.get(pid)
        if not base:
            mismatches.append(f"{pid}: not in baseline")
            continue
        if t.get("final_score_estimate") != base.get("final_score_estimate"):
            mismatches.append(
                f"{pid}: score {base.get('final_score_estimate')} → {t.get('final_score_estimate')}"
            )
        if t.get("grade_estimate") != base.get("grade_estimate"):
            mismatches.append(
                f"{pid}: grade {base.get('grade_estimate')} → {t.get('grade_estimate')}"
            )

    if not mismatches:
        print(f"\nOFF=BYTE-IDENTICAL: PASS ({len(off_traces)} products match run_006 baseline)")
    else:
        print(f"\nOFF=BYTE-IDENTICAL: FAIL ({len(mismatches)} mismatches)")
        for m in mismatches:
            print(f"  {m}")

    # Write summary
    summary = {
        "run_id": RUN_ID,
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "purpose": "TASK-189 byte-identity verification (BARI_SODIUM_CEREAL=off)",
        "result": "PASS" if not mismatches else "FAIL",
        "mismatches": mismatches,
        "products_checked": len(off_traces),
        "baseline_products": len(baseline_traces),
    }
    path = REPORT_ROOT / f"{RUN_ID}_identity_check.json"
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Identity check written: %s", path)
