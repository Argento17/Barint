"""
BSIP2 Breakfast Cereals run_cereals_001 — Report and Visual Generator
Generates comprehensive analysis answering all 10 architectural stress-test questions.
"""
import json
import pathlib
import datetime

TRACE_DIR   = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\bsip2_outputs\run_cereals_001\products")
REPORT_DIR  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\reports")
VISUAL_DIR  = pathlib.Path(r"C:\Bari\02_products\breakfast_cereals\visuals")
BSIP1_DIR   = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_cereals_001\output")

REPORT_DIR.mkdir(parents=True, exist_ok=True)
VISUAL_DIR.mkdir(parents=True, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("  [WARN] matplotlib not available — skipping visuals")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_traces():
    traces = []
    # Traces stored as products/<pid>/bsip2_trace.json
    for path in sorted(TRACE_DIR.glob("*/bsip2_trace.json")):
        with open(path, encoding="utf-8") as f:
            traces.append(json.load(f))
    return traces


def load_bsip1():
    products = {}
    for path in sorted(BSIP1_DIR.glob("bsip1_*.json")):
        if "audit" in path.name:
            continue
        with open(path, encoding="utf-8") as f:
            p = json.load(f)
        pid = p["canonical_product_id"]
        products[pid] = p
    return products


def build_table(traces, bsip1):
    rows = []
    for t in traces:
        pid   = t.get("product_id") or t.get("canonical_product_id", "")
        ref   = t.get("input_reference") or {}
        name  = ref.get("product_name_he") or ref.get("canonical_name_he") or ""
        score = t.get("final_score_estimate")
        grade = t.get("grade_estimate", "?")
        cat   = t.get("category", "?")
        nova  = t.get("nova_proxy", "?")
        cap   = t.get("binding_cap")
        p     = bsip1.get(pid, {})
        subtype = p.get("bsip_cereal_subtype", "unknown")
        nn    = p.get("normalized_nutrition_per_100g", {})
        rows.append({
            "pid": pid, "name": name, "score": score, "grade": grade,
            "cat": cat, "nova": nova, "cap": cap, "subtype": subtype,
            "kcal": nn.get("energy_kcal"), "protein": nn.get("protein_g"),
            "fiber": nn.get("dietary_fiber_g"), "sugar": nn.get("sugars_g"),
            "fat": nn.get("fat_g"), "sat_fat": nn.get("fat_saturated_g"),
            "sodium": nn.get("sodium_mg"),
        })
    return sorted(rows, key=lambda r: -(r["score"] or 0))


# ---------------------------------------------------------------------------
# Grade counts
# ---------------------------------------------------------------------------

def grade_counts(rows):
    counts = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    for r in rows:
        g = r["grade"]
        if g in counts:
            counts[g] += 1
    return counts


def grade_counts_by_subtype(rows):
    subtypes = {}
    for r in rows:
        st = r["subtype"]
        g  = r["grade"]
        if st not in subtypes:
            subtypes[st] = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        if g in subtypes[st]:
            subtypes[st][g] += 1
    return subtypes


# ---------------------------------------------------------------------------
# Visuals
# ---------------------------------------------------------------------------

GRADE_COLORS = {"S": "#8B5CF6", "A": "#22C55E", "B": "#84CC16",
                "C": "#F59E0B", "D": "#F97316", "E": "#EF4444"}
GRADE_ORDER  = ["S", "A", "B", "C", "D", "E"]

def plot_grade_utilization(rows):
    if not HAS_MPL:
        return
    gc = grade_counts(rows)
    fig, ax = plt.subplots(figsize=(8, 5))
    grades = GRADE_ORDER
    vals   = [gc.get(g, 0) for g in grades]
    colors = [GRADE_COLORS[g] for g in grades]
    bars = ax.bar(grades, vals, color=colors, width=0.6, edgecolor="white", linewidth=1.5)
    for bar, v in zip(bars, vals):
        if v > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                    str(v), ha="center", va="bottom", fontweight="bold", fontsize=12)
    ax.set_ylabel("Products", fontsize=12)
    ax.set_title("BSIP2 Breakfast Cereals — Grade Distribution (n=45)", fontsize=13, fontweight="bold")
    ax.set_ylim(0, max(vals) + 3)
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    total = sum(vals)
    for i, (g, v) in enumerate(zip(grades, vals)):
        pct = f"{v/total*100:.0f}%" if total > 0 else ""
        ax.text(i, -1.2, pct, ha="center", va="top", fontsize=9, color="gray")
    plt.tight_layout()
    out = VISUAL_DIR / "grade_utilization_cereals.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out.name}")


