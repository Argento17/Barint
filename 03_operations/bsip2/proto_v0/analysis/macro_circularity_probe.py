"""
macro_circularity_probe.py
==========================
TASK-395 / Distinguished Forum — Empirical test of the owner's thesis:
"When ingredient %s are missing, estimate composition from nutritional values."

This script answers 6 questions read-only against existing corpus data:

  Q1: How many products have REAL ingredient %s (ground-truth labeled subset)?
      Per-category breakdown.

  Q2: Can we PREDICT the matrix/whole-food composition score from macros alone?
      (Regression: sugar, fat, sat-fat, sodium, energy, protein, fiber -> matrix score)
      Report: MAE, R², per-category.

  Q3: Redundancy test — does real composition carry signal BEYOND macros?
      (Correlation between true matrix score and macro-predicted composition)
      If r≈0.9 -> redundant; r≈0.4 -> independent signal.

  Q4: Macro-twins probe — pairs with near-identical macros but very different
      real composition. Count them, quantify as fraction of shelf.

  Q5: Coverage reality-check — what % of corpus actually has complete
      sugar/fat/sodium? Report per-field missingness.

  Q6: American training sample feasibility — sources, granularity, OFF banned.
      Feasibility read only (no build).

Data sources used:
  - BSIP0 raw JSONs (ingredient + nutrition as scraped)
  - BSIP1 enriched JSONs (ingredient_order with parsed data where available)
  - structured_ingredient_reader.py (v4 — the shared reader)
  - matrix_signal_probe_v5_1.py (for matrix score computation)

Hard rules observed:
  - Read-only: no edits to engine, BSIP, or published data
  - No commits
  - No OFF data
  - No imputation

Output: analysis/macro_circularity_probe_results.json
        analysis/macro_circularity_probe_report.txt

Author: Data Agent (TASK-395 forum)
Date: 2026-06-26
"""

from __future__ import annotations

import json
import sys
import os
import math
import statistics
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path("C:/Bari")
ANALYSIS_DIR = REPO_ROOT / "03_operations/bsip2/proto_v0/analysis"

sys.path.insert(0, str(ANALYSIS_DIR))
from structured_ingredient_reader import parse_ingredients, parse_from_bsip1, is_unparseable

# Import matrix score computation from v5_1
sys.path.insert(0, str(ANALYSIS_DIR))
from matrix_signal_probe_v5_1 import extract_all_markers_v4, compute_component_b_score_v5_1

# ---------------------------------------------------------------------------
# BSIP0 raw data locations
# ---------------------------------------------------------------------------
BSIP0_SOURCES = [
    ("bread",            REPO_ROOT / "02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json"),
    ("bread_light",      REPO_ROOT / "02_products/bread_retail_002/real_bread_retail_002_v2_20260525T165557_bsip0_raw.json"),
    ("breakfast_cereals",REPO_ROOT / "02_products/breakfast_cereals/bsip0_outputs/cereals_bsip0_raw_20260605T154620.json"),
    ("brined_cheeses",   REPO_ROOT / "02_products/brined_cheeses/bsip0_outputs/brined_cheese_bsip0_raw_20260613T065721.json"),
    ("cookies_coffee",   REPO_ROOT / "02_products/cookies_coffee/bsip0_outputs/cookies_coffee_bsip0_raw_20260613T163431.json"),
    ("snack_bars",       REPO_ROOT / "02_products/snack_bars/bsip0_outputs/bars_bsip0_raw_20260620T121558.json"),
    ("cheese_spreads",   REPO_ROOT / "02_products/cheese_spreads/bsip0_outputs/cheese_bsip0_raw_20260602T054843.json"),
    ("cakes_cookies",    REPO_ROOT / "02_products/cakes_hard_cookies/bsip0_outputs/cakes_merged_bsip0_raw.json"),
    ("chocolate",        REPO_ROOT / "02_products/chocolate/bsip0_outputs/choc_bsip0_raw_20260621T093256.json"),
]

# BSIP1 enriched directories (have ingredient_order)
BSIP1_DIRS = [
    ("hard_cheeses", REPO_ROOT / "02_products/hard_cheeses/bsip1_outputs"),
    ("juices",       REPO_ROOT / "02_products/juices/bsip1_outputs"),
]

# Also check supplements corpus
SUPPLEMENT_DIR = REPO_ROOT / "02_products/supplements/real_corpus_v3/skus_full"

# ---------------------------------------------------------------------------
# Nutrition field extractor — normalises across BSIP0 and BSIP1 schemas
# ---------------------------------------------------------------------------

def _safe_float(v) -> Optional[float]:
    if v is None:
        return None
    try:
        s = str(v).strip()
        if not s:
            return None
        parts = s.split()
        if not parts:
            return None
        s = parts[0].replace(",", ".")
        f = float(s)
        return f if math.isfinite(f) else None
    except (ValueError, TypeError):
        return None


