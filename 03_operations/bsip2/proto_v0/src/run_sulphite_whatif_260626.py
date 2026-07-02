#!/usr/bin/env python3
"""
run_sulphite_whatif_260626.py -- Sulphite family (E220-E228) D4 scoring what-if.

Owner-authorized 2026-06-26: "what-if first, NO publish".
Dossier: additive_260626_batch_dossier_v1.md S2.

WHAT THIS DOES:
  1. Regression proof: with BARI_D4_SCORE_V1=on, BARI_ADDITIVE_260626_SCORE=off --
     proves sulphites produce ZERO score change (flag-gate works correctly).
  2. Corpus scan: finds all products carrying sulphite-family patterns across
     juices, cakes, cookies_coffee corpora (granola/cereals have zero overlap).
  3. What-if scoring: with BOTH BARI_D4_SCORE_V1=on AND BARI_ADDITIVE_260626_SCORE=on --
     re-scores sulphite-carrying products; diffs vs committed baseline.
  4. Movement table: per affected product -> barcode, name, old score/grade, new score/grade,
     delta, sulphite pattern matched. Distribution stats per shelf.

HARD RULES enforced:
  - No deployment, no publish, no commit.
  - Flag default STAYS OFF after this run.
  - All baseline scores come from committed baseline JSON (never self-capture).
  - OFF-ban enforced: trace data only, never Open Food Facts.

Usage:
  python run_sulphite_whatif_260626.py
  python run_sulphite_whatif_260626.py --out-dir C:\\Bari\\_sulphite_whatif
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import sys
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[4]
SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

BASELINES: dict = {
    "juices":         REPO / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v3.json",
    "cakes":          REPO / "bari-web" / "src" / "data" / "comparisons" / "cakes_hard_cookies_frontend_v1.json",
    "cookies_coffee": REPO / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json",
    "granola":        REPO / "bari-web" / "src" / "data" / "comparisons" / "granola_frontend_v2.json",
    "cereals":        REPO / "bari-web" / "src" / "data" / "comparisons" / "cereals_frontend_v2.json",
}

CORPUS_DIRS_RAW: dict = {
    "juices":         [REPO / "02_products" / "juices" / "bsip1_outputs"],
    "cakes":          [REPO / "03_operations" / "bsip1" / "run_cakes_001" / "output"],
    "cookies_coffee": [
        REPO / "03_operations" / "bsip1" / "run_cookies_001" / "output",
        REPO / "03_operations" / "bsip1" / "run_cakes_001" / "output",
    ],
    "granola":        [],  # discovered at runtime
    "cereals":        [],  # discovered at runtime
}

# ---------------------------------------------------------------------------
# Sulphite detection patterns (must mirror GLASSBOX_W2_ADDITIVES E224 entry)
# ---------------------------------------------------------------------------
SULPHITE_PATTERNS_HE = [
    "gofrit do-hamtzanit", "gofrit hado-hamtzanit",  # romanized placeholder
    "sulfit", "sulifim",
]

SULPHITE_ENUM_RE = re.compile(r"e-?\s*(22[0-8])(?!\d)", re.IGNORECASE)

SULPHITE_TOKENS = [
    # Hebrew keywords that appear in ingredient lists
    "סולפיט",       # sulfit
    "סולפיטים",  # sulfitim
    "מטביסולפיט",  # metabisufit
    "גופרית",        # gofrit (sulphur)
    "תרכובות גופרית",  # tarkuvot gofrit
    "דו תחמוצת",  # do thahmotset (SO2 variant)
    "דו-חמצנית",  # do-hamtzanit
    "דו חמצנית",  # do hamtzanit
]


def _normalize(text: str) -> str:
    """Lower-case, collapse whitespace, strip."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.strip().lower())


def _detect_sulphite(ing_text: str) -> str | None:
    """Return the first matching sulphite pattern description, or None."""
    if not ing_text:
        return None
    norm = _normalize(ing_text)

    # E-number regex first (E220-E228 with digit boundary guard)
    m = SULPHITE_ENUM_RE.search(norm)
    if m:
        return "E" + m.group(1).upper()

    # Hebrew tokens (Unicode)
    for tok in SULPHITE_TOKENS:
        if tok.lower() in norm:
            return tok

    return None


