"""
BSIP2 Prototype v0 — Snack Bars Batch Runner (run_snack_bars_001)
Source: Yohananof scrape — 53 canonical products across 8+ subtypes
Framework: v2 grade calibration (architecture validation run)
Purpose: validate BSIP2 routing, NOVA proxy, cap/floor logic against:
         granola instability, whole_food_fat misrouting, protein bar handling,
         fiber laundering, whole-grain laundering, NOVA dominance,
         routing contamination, cap/floor explainability.
Output: 02_products/snack_bars/bsip2_outputs/run_snack_bars_001/
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\snack_bars\reports")
CATEGORY_TAG = "snack_bars"
RUN_ID       = "run_snack_bars_001"


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


def _infer_subtype(product: dict) -> str:
    """Best-effort subtype from bsip_snack_subtype or product name."""
    st = product.get("bsip_snack_subtype")
    if st:
        return st
    name = (product.get("canonical_name_he") or product.get("product_name_he") or "").lower()
    if "granola" in name or "גרנולה" in name:
        return "granola_bar"
    if "קראנצ'י" in name or "crunchy" in name:
        return "granola_crunchy"
    if "protein" in name or "חלבון" in name:
        return "protein_bar"
    if "תמר" in name or "date" in name:
        return "date_bar"
    if "אגוז" in name or "nut" in name:
        return "nut_bar"
    if "slim" in name or "דייט" in name:
        return "diet_bar"
    if "fitness" in name or "פיטנס" in name or "pezzi" in name:
        return "fitness_bar"
    return "cereal_bar"


def run_batch():
    log.info("=== BSIP2 Snack Bars — %s ===", RUN_ID)
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
            score   = trace.get("final_score_estimate")
            grade   = trace.get("grade_estimate")
            cat     = trace.get("category")
            nova    = trace.get("nova_proxy")
            subtype = _infer_subtype(product)
            cap     = trace.get("binding_cap") or "-"
            log.info("  %-45s score=%-5s grade=%s  cat=%-22s nova=%s  sub=%-18s cap=%s",
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

    # Grade distribution
    grade_counts: dict[str, int] = {}
    for t in sufficient:
        g = t.get("grade_estimate", "?")
        grade_counts[g] = grade_counts.get(g, 0) + 1

    # NOVA distribution
    nova_counts: dict[str, int] = {}
    for t in traces:
        n = str(t.get("nova_proxy", "?"))
        nova_counts[n] = nova_counts.get(n, 0) + 1

    # Cap summary
    capped = [t for t in traces if t.get("binding_cap")]

    lines = [
        f"# BSIP2 Snack Bars — {RUN_ID} Batch Summary",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Source:** Yohananof — real retailer scrape (53 canonical products)",
        f"**Framework:** BSIP2 proto_v0 — architecture validation run",
        f"**Products processed:** {len(traces)}",
        f"**Scored:** {len(sufficient)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Count |",
        "|-------|-------|",
    ]
    for g in ["S", "A", "B", "C", "D", "E"]:
        lines.append(f"| {g}     | {grade_counts.get(g, 0)}     |")

    lines += [
        "",
        "## NOVA Distribution",
        "",
        "| NOVA | Count |",
        "|------|-------|",
    ]
    for n in ["1", "2", "3", "4"]:
        lines.append(f"| NOVA{n} | {nova_counts.get(n, 0)}     |")

    lines += [
        "",
        f"## Caps Applied: {len(capped)} products",
        "",
    ]

    lines += [
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

    lines += [
        "",
        "## Architecture Validation Notes",
        "",
        "Architectural questions to investigate in regression analysis:",
        "1. **Granola instability** — does routing flip between snack_bar and breakfast_cereal?",
        "2. **whole_food_fat misrouting** — are nut-heavy bars penalized for fat quality?",
        "3. **Protein bar handling** — does protein_quality dimension reward engineered bars?",
        "4. **Fiber laundering** — bars using chicory/inulin for fiber inflation",
        "5. **Whole-grain laundering** — bars with token whole grain first-ingredient",
        "6. **NOVA dominance** — does NOVA4 classification overwhelm other dimensions?",
        "7. **Routing contamination** — are date bars / nut bars misrouted?",
        "8. **Cap/floor explainability** — are guardrail overrides traceable and defensible?",
        "",
        f"See: {REPORT_ROOT / 'snack_bars_regression_analysis.md'}",
    ]

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
