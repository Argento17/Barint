"""
BSIP2 Score Synthesis Calibration — batch_run_synthesis_calibration_001

Runs the bread-light corpus (32 products) through the full BSIP2 pipeline
PLUS the new Score Synthesis Layer v1. Produces before/after comparison data
for the 6 validation reports.

Source corpus: same BSIP1 products as run_bread_light_002.
Baseline for comparison: run_bread_light_002 traces.
"""
import sys
import json
import pathlib
import logging
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader       import load_batch
from signal_extractor   import extract_signals
from router_v2          import classify_category
from nova_proxy         import infer_nova
from evaluation_scope   import assign_evaluation_scope
from score_engine       import score_product
from trace_writer       import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from bakery_semantics   import run_bakery_semantics
from score_synthesis    import run_synthesis
from constants          import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

BSIP1_SOURCE  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_bread_light_001\output")
BASELINE_ROOT = pathlib.Path(r"C:\Bari\02_products\bread_light\bsip2_outputs\run_bread_light_002\products")
OUTPUT_ROOT   = pathlib.Path(r"C:\Bari\02_products\bread_light\bsip2_outputs\run_synthesis_calibration_001")
REPORT_ROOT   = pathlib.Path(r"C:\Bari\03_operations\reports\synthesis_calibration")
RUN_ID        = "run_synthesis_calibration_001"


def _load_baseline(pid: str) -> dict | None:
    p = BASELINE_ROOT / pid / "bsip2_trace.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)

    bakery_result = run_bakery_semantics(product, cat_result["category"], l3)
    trace["bakery_semantics"] = bakery_result
    trace["structural_class"] = classify_structural_class(trace, bakery_result)
    trace["synthesis_result"] = run_synthesis(trace)

    return trace


def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def run_batch():
    log.info("=== BSIP2 Synthesis Calibration 001 ===")
    log.info("Source:   %s", BSIP1_SOURCE)
    log.info("Baseline: %s", BASELINE_ROOT)
    log.info("Output:   %s", OUTPUT_ROOT)

    if not BSIP1_SOURCE.exists():
        log.error("BSIP1 source not found: %s", BSIP1_SOURCE)
        return [], []

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / "products").mkdir(parents=True, exist_ok=True)

    products = load_batch(BSIP1_SOURCE)
    products = [p for p in products if isinstance(p, dict) and p.get("schema_version")]
    log.info("Products loaded: %d", len(products))

    traces  = []
    errors  = []
    comparisons = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace    = run_pipeline(product)
            baseline = _load_baseline(pid)
            write_trace(trace, OUTPUT_ROOT)

            syn   = trace.get("synthesis_result") or {}
            base  = syn.get("base_score")
            synth = syn.get("synthesized_score")
            delta = round(synth - base, 1) if (base is not None and synth is not None) else None
            bg    = syn.get("base_grade")
            sg    = syn.get("synthesized_grade")

            bak   = trace.get("bakery_semantics") or {}
            gss   = bak.get("grain_structure_score", "—")
            fq    = (bak.get("fermentation_quality") or {}).get("fermentation_quality", "—")
            fibrq = (bak.get("fiber_source_quality") or {}).get("fiber_source_quality", "—")
            sc    = (trace.get("structural_class") or {}).get("primary", "?")
            group = product.get("bsip_stress_group", "?")

            log.info("  [%s] %-40s base=%-5s(%s) → synth=%-5s(%s) Δ=%+.1f  gss=%s ferm=%s fiber=%s sc=%s",
                     group, pid, base, bg, synth, sg,
                     delta if delta is not None else 0,
                     f"{gss:.0f}" if isinstance(gss, float) else gss,
                     fq[:4] if isinstance(fq, str) else fq,
                     fibrq[:4] if isinstance(fibrq, str) else fibrq,
                     sc)

            traces.append(trace)
            comparisons.append({
                "product_id":  pid,
                "product":     product,
                "trace":       trace,
                "baseline":    baseline,
                "base_score":  base,
                "synth_score": synth,
                "delta":       delta,
                "base_grade":  bg,
                "synth_grade": sg,
                "group":       group,
                "gss":         gss,
                "ferm_q":      fq,
                "fiber_q":     fibrq,
                "sc_primary":  sc,
            })
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))
    _write_summary(comparisons, errors)

    # Write comparison data as JSON for report generator
    cmp_path = OUTPUT_ROOT / "synthesis_comparison_data.json"
    export = []
    for c in comparisons:
        ref  = (c["trace"].get("input_reference") or {})
        name = ref.get("product_name_he") or ref.get("canonical_name_he") or c["product_id"]
        syn  = c["trace"].get("synthesis_result") or {}
        adjs = syn.get("synthesis_adjustments") or []
        conf = (syn.get("synthesis_confidence") or {})
        export.append({
            "product_id":    c["product_id"],
            "name":          name,
            "group":         c["group"],
            "base_score":    c["base_score"],
            "synth_score":   c["synth_score"],
            "delta":         c["delta"],
            "base_grade":    c["base_grade"],
            "synth_grade":   c["synth_grade"],
            "gss":           c["gss"],
            "ferm_q":        c["ferm_q"],
            "fiber_q":       c["fiber_q"],
            "sc_primary":    c["sc_primary"],
            "adjustments":   adjs,
            "confidence":    conf.get("synthesis_confidence"),
            "conf_factors":  conf.get("confidence_factors") or [],
            "nova":          c["trace"].get("nova_proxy"),
            "category":      c["trace"].get("category"),
            "adj_clamped":   syn.get("adjustment_clamped", False),
        })
    cmp_path.write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Comparison data written: %s", cmp_path)

    return traces, errors, comparisons


