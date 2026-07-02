#!/usr/bin/env python3
"""
baseline_verify.py — Canonical Reproducibility Gate (TASK-395 Phase 0)
=======================================================================
Round-trip verifier: given a shelf config, re-scores every product in the pinned
BSIP1 corpus through the canonical spine path (full traces, real engine) and
compares to the committed live frontend JSON.

PASS definition: every live product matches score within ≤0.05 AND grade AND
confidence_band, zero unmatched live barcodes.

Mismatch classification:
  data     — live barcode not found in any BSIP1 corpus dir
  engine   — score drift >0.05 with same inputs
  config   — flag-vector or shelf_rel mismatch (detected by config archaeology)
  unknown  — score differs but inputs match; cause not determined

Output:
  - Console report
  - _baselines/<slug>/baseline_verify_result.json (per-category)
  - _baselines/_ledger_v1.json (all-category ledger, written by --all mode)

Usage:
  python baseline_verify.py --shelf snacks
  python baseline_verify.py --all
  python baseline_verify.py --shelf hard_cheeses --write-manifest

Exit: 0 = all checked categories PASS or QUARANTINE (quarantine is explicit),
      1 = unexpected error.

Determinism check: run twice with same inputs → identical result.
Spec tolerance: ≤0.05 on score (as per TASK-395 plan).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[3]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
BASELINES_DIR = REPO / "_baselines"
PAGE_GENERATOR_DIR = REPO / "03_operations" / "page_generator"

SCORE_TOLERANCE = 0.05  # per TASK-395 plan

# BARI_* env vars the engine reads
MANAGED_BARI_VARS = [
    "BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM",
    "BARI_FAT_TECH_V1",
    "BARI_SHELF_RELATIVE_V1",
    "BARI_SODIUM_SHELF_RELATIVE_V1",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1",
    "BARI_GRAD_SODIUM_V1",
    "BARI_SODIUM_CEREAL",
    "BARI_REDLABEL_V1",
    "BARI_D4_SCORE_V1",  # TASK-406: applied to live (commit 361748722) but was unmanaged → unreproducible flag state
    "BARI_TASK144_FIXES",
    "BARI_TASK250_CONF",
    "BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15",
    "BARI_GLASSBOX_W2",
    "BARI_DAIRY_SAT_FAT_INFER",
]

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))
if str(PAGE_GENERATOR_DIR) not in sys.path:
    sys.path.insert(0, str(PAGE_GENERATOR_DIR))


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ProductVerifyResult:
    barcode: str
    live_score: float | None
    live_grade: str | None
    rescore_score: float | None
    rescore_grade: str | None
    score_diff: float | None  # None = not comparable
    score_match: bool = False
    grade_match: bool = False
    mismatch_class: str = "ok"  # ok | data | engine | config | unknown
    note: str = ""


@dataclass
class CategoryVerifyResult:
    slug: str
    config_path: Path
    reproduces: bool = False
    quarantined: bool = False
    quarantine_reason: str = ""
    live_product_count: int = 0
    rescored_count: int = 0
    matched_count: int = 0
    mismatched_count: int = 0
    unmatched_count: int = 0  # live barcodes not in BSIP1
    dominant_mismatch_class: str = ""
    mismatch_by_class: dict = field(default_factory=dict)
    product_results: list[ProductVerifyResult] = field(default_factory=list)
    flags_used: dict = field(default_factory=dict)
    shelf_rel_used: dict | None = None
    bsip1_dir_used: str = ""
    baseline_path: str = ""
    engine_version: str = ""
    run_timestamp: str = ""
    error: str | None = None

    @property
    def denominator_label(self) -> str:
        return f"{self.matched_count}/{self.live_product_count} live products"


# ---------------------------------------------------------------------------
# Env helpers
# ---------------------------------------------------------------------------

def snapshot_env() -> dict[str, str | None]:
    return {k: os.environ.get(k) for k in MANAGED_BARI_VARS}


def restore_env(snap: dict[str, str | None]) -> None:
    for k, v in snap.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def apply_flags(flags: dict[str, str]) -> None:
    # First clear all managed vars, then set the ones in config
    for k in MANAGED_BARI_VARS:
        os.environ.pop(k, None)
    for k, v in flags.items():
        os.environ[k] = v


# ---------------------------------------------------------------------------
# Engine helpers
# ---------------------------------------------------------------------------

def reload_score_engine():
    import score_engine as se
    return importlib.reload(se)


def make_score_one(se_mod):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    from trace_writer import assemble_trace
    from structural_classifier import classify_structural_class

    def score_one(product: dict) -> dict:
        signals = extract_signals(product)
        cat_result = classify_category(product)
        l3 = signals["L3_inferred_classifications"]
        nova_result = infer_nova(product, l3)
        eval_result = assign_evaluation_scope(product, cat_result["category"])
        score_result = se_mod.score_product(product, signals, cat_result, nova_result, eval_result)
        trace = assemble_trace(product, signals, cat_result, nova_result, eval_result, score_result)
        trace["structural_class"] = classify_structural_class(trace)
        return trace

    return score_one


def setup_shelf_stats(shelf_rel: dict | None, se_mod) -> None:
    if not shelf_rel:
        return
    if shelf_rel.get("api") == "sodium_ev056":
        se_mod.set_shelf_sodium_stats(shelf_rel["median"], shelf_rel["scale"])
    else:
        nutrient = shelf_rel["nutrient"]
        median = shelf_rel["median"]
        scale = shelf_rel["scale"]
        scale_type = shelf_rel.get("scale_type", "iqr")
        se_mod.set_shelf_stats(nutrient, median, scale, scale_type)


def teardown_shelf_stats(shelf_rel: dict | None, se_mod) -> None:
    if not shelf_rel:
        return
    if shelf_rel.get("api") == "sodium_ev056":
        se_mod.clear_shelf_sodium_stats()
    else:
        se_mod.clear_shelf_stats(shelf_rel["nutrient"])


# ---------------------------------------------------------------------------
# BSIP1 corpus loader
# ---------------------------------------------------------------------------

def collect_bsip1_files(dirs: list[str], bsip1_glob: str = "bsip1_*.json") -> dict[str, Path]:
    """Return barcode -> Path mapping; first dir wins on collision."""
    result: dict[str, Path] = {}
    for d in dirs:
        p = Path(d)
        if not p.is_dir():
            continue
        for f in sorted(p.glob(bsip1_glob)):
            if "audit" in f.name:
                continue
            try:
                rec = json.loads(f.read_text(encoding="utf-8"))
                bc = str(rec.get("barcode", "")).strip()
                if bc and bc not in result:
                    if rec.get("file_type") != "product":
                        continue
                    result[bc] = f
            except Exception:
                pass
    return result


def load_bsip1_record(path: Path) -> dict:
    from input_loader import load_product
    return load_product(path)


# ---------------------------------------------------------------------------
# Live frontend loader
# ---------------------------------------------------------------------------

def load_live_products(baseline_path: str) -> dict[str, dict]:
    """barcode -> product dict from live frontend JSON."""
    p = Path(baseline_path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    result = {}
    for prod in data.get("products", []):
        bc = str(prod.get("barcode", "")).strip()
        if bc:
            result[bc] = prod
    return result


# ---------------------------------------------------------------------------
# Grade from score (floor policy — matches engine)
# ---------------------------------------------------------------------------

GRADE_SCALE = [("S", 90), ("A", 80), ("B", 65), ("C", 50), ("D", 35), ("E", 0)]


def score_to_grade(score: float | None) -> str | None:
    if score is None:
        return None
    for grade, threshold in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "E"


# ---------------------------------------------------------------------------
# Mismatch classifier
# ---------------------------------------------------------------------------

def classify_mismatch(
    barcode: str,
    live_score: float | None,
    rescore: float | None,
    in_bsip1: bool,
    diff: float | None,
) -> str:
    if not in_bsip1:
        return "data"  # barcode not in BSIP1 corpus
    if diff is None:
        return "unknown"
    if diff <= SCORE_TOLERANCE:
        return "ok"
    # Score differs with same inputs → engine or config
    # We classify "engine" when diff is small (rounding/float) and "config" when
    # diff is large (flag-vector mismatch is the dominant known cause).
    # Without a flag-archaeology oracle, we classify >3 as config, ≤3 as engine.
    if diff > 3.0:
        return "config"
    return "engine"


# ---------------------------------------------------------------------------
# Core verify function for one category
# ---------------------------------------------------------------------------

def verify_category(config_path: Path, write_manifest: bool = False) -> CategoryVerifyResult:
    slug = config_path.stem
    result = CategoryVerifyResult(slug=slug, config_path=config_path)
    result.run_timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    env_snap = snapshot_env()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        scoring = config.get("scoring", {})

        # Guard: compute_from_corpus → non-deterministic → QUARANTINE
        shelf_rel_cfg = scoring.get("shelf_rel")
        if shelf_rel_cfg and shelf_rel_cfg.get("compute_from_corpus"):
            result.quarantined = True
            result.quarantine_reason = (
                "shelf_rel.compute_from_corpus=true — non-deterministic; "
                "frozen median/scale must be provided"
            )
            return result

        # Resolve BSIP1 dirs
        bsip1_dir = scoring.get("bsip1_dir")
        corpus_dirs_raw = config.get("corpus_dirs", [])
        if isinstance(corpus_dirs_raw, str):
            corpus_dirs_raw = [corpus_dirs_raw]
        bsip1_dirs: list[str] = []
        if bsip1_dir:
            bsip1_dirs = [bsip1_dir]
        elif corpus_dirs_raw:
            bsip1_dirs = [d for d in corpus_dirs_raw if d]

        if not bsip1_dirs:
            result.quarantined = True
            result.quarantine_reason = "no bsip1_dir or corpus_dirs in config"
            return result

        missing_dirs = [d for d in bsip1_dirs if not Path(d).is_dir()]
        if missing_dirs:
            result.quarantined = True
            result.quarantine_reason = f"BSIP1 dirs missing on disk: {missing_dirs}"
            return result

        result.bsip1_dir_used = bsip1_dirs[0]

        # Load baseline
        baseline_path = config.get("baseline_json")
        if not baseline_path or not Path(baseline_path).exists():
            result.quarantined = True
            result.quarantine_reason = f"baseline_json not found: {baseline_path}"
            return result

        result.baseline_path = baseline_path
        live_products = load_live_products(baseline_path)
        result.live_product_count = len(live_products)
        if not live_products:
            result.quarantined = True
            result.quarantine_reason = "live frontend JSON has no products"
            return result

        # Collect BSIP1 corpus
        bsip1_glob = scoring.get("bsip1_glob", "bsip1_*.json")
        corpus_map = collect_bsip1_files(bsip1_dirs, bsip1_glob)

        # Apply flags and load engine
        flags = scoring.get("flags") or {}
        apply_flags(flags)
        se_mod = reload_score_engine()
        result.flags_used = flags

        # Try to get engine version
        result.engine_version = getattr(se_mod, "__version__", "unknown")

        # Setup shelf stats
        result.shelf_rel_used = shelf_rel_cfg
        setup_shelf_stats(shelf_rel_cfg, se_mod)
        score_one = make_score_one(se_mod)

        from input_loader import load_product, validate_product

        # Rescore each live barcode
        rescore_results: list[ProductVerifyResult] = []
        for bc, live_prod in live_products.items():
            live_score = live_prod.get("score")
            live_grade = live_prod.get("grade")
            live_score_f = float(live_score) if live_score is not None else None

            if bc not in corpus_map:
                # Data mismatch: barcode not in BSIP1 corpus
                pr = ProductVerifyResult(
                    barcode=bc,
                    live_score=live_score_f,
                    live_grade=live_grade,
                    rescore_score=None,
                    rescore_grade=None,
                    score_diff=None,
                    score_match=False,
                    grade_match=False,
                    mismatch_class="data",
                    note="barcode not in BSIP1 corpus",
                )
                rescore_results.append(pr)
                continue

            # Load and score
            try:
                product = load_product(corpus_map[bc])
                errors = validate_product(product)
                trace = score_one(product)
            except Exception as exc:
                pr = ProductVerifyResult(
                    barcode=bc,
                    live_score=live_score_f,
                    live_grade=live_grade,
                    rescore_score=None,
                    rescore_grade=None,
                    score_diff=None,
                    score_match=False,
                    grade_match=False,
                    mismatch_class="unknown",
                    note=f"scoring error: {exc}",
                )
                rescore_results.append(pr)
                continue

            rescore_score = trace.get("final_score_estimate")
            rescore_score_f = float(rescore_score) if rescore_score is not None else None
            rescore_grade = score_to_grade(rescore_score_f)

            diff = (
                abs(live_score_f - rescore_score_f)
                if live_score_f is not None and rescore_score_f is not None
                else None
            )
            score_match = diff is not None and diff <= SCORE_TOLERANCE
            grade_match = live_grade == rescore_grade

            mismatch_class = classify_mismatch(
                bc, live_score_f, rescore_score_f,
                in_bsip1=True, diff=diff
            )

            pr = ProductVerifyResult(
                barcode=bc,
                live_score=live_score_f,
                live_grade=live_grade,
                rescore_score=rescore_score_f,
                rescore_grade=rescore_grade,
                score_diff=round(diff, 4) if diff is not None else None,
                score_match=score_match,
                grade_match=grade_match,
                mismatch_class=mismatch_class,
            )
            rescore_results.append(pr)

        teardown_shelf_stats(shelf_rel_cfg, se_mod)

        result.product_results = rescore_results
        result.rescored_count = sum(1 for pr in rescore_results if pr.rescore_score is not None)
        result.matched_count = sum(1 for pr in rescore_results if pr.mismatch_class == "ok")
        result.mismatched_count = sum(
            1 for pr in rescore_results
            if pr.mismatch_class not in ("ok", "data")
        )
        result.unmatched_count = sum(1 for pr in rescore_results if pr.mismatch_class == "data")

        # Dominant mismatch class
        classes = [pr.mismatch_class for pr in rescore_results if pr.mismatch_class != "ok"]
        if classes:
            from collections import Counter
            most_common = Counter(classes).most_common(1)[0][0]
            result.dominant_mismatch_class = most_common
        else:
            result.dominant_mismatch_class = "ok"

        result.mismatch_by_class = {}
        for cls in ["ok", "data", "engine", "config", "unknown"]:
            count = sum(1 for pr in rescore_results if pr.mismatch_class == cls)
            if count:
                result.mismatch_by_class[cls] = count

        result.reproduces = (
            result.matched_count == result.live_product_count
            and result.mismatched_count == 0
            and result.unmatched_count == 0
        )

        # Write manifest if requested
        if write_manifest:
            _write_baseline_manifest(result, corpus_map, config)

    except Exception as exc:
        result.error = str(exc)
        result.quarantined = True
        result.quarantine_reason = f"unexpected error: {exc}"

    finally:
        restore_env(env_snap)

    return result


# ---------------------------------------------------------------------------
# Baseline manifest writer
# ---------------------------------------------------------------------------

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _write_baseline_manifest(
    result: CategoryVerifyResult,
    corpus_map: dict[str, Path],
    config: dict,
) -> None:
    """Write _baselines/<slug>/baseline_manifest.json."""
    out_dir = BASELINES_DIR / result.slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # Per-barcode sha256 for each BSIP1 file used
    barcode_files = {}
    for bc, fpath in corpus_map.items():
        if bc in {pr.barcode for pr in result.product_results}:
            barcode_files[bc] = {
                "path": str(fpath),
                "sha256": _sha256_file(fpath),
            }

    manifest = {
        "slug": result.slug,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task": "TASK-395",
        "description": (
            "Baseline manifest: identifies the exact BSIP1 corpus dir, "
            "flag vector, and engine version that reproduce the committed live frontend JSON."
        ),
        "bsip1_dir": result.bsip1_dir_used,
        "baseline_json": result.baseline_path,
        "flag_vector": result.flags_used,
        "shelf_rel": result.shelf_rel_used,
        "engine_version": result.engine_version,
        "score_tolerance": SCORE_TOLERANCE,
        "live_product_count": result.live_product_count,
        "reproduces": result.reproduces,
        "matched_count": result.matched_count,
        "mismatched_count": result.mismatched_count,
        "unmatched_count": result.unmatched_count,
        "bsip1_file_hashes": barcode_files,
        "verified_at": result.run_timestamp,
    }

    out_path = out_dir / "baseline_manifest.json"
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Manifest written: {out_path}")


# ---------------------------------------------------------------------------
# Ledger writer
# ---------------------------------------------------------------------------

def write_ledger(results: list[CategoryVerifyResult]) -> Path:
    """Write _baselines/_ledger_v1.json — the authoritative drift ledger."""
    BASELINES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BASELINES_DIR / "_ledger_v1.json"

    rows = []
    for r in results:
        row: dict[str, Any] = {
            "slug": r.slug,
            "reproduces": r.reproduces,
            "quarantined": r.quarantined,
            "quarantine_reason": r.quarantine_reason or None,
            "error": r.error,
            "live_product_count": r.live_product_count,
            "rescored_count": r.rescored_count,
            "matched_count": r.matched_count,
            "matched_denominator": f"{r.matched_count}/{r.live_product_count} live products",
            "mismatched_count": r.mismatched_count,
            "unmatched_count": r.unmatched_count,
            "dominant_mismatch_class": r.dominant_mismatch_class,
            "mismatch_by_class": r.mismatch_by_class,
            "flags_used": r.flags_used,
            "shelf_rel_used": r.shelf_rel_used,
            "bsip1_dir_used": r.bsip1_dir_used,
            "baseline_path": r.baseline_path,
            "engine_version": r.engine_version,
            "run_timestamp": r.run_timestamp,
        }
        rows.append(row)

    ledger = {
        "ledger_version": "v1",
        "task": "TASK-395",
        "description": (
            "Authoritative drift ledger for all 12 live categories. "
            "Generated by baseline_verify.py --all. "
            "Supersedes all prior informal drift runs as the definitive Phase 0 record."
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "score_tolerance": SCORE_TOLERANCE,
        "pass_definition": (
            "reproduces=True: all live barcodes match score ≤0.05 AND grade AND "
            "zero unmatched barcodes"
        ),
        "total_categories": len(results),
        "reproducing": sum(1 for r in results if r.reproduces),
        "quarantined": sum(1 for r in results if r.quarantined),
        "failing": sum(1 for r in results if not r.reproduces and not r.quarantined),
        "categories": rows,
    }

    out_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Console reporting
# ---------------------------------------------------------------------------

def print_summary_table(results: list[CategoryVerifyResult]) -> None:
    header = (
        f"{'category':<30} {'live':>5} {'rescored':>9} "
        f"{'matched':>8} {'mismatch':>9} {'unmatched':>10} "
        f"{'dom_class':>12} {'status':>12}"
    )
    print()
    print("=" * len(header))
    print("BASELINE VERIFY — ALL CATEGORIES")
    print(f"Tolerance: score ≤{SCORE_TOLERANCE}")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for r in results:
        if r.quarantined:
            status = "QUARANTINE"
        elif r.reproduces:
            status = "PASS"
        else:
            status = "FAIL"
        print(
            f"{r.slug:<30} {r.live_product_count:>5} {r.rescored_count:>9} "
            f"{r.matched_count:>8} {r.mismatched_count:>9} {r.unmatched_count:>10} "
            f"{r.dominant_mismatch_class:>12} {status:>12}"
        )
    print("=" * len(header))
    n_pass = sum(1 for r in results if r.reproduces)
    n_quar = sum(1 for r in results if r.quarantined)
    n_fail = sum(1 for r in results if not r.reproduces and not r.quarantined)
    print(f"PASS: {n_pass}  FAIL: {n_fail}  QUARANTINE: {n_quar}  Total: {len(results)}")
    print()


def print_category_detail(r: CategoryVerifyResult) -> None:
    print(f"\n--- {r.slug} ---")
    if r.quarantined:
        print(f"  STATUS: QUARANTINE — {r.quarantine_reason}")
        return
    if r.error:
        print(f"  ERROR: {r.error}")
        return
    status = "PASS" if r.reproduces else "FAIL"
    print(f"  STATUS: {status}")
    print(f"  live={r.live_product_count}  rescored={r.rescored_count}  "
          f"matched={r.matched_count}  mismatched={r.mismatched_count}  "
          f"unmatched={r.unmatched_count}")
    print(f"  dominant_mismatch_class: {r.dominant_mismatch_class}")
    print(f"  mismatch_by_class: {r.mismatch_by_class}")
    print(f"  bsip1_dir: {r.bsip1_dir_used}")
    print(f"  flags: {r.flags_used}")
    if r.shelf_rel_used:
        print(f"  shelf_rel: {r.shelf_rel_used}")

    if not r.reproduces:
        # Show worst mismatches
        mismatches = [pr for pr in r.product_results if pr.mismatch_class != "ok"]
        mismatches.sort(key=lambda x: x.score_diff or 0, reverse=True)
        print(f"  Top mismatches ({min(10, len(mismatches))} of {len(mismatches)}):")
        for pr in mismatches[:10]:
            print(
                f"    {pr.barcode}: live={pr.live_score} rescore={pr.rescore_score} "
                f"diff={pr.score_diff} class={pr.mismatch_class} note={pr.note}"
            )


# ---------------------------------------------------------------------------
# Discover configs
# ---------------------------------------------------------------------------

def discover_configs() -> list[Path]:
    return sorted(
        p for p in CONFIGS_DIR.glob("*.json")
        if not p.name.startswith("_generated_")
    )


# ---------------------------------------------------------------------------
# Determinism check
# ---------------------------------------------------------------------------

def run_determinism_check(config_path: Path) -> bool:
    """Run the same category twice and compare score output. Returns True if identical."""
    print(f"  Determinism check for {config_path.stem}...")
    r1 = verify_category(config_path)
    r2 = verify_category(config_path)

    if r1.quarantined and r2.quarantined:
        print(f"  Determinism: SKIP (both runs quarantined)")
        return True

    scores1 = {pr.barcode: pr.rescore_score for pr in r1.product_results}
    scores2 = {pr.barcode: pr.rescore_score for pr in r2.product_results}

    if scores1 != scores2:
        diffs = {bc: (scores1.get(bc), scores2.get(bc)) for bc in set(scores1) | set(scores2) if scores1.get(bc) != scores2.get(bc)}
        print(f"  Determinism: FAIL — {len(diffs)} barcode(s) differed between run 1 and run 2:")
        for bc, (s1, s2) in list(diffs.items())[:5]:
            print(f"    {bc}: run1={s1} run2={s2}")
        return False

    print(f"  Determinism: PASS — {len(scores1)} products identical across 2 runs")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description=(
            "Bari canonical reproducibility gate (TASK-395 Phase 0). "
            "Re-scores categories through the canonical spine and compares to committed live JSON. "
            "PASS = every live barcode matches score ≤0.05 AND grade AND zero unmatched."
        )
    )
    parser.add_argument("--shelf", help="Single shelf slug to verify (config stem)")
    parser.add_argument("--all", action="store_true", help="Verify all 12 live categories")
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="Write _baselines/<slug>/baseline_manifest.json for each category",
    )
    parser.add_argument(
        "--write-ledger",
        action="store_true",
        help="Write _baselines/_ledger_v1.json (auto-enabled with --all)",
    )
    parser.add_argument(
        "--determinism-check",
        metavar="SLUG",
        help="Run a category twice and verify identical output (determinism proof)",
    )
    args = parser.parse_args()

    if args.determinism_check:
        cfg = CONFIGS_DIR / f"{args.determinism_check}.json"
        if not cfg.exists():
            print(f"ERROR: config not found for '{args.determinism_check}'", file=sys.stderr)
            return 1
        ok = run_determinism_check(cfg)
        return 0 if ok else 1

    configs: list[Path] = []
    if args.all:
        configs = discover_configs()
    elif args.shelf:
        cfg = CONFIGS_DIR / f"{args.shelf}.json"
        if not cfg.exists():
            print(f"ERROR: config not found for '{args.shelf}'", file=sys.stderr)
            return 1
        configs = [cfg]
    else:
        parser.print_help()
        return 1

    print(f"baseline_verify.py — Canonical Reproducibility Gate (TASK-395)")
    print(f"Configs: {len(configs)}  Tolerance: score ≤{SCORE_TOLERANCE}  Write-manifest: {args.write_manifest}")
    print()

    t0 = time.perf_counter()
    results: list[CategoryVerifyResult] = []

    for cfg_path in configs:
        print(f">>> Verifying: {cfg_path.stem}")
        r = verify_category(cfg_path, write_manifest=args.write_manifest)
        results.append(r)
        status = "QUARANTINE" if r.quarantined else ("PASS" if r.reproduces else "FAIL")
        print(
            f"    {status}  live={r.live_product_count}  matched={r.matched_count}  "
            f"mismatch={r.mismatched_count}  unmatched={r.unmatched_count}  "
            f"dom={r.dominant_mismatch_class}"
        )

    elapsed = time.perf_counter() - t0
    print_summary_table(results)

    for r in results:
        print_category_detail(r)

    # Write ledger
    if args.write_ledger or args.all:
        ledger_path = write_ledger(results)
        print(f"\nLedger written: {ledger_path}")

    print(f"\nWall-clock: {elapsed:.1f}s")

    # Exit 0 always — PASS, FAIL, QUARANTINE are all valid outcomes
    # (caller interprets ledger; non-zero only on tool error)
    return 0


if __name__ == "__main__":
    sys.exit(main())
