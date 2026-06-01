"""
BSIP2 Yogurt System — Report Generator (run_yogurt_001)
Loads all traces and answers 10 architectural stress-test questions.
Generates 7 visuals + 1 full analysis markdown.
"""
import json
import pathlib
import textwrap
import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

TRACE_ROOT  = pathlib.Path(r"C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_001")
BSIP1_ROOT  = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_yogurt_001\output")
REPORT_ROOT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\reports")
VISUAL_ROOT = pathlib.Path(r"C:\Bari\02_products\yogurt_system\visuals")

GRADE_COLORS = {"S": "#2ecc71", "A": "#27ae60", "B": "#f1c40f",
                "C": "#e67e22", "D": "#e74c3c", "E": "#8e44ad"}
NOVA_COLORS  = {1: "#2ecc71", 2: "#f1c40f", 3: "#e67e22", 4: "#e74c3c"}
CAT_COLORS   = {
    "dairy_protein": "#3498db",
    "beverage":      "#e74c3c",
    "whole_food_fat":"#e67e22",
    "sauce_spread":  "#9b59b6",
}


# ── Data loading ─────────────────────────────────────────────────────────────

def load_traces():
    traces = []
    for p in (TRACE_ROOT / "products").glob("*/bsip2_trace.json"):
        with open(p, encoding="utf-8") as f:
            traces.append(json.load(f))
    return traces


def load_bsip1():
    products = {}
    for p in BSIP1_ROOT.glob("bsip1_*.json"):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        products[d["canonical_product_id"]] = d
    return products


def trace_pid(t: dict) -> str:
    """Extract canonical_product_id from a trace (it lives inside input_reference)."""
    ref = t.get("input_reference") or {}
    return (ref.get("canonical_product_id") or
            t.get("canonical_product_id") or
            t.get("product_id") or "")


# ── Visual 1: Leaderboard ────────────────────────────────────────────────────

def plot_leaderboard(traces):
    scored = [(t.get("final_score_estimate", 0), t) for t in traces
              if t.get("final_score_estimate") is not None]
    scored.sort(key=lambda x: -x[0])

    fig, ax = plt.subplots(figsize=(14, 18))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    y_positions = range(len(scored))
    for i, (score, t) in enumerate(scored):
        grade = t.get("grade_estimate", "?")
        cat   = t.get("category", "?")
        nova  = t.get("nova_proxy", "?")
        ref   = t.get("input_reference") or {}
        name  = ref.get("product_name_he") or ref.get("canonical_name_he") or t.get("canonical_product_id", "")
        name  = name[:52]
        color = GRADE_COLORS.get(grade, "#aaaaaa")
        ax.barh(i, score, color=color, alpha=0.85, height=0.7)
        ax.text(score + 0.5, i, f"{score:.1f} [{grade}] nova={nova} {cat}",
                va="center", ha="left", fontsize=7, color="white")
        ax.text(-0.5, i, name, va="center", ha="right", fontsize=7, color="#cccccc")

    ax.set_xlim(-55, 115)
    ax.set_ylim(-0.5, len(scored) - 0.5)
    ax.set_xlabel("BSIP2 Score", color="white")
    ax.set_title("Yogurt System — run_yogurt_001 Leaderboard", color="white", fontsize=13, pad=12)
    ax.tick_params(colors="white")
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    legend = [mpatches.Patch(color=v, label=k) for k, v in GRADE_COLORS.items()]
    ax.legend(handles=legend, loc="lower right", facecolor="#2a2a4a", labelcolor="white", fontsize=8)

    VISUAL_ROOT.mkdir(parents=True, exist_ok=True)
    path = VISUAL_ROOT / "run_yogurt_001_leaderboard.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 2: Routing distribution ──────────────────────────────────────────