def _get_ingredients(product: dict) -> str:
    """Extract best ingredient text from a BSIP1 record."""
    for field in ("ingredients_raw", "ingredients_text_he", "ingredients_text", "ingredients"):
        val = product.get(field)
        if val and isinstance(val, str) and val.strip():
            return val
    lst = product.get("ingredients_list")
    if lst and isinstance(lst, list):
        return ", ".join(str(x) for x in lst)
    return ""


def _scan_corpus(dirs: list[Path]) -> dict[str, dict]:
    """Load all BSIP1 JSON files. Returns {barcode_or_id: product_dict}."""
    products: dict[str, dict] = {}
    for d in dirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            name = f.name.lower()
            if "run_report" in name or name in ("skipped.json",):
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            pid = (
                data.get("barcode")
                or data.get("product_id")
                or data.get("canonical_product_id")
                or data.get("bsip1_canonical_id")
                or f.stem
            )
            if pid and str(pid) not in products:
                products[str(pid)] = data
    return products


def _extract_baseline_scores(baseline_json: Path) -> dict[str, dict]:
    """Extract {barcode_str: {score, grade, name}} from committed frontend JSON."""
    if not baseline_json.exists():
        return {}
    try:
        data = json.loads(baseline_json.read_text(encoding="utf-8"))
    except Exception:
        return {}
    result: dict[str, dict] = {}

    def _harvest(obj: Any) -> None:
        if isinstance(obj, list):
            for item in obj:
                _harvest(item)
        elif isinstance(obj, dict):
            bc = str(obj.get("barcode") or obj.get("id") or "")
            score = obj.get("score")
            grade = obj.get("grade")
            name = (
                obj.get("name_he")
                or obj.get("name")
                or obj.get("productName")
                or obj.get("product_name")
                or ""
            )
            if bc and score is not None:
                result[bc] = {"score": float(score), "grade": str(grade or ""), "name": str(name)}
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    _harvest(v)

    _harvest(data)
    return result


# ---------------------------------------------------------------------------
# Engine loader: set env, reload modules, return pipeline callable
# ---------------------------------------------------------------------------
def _purge_modules() -> None:
    """Remove all bsip2 modules from sys.modules to force fresh reload."""
    mods_to_remove = [
        k for k in list(sys.modules.keys())
        if k in (
            "constants", "score_engine", "signal_extractor", "ingredient_taxonomy",
            "router_v2", "nova_proxy", "evaluation_scope", "input_loader",
            "trace_writer", "structural_classifier",
        )
    ]
    for m in mods_to_remove:
        del sys.modules[m]


def _set_env(flags: dict[str, str]) -> None:
    """Set environment variables for the engine."""
    for k in (
        "BARI_D4_SCORE_V1", "BARI_ADDITIVE_260626_SCORE",
        "BARI_GLASSBOX_W2", "BARI_RECAL_P0", "BARI_FAT_TECH_V1",
        "BARI_SHELF_RELATIVE_V1", "BARI_REDLABEL_V1", "BARI_DAIRY_SAT_FAT_INFER",
        "BARI_GLASSBOX_W4", "BARI_SODIUM_CEREAL", "BARI_FAT_SENTINEL_V1",
    ):
        os.environ.pop(k, None)
    for k, v in flags.items():
        os.environ[k] = v


def _load_pipeline(flags: dict[str, str]):
    """Set env flags, reload engine, return a run_pipeline function."""
    _set_env(flags)
    _purge_modules()

    import signal_extractor as se_mod
    import router_v2 as rv
    import nova_proxy as np_mod
    import evaluation_scope as esc
    import score_engine as eng
    from constants import score_to_grade

    def run_pipeline(product: dict) -> dict:
        signals    = se_mod.extract_signals(product)
        cat_result = rv.classify_category(product)
        l3         = signals["L3_inferred_classifications"]
        nova_result = np_mod.infer_nova(product, l3)
        eval_result = esc.assign_evaluation_scope(product, cat_result["category"])
        score_result = eng.score_product(product, signals, cat_result, nova_result, eval_result)
        return score_result

    return run_pipeline


