"""
BSIP2 Prototype v0 — Diagnostic Visuals
Internal diagnostic charts from bsip2_trace.json files.
Not for external use. Prioritizes clarity, labels, and traceability.

Run from: C:\Bari\03_operations\bsip2\proto_v0\src\
  python generate_visuals.py
"""
import json
import pathlib
import collections
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
TRACE_ROOT     = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
VISUAL_ROOT    = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\visuals")
DATA_ROOT      = VISUAL_ROOT / "data"
WATERFALL_ROOT = VISUAL_ROOT / "product_waterfall_examples"

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
GRADE_COLORS = {
    "A":                "#1b4332",
    "B":                "#40916c",
    "C":                "#95d5b2",
    "D":                "#f4a261",
    "E":                "#e63946",
    "insufficient_data":"#adb5bd",
    "?":                "#dee2e6",
}
NOVA_COLORS = {1: "#40916c", 2: "#95d5b2", 3: "#f4a261", 4: "#e63946"}
CATEGORY_ORDER = [
    "whole_food_fat", "snack_bar_granola", "cereal",
    "dairy_protein", "dessert", "beverage", "sauce_spread", "default",
]
DPI = 150

# Grade thresholds for reference lines
GRADE_LINES = [(85, "A", "#1b4332"), (70, "B", "#40916c"),
               (55, "C", "#95d5b2"), (40, "D", "#f4a261")]

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "font.size":          10,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.3,
    "grid.linestyle":     "--",
    "figure.facecolor":   "white",
    "axes.facecolor":     "white",
    "axes.edgecolor":     "#444444",
    "xtick.color":        "#444444",
    "ytick.color":        "#444444",
})


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_traces() -> list[dict]:
    traces = []
    for path in sorted(TRACE_ROOT.glob("*/bsip2_trace.json")):
        with open(path, encoding="utf-8") as f:
            traces.append(json.load(f))
    print(f"Loaded {len(traces)} traces from {TRACE_ROOT}")
    return traces


def build_dataframe(traces: list[dict]) -> pd.DataFrame:
    rows = []
    for t in traces:
        ref  = t.get("input_reference") or {}
        pid  = ref.get("canonical_product_id") or "unknown"
        name = ref.get("product_name_he") or ""
        rows.append({
            "pid":                    pid,
            "name":                   name,
            "name_short":             name[:35] + "…" if len(name) > 35 else name,
            "final_score":            t.get("final_score_estimate"),
            "grade":                  t.get("grade_estimate") or "?",
            "data_sufficiency":       t.get("data_sufficiency") or "sufficient",
            "evaluation_status":      t.get("evaluation_status"),
            "category":               t.get("category") or "default",
            "nova":                   t.get("nova_proxy"),
            "confidence_score":       t.get("confidence_score"),
            "confidence_band":        t.get("confidence_band"),
            "category_instability":   t.get("category_instability_flag") or False,
            "secondary_category":     t.get("secondary_category") or "",
            "category_confidence":    t.get("category_confidence"),
            "caps_applied":           t.get("caps_applied") or [],
            "penalties_applied":      t.get("penalties_applied") or [],
            "unresolved_flags":       t.get("unresolved_flags") or [],
            "floors_applied":         t.get("floors_applied") or [],
            "weighted_dim_score":     t.get("weighted_dimension_score"),
            "score_after_cap":        t.get("score_after_cap"),
            "binding_cap":            t.get("binding_cap"),
            "score_after_penalty":    t.get("score_after_penalty"),
            "score_after_floors":     t.get("score_after_floors"),
            "concern_family":         t.get("concern_family_coordination") or {},
        })
    return pd.DataFrame(rows)


def sufficient(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["data_sufficiency"] == "sufficient"].copy()


# ---------------------------------------------------------------------------
# CSV exports
# ---------------------------------------------------------------------------

