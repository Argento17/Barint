"""
BSIP2 Sprint 1 — Production Validation: Snack Bars
Uses the merged production engine (proto_v0/src) with all approved sprint1 signals.
Writes results to sprint1/outputs/production_snack_bars.json and a summary .md.
"""
import sys, json, pathlib, datetime

SPRINT1_DIR  = pathlib.Path(__file__).resolve().parent
BSIP2_SRC    = SPRINT1_DIR.parent / "proto_v0" / "src"
BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
OUTPUT_DIR   = SPRINT1_DIR / "outputs"

sys.path.insert(0, str(BSIP2_SRC))

from input_loader     import load_batch
from signal_extractor import extract_signals      # production — sprint1 signals merged
from router_v2        import classify_category
from nova_proxy       import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine     import score_product        # production — sprint1 scoring merged
from constants        import score_to_grade

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _run(product):
    signals    = extract_signals(product)
    cat_result = classify_category(product)
    l3         = signals["L3_inferred_classifications"]
    nova       = infer_nova(product, l3)
    evscope    = assign_evaluation_scope(product, cat_result["category"])
    return score_product(product, signals, cat_result, nova, evscope)


def main():
    print("=== BSIP2 Production Validation — Snack Bars ===")
    products = load_batch(BSIP1_SOURCE)
    print(f"Products: {len(products)}")

    rows = []
    for p in products:
        pid  = p.get("canonical_product_id", "?")
        name = p.get("canonical_name_he") or pid
        try:
            r = _run(p)
            score = r.get("final_score_estimate")
            grade = r.get("grade_estimate")
            polyol_pen = r.get("polyol_penalty", 0)
            l3    = extract_signals(p)["L3_inferred_classifications"]
            row = {
                "pid": pid, "name": name,
                "score": score, "grade": grade,
                "polyol_count":       l3.get("sprint1_polyol_count", 0),
                "penalty_polyol_count": l3.get("sprint1_penalty_polyol_count", 0),
                "humectant_polyols":  l3.get("sprint1_humectant_polyols", []),
                "detected_polyols":   l3.get("sprint1_detected_polyols", []),
                "polyol_penalty":     polyol_pen,
                "sprint1_additive_count": l3.get("sprint1_additive_count"),
                "additive_correction":    l3.get("sprint1_additive_correction", 0),
                "high_risk_emulsifier":   l3.get("sprint1_high_risk_emulsifier_detected", False),
                "neutral_emulsifier":     l3.get("sprint1_neutral_emulsifier_detected", False),
                "allulose_detected":      l3.get("sprint1_allulose_detected", False),
                "binding_cap": r.get("binding_cap"),
                "sufficient":  r.get("data_sufficiency") != "insufficient",
            }
        except Exception as e:
            row = {"pid": pid, "name": name, "error": str(e)}
        rows.append(row)
        status = f"score={row.get('score')} grade={row.get('grade')}"
        if row.get("polyol_penalty", 0) > 0:
            status += f" polyol_pen=-{row['polyol_penalty']}"
        if row.get("humectant_polyols"):
            status += f" [humectant-exempt: {row['humectant_polyols']}]"
        print(f"  {str(name)[:45]:45s}  {status}")

    # Save JSON
    out_json = OUTPUT_DIR / "production_snack_bars.json"
    out_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Build summary
    scored = [r for r in rows if r.get("sufficient") and r.get("score") is not None]
    polyol_products  = [r for r in rows if r.get("polyol_count", 0) > 0]
    humectant_exempt = [r for r in rows if r.get("humectant_polyols")]
    penalty_applied  = [r for r in rows if r.get("polyol_penalty", 0) > 0]
    high_risk        = [r for r in rows if r.get("high_risk_emulsifier")]
    lecithin_exempt  = [r for r in rows if r.get("neutral_emulsifier") and r.get("additive_correction", 0) < 0]

    grade_dist: dict = {}
    for r in scored:
        g = r.get("grade","?")
        grade_dist[g] = grade_dist.get(g,0)+1

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# BSIP2 Sprint 1 — Production Validation: Snack Bars",
        f"\n**Generated:** {ts}",
        f"**Engine:** proto_v0/src (Sprint 1 merged — EV-003/004/005/012/019)**",
        f"**Corpus:** {BSIP1_SOURCE}",
        f"**Total products:** {len(rows)}",
        f"**Scored:** {len(scored)}",
        "",
        "---",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Count |",
        "|-------|-------|",
    ]
    for g in ["S","A","B","C","D","E","insufficient_data"]:
        n = grade_dist.get(g,0)
        if n: lines.append(f"| {g} | {n} |")

    lines += [
        "",
        "## EV-005 Polyol Signal Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Products with any polyol detected | {len(polyol_products)} |",
        f"| Products with humectant-exempt polyol | {len(humectant_exempt)} |",
        f"| Products receiving polyol penalty | {len(penalty_applied)} |",
        "",
    ]
    if humectant_exempt:
        lines += ["### Humectant-Exempt Products (no polyol penalty)", ""]
        lines.append("| Product | Polyol | Position |")
        lines.append("|---------|--------|----------|")
        for r in humectant_exempt:
            lines.append(f"| {str(r['name'])[:50]} | {r.get('humectant_polyols')} | humectant group |")

    if penalty_applied:
        lines += ["", "### Products Receiving Polyol Penalty", ""]
        lines.append("| Product | Polyol | Penalty |")
        lines.append("|---------|--------|---------|")
        for r in penalty_applied:
            lines.append(f"| {str(r['name'])[:50]} | {r.get('detected_polyols')} | -{r['polyol_penalty']} |")

    lines += [
        "",
        "## EV-003/019 Emulsifier Signal Summary",
        "",
        f"| Signal | Count |",
        f"|--------|-------|",
        f"| High-risk emulsifier detected | {len(high_risk)} |",
        f"| Lecithin-only exempt (additive count corrected) | {len(lecithin_exempt)} |",
        "",
        f"*Full data: {out_json}*",
    ]

    out_md = OUTPUT_DIR / "production_snack_bars_summary.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResults: {out_json}")
    print(f"Summary: {out_md}")
    print(f"Scored: {len(scored)} | Polyol penalty applied: {len(penalty_applied)} | Humectant-exempt: {len(humectant_exempt)}")


if __name__ == "__main__":
    main()