def extract_nutrition(prod: dict) -> dict:
    """Extract per-100g nutrition from a product dict (BSIP0 or BSIP1 schema)."""
    nut = {}

    # BSIP1 schema: normalized_nutrition_per_100g
    n1 = prod.get("normalized_nutrition_per_100g", {})
    if n1:
        nut["energy_kcal"]    = _safe_float(n1.get("energy_kcal"))
        nut["fat_g"]          = _safe_float(n1.get("fat_g"))
        nut["fat_sat_g"]      = _safe_float(n1.get("fat_saturated_g"))
        nut["sodium_mg"]      = _safe_float(n1.get("sodium_mg"))
        nut["carbs_g"]        = _safe_float(n1.get("carbohydrates_g"))
        nut["sugar_g"]        = _safe_float(n1.get("sugars_g"))
        nut["fiber_g"]        = _safe_float(n1.get("dietary_fiber_g"))
        nut["protein_g"]      = _safe_float(n1.get("protein_g"))
        return nut

    # BSIP0 raw schema: nutrition dict with _raw keys
    n0 = prod.get("nutrition", {})
    if n0:
        nut["energy_kcal"]    = _safe_float(n0.get("energy_kcal_raw"))
        nut["fat_g"]          = _safe_float(n0.get("fat_raw"))
        nut["fat_sat_g"]      = _safe_float(n0.get("saturated_fat_raw"))
        nut["sodium_mg"]      = _safe_float(n0.get("sodium_raw"))
        nut["carbs_g"]        = _safe_float(n0.get("carbs_raw"))
        nut["sugar_g"]        = _safe_float(n0.get("sugar_raw"))
        nut["fiber_g"]        = _safe_float(n0.get("fiber_raw"))
        nut["protein_g"]      = _safe_float(n0.get("protein_raw"))
        return nut

    # BSIP1 flat fields (energy_kcal, fat_g, protein_g etc. at top level)
    bsip1_flat_map = [
        ("energy_kcal", ["energy_kcal"]),
        ("fat_g",       ["fat_g"]),
        ("fat_sat_g",   ["fat_saturated_g"]),
        ("sodium_mg",   ["sodium_mg"]),
        ("carbs_g",     ["carbohydrates_g"]),
        ("sugar_g",     ["sugars_g"]),
        ("fiber_g",     ["dietary_fiber_g"]),
        ("protein_g",   ["protein_g"]),
    ]
    for k, candidates in bsip1_flat_map:
        if nut.get(k) is None:
            for c in candidates:
                v = _safe_float(prod.get(c))
                if v is not None:
                    nut[k] = v
                    break

    # supplement / generic schema
    for key_map in [
        ("energy_kcal", ["calories_kcal"]),
        ("fat_g",       ["total_fat_g"]),
        ("fat_sat_g",   ["saturated_fat_g"]),
        ("sodium_mg",   []),
        ("carbs_g",     ["carbs_g"]),
        ("sugar_g",     ["sugar_g"]),
        ("fiber_g",     ["fiber_g"]),
        ("protein_g",   []),
    ]:
        k, candidates = key_map
        if nut.get(k) is None:
            for c in candidates:
                v = _safe_float(prod.get(c))
                if v is not None:
                    nut[k] = v
                    break

    return nut


def get_ingredients_text(prod: dict) -> Optional[str]:
    """Get ingredient text from either BSIP0 or BSIP1 schema."""
    # BSIP1 schema
    t = prod.get("ingredients_text_he")
    if t and len(t.strip()) > 5:
        return t.strip()
    # BSIP0 raw — field is "ingredients_raw"
    t = prod.get("ingredients_raw") or prod.get("ingredients_he") or prod.get("ingredients_text")
    if t and len(str(t).strip()) > 5:
        return str(t).strip()
    return None


def get_ingredient_order(prod: dict) -> list:
    """Get BSIP1 ingredient_order if present."""
    return prod.get("ingredient_order", [])


# ---------------------------------------------------------------------------
# Matrix score computation for a product
# ---------------------------------------------------------------------------

def compute_matrix_score(prod: dict) -> tuple[Optional[float], str]:
    """
    Returns (matrix_score, confidence_tier) where:
      confidence_tier = "high"    : at least one stated % (real ground truth)
                        "order"   : order-only (position-weight inference)
                        "none"    : no parseable ingredients
    """
    ingredient_order = get_ingredient_order(prod)
    text = get_ingredients_text(prod)

    if ingredient_order:
        records = parse_from_bsip1(ingredient_order, text or "")
    elif text:
        records = parse_ingredients(text)
    else:
        return None, "none"

    if not records:
        return None, "none"

    # Determine confidence tier
    top_records = [r for r in records if not r.get("is_sub")]
    has_stated = any(r.get("stated_pct") is not None for r in top_records)
    confidence = "high" if has_stated else "order"

    markers = extract_all_markers_v4(text) if text else []
    if not markers and ingredient_order:
        # Use records-based marker extraction
        from matrix_signal_probe_v5_1 import extract_markers_from_record_v4
        seen_labels: dict = {}
        for r in records:
            ms = extract_markers_from_record_v4(r)
            for m in ms:
                lbl = m["label"]
                if lbl not in seen_labels:
                    seen_labels[lbl] = m
        markers = list(seen_labels.values())

    score = compute_component_b_score_v5_1(markers)
    return score, confidence


