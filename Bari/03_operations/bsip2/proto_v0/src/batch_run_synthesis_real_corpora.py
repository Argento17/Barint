"""
BSIP2 Score Synthesis — Real Corpora Runner
Applies Score Synthesis Layer v1 to snack_bars and cereals (real Yohananof products).

For non-bakery products:
  - bakery_semantics = None  →  no GSS / fiber / fermentation components
  - engineering_nuance still fires for class D/E/F where applicable
  - synthesis_confidence = "medium" (non-bakery)
  - All synthesis_adj = 0 for most products; only engineering signals produce movement

Output:
  snack_bars  → 02_products/snack_bars/bsip2_outputs/run_snack_bars_synthesis_001/
  cereals     → 02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/
  reports     → 03_operations/reports/synthesis_calibration/
               (snack_bars_synthesis_001_*.md, cereals_synthesis_001_*.md, combined report)
"""

import sys
import json
import pathlib
import logging
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from input_loader          import load_batch
from signal_extractor      import extract_signals
from router_v2             import classify_category
from nova_proxy            import infer_nova
from evaluation_scope      import assign_evaluation_scope
from score_engine          import score_product
from trace_writer          import assemble_trace, write_trace
from structural_classifier import classify_structural_class
from score_synthesis       import run_synthesis
from constants             import score_to_grade

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

REPORT_ROOT = pathlib.Path(r"C:\Bari\03_operations\reports\synthesis_calibration")

CORPORA = [
    {
        "name":        "snack_bars",
        "label":       "Snack Bars",
        "bsip1_source": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output"),
        "output_root":  pathlib.Path(r"C:\Bari\02_products\snack_bars\bsip2_outputs\run_snack_bars_synthesis_001"),
        "run_id":      "run_snack_bars_synthesis_001",
        "subtype_field": "bsip_snack_subtype",
    },
    {
        "name":        "cereals",
        "label":       "Breakfast Cereals",
        "bsip1_source": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output"),
        "output_root":  pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_synthesis_001"),
        "run_id":      "run_cereals_synthesis_001",
        "subtype_field": "bsip_cereal_subtype",
    },
]


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(product: dict) -> dict:
    signals      = extract_signals(product)
    cat_result   = classify_category(product)
    l3           = signals["L3_inferred_classifications"]
    nova_result  = infer_nova(product, l3)
    eval_result  = assign_evaluation_scope(product, cat_result["category"])
    score_result = score_product(product, signals, cat_result, nova_result, eval_result)
    trace        = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
    # No bakery_semantics for non-bakery categories
    trace["bakery_semantics"] = None
    trace["structural_class"] = classify_structural_class(trace, None)
    trace["synthesis_result"] = run_synthesis(trace)
    return trace


