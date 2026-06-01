"""
BSIP2 Matrix Integrity Engine — Calibration Comparison Runner v2

Runs BOTH v1 (archive) and v2 on all four BSIP1 datasets and generates a
side-by-side comparison report.

Report evaluates:
  - Top-end compression reduction (products no longer clustering at 100)
  - Score distribution widening
  - Gradient realism across category ladders
  - Traditional food handling (no unfair penalties)
  - False-positive detection
  - Compensation handling improvement
  - HP triad behaviour changes
  - Transformation type classification (new in v2)
  - Assembly drag impact
  - Provenance signal quality (example traces)

Output:
  C:\\Bari\\03_operations\\reports\\matrix_integrity\\matrix_integrity_calibration_v2.md
"""

import json
import pathlib
import sys
import datetime

_src_dir = pathlib.Path(__file__).parent
sys.path.insert(0, str(_src_dir))
# v1 archive lives in 99_archive/legacy_bsip2/ after 2026-05-20 hygiene sprint
sys.path.insert(0, str(_src_dir.parents[3] / "99_archive" / "legacy_bsip2"))

from matrix_integrity    import compute_matrix_integrity,   MODULE_VERSION as V2_VERSION
from matrix_integrity_v1 import compute_matrix_integrity as compute_matrix_integrity_v1, MODULE_VERSION as V1_VERSION

BSIP1_SOURCES = {
    "snack_bars": pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output"),
    "cereals":    pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output"),
    "yogurt":     pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output"),
    "milk":       pathlib.Path(r"C:\Bari\03_operations\bsip1\run_milk_002\output"),
}

