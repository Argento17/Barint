# -*- coding: utf-8 -*-
"""
ingredient_quality_gate.py  — TASK-129A (P0 confidence-gate fix, reference impl)
================================================================================
Corrected `verified` data-sufficiency gate for the launch shelves.

Background (audit: 03_operations/bsip2/confidence_reaudit_launch_v1.md, P0 #1):
the Launch-Definition §5 gate is *presence-based* —

    verified  ⇐  (≥3/6 nutrition fields filled)  AND  bool(ingredients_text)

so any non-empty string in the ingredient field earns `verified`, even when the
field actually contains a scraped nutrition table, marketing prose, or an
allergen/handling sentence rather than a real ingredient list. Examples found in
the shipping corpora:

  • hummus "חומוס גדול שופרסל" (85/A, verified): ingredients =
    "גרגירי חומוס ערכים תזונתיים 100 גרם 17.4 גרם סיבים..." — one ingredient word
    followed by the whole nutrition panel; positiveSignals then quote those
    bled-in numbers.
  • maadanim "מעדן חלבון בטעם וניל" (54/C, verified): real list with an allergen
    prose tail ("...מכיל חלב עלול להכיל...").

This module adds the missing *quality* check. It is a PURE function with no I/O
and is NOT yet wired into any build script — integration is Phase 2/3 of the
TASK-129A plan (each category's build_*.py and the §5 spec). Import and call:

    from ingredient_quality_gate import assess_ingredients, gate_confidence

    verdict = assess_ingredients(ingredients_text)
    conf    = gate_confidence(nutrition_fields_filled, ingredients_text)

`verdict.is_real_list` is False when the field is prose/bled/empty; in that case
the consumer must (a) downgrade `verified` → `partial`, and (b) suppress any
ingredient-derived positive signal (additive-free / NOVA / sweetener claims),
because those signals were computed from non-ingredient text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# ── detector vocabulary ───────────────────────────────────────────────────────
# Calibration note (TASK-129A): tokens are deliberately narrow. A first cut used
# broad tokens and false-flagged ~80% of genuine lists; a second cut still tripped
# on words that legitimately appear *inside* real Hebrew lists or in footnotes —
# "סיבים תזונתיים" (dietary fiber, an ingredient), "ל-100 גרם" (a per-100g vitamin
# note), "מיחזור"/"מתכון"/"האריזה" (packaging / Passover footnotes appended after a
# real list). Those are NOT bleed/prose markers; they are handled by tail-stripping
# (strip the trailing footnote, then judge the head) instead of rejecting the row.

# Promo / marketing prose — phrases that only occur in copy, never as an ingredient.
PROMO_TOKENS = (
    "מסייע", "חשוב בתזונה", "עשיר בחלבון", "מומלץ על", "אורח חיים בריא",
    "מתאים לכל המשפחה", "להנות מ", "ליהנות מ",
)

# STRICT nutrition-panel phrases (panel-only; never an ingredient name).
PANEL_TOKENS = (
    "ערכים תזונתיים", "קל אנרגיה", "מתוך פחמימות", "מג נתרן",
    "ערך אנרגטי", "מתוכן חומצות שומן",
)

# Tail markers: a real list often has a footnote/packaging/allergen tail appended.
# Cut at the earliest of these (when well into the string) and judge the HEAD.
TAIL_MARKERS = (
    "מאפיינים נוספים", "ניתן למיחזור", "ניתנת למיחזור", "יש לשמור", "בתנאי קירור",
    "לאחר הפתיחה", "לאחר פתיחה", "תאריך אחרון", "בתקופת פסח", "עלול להכיל", "מכיל ",
)

# Allergen / handling sentence tails (used only to label a head that is itself a tail).
HANDLING_TOKENS = ("עלול להכיל", "יש לשמור", "בתנאי קירור", "לאחר הפתיחה", "תאריך אחרון")

_DIGIT_RE = re.compile(r"\d")
# A real ingredient list is comma/paren separated tokens; prose is long & flat.
_LIST_SEP_RE = re.compile(r"[,\(\)\[\]{}•·]")


def _strip_tail(text: str) -> str:
    """Cut a trailing footnote/packaging/allergen tail, keeping the ingredient head.
    Only cuts when the marker is >20 chars in, so a list isn't truncated to nothing."""
    cut = len(text)
    for m in TAIL_MARKERS:
        i = text.find(m)
        if i > 20:
            cut = min(cut, i)
    return text[:cut].strip().rstrip(".,*• ")


@dataclass(frozen=True)
class IngredientVerdict:
    is_real_list: bool
    reason: str          # "" when ok; machine-readable code otherwise
    detail: str          # human note for the audit trail


def _digit_density(text: str) -> float:
    if not text:
        return 0.0
    return len(_DIGIT_RE.findall(text)) / len(text)


