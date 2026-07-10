#!/usr/bin/env python3
"""Unit tests for conformance.resolve_repo_path (TASK-560).

The page_generator configs declare corpus/baseline paths as absolute Windows literals
(``C:\\Bari\\02_products\\...``). POSIX cannot parse a drive letter, so such a string
becomes ONE relative filename and every ``is_dir()`` / ``is_file()`` check returns False.
That made HARD-1 and HARD-3 fail for every live shelf on the ubuntu CI runner, and made
the checks silently interrogate the WRONG checkout when run from a git worktree.

These tests run on the CI runner itself, so the POSIX behavior is asserted where it
actually matters. PureWindowsPath / PurePosixPath are platform-independent, which lets
the same assertions hold on both hosts.

Run: python -m pytest 03_operations/page_generator/test_conformance_paths.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

sys.path.insert(0, str(Path(__file__).resolve().parent))

import conformance as C  # noqa: E402

WIN_LITERAL = r"C:\Bari\03_operations\bsip1\run_bread_conform_001\output"
WIN_BASELINE = r"C:\Bari\bari-web\src\data\comparisons\bread_frontend_v4.json"


def test_naive_posix_parse_is_the_bug():
    """A drive-letter literal is a single relative filename on POSIX -- the root cause."""
    pp = PurePosixPath(WIN_LITERAL)
    assert len(pp.parts) == 1
    assert not pp.is_absolute()


def test_purewindowspath_parses_the_same_on_any_host():
    """The resolver's parsing step is host-independent, so CI and Windows agree."""
    parts = PureWindowsPath(WIN_LITERAL).parts
    assert parts[0] == "C:\\"
    assert "03_operations" in parts
    assert parts[-1] == "output"


def test_reanchors_onto_this_checkout():
    """Resolved path is under THIS repo, not the literal C:\\Bari."""
    resolved = C.resolve_repo_path(WIN_LITERAL)
    assert resolved.is_absolute()
    rel = resolved.relative_to(C.REPO)
    assert rel.as_posix() == "03_operations/bsip1/run_bread_conform_001/output"
    # no drive letter survives into the resolved path
    assert ":" not in rel.as_posix()


def test_reanchors_bari_web_baseline():
    resolved = C.resolve_repo_path(WIN_BASELINE)
    rel = resolved.relative_to(C.REPO)
    assert rel.as_posix() == "bari-web/src/data/comparisons/bread_frontend_v4.json"


def test_path_arithmetic_under_a_posix_root(monkeypatch):
    """Simulate the ubuntu runner: a POSIX REPO root must yield a clean POSIX path."""
    monkeypatch.setattr(C, "REPO", PurePosixPath("/home/runner/work/Barint/Barint"))
    resolved = C.resolve_repo_path(WIN_LITERAL)
    assert str(resolved) == (
        "/home/runner/work/Barint/Barint/03_operations/bsip1/run_bread_conform_001/output"
    )
    assert "\\" not in str(resolved)
    assert "C:" not in str(resolved)


def test_unknown_shape_is_returned_unchanged():
    """A path with no repo-top segment must NOT be silently re-anchored -- fail loudly."""
    weird = r"C:\bari_snacks\some\other\repo\products"
    resolved = C.resolve_repo_path(weird)
    assert str(resolved) == weird


def test_empty_and_none():
    assert str(C.resolve_repo_path("")) == "."
    assert str(C.resolve_repo_path(None)) == "."


def test_already_relative_path_is_preserved():
    rel_in = "03_operations/bsip1/run_bread_conform_001/output"
    resolved = C.resolve_repo_path(rel_in)
    assert resolved.relative_to(C.REPO).as_posix() == rel_in


def test_live_configs_all_resolve():
    """Every live shelf's declared dirs must exist once re-anchored on this checkout."""
    import json

    configs_dir = C.CONFIGS_DIR
    manifest = C.load_manifest_raw()
    configs = C.load_configs()
    stems = C.manifest_config_stems(manifest, configs)
    assert stems, "no live config stems resolved from live_manifest"

    unresolved: list[str] = []
    for stem in stems:
        cfg = json.loads((configs_dir / f"{stem}.json").read_text(encoding="utf-8-sig"))
        for key in ("corpus_dirs", "run_products_dir"):
            val = cfg.get(key)
            items = val if isinstance(val, list) else ([val] if val else [])
            for item in items:
                if item and not C.resolve_repo_path(item).is_dir():
                    unresolved.append(f"{stem}.{key}: {item}")
    assert not unresolved, f"unresolved corpus dirs after re-anchoring: {unresolved}"


if __name__ == "__main__":
    raise SystemExit(__import__("pytest").main([__file__, "-v", "--tb=short"]))
