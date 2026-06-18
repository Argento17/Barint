#!/usr/bin/env python3
"""
spine_pipeline.py — Spine step 5: DAG runner + lineage integration (TASK-320 / P170).

Thin orchestration layer that routes spine_flip's per-shelf chain
(rescore -> copy -> gate) THROUGH the Spine DAG runner so re-runs are:
  - content-hashed and SKIPPED when inputs are unchanged (incremental)
  - self-recording: lineage in spine.db automatically

Imported and called by spine_flip.py when --via-spine is passed.

Per affected shelf (after the frozen gate passes), declares 3 Stage objects:

  rescore_<shelf>
      inputs  = 9 engine source files + shelf config + corpus manifest
      outputs = _rescore_staging/<shelf>/<shelf>_rescored.json
      fn      = python rescore_all.py --shelf <shelf>  (with flag env)

  copy_<shelf>
      inputs  = rescored page + config baseline_json
      outputs = rescored page (in-place rewrite) + author_set.json
      fn      = python copy_stage.py --staging ... --live ... --shelf ...

  gate_<shelf>
      inputs  = rescored page (post-copy)
      outputs = <shelf>_rescored_gates_report.md
      fn      = python run_gates.py <page> --config ... --baseline ... [--schema ...]
                                           [--corpus ...] [--run ...]

After run_pipeline() returns the {stage_name: 'ran'|'skipped'} dict,
run_via_spine() rebuilds exactly the same per_shelf / per_shelf_authors
list that spine_flip's main() loop produces (by reading the files that
the stages wrote) so the caller can assemble the report unchanged.

CONSTRAINTS (TASK-320 / P170 non-negotiables):
  - Uses the EXISTING runner + spine_db; no duplicate hashing/lineage logic.
  - NO engine / score / page / bari-web edits.
  - spine.db is gitignored generated state; never committed.
  - NO push / NO deploy.
  - OFF-ban absolute (TASK-238).
  - The frozen gate (from spine_flip step 4) still hard-stops BEFORE any
    pipeline runs: frozen breach -> caller exits 2, run_via_spine is never
    reached.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[2]
PAGE_GEN = REPO / "03_operations" / "page_generator"
CONFIGS_DIR = PAGE_GEN / "configs"
STAGING_ROOT = REPO / "_rescore_staging"
SPINE_DIR = REPO / "03_operations" / "spine"

RESCORE_PY = PAGE_GEN / "rescore_all.py"
COPY_PY = PAGE_GEN / "copy_stage.py"
GATES_PY = PAGE_GEN / "gates" / "run_gates.py"
SCHEMA_V3 = PAGE_GEN / "contract" / "page_output_schema_v3.json"

ENGINE_SRC = REPO / "03_operations" / "bsip2" / "proto_v0" / "src"

# The canonical 9 engine source files (from shadow_backtest.py ENGINE_FILES).
ENGINE_FILE_NAMES = [
    "score_engine.py",
    "constants.py",
    "nova_proxy.py",
    "signal_extractor.py",
    "router_v2.py",
    "evaluation_scope.py",
    "input_loader.py",
    "structural_classifier.py",
    "trace_writer.py",
]

# spine_pipeline code version — bump when this file's stage-building logic changes.
SPINE_PIPELINE_VERSION = "v1.0"


# ---------------------------------------------------------------------------
# Runner import (spine dir must be on sys.path)
# ---------------------------------------------------------------------------

def _ensure_spine_on_path() -> None:
    spine_str = str(SPINE_DIR)
    if spine_str not in sys.path:
        sys.path.insert(0, spine_str)


def _import_runner():
    _ensure_spine_on_path()
    from runner import Stage, run_pipeline  # noqa: PLC0415
    return Stage, run_pipeline


# ---------------------------------------------------------------------------
# Corpus manifest helper
# ---------------------------------------------------------------------------

def _write_corpus_manifest(corpus_dirs: list[str], shelf: str) -> Path:
    """
    Write a deterministic manifest of all bsip1_*.json file hashes in the
    corpus dirs.  This single file acts as the runner input for the corpus
    so that adding/removing/changing a BSIP1 record invalidates rescore.
    Returns the manifest path under _rescore_staging/<shelf>/.
    """
    manifest_dir = STAGING_ROOT / shelf
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / "corpus_manifest.txt"

    lines: list[str] = []
    for corpus_dir in corpus_dirs:
        cdir = Path(corpus_dir)
        if not cdir.is_dir():
            lines.append(f"MISSING:{corpus_dir}")
            continue
        for bsip1_file in sorted(cdir.glob("bsip1_*.json")):
            if "audit" in bsip1_file.name:
                continue
            try:
                digest = _sha256_file(bsip1_file)
                lines.append(f"{digest}  {bsip1_file}")
            except Exception as exc:
                lines.append(f"ERROR:{bsip1_file}:{exc}")

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Per-shelf config helpers (mirrors spine_flip helpers)
# ---------------------------------------------------------------------------

def _load_json(p: Path) -> dict[str, Any]:
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _get_shelf_config(shelf: str) -> tuple[Path, dict[str, Any]]:
    cfg_path = CONFIGS_DIR / f"{shelf}.json"
    if not cfg_path.is_file():
        raise FileNotFoundError(f"no config for shelf {shelf}: {cfg_path}")
    return cfg_path, _load_json(cfg_path)


def _normalize_corpus_dirs(cfg: dict[str, Any]) -> list[str]:
    scoring = cfg.get("scoring") or {}
    bsip1_dir = scoring.get("bsip1_dir")
    if bsip1_dir:
        return [bsip1_dir]
    corpus_dirs = cfg.get("corpus_dirs", [])
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    return [d for d in corpus_dirs if d]


def _derive_corpus_run_for_gates(
    cfg: dict[str, Any], shelf: str
) -> tuple[str | None, str | None]:
    """Return (corpus_dir, run_products_dir) — mirrors spine_flip.derive_corpus_run_for_gates."""
    corpus: str | None = None
    corpus_dirs = cfg.get("corpus_dirs") or []
    if isinstance(corpus_dirs, str):
        corpus_dirs = [corpus_dirs]
    for d in corpus_dirs:
        if d and Path(d).is_dir():
            corpus = str(d)
            break
    if not corpus:
        scoring = cfg.get("scoring") or {}
        bs = scoring.get("bsip1_dir")
        if bs and Path(bs).is_dir():
            corpus = str(bs)

    run_dir = str(STAGING_ROOT / shelf / "products")
    if not Path(run_dir).is_dir():
        rp = cfg.get("run_products_dir")
        if rp:
            if isinstance(rp, list):
                rp = next((x for x in rp if x and Path(x).is_dir()), None)
            if rp and Path(rp).is_dir():
                run_dir = str(rp)
            else:
                run_dir = None
        else:
            run_dir = None
    return corpus, run_dir


# ---------------------------------------------------------------------------
# Stage-function builders
# ---------------------------------------------------------------------------

def _make_rescore_fn(
    shelf: str,
    flag_env: dict[str, str],
    raw_scored: Path,
) -> Any:
    """
    Return a zero-arg callable that:
      1. Runs rescore_all.py --shelf <shelf>  (writes _rescored.json)
      2. Copies _rescored.json -> _rescored_raw.json so the runner's output
         contract has a stable hash that copy_stage.py won't overwrite.
    """
    import shutil as _shutil

    def fn() -> None:
        env = os.environ.copy()
        env.update(flag_env)
        staged = STAGING_ROOT / shelf / f"{shelf}_rescored.json"
        cmd = [sys.executable, str(RESCORE_PY), "--shelf", shelf]
        result = subprocess.run(
            cmd,
            cwd=str(REPO),
            env=env,
            capture_output=False,   # let output stream for visibility
        )
        if result.returncode not in (0, 1):
            # exit 1 = hard gate fail (OFF / C10) but output still produced.
            # Only non-{0,1} is a pipeline crash.
            raise RuntimeError(
                f"rescore_all.py --shelf {shelf} returned exit {result.returncode}"
            )
        # Snapshot the raw-scored page before copy_stage modifies it.
        if staged.is_file():
            _shutil.copy2(staged, raw_scored)
        else:
            raise RuntimeError(
                f"rescore_all.py did not produce {staged}"
            )

    return fn


def _make_copy_fn(
    shelf: str,
    raw_scored: Path,
    staged: Path,
    baseline_path: Path,
) -> Any:
    """
    Return a zero-arg callable that:
      1. Copies _rescored_raw.json -> _rescored.json  (restore clean rescore output)
      2. Runs copy_stage.py --staging <staged> which modifies staged in-place
         and writes author_set.json alongside.
    """
    import shutil as _shutil

    def fn() -> None:
        # Restore the raw scored page so copy_stage gets a clean pre-copy input.
        # (Needed on re-runs where staged may already be the copy-applied version.)
        _shutil.copy2(raw_scored, staged)
        cmd = [
            sys.executable, str(COPY_PY),
            "--staging", str(staged),
            "--live", str(baseline_path),
            "--shelf", shelf,
        ]
        result = subprocess.run(cmd, cwd=str(REPO), capture_output=False)
        if result.returncode not in (0, 1):
            raise RuntimeError(
                f"copy_stage.py for {shelf} returned exit {result.returncode}"
            )

    return fn


def _make_gate_fn(
    shelf: str,
    staged: Path,
    cfg_path: Path,
    baseline_path: Path,
    corpus_arg: str | None,
    run_arg: str | None,
) -> Any:
    def fn() -> None:
        cmd = [
            sys.executable, str(GATES_PY),
            str(staged),
            "--config", str(cfg_path),
            "--baseline", str(baseline_path),
        ]
        if SCHEMA_V3.is_file():
            cmd += ["--schema", str(SCHEMA_V3)]
        if corpus_arg:
            cmd += ["--corpus", corpus_arg]
        if run_arg:
            cmd += ["--run", run_arg]
        result = subprocess.run(cmd, cwd=str(REPO), capture_output=False)
        # Gate exit 0 = all pass, 1 = FAIL gates — both are valid; let the
        # caller inspect the report file.  Only a crash (returncode<0 or
        # unexpected) is an error here.
        if result.returncode not in (0, 1):
            raise RuntimeError(
                f"run_gates.py for {shelf} returned exit {result.returncode}"
            )

    return fn


# ---------------------------------------------------------------------------
# Main public API
# ---------------------------------------------------------------------------

def build_stages_for_shelf(
    shelf: str,
    flag_env: dict[str, str],
) -> tuple[list[Any], dict[str, Any]] | tuple[None, dict[str, Any]]:
    """
    Build the 3 Stage objects for a shelf.

    Returns (stages_list, shelf_meta) where shelf_meta carries cfg_path,
    baseline_path, gate_report_path, staged_page_path so the caller can
    assemble post-run reports without re-reading configs.

    Returns (None, {"error": ...}) if the shelf cannot be staged.
    """
    Stage, _ = _import_runner()

    try:
        cfg_path, cfg = _get_shelf_config(shelf)
    except FileNotFoundError as exc:
        return None, {"error": str(exc)}

    baseline_raw = cfg.get("baseline_json")
    if not baseline_raw or not Path(baseline_raw).is_file():
        return None, {"error": f"baseline_json missing or not found: {baseline_raw}"}

    baseline_path = Path(baseline_raw)
    corpus_dirs = _normalize_corpus_dirs(cfg)
    if not corpus_dirs:
        return None, {"error": "no corpus_dirs / bsip1_dir in config"}

    # Write the corpus manifest (stable hash-of-hashes over bsip1 files)
    corpus_manifest = _write_corpus_manifest(corpus_dirs, shelf)

    # Engine inputs (9 canonical files)
    engine_inputs: list[Path] = []
    for name in ENGINE_FILE_NAMES:
        p = ENGINE_SRC / name
        if p.is_file():
            engine_inputs.append(p)

    # Staging output paths.
    # rescore_all.py writes to _rescored.json in-place; copy_stage.py also modifies
    # that same file.  To avoid hash conflicts in the runner (rescore records the
    # pre-copy hash; copy then changes it so rescore always looks stale on the next
    # run), we save a separate snapshot of the raw-scored output for the runner:
    #   _rescored_raw.json  — rescore stage output (runner contract; never modified again)
    #   _rescored.json      — copy stage in+out (overwritten in-place by copy_stage.py)
    #   author_set.json     — copy stage output
    #   _gates_report.md    — gate stage output
    staged_page = STAGING_ROOT / shelf / f"{shelf}_rescored.json"
    raw_scored = STAGING_ROOT / shelf / f"{shelf}_rescored_raw.json"
    author_set = STAGING_ROOT / shelf / "author_set.json"
    gate_report = STAGING_ROOT / shelf / f"{shelf}_rescored_gates_report.md"

    corpus_arg, run_arg = _derive_corpus_run_for_gates(cfg, shelf)

    # Stage 1: rescore — outputs _rescored_raw.json (the runner's hash target)
    rescore_stage = Stage(
        name=f"rescore_{shelf}",
        fn=_make_rescore_fn(shelf, flag_env, raw_scored),
        inputs=engine_inputs + [cfg_path, corpus_manifest],
        outputs=[raw_scored],
        code_version=SPINE_PIPELINE_VERSION,
    )

    # Stage 2: copy — input = _rescored_raw.json + baseline;
    #                  output = _rescored.json (copy-applied) + author_set.json
    copy_stage = Stage(
        name=f"copy_{shelf}",
        fn=_make_copy_fn(shelf, raw_scored, staged_page, baseline_path),
        inputs=[raw_scored, baseline_path],
        outputs=[staged_page, author_set],
        code_version=SPINE_PIPELINE_VERSION,
    )

    # Stage 3: gate — input = _rescored.json (post-copy); output = gate report
    gate_stage = Stage(
        name=f"gate_{shelf}",
        fn=_make_gate_fn(shelf, staged_page, cfg_path, baseline_path, corpus_arg, run_arg),
        inputs=[staged_page],
        outputs=[gate_report],
        code_version=SPINE_PIPELINE_VERSION,
    )

    stages = [rescore_stage, copy_stage, gate_stage]
    meta = {
        "cfg_path": cfg_path,
        "cfg": cfg,
        "baseline_path": baseline_path,
        "staged_page": staged_page,
        "raw_scored": raw_scored,
        "author_set": author_set,
        "gate_report": gate_report,
        "corpus_dirs": corpus_dirs,
        "corpus_manifest": corpus_manifest,
    }
    return stages, meta


def run_via_spine(
    affected_shelves: list[str],
    overrides: dict[str, str],
    force: bool = False,
    db_path: Path | str | None = None,
) -> tuple[dict[str, str], list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Run the rescore->copy->gate chain for all affected_shelves through the
    Spine DAG runner.

    Parameters
    ----------
    affected_shelves : shelves to process (frozen gate already passed by caller)
    overrides        : flag env vars to inject (e.g. {"BARI_GLASSBOX_W4": "on"})
    force            : pass force=True to run_pipeline to re-run all stages
    db_path          : override spine.db path (None = default per spine_db.py)

    Returns
    -------
    pipeline_results : {stage_name: 'ran'|'skipped'} from run_pipeline()
    per_shelf        : list of per-shelf dicts matching spine_flip's format
    per_shelf_authors: list of {"shelf": ..., "author_set": ...} dicts
    """
    _, run_pipeline = _import_runner()

    flag_env: dict[str, str] = {}
    flag_env.update(overrides)

    all_stages: list[Any] = []
    shelf_metas: dict[str, dict[str, Any]] = {}
    shelf_errors: dict[str, str] = {}

    for shelf in affected_shelves:
        stages, meta = build_stages_for_shelf(shelf, flag_env)
        if stages is None:
            shelf_errors[shelf] = meta.get("error", "unknown error building stages")
            print(
                f"  SPINE PIPELINE WARNING: cannot build stages for {shelf}: {shelf_errors[shelf]}",
                file=sys.stderr,
            )
        else:
            all_stages.extend(stages)
            shelf_metas[shelf] = meta

    if not all_stages:
        # All shelves errored at stage-build time; nothing to run
        per_shelf = []
        for shelf in affected_shelves:
            per_shelf.append(
                _build_shelf_rec_error(shelf, shelf_errors.get(shelf, "stage build failed"))
            )
        return {}, per_shelf, []

    # Run the DAG — this enforces toposort, signatures, skip/run, and records lineage
    print(
        f"\n>>> run_pipeline: {len(all_stages)} stages across {len(shelf_metas)} shelf(s)"
    )
    t0 = time.perf_counter()
    pipeline_results = run_pipeline(all_stages, db_path=db_path, force=force)
    elapsed = time.perf_counter() - t0
    print(f"<<< run_pipeline done in {elapsed:.1f}s  results={pipeline_results}")

    # Now collect per-shelf records (mirrors spine_flip's existing report structure)
    per_shelf: list[dict[str, Any]] = []
    per_shelf_authors: list[dict[str, Any]] = []

    for shelf in affected_shelves:
        if shelf in shelf_errors:
            per_shelf.append(_build_shelf_rec_error(shelf, shelf_errors[shelf]))
            continue

        meta = shelf_metas[shelf]
        rec = _collect_shelf_record(shelf, meta, pipeline_results)
        per_shelf.append(rec)

        # Collect author set for consolidated report
        author_p = meta["author_set"]
        if author_p.is_file():
            try:
                adata = _load_json(author_p)
                per_shelf_authors.append({"shelf": shelf, "author_set": adata})
            except Exception as exc:
                rec["error"] = (rec.get("error") or "") + f"; author_set load: {exc}"

    return pipeline_results, per_shelf, per_shelf_authors


