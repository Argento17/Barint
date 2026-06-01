"""
BSIP2 Dashboard — UI Components
Reusable Streamlit rendering functions. No data logic here.
"""
import streamlit as st
import pandas as pd
from anomaly_engine import SEVERITY_COLORS, SEVERITY_TEXT_COLORS

# ── CSS ────────────────────────────────────────────────────────────────────────

DASHBOARD_CSS = """
<style>
/* ── Rule trace cards ──────────────────────────────────── */
.rule-card {
    background: #12151f;
    border-left: 3px solid #3498db;
    padding: 8px 14px;
    margin: 3px 0;
    font-size: 0.83rem;
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    line-height: 1.5;
}
.rule-card.cap   { border-left-color: #e74c3c; }
.rule-card.floor { border-left-color: #2ecc71; }
.rule-card.info  { border-left-color: #3498db; }
.rule-card .label {
    color: #7f8fa6; font-size: 0.74rem;
    text-transform: uppercase; letter-spacing: 0.06em;
}
.rule-card .val   { color: #ecf0f1; font-weight: 600; }
.rule-card .note  { color: #95a5a6; font-size: 0.78rem; margin-top: 2px; }

/* ── Severity badges ────────────────────────────────────── */
.sev {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 2px;
    font-size: 0.70rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    letter-spacing: 0.08em;
}
.sev-CRITICAL { background:#c0392b; color:#fff; }
.sev-HIGH     { background:#e67e22; color:#fff; }
.sev-MEDIUM   { background:#b7950b; color:#fff; }
.sev-LOW      { background:#1a5276; color:#aac8e8; }

/* ── Insight chips ──────────────────────────────────────── */
.chip {
    display: inline-block;
    background: #1c1f2b;
    border: 1px solid #2a2d3e;
    border-radius: 2px;
    padding: 3px 10px;
    margin: 2px 3px;
    font-size: 0.79rem;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    color: #c8d3e0;
}
.chip.warn { border-color:#e67e22; color:#f0a000; }
.chip.bad  { border-color:#c0392b; color:#e55; }
.chip.good { border-color:#27ae60; color:#2ecc71; }
.chip.info { border-color:#3498db; color:#7fbbff; }

/* ── Routing trace panel ────────────────────────────────── */
.routing-panel {
    background: #12151f;
    border: 1px solid #1e2338;
    border-radius: 3px;
    padding: 12px 16px;
    margin: 4px 0;
    font-size: 0.84rem;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
}
.routing-panel .rl { color:#7f8fa6; font-size:0.74rem; text-transform:uppercase; letter-spacing:0.06em; }
.routing-panel .rv { color:#ecf0f1; font-weight:600; }
.routing-panel .rsig { color:#95a5a6; margin-top:6px; font-size:0.79rem; }

/* ── Delta colors ───────────────────────────────────────── */
.dpos { color:#2ecc71; font-weight:700; }
.dneg { color:#e74c3c; font-weight:700; }
.dzero{ color:#7f8fa6; }

/* ── Tabs ───────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { gap: 3px; }
.stTabs [data-baseweb="tab"] { padding: 5px 13px; font-size: 0.86rem; }

/* ── Grade pill ─────────────────────────────────────────── */
.grade-pill {
    display: inline-block;
    padding: 3px 14px;
    border-radius: 2px;
    font-weight: 800;
    font-size: 1.1rem;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
}

/* ── Product placeholder ────────────────────────────────── */
.img-placeholder {
    background: #1c1f2b;
    border: 1px solid #2a2d3e;
    border-radius: 4px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #555;
    font-size: 2.2rem;
}

/* ── Metric card ────────────────────────────────────────── */
.metric-card {
    background: #1c1f2b;
    border: 1px solid #1e2338;
    border-radius: 3px;
    padding: 10px 14px;
    margin: 3px 0;
}

/* ── RTL text ───────────────────────────────────────────── */
.rtl { direction: rtl; text-align: right; }

/* ── Code-style values ──────────────────────────────────── */
.mono { font-family: 'JetBrains Mono', 'Consolas', monospace; }

/* ── Section header ─────────────────────────────────────── */
.section-header {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #7f8fa6;
    border-bottom: 1px solid #1e2338;
    padding-bottom: 4px;
    margin: 12px 0 8px 0;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
}

/* ── Divider ─────────────────────────────────────────────── */
hr { border-color: #1e2338 !important; margin: 10px 0 !important; }
</style>
"""