REPORT_PATH = pathlib.Path(
    r"C:\Bari\03_operations\reports\matrix_integrity\matrix_integrity_calibration_v2.md"
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
            print(f"  WARN: {f.name}: {e}")
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
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def _distribution(scores: list[float]) -> dict[str, int]:
    buckets = {
        "90-100 (minimal)": 0, "75-89 (low)": 0, "58-74 (moderate)": 0,
        "40-57 (high)": 0,     "22-39 (severe)": 0, "0-21 (extreme)": 0,
    }
    for s in scores:
        if s >= 90:   buckets["90-100 (minimal)"] += 1
        elif s >= 75: buckets["75-89 (low)"] += 1
        elif s >= 58: buckets["58-74 (moderate)"] += 1
        elif s >= 40: buckets["40-57 (high)"] += 1
        elif s >= 22: buckets["22-39 (severe)"] += 1
        else:         buckets["0-21 (extreme)"] += 1
    return buckets


def run_validation():
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"=== Matrix Integrity Calibration Comparison: {V1_VERSION} vs {V2_VERSION} ===")

    all_pairs: list[dict] = []
    by_category: dict[str, list[dict]] = {}

    for cat_tag, source_dir in BSIP1_SOURCES.items():
        if not source_dir.exists():
            print(f"  SKIP {cat_tag}: {source_dir}")
            continue
        products = load_products(source_dir)
        print(f"  {cat_tag}: {len(products)} products")

        cat_pairs = []
        for p in products:
            pid  = p.get("canonical_product_id", "unknown")
            name = _label(p)
            try:
                v1 = compute_matrix_integrity_v1(p)
                v2 = compute_matrix_integrity(p)
                row = {
                    "pid":          pid,
                    "name":         name,
                    "category_tag": cat_tag,
                    "v1_score":     v1["matrix_integrity_score"],
                    "v2_score":     v2["matrix_integrity_score"],
                    "delta":        round(v2["matrix_integrity_score"] - v1["matrix_integrity_score"], 1),
                    "v1_depth":     v1["reconstruction_depth"],
                    "v2_depth":     v2["reconstruction_depth"],
                    "v1_level":     v1["structural_degradation_level"],
                    "v2_level":     v2["structural_degradation_level"],
                    "v2_transform": v2["matrix_integrity_trace"].get("transformation_type", "—"),
                    "v2_assembly":  v2["matrix_integrity_trace"].get("assembly_drag", 0),
                    "v2_ferm":      v2["matrix_integrity_trace"].get("fermentation_factor", 0),
                    "v2_hp":        v2["matrix_integrity_trace"].get("hp_reconstruction_score", 0),
                    "v1_hp":        v1["matrix_integrity_trace"].get("hp_reconstruction_score", 0),
                    "v2_fortif":    v2["matrix_integrity_trace"].get("fortification_type", "none"),
                    "v2_provenance": v2["matrix_integrity_trace"].get("provenance", {}),
                    "v2_supp":      v2["matrix_integrity_trace"].get("supplemental_provenance", []),
                    "v1_comp":      v1["compensation_signals"],
                    "v2_comp":      v2["compensation_signals"],
                    "v1_dom":       v1["dominant_matrix_signals"],
                    "v2_dom":       v2["dominant_matrix_signals"],
                }
                cat_pairs.append(row)
                all_pairs.append(row)
            except Exception as e:
                import traceback
                print(f"    ERROR {pid}: {e}")
                traceback.print_exc()

        by_category[cat_tag] = cat_pairs

        v1_scores = [r["v1_score"] for r in cat_pairs]
        v2_scores = [r["v2_score"] for r in cat_pairs]
        if v1_scores:
            print(f"    v1: min={min(v1_scores):.1f}  avg={sum(v1_scores)/len(v1_scores):.1f}  max={max(v1_scores):.1f}")
            print(f"    v2: min={min(v2_scores):.1f}  avg={sum(v2_scores)/len(v2_scores):.1f}  max={max(v2_scores):.1f}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_report(run_dt, all_pairs, by_category)
    print(f"\nReport written: {REPORT_PATH}")


def _write_report(run_dt: str, all_pairs: list, by_category: dict):
    lines = [
        "# Matrix Integrity Engine — Calibration Comparison Report",
        "",
        f"**v1 (baseline):** `{V1_VERSION}`",
        f"**v2 (calibrated):** `{V2_VERSION}`",
        f"**Run date:** {run_dt}",
        f"**Products evaluated:** {len(all_pairs)}",
        "",
        "## What Changed in v2",
        "",
        "| Change | Effect |",
        "|--------|--------|",
        "| Supplemental mechanical scan | Rolled oats, granola, muesli now get soft degradation signals |",
        "| Assembly complexity drag (0–12) | Products with 3+ ingredients accumulate mild drag |",
        "| Fortification nuance | basic_restoration ≤10 pts; wellness_engineering up to 28 pts |",
        "| HP triad: position weighting | Early-position signals amplified ×1.1–1.2 |",
        "| HP triad: false-positive guard | Single flavor on clean matrix halved |",
        "| HP triad: matrix amplification | Degraded matrix + HP amplified ×1.12 |",
        "| Transformation type classification | New A/B/C/D taxonomy in trace |",
        "| Provenance trace block | Human-readable signal lists per product |",
        "",
        "---",
        "",
    ]

    # ── Overall score shift ───────────────────────────────────────────────────
    lines += ["## Overall Score Distribution: v1 vs v2", ""]
    v1_scores_all = [r["v1_score"] for r in all_pairs]
    v2_scores_all = [r["v2_score"] for r in all_pairs]
    d1 = _distribution(v1_scores_all)
    d2 = _distribution(v2_scores_all)
    dist_rows = [[k, d1[k], d2[k], d2[k] - d1[k]] for k in d1]
    lines.append(_md_table(["Score Range", "v1 Count", "v2 Count", "Δ"], dist_rows))
    lines.append("")

    v1_at_100 = sum(1 for s in v1_scores_all if s >= 100)
    v2_at_100 = sum(1 for s in v2_scores_all if s >= 100)
    v1_at_95  = sum(1 for s in v1_scores_all if s >= 95)
    v2_at_95  = sum(1 for s in v2_scores_all if s >= 95)
    lines += [
        f"**Products at score = 100:** v1 = {v1_at_100},  v2 = {v2_at_100}  "
        f"({v2_at_100 - v1_at_100:+d} change)",
        "",
        f"**Products at score ≥ 95:** v1 = {v1_at_95},   v2 = {v2_at_95}  "
        f"({v2_at_95 - v1_at_95:+d} change)",
        "",
    ]

    # ── Per-category summary ──────────────────────────────────────────────────
    lines += ["## Per-Category Score Summary", ""]
    cat_rows = []
    for cat, pairs in by_category.items():
        if not pairs:
            continue
        v1s = [r["v1_score"] for r in pairs]
        v2s = [r["v2_score"] for r in pairs]
        cat_rows.append([
            cat, len(pairs),
            f"{min(v1s):.1f}", f"{sum(v1s)/len(v1s):.1f}", f"{max(v1s):.1f}",
            f"{min(v2s):.1f}", f"{sum(v2s)/len(v2s):.1f}", f"{max(v2s):.1f}",
            f"{sum(v2s)/len(v2s) - sum(v1s)/len(v1s):+.1f}",
        ])
    lines.append(_md_table(
        ["Category", "N", "v1 Min", "v1 Avg", "v1 Max", "v2 Min", "v2 Avg", "v2 Max", "Avg Δ"],
        cat_rows,
    ))
    lines.append("")

    # ── Largest score changes ─────────────────────────────────────────────────
    lines += ["## Largest Score Changes (v2 vs v1)", ""]
    sorted_by_delta = sorted(all_pairs, key=lambda x: x["delta"])
    most_dropped = sorted_by_delta[:10]
    most_gained  = sorted_by_delta[-5:]

    lines += ["### Products Most Reduced (top 10 largest drops)", ""]
    drop_rows = [
        [r["name"][:50], r["category_tag"],
         f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
         f"{r['v2_assembly']:.1f}", r["v2_transform"][:30]]
        for r in most_dropped
    ]
    lines.append(_md_table(
        ["Product", "Category", "v1 Score", "v2 Score", "Δ", "Drag", "Transform Type"],
        drop_rows,
    ))
    lines.append("")

    lines += ["### Products Most Increased (should be rare)", ""]
    gain_rows = [
        [r["name"][:50], r["category_tag"],
         f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
         r["v2_fortif"]]
        for r in most_gained if r["delta"] > 0
    ]
    if gain_rows:
        lines.append(_md_table(
            ["Product", "Category", "v1 Score", "v2 Score", "Δ", "Fortif Type"],
            gain_rows,
        ))
    else:
        lines.append("_No products gained score in v2 — expected behavior._")
    lines.append("")

    # ── Soft degradation ladder ───────────────────────────────────────────────
    lines += ["## A. Soft Degradation Ladder", ""]
    lines.append(
        "Products with soft supplemental signals detected — showing how rolling, "
        "flaking, and clustering now introduce mild structural friction."
    )
    lines.append("")
    supp_products = [r for r in all_pairs if r["v2_supp"]]
    if supp_products:
        supp_sorted = sorted(supp_products, key=lambda x: -x["v2_score"])
        supp_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             "; ".join(r["v2_supp"])[:45]]
            for r in supp_sorted[:12]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1", "v2", "Δ", "Supplemental Signal"],
            supp_rows,
        ))
    else:
        lines.append("_No supplemental signals detected — may indicate vocabulary gap in ingredient texts._")
    lines.append("")

    # ── Assembly drag examples ────────────────────────────────────────────────
    lines += ["### Assembly Drag Examples (products previously at 100)", ""]
    was_100 = [r for r in all_pairs if r["v1_score"] >= 100 and r["v2_score"] < 100]
    if was_100:
        was_100_sorted = sorted(was_100, key=lambda x: -x["v2_score"])
        asm_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}",
             f"{r['v2_assembly']:.1f}", r["v2_transform"][:25]]
            for r in was_100_sorted[:15]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1 (was 100)", "v2 Score", "Drag", "Transform Type"],
            asm_rows,
        ))
    else:
        lines.append("_No products moved from 100 — check supplemental scan vocabulary coverage._")
    lines.append("")

    # ── Traditional transformation examples ──────────────────────────────────
    lines += ["## B. Traditional Transformation — Correctly Handled", ""]
    lines.append(
        "Products where strong fermentation or traditional processing is recognized "
        "and does NOT receive unfair penalty."
    )
    lines.append("")
    traditional = [
        r for r in all_pairs
        if r["v2_ferm"] >= 0.25 and r["v2_score"] >= 80
    ]
    if traditional:
        trad_sorted = sorted(traditional, key=lambda x: -x["v2_score"])
        trad_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             f"{r['v2_ferm']:.2f}", r["v2_transform"][:25]]
            for r in trad_sorted[:10]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1", "v2", "Δ", "Ferm Factor", "Transform Type"],
            trad_rows,
        ))
    else:
        lines.append("_No high-fermentation products detected in dataset._")
    lines.append("")

    # ── Engineered wellness halo examples ─────────────────────────────────────
    lines += ["## C. Engineered Wellness Halo — Correctly Penalized", ""]
    lines.append(
        "Products with high integrity scores that also carry engineering signals — "
        "potential 'clean' appearance masking compensation systems."
    )
    lines.append("")
    halo = [r for r in all_pairs if r["v2_score"] >= 70 and r["v2_fortif"] in {"wellness_engineering", "partial_compensation"}]
    if halo:
        halo_sorted = sorted(halo, key=lambda x: -x["v2_score"])
        halo_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             r["v2_fortif"]]
            for r in halo_sorted[:10]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1", "v2", "Δ", "Fortification Type"],
            halo_rows,
        ))
    else:
        lines.append("_No wellness_engineering fortification detected._")
    lines.append("")

    # ── Structural void examples ───────────────────────────────────────────────
    lines += ["## D. Structural Void — Primary Position Occupied by Refined Sweetener", ""]
    void_products = [
        r for r in all_pairs
        if any("pos1_primary_sweetener" in d for d in r.get("v2_dom", []))
        or any("pos2_primary_sweetener" in d for d in r.get("v2_dom", []))
    ]
    if void_products:
        void_sorted = sorted(void_products, key=lambda x: x["v2_score"])
        void_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             r["v2_dom"][0][:40] if r["v2_dom"] else "—"]
            for r in void_sorted[:10]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1", "v2", "Δ", "Primary Signal"],
            void_rows,
        ))
    else:
        lines.append("_No structural void products in dataset._")
    lines.append("")

    # ── HP triad behaviour changes ────────────────────────────────────────────
    lines += ["## HP Triad Behaviour Changes", ""]
    hp_changed = [r for r in all_pairs if abs(r["v2_hp"] - r["v1_hp"]) > 5.0]
    if hp_changed:
        hp_sorted = sorted(hp_changed, key=lambda x: -(x["v2_hp"] - x["v1_hp"]))
        hp_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_hp']:.0f}", f"{r['v2_hp']:.0f}",
             f"{r['v2_hp'] - r['v1_hp']:+.0f}",
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}"]
            for r in hp_sorted[:12]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1 HP", "v2 HP", "HP Δ", "v1 Score", "v2 Score"],
            hp_rows,
        ))
    else:
        lines.append("_No significant HP score changes detected._")
    lines.append("")

    # ── Fortification nuance ──────────────────────────────────────────────────
    lines += ["## Fortification Nuance: restoration vs wellness_engineering", ""]
    has_fortif = [r for r in all_pairs if r["v2_fortif"] != "none"]
    if has_fortif:
        fortif_sorted = sorted(has_fortif, key=lambda x: x["v2_fortif"])
        fortif_rows = [
            [r["name"][:48], r["category_tag"],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             r["v2_fortif"]]
            for r in fortif_sorted[:15]
        ]
        lines.append(_md_table(
            ["Product", "Category", "v1", "v2", "Δ", "Fortification Type"],
            fortif_rows,
        ))
    else:
        lines.append("_No fortified products in dataset._")
    lines.append("")

    # ── Per-category full tables ──────────────────────────────────────────────
    for cat, pairs in by_category.items():
        if not pairs:
            continue
        sorted_pairs = sorted(pairs, key=lambda x: -x["v2_score"])
        lines += [f"## {cat.replace('_', ' ').title()} — Full Comparison", ""]
        rows = [
            [r["name"][:44],
             f"{r['v1_score']:.1f}", f"{r['v2_score']:.1f}", f"{r['delta']:+.1f}",
             r["v1_level"][:3], r["v2_level"][:3],
             f"{r['v2_assembly']:.1f}",
             r["v2_transform"][:22],
             "; ".join(r["v2_supp"])[:30] if r["v2_supp"] else "—"]
            for r in sorted_pairs
        ]
        lines.append(_md_table(
            ["Product", "v1", "v2", "Δ", "L1", "L2", "Drag", "Transform", "Supp Signal"],
            rows,
        ))
        lines.append("")

    # ── Provenance examples ───────────────────────────────────────────────────
    lines += ["## Provenance Trace Examples (top 6 most interesting)", ""]
    lines.append(
        "Sample provenance blocks from v2 for selected products. "
        "These show the human-readable signal decomposition."
    )
    lines.append("")

    interesting = (
        sorted([r for r in all_pairs if r["delta"] < -5], key=lambda x: x["delta"])[:2]
        + sorted([r for r in all_pairs if r["v2_ferm"] >= 0.3], key=lambda x: -x["v2_score"])[:2]
        + sorted([r for r in all_pairs if r["v2_hp"] >= 50], key=lambda x: -x["v2_hp"])[:2]
    )
    seen_pids: set[str] = set()
    for r in interesting:
        if r["pid"] in seen_pids:
            continue
        seen_pids.add(r["pid"])
        prov = r["v2_provenance"]
        lines += [f"### {r['name'][:60]} ({r['category_tag']})", ""]
        lines.append(f"v1 score: **{r['v1_score']:.0f}** → v2 score: **{r['v2_score']:.0f}** (Δ {r['delta']:+.1f})")
        lines.append(f"Transform type: `{r['v2_transform']}`  |  Assembly drag: {r['v2_assembly']:.1f}")
        lines.append("")

        if prov.get("degradation_signals"):
            lines.append("**Degradation signals:**")
            for s in prov["degradation_signals"]:
                lines.append(f"- {s}")
        if prov.get("engineering_signals"):
            lines.append("")
            lines.append("**Engineering signals:**")
            for s in prov["engineering_signals"]:
                lines.append(f"- {s}")
        if prov.get("compensation_signals"):
            lines.append("")
            lines.append("**Compensation signals:**")
            for s in prov["compensation_signals"]:
                lines.append(f"- {s}")
        if prov.get("protective_signals"):
            lines.append("")
            lines.append("**Protective signals:**")
            for s in prov["protective_signals"]:
                lines.append(f"- {s}")
        lines.append("")

    lines += [
        "---",
        "",
        f"*Generated by {V2_VERSION} vs {V1_VERSION} — BSIP2 Matrix Integrity Calibration Sprint*",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


_DEGRADATION_LEVEL_LABELS_SHORT = {
    0: "minimal", 1: "low", 2: "moderate", 3: "high", 4: "severe", 5: "extreme",
}


if __name__ == "__main__":
    run_validation()
