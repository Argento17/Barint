r"""
adapters_parity_selftest.py — Bari adapter version-parity selftest (TASK-605)
================================================================================
Living-rules pilot (STF verdict memo `01_framework/governance/stf_memos/
2026-07-11_lesson-resolution-mechanism.md`, section "Living rules"). The STF
explicitly rejected a new `shared_rules/` directory as a second source of truth
mid-migration and instead said: extend the proven `dispatch.py --selftest-table`
byte-parity pattern to the per-vendor rule ADAPTERS, fail CI on retired version
strings, fix the live v4.2 drift as the pilot.

Canonical SoT: `01_framework/operations/capability_router_v5.md` (Capability
Router v5.2, TASK-600). Adapters — `CLAUDE.md`, `AGENTS.md`, every
`.claude/agents/*.md` — must be POINTERS into that doc, never duplicated law:
each must (a) reference the CURRENT router version/doc, and (b) contain zero
retired version strings (`v4.2`, `bari_router_v4_2` — the superseded router
this file's canonical doc replaced, per its own title line: "supersedes Router
v4.2").

This mirrors `dispatch.py`'s `cmd_selftest_table()` in spirit (doc is the SoT,
code/adapters follow it, `--selftest*` asserts the two never silently drift)
but checks adapter POINTERS rather than the Layer 1 / Layer 2 routing tables —
a deliberately different, narrower check. It does not read or alter
`dispatch.py`'s own LAYER1_TABLE/LAYER2_TABLE parity; run
`dispatch.py --selftest-table` separately for that.

Usage
-----
  python adapters_parity_selftest.py --selftest
      Check every real adapter in the repo. Exit 0 = PASS, exit 1 = FAIL
      (prints which adapter and which retired string / missing pointer).

  python adapters_parity_selftest.py --selftest-fixture
      Regression fixture (DoD requirement): builds a throwaway temp copy of the
      adapter set, injects a retired `v4.2` string into one of them, and
      asserts running the SAME check_adapter()/cmd_selftest() codepath against
      that poisoned tree returns exit 1. Proves the checker isn't a no-op.
      Never reads or writes any real adapter file.

Exit code convention (matches dispatch.py):
  0 = PASS
  1 = FAIL (a real problem — drift found, or the fixture failed to catch it)
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent.parent  # C:\Bari
CANONICAL_DOC_REL = Path("01_framework") / "operations" / "capability_router_v5.md"

# ── Retired-law patterns (Layer 0 invariant 7 territory: never re-add) ────────
# The canonical doc's OWN title line says "supersedes Router v4.2" — that's the
# SoT talking about its own history, not an adapter citing v4.2 as if it were
# still law. Adapters must carry zero occurrences of either string.
RETIRED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"v4\.2", re.IGNORECASE),
    re.compile(r"bari_router_v4_2", re.IGNORECASE),
]

# A pointer is machine-checkable if it names the canonical doc's file stem or
# the current "Capability Router vX.Y" version string somewhere in the file.
POINTER_PATTERN = re.compile(
    r"capability_router_v5(?:\.md)?|Capability Router v5(?:\.\d+)?",
    re.IGNORECASE,
)


def canonical_version(root: Path) -> str:
    """Derive the current version string from the canonical doc's own title
    line, so this checker never hardcodes a version the doc doesn't also
    assert (the same doc-is-SoT principle `--selftest-table` uses for the
    routing tables)."""
    doc_path = root / CANONICAL_DOC_REL
    text = doc_path.read_text(encoding="utf-8")
    first_line = text.splitlines()[0] if text else ""
    m = re.search(r"Capability Router (v\d+\.\d+)", first_line)
    if not m:
        raise ValueError(
            f"could not parse a 'Capability Router vX.Y' version from "
            f"{doc_path}'s title line: {first_line!r}"
        )
    return m.group(1)


def discover_adapters(root: Path) -> list[Path]:
    """The adapter set this selftest guards: CLAUDE.md, AGENTS.md, and every
    .claude/agents/*.md persona file (TASK-605 scope item 1)."""
    adapters = [root / "CLAUDE.md", root / "AGENTS.md"]
    agents_dir = root / ".claude" / "agents"
    if agents_dir.is_dir():
        adapters += sorted(agents_dir.glob("*.md"))
    return [p for p in adapters if p.exists()]


def check_adapter(path: Path, text: str | None = None) -> list[str]:
    """Return a list of problem strings for one adapter (empty list = clean).
    `text` lets callers check in-memory content (e.g. a poisoned fixture)
    without touching the filesystem."""
    problems: list[str] = []
    content = text if text is not None else path.read_text(encoding="utf-8")

    for pat in RETIRED_PATTERNS:
        m = pat.search(content)
        if m:
            line_no = content[: m.start()].count("\n") + 1
            problems.append(f"retired version string {m.group()!r} at line {line_no}")

    if not POINTER_PATTERN.search(content):
        problems.append(
            "no machine-checkable pointer to the canonical router doc/version found "
            "(expected 'capability_router_v5.md' or 'Capability Router v5.x')"
        )

    return problems


def cmd_selftest(root: Path = REPO_ROOT) -> int:
    try:
        version = canonical_version(root)
    except (OSError, ValueError) as e:
        print(f"[adapters-parity] FAIL — {e}", file=sys.stderr)
        return 1

    doc_path = root / CANONICAL_DOC_REL
    print(f"[adapters-parity] canonical SoT: {doc_path} (Capability Router {version})")

    adapters = discover_adapters(root)
    if not adapters:
        print("[adapters-parity] FAIL — no adapters discovered (CLAUDE.md/AGENTS.md/"
              ".claude/agents missing?)", file=sys.stderr)
        return 1

    ok = True
    for path in adapters:
        problems = check_adapter(path)
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        if problems:
            ok = False
            print(f"[adapters-parity] FAIL {rel}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"[adapters-parity] OK   {rel}")

    print(f"[adapters-parity] {len(adapters)} adapters checked. "
          f"{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def cmd_selftest_fixture() -> int:
    """DoD regression fixture: build a temp copy of the real adapter set,
    poison one file with a reintroduced retired v4.2 string, and assert the
    SAME cmd_selftest() codepath used in production returns exit 1 against it.
    Never mutates a real repo file."""
    with tempfile.TemporaryDirectory(prefix="adapters_parity_fixture_") as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "01_framework" / "operations").mkdir(parents=True)
        (tmp_root / ".claude" / "agents").mkdir(parents=True)

        # Minimal canonical doc stand-in (only the title line is parsed).
        (tmp_root / CANONICAL_DOC_REL).write_text(
            "# Capability Router v5.2 — HARD-STONED\n\nlaw.\n", encoding="utf-8"
        )
        # A clean adapter (should stay OK).
        (tmp_root / "CLAUDE.md").write_text(
            "Model routing: Capability Router v5.2 — capability_router_v5.md is law.\n",
            encoding="utf-8",
        )
        # A clean-pointer adapter that we then poison with a reintroduced
        # retired string — this is the exact drift class TASK-605 fixed.
        poisoned_text = (
            "Model routing: Capability Router v5.2 — capability_router_v5.md is law.\n"
            "Routing/lane law: `01_framework/operations/bari_router_v4_2.md` (canonical)\n"
        )
        (tmp_root / "AGENTS.md").write_text(poisoned_text, encoding="utf-8")
        (tmp_root / ".claude" / "agents" / "content-agent.md").write_text(
            "Capability Router v5.2 — capability_router_v5.md is the canonical pointer.\n",
            encoding="utf-8",
        )

        print("[adapters-parity-fixture] built a temp adapter tree and reintroduced "
              "'bari_router_v4_2' into a fixture AGENTS.md ...")
        rc = cmd_selftest(root=tmp_root)
        caught = (rc == 1)
        print(f"[adapters-parity-fixture] cmd_selftest() against the poisoned tree "
              f"returned exit {rc} -> {'CAUGHT (as expected)' if caught else 'MISSED — BUG'}")
        print(f"[adapters-parity-fixture] {'PASS' if caught else 'FAIL'}")
        return 0 if caught else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bari adapter version-parity selftest — implements the TASK-605 "
                     "living-rules pilot (extends dispatch.py --selftest-table to the "
                     "per-vendor rule adapters).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--selftest", action="store_true",
                         help="Check every real adapter for retired version strings "
                              "and a live pointer to the canonical router doc.")
    parser.add_argument("--selftest-fixture", action="store_true",
                         help="Regression fixture: prove the checker catches a "
                              "reintroduced v4.2 string. Never touches real files.")
    args = parser.parse_args()

    if args.selftest_fixture:
        sys.exit(cmd_selftest_fixture())
    if args.selftest:
        sys.exit(cmd_selftest())

    parser.error("no action given — pass --selftest or --selftest-fixture.")


if __name__ == "__main__":
    main()
