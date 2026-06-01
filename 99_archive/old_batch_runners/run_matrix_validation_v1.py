"""
BSIP2 Matrix Integrity Engine — Validation Runner v1

Runs matrix_integrity across all four BSIP1 datasets:
  - snack_bars  (run_001)
  - cereals     (run_cereals_001)
  - yogurt      (run_yogurt_001)
  - milk        (run_milk_002)

Generates a validation report in:
  C:\Bari\03_operations\bsip2\reports\matrix_integrity_validation_001.md
"""

import json
import pathlib
import sys
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from matrix_integrity import compute_matrix_integrity, MODULE_VERSION

BSIP1_SOURCES = {
    "snack_bars": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output"),
    "cereals":    pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output"),
    "yogurt":     pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output"),
    "milk":       pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output"),
}

REPORT_PATH = pathlib.Path(
    r"C:\Bari\03_operations\bsip2\reports\matrix_integrity_validation_001.md"
)


def load_products(source_dir: pathlib.Path) -> list[dict]:
    products = []
    for f in sorted(source_dir.glob("bsip1_*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                rec = json.load(fh)
            if rec.get("file_type") == "product":
                products.append(rec)
        except Exception as e:
            print(f"  WARN: could not load {f.name}: {e}")
    return products


def _label(product: dict) -> str:
    return (
        product.get("canonical_name_he")
        or product.get("product_name_he")
        or product.get("canonical_product_id")
        or "unknown"
    )


def _md_table(headers: list, rows: list) -> str:
    widths = [
        max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
        for i, h in enumerate(headers)
    ]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    lines = [row_line(headers), sep] + [row_line(r) for r in rows]
    return "\n".join(lines)


def run_validation():
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    all_results: list[dict] = []
    by_category: dict[str, list[dict]] = {}

    print(f"=== Matrix Integrity Validation — {MODULE_VERSION} ===")

    for cat_tag, source_dir in BSIP1_SOURCES.items():
        if not source_dir.exists():
            print(f"  SKIP {cat_tag}: source not found at {source_dir}")
            continue

        products = load_products(source_dir)
        print(f"  {cat_tag}: {len(products)} products loaded")

        cat_results = []
        for p in products:
            pid = p.get("canonical_product_id", "unknown")
            try:
                mi = compute_matrix_integrity(p)
                row = {
                    "pid":          pid,
                    "name":         _label(p),
                    "category_tag": cat_tag,
                    "score":        mi["matrix_integrity_score"],
                    "depth":        mi["reconstruction_depth"],
                    "level":        mi["structural_degradation_level"],
                    "eng":          mi["engineering_intensity"],
                    "hp":           mi["matrix_integrity_trace"]["hp_reconstruction_score"],
                    "ferm_factor":  mi["matrix_integrity_trace"]["fermentation_factor"],
                    "comp_signals": mi["compensation_signals"],
                    "dom_signals":  mi["dominant_matrix_signals"],
                    "summary":      mi["integrity_summary"],
                }
                cat_results.append(row)
                all_results.append(row)
            except Exception as e:
                print(f"    ERROR on {pid}: {e}")
                import traceback; traceback.print_exc()

        by_category[cat_tag] = cat_results
        scores = [r["score"] for r in cat_results]
        if scores:
            avg = sum(scores) / len(scores)
            print(f"    scores: min={min(scores):.1f}  avg={avg:.1f}  max={max(scores):.1f}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_report(run_dt, all_results, by_category)
    print(f"\nReport written: {REPORT_PATH}")


def _write_report(run_dt: str, all_results: list, by_category: dict):
    lines = [
        f"# Matrix Integrity Engine v1 — Validation Report 001",
        f"",
        f"**Engine version:** {MODULE_VERSION}",
        f"**Run date:** {run_dt}",
        f"**Products evaluated:** {len(all_results)}",
        f"",
        "---",
        "",
    ]

    # ── Per-category summary table ────────────────────────────────────────────
    lines += ["## Category Summary", ""]
    cat_rows = []
    for cat, results in by_category.items():
        if not results:
            continue
        scores = [r["score"] for r in results]
        depths = [r["depth"] for r in results]
        engs   = [r["eng"] for r in results]
        cat_rows.append([
            cat,
            len(results),
            f"{min(scores):.1f}",
            f"{sum(scores)/len(scores):.1f}",
            f"{max(scores):.1f}",
            f"{sum(depths)/len(depths):.2f}",
            f"{sum(engs)/len(engs):.1f}",
        ])
    lines.append(_md_table(
        ["Category", "N", "Min Score", "Avg Score", "Max Score", "Avg Depth", "Avg Eng"],
        cat_rows,
    ))
    lines.append("")

    # ── Score distribution ────────────────────────────────────────────────────
    lines += ["## Score Distribution (All Categories)", ""]
    buckets = {
        "90-100 (minimal)":  0,
        "75-89  (low)":      0,
        "58-74  (moderate)": 0,
        "40-57  (high)":     0,
        "22-39  (severe)":   0,
        "0-21   (extreme)":  0,
    }
    for r in all_results:
        s = r["score"]
        if s >= 90:   buckets["90-100 (minimal)"] += 1
        elif s >= 75: buckets["75-89  (low)"] += 1
        elif s >= 58: buckets["58-74  (moderate)"] += 1
        elif s >= 40: buckets["40-57  (high)"] += 1
        elif s >= 22: buckets["22-39  (severe)"] += 1
        else:         buckets["0-21   (extreme)"] += 1

    lines.append(_md_table(
        ["Score Range", "Count"],
        [[k, v] for k, v in buckets.items()],
    ))
    lines.append("")

    # ── Strongest integrity (top 12) ──────────────────────────────────────────
    top = sorted(all_results, key=lambda x: -x["score"])[:12]
    lines += ["## Strongest Matrix Integrity (top 12)", ""]
    top_rows = [
        [
            r["name"][:52],
            r["category_tag"],
            f"{r['score']:.1f}",
            r["depth"],
            r["level"],
            r["dom_signals"][0][:45] if r["dom_signals"] else "none",
        ]
        for r in top
    ]
    lines.append(_md_table(
        ["Product", "Category", "Score", "Depth", "Level", "Primary Signal"],
        top_rows,
    ))
    lines.append("")

    # ── Weakest integrity (bottom 12) ────────────────────────────────────────
    bottom = sorted(all_results, key=lambda x: x["score"])[:12]
    lines += ["## Weakest Matrix Integrity (bottom 12)", ""]
    bot_rows = [
        [
            r["name"][:52],
            r["category_tag"],
            f"{r['score']:.1f}",
            r["depth"],
            r["level"],
            r["dom_signals"][0][:45] if r["dom_signals"] else "none",
        ]
        for r in bottom
    ]
    lines.append(_md_table(
        ["Product", "Category", "Score", "Depth", "Level", "Primary Signal"],
        bot_rows,
    ))
    lines.append("")

    # ── Per-category deep dives ───────────────────────────────────────────────
    for cat, results in by_category.items():
        if not results:
            continue
        sorted_results = sorted(results, key=lambda x: -x["score"])
        lines += [f"## {cat.replace('_', ' ').title()} — All Products", ""]
        rows = [
            [
                r["name"][:48],
                f"{r['score']:.1f}",
                r["depth"],
                r["level"],
                f"{r['eng']:.1f}",
                f"{r['hp']:.0f}",
                f"{r['ferm_factor']:.2f}",
                ", ".join(r["comp_signals"])[:35] if r["comp_signals"] else "—",
            ]
            for r in sorted_results
        ]
        lines.append(_md_table(
            ["Product", "Score", "D", "Level", "Eng", "HP", "Ferm", "Compensation"],
            rows,
        ))
        lines.append("")

    # ── Interesting edge cases ────────────────────────────────────────────────
    lines += ["## Edge Cases and Analytical Notes", ""]

    # Products with high fermentation factor
    high_ferm = [r for r in all_results if r["ferm_factor"] >= 0.30]
    if high_ferm:
        lines += ["### High Fermentation Credit (factor ≥ 0.30)", ""]
        for r in sorted(high_ferm, key=lambda x: -x["ferm_factor"])[:8]:
            lines.append(
                f"- **{r['name'][:55]}** ({r['category_tag']}) — "
                f"score={r['score']:.0f}, ferm_factor={r['ferm_factor']:.2f}"
            )
        lines.append("")

    # Products with compensation signals
    with_comp = [r for r in all_results if r["comp_signals"]]
    if with_comp:
        lines += ["### Products with Engineered Compensation Signals", ""]
        for r in sorted(with_comp, key=lambda x: -len(x["comp_signals"]))[:10]:
            lines.append(
                f"- **{r['name'][:55]}** ({r['category_tag']}) — "
                f"score={r['score']:.0f}, signals: {', '.join(r['comp_signals'])}"
            )
        lines.append("")

    # HP pattern detected
    hp_products = [r for r in all_results if r["hp"] >= 50]
    if hp_products:
        lines += ["### HP Reconstruction Pattern Detected (score ≥ 50)", ""]
        for r in sorted(hp_products, key=lambda x: -x["hp"])[:10]:
            lines.append(
                f"- **{r['name'][:55]}** ({r['category_tag']}) — "
                f"integrity={r['score']:.0f}, hp={r['hp']:.0f}, depth={r['depth']}"
            )
        lines.append("")

    # Divergence: high integrity despite many ingredients
    likely_halo = [
        r for r in all_results
        if r["score"] >= 75 and r["eng"] >= 20
    ]
    if likely_halo:
        lines += ["### Healthy-Halo Risk: High Score but Non-Zero Engineering", ""]
        lines.append(
            "_Products where matrix_integrity_score is high but engineering signals are present — "
            "potential for misleading 'clean' appearance._"
        )
        lines.append("")
        for r in sorted(likely_halo, key=lambda x: -x["eng"])[:8]:
            lines.append(
                f"- **{r['name'][:55]}** ({r['category_tag']}) — "
                f"score={r['score']:.0f}, eng={r['eng']:.1f}"
            )
        lines.append("")

    # Traditionally processed foods that avoided unfair penalties
    traditional_ok = [
        r for r in all_results
        if r["score"] >= 80 and r["ferm_factor"] >= 0.20 and r["eng"] < 15
    ]
    if traditional_ok:
        lines += ["### Traditional Foods Correctly Avoided Unfair Penalties", ""]
        for r in sorted(traditional_ok, key=lambda x: -x["score"])[:8]:
            lines.append(
                f"- **{r['name'][:55]}** ({r['category_tag']}) — "
                f"score={r['score']:.0f}, fermentation properly credited"
            )
        lines.append("")

    # ── Limitations ──────────────────────────────────────────────────────────
    lines += [
        "## Known Limitations",
        "",
        "1. **Hidden industrial processes**: Extrusion, expansion, and cooking are not declared "
        "in ingredient lists. Corn flakes made from extruded corn flour look the same as "
        "a product where corn flour is simply ground.",
        "",
        "2. **No ingredient quantities** (except % when declared): We cannot distinguish "
        "a product that is 80% oat flour from one that is 5% oat flour — only position proxy.",
        "",
        "3. **Vocabulary gaps**: The enricher's Hebrew dictionaries do not cover all "
        "ingredients. Ingredients that don't match any term are treated as neutral "
        "(no degradation signal), which may inflate integrity scores for complex products.",
        "",
        "4. **Fortification detection is approximate**: The vitamin/mineral fortification "
        "detection relies on Hebrew term matching. Some fortification may be missed when "
        "described differently (e.g., 'enriched with X').",
        "",
        "5. **Fermentation credit is categorical, not quantitative**: All live-culture "
        "yogurts receive the same fermentation credit regardless of whether they are "
        "simple natural yogurt or a heavily engineered dairy dessert with added cultures.",
        "",
        "6. **Product name as proxy not used**: 'בטעם' (flavored) detection from ingredients "
        "is not directly connected to the HP reconstruction score here — it is captured via "
        "the flavor marker system.",
        "",
        "7. **No cross-product comparison**: Score is absolute, not percentile-ranked. "
        "A score of 70 means 'moderate degradation' not '70th percentile of products'.",
        "",
    ]

    # ── Graduated severity examples ──────────────────────────────────────────
    lines += ["## Graduated Severity Behavior Examples", ""]
    lines.append("Demonstrating the engine's ability to distinguish structural stages:")
    lines.append("")

    oat_products = sorted(
        [r for r in all_results if "שיבולת שועל" in r["name"] or "oat" in r["name"].lower()],
        key=lambda x: -x["score"]
    )
    if oat_products:
        lines.append("**Oat family gradient (where present):**")
        for r in oat_products[:5]:
            lines.append(
                f"- {r['name'][:50]} — score={r['score']:.0f}, depth={r['depth']}, "
                f"signals: {r['dom_signals'][0][:40] if r['dom_signals'] else 'none'}"
            )
        lines.append("")

    depth_examples: dict[int, list] = {}
    for r in all_results:
        depth_examples.setdefault(r["depth"], []).append(r)

    lines.append("**One example per reconstruction depth:**")
    for d in range(6):
        candidates = depth_examples.get(d, [])
        if candidates:
            ex = sorted(candidates, key=lambda x: abs(x["score"] - 50))[0]  # most representative
            if d <= 1:
                ex = sorted(candidates, key=lambda x: -x["score"])[0]
            elif d >= 4:
                ex = sorted(candidates, key=lambda x: x["score"])[0]
            lines.append(
                f"- Depth {d} ({_DEGRADATION_LEVEL_LABELS_SHORT[d]}): "
                f"**{ex['name'][:48]}** — score={ex['score']:.0f}, "
                f"eng={ex['eng']:.0f}, hp={ex['hp']:.0f}"
            )
    lines.append("")

    lines += [
        "---",
        "",
        f"*Generated by {MODULE_VERSION} — BSIP2 Matrix Integrity Engine*",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


_DEGRADATION_LEVEL_LABELS_SHORT = {
    0: "minimal",
    1: "low",
    2: "moderate",
    3: "high",
    4: "severe",
    5: "extreme",
}


if __name__ == "__main__":
    run_validation()