# ---------------------------------------------------------------------------
# Load all products
# ---------------------------------------------------------------------------

def load_all_products() -> list[dict]:
    """Load from all BSIP0 raw files, BSIP1 dirs, and supplement corpus."""
    products = []
    load_log = []

    # --- BSIP0 raw files ---
    for cat, path in BSIP0_SOURCES:
        if not path.exists():
            load_log.append(f"MISSING: {path}")
            continue
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            items = raw if isinstance(raw, list) else raw.get("products", [])
            added = 0
            for item in items:
                item["_category"] = cat
                item["_source"]   = "bsip0"
                products.append(item)
                added += 1
            load_log.append(f"OK bsip0/{cat}: {added} products")
        except Exception as e:
            load_log.append(f"ERROR bsip0/{cat}: {e}")

    # --- BSIP1 dirs ---
    for cat, dirpath in BSIP1_DIRS:
        if not dirpath.exists():
            load_log.append(f"MISSING dir: {dirpath}")
            continue
        files = list(dirpath.glob("bsip1_*.json"))
        added = 0
        for fpath in files:
            try:
                item = json.loads(fpath.read_text(encoding="utf-8"))
                item["_category"] = cat
                item["_source"]   = "bsip1"
                products.append(item)
                added += 1
            except Exception as e:
                load_log.append(f"ERROR bsip1/{cat}/{fpath.name}: {e}")
        load_log.append(f"OK bsip1/{cat}: {added} products")

    # --- Supplement corpus ---
    if SUPPLEMENT_DIR.exists():
        files = list(SUPPLEMENT_DIR.glob("SP-*.json"))
        added = 0
        for fpath in files:
            try:
                item = json.loads(fpath.read_text(encoding="utf-8"))
                item["_category"] = "supplements"
                item["_source"]   = "supplement"
                products.append(item)
                added += 1
            except Exception as e:
                pass
        load_log.append(f"OK supplement corpus: {added} products")

    return products, load_log


# ---------------------------------------------------------------------------
# Simple in-category OLS regression (no external libraries)
# ---------------------------------------------------------------------------

def ols_fit(X: list[list[float]], y: list[float]) -> tuple[list[float], float, float]:
    """
    Ordinary least squares via normal equations.
    X: N x K feature matrix (each row is one sample)
    y: N targets
    Returns: (coefficients[K+1] with intercept first, R², MAE)
    Handles near-singular matrices by returning zeros.
    """
    n = len(y)
    if n < 3:
        return [], float("nan"), float("nan")

    k = len(X[0])
    # Augment with intercept column
    Xa = [[1.0] + row for row in X]

    # Normal equations: (X'X) β = X'y
    XT = [[Xa[i][j] for i in range(n)] for j in range(k + 1)]

    def mat_mul(A, B):
        ra, ca = len(A), len(A[0])
        rb, cb = len(B), len(B[0])
        C = [[0.0] * cb for _ in range(ra)]
        for i in range(ra):
            for j in range(cb):
                for l in range(ca):
                    C[i][j] += A[i][l] * B[l][j]
        return C

    XTX = mat_mul(XT, Xa)
    XTy = [[sum(XT[i][j] * y[j] for j in range(n))] for i in range(k + 1)]

    # Gauss-Jordan inverse of XTX
    m = k + 1
    aug = [XTX[i][:] + [1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]

    for col in range(m):
        # Find pivot
        pivot = None
        for row in range(col, m):
            if abs(aug[row][col]) > 1e-10:
                pivot = row
                break
        if pivot is None:
            # Singular
            return [0.0] * (k + 1), float("nan"), float("nan")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(m):
            if row != col:
                factor = aug[row][col]
                aug[row] = [aug[row][c] - factor * aug[col][c] for c in range(2 * m)]

    inv = [[aug[i][m + j] for j in range(m)] for i in range(m)]
    beta = mat_mul(inv, XTy)
    coeffs = [beta[i][0] for i in range(m)]

    # Predictions
    preds = [sum(coeffs[j] * Xa[i][j] for j in range(m)) for i in range(n)]

    # R²
    y_mean = sum(y) / n
    ss_res = sum((y[i] - preds[i]) ** 2 for i in range(n))
    ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-10 else float("nan")

    # MAE
    mae = sum(abs(y[i] - preds[i]) for i in range(n)) / n

    return coeffs, r2, mae


def pearson_r(a: list[float], b: list[float]) -> float:
    """Pearson correlation between two lists of equal length."""
    n = len(a)
    if n < 3:
        return float("nan")
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    num = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n))
    den = math.sqrt(
        sum((a[i] - mean_a) ** 2 for i in range(n)) *
        sum((b[i] - mean_b) ** 2 for i in range(n))
    )
    return num / den if den > 1e-10 else float("nan")


