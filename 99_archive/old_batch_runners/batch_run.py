"""
BSIP2 Prototype v0 — Batch Runner
Runs full BSIP2 pipeline against all frozen BSIP1 products.
Writes per-product traces and summary reports.
"""
import sys
import json
import pathlib
import logging
import datetime
import collections

# Ensure src/ is on the path
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

BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
OUTPUT_ROOT  = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs")
REPORT_ROOT  = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\reports")


def run_pipeline(product: dict) -> dict:
    """Run the full BSIP2 pipeline for one product. Returns the trace dict."""
    signals    = extract_signals(product)
    cat_result = classify_category(product)
    l3         = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    return assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)


def _load_previous_scores(output_root: pathlib.Path) -> dict:
    """Load scores from existing trace files before the run overwrites them."""
    old = {}
    products_dir = output_root / "products"
    if not products_dir.exists():
        return old
    for trace_file in products_dir.glob("*/bsip2_trace.json"):
        try:
            with open(trace_file, encoding="utf-8") as f:
                data = json.load(f)
            pid = (data.get("input_reference") or {}).get("canonical_product_id")
            if pid:
                old[pid] = {
                    "score": data.get("final_score_estimate"),
                    "grade": data.get("grade_estimate"),
                    "flags": data.get("unresolved_flags") or [],
                    "category_instability": data.get("category_instability_flag"),
                }
        except Exception:
            pass
    return old


def run_batch():
    log.info("=== BSIP2 Prototype v0 — Batch Run ===")
    log.info("Source: %s", BSIP1_SOURCE)
    log.info("Output: %s", OUTPUT_ROOT)

    old_scores = _load_previous_scores(OUTPUT_ROOT)
    log.info("Previous scores loaded: %d products (for delta report)", len(old_scores))

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
            log.info("  %s → score=%s grade=%s  [%s]", pid, score, grade,
                     trace.get("evaluation_status"))
        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("Batch complete. Processed: %d, Errors: %d", len(traces), len(errors))

    # Write reports
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    _write_batch_summary(traces, errors, products)
    _write_score_distribution(traces)
    _write_flagged_products(traces)
    _write_top_failure_candidates(traces)
    _write_category_instability(traces)
    _write_structural_emptiness(traces)
    _write_low_confidence(traces)
    _write_delta_report(traces, old_scores)

    return traces, errors


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def _md_table(headers: list, rows: list) -> str:
    widths = [max(len(h), max((len(str(r[i])) for r in rows), default=0)) for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w+2) for w in widths) + "|"
    lines = [row_line(headers), sep] + [row_line(r) for r in rows]
    return "\n".join(lines)


def _score_grade(trace):
    s = trace.get("final_score_estimate")
    g = trace.get("grade_estimate") or "?"
    return s, g


def _product_label(trace):
    ref = trace.get("input_reference", {})
    name = ref.get("product_name_he") or ""
    pid  = ref.get("canonical_product_id") or ""
    return f"{pid} | {name[:50]}"