def _md_table(headers, rows):
    if not rows:
        return "_No data._"
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    def rl(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    return "\n".join([rl(headers), sep] + [rl(r) for r in rows])


def _delta_str(d):
    return f"{d:+.1f}" if d is not None else "—"


# ---------------------------------------------------------------------------
# Per-corpus run
# ---------------------------------------------------------------------------

def run_corpus(corpus: dict) -> list[dict]:
    name   = corpus["name"]
    label  = corpus["label"]
    src    = corpus["bsip1_source"]
    out    = corpus["output_root"]
    run_id = corpus["run_id"]
    sub_f  = corpus["subtype_field"]

    log.info("")
    log.info("=== %s — %s ===", label, run_id)
    log.info("Source: %s", src)
    log.info("Output: %s", out)

    if not src.exists():
        log.error("BSIP1 source not found: %s", src)
        return []

    out.mkdir(parents=True, exist_ok=True)
    (out / "products").mkdir(parents=True, exist_ok=True)

    products = load_batch(src)
    products = [p for p in products if isinstance(p, dict) and p.get("schema_version")]
    log.info("Products loaded: %d", len(products))

    records = []
    errors  = []

    for product in products:
        pid = product.get("canonical_product_id", "unknown")
        try:
            trace = run_pipeline(product)
            write_trace(trace, out)

            syn   = trace.get("synthesis_result") or {}
            base  = syn.get("base_score")
            synth = syn.get("synthesized_score")
            delta = round(synth - base, 1) if (base is not None and synth is not None) else None
            bg    = syn.get("base_grade")
            sg    = syn.get("synthesized_grade")
            sc    = (trace.get("structural_class") or {}).get("primary", "?")
            nova  = trace.get("nova_proxy")
            cat   = trace.get("category")
            sub   = product.get(sub_f, "?")
            adjs  = syn.get("synthesis_adjustments") or []

            log.info("  %-44s base=%-5s(%s) → synth=%-5s(%s) Δ=%+.1f  sc=%s nova=%s sub=%s",
                     pid, base, bg, synth, sg,
                     delta if delta is not None else 0,
                     sc, nova, str(sub)[:12])

            records.append({
                "product_id":  pid,
                "name":        ((trace.get("input_reference") or {}).get("product_name_he")
                                or (trace.get("input_reference") or {}).get("canonical_name_he")
                                or pid),
                "corpus":      name,
                "label":       label,
                "subtype":     sub,
                "category":    cat,
                "nova":        nova,
                "sc_primary":  sc,
                "base_score":  base,
                "synth_score": synth,
                "delta":       delta,
                "base_grade":  bg,
                "synth_grade": sg,
                "adjustments": adjs,
                "adj_clamped": syn.get("adjustment_clamped", False),
                "confidence":  (syn.get("synthesis_confidence") or {}).get("synthesis_confidence"),
            })

        except Exception as e:
            log.error("  PIPELINE ERROR for %s: %s", pid, e)
            import traceback; traceback.print_exc()
            errors.append({"product_id": pid, "error": str(e)})

    log.info("%s: processed=%d errors=%d", label, len(records), len(errors))
    _write_corpus_summary(corpus, records, errors)

    # Write comparison JSON for report generator
    cmp_path = out / f"{run_id}_synthesis_data.json"
    cmp_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("Data written: %s", cmp_path)

    return records


def _write_corpus_summary(corpus: dict, records: list[dict], errors: list[dict]):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    label  = corpus["label"]
    run_id = corpus["run_id"]

    scored = [r for r in records if r.get("synth_score") is not None]
    n_up   = sum(1 for r in scored if (r.get("delta") or 0) > 0)
    n_dn   = sum(1 for r in scored if (r.get("delta") or 0) < 0)
    n_same = sum(1 for r in scored if (r.get("delta") or 0) == 0)
    grade_changes = [r for r in scored if r.get("base_grade") != r.get("synth_grade")]

    # Grade distribution
    grades = ["A", "B", "C", "D", "E"]
    bg_dist = {g: sum(1 for r in scored if r.get("base_grade") == g)  for g in grades}
    sg_dist = {g: sum(1 for r in scored if r.get("synth_grade") == g) for g in grades}

    # Structural class distribution
    sc_dist: dict[str, int] = {}
    for r in scored:
        sc = r.get("sc_primary") or "?"
        sc_dist[sc] = sc_dist.get(sc, 0) + 1

    # Engineering nuance activations
    eng_fired = [r for r in scored
                 if any(a.get("component") == "engineering_nuance"
                        for a in (r.get("adjustments") or []))]

    lines = [
        f"# BSIP2 Synthesis — {label} ({run_id})",
        f"\n**Generated:** {run_dt}",
        f"**Corpus:** {label} — real Yohananof products",
        f"**Synthesis version:** score_synthesis_v1",
        f"**Products:** {len(records)}  |  **Scored:** {len(scored)}  |  **Errors:** {len(errors)}",
        "",
        "## Synthesis Impact",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Products shifted up (Δ > 0) | {n_up} |",
        f"| Products unchanged (Δ = 0) | {n_same} |",
        f"| Products shifted down (Δ < 0) | {n_dn} |",
        f"| Grade changes | {len(grade_changes)} |",
        f"| Engineering nuance fired | {len(eng_fired)} |",
        "",
        "**Note:** Synthesis v1 is bakery-focused. Non-bakery products receive only engineering",
        "type nuance adjustments (class D/E/F with GF/keto/protein-functional/hyper-palatable signals).",
        "GSS, fiber source, and fermentation components require bakery_semantics — not available here.",
        "",
        "## Grade Distribution: Base vs Synthesized",
        "",
    ]

    grade_rows = []
    for g in grades:
        b = bg_dist.get(g, 0)
        s = sg_dist.get(g, 0)
        d = s - b
        grade_rows.append([g, b, s, f"{d:+d}" if d != 0 else "0"])
    lines.append(_md_table(["Grade", "Base", "Synth", "Δ"], grade_rows))

    lines += ["", "## Structural Class Distribution", ""]
    sc_rows = [[sc, n] for sc, n in sorted(sc_dist.items())]
    lines.append(_md_table(["Structural Class", "Count"], sc_rows))

    lines += ["", "## Engineering Nuance Activations", ""]
    if eng_fired:
        eng_rows = []
        for r in sorted(eng_fired, key=lambda x: x.get("delta") or 0):
            eng_adj = next((a["adjustment"] for a in (r.get("adjustments") or [])
                            if a.get("component") == "engineering_nuance"), 0)
            reason = next(
                (a["drivers"][0][:65] if a.get("drivers") else ""
                 for a in (r.get("adjustments") or [])
                 if a.get("component") == "engineering_nuance"),
                ""
            )
            eng_rows.append([
                r.get("name", "")[:36], r.get("base_score"), r.get("synth_score"),
                _delta_str(r.get("delta")), f"{eng_adj:+.1f}",
                r.get("sc_primary", "?"), reason[:65]
            ])
        lines.append(_md_table(
            ["Product", "Base", "Synth", "Total Δ", "Eng Adj", "SC", "Reason"],
            eng_rows
        ))
    else:
        lines.append("_No engineering nuance activations in this corpus._")

    if grade_changes:
        lines += ["", "## Grade Changes", ""]
        gc_rows = []
        for r in grade_changes:
            gc_rows.append([
                r.get("name", "")[:40],
                r.get("base_grade"), r.get("synth_grade"),
                _delta_str(r.get("delta")),
                r.get("sc_primary", "?"),
                r.get("subtype", "?")
            ])
        lines.append(_md_table(["Product", "From", "To", "Δ", "SC", "Subtype"], gc_rows))

    lines += ["", "## Full Score Table", ""]
    rows = []
    for r in sorted(scored, key=lambda x: -(x.get("synth_score") or 0)):
        d = r.get("delta")
        rows.append([
            r.get("name", "")[:42],
            r.get("base_score"), r.get("base_grade"),
            r.get("synth_score"), r.get("synth_grade"),
            _delta_str(d),
            r.get("sc_primary", "?"),
            r.get("nova"), str(r.get("subtype", ""))[:14],
        ])
    lines.append(_md_table(
        ["Product", "Base", "BG", "Synth", "SG", "Δ", "SC", "NOVA", "Subtype"],
        rows
    ))

    if errors:
        lines += ["", "## Errors", ""]
        for e in errors:
            lines.append(f"- `{e['product_id']}`: {e['error']}")

    path = REPORT_ROOT / f"{run_id}_summary.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Summary written: %s", path)


