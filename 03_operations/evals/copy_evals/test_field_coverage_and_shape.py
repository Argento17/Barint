#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_field_coverage_and_shape.py — TASK-576

Regression proof for the two blindnesses closed alongside CHECK 6:

  (A) CRASH — iter_consumer_copy_fields assumed expansion.consumerExplanation
      is a dict. granola_frontend_v2.json ships it as a bare `str` (7 products)
      and `None` (15). Pre-fix: AttributeError → the gate NEVER ran on granola.
      Post-fix: no crash; a malformed str shape becomes a visible FINDING.

  (B) FIELD COVERAGE — expansion.limitingFactors[] / positiveSignals[] /
      comparisonContext are rendered to the consumer (expansion-section.tsx
      AssessmentSection lines 515/580 and ShelfContextSection line 721) but were
      never walked, so "הציון מבוסס על" in juices_frontend_v3.json passed with
      banned_pattern=0. Post-fix: the banned-pattern families fire on them.

Each test below FAILS against the pre-fix validate_copy_authored.py (the crash
one raises; the coverage ones assert a hit the pre-fix code cannot produce) and
passes after. Pure stdlib. Run:  python test_field_coverage_and_shape.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_GATE = Path(r"C:\Bari\03_operations\spine\validate_copy_authored.py")
_spec = importlib.util.spec_from_file_location("validate_copy_authored", _GATE)
vca = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vca)


def _page(products: list[dict]) -> dict:
    return {"products": products}


# ── (A) granola-shaped consumerExplanation: str and None ──────────────────────
GRANOLA_STR = {
    "barcode": "GRANOLA-STR",
    "insightLine": "דגן מלא הוא הבסיס.",
    "expansion": {"consumerExplanation": "מחרוזת חופשית שהגיעה במקום אובייקט"},
}
GRANOLA_NONE = {
    "barcode": "GRANOLA-NONE",
    "insightLine": "דגן מלא הוא הבסיס.",
    "expansion": {"consumerExplanation": None},
}


def test_no_crash_on_str_and_none_consumer_explanation() -> list[str]:
    """iter + check must tolerate str / None consumerExplanation (no traceback)."""
    fails: list[str] = []
    try:
        # iter_consumer_copy_fields post-fix returns (fields, malformed).
        res = vca.iter_consumer_copy_fields(GRANOLA_STR)
        fields, malformed = res if isinstance(res, tuple) else (res, [])
    except AttributeError as exc:
        return [f"(A) iter crashed on str consumerExplanation: {exc!r}"]
    # str shape must be a VISIBLE finding, never a silent skip.
    if not any(m.get("check") == "malformed_shape" for m in malformed):
        fails.append("(A) str consumerExplanation produced no malformed_shape finding")

    try:
        r_str = vca.check_copy_authored(_page([GRANOLA_STR]))
        r_none = vca.check_copy_authored(_page([GRANOLA_NONE]))
    except AttributeError as exc:
        return [f"(A) check_copy_authored crashed: {exc!r}"]
    # None is a legitimate empty shape → no malformed finding for it.
    if r_none.get("shape_hits", 0) != 0:
        fails.append("(A) None consumerExplanation wrongly flagged as malformed")
    # str shape fails the gate (malformed data must be visible, not silently passed).
    if r_str.get("shape_hits", 0) < 1:
        fails.append("(A) str consumerExplanation not counted in shape_hits")
    return fails