def inject_css() -> None:
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


# ── Badges & pills ────────────────────────────────────────────────────────────

def severity_badge(severity: str) -> str:
    cls = f"sev sev-{severity}"
    return f'<span class="{cls}">{severity}</span>'


def grade_pill_html(grade: str, color: str) -> str:
    return (f'<span class="grade-pill" '
            f'style="background:{color};color:{"#fff" if grade in "SDCE" else "#000"}">'
            f'{grade}</span>')


def delta_html(val: float | None) -> str:
    if val is None or pd.isna(val):
        return '<span class="dzero">—</span>'
    if val > 0:
        return f'<span class="dpos">+{val:.1f}</span>'
    if val < 0:
        return f'<span class="dneg">{val:.1f}</span>'
    return f'<span class="dzero">0.0</span>'


# ── Product image ─────────────────────────────────────────────────────────────

def render_product_image(url: str, name: str, width: int = 140) -> None:
    if url and url.startswith("http"):
        try:
            st.image(url, width=width)
        except Exception:
            _render_placeholder(name)
    else:
        _render_placeholder(name)


def _render_placeholder(name: str) -> None:
    icon = "🧀" if "יוגורט" in name or "חלב" in name else "🌾" if "דגני" in name else "🥫"
    st.markdown(f'<div class="img-placeholder">{icon}</div>', unsafe_allow_html=True)


# ── Executive summary ─────────────────────────────────────────────────────────

def render_run_summary(insights: list[dict], run_label: str) -> None:
    with st.expander(f"🔬 Run Intelligence — {run_label}", expanded=False):
        chips_html = " ".join(
            f'<span class="chip {i.get("level","info")}">{i["text"]}</span>'
            for i in insights
        )
        st.markdown(chips_html, unsafe_allow_html=True)


# ── Routing trace panel ───────────────────────────────────────────────────────

def render_routing_trace(row: dict, trace: dict | None = None) -> None:
    cat       = row.get("category", "—")
    conf      = row.get("cat_confidence", 0)
    band      = row.get("cat_band", "—")
    unstable  = row.get("cat_unstable", False)
    secondary = row.get("secondary_cat", "")
    scope     = row.get("scope_basis", "")

    conf_color = "#2ecc71" if band == "high" else "#f1c40f" if band == "medium" else "#e74c3c"
    unstable_badge = (
        '<span style="background:#c0392b;color:#fff;padding:2px 7px;'
        'border-radius:2px;font-size:0.72rem;font-weight:700;margin-left:8px">⚠ UNSTABLE</span>'
        if unstable else ""
    )

    st.markdown('<div class="section-header">Routing Trace</div>', unsafe_allow_html=True)

    html = f"""
<div class="routing-panel">
  <div style="margin-bottom:8px">
    <span class="rl">Primary archetype</span><br>
    <span class="rv" style="font-size:1.05rem">{cat}</span>
    {unstable_badge}
  </div>
  <div style="display:flex;gap:32px;margin-bottom:6px">
    <div>
      <span class="rl">Confidence</span><br>
      <span class="val" style="color:{conf_color};font-weight:700">{conf:.2f}</span>
      <span class="mono" style="color:#7f8fa6;font-size:0.8rem"> [{band}]</span>
    </div>
    {'<div><span class="rl">Secondary</span><br><span class="rv">' + secondary + '</span></div>' if secondary and secondary != cat else ''}
  </div>
  <div class="rsig">
    <span class="rl">Scope basis</span><br>
    {scope or '<span style="color:#555">no scope signals recorded</span>'}
  </div>
</div>
""".replace("  ", " ")
    st.markdown(html, unsafe_allow_html=True)