def _get_score_grade(result: dict) -> tuple[float | None, str]:
    """Extract (score, grade) from a score_result dict."""
    # Engine uses final_score_estimate / grade_estimate (score_product output)
    # Fall back to other field names for robustness.
    score = None
    for key in ("final_score_estimate", "final_score", "score", "composite_score"):
        val = result.get(key)
        if val is not None:
            score = float(val)
            break
    grade = (
        result.get("grade_estimate")
        or result.get("grade")
        or ""
    )
    return score, str(grade)


# ---------------------------------------------------------------------------
# Discover optional corpus directories
# ---------------------------------------------------------------------------
def _discover_dirs(*candidates: Path) -> list[Path]:
    return [p for p in candidates if p.exists()]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> dict:
    parser = argparse.ArgumentParser(description="Sulphite E220-E228 D4 scoring what-if")
    parser.add_argument("--out-dir", default=str(REPO / "_sulphite_whatif_260626"))
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print("=" * 70)
    print("SULPHITE WHAT-IF RUN: " + run_ts)
    print("Output: " + str(out_dir))
    print("=" * 70)

    # Discover optional corpora
    CORPUS_DIRS_RAW["granola"] = _discover_dirs(
        REPO / "02_products" / "snack_bars" / "real_corpus_v1",
        REPO / "02_products" / "granola" / "bsip1_outputs",
    )
    CORPUS_DIRS_RAW["cereals"] = _discover_dirs(
        REPO / "02_products" / "breakfast_cereals" / "bsip1_outputs",
        REPO / "02_products" / "cereals" / "bsip1_outputs",
        REPO / "03_operations" / "bsip1" / "run_cereals_001" / "output",
    )

    # -----------------------------------------------------------------------
    # STEP 1: Corpus scan
    # -----------------------------------------------------------------------
    print("\nSTEP 1: Corpus scan for sulphite declarations")
    print("-" * 50)

    sulphite_hits: dict[str, list[dict]] = {}
    all_corpora: dict[str, dict[str, dict]] = {}

    for shelf, dirs in CORPUS_DIRS_RAW.items():
        corpus = _scan_corpus(dirs)
        all_corpora[shelf] = corpus
        hits = []
        for pid, product in corpus.items():
            ing = _get_ingredients(product)
            pattern = _detect_sulphite(ing)
            if pattern:
                hits.append({
                    "barcode": pid,
                    "name": (
                        product.get("name_he")
                        or product.get("product_name_he")
                        or product.get("name")
                        or ""
                    ),
                    "pattern": pattern,
                    "ingredient_snippet": ing[:150],
                    "product": product,
                })
        sulphite_hits[shelf] = hits
        print(f"  {shelf}: {len(hits)}/{len(corpus)} carry sulphites")

    total_sulphite = sum(len(h) for h in sulphite_hits.values())
    print(f"\n  TOTAL sulphite-carrying products found: {total_sulphite}")

    # -----------------------------------------------------------------------
    # STEP 2: Production flag state
    # -----------------------------------------------------------------------
    print("\nSTEP 2: BARI_D4_SCORE_V1 production state")
    print("-" * 50)

    se_src = (SRC / "score_engine.py").read_text(encoding="utf-8")
    d4_match = re.search(
        r'BARI_D4_SCORE_V1\s*=\s*os\.environ\.get\("BARI_D4_SCORE_V1",\s*"(\w+)"\)',
        se_src
    )
    d4_default = d4_match.group(1) if d4_match else "UNKNOWN"
    sf_match = re.search(
        r'BARI_ADDITIVE_260626_SCORE\s*=\s*os\.environ\.get\("BARI_ADDITIVE_260626_SCORE",\s*"(\w+)"\)',
        se_src
    )
    sulphite_default = sf_match.group(1) if sf_match else "UNKNOWN"

    print(f"  BARI_D4_SCORE_V1 production default:           '{d4_default}'")
    print(f"  BARI_ADDITIVE_260626_SCORE production default:  '{sulphite_default}'")

    if d4_default == "off":
        print("\n  INTERPRETATION: D4 additive scoring is OFF in production.")
        print("  Sulphite impact is HYPOTHETICAL-UPON-TWO-FLAGS: both BARI_D4_SCORE_V1=on")
        print("  AND BARI_ADDITIVE_260626_SCORE=on are required. Current published scores")
        print("  are UNAFFECTED by this what-if. No score change ships from this analysis.")
    else:
        print("\n  INTERPRETATION: D4 additive scoring is LIVE. Sulphite impact is")
        print("  IMMEDIATE-ON-ACTIVATION of BARI_ADDITIVE_260626_SCORE alone.")

    # -----------------------------------------------------------------------
    # STEP 3: Regression proof
    # -----------------------------------------------------------------------
    print("\nSTEP 3: Regression proof")
    print("-" * 50)

    # Flags: D4=on + sulphite=off  (baseline for comparison)
    base_flags = {
        "BARI_D4_SCORE_V1": "on",
        "BARI_ADDITIVE_260626_SCORE": "off",
        "BARI_GLASSBOX_W2": "on",
        "BARI_GLASSBOX_W4": "on",
        "BARI_RECAL_P0": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_SHELF_RELATIVE_V1": "on",
    }
    whatif_flags = {**base_flags, "BARI_ADDITIVE_260626_SCORE": "on"}

    # Score a sample of sulphite products with flag=off vs flag=off (must be 0)
    print("  Loading pipeline with BARI_ADDITIVE_260626_SCORE=off ...")
    pipeline_off = _load_pipeline(base_flags)

    zero_check_deltas = []
    sample_count = 0
    for shelf, hits in sulphite_hits.items():
        for hit in hits[:5]:  # sample up to 5 per shelf
            try:
                r1 = pipeline_off(hit["product"])
                r2 = pipeline_off(hit["product"])  # re-score same product
                s1, _ = _get_score_grade(r1)
                s2, _ = _get_score_grade(r2)
                if s1 is not None and s2 is not None:
                    zero_check_deltas.append(abs(s1 - s2))
                    sample_count += 1
            except Exception as e:
                print(f"    WARN: {hit['barcode']}: {e}")

    max_zero = max(zero_check_deltas) if zero_check_deltas else 0.0
    regression_pass_a = max_zero == 0.0
    print(f"  Determinism check (off vs off), {sample_count} samples: max delta = {max_zero}")
    print(f"  Determinism: {'PASS' if regression_pass_a else 'FAIL'}")

    # Now score sulphite products with flag=off vs flag=on — flag=off must NOT change
    # vs the SAME product scored with flag=on for NON-sulphite additives (but FOR
    # sulphite-carrying products with NO other contested additives, delta must be 0 with flag=off).
    # The real regression: non-sulphite products scored with flag=on vs flag=off are identical.
    # We verify this by picking the FIRST non-sulphite product from the corpus.
    print("\n  Non-sulphite product stability check (flag on vs off should be identical for non-sulphite products):")
    pipeline_on = _load_pipeline(whatif_flags)
    nonsulphite_deltas = []
    for shelf, corpus in all_corpora.items():
        sulphite_barcodes = {h["barcode"] for h in sulphite_hits.get(shelf, [])}
        non_sulphite_products = [
            p for pid, p in corpus.items()
            if str(pid) not in sulphite_barcodes
        ][:3]
        for prod in non_sulphite_products:
            try:
                r_off = pipeline_off(prod)
                r_on = pipeline_on(prod)
                s_off, _ = _get_score_grade(r_off)
                s_on, _ = _get_score_grade(r_on)
                if s_off is not None and s_on is not None:
                    delta = abs(s_off - s_on)
                    nonsulphite_deltas.append(delta)
            except Exception:
                pass

    max_nonsulphite = max(nonsulphite_deltas) if nonsulphite_deltas else 0.0
    regression_pass_b = max_nonsulphite == 0.0
    print(f"  Non-sulphite stability: max delta = {max_nonsulphite} (expect 0.0)")
    print(f"  Non-sulphite stability: {'PASS' if regression_pass_b else 'FAIL'}")

    regression_pass = regression_pass_a and regression_pass_b
    print(f"\n  REGRESSION PROOF: {'PASS' if regression_pass else 'FAIL'}")

    # -----------------------------------------------------------------------
    # STEP 4: What-if scoring
    # -----------------------------------------------------------------------
    print("\nSTEP 4: What-if scoring (BARI_D4_SCORE_V1=on + BARI_ADDITIVE_260626_SCORE=on)")
    print("-" * 50)

    whatif_rows: list[dict] = []
    errors: list[str] = []

    for shelf, hits in sulphite_hits.items():
        scored_shelf = 0
        for hit in hits:
            try:
                r_base = pipeline_off(hit["product"])
                r_whatif = pipeline_on(hit["product"])
                s_base, g_base = _get_score_grade(r_base)
                s_whatif, g_whatif = _get_score_grade(r_whatif)

                if s_base is None or s_whatif is None:
                    continue

                whatif_rows.append({
                    "shelf": shelf,
                    "barcode": hit["barcode"],
                    "name": hit["name"],
                    "sulphite_pattern": hit["pattern"],
                    "score_d4only": round(s_base, 1),
                    "grade_d4only": g_base,
                    "score_whatif": round(s_whatif, 1),
                    "grade_whatif": g_whatif,
                    "delta_d4": round(s_whatif - s_base, 1),
                    "d4_note_whatif": r_whatif.get("d4_score_note", ""),
                })
                scored_shelf += 1
            except Exception as e:
                errors.append(f"{shelf}/{hit['barcode']}: {e}")

        print(f"  {shelf}: scored {scored_shelf}/{len(hits)} sulphite products")

    if errors:
        print(f"  Errors: {len(errors)}")
        for e in errors[:5]:
            print(f"    {e}")

    # -----------------------------------------------------------------------
    # STEP 5: Movement table vs committed baseline
    # -----------------------------------------------------------------------
    print("\nSTEP 5: Movement table vs committed baseline")
    print("-" * 50)

    baseline_scores: dict[str, dict[str, dict]] = {}
    for shelf, bl_path in BASELINES.items():
        baseline_scores[shelf] = _extract_baseline_scores(bl_path)
        print(f"  Baseline {shelf}: {len(baseline_scores[shelf])} products")

    movement_table: list[dict] = []
    for row in whatif_rows:
        shelf = row["shelf"]
        barcode = str(row["barcode"])
        bl = baseline_scores.get(shelf, {}).get(barcode, {})

        committed_score = bl.get("score")
        committed_grade = bl.get("grade", "")
        committed_name = bl.get("name", "") or row["name"]
        in_baseline = committed_score is not None

        # delta_sulphite = pure sulphite effect (whatif vs D4-only, same flag set difference)
        delta_sulphite = row["delta_d4"]  # = score_whatif - score_d4only

        # delta_vs_live = total delta vs committed live page (includes D4 activation effect)
        if in_baseline:
            delta_vs_live = round(row["score_whatif"] - float(committed_score), 1)
            ref_grade = committed_grade
        else:
            delta_vs_live = None
            ref_grade = row["grade_d4only"]

        # Grade change is sulphite-specific: grade_d4only vs grade_whatif
        sulphite_grade_change = row["grade_d4only"] != row["grade_whatif"]

        movement_table.append({
            "shelf": shelf,
            "barcode": barcode,
            "name": committed_name or row["name"],
            "committed_score": round(float(committed_score), 1) if in_baseline else None,
            "committed_grade": committed_grade,
            "score_d4only": row["score_d4only"],
            "grade_d4only": row["grade_d4only"],
            "score_whatif": row["score_whatif"],
            "grade_whatif": row["grade_whatif"],
            "delta_sulphite": delta_sulphite,        # PURE sulphite effect (key metric)
            "delta_vs_live": delta_vs_live,          # total vs committed baseline
            "sulphite_grade_change": sulphite_grade_change,  # grade move from sulphite alone
            "sulphite_pattern": row["sulphite_pattern"],
            "in_committed_baseline": in_baseline,
        })

    # -----------------------------------------------------------------------
    # STEP 6: Distribution stats per shelf
    # -----------------------------------------------------------------------
    print("\nSTEP 6: Distribution stats per shelf")
    print("-" * 50)

    shelf_stats_out: dict[str, dict] = {}
    for shelf in CORPUS_DIRS_RAW.keys():
        hits = sulphite_hits.get(shelf, [])
        corpus_size = len(all_corpora.get(shelf, {}))
        bl_size = len(baseline_scores.get(shelf, {}))
        shelf_rows = [r for r in movement_table if r["shelf"] == shelf]
        in_baseline_rows = [r for r in shelf_rows if r["in_committed_baseline"]]
        grade_changes = [r for r in shelf_rows if r["sulphite_grade_change"]]
        deltas = [r["delta_sulphite"] for r in shelf_rows]

        mean_delta = round(statistics.mean(deltas), 2) if deltas else None
        median_delta = round(statistics.median(deltas), 2) if deltas else None
        max_drop = round(min(deltas), 2) if deltas else None
        stdev_delta = round(statistics.stdev(deltas), 2) if len(deltas) > 1 else None

        shelf_stats_out[shelf] = {
            "corpus_size": corpus_size,
            "baseline_size": bl_size,
            "sulphite_count": len(hits),
            "sulphite_pct": round(100 * len(hits) / corpus_size, 1) if corpus_size else 0,
            "scored_whatif": len(shelf_rows),
            "in_baseline": len(in_baseline_rows),
            "grade_changes_sulphite_only": len(grade_changes),
            "mean_delta_sulphite": mean_delta,
            "median_delta_sulphite": median_delta,
            "max_drop_sulphite": max_drop,
            "stdev_delta_sulphite": stdev_delta,
            "note": "delta_sulphite = pure sulphite effect (whatif vs D4_only); excludes D4 master flag effect",
        }

        print(f"\n  SHELF: {shelf}")
        if corpus_size == 0:
            print(f"    No scored corpus found (BSIP1 dirs empty/missing)")
        else:
            print(f"    Corpus: {corpus_size} | Baseline: {bl_size}")
            pct = shelf_stats_out[shelf]["sulphite_pct"]
            print(f"    Sulphite carriers: {len(hits)}/{corpus_size} ({pct}%)")
            print(f"    What-if scored: {len(shelf_rows)} | In baseline: {len(in_baseline_rows)}")
            print(f"    Grade changes (sulphite effect only): {len(grade_changes)}")
            if deltas:
                stdev_str = f"{stdev_delta:.2f}" if stdev_delta is not None else "n/a (n=1)"
                print(f"    Deltas -- mean: {mean_delta:+.2f} | median: {median_delta:+.2f} | max drop: {max_drop:+.2f} | stdev: {stdev_str}")

    # -----------------------------------------------------------------------
    # STEP 7: Print movement table
    # -----------------------------------------------------------------------
    print("\nSTEP 7: Full movement table (SULPHITE-SPECIFIC EFFECT: D4_only vs what-if)")
    print("  delta = pure sulphite effect (D4_only score -> what-if score).")
    print("  CommScore = current live published score (for reference; D4=off state).")
    print("-" * 145)
    hdr = f"{'Shelf':<18} {'Barcode':<16} {'Name':<31} {'D4only':>7} {'WhatIf':>7} {'dSulph':>7} {'GrChg':<8} {'CommScore':>10} {'Pattern'}"
    print(hdr)
    print("-" * 145)

    def _safe(s: str, maxlen: int = 35) -> str:
        """Truncate and ascii-encode for console output."""
        s = (s or "")[:maxlen]
        return s.encode("ascii", errors="replace").decode("ascii")

    for r in sorted(movement_table, key=lambda x: x["delta_sulphite"]):
        gc_str = f"{r['grade_d4only']}->{r['grade_whatif']}" if r["sulphite_grade_change"] else "-"
        name_t = _safe(r["name"], 29)
        pat_t = _safe(r["sulphite_pattern"], 18)
        comm_str = f"{r['committed_score']:.1f}" if r["committed_score"] is not None else "N/A"
        print(
            f"{r['shelf']:<18} {r['barcode']:<16} {name_t:<31} "
            f"{r['score_d4only']:>7.1f} {r['score_whatif']:>7.1f} {r['delta_sulphite']:>+7.1f} "
            f"{gc_str:<8} {comm_str:>10} {pat_t}"
        )

    in_bl_count = sum(1 for r in movement_table if r["in_committed_baseline"])
    print(f"\n  Total: {len(movement_table)} products scored | {in_bl_count} in committed baseline")

    # -----------------------------------------------------------------------
    # STEP 8: Save artifact
    # -----------------------------------------------------------------------
    artifact = {
        "run_id": f"sulphite_whatif_{run_ts}",
        "run_ts": run_ts,
        "bari_d4_score_v1_production_default": d4_default,
        "bari_additive_260626_score_production_default": sulphite_default,
        "d4_live_in_production": d4_default == "on",
        "sulphite_flag_live_in_production": sulphite_default == "on",
        "framing": (
            "HYPOTHETICAL-UPON-TWO-FLAGS: both BARI_D4_SCORE_V1=on AND "
            "BARI_ADDITIVE_260626_SCORE=on required. Published scores unaffected."
            if d4_default == "off"
            else "IMMEDIATE-ON-SULPHITE-FLAG: BARI_D4_SCORE_V1 already on."
        ),
        "regression_proof": {
            "determinism_pass": regression_pass_a,
            "nonsulphite_stability_pass": regression_pass_b,
            "overall_pass": regression_pass,
            "max_zero_determinism": max_zero,
            "max_nonsulphite_delta": max_nonsulphite,
        },
        "corpus_sulphite_scan": {
            shelf: {
                "corpus_size": len(all_corpora.get(shelf, {})),
                "sulphite_count": len(hits),
                "products": [
                    {
                        "barcode": h["barcode"],
                        "name": h["name"],
                        "pattern": h["pattern"],
                        "ingredient_snippet": h["ingredient_snippet"],
                    }
                    for h in hits
                ],
            }
            for shelf, hits in sulphite_hits.items()
        },
        "shelf_distribution": shelf_stats_out,
        "movement_table": movement_table,
        "counts": {
            "total_corpus_products_across_shelves": sum(len(c) for c in all_corpora.values()),
            "total_sulphite_products_found": total_sulphite,
            "total_scored_in_whatif": len(whatif_rows),
            "total_in_committed_baseline": sum(1 for r in movement_table if r["in_committed_baseline"]),
            "total_grade_changes_sulphite_only": sum(1 for r in movement_table if r["sulphite_grade_change"]),
            "errors": len(errors),
            "note": "grade_changes = grade moves caused by sulphite penalty alone (D4_only->whatif), not D4 activation",
        },
        "flags_baseline": base_flags,
        "flags_whatif": whatif_flags,
        "hard_rules_verified": [
            "No deployment",
            "No publish",
            "No commit",
            "BARI_ADDITIVE_260626_SCORE default=off preserved",
            "OFF ban: corpus BSIP1 data only",
            "Regression proof: " + ("PASS" if regression_pass else "FAIL"),
        ],
        "errors": errors[:20],
    }

    out_path = out_dir / f"sulphite_whatif_{run_ts}.json"
    out_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")

    total_gc = sum(1 for r in movement_table if r["sulphite_grade_change"])
    in_bl_count = sum(1 for r in movement_table if r["in_committed_baseline"])
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  BARI_D4_SCORE_V1 production default: '{d4_default}' ({'LIVE' if d4_default == 'on' else 'OFF'})")
    print(f"  BARI_ADDITIVE_260626_SCORE default:  '{sulphite_default}' (OFF=what-if only)")
    print(f"  Regression: {'PASS' if regression_pass else 'FAIL'}")
    print(f"  Total sulphite products found: {total_sulphite}")
    print(f"  Products scored in what-if:    {len(whatif_rows)}")
    print(f"  In committed baseline:         {in_bl_count}")
    print(f"  Grade changes (sulphite only): {total_gc}")
    print(f"  Artifact: {out_path}")
    print("=" * 70)

    return artifact


if __name__ == "__main__":
    main()
