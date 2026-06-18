#!/usr/bin/env python3
"""
TASK-254/F1 — Reconstruct cereals scoring traces for run_cereals_008
and run_cereals_multiretailer_001.

Purpose:
  Regenerate BSIP2 traces for BOTH runs into a NEW reconstruction dir.
  Does NOT touch the original run_cereals_008/ or any published artifacts.

Usage:
  cd C:\Bari\03_operations\bsip2\proto_v0\src
  set BARI_RECAL_P0=on
  python C:\Bari\03_operations\bsip0\scrape_runner\reconstruct_cereals_008.py
"""

import os, sys, json, pathlib, logging, datetime, shutil

os.environ["BARI_RECAL_P0"] = "on"

SRC = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\src")
sys.path.insert(0, str(SRC))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

CEREAL_OK = {"cereal", "breakfast_cereals", "cereal_system", "snack_bar_granola"}

RECON_ROOT = pathlib.Path(
    r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs"
)

RUNS = [
    {
        "id": "run_cereals_008",
        "bsip1": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_008\output"),
    },
    {
        "id": "run_cereals_multiretailer_001",
        "bsip1": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_multiretailer_001\output"),
    },
]


def run_pipeline(product):
    signals = extract_signals(product)
    cat = classify_category(product)
    l3 = signals["L3_inferred_classifications"]
    nova = infer_nova(product, l3)
    scope = assign_evaluation_scope(product, cat["category"])
    score = score_product(product, signals, cat, nova, scope)
    trace = assemble_trace(product, signals, cat, nova, scope, score)
    trace["structural_class"] = classify_structural_class(trace)
    return trace


def process_run(run_cfg):
    run_id = run_cfg["id"]
    recon_dir = RECON_ROOT / f"{run_id}_reconstruction"
    prod_dir = recon_dir / "products"

    if prod_dir.exists():
        shutil.rmtree(prod_dir)
    prod_dir.mkdir(parents=True, exist_ok=True)

    if not run_cfg["bsip1"].exists():
        log.error("BSIP1 source not found: %s", run_cfg["bsip1"])
        return [], []

    products = load_batch(run_cfg["bsip1"])
    log.info("[%s] BSIP1 products loaded: %d", run_id, len(products))

    traces, errors = [], []
    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, recon_dir)
            traces.append(trace)
        except Exception as e:
            log.error("[%s] PIPELINE ERROR %s: %s", run_id, pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    sufficient = [t for t in traces
                  if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    log.info("[%s] Scored: %d / %d, Errors: %d",
             run_id, len(sufficient), len(traces), len(errors))

    # Write summary
    summary = {
        "run_id": f"{run_id}_reconstruction",
        "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "engine": "proto_v0 / BARI_RECAL_P0=on (reconstruction)",
        "source": f"BSIP1 {run_id}",
        "processed": len(traces),
        "scored": len(sufficient),
        "errors": len(errors),
    }
    (recon_dir / "run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log.info("[%s] Output: %s", run_id, recon_dir)
    return traces, errors


if __name__ == "__main__":
    recal = os.environ.get("BARI_RECAL_P0", "off")
    log.info("=== Cereals trace reconstruction (BARI_RECAL_P0=%s) ===", recal)

    all_traces = {}
    for run in RUNS:
        traces, errors = process_run(run)
        all_traces[run["id"]] = traces
        log.info("---")

    log.info("Done. Reconstruction dirs:")
    for run in RUNS:
        log.info("  %s_reconstruction/", run["id"])
