"""
BSIP2 Sprint 1 — Before/After Comparison Runner

Scores the full snack bar corpus with both v1 and v2 engines and writes
a structured comparison to sprint1/outputs/.

Usage: python run_sprint1_snack_bars.py
"""

import sys
import json
import pathlib
import datetime
import traceback

# ── Path setup ──────────────────────────────────────────────────────────────
SPRINT1_DIR  = pathlib.Path(__file__).resolve().parent
BSIP2_SRC    = SPRINT1_DIR.parent / "proto_v0" / "src"
BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
OUTPUT_DIR   = SPRINT1_DIR / "outputs"

sys.path.insert(0, str(BSIP2_SRC))
sys.path.insert(0, str(SPRINT1_DIR))

# ── v1 imports ───────────────────────────────────────────────────────────────
from input_loader    import load_batch
from signal_extractor import extract_signals as extract_signals_v1
from router_v2       import classify_category
from nova_proxy      import infer_nova
from evaluation_scope import assign_evaluation_scope
from score_engine    import score_product as score_product_v1
from constants       import score_to_grade

# ── v2 imports ───────────────────────────────────────────────────────────────
from signal_extractor_v2 import extract_signals as extract_signals_v2
from score_engine_v2     import score_product as score_product_v2

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def run_pipeline(product: dict, extractor_fn, scorer_fn) -> dict:
    signals     = extractor_fn(product)
    cat_result  = classify_category(product)
    l3          = signals["L3_inferred_classifications"]
    nova_result = infer_nova(product, l3)
    eval_result = assign_evaluation_scope(product, cat_result["category"])
    return scorer_fn(product, signals, cat_result, nova_result, eval_result)


def score_one(product: dict) -> dict:
    pid = product.get("canonical_product_id", "unknown")
    name = product.get("canonical_name_he") or product.get("product_name_he") or pid

    result = {"pid": pid, "name": name}

    # v1
    try:
        r1 = run_pipeline(product, extract_signals_v1, score_product_v1)
        result["v1_score"]  = r1.get("final_score_estimate")
        result["v1_grade"]  = r1.get("grade_estimate")
        result["v1_sufficient"] = r1.get("data_sufficiency") != "insufficient"
        result["v1_dims"]   = r1.get("dimension_scores", {})
        result["v1_cap"]    = r1.get("binding_cap")
        result["v1_penalty"]= r1.get("scaled_penalty", 0)
        result["v1_nova"]   = r1.get("nova_proxy")
        result["v1_cat"]    = r1.get("category")
    except Exception as e:
        result["v1_error"] = str(e)
        result["v1_score"] = None
        result["v1_grade"] = None
        result["v1_sufficient"] = False

    # v2
    try:
        r2 = run_pipeline(product, extract_signals_v2, score_product_v2)
        result["v2_score"]   = r2.get("final_score_estimate")
        result["v2_grade"]   = r2.get("grade_estimate")
        result["v2_sufficient"] = r2.get("data_sufficiency") != "insufficient"
        result["v2_dims"]    = r2.get("dimension_scores", {})
        result["v2_cap"]     = r2.get("binding_cap")
        result["v2_penalty"] = r2.get("scaled_penalty", 0) + r2.get("polyol_penalty", 0)
        result["sprint1"]    = r2.get("sprint1_signals", {})
        result["v2_polyol_penalty"] = r2.get("polyol_penalty", 0)
    except Exception as e:
        result["v2_error"] = str(e)
        result["v2_score"] = None
        result["v2_grade"] = None
        result["v2_sufficient"] = False
        import traceback as tb; tb.print_exc()

    # Delta
    if result.get("v1_score") is not None and result.get("v2_score") is not None:
        result["delta"] = round(result["v2_score"] - result["v1_score"], 1)
    else:
        result["delta"] = None

    return result


def grade_order(g: str) -> int:
    return {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
            "insufficient_data": 6, None: 7}.get(g, 7)


