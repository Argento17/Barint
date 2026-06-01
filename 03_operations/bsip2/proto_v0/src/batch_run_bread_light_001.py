"""
BSIP2 Prototype v0 — Bread-Light Stress Test Batch Runner (run_bread_light_001)
Source: Synthetic corpus — 32 products across 6 stress groups (A-F)
Framework: same scoring engine as all active runs
Purpose: expose weaknesses in matrix integrity, flour semantics, routing,
         structural classes, fiber laundering, seed halo, fermentation interpretation.
Output: 02_products/bread_light/bsip2_outputs/run_bread_light_001/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_light_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\bread_light\bsip2_outputs\run_bread_light_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\bread_light\reports")
CATEGORY_TAG = "bread_light"
RUN_ID       = "run_bread_light_001"


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
    log.info("=== BSIP2 Bread-Light Stress Test — %s ===", RUN_ID)
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    # Skip manifest
    products = [p for p in products if isinstance(p, dict) and p.get("schema_version")]
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
            group  = product.get("bsip_stress_group", "?")
            sc     = (trace.get("structural_class") or {}).get("structural_class", "?")
            cap    = trace.get("binding_cap") or "-"
            name   = (product.get("canonical_name_he") or "")[:40]
            log.info("  [%s] %-42s score=%-5s grade=%s  cat=%-18s nova=%s  sc=%s  cap=%s",
                     group, pid, score, grade, cat, nova, sc, cap)
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(traces, errors, products)
    return traces, errors


def _write_summary(traces, errors, products):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build lookup: pid → product for stress metadata
    pid_to_product = {p.get("canonical_product_id"): p for p in products}

    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]

    lines = [
        f"# BSIP2 Bread-Light Stress Test — {RUN_ID} Batch Summary",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Source:** Synthetic corpus — 32 products across 6 stress groups (A-F)",
        f"**Purpose:** Ontology pressure test (grain structure, flour degradation, routing, fermentation)",
        f"**Products processed:** {len(traces)}",
        f"**Scored:** {len(sufficient)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        "## Score Summary by Stress Group",
        "",
    ]

    rows = []
    for t in sorted(sufficient, key=lambda x: (
        pid_to_product.get(x.get("product_id"), {}).get("bsip_stress_group", "Z"),
        -(x.get("final_score_estimate") or 0)
    )):
        pid   = t.get("product_id") or t.get("canonical_product_id") or ""
        prod  = pid_to_product.get(pid, {})
        ref   = t.get("input_reference") or {}
        name  = ref.get("canonical_name_he") or ref.get("product_name_he") or prod.get("canonical_name_he") or ""
        group = prod.get("bsip_stress_group", "?")
        s     = t.get("final_score_estimate")
        g     = t.get("grade_estimate")
        cat   = t.get("category")
        nova  = t.get("nova_proxy")
        sc    = (t.get("structural_class") or {}).get("structural_class", "?")
        cap   = t.get("binding_cap") or "-"
        rows.append([group, name[:42], s, g, cat, nova, sc, cap])

    if rows:
        lines.append(_md_table(
            ["Grp", "Product", "Score", "Grade", "Category", "NOVA", "Struct", "Cap"],
            rows
        ))
    else:
        lines.append("*No scoreable products.*")

    if errors:
        lines += ["", "## Pipeline Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
