#!/usr/bin/env python3
"""
affected_set.py — Spine step 2: resolve shadow what-if into an affected-set manifest.

Given flag overrides (or an existing shadow_report.json), determine which corpora
moved and which rescore_all shelf configs must re-run. No freeze gate (owner ruling
2026-06-18: nothing is frozen). Read-only over shadow/registry/configs — no scoring
re-implementation.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
CONFIGS_DIR = REPO / "03_operations" / "page_generator" / "configs"
SHADOW_ROOT = REPO / "03_operations" / "shadow"
SHADOW_REGISTRY = SHADOW_ROOT / "shadow_registry_v1.json"
SHADOW_RUNS_DIR = SHADOW_ROOT / "runs"
SHADOW_BACKTEST = REPO / "03_operations" / "bsip2" / "proto_v0" / "src" / "shadow_backtest.py"

# Known corpus name → rescore_all config stem aliases (filename without .json).
CORPUS_SHELF_ALIASES: dict[str, str] = {
    "hummus": "hummus_shelfrel_002",
    "cakes_hard_cookies": "cakes",
    "snack_bars": "snacks",
}

# Bidirectional alias lookup (corpus may appear under either name).
_CORPUS_ALIASES_REV: dict[str, str] = {}
for _corpus, _shelf in CORPUS_SHELF_ALIASES.items():
    _CORPUS_ALIASES_REV[_corpus] = _shelf
    if _shelf not in _CORPUS_ALIASES_REV:
        _CORPUS_ALIASES_REV[_shelf] = _corpus


def _norm_path(p: str | None) -> str:
    if not p:
        return ""
    return str(Path(p).resolve()).lower().replace("\\", "/")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _discover_shelf_configs() -> dict[str, dict[str, Any]]:
    """Return config stem → {category, source_paths}."""
    shelves: dict[str, dict[str, Any]] = {}
    for cfg_path in sorted(CONFIGS_DIR.glob("*.json")):
        if cfg_path.name.startswith("_generated_"):
            continue
        stem = cfg_path.stem
        cfg = _load_json(cfg_path)
        scoring = cfg.get("scoring") or {}
        sources: set[str] = set()
        for key in ("corpus_dirs", "run_products_dir"):
            val = cfg.get(key)
            if isinstance(val, str) and val:
                sources.add(_norm_path(val))
            elif isinstance(val, list):
                for item in val:
                    if item:
                        sources.add(_norm_path(item))
        bsip1 = scoring.get("bsip1_dir")
        if isinstance(bsip1, str) and bsip1:
            sources.add(_norm_path(bsip1))
        shelves[stem] = {
            "category": (cfg.get("category") or "").lower().replace("-", "_"),
            "sources": sources,
        }
    return shelves


def _registry_sources() -> dict[str, str | list[str]]:
    reg = _load_json(SHADOW_REGISTRY)
    out: dict[str, str | list[str]] = {}
    for c in reg.get("corpora", []):
        src = c.get("source")
        if isinstance(src, list):
            out[c["name"]] = [_norm_path(s) for s in src]
        else:
            out[c["name"]] = _norm_path(src)
    return out


def build_corpus_to_shelves_map() -> dict[str, list[str]]:
    """
    Map shadow corpus name → one or more rescore_all config stems.
    Multiple shelves may share a corpus dir (e.g. cereals + granola).
    """
    shelves = _discover_shelf_configs()
    reg_sources = _registry_sources()

    corpus_to_shelves: dict[str, list[str]] = {}

    def add_mapping(corpus: str, shelf: str) -> None:
        corpus_to_shelves.setdefault(corpus, [])
        if shelf not in corpus_to_shelves[corpus]:
            corpus_to_shelves[corpus].append(shelf)

    for corpus in reg_sources:
        if corpus in CORPUS_SHELF_ALIASES:
            add_mapping(corpus, CORPUS_SHELF_ALIASES[corpus])

        if corpus in shelves:
            add_mapping(corpus, corpus)

        norm_corpus = corpus.lower().replace("-", "_")
        for stem, meta in shelves.items():
            if meta["category"] and meta["category"] == norm_corpus:
                add_mapping(corpus, stem)

        src = reg_sources.get(corpus, "")
        srcs = src if isinstance(src, list) else ([src] if src else [])
        for reg_src in srcs:
            if not reg_src:
                continue
            for stem, meta in shelves.items():
                if reg_src in meta["sources"]:
                    add_mapping(corpus, stem)

    return corpus_to_shelves


def _grade_changes_count(entry: dict[str, Any]) -> int:
    gc = entry.get("grade_changes")
    if isinstance(gc, list):
        return len(gc)
    if isinstance(gc, (int, float)):
        return int(gc)
    return 0


def _is_affected(entry: dict[str, Any]) -> bool:
    if entry.get("skipped_missing_source"):
        return False
    moved = int(entry.get("moved") or 0)
    grade_changes = _grade_changes_count(entry)
    added = entry.get("added_pids") or []
    removed = entry.get("removed_pids") or []
    violations = entry.get("invariant_violations") or []
    return bool(moved > 0 or grade_changes > 0 or added or removed or violations)


def _max_abs_move(entry: dict[str, Any]) -> float:
    moves = entry.get("moves") or []
    if not moves:
        return 0.0
    deltas = [abs(float(m.get("delta") or 0.0)) for m in moves]
    return round(max(deltas), 1) if deltas else 0.0


def resolve_shelf(corpus: str, corpus_to_shelves: dict[str, list[str]]) -> tuple[str | None, str | None]:
    """Return (primary_shelf, no_config_reason)."""
    shelves = corpus_to_shelves.get(corpus, [])
    if shelves:
        return shelves[0], None
    if corpus in _CORPUS_ALIASES_REV:
        alias = _CORPUS_ALIASES_REV[corpus]
        if alias in corpus_to_shelves:
            return corpus_to_shelves[alias][0], None
    return None, "no matching page_generator config (deferred/bespoke or not yet shelved)"


def build_affected_set(report: dict[str, Any]) -> dict[str, Any]:
    corpus_to_shelves = build_corpus_to_shelves_map()
    corpora = report.get("corpora") or {}

    affected: list[dict[str, Any]] = []
    affected_shelves: list[str] = []
    affected_no_config: list[dict[str, str]] = []

    for corpus, entry in sorted(corpora.items()):
        if not _is_affected(entry):
            continue

        cls = entry.get("class", "")
        shelf, no_config_reason = resolve_shelf(corpus, corpus_to_shelves)

        affected.append({
            "corpus": corpus,
            "class": cls,
            "n": int(entry.get("n") or 0),
            "moved": int(entry.get("moved") or 0),
            "grade_changes": _grade_changes_count(entry),
            "max_abs_move": _max_abs_move(entry),
            "shelf": shelf,
        })

        if shelf:
            for s in corpus_to_shelves.get(corpus, [shelf]):
                if s not in affected_shelves:
                    affected_shelves.append(s)
        else:
            affected_no_config.append({"corpus": corpus, "reason": no_config_reason or "unmapped"})

    return {
        "flag_overrides": report.get("flag_overrides") or {},
        "shadow_verdict": report.get("verdict", ""),
        "shadow_exit_code": int(report.get("exit_code", 0)),
        "affected": affected,
        "affected_shelves": sorted(affected_shelves),
        "affected_no_config": affected_no_config,
    }


def compute_exit_code(manifest: dict[str, Any]) -> int:
    # No freeze gate (owner 2026-06-18: nothing is frozen). 1 = movement, 0 = none.
    if manifest["affected"]:
        return 1
    return 0


def print_summary(manifest: dict[str, Any], report_path: Path) -> None:
    print(f"shadow report: {report_path}")
    print(f"verdict: {manifest['shadow_verdict']}  exit_code: {manifest['shadow_exit_code']}")
    print(f"affected corpora: {len(manifest['affected'])}")
    for row in manifest["affected"]:
        print(
            f"  {row['corpus']:22s} [{row['class']:9s}] "
            f"moved={row['moved']:3d} grade_changes={row['grade_changes']:2d} "
            f"max_abs_move={row['max_abs_move']:4.1f} shelf={row['shelf']}"
        )
    if manifest["affected_shelves"]:
        print(f"affected_shelves (rescore_all --shelf): {', '.join(manifest['affected_shelves'])}")
    if manifest["affected_no_config"]:
        print("affected_no_config:")
        for row in manifest["affected_no_config"]:
            print(f"  {row['corpus']}: {row['reason']}")


def _parse_written_report(stdout: str) -> Path | None:
    for line in stdout.splitlines():
        m = re.search(r"written:\s+(.+)", line)
        if m:
            written = Path(m.group(1).strip())
            json_path = written.with_name("shadow_report.json")
            if json_path.is_file():
                return json_path
            if written.suffix == ".md":
                candidate = written.parent / "shadow_report.json"
                if candidate.is_file():
                    return candidate
    return None


def _newest_shadow_report() -> Path | None:
    if not SHADOW_RUNS_DIR.is_dir():
        return None
    candidates = sorted(
        SHADOW_RUNS_DIR.glob("shadow_*/shadow_report.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def run_shadow_diff(flag_sets: list[str]) -> tuple[Path, int]:
    cmd = [sys.executable, str(SHADOW_BACKTEST), "diff"]
    for kv in flag_sets:
        cmd.extend(["--set", kv])
    result = subprocess.run(
        cmd,
        cwd=str(SHADOW_BACKTEST.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    stdout = (result.stdout or "") + (result.stderr or "")
    report_path = _parse_written_report(stdout)
    if report_path is None:
        report_path = _newest_shadow_report()
    if report_path is None or not report_path.is_file():
        print("ERROR: shadow_backtest diff did not produce shadow_report.json", file=sys.stderr)
        print(stdout, file=sys.stderr)
        sys.exit(3)
    return report_path, result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve shadow what-if into affected-set manifest for spine orchestrator."
    )
    parser.add_argument(
        "--set",
        action="append",
        metavar="FLAG=VAL",
        help="what-if flag override (repeatable); used when --report is omitted",
    )
    parser.add_argument(
        "--report",
        help="path to existing shadow_report.json (skip shadow_backtest invocation)",
    )
    parser.add_argument(
        "--out",
        default="affected_set.json",
        help="output path for affected_set.json (default: affected_set.json)",
    )
    args = parser.parse_args()

    if args.report:
        report_path = Path(args.report)
        if not report_path.is_file():
            print(f"ERROR: report not found: {report_path}", file=sys.stderr)
            return 3
        report = _load_json(report_path)
    else:
        if not args.set:
            print("ERROR: provide --report or at least one --set FLAG=VAL", file=sys.stderr)
            return 3
        report_path, _ = run_shadow_diff(args.set)
        report = _load_json(report_path)

    manifest = build_affected_set(report)
    exit_code = compute_exit_code(manifest)

    out_path = Path(args.out)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print_summary(manifest, report_path)
    print(f"written: {out_path.resolve()}")
    print(f"exit: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())