#!/usr/bin/env python3
"""
TASK-395 — BARI_ADDITIVE_PARSE_FIX_V1: L3 Parser Coverage Fix
==============================================================
Extends the dechain runner with a FOURTH column:
  Column A: baseline     (W4_WFI=off, D4=off, PARSE_FIX=off) — zero-drift check
  Column B: +Stage0      (W4_WFI=on,  D4=off, PARSE_FIX=off)
  Column C: +Stage0+1A   (W4_WFI=on,  D4=on,  PARSE_FIX=off) — pre-existing
  Column D: +Stage0+1A+ParseFix (W4_WFI=on, D4=on, PARSE_FIX=on) — the target

All 12 live categories are re-scored (blast radius).
Chokita/Petit-Beurre inversion is measured in each column.
G9 inversion-invariant gate is re-run on the post-fix cookies traces.

CRITICAL: BARI_ADDITIVE_PARSE_FIX_V1 is a PARSER flag (L3 inference), not just
a scoring flag. It must be set BEFORE importing signal_extractor so the engine
re-infers additive_marker_count from the changed ADDITIVE_MARKER_PATTERNS.
The rescore_category() helper below reloads both signal_extractor AND score_engine
on each column via importlib.reload() so the flag takes effect cleanly.

Output: C:\\Bari\\_rescore_staging\\_task395_parse_fix\\
No committed artifacts modified. No git ops.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path("C:/Bari")
SRC  = REPO / "03_operations/bsip2/proto_v0/src"
COMPARISONS_DIR = REPO / "bari-web/src/data/comparisons"
GATES_DIR = REPO / "03_operations/page_generator/gates"
OUT_DIR = REPO / "_rescore_staging/_task395_parse_fix"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TRACES_OUT_DIR = OUT_DIR / "cookies_traces_parse_fix"
TRACES_OUT_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SRC))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# BSIP1 corpus source map (from run_task395_dechain_drift.py)
# ---------------------------------------------------------------------------
BSIP1_SOURCES: dict[str, list[tuple[str, str]]] = {
    "brined_cheeses":    [("03_operations/bsip1/run_brined_cheeses_002/output", "bsip1_brinedcheese_*.json")],
    "cakes":             [("03_operations/bsip1/run_cakes_001/output", "bsip1_cakes_*.json")],
    "breakfast-cereals": [("03_operations/bsip1/run_cereals_008/output", "*.json")],
    "cheese-spreads":    [("03_operations/bsip1/run_cheese_003/output", "*.json")],
    "cookies_coffee":    [
        ("03_operations/bsip1/run_cookies_001/output", "*.json"),
        ("03_operations/bsip1/run_cakes_001/output",   "bsip1_cakes_*.json"),
    ],
    "granola":           [("03_operations/bsip1/run_cereals_005/output", "*.json")],
    "hard_cheeses":      [("02_products/hard_cheeses/bsip1_outputs",     "*.json")],
    "hummus":            [("02_products/hummus/canonical_bsip1",          "*.json")],
    "juices":            [("02_products/juices/bsip1_outputs",            "*.json")],
    "milk":              [("03_operations/bsip1/run_milk_002/output",     "*.json")],
    "snacks":            [("03_operations/bsip1/run_001/output",          "*.json")],
    "bread":             [("03_operations/bsip1/run_bread_conform_001/output", "*.json")],
}

CATEGORY_BASELINES: dict[str, str] = {
    "bread":             "bread_frontend_v3.json",
    "brined_cheeses":    "brined_cheeses_frontend_v2.json",
    "cakes":             "cakes_hard_cookies_frontend_v1.json",
    "breakfast-cereals": "cereals_frontend_v2.json",
    "cheese-spreads":    "cheese_frontend_v4.json",
    "cookies_coffee":    "cookies_coffee_frontend_v2.json",
    "granola":           "granola_frontend_v1.json",
    "hard_cheeses":      "hard_cheeses_frontend_v2.json",
    "hummus":            "hummus_frontend_v5.json",
    "juices":            "juices_frontend_v3.json",
    "milk":              "milk_frontend_v1.json",
    "snacks":            "snacks_frontend_v5.json",
}

CONFIG_DIR = REPO / "03_operations/page_generator/configs"
CATEGORY_CONFIGS: dict[str, str] = {
    "bread":             "bread.json",
    "brined_cheeses":    "brined_cheeses.json",
    "cakes":             "cakes.json",
    "breakfast-cereals": "cereals.json",
    "cheese-spreads":    "cheese.json",
    "cookies_coffee":    "cookies_coffee.json",
    "granola":           "granola.json",
    "hard_cheeses":      "hard_cheeses.json",
    "hummus":            "hummus_shelfrel_002.json",
    "juices":            "juices.json",
    "milk":              "milk.json",
    "snacks":            "snacks.json",
}

CHOKITA_BC = "7290019870470"
PETIT_BC   = "74184"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(p: Path) -> dict | list:
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json(p: Path, data) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    p.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(p: Path) -> str:
    if not p.is_file():
        return ""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _grade(score: float | None) -> str:
    if score is None:
        return "?"
    if score >= 90: return "S"
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 50: return "C"
    if score >= 35: return "D"
    return "E"


def collect_bsip1_records(category: str) -> dict[str, dict]:
    sources = BSIP1_SOURCES.get(category, [])
    by_barcode: dict[str, dict] = {}
    for rel_dir, glob_pat in sources:
        d = REPO / rel_dir
        if not d.is_dir():
            print(f"  [WARN] BSIP1 dir missing: {d}")
            continue
        for fpath in sorted(d.glob(glob_pat)):
            if "audit" in fpath.name:
                continue
            try:
                rec = load_json(fpath)
            except Exception:
                continue
            if not isinstance(rec, dict) or rec.get("file_type") != "product":
                continue
            bc = str(rec.get("barcode", "")).strip()
            if bc and bc not in by_barcode:
                by_barcode[bc] = rec
    return by_barcode


def load_baseline_scores(category: str) -> dict[str, dict]:
    fname = CATEGORY_BASELINES.get(category)
    if not fname:
        return {}
    fpath = COMPARISONS_DIR / fname
    if not fpath.is_file():
        return {}
    data = load_json(fpath)
    result: dict[str, dict] = {}
    for p in data.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if bc:
            result[bc] = {"score": p.get("score"), "grade": p.get("grade"), "name": p.get("name", "")}
    return result


def load_shelf_flags(category: str) -> dict[str, str]:
    cfg_name = CATEGORY_CONFIGS.get(category)
    if not cfg_name:
        return {}
    cfg_path = CONFIG_DIR / cfg_name
    if not cfg_path.is_file():
        return {}
    cfg = load_json(cfg_path)
    flags = cfg.get("scoring", {}).get("flags", {})
    return {k: str(v) for k, v in flags.items()}


def load_shelf_rel(category: str) -> dict | None:
    cfg_name = CATEGORY_CONFIGS.get(category)
    if not cfg_name:
        return None
    cfg_path = CONFIG_DIR / cfg_name
    if not cfg_path.is_file():
        return None
    cfg = load_json(cfg_path)
    return cfg.get("scoring", {}).get("shelf_rel") or None


def apply_shelf_rel(shelf_rel: dict | None, engine_mod) -> None:
    if not shelf_rel:
        return
    api = shelf_rel.get("api")
    median = shelf_rel.get("median")
    scale = shelf_rel.get("scale")
    nutrient = shelf_rel.get("nutrient")
    scale_type = shelf_rel.get("scale_type", "iqr")
    if api == "sodium_ev056":
        if median is not None and scale is not None:
            engine_mod.set_shelf_sodium_stats(median, scale)
    elif nutrient and median is not None and scale is not None:
        engine_mod.set_shelf_stats(nutrient, median, scale, scale_type)


# ---------------------------------------------------------------------------
# Reload both signal_extractor AND score_engine so flag takes effect.
# This is required because ADDITIVE_MARKER_PATTERNS is evaluated at import
# time in signal_extractor.py (it's a module-level constant).
# ---------------------------------------------------------------------------

def _apply_env_flags(flags: dict[str, str]) -> None:
    for k, v in flags.items():
        os.environ[k] = v


def _reload_engine_and_extractor():
    """Reload signal_extractor (L3 patterns) and score_engine so all flags apply."""
    import signal_extractor
    import score_engine
    importlib.reload(signal_extractor)
    importlib.reload(score_engine)
    return score_engine


def _make_score_one_with_trace(engine_mod):
    """Build a score_one callable that returns (score, l3_additive_info, full_result)."""
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope

    _first_error = [None]

    def score_one(product: dict):
        try:
            signals = extract_signals(product)
            cat_result = classify_category(product)
            l3 = signals["L3_inferred_classifications"]
            nova_result = infer_nova(product, l3)
            eval_result = assign_evaluation_scope(product, cat_result["category"])
            score_result = engine_mod.score_product(
                product, signals, cat_result, nova_result, eval_result
            )
            if not isinstance(score_result, dict):
                return None, {}, score_result
            fse = score_result.get("final_score_estimate")
            fse_f = float(fse) if fse is not None else None
            l3_info = {
                "additive_marker_count": l3.get("additive_marker_count"),
                "additive_categories": l3.get("additive_categories"),
                "has_flavor_enhancer": l3.get("has_flavor_enhancer"),
                "additive_quality": score_result.get("additive_quality"),
                "whole_food_integrity": score_result.get("whole_food_integrity"),
            }
            return fse_f, l3_info, score_result
        except Exception as exc:
            if _first_error[0] is None:
                import traceback
                _first_error[0] = traceback.format_exc()
                print(f"    [score_one ERROR] {exc}")
                print(f"    {_first_error[0][:300]}")
            return None, {}, {}

    score_one._first_error = _first_error
    return score_one


def rescore_category_with_trace(
    bsip1_records: dict[str, dict],
    shelf_flags: dict[str, str],
    extra_flags: dict[str, str],
    shelf_rel: dict | None = None,
) -> tuple[dict[str, float | None], dict[str, dict]]:
    """Rescore, returning (barcode->score, barcode->l3_info)."""
    combined = {**shelf_flags, **extra_flags}
    _apply_env_flags(combined)
    engine = _reload_engine_and_extractor()
    apply_shelf_rel(shelf_rel, engine)
    score_fn = _make_score_one_with_trace(engine)

    scores: dict[str, float | None] = {}
    l3_infos: dict[str, dict] = {}
    for bc, rec in bsip1_records.items():
        score, l3_info, _ = score_fn(rec)
        scores[bc] = score
        l3_infos[bc] = l3_info
    return scores, l3_infos


def rescore_category_score_only(
    bsip1_records: dict[str, dict],
    shelf_flags: dict[str, str],
    extra_flags: dict[str, str],
    shelf_rel: dict | None = None,
) -> dict[str, float | None]:
    combined = {**shelf_flags, **extra_flags}
    _apply_env_flags(combined)
    engine = _reload_engine_and_extractor()
    apply_shelf_rel(shelf_rel, engine)
    score_fn = _make_score_one_with_trace(engine)

    scores: dict[str, float | None] = {}
    for bc, rec in bsip1_records.items():
        score, _, _ = score_fn(rec)
        scores[bc] = score
    return scores


# ---------------------------------------------------------------------------
# Movement + stats helpers
# ---------------------------------------------------------------------------

def movement_table_4col(
    baseline: dict[str, dict],
    col_a: dict[str, float | None],
    col_b: dict[str, float | None],
    col_c: dict[str, float | None],
    col_d: dict[str, float | None],
) -> list[dict]:
    all_bcs = (set(baseline.keys()) | set(col_a.keys()) |
               set(col_b.keys()) | set(col_c.keys()) | set(col_d.keys()))
    rows = []
    for bc in sorted(all_bcs):
        name = baseline.get(bc, {}).get("name", "")
        committed_score = baseline.get(bc, {}).get("score")
        committed_grade = baseline.get(bc, {}).get("grade")
        sa = col_a.get(bc)
        sb = col_b.get(bc)
        sc = col_c.get(bc)
        sd = col_d.get(bc)
        ga, gb, gc, gd = _grade(sa), _grade(sb), _grade(sc), _grade(sd)
        rows.append({
            "barcode": bc,
            "name": name,
            "committed_score": committed_score,
            "committed_grade": committed_grade,
            "col_a_score": round(sa, 1) if sa is not None else None,
            "col_a_grade": ga,
            "col_b_score": round(sb, 1) if sb is not None else None,
            "col_b_grade": gb,
            "col_c_score": round(sc, 1) if sc is not None else None,
            "col_c_grade": gc,
            "col_d_score": round(sd, 1) if sd is not None else None,
            "col_d_grade": gd,
            "c_delta_vs_a": round(sc - sa, 1) if sa is not None and sc is not None else None,
            "d_delta_vs_a": round(sd - sa, 1) if sa is not None and sd is not None else None,
            "d_delta_vs_c": round(sd - sc, 1) if sc is not None and sd is not None else None,
            "d_grade_change_vs_a": gd != ga if (sa is not None and sd is not None) else None,
            "d_grade_change_vs_c": gd != gc if (sc is not None and sd is not None) else None,
            "a_vs_committed_delta": round(sa - committed_score, 1)
                                    if sa is not None and committed_score is not None else None,
        })
    rows.sort(key=lambda r: (-(abs(r["d_delta_vs_a"]) if r["d_delta_vs_a"] is not None else 0), r["barcode"]))
    return rows


def delta_stats(deltas: list[float]) -> dict:
    if not deltas:
        return {"count": 0, "min": None, "max": None, "median": None, "stdev": None}
    return {
        "count": len(deltas),
        "min": round(min(deltas), 2),
        "max": round(max(deltas), 2),
        "median": round(statistics.median(deltas), 2),
        "stdev": round(statistics.stdev(deltas), 2) if len(deltas) > 1 else 0.0,
    }


def check_baseline_drift(rows: list[dict]) -> dict:
    mismatches, matched = [], 0
    for r in rows:
        committed = r["committed_score"]
        sa = r["col_a_score"]
        if committed is None or sa is None:
            continue
        if abs(sa - committed) > 0.2:
            mismatches.append({"barcode": r["barcode"], "name": r["name"],
                                "committed": committed, "col_a": sa,
                                "delta": round(sa - committed, 1)})
        else:
            matched += 1
    return {"matched": matched, "mismatches": len(mismatches),
            "mismatch_details": mismatches[:10], "zero_drift_pass": len(mismatches) == 0}


def grade_movers_vs_col(rows: list[dict], change_key: str, score_before_key: str,
                        grade_before_key: str, score_after_key: str, grade_after_key: str,
                        delta_key: str) -> list[dict]:
    movers = []
    for r in rows:
        if r.get(change_key):
            movers.append({
                "barcode": r["barcode"], "name": r["name"],
                "score_before": r[score_before_key], "grade_before": r[grade_before_key],
                "score_after": r.get(score_after_key), "grade_after": r.get(grade_after_key),
                "delta": r.get(delta_key),
            })
    movers.sort(key=lambda m: abs(m["delta"] or 0), reverse=True)
    return movers


# ---------------------------------------------------------------------------
# G9 inversion invariant re-run on fresh traces
# ---------------------------------------------------------------------------

def run_g9_on_traces(traces: list[dict]) -> dict:
    """Run the G9 inversion invariant gate on a list of trace dicts."""
    sys.path.insert(0, str(GATES_DIR))
    import inversion_invariant as ii
    importlib.reload(ii)
    g = ii.gate_inversion_invariant(traces)
    # Count firing pairs
    firing_count = sum(1 for line in g.lines if "FAIL: INVERSION:" in line)
    return {
        "status": g.status,
        "firing_pairs": firing_count,
        "lines": g.lines[:30],  # cap for report
    }


def build_cookies_trace_for_g9(bc: str, rec: dict, score: float | None, l3_info: dict) -> dict:
    """Build a minimal trace dict the G9 gate can consume."""
    nn = rec.get("normalized_nutrition_per_100g") or {}
    l3_full = {
        "additive_marker_count": l3_info.get("additive_marker_count"),
        "red_label_count": None,  # G9 uses this; will be None if not in l3_info
        "has_palm_oil": rec.get("L3_inferred_classifications", {}).get("has_palm_oil"),
        "has_seed_oil": rec.get("L3_inferred_classifications", {}).get("has_seed_oil"),
    }
    return {
        "input_reference": {"barcode": bc, "product_name_he": rec.get("canonical_name_he", "")},
        "final_score_estimate": score,
        "evaluation_status": "scored",
        "confidence_band": "medium",
        "L1_observed_signals": {
            "sugars_g": nn.get("sugars_g"),
            "fat_saturated_g": nn.get("fat_saturated_g"),
        },
        "L3_inferred_classifications": l3_full,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"\n{'='*72}")
    print(f"TASK-395 Parse-Fix Runner — {run_ts}")
    print(f"Output dir: {OUT_DIR}")
    print(f"{'='*72}\n")

    all_results = {}
    baseline_drift_summary = []
    total_scored = 0

    # Cross-category aggregates
    agg_c_deltas, agg_d_deltas = [], []
    agg_d_vs_c_deltas = []
    agg_grade_movers_d_vs_a = []
    agg_grade_movers_d_vs_c = []

    chokita_row: dict | None = None
    petit_row: dict | None = None
    chokita_l3_a: dict = {}
    chokita_l3_d: dict = {}

    # Additive threshold crossings (3_PLUS cap=72, 5_PLUS cap=60)
    threshold_crossings = []

    for category in sorted(CATEGORY_BASELINES.keys()):
        print(f"\n--- {category} ---")
        baseline = load_baseline_scores(category)
        shelf_flags = load_shelf_flags(category)
        shelf_rel = load_shelf_rel(category)
        bsip1 = collect_bsip1_records(category)

        n_bsip1 = len(bsip1)
        n_baseline = len(baseline)
        print(f"  BSIP1 records: {n_bsip1} | Baseline products: {n_baseline}")

        if n_bsip1 == 0:
            print(f"  [SKIP] No BSIP1 records found.")
            continue

        # Column A: all new flags OFF
        print(f"  Col A (baseline)...")
        col_a, l3_a = rescore_category_with_trace(
            bsip1, shelf_flags,
            {"BARI_W4_WFI_V1": "off", "BARI_D4_SCORE_V1": "off", "BARI_ADDITIVE_PARSE_FIX_V1": "off"},
            shelf_rel)

        # Column B: +WFI
        print(f"  Col B (+WFI)...")
        col_b = rescore_category_score_only(
            bsip1, shelf_flags,
            {"BARI_W4_WFI_V1": "on", "BARI_D4_SCORE_V1": "off", "BARI_ADDITIVE_PARSE_FIX_V1": "off"},
            shelf_rel)

        # Column C: +WFI +D4
        print(f"  Col C (+WFI+D4)...")
        col_c = rescore_category_score_only(
            bsip1, shelf_flags,
            {"BARI_W4_WFI_V1": "on", "BARI_D4_SCORE_V1": "on", "BARI_ADDITIVE_PARSE_FIX_V1": "off"},
            shelf_rel)

        # Column D: +WFI +D4 +ParseFix — the TARGET column
        print(f"  Col D (+WFI+D4+ParseFix)...")
        col_d, l3_d = rescore_category_with_trace(
            bsip1, shelf_flags,
            {"BARI_W4_WFI_V1": "on", "BARI_D4_SCORE_V1": "on", "BARI_ADDITIVE_PARSE_FIX_V1": "on"},
            shelf_rel)

        # Build movement table
        rows = movement_table_4col(baseline, col_a, col_b, col_c, col_d)
        n_scored = sum(1 for r in rows if r["col_a_score"] is not None)
        total_scored += n_scored

        # Zero-drift check (col A must reproduce baseline)
        drift_check = check_baseline_drift(rows)
        baseline_drift_summary.append({"category": category, **drift_check})
        if not drift_check["zero_drift_pass"]:
            print(f"  [WARN] Col A drift: {drift_check['mismatches']} mismatches")
        else:
            print(f"  [OK] Col A zero-drift: {drift_check['matched']}/{n_baseline} matched")

        # Additive count changes in column D (parse-fix adds L3 counts)
        additive_changed = []
        for bc in bsip1:
            a_count = l3_a.get(bc, {}).get("additive_marker_count")
            d_count = l3_d.get(bc, {}).get("additive_marker_count")
            if a_count is not None and d_count is not None and d_count != a_count:
                a_cats = l3_a.get(bc, {}).get("additive_categories", [])
                d_cats = l3_d.get(bc, {}).get("additive_categories", [])
                additive_changed.append({
                    "barcode": bc,
                    "name": bsip1[bc].get("canonical_name_he", "")[:60],
                    "count_col_a": a_count,
                    "count_col_d": d_count,
                    "cats_col_a": a_cats,
                    "cats_col_d": d_cats,
                    "new_categories": sorted(set(d_cats) - set(a_cats)),
                })
                # Check threshold crossings
                if a_count < 3 <= d_count:
                    threshold_crossings.append({"category": category, "barcode": bc,
                        "name": bsip1[bc].get("canonical_name_he", "")[:60],
                        "threshold": "3_PLUS", "count_before": a_count, "count_after": d_count})
                if a_count < 5 <= d_count:
                    threshold_crossings.append({"category": category, "barcode": bc,
                        "name": bsip1[bc].get("canonical_name_he", "")[:60],
                        "threshold": "5_PLUS", "count_before": a_count, "count_after": d_count})

        # Aggregate deltas
        c_deltas = [r["c_delta_vs_a"] for r in rows if r["c_delta_vs_a"] is not None]
        d_deltas = [r["d_delta_vs_a"] for r in rows if r["d_delta_vs_a"] is not None]
        d_vs_c_deltas = [r["d_delta_vs_c"] for r in rows if r["d_delta_vs_c"] is not None]
        agg_c_deltas.extend(c_deltas)
        agg_d_deltas.extend(d_deltas)
        agg_d_vs_c_deltas.extend(d_vs_c_deltas)

        # Grade movers
        gm_d_vs_a = grade_movers_vs_col(rows,
            "d_grade_change_vs_a", "col_a_score", "col_a_grade",
            "col_d_score", "col_d_grade", "d_delta_vs_a")
        gm_d_vs_c = grade_movers_vs_col(rows,
            "d_grade_change_vs_c", "col_c_score", "col_c_grade",
            "col_d_score", "col_d_grade", "d_delta_vs_c")
        agg_grade_movers_d_vs_a.extend([{**m, "category": category} for m in gm_d_vs_a])
        agg_grade_movers_d_vs_c.extend([{**m, "category": category} for m in gm_d_vs_c])

        # Track Chokita/Petit-Beurre
        for r in rows:
            if r["barcode"] == CHOKITA_BC:
                chokita_row = {**r, "category": category}
                chokita_l3_a = l3_a.get(CHOKITA_BC, {})
                chokita_l3_d = l3_d.get(CHOKITA_BC, {})
            if r["barcode"] == PETIT_BC:
                petit_row = {**r, "category": category}

        d_affected = sum(1 for d in d_deltas if abs(d) > 0)
        d_vs_c_affected = sum(1 for d in d_vs_c_deltas if abs(d) > 0)
        print(f"  Scored: {n_scored} | D-affected (vs A): {d_affected} "
              f"({len(gm_d_vs_a)} grade moves vs A) | "
              f"D-vs-C diff: {d_vs_c_affected} ({len(gm_d_vs_c)} grade moves vs C)")
        print(f"  Additive count changes (L3): {len(additive_changed)} products")

        cat_out = {
            "category": category,
            "n_bsip1_records": n_bsip1,
            "n_baseline_products": n_baseline,
            "n_scored": n_scored,
            "zero_drift_col_a": drift_check,
            "additive_count_changes": additive_changed,
            "grade_movers_d_vs_a": gm_d_vs_a,
            "grade_movers_d_vs_c": gm_d_vs_c,
            "movement_table": rows,
        }
        write_json(OUT_DIR / f"{category}_parse_fix.json", cat_out)
        all_results[category] = cat_out

    # -----------------------------------------------------------------------
    # Cookies-specific: L3 verification + G9 inversion re-run
    # -----------------------------------------------------------------------
    print(f"\n{'='*72}")
    print("COOKIES-SPECIFIC: L3 ADDITIVE VERIFICATION + G9 RE-RUN")
    print(f"{'='*72}")

    cookies_bsip1 = collect_bsip1_records("cookies_coffee")
    cookies_shelf = load_shelf_flags("cookies_coffee")
    cookies_sr = load_shelf_rel("cookies_coffee")

    # Produce fresh traces with parse-fix ON (col D config) for G9
    print(f"\nProducing fresh cookies traces with parse-fix ON for G9...")
    _apply_env_flags({**cookies_shelf,
                      "BARI_W4_WFI_V1": "on", "BARI_D4_SCORE_V1": "on",
                      "BARI_ADDITIVE_PARSE_FIX_V1": "on"})
    engine = _reload_engine_and_extractor()
    apply_shelf_rel(cookies_sr, engine)

    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope

    g9_traces = []
    chokita_trace_info = None
    petit_trace_info = None

    for bc, rec in sorted(cookies_bsip1.items()):
        try:
            signals = extract_signals(rec)
            cat_result = classify_category(rec)
            l3 = signals["L3_inferred_classifications"]
            nova_result = infer_nova(rec, l3)
            eval_result = assign_evaluation_scope(rec, cat_result["category"])
            score_result = engine.score_product(rec, signals, cat_result, nova_result, eval_result)
            fse = score_result.get("final_score_estimate") if isinstance(score_result, dict) else None

            trace = {
                "input_reference": {"barcode": bc, "product_name_he": rec.get("canonical_name_he", "")},
                "final_score_estimate": fse,
                "evaluation_status": score_result.get("evaluation_status", "scored") if isinstance(score_result, dict) else "error",
                "confidence_band": score_result.get("confidence_band", "medium") if isinstance(score_result, dict) else "medium",
                "L1_observed_signals": signals.get("L1_observed_signals", {}),
                "L3_inferred_classifications": l3,
            }
            g9_traces.append(trace)

            if bc == CHOKITA_BC:
                chokita_trace_info = {
                    "barcode": bc,
                    "name": rec.get("canonical_name_he", ""),
                    "final_score": fse,
                    "grade": _grade(fse),
                    "additive_marker_count": l3.get("additive_marker_count"),
                    "additive_categories": l3.get("additive_categories"),
                    "has_flavor_enhancer": l3.get("has_flavor_enhancer"),
                    "additive_quality": score_result.get("additive_quality") if isinstance(score_result, dict) else None,
                    "whole_food_integrity": score_result.get("whole_food_integrity") if isinstance(score_result, dict) else None,
                }
            if bc == PETIT_BC:
                petit_trace_info = {
                    "barcode": bc,
                    "name": rec.get("canonical_name_he", ""),
                    "final_score": fse,
                    "grade": _grade(fse),
                    "additive_marker_count": l3.get("additive_marker_count"),
                    "additive_categories": l3.get("additive_categories"),
                    "has_flavor_enhancer": l3.get("has_flavor_enhancer"),
                }
        except Exception as exc:
            print(f"    [WARN] score error for {bc}: {exc}")

    print(f"  Produced {len(g9_traces)} fresh traces for G9")

    # G9 run
    print(f"\nRunning G9 inversion invariant on {len(g9_traces)} cookies traces...")
    g9_result = run_g9_on_traces(g9_traces)
    print(f"  G9 status: {g9_result['status']} | Firing pairs: {g9_result['firing_pairs']}")
    for line in g9_result["lines"][:20]:
        print(f"  {line}")

    # -----------------------------------------------------------------------
    # Chokita / Petit-Beurre inversion resolution
    # -----------------------------------------------------------------------
    print(f"\n{'='*72}")
    print("CHOKITA / PETIT-BEURRE INVERSION CHECK")
    print(f"{'='*72}")

    if chokita_row and petit_row:
        print(f"\nChokita ({CHOKITA_BC}):")
        print(f"  Col A (baseline):  {chokita_row.get('col_a_score')}/{chokita_row.get('col_a_grade')}")
        print(f"  Col C (+WFI+D4):   {chokita_row.get('col_c_score')}/{chokita_row.get('col_c_grade')}")
        print(f"  Col D (+ParseFix): {chokita_row.get('col_d_score')}/{chokita_row.get('col_d_grade')}")
        if chokita_l3_a:
            print(f"  L3 additive (col A): count={chokita_l3_a.get('additive_marker_count')} cats={chokita_l3_a.get('additive_categories')}")
        if chokita_l3_d:
            print(f"  L3 additive (col D): count={chokita_l3_d.get('additive_marker_count')} cats={chokita_l3_d.get('additive_categories')}")
        if chokita_trace_info:
            print(f"  Full trace (col D):  score={chokita_trace_info['final_score']}/{chokita_trace_info['grade']} "
                  f"additive_quality={chokita_trace_info.get('additive_quality')} "
                  f"whole_food_integrity={chokita_trace_info.get('whole_food_integrity')}")

        print(f"\nPetit-Beurre ({PETIT_BC}):")
        print(f"  Col A (baseline):  {petit_row.get('col_a_score')}/{petit_row.get('col_a_grade')}")
        print(f"  Col C (+WFI+D4):   {petit_row.get('col_c_score')}/{petit_row.get('col_c_grade')}")
        print(f"  Col D (+ParseFix): {petit_row.get('col_d_score')}/{petit_row.get('col_d_grade')}")
        if petit_trace_info:
            print(f"  L3 additive (col D): count={petit_trace_info.get('additive_marker_count')} cats={petit_trace_info.get('additive_categories')}")

        # Inversion resolution
        chokita_d = chokita_row.get("col_d_score")
        petit_d = petit_row.get("col_d_score")
        chokita_c = chokita_row.get("col_c_score")
        petit_c = petit_row.get("col_c_score")

        print(f"\nInversion resolution:")
        print(f"  Col C (pre-fix):  Chokita={chokita_c} PB={petit_c} → {'RESOLVED (PB>=Chokita)' if (petit_c is not None and chokita_c is not None and petit_c >= chokita_c) else 'NOT RESOLVED'}")
        print(f"  Col D (post-fix): Chokita={chokita_d} PB={petit_d} → {'RESOLVED (PB>=Chokita)' if (petit_d is not None and chokita_d is not None and petit_d >= chokita_d) else 'NOT RESOLVED'}")
        if petit_d is not None and chokita_d is not None:
            residual_gap = round(chokita_d - petit_d, 1)
            print(f"  Residual gap (Chokita - PB): {residual_gap:+.1f} points "
                  f"({'PB leads' if residual_gap < 0 else 'Chokita leads' if residual_gap > 0 else 'tied'})")
    else:
        print(f"  [WARN] Chokita or PB not found in corpus")
        if not chokita_row: print(f"  Chokita ({CHOKITA_BC}) not found")
        if not petit_row: print(f"  Petit-Beurre ({PETIT_BC}) not found")

    # -----------------------------------------------------------------------
    # Aggregate summary
    # -----------------------------------------------------------------------
    print(f"\n{'='*72}")
    print("AGGREGATE SUMMARY")
    print(f"{'='*72}")

    a_total_mm = sum(d["mismatches"] for d in baseline_drift_summary)
    a_total_match = sum(d["matched"] for d in baseline_drift_summary)
    zero_drift_cats = [d["category"] for d in baseline_drift_summary if d["zero_drift_pass"]]
    drift_cats = [d["category"] for d in baseline_drift_summary if not d["zero_drift_pass"]]
    print(f"\nCol A zero-drift: {a_total_match} matched, {a_total_mm} mismatches")
    print(f"  PARSE_FIX_V1=OFF → zero-drift categories: {', '.join(zero_drift_cats)}")
    print(f"  Pre-existing drift (not from new flags): {', '.join(drift_cats)}")

    d_nonzero = [d for d in agg_d_deltas if d != 0]
    d_vs_c_nonzero = [d for d in agg_d_vs_c_deltas if d != 0]
    print(f"\nCol D vs A (full stack W4+D4+ParseFix):")
    print(f"  Products affected: {len(d_nonzero)}/{len(agg_d_deltas)}")
    print(f"  Grade movers vs A: {len(agg_grade_movers_d_vs_a)}")
    if d_nonzero:
        ds = delta_stats(d_nonzero)
        print(f"  Delta distribution: min={ds['min']} median={ds['median']} max={ds['max']} stdev={ds['stdev']}")

    print(f"\nCol D vs C (parse-fix incremental over D4+WFI):")
    print(f"  Products affected: {len(d_vs_c_nonzero)}/{len(agg_d_vs_c_deltas)}")
    print(f"  Grade movers vs C: {len(agg_grade_movers_d_vs_c)}")
    if d_vs_c_nonzero:
        ds = delta_stats(d_vs_c_nonzero)
        print(f"  Delta distribution: min={ds['min']} median={ds['median']} max={ds['max']} stdev={ds['stdev']}")

    # Direction check (expected: downward)
    upward_d_vs_a = [m for m in agg_grade_movers_d_vs_a if (m["delta"] or 0) > 0]
    downward_d_vs_a = [m for m in agg_grade_movers_d_vs_a if (m["delta"] or 0) < 0]
    print(f"\nDirection check (grade movers D vs A):")
    print(f"  Downward (expected): {len(downward_d_vs_a)}")
    print(f"  Upward (flag if any): {len(upward_d_vs_a)}")
    for m in upward_d_vs_a[:10]:
        print(f"  [UPWARD] [{m['category']}] {m['barcode']} {m['name'][:40]}: "
              f"{m['score_before']}/{m['grade_before']} → {m['score_after']}/{m['grade_after']} Δ{m['delta']:+.1f}")

    # Threshold crossings
    print(f"\nAdditive threshold crossings (via parse-fix L3 change):")
    print(f"  3_PLUS (cap=72) crossings: {sum(1 for t in threshold_crossings if t['threshold']=='3_PLUS')}")
    print(f"  5_PLUS (cap=60) crossings: {sum(1 for t in threshold_crossings if t['threshold']=='5_PLUS')}")
    for t in threshold_crossings[:20]:
        print(f"  [{t['category']}] BC={t['barcode']} {t['name'][:40]} "
              f"{t['threshold']}: {t['count_before']}→{t['count_after']}")

    # Grade movers table
    print(f"\nAll grade movers (D vs A), top 30:")
    for m in agg_grade_movers_d_vs_a[:30]:
        print(f"  [{m['category']}] {m['barcode']} {m['name'][:40]}: "
              f"{m['score_before']}/{m['grade_before']} → {m['score_after']}/{m['grade_after']} Δ{m['delta']:+.1f}")

    # Save aggregate report
    agg_report = {
        "run_id": f"parse_fix_task395_{run_ts}",
        "generated_at": run_ts,
        "flag_set": {
            "col_a": {"BARI_W4_WFI_V1": "off", "BARI_D4_SCORE_V1": "off", "BARI_ADDITIVE_PARSE_FIX_V1": "off"},
            "col_d": {"BARI_W4_WFI_V1": "on", "BARI_D4_SCORE_V1": "on", "BARI_ADDITIVE_PARSE_FIX_V1": "on"},
        },
        "total_products_scored": total_scored,
        "zero_drift_col_a": {
            "total_matched": a_total_match, "total_mismatches": a_total_mm,
            "pass": a_total_mm == 0,
            "zero_drift_categories": zero_drift_cats,
            "pre_existing_drift_categories": drift_cats,
        },
        "col_d_vs_a_summary": {
            "affected": len(d_nonzero), "total": len(agg_d_deltas),
            "grade_movers": len(agg_grade_movers_d_vs_a),
            "upward_grade_movers": len(upward_d_vs_a),
            "delta_stats": delta_stats(d_nonzero),
        },
        "col_d_vs_c_summary": {
            "affected": len(d_vs_c_nonzero), "total": len(agg_d_vs_c_deltas),
            "grade_movers": len(agg_grade_movers_d_vs_c),
            "delta_stats": delta_stats(d_vs_c_nonzero),
        },
        "chokita_inversion": {
            "chokita_bc": CHOKITA_BC,
            "petit_bc": PETIT_BC,
            "chokita_col_a_score": chokita_row.get("col_a_score") if chokita_row else None,
            "chokita_col_c_score": chokita_row.get("col_c_score") if chokita_row else None,
            "chokita_col_d_score": chokita_row.get("col_d_score") if chokita_row else None,
            "petit_col_a_score": petit_row.get("col_a_score") if petit_row else None,
            "petit_col_c_score": petit_row.get("col_c_score") if petit_row else None,
            "petit_col_d_score": petit_row.get("col_d_score") if petit_row else None,
            "chokita_l3_col_a": chokita_l3_a,
            "chokita_l3_col_d": chokita_l3_d,
            "chokita_full_trace_col_d": chokita_trace_info,
            "petit_trace_col_d": petit_trace_info,
            "inversion_resolved_col_c": (
                chokita_row is not None and petit_row is not None and
                chokita_row.get("col_c_score") is not None and
                petit_row.get("col_c_score") is not None and
                petit_row["col_c_score"] >= chokita_row["col_c_score"]
            ),
            "inversion_resolved_col_d": (
                chokita_row is not None and petit_row is not None and
                chokita_row.get("col_d_score") is not None and
                petit_row.get("col_d_score") is not None and
                petit_row["col_d_score"] >= chokita_row["col_d_score"]
            ),
        },
        "g9_result": g9_result,
        "additive_threshold_crossings": threshold_crossings,
        "grade_movers_d_vs_a": agg_grade_movers_d_vs_a,
        "grade_movers_d_vs_c": agg_grade_movers_d_vs_c,
        "per_category": {
            cat: {
                "n_scored": v["n_scored"],
                "zero_drift_pass": v["zero_drift_col_a"]["zero_drift_pass"],
                "additive_count_changes": len(v["additive_count_changes"]),
                "grade_movers_d_vs_a": len(v["grade_movers_d_vs_a"]),
                "grade_movers_d_vs_c": len(v["grade_movers_d_vs_c"]),
            }
            for cat, v in all_results.items()
        },
    }
    agg_path = OUT_DIR / "aggregate_parse_fix_report.json"
    agg_sha = write_json(agg_path, agg_report)
    print(f"\nAggregate report: {agg_path}")
    print(f"  sha256: {agg_sha}")

    # Exit code
    inversion_resolved = agg_report["chokita_inversion"]["inversion_resolved_col_d"]
    flag_leaks_into_a = a_total_mm > 0 and len(zero_drift_cats) == 0
    if flag_leaks_into_a:
        print(f"\n[FAIL] PARSE_FIX flag leaks into Col A (zero zero-drift categories). Stop.")
        sys.exit(1)
    elif not inversion_resolved:
        print(f"\n[PARTIAL] Inversion NOT resolved in col D. Report results.")
        sys.exit(0)
    else:
        print(f"\n[PASS] Flag does not leak into col A. Inversion resolved in col D.")
        sys.exit(0)


if __name__ == "__main__":
    main()