def _write_summary(comparisons, errors):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    scored = [c for c in comparisons if c["synth_score"] is not None]

    # Group stats
    groups: dict[str, list] = {}
    for c in scored:
        g = c["group"]
        groups.setdefault(g, []).append(c)

    lines = [
        f"# BSIP2 Score Synthesis Calibration — {RUN_ID}",
        f"\n**Run date:** {run_dt}",
        f"**Corpus:** bread_light (32 synthetic products, 6 stress groups)",
        f"**Products processed:** {len(comparisons)}  |  **Scored:** {len(scored)}  |  **Errors:** {len(errors)}",
        "",
        "## Score Shift Summary by Group",
        "",
    ]

    grp_rows = []
    for g in sorted(groups.keys()):
        items  = groups[g]
        avg_b  = round(sum(c["base_score"] for c in items if c["base_score"]) / len(items), 1)
        avg_s  = round(sum(c["synth_score"] for c in items if c["synth_score"]) / len(items), 1)
        avg_d  = round(avg_s - avg_b, 1)
        n_up   = sum(1 for c in items if (c["delta"] or 0) > 0)
        n_down = sum(1 for c in items if (c["delta"] or 0) < 0)
        n_same = sum(1 for c in items if (c["delta"] or 0) == 0)
        grp_rows.append([g, len(items), avg_b, avg_s, f"{avg_d:+.1f}", n_up, n_same, n_down])

    lines.append(_md_table(
        ["Group", "N", "Avg Base", "Avg Synth", "Avg Δ", "↑Up", "=Same", "↓Down"],
        grp_rows
    ))

    # Full product table
    lines += ["", "## Full Product Comparison", ""]
    rows = []
    for c in sorted(scored, key=lambda x: (x["group"], -(x["synth_score"] or 0))):
        ref  = (c["trace"].get("input_reference") or {})
        name = ref.get("product_name_he") or ref.get("canonical_name_he") or c["product_id"]
        d    = c["delta"]
        d_str = f"{d:+.1f}" if d is not None else "—"
        gss  = c["gss"]
        gss_s = f"{gss:.0f}" if isinstance(gss, float) else str(gss)
        fiber = (c["fiber_q"] or "")[:4]
        ferm  = (c["ferm_q"] or "")[:5]
        rows.append([
            c["group"], name[:40], c["base_score"], c["base_grade"],
            c["synth_score"], c["synth_grade"], d_str,
            c["sc_primary"], gss_s, ferm, fiber
        ])

    lines.append(_md_table(
        ["Grp", "Product", "Base", "BG", "Synth", "SG", "Δ", "SC", "GSS", "Ferm", "Fiber"],
        rows
    ))

    # Grade shift analysis
    grade_changes = [(c["base_grade"], c["synth_grade"]) for c in scored
                     if c["base_grade"] != c["synth_grade"]]
    if grade_changes:
        lines += ["", "## Grade Changes", ""]
        gc_rows = []
        for c in scored:
            if c["base_grade"] != c["synth_grade"]:
                ref  = (c["trace"].get("input_reference") or {})
                name = ref.get("product_name_he") or ""
                gc_rows.append([c["group"], name[:38], c["base_grade"], c["synth_grade"],
                                 f"{c['delta']:+.1f}" if c["delta"] is not None else "—"])
        lines.append(_md_table(["Grp", "Product", "From", "To", "Δ"], gc_rows))

    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / f"{RUN_ID}_batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


if __name__ == "__main__":
    traces, errors, comparisons = run_batch()
    log.info("Done. Run generate_synthesis_calibration_reports.py for full analysis.")
