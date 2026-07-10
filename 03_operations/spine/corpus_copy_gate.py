#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corpus_copy_gate.py — TASK-576

The missing enforcement line. Every copy detector Bari owns runs at GENERATION
(only when a page is rebuilt) or at COMMIT (staged files only, fails open). The
710-row LIVE corpus sits behind nothing, so a rule added after a page was signed
off is never applied to it — the `gates_designed_not_enforced` failure class.

This gate runs every HARD copy rule across ALL live comparison shelves on every
push, in CI. Because the corpus is already dirty (hundreds of pre-existing
violations), a gate that hard-failed on the absolute count could never go green,
so it is a RATCHET against a committed baseline:

  * baseline = {shelf: {rule: count}}  (copy_violation_baseline.json)
  * --check FAILS iff any (shelf, rule) count EXCEEDS its baseline, or a NEW
    (shelf, rule) pair appears. Counts at or below baseline PASS.
  * The baseline can only be regenerated with --write-baseline, which is a
    reviewable diff — a human sees the numbers move.

Net effect: you cannot ADD a violation (regression blocked), and every fix
lowers the baseline the next time it is written. The corpus can only get cleaner.

Rules enforced (HARD): banned_phrase, banned_pattern (data-state narration),
malformed_shape, grade_in_prose, ingredient_count, stock_phrase, antithesis,
cross_field_value_repetition, sodium_term.

Rules reported but NOT gated (owner ruling — minimize, not ban): em_dash,
number_density, recite (WARN). These are surfaced in --report for the sweep but
never move the exit code.

Usage:
  python corpus_copy_gate.py --check            # CI: exit 1 on any regression
  python corpus_copy_gate.py --report           # human: full per-shelf table
  python corpus_copy_gate.py --write-baseline    # regenerate the baseline JSON
  python corpus_copy_gate.py --emit-json        # machine-readable current counts

Exit codes: 0 clean / no regression · 1 regression vs baseline · 2 usage/load error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

_ROOT = Path(__file__).resolve().parent.parent.parent
_COMPARISONS = _ROOT / "bari-web" / "src" / "data" / "comparisons"
_BASELINE = Path(__file__).resolve().parent / "copy_violation_baseline.json"

