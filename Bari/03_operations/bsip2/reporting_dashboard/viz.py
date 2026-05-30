"""
BSIP2 Dashboard — Visualization Layer
All Plotly figure factories. No Streamlit imports here.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data_loader import DIMENSION_NAMES, DIM_COLS, DIMENSION_LABELS

# ── Palette ────────────────────────────────────────────────────────────────

GRADE_COLORS = {
    "S": "#2ecc71", "A": "#27ae60", "B": "#f1c40f",
    "C": "#e67e22", "D": "#e74c3c", "E": "#8e44ad", "?": "#888888",
}
NOVA_COLORS = {
    1: "#2ecc71", 2: "#f1c40f", 3: "#e67e22", 4: "#e74c3c",
}
BG = "#0e1117"         # Streamlit dark background
CARD_BG = "#1c1f2b"


def _grade_color(g):
    return GRADE_COLORS.get(str(g), "#888888")


def _nova_color(n):
    return NOVA_COLORS.get(int(n) if pd.notna(n) else 0, "#888888")


# ── 1. Leaderboard ─────────────────────────────────────────────────────────

def leaderboard_fig(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    d = df.dropna(subset=["score"]).sort_values("score", ascending=True)
    colors = [_grade_color(g) for g in d["grade"]]
    fig = go.Figure(go.Bar(
        y=d["name_he"],
        x=d["score"],
        orientation="h",
        marker_color=colors,
        marker_line_color="rgba(255,255,255,0.15)",
        marker_line_width=0.5,
        text=[f"{s:.1f} [{g}]" for s, g in zip(d["score"], d["grade"])],
        textposition="outside",
        textfont_size=10,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Score: %{x:.1f}<br>"
            "NOVA: %{customdata[0]}<br>"
            "Archetype: %{customdata[1]}<br>"
            "Cap: %{customdata[2]}<extra></extra>"
        ),
        customdata=list(zip(
            d["nova"].fillna("?"),
            d["category"].fillna("?"),
            d["binding_cap"].fillna("none"),
        )),
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=max(350, len(d) * 26 + 80),
        margin=dict(l=10, r=80, t=20, b=20),
        xaxis=dict(range=[0, 110], showgrid=True, gridcolor="#2a2a3a",
                   color="white", title=""),
        yaxis=dict(showgrid=False, color="white", title="",
                   tickfont=dict(size=11)),
        font_color="white",
        showlegend=False,
    )
    return fig


# ── 2. Radar / Spider ──────────────────────────────────────────────────────

def radar_fig(
    dim_dict_a: dict, label_a: str,
    dim_dict_b: dict | None = None, label_b: str | None = None,
) -> go.Figure:
    cats = [DIMENSION_LABELS.get(d, d) for d in DIMENSION_NAMES] + [DIMENSION_LABELS.get(DIMENSION_NAMES[0], DIMENSION_NAMES[0])]
    vals_a = [dim_dict_a.get(d, 0) or 0 for d in DIMENSION_NAMES]
    vals_a = vals_a + [vals_a[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_a, theta=cats,
        fill="toself", name=label_a,
        line_color="#3498db", fillcolor="rgba(52,152,219,0.25)",
    ))
    if dim_dict_b is not None:
        vals_b = [dim_dict_b.get(d, 0) or 0 for d in DIMENSION_NAMES]
        vals_b = vals_b + [vals_b[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals_b, theta=cats,
            fill="toself", name=label_b or "B",
            line_color="#e67e22", fillcolor="rgba(230,126,34,0.20)",
        ))
    fig.update_layout(
        polar=dict(
            bgcolor=CARD_BG,
            radialaxis=dict(visible=True, range=[0, 100], color="white",
                            gridcolor="#333355", tickfont=dict(size=9)),
            angularaxis=dict(color="white", gridcolor="#333355",
                             tickfont=dict(size=10)),
        ),
        paper_bgcolor=BG,
        font_color="white",
        showlegend=dim_dict_b is not None,
        legend=dict(bgcolor="#1c1f2b", bordercolor="#444"),
        margin=dict(l=60, r=60, t=40, b=40),
        height=380,
    )
    return fig


# ── 3. Score Waterfall ─────────────────────────────────────────────────────

def waterfall_fig(row: dict) -> go.Figure:
    w  = row.get("weighted_score") or 0
    ac = row.get("score_after_cap")
    ap = row.get("score_after_penalty")
    af = row.get("score_after_floors")
    fs = row.get("score") or 0

    # Build steps
    steps_x = ["Weighted"]
    steps_y = [w]
    steps_measure = ["absolute"]
    steps_color = ["#3498db"]

    if ac is not None and abs(ac - w) > 0.01:
        steps_x.append("Cap")
        steps_y.append(ac - w)
        steps_measure.append("relative")
        steps_color.append("#e74c3c" if ac < w else "#2ecc71")

    if ap is not None and ac is not None and abs(ap - ac) > 0.01:
        steps_x.append("Penalty")
        steps_y.append(ap - ac)
        steps_measure.append("relative")
        steps_color.append("#e74c3c")

    if af is not None:
        prev = ap if ap is not None else (ac if ac is not None else w)
        if abs(af - prev) > 0.01:
            steps_x.append("Floor")
            steps_y.append(af - prev)
            steps_measure.append("relative")
            steps_color.append("#2ecc71")

    steps_x.append("Final")
    steps_y.append(fs)
    steps_measure.append("absolute")
    steps_color.append(_grade_color(row.get("grade", "?")))

    fig = go.Figure(go.Waterfall(
        x=steps_x, y=steps_y, measure=steps_measure,
        connector=dict(line=dict(color="#444466", dash="dot")),
        decreasing=dict(marker_color="#e74c3c"),
        increasing=dict(marker_color="#2ecc71"),
        totals=dict(marker_color=_grade_color(row.get("grade", "?"))),
        texttemplate="%{y:.1f}",
        textfont_color="white",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=CARD_BG,
        height=280, margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(color="white", showgrid=False),
        yaxis=dict(color="white", range=[0, 105], gridcolor="#2a2a3a"),
        font_color="white",
        showlegend=False,
    )
    return fig


# ── 4. Grade Distribution ──────────────────────────────────────────────────

def grade_dist_fig(df: pd.DataFrame) -> go.Figure:
    order = ["S", "A", "B", "C", "D", "E"]
    counts = df["grade"].value_counts().reindex(order, fill_value=0)
    fig = go.Figure(go.Bar(
        x=counts.index,
        y=counts.values,
        marker_color=[_grade_color(g) for g in counts.index],
        marker_line_color="rgba(255,255,255,0.15)",
        text=counts.values,
        textposition="outside",
        textfont_color="white",
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=300, margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(color="white", title="", showgrid=False),
        yaxis=dict(color="white", title="Count", gridcolor="#2a2a3a"),
        font_color="white", showlegend=False,
        title_text="Grade Distribution", title_font_color="white",
    )
    return fig


# ── 5. NOVA Distribution ───────────────────────────────────────────────────

def nova_dist_fig(df: pd.DataFrame) -> go.Figure:
    counts = df["nova"].dropna().astype(int).value_counts().sort_index()
    fig = go.Figure(go.Pie(
        labels=[f"NOVA {n}" for n in counts.index],
        values=counts.values,
        marker_colors=[_nova_color(n) for n in counts.index],
        hole=0.4,
        textinfo="label+percent",
        textfont_color="white",
    ))
    fig.update_layout(
        paper_bgcolor=BG,
        height=300, margin=dict(l=20, r=20, t=40, b=20),
        font_color="white",
        title_text="NOVA Distribution", title_font_color="white",
        legend=dict(bgcolor="#1c1f2b", font_color="white"),
    )
    return fig


# ── 6. Subtype / Archetype Distribution ───────────────────────────────────

def subtype_dist_fig(df: pd.DataFrame, col: str = "subtype", title: str = "Subtype") -> go.Figure:
    counts = df[col].fillna("—").value_counts()
    medians = df.groupby(col)["score"].median().reindex(counts.index)
    colors = [
        _grade_color("A") if (m >= 80) else
        _grade_color("B") if (m >= 65) else
        _grade_color("C") if (m >= 50) else
        _grade_color("D")
        for m in medians.fillna(50)
    ]
    fig = go.Figure(go.Bar(
        x=counts.index,
        y=counts.values,
        marker_color=colors,
        text=counts.values,
        textposition="outside",
        textfont_color="white",
        hovertemplate="<b>%{x}</b><br>Count: %{y}<br>Median score: %{customdata:.1f}<extra></extra>",
        customdata=medians.fillna(0).values,
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=300, margin=dict(l=20, r=20, t=40, b=60),
        xaxis=dict(color="white", title="", tickangle=-30, showgrid=False),
        yaxis=dict(color="white", title="Count", gridcolor="#2a2a3a"),
        font_color="white", showlegend=False,
        title_text=f"{title} Distribution (color = median grade)",
        title_font_color="white",
    )
    return fig


# ── 7. Scatter – Score vs Nutrition ───────────────────────────────────────

def score_scatter_fig(df: pd.DataFrame, x_col: str, y_col: str = "score",
                      x_label: str | None = None) -> go.Figure:
    d = df.dropna(subset=[x_col, y_col])
    if d.empty:
        return go.Figure()
    fig = px.scatter(
        d, x=x_col, y=y_col,
        color="grade",
        color_discrete_map=GRADE_COLORS,
        hover_name="name_he",
        hover_data={"nova": True, "category": True, x_col: ":.1f", y_col: ":.1f"},
        labels={x_col: x_label or x_col, y_col: "Score"},
    )
    fig.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.5, color="white")))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=CARD_BG,
        height=340, margin=dict(l=30, r=20, t=20, b=40),
        xaxis=dict(color="white", gridcolor="#2a2a3a"),
        yaxis=dict(color="white", range=[0, 105], gridcolor="#2a2a3a"),
        font_color="white",
        legend=dict(bgcolor="#1c1f2b", font_color="white", title_text="Grade"),
    )
    return fig


# ── 8. Dimension comparison bar (side-by-side) ────────────────────────────

def dim_compare_bar(row_a: dict, label_a: str,
                    row_b: dict, label_b: str) -> go.Figure:
    labels  = [DIMENSION_LABELS.get(d, d) for d in DIMENSION_NAMES]
    vals_a  = [row_a.get(f"dim_{d}") or 0 for d in DIMENSION_NAMES]
    vals_b  = [row_b.get(f"dim_{d}") or 0 for d in DIMENSION_NAMES]
    deltas  = [b - a for a, b in zip(vals_a, vals_b)]

    fig = go.Figure()
    fig.add_trace(go.Bar(name=label_a[:30], x=labels, y=vals_a,
                         marker_color="#3498db", opacity=0.85))
    fig.add_trace(go.Bar(name=label_b[:30], x=labels, y=vals_b,
                         marker_color="#e67e22", opacity=0.85))
    fig.update_layout(
        barmode="group",
        paper_bgcolor=BG, plot_bgcolor=CARD_BG,
        height=340, margin=dict(l=20, r=20, t=20, b=60),
        xaxis=dict(color="white", tickangle=-30, showgrid=False),
        yaxis=dict(color="white", range=[0, 110], gridcolor="#2a2a3a", title="Score"),
        font_color="white",
        legend=dict(bgcolor="#1c1f2b", font_color="white"),
    )
    return fig


# ── 9. Score histogram ────────────────────────────────────────────────────

def score_hist_fig(df: pd.DataFrame) -> go.Figure:
    d = df.dropna(subset=["score"])
    fig = go.Figure()
    bins  = [0, 35, 50, 65, 80, 90, 100]
    grade_labels = ["E", "D", "C", "B", "A", "S"]
    for lo, hi, gl in zip(bins[:-1], bins[1:], grade_labels):
        band = d[(d["score"] >= lo) & (d["score"] < hi)]
        if not band.empty:
            fig.add_trace(go.Histogram(
                x=band["score"], name=f"Grade {gl}",
                marker_color=_grade_color(gl),
                xbins=dict(start=lo, end=hi, size=5),
                opacity=0.85, showlegend=True,
            ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor=BG, plot_bgcolor=CARD_BG,
        height=300, margin=dict(l=20, r=20, t=20, b=40),
        xaxis=dict(color="white", range=[0, 105], showgrid=False,
                   title="Score"),
        yaxis=dict(color="white", gridcolor="#2a2a3a", title="Products"),
        font_color="white",
        legend=dict(bgcolor="#1c1f2b", font_color="white"),
    )
    return fig


# ── 10. Run delta bar ─────────────────────────────────────────────────────────

def delta_bar_fig(
    df_merged: pd.DataFrame,
    run_a_id: str = "Run A",
    run_b_id: str = "Run B",
) -> go.Figure:
    d = df_merged.dropna(subset=["delta", "name_he"]).sort_values("delta")
    colors = ["#e74c3c" if v < 0 else "#2ecc71" if v > 0 else "#555" for v in d["delta"]]
    changed_marker = [
        "★" if bool(row.get("grade_changed")) or bool(row.get("routing_changed")) else ""
        for _, row in d.iterrows()
    ]

    fig = go.Figure(go.Bar(
        y=d["name_he"],
        x=d["delta"],
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:+.1f}{m}" for v, m in zip(d["delta"], changed_marker)],
        textposition="outside",
        textfont=dict(size=10, color="white"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"Score {run_a_id}: " + "%{customdata[0]:.1f}<br>"
            f"Score {run_b_id}: " + "%{customdata[1]:.1f}<br>"
            "Δ: %{x:+.1f}"
            "<extra></extra>"
        ),
        customdata=list(zip(
            pd.to_numeric(d.get("score_a", pd.Series(dtype=float)), errors="coerce").fillna(0),
            pd.to_numeric(d.get("score_b", pd.Series(dtype=float)), errors="coerce").fillna(0),
        )),
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        height=max(350, len(d) * 24 + 80),
        margin=dict(l=10, r=70, t=30, b=20),
        xaxis=dict(color="white", zeroline=True, zerolinecolor="#444", showgrid=True,
                   gridcolor="#2a2a3a", title="Score delta (B − A)"),
        yaxis=dict(color="white", showgrid=False, tickfont=dict(size=10)),
        font_color="white",
        showlegend=False,
        title_text=f"Score delta: {run_b_id} − {run_a_id}  (★ = grade/routing changed)",
        title_font_color="#aaa",
        title_font_size=12,
    )
    return fig


# ── 11. Grade movement matrix ─────────────────────────────────────────────────

def grade_matrix_fig(df_merged: pd.DataFrame) -> go.Figure:
    order = ["S", "A", "B", "C", "D", "E"]
    g_a = df_merged["grade_a"].fillna("?") if "grade_a" in df_merged else pd.Series(dtype=str)
    g_b = df_merged["grade_b"].fillna("?") if "grade_b" in df_merged else pd.Series(dtype=str)

    all_grades = [g for g in order if g in g_a.values or g in g_b.values]
    if not all_grades:
        return go.Figure()

    mat = pd.crosstab(g_a, g_b).reindex(index=all_grades, columns=all_grades, fill_value=0)
    z = mat.values.tolist()
    text = [[str(v) if v > 0 else "" for v in row] for row in z]

    # Diagonal = maintained; above diagonal = improved; below = degraded
    color_z = []
    for ri, row_vals in enumerate(z):
        color_row = []
        for ci, v in enumerate(row_vals):
            if v == 0:
                color_row.append(0)
            elif ri == ci:
                color_row.append(2)   # maintained
            elif ri > ci:
                color_row.append(3)   # improved (lower row = worse old grade)
            else:
                color_row.append(1)   # degraded
        color_z.append(color_row)

    colorscale = [
        [0.00, "#0e1117"],  # 0 = empty
        [0.34, "#1a3a5c"],  # 1 = degraded
        [0.67, "#1c2b1c"],  # 2 = maintained
        [1.00, "#1a4a1a"],  # 3 = improved
    ]

    fig = go.Figure(go.Heatmap(
        z=color_z,
        x=list(mat.columns),
        y=list(mat.index),
        colorscale=colorscale,
        showscale=False,
        text=text,
        texttemplate="%{text}",
        textfont=dict(color="white", size=14),
        hovertemplate="Old grade %{y} → New grade %{x}: %{text} products<extra></extra>",
        zmin=0, zmax=3,
    ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=CARD_BG,
        height=340,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(color="white", title="New grade (Run B)", side="top",
                   showgrid=False, tickfont=dict(size=14, family="Consolas")),
        yaxis=dict(color="white", title="Old grade (Run A)", autorange="reversed",
                   showgrid=False, tickfont=dict(size=14, family="Consolas")),
        font_color="white",
        title_text="Grade movement matrix",
        title_font_color="#aaa",
        title_font_size=12,
    )
    return fig