def _write_batch_summary(traces, errors, products):
    run_dt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    status_counts = collections.Counter(t.get("evaluation_status") for t in traces)
    cat_counts    = collections.Counter(t.get("category") for t in traces)
    nova_counts   = collections.Counter(t.get("nova_proxy") for t in traces)
    conf_counts   = collections.Counter(t.get("confidence_band") for t in traces)

    # Separate scored products with sufficient data from insufficient ones
    insufficient = [t for t in traces if t.get("data_sufficiency") == "insufficient"]
    sufficient   = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                    and t.get("final_score_estimate") is not None]

    scores = [t.get("final_score_estimate") for t in sufficient]
    avg_score    = round(sum(scores)/len(scores), 1) if scores else "N/A"
    median_score = sorted(scores)[len(scores)//2] if scores else "N/A"

    # Grade distribution — exclude insufficient_data from the letter-grade count
    grade_counts = collections.Counter(
        t.get("grade_estimate") for t in sufficient if t.get("grade_estimate")
    )

    flagged    = sum(1 for t in traces if t.get("unresolved_flags"))
    unstable   = sum(1 for t in traces if t.get("category_instability_flag"))
    empty      = sum(1 for t in traces if (t.get("structural_emptiness_result") or {}).get("structurally_empty"))
    floors_hit = sum(1 for t in traces if t.get("floors_applied"))
    caps_hit   = sum(1 for t in traces if t.get("caps_applied"))

    lines = [
        "# BSIP2 Prototype v0 — Batch Summary",
        f"\n**Run date:** {run_dt}  ",
        f"**Source:** `{BSIP1_SOURCE}`  ",
        f"**Specification:** bsip2_concept_v1 + score_resolution_contract_SRC-v1  ",
        "",
        "## Volumes",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| BSIP1 products loaded | {len(products)} |",
        f"| Products processed | {len(traces)} |",
        f"| Pipeline errors | {len(errors)} |",
        f"| Products with sufficient data | {len(sufficient)} |",
        f"| Products with insufficient data (tentative score only) | {len(insufficient)} |",
        f"| Products with unresolved flags | {flagged} |",
        f"| Products with category instability | {unstable} |",
        f"| Products with structural emptiness | {empty} |",
        f"| Products where floor was binding | {floors_hit} |",
        f"| Products where a cap was applied | {caps_hit} |",
        "",
        "## Evaluation Status Distribution",
        "",
        _md_table(["Status","Count"], [(k,v) for k,v in sorted(status_counts.items())]),
        "",
        "## Score Statistics (sufficient-data products only)",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Count | {len(scores)} |",
        f"| Average score | {avg_score} |",
        f"| Median score | {median_score} |",
        f"| Min score | {min(scores) if scores else 'N/A'} |",
        f"| Max score | {max(scores) if scores else 'N/A'} |",
        "",
        "## Grade Distribution (sufficient-data products only)",
        "",
        _md_table(["Grade","Count"], [(k,v) for k,v in sorted(grade_counts.items())]),
        "",
        "## Category Distribution",
        "",
        _md_table(["Category","Count"], sorted(cat_counts.items(), key=lambda x: -x[1])),
        "",
        "## NOVA Proxy Distribution",
        "",
        _md_table(["NOVA Level","Count"], sorted([(str(k),v) for k,v in nova_counts.items()])),
        "",
        "## Confidence Band Distribution",
        "",
        _md_table(["Confidence Band","Count"], sorted(conf_counts.items())),
        "",
        "## Top 10 Highest Scores (sufficient data only)",
        "",
    ]

    # Rankings exclude insufficient_data products
    top10 = sorted(sufficient, key=lambda t: t.get("final_score_estimate") or 0, reverse=True)[:10]
    rows = [(i+1, _product_label(t), t.get("final_score_estimate"), t.get("grade_estimate"),
             t.get("category"), t.get("nova_proxy"))
            for i, t in enumerate(top10)]
    lines.append(_md_table(["#","Product","Score","Grade","Category","NOVA"], rows))
    lines.append("")
    lines.append("## Top 10 Lowest Scores (sufficient data only)")
    lines.append("")

    bot10 = sorted(sufficient, key=lambda t: t.get("final_score_estimate") or 0)[:10]
    rows = [(i+1, _product_label(t), t.get("final_score_estimate"), t.get("grade_estimate"),
             t.get("category"), t.get("nova_proxy"))
            for i, t in enumerate(bot10)]
    lines.append(_md_table(["#","Product","Score","Grade","Category","NOVA"], rows))

    if insufficient:
        lines += ["", "## Insufficient Data Products (tentative score, no grade)", ""]
        for t in insufficient:
            ref  = t.get("input_reference") or {}
            pid  = ref.get("canonical_product_id") or ""
            name = ref.get("product_name_he") or ""
            s    = t.get("final_score_estimate")
            conf = t.get("confidence_score")
            lines.append(f"- `{pid}` | {name[:60]} | tentative={s} conf={conf}")

    if errors:
        lines += ["", "## Pipeline Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / "batch_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Report written: %s", path)


def _write_score_distribution(traces):
    buckets = collections.defaultdict(list)
    for t in traces:
        s = t.get("final_score_estimate")
        if s is None:
            buckets["no_score"].append(t)
        elif s >= 85:
            buckets["85-100 (A)"].append(t)
        elif s >= 70:
            buckets["70-84 (B)"].append(t)
        elif s >= 55:
            buckets["55-69 (C)"].append(t)
        elif s >= 40:
            buckets["40-54 (D)"].append(t)
        else:
            buckets["0-39 (E)"].append(t)

    lines = ["# BSIP2 Prototype v0 — Score Distribution", ""]
    for band, ts in sorted(buckets.items()):
        lines.append(f"## {band} — {len(ts)} products")
        lines.append("")
        for t in sorted(ts, key=lambda x: x.get("final_score_estimate") or 0, reverse=True):
            score = t.get("final_score_estimate")
            cats  = t.get("category")
            nova  = t.get("nova_proxy")
            name  = (t.get("input_reference") or {}).get("product_name_he") or ""
            pid   = (t.get("input_reference") or {}).get("canonical_product_id") or ""
            lines.append(f"- **{score}** {pid} | {name[:60]} | cat={cats} nova={nova}")
        lines.append("")

    (REPORT_ROOT / "score_distribution.md").write_text("\n".join(lines), encoding="utf-8")


def _write_flagged_products(traces):
    flagged = [t for t in traces if t.get("unresolved_flags")]
    lines = [f"# BSIP2 Prototype v0 — Flagged Products ({len(flagged)} products)", ""]
    for t in sorted(flagged, key=lambda x: len(x.get("unresolved_flags") or []), reverse=True):
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        lines.append(f"## {pid}")
        lines.append(f"**Name:** {name}  ")
        lines.append(f"**Score:** {s} ({g})  ")
        lines.append(f"**Category:** {t.get('category')} | NOVA: {t.get('nova_proxy')}  ")
        lines.append("")
        lines.append("**Unresolved flags:**")
        for fl in t.get("unresolved_flags") or []:
            lines.append(f"- {fl}")
        lines.append("")

    (REPORT_ROOT / "flagged_products.md").write_text("\n".join(lines), encoding="utf-8")


def _write_top_failure_candidates(traces):
    scored = [t for t in traces if t.get("final_score_estimate") is not None]
    scored_sufficient = [t for t in scored if t.get("data_sufficiency") != "insufficient"]

    # Suspicious = low score + flags + context_limited
    def suspicion_score(t):
        base = -(t.get("final_score_estimate") or 100)
        base += len(t.get("unresolved_flags") or []) * 10
        if t.get("evaluation_status") == "context_limited":
            base += 5
        if t.get("category_instability_flag"):
            base += 8
        if (t.get("confidence_band") or "") in ("low", "insufficient"):
            base += 15
        return base

    suspicious = sorted(scored, key=suspicion_score, reverse=True)[:5]
    # Most correct = high score + no flags + high confidence (sufficient data only)
    def correctness_score(t):
        base = t.get("final_score_estimate") or 0
        base -= len(t.get("unresolved_flags") or []) * 10
        if t.get("confidence_band") == "high":
            base += 10
        if not t.get("category_instability_flag"):
            base += 5
        if t.get("evaluation_status") == "standard":
            base += 5
        return base

    correct = sorted(scored_sufficient, key=correctness_score, reverse=True)[:5]

    lines = ["# BSIP2 Prototype v0 — Top Failure Candidates & Most Correct", ""]
    lines.append("## 5 Most Suspicious Products")
    lines.append("")
    lines.append("These products show the most signs of scoring unreliability or architectural mismatch.")
    lines.append("")
    for t in suspicious:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        flags = t.get("unresolved_flags") or []
        drivers = t.get("explanation_drivers") or []
        lines.append(f"### {pid}")
        lines.append(f"**{name}**  ")
        lines.append(f"Score: {s} ({g}) | Category: {t.get('category')} | NOVA: {t.get('nova_proxy')} | "
                     f"Confidence: {t.get('confidence_score')} ({t.get('confidence_band')})  ")
        lines.append(f"Flags: {len(flags)} | Instability: {t.get('category_instability_flag')} | "
                     f"Status: {t.get('evaluation_status')}  ")
        lines.append("")
        if flags:
            lines.append("**Flags:**")
            for f in flags[:3]:
                lines.append(f"- {f}")
        if drivers:
            lines.append("")
            lines.append("**Score drivers:**")
            for d in drivers[:2]:
                lines.append(f"- {d}")
        lines.append("")

    lines.append("## 5 Most Correct Products")
    lines.append("")
    lines.append("These products show the clearest, most defensible scoring traces.")
    lines.append("")
    for t in correct:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        g    = t.get("grade_estimate")
        drivers = t.get("explanation_drivers") or []
        lines.append(f"### {pid}")
        lines.append(f"**{name}**  ")
        lines.append(f"Score: {s} ({g}) | Category: {t.get('category')} | NOVA: {t.get('nova_proxy')} | "
                     f"Confidence: {t.get('confidence_score')} ({t.get('confidence_band')})  ")
        lines.append("")
        if drivers:
            lines.append("**Drivers:**")
            for d in drivers[:2]:
                lines.append(f"- {d}")
        lines.append("")

    (REPORT_ROOT / "top_failure_candidates.md").write_text("\n".join(lines), encoding="utf-8")


def _write_category_instability(traces):
    unstable = [t for t in traces if t.get("category_instability_flag")]
    lines = [f"# BSIP2 Prototype v0 — Category Instability Report ({len(unstable)} products)", ""]
    for t in unstable:
        ref   = t.get("input_reference") or {}
        pid   = ref.get("canonical_product_id") or ""
        name  = ref.get("product_name_he") or ""
        s     = t.get("final_score_estimate")
        lines.append(f"## {pid}")
        lines.append(f"**{name}**  ")
        lines.append(f"Score: {s} | Primary: **{t.get('category')}** (conf={t.get('category_confidence')}) "
                     f"| Secondary: **{t.get('secondary_category')}** (conf={t.get('secondary_confidence')})  ")
        lines.append(f"Basis: {t.get('classification_basis')}  ")
        lines.append("")

    (REPORT_ROOT / "category_instability_report.md").write_text("\n".join(lines), encoding="utf-8")


def _write_structural_emptiness(traces):
    empty = [t for t in traces if (t.get("structural_emptiness_result") or {}).get("structurally_empty")]
    lines = [f"# BSIP2 Prototype v0 — Structural Emptiness Report ({len(empty)} products)", ""]
    lines.append("Products where the SRC-04 gate capped the calorie density dimension at 50.")
    lines.append("")
    for t in empty:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        se   = t.get("structural_emptiness_result") or {}
        lines.append(f"- **{s}** `{pid}` | {name[:70]}")
        lines.append(f"  SE conditions: {se.get('se_conditions')}")
        lines.append("")

    (REPORT_ROOT / "structural_emptiness_report.md").write_text("\n".join(lines), encoding="utf-8")


def _write_low_confidence(traces):
    low_conf = [t for t in traces if t.get("confidence_band") in ("low", "insufficient")]
    lines = [f"# BSIP2 Prototype v0 — Low Confidence Report ({len(low_conf)} products)", ""]
    lines.append("Products where confidence was below 60. Scores are unreliable without data improvement.")
    lines.append("")
    for t in sorted(low_conf, key=lambda x: x.get("confidence_score") or 100):
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or ""
        name = ref.get("product_name_he") or ""
        s    = t.get("final_score_estimate")
        conf = t.get("confidence_score")
        band = t.get("confidence_band")
        reds = t.get("confidence_reductions") or []
        lines.append(f"## {pid} — confidence={conf} ({band})")
        lines.append(f"**{name}** | Score: {s}  ")
        lines.append("**Confidence reductions:**")
        for r in reds[:5]:
            lines.append(f"- {r.get('factor')}: {r.get('reduction')}")
        lines.append("")

    (REPORT_ROOT / "low_confidence_report.md").write_text("\n".join(lines), encoding="utf-8")


def _write_delta_report(traces: list, old_scores: dict):
    """Compare new run results against the previous run. Written to reports/delta_report.md."""
    if not old_scores:
        (REPORT_ROOT / "delta_report.md").write_text(
            "# Delta Report\n\nNo previous run found — nothing to compare.\n", encoding="utf-8"
        )
        return

    # Per-product score changes
    score_changes = []
    for t in traces:
        pid = (t.get("input_reference") or {}).get("canonical_product_id")
        new_score = t.get("final_score_estimate")
        old = old_scores.get(pid) or {}
        old_score = old.get("score")
        if new_score is not None and old_score is not None:
            delta = round(new_score - old_score, 1)
            if abs(delta) > 5:
                score_changes.append((pid, old_score, new_score, delta, t))
    score_changes.sort(key=lambda x: abs(x[3]), reverse=True)

    # Aggregate before/after stats
    def _count_flags(entries):
        return sum(1 for v in entries if (v.get("flags") if isinstance(v, dict) else v.get("unresolved_flags") or []))

    def _count_tf_flags(entries, is_trace=False):
        total = 0
        for v in entries:
            flags = (v.get("unresolved_flags") or []) if is_trace else (v.get("flags") or [])
            if any("TRANS_FAT" in f for f in flags):
                total += 1
        return total

    old_flag_ct     = sum(1 for v in old_scores.values() if v.get("flags"))
    new_flag_ct     = sum(1 for t in traces if t.get("unresolved_flags"))
    old_tf_ct       = _count_tf_flags(old_scores.values(), is_trace=False)
    new_tf_ct       = _count_tf_flags(traces, is_trace=True)
    old_unstable_ct = sum(1 for v in old_scores.values() if v.get("category_instability"))
    new_unstable_ct = sum(1 for t in traces if t.get("category_instability_flag"))

    old_grade_dist  = collections.Counter(v.get("grade") for v in old_scores.values() if v.get("grade"))
    new_grade_dist  = collections.Counter(
        t.get("grade_estimate") for t in traces
        if t.get("data_sufficiency") != "insufficient" and t.get("grade_estimate")
    )
    new_insuff_ct   = sum(1 for t in traces if t.get("data_sufficiency") == "insufficient")

    lines = [
        "# BSIP2 Prototype v0 — Before/After Delta Report",
        "",
        "Comparing previous run (before signal hygiene fixes) to this run.",
        "",
        "## Key Metric Comparison",
        "",
        "| Metric | Before | After | Change |",
        "|--------|--------|-------|--------|",
        f"| Products with unresolved flags | {old_flag_ct} | {new_flag_ct} | {new_flag_ct - old_flag_ct:+d} |",
        f"| Trans fat flags (PRESENT / HIGH_CONCERN) | {old_tf_ct} | {new_tf_ct} | {new_tf_ct - old_tf_ct:+d} |",
        f"| Products with category instability | {old_unstable_ct} | {new_unstable_ct} | {new_unstable_ct - old_unstable_ct:+d} |",
        f"| Products with insufficient_data grade | — | {new_insuff_ct} | (new metric) |",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Before | After |",
        "|-------|--------|-------|",
    ]

    all_grades = sorted(set(list(old_grade_dist.keys()) + list(new_grade_dist.keys())))
    for g in all_grades:
        old_n = old_grade_dist.get(g, 0)
        new_n = new_grade_dist.get(g, 0)
        lines.append(f"| {g} | {old_n} | {new_n} |")
    lines.append(f"| insufficient_data | — | {new_insuff_ct} |")

    # Top/bottom 10 after
    sufficient = [t for t in traces if t.get("data_sufficiency") != "insufficient"
                  and t.get("final_score_estimate") is not None]
    top10_new = sorted(sufficient, key=lambda t: t.get("final_score_estimate") or 0, reverse=True)[:10]
    bot10_new = sorted(sufficient, key=lambda t: t.get("final_score_estimate") or 0)[:10]

    lines += [
        "",
        "## Top 10 Highest Scores (after fixes)",
        "",
        _md_table(["#","Product","Score","Grade"],
                  [(i+1, _product_label(t), t.get("final_score_estimate"), t.get("grade_estimate"))
                   for i, t in enumerate(top10_new)]),
        "",
        "## Top 10 Lowest Scores (after fixes)",
        "",
        _md_table(["#","Product","Score","Grade"],
                  [(i+1, _product_label(t), t.get("final_score_estimate"), t.get("grade_estimate"))
                   for i, t in enumerate(bot10_new)]),
    ]

    if score_changes:
        lines += [
            "",
            "## Products with Score Change > 5 Points",
            "",
            _md_table(
                ["Product ID", "Old Score", "New Score", "Delta", "Grade After"],
                [(pid, old_s, new_s, f"{delta:+.1f}", t.get("grade_estimate"))
                 for pid, old_s, new_s, delta, t in score_changes]
            ),
        ]
    else:
        lines += ["", "## Score Changes", "", "No product changed score by more than 5 points."]

    path = REPORT_ROOT / "delta_report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Report written: %s", path)


if __name__ == "__main__":
    traces, errors = run_batch()
    log.info("Done.")