def export_csvs(df: pd.DataFrame, traces: list[dict]):
    DATA_ROOT.mkdir(parents=True, exist_ok=True)

    # product_scores.csv
    cols = ["pid", "name", "final_score", "grade", "data_sufficiency",
            "evaluation_status", "category", "nova", "confidence_score",
            "confidence_band", "category_instability", "binding_cap"]
    df[cols].to_csv(DATA_ROOT / "product_scores.csv", index=False, encoding="utf-8-sig")
    print("  Exported: product_scores.csv")

    # cap_frequency.csv
    cap_counts = collections.Counter()
    for t in traces:
        for c in (t.get("caps_applied") or []):
            cap_counts[c["rule"]] += 1
    with open(DATA_ROOT / "cap_frequency.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["rule", "count"])
        for rule, cnt in cap_counts.most_common():
            w.writerow([rule, cnt])
    print("  Exported: cap_frequency.csv")

    # penalty_frequency.csv
    pen_counts = collections.Counter()
    for t in traces:
        for p in (t.get("penalties_applied") or []):
            pen_counts[p["rule"]] += 1
    with open(DATA_ROOT / "penalty_frequency.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["rule", "count"])
        for rule, cnt in pen_counts.most_common():
            w.writerow([rule, cnt])
    print("  Exported: penalty_frequency.csv")

    # concern_family_frequency.csv
    family_caps  = collections.Counter()
    family_pens  = collections.Counter()
    for t in traces:
        cf = t.get("concern_family_coordination") or {}
        for fam, data in cf.items():
            if data.get("binding_cap") is not None:
                family_caps[fam] += 1
            if (data.get("coordinated_penalty") or 0) > 0:
                family_pens[fam] += 1
    all_fams = sorted(set(list(family_caps.keys()) + list(family_pens.keys())))
    with open(DATA_ROOT / "concern_family_frequency.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["family", "cap_applications", "penalty_applications"])
        for fam in all_fams:
            w.writerow([fam, family_caps[fam], family_pens[fam]])
    print("  Exported: concern_family_frequency.csv")

    # category_grade_matrix.csv
    suf = sufficient(df)
    cats = [c for c in CATEGORY_ORDER if c in suf["category"].values]
    grades = ["A","B","C","D","E"]
    with open(DATA_ROOT / "category_grade_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["category"] + grades)
        for cat in cats:
            row = [cat]
            for g in grades:
                row.append(int(((suf["category"] == cat) & (suf["grade"] == g)).sum()))
            w.writerow(row)
    print("  Exported: category_grade_matrix.csv")

    # unstable_products.csv
    unstable = df[df["category_instability"]].copy()
    unstable_cols = ["pid", "name", "final_score", "grade", "category",
                     "category_confidence", "secondary_category", "nova"]
    unstable[unstable_cols].to_csv(DATA_ROOT / "unstable_products.csv",
                                   index=False, encoding="utf-8-sig")
    print("  Exported: unstable_products.csv")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _grade_line_legend():
    return [mpatches.Patch(color=c, label=f"Grade {g} threshold ({v})")
            for v, g, c in GRADE_LINES]


def _add_grade_lines(ax, orientation="horizontal", alpha=0.25, linewidth=1.0):
    for v, g, c in GRADE_LINES:
        if orientation == "horizontal":
            ax.axhline(v, color=c, linestyle=":", alpha=alpha, linewidth=linewidth, zorder=1)
        else:
            ax.axvline(v, color=c, linestyle=":", alpha=alpha, linewidth=linewidth, zorder=1)


def _save(fig, name: str):
    path = VISUAL_ROOT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {name}")


# ---------------------------------------------------------------------------
# 1. Score distribution histogram
# ---------------------------------------------------------------------------

def chart_score_histogram(df: pd.DataFrame):
    suf = sufficient(df)
    scores = suf["final_score"].dropna().tolist()
    mean_s = np.mean(scores)
    median_s = np.median(scores)

    fig, ax = plt.subplots(figsize=(10, 5))
    bins = np.arange(10, 70, 4)
    counts, edges, patches = ax.hist(scores, bins=bins, color="#4361ee", alpha=0.75,
                                      edgecolor="white", linewidth=0.8)

    # Color bars by grade
    for patch, left in zip(patches, edges[:-1]):
        right = left + (edges[1] - edges[0])
        mid = (left + right) / 2
        for v, g, c in sorted(GRADE_LINES, key=lambda x: -x[0]):
            if mid >= v:
                patch.set_facecolor(GRADE_COLORS[g])
                break
        else:
            patch.set_facecolor(GRADE_COLORS["E"])

    ax.axvline(mean_s,   color="#333333", linestyle="--", linewidth=1.5,
               label=f"Mean: {mean_s:.1f}")
    ax.axvline(median_s, color="#666666", linestyle=":",  linewidth=1.5,
               label=f"Median: {median_s:.1f}")
    _add_grade_lines(ax, "vertical", alpha=0.35, linewidth=1.2)

    ax.set_xlabel("Final Score (sufficient-data products only)")
    ax.set_ylabel("Count")
    ax.set_title(f"Score Distribution — {len(scores)} products (5 insufficient_data excluded)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    _save(fig, "score_distribution_histogram.png")


# ---------------------------------------------------------------------------
# 2. Grade distribution bar
# ---------------------------------------------------------------------------

def chart_grade_bar(df: pd.DataFrame):
    grade_order = ["A", "B", "C", "D", "E", "insufficient_data"]
    counts = df["grade"].value_counts()
    vals   = [counts.get(g, 0) for g in grade_order]
    colors = [GRADE_COLORS[g] for g in grade_order]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(grade_order, vals, color=colors, edgecolor="white", linewidth=0.8, width=0.6)
    for bar, val in zip(bars, vals):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_xlabel("Grade")
    ax.set_ylabel("Product Count")
    ax.set_title(f"Grade Distribution — all 53 products\n"
                 f"(insufficient_data = no nutrition panel; score tentative)")
    ax.set_ylim(0, max(vals) * 1.15)
    ax.grid(axis="y", alpha=0.3)
    ax.grid(axis="x", alpha=0)
    fig.tight_layout()
    _save(fig, "grade_distribution_bar.png")


# ---------------------------------------------------------------------------
# 3. Category × Grade heatmap
# ---------------------------------------------------------------------------

def chart_category_grade_heatmap(df: pd.DataFrame):
    suf = sufficient(df)
    grade_cols = ["A","B","C","D","E"]
    cats = [c for c in CATEGORY_ORDER if c in suf["category"].values]
    matrix = pd.DataFrame(0, index=cats, columns=grade_cols)
    for _, row in suf.iterrows():
        g = row["grade"]
        c = row["category"]
        if g in grade_cols and c in cats:
            matrix.loc[c, g] += 1

    fig, ax = plt.subplots(figsize=(9, max(4, len(cats) * 0.9 + 1.5)))
    im = ax.imshow(matrix.values, cmap="YlOrRd", aspect="auto", vmin=0)
    ax.set_xticks(range(len(grade_cols)))
    ax.set_xticklabels(grade_cols, fontsize=11)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels(cats, fontsize=9)
    ax.set_xlabel("Grade")
    ax.set_ylabel("Category")
    ax.set_title("Product Count by Category × Grade (sufficient data only)")

    for i in range(len(cats)):
        for j in range(len(grade_cols)):
            val = matrix.iloc[i, j]
            if val > 0:
                textcol = "white" if val > matrix.values.max() * 0.6 else "black"
                ax.text(j, i, str(val), ha="center", va="center",
                        fontsize=12, fontweight="bold", color=textcol)

    plt.colorbar(im, ax=ax, label="Product count", shrink=0.7)
    fig.tight_layout()
    _save(fig, "category_grade_heatmap.png")


# ---------------------------------------------------------------------------
# 4. NOVA × Score boxplot
# ---------------------------------------------------------------------------

def chart_nova_boxplot(df: pd.DataFrame):
    suf = sufficient(df)
    nova_levels = sorted(suf["nova"].dropna().unique())
    data_by_nova = {int(n): suf[suf["nova"] == n]["final_score"].dropna().tolist()
                    for n in nova_levels}

    fig, ax = plt.subplots(figsize=(9, 5))
    positions = list(range(len(nova_levels)))
    bps = ax.boxplot([data_by_nova[int(n)] for n in nova_levels],
                      positions=positions, widths=0.5, patch_artist=True,
                      medianprops=dict(color="black", linewidth=2),
                      whiskerprops=dict(linewidth=1.2),
                      boxprops=dict(linewidth=1.2),
                      flierprops=dict(marker="o", markersize=5, alpha=0.5))

    for patch, nova in zip(bps["boxes"], nova_levels):
        patch.set_facecolor(NOVA_COLORS.get(int(nova), "#cccccc"))
        patch.set_alpha(0.75)

    # Overlay jittered points
    for i, nova in enumerate(nova_levels):
        pts = data_by_nova[int(nova)]
        jitter = np.random.uniform(-0.15, 0.15, len(pts))
        ax.scatter(np.full(len(pts), i) + jitter, pts,
                   color=NOVA_COLORS.get(int(nova), "#cccccc"),
                   alpha=0.4, s=18, zorder=5)
        ax.text(i, ax.get_ylim()[0] - 3 if ax.get_ylim()[0] > 5 else 1,
                f"n={len(pts)}", ha="center", va="top", fontsize=8, color="#555")

    _add_grade_lines(ax, "horizontal", alpha=0.3, linewidth=1.2)
    ax.set_xticks(positions)
    ax.set_xticklabels([f"NOVA {int(n)}" for n in nova_levels], fontsize=10)
    ax.set_ylabel("Final Score")
    ax.set_title("Score Distribution by NOVA Proxy Level (sufficient data only)")
    ax.set_ylim(0, 100)
    nova_legend = [mpatches.Patch(color=NOVA_COLORS[n], label=f"NOVA {n}", alpha=0.75)
                   for n in nova_levels if n in NOVA_COLORS]
    ax.legend(handles=nova_legend + _grade_line_legend(), fontsize=8,
              loc="upper left", ncol=2)
    fig.tight_layout()
    _save(fig, "nova_score_boxplot.png")


# ---------------------------------------------------------------------------
# 5. Confidence × Score scatter
# ---------------------------------------------------------------------------

def chart_confidence_scatter(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 6))

    grade_order = ["C", "D", "E", "insufficient_data"]
    for grade in grade_order:
        sub = df[df["grade"] == grade]
        label = grade if grade != "insufficient_data" else "insufficient_data (tentative)"
        ax.scatter(sub["confidence_score"], sub["final_score"],
                   color=GRADE_COLORS.get(grade, "#999"),
                   label=label, alpha=0.75, s=55, edgecolors="white", linewidths=0.5, zorder=3)

    # Annotate outliers (very low confidence + score)
    for _, row in df.iterrows():
        if (row["confidence_score"] or 100) < 30 or (row["final_score"] or 100) < 15:
            ax.annotate(row["pid"].replace("bsip1_", ""),
                        xy=(row["confidence_score"], row["final_score"]),
                        xytext=(5, 5), textcoords="offset points",
                        fontsize=6.5, color="#555")

    # Confidence ceiling reference lines
    ax.axvline(40, color="#adb5bd", linestyle="--", linewidth=1, alpha=0.8,
               label="Confidence ceiling threshold (40)")
    ax.axhline(50, color="#adb5bd", linestyle=":", linewidth=1, alpha=0.6,
               label="Insufficient confidence ceiling (50)")

    _add_grade_lines(ax, "horizontal", alpha=0.2, linewidth=1.0)
    ax.set_xlabel("Confidence Score (0–100)")
    ax.set_ylabel("Final Score Estimate")
    ax.set_title("Confidence Score vs. Final Score — all 53 products")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 100)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _save(fig, "confidence_score_scatter.png")


# ---------------------------------------------------------------------------
# 6. Cap frequency bar
# ---------------------------------------------------------------------------

def chart_cap_frequency(traces: list[dict]):
    cap_counts = collections.Counter()
    for t in traces:
        for c in (t.get("caps_applied") or []):
            cap_counts[c["rule"]] += 1

    if not cap_counts:
        print("  WARNING: no cap data found")
        return

    rules, counts = zip(*cap_counts.most_common())
    colors = ["#e63946" if "NOVA" in r or "ULTRA" in r else
              "#f4a261" if "SUGAR" in r or "CAL" in r else
              "#4361ee" if "ADDITIVE" in r else
              "#7b2d8b" if "SAT_FAT" in r else "#888"
              for r in rules]

    fig, ax = plt.subplots(figsize=(12, max(5, len(rules) * 0.5 + 1.5)))
    y = np.arange(len(rules))
    ax.barh(y, counts, color=colors, alpha=0.82, edgecolor="white", linewidth=0.6)
    for i, (cnt, rule) in enumerate(zip(counts, rules)):
        ax.text(cnt + 0.2, i, str(cnt), va="center", fontsize=8.5)
    ax.set_yticks(y)
    ax.set_yticklabels(rules, fontsize=8.5)
    ax.set_xlabel("Number of Products Where Cap Was Applied")
    ax.set_title(f"Cap Rule Application Frequency — {len(traces)} products")
    ax.set_xlim(0, max(counts) * 1.15)
    ax.invert_yaxis()

    # Legend for color coding
    legend_items = [
        mpatches.Patch(color="#e63946", alpha=0.82, label="NOVA / processing"),
        mpatches.Patch(color="#f4a261", alpha=0.82, label="Sugar / calorie load"),
        mpatches.Patch(color="#4361ee", alpha=0.82, label="Additive"),
        mpatches.Patch(color="#7b2d8b", alpha=0.82, label="Fat quality"),
    ]
    ax.legend(handles=legend_items, fontsize=8, loc="lower right")
    fig.tight_layout()
    _save(fig, "cap_frequency_bar.png")


# ---------------------------------------------------------------------------
# 7. Penalty frequency bar
# ---------------------------------------------------------------------------

def chart_penalty_frequency(traces: list[dict]):
    pen_counts = collections.Counter()
    for t in traces:
        for p in (t.get("penalties_applied") or []):
            pen_counts[p["rule"]] += 1

    if not pen_counts:
        print("  WARNING: no penalty data found")
        return

    rules, counts = zip(*pen_counts.most_common())

    fig, ax = plt.subplots(figsize=(11, max(4, len(rules) * 0.55 + 1.5)))
    y = np.arange(len(rules))
    ax.barh(y, counts, color="#f4a261", alpha=0.82, edgecolor="white", linewidth=0.6)
    for i, cnt in enumerate(counts):
        ax.text(cnt + 0.1, i, str(cnt), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(rules, fontsize=9)
    ax.set_xlabel("Number of Products Where Penalty Was Applied")
    ax.set_title(f"Penalty Rule Application Frequency — {len(traces)} products")
    ax.set_xlim(0, max(counts) * 1.15)
    ax.invert_yaxis()
    fig.tight_layout()
    _save(fig, "penalty_frequency_bar.png")


# ---------------------------------------------------------------------------
# 8. Concern family frequency bar
# ---------------------------------------------------------------------------

def chart_concern_family_frequency(traces: list[dict]):
    family_caps  = collections.Counter()
    family_pens  = collections.Counter()

    for t in traces:
        cf = t.get("concern_family_coordination") or {}
        for fam, data in cf.items():
            if data.get("binding_cap") is not None:
                family_caps[fam] += 1
            if (data.get("coordinated_penalty") or 0) > 0:
                family_pens[fam] += 1

    # Add confidence/data_quality family from unresolved flags
    data_quality_ct = 0
    for t in traces:
        for f in (t.get("unresolved_flags") or []):
            if any(kw in f for kw in ("BSIP1_", "KCAL_IMPL", "SUGAR_EXCEEDS", "SATFAT_EXCEEDS")):
                data_quality_ct += 1
                break
    if data_quality_ct:
        family_pens["confidence/data_quality"] = data_quality_ct

    all_fams = sorted(set(list(family_caps.keys()) + list(family_pens.keys())))
    x = np.arange(len(all_fams))
    width = 0.38

    fig, ax = plt.subplots(figsize=(12, 5))
    b1 = ax.bar(x - width/2, [family_caps[f] for f in all_fams], width,
                label="Cap applied", color="#e63946", alpha=0.8, edgecolor="white")
    b2 = ax.bar(x + width/2, [family_pens[f] for f in all_fams], width,
                label="Penalty applied", color="#f4a261", alpha=0.8, edgecolor="white")

    for bar in list(b1) + list(b2):
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.3,
                    str(int(h)), ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(all_fams, fontsize=9, rotation=20, ha="right")
    ax.set_ylabel("Number of Products")
    ax.set_title(f"Guardrail Activation by Concern Family — {len(traces)} products")
    ax.legend(fontsize=9)
    fig.tight_layout()
    _save(fig, "concern_family_frequency_bar.png")


# ---------------------------------------------------------------------------
# 9. Floor application bar
# ---------------------------------------------------------------------------

def chart_floor_application(df: pd.DataFrame, traces: list[dict]):
    floor_counts = collections.Counter()
    binding_counts = collections.Counter()

    for t in traces:
        for fl in (t.get("floors_applied") or []):
            ft = fl.get("floor_type") or "unknown"
            floor_counts[ft] += 1
            if fl.get("pre_floor") is not None:
                binding_counts[ft] += 1

    considered = collections.Counter()
    for t in traces:
        for fc in (t.get("floors_considered") or []):
            if isinstance(fc, dict):
                ft = fc.get("floor_type") or "unknown"
                considered[ft] += 1

    all_floors = sorted(set(list(floor_counts.keys()) + list(considered.keys())))
    if not all_floors:
        print("  No floor data found — skipping floor chart")
        return

    x = np.arange(len(all_floors))
    width = 0.38
    fig, ax = plt.subplots(figsize=(10, 5))
    b1 = ax.bar(x - width/2, [considered.get(f, 0) for f in all_floors], width,
                label="Floor considered (eligible)", color="#95d5b2", alpha=0.85, edgecolor="white")
    b2 = ax.bar(x + width/2, [floor_counts.get(f, 0) for f in all_floors], width,
                label="Floor actually binding (raised score)", color="#40916c", alpha=0.85, edgecolor="white")

    for bar in list(b1) + list(b2):
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.1,
                    str(int(h)), ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(all_floors, fontsize=9, rotation=15, ha="right")
    ax.set_ylabel("Number of Products")
    ax.set_title("Floor Application — Eligible vs. Binding")
    ax.legend(fontsize=9)
    ax.set_ylim(0, max(considered.values() or [1]) * 1.2)
    fig.tight_layout()
    _save(fig, "floor_application_bar.png")


# ---------------------------------------------------------------------------
# 10. Category instability chart
# ---------------------------------------------------------------------------

def chart_category_instability(df: pd.DataFrame):
    unstable = df[df["category_instability"]].copy()
    stable   = df[~df["category_instability"]].copy()

    # Bar chart: count of instability by primary category
    cat_unstable = unstable["category"].value_counts()
    cat_stable   = stable["category"].value_counts()
    all_cats = [c for c in CATEGORY_ORDER
                if c in cat_unstable.index or c in cat_stable.index]

    x = np.arange(len(all_cats))
    width = 0.38
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5),
                                    gridspec_kw={"width_ratios": [1, 1.3]})

    # Left: stacked count by category
    b_stable   = ax1.bar(x, [cat_stable.get(c, 0) for c in all_cats],
                          width*2, label="Stable", color="#95d5b2", alpha=0.8, edgecolor="white")
    b_unstable = ax1.bar(x, [cat_unstable.get(c, 0) for c in all_cats],
                          width*2, bottom=[cat_stable.get(c, 0) for c in all_cats],
                          label="Unstable", color="#e63946", alpha=0.8, edgecolor="white")
    ax1.set_xticks(x)
    ax1.set_xticklabels(all_cats, fontsize=8, rotation=20, ha="right")
    ax1.set_ylabel("Product Count")
    ax1.set_title("Category Stability by Primary Category")
    ax1.legend(fontsize=9)

    # Right: scatter of category_confidence for unstable products
    if not unstable.empty:
        cats_u = unstable["category"].tolist()
        confs  = unstable["category_confidence"].tolist()
        colors_u = ["#e63946" if c < 0.5 else "#f4a261" for c in confs]
        y_pos = np.arange(len(cats_u))
        ax2.barh(y_pos, confs, color=colors_u, alpha=0.8, edgecolor="white")
        ax2.axvline(0.5, color="#888", linestyle="--", linewidth=1, alpha=0.7,
                    label="Low conf. threshold (0.5)")
        ax2.axvline(0.8, color="#333", linestyle="--", linewidth=1, alpha=0.7,
                    label="High conf. threshold (0.8)")
        labels_u = [f"{row['pid'].replace('bsip1_','')} → {row['secondary_category']}"
                    for _, row in unstable.iterrows()]
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(labels_u, fontsize=7.5)
        ax2.set_xlabel("Category Confidence")
        ax2.set_title(f"Unstable Products (n={len(unstable)}): Confidence & Secondary Category")
        ax2.set_xlim(0, 1.05)
        ax2.legend(fontsize=8)
        ax2.invert_yaxis()

    fig.suptitle("Category Instability Analysis", fontsize=12, fontweight="bold")
    fig.tight_layout()
    _save(fig, "category_instability_chart.png")


# ---------------------------------------------------------------------------
# 11. Before/after signal hygiene delta
# ---------------------------------------------------------------------------

BEFORE_VALUES = {
    "Unresolved flags":         52,
    "Trans fat flags":          46,
    "Category instability":     11,
    "insufficient_data grades": 0,
}


def chart_signal_hygiene_delta(df: pd.DataFrame, traces: list[dict]):
    # Compute after values
    after = {
        "Unresolved flags":         int(df["unresolved_flags"].apply(bool).sum()),
        "Trans fat flags":          sum(
            1 for t in traces
            for f in (t.get("unresolved_flags") or []) if "TRANS_FAT" in f
        ),
        "Category instability":     int(df["category_instability"].sum()),
        "insufficient_data grades": int((df["grade"] == "insufficient_data").sum()),
    }

    metrics = list(BEFORE_VALUES.keys())
    before_vals = [BEFORE_VALUES[m] for m in metrics]
    after_vals  = [after[m] for m in metrics]
    x = np.arange(len(metrics))
    width = 0.36

    fig, ax = plt.subplots(figsize=(11, 5))
    b1 = ax.bar(x - width/2, before_vals, width, label="Before (v0 first run)",
                color="#e63946", alpha=0.8, edgecolor="white")
    b2 = ax.bar(x + width/2, after_vals, width, label="After (signal hygiene)",
                color="#40916c", alpha=0.8, edgecolor="white")

    for bar, val in zip(list(b1) + list(b2), before_vals + after_vals):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(val), ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Delta annotations
    for i, (bv, av) in enumerate(zip(before_vals, after_vals)):
        delta = av - bv
        sign  = "+" if delta > 0 else ""
        color = "#40916c" if delta <= 0 else "#e63946"
        ax.text(x[i], max(bv, av) + 1.5, f"{sign}{delta}",
                ha="center", fontsize=10, color=color, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_ylabel("Count")
    ax.set_title("Signal Hygiene Fixes: Before vs. After\n"
                 "(Fixes applied: trans fat artifact gate, category name-only matching, insufficient_data grade)")
    ax.legend(fontsize=9)
    ax.set_ylim(0, max(before_vals) * 1.25)
    ax.text(0.98, 0.97, "Note: insufficient_data is a NEW metric — previously\nthese 5 products received D or E grades.",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.5,
            color="#666", style="italic")
    fig.tight_layout()
    _save(fig, "before_after_signal_hygiene_delta.png")


# ---------------------------------------------------------------------------
# 12. Product waterfall charts
# ---------------------------------------------------------------------------

def _pipeline_stages(t: dict) -> list[tuple[str, float]]:
    """Extract cumulative pipeline values for waterfall display."""
    stages = []
    dim  = t.get("weighted_dimension_score")
    cap  = t.get("score_after_cap")
    pen  = t.get("score_after_penalty")
    flo  = t.get("score_after_floors")
    fin  = t.get("final_score_estimate")

    if dim is None or fin is None:
        return []

    stages.append(("Dimension\nScore", dim))

    cap_val = cap if cap is not None else dim
    if abs(cap_val - dim) > 0.05:
        stages.append(("Cap\nApplied", cap_val))

    pen_val = pen if pen is not None else cap_val
    if abs(pen_val - cap_val) > 0.05:
        stages.append(("Penalty\nApplied", pen_val))

    flo_val = flo if flo is not None else pen_val
    if abs(flo_val - pen_val) > 0.05:
        stages.append(("Floor\nApplied", flo_val))

    if abs(fin - flo_val) > 0.05:
        stages.append(("Confidence\nCeiling", fin))
    elif len(stages) == 0 or stages[-1][1] != fin:
        stages.append(("Final\nScore", fin))

    return stages


def _waterfall_chart_for_product(t: dict, ax: plt.Axes):
    stages = _pipeline_stages(t)
    if not stages:
        ax.text(0.5, 0.5, "Insufficient data for waterfall",
                ha="center", va="center", transform=ax.transAxes, color="#888")
        return

    labels = [s[0] for s in stages]
    values = [s[1] for s in stages]
    n = len(stages)
    x = np.arange(n)

    # Determine colors and bar geometry for each stage
    bar_bottoms = []
    bar_heights = []
    bar_colors  = []

    for i, (label, val) in enumerate(stages):
        if i == 0:
            bar_bottoms.append(0)
            bar_heights.append(val)
            bar_colors.append("#4361ee")
        else:
            prev = values[i - 1]
            delta = val - prev
            if delta < -0.05:
                bar_bottoms.append(val)
                bar_heights.append(abs(delta))
                bar_colors.append("#e63946")  # red: reduction
            elif delta > 0.05:
                bar_bottoms.append(prev)
                bar_heights.append(delta)
                bar_colors.append("#40916c")  # green: floor increase
            else:
                bar_bottoms.append(val - 0.5)
                bar_heights.append(1)
                bar_colors.append("#adb5bd")  # gray: no change

    ax.bar(x, bar_heights, bottom=bar_bottoms, color=bar_colors,
           edgecolor="white", linewidth=0.8, width=0.6, alpha=0.87)

    # Value labels
    for i, val in enumerate(values):
        va = "bottom"
        offset = 1.2
        if i > 0 and values[i] < values[i - 1]:
            va = "top"; offset = -1.2
        ax.text(i, val + offset, f"{val:.1f}", ha="center", va=va,
                fontsize=9, fontweight="bold")

    # Delta labels on reduction/addition bars
    for i in range(1, n):
        delta = values[i] - values[i - 1]
        if abs(delta) > 0.5:
            mid_y = (values[i] + values[i-1]) / 2
            sign  = "+" if delta > 0 else ""
            ax.text(i, mid_y, f"{sign}{delta:.1f}",
                    ha="center", va="center", fontsize=7.5,
                    color="white", fontweight="bold")

    # Connector lines (step lines at current value)
    for i in range(n - 1):
        ax.plot([i + 0.3, i + 0.7], [values[i], values[i]],
                color="#777", linestyle="--", linewidth=0.7, alpha=0.5)

    # Grade threshold lines
    _add_grade_lines(ax, "horizontal", alpha=0.3, linewidth=1.0)

    # Cap rule annotation (if cap was applied)
    if t.get("binding_cap") is not None:
        caps = [c["rule"] for c in (t.get("caps_applied") or [])]
        cap_text = "Cap: " + ", ".join(caps[:2])
        if len(caps) > 2:
            cap_text += f" +{len(caps)-2}"
        ax.text(0.98, 0.02, cap_text, transform=ax.transAxes,
                ha="right", va="bottom", fontsize=7, color="#e63946",
                style="italic")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score")

    # Binding cap reference line
    if t.get("binding_cap") is not None:
        ax.axhline(t["binding_cap"], color="#e63946", linestyle=":",
                   linewidth=1.2, alpha=0.6)

    # Final score annotation
    final = t.get("final_score_estimate")
    grade = t.get("grade_estimate") or "?"
    grade_color = GRADE_COLORS.get(grade, "#555")
    ax.axhline(final, color=grade_color, linestyle="-", linewidth=1.5, alpha=0.8,
               label=f"Final: {final} ({grade})")
    ax.legend(fontsize=8, loc="upper right")


def waterfall_for_product(t: dict, output_path: pathlib.Path):
    ref   = t.get("input_reference") or {}
    pid   = ref.get("canonical_product_id") or "unknown"
    name  = ref.get("product_name_he") or ""
    score = t.get("final_score_estimate")
    grade = t.get("grade_estimate") or "?"
    cat   = t.get("category") or "?"
    nova  = t.get("nova_proxy") or "?"
    conf  = t.get("confidence_score") or "?"
    suf   = t.get("data_sufficiency") or "sufficient"

    fig, ax = plt.subplots(figsize=(11, 5))
    _waterfall_chart_for_product(t, ax)

    # Score dimension breakdown as inset table
    dim_scores = t.get("dimension_scores") or {}
    dim_weights = t.get("dimension_weights") or {}
    if dim_scores and dim_weights:
        rows = []
        for dim, score_d in sorted(dim_scores.items(), key=lambda x: -x[1]):
            w = dim_weights.get(dim, 0)
            rows.append([dim.replace("_", "\n"), f"{score_d:.0f}", f"{w*100:.0f}%",
                         f"{score_d * w:.1f}"])
        if rows:
            table = ax.table(cellText=rows,
                             colLabels=["Dimension", "Score", "Weight", "Contrib."],
                             bbox=[1.02, 0, 0.45, 1],
                             cellLoc="center")
            table.auto_set_font_size(False)
            table.set_fontsize(6.5)
            for (row, col), cell in table.get_celld().items():
                cell.set_edgecolor("#ddd")
                if row == 0:
                    cell.set_facecolor("#f0f0f0")
                    cell.set_text_props(fontweight="bold")

    suffix = f" [INSUFFICIENT DATA]" if suf == "insufficient" else ""
    ax.set_title(
        f"{pid}  |  Cat: {cat}  NOVA: {nova}  Conf: {conf}\n"
        f"Score: {score} ({grade}{suffix})",
        fontsize=9
    )
    fig.subplots_adjust(right=0.68)
    fig.savefig(output_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {output_path.name}")


def chart_waterfall_examples(df: pd.DataFrame, traces: list[dict]):
    WATERFALL_ROOT.mkdir(parents=True, exist_ok=True)
    trace_by_pid = {
        (t.get("input_reference") or {}).get("canonical_product_id"): t
        for t in traces
    }

    suf = sufficient(df)

    def pick(criteria_df, label):
        if criteria_df.empty:
            print(f"  WARNING: no product found for waterfall '{label}'")
            return None
        return trace_by_pid.get(criteria_df.iloc[0]["pid"])

    # 1. Highest scoring (sufficient data)
    t1 = pick(suf.sort_values("final_score", ascending=False).head(1), "top scorer")

    # 2. Lowest scoring (sufficient data)
    t2 = pick(suf.sort_values("final_score", ascending=True).head(1), "lowest scorer")

    # 3. Insufficient data product
    insuf = df[df["data_sufficiency"] == "insufficient"]
    t3 = pick(insuf.sort_values("confidence_score", ascending=True).head(1),
              "insufficient data")

    # 4. Category instability (sufficient data)
    unstable = suf[suf["category_instability"]].sort_values("category_confidence")
    t4 = pick(unstable.head(1), "category instability")

    # 5. Mid-score D (closest to 45)
    d_products = suf[suf["grade"] == "D"].copy()
    d_products["dist_to_45"] = (d_products["final_score"] - 45).abs()
    t5 = pick(d_products.sort_values("dist_to_45").head(1), "mid-score D")

    waterfall_specs = [
        (t1, "1_top_scorer"),
        (t2, "2_lowest_scorer"),
        (t3, "3_insufficient_data"),
        (t4, "4_category_instability"),
        (t5, "5_mid_score_D"),
    ]

    for trace, fname in waterfall_specs:
        if trace is None:
            continue
        waterfall_for_product(trace, WATERFALL_ROOT / f"{fname}_waterfall.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    VISUAL_ROOT.mkdir(parents=True, exist_ok=True)

    print("Loading traces…")
    traces = load_traces()
    df = build_dataframe(traces)

    print("\nExporting CSVs…")
    export_csvs(df, traces)

    print("\nGenerating charts…")
    chart_score_histogram(df)
    chart_grade_bar(df)
    chart_category_grade_heatmap(df)
    chart_nova_boxplot(df)
    chart_confidence_scatter(df)
    chart_cap_frequency(traces)
    chart_penalty_frequency(traces)
    chart_concern_family_frequency(traces)
    chart_floor_application(df, traces)
    chart_category_instability(df)
    chart_signal_hygiene_delta(df, traces)

    print("\nGenerating product waterfall examples…")
    chart_waterfall_examples(df, traces)

    print(f"\nDone. Visuals written to: {VISUAL_ROOT}")
    print(f"Data CSVs written to:     {DATA_ROOT}")
    print(f"Waterfall charts:         {WATERFALL_ROOT}")


if __name__ == "__main__":
    main()