# ── Guardrail / cap-floor diagnostic panel ───────────────────────────────────

def render_guardrail_panel(row: dict, trace: dict | None = None) -> None:
    w   = row.get("weighted_score") or 0
    ac  = row.get("score_after_cap")
    ap  = row.get("score_after_penalty")
    af  = row.get("score_after_floors")
    fs  = row.get("score") or 0

    # Get raw rule lists from trace if available
    caps_raw   = (trace or {}).get("caps_applied", []) if trace else []
    floors_raw = (trace or {}).get("floors_applied", []) if trace else []

    st.markdown('<div class="section-header">Guardrail Resolution</div>', unsafe_allow_html=True)

    def score_box(label: str, value: float, color: str = "#3498db") -> str:
        return (
            f'<div style="display:inline-block;background:#12151f;border:1px solid {color};'
            f'border-radius:2px;padding:4px 12px;margin:2px 0">'
            f'<span style="color:#7f8fa6;font-size:0.72rem;text-transform:uppercase">{label}</span>'
            f'<br><span style="color:{color};font-weight:700;font-size:1.1rem;'
            f'font-family:\'JetBrains Mono\',monospace">{value:.1f}</span></div>'
        )

    def rule_card(rule_name: str, value: float | None, note: str, kind: str) -> str:
        arrow = {"cap": "🔻", "floor": "🔺", "info": "→"}.get(kind, "→")
        val_str = f"{value:.1f}" if value is not None else "—"
        note_html = f'<br><span class="note">{note}</span>' if note else ""
        return (
            f'<div class="rule-card {kind}">'
            f'<span class="label">{kind.upper()}</span>&nbsp;'
            f'<span class="val">{rule_name}</span> → {arrow} {val_str}'
            f'{note_html}'
            f'</div>'
        )

    parts = [score_box("Weighted score", w, "#3498db")]

    if caps_raw:
        binding = min(c["cap"] for c in caps_raw if isinstance(c, dict) and "cap" in c) if caps_raw else None
        for c in caps_raw:
            if isinstance(c, dict):
                rname = c.get("rule", str(c))
                cval  = c.get("cap")
                is_binding = (cval == binding)
                note = "⬅ BINDING" if is_binding else ""
                parts.append(rule_card(rname, cval, note, "cap"))
    elif ac is not None and abs(ac - w) > 0.01:
        parts.append(rule_card(f"binding_cap={row.get('binding_cap','?')}", ac, "from caps_applied", "cap"))

    if ap is not None and ac is not None and abs(ap - ac) > 0.01:
        parts.append(rule_card("penalty adjustment", ap, "", "cap"))

    if floors_raw:
        for f in floors_raw:
            if isinstance(f, dict):
                fname  = f.get("floor_type", str(f))
                fval   = f.get("floor_value")
                fnote  = f.get("note", "")
                pre    = f.get("pre_floor")
                full_note = f"{fnote} (pre-floor: {pre:.1f})" if pre is not None else fnote
                parts.append(rule_card(fname, fval, full_note, "floor"))
    elif af is not None:
        prev = ap if ap is not None else (ac if ac is not None else w)
        if abs(af - prev) > 0.01:
            applied = row.get("floors_applied", "")
            parts.append(rule_card(applied or "floor applied", af, "", "floor"))

    final_color = "#2ecc71" if fs >= 80 else "#f1c40f" if fs >= 65 else "#e67e22" if fs >= 50 else "#e74c3c"
    parts.append(score_box("Final score", fs, final_color))

    st.markdown("".join(parts), unsafe_allow_html=True)