sys.path.insert(0, str(_ROOT / "03_operations" / "evals" / "copy_evals"))
sys.path.insert(0, str(_ROOT / "03_operations" / "page_generator" / "copy"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import copy_rules as R  # noqa: E402
import copy_constants as C  # noqa: E402
import validate_copy_authored as V  # noqa: E402

# HARD rules — each contributes to the gated count. em_dash / number_density are
# deliberately absent (owner: minimize, not ban).
_BANNED_PATTERNS = [(name, re.compile(rx)) for name, rx in C.get_banned_patterns()]
_BANNED_PHRASES = C.get_banned_phrases()


def _load_shelves() -> list[tuple[str, dict]]:
    out = []
    for path in sorted(_COMPARISONS.glob("*.json")):
        if "ledger" in path.name:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise SystemExit(f"[corpus-gate] cannot load {path.name}: {exc}")
        shelf = path.name.replace("_frontend", "").replace(".json", "")
        out.append((shelf, data))
    return out


def _products(data: dict) -> list:
    p = data.get("products")
    if isinstance(p, dict):
        return list(p.values())
    return p or []


def scan_shelf(data: dict) -> dict[str, int]:
    """Return {rule: violation_count} for one shelf using the canonical detectors."""
    counts: dict[str, int] = defaultdict(int)
    for product in _products(data):
        if not isinstance(product, dict):
            counts["malformed_shape"] += 1
            continue
        fields, malformed = V.iter_consumer_copy_fields(product)
        counts["malformed_shape"] += len(malformed)

        # Per-field single-string rules.
        prose_by_name: dict[str, str] = {}
        for path, text in fields:
            short = path.split(":", 1)[-1]
            prose_by_name[short] = prose_by_name.get(short, "") + " " + text

            for phrase in _BANNED_PHRASES:
                if phrase in text:
                    counts["banned_phrase"] += 1
                    break
            for _name, prx in _BANNED_PATTERNS:
                if prx.search(text):
                    counts["banned_pattern"] += 1
                    break
            if R.rule_grade_in_prose(text):
                counts["grade_in_prose"] += 1
            if R.ingredient_count_hard_fires(text):
                counts["ingredient_count"] += 1
            if R.stock_phrase_hard_fires(text):
                counts["stock_phrase"] += 1
            if R.antithesis_hard_fires(text):
                counts["antithesis"] += 1
            if R.sodium_term_hard_fires(text):
                counts["sodium_term"] += 1
            # Advisory — reported, never gated.
            if R.rule_em_dash(text):
                counts["_em_dash_advisory"] += text.count("—")

        # Cross-field: one entry per product with any repeated nutrition figure.
        if R.find_cross_field_value_repetition(prose_by_name):
            counts["cross_field_value_repetition"] += 1

    return dict(counts)


# Rules whose count moves the exit code. Advisory keys start with "_".
GATED_RULES = frozenset({
    "banned_phrase", "banned_pattern", "malformed_shape", "grade_in_prose",
    "ingredient_count", "stock_phrase", "antithesis",
    "cross_field_value_repetition", "sodium_term",
})


def scan_all() -> dict[str, dict[str, int]]:
    return {shelf: scan_shelf(data) for shelf, data in _load_shelves()}


def _gated_only(counts: dict[str, int]) -> dict[str, int]:
    return {r: n for r, n in counts.items() if r in GATED_RULES and n > 0}


def check(current: dict[str, dict[str, int]], baseline: dict) -> tuple[bool, list[str]]:
    """Return (ok, regressions). A regression = a gated (shelf, rule) count that
    exceeds baseline, or a new gated (shelf, rule) not in baseline."""
    regressions: list[str] = []
    base_shelves = baseline.get("shelves", {})
    for shelf, counts in current.items():
        base = base_shelves.get(shelf, {})
        for rule, n in _gated_only(counts).items():
            allowed = base.get(rule, 0)
            if n > allowed:
                regressions.append(
                    f"{shelf} · {rule}: {n} > baseline {allowed} (+{n - allowed})"
                )
    return (len(regressions) == 0, sorted(regressions))


def _totals(current: dict[str, dict[str, int]]) -> dict[str, int]:
    tot: dict[str, int] = defaultdict(int)
    for counts in current.values():
        for rule, n in counts.items():
            tot[rule] += n
    return dict(tot)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Corpus-wide copy ratchet gate")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="CI mode: exit 1 on regression vs baseline")
    g.add_argument("--report", action="store_true", help="human per-shelf table")
    g.add_argument("--write-baseline", action="store_true", help="regenerate the baseline JSON")
    g.add_argument("--emit-json", action="store_true", help="machine-readable current counts")
    args = ap.parse_args(argv)

    current = scan_all()

    if args.write_baseline:
        payload = {
            "_comment": (
                "Ratchet baseline for corpus_copy_gate.py — max ALLOWED gated "
                "violations per (shelf, rule). Regenerate ONLY via --write-baseline; "
                "the diff must show counts going DOWN. Advisory keys (_em_dash*) are "
                "recorded for visibility but never gate."
            ),
            "shelves": {s: c for s, c in sorted(current.items())},
        }
        _BASELINE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        tot = _totals(current)
        gated = sum(n for r, n in tot.items() if r in GATED_RULES)
        print(f"[corpus-gate] baseline written: {len(current)} shelves, "
              f"{gated} gated violations, {tot.get('_em_dash_advisory', 0)} em-dashes (advisory).")
        return 0

    if args.emit_json:
        print(json.dumps({"shelves": current, "totals": _totals(current)},
                         ensure_ascii=False, indent=1))
        return 0

    if args.report:
        rules = sorted(GATED_RULES) + ["_em_dash_advisory"]
        w = 15
        print(f"{'shelf':<24}" + "".join(f"{r[:13]:>{w}}" for r in rules))
        print("-" * (24 + w * len(rules)))
        for shelf, counts in sorted(current.items()):
            print(f"{shelf:<24}" + "".join(f"{counts.get(r, 0):>{w}}" for r in rules))
        print("-" * (24 + w * len(rules)))
        tot = _totals(current)
        print(f"{'TOTAL':<24}" + "".join(f"{tot.get(r, 0):>{w}}" for r in rules))
        gated = sum(n for r, n in tot.items() if r in GATED_RULES)
        print(f"\ngated violations: {gated}   (advisory em-dashes: {tot.get('_em_dash_advisory', 0)})")
        return 0

    # default / --check
    if not _BASELINE.exists():
        print(f"[corpus-gate] no baseline at {_BASELINE.name}; run --write-baseline first.",
              file=sys.stderr)
        return 2
    baseline = json.loads(_BASELINE.read_text(encoding="utf-8"))
    ok, regressions = check(current, baseline)
    if ok:
        gated = sum(n for r, n in _totals(current).items() if r in GATED_RULES)
        print(f"[corpus-gate] PASS — no copy-rule regression vs baseline "
              f"({gated} gated violations, all at/below baseline).")
        return 0
    print(f"[corpus-gate] FAIL — {len(regressions)} copy-rule regression(s) vs baseline:")
    for r in regressions:
        print(f"  · {r}")
    print("\nA new consumer-copy violation was introduced. Fix the copy, or if this "
          "is an intentional (reviewed) change, regenerate the baseline with "
          "--write-baseline and commit the diff.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
