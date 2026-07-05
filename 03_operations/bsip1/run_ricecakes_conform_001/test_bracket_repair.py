"""
TASK-517 — Reversed-bracket-nesting repair — Test Harness
Pins the repair to the exact confirmed real-world string (barcode 4267230,
Shufersal raw HTML source: 03_operations/bsip0/raw_store/shufersal/
ricecakes/P_4267230/20260705T055346868812.html, line 2790) plus negative
controls proving the detector never fires on ordinary bracketed text.
Run with: python test_bracket_repair.py
"""
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_ricecakes_bsip1 import detect_reversed_brackets, normalize_reversed_brackets  # noqa: E402

PASS = "PASS"
FAIL = "FAIL"
_results: list[tuple[str, str]] = []


def check(name: str, condition: bool):
    status = PASS if condition else FAIL
    _results.append((status, name))
    marker = "+" if condition else "X"
    print(f"  [{marker}] {name}")


# ── Real-world pinned case: barcode 4267230 verbatim raw scrape text ──────
# (post bleed-clean, pre-repair; exact string as extracted from BSIP0)
RAW_4267230 = (
    "פריכיות אורז)אורז חום,מלח(,ציפוי בטעם שוקולד}מכיל:סוכר,שמנים ושומנים "
    "מהצומח)מוקשים חלקית(אבקת קקאו,מתחלב:לציטין סויה)(E-322,חומרי טע     "
    "ם וריח{"
)

# Coherent, correctly-nested Hebrew text that the repair must reproduce
# exactly. This is a PURE position-preserving character swap of the raw
# string above -- '('<->')' and '{'<->'}' only, no reordering. The raw
# string has adjacent ")(" immediately before "E-322" (no characters
# between them), so the swap correctly yields an adjacent empty "()"
# in the same spot in the output (the swap must never reorder characters
# to "tidy up" the result -- doing so would be fabricating structure, not
# repairing an encoding artifact).
EXPECTED_REPAIRED_4267230 = (
    "פריכיות אורז(אורז חום,מלח),ציפוי בטעם שוקולד{מכיל:סוכר,שמנים ושומנים "
    "מהצומח(מוקשים חלקית)אבקת קקאו,מתחלב:לציטין סויה()E-322,חומרי טע     "
    "ם וריח}"
)

print("TASK-517 bracket-repair pinned test:\n")

check(
    "detect_reversed_brackets(RAW_4267230) == True (signature confirmed present)",
    detect_reversed_brackets(RAW_4267230) is True,
)

repaired = normalize_reversed_brackets(RAW_4267230)
check(
    "normalize_reversed_brackets(RAW_4267230) == EXPECTED_REPAIRED_4267230 (exact pin)",
    repaired == EXPECTED_REPAIRED_4267230,
)


def _bracket_balance_ok(text: str) -> bool:
    """True iff every close has a matching, correctly-ordered open (i.e.
    the repaired text is NOT itself flagged by the same detector)."""
    return not detect_reversed_brackets(text)


check(
    "repaired text is no longer flagged by the detector (balanced, correct nesting)",
    _bracket_balance_ok(repaired),
)

# ── Negative controls: the detector must NOT fire on ordinary text ────────
NORMAL_CASES = [
    "פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן), סוכר לבן",
    "כוסמת (99.5%), מלח",
    "אבקת קקאו, מתחלב: לציטין סויה (E-322)",
    "מוצר ללא סוגריים כלל",
    "",
    None,
]
for i, case in enumerate(NORMAL_CASES):
    check(
        f"detect_reversed_brackets() == False on ordinary case #{i} ({case!r})",
        detect_reversed_brackets(case) is False,
    )

# Idempotency / no-op guard: repair must be a pure function of the flagged
# string only -- applying normalize_reversed_brackets() to an UNFLAGGED
# ordinary string would corrupt it, which is exactly why the pipeline only
# ever calls it behind the detector gate (repair_reversed_brackets()), never
# as a blanket transform. This test documents that hazard explicitly.
check(
    "normalize_reversed_brackets() on a normal (unflagged) string would NOT be a no-op "
    "(proves the gate in repair_reversed_brackets() is load-bearing, not decorative)",
    normalize_reversed_brackets(NORMAL_CASES[0]) != NORMAL_CASES[0],
)

failed = [r for r in _results if r[0] == FAIL]
print(f"\n{len(_results) - len(failed)}/{len(_results)} checks passed.")
if failed:
    print("FAILURES:")
    for status, name in failed:
        print(f"  - {name}")
    sys.exit(1)
sys.exit(0)
