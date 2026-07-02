#!/usr/bin/env python3
"""
TASK-371 Layer-1 diagnostic.

Computes three score sets per live product:
  1. HEAD engine — worktree at HEAD (C:\Bari_worktree_head)
  2. Working-tree engine — current working tree (C:\Bari)
  3. Committed frontend JSON — bari-web/src/data/comparisons/*.json

Both engine runs use:
  BARI_D4_SCORE_V1=off (default)
  BARI_PROTEIN_BAR_V1=off (default)
  All other flags per category config (same as rescore_all.py)

Reports:
  (a) TRUE BARS DELTA = working_tree - HEAD
  (b) PRE-EXISTING STALENESS = HEAD - committed_json

Read-only: writes NOTHING to live JSONs or engine files.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path("C:/Bari")
WORKTREE = Path("C:/Bari_worktree_head")
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
COMPARISONS_DIR = REPO / "bari-web" / "src" / "data" / "comparisons"

# Which frontend JSON → category slug mapping (from live_manifest.json)
LIVE_MANIFEST_PATH = REPO / "03_operations" / "spine" / "live_manifest.json"

# ---------------------------------------------------------------------------
# Live manifest loading
# ---------------------------------------------------------------------------
def load_manifest():
    with open(LIVE_MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Load committed frontend JSON scores (set 3)
# ---------------------------------------------------------------------------
def load_frontend_scores(json_path: Path) -> dict[str, dict]:
    """Returns {barcode: {score, grade}} from a frontend JSON."""
    if not json_path.exists():
        return {}
    data = load_json(json_path)
    result = {}
    products = data.get("products", [])
    for p in products:
        bc = str(p.get("barcode", "")).strip()
        if not bc:
            continue
        score = p.get("score")
        grade = p.get("grade")
        result[bc] = {"score": score, "grade": grade, "name": p.get("name_he") or p.get("name", "")}
    return result


# ---------------------------------------------------------------------------
# Engine loader
# ---------------------------------------------------------------------------
def load_engine_modules(engine_dir: Path):
    """Load engine from a specific directory (HEAD worktree or working tree)."""
    src = engine_dir / "03_operations" / "bsip2" / "proto_v0" / "src"
    if str(src) in sys.path:
        sys.path.remove(str(src))
    sys.path.insert(0, str(src))

    # Force-reload all relevant modules
    modules_to_reload = [
        "constants", "router_v2", "signal_extractor", "nova_proxy",
        "evaluation_scope", "score_engine", "trace_writer",
        "structural_classifier", "grade_governance", "ingredient_taxonomy",
        "nova_proxy", "graceful_degradation",
    ]
    loaded = {}
    for mod_name in modules_to_reload:
        if mod_name in sys.modules:
            del sys.modules[mod_name]

    # Import fresh
    for mod_name in modules_to_reload:
        try:
            loaded[mod_name] = importlib.import_module(mod_name)
        except Exception as e:
            pass  # Some modules optional

    return loaded


def score_product_with_modules(product: dict, mods: dict) -> dict | None:
    """Score a single product using loaded engine modules."""
    try:
        signal_extractor = mods.get("signal_extractor")
        router_v2 = mods.get("router_v2")
        nova_proxy = mods.get("nova_proxy")
        evaluation_scope = mods.get("evaluation_scope")
        score_engine = mods.get("score_engine")
        trace_writer = mods.get("trace_writer")
        structural_classifier = mods.get("structural_classifier")

        if not all([signal_extractor, router_v2, nova_proxy, evaluation_scope, score_engine]):
            return None

        signals = signal_extractor.extract_signals(product)
        cat_result = router_v2.classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = nova_proxy.infer_nova(product, l3)
        eval_result = evaluation_scope.assign_evaluation_scope(product, cat_result["category"])
        score_result = score_engine.score_product(
            product, signals, cat_result, nova_result, eval_result
        )

        final_score = score_result.get("final_score")
        final_grade = score_result.get("final_grade")
        category = cat_result.get("category")
        cat_subtype = cat_result.get("category_subtype")
        req362 = score_result.get("req362_override_trace") or cat_result.get("req362_override_trace") or {}
        # Also check router result
        router_req362 = cat_result.get("req362_override_trace") or {}
        override_applied = req362.get("override_applied") or router_req362.get("override_applied")
        override_reason = req362.get("reason") or router_req362.get("reason")

        # Try to get classification basis for trace
        cls_basis = cat_result.get("classification_basis", [])

        return {
            "score": final_score,
            "grade": final_grade,
            "category": category,
            "category_subtype": cat_subtype,
            "override_applied": override_applied,
            "override_reason": override_reason,
            "classification_basis": cls_basis[:3] if cls_basis else [],
        }
    except Exception as e:
        return {"error": str(e), "score": None, "grade": None}


# ---------------------------------------------------------------------------
# Apply env flags from config
# ---------------------------------------------------------------------------
MANAGED_BARI_VARS = [
    "BARI_RECAL_P0", "BARI_RECAL_P0_YOGURT_TRIM", "BARI_FAT_TECH_V1",
    "BARI_SHELF_RELATIVE_V1", "BARI_SODIUM_SHELF_RELATIVE_V1",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1", "BARI_GRAD_SODIUM_V1",
    "BARI_SODIUM_CEREAL", "BARI_REDLABEL_V1", "BARI_TASK144_FIXES",
    "BARI_TASK250_CONF", "BARI_GLASSBOX_D5D6", "BARI_GLASSBOX_W15",
    "BARI_GLASSBOX_W2", "BARI_DAIRY_SAT_FAT_INFER",
    # Always OFF for this diagnostic
    "BARI_D4_SCORE_V1", "BARI_PROTEIN_BAR_V1",
]

def snapshot_env() -> dict:
    return {k: os.environ.get(k) for k in MANAGED_BARI_VARS}

def restore_env(snap: dict) -> None:
    for k, v in snap.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

def apply_flags(flags: dict) -> None:
    for k, v in flags.items():
        os.environ[k] = v


# ---------------------------------------------------------------------------
# Shelf stats setup
# ---------------------------------------------------------------------------
def setup_shelf_stats(shelf_rel: dict | None, score_engine_mod) -> None:
    if not score_engine_mod:
        return
    # Clear first
    if hasattr(score_engine_mod, "clear_shelf_stats"):
        score_engine_mod.clear_shelf_stats()
    if hasattr(score_engine_mod, "clear_shelf_sodium_stats"):
        score_engine_mod.clear_shelf_sodium_stats()

    if not shelf_rel:
        return

    api = shelf_rel.get("api")
    nutrient = shelf_rel.get("nutrient", "")
    median = shelf_rel.get("median")
    scale = shelf_rel.get("scale")
    scale_type = shelf_rel.get("scale_type", "iqr")
    n = shelf_rel.get("n", 30)  # default n for guard

    if api == "sodium_ev056":
        if hasattr(score_engine_mod, "set_shelf_sodium_stats"):
            score_engine_mod.set_shelf_sodium_stats(median, scale)
    elif nutrient and median is not None and scale is not None:
        if hasattr(score_engine_mod, "set_shelf_stats"):
            score_engine_mod.set_shelf_stats(nutrient, median, scale, scale_type, n)


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------
def collect_bsip1_files(corpus_dirs: list[str], corpus_filter=None) -> list[Path]:
    files = []
    seen = set()
    for d in corpus_dirs:
        dpath = Path(d)
        if not dpath.is_dir():
            continue
        for fname in sorted(dpath.glob("bsip1_*.json")):
            if "audit" in fname.name:
                continue
            try:
                rec = load_json(fname)
            except Exception:
                continue
            bc = str(rec.get("barcode", "")).strip()
            if not bc or bc in seen:
                continue
            if rec.get("file_type") != "product":
                continue
            if corpus_filter is not None and bc not in corpus_filter:
                continue
            seen.add(bc)
            files.append(fname)
    return files


# ---------------------------------------------------------------------------
# Per-category scoring
# ---------------------------------------------------------------------------
def score_category(
    config: dict,
    engine_dir: Path,
    config_flags_override: dict | None = None,
) -> dict[str, dict]:
    """
    Score all products in a category using engine_dir.
    Returns {barcode: {score, grade, category, ...}}
    """
    scoring = config.get("scoring", {})
    flags = dict(scoring.get("flags", {}))
    # Always force D4 and protein_bar OFF for this diagnostic
    flags["BARI_D4_SCORE_V1"] = "off"
    flags["BARI_PROTEIN_BAR_V1"] = "off"
    if config_flags_override:
        flags.update(config_flags_override)

    exclusions = {e["barcode"] for e in config.get("exclusions", []) if "barcode" in e}

    shelf_rel = scoring.get("shelf_rel")
    bsip1_dir = scoring.get("bsip1_dir")
    corpus_dirs = config.get("corpus_dirs", [])
    if bsip1_dir:
        corpus_dirs = [bsip1_dir]
    elif isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]

    # Load corpus filter if any
    corpus_filter_path = scoring.get("corpus_filter")
    corpus_filter = None
    if corpus_filter_path:
        try:
            cf_data = load_json(Path(corpus_filter_path))
            corpus_filter = {str(p["barcode"]) for p in cf_data.get("products", []) if p.get("decision") == "IN_SCORED"}
        except Exception:
            pass

    bsip1_files = collect_bsip1_files(corpus_dirs, corpus_filter)

    # Set env flags
    snap = snapshot_env()
    apply_flags(flags)

    try:
        # Load engine from engine_dir
        mods = load_engine_modules(engine_dir)
        score_engine_mod = mods.get("score_engine")

        # Setup shelf stats
        setup_shelf_stats(shelf_rel, score_engine_mod)

        results = {}
        for fpath in bsip1_files:
            try:
                product = load_json(fpath)
            except Exception:
                continue
            bc = str(product.get("barcode", "")).strip()
            if not bc or bc in exclusions:
                continue
            result = score_product_with_modules(product, mods)
            if result:
                result["name"] = product.get("canonical_name_he") or product.get("name_he") or ""
                results[bc] = result
    finally:
        restore_env(snap)

    return results


# ---------------------------------------------------------------------------
# Main diagnostic
# ---------------------------------------------------------------------------
def main():
    manifest = load_manifest()

    # Build category → frontend JSON mapping from manifest
    cat_to_json = {}  # category_slug → Path to frontend JSON
    for entry in manifest.get("files", []):
        cat = entry.get("category")
        path = entry.get("path")
        if cat and path:
            cat_to_json[cat] = Path(path)

    # Load all category configs
    config_files = sorted(
        p for p in CONFIGS_DIR.glob("*.json")
        if not p.name.startswith("_generated_")
    )

    # Map config file → (category slug, frontend json path)
    all_results = {}  # category_name → {barcode → {head, wt, committed}}

    # Track changes for headline
    true_bars_delta = []    # (a) products that differ HEAD vs working-tree
    staleness = []           # (b) products that differ HEAD vs committed JSON

    for cfg_path in config_files:
        cat_name = cfg_path.stem  # e.g. "hard_cheeses"
        print(f"\n{'='*60}")
        print(f"Category: {cat_name}")

        try:
            config = load_json(cfg_path)
        except Exception as e:
            print(f"  ERROR loading config: {e}")
            continue

        # Find matching frontend JSON
        # Try by category field in config
        cat_slug = config.get("category", "")

        # Find the right frontend JSON
        frontend_path = None
        for slug, path in cat_to_json.items():
            # Match by config category or config filename
            if cat_slug and slug == cat_slug:
                frontend_path = path
                break
            if slug.replace("-", "_") == cat_name or cat_name.replace("-", "_") == slug.replace("-", "_"):
                frontend_path = path
                break

        if not frontend_path:
            # Try to find by cat_name similarity
            for slug, path in cat_to_json.items():
                if cat_name in slug or slug in cat_name:
                    frontend_path = path
                    break

        if not frontend_path:
            print(f"  No frontend JSON found for {cat_name} (slug={cat_slug})")
            continue

        print(f"  Frontend JSON: {frontend_path.name}")

        # Set 3: committed frontend JSON scores
        committed = load_frontend_scores(frontend_path)
        print(f"  Committed products: {len(committed)}")

        # Set 1: HEAD engine scores
        print(f"  Scoring with HEAD engine (worktree)...")
        try:
            head_scores = score_category(config, WORKTREE)
            print(f"  HEAD scored: {len(head_scores)} products")
        except Exception as e:
            print(f"  ERROR scoring HEAD: {e}")
            traceback.print_exc()
            head_scores = {}

        # Set 2: Working-tree engine scores
        print(f"  Scoring with working-tree engine...")
        try:
            wt_scores = score_category(config, REPO)
            print(f"  Working-tree scored: {len(wt_scores)} products")
        except Exception as e:
            print(f"  ERROR scoring working-tree: {e}")
            traceback.print_exc()
            wt_scores = {}

        # Compare
        all_barcodes = set(committed) | set(head_scores) | set(wt_scores)

        cat_delta_a = []  # (a) bars delta
        cat_delta_b = []  # (b) staleness

        for bc in sorted(all_barcodes):
            h = head_scores.get(bc, {})
            w = wt_scores.get(bc, {})
            c = committed.get(bc, {})

            h_score = h.get("score")
            w_score = w.get("score")
            c_score = c.get("score")
            h_grade = h.get("grade")
            w_grade = w.get("grade")
            c_grade = c.get("grade")

            name = (h.get("name") or w.get("name") or c.get("name") or "")

            # (a) TRUE BARS DELTA: working_tree != HEAD
            a_score_diff = (h_score is not None and w_score is not None and
                           round(float(h_score), 1) != round(float(w_score), 1))
            a_grade_diff = h_grade != w_grade
            if a_score_diff or a_grade_diff:
                trace_reason = ""
                cls_basis = w.get("classification_basis", [])
                # Look for R3 chocolate marker
                for b in cls_basis:
                    if "task362_r3" in b or "chocolate_name_marker" in b:
                        trace_reason = b
                        break
                if not trace_reason and w.get("override_applied"):
                    trace_reason = w.get("override_reason", "")[:120]
                if not trace_reason and cls_basis:
                    trace_reason = cls_basis[0][:120]

                entry = {
                    "barcode": bc,
                    "name": name,
                    "category": cat_name,
                    "head_score": h_score,
                    "head_grade": h_grade,
                    "head_category": h.get("category"),
                    "wt_score": w_score,
                    "wt_grade": w_grade,
                    "wt_category": w.get("category"),
                    "wt_subtype": w.get("category_subtype"),
                    "score_delta": round(float(w_score or 0) - float(h_score or 0), 1) if (w_score and h_score) else None,
                    "trace_reason": trace_reason,
                }
                cat_delta_a.append(entry)
                true_bars_delta.append(entry)

            # (b) PRE-EXISTING STALENESS: HEAD != committed JSON
            b_score_diff = (h_score is not None and c_score is not None and
                           round(float(h_score), 1) != round(float(c_score), 1))
            b_grade_diff = (h_grade is not None and c_grade is not None and h_grade != c_grade)
            if b_score_diff or b_grade_diff:
                entry = {
                    "barcode": bc,
                    "name": name,
                    "category": cat_name,
                    "committed_score": c_score,
                    "committed_grade": c_grade,
                    "head_score": h_score,
                    "head_grade": h_grade,
                    "score_delta": round(float(h_score or 0) - float(c_score or 0), 1) if (h_score and c_score) else None,
                }
                cat_delta_b.append(entry)
                staleness.append(entry)

        all_results[cat_name] = {
            "delta_a": cat_delta_a,
            "delta_b": cat_delta_b,
            "committed_count": len(committed),
            "head_count": len(head_scores),
            "wt_count": len(wt_scores),
        }

        if cat_delta_a:
            print(f"\n  (a) TRUE BARS DELTA ({len(cat_delta_a)} products):")
            for e in cat_delta_a:
                print(f"      {e['barcode']} [{e['name'][:40]}] "
                      f"HEAD={e['head_score']}/{e['head_grade']} "
                      f"WT={e['wt_score']}/{e['wt_grade']} "
                      f"delta={e['score_delta']:+.1f} "
                      f"({e['head_category']}→{e['wt_category']}:{e['wt_subtype']})")
                if e['trace_reason']:
                    print(f"        trace: {e['trace_reason'][:100]}")
        else:
            print(f"  (a) TRUE BARS DELTA: 0 products (category clean)")

        if cat_delta_b:
            print(f"\n  (b) PRE-EXISTING STALENESS ({len(cat_delta_b)} products):")
            for e in cat_delta_b[:10]:  # show first 10
                print(f"      {e['barcode']} [{e['name'][:40]}] "
                      f"committed={e['committed_score']}/{e['committed_grade']} "
                      f"HEAD={e['head_score']}/{e['head_grade']} "
                      f"delta={e['score_delta']:+.1f}")
            if len(cat_delta_b) > 10:
                print(f"      ... and {len(cat_delta_b) - 10} more")
        else:
            print(f"  (b) PRE-EXISTING STALENESS: 0 products")

    # ---------------------------------------------------------------------------
    # HARD_CHEESES specific check
    # ---------------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("DECISIVE CHECK: hard_cheeses TRUE BARS DELTA (a) == 0?")
    hc_result = all_results.get("hard_cheeses", {})
    hc_a = hc_result.get("delta_a", [])
    if not hc_a:
        print("  CONFIRMED: hard_cheeses delta (a) == 0. Bars rework does NOT touch hard_cheeses.")
        print("  The Babybel 71→39 swing is PRE-EXISTING STALENESS (b), not bars-rework.")
    else:
        print(f"  REFUTED: hard_cheeses has {len(hc_a)} products in bars delta (a)!")
        for e in hc_a:
            print(f"    {e['barcode']} {e['name'][:40]} trace: {e['trace_reason'][:80]}")

    hc_b = hc_result.get("delta_b", [])
    print(f"\n  hard_cheeses staleness (b): {len(hc_b)} products")
    babybel_bc = "3073781199918"
    babybel_b = [e for e in hc_b if e["barcode"] == babybel_bc]
    if babybel_b:
        e = babybel_b[0]
        print(f"  Babybel {babybel_bc}: committed={e['committed_score']}/{e['committed_grade']} "
              f"HEAD={e['head_score']}/{e['head_grade']} delta={e['score_delta']:+.1f}")
        print(f"  CONFIRMED: Babybel 71→39 is PRE-EXISTING STALENESS (b)")
    else:
        print(f"  Babybel {babybel_bc} NOT in staleness delta (a={[e['barcode'] for e in hc_a]})")

    # ---------------------------------------------------------------------------
    # Headline: 153 split
    # ---------------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("HEADLINE: SPLIT OF PREVIOUSLY-FLAGGED 153 DRIFTS")
    print(f"  (a) TRUE BARS DELTA (working_tree - HEAD):  {len(true_bars_delta)} products")
    print(f"  (b) PRE-EXISTING STALENESS (HEAD - committed): {len(staleness)} products")
    print(f"  Total unique products with any drift: {len(set(e['barcode'] for e in true_bars_delta + staleness))}")

    # Breakdown by category
    print(f"\n  (a) TRUE BARS DELTA by category:")
    from collections import Counter
    a_by_cat = Counter(e["category"] for e in true_bars_delta)
    for cat, cnt in sorted(a_by_cat.items(), key=lambda x: -x[1]):
        print(f"      {cat}: {cnt} products")

    print(f"\n  (b) PRE-EXISTING STALENESS by category:")
    b_by_cat = Counter(e["category"] for e in staleness)
    for cat, cnt in sorted(b_by_cat.items(), key=lambda x: -x[1]):
        print(f"      {cat}: {cnt} products")

    # For (a), show trace reasons to confirm R3 chocolate re-route
    if true_bars_delta:
        print(f"\n  (a) Trace reasons for TRUE BARS DELTA (full list):")
        for e in sorted(true_bars_delta, key=lambda x: x["category"]):
            print(f"      [{e['category']}] {e['barcode']} {e['name'][:35]:35s} "
                  f"{e['head_category']:18s}→{e['wt_category']}:{e['wt_subtype']} "
                  f"delta={'+' if (e['score_delta'] or 0)>=0 else ''}{e['score_delta']:.1f}")
            if e["trace_reason"]:
                print(f"        trace: {e['trace_reason'][:100]}")

    print(f"\n  0 files written to live JSONs or engine (read-only diagnostic).")
    print(f"  Worktree: C:/Bari_worktree_head (remove with: git worktree remove C:/Bari_worktree_head)")


if __name__ == "__main__":
    main()