# ---------------------------------------------------------------------------
# Combined cross-corpus report
# ---------------------------------------------------------------------------

def write_combined_report(all_records: list[dict]):
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    scored = [r for r in all_records if r.get("synth_score") is not None]
    eng_fired = [r for r in scored
                 if any(a.get("component") == "engineering_nuance"
                        for a in (r.get("adjustments") or []))]

    # By corpus
    by_corpus: dict[str, list] = {}
    for r in scored:
        by_corpus.setdefault(r["corpus"], []).append(r)

    # Structural class distribution across both
    sc_dist: dict[str, int] = {}
    for r in scored:
        sc = r.get("sc_primary") or "?"
        sc_dist[sc] = sc_dist.get(sc, 0) + 1

    lines = [
        "# BSIP2 Score Synthesis — Real Corpora Combined Report",
        f"\n**Generated:** {run_dt}",
        f"**Synthesis version:** score_synthesis_v1",
        f"**Total products:** {len(scored)} across 2 corpora",
        "",
        "## Corpus Summary",
        "",
    ]

    corpus_rows = []
    for corp, items in sorted(by_corpus.items()):
        n_up   = sum(1 for r in items if (r.get("delta") or 0) > 0)
        n_dn   = sum(1 for r in items if (r.get("delta") or 0) < 0)
        n_same = sum(1 for r in items if (r.get("delta") or 0) == 0)
        eng    = sum(1 for r in items
                     if any(a.get("component") == "engineering_nuance"
                            for a in (r.get("adjustments") or [])))
        gc     = sum(1 for r in items if r.get("base_grade") != r.get("synth_grade"))
        corpus_rows.append([corp, len(items), n_up, n_same, n_dn, gc, eng])
    lines.append(_md_table(
        ["Corpus", "N", "↑Up", "=Same", "↓Down", "Grade Changes", "Eng Nuance Fired"],
        corpus_rows
    ))

    lines += ["", "## Structural Class Distribution (combined)", ""]
    sc_rows = [[sc, n] for sc, n in sorted(sc_dist.items())]
    lines.append(_md_table(["SC", "Count"], sc_rows))

    lines += [
        "",
        "## Synthesis v1 Scope for Non-Bakery Corpora",
        "",
        "### What fires",
        "- **Engineering nuance** (class D/E/F only): gluten-free (+7 w/ isolated fiber, +3 without),",
        "  keto (+8 w/ isolated fiber, +2 without), protein-functional (+1.5),",
        "  hyper-palatable class-F confirmation (−3).",
        "",
        "### What does NOT fire (requires bakery_semantics)",
        "- **Fiber source quality discount** — no GSS, no fiber_source_quality computed",
        "- **Fermentation credit** — no fermentation_quality computed",
        "- **GSS coherence adjustment** — grain_structure_score not available",
        "",
        "### Implication",
        "The synthesis pass-through rate for non-bakery is high (~80–90%) by design.",
        "Products that shift are those where structural class + L3 signals clearly indicate",
        "engineering intent (hyper-palatable F-class) or functional necessity (GF/keto E-class).",
        "",
        "## Engineering Nuance Activations (all products)", "",
    ]

    if eng_fired:
        eng_rows = []
        for r in sorted(eng_fired, key=lambda x: x.get("delta") or 0):
            eng_adj = next((a["adjustment"] for a in (r.get("adjustments") or [])
                            if a.get("component") == "engineering_nuance"), 0)
            reason = next(
                (a["drivers"][0][:55] if a.get("drivers") else ""
                 for a in (r.get("adjustments") or [])
                 if a.get("component") == "engineering_nuance"),
                ""
            )
            eng_rows.append([
                r["corpus"], r.get("name", "")[:34],
                r.get("base_score"), r.get("synth_score"),
                _delta_str(r.get("delta")), f"{eng_adj:+.1f}",
                r.get("sc_primary"), reason[:55]
            ])
        lines.append(_md_table(
            ["Corpus", "Product", "Base", "Synth", "Δ", "Adj", "SC", "Reason"],
            eng_rows
        ))
    else:
        lines.append("_No engineering nuance activations found._")

    lines += [
        "",
        "## Products Remaining Unchanged (synthesis pass-through)",
        "",
        "These products are candidates for v2 synthesis extensions:",
        "- Isolated fiber inflation (chicory/inulin in granola/cereal bars) → needs fiber_source detection",
        "- Fortification compensation (NOVA4 cereals with vitamins) → needs matrix_integrity signals",
        "- Protein realism (protein cereals with moderate isolate) → protein_quality already in score_engine",
        "",
        "## Recommended v2 Extensions for Non-Bakery",
        "",
        "1. **Fiber source classification** (from signal_extractor L3): isolated fiber markers already",
        "   detected in L3.extracted_matrix_markers — can be wired to synthesis without bakery_semantics.",
        "2. **Matrix integrity integration**: run matrix_integrity.py in the batch pipeline and pass",
        "   engineering_intensity + transformation_type to synthesis.",
        "3. **NOVA4 + fortification discount**: wellness_engineering fortification (currently untested)",
        "   maps to synthesis penalty once protein shake / sports bar categories are added.",
    ]

    path = REPORT_ROOT / "real_corpora_synthesis_001_combined.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Combined report written: %s", path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    all_records = []

    for corpus in CORPORA:
        records = run_corpus(corpus)
        all_records.extend(records)

    log.info("")
    log.info("=== Writing combined report (%d total products) ===", len(all_records))
    write_combined_report(all_records)
    log.info("Done.")


if __name__ == "__main__":
    main()
