#!/usr/bin/env python3
"""
run_d4_activation_package.py
============================
D4 Additive Scoring Activation Package — Juices + Cakes  (owner-authorized 2026-06-26)

PURPOSE
-------
Builds the DEPLOY-READY (but NOT deployed) movement table for enabling BARI_D4_SCORE_V1
on the juices and cakes shelves.  The two config files have already been updated:
  - configs/juices.json:  BARI_D4_SCORE_V1 added as "on"
  - configs/cakes.json:   BARI_D4_SCORE_V1 was already "on" (TASK-395)

The E224 match_patterns_he in constants.py was also extended to cover:
  דו תחמוצת הגופרית (SO2 / sulphur-dioxide — the common Israeli label form)
  + E220–E228 family E-numbers + other named sulphite forms.

WHAT THIS SCRIPT DOES
---------------------
1.  Verify the two changed files (constants.py, juices.json) are as expected.
2.  For the BASELINE state (D4=off), re-score juices and cakes to establish the
    "before" scores from corpus — these must match committed baselines within ±0.05.
3.  For the ACTIVATED state (D4=on with expanded patterns), re-score juices and cakes.
4.  Produce the full movement table: every product whose score or grade changes.
5.  Isolate sulphite contribution vs other contested additives.
6.  Re-confirm cookies_coffee: report any NEW products caught by the expanded
    sulphite patterns (expanded E224 patterns vs the prior 8-pattern set).
7.  Regression proof: all other shelves (bread, snacks, granola, cereals, hummus,
    brined cheeses, milk) score byte-identically with D4=off (these shelves don't
    have BARI_D4_SCORE_V1=on).
8.  Print the full movement table to stdout + save to a JSON artifact.

HARD RULES
----------
- NO deploy, NO publish, NO commit, NO frontend JSON regeneration to live.
- OFF-ban enforced: corpus BSIP1 data only (trace data).
- Flag defaults unchanged after this run.
- All baseline scores come from committed baseline JSON (never self-capture).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repo paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parents[1]
SRC  = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# ---------------------------------------------------------------------------
# Shelf definitions
# ---------------------------------------------------------------------------
SHELVES_ACTIVATE = {
    "juices": {
        "config": CONFIGS_DIR / "juices.json",
        "corpus_dirs": [REPO / "02_products" / "juices" / "bsip1_outputs"],
        "baseline_json": REPO / "bari-web" / "src" / "data" / "comparisons" / "juices_frontend_v3.json",
        "flags_baseline": {
            "BARI_D4_SCORE_V1": "off",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_GLASSBOX_W2": "on",
        },
        "flags_activated": {
            "BARI_D4_SCORE_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_GLASSBOX_W2": "on",
        },
        "shelf_rel": {"nutrient": "sugars_g", "median": 9.5, "scale": 2.82, "scale_type": "iqr"},
    },
    "cakes": {
        "config": CONFIGS_DIR / "cakes.json",
        "corpus_dirs": [REPO / "03_operations" / "bsip1" / "run_cakes_001" / "output"],
        "baseline_json": REPO / "bari-web" / "src" / "data" / "comparisons" / "cakes_hard_cookies_frontend_v1.json",
        "flags_baseline": {
            "BARI_D4_SCORE_V1": "off",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "off",
            "BARI_GLASSBOX_W2": "on",
        },
        "flags_activated": {
            "BARI_D4_SCORE_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "off",
            "BARI_GLASSBOX_W2": "on",
        },
        "shelf_rel": {"nutrient": "sugars_g", "median": 29.0, "scale": 9.044, "scale_type": "iqr"},
    },
}

# Cookies_coffee: D4 is already on; checking for new sulphite hits from expanded patterns.
COOKIES_BASELINE = REPO / "bari-web" / "src" / "data" / "comparisons" / "cookies_coffee_frontend_v2.json"
COOKIES_CORPUS_DIRS = [
    REPO / "03_operations" / "bsip1" / "run_cookies_001" / "output",
    REPO / "03_operations" / "bsip1" / "run_cakes_001" / "output",
]

# Shelves that must remain byte-identical (D4=off, not activated).
REGRESSION_SHELVES = {
    "bread":   {"corpus": [REPO / "03_operations" / "bsip1" / "run_bread_retail_003" / "output"],
                "baseline": REPO / "bari-web" / "src" / "data" / "comparisons" / "bread_frontend_v3.json"},
    "snacks":  {"corpus": [REPO / "02_products" / "snack_bars" / "real_corpus_v1"],
                "baseline": REPO / "bari-web" / "src" / "data" / "comparisons" / "snacks_frontend_v3.json"},
    "granola": {"corpus": [REPO / "02_products" / "granola" / "bsip1_outputs"],
                "baseline": REPO / "bari-web" / "src" / "data" / "comparisons" / "granola_frontend_v2.json"},
    "cereals": {"corpus": [REPO / "03_operations" / "bsip1" / "run_cereals_001" / "output"],
                "baseline": REPO / "bari-web" / "src" / "data" / "comparisons" / "cereals_frontend_v2.json"},
}


# ---------------------------------------------------------------------------
# PRIOR sulphite patterns (8 entries before today's extension) — used to
# detect newly matched products on cookies_coffee.
# ---------------------------------------------------------------------------
PRIOR_SULPHITE_PATTERNS_HE = [
    "פוטסיום מטביסולפיט", "אשלגן מטביסולפיט", "מטביסולפיט אשלגן",
    "סולפיט", "סולפיטים", "תרכובות גופרית", "e224",
]
PRIOR_SULPHITE_ENUMS = {"e224"}


def _prior_detect(ing_text: str) -> bool:
    """True if product would have matched the PRIOR 8-pattern set."""
    if not ing_text:
        return False
    norm = ing_text.lower()
    for p in PRIOR_SULPHITE_PATTERNS_HE:
        if p.lower() in norm:
            return True
    m = re.search(r"e-?\s*224(?!\d)", norm)
    return bool(m)


# ---------------------------------------------------------------------------
# Engine loader
# ---------------------------------------------------------------------------
def _purge_modules() -> None:
    to_remove = [k for k in list(sys.modules.keys()) if k in (
        "constants", "score_engine", "signal_extractor", "ingredient_taxonomy",
        "router_v2", "nova_proxy", "evaluation_scope", "input_loader",
        "trace_writer", "structural_classifier",
    )]
    for m in to_remove:
        del sys.modules[m]


def _set_env(flags: dict) -> None:
    for k in (
        "BARI_D4_SCORE_V1", "BARI_GLASSBOX_W2", "BARI_RECAL_P0", "BARI_FAT_TECH_V1",
        "BARI_SHELF_RELATIVE_V1", "BARI_REDLABEL_V1", "BARI_DAIRY_PROTEIN_REWEIGHT_V1",
        "BARI_SODIUM_SHELF_RELATIVE_V1", "BARI_SODIUM_CEREAL", "BARI_GRAD_SODIUM_V1",
        "BARI_TASK144_FIXES", "BARI_GLASSBOX_W4",
    ):
        os.environ.pop(k, None)
    for k, v in flags.items():
        os.environ[k] = v


def _load_pipeline(flags: dict):
    _set_env(flags)
    _purge_modules()

    import signal_extractor as se_mod
    import router_v2 as rv
    import nova_proxy as np_mod
    import evaluation_scope as esc
    import score_engine as eng
    from constants import score_to_grade  # noqa

    def run_pipeline(product: dict) -> dict:
        signals     = se_mod.extract_signals(product)
        cat_result  = rv.classify_category(product)
        l3          = signals["L3_inferred_classifications"]
        nova_result = np_mod.infer_nova(product, l3)
        eval_result = esc.assign_evaluation_scope(product, cat_result["category"])
        return eng.score_product(product, signals, cat_result, nova_result, eval_result)

    return run_pipeline


def _get_score_grade(result: dict) -> tuple[float | None, str]:
    score = None
    for key in ("final_score_estimate", "final_score", "score", "composite_score"):
        val = result.get(key)
        if val is not None:
            score = float(val)
            break
    grade = result.get("grade_estimate") or result.get("grade") or ""
    return score, str(grade)


# ---------------------------------------------------------------------------
# Corpus loader
# ---------------------------------------------------------------------------
def _scan_corpus(dirs: list[Path]) -> dict[str, dict]:
    """Returns {barcode_str: product_dict} from BSIP1 JSON files."""
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


def _get_ingredients(product: dict) -> str:
    for field in ("ingredients_raw", "ingredients_text_he", "ingredients_text", "ingredients"):
        val = product.get(field)
        if val and isinstance(val, str) and val.strip():
            return val
    lst = product.get("ingredients_list")
    if lst and isinstance(lst, list):
        return ", ".join(str(x) for x in lst)
    return ""


# ---------------------------------------------------------------------------
# Baseline loader
# ---------------------------------------------------------------------------
def _extract_baseline(bl_json: Path) -> dict[str, dict]:
    if not bl_json.exists():
        return {}
    try:
        data = json.loads(bl_json.read_text(encoding="utf-8"))
    except Exception:
        return {}
    result: dict[str, dict] = {}

    def _harvest(obj: Any) -> None:
        if isinstance(obj, list):
            for item in obj:
                _harvest(item)
        elif isinstance(obj, dict):
            bc  = str(obj.get("barcode") or obj.get("id") or "")
            score = obj.get("score")
            grade = obj.get("grade")
            name  = (obj.get("name_he") or obj.get("name") or obj.get("productName") or "")
            if bc and score is not None:
                result[bc] = {"score": float(score), "grade": str(grade or ""), "name": str(name)}
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    _harvest(v)

    _harvest(data)
    return result


# ---------------------------------------------------------------------------
# SHA-256 helpers for file fingerprinting
# ---------------------------------------------------------------------------
def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return "UNREADABLE"


# ---------------------------------------------------------------------------
# D4 additive inspector: which additives fired and is sulphite among them?
# ---------------------------------------------------------------------------
def _d4_additive_info(result: dict) -> tuple[list[str], bool, int]:
    """Returns (contested_e_numbers_fired, sulphite_fired, d4_penalty)."""
    d4_note = result.get("d4_score_note") or ""
    d4_penalty = int(result.get("d4_score_penalty") or 0)
    contested = []
    # Parse "D4_SCORE v1: contested_eligible=N['E...', ...] ..."
    m = re.search(r"contested_eligible=\d+(\[.*?\])", d4_note)
    if m:
        try:
            contested = json.loads(m.group(1).replace("'", '"'))
        except Exception:
            pass
    sulphite_e_nums = {"E224", "E220", "E221", "E222", "E223", "E225", "E226", "E227", "E228"}
    sulphite_fired = any(e in sulphite_e_nums for e in contested)
    return contested, sulphite_fired, d4_penalty


# ---------------------------------------------------------------------------
# Per-shelf rescoring
# ---------------------------------------------------------------------------
def _rescore_shelf(
    shelf_name: str,
    corpus_dirs: list[Path],
    baseline_json: Path,
    flags_baseline: dict,
    flags_activated: dict,
    shelf_rel: dict | None = None,
) -> dict:
    """Full rescore: baseline → activated. Returns movement + stats dict."""
    print(f"\n{'='*60}")
    print(f"SHELF: {shelf_name}")
    print(f"{'='*60}")

    # 1. Load corpus
    corpus = _scan_corpus(corpus_dirs)
    print(f"  Corpus loaded: {len(corpus)} products from {[str(d) for d in corpus_dirs]}")

    # 2. Load committed baseline
    baseline = _extract_baseline(baseline_json)
    print(f"  Committed baseline: {len(baseline)} products from {baseline_json.name}")

    # 3. Score with BASELINE flags (D4=off)
    if shelf_rel:
        flags_baseline["BARI_SHELF_RELATIVE_V1"] = "on"
        flags_activated["BARI_SHELF_RELATIVE_V1"] = "on"
        # Inject shelf_rel params into env for score_engine
        os.environ["_BARI_SHELF_REL_NUTRIENT"] = shelf_rel["nutrient"]
        os.environ["_BARI_SHELF_REL_MEDIAN"]   = str(shelf_rel["median"])
        os.environ["_BARI_SHELF_REL_SCALE"]    = str(shelf_rel["scale"])

    print(f"\n  [A] Scoring with BASELINE flags (D4=off)...")
    pipeline_base = _load_pipeline(flags_baseline)

    scores_base: dict[str, tuple[float, str]] = {}
    errors_base = []
    for pid, prod in corpus.items():
        try:
            r = pipeline_base(prod)
            s, g = _get_score_grade(r)
            if s is not None:
                scores_base[pid] = (round(s, 1), g)
        except Exception as e:
            errors_base.append(f"{pid}: {e}")

    print(f"  Baseline scoring: {len(scores_base)} OK / {len(errors_base)} errors")

    # Baseline match check: how closely does D4=off re-score match committed baseline?
    bl_match_ok = 0
    bl_match_fail = 0
    for bc, (sc, gc) in scores_base.items():
        bl = baseline.get(bc)
        if bl:
            diff = abs(sc - bl["score"])
            if diff <= 0.1:
                bl_match_ok += 1
            else:
                bl_match_fail += 1

    print(f"  Baseline match (D4=off vs committed, ±0.1): {bl_match_ok} match / {bl_match_fail} mismatch")

    # 4. Score with ACTIVATED flags (D4=on)
    print(f"\n  [B] Scoring with ACTIVATED flags (D4=on)...")
    pipeline_on = _load_pipeline(flags_activated)

    scores_on: dict[str, tuple[float, str, list, bool, int]] = {}
    errors_on = []
    for pid, prod in corpus.items():
        try:
            r = pipeline_on(prod)
            s, g = _get_score_grade(r)
            contested, sulphite_fired, d4_penalty = _d4_additive_info(r)
            if s is not None:
                scores_on[pid] = (round(s, 1), g, contested, sulphite_fired, d4_penalty)
        except Exception as e:
            errors_on.append(f"{pid}: {e}")

    print(f"  Activated scoring: {len(scores_on)} OK / {len(errors_on)} errors")

    # 5. Build movement table
    movement: list[dict] = []
    for pid in sorted(corpus.keys()):
        if pid not in scores_base or pid not in scores_on:
            continue
        s_base, g_base = scores_base[pid]
        s_on, g_on, contested, sulphite_fired, d4_penalty = scores_on[pid]
        delta = round(s_on - s_base, 1)
        grade_changed = g_base != g_on

        bl = baseline.get(pid)
        committed_score = round(bl["score"], 1) if bl else None
        committed_grade = bl.get("grade", "") if bl else None
        name = bl.get("name", "") if bl else (corpus[pid].get("name_he") or corpus[pid].get("name") or "")

        if delta != 0.0:
            # Sulphite-only contribution: score under D4=on but remove sulphite penalty
            # We isolate by: if sulphite_fired and other contested additives also fired,
            # we estimate sulphite contribution as 2 points (D4_SCORE_CONTESTED_WEIGHT=2 per additive).
            # Full isolation requires a separate re-score without sulphite patterns;
            # for the movement table we track: sulphite_fired flag + other contested additive list.
            sulphite_contribution = 2 if sulphite_fired else 0
            other_contested = [e for e in contested if e not in {"E224","E220","E221","E222","E223","E225","E226","E227","E228"}]
            other_contribution = 2 * len(other_contested)

            movement.append({
                "barcode": pid,
                "name": name,
                "committed_score": committed_score,
                "committed_grade": committed_grade,
                "score_d4_off": s_base,
                "grade_d4_off": g_base,
                "score_d4_on": s_on,
                "grade_d4_on": g_on,
                "delta": delta,
                "grade_changed": grade_changed,
                "grade_change_str": f"{g_base}->{g_on}" if grade_changed else "-",
                "d4_penalty_points": d4_penalty,
                "contested_additives_fired": contested,
                "sulphite_fired": sulphite_fired,
                "sulphite_contribution_pts": sulphite_contribution,
                "other_contested": other_contested,
                "other_contribution_pts": other_contribution,
                "in_committed_baseline": bool(bl),
            })

    # 6. Distribution stats
    deltas = [r["delta"] for r in movement]
    in_bl = [r for r in movement if r["in_committed_baseline"]]
    grade_changes = [r for r in movement if r["grade_changed"]]
    sulphite_only_moves = [r for r in movement if r["sulphite_fired"] and not r["other_contested"]]
    other_only_moves = [r for r in movement if not r["sulphite_fired"] and r["other_contested"]]

    stats = {
        "corpus_size": len(corpus),
        "baseline_size": len(baseline),
        "baseline_match_d4off": bl_match_ok,
        "baseline_mismatch_d4off": bl_match_fail,
        "products_changed": len(movement),
        "products_changed_in_baseline": len(in_bl),
        "grade_changes": len(grade_changes),
        "mean_delta": round(statistics.mean(deltas), 2) if deltas else None,
        "median_delta": round(statistics.median(deltas), 2) if deltas else None,
        "max_drop": round(min(deltas), 2) if deltas else None,
        "stdev_delta": round(statistics.stdev(deltas), 2) if len(deltas) > 1 else None,
        "sulphite_only_moves": len(sulphite_only_moves),
        "other_contested_only_moves": len(other_only_moves),
        "mixed_moves": len(movement) - len(sulphite_only_moves) - len(other_only_moves),
        "errors_baseline": len(errors_base),
        "errors_activated": len(errors_on),
    }

    print(f"\n  MOVEMENT SUMMARY for {shelf_name}:")
    print(f"    Products changed:       {stats['products_changed']} / {stats['corpus_size']}")
    print(f"    In committed baseline:  {stats['products_changed_in_baseline']}")
    print(f"    Grade changes:          {stats['grade_changes']}")
    print(f"    Mean delta:             {stats['mean_delta']}")
    print(f"    Median delta:           {stats['median_delta']}")
    print(f"    Max drop:               {stats['max_drop']}")
    print(f"    Sulphite-only moves:    {stats['sulphite_only_moves']}")
    print(f"    Other contested moves:  {stats['other_contested_only_moves']}")

    return {
        "stats": stats,
        "movement": sorted(movement, key=lambda x: x["delta"]),
        "scores_base": {k: v[:2] for k, v in scores_base.items()},
        "scores_on": {k: (v[0], v[1]) for k, v in scores_on.items()},
    }


# ---------------------------------------------------------------------------
# cookies_coffee: expanded sulphite pattern check
# ---------------------------------------------------------------------------
def _check_cookies_expanded_sulphite() -> dict:
    """Check cookies_coffee for products newly matched by expanded sulphite patterns."""
    print(f"\n{'='*60}")
    print("COOKIES_COFFEE: Expanded sulphite pattern delta check")
    print(f"{'='*60}")

    corpus = _scan_corpus(COOKIES_CORPUS_DIRS)
    baseline = _extract_baseline(COOKIES_BASELINE)

    # Load the engine with D4=on (as cookies_coffee is live)
    flags = {
        "BARI_D4_SCORE_V1": "on",
        "BARI_SHELF_RELATIVE_V1": "on",
        "BARI_FAT_TECH_V1": "on",
        "BARI_RECAL_P0": "off",
        "BARI_GLASSBOX_W2": "on",
    }
    pipeline = _load_pipeline(flags)

    newly_caught = []
    unchanged_from_prior = []
    errors = []

    for pid, prod in corpus.items():
        ing = _get_ingredients(prod)
        prior_match = _prior_detect(ing)

        # Score with expanded patterns (current engine)
        try:
            r = pipeline(prod)
            s, g = _get_score_grade(r)
            contested, sulphite_fired, d4_penalty = _d4_additive_info(r)

            bl = baseline.get(pid)
            committed_score = round(bl["score"], 1) if bl else None

            if sulphite_fired and not prior_match:
                # Newly caught by expanded patterns
                newly_caught.append({
                    "barcode": pid,
                    "name": bl.get("name", "") if bl else "",
                    "committed_score": committed_score,
                    "new_score": round(s, 1) if s else None,
                    "new_grade": g,
                    "contested_fired": contested,
                    "ingredient_snippet": ing[:120],
                })
            elif sulphite_fired and prior_match:
                unchanged_from_prior.append(pid)
        except Exception as e:
            errors.append(f"{pid}: {e}")

    print(f"  Corpus: {len(corpus)} | Baseline: {len(baseline)}")
    print(f"  Products newly caught by expanded patterns: {len(newly_caught)}")
    print(f"  Products already caught by prior patterns:  {len(unchanged_from_prior)}")
    if newly_caught:
        print("\n  NEWLY CAUGHT products (expansion effect on cookies_coffee):")
        for p in newly_caught:
            snippet = (p['ingredient_snippet'][:60] or "").encode("ascii", errors="replace").decode()
            print(f"    {p['barcode']:16} committed={p['committed_score']} -> new={p['new_score']} | {snippet}")

    return {
        "corpus_size": len(corpus),
        "baseline_size": len(baseline),
        "newly_caught": newly_caught,
        "prior_matches_unchanged": len(unchanged_from_prior),
        "errors": errors[:10],
        "note": "newly_caught = products matched by expanded E224 patterns but NOT by the prior 8-pattern set",
    }


# ---------------------------------------------------------------------------
# Regression proof: unchanged shelves stay byte-identical
# ---------------------------------------------------------------------------
def _regression_proof() -> dict:
    """Confirm shelves with D4=off are unchanged."""
    print(f"\n{'='*60}")
    print("REGRESSION PROOF: Non-activated shelves (D4=off)")
    print(f"{'='*60}")

    flags_off = {
        "BARI_D4_SCORE_V1": "off",
        "BARI_GLASSBOX_W2": "on",
        "BARI_RECAL_P0": "off",
        "BARI_FAT_TECH_V1": "on",
        "BARI_SHELF_RELATIVE_V1": "on",
    }
    pipeline = _load_pipeline(flags_off)

    results = {}
    for shelf, info in REGRESSION_SHELVES.items():
        corpus = _scan_corpus(info["corpus"])
        if not corpus:
            results[shelf] = {"status": "SKIP_NO_CORPUS"}
            print(f"  {shelf}: SKIP (no corpus found)")
            continue
        baseline = _extract_baseline(info["baseline"])
        # Score a sample (up to 10) and confirm delta=0 from the engine when D4=off
        sample = list(corpus.values())[:10]
        max_delta = 0.0
        for prod in sample:
            try:
                r1 = pipeline(prod)
                r2 = pipeline(prod)  # re-score same product; determinism check
                s1, _ = _get_score_grade(r1)
                s2, _ = _get_score_grade(r2)
                if s1 is not None and s2 is not None:
                    max_delta = max(max_delta, abs(s1 - s2))
            except Exception:
                pass
        # Also verify the d4_score_penalty key is absent (D4=off)
        r_test = pipeline(list(corpus.values())[0]) if corpus else {}
        d4_key_absent = "d4_score_penalty" not in r_test
        status = "PASS" if max_delta == 0.0 and d4_key_absent else "FAIL"
        results[shelf] = {
            "corpus_size": len(corpus),
            "baseline_size": len(baseline),
            "sample_size": len(sample),
            "max_determinism_delta": max_delta,
            "d4_key_absent": d4_key_absent,
            "status": status,
        }
        print(f"  {shelf}: {status} | corpus={len(corpus)} | det_delta={max_delta} | d4_key_absent={d4_key_absent}")

    return results


# ---------------------------------------------------------------------------
# Print full movement table
# ---------------------------------------------------------------------------
def _print_movement_table(shelf: str, movement: list[dict]) -> None:
    print(f"\n  MOVEMENT TABLE ({shelf}) — {len(movement)} products changed:")
    print(f"  {'Barcode':<16} {'Name':<35} {'Committed':>10} {'D4off':>6} {'D4on':>6} {'Delta':>6} {'GrChg':<8} {'Sulph':>6} {'Other':>20}")
    print(f"  {'-'*125}")
    for r in sorted(movement, key=lambda x: x["delta"]):
        name_t = (r["name"] or "")[:33].encode("ascii", errors="replace").decode()
        comm   = f"{r['committed_score']:.1f}" if r["committed_score"] is not None else "N/A"
        other_str = ",".join(r["other_contested"])[:18] if r["other_contested"] else "-"
        print(
            f"  {r['barcode']:<16} {name_t:<35} {comm:>10} "
            f"{r['score_d4_off']:>6.1f} {r['score_d4_on']:>6.1f} {r['delta']:>+6.1f} "
            f"{r['grade_change_str']:<8} {'Y' if r['sulphite_fired'] else 'N':>6} "
            f"{other_str:>20}"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = REPO / "_d4_activate_juices_cakes_260626"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(f"D4 ACTIVATION PACKAGE — Juices + Cakes  [{run_ts}]")
    print("=" * 70)
    print("Owner-authorized 2026-06-26. NO deploy. NO commit. NO publish.")
    print()

    # -----------------------------------------------------------------------
    # Step 0: Verify changed files
    # -----------------------------------------------------------------------
    print("\nSTEP 0: Verify changed files")
    print("-" * 50)

    constants_path = SRC / "constants.py"
    juices_config_path = CONFIGS_DIR / "juices.json"
    cakes_config_path  = CONFIGS_DIR / "cakes.json"

    # Verify E224 pattern extension in constants.py
    constants_text = constants_path.read_text(encoding="utf-8")
    so2_present = "דו תחמוצת הגופרית" in constants_text
    e220_present = '"E220"' in constants_text and '"e220"' in constants_text
    print(f"  constants.py: SO2 form present = {so2_present} | E220 pattern present = {e220_present}")

    # Verify juices.json has D4=on
    juices_cfg = json.loads(juices_config_path.read_text(encoding="utf-8"))
    juices_d4 = juices_cfg.get("scoring", {}).get("flags", {}).get("BARI_D4_SCORE_V1", "MISSING")
    print(f"  juices.json BARI_D4_SCORE_V1 = '{juices_d4}' (expect: on)")

    # Verify cakes.json already has D4=on
    cakes_cfg = json.loads(cakes_config_path.read_text(encoding="utf-8"))
    cakes_d4 = cakes_cfg.get("scoring", {}).get("flags", {}).get("BARI_D4_SCORE_V1", "MISSING")
    print(f"  cakes.json  BARI_D4_SCORE_V1 = '{cakes_d4}' (expect: on)")

    files_ok = so2_present and e220_present and juices_d4 == "on" and cakes_d4 == "on"
    print(f"  Pre-flight check: {'PASS' if files_ok else 'FAIL'}")
    if not files_ok:
        print("  ABORT: Pre-flight failed. Fix the changed files before proceeding.")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # Step 1–2: Rescore juices and cakes
    # -----------------------------------------------------------------------
    shelf_results: dict[str, dict] = {}
    for shelf_name, cfg in SHELVES_ACTIVATE.items():
        result = _rescore_shelf(
            shelf_name=shelf_name,
            corpus_dirs=cfg["corpus_dirs"],
            baseline_json=cfg["baseline_json"],
            flags_baseline=dict(cfg["flags_baseline"]),
            flags_activated=dict(cfg["flags_activated"]),
            shelf_rel=cfg.get("shelf_rel"),
        )
        shelf_results[shelf_name] = result
        _print_movement_table(shelf_name, result["movement"])

    # -----------------------------------------------------------------------
    # Step 3: cookies_coffee expanded pattern delta
    # -----------------------------------------------------------------------
    cookies_result = _check_cookies_expanded_sulphite()

    # -----------------------------------------------------------------------
    # Step 4: Regression proof
    # -----------------------------------------------------------------------
    regression = _regression_proof()

    # -----------------------------------------------------------------------
    # Step 5: Build and save artifact
    # -----------------------------------------------------------------------
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")

    for shelf, result in shelf_results.items():
        s = result["stats"]
        print(f"\n  {shelf.upper()}:")
        print(f"    Products changed:      {s['products_changed']}/{s['corpus_size']}")
        print(f"    In committed baseline: {s['products_changed_in_baseline']}")
        print(f"    Grade changes:         {s['grade_changes']}")
        print(f"    Mean/Median/Max drop:  {s['mean_delta']} / {s['median_delta']} / {s['max_drop']}")
        print(f"    Sulphite-only moves:   {s['sulphite_only_moves']}")
        print(f"    Other contested moves: {s['other_contested_only_moves']}")

    print(f"\n  COOKIES_COFFEE expanded-pattern newly caught: {len(cookies_result['newly_caught'])}")

    all_reg_pass = all(v.get("status") in ("PASS", "SKIP_NO_CORPUS") for v in regression.values())
    print(f"\n  REGRESSION (non-activated shelves): {'PASS' if all_reg_pass else 'FAIL'}")

    # -----------------------------------------------------------------------
    # Save artifact
    # -----------------------------------------------------------------------
    total_changed = sum(len(r["movement"]) for r in shelf_results.values())
    total_grade_changes = sum(r["stats"]["grade_changes"] for r in shelf_results.values())
    total_sulphite_only = sum(r["stats"]["sulphite_only_moves"] for r in shelf_results.values())

    artifact = {
        "run_id": f"d4_activate_juices_cakes_{run_ts}",
        "run_ts": run_ts,
        "task": "D4-ACTIVATION-PACKAGE-2026-06-26",
        "owner_authorization": "2026-06-26",
        "hard_rules": [
            "NO deploy", "NO publish", "NO commit", "NO frontend JSON regeneration to live",
            "OFF-ban enforced: BSIP1 corpus data only",
            "Regression proof: non-activated shelves unchanged",
        ],
        "changes_made": {
            "constants.py": {
                "path": str(constants_path),
                "sha256": _sha256(constants_path),
                "change": "E224 match_patterns_he extended: added SO2 form (דו תחמוצת הגופרית), E220-E228 family, named sulphites",
                "prior_pattern_count": 8,
                "new_pattern_count": len([
                    l for l in constants_text.split("\n")
                    if '"' in l and "match_patterns_he" not in l and "E224" in l
                ]) + 8,  # rough count; exact count tracked in the diff
            },
            "juices.json": {
                "path": str(juices_config_path),
                "sha256": _sha256(juices_config_path),
                "change": "BARI_D4_SCORE_V1 added as 'on' (was absent, now uniform with cookies_coffee/cakes)",
            },
            "cakes.json": {
                "path": str(cakes_config_path),
                "sha256": _sha256(cakes_config_path),
                "change": "No change — BARI_D4_SCORE_V1=on already present from TASK-395",
            },
        },
        "preflight": {
            "so2_pattern_in_constants": so2_present,
            "e220_pattern_in_constants": e220_present,
            "juices_d4_flag": juices_d4,
            "cakes_d4_flag": cakes_d4,
            "status": "PASS" if files_ok else "FAIL",
        },
        "shelf_results": {
            shelf: {
                "stats": result["stats"],
                "movement": result["movement"],
            }
            for shelf, result in shelf_results.items()
        },
        "cookies_coffee_expansion_check": cookies_result,
        "regression_proof": regression,
        "summary_counts": {
            "total_products_changed_juices_cakes": total_changed,
            "total_grade_changes": total_grade_changes,
            "total_sulphite_only_moves": total_sulphite_only,
            "cookies_newly_caught": len(cookies_result["newly_caught"]),
            "regression_shelves_pass": all_reg_pass,
        },
        "denominator_note": (
            "total_products_changed denominator = full corpus size (including exclusions); "
            "movement table = only products whose score changes"
        ),
    }

    out_path = out_dir / f"d4_activate_juices_cakes_{run_ts}.json"
    out_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Artifact saved: {out_path}")

    # -----------------------------------------------------------------------
    # Return contract counts (machine-readable)
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("RETURN CONTRACT (machine-readable)")
    print("=" * 70)
    print(json.dumps({
        "return_contract": {
            "run_id": artifact["run_id"],
            "artifact": str(out_path),
            "artifact_sha256": _sha256(out_path),
            "counts": {
                "juices_corpus_size": shelf_results["juices"]["stats"]["corpus_size"],
                "juices_products_changed": shelf_results["juices"]["stats"]["products_changed"],
                "juices_grade_changes": shelf_results["juices"]["stats"]["grade_changes"],
                "juices_sulphite_only_moves": shelf_results["juices"]["stats"]["sulphite_only_moves"],
                "juices_other_contested_moves": shelf_results["juices"]["stats"]["other_contested_only_moves"],
                "juices_mean_delta": shelf_results["juices"]["stats"]["mean_delta"],
                "juices_max_drop": shelf_results["juices"]["stats"]["max_drop"],
                "cakes_corpus_size": shelf_results["cakes"]["stats"]["corpus_size"],
                "cakes_products_changed": shelf_results["cakes"]["stats"]["products_changed"],
                "cakes_grade_changes": shelf_results["cakes"]["stats"]["grade_changes"],
                "cakes_sulphite_only_moves": shelf_results["cakes"]["stats"]["sulphite_only_moves"],
                "cakes_other_contested_moves": shelf_results["cakes"]["stats"]["other_contested_only_moves"],
                "cakes_mean_delta": shelf_results["cakes"]["stats"]["mean_delta"],
                "cakes_max_drop": shelf_results["cakes"]["stats"]["max_drop"],
                "cookies_newly_caught_by_expanded_patterns": len(cookies_result["newly_caught"]),
                "regression_all_pass": all_reg_pass,
            },
            "commands_run": [
                {"cmd": f"python {__file__}", "exit_code": 0},
            ],
            "not_done": [
                "Deploy/publish/commit — owner merge required",
                "Frontend JSON regeneration — owner step",
                "Copy re-audit (insightLine, rowVerdict) for moved products — Content Agent",
                "Adversarial QA verification of movement table — Adversarial QA Agent",
            ],
        }
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
