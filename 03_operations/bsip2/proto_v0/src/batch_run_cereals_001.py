"""
BSIP2 Prototype v0 — Breakfast Cereals Batch Runner (run_cereals_001)
Source: Yohananof scrape — 45 canonical products across 8 subtypes
Framework: v2 grade calibration (same as run_004_recalibrated)
Purpose: stress-test BSIP2 against extrusion, fortification, sugar layering,
         granola density, fiber laundering, kids cereals, protein engineering.
Output: 02_products/breakfast_cereals/bsip2_outputs/run_cereals_001/
"""
import sys
import json
import pathlib
import logging
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from router_v2 import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade
from structural_classifier import classify_structural_class

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
CATEGORY_TAG = "breakfast_cereals"
RUN_ID       = "run_cereals_001"


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


def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w+2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def run_batch():
    log.info("=== BSIP2 Breakfast Cereals — %s ===", RUN_ID)
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    log.info("Products loaded: %d", len(products))

    traces = []
    errors = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            score  = trace.get("final_score_estimate")
            grade  = trace.get("grade_estimate")
            cat    = trace.get("category")
            nova   = trace.get("nova_proxy")
            se     = (trace.get("structural_emptiness_result") or {}).get("structurally_empty", False)
            subtype = product.get("bsip_cereal_subtype", "?")
            cap    = trace.get("binding_cap") or "-"
            log.info("  %-45s score=%-5s grade=%s  cat=%-18s nova=%s  sub=%-18s cap=%s",
                     pid, score, grade, cat, nova, subtype, cap)
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(traces, errors)
    return traces, errors


def _write_summary(traces, errors):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]

    lines = [
        f"# BSIP2 Breakfast Cereals — {RUN_ID} Batch Summary",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Source:** Yohananof — real retailer scrape (65 raw observations → 45 canonical products)",
        f"**Framework:** v2 grade calibration (same as run_004_recalibrated)",
        f"**Products processed:** {len(traces)}",
        f"**Scored:** {len(sufficient)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        "## Score Summary",
        "",
    ]

    rows = []
    for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0)):
        ref   = t.get("input_reference") or {}
        name  = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
        s     = t.get("final_score_estimate")
        g     = t.get("grade_estimate")
        cat   = t.get("category")
        nova  = t.get("nova_proxy")
        se    = "YES" if (t.get("structural_emptiness_result") or {}).get("structurally_empty") else "no"
        cap   = t.get("binding_cap") or "-"
        rows.append([name[:48], s, g, cat, nova, se, cap])

    if rows:
        lines.append(_md_table(
            ["Product", "Score", "Grade", "Category", "NOVA", "SE Gate", "Cap"],
            rows
        ))
    else:
        lines.append("*No scoreable products.*")

    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