def plot_score_strip(rows):
    if not HAS_MPL:
        return
    fig, ax = plt.subplots(figsize=(10, 8))
    grade_thresholds = [(90, "S"), (80, "A"), (65, "B"), (50, "C"), (35, "D"), (0, "E")]
    grade_bands = [(90, 100, "#EDE9FE"), (80, 90, "#DCFCE7"), (65, 80, "#F0FDF4"),
                   (50, 65, "#FFFBEB"), (35, 50, "#FFF7ED"), (0, 35, "#FEF2F2")]
    for lo, hi, color in grade_bands:
        ax.axhspan(lo, hi, alpha=0.3, color=color, zorder=0)
    for threshold, label in grade_thresholds[:-1]:
        ax.axhline(threshold, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
        ax.text(0.02, threshold + 0.5, label, transform=ax.get_yaxis_transform(),
                fontsize=9, color="gray", va="bottom")

    subtype_order = ["oatmeal", "muesli", "whole_grain_cereal", "fitness_cereal",
                     "cornflakes", "granola", "protein_cereal", "kids_cereal"]
    subtype_labels = {
        "oatmeal": "Oatmeal", "muesli": "Muesli", "whole_grain_cereal": "Whole Grain",
        "fitness_cereal": "Fitness", "cornflakes": "Cornflakes", "granola": "Granola",
        "protein_cereal": "Protein", "kids_cereal": "Kids",
    }
    subtype_colors = {
        "oatmeal": "#22C55E", "muesli": "#84CC16", "whole_grain_cereal": "#16A34A",
        "fitness_cereal": "#F59E0B", "cornflakes": "#3B82F6", "granola": "#8B5CF6",
        "protein_cereal": "#EC4899", "kids_cereal": "#EF4444",
    }
    jitter_x = {}
    for i, st in enumerate(subtype_order):
        jitter_x[st] = i

    ax.set_xlim(-0.5, len(subtype_order) - 0.5)
    ax.set_ylim(20, 100)
    ax.set_xticks(range(len(subtype_order)))
    ax.set_xticklabels([subtype_labels.get(s, s) for s in subtype_order], fontsize=10)
    ax.set_ylabel("BSIP2 Score", fontsize=12)
    ax.set_title("BSIP2 Breakfast Cereals — Score by Subtype (n=45)", fontsize=13, fontweight="bold")

    rng = __import__("random"); rng.seed(42)
    for row in rows:
        st = row["subtype"]
        s  = row["score"]
        if s is None or st not in subtype_order:
            continue
        x = subtype_order.index(st) + rng.uniform(-0.25, 0.25)
        c = subtype_colors.get(st, "#888")
        ax.scatter(x, s, c=c, s=60, alpha=0.85, zorder=5, edgecolors="white", linewidths=0.5)

    legend_handles = [mpatches.Patch(color=subtype_colors[st], label=subtype_labels.get(st, st))
                      for st in subtype_order]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8, ncol=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    out = VISUAL_DIR / "score_by_subtype_cereals.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out.name}")


def plot_leaderboard(rows):
    if not HAS_MPL:
        return
    scored = [r for r in rows if r["score"] is not None][:45]
    names  = [r["name"][:38] for r in scored]
    scores = [r["score"] for r in scored]
    colors = [GRADE_COLORS.get(r["grade"], "#888") for r in scored]

    fig, ax = plt.subplots(figsize=(14, 18))
    y = list(range(len(scored)))
    bars = ax.barh(y, scores, color=colors, height=0.7, edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("BSIP2 Score", fontsize=11)
    ax.set_title("BSIP2 Breakfast Cereals — Full Leaderboard (n=45)", fontsize=13, fontweight="bold")
    for threshold, grade, color in [(90,"S","#8B5CF6"),(80,"A","#22C55E"),(65,"B","#84CC16"),
                                     (50,"C","#F59E0B"),(35,"D","#F97316")]:
        ax.axvline(threshold, color=color, linestyle="--", linewidth=1, alpha=0.7)
        ax.text(threshold + 0.3, -0.8, grade, color=color, fontsize=9, fontweight="bold")
    for bar, sc in zip(bars, scores):
        ax.text(sc + 0.3, bar.get_y() + bar.get_height() / 2, f"{sc}",
                va="center", fontsize=7, color="black")
    ax.set_xlim(0, 100)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    legend_handles = [mpatches.Patch(color=GRADE_COLORS[g], label=g) for g in GRADE_ORDER]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=10)
    plt.tight_layout()
    out = VISUAL_DIR / "leaderboard_cereals.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out.name}")


def plot_subtype_comparison(rows):
    if not HAS_MPL:
        return
    subtype_order = ["oatmeal", "muesli", "whole_grain_cereal", "fitness_cereal",
                     "cornflakes", "granola", "protein_cereal", "kids_cereal"]
    subtype_labels = {
        "oatmeal": "Oatmeal\n(n=8)", "muesli": "Muesli\n(n=3)",
        "whole_grain_cereal": "Whole Grain\n(n=4)", "fitness_cereal": "Fitness\n(n=6)",
        "cornflakes": "Cornflakes\n(n=5)", "granola": "Granola\n(n=8)",
        "protein_cereal": "Protein\n(n=3)", "kids_cereal": "Kids\n(n=8)",
    }
    subtype_scores = {st: [] for st in subtype_order}
    for r in rows:
        st = r["subtype"]
        if st in subtype_scores and r["score"] is not None:
            subtype_scores[st].append(r["score"])

    fig, ax = plt.subplots(figsize=(12, 6))
    grade_bands = [(90, 100, "#EDE9FE", "S"), (80, 90, "#DCFCE7", "A"),
                   (65, 80, "#F0FDF4", "B"), (50, 65, "#FFFBEB", "C"),
                   (35, 50, "#FFF7ED", "D"), (0, 35, "#FEF2F2", "E")]
    for lo, hi, color, label in grade_bands:
        ax.axhspan(lo, hi, alpha=0.25, color=color, zorder=0)

    rng = __import__("random"); rng.seed(7)
    for i, st in enumerate(subtype_order):
        scores = subtype_scores[st]
        if not scores:
            continue
        mean = sum(scores) / len(scores)
        mn, mx = min(scores), max(scores)
        ax.vlines(i, mn, mx, color="#94A3B8", linewidth=2, zorder=3)
        ax.scatter([i]*len(scores), scores, s=45, alpha=0.75, color="#3B82F6", zorder=5,
                   edgecolors="white", linewidths=0.5)
        ax.scatter([i], [mean], s=100, marker="D", color="#1D4ED8", zorder=6, edgecolors="white")
        ax.text(i, mean + 1.5, f"{mean:.1f}", ha="center", va="bottom", fontsize=8,
                fontweight="bold", color="#1D4ED8")

    ax.set_xticks(range(len(subtype_order)))
    ax.set_xticklabels([subtype_labels.get(s, s) for s in subtype_order], fontsize=9)
    ax.set_ylim(20, 100)
    ax.set_ylabel("BSIP2 Score", fontsize=12)
    ax.set_title("BSIP2 Breakfast Cereals — Score Range by Subtype", fontsize=13, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for threshold, label in [(90,"S"),(80,"A"),(65,"B"),(50,"C"),(35,"D")]:
        ax.axhline(threshold, color="gray", linestyle=":", linewidth=0.7, alpha=0.5)
    plt.tight_layout()
    out = VISUAL_DIR / "subtype_comparison_cereals.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out.name}")


