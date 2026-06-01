"""
BSIP2 Prototype v0 — Milk & Alternatives Batch Runner (run_001)
Runs the full BSIP2 pipeline against the 8-product adversarial milk corpus.
Source: 03_operations/bsip1/run_milk_001/output/
Output: 02_products/milk_and_alternatives/intelligence_bsip2/run_001/
"""
import sys
import json
import pathlib
import logging
import datetime
import collections

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader import load_batch
from signal_extractor import extract_signals
from category_classifier import classify_category
from nova_proxy import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine import score_product
from trace_writer import assemble_trace, write_trace
from constants import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\milk_and_alternatives\intelligence_bsip2\run_001\reports")
CATEGORY_TAG = "milk_and_alternatives"


def run_pipeline(product: dict) -> dict:
    signals     = extract_signals(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    return assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)


def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w+2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def run_batch():
    log.info("=== BSIP2 Milk & Alternatives — run_001 ===")
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)

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
            out_path = write_trace(trace, OUTPUT_ROOT)
            traces.append(trace)
            score = trace.get("final_score_estimate")
            grade = trace.get("grade_estimate")
            cat   = trace.get("category")
            nova  = trace.get("nova_proxy")
            se    = (trace.get("structural_emptiness_result") or {}).get("structurally_empty", False)
            log.info("  %-40s score=%-5s grade=%s  cat=%-15s nova=%s  SE=%s",
                     pid, score, grade, cat, nova, se)
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))
    _write_milk_summary(traces, errors)
    return traces, errors


def _write_milk_summary(traces, errors):
    run_dt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    scores = [t.get("final_score_estimate") for t in sufficient]

    lines = [
        "# BSIP2 Milk & Alternatives — run_001 Summary",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Products processed:** {len(traces)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        "## Score Summary",
        "",
    ]

    rows = []
    for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0)):
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        cat  = t.get("category")
        nova = t.get("nova_proxy")
        se   = "YES" if (t.get("structural_emptiness_result") or {}).get("structurally_empty") else "no"
        sw   = "YES" if t.get("sweetener_cap_active") else "no"
        cap  = t.get("binding_cap") or "-"
        rows.append([name[:45], s, g, cat, nova, se, cap])

    lines.append(_md_table(
        ["Product", "Score", "Grade", "Category", "NOVA", "SE Gate", "Cap"],
        rows
    ))

    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / "run_001_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