# ---------------------------------------------------------------------------
# Internal helpers for building per-shelf report records
# ---------------------------------------------------------------------------

def _build_shelf_rec_error(shelf: str, error: str) -> dict[str, Any]:
    return {
        "shelf": shelf,
        "rescore_exit": None,
        "copy_exit": None,
        "gate_exit": None,
        "score_moves": 0,
        "grade_moves": 0,
        "carried": 0,
        "author_needed": 0,
        "off_count": 0,
        "gate_overall": "UNKNOWN",
        "gate_report": None,
        "error": error,
        "staged_page_in_bundle": None,
        "spine_stages": {},
    }


def _count_off_in_page(page: dict[str, Any]) -> int:
    import re
    OFF_RE = re.compile(
        r"open_food_facts|openfoodfacts\.org|images\.openfoodfacts|off_candidate_panel",
        re.IGNORECASE,
    )
    return len(OFF_RE.findall(json.dumps(page.get("products", []), ensure_ascii=False)))


def _collect_shelf_record(
    shelf: str,
    meta: dict[str, Any],
    pipeline_results: dict[str, str],
) -> dict[str, Any]:
    """Build the per-shelf dict that spine_flip.main() aggregates into the report."""
    staged_page: Path = meta["staged_page"]
    baseline_path: Path = meta["baseline_path"]
    cfg: dict[str, Any] = meta["cfg"]
    gate_report: Path = meta["gate_report"]

    # Stage outcomes for this shelf
    shelf_stages = {
        k: v
        for k, v in pipeline_results.items()
        if k in (f"rescore_{shelf}", f"copy_{shelf}", f"gate_{shelf}")
    }

    rec: dict[str, Any] = {
        "shelf": shelf,
        "rescore_exit": None,
        "copy_exit": None,
        "gate_exit": None,
        "score_moves": 0,
        "grade_moves": 0,
        "carried": 0,
        "author_needed": 0,
        "off_count": 0,
        "gate_overall": "UNKNOWN",
        "gate_report": None,
        "error": None,
        "staged_page_in_bundle": None,
        "spine_stages": shelf_stages,
    }

    # Derive rescore outcome from the run_summary written by rescore_all
    rsumm = STAGING_ROOT / "run_summary.json"
    if rsumm.is_file():
        try:
            summ = _load_json(rsumm)
            for ent in summ.get("shelves", []):
                if ent.get("shelf") == shelf:
                    rec["score_moves"] = int(ent.get("score_moves") or 0)
                    rec["grade_moves"] = int(ent.get("grade_moves") or 0)
                    # rescore_all exit 0 = all gates pass, 1 = soft gate fail
                    rec["rescore_exit"] = 0 if ent.get("gate_pass") else 1
                    break
        except Exception:
            pass

    # copy_exit: infer from author_set presence
    author_p: Path = meta["author_set"]
    if author_p.is_file():
        rec["copy_exit"] = 0
        try:
            adata = _load_json(author_p)
            rec["carried"] = int(adata.get("carried", 0))
            rec["author_needed"] = len(adata.get("authored_needed", []))
        except Exception:
            pass
    elif pipeline_results.get(f"copy_{shelf}") == "skipped":
        rec["copy_exit"] = 0  # skipped = previously succeeded

    # gate outcome
    if gate_report.is_file():
        rec["gate_report"] = str(gate_report)
        # Derive gate_exit from the report content (PASS/FAIL summary line)
        try:
            text = gate_report.read_text(encoding="utf-8", errors="replace")
            if "FAIL" in text:
                rec["gate_exit"] = 1
                rec["gate_overall"] = "FAIL"
            else:
                rec["gate_exit"] = 0
                rec["gate_overall"] = "PASS"
        except Exception:
            rec["gate_overall"] = "UNKNOWN"
    elif pipeline_results.get(f"gate_{shelf}") == "skipped":
        # Skipped means last run was ok; reflect that
        rec["gate_exit"] = 0
        rec["gate_overall"] = "PASS (skipped)"

    # OFF check on the staged page
    if staged_page.is_file():
        try:
            page = _load_json(staged_page)
            rec["off_count"] = _count_off_in_page(page)
        except Exception:
            pass

    return rec