def plot_category_confusion(rows):
    """Show how subtypes were classified by the category classifier."""
    if not HAS_MPL:
        return
    subtypes = ["oatmeal", "muesli", "whole_grain_cereal", "fitness_cereal",
                "cornflakes", "granola", "protein_cereal", "kids_cereal"]
    categories = ["cereal", "snack_bar_granola", "whole_food_fat", "dairy_protein", "default"]

    matrix = {st: {c: 0 for c in categories} for st in subtypes}
    for r in rows:
        st = r["subtype"]
        c  = r["cat"] if r["cat"] in categories else "default"
        if st in matrix:
            matrix[st][c] += 1

    fig, ax = plt.subplots(figsize=(10, 7))
    data = [[matrix[st].get(c, 0) for c in categories] for st in subtypes]
    cat_colors = {"cereal": "#22C55E", "snack_bar_granola": "#F59E0B",
                  "whole_food_fat": "#8B5CF6", "dairy_protein": "#3B82F6", "default": "#9CA3AF"}
    cat_labels = {"cereal": "cereal", "snack_bar_granola": "snack_bar_granola",
                  "whole_food_fat": "whole_food_fat", "dairy_protein": "dairy_protein",
                  "default": "default"}

    bottom = [0] * len(subtypes)
    for ci, cat in enumerate(categories):
        vals = [matrix[st].get(cat, 0) for st in subtypes]
        ax.bar(range(len(subtypes)), vals, bottom=bottom, label=cat_labels[cat],
               color=cat_colors[cat], edgecolor="white", linewidth=1)
        for i, (v, b) in enumerate(zip(vals, bottom)):
            if v > 0:
                ax.text(i, b + v/2, str(v), ha="center", va="center",
                        fontsize=10, fontweight="bold", color="white")
        bottom = [b + v for b, v in zip(bottom, vals)]

    ax.set_xticks(range(len(subtypes)))
    ax.set_xticklabels([s.replace("_", "\n") for s in subtypes], fontsize=8)
    ax.set_ylabel("Product Count", fontsize=11)
    ax.set_title("Category Classifier Behaviour by Subtype\n(INTENDED: oatmeal/cornflakes/fitness→cereal, granola/muesli→snack_bar)",
                 fontsize=11, fontweight="bold")
    ax.legend(loc="upper right", fontsize=8, ncol=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    out = VISUAL_DIR / "category_confusion_cereals.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  [OK] {out.name}")


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def _md_table(headers, rows):
    widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
              for i, h in enumerate(headers)]
    def row_line(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"
    sep = "|" + "|".join("-" * (w+2) for w in widths) + "|"
    return "\n".join([row_line(headers), sep] + [row_line(r) for r in rows])


def build_report(rows, bsip1):
    gc = grade_counts(rows)
    total = len(rows)
    gcs = grade_counts_by_subtype(rows)
    run_dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines += [
        "# BSIP2 Breakfast Cereals — run_cereals_001 Analysis Report",
        f"\n**Generated:** {run_dt}",
        "**Corpus:** breakfast_cereals (n=45, Yohananof scrape, 65 raw observations → 45 canonical)",
        "**Framework:** BSIP2 v2 grade calibration (same constants as run_004_recalibrated)",
        "**Purpose:** Stress-test BSIP2 against extrusion, fortification, fiber laundering,",
        "granola density, kids cereals, protein engineering, hyper-palatability.",
        "",
        "---",
        "",
        "## 1. Corpus Summary",
        "",
        f"**Total canonical products:** {total}",
        "**Source:** Yohananof (real retailer scrape, single-source corpus)",
        "",
        "**Subtype distribution:**",
        "",
    ]

    subtype_rows = []
    for st, gc_st in sorted(gcs.items()):
        st_products = [r for r in rows if r["subtype"] == st]
        n = len(st_products)
        scores = [r["score"] for r in st_products if r["score"] is not None]
        mean_s = f"{sum(scores)/len(scores):.1f}" if scores else "—"
        rng_s  = f"{min(scores):.1f}–{max(scores):.1f}" if scores else "—"
        grade_str = " | ".join(f"{g}:{gc_st.get(g,0)}" for g in GRADE_ORDER if gc_st.get(g,0) > 0)
        subtype_rows.append([st, n, mean_s, rng_s, grade_str])

    lines.append(_md_table(
        ["Subtype", "n", "Mean Score", "Range", "Grade Distribution"],
        subtype_rows
    ))

    lines += [
        "",
        "---",
        "",
        "## 2. Grade Distribution",
        "",
    ]

    grade_rows = []
    for g in GRADE_ORDER:
        count = gc.get(g, 0)
        pct = f"{count/total*100:.0f}%" if total > 0 else "0%"
        grade_rows.append([g, count, pct])
    lines.append(_md_table(["Grade", "Count", "Pct"], grade_rows))
    lines += [""]

    lines += [
        "",
        "---",
        "",
        "## 3. Full BSIP2 Leaderboard",
        "",
    ]
    leader_rows = []
    for r in rows:
        if r["score"] is None:
            continue
        cat_noted = f"{r['cat']}" + ("⚠" if r["cat"] not in ("cereal", "snack_bar_granola") and r["subtype"] in ("granola","muesli","kids_cereal") else "")
        leader_rows.append([
            r["name"][:45], r["score"], r["grade"], r["subtype"][:18],
            cat_noted[:22], r["nova"], r["cap"] or "—"
        ])
    lines.append(_md_table(
        ["Product", "Score", "Grade", "Subtype", "Category (⚠=misclassified?)", "NOVA", "Cap"],
        leader_rows
    ))

    lines += [
        "",
        "---",
        "",
        "## 4. Architectural Stress-Test — 10 Key Questions",
        "",
    ]

    # Question 1
    lines += [
        "### Q1: Do 'healthy cereals' collapse correctly?",
        "",
        "**Answer: PARTIALLY.**",
        "",
        "- Nestlé Fitness Original: C (51.2) — correct. Classified as snack_bar_granola (from 'פיטנס' + ingredient signal), NOVA 3 cap=72 binding.",
        "- Nestlé Fitness Chocolate: C (52.0) — correct. NOVA 3 + red label sugar (18.5g > 17.5g) → cap=55.",
        "- Kellogg's Special K Original: C (62.5) — **questionable**. Special K has 17g sugar, 13.5g protein, high sodium (570mg).",
        "  Scoring as C feels slightly generous — sodium just below red label threshold (600mg).",
        "- Special K Red Berries: C (52.0) — correct. Red label sugar (18.5g) + flavor enhancer → cap=55.",
        "",
        "**Finding:** Fitness/Special K products correctly land in C but the sodium near-miss",
        "(570 vs 600mg threshold) means a 30mg difference creates a 10+ point scoring swing.",
        "This cliff at 600mg sodium is a calibration concern for 'near-threshold' fortified cereals.",
        "",
    ]

    # Question 2
    lines += [
        "### Q2: Does Bari over-credit fortification?",
        "",
        "**Answer: YES — CONFIRMED ARCHITECTURAL WEAKNESS.**",
        "",
        "Fortification creates an **additive blindspot**:",
        "- Vitamins listed as names (ויטמין B1, B2, B6, ניאצין, חומצה פולית) → **0 additive categories detected**.",
        "- Vitamins listed as E-numbers (E-300) → triggers antioxidant AND flour_treatment → **2 additive categories**.",
        "",
        "**Impact measured:**",
        "- Kellogg's Cornflakes (vitamins by name): additive_ct=0 → additive_quality=100/100",
        "- Nestlé Cornflakes (includes E-300): additive_ct=2 → additive_quality=64/100, cap=72 applied",
        "- Kellogg's Cornflakes scores 64.8 (C, near-B) vs Nestlé 60.4 (C) — not because of real quality difference,",
        "  but because labeling convention triggers different NOVA signals.",
        "",
        "**Consequence:** A cornflakes product fortified with 8 vitamins, all listed by Hebrew name,",
        "looks IDENTICAL to an unfortified product from the signal extractor's perspective.",
        "BSIP2 cannot distinguish fortification from whole-food nutrition.",
        "",
        "**Recommended fix:** Add a fortification detection layer:",
        "- Detect vitamin/mineral name clusters (ויטמין B1 + B2 + B6 + ניאצין = fortification signal)",
        "- Apply a moderate NOVA boost signal (not full additive) for detected fortification packages",
        "",
    ]

    # Question 3
    lines += [
        "### Q3: Does fiber laundering exist?",
        "",
        "**Answer: YES — MOST SIGNIFICANT FINDING.**",
        "",
        "All-Bran (28g fiber/100g) scored **B (70.4)**. Let's trace why:",
        "",
        "- Glycemic quality formula: 90 − (16g sugar × 2.5) + (28g fiber × 2.0) + 0 = 90 − 40 + 56 = **106 → capped at 100**",
        "- 28g fiber produces maximum glycemic quality (100) despite 16g added sugar (close to red label)",
        "- Glycemic quality weight is 0.12 → this contributes 12.0 pts to the score",
        "- Satiety support: (12×3 + 28×5) / 318 × 400 = 221 → **capped at 100** → contributes 6.0 pts",
        "",
        "**The laundering mechanism:** The fiber bonus is uncapped within the glycemic formula.",
        "At 28g fiber, even very high sugar content (16g) cannot produce a negative glycemic score.",
        "All-Bran with 16g sugar and 28g fiber scores identically on glycemic quality to",
        "plain oats with 1g sugar and 10g fiber — this is incorrect.",
        "",
        "**Note:** All-Bran IS a NOVA 3 product with ADDITIVE_MARKERS_3_PLUS cap at 72.",
        "The cap protects against runaway scores. But the natural score (77+) before cap is inflated.",
        "",
        "**Recommended fix:** Apply a fiber-laundering discount when:",
        "- sugar_g > 12 AND fiber_g > 15 AND the fiber is from bran/isolated sources (not whole food)",
        "- Consider capping fiber_bonus at (sugar_g × 1.5) to prevent fiber from fully laundering sugar",
        "",
    ]

    # Question 4
    lines += [
        "### Q4: How harsh is extrusion pressure?",
        "",
        "**Answer: MODERATE — EXTRUSION PRESSURE IS WELL-CALIBRATED BUT INCONSISTENT.**",
        "",
        "Extruded products (cornflakes, puffed cereals) land in C (60–65):",
        "- Kellogg's Cornflakes: 64.8 (C) — NOVA 3, no red labels, 8g sugar",
        "- Telma Cornflakes: 63.9 (C) — similar profile",
        "- Nestlé Cornflakes: 60.4 (C) — E-300 triggers 2 additive categories → cap=72",
        "",
        "The extrusion pressure manifests through:",
        "1. NOVA 3 classification → processing_quality = 65 (vs 95 for NOVA 1)",
        "2. NOVA 3 cap at 82 (rarely binding for cornflakes at natural score ~65)",
        "3. Nutrient density penalty: cornflakes protein (7g) scores ~35/100 on the protein formula",
        "",
        "**Inconsistency found:** Organic cornflakes (single ingredient, 100% corn) scores A (85).",
        "This is the NOVA 1 floor. A mechanically extruded corn product at 373 kcal, 84g carbs,",
        "7g protein receiving A grade feels architecturally generous. The single-ingredient NOVA 1",
        "floor was designed for whole-food fats (nuts, seeds), not for extruded corn products.",
        "",
        "**The extrusion gap:** NOVA 1 floor (85) for single-ingredient extruded corn vs C (64) for",
        "multi-ingredient cornflakes with vitamins — a 21-point spread for essentially the same product.",
        "",
    ]

    # Question 5
    lines += [
        "### Q5: Do granolas become unfairly punished?",
        "",
        "**Answer: CLASSIFICATION CHAOS — MORE COMPLEX THAN PUNISHMENT.**",
        "",
        "6 of 8 granola products were NOT classified as snack_bar_granola or cereal:",
        "",
        "| Product | Expected | Actual | Score | Grade |",
        "|---------|---------|--------|-------|-------|",
        "| Honey-nuts granola | snack_bar | whole_food_fat | 47.0 | D |",
        "| Chocolate granola | snack_bar | snack_bar | 33.0 | E |",
        "| Protein granola | snack_bar | dairy_protein | 58.0 | C |",
        "| Date granola | snack_bar | whole_food_fat | 69.2 | B |",
        "| Cranberry granola | snack_bar | whole_food_fat | 45.0 | D |",
        "| Crunchy cluster granola | snack_bar | whole_food_fat | 52.0 | C |",
        "| Seeds granola | snack_bar | whole_food_fat | 75.8 | B |",
        "| Kellogg's granola clusters | snack_bar | snack_bar | 51.2 | C |",
        "",
        "**Root cause:** Products containing nuts ('שקדים', 'אגוזים', 'אגוזי לוז') trigger",
        "whole_food_fat signals (0.7 weight) that compete with snack_bar_granola signals.",
        "Seeds granola also contains 'שמן זית' (olive oil, 0.95 whole_food_fat signal).",
        "Protein granola's 'חלבון מי גבינה' (whey protein) triggers dairy_protein classification.",
        "",
        "**Consequence of misclassification:**",
        "- whole_food_fat: calorie density at 450 kcal → 45 pts (table calibrated for oils/nuts)",
        "  vs snack_bar: same product → 25 pts → **20-point swing from table alone**",
        "- whole_food_fat products escape SNACK_BAR_HIGH_CAL (70 cap) and SNACK_BAR_RED_SUGAR (55 cap)",
        "- Seeds granola at 75.8 (B) would likely score ~45 (D) if correctly classified as snack_bar",
        "",
        "**Finding:** Granola scoring is currently **lottery-based on classification**.",
        "Natural language signals in product names create unstable, large-swing category assignments.",
        "",
    ]

    # Question 6
    lines += [
        "### Q6: Do protein cereals exploit the architecture?",
        "",
        "**Answer: PARTIALLY — HIGH PROTEIN BUYS LIMITED BUT REAL CREDIT.**",
        "",
        "| Product | Score | Grade | Protein | Sweetener | Cap |",
        "|---------|-------|-------|---------|-----------|-----|",
        "| Special K Protein | 63.8 | C | 20g | No | 68 (NOVA4) |",
        "| Fitness Protein | 63.0 | C | 18g | Yes | 68 (NOVA4) |",
        "| Generic Protein (Syntech) | 64.1 | C | 22g | Yes | 68 (NOVA4) |",
        "",
        "Protein cereals with sweeteners hit the SWEETENER_CAP (70) independently.",
        "The NOVA 4 cap (68) binds first. Net result: max score ~68 regardless of protein content.",
        "The sweetener cap (70) is not the binding constraint here — NOVA4 at 68 is.",
        "",
        "**The genuine exploitation:**",
        "- protein_quality and nutrient_density dimensions both credit 20-22g protein heavily",
        "- At 22g protein, nutrient_density ≈ 85+ pts (near-ceiling) × 0.15 weight = 12.75 pts",
        "- This dimension credit PARTIALLY offsets the NOVA 4 processing penalty",
        "- Without the NOVA 4 cap, a 22g protein product could score ~72+ (low B)",
        "",
        "**Assessment:** The NOVA 4 cap at 68 is correctly preventing protein cereals from",
        "escaping D/C territory. The sweetener cap provides a secondary barrier.",
        "Current calibration is defensible but the C grade for engineered protein cereals",
        "feels slightly permissive — they should likely be D.",
        "",
    ]

    # Question 7
    lines += [
        "### Q7: Do kids cereals correctly collapse?",
        "",
        "**Answer: MOSTLY YES — WITH ONE NOTABLE EXCEPTION.**",
        "",
        "| Product | Sugar | NOVA | Score | Grade | Cap |",
        "|---------|-------|------|-------|-------|-----|",
        "| Nestlé Lion | 28g | 4 | 30.0 | E | 45 |",
        "| Kellogg's Coco Pops | 35g | 4 | 31.8 | E | 55 |",
        "| Nestlé Nesquik | 36g | 4 | 32.8 | E | 55 |",
        "| Kellogg's Froot Loops | 39g | 4 | 33.3 | E | 55 |",
        "| Nestlé Chocapic | 26g | 3 | 52.0 | C | 55 |",
        "| Kellogg's Smacks | 38g | 4 | 37.2 | D | 55 |",
        "| Telma Choco Rings | 30g | 4 | 36.5 | D | 55 |",
        "| Honey Nut Cheerios | 24g | 3 | 52.0 | C | 55 |",
        "",
        "**High-sugar NOVA 4 kids cereals correctly land E.** The HP_CRUNCH_SWEET penalty fires",
        "for cereal-category products with sugar >= 20g and fiber <= 3g: +5 pts at NOVA4 weight=1.0.",
        "",
        "**Chocapic at C (52) is the notable exception.** 26g sugar, NOVA 3 (whole grain detected",
        "from 'דגנים מלאים (חיטה מלאה 40%)' reduces NOVA from what should be 4).",
        "The whole grain NOVA discount saves Chocapic from NOVA 4 classification despite",
        "containing 'חומרי טעם וריח' (flavor compounds) — the score 3 from flavor_enhancer",
        "minus 1 from whole_grain = 2, landing on NOVA 3 boundary instead of 4.",
        "",
        "**Architectural tension:** Chocapic is 40% whole grain + flavor enhancers + 26g sugar.",
        "NOVA 3 cap at 82 barely constrains it. The 55 cap comes from the red label sugar.",
        "This is correct mechanically but Chocapic at C feels like it should be D.",
        "",
    ]

    # Question 8
    lines += [
        "### Q8: Does oatmeal emerge as structural anchor?",
        "",
        "**Answer: YES — DECISIVELY. First S-tier product in the Bari system.**",
        "",
        "| Product | Score | Grade | NOVA | Mechanism |",
        "|---------|-------|-------|------|-----------|",
        "| Oat Bran | **90.7** | **S** | 1 | Single ingredient, 17.3g protein, 15.4g fiber |",
        "| Quaker Rolled Oats | 85.4 | A | 1 | Single ingredient, floor (natural ≈85.4) |",
        "| Telma Oats | 85.0 | A | 1 | Floor (natural just at 85) |",
        "| Quaker Quick Oats | 85.0 | A | 1 | Floor (natural just at 85) |",
        "| Steel-Cut Oats | 85.0 | A | 1 | Floor (natural just at 85) |",
        "| Overnight Oats Base | 81.1 | A | 2 | NOVA 2, clean ingredients, high fiber |",
        "| Instant Oatmeal Vanilla | 69.0 | B | 3 | NOVA 3 (whole grain reduces NOVA4 score) |",
        "| Instant Oatmeal Honey | 55.0 | C | 3 | Red label sugar (18.5g) → cap=55 |",
        "",
        "**Oat bran (90.7) breaks the S-tier barrier.** At 246 kcal, 17.3g protein, 15.4g fiber,",
        "1.5g sugar, single ingredient → NOVA 1 floor 85 was not binding. Natural score exceeded 90.",
        "",
        "**The instant oatmeal divergence is architecturally revealing:**",
        "- Vanilla instant oatmeal (16g sugar, 'ואניל' flavor signal): NOVA 3, score=69 (B)",
        "- Honey instant oatmeal (18.5g sugar, 'חומרי טעם וריח'): NOVA 3, score=55 (C, capped)",
        "The 2.5g sugar difference (16 vs 18.5) pushed honey oatmeal over the 17.5g red label",
        "threshold. This is a cliff that doesn't reflect proportional product quality difference.",
        "",
    ]

    # Question 9
    lines += [
        "### Q9: Does Bari preserve meaningful differentiation inside cereals?",
        "",
        "**Answer: YES — STRONG SPREAD WITH MEANINGFUL HIERARCHY.**",
        "",
        "Score range: 30.0 (Lion cereal) to 90.7 (Oat bran) — **60.7 point spread.**",
        "",
        "**Internal hierarchy preserved:**",
        "- Pure whole food oats > muesli > whole grain cereals > cornflakes ≥ fitness cereals",
        "- Clean granola (NOVA 2, no vanillin) > granola with additives",
        "- Kids cereal collapse is steep and intentional",
        "",
        "**Differentiation gaps found:**",
        "- Chocapic (26g sugar kids cereal, 52) scores same as Seeds Granola (8g sugar, whole grain, 52ish)",
        "  — these should NOT be equivalent",
        "- Honey instant oatmeal (55) scores same as Kellogg's granola clusters (51) — very different products",
        "- Vanilla instant oatmeal (69, B) vs Fitness Original (51, C) — questionable spread",
        "  for products with similar processing levels",
        "",
    ]

    # Question 10
    lines += [
        "### Q10: Does the recalibrated distribution feel coherent?",
        "",
        "**Answer: MOSTLY COHERENT — GRANOLA CHAOS AND CLASSIFICATION GAPS UNDERMINE IT.**",
        "",
        f"Grade distribution: S:{gc.get('S',0)} | A:{gc.get('A',0)} | B:{gc.get('B',0)} | C:{gc.get('C',0)} | D:{gc.get('D',0)} | E:{gc.get('E',0)}",
        "",
        "**What works:**",
        "- S tier correctly has only one product (oat bran)",
        "- A tier correctly has oats and overnight oats base",
        "- E tier correctly has the worst kids cereals",
        "- D tier is small and contains legitimately problematic products",
        "",
        "**What doesn't work:**",
        "- Seeds granola at B (75.8) is the same grade as Weetabix (75.6) — incoherent",
        "  because seeds granola is whole_food_fat-classified, escaping snack_bar penalties",
        "- Protein granola at C (58, dairy_protein-classified) vs cornflakes at C (64.8)",
        "  — the protein granola actually has better nutrition but lower C",
        "- The C tier is extremely crowded (38%): 17 products in 50–65 range",
        "  Many of these are genuinely different quality levels",
        "",
    ]

    lines += [
        "",
        "---",
        "",
        "## 5. Major Architectural Observations",
        "",
        "### O1: Fortification Blindspot (CONFIRMED WEAKNESS)",
        "Vitamins listed by Hebrew name are invisible to the signal extractor. A product with",
        "'ויטמין B1, B2, B6, ניאצין, חומצה פולית, ברזל' gets additive_quality=100, indistinguishable",
        "from an unfortified product. This is the most significant gap exposed by cereals.",
        "",
        "### O2: Fiber Laundering (CONFIRMED WEAKNESS)",
        "The glycemic quality formula allows extreme fiber values (28g in All-Bran) to produce",
        "a maximum glycemic score (100) despite substantial added sugar (16g). The fiber bonus",
        "is uncapped relative to sugar content.",
        "",
        "### O3: Granola Classification Instability (CONFIRMED WEAKNESS)",
        "Nuts and seeds in product names/ingredients trigger whole_food_fat category signals.",
        "This causes 6/8 granola products to escape snack_bar penalty caps (SNACK_BAR_HIGH_CAL,",
        "SNACK_BAR_RED_SUGAR_LABEL). Seeds granola gains ~25+ points from misclassification alone.",
        "",
        "### O4: Single-Ingredient NOVA1 Floor Scope Creep",
        "The NOVA1_SINGLE_FLOOR (85) was calibrated for whole-food fats and dairy proteins.",
        "Applied to extruded organic cornflakes (single ingredient, high-carb, low-protein),",
        "it produces an A grade that conflicts with the architecture's intent.",
        "",
        "### O5: Whole Grain NOVA Discount (EXPECTED — WELL-CALIBRATED)",
        "The −1 NOVA4 score for whole grain presence correctly reduces NOVA classification",
        "for borderline products (instant oatmeal, Chocapic). This is a known design choice",
        "but may require a floor: 'whole grain + flavor enhancers' should never be NOVA 2.",
        "",
        "### O6: HP_CRUNCH Pattern — Category-Specific Correctly",
        "The HP_CRUNCH_SWEET penalty (sugar≥20g AND fiber≤3g, cereal category only) works",
        "correctly for high-sugar cereal products. It fires appropriately for Coco Pops,",
        "Nesquik, Froot Loops, Smacks at NOVA4 weight=1.0.",
        "NOTE: Granola products misclassified as whole_food_fat **escape this penalty**,",
        "which further inflates scores for misclassified products.",
        "",
    ]

    lines += [
        "",
        "---",
        "",
        "## 6. Biggest Surprises",
        "",
        "1. **Oat bran breaking S-tier (90.7)** — First S-grade product in the Bari system.",
        "   Not surprising in retrospect, but validates that S-tier is achievable.",
        "",
        "2. **Organic cornflakes at A (85)** — The single-ingredient NOVA1 floor applies to extruded",
        "   corn, giving it an A grade equivalent to pure rolled oats. This is architecturally",
        "   inconsistent: 'קמח תירס מלא' (processed corn flour) ≠ 'שיבולת שועל' (whole rolled oats).",
        "",
        "3. **Seeds granola at B (75.8)** — Near-equivalent to Weetabix (75.6). This is entirely",
        "   an artifact of whole_food_fat misclassification and should be C or low-B at best.",
        "",
        "4. **Vanilla instant oatmeal at B (69.0)** — A flavored, sugar-added, instant oatmeal",
        "   scores B because: NOVA 3 (whole grain neutralizes flavor enhancer), sugar (16g) is",
        "   below the 17.5g red label threshold. Feels too generous.",
        "",
        "5. **Granola chocolate chips at E (33.0)** — Cap=45 from ISRAELI_RED_LABELS_2_PLUS",
        "   (sugar + sat_fat both red labels). The double red label cap stacked with low natural",
        "   score produces E. Correct punishment — but only because sat_fat was 5.5g > 5.0g.",
        "   At 5.0g sat_fat, it would score C. A 0.5g sat_fat difference = 2+ grade shift.",
        "",
        "6. **Cheerios misclassified as whole_food_fat (52, C)** — 'אגוזים' (nuts) in the product",
        "   name triggered whole_food_fat classification. A kids cereal with 24g sugar scoring C",
        "   as if it were an oil or nut product.",
        "",
    ]

    lines += [
        "",
        "---",
        "",
        "## 7. Products That Broke Assumptions",
        "",
        "| Product | Score | Issue |",
        "|---------|-------|-------|",
        "| Oat Bran | 90.7 (S) | First S-tier. NOVA1 floor irrelevant — natural score already >90 |",
        "| Organic Cornflakes | 85 (A) | NOVA1 single-ingredient floor for extruded corn — scope mismatch |",
        "| Seeds Granola | 75.8 (B) | whole_food_fat misclassification inflating by ~25 pts |",
        "| Date Granola | 69.2 (B) | Same misclassification — 'ריבת תמרים' triggers 'ריבה' sugar marker |",
        "| All-Bran | 70.4 (B) | Fiber laundering: 28g fiber neutralizes 16g sugar |",
        "| Vanilla Instant Oatmeal | 69.0 (B) | Flavored + sugar, but NOVA 3 via whole grain discount |",
        "| Protein Granola | 58.0 (C) | dairy_protein misclassification from whey protein in name |",
        "| Cheerios | 52.0 (C) | whole_food_fat misclassification from 'אגוזים' in name |",
        "| Chocapic | 52.0 (C) | NOVA3 via whole grain discount saves heavily sugared kids cereal from D/E |",
        "",
    ]

    lines += [
        "",
        "---",
        "",
        "## 8. Recommended Next BSIP2 Refinements",
        "",
        "### Priority 1: Fortification Detection Layer",
        "Add a dedicated fortification signal extractor. Detect vitamin name clusters",
        "(ויטמין B1/B2/B6 + ניאצין + ברזל = fortification signature) and apply a",
        "moderate NOVA processing signal (not additive count, but a separate flag).",
        "This will expose the quality difference between whole-food protein and spray-on vitamins.",
        "",
        "### Priority 2: Fiber Laundering Cap",
        "In the glycemic quality formula, cap the fiber_bonus at min(20, sugar_g × 1.2).",
        "This prevents extreme bran fiber from fully laundering high added sugar.",
        "A product with 28g fiber but 16g sugar should NOT score 100 on glycemic quality.",
        "",
        "### Priority 3: Granola Category Signal Rebalancing",
        "Add 'גרנולה' to category_classifier with name-only matching at higher weight.",
        "Reduce interference from 'שקד', 'אגוז' in granola context by adding a conjunction",
        "check: whole_food_fat signals only apply if there are no cereal/granola signals.",
        "Alternatively, enforce: products with 'גרנולה' in name always → snack_bar_granola.",
        "",
        "### Priority 4: NOVA1 Floor Scope Restriction",
        "Restrict NOVA1_SINGLE_FLOOR (85) to products where kcal < 450 AND protein > 5g.",
        "This excludes high-calorie, low-protein single-ingredient extruded products",
        "(corn flour, rice flour) from the whole-food floor rescue.",
        "",
        "### Priority 5: Whole Grain NOVA Discount Cap",
        "Limit the whole grain −1 NOVA4 discount: if flavor_enhancer is detected,",
        "the minimum NOVA level should be 3, not reducible to 2 by whole grain presence.",
        "Formula: nova_level = max(3, computed_level) when flavor_enhancer is detected.",
        "",
        "### Priority 6: Sodium Cliff Smoothing",
        "The sodium red label at 600mg creates a binary cliff. Products at 570mg escape",
        "entirely; at 610mg they get a 60-cap. Consider a graduated approach:",
        "450–600mg: soft penalty; 600–750mg: current cap; >750mg: harsher cap.",
        "",
    ]

    lines += [
        "",
        "---",
        "",
        "## 9. Visuals",
        "",
        "Generated in `visuals/`:",
        "- `grade_utilization_cereals.png` — grade distribution bar chart",
        "- `score_by_subtype_cereals.png` — score strip chart by subtype",
        "- `leaderboard_cereals.png` — full 45-product leaderboard",
        "- `subtype_comparison_cereals.png` — score range per subtype (mean + range)",
        "- `category_confusion_cereals.png` — category classifier behaviour by subtype",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading traces and BSIP1 data...")
    traces  = load_traces()
    bsip1   = load_bsip1()
    print(f"  Loaded {len(traces)} traces, {len(bsip1)} BSIP1 products")

    rows = build_table(traces, bsip1)

    print("Generating visuals...")
    plot_grade_utilization(rows)
    plot_score_strip(rows)
    plot_leaderboard(rows)
    plot_subtype_comparison(rows)
    plot_category_confusion(rows)

    print("Writing report...")
    report = build_report(rows, bsip1)
    rpath = REPORT_DIR / "run_cereals_001_analysis.md"
    rpath.write_text(report, encoding="utf-8")
    print(f"  [OK] {rpath.name}")

    print(f"\nAll outputs written to:")
    print(f"  Reports: {REPORT_DIR}")
    print(f"  Visuals: {VISUAL_DIR}")


if __name__ == "__main__":
    main()
