"""
BSIP2 Batch Runner — מעדנים (Dairy Desserts) run_maadanim_001.

Source: C:\Bari\03_operations\bsip1\run_maadanim_001\output\
Output: C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\
Reports: C:\Bari\02_products\maadanim\reports\

Category: dessert (dairy desserts subtype)
Router anchors: מילקי / מעדן / עדנה / יופלה / פרוביו — added to router_v2.py
Architecture: same pipeline as snack_bars / bread_retail runs.
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_maadanim_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\02_products\maadanim\reports")
CATEGORY_TAG = "maadanim"
RUN_ID       = "run_maadanim_001"

MAADANIM_SUBTYPES = {
    "milky_style", "protein_dessert", "kids_dessert", "reduced_sugar_dessert",
    "probiotic_dessert", "mousse_dessert", "pudding_dessert", "adina_style",
    "flavored_yogurt_dessert", "cream_dessert", "patisserie_dessert",
    "dairy_dessert_generic",
}


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
    st = product.get("bsip_maadanim_subtype")
    if st and st in MAADANIM_SUBTYPES:
        return st
    name = (product.get("canonical_name_he") or "").lower()
    if "חלבון" in name or "פרוטאין" in name or "protein" in name:
        return "protein_dessert"
    if "ילדים" in name or "kids" in name:
        return "kids_dessert"
    if "ללא סוכר" in name or "light" in name:
        return "reduced_sugar_dessert"
    if "מילקי" in name:
        return "milky_style"
    if "עדנה" in name:
        return "adina_style"
    if "יופלה" in name:
        return "flavored_yogurt_dessert"
    if "פרוביו" in name:
        return "probiotic_dessert"
    if "מוס" in name:
        return "mousse_dessert"
    if "פודינג" in name:
        return "pudding_dessert"
    return "dairy_dessert_generic"


def run_batch():
    log.info("=== BSIP2 מעדנים — %s ===", RUN_ID)
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        log.error("Run 02_build_bsip1_maadanim.py first.")
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
            log.info("  %-50s score=%-5s grade=%s  cat=%-18s nova=%s  sub=%-28s cap=%s",
                     pid[:50], score, grade, cat, nova, subtype, cap)
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

    grade_counts: dict[str, int] = {}
    for t in sufficient:
        g = t.get("grade_estimate", "?")
        grade_counts[g] = grade_counts.get(g, 0) + 1

    nova_counts: dict[str, int] = {}
    for t in traces:
        n = str(t.get("nova_proxy", "?"))
        nova_counts[n] = nova_counts.get(n, 0) + 1

    cat_counts: dict[str, int] = {}
    for t in traces:
        c = t.get("category", "?")
        cat_counts[c] = cat_counts.get(c, 0) + 1

    capped = [t for t in traces if t.get("binding_cap")]
    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"
                    or t.get("final_score_estimate") is None]

    lines = [
        f"# BSIP2 מעדנים — {RUN_ID} Batch Summary",
        f"\n**Run date:** {run_dt}",
        f"**Category:** {CATEGORY_TAG}",
        f"**Source:** Shufersal — real retailer scrape",
        f"**Framework:** BSIP2 proto_v0 — router_v2 with מעדנים anchors",
        f"**Products processed:** {len(traces)}",
        f"**Scored (sufficient data):** {len(sufficient)}",
        f"**Insufficient data:** {len(insufficient)}",
        f"**Pipeline errors:** {len(errors)}",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Count | % |",
        "|-------|-------|---|",
    ]
    total_suf = max(len(sufficient), 1)
    for g in ["S", "A", "B", "C", "D", "E"]:
        c = grade_counts.get(g, 0)
        lines.append(f"| {g}     | {c}     | {100*c//total_suf}% |")

    lines += [
        "",
        "## NOVA Distribution",
        "",
        "| NOVA | Count | % |",
        "|------|-------|---|",
    ]
    total_all = max(len(traces), 1)
    for n in ["1", "2", "3", "4"]:
        c = nova_counts.get(n, 0)
        lines.append(f"| NOVA{n} | {c}     | {100*c//total_all}% |")

    lines += [
        "",
        "## Category Routing Distribution",
        "",
        "| Category | Count |",
        "|----------|-------|",
    ]
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {cnt} |")

    lines += [
        "",
        f"## Caps Applied: {len(capped)} products ({100*len(capped)//total_all}%)",
        "",
        "## Score Summary (Scored Products, Sorted)",
        "",
    ]

    rows = []
    for t in sorted(sufficient, key=lambda x: -(x.get("final_score_estimate") or 0)):
        ref  = t.get("input_reference") or {}
        name = ref.get("canonical_name_he") or ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        cat  = t.get("category")
        nova = t.get("nova_proxy")
        cap  = t.get("binding_cap") or "-"
        rows.append([name[:50], s, g, cat, nova, cap])

    if rows:
        lines.append(_md_table(
            ["Product", "Score", "Grade", "Category", "NOVA", "Cap"],
            rows
        ))
    else:
        lines.append("*No scoreable products.*")

    if insufficient:
        lines += ["", "## Insufficient Data Products", ""]
        for t in insufficient[:20]:
            ref  = t.get("input_reference") or {}
            name = ref.get("canonical_name_he") or ""
            ds   = t.get("data_sufficiency", "?")
            lines.append(f"- {name[:60]}: {ds}")

    if errors:
        lines += ["", "## Pipeline Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    lines += [
        "",
        "## Category Architecture Notes",
        "",
        "Key questions to investigate in regression analysis:",
        "1. **Routing accuracy** — are all מעדן* products routing to 'dessert'?",
        "2. **יופלה routing** — flavored yogurt dessert vs. dairy_protein instability?",
        "3. **Protein dessert** — מעדן חלבון vs. dairy_protein routing conflict?",
        "4. **NOVA dominance** — what % of מעדנים are NOVA3/4?",
        "5. **Sugar cap behavior** — desserts with >17.5g sugar: cap at 55?",
        "6. **Reduced-sugar positioning** — ללא סוכר products: sweetener cap at 70?",
        "7. **Children's desserts** — distinct score pattern from adult desserts?",
        "8. **Calorie density** — milky-style products at ~130-150 kcal: where do they land?",
        "",
        "See: editorial recovery document for Cursor implementation guidance.",
    ]

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
