"""
BSIP2 Dashboard — Run Comparison Engine
Merges two run DataFrames and computes delta analytics.
"""
import pandas as pd

_MERGE_COLS = [
    "product_id", "name_he", "score", "grade",
    "nova", "category", "binding_cap", "brand",
    "subtype", "caps_applied",
]


def merge_runs(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
    """
    Match products by canonical_product_id.
    Returns merged DataFrame with *_a / *_b columns + delta columns.
    """
    def pick(df: pd.DataFrame) -> pd.DataFrame:
        avail = [c for c in _MERGE_COLS if c in df.columns]
        return df[avail].copy()

    a = pick(df_a)
    b = pick(df_b)

    # Rename payload columns with suffix (keep product_id as join key)
    shared_meta = {"product_id", "name_he", "brand"}
    a = a.rename(columns={c: f"{c}_a" for c in a.columns if c not in shared_meta})
    b = b.rename(columns={c: f"{c}_b" for c in b.columns if c not in shared_meta})
    # Drop duplicate name/brand from b to avoid _x/_y collision
    b = b.drop(columns=[c for c in ["name_he", "brand"] if c in b.columns], errors="ignore")

    merged = a.merge(b, on="product_id", how="outer")

    # Derived delta columns
    score_a = pd.to_numeric(merged.get("score_a"), errors="coerce")
    score_b = pd.to_numeric(merged.get("score_b"), errors="coerce")
    merged["delta"]          = (score_b - score_a).round(1)
    merged["grade_changed"]  = merged.get("grade_a") != merged.get("grade_b")
    merged["nova_changed"]   = merged.get("nova_a")  != merged.get("nova_b")
    merged["routing_changed"]= merged.get("category_a") != merged.get("category_b")
    merged["cap_changed"]    = merged.get("binding_cap_a") != merged.get("binding_cap_b")

    return merged.sort_values("delta", ascending=False, na_position="last").reset_index(drop=True)


def run_insights(df: pd.DataFrame) -> list[dict]:
    """
    Generate auto-insights from a run DataFrame.
    Returns list of dicts: {text, level} where level in "good"/"warn"/"bad"/"info"
    """
    n = len(df)
    if n == 0:
        return [{"text": "No products loaded.", "level": "warn"}]
    insights = []

    # Routing concentration
    if "category" in df.columns:
        vc = df["category"].value_counts()
        if not vc.empty:
            pct = int(vc.iloc[0] / n * 100)
            level = "info" if pct < 80 else "warn" if pct >= 95 else "info"
            insights.append({"text": f"{pct}% → `{vc.index[0]}`", "level": level})

    # S-tier
    s = int((df.get("grade", pd.Series()) == "S").sum())
    if s == 0:
        insights.append({"text": "no S-tier products", "level": "warn"})
    else:
        insights.append({"text": f"{s} S-tier", "level": "good"})

    # Caps applied
    capped = int(df["binding_cap"].notna().sum()) if "binding_cap" in df.columns else 0
    if capped:
        pct_c = int(capped / n * 100)
        lvl = "bad" if pct_c > 40 else "warn"
        insights.append({"text": f"{capped} cap{'s' if capped>1 else ''} ({pct_c}%)", "level": lvl})

    # NOVA4
    if "nova" in df.columns:
        n4 = int((df["nova"] == 4).sum())
        if n4:
            lvl = "bad" if n4/n > 0.3 else "warn"
            insights.append({"text": f"NOVA4: {n4} ({int(n4/n*100)}%)", "level": lvl})

    # NOVA1 floor cluster
    if "nova" in df.columns and "score" in df.columns:
        n1f = int(((df["nova"] == 1) & (df["score"] >= 84)).sum())
        if n1f >= 2:
            insights.append({"text": f"{n1f} at NOVA1 floor=85", "level": "info"})

    # Routing instability
    if "cat_unstable" in df.columns:
        unstable = int(df["cat_unstable"].sum())
        if unstable:
            insights.append({"text": f"{unstable} routing flag{'s' if unstable>1 else ''}", "level": "warn"})

    # Score range
    if "score" in df.columns:
        s_min = df["score"].min()
        s_max = df["score"].max()
        if pd.notna(s_min) and pd.notna(s_max):
            insights.append({"text": f"range {s_min:.0f}–{s_max:.0f}", "level": "info"})

    # Double red labels
    if "red_labels" in df.columns:
        dred = int((df["red_labels"] >= 2).sum())
        if dred:
            insights.append({"text": f"{dred} double-red label{'s' if dred>1 else ''}", "level": "bad"})

    # Flavor enhancer NOVA4 (vanilla bug proxy)
    if "has_flavor_enh" in df.columns and "has_sweetener" in df.columns and "nova" in df.columns:
        vanilla_n4 = int(
            ((df["nova"] == 4) & df["has_flavor_enh"].fillna(False) & ~df["has_sweetener"].fillna(False)).sum()
        )
        if vanilla_n4:
            insights.append({"text": f"flavor_enh NOVA4: {vanilla_n4}", "level": "warn"})

    return insights