# ── (B) limitingFactors / positiveSignals / comparisonContext coverage ────────
LEAK_LIMITING = {
    "barcode": "LEAK-LF",
    "insightLine": "מיץ עם ריכוז סוכר גבוה יחסית.",
    "expansion": {
        "limitingFactors": [
            {"text": "השומן הגבוה ועדר נתוני רכיבים, כך שהציון מבוסס על הנתונים התזונתיים בלבד.", "magnitude": 2},
        ],
    },
}
LEAK_POSITIVE = {
    "barcode": "LEAK-PS",
    "insightLine": "מיץ עם ריכוז סוכר גבוה יחסית.",
    "expansion": {"positiveSignals": ["רשימת הרכיבים לא הגיעה מהסריקה."]},
}
LEAK_CONTEXT = {
    "barcode": "LEAK-CTX",
    "insightLine": "מיץ עם ריכוז סוכר גבוה יחסית.",
    "expansion": {"comparisonContext": "לא ניתן לאמת את רשימת הרכיבים במדף הזה."},
}
# A limitingFactors entry as a bare STRING (the other live shape) must also be scanned.
LEAK_LIMITING_STR = {
    "barcode": "LEAK-LF-STR",
    "insightLine": "מיץ עם ריכוז סוכר גבוה יחסית.",
    "expansion": {"limitingFactors": ["חסרים נתונים על התוספים."]},
}
# Clean control — none of these fields may fire.
CLEAN = {
    "barcode": "CLEAN",
    "insightLine": "הסוכר גבוה יחסית לרוב המיצים כאן.",
    "expansion": {
        "limitingFactors": [{"text": "הסוכר גבוה יחסית.", "magnitude": 1}],
        "positiveSignals": ["בלי ממתיקים מלאכותיים."],
        "comparisonContext": "מדורג באמצע המדף על סמך פרופיל הסוכר.",
    },
}


def _pattern_hits(product: dict) -> int:
    return vca.check_copy_authored(_page([product])).get("banned_pattern_hits", 0)


def test_limiting_factors_leak_now_caught() -> list[str]:
    fails: list[str] = []
    if _pattern_hits(LEAK_LIMITING) < 1:
        fails.append("(B) limitingFactors[].text leak NOT caught (pre-fix behaviour)")
    if _pattern_hits(LEAK_LIMITING_STR) < 1:
        fails.append("(B) limitingFactors[] bare-string leak NOT caught")
    return fails


def test_positive_signals_leak_now_caught() -> list[str]:
    return (
        []
        if _pattern_hits(LEAK_POSITIVE) >= 1
        else ["(B) positiveSignals[] leak NOT caught (pre-fix behaviour)"]
    )


def test_comparison_context_leak_now_caught() -> list[str]:
    return (
        []
        if _pattern_hits(LEAK_CONTEXT) >= 1
        else ["(B) comparisonContext leak NOT caught (pre-fix behaviour)"]
    )


def test_clean_new_fields_do_not_fire() -> list[str]:
    r = vca.check_copy_authored(_page([CLEAN]))
    fails = []
    if r.get("banned_pattern_hits", 0) != 0:
        fails.append("(B) clean new fields wrongly fired a banned pattern")
    if r.get("shape_hits", 0) != 0:
        fails.append("(B) clean well-typed fields wrongly flagged malformed")
    return fails


def main() -> int:
    tests = [
        ("A: no crash on str/None consumerExplanation", test_no_crash_on_str_and_none_consumer_explanation),
        ("B: limitingFactors leak caught", test_limiting_factors_leak_now_caught),
        ("B: positiveSignals leak caught", test_positive_signals_leak_now_caught),
        ("B: comparisonContext leak caught", test_comparison_context_leak_now_caught),
        ("B: clean new fields silent", test_clean_new_fields_do_not_fire),
    ]
    all_fails: list[str] = []
    for name, fn in tests:
        try:
            fails = fn()
        except Exception as exc:  # a raised exception is itself a failure (pre-fix crash)
            fails = [f"{name}: raised {type(exc).__name__}: {exc}"]
        status = "ok  " if not fails else "FAIL"
        print(f"  [{status}] {name}")
        all_fails.extend(fails)

    print()
    if all_fails:
        print(f"FAILED ({len(all_fails)}):")
        for f in all_fails:
            print("  -", f)
        return 1
    print(f"all field-coverage + shape tests passed ({len(tests)} groups)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