def main():
    print("=== BSIP2 Sprint 1 — Snack Bar Before/After ===")
    print(f"Source: {BSIP1_SOURCE}")

    if not BSIP1_SOURCE.exists():
        print(f"ERROR: BSIP1 source not found: {BSIP1_SOURCE}")
        return

    products = load_batch(BSIP1_SOURCE)
    print(f"Products loaded: {len(products)}")

    results = []
    for i, product in enumerate(products):
        r = score_one(product)
        results.append(r)
        delta_str = f"{r['delta']:+.1f}" if r["delta"] is not None else "N/A"
        v1s = r.get("v1_score", "?")
        v2s = r.get("v2_score", "?")
        print(f"  [{i+1:3d}] {str(r['name'])[:40]:40s}  v1={v1s}  v2={v2s}  Δ={delta_str}")

    # Save full results
    out_json = OUTPUT_DIR / "sprint1_comparison_snack_bars.json"
    out_json.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\nFull results: {out_json}")

    # Build summary statistics
    scored = [r for r in results if r.get("v1_score") is not None and r.get("v2_score") is not None
              and r.get("v1_sufficient") and r.get("v2_sufficient")]

    print(f"\n{'='*60}")
    print(f"Scoreable products: {len(scored)} / {len(results)}")

    if scored:
        deltas = [r["delta"] for r in scored if r["delta"] is not None]
        avg_delta = round(sum(deltas) / len(deltas), 2)
        max_up   = max(deltas)
        max_down = min(deltas)
        changed  = sum(1 for d in deltas if abs(d) >= 1.0)
        print(f"Average delta: {avg_delta:+.2f}")
        print(f"Largest gain:  {max_up:+.1f}")
        print(f"Largest drop:  {max_down:+.1f}")
        print(f"Products with |Δ| >= 1: {changed}")

        # Grade migrations
        migrations = [(r["name"], r["v1_grade"], r["v2_grade"])
                      for r in scored if r.get("v1_grade") != r.get("v2_grade")]
        print(f"Grade migrations: {len(migrations)}")
        for name, g1, g2 in migrations:
            print(f"  {str(name)[:45]:45s}  {g1} → {g2}")

        # Sprint1 signal fire counts
        sig_counts = {
            "high_risk_emulsifier": 0,
            "neutral_emulsifier":   0,
            "prebiotic_gum":        0,
            "allulose":             0,
            "polyol_2plus":         0,
        }
        for r in results:
            s = r.get("sprint1", {})
            if s.get("high_risk_emulsifier"): sig_counts["high_risk_emulsifier"] += 1
            if s.get("neutral_emulsifier"):   sig_counts["neutral_emulsifier"]   += 1
            if s.get("prebiotic_gum"):        sig_counts["prebiotic_gum"]        += 1
            if s.get("allulose_detected"):    sig_counts["allulose"]             += 1
            if (s.get("polyol_count") or 0) >= 2: sig_counts["polyol_2plus"]    += 1
        print(f"\nSignal fire counts across {len(results)} products:")
        for k, v in sig_counts.items():
            print(f"  {k}: {v}")

    # Write summary report
    _write_md_summary(results, scored, out_json)
    print(f"\nDone.")