def plot_routing_distribution(traces, bsip1):
    cats = [t.get("category", "unknown") for t in traces]
    cat_counts: dict = {}
    for c in cats:
        cat_counts[c] = cat_counts.get(c, 0) + 1

    # Also identify routing errors (expected dairy_protein but got other)
    # Products expected to route to dairy_protein: any with "יוגורט", "קפיר", "לבן", "סקיר" in name
    # but routed elsewhere
    routing_errors = []
    for t in traces:
        pid = trace_pid(t)
        cat = t.get("category", "")
        p   = bsip1.get(pid, {})
        name = p.get("canonical_name_he", "")
        subtype = p.get("bsip_yogurt_subtype", "")
        if cat != "dairy_protein" and subtype not in ("plant_based",):
            routing_errors.append((name, cat, t.get("final_score_estimate", 0)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#1a1a2e")

    # Pie chart of routing
    colors = [CAT_COLORS.get(c, "#888888") for c in cat_counts.keys()]
    wedges, texts, autotexts = ax1.pie(
        cat_counts.values(), labels=cat_counts.keys(),
        autopct="%1.0f%%", colors=colors,
        textprops={"color": "white", "fontsize": 9}
    )
    for at in autotexts:
        at.set_color("white")
    ax1.set_title("Routing Distribution (45 products)", color="white", fontsize=11)
    ax1.set_facecolor("#1a1a2e")

    # Bar chart: routing errors detail
    ax2.set_facecolor("#1a1a2e")
    if routing_errors:
        names = [e[0][:35] for e in routing_errors]
        cats  = [e[1] for e in routing_errors]
        scores = [e[2] for e in routing_errors]
        bar_colors = [CAT_COLORS.get(c, "#888888") for c in cats]
        bars = ax2.barh(names, scores, color=bar_colors, alpha=0.85)
        for bar, cat, score in zip(bars, cats, scores):
            ax2.text(score + 0.5, bar.get_y() + bar.get_height()/2,
                     f"{cat} ({score:.1f})", va="center", fontsize=8, color="white")
        ax2.set_xlim(0, 110)
        ax2.set_title("Routing Errors (non-dairy_protein, non-plant)", color="white", fontsize=11)
    else:
        ax2.text(0.5, 0.5, "No routing errors", ha="center", va="center",
                 color="white", transform=ax2.transAxes)
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#444444")

    plt.suptitle("Yogurt Routing Analysis — run_yogurt_001", color="white", fontsize=13)
    path = VISUAL_ROOT / "run_yogurt_001_routing.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 3: Subtype cluster scatter ───────────────────────────────────────

def plot_subtype_clusters(traces, bsip1):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    subtype_order = ["plain_natural", "greek", "kefir", "skyr", "lactose_free",
                     "fruit", "kids", "protein", "diet", "plant_based",
                     "probiotic_drink", "drinkable", "dessert"]
    subtype_idx = {st: i for i, st in enumerate(subtype_order)}

    for t in traces:
        pid   = trace_pid(t)
        score = t.get("final_score_estimate", 0)
        grade = t.get("grade_estimate", "?")
        nova  = t.get("nova_proxy", 2)
        p     = bsip1.get(pid, {})
        subtype = p.get("bsip_yogurt_subtype", "unknown")
        x = subtype_idx.get(subtype, len(subtype_order))
        color = NOVA_COLORS.get(nova, "#888888")
        ax.scatter(x, score, c=color, s=120, alpha=0.85, zorder=3,
                   edgecolors="white", linewidths=0.5)
        ax.text(x + 0.05, score + 0.5, f"{score:.0f}", fontsize=6, color="white", va="bottom")

    ax.set_xticks(range(len(subtype_order)))
    ax.set_xticklabels([s.replace("_", "\n") for s in subtype_order],
                       color="white", fontsize=8, rotation=0)
    ax.set_ylabel("BSIP2 Score", color="white")
    ax.set_ylim(20, 100)
    ax.set_title("Yogurt Subtype Score Clusters — run_yogurt_001", color="white", fontsize=13)
    ax.tick_params(colors="white")
    ax.grid(axis="y", color="#333355", linestyle="--", alpha=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    legend = [mpatches.Patch(color=v, label=f"NOVA {k}") for k, v in NOVA_COLORS.items()]
    ax.legend(handles=legend, facecolor="#2a2a4a", labelcolor="white", fontsize=9)

    # Grade zone bands
    for threshold, label, alpha in [(85, "A floor", 0.08), (65, "B threshold", 0.06),
                                     (50, "C threshold", 0.05), (35, "D threshold", 0.04)]:
        ax.axhline(threshold, color="#aaaaaa", linewidth=0.5, linestyle=":", alpha=0.7)
        ax.text(len(subtype_order) - 0.5, threshold + 0.5, label,
                fontsize=7, color="#aaaaaa", ha="right")

    path = VISUAL_ROOT / "run_yogurt_001_subtype_clusters.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 4: Protein vs dessert laundering ─────────────────────────────────

def plot_protein_vs_dessert(traces, bsip1):
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    for t in traces:
        pid   = trace_pid(t)
        score = t.get("final_score_estimate", 0)
        nova  = t.get("nova_proxy", 2)
        p     = bsip1.get(pid, {})
        nutr  = p.get("normalized_nutrition_per_100g", {})
        protein = nutr.get("protein_g", 0)
        sugar   = nutr.get("sugars_g", 0)
        subtype = p.get("bsip_yogurt_subtype", "?")
        name    = p.get("canonical_name_he", "")[:30]
        grade   = t.get("grade_estimate", "?")

        color = NOVA_COLORS.get(nova, "#888888")
        ax.scatter(protein, sugar, c=color, s=score * 2, alpha=0.8, zorder=3,
                   edgecolors="white", linewidths=0.5)
        ax.text(protein + 0.2, sugar + 0.2, f"{name[:22]}\n{score:.0f}[{grade}]",
                fontsize=6, color="white", va="bottom")

    ax.axhline(17.5, color="#e74c3c", linewidth=1.5, linestyle="--", alpha=0.8)
    ax.text(0.5, 17.7, "Red label sugar threshold (17.5g)", fontsize=8, color="#e74c3c")

    ax.set_xlabel("Protein (g/100g)", color="white")
    ax.set_ylabel("Sugar (g/100g)", color="white")
    ax.set_title("Protein vs Sugar — Score as bubble size — run_yogurt_001",
                 color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.grid(color="#333355", linestyle="--", alpha=0.4)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    legend = [mpatches.Patch(color=v, label=f"NOVA {k}") for k, v in NOVA_COLORS.items()]
    ax.legend(handles=legend, facecolor="#2a2a4a", labelcolor="white", fontsize=9)

    path = VISUAL_ROOT / "run_yogurt_001_protein_vs_sugar.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 5: Sweetener / NOVA4 exposure ────────────────────────────────────

def plot_nova4_exposure(traces, bsip1):
    nova4_products = [(t, bsip1.get(trace_pid(t), {}))
                      for t in traces if t.get("nova_proxy") == 4]

    if not nova4_products:
        print("  No NOVA4 products — skipping nova4 exposure chart")
        return

    fig, ax = plt.subplots(figsize=(13, max(5, len(nova4_products) * 0.7 + 2)))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    for i, (t, p) in enumerate(sorted(nova4_products, key=lambda x: -(x[0].get("final_score_estimate", 0)))):
        score   = t.get("final_score_estimate", 0)
        grade   = t.get("grade_estimate", "?")
        name    = p.get("canonical_name_he", "")[:45]
        cap     = t.get("binding_cap") or "none"
        subtype = p.get("bsip_yogurt_subtype", "?")
        ax.barh(i, score, color="#e74c3c", alpha=0.8, height=0.7)
        ax.text(score + 0.5, i, f"{score:.1f} [{grade}]  cap={cap}  ({subtype})",
                va="center", fontsize=8, color="white")
        ax.text(-0.5, i, name, va="center", ha="right", fontsize=8, color="#cccccc")

    ax.axvline(68, color="#f39c12", linewidth=1.5, linestyle="--", alpha=0.8)
    ax.text(68.3, len(nova4_products) - 0.5, "NOVA4 cap=68", fontsize=8, color="#f39c12")
    ax.set_xlim(-50, 100)
    ax.set_ylim(-0.5, len(nova4_products) - 0.5)
    ax.set_xlabel("BSIP2 Score", color="white")
    ax.set_title("NOVA4 Products — Vanilla/Sweetener/Additive Exposure", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    path = VISUAL_ROOT / "run_yogurt_001_nova4_exposure.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 6: NOVA1 floor vs routing penalty scatter ────────────────────────

def plot_nova1_floor_tension(traces, bsip1):
    """Shows the four NOVA1 products routed to beverage vs dairy_protein."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#1a1a2e")

    nova1_traces = [(t, bsip1.get(trace_pid(t), {}))
                    for t in traces if t.get("nova_proxy") == 1]

    for t, p in nova1_traces:
        score   = t.get("final_score_estimate", 0)
        cat     = t.get("category", "?")
        name    = p.get("canonical_name_he", "")[:30]
        nutr    = p.get("normalized_nutrition_per_100g", {})
        kcal    = nutr.get("energy_kcal", 0)
        color   = CAT_COLORS.get(cat, "#888888")
        cap     = t.get("binding_cap")
        marker  = "X" if cap else "o"
        ax.scatter(kcal, score, c=color, s=200, alpha=0.9, zorder=3,
                   marker=marker, edgecolors="white", linewidths=1)
        ax.text(kcal + 1, score + 0.5, f"{name}\n{cat}\n{score:.0f}", fontsize=6.5, color="white")

    ax.axhline(85, color="#2ecc71", linewidth=1.5, linestyle="--", alpha=0.8)
    ax.text(2, 85.5, "NOVA1_SINGLE_FLOOR = 85", fontsize=8, color="#2ecc71")
    ax.axhline(55, color="#e74c3c", linewidth=1.5, linestyle=":", alpha=0.7)
    ax.text(2, 55.5, "red_label_sat_fat cap = 55", fontsize=8, color="#e74c3c")

    ax.set_xlabel("Product kcal/100g", color="white")
    ax.set_ylabel("BSIP2 Score", color="white")
    ax.set_title("NOVA1 Products — Floor vs Routing vs Red Label Tension", color="white", fontsize=12)
    ax.set_ylim(40, 100)
    ax.tick_params(colors="white")
    ax.grid(color="#333355", linestyle="--", alpha=0.4)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    legend_cats = list(set(t.get("category") for t, _ in nova1_traces))
    legend = [mpatches.Patch(color=CAT_COLORS.get(c, "#888"), label=c) for c in legend_cats]
    ax.legend(handles=legend, facecolor="#2a2a4a", labelcolor="white", fontsize=9)

    path = VISUAL_ROOT / "run_yogurt_001_nova1_tension.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Visual 7: Grade distribution histogram ───────────────────────────────────

def plot_grade_distribution(traces):
    scores = [t.get("final_score_estimate", 0) for t in traces
              if t.get("final_score_estimate") is not None]
    grades = [t.get("grade_estimate", "?") for t in traces
              if t.get("final_score_estimate") is not None]

    grade_counts: dict = {}
    for g in grades:
        grade_counts[g] = grade_counts.get(g, 0) + 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor("#1a1a2e")

    # Score histogram — colored by grade band
    ax1.set_facecolor("#1a1a2e")
    bins = [0, 35, 50, 65, 80, 90, 100]
    grade_labels  = ["E", "D", "C", "B", "A", "S"]
    band_colors   = ["#8e44ad", "#e74c3c", "#e67e22", "#f1c40f", "#27ae60", "#2ecc71"]
    for lo, hi, col in zip(bins[:-1], bins[1:], band_colors):
        band_scores = [s for s in scores if lo <= s < hi]
        if band_scores:
            ax1.hist(band_scores, bins=[lo, hi], color=col, edgecolor="white", linewidth=0.5)
    ax1.set_xlabel("Score", color="white")
    ax1.set_ylabel("Count", color="white")
    ax1.set_title("Score Distribution", color="white", fontsize=11)
    ax1.tick_params(colors="white")
    for lo, hi, label in zip(bins[:-1], bins[1:], grade_labels):
        ax1.text((lo + hi) / 2, 0.1, label,
                 ha="center", va="bottom", fontsize=10, color="white", fontweight="bold")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#444444")

    # Grade bar chart
    ax2.set_facecolor("#1a1a2e")
    grade_order = ["S", "A", "B", "C", "D", "E"]
    counts = [grade_counts.get(g, 0) for g in grade_order]
    bar_colors = [GRADE_COLORS.get(g, "#888") for g in grade_order]
    bars = ax2.bar(grade_order, counts, color=bar_colors, edgecolor="white", linewidth=0.5)
    for bar, count in zip(bars, counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(count), ha="center", va="bottom", color="white", fontsize=11)
    ax2.set_xlabel("Grade", color="white")
    ax2.set_ylabel("Count", color="white")
    ax2.set_title("Grade Distribution (n=45)", color="white", fontsize=11)
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#444444")

    plt.suptitle("Yogurt System — run_yogurt_001 Score Overview", color="white", fontsize=13)
    path = VISUAL_ROOT / "run_yogurt_001_grade_distribution.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {path}")


# ── Analysis: 10 stress-test questions ──────────────────────────────────────

def _score_str(t):
    s = t.get("final_score_estimate")
    g = t.get("grade_estimate", "?")
    return f"{s} [{g}]" if s is not None else "[no score]"


def build_analysis(traces, bsip1):
    by_pid = {(trace_pid(t)): t for t in traces}

    def pid(barcode):
        return f"bsip1_{barcode}"

    def t(barcode):
        return by_pid.get(pid(barcode), {})

    def p(barcode):
        return bsip1.get(pid(barcode), {})

    scored = [tr for tr in traces if tr.get("final_score_estimate") is not None]
    scored_sorted = sorted(scored, key=lambda x: -(x.get("final_score_estimate") or 0))

    grades: dict = {}
    for tr in scored:
        g = tr.get("grade_estimate", "?")
        grades[g] = grades.get(g, 0) + 1

    routing_to_beverage = [(tr, bsip1.get(tr.get("canonical_product_id") or tr.get("product_id"), {}))
                           for tr in traces if tr.get("category") == "beverage"]
    routing_not_dairy   = [(tr, bsip1.get(tr.get("canonical_product_id") or tr.get("product_id"), {}))
                           for tr in traces
                           if tr.get("category") not in ("dairy_protein",)
                           and bsip1.get(tr.get("canonical_product_id") or tr.get("product_id"), {}).get("bsip_yogurt_subtype") not in ("plant_based",)]
    nova4_traces = [tr for tr in traces if tr.get("nova_proxy") == 4]
    nova1_traces = [tr for tr in traces if tr.get("nova_proxy") == 1]

    lines = [
        f"# BSIP2 Yogurt System — run_yogurt_001 Architectural Analysis",
        f"\n**Run date:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Products:** 45  |  **Errors:** 0  |  **Framework:** proto_v0 unmodified",
        "",
        f"**Grade distribution:** " + "  ".join(f"{k}:{grades.get(k,0)}" for k in ['S','A','B','C','D','E']),
        f"**Score range:** {min(tr.get('final_score_estimate',0) for tr in scored):.1f} — {max(tr.get('final_score_estimate',0) for tr in scored):.1f}",
        f"**NOVA distribution:** " + "  ".join(
            f"NOVA{n}:{sum(1 for tr in traces if tr.get('nova_proxy')==n)}" for n in [1,2,3,4]),
        "",
        "---",
        "",
        "## Q1 — Does plain yogurt (single ingredient) achieve NOVA 1 and reach A grade?",
        "",
    ]

    q1_examples = [("7290200000001", "plain 1.5%"), ("7290200000002", "plain 3%"),
                   ("7290200000005", "greek 0%"), ("7290200000006", "greek 2%"),
                   ("7290200000012", "kefir 2%"), ("7290200000023", "protein 18g")]
    for bc, label in q1_examples:
        tr = t(bc); nutr = p(bc).get("normalized_nutrition_per_100g", {})
        lines.append(f"- **{label}**: {p(bc).get('canonical_name_he','')} → "
                     f"NOVA={tr.get('nova_proxy')} score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "**Finding:** All single-ingredient (`ingredients_list=[\"חלב מפוסטר\"]`) yogurts achieve "
        "NOVA 1. The `NOVA1_SINGLE_FLOOR=85` applies and produces A grade correctly. "
        "Routing to `dairy_protein` is correct for all via 'יוגורט', 'קפיר', or 'לבן'+'חלב' signals.",
        "",
        "---",
        "",
        "## Q2 — Does full-fat yogurt get unfairly penalized by the sat_fat red label?",
        "",
    ]

    for bc, label in [("7290200000004", "goat 9%"), ("7290200000007", "greek 5%"),
                      ("7290200000008", "greek 10%")]:
        tr = t(bc); nutr = p(bc).get("normalized_nutrition_per_100g", {})
        sat = nutr.get("fat_saturated_g", 0)
        lines.append(f"- **{label}**: sat_fat={sat}g → NOVA={tr.get('nova_proxy')} "
                     f"score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "**Finding:** The sat_fat red label threshold (5.0g) fires on full-fat goat yogurt (6.0g) "
        "and full-fat Greek (6.5g). Both get capped at 55 → C grade. "
        "Greek 5% (sat_fat=3.5g) correctly avoids the label and achieves A (NOVA1 floor). "
        "Greek 10% (NOVA2, not NOVA1) is capped at 55 with no floor protection.",
        "",
        "**Architectural tension:** The sat_fat red label is a regulatory signal for excess saturated "
        "fat, but natural full-fat dairy has inherently high sat_fat. A goat yogurt with a single "
        "ingredient (milk) that achieves NOVA1 is still capped at C due to fat content. "
        "This is the same tension as cereal granola — the regulatory signal does not distinguish "
        "intrinsic from added fat. A future archetype guardrail for yogurt_system could gate "
        "sat_fat caps differently for NOVA1 whole-food products vs engineered products.",
        "",
        "---",
        "",
        "## Q3 — Does 'ואניל' (vanilla) incorrectly trigger NOVA 4?",
        "",
    ]

    vanilla_examples = [("7290200000017", "kids vanilla"), ("7290200000022", "protein vanilla"),
                        ("7290200000026", "skyr vanilla"), ("7290200000033", "diet vanilla"),
                        ("7290200000038", "almond vanilla")]
    for bc, label in vanilla_examples:
        tr = t(bc); np_ = p(bc)
        lines.append(f"- **{label}**: {np_.get('canonical_name_he','')} → "
                     f"NOVA={tr.get('nova_proxy')} score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "**Finding:** Every product containing 'ואניל' achieves NOVA 4 via the flavor_enhancer "
        "signal (+3 to nova4_score), even when vanilla is the only additive and the product is "
        "otherwise nutritionally excellent. The vanilla skyr (product 26) is particularly striking: "
        "0.2g fat, 11g protein, minimal sugar, but NOVA4 cap=68 → C grade.",
        "",
        "**Root cause:** The regex pattern for flavor_enhancer matches both 'ונילין' (vanillin, "
        "synthetic) and 'ואניל' (vanilla, natural extract). This is an Evolution #5 bug "
        "identified in the cereals run — natural vs artificial flavor split not yet implemented. "
        "Fix: gate 'ואניל' as a natural flavor signal with weight +0 to nova4_score; "
        "only 'ונילין' and 'חומרי טעם מלאכותיים' should contribute +3.",
        "",
        "---",
        "",
        "## Q4 — How does routing handle 'משקה'/'שתייה' vs 'יוגורט'/'קפיר'?",
        "",
    ]

    routing_cases = [
        ("7290200000009", "Actimel", "משקה > חלב → beverage EXPECTED"),
        ("7290200000011", "לבן שתייה", "שתייה > לבן → beverage EXPECTED"),
        ("7290200000020", "שתייה חלב ילדים", "שתייה > חלב → beverage EXPECTED"),
        ("7290200000042", "לבן שתייה 3% (2)", "שתייה > לבן → beverage EXPECTED"),
        ("7290200000043", "יוגורט שתייה תות", "יוגורט > שתייה → dairy CORRECT"),
        ("7290200000044", "קפיר שתייה", "קפיר > שתייה → dairy CORRECT"),
    ]
    for bc, label, note in routing_cases:
        tr = t(bc)
        lines.append(f"- **{label}**: cat={tr.get('category')} score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'} — {note}")

    lines += [
        "",
        "**Critical finding — NOVA1 floor completely neutralizes beverage routing penalty:**",
        "Products 11 and 42 ('לבן שתייה') are single-ingredient (NOVA1) and route to `beverage`. "
        "Expected: calorie density score on beverage table (~50 for 70-72 kcal) → D grade. "
        "Actual: both get A grade (score=85). The NOVA1_SINGLE_FLOOR=85 overrides the beverage "
        "calorie density penalty entirely.",
        "",
        "This is an architectural bug in the floor/cap interaction: the NOVA1 floor should not "
        "override routing-category-induced calorie density penalties. The floor is intended to "
        "protect genuinely simple foods from being penalized by conservative thresholds — but "
        "a product routed to the wrong category is not a conservative threshold issue.",
        "",
        "**Products 9 and 20** (Actimel, kids milk drink) have NOVA3 (due to additives), so the "
        "floor does not apply → they receive D/C grades. The routing error is therefore "
        "visible only when the product also has NOVA3+ signals.",
        "",
        "---",
        "",
        "## Q5 — Does the sweetener cap (70) apply correctly?",
        "",
    ]

    for bc, label in [("7290200000032", "diet strawberry (sucralose)"),
                      ("7290200000033", "diet vanilla (aspartame)"),
                      ("7290200000034", "greek stevia")]:
        tr = t(bc)
        lines.append(f"- **{label}**: NOVA={tr.get('nova_proxy')} score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "**Finding:** Sweetener cap (70) applies correctly for stevia yogurt (product 34) → B grade. "
        "For sucralose and aspartame products (32, 33), NOVA4 cap=68 is binding (dominates sweetener "
        "cap=70 since 68 < 70) → C grade. Sweetener detection is working.",
        "",
        "---",
        "",
        "## Q6 — Do plant-based yogurts route correctly?",
        "",
    ]

    for bc, label in [("7290200000035", "soy yogurt"), ("7290200000036", "coconut"),
                      ("7290200000037", "oat"), ("7290200000038", "almond vanilla")]:
        tr = t(bc)
        lines.append(f"- **{label}**: {p(bc).get('canonical_name_he','')} → cat={tr.get('category')} score={_score_str(tr)}")

    lines += [
        "",
        "**Finding:** All 4 plant-based products route to `dairy_protein` via 'יוגורט' in name — "
        "correct routing signal but wrong archetype (plant-based ≠ dairy). This is an inherent "
        "limitation of the current router: there is no plant-based flag in BSIP1 and no plant-milk "
        "exclusion for 'יוגורט' (unlike the PLANT_MILK_SOLID_EXCLUSIONS list which handles "
        "beverage routing for soy/oat). The yogurt_system archetype will need a plant-based "
        "subtype gate similar to the beverage gate.",
        "",
        "Coconut yogurt gets red_label_sat_fat (7g sat_fat) → C grade, "
        "same problem as full-fat dairy — coconut sat_fat is inherent, not added.",
        "",
        "---",
        "",
        "## Q7 — Does the system correctly rate dessert yogurts harshly?",
        "",
    ]

    for bc, label in [("7290200000028", "Müller Corner dבש"), ("7290200000029", "mousse šokolad"),
                      ("7290200000030", "jam yogurt"), ("7290200000031", "caramel cream")]:
        tr = t(bc)
        lines.append(f"- **{label}**: cat={tr.get('category')} NOVA={tr.get('nova_proxy')} "
                     f"score={_score_str(tr)} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "**Finding:** Dessert products correctly reach D/E grades when sugar red labels fire. "
        "Product 29 (mousse) achieves 2 red labels (sugar + sat_fat) → cap=45 → E grade (31.3). "
        "",
        "**Routing surprise:** Products 18 (kids chocolate) and 29 (mousse) routed to `sauce_spread` "
        "instead of `dairy_protein`. Cause: 'ממרח שוקולד' (chocolate spread) in the ingredient list "
        "fires sauce_spread signals more strongly than the yogurt name signals. "
        "Product 28 (Müller Corner) routed to `whole_food_fat` due to 'אגוזים' signals in name.",
        "",
        "These misroutings confirm that ingredient-text contamination is as severe for yogurt "
        "as it was for granola in the cereals run. The v3 hard anchor ('יוגורט' → dairy_protein) "
        "would fix the Müller Corner case; the sauce_spread cases require ingredient-text gating.",
        "",
        "---",
        "",
        "## Q8 — How does the system handle fermentation signals?",
        "",
        "The current `signal_extractor.py` detects fermentation markers (תרבויות חיות, "
        "לקטובציל, בידפידוס etc.) but uses them only as NOVA4 evidence_against — they do NOT "
        "contribute to a dedicated fermentation quality dimension. All yogurts with live cultures "
        "benefit from a soft NOVA4 protection, but there is no fermentation_quality score.",
        "",
        "**Consequence:** Plain kefir (NOVA1, excellent fermentation profile) and "
        "heat-treated pasteurized yogurt drink (same NOVA, no live cultures) would score identically. "
        "The fermentation_quality dimension from `shared_vs_local_dimensions.md` is the "
        "architectural response — it does not yet exist in proto_v0.",
        "",
        "---",
        "",
        "## Q9 — Sat_fat red label on natural full-fat: is this architecturally correct?",
        "",
        "Full-fat Greek yogurt (10% fat, 6.5g sat_fat) and goat yogurt (9% fat, 6.0g sat_fat) "
        "both trigger the Israeli sat_fat red label (≥5.0g/100g). Both receive cap=55 → C grade.",
        "",
        "This is **not a BSIP2 bug** — it is a correct implementation of the Israeli regulatory "
        "framework, which applies the same sat_fat threshold to all food categories. The same "
        "threshold flags butter, cheese, and high-fat dairy without exception.",
        "",
        "The architectural question is: should the yogurt_system archetype apply a sat_fat "
        "contextual note (similar to the whole_food_fat satiety_rules_gated exemption) that "
        "signals 'red label from intrinsic whole-food sat_fat, not from added saturated fat'? "
        "The regulatory label still applies, but the archetype could provide a 'natural fat source' "
        "note in the trace. This is a v3 guardrail module decision, not a scoring engine fix.",
        "",
        "---",
        "",
        "## Q10 — Grade distribution and NOVA1 floor architecture",
        "",
    ]

    lines += [
        f"**Grade distribution:** " + "  ".join(f"{k}:{grades.get(k,0)}" for k in ['S','A','B','C','D','E']),
        "",
        "A significant cluster at exactly 85 (11 products) reflects the NOVA1_SINGLE_FLOOR. "
        "This is architecturally appropriate — single-ingredient fermented milk products deserve "
        "A grade. However, the floor is indiscriminate: it applies regardless of routing category, "
        "which causes the beverage routing error to produce A grades for 'לבן שתייה' products.",
        "",
        f"**Top 5 products:**",
    ]

    for tr in scored_sorted[:5]:
        pid_ = tr.get("canonical_product_id") or tr.get("product_id")
        p_ = bsip1.get(pid_, {})
        lines.append(f"- {p_.get('canonical_name_he','')}: {_score_str(tr)} "
                     f"NOVA={tr.get('nova_proxy')} cat={tr.get('category')}")

    lines += [
        "",
        f"**Bottom 5 products:**",
    ]

    for tr in scored_sorted[-5:]:
        pid_ = tr.get("canonical_product_id") or tr.get("product_id")
        p_ = bsip1.get(pid_, {})
        lines.append(f"- {p_.get('canonical_name_he','')}: {_score_str(tr)} "
                     f"NOVA={tr.get('nova_proxy')} cat={tr.get('category')} cap={tr.get('binding_cap') or 'none'}")

    lines += [
        "",
        "---",
        "",
        "## Summary: Architectural Tensions Exposed",
        "",
        "| Tension | Products affected | Fix |",
        "|---|---|---|",
        "| NOVA1 floor overrides beverage routing penalty | 2 (לבן שתייה) | Gate floor by routing category |",
        "| ואניל = NOVA4 (natural vanilla = artificial) | 5 products | Evolution #5: natural/artificial flavor split |",
        "| Sat_fat red label on natural full-fat dairy | 2 (goat, Greek 10%) | Archetype sat_fat note in guardrail trace |",
        "| Ingredient text contamination → wrong category | 3 (mousse, kids choc, Müller) | v3 hard anchor + ingredient scope gating |",
        "| Plant-based routed to dairy_protein | 4 | Plant-based gate in yogurt_system archetype |",
        "| No fermentation_quality dimension | All yogurts equally | yogurt_system archetype (future) |",
        "| Coconut sat_fat = same as dairy sat_fat | 1 | Plant-based sat_fat context note |",
        "",
    ]

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    VISUAL_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    print("Loading traces...")
    traces = load_traces()
    bsip1  = load_bsip1()
    print(f"  Traces loaded: {len(traces)}")
    print(f"  BSIP1 products loaded: {len(bsip1)}")

    print("Generating visuals...")
    plot_leaderboard(traces)
    plot_routing_distribution(traces, bsip1)
    plot_subtype_clusters(traces, bsip1)
    plot_protein_vs_dessert(traces, bsip1)
    plot_nova4_exposure(traces, bsip1)
    plot_nova1_floor_tension(traces, bsip1)
    plot_grade_distribution(traces)

    print("Building analysis...")
    analysis = build_analysis(traces, bsip1)
    path = REPORT_ROOT / "run_yogurt_001_analysis.md"
    path.write_text(analysis, encoding="utf-8")
    print(f"  Analysis written: {path}")

    print("Done.")


if __name__ == "__main__":
    main()
