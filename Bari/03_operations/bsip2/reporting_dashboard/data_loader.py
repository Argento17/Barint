"""
BSIP2 Dashboard — Data Loader
Discovers runs under 02_products/, loads traces, enriches with BSIP1 data,
returns a flat pandas DataFrame ready for filtering and display.
"""
import json
import pathlib
import pandas as pd

PRODUCTS_ROOT = pathlib.Path(r"C:\Bari\02_products")

# Columns that hold per-dimension scores (prefix dim_)
DIMENSION_NAMES = [
    "processing_quality", "nutrient_density", "calorie_density",
    "glycemic_quality", "protein_quality", "additive_quality",
    "satiety_support", "fat_quality", "regulatory_quality",
    "whole_food_integrity",
]
DIM_COLS = [f"dim_{d}" for d in DIMENSION_NAMES]

DIMENSION_LABELS = {
    "processing_quality":  "Processing",
    "nutrient_density":    "Nutrients",
    "calorie_density":     "Calories",
    "glycemic_quality":    "Glycemic",
    "protein_quality":     "Protein",
    "additive_quality":    "Additives",
    "satiety_support":     "Satiety",
    "fat_quality":         "Fat",
    "regulatory_quality":  "Regulatory",
    "whole_food_integrity":"Integrity",
}


