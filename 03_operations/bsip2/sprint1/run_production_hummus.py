"""
BSIP2 Sprint 1 — Production Validation: Hummus
Uses the merged production engine (proto_v0/src) with all approved sprint1 signals.
Writes results to sprint1/outputs/production_hummus.json and a summary .md.

Note: fat_quality dimension may be unreliable for ~58/69 products due to the
Shufersal fat-row scraping defect (TASK-039). Scores are valid for all other dims.
"""
import sys, json, pathlib, datetime

SPRINT1_DIR  = pathlib.Path(__file__).resolve().parent
BSIP2_SRC    = SPRINT1_DIR.parent / "proto_v0" / "src"
BSIP1_SOURCE = pathlib.Path(r"C:\Bari\02_products\hummus\canonical_bsip1")
OUTPUT_DIR   = SPRINT1_DIR / "outputs"

sys.path.insert(0, str(BSIP2_SRC))

from input_loader     import load_batch
from signal_extractor import extract_signals
from router_v2        import classify_category
from nova_proxy       import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine     import score_product
from constants        import score_to_grade

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KNOWN_LIMITATION = (
    "fat_quality dimension may be unreliable for ~58/69 products "
    "due to Shufersal fat-row scraping defect (TASK-039)."
)


def _run(product):
    signals    = extract_signals(product)
    cat_result = classify_category(product)
    l3         = signals["L3_inferred_classifications"]
    nova       = infer_nova(product, l3)
    evscope    = assign_evaluation_scope(product, cat_result["category"])
    return score_product(product, signals, cat_result, nova, evscope), signals


def main():
    print("=== BSIP2 Production Validation — Hummus ===")
    print(f"Known limitation: {KNOWN_LIMITATION}")
    if not BSIP1_SOURCE.exists():
        print(f"ERROR: corpus not found: {BSIP1_SOURCE}")
        return
    products = load_batch(BSIP1_SOURCE)
    print(f"Products: {len(products)}")

    rows = []
    for p in products:
        pid  = p.get("canonical_product_id", "?")
        name = p.get("canonical_name_he") or p.get("product_name_he") or pid
        try:
            r, signals = _run(p)
            l3 = signals["L3_inferred_classifications"]
            score = r.get("final_score_estimate")
            grade = r.get("grade_estimate")
            row = {
                "pid": pid, "name": name,
                "score": score, "grade": grade,
                "category": r.get("category"),
                "nova": r.get("nova_proxy"),
                "binding_cap": r.get("binding_cap"),
                "sufficient":  r.get("data_sufficiency") != "insufficient",
                "polyol_count":         l3.get("sprint1_polyol_count", 0),
                "penalty_polyol_count": l3.get("sprint1_penalty_polyol_count", 0),
                "humectant_polyols":    l3.get("sprint1_humectant_polyols", []),
                "detected_polyols":     l3.get("sprint1_detected_polyols", []),
                "polyol_penalty":       r.get("polyol_penalty", 0),
                "sprint1_additive_count": l3.get("sprint1_additive_count"),
                "additive_correction":    l3.get("sprint1_additive_correction", 0),
                "high_risk_emulsifier":   l3.get("sprint1_high_risk_emulsifier_detected", False),
                "neutral_emulsifier":     l3.get("sprint1_neutral_emulsifier_detected", False),
                "allulose_detected":      l3.get("sprint1_allulose_detected", False),
            }
        except Exception as e:
            row = {"pid": pid, "name": name, "error": str(e)}
            import traceback; traceback.print_exc()
        rows.append(row)
        print(f"  {str(name)[:45]:45s}  score={row.get('score')} grade={row.get('grade')} cat={row.get('category')}")

    # Save JSON
    out_json = OUTPUT_DIR / "production_hummus.json"
    out_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # Summary stats
    scored = [r for r in rows if r.get("sufficient") and r.get("score") is not None]
    scores = [r["score"] for r in scored]
    polyol_products  = [r for r in rows if r.get("polyol_count", 0) > 0]
    humectant_exempt = [r for r in rows if r.get("humectant_polyols")]
    penalty_applied  = [r for r in rows if r.get("polyol_penalty", 0) > 0]
    high_risk        = [r for r in rows if r.get("high_risk_emulsifier")]
    lecithin_exempt  = [r for r in rows if r.get("neutral_emulsifier") and r.get("additive_correction",0) < 0]

    grade_dist: dict = {}
    for r in scored:
        g = r.get("grade","?")
        grade_dist[g] = grade_dist.get(g,0)+1

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# BSIP2 Sprint 1 — Production Validation: Hummus",
        f"\n**Generated:** {ts}",
        f"**Engine:** proto_v0/src (Sprint 1 merged — EV-003/004/005/012/019)**",
        f"**Corpus:** {BSIP1_SOURCE} — 69 products",
        f"**Total products:** {len(rows)}",
        f"**Scored:** {len(scored)}",
        f"**Insufficient data:** {len(rows) - len(scored)}",
        "",
        f"> **Known limitation:** {KNOWN_LIMITATION}",
        "",
        "---",
        "",
        "## Score Statistics",
        "",
    ]
    if scores:
        lines += [
            f"| Statistic | Value |",
            f"|-----------|-------|",
            f"| Mean  | {round(sum(scores)/len(scores),1)} |",
            f"| Min   | {min(scores)} |",
            f"| Max   | {max(scores)} |",
            f"| Count | {len(scores)} |",
        ]

    lines += [
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
    ]
    if polyol_products:
        lines += ["", "### Polyol Detections", ""]
        for r in polyol_products:
            lines.append(f"- {r['name'][:60]}: {r.get('detected_polyols')} "
                         f"(penalty_count={r.get('penalty_polyol_count')} "
                         f"humectant={r.get('humectant_polyols')})")
    else:
        lines += ["", "*No polyols detected in hummus corpus.*"]

    lines += [
        "",
        "## EV-003/019 Emulsifier Summary",
        "",
        f"| Signal | Count |",
        f"|--------|-------|",
        f"| High-risk emulsifier | {len(high_risk)} |",
        f"| Lecithin-only exempt | {len(lecithin_exempt)} |",
        "",
        "## Full Score Table",
        "",
        "| Product | Score | Grade | Category | Cap |",
        "|---------|-------|-------|----------|-----|",
    ]
    for r in sorted(scored, key=lambda x: -(x.get("score") or 0)):
        lines.append(f"| {str(r['name'])[:45]} | {r['score']} | {r['grade']} "
                     f"| {r.get('category','-')} | {r.get('binding_cap','-')} |")

    lines += ["", f"*Full data: {out_json}*"]

    out_md = OUTPUT_DIR / "production_hummus_summary.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResults: {out_json}")
    print(f"Summary: {out_md}")
    print(f"Scored: {len(scored)} | Polyol detected: {len(polyol_products)} | Penalty applied: {len(penalty_applied)}")


if __name__ == "__main__":
    main()
