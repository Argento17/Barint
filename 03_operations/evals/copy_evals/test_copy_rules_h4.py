#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_copy_rules_h4.py — TASK-576

Proof that the H4 rules catch the exact owner-flagged strings and stay silent on
the owner-approved ones. Every POSITIVE below is a real string the owner rejected
in the 2026-07-10 review of 30 live rows; every NEGATIVE is either a string he
approved outright or a near-miss that a lazier regex would have caught.

Written because the superlative gate shipped reporting "0 violations" on copy it
was structurally incapable of examining (final-kaf vs. medial-kaf), and the
antithesis rule shipped enforced-nowhere. A rule is not a rule until a test
proves it fires. Run:  python test_copy_rules_h4.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import copy_rules as R  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# (label, text) — every one of these MUST fire.
GRADE_POSITIVE = [
    ("owner row 21", "הם הפשרה שמשאירה אותו ב-B"),
    ("live bread_v3", "מקור צמחי-זרעי הם הסיבה לפרופיל הזה. ציון S."),
    ("live cheese", "השומן הבינוני-גבוה הוא מה שמציב אותה ב-C."),
    ("live cookies", "העוגיות המרוקאיות של לה פזואלוס מגיעות ל-D."),
    ("live crackers", "סולפיט ברשימה, אלרגן מוצהר, מוריד ל-E."),
    ("range form", "ההפרש בין C ל-E הוא ממשי."),
    ("בציון form", "המוצר מסתיים בציון B בגלל הנתרן."),
    ("דירוג form", "דירוג C משקף את הסוכר."),
]

# These MUST NOT fire — vitamin letters and grade-like tokens that aren't grades.
GRADE_NEGATIVE = [
    ("vitamin C", "מקור טוב לוויטמין C ולסיבים."),
    ("vitamin B12", "מועשר בוויטמין B12."),
    ("vitamin E", "שמן קנולה תורם ויטמין E."),
    ("vitamin, ל- form", "עשיר בוויטמין D בזכות הביצה."),
    ("omega", "אומגה 3 ממקור צמחי."),
    ("no grade at all", "טחינה גולמית ומעט מלח."),
]

INGREDIENT_POSITIVE = [
    ("owner row 4", "בזכות שלושה רכיבים בלבד"),
    ("owner row 5, digit", "מכיל 5 רכיבים ותו לא."),
    ("our own cereals v2", "שלושה רכיבים, אפס תוספי מזון"),
    ("teen number", "אחד עשר רכיבים ברשימה."),
    ("מרכיבים variant", "ארבעה מרכיבים בסך הכל."),
]

INGREDIENT_NEGATIVE = [
    ("no number", "רשימת רכיבים קצרה ונקייה."),
    ("number, other noun", "שלושה כפות טחינה."),
    ("count of additives", "אפס תוספי מזון."),
]

STOCK_POSITIVE = [
    ("owner row 18", "שיבולת השועל עושה כאן את רוב העבודה."),
    ("plural", "הסיבים עושים את רוב העבודה."),
    ("no רוב", "החלבון עושה את העבודה."),
]
STOCK_NEGATIVE = [("unrelated", "המוצר עובד טוב כארוחת בוקר.")]


def _check(label, text, fired, want, failures):
    ok = fired == want
    mark = "ok  " if ok else "FAIL"
    verb = "fired" if fired else "silent"
    print(f"  [{mark}] {label:<22} {verb:<7} {text[:44]}")
    if not ok:
        failures.append(f"{label}: expected {'fire' if want else 'silence'}, got {verb}")


def main() -> int:
    failures: list[str] = []

    print("grade_in_prose — must fire (H4-P7)")
    for label, text in GRADE_POSITIVE:
        _check(label, text, R.rule_grade_in_prose(text) is not None, True, failures)
    print("grade_in_prose — must stay silent (vitamin letters)")
    for label, text in GRADE_NEGATIVE:
        _check(label, text, R.rule_grade_in_prose(text) is not None, False, failures)

    print("\ningredient_count — must fire (H4-P2)")
    for label, text in INGREDIENT_POSITIVE:
        _check(label, text, R.ingredient_count_hard_fires(text), True, failures)
    print("ingredient_count — must stay silent")
    for label, text in INGREDIENT_NEGATIVE:
        _check(label, text, R.ingredient_count_hard_fires(text), False, failures)

    print("\nstock_phrase — must fire (H4-P6)")
    for label, text in STOCK_POSITIVE:
        _check(label, text, R.stock_phrase_hard_fires(text), True, failures)
    print("stock_phrase — must stay silent")
    for label, text in STOCK_NEGATIVE:
        _check(label, text, R.stock_phrase_hard_fires(text), False, failures)

    print("\ncross_field_value_repetition — must fire (H4-P3)")
    repeated = {
        "insightLine": "מכיל 12 גרם חלבון למנה.",
        "rowVerdict": "החלבון עומד על 12 גרם, והנתרן על 400 מ\"ג.",
        "consumerTakeaway": "בחירה סבירה לארוחת בוקר.",
    }
    hits = R.find_cross_field_value_repetition(repeated)
    _check("12 גרם in 2 fields", "insightLine+rowVerdict",
           any(h["value"] == "12גרם" for h in hits), True, failures)
    _check("400 מ\"ג in 1 field", "rowVerdict only",
           any(h["value"].startswith("400") for h in hits), False, failures)

    print("cross_field_value_repetition — must stay silent")
    # "100%" is a composition claim, not a nutrition value. Counting it once
    # inflated this rule's site-wide reading from 34% to 57%.
    pct = {"insightLine": "100% קמח חיטה מלא.", "rowVerdict": "100% דגן מלא, בלי תוספות."}
    _check("100% composition", "not a nutrition value",
           bool(R.find_cross_field_value_repetition(pct)), False, failures)
    # Same figure twice inside ONE field is rule_number_density's job, not this one.
    one = {"rowVerdict": "12 גרם חלבון ועוד 12 גרם פחמימות."}
    _check("same value, one field", "within-field, not cross-field",
           bool(R.find_cross_field_value_repetition(one)), False, failures)

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print("  -", f)
        return 1
    print("all H4 rule tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