def _write_md_summary(results, scored, json_path):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Grade distribution
    def grade_dist(key):
        dist = {}
        for r in results:
            if r.get(f"{key}_sufficient"):
                g = r.get(f"{key}_grade", "?")
                dist[g] = dist.get(g, 0) + 1
        return dist

    v1_dist = grade_dist("v1")
    v2_dist = grade_dist("v2")

    def gd_row(g):
        return f"| {g} | {v1_dist.get(g,0)} | {v2_dist.get(g,0)} |"

    top_gains = sorted(scored, key=lambda r: -(r["delta"] or 0))[:20]
    top_drops = sorted(scored, key=lambda r: (r["delta"] or 0))[:20]

    def signal_fires(r):
        s = r.get("sprint1", {})
        fired = []
        if s.get("high_risk_emulsifier"):  fired.append("HIGH_RISK_EMULS")
        if s.get("neutral_emulsifier") and (s.get("additive_correction",0) < 0):
            fired.append("LECITHIN_EXEMPT")
        if s.get("prebiotic_gum") and (s.get("additive_correction",0) < 0):
            fired.append("GUM_EXEMPT")
        if s.get("allulose_detected"):     fired.append("ALLULOSE")
        pc = s.get("polyol_count",0)
        if pc >= 2: fired.append(f"POLYOL×{pc}")
        elif pc == 1: fired.append("POLYOL×1")
        if not fired:
            fat = (r.get("v2_dims") or {}).get("fat_quality")
            fat1 = (r.get("v1_dims") or {}).get("fat_quality")
            if fat is not None and fat1 is not None and abs(fat - fat1) >= 1:
                fired.append(f"FAT_RATIO(Δfq={fat-fat1:+.0f})")
        return ", ".join(fired) if fired else "fat_quality_v2"

    lines = [
        f"# Sprint 1 — Snack Bar Before/After Summary",
        f"",
        f"**Generated:** {ts}",
        f"**Corpus:** Snack bars — `{BSIP1_SOURCE}`",
        f"**Total products:** {len(results)}",
        f"**Scoreable (both v1 and v2):** {len(scored)}",
        f"",
        f"---",
        f"",
        f"## Grade Distribution",
        f"",
        f"| Grade | v1 | v2 |",
        f"|-------|----|----|",
    ]
    for g in ["S", "A", "B", "C", "D", "E"]:
        lines.append(gd_row(g))

    if scored:
        deltas = [r["delta"] for r in scored if r["delta"] is not None]
        avg_delta = round(sum(deltas) / len(deltas), 2)
        migrations = [(r["name"], r["v1_grade"], r["v2_grade"], r["delta"])
                      for r in scored if r.get("v1_grade") != r.get("v2_grade")]
        lines += [
            f"",
            f"## Score Movement",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Average delta (v2 - v1) | {avg_delta:+.2f} |",
            f"| Products with \\|Δ\\| ≥ 1 | {sum(1 for d in deltas if abs(d)>=1)} |",
            f"| Products with \\|Δ\\| ≥ 3 | {sum(1 for d in deltas if abs(d)>=3)} |",
            f"| Products with \\|Δ\\| ≥ 5 | {sum(1 for d in deltas if abs(d)>=5)} |",
            f"| Grade migrations | {len(migrations)} |",
            f"",
            f"## Grade Migrations",
            f"",
        ]
        if migrations:
            lines.append(f"| Product | v1 grade | v2 grade | Δ |")
            lines.append(f"|---------|----------|----------|---|")
            for name, g1, g2, d in sorted(migrations, key=lambda x: -abs(x[3] or 0)):
                lines.append(f"| {str(name)[:50]} | {g1} | {g2} | {d:+.1f} |")
        else:
            lines.append("*No grade migrations.*")

        lines += [
            f"",
            f"## Top 20 Positive Movements",
            f"",
            f"| Product | v1 | v2 | Δ | Signals |",
            f"|---------|----|----|---|---------|",
        ]
        for r in top_gains:
            if (r.get("delta") or 0) <= 0: break
            lines.append(f"| {str(r['name'])[:48]} | {r['v1_score']} | {r['v2_score']} "
                        f"| {r['delta']:+.1f} | {signal_fires(r)} |")

        lines += [
            f"",
            f"## Top 20 Negative Movements",
            f"",
            f"| Product | v1 | v2 | Δ | Signals |",
            f"|---------|----|----|---|---------|",
        ]
        for r in top_drops:
            if (r.get("delta") or 0) >= 0: break
            lines.append(f"| {str(r['name'])[:48]} | {r['v1_score']} | {r['v2_score']} "
                        f"| {r['delta']:+.1f} | {signal_fires(r)} |")

    lines += [
        f"",
        f"---",
        f"",
        f"*Full data: {json_path}*",
    ]

    out_md = OUTPUT_DIR / "sprint1_summary_snack_bars.md"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary report: {out_md}")


if __name__ == "__main__":
    main()