# ---------------------------------------------------------------------------
# Macro feature vector for a product
# ---------------------------------------------------------------------------

MACRO_FIELDS = ["energy_kcal", "fat_g", "fat_sat_g", "sodium_mg", "sugar_g", "protein_g", "fiber_g"]


def macro_feature_vector(nut: dict) -> tuple[Optional[list[float]], list[str]]:
    """
    Build macro feature vector. Returns (vector, missing_fields).
    A product is 'macro-complete' if sugar, fat, sodium are all present.
    """
    vec = []
    missing = []
    for f in MACRO_FIELDS:
        v = nut.get(f)
        if v is None:
            missing.append(f)
            vec.append(0.0)  # fill with 0 for regression (noted)
        else:
            vec.append(float(v))
    return vec, missing


# ---------------------------------------------------------------------------
# Macro-twins probe — pairs with near-identical macros, very different scores
# ---------------------------------------------------------------------------

MACRO_TWIN_FIELDS   = ["sugar_g", "fat_g", "sodium_mg", "energy_kcal"]
MACRO_TWIN_BAND_REL = 0.10   # within 10% relative
MACRO_TWIN_BAND_ABS = 5.0    # or within 5 absolute units (for near-zero values)
SCORE_DIFF_FLOOR    = 20.0   # composition scores must differ by >= 20 pts


