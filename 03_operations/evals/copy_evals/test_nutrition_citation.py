#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_nutrition_citation.py — OWNER RULING 2026-07-10 (TASK-576)

"No more citing nutritional values — that's it." Proof that
rule_nutrition_value_citation fires on every nutrition-panel figure and stays
silent on ingredient proportions and pure description.

POSITIVES are verbatim strings from the v2 drafts the owner REJECTED for exactly
this reason. NEGATIVES are the line we must not cross: an ingredient percentage
(18% almonds) describes the food and is allowed; only PANEL values are banned.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import copy_rules as R  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Must FIRE — verbatim from the rejected v2 batch + paraphrases.
POSITIVE = [
    ("grams protein", "חלבון גבוה יחסית, 26 גרם, לצד נתרן גבוה."),
    ("mg sodium full", "הנתרן עומד על 660 מיליגרם."),
    ("mg sodium abbr", 'הנתרן, 490 מ"ג, נמוך יחסית.'),
    ("calories", "הצפיפות הקלורית גבוהה, 453 קלוריות ל-100 גרם."),
    ("satfat grams", "השומן הרווי גבוה, 6.1 גרם ל-100 גרם."),
    ("fat percent", "גבינה צהובה 32% שומן עם נתרן נמוך."),
    ("fat percent tight", "גאודה 30% שומן."),
    ("nutrient then pct", "רמת השומן כאן מגיעה ל-32%."),
    ("per-100g frame", "27 גרם שומן ל-100 גרם, נמוך יחסית."),
]

# Must STAY SILENT — description, ingredient proportion, experience words.
NEGATIVE = [
    ("almond ingredient %", "שקדים כרכיב הראשון (18%) וחמוציות אמיתיות."),
    ("spelt flour %", "עוגיות כוסמין מלא עם 34% קמח כוסמין."),
    ("white choc %", "קוקיס עם שוקולד לבן (כ-20%) ומרגרינה."),
    ("salty as experience", "גבינה מלוחה ועשירה שנועדה לטעם, לא לכל יום."),
    ("lean description", "גבינה רזה יחסית עם מרקם נעים."),
    ("pure identity", "עוגיות בטעם חמאה שאין בהן חמאה אמיתית."),
    ("ingredient list", "חלב, מלח, תרבית לקטית ומקריש."),
    ("rank not value", "הנתרן הגבוה ביותר מכל הגבינות הקשות בסקירה."),
]


def main() -> int:
    failures: list[str] = []

    print("nutrition_value_citation — MUST FIRE (owner: no cited values)")
    for label, text in POSITIVE:
        fired = R.nutrition_value_citation_hard_fires(text)
        print(f"  [{'ok  ' if fired else 'FAIL'}] {label:<20} {text[:42]}")
        if not fired:
            failures.append(f"{label}: expected fire, silent")

    print("\nnutrition_value_citation — MUST STAY SILENT (description / ingredient %)")
    for label, text in NEGATIVE:
        fired = R.nutrition_value_citation_hard_fires(text)
        print(f"  [{'ok  ' if not fired else 'FAIL'}] {label:<20} {text[:42]}")
        if fired:
            failures.append(f"{label}: expected silence, fired")

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print("  -", f)
        return 1
    print(f"all nutrition-citation tests passed ({len(POSITIVE)} fire, {len(NEGATIVE)} silent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
