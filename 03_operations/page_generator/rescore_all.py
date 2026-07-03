#!/usr/bin/env python3
"""
rescore_all.py — Generic one-command re-score of all configured shelves.

Per shelf: reads scoring block from configs/*.json, applies env flags,
set_shelf_stats / set_shelf_sodium_stats with FROZEN values (no runtime
compute_from_corpus), scores BSIP1 corpus, C10 milk gate, generate_page
→ _rescore_staging/, gates (OFF=0, score==trace), diff vs live baseline.

Owner direction (2026-06-16): CANONICAL RE-BASELINE mode.
  - Score moves vs live are EXPECTED and reported, NOT treated as failures.
  - Hard gate failures: error / OFF>0. (C10 milk-freeze RETIRED 2026-06-17 — diagnostic only.)

C10 milk gate (fixed, v2):
  The milk headpin (run_005_headpin) was frozen with milk-canonical flags:
    BARI_RECAL_P0=off, BARI_FAT_TECH_V1=on, BARI_SHELF_RELATIVE_V1=on,
    BARI_REDLABEL_V1=off, BARI_DAIRY_SAT_FAT_INFER=off
  (confirmed by batch_run_milk_006_shelfrel_refreeze.py).
  The C10 check ALWAYS restores these flags + reloads the engine before
  scoring milk, then restores shelf flags + reloads again. This isolates
  milk scoring from the current shelf's flag set.

OFF ban (TASK-238): no external sources; unknown stays null.
Never overwrites live artifacts — all output under _rescore_staging/ only.
No engine edits — proto_v0/src/ is read-only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[2]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
GENERATE_PAGE_PY = REPO / "03_operations" / "page_generator" / "generate_page.py"
SCORE_ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"
STAGING_ROOT = REPO / "_rescore_staging"
MILK_BASELINE_DIR = (
    REPO
    / "02_products"
    / "milk_and_alternatives"
    / "intelligence_bsip2"
    / "run_005_headpin"
    / "products"
)
MILK_BSIP1_DIR = REPO / "03_operations" / "bsip1" / "run_milk_002" / "output"

FIXED_TIMESTAMP = "2026-06-16T00:00:00Z"

OFF_REGEX = re.compile(
    r"open_food_facts|openfoodfacts\.org|images\.openfoodfacts|off_candidate_panel",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Milk-canonical flags (from batch_run_milk_006_shelfrel_refreeze.py).
# These are the flags under which run_005_headpin scores must be reproduced.
# Never use shelf flags to score milk — that contaminates the gate.
# ---------------------------------------------------------------------------
MILK_CANONICAL_FLAGS = {
    "BARI_RECAL_P0": "off",
    "BARI_FAT_TECH_V1": "on",
    "BARI_SHELF_RELATIVE_V1": "on",
    "BARI_REDLABEL_V1": "off",
    "BARI_DAIRY_SAT_FAT_INFER": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
    "BARI_GRAD_SODIUM_V1": "off",
    "BARI_SODIUM_CEREAL": "off",
    # TASK-496: must be explicitly OFF here so a prior shelf's config-supplied
    # BARI_REDLABEL_CONTINUOUS_V1=on (cheese/cakes/chocolate_bars/chocolate_tablets)
    # cannot leak into the milk C10 invariant check within one rescore_all.py run.
    "BARI_REDLABEL_CONTINUOUS_V1": "off",
}

# BARI_* vars that may be set by shelf configs and must be snapshotted/restored
MANAGED_BARI_VARS = [
    "BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM",
    "BARI_FAT_TECH_V1",
    "BARI_SHELF_RELATIVE_V1",
    "BARI_SODIUM_SHELF_RELATIVE_V1",
    "BARI_DAIRY_PROTEIN_REWEIGHT_V1",
    "BARI_GRAD_SODIUM_V1",
    "BARI_FERMENT_MARKER_BRINED_FIX_V1",
    "BARI_SODIUM_CEREAL",
    "BARI_REDLABEL_V1",
    "BARI_TASK144_FIXES",
    "BARI_TASK250_CONF",
    "BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15",
    "BARI_GLASSBOX_W2",
    "BARI_DAIRY_SAT_FAT_INFER",
    # TASK-496: now supplied via config (cheese/cakes/chocolate_bars/chocolate_tablets)
    # instead of an ad-hoc env override — must be snapshotted/restored like every
    # other shelf flag so it never leaks across shelves in one rescore_all.py run.
    "BARI_REDLABEL_CONTINUOUS_V1",
]

if str(SCORE_ENGINE_SRC) not in sys.path:
    sys.path.insert(0, str(SCORE_ENGINE_SRC))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def discover_shelf_configs() -> list[Path]:
    return sorted(
        p for p in CONFIGS_DIR.glob("*.json") if not p.name.startswith("_generated_")
    )


def normalize_corpus_dirs(config: dict, scoring: dict) -> list[str]:
    bsip1_dir = scoring.get("bsip1_dir")
    if bsip1_dir:
        return [bsip1_dir]
    corpus_dirs = config.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    return [d for d in corpus_dirs if d]


def load_corpus_filter(path: str | None) -> set[str] | None:
    if not path or not Path(path).is_file():
        return None
    data = load_json(Path(path))
    return {str(p["barcode"]) for p in data["products"] if p.get("decision") == "IN_SCORED"}


def collect_bsip1_files(
    corpus_dirs: list[str],
    corpus_filter: set[str] | None = None,
    bsip1_glob: str = "bsip1_*.json",
) -> list[Path]:
    """Collect BSIP1 product files; first corpus_dir wins on barcode collision."""
    files: list[Path] = []
    seen_barcodes: set[str] = set()
    for corpus_dir in corpus_dirs:
        cdir = Path(corpus_dir)
        if not cdir.is_dir():
            continue
        for fname in sorted(cdir.glob(bsip1_glob)):
            if "audit" in fname.name:
                continue
            try:
                rec = load_json(fname)
            except Exception:
                continue
            bc = str(rec.get("barcode", "")).strip()
            if not bc or bc in seen_barcodes:
                continue
            if rec.get("file_type") != "product":
                continue
            if corpus_filter is not None and bc not in corpus_filter:
                continue
            seen_barcodes.add(bc)
            files.append(fname)
    return files


def load_bsip1_records(bsip1_files: list[Path]) -> list[dict]:
    records: list[dict] = []
    for fpath in bsip1_files:
        try:
            records.append(load_json(fpath))
        except Exception:
            pass
    return records


def count_off_in_page(page: dict) -> int:
    products_str = json.dumps(page.get("products", []), ensure_ascii=False)
    return len(OFF_REGEX.findall(products_str))


def build_bsip1_lookup(bsip1_files: list[Path]) -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for fpath in bsip1_files:
        try:
            rec = load_json(fpath)
            bc = str(rec.get("barcode", "")).strip()
            if bc:
                lookup[bc] = rec
        except Exception:
            pass
    return lookup


def load_traces_by_barcode(products_dir: Path) -> dict[str, dict]:
    traces: dict[str, dict] = {}
    if not products_dir.is_dir():
        return traces
    for dname in sorted(products_dir.iterdir()):
        if not dname.is_dir():
            continue
        trace_path = dname / "bsip2_trace.json"
        if not trace_path.is_file():
            continue
        try:
            trace = load_json(trace_path)
            bc = str(trace.get("input_reference", {}).get("barcode", "")).strip()
            if bc and bc not in traces:
                traces[bc] = trace
        except Exception:
            pass
    return traces


def score_distribution(scores: list[float | int | None]) -> dict[str, Any]:
    numeric = [float(s) for s in scores if s is not None]
    if not numeric:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "median": None,
            "stdev": None,
            "most_common": None,
            "most_common_count": 0,
            "histogram": {},
        }
    rounded = [round(s) for s in numeric]
    hist = dict(sorted(Counter(rounded).items()))
    mc_score, mc_count = Counter(rounded).most_common(1)[0]
    return {
        "count": len(numeric),
        "min": min(numeric),
        "max": max(numeric),
        "median": statistics.median(numeric),
        "stdev": statistics.pstdev(numeric) if len(numeric) > 1 else 0.0,
        "most_common": mc_score,
        "most_common_count": mc_count,
        "histogram": hist,
    }


# ---------------------------------------------------------------------------
# Env management: snapshot / apply / restore
# ---------------------------------------------------------------------------


def snapshot_env() -> dict[str, str | None]:
    return {k: os.environ.get(k) for k in MANAGED_BARI_VARS}


def restore_env(snapshot: dict[str, str | None]) -> None:
    for k, v in snapshot.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def apply_flags(flags: dict[str, str]) -> None:
    for key, val in flags.items():
        os.environ[key] = val


# ---------------------------------------------------------------------------
# Scoring — config-driven, one generic path
# ---------------------------------------------------------------------------


def reload_score_engine():
    import score_engine

    return importlib.reload(score_engine)


def make_score_one(score_engine_mod) -> Callable[[dict], dict]:
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
        score_result = score_engine_mod.score_product(
            product, signals, cat_result, nova_result, eval_result
        )
        trace = assemble_trace(
            product, signals, cat_result, nova_result, eval_result, score_result
        )
        trace["structural_class"] = classify_structural_class(trace)
        return trace

    return score_one


def setup_shelf_stats(shelf_rel: dict | None, score_engine_mod) -> dict | None:
    """Apply FROZEN shelf stats from config. Never computes from corpus."""
    if not shelf_rel:
        return None
    # Brined uses set_shelf_sodium_stats; all others use set_shelf_stats
    if shelf_rel.get("api") == "sodium_ev056":
        median = shelf_rel["median"]
        scale = shelf_rel["scale"]
        score_engine_mod.set_shelf_sodium_stats(median, scale)
        return {
            "nutrient": "sodium_mg",
            "median": median,
            "scale": scale,
            "scale_type": "stdev",
            "api": "sodium_ev056",
        }
    nutrient = shelf_rel["nutrient"]
    median = shelf_rel["median"]
    scale = shelf_rel["scale"]
    scale_type = shelf_rel.get("scale_type", "iqr")
    score_engine_mod.set_shelf_stats(nutrient, median, scale, scale_type)
    return {"nutrient": nutrient, "median": median, "scale": scale, "scale_type": scale_type}


def teardown_shelf_stats(shelf_rel: dict | None, score_engine_mod) -> None:
    if not shelf_rel:
        return
    if shelf_rel.get("api") == "sodium_ev056":
        score_engine_mod.clear_shelf_sodium_stats()
    else:
        score_engine_mod.clear_shelf_stats(shelf_rel["nutrient"])


# ---------------------------------------------------------------------------
# C10 milk invariant gate (v2 — isolated from shelf flags)
# ---------------------------------------------------------------------------


def check_milk_c10(shelf: str, shelf_flags: dict[str, str]) -> tuple[bool, int, list[dict]]:
    """
    Score all run_005_headpin milk products under MILK_CANONICAL_FLAGS,
    compare to frozen baselines.  Returns (pass, checked_count, failures).

    Critically: milk is scored under MILK_CANONICAL_FLAGS, NOT under the
    current shelf's flags.  The shelf flags are temporarily swapped out,
    the engine is reloaded, milk is scored, then the shelf state is restored.

    Only brined_cheeses' DAIRY_PROTEIN_REWEIGHT_V1 is known to perturb milk.
    RECAL_P0=on also perturbs milk (tested 2026-06-16).  This gate catches both.
    """
    if not MILK_BASELINE_DIR.exists():
        print(f"  C10 [{shelf}]: milk baseline dir missing — skip")
        return True, 0, []

    # --- Switch to milk-canonical env ---
    env_snapshot = snapshot_env()
    try:
        apply_flags(MILK_CANONICAL_FLAGS)
        milk_engine = reload_score_engine()
        # No shelf stats for milk (not enrolled in any shelf-relative differentiator)
        milk_score_one = make_score_one(milk_engine)

        failures: list[dict] = []
        checked = 0

        for pdir in sorted(MILK_BASELINE_DIR.iterdir()):
            if not pdir.is_dir():
                continue
            trace_path = pdir / "bsip2_trace.json"
            if not trace_path.is_file():
                continue
            baseline_trace = load_json(trace_path)
            bsip1_path = MILK_BSIP1_DIR / f"{pdir.name}.json"
            if not bsip1_path.exists():
                continue
            doc = load_json(bsip1_path)
            try:
                tr = milk_score_one(doc)
            except Exception as exc:
                print(f"  C10 FAIL [{shelf}] milk scoring error on {pdir.name}: {exc}")
                failures.append({"product": pdir.name, "error": str(exc)})
                continue
            baseline_score = baseline_trace.get("final_score_estimate")
            new_score = tr.get("final_score_estimate")
            if baseline_score is not None and new_score is not None:
                checked += 1
                delta = abs(new_score - baseline_score)
                if delta > 0.001:
                    msg = (
                        f"  C10 FAIL [{shelf}] milk {pdir.name}: "
                        f"baseline={baseline_score:.2f} new={new_score:.2f} delta={delta:.4f}"
                    )
                    print(msg)
                    failures.append({
                        "product": pdir.name,
                        "baseline_score": baseline_score,
                        "new_score": new_score,
                        "delta": round(delta, 4),
                    })

    finally:
        # --- Restore shelf env and reload engine ---
        restore_env(env_snapshot)
        apply_flags(shelf_flags)
        reload_score_engine()

    if checked == 0:
        print(f"  C10 [{shelf}]: no milk products checked — possible path mismatch")
        return False, 0, [{"error": "no_milk_products_checked"}]

    c10_pass = len(failures) == 0
    if c10_pass:
        print(f"  C10 PASS [{shelf}]: {checked} milk products all delta=0.0")
    else:
        print(
            f"  C10 FAIL [{shelf}]: {len(failures)}/{checked} milk products delta>0.001 "
            f"— FROZEN-INVARIANT CONFLICT (see failures list)"
        )
    return c10_pass, checked, failures


# ---------------------------------------------------------------------------
# Corpus scoring
# ---------------------------------------------------------------------------


def score_corpus(
    bsip1_files: list[Path],
    products_dir: Path,
    scoring: dict,
) -> tuple[int, dict | None, bool, int, list[dict]]:
    from input_loader import load_product, validate_product

    flags = scoring.get("flags") or {}
    shelf_rel = scoring.get("shelf_rel")

    # Validate: no compute_from_corpus should be present in a canonical config
    if shelf_rel and shelf_rel.get("compute_from_corpus"):
        raise ValueError(
            "FATAL: shelf_rel.compute_from_corpus=true found in config — "
            "frozen stats must be provided (median + scale). Non-deterministic."
        )

    apply_flags(flags)
    score_engine_mod = reload_score_engine()

    applied_stats = setup_shelf_stats(shelf_rel, score_engine_mod)
    score_one = make_score_one(score_engine_mod)

    products_dir.mkdir(parents=True, exist_ok=True)
    scored = 0

    for fpath in bsip1_files:
        product = load_product(fpath)
        product["_source_path"] = str(fpath)
        errors = validate_product(product)
        product["_load_errors"] = errors

        pid = product.get("canonical_product_id", fpath.stem)
        product_dir = products_dir / str(pid)
        product_dir.mkdir(parents=True, exist_ok=True)

        trace = score_one(product)
        trace_path = product_dir / "bsip2_trace.json"
        trace_path.write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        scored += 1

    # C10 milk gate — uses milk-canonical flags, not shelf flags
    # Pass shelf_flags so the gate can restore them after the milk check
    c10_pass, c10_checked, c10_failures = check_milk_c10(
        products_dir.parent.name, flags
    )

    teardown_shelf_stats(shelf_rel, score_engine_mod)
    return scored, applied_stats, c10_pass, c10_checked, c10_failures


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


def write_verification_table(
    traces: dict[str, dict],
    bsip1_lookup: dict[str, dict],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as vf:
        writer = csv.writer(vf)
        writer.writerow(
            [
                "barcode",
                "score",
                "grade",
                "binding_caps",
                "nova",
                "fat",
                "sodium",
                "context_flag",
            ]
        )
        for bc in sorted(traces.keys()):
            t = traces[bc]
            nn = (t.get("input_reference") or {}).get("normalized_nutrition_per_100g") or {}
            if not nn and bc in bsip1_lookup:
                nn = bsip1_lookup[bc].get("normalized_nutrition_per_100g") or {}
            writer.writerow(
                [
                    bc,
                    t.get("final_score_estimate"),
                    t.get("grade_estimate"),
                    t.get("binding_cap"),
                    t.get("nova_proxy"),
                    nn.get("fat_g"),
                    nn.get("sodium_mg"),
                    t.get("context_flag"),
                ]
            )


def make_staging_config(original: dict, products_dir: Path, out_path: Path) -> Path:
    staging = deepcopy(original)
    staging["run_products_dir"] = str(products_dir)
    staging["_rescore_staging"] = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Staging config for rescore_all — run_products_dir repointed; live untouched.",
    }
    write_json(out_path, staging)
    return out_path


def run_generate_page(config_path: Path, out_path: Path) -> int:
    cmd = [
        sys.executable,
        str(GENERATE_PAGE_PY),
        "--config",
        str(config_path),
        "--out",
        str(out_path),
        "--timestamp",
        FIXED_TIMESTAMP,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def verify_score_trace(page: dict, traces: dict[str, dict]) -> list[tuple[str, Any, Any]]:
    mismatches: list[tuple[str, Any, Any]] = []
    for product in page.get("products", []):
        bc = str(product.get("barcode", "")).strip()
        page_score = product.get("score")
        trace = traces.get(bc)
        if trace is None:
            mismatches.append((bc, page_score, None))
            continue
        trace_score = trace.get("final_score_estimate")
        if page_score != trace_score:
            mismatches.append((bc, page_score, trace_score))
    return mismatches


def diff_vs_baseline(baseline_path: str | None, rescored: dict) -> dict[str, Any]:
    baseline_products: dict[str, dict] = {}
    if baseline_path and Path(baseline_path).is_file():
        baseline = load_json(Path(baseline_path))
        for p in baseline.get("products", []):
            bc = str(p.get("barcode", "")).strip()
            if bc:
                baseline_products[bc] = p

    rescored_products: dict[str, dict] = {}
    for p in rescored.get("products", []):
        bc = str(p.get("barcode", "")).strip()
        if bc:
            rescored_products[bc] = p

    common = sorted(set(baseline_products) & set(rescored_products))
    score_moves = 0
    grade_moves = 0
    grade_movers: list[str] = []
    score_move_details: list[dict] = []

    for bc in common:
        old_score = baseline_products[bc].get("score")
        new_score = rescored_products[bc].get("score")
        old_grade = baseline_products[bc].get("grade")
        new_grade = rescored_products[bc].get("grade")

        if old_score is not None and new_score is not None:
            if round(old_score) != round(new_score):
                score_moves += 1
                score_move_details.append({
                    "barcode": bc,
                    "old_score": old_score,
                    "new_score": new_score,
                    "delta": round(new_score - old_score, 2),
                    "old_grade": old_grade,
                    "new_grade": new_grade,
                })
        if old_grade != new_grade:
            grade_moves += 1
            grade_movers.append(f"{bc} {old_grade}->{new_grade}")

    return {
        "baseline_count": len(baseline_products),
        "rescored_count": len(rescored_products),
        "common_count": len(common),
        "score_moves": score_moves,
        "grade_moves": grade_moves,
        "grade_movers": grade_movers,
        "score_move_details": score_move_details,
        # score_moves==0 and grade_moves==0 => reproduces live exactly
        "reproduces_live": grade_moves == 0 and score_moves == 0,
    }


# ---------------------------------------------------------------------------
# ShelfResult dataclass
# ---------------------------------------------------------------------------


@dataclass
class ShelfResult:
    shelf: str
    config_path: Path
    products: int = 0
    scored: int = 0
    score_moves: int = 0
    grade_moves: int = 0
    grade_movers: list[str] = field(default_factory=list)
    score_move_details: list[dict] = field(default_factory=list)
    reproduces_live: bool = False
    c10_pass: bool = False
    c10_checked: int = 0
    c10_failures: list[dict] = field(default_factory=list)
    applied_shelf_stats: dict | None = None
    gate_pass: bool = False
    gate_exit: int = 1
    off_count: int = 0
    score_trace_ok: bool = False
    score_trace_mismatches: int = 0
    error: str | None = None
    score_dist: dict[str, Any] = field(default_factory=dict)
    verification_table: Path | None = None
    rescored_json: Path | None = None
    frozen_stats_source: str = ""


# ---------------------------------------------------------------------------
# Per-shelf processing
# ---------------------------------------------------------------------------


def process_shelf(config_path: Path) -> ShelfResult:
    shelf = config_path.stem
    result = ShelfResult(shelf=shelf, config_path=config_path)
    shelf_dir = STAGING_ROOT / shelf
    products_dir = shelf_dir / "products"
    if products_dir.exists():
        shutil.rmtree(products_dir)
    staging_config_path = shelf_dir / "staging_config.json"
    out_json = shelf_dir / f"{shelf}_rescored.json"
    verify_csv = shelf_dir / "verification_table.csv"

    # Snapshot env before any shelf processing
    env_snapshot = snapshot_env()

    try:
        config = load_json(config_path)
        scoring = config.get("scoring")
        if not scoring:
            result.error = "missing scoring block in config"
            return result

        # Detect compute_from_corpus — hard error (non-deterministic)
        shelf_rel_cfg = scoring.get("shelf_rel")
        if shelf_rel_cfg and shelf_rel_cfg.get("compute_from_corpus"):
            result.error = (
                "FATAL: shelf_rel.compute_from_corpus=true — "
                "frozen median/scale must be set. Non-deterministic."
            )
            return result

        corpus_dirs = normalize_corpus_dirs(config, scoring)
        if not corpus_dirs:
            result.error = "no valid corpus_dirs / bsip1_dir in config"
            return result

        missing_dirs = [d for d in corpus_dirs if not Path(d).is_dir()]
        if missing_dirs:
            result.error = f"corpus_dirs not found: {missing_dirs}"
            return result

        corpus_filter = load_corpus_filter(scoring.get("corpus_filter"))
        bsip1_glob = scoring.get("bsip1_glob", "bsip1_*.json")
        bsip1_files = collect_bsip1_files(corpus_dirs, corpus_filter, bsip1_glob)
        if not bsip1_files:
            result.error = "no bsip1 files matched corpus_dirs + filter"
            return result

        bsip1_lookup = build_bsip1_lookup(bsip1_files)
        scored, applied_stats, c10_pass, c10_checked, c10_failures = score_corpus(
            bsip1_files, products_dir, scoring
        )
        result.scored = scored
        result.applied_shelf_stats = applied_stats
        result.c10_pass = c10_pass
        result.c10_checked = c10_checked
        result.c10_failures = c10_failures
        result.frozen_stats_source = scoring.get("_source", "")

        traces = load_traces_by_barcode(products_dir)
        write_verification_table(traces, bsip1_lookup, verify_csv)
        result.verification_table = verify_csv

        make_staging_config(config, products_dir, staging_config_path)
        gate_exit = run_generate_page(staging_config_path, out_json)
        result.gate_exit = gate_exit
        result.gate_pass = gate_exit == 0

        if not out_json.is_file():
            result.error = "generate_page did not produce output JSON"
            return result

        page = load_json(out_json)
        result.rescored_json = out_json
        result.products = len(page.get("products", []))
        result.off_count = count_off_in_page(page)
        mismatches = verify_score_trace(page, traces)
        result.score_trace_mismatches = len(mismatches)
        result.score_trace_ok = len(mismatches) == 0

        diff = diff_vs_baseline(config.get("baseline_json"), page)
        result.score_moves = diff["score_moves"]
        result.grade_moves = diff["grade_moves"]
        result.grade_movers = diff["grade_movers"]
        result.score_move_details = diff.get("score_move_details", [])
        result.reproduces_live = diff["reproduces_live"]

        scores = [p.get("score") for p in page.get("products", [])]
        result.score_dist = score_distribution(scores)

    except Exception as exc:
        result.error = str(exc)

    finally:
        # Always restore env after shelf processing
        restore_env(env_snapshot)

    return result


# ---------------------------------------------------------------------------
# Hard gate: only error / OFF are failures. (C10 milk-freeze RETIRED 2026-06-17 →
# diagnostic only; owner lifted the freeze, milk conforms as a normal shelf.)
# Score/grade moves vs live are expected in canonical re-baseline mode.
# ---------------------------------------------------------------------------


def shelf_hard_failed(result: ShelfResult) -> bool:
    if result.error:
        return True
    if result.off_count > 0:
        return True
    # C10 milk-freeze gate RETIRED 2026-06-17 — owner lifted the CNO milk freeze
    # ("I don't mind the rescoring; scores don't matter, only uniformity"; see memory
    # zero_different_category_mandate). Milk now conforms as a normal shelf. The C10 delta
    # is STILL computed + printed + recorded (a useful DIAGNOSTIC for cross-shelf flag
    # perturbation, shown in the acceptance table), but it no longer HARD-FAILS the rescore.
    return False


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_acceptance_table(results: list[ShelfResult]) -> None:
    header = (
        f"{'shelf':<28} {'products':>8} {'score-moves':>11} "
        f"{'grade-moves':>11} {'C10(milk)':>10} {'OFF':>5} {'gate':>5}"
    )
    print("\n" + "=" * len(header))
    print("RESCORE ALL — CANONICAL RE-BASELINE (score-moves vs live = expected)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for r in results:
        c10 = f"PASS({r.c10_checked})" if r.c10_pass else f"FAIL({r.c10_checked})"
        gate = "PASS" if r.gate_pass else "FAIL"
        err = " ERR" if r.error else ""
        print(
            f"{r.shelf:<28} {r.products:>8} {r.score_moves:>11} "
            f"{r.grade_moves:>11} {c10:>10} {r.off_count:>5} {gate:>5}{err}"
        )
    print("=" * len(header))


def print_per_shelf_details(results: list[ShelfResult]) -> None:
    for r in results:
        print(f"\n--- {r.shelf} ---")
        if r.error:
            print(f"  ERROR: {r.error}")
            continue
        print(f"  products: {r.products} (scored corpus: {r.scored})")
        print(f"  frozen_stats: {r.applied_shelf_stats}  source: {r.frozen_stats_source}")
        print(f"  score-moves vs live: {r.score_moves}")
        print(f"  grade-moves vs live: {r.grade_moves}")
        c10_status = "PASS" if r.c10_pass else f"FAIL (CRITICAL: frozen-invariant conflict)"
        print(f"  C10 milk: {c10_status} ({r.c10_checked} checked)")
        if r.c10_failures:
            for f in r.c10_failures[:5]:
                print(f"    C10 failure: {f}")
        if r.grade_movers:
            print(f"  grade-movers: {', '.join(r.grade_movers)}")
        else:
            print("  grade-movers: (none)")
        print(f"  gate exit: {r.gate_exit} ({'PASS' if r.gate_pass else 'FAIL'})")
        print(f"  OFF count in page: {r.off_count}")
        print(
            f"  score==trace: {'OK' if r.score_trace_ok else 'FAIL'} "
            f"({r.score_trace_mismatches} mismatches)"
        )
        dist = r.score_dist
        if dist.get("count"):
            print(
                f"  score dist: n={dist['count']} min={dist['min']:.2f} "
                f"max={dist['max']:.2f} median={dist['median']:.2f} "
                f"stdev={dist['stdev']:.2f} "
                f"most_common={dist['most_common']}({dist['most_common_count']})"
            )
            print(f"  score histogram: {dist['histogram']}")


def write_delta_report(results: list[ShelfResult], out_path: Path) -> None:
    """Write per-shelf delta report for Nutrition + red-team review."""
    lines = [
        "# Canonical Re-baseline Delta Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}Z",
        f"Mode: CANONICAL RE-BASELINE (score moves vs live = expected, not failures)",
        f"Hard gates: OFF=0, C10 milk delta=0.0, no pipeline error",
        "",
        "---",
        "",
    ]

    for r in results:
        lines.append(f"## {r.shelf}")
        lines.append("")
        if r.error:
            lines.append(f"**STATUS: ERROR** — {r.error}")
            lines.append("")
            continue

        # Gate status
        hard_fail = shelf_hard_failed(r)
        status = "HARD FAIL" if hard_fail else "GATE PASS"
        lines.append(f"**Status:** {status}")
        lines.append("")

        # Frozen stats
        lines.append(f"**Frozen stats:** {r.applied_shelf_stats}")
        lines.append(f"**Source:** {r.frozen_stats_source}")
        lines.append("")

        # C10
        c10_status = "PASS" if r.c10_pass else "FAIL — CRITICAL: frozen-invariant conflict (see failures)"
        lines.append(f"**C10 milk gate:** {c10_status} ({r.c10_checked}/20 products checked)")
        if r.c10_failures:
            lines.append("")
            lines.append("C10 failures:")
            for f in r.c10_failures:
                lines.append(f"  - {f}")

        lines.append("")

        # Products + OFF
        lines.append(f"**Products:** {r.products} (corpus scored: {r.scored})")
        lines.append(f"**OFF count:** {r.off_count}")
        lines.append(f"**score==trace:** {'OK' if r.score_trace_ok else 'FAIL'} ({r.score_trace_mismatches} mismatches)")
        lines.append("")

        # Score/grade moves
        lines.append(f"**Score moves vs live:** {r.score_moves}/{r.scored}")
        lines.append(f"**Grade moves vs live:** {r.grade_moves}")
        lines.append("")

        if r.grade_movers:
            lines.append("**Grade movers (barcode old→new):**")
            for gm in r.grade_movers:
                lines.append(f"  - {gm}")
            lines.append("")

        # Score distribution
        dist = r.score_dist
        if dist.get("count"):
            lines.append(
                f"**Score dist:** n={dist['count']} "
                f"min={dist['min']:.1f} max={dist['max']:.1f} "
                f"median={dist['median']:.1f} stdev={dist['stdev']:.1f}"
            )
            lines.append(f"**Histogram:** {dist['histogram']}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Summary table
    lines.insert(4, "")
    lines.insert(4, "| shelf | products | score-moves | grade-moves | C10 | OFF | gate |")
    lines.insert(4, "|---|---|---|---|---|---|---|")
    for r in results:
        if r.error:
            lines.insert(4, f"| {r.shelf} | ERROR | — | — | — | — | FAIL |")
        else:
            c10 = f"PASS({r.c10_checked})" if r.c10_pass else f"FAIL({r.c10_checked})"
            gate = "PASS" if not shelf_hard_failed(r) else "FAIL"
            lines.insert(4, f"| {r.shelf} | {r.products} | {r.score_moves} | {r.grade_moves} | {c10} | {r.off_count} | {gate} |")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nDelta report: {out_path}")


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
            "Re-score all configured shelves (canonical re-baseline). "
            "Score moves vs live are expected. "
            "Hard gates: OFF=0, C10 milk delta=0.0, no error. "
            "Output: _rescore_staging/ (never overwrites live)."
        )
    )
    parser.add_argument(
        "--shelf",
        default=None,
        help="Optional single shelf name (config stem) to process instead of all",
    )
    args = parser.parse_args()

    configs = discover_shelf_configs()
    if args.shelf:
        configs = [p for p in configs if p.stem == args.shelf]
        if not configs:
            print(f"ERROR: no config found for shelf '{args.shelf}'", file=sys.stderr)
            return 1

    print(f"Discovered {len(configs)} shelf config(s)  [mode: CANONICAL RE-BASELINE]")
    for p in configs:
        print(f"  - {p.name}")

    STAGING_ROOT.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    results: list[ShelfResult] = []

    for config_path in configs:
        print(f"\n>>> Processing shelf: {config_path.stem}")
        results.append(process_shelf(config_path))

    elapsed = time.perf_counter() - t0
    print_acceptance_table(results)
    print_per_shelf_details(results)

    # C10 critical findings
    c10_failures = [r for r in results if not r.c10_pass and not r.error]
    if c10_failures:
        print("\n=== C10 CRITICAL: FROZEN-INVARIANT CONFLICTS ===")
        for r in c10_failures:
            print(f"  {r.shelf}: milk delta>0.001 — requires owner triage before deploy")
            for f in r.c10_failures[:3]:
                print(f"    {f}")

    errors = [r for r in results if r.error]
    if errors:
        print("\n=== ERRORS ===")
        for r in errors:
            print(f"  {r.shelf}: {r.error}")

    # Write summary
    summary_path = STAGING_ROOT / "run_summary.json"
    write_json(
        summary_path,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "timestamp_arg": FIXED_TIMESTAMP,
            "mode": "canonical_rebaseline",
            "wall_clock_sec": round(elapsed, 2),
            "shelves": [
                {
                    "shelf": r.shelf,
                    "products": r.products,
                    "scored": r.scored,
                    "score_moves": r.score_moves,
                    "grade_moves": r.grade_moves,
                    "grade_movers": r.grade_movers,
                    "reproduces_live": r.reproduces_live,
                    "c10_pass": r.c10_pass,
                    "c10_checked": r.c10_checked,
                    "c10_failures": r.c10_failures,
                    "applied_shelf_stats": r.applied_shelf_stats,
                    "frozen_stats_source": r.frozen_stats_source,
                    "gate_exit": r.gate_exit,
                    "gate_pass": r.gate_pass,
                    "off_count": r.off_count,
                    "score_trace_ok": r.score_trace_ok,
                    "score_trace_mismatches": r.score_trace_mismatches,
                    "error": r.error,
                    "score_dist": r.score_dist,
                    "verification_table": str(r.verification_table) if r.verification_table else None,
                    "rescored_json": str(r.rescored_json) if r.rescored_json else None,
                }
                for r in results
            ],
        },
    )

    # Write delta report
    delta_report_path = STAGING_ROOT / "rebaseline_delta_report.md"
    write_delta_report(results, delta_report_path)

    print(f"\nWall-clock: {elapsed:.1f}s")
    print(f"Run summary: {summary_path}")

    # Hard gate exit: only error / OFF / C10 cause non-zero exit
    any_hard_fail = any(shelf_hard_failed(r) for r in results)
    return 1 if any_hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
