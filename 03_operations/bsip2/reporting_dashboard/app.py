"""
BSIP2 Reporting Dashboard  —  v2 Diagnostic Intelligence
Run:  streamlit run app.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

import streamlit as st
import pandas as pd

from data_loader import discover_runs, load_run, DIMENSION_NAMES, DIM_COLS, DIMENSION_LABELS
from viz import (
    leaderboard_fig, radar_fig, waterfall_fig,
    grade_dist_fig, nova_dist_fig, subtype_dist_fig,
    score_scatter_fig, dim_compare_bar, score_hist_fig,
    delta_bar_fig, grade_matrix_fig,
    GRADE_COLORS,
)
from anomaly_engine import build_anomaly_frame, severity_counts, SEVERITY_COLORS, SEVERITY_ORDER
from compare_engine import merge_runs, run_insights
from ui_components import (
    inject_css,
    render_product_image,
    render_run_summary,
    render_routing_trace,
    render_guardrail_panel,
    render_signal_inspector,
    render_severity_header,
    severity_badge,
    delta_html,
)

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="BSIP2 Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()


# ── Cached loaders ────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading traces…")
def cached_load(trace_root: str, bsip1_root: str) -> tuple[list, pd.DataFrame]:
    return load_run({"trace_root": trace_root, "bsip1_root": bsip1_root})


# ── Quick-view filter definitions ─────────────────────────────────────────────

def _apply_quick_view(df: pd.DataFrame, view: str) -> pd.DataFrame:
    if view == "— All Products —":
        return df
    if view == "🔴 Routing Errors":
        return df[df["cat_unstable"] == True]
    if view == "🟣 NOVA4 Products":
        return df[df["nova"] == 4]
    if view == "🔺 Floor-Masked":
        return df[(df["nova"] == 1) & (df["score"] >= 84)]
    if view == "🍬 Sweetener Products":
        return df[df["has_sweetener"] == True]
    if view == "🚫 Red Label Conflicts":
        return df[df["red_labels"] >= 1]
    if view == "⚡ High Conf / Low Score":
        return df[(df["conf_band"] == "high") & (df["score"] < 50)]
    if view == "🌿 Vanilla Cases":
        mask = ((df["nova"] == 4) &
                df["has_flavor_enh"].fillna(False) &
                ~df["has_sweetener"].fillna(False))
        return df[mask]
    if view == "📊 Capped Products":
        return df[df["binding_cap"].notna()]
    if view == "💥 Anomalous Products":
        adf = build_anomaly_frame(df)
        if adf.empty:
            return df.iloc[:0]
        pids = set(
            df[df["name_he"].isin(adf["Product"].unique())]["product_id"].tolist()
        )
        return df[df["product_id"].isin(pids)]
    return df


QUICK_VIEW_OPTIONS = [
    "— All Products —",
    "🔴 Routing Errors",
    "🟣 NOVA4 Products",
    "🔺 Floor-Masked",
    "🍬 Sweetener Products",
    "🚫 Red Label Conflicts",
    "⚡ High Conf / Low Score",
    "🌿 Vanilla Cases",
    "📊 Capped Products",
    "💥 Anomalous Products",
]


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🔬 BSIP2 Dashboard")
    st.caption("Bari · proto_v0 · diagnostic mode")
    st.divider()

    runs = discover_runs()
    if not runs:
        st.error("No BSIP2 runs found under `C:\\Bari\\02_products`.")
        st.stop()

    run_labels = [r["label"] for r in runs]
    sel_label  = st.selectbox("Run", run_labels, key="run_select")
    sel_run    = runs[run_labels.index(sel_label)]

    records, df_all = cached_load(sel_run["trace_root"], sel_run["bsip1_root"])
    st.caption(f"**{sel_run['n_products']} products** · {sel_run['category']}")

    st.divider()
    st.markdown("### ⚡ Quick Views")
    quick_view = st.selectbox(
        "Preset filter",
        QUICK_VIEW_OPTIONS,
        key="quick_view",
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Filters")

    all_grades = sorted(df_all["grade"].dropna().unique().tolist())
    f_grade = st.multiselect("Grade", all_grades, default=all_grades, key="f_grade")

    all_nova = sorted([int(n) for n in df_all["nova"].dropna().unique()])
    f_nova = st.multiselect("NOVA", all_nova, default=all_nova,
                            format_func=lambda n: f"NOVA {n}", key="f_nova")

    all_cats = sorted(df_all["category"].dropna().unique().tolist())
    f_cat = st.multiselect("Archetype", all_cats, default=all_cats, key="f_cat")

    all_sub = sorted(df_all["subtype"].dropna().unique().tolist())
    f_sub = st.multiselect("Subtype", all_sub, default=all_sub, key="f_sub")

    min_s = float(df_all["score"].min() or 0)
    max_s = float(df_all["score"].max() or 100)
    f_score = st.slider("Score range", 0, 100,
                        (max(0, int(min_s) - 1), min(100, int(max_s) + 1)),
                        key="f_score")

    f_search = st.text_input("Search name / brand", key="f_search")

    st.divider()
    st.markdown("### Flags")
    f_capped    = st.checkbox("Has binding cap", key="f_capped")
    f_unstable  = st.checkbox("Routing unstable", key="f_unstable")
    f_sweetener = st.checkbox("Contains sweetener", key="f_sweetener")


# ── Apply filters ─────────────────────────────────────────────────────────────

if quick_view != "— All Products —":
    df = _apply_quick_view(df_all, quick_view)
else:
    df = df_all.copy()
    if f_grade:    df = df[df["grade"].isin(f_grade)]
    if f_nova:     df = df[df["nova"].isin(f_nova)]
    if f_cat:      df = df[df["category"].isin(f_cat)]
    if f_sub:      df = df[df["subtype"].isin(f_sub)]
    df = df[df["score"].between(f_score[0], f_score[1], inclusive="both")]
    if f_search:
        mask = (df["name_he"].str.contains(f_search, na=False, case=False) |
                df["brand"].str.contains(f_search, na=False, case=False))
        df = df[mask]
    if f_capped:    df = df[df["binding_cap"].notna()]
    if f_unstable:  df = df[df["cat_unstable"] == True]
    if f_sweetener: df = df[df["has_sweetener"] == True]

n_shown = len(df)


# ── Helper functions ──────────────────────────────────────────────────────────

def get_record(pid: str) -> dict | None:
    for r in records:
        ref = r["trace"].get("input_reference", {})
        if ref.get("canonical_product_id") == pid:
            return r
    return None


def row_of(pid: str) -> dict:
    rows = df_all[df_all["product_id"] == pid]
    return rows.iloc[0].to_dict() if not rows.empty else {}


# ── Page header ───────────────────────────────────────────────────────────────

cat_title = sel_run["category"].replace("_", " ").title()
st.markdown(f"## BSIP2 · {cat_title}  `{sel_run['run_id']}`")

grade_order = ["S", "A", "B", "C", "D", "E"]
cols_g = st.columns(6)
for col, g in zip(cols_g, grade_order):
    cnt = int((df_all["grade"] == g).sum())
    col.metric(f"Grade {g}", cnt)

filter_note = (
    f"**Quick view:** {quick_view}" if quick_view != "— All Products —"
    else f"Showing **{n_shown}** of **{len(df_all)}** products after filters"
)
st.caption(filter_note)

# Executive summary (auto-generated insights)
insights = run_insights(df_all)
render_run_summary(insights, f"{sel_run['category']}  /  {sel_run['run_id']}")

st.divider()


# ── Tabs ──────────────────────────────────────────────────────────────────────

(tab_lb, tab_detail, tab_compare,
 tab_charts, tab_anomaly, tab_runcompare, tab_export) = st.tabs([
    "📊 Leaderboard",
    "🔍 Product Detail",
    "⚖️ Compare",
    "📈 Charts",
    "⚠️ Anomalies",
    "🔄 Run Compare",
    "📥 Export",
])


# ════════════════════════════════════════════════════════════════════
# Tab 1 — Leaderboard
# ════════════════════════════════════════════════════════════════════

with tab_lb:
    if df.empty:
        st.warning("No products match current filters.")
    else:
        st.plotly_chart(leaderboard_fig(df), width="stretch")
        st.markdown("#### Filtered table")
        disp_cols = ["name_he", "brand", "score", "grade", "category",
                     "nova", "subtype", "binding_cap", "kcal",
                     "protein_g", "sugar_g", "red_labels"]
        avail = [c for c in disp_cols if c in df.columns]
        st.dataframe(
            df[avail].rename(columns={
                "name_he": "Product", "brand": "Brand",
                "score": "Score", "grade": "Grade",
                "category": "Archetype", "nova": "NOVA",
                "subtype": "Subtype", "binding_cap": "Cap",
                "kcal": "kcal", "protein_g": "Protein",
                "sugar_g": "Sugar", "red_labels": "Red Labels",
            }).reset_index(drop=True),
            width="stretch",
            height=420,
        )


# ════════════════════════════════════════════════════════════════════
# Tab 2 — Product Detail
# ════════════════════════════════════════════════════════════════════

with tab_detail:
    if df.empty:
        st.warning("No products match current filters.")
    else:
        sorted_names = df.sort_values("score", ascending=False)["name_he"].tolist()
        sorted_pids  = df.sort_values("score", ascending=False)["product_id"].tolist()
        sel_name = st.selectbox("Select product", sorted_names, key="detail_select")
        sel_pid  = sorted_pids[sorted_names.index(sel_name)]
        row = row_of(sel_pid)
        rec = get_record(sel_pid)
        raw_trace = rec["trace"] if rec else {}

        # ── Product header ──────────────────────────────────────────
        col_img, col_info = st.columns([1, 3])
        with col_img:
            render_product_image(row.get("image_url", ""), row.get("name_he", ""))

        with col_info:
            grade = row.get("grade", "?")
            score = row.get("score", 0)
            grade_color = GRADE_COLORS.get(grade, "#888")
            st.markdown(
                f'<div class="rtl" style="font-size:1.2rem;font-weight:700;color:#ecf0f1">{sel_name}</div>'
                f'<div style="color:#7f8fa6;margin-bottom:8px">{row.get("brand","")}</div>',
                unsafe_allow_html=True,
            )
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Score", f"{score:.1f}" if pd.notna(score) else "—")
            m2.metric("Grade", grade)
            m3.metric("NOVA", str(int(row.get("nova"))) if pd.notna(row.get("nova")) else "?")
            m4.metric("Archetype", str(row.get("category", "?")))
            m5.metric("Confidence", f"{row.get('confidence', '?')}")

        st.divider()

        # ── Radar + Waterfall ────────────────────────────────────────
        col_radar, col_water = st.columns([3, 2])
        with col_radar:
            st.markdown("**Dimension scores**")
            dim_dict = {d: row.get(f"dim_{d}") for d in DIMENSION_NAMES}
            st.plotly_chart(radar_fig(dim_dict, sel_name[:35]), width="stretch")

        with col_water:
            st.markdown("**Score waterfall**")
            st.plotly_chart(waterfall_fig(row), width="stretch")

        st.divider()

        # ── Routing trace + Guardrail panels (new in v2) ─────────────
        trace_col, guard_col = st.columns(2)
        with trace_col:
            render_routing_trace(row, raw_trace)
        with guard_col:
            render_guardrail_panel(row, raw_trace)

        st.divider()

        # ── Dimension breakdown table ─────────────────────────────────
        st.markdown("**Dimension breakdown**")
        weights = raw_trace.get("dimension_weights", {}) if raw_trace else {}
        dim_rows = []
        for d in DIMENSION_NAMES:
            v = row.get(f"dim_{d}")
            w = weights.get(d, 0)
            dim_rows.append({
                "Dimension":    DIMENSION_LABELS.get(d, d),
                "Score":        round(v, 1) if pd.notna(v) else "—",
                "Weight":       f"{w:.0%}" if w else "—",
                "Contribution": round(v * w, 1) if (pd.notna(v) and w) else "—",
            })
        st.dataframe(pd.DataFrame(dim_rows), width="stretch", hide_index=True)

        st.divider()

        # ── Explanation + Flags ──────────────────────────────────────
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("**Explanation drivers**")
            for driver in (row.get("explanation", "") or "").split(" | "):
                if driver.strip():
                    st.success(driver.strip(), icon="✅")
        with col_neg:
            st.markdown("**Unresolved flags**")
            for flag in (row.get("unresolved", "") or "").split(" | "):
                if flag.strip():
                    st.warning(flag.strip(), icon="⚠️")

        st.divider()

        # ── Signal inspector (expandable trace sections) ──────────────
        render_signal_inspector(raw_trace)

        st.divider()

        # ── Nutrition + Ingredients ───────────────────────────────────
        col_n, col_i = st.columns([1, 2])
        with col_n:
            st.markdown("**Nutrition (per 100g)**")
            nutr_rows = [
                ("Energy", f"{row.get('kcal', '?')} kcal"),
                ("Fat", f"{row.get('fat_g', '?')} g"),
                ("Sat. fat", f"{row.get('sat_fat_g', '?')} g"),
                ("Sodium", f"{row.get('sodium_mg', '?')} mg"),
                ("Sugar", f"{row.get('sugar_g', '?')} g"),
                ("Fibre", f"{row.get('fiber_g', '?')} g"),
                ("Protein", f"{row.get('protein_g', '?')} g"),
                ("Ingredients", str(row.get("ing_count", "?"))),
            ]
            for label, val in nutr_rows:
                st.markdown(f"- **{label}:** {val}")

        with col_i:
            st.markdown("**Ingredients**")
            ing = row.get("ingredients_text", "") or "Not available"
            st.markdown(
                f'<div class="rtl mono" style="font-size:0.85rem;color:#c8d3e0;'
                f'background:#12151f;padding:10px;border-radius:3px;">{ing}</div>',
                unsafe_allow_html=True,
            )
            if row.get("allergens"):
                st.caption(f"⚠️ Allergens: {row['allergens']}")
            if row.get("claims"):
                st.caption(f"Claims: {row['claims']}")

        # ── Active anomalies for this product ──────────────────────────
        anomalies = build_anomaly_frame(pd.DataFrame([row]))
        if not anomalies.empty:
            st.divider()
            st.markdown("**Active anomaly flags**")
            for _, a in anomalies.iterrows():
                sev = a["Severity"]
                color = SEVERITY_COLORS.get(sev, "#888")
                st.markdown(
                    f'{severity_badge(sev)} &nbsp; <span style="color:#ecf0f1">{a["Description"]}</span>'
                    f'<br><span style="color:#7f8fa6;font-size:0.8rem">→ {a["Remediation"]}</span>',
                    unsafe_allow_html=True,
                )


# ════════════════════════════════════════════════════════════════════
# Tab 3 — Compare (two products, same run)
# ════════════════════════════════════════════════════════════════════

with tab_compare:
    st.markdown("#### Side-by-side product comparison")
    all_names_sorted = df_all.sort_values("score", ascending=False)["name_he"].tolist()
    all_pids_sorted  = df_all.sort_values("score", ascending=False)["product_id"].tolist()

    col_sel_a, col_sel_b = st.columns(2)
    with col_sel_a:
        sel_a = st.selectbox("Product A", all_names_sorted, index=0, key="cmp_a")
    with col_sel_b:
        sel_b = st.selectbox("Product B", all_names_sorted,
                             index=min(1, len(all_names_sorted) - 1), key="cmp_b")

    pid_a = all_pids_sorted[all_names_sorted.index(sel_a)]
    pid_b = all_pids_sorted[all_names_sorted.index(sel_b)]
    row_a = row_of(pid_a)
    row_b = row_of(pid_b)

    st.divider()

    ca, cb = st.columns(2)
    with ca:
        st.markdown(f'<div class="rtl" style="font-weight:700;font-size:1rem">{sel_a}</div>',
                    unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Score", f"{row_a.get('score',0):.1f}")
        m2.metric("Grade", row_a.get("grade", "?"))
        m3.metric("NOVA",  str(int(row_a.get("nova") or 0)))
        st.caption(f"Archetype: `{row_a.get('category','?')}` · Cap: `{row_a.get('binding_cap','—')}`")
    with cb:
        st.markdown(f'<div class="rtl" style="font-weight:700;font-size:1rem">{sel_b}</div>',
                    unsafe_allow_html=True)
        delta_score = float(row_b.get("score", 0) or 0) - float(row_a.get("score", 0) or 0)
        m1, m2, m3 = st.columns(3)
        m1.metric("Score", f"{row_b.get('score',0):.1f}", delta=round(delta_score, 1))
        m2.metric("Grade", row_b.get("grade", "?"))
        m3.metric("NOVA",  str(int(row_b.get("nova") or 0)))
        st.caption(f"Archetype: `{row_b.get('category','?')}` · Cap: `{row_b.get('binding_cap','—')}`")

    st.divider()

    dim_a = {d: row_a.get(f"dim_{d}") for d in DIMENSION_NAMES}
    dim_b = {d: row_b.get(f"dim_{d}") for d in DIMENSION_NAMES}
    st.plotly_chart(radar_fig(dim_a, sel_a[:30], dim_b, sel_b[:30]), width="stretch")
    st.plotly_chart(dim_compare_bar(row_a, sel_a[:25], row_b, sel_b[:25]), width="stretch")

    st.markdown("**Dimension delta (B − A)**")
    delta_rows = []
    for d in DIMENSION_NAMES:
        va = float(row_a.get(f"dim_{d}") or 0)
        vb = float(row_b.get(f"dim_{d}") or 0)
        delta_rows.append({
            "Dimension": DIMENSION_LABELS.get(d, d),
            "A": round(va, 1),
            "B": round(vb, 1),
            "Δ (B−A)": round(vb - va, 1),
        })
    st.dataframe(pd.DataFrame(delta_rows), width="stretch", hide_index=True)

    st.markdown("**Nutrition comparison**")
    nutr_fields = [
        ("kcal", "Energy (kcal)"), ("fat_g", "Fat (g)"),
        ("sat_fat_g", "Sat. fat (g)"), ("sodium_mg", "Sodium (mg)"),
        ("sugar_g", "Sugar (g)"), ("fiber_g", "Fibre (g)"), ("protein_g", "Protein (g)"),
    ]
    nutr_rows = []
    for field, label in nutr_fields:
        va = row_a.get(field)
        vb = row_b.get(field)
        nutr_rows.append({
            "Nutrient": label, "A": va, "B": vb,
            "Δ": round(float(vb or 0) - float(va or 0), 1) if pd.notna(va) and pd.notna(vb) else "—",
        })
    st.dataframe(pd.DataFrame(nutr_rows), width="stretch", hide_index=True)


# ════════════════════════════════════════════════════════════════════
# Tab 4 — Charts
# ════════════════════════════════════════════════════════════════════

with tab_charts:
    st.markdown("#### Distribution overview")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(grade_dist_fig(df), width="stretch")
    with c2:
        st.plotly_chart(nova_dist_fig(df), width="stretch")

    st.plotly_chart(score_hist_fig(df), width="stretch")

    st.divider()
    st.markdown("#### Subtype / archetype breakdown")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(subtype_dist_fig(df, "subtype", "Subtype"), width="stretch")
    with c4:
        st.plotly_chart(subtype_dist_fig(df, "category", "Archetype"), width="stretch")

    st.divider()
    st.markdown("#### Score vs nutrition")
    x_options = {
        "Protein (g)":     "protein_g",
        "Sugar (g)":       "sugar_g",
        "Sat. fat (g)":    "sat_fat_g",
        "Sodium (mg)":     "sodium_mg",
        "Energy (kcal)":   "kcal",
        "Fibre (g)":       "fiber_g",
        "Additive count":  "additive_count",
        "Ingredients":     "ing_count",
    }
    sel_x = st.selectbox("X axis", list(x_options.keys()), key="scatter_x")
    st.plotly_chart(
        score_scatter_fig(df, x_options[sel_x], x_label=sel_x),
        width="stretch",
    )


# ════════════════════════════════════════════════════════════════════
# Tab 5 — Anomalies  (severity-tiered)
# ════════════════════════════════════════════════════════════════════

with tab_anomaly:
    st.markdown("#### Anomaly detection — severity-tiered")
    st.caption(
        "Architectural violations, scoring engine edge cases, and routing failures "
        "detected automatically from BSIP2 trace data."
    )

    adf = build_anomaly_frame(df_all)
    sev_counts = severity_counts(df_all)
    render_severity_header(sev_counts)

    if adf.empty:
        st.success("No anomalies detected in current run.", icon="✅")
    else:
        # Severity filter
        show_sevs = st.multiselect(
            "Show severities",
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            key="anom_sev_filter",
        )
        adf_filtered = adf[adf["Severity"].isin(show_sevs)] if show_sevs else adf

        # Render per severity
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if sev not in show_sevs:
                continue
            sev_df = adf_filtered[adf_filtered["Severity"] == sev]
            if sev_df.empty:
                continue
            color = SEVERITY_COLORS.get(sev, "#888")
            st.markdown(
                f'<div style="margin:16px 0 6px;font-family:Consolas,monospace;'
                f'font-size:0.8rem;color:{color};font-weight:700;letter-spacing:0.1em">'
                f'── {sev} ({len(sev_df)}) ────────────────────────────</div>',
                unsafe_allow_html=True,
            )
            display_cols = ["Product", "Score", "Grade", "NOVA", "Archetype", "Code", "Description"]
            avail = [c for c in display_cols if c in sev_df.columns]
            st.dataframe(
                sev_df[avail].reset_index(drop=True),
                width="stretch",
                hide_index=True,
                height=min(200, 36 + len(sev_df) * 35),
            )

        # Remediation expandable
        with st.expander("Remediation notes"):
            for _, a in adf.drop_duplicates(subset=["Code"]).iterrows():
                if a.get("Remediation"):
                    sev = a["Severity"]
                    color = SEVERITY_COLORS.get(sev, "#888")
                    st.markdown(
                        f'<span style="color:{color};font-family:Consolas,monospace;'
                        f'font-size:0.78rem;font-weight:700">{a["Code"]}</span>  '
                        f'— {a["Remediation"]}',
                        unsafe_allow_html=True,
                    )

    st.divider()
    st.markdown("#### Cap / floor distribution")
    cap_counts = (
        df_all[df_all["binding_cap"].notna()]
        .groupby("binding_cap").size()
        .reset_index(name="count")
        .rename(columns={"binding_cap": "Cap value", "count": "Products"})
    )
    if not cap_counts.empty:
        st.dataframe(cap_counts.sort_values("Cap value"), width="stretch", hide_index=True)
    else:
        st.info("No caps applied in this run.")


# ════════════════════════════════════════════════════════════════════
# Tab 6 — Run Compare  (regression analysis between two runs)
# ════════════════════════════════════════════════════════════════════

with tab_runcompare:
    st.markdown("#### Run-to-run regression analysis")
    st.caption(
        "Compare two BSIP2 runs by canonical_product_id. "
        "Highlights products where score, grade, routing, or NOVA changed."
    )

    rc1, rc2 = st.columns(2)
    with rc1:
        run_a_label = st.selectbox("Run A (baseline)", run_labels, key="rc_run_a", index=0)
    with rc2:
        run_b_label = st.selectbox("Run B (new)", run_labels, key="rc_run_b",
                                   index=min(1, len(run_labels) - 1))

    run_a = runs[run_labels.index(run_a_label)]
    run_b = runs[run_labels.index(run_b_label)]

    if run_a_label == run_b_label:
        st.warning("Select two different runs to compare.")
    else:
        with st.spinner("Loading both runs…"):
            _, df_a = cached_load(run_a["trace_root"], run_a["bsip1_root"])
            _, df_b = cached_load(run_b["trace_root"], run_b["bsip1_root"])

        df_merged = merge_runs(df_a, df_b)
        both_mask = df_merged["score_a"].notna() & df_merged["score_b"].notna()
        n_both   = int(both_mask.sum())
        n_only_a = int((df_merged["score_a"].notna() & df_merged["score_b"].isna()).sum())
        n_only_b = int((df_merged["score_a"].isna()  & df_merged["score_b"].notna()).sum())
        n_grade  = int(df_merged.get("grade_changed",   pd.Series(dtype=bool)).sum())
        n_route  = int(df_merged.get("routing_changed", pd.Series(dtype=bool)).sum())
        n_nova   = int(df_merged.get("nova_changed",    pd.Series(dtype=bool)).sum())
        avg_d    = df_merged.loc[both_mask, "delta"].mean() if n_both else float("nan")

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Matched", n_both)
        m2.metric("Only in A", n_only_a)
        m3.metric("Only in B", n_only_b)
        m4.metric("Grade Δ", n_grade)
        m5.metric("Routing Δ", n_route)
        m6.metric("Avg score Δ", f"{avg_d:+.1f}" if pd.notna(avg_d) else "—")

        if n_both == 0:
            st.warning(
                "No shared products found. Run Compare requires runs from the **same category** "
                f"with overlapping product IDs. "
                f"Run A: {n_only_a} products. Run B: {n_only_b} products. 0 matched."
            )
        else:
            matched = df_merged[both_mask].copy()
            st.divider()

            # Delta leaderboard
            st.plotly_chart(
                delta_bar_fig(matched, run_a["run_id"], run_b["run_id"]),
                width="stretch",
            )

            # Grade movement matrix
            if "grade_a" in matched.columns and "grade_b" in matched.columns:
                st.plotly_chart(grade_matrix_fig(matched), width="stretch")

            st.divider()

            # Biggest movers
            col_imp, col_deg = st.columns(2)
            _move_cols = ["name_he", "score_a", "score_b", "delta", "grade_a", "grade_b"]
            _move_rename = {"name_he": "Product", "score_a": "Score A", "score_b": "Score B",
                            "delta": "Δ", "grade_a": "Grade A", "grade_b": "Grade B"}

            with col_imp:
                st.markdown("**⬆️ Biggest improvers**")
                avail_m = [c for c in _move_cols if c in matched.columns]
                st.dataframe(
                    matched.nlargest(10, "delta")[avail_m]
                    .rename(columns=_move_rename).reset_index(drop=True),
                    width="stretch", hide_index=True,
                )

            with col_deg:
                st.markdown("**⬇️ Biggest degraders**")
                st.dataframe(
                    matched.nsmallest(10, "delta")[avail_m]
                    .rename(columns=_move_rename).reset_index(drop=True),
                    width="stretch", hide_index=True,
                )

            st.divider()

            # Routing changes
            if n_route > 0:
                st.markdown("**Routing changes**")
                _rc = matched[matched["routing_changed"] == True]
                _rc_cols = [c for c in ["name_he","score_a","score_b","delta","category_a","category_b"] if c in _rc.columns]
                st.dataframe(
                    _rc[_rc_cols].rename(columns={
                        "name_he": "Product", "score_a": "Score A", "score_b": "Score B",
                        "delta": "Δ", "category_a": "Archetype A", "category_b": "Archetype B",
                    }).reset_index(drop=True),
                    width="stretch", hide_index=True,
                )

            # NOVA changes
            if n_nova > 0:
                st.markdown("**NOVA classification changes**")
                _nc = matched[matched["nova_changed"] == True]
                _nc_cols = [c for c in ["name_he","score_a","score_b","nova_a","nova_b","delta"] if c in _nc.columns]
                st.dataframe(
                    _nc[_nc_cols].rename(columns={
                        "name_he": "Product", "score_a": "Score A", "score_b": "Score B",
                        "nova_a": "NOVA A", "nova_b": "NOVA B", "delta": "Δ",
                    }).reset_index(drop=True),
                    width="stretch", hide_index=True,
                )

            # Cap changes
            if "cap_changed" in matched.columns and matched["cap_changed"].sum() > 0:
                st.markdown("**Cap changes**")
                _cc = matched[matched["cap_changed"] == True]
                _cc_cols = [c for c in ["name_he","score_a","score_b","binding_cap_a","binding_cap_b","delta"] if c in _cc.columns]
                st.dataframe(
                    _cc[_cc_cols].rename(columns={
                        "name_he": "Product", "score_a": "Score A", "score_b": "Score B",
                        "binding_cap_a": "Cap A", "binding_cap_b": "Cap B", "delta": "Δ",
                    }).reset_index(drop=True),
                    width="stretch", hide_index=True,
                )

            # Full table
            with st.expander("Full merged table"):
                _ft_cols = ["name_he","score_a","score_b","delta",
                            "grade_a","grade_b","category_a","category_b",
                            "nova_a","nova_b","grade_changed","routing_changed","nova_changed"]
                _ft_avail = [c for c in _ft_cols if c in matched.columns]
                st.dataframe(matched[_ft_avail].reset_index(drop=True), width="stretch", hide_index=True)


# ════════════════════════════════════════════════════════════════════
# Tab 7 — Export
# ════════════════════════════════════════════════════════════════════

with tab_export:
    st.markdown("#### Export filtered data")
    st.caption(f"Currently showing **{n_shown}** products after filters.")

    export_cols = [
        "product_id", "name_he", "brand", "barcode", "score", "grade",
        "category", "nova", "subtype", "retailer",
        "binding_cap", "caps_applied", "floors_applied",
        "kcal", "fat_g", "sat_fat_g", "sodium_mg",
        "sugar_g", "fiber_g", "protein_g", "ing_count",
        "red_labels", "has_sweetener", "has_flavor_enh", "has_whole_grain",
        "additive_count", "additive_cats",
        "confidence", "conf_band", "data_sufficiency",
        "cat_confidence", "cat_band", "cat_unstable",
        "explanation", "unresolved",
    ] + DIM_COLS
    avail_export = [c for c in export_cols if c in df.columns]
    df_export = df[avail_export].reset_index(drop=True)

    st.dataframe(df_export.head(10), width="stretch")

    @st.cache_data
    def to_csv_bytes(data: pd.DataFrame) -> bytes:
        return data.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label=f"⬇️ Download CSV ({n_shown} rows)",
        data=to_csv_bytes(df_export),
        file_name=f"bsip2_{sel_run['run_id']}_export.csv",
        mime="text/csv",
    )

    st.divider()
    st.markdown("#### Field guide")
    for field, desc in {
        "score":            "Final BSIP2 score (0–100)",
        "grade":            "S≥90  A≥80  B≥65  C≥50  D≥35  E<35",
        "nova":             "NOVA processing proxy (1=minimal · 4=ultra-processed)",
        "binding_cap":      "Guardrail ceiling that constrained the final score",
        "caps_applied":     "All guardrail cap rules that fired (semicolon-separated)",
        "floors_applied":   "Floor rules that raised the score",
        "red_labels":       "Israeli red label count (0 · 1 · 2+)",
        "explanation":      "Top score drivers (pipe-separated)",
        "unresolved":       "Outstanding quality flags",
        "dim_*":            "Per-dimension scores (0–100, weighted into 'score')",
    }.items():
        st.markdown(f"- `{field}`: {desc}")