def _token_count(text: str) -> int:
    # number of separated chunks — a list has several, prose has ~1
    return len([t for t in _LIST_SEP_RE.split(text) if t.strip()])


def assess_ingredients(text: str | None) -> IngredientVerdict:
    """Classify whether `text` is a genuine ingredient list.

    Order matters: nutrition-bleed and emptiness are hard failures; promo prose
    and long-flat-prose are heuristic failures.
    """
    if not text or not text.strip():
        return IngredientVerdict(False, "empty", "no ingredient text")

    raw = text.strip()

    # (1) nutrition-table bleed — most common shipping defect (hummus 85/A rows).
    #     Strict panel phrases + high digit density. Evaluated on RAW because the
    #     panel can bleed in anywhere.
    panel_hits = [tok for tok in PANEL_TOKENS if tok in raw]
    if panel_hits and _digit_density(raw) >= 0.045:
        return IngredientVerdict(False, "nutrition_bleed",
                                 f"nutrition-panel text in ingredient field: {panel_hits}")

    # (2) strip a trailing footnote/packaging/allergen tail, then judge the head.
    head = _strip_tail(raw)
    if not head:
        return IngredientVerdict(False, "handling_only",
                                 "allergen/handling/footnote only, no ingredient list")

    # (3) explicit promo / marketing prose in the head.
    promo_hits = [tok for tok in PROMO_TOKENS if tok in head]
    if promo_hits:
        return IngredientVerdict(False, "marketing_prose",
                                 f"promo tokens present: {promo_hits}")

    # (4) long flat prose with almost no list structure.
    if len(head) > 200 and _token_count(head) <= 3:
        return IngredientVerdict(False, "long_prose",
                                 f"{len(head)} chars but only {_token_count(head)} list tokens")

    return IngredientVerdict(True, "", "real ingredient list")


def gate_confidence(nutrition_fields_filled: int, ingredients_text: str | None) -> str:
    """Corrected §5 gate. Returns 'verified' | 'partial' | 'insufficient'.

    verified  ⇐  ≥3/6 nutrition fields  AND  ingredient field is a REAL list.
    partial   ⇐  some data present but quality/quantity below the verified bar.
    insufficient ⇐ effectively no usable data.
    """
    has_real_list = assess_ingredients(ingredients_text).is_real_list
    if nutrition_fields_filled >= 3 and has_real_list:
        return "verified"
    if nutrition_fields_filled >= 1 or has_real_list:
        return "partial"
    return "insufficient"


# ── self-test (run: python ingredient_quality_gate.py) ────────────────────────
def _selftest() -> None:
    REAL = [
        "חלב, חלבוני חלב (7.4%), אבקת חלב",
        "חומוס גרגירים (34%), טחינה גולמית, מים, מיץ לימון, שום, מלח",
        "שמנת, חלב, מים, סוכר, מייצבים (E1442 E407), קוקוס, פיסטוק",
        # real list + per-100g vitamin note + Passover footnote + allergen tail (was a false positive)
        "יוגורט 2.3% שומן (87.1%), מים, סיבים תזונתיים, מחיות פרי (1.6%), סוכר, "
        "ויטמינים (A, D ל-100 גרם). *בתקופת פסח- המתכון ללא ויטמין A. "
        "מאפיינים נוספים ניתן למיחזור מכיל חלב",
    ]
    BAD = {
        "nutrition_bleed":
            "גרגירי חומוס ערכים תזונתיים 100 גרם 17.4 גרם סיבים תזונתיים 10.7 גרם "
            "סוכרים מתוך פחמימות 339 קל אנרגיה 19.3 גרם חלבונים 43.2 גרם פחמימות",
        "marketing_prose":
            "מוצר עשיר בחלבון המסייע לאורח חיים בריא, מומלץ על ידי תזונאים",
        "empty": "",
    }
    ok = True
    for s in REAL:
        v = assess_ingredients(s)
        flag = "PASS" if v.is_real_list else "FAIL"
        if not v.is_real_list:
            ok = False
        print(f"[{flag}] real-list expected real  -> {v.reason or 'real'}")
    for expect, s in BAD.items():
        v = assess_ingredients(s)
        flag = "PASS" if (not v.is_real_list and v.reason == expect) else "FAIL"
        if v.is_real_list or v.reason != expect:
            ok = False
        print(f"[{flag}] bad expected {expect!r:18} -> got {v.reason!r}")
    # gate behaviour
    assert gate_confidence(5, "חלב, סוכר, מלח") == "verified"
    assert gate_confidence(5, BAD["nutrition_bleed"]) == "partial"   # was 'verified'
    assert gate_confidence(0, "") == "insufficient"
    print("gate transitions OK" if ok else "SELFTEST FAILED")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    _selftest()