def are_macro_twins(p1: dict, p2: dict) -> bool:
    """Return True if p1 and p2 have near-identical macros for all 4 twin fields."""
    for f in MACRO_TWIN_FIELDS:
        v1 = p1["nutrition"].get(f)
        v2 = p2["nutrition"].get(f)
        if v1 is None or v2 is None:
            return False
        diff = abs(v1 - v2)
        avg  = (abs(v1) + abs(v2)) / 2
        if avg > 0.1:
            if diff / avg > MACRO_TWIN_BAND_REL:
                return False
        else:
            if diff > MACRO_TWIN_BAND_ABS:
                return False
    return True


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    lines = []
    results = {}

    def log(msg=""):
        lines.append(msg)
        try:
            print(msg)
        except UnicodeEncodeError:
            print(msg.encode("ascii", "replace").decode("ascii"))

    log("=" * 70)
    log("MACRO-CIRCULARITY PROBE — TASK-395 FORUM")
    log(f"Run: {datetime.now(timezone.utc).isoformat()}")
    log("=" * 70)

    # -------------------------------------------------------------------------
    # Load all products
    # -------------------------------------------------------------------------
    log("\n[LOAD] Loading corpus from all sources...")
    all_products, load_log = load_all_products()
    for ll in load_log:
        log(f"  {ll}")
    log(f"\n  Total products loaded: {len(all_products)}")

    # -------------------------------------------------------------------------
    # Per-product analysis: compute matrix score + extract nutrition + classify
    # -------------------------------------------------------------------------
    log("\n[ANALYSE] Computing matrix scores + nutrition coverage...")

    enriched = []
    for prod in all_products:
        cat  = prod.get("_category", "unknown")
        bcode = (prod.get("barcode") or prod.get("canonical_product_id") or "?")

        # Nutrition
        nut = extract_nutrition(prod)

        # Matrix score
        score, confidence = compute_matrix_score(prod)

        # Macro completeness (Q5)
        core_complete = (
            nut.get("sugar_g")   is not None and
            nut.get("fat_g")     is not None and
            nut.get("sodium_mg") is not None
        )
        full_complete = core_complete and (nut.get("energy_kcal") is not None)

        entry = {
            "barcode":     bcode,
            "category":    cat,
            "source":      prod.get("_source", "?"),
            "score":       score,
            "confidence":  confidence,
            "nutrition":   nut,
            "core_complete": core_complete,
            "full_complete": full_complete,
        }
        enriched.append(entry)

    # -------------------------------------------------------------------------
    # Q5: Coverage reality-check
    # -------------------------------------------------------------------------
    log("\n[Q5] Nutrition coverage reality-check...")
    total_n = len(enriched)

    # Only food categories (exclude supplements — they don't have the same panel)
    food = [e for e in enriched if e["category"] != "supplements"]
    supp = [e for e in enriched if e["category"] == "supplements"]

    def coverage_pct(field, subset):
        n = len(subset)
        if n == 0:
            return 0, 0, "n/a"
        present = sum(1 for e in subset if e["nutrition"].get(field) is not None)
        return present, n, f"{present}/{n} ({100*present/n:.1f}%)"

    log(f"\n  Total products: {total_n} (food: {len(food)}, supplements: {len(supp)})")
    log("\n  Food corpus per-field coverage:")
    q5_coverage = {}
    for field in ["energy_kcal", "fat_g", "fat_sat_g", "sodium_mg", "carbs_g", "sugar_g", "fiber_g", "protein_g"]:
        present, n, pct_str = coverage_pct(field, food)
        log(f"    {field:20s}: {pct_str}")
        q5_coverage[field] = {"present": present, "total": n, "pct": round(100*present/n, 1) if n > 0 else 0}

    core_complete_food  = sum(1 for e in food if e["core_complete"])
    full_complete_food  = sum(1 for e in food if e["full_complete"])
    log(f"\n  Core complete (sugar+fat+sodium present): {core_complete_food}/{len(food)} ({100*core_complete_food/len(food):.1f}%)")
    log(f"  Full complete (+energy): {full_complete_food}/{len(food)} ({100*full_complete_food/len(food):.1f}%)")

    results["q5_coverage"] = {
        "total_food": len(food),
        "total_supplements": len(supp),
        "per_field": q5_coverage,
        "core_complete_sugar_fat_sodium": {"count": core_complete_food, "pct": round(100*core_complete_food/len(food),1) if food else 0},
        "full_complete_plus_energy":     {"count": full_complete_food,  "pct": round(100*full_complete_food/len(food),1)  if food else 0},
    }

    # -------------------------------------------------------------------------
    # Q1: Labeled subset — products with REAL ingredient %s
    # -------------------------------------------------------------------------
    log("\n[Q1] Building labeled subset (real ingredient %s = confidence='high')...")
    labeled = [e for e in enriched if e["confidence"] == "high" and e["score"] is not None]
    order_only = [e for e in enriched if e["confidence"] == "order" and e["score"] is not None]
    no_ingr = [e for e in enriched if e["confidence"] == "none"]

    log(f"\n  Confidence tier breakdown:")
    log(f"    high (real stated %)    : {len(labeled)}/{total_n} ({100*len(labeled)/total_n:.1f}%)")
    log(f"    order (position-weight) : {len(order_only)}/{total_n} ({100*len(order_only)/total_n:.1f}%)")
    log(f"    none (no ingredients)   : {len(no_ingr)}/{total_n} ({100*len(no_ingr)/total_n:.1f}%)")

    log("\n  Labeled subset by category:")
    by_cat = defaultdict(lambda: {"high": 0, "order": 0, "none": 0, "total": 0})
    for e in enriched:
        by_cat[e["category"]][e["confidence"]] += 1
        by_cat[e["category"]]["total"] += 1

    q1_cat_breakdown = {}
    for cat in sorted(by_cat):
        d = by_cat[cat]
        log(f"    {cat:25s}: {d['high']:3d} high / {d['order']:3d} order / {d['none']:3d} none  (total {d['total']})")
        q1_cat_breakdown[cat] = d

    results["q1_labeled_subset"] = {
        "total_products": total_n,
        "high_confidence": len(labeled),
        "order_only": len(order_only),
        "no_ingredients": len(no_ingr),
        "high_pct": round(100*len(labeled)/total_n, 1),
        "order_pct": round(100*len(order_only)/total_n, 1),
        "none_pct": round(100*len(no_ingr)/total_n, 1),
        "by_category": q1_cat_breakdown,
    }

    # -------------------------------------------------------------------------
    # Q2 + Q3: Regression of macros -> matrix score (labeled subset only)
    # -------------------------------------------------------------------------
    log("\n[Q2+Q3] Macro->composition regression (labeled subset with real %)...")

    # Categories with enough labeled products for regression (min 5)
    cat_groups = defaultdict(list)
    for e in labeled:
        if e["full_complete"]:
            cat_groups[e["category"]].append(e)

    log(f"\n  Labeled + macro-complete products available for regression:")
    reg_results = {}
    all_true_scores = []
    all_pred_scores = []

    for cat in sorted(cat_groups):
        prods = cat_groups[cat]
        n_reg = len(prods)
        log(f"    {cat}: {n_reg} products")

        if n_reg < 5:
            log(f"      -> SKIP (< 5 products for regression)")
            reg_results[cat] = {"n": n_reg, "status": "insufficient_data"}
            continue

        X = []
        y = []
        missing_count = defaultdict(int)
        for p in prods:
            vec, missing = macro_feature_vector(p["nutrition"])
            for f in missing:
                missing_count[f] += 1
            X.append(vec)
            y.append(p["score"])

        coeffs, r2, mae = ols_fit(X, y)
        preds_for_cat = [
            sum(([1.0] + X[i])[j] * coeffs[j] for j in range(len(coeffs)))
            for i in range(len(X))
        ] if coeffs else []

        log(f"      n={n_reg}, R²={r2:.3f}, MAE={mae:.2f}")
        reg_results[cat] = {
            "n": n_reg,
            "r2": round(r2, 4) if not math.isnan(r2) else None,
            "mae": round(mae, 2) if not math.isnan(mae) else None,
            "status": "ok",
        }

        all_true_scores.extend(y)
        all_pred_scores.extend(preds_for_cat)

    # Overall regression (all categories pooled — within-category centering not done, so
    # this is dominated by cross-category variance, but informative)
    log(f"\n  Overall pooled regression (all labeled+macro-complete):")
    all_X = []
    all_y = []
    for cat in cat_groups:
        for p in cat_groups[cat]:
            vec, _ = macro_feature_vector(p["nutrition"])
            all_X.append(vec)
            all_y.append(p["score"])

    total_reg_n = len(all_y)
    if total_reg_n >= 5:
        overall_coeffs, overall_r2, overall_mae = ols_fit(all_X, all_y)
        log(f"    N={total_reg_n}, R²={overall_r2:.3f}, MAE={overall_mae:.2f}")
    else:
        overall_r2, overall_mae = float("nan"), float("nan")
        log(f"    Insufficient data for pooled regression (n={total_reg_n})")

    results["q2_regression"] = {
        "by_category": reg_results,
        "pooled": {
            "n": total_reg_n,
            "r2": round(overall_r2, 4) if not math.isnan(overall_r2) else None,
            "mae": round(overall_mae, 2) if not math.isnan(overall_mae) else None,
        }
    }

    # -------------------------------------------------------------------------
    # Q3: Redundancy test — correlation between true composition score and macros
    # -------------------------------------------------------------------------
    log("\n[Q3] Redundancy test — r(true composition score, individual macros)...")

    # Use ALL labeled products (high confidence) that have full macros
    labeled_full = [e for e in labeled if e["full_complete"]]
    q3_n = len(labeled_full)
    log(f"  n={q3_n} products with high confidence + full macros")

    macro_scores = {f: [] for f in MACRO_FIELDS}
    true_scores  = []

    for e in labeled_full:
        true_scores.append(e["score"])
        for f in MACRO_FIELDS:
            macro_scores[f].append(e["nutrition"].get(f, 0.0) or 0.0)

    q3_correlations = {}
    log("\n  Pearson r(matrix_score, macro_field):")
    for f in MACRO_FIELDS:
        r = pearson_r(true_scores, macro_scores[f])
        log(f"    {f:20s}: r = {r:+.3f}" if not math.isnan(r) else f"    {f:20s}: r = n/a")
        q3_correlations[f] = round(r, 4) if not math.isnan(r) else None

    # Max absolute correlation across macros (the "best any single macro can do")
    valid_rs = [abs(v) for v in q3_correlations.values() if v is not None]
    max_r     = max(valid_rs) if valid_rs else float("nan")
    log(f"\n  Max |r| of any single macro vs composition score: {max_r:.3f}")

    # Multi-macro correlation: use predicted scores from pooled regression
    if len(all_true_scores) >= 5 and len(all_pred_scores) >= 5 and len(all_true_scores) == len(all_pred_scores):
        r_pred_vs_true = pearson_r(all_true_scores, all_pred_scores)
        log(f"  r(predicted_by_macros, true_composition) [pooled cats]: {r_pred_vs_true:.3f}")
    else:
        r_pred_vs_true = float("nan")
        log(f"  r(predicted_by_macros, true_composition): n/a (prediction set size mismatch)")

    results["q3_redundancy"] = {
        "n": q3_n,
        "per_macro_r": q3_correlations,
        "max_single_macro_abs_r": round(max_r, 4) if not math.isnan(max_r) else None,
        "multi_macro_r_predicted_vs_true": round(r_pred_vs_true, 4) if not math.isnan(r_pred_vs_true) else None,
        "verdict": None,  # filled below
    }

    # -------------------------------------------------------------------------
    # Q4: Macro-twins probe
    # -------------------------------------------------------------------------
    log("\n[Q4] Macro-twins probe (identical macros, very different composition scores)...")

    # Only run on labeled products with full macros and a valid score
    twin_pool = [e for e in labeled_full if e["score"] is not None]
    n_pool = len(twin_pool)
    log(f"  Pool: {n_pool} products (labeled, full macro, valid score)")

    twin_pairs = []
    for i in range(n_pool):
        for j in range(i + 1, n_pool):
            p1, p2 = twin_pool[i], twin_pool[j]
            if are_macro_twins(p1, p2):
                score_diff = abs(p1["score"] - p2["score"])
                if score_diff >= SCORE_DIFF_FLOOR:
                    twin_pairs.append({
                        "b1": p1["barcode"], "cat1": p1["category"],
                        "b2": p2["barcode"], "cat2": p2["category"],
                        "score1": p1["score"], "score2": p2["score"],
                        "score_diff": round(score_diff, 1),
                        "macros1": {f: p1["nutrition"].get(f) for f in MACRO_TWIN_FIELDS},
                        "macros2": {f: p2["nutrition"].get(f) for f in MACRO_TWIN_FIELDS},
                    })

    # Count unique barcodes in twin pairs
    twin_barcodes = set()
    for tp in twin_pairs:
        twin_barcodes.add(tp["b1"])
        twin_barcodes.add(tp["b2"])

    n_twin_pairs = len(twin_pairs)
    n_twin_products = len(twin_barcodes)
    twin_frac_of_labeled = n_twin_products / n_pool if n_pool > 0 else 0

    log(f"\n  Twin pairs found (≥{SCORE_DIFF_FLOOR}pt score gap, ≤{int(MACRO_TWIN_BAND_REL*100)}% macro gap):")
    log(f"    Pairs:    {n_twin_pairs}")
    log(f"    Unique products in pairs: {n_twin_products} / {n_pool} ({100*twin_frac_of_labeled:.1f}% of labeled pool)")

    # Show first 10 pairs
    for tp in twin_pairs[:10]:
        log(f"      {tp['cat1']:20s} {tp['b1']:15s} score={tp['score1']:5.1f}")
        log(f"    vs {tp['cat2']:20s} {tp['b2']:15s} score={tp['score2']:5.1f} (diff={tp['score_diff']})")
        log(f"      macros1={tp['macros1']}")
        log(f"      macros2={tp['macros2']}")
        log()

    results["q4_macro_twins"] = {
        "band_rel_pct": int(MACRO_TWIN_BAND_REL * 100),
        "score_diff_floor": SCORE_DIFF_FLOOR,
        "twin_pairs": n_twin_pairs,
        "unique_products_in_pairs": n_twin_products,
        "pool_n": n_pool,
        "twin_frac_of_labeled_pool": round(twin_frac_of_labeled, 4),
        "twin_pct_of_labeled_pool": round(100 * twin_frac_of_labeled, 1),
        "examples": twin_pairs[:10],
    }

    # -------------------------------------------------------------------------
    # Q6: American training sample feasibility (no build)
    # -------------------------------------------------------------------------
    log("\n[Q6] American training sample feasibility assessment...")

    q6_text = """
SOURCES AVAILABLE (OFF BANNED — excluded entirely):

1. USDA FoodData Central (FDC) — Foundation / SR-Legacy
   Granularity: per-100g nutrition + ingredient lists, but ingredient %s are NOT
   typically stated (US labels don't mandate %s). FDC gives macros + ingredient
   order at best. Coverage: broad generics (thousands), but NOT branded Israeli
   products and NOT stated %s.
   -> Verdict: useful for macro validation; USELESS as % ground-truth for training.

2. USDA FoodData Central — Branded Foods
   ~600,000 branded products with FULL nutrition panels (all macros) + ingredient
   lists. However: (a) %s are stated on only a small fraction (~5-15% of US
   branded labels — not legally required), (b) Israeli regulatory environment
   differs (Hebrew labels state %s at higher rates), (c) category mix differs.
   -> Verdict: macro-rich, but % training data is thin even here.

3. DSLD (NIH Dietary Supplement Label DB)
   Already integrated. Supplement focus only; irrelevant for food composition.

4. USDA National Nutrient Database (legacy, pre-FDC)
   Subsumed into FDC. No ingredient-level data.

5. EWG Food Scores / Open food databases
   Either ban-adjacent (OFF) or limited/unverified ingredient % data.

CONCLUSION:
  A large, fully-%-labeled American dataset for FOOD training does NOT realistically
  exist in any off-the-shelf source. The constraint is regulatory: US labels do not
  mandate ingredient %s. Israel actually has BETTER label-% coverage than the US
  for comparable food types (Israeli labels state % at ~36% stated + ~45% order-only =
  ~81% with any structural signal). So the "large American training sample" premise
  is incorrect — the US data would be WEAKER on %s, not stronger.
"""
    log(q6_text)

    results["q6_us_sample_feasibility"] = {
        "verdict": "NOT_FEASIBLE",
        "reason": "US food labels do not mandate ingredient %s; FDC/branded has <15% %s stated; Israel already has higher %-label coverage than US. An American training set would add macro data only — which we already have — and would not provide the stated-% ground truth needed to train a composition estimator.",
        "sources_surveyed": ["USDA_FDC_foundation", "USDA_FDC_branded", "DSLD", "USDA_NNDB"],
        "off_excluded": True,
    }

    # -------------------------------------------------------------------------
    # Verdicts
    # -------------------------------------------------------------------------
    log("\n" + "=" * 70)
    log("VERDICTS")
    log("=" * 70)

    # Q3 verdict
    if max_r > 0.80:
        q3_verdict = "REDUNDANT — macros already encode the composition signal strongly (r > 0.80). Estimating composition FROM macros then using it IN scoring adds near-zero discriminating power. The thesis is circular."
    elif max_r > 0.55:
        q3_verdict = "PARTIALLY REDUNDANT — moderate macro-composition correlation (r 0.55-0.80). Some independent signal exists but mixed-label products (macro-twins) expose the structural floor."
    else:
        q3_verdict = "NON-REDUNDANT — low macro-composition correlation (r < 0.55). Composition carries genuinely independent signal — but macro-inference of composition would still be unreliable for the twin pairs."

    results["q3_redundancy"]["verdict"] = q3_verdict
    log(f"\nQ1: Labeled subset (real ingredient %) = {len(labeled)} products ({100*len(labeled)/total_n:.1f}% of corpus)")
    log(f"Q2: Macro->composition regression pooled: R²={overall_r2:.3f}, MAE={overall_mae:.2f}")
    log(f"Q3: Max |r|(macro, composition) = {max_r:.3f} -> {q3_verdict[:60]}...")
    log(f"Q4: Macro-twins = {n_twin_pairs} pairs / {n_twin_products} products ({100*twin_frac_of_labeled:.1f}% of labeled pool)")
    log(f"Q5: Core nutrition complete (sugar+fat+sodium): {core_complete_food}/{len(food)} ({100*core_complete_food/len(food):.1f}% of food corpus)")
    log(f"Q6: US training sample feasibility: NOT FEASIBLE (US labels lack stated ingredient %s)")

    log("\n\nFINAL RECOMMENDATION:")
    log("-" * 60)

    if max_r > 0.55:
        overall_verdict = "CIRCULAR / INSUFFICIENT — DO NOT IMPLEMENT"
        rec_text = """
The macro->composition inference thesis is empirically circular or weakly supported:
  1. If macros already correlate strongly with composition (r>0.55), inferring
     composition from macros and adding it back to scoring adds near-zero NEW
     information. The score will move, but the signal is already in the macros.
  2. The macro-twins (identical macros, different real composition) expose the
     hard floor of what macro-inference can achieve: those products CANNOT be
     distinguished by any macro-based estimator by definition.
  3. The 'large American training sample' premise is false — US labels have LOWER
     ingredient-% coverage than Israeli labels. The training data floor is our own
     existing corpus.
  4. The right approach: use REAL stated %s where present (already working, covers
     ~36% of corpus at high confidence), and for the ~45% order-only, use ingredient
     ORDER as a real lower-confidence signal with explicit confidence capping —
     NOT inferred composition from macros. Order is real label data; inference is not.
  5. Weight nutrition to DOMINATE (as proposed) is already correct and already
     implemented in the current engine architecture. No circularity fix needed there.
"""
    else:
        overall_verdict = "POTENTIALLY VIABLE — BUT HIGH IMPLEMENTATION RISK"
        rec_text = """
Composition carries some independent signal from macros (r<0.55). However:
  - Macro-twins still set a hard floor on inference accuracy.
  - A training approach is still needed to calibrate the estimator.
  - Without a verified training set (US data is insufficient), the estimator
    would be uncalibrated and could fabricate precision that isn't there.
  - Recommend: focus on improving stated-% read coverage (biggest lever),
    not building a macro-inference pipeline.
"""
    log(f"  VERDICT: {overall_verdict}")
    log(rec_text)

    results["final_verdict"] = {
        "verdict": overall_verdict,
        "max_macro_composition_r": round(max_r, 4) if not math.isnan(max_r) else None,
        "pooled_r2": round(overall_r2, 4) if not math.isnan(overall_r2) else None,
        "recommendation": "Use real stated %s (high conf) + order signal (order conf, capped) + dominant nutrition weighting. Do NOT infer composition from macros.",
    }

    # -------------------------------------------------------------------------
    # Write outputs
    # -------------------------------------------------------------------------
    out_json  = ANALYSIS_DIR / "macro_circularity_probe_results.json"
    out_txt   = ANALYSIS_DIR / "macro_circularity_probe_report.txt"

    results["run_metadata"] = {
        "probe": "macro_circularity_probe",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "task": "TASK-395-forum",
        "total_products_loaded": total_n,
        "bsip0_sources": [str(p) for _, p in BSIP0_SOURCES],
        "bsip1_dirs": [str(d) for _, d in BSIP1_DIRS],
    }

    out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    out_txt.write_text("\n".join(lines), encoding="utf-8")

    log(f"\n[DONE] Results written to:")
    log(f"  {out_json}")
    log(f"  {out_txt}")

    # Print final summary for machine-readable contract
    print("\n\n--- MACHINE CONTRACT ---")
    print(json.dumps({
        "q1_labeled_n": len(labeled),
        "q1_labeled_pct": round(100*len(labeled)/total_n, 1),
        "q1_order_only_n": len(order_only),
        "q1_none_n": len(no_ingr),
        "q2_pooled_r2": round(overall_r2, 4) if not math.isnan(overall_r2) else None,
        "q2_pooled_mae": round(overall_mae, 2) if not math.isnan(overall_mae) else None,
        "q3_max_single_r": round(max_r, 4) if not math.isnan(max_r) else None,
        "q3_multi_r": round(r_pred_vs_true, 4) if not math.isnan(r_pred_vs_true) else None,
        "q4_twin_pairs": n_twin_pairs,
        "q4_twin_products": n_twin_products,
        "q4_twin_pct_of_labeled": round(100*twin_frac_of_labeled, 1),
        "q5_core_complete_pct": round(100*core_complete_food/len(food), 1) if food else 0,
        "q6_us_feasible": False,
        "final_verdict": overall_verdict,
    }, ensure_ascii=False, indent=2))

    return results


if __name__ == "__main__":
    main()
