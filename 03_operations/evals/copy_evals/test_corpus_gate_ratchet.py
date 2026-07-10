#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_corpus_gate_ratchet.py — TASK-576

Proof that the corpus ratchet gate does the one thing it exists to do: block a
NEW copy violation while tolerating the pre-existing dirty baseline. Without this
test the gate is just another `gates_designed_not_enforced` artifact — green
because it never actually fails on anything.

No live file is touched: the gate's pure functions (scan_shelf, check) are
exercised against synthetic in-memory product dicts.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "spine"))

import corpus_copy_gate as G  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _product(rowVerdict="", insightLine="", consumerTakeaway="", expansion=None):
    p = {"barcode": "test", "rowVerdict": rowVerdict, "insightLine": insightLine,
         "consumerTakeaway": consumerTakeaway}
    if expansion is not None:
        p["expansion"] = expansion
    return p


def main() -> int:
    failures: list[str] = []

    def expect(label, cond):
        print(f"  [{'ok  ' if cond else 'FAIL'}] {label}")
        if not cond:
            failures.append(label)

    print("scan_shelf — detects each gated rule")
    # banned pattern (data-state narration)
    s = G.scan_shelf({"products": [_product(rowVerdict="הציון מבוסס על הנתונים התזונתיים בלבד.")]})
    expect("banned_pattern counted", s.get("banned_pattern", 0) == 1)
    # grade in prose
    s = G.scan_shelf({"products": [_product(rowVerdict="היא נוחתת ב-B מוצק.")]})
    expect("grade_in_prose counted", s.get("grade_in_prose", 0) == 1)
    # ingredient count
    s = G.scan_shelf({"products": [_product(insightLine="שלושה רכיבים בלבד.")]})
    expect("ingredient_count counted", s.get("ingredient_count", 0) == 1)
    # malformed shape (granola-style str consumerExplanation)
    s = G.scan_shelf({"products": [_product(expansion={"consumerExplanation": "raw string"})]})
    expect("malformed_shape counted", s.get("malformed_shape", 0) == 1)
    # em dash is ADVISORY — must not be a gated key
    s = G.scan_shelf({"products": [_product(rowVerdict="חלב, מלח — ותרבית.")]})
    expect("em_dash is advisory (underscore key)", s.get("_em_dash_advisory", 0) == 1)
    expect("em_dash not in GATED_RULES", "_em_dash_advisory" not in G.GATED_RULES)

    print("\ncheck — ratchet semantics")
    baseline = {"shelves": {"demo": {"banned_phrase": 2, "grade_in_prose": 5}}}

    # at baseline → PASS
    ok, regr = G.check({"demo": {"banned_phrase": 2, "grade_in_prose": 5}}, baseline)
    expect("counts equal to baseline pass", ok and not regr)

    # below baseline (a fix landed) → PASS
    ok, regr = G.check({"demo": {"banned_phrase": 0, "grade_in_prose": 5}}, baseline)
    expect("counts below baseline pass (fixing always allowed)", ok)

    # one more banned_phrase → FAIL
    ok, regr = G.check({"demo": {"banned_phrase": 3, "grade_in_prose": 5}}, baseline)
    expect("regression above baseline fails", (not ok) and len(regr) == 1)

    # a brand-new rule not in baseline → FAIL
    ok, regr = G.check({"demo": {"banned_phrase": 2, "grade_in_prose": 5, "ingredient_count": 1}}, baseline)
    expect("new gated rule not in baseline fails", not ok)

    # a brand-new shelf with a violation → FAIL
    ok, regr = G.check({"demo": {"banned_phrase": 2, "grade_in_prose": 5},
                        "newshelf": {"antithesis": 1}}, baseline)
    expect("new shelf with violation fails", not ok)

    # advisory-only change (em dash) must NEVER fail the gate
    ok, regr = G.check({"demo": {"banned_phrase": 2, "grade_in_prose": 5, "_em_dash_advisory": 999}}, baseline)
    expect("advisory em-dash spike does not fail", ok)

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print("  -", f)
        return 1
    print("all corpus-gate ratchet tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