def discover_runs() -> list[dict]:
    """Scan 02_products/ and return all BSIP2 runs with product counts."""
    runs = []
    if not PRODUCTS_ROOT.exists():
        return runs
    for cat_dir in sorted(PRODUCTS_ROOT.iterdir()):
        if not cat_dir.is_dir():
            continue
        bsip2_dir = cat_dir / "bsip2_outputs"
        if not bsip2_dir.exists():
            continue
        for run_dir in sorted(bsip2_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            products_dir = run_dir / "products"
            if not products_dir.exists():
                continue
            trace_paths = list(products_dir.glob("*/bsip2_trace.json"))
            if not trace_paths:
                continue
            # Peek at first trace to find BSIP1 source root
            with open(trace_paths[0], encoding="utf-8") as f:
                first = json.load(f)
            bsip1_src_path = first.get("input_reference", {}).get("bsip1_source_path", "")
            bsip1_root = pathlib.Path(bsip1_src_path).parent if bsip1_src_path else None
            runs.append({
                "label":       f"{cat_dir.name}  /  {run_dir.name}  ({len(trace_paths)} products)",
                "category":    cat_dir.name,
                "run_id":      run_dir.name,
                "trace_root":  str(products_dir),
                "bsip1_root":  str(bsip1_root) if bsip1_root and bsip1_root.exists() else "",
                "n_products":  len(trace_paths),
            })
    return runs


def _load_json(path: pathlib.Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _get_subtype(bsip1: dict) -> str:
    for key, val in bsip1.items():
        if key.startswith("bsip_") and key.endswith("_subtype") and val:
            return str(val)
    return "—"


def _safe(d: dict, *keys, default=None):
    """Nested dict get."""
    cur = d
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
    return cur


def _extract_row(t: dict, bsip1: dict) -> dict:
    ref  = t.get("input_reference", {})
    nutr = t.get("L1_observed_signals", {})
    l3   = t.get("L3_inferred_classifications", {})
    dims = t.get("dimension_scores", {})

    # Waterfall deltas
    w  = t.get("weighted_dimension_score") or 0
    ac = t.get("score_after_cap")
    ap = t.get("score_after_penalty")
    af = t.get("score_after_floors")
    fs = t.get("final_score_estimate")

    caps_raw     = t.get("caps_applied", []) or []
    caps_applied = "; ".join(
        c.get("rule", str(c)) if isinstance(c, dict) else str(c)
        for c in caps_raw
    )
    floors_raw   = t.get("floors_applied", []) or []
    floors_str   = "; ".join(
        f.get("floor_type", str(f)) if isinstance(f, dict) else str(f)
        for f in floors_raw
    )

    row = {
        # ── Identity ──────────────────────────────────────────────
        "product_id":   ref.get("canonical_product_id", ""),
        "name_he":      ref.get("product_name_he") or bsip1.get("canonical_name_he", ""),
        "brand":        ref.get("brand") or bsip1.get("brand", ""),
        "barcode":      ref.get("barcode", ""),
        "image_url":    bsip1.get("image_url") or "",
        "subtype":      _get_subtype(bsip1),
        "retailer":     ", ".join(bsip1.get("source_retailers", [])),
        "claims":       "; ".join(bsip1.get("claims", [])),
        "allergens":    ", ".join(bsip1.get("allergens_contains", [])),
        "ingredients_text": bsip1.get("ingredients_text_he", ""),
        # ── Routing ───────────────────────────────────────────────
        "category":         t.get("category", ""),
        "cat_confidence":   t.get("category_confidence", 0),
        "cat_band":         t.get("category_confidence_band", ""),
        "cat_unstable":     bool(t.get("category_instability_flag", False)),
        "secondary_cat":    t.get("secondary_category") or "",
        # ── NOVA ──────────────────────────────────────────────────
        "nova":             t.get("nova_proxy"),
        "nova_conf":        t.get("nova_confidence", 0),
        "nova_band":        t.get("nova_confidence_band", ""),
        "nova_evidence_for":    "; ".join(t.get("nova_evidence_for", [])),
        "nova_evidence_against":"; ".join(t.get("nova_evidence_against", [])),
        # ── Final Score ────────────────────────────────────────────
        "score":            fs,
        "grade":            t.get("grade_estimate", "?"),
        "confidence":       t.get("confidence_score"),
        "conf_band":        t.get("confidence_band", ""),
        "data_sufficiency": t.get("data_sufficiency", ""),
        # ── Waterfall ─────────────────────────────────────────────
        "weighted_score":   w,
        "score_after_cap":  ac,
        "score_after_penalty": ap,
        "score_after_floors":  af,
        "binding_cap":      t.get("binding_cap"),
        "caps_applied":     caps_applied,
        "floors_applied":   floors_str,
        # ── Nutrition (L1) ────────────────────────────────────────
        "kcal":      nutr.get("energy_kcal"),
        "fat_g":     nutr.get("fat_g"),
        "sat_fat_g": nutr.get("fat_saturated_g"),
        "sodium_mg": nutr.get("sodium_mg"),
        "sugar_g":   nutr.get("sugars_g"),
        "fiber_g":   nutr.get("dietary_fiber_g"),
        "protein_g": nutr.get("protein_g"),
        "ing_count": nutr.get("ingredient_count"),
        # ── L3 flags ──────────────────────────────────────────────
        "red_labels":       len(l3.get("red_labels", []) or []),
        "has_sweetener":    bool(l3.get("sweetener_detected", False)),
        "has_flavor_enh":   bool(l3.get("has_flavor_enhancer", False)),
        "has_whole_grain":  bool(l3.get("has_whole_grain", False)),
        "has_fermentation": bool(l3.get("has_fermentation", False)),
        "has_palm_oil":     bool(l3.get("has_palm_oil", False)),
        "additive_count":   l3.get("additive_marker_count", 0) or 0,
        "additive_cats":    ", ".join(l3.get("additive_categories", []) or []),
        "sugar_context":    t.get("sugar_context_class", ""),
        # ── Dimension scores ─────────────────────────────────────
        **{f"dim_{k}": dims.get(k) for k in DIMENSION_NAMES},
        # ── Trace narrative ──────────────────────────────────────
        "explanation":   " | ".join(t.get("explanation_drivers", []) or []),
        "unresolved":    " | ".join(t.get("unresolved_flags", []) or []),
        "scope_basis":   " | ".join(t.get("scope_basis", []) or []),
    }
    return row


def load_run(run: dict) -> tuple[list[dict], pd.DataFrame]:
    """
    Load all traces for a run.
    Returns (raw_trace_records, flat_dataframe).
    raw_trace_records = [{"trace": ..., "bsip1": ..., "row": ...}, ...]
    """
    trace_root = pathlib.Path(run["trace_root"])
    bsip1_root = pathlib.Path(run["bsip1_root"]) if run.get("bsip1_root") else None

    records = []
    rows = []

    for trace_path in sorted(trace_root.glob("*/bsip2_trace.json")):
        t = _load_json(trace_path)
        if not t:
            continue

        # Resolve BSIP1 file
        bsip1_src = t.get("input_reference", {}).get("bsip1_source_path", "")
        bsip1 = _load_json(pathlib.Path(bsip1_src)) if bsip1_src else {}
        # Fallback: look in the known bsip1_root
        if not bsip1 and bsip1_root:
            pid = (t.get("input_reference") or {}).get("canonical_product_id", "")
            fallback = bsip1_root / f"{pid}.json"
            if fallback.exists():
                bsip1 = _load_json(fallback)

        row = _extract_row(t, bsip1)
        records.append({"trace": t, "bsip1": bsip1, "row": row})
        rows.append(row)

    df = pd.DataFrame(rows)
    # Coerce numeric columns
    for col in ["score", "nova", "kcal", "fat_g", "sat_fat_g", "sodium_mg",
                "sugar_g", "fiber_g", "protein_g", "binding_cap",
                "weighted_score", "confidence", "additive_count"] + DIM_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return records, df
