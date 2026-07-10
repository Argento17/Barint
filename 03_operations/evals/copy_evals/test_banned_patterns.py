#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_banned_patterns.py — TASK-576

Proof for CHECK 6 (copy_constants.BANNED_CONSUMER_PATTERNS): the data-state /
confidence narration families fire on every real live violation and stay silent
on legitimate copy that merely happens to contain a similar word.

The POSITIVES are verbatim strings pulled from live comparison JSON on
2026-07-10 — every one of them passed CHECK 1 with banned=0.

The NEGATIVES are the traps. "בהיעדר סוכר מוסף" is good copy and must not fire;
only the DATA-absence framing is banned. "אומת" inside "מאומת במלואו" is already
CHECK 1's job. Run:  python test_banned_patterns.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "page_generator" / "copy"))

import copy_constants as C  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATTERNS = [(n, re.compile(rx)) for n, rx in C.get_banned_patterns()]


def fires(text: str) -> str | None:
    for name, rx in PATTERNS:
        if rx.search(text):
            return name
    return None


# Verbatim live strings that CHECK 1 passed. Each MUST now fire.
POSITIVE = [
    ("hard_cheeses_v4", "רשימת הרכיבים לא הגיעה מהסריקה, כך שהציון מבוסס על הנתונים התזונתיים בלבד."),
    ("hard_cheeses_v4", "רשימת הרכיבים לא הגיעה מהסריקה, כך שאי-אפשר לאמת את פרופיל התוספים."),
    ("hard_cheeses_v4", "השומן הגבוה (32%) ועדר נתוני רכיבים שמגביל את האמינות."),
    ("hard_cheeses_v4", "גאודה גוסטו 30%: 28 גרם חלבון, נתרן 680 מיליגרם, רשימת רכיבים שלא הגיעה מהסריקה."),
    ("cookies_coffee_v2", "שומן רווי נמוך, נתון הסוכר לא אומת."),
    ("paraphrase: מהימנות", "התוצאה מוגבלת בגלל מהימנות הנתונים."),
    ("paraphrase: לא ניתן", "לא ניתן לאמת את רשימת הרכיבים."),
    ("paraphrase: היעדר", "בהיעדר נתוני רכיבים הציון נשען על התזונה."),
    ("paraphrase: חסרים", "חסרים נתונים על התוספים."),
    ("paraphrase: לא נסרק", "המוצר לא נסרק במלואו."),
]

# Legitimate copy. NONE may fire.
NEGATIVE = [
    ("בהיעדר + non-data noun", "בהיעדר סוכר מוסף, המתיקות מגיעה מהפרי עצמו."),
    ("בהיעדר + additive", "בהיעדר תוספי מזון, רשימת הרכיבים קצרה."),
    ("plain nutrition", "הנתרן עומד על 491 מיליגרם ל-100 גרם, סביר ביחס לרוב הצהובות כאן."),
    ("real ingredient prose", "חלב, מלח, תרבית לקטית ומקריש."),
    ("owner-approved cereal", "95% מהמוצר הוא חיטה. הדגן הוא הסיפור כולו."),
    ("herd word, no data noun", "גבינת עדר מסורתית."),
    ("verified, positive", "החלבון הגבוה הוא מה שמייחד אותה."),
    ("scan-free sentence", "הסריקה של המדף מצאה 31 גבינות."),
]


def main() -> int:
    failures: list[str] = []

    print("must fire — live violations CHECK 1 passed with banned=0")
    for label, text in POSITIVE:
        name = fires(text)
        ok = name is not None
        print(f"  [{'ok  ' if ok else 'FAIL'}] {label:<26} {name or '(silent)':<24} {text[:40]}")
        if not ok:
            failures.append(f"{label}: expected fire, silent")

    print("\nmust stay silent — legitimate copy")
    for label, text in NEGATIVE:
        name = fires(text)
        ok = name is None
        print(f"  [{'ok  ' if ok else 'FAIL'}] {label:<26} {name or '(silent)':<24} {text[:40]}")
        if not ok:
            failures.append(f"{label}: expected silence, fired [{name}]")

    print()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print("  -", f)
        return 1
    print(f"all banned-pattern tests passed ({len(POSITIVE)} fire, {len(NEGATIVE)} silent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