# ── Signal inspector (expandable) ─────────────────────────────────────────────

def render_signal_inspector(trace: dict) -> None:
    if not trace:
        return

    st.markdown('<div class="section-header">Signal Inspector</div>', unsafe_allow_html=True)

    l3 = trace.get("L3_inferred_classifications", {})
    l1 = trace.get("L1_observed_signals", {})

    # NOVA evidence
    ev_for = trace.get("nova_evidence_for", []) or []
    ev_ag  = trace.get("nova_evidence_against", []) or []
    nova_conf = trace.get("nova_confidence", 0)
    nova_band = trace.get("nova_confidence_band", "—")

    with st.expander(f"NOVA classification  [{trace.get('nova_proxy','?')} · conf={nova_conf:.2f} {nova_band}]"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Evidence FOR NOVA4**")
            for e in (ev_for or ["none"]):
                st.markdown(f"🔴 `{e}`")
        with c2:
            st.markdown("**Evidence AGAINST NOVA4**")
            for e in (ev_ag or ["none"]):
                st.markdown(f"🟢 `{e}`")

    # Additive signals
    add_cats = l3.get("additive_categories", []) or []
    add_count = l3.get("additive_marker_count", 0) or 0
    with st.expander(f"Additives  [{add_count} markers · {len(add_cats)} categories]"):
        if add_cats:
            for cat in add_cats:
                st.markdown(f"- `{cat}`")
        else:
            st.caption("No additive categories detected.")

        flags = []
        if l3.get("sweetener_detected"):     flags.append("sweetener_detected")
        if l3.get("has_flavor_enhancer"):    flags.append("flavor_enhancer")
        if l3.get("has_palm_oil"):           flags.append("palm_oil")
        if l3.get("has_whole_grain"):        flags.append("whole_grain")
        if l3.get("has_fermentation"):       flags.append("fermentation_markers")
        if flags:
            st.markdown("**Active flags:** " + " · ".join(f"`{f}`" for f in flags))

    # L3 flags
    red_labels = l3.get("red_labels", []) or []
    with st.expander(f"Red labels  [{len(red_labels)} fired]"):
        if red_labels:
            for rl in red_labels:
                label = rl if isinstance(rl, str) else str(rl)
                st.markdown(f"🚫 `{label}`")
        else:
            st.success("No red labels triggered.", icon="✅")

    # Sugar context
    sugar_ctx = trace.get("sugar_context_class", "")
    with st.expander(f"Sugar context  [{sugar_ctx or '—'}]"):
        st.markdown(f"**Class:** `{sugar_ctx or 'not set'}`")
        st.markdown(f"**Sugar (g):** {l1.get('sugars_g','?')}")
        if l3.get("sweetener_detected"):
            st.warning("Sweetener detected — may mask sugar content in NOVA classification.")

    # Scope basis
    scope = trace.get("scope_basis", []) or []
    with st.expander(f"Scope basis  [{len(scope)} signal(s)]"):
        for s in scope:
            st.markdown(f"- {s}")
        if not scope:
            st.caption("No scope signals recorded.")

    # Explanation drivers
    drivers = trace.get("explanation_drivers", []) or []
    unresolved = trace.get("unresolved_flags", []) or []
    with st.expander(f"Explanation drivers  [{len(drivers)} driver(s) · {len(unresolved)} unresolved]"):
        for d in drivers:
            st.markdown(f"✅ {d}")
        for u in unresolved:
            st.warning(u, icon="⚠️")


# ── Anomaly severity summary row ──────────────────────────────────────────────

def render_severity_header(counts: dict[str, int]) -> None:
    cols = st.columns(4)
    labels = [("CRITICAL", "🔴"), ("HIGH", "🟠"), ("MEDIUM", "🟡"), ("LOW", "🔵")]
    for col, (sev, icon) in zip(cols, labels):
        n = counts.get(sev, 0)
        col.metric(f"{icon} {sev}", n, delta=None)
