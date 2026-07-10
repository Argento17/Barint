#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
copy_rules.py — TASK-506 D3

Single source of truth for the Bari copy-conformance detectors. Extracted from
conformance_scan.py (TASK-506 D1) so BOTH consumers import the SAME rule
implementation instead of maintaining duplicate regexes:

  1. conformance_scan.py (D1)  — the reporting scanner. Runs every rule over
     every scanned line and reports ALL matches (including documented
     false-positive classes, e.g. "דיסודיום" / "גוג'י ברי") with a note, so the
     owner's manual rewrite pass can see and discount them. Uses the plain
     rule_* functions below exactly as before — no behavior change.

  2. integrations/clients/hebrew_readability.py (D3) — the copy sign-off GATE.
     Needs higher precision than the scanner: a hard defect must block the
     gate, but a known false-positive (a disodium-class additive name, the
     "goji berry" loanword) must NOT. The *_hard_* helpers below narrow each
     rule's raw matches to the gate-safe subset. The gate is the only consumer
     of the *_hard_* helpers; the scanner's own counts/behavior are untouched.

Rules:
  - sodium_term    (DETERMINISTIC)        "סודיום"/"סודים" instead of "נתרן"
  - brand_spelling (DETERMINISTIC-w/review) standalone "ברי" instead of "בארי"
  - em_dash        (count, minimize)       U+2014 "—"
  - antithesis     (owner ban)             "X, not Y" / "ו/אלא לא" framing
  - number_density (advisory heuristic)    >=4 nutrition figures restated in one line
  - grade_in_prose (owner ban, H4-P7)     the letter grade written into a sentence
  - ingredient_count (owner ban, H4-P2)   the NUMBER of ingredients narrated
  - stock_phrase   (owner ban, H4-P6)     "עושים את רוב העבודה" and kin

Cross-field (not a single-string rule, so not in RULES):
  - find_cross_field_value_repetition()   (owner ban, H4-P3) the same nutrition
    figure restated across two or more consumer fields of one product.

The H4-* rules were derived from the owner's verbatim review of 30 live rows on
2026-07-10 (TASK-576); see content_voice/tom_bari_voice/8_edit_feedback_log.md §H4.

TOOLING ONLY. This module contains no I/O — it never reads/writes any product
JSON, page-data.ts, or consumer copy. Pure functions over an input string.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# sodium_term
# ---------------------------------------------------------------------------

SODIUM_TERM_RE = re.compile(r"סודיום|סודים")

# Chemical/additive compound-name prefixes that turn "סודיום" into an
# ingredient name (e.g. "דיסודיום דיפוספט" / disodium diphosphate), NOT an
# editorial sodium-prose mention. Word-internal, no space (דיסודיום is one word).
_SODIUM_CHEM_PREFIXES = ("די", "מונו", "טרי")


def rule_sodium_term(text: str) -> dict | None:
    matches = SODIUM_TERM_RE.findall(text)
    if not matches:
        return None
    return {"rule": "sodium_term", "count": len(matches), "terms": sorted(set(matches))}


def _sodium_hit_is_chem_compound(text: str, match_start: int) -> bool:
    for prefix in _SODIUM_CHEM_PREFIXES:
        if text[max(0, match_start - len(prefix)):match_start] == prefix:
            return True
    return False


def sodium_term_hard_fires(text: str) -> bool:
    """Gate-safe check for the HARD leak kind: True iff at least one
    "סודיום"/"סודים" occurrence is genuine editorial sodium-prose (i.e. NOT
    the tail of a disodium/monosodium/trisodium-class additive compound name).
    Conservative in the safe direction — a chem-compound hit never fires."""
    for m in SODIUM_TERM_RE.finditer(text):
        if not _sodium_hit_is_chem_compound(text, m.start()):
            return True
    return False


# ---------------------------------------------------------------------------
# brand_spelling
# ---------------------------------------------------------------------------

# (?<![א-ת])ברי(?![א-ת]) — standalone "ברי", not part of a longer Hebrew word
# (e.g. excludes עברי, ברירה, ברים, בריא, מברי*, מוברי*).
BRAND_SPELLING_RE = re.compile(r"(?<![א-ת])ברי(?![א-ת])")

# Words immediately after/before a "ברי" hit that indicate a clear
# brand-as-grammatical-subject use ("Bari does/finds/chooses/does not...",
# "per/understanding/in Bari's view").
_BRAND_SUBJECT_FOLLOW = (
    "עובדת", "מצאה", "בוחרת", "לא", "מוצאת", "ממליצה", "בודקת",
    "משווה", "מדרגת", "מציגה", "מסבירה", "רואה", "מזהה", "מתעדפת",
)
_BRAND_SUBJECT_PRECEDE = ("לפי", "הבנת", "לדעת", "של", "מבחינת")

# The transliterated loanword "גוג'י ברי" (goji berry) — not the Bari brand token.
_BRAND_LOANWORD_PRECEDE = ("גוג'י", "גוגי")


def rule_brand_spelling(text: str) -> dict | None:
    hits = list(BRAND_SPELLING_RE.finditer(text))
    if not hits:
        return None
    detail_hits = []
    subject_use_count = 0
    for m in hits:
        start, end = m.span()
        before = text[:start].rstrip()
        after = text[end:].lstrip()
        next_word = re.split(r"[\s,.;:!?]+", after, maxsplit=1)[0] if after else ""
        prev_word = re.split(r"[\s,.;:!?]+", before[::-1], maxsplit=1)[0][::-1] if before else ""
        is_subject_use = next_word in _BRAND_SUBJECT_FOLLOW or prev_word in _BRAND_SUBJECT_PRECEDE
        if is_subject_use:
            subject_use_count += 1
        detail_hits.append({
            "context": text[max(0, start - 15):min(len(text), end + 15)],
            "brand_subject_use": is_subject_use,
        })
    return {
        "rule": "brand_spelling",
        "count": len(hits),
        "brand_subject_use_count": subject_use_count,
        "hits": detail_hits,
    }


def _is_goji_loanword(text: str, match_start: int) -> bool:
    before = text[:match_start]
    for w in _BRAND_LOANWORD_PRECEDE:
        idx = before.rfind(w)
        if idx != -1 and 0 <= (match_start - (idx + len(w))) <= 3:
            return True
    return False


def brand_spelling_hard_hits(text: str) -> list[dict]:
    """Gate-safe subset for the HARD leak kind: only standalone "ברי" hits that
    are (a) NOT the "גוג'י ברי" loanword, AND (b) clearly brand-as-subject use
    per the follow/precede heuristics. Conservative — an ambiguous standalone
    "ברי" that is neither loanword-adjacent nor clearly subject-use does NOT
    hard-fail (per spec: "if not clearly the brand acting as subject, do not
    hard-fail")."""
    out: list[dict] = []
    for m in BRAND_SPELLING_RE.finditer(text):
        start, end = m.span()
        if _is_goji_loanword(text, start):
            continue
        before = text[:start].rstrip()
        after = text[end:].lstrip()
        next_word = re.split(r"[\s,.;:!?]+", after, maxsplit=1)[0] if after else ""
        prev_word = re.split(r"[\s,.;:!?]+", before[::-1], maxsplit=1)[0][::-1] if before else ""
        if next_word in _BRAND_SUBJECT_FOLLOW or prev_word in _BRAND_SUBJECT_PRECEDE:
            out.append({"context": text[max(0, start - 15):min(len(text), end + 15)]})
    return out


# ---------------------------------------------------------------------------
# em_dash — advisory only, never hard-fails
# ---------------------------------------------------------------------------

EM_DASH_CHAR = "—"  # U+2014


def rule_em_dash(text: str) -> dict | None:
    n = text.count(EM_DASH_CHAR)
    if n == 0:
        return None
    return {"rule": "em_dash", "count": n}


# ---------------------------------------------------------------------------
# antithesis — owner ban on "X, not Y" define-by-negation. HARD.
# ---------------------------------------------------------------------------

# ",\s*לא\b" OR "\bולא\b" OR "\bאלא\b"
ANTITHESIS_RE = re.compile(r",\s*לא\b|\bולא\b|\bאלא\b")


def rule_antithesis(text: str) -> dict | None:
    matches = ANTITHESIS_RE.findall(text)
    if not matches:
        return None
    return {"rule": "antithesis", "count": len(matches)}


def antithesis_hard_fires(text: str) -> bool:
    """Gate-safe check for the HARD leak kind: True iff the antithesis pattern
    fires at all (no exclusion class defined for this rule — every match is a
    genuine define-by-negation instance per the owner ban)."""
    return ANTITHESIS_RE.search(text) is not None


# ---------------------------------------------------------------------------
# number_density — advisory heuristic, never hard-fails
# ---------------------------------------------------------------------------

# Nutrition-figure mentions: N + unit, calorie words, percent, per-100 marker.
_NUMBER_UNIT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:גרם|גר['’]|מ\"ג|מ״ג|קלוריות|קק\"ל|קק״ל|%)"
    r"|קלוריות|קק\"ל|קק״ל|ל-100"
)


def rule_number_density(text: str) -> dict | None:
    """Advisory heuristic — NOT a hard violation. Flags >=4 nutrition-figure
    mentions in a single copy line as "check for nutritional-value restatement"."""
    matches = _NUMBER_UNIT_RE.findall(text)
    n = len(matches)
    if n < 4:
        return None
    return {"rule": "number_density", "count": n, "advisory": True,
            "note": "check for nutritional-value restatement"}


# ---------------------------------------------------------------------------
# grade_in_prose — owner ban (H4-P7). The grade is the badge, never the sentence.
# ---------------------------------------------------------------------------

# Grade letters: S, A, B, C, D, E. These collide with vitamin letters, so every
# hit is checked against _VITAMIN_PRECEDE before it counts.
GRADE_IN_PROSE_RE = re.compile(
    r"(?:ב|ל)-[SABCDE](?![A-Za-z0-9])"          # "עוצר ב-B", "מוריד ל-E"
    r"|(?:ב?ציון|דירוג|בדירוג)\s+[SABCDE](?![A-Za-z0-9])"  # "ציון S.", "בציון B"
    r"|בין\s+[SABCDE]\s+ל-[SABCDE](?![A-Za-z0-9])"          # "בין C ל-E"
)

# A grade letter preceded by a vitamin word is a nutrient, not a grade
# ("עשיר ב-C"). Guard against the whole vitamin family; B12-style tokens are
# already excluded by the trailing (?![A-Za-z0-9]).
_VITAMIN_PRECEDE = ("ויטמין", "ויטמינים", "וויטמין")
_VITAMIN_LOOKBACK = 12


def _grade_hit_is_vitamin(text: str, match_start: int) -> bool:
    window = text[max(0, match_start - _VITAMIN_LOOKBACK):match_start]
    return any(w in window for w in _VITAMIN_PRECEDE)


def rule_grade_in_prose(text: str) -> dict | None:
    hits = [m for m in GRADE_IN_PROSE_RE.finditer(text)
            if not _grade_hit_is_vitamin(text, m.start())]
    if not hits:
        return None
    return {
        "rule": "grade_in_prose",
        "count": len(hits),
        "terms": sorted({m.group() for m in hits}),
    }


def grade_in_prose_hard_hits(text: str) -> list[dict]:
    """Gate-safe subset: every non-vitamin hit. The owner ban is absolute —
    consumer copy never writes the grade letter (and never writes "S" at all)."""
    return [
        {"context": text[max(0, m.start() - 20):m.end() + 20], "match": m.group()}
        for m in GRADE_IN_PROSE_RE.finditer(text)
        if not _grade_hit_is_vitamin(text, m.start())
    ]


# ---------------------------------------------------------------------------
# ingredient_count — owner ban (H4-P2): "אני לא רוצה לראות את זה כתוב."
# ---------------------------------------------------------------------------

# Spelled-out counts, longest-first so the alternation cannot truncate
# "אחד עשר" into "אחד". Mirrors copy_constants._SPELLED_INGREDIENT_COUNTS.
_SPELLED_COUNTS = (
    "שנים עשר|שלושה עשר|ארבעה עשר|חמישה עשר|שישה עשר|אחד עשר|"
    "שני|שתי|שלושה|שלוש|ארבעה|ארבע|חמישה|חמש|שישה|שש|שבעה|שבע|"
    "שמונה|תשעה|תשע|עשרה|עשר"
)

# A count (digit or spelled) immediately governing "רכיבים"/"מרכיבים",
# optionally through one modifier ("שלושה רכיבים בלבד", "5 רכיבים בסך הכל").
INGREDIENT_COUNT_RE = re.compile(
    rf"(?:\d+|{_SPELLED_COUNTS})\s+(?:רכיבים|מרכיבים)"
)


def rule_ingredient_count(text: str) -> dict | None:
    hits = list(INGREDIENT_COUNT_RE.finditer(text))
    if not hits:
        return None
    return {"rule": "ingredient_count", "count": len(hits),
            "terms": sorted({m.group() for m in hits})}


def ingredient_count_hard_fires(text: str) -> bool:
    """Gate-safe check. No exclusion class: the owner banned narrating the
    ingredient COUNT outright. Showing the ingredient list is still fine."""
    return INGREDIENT_COUNT_RE.search(text) is not None


# ---------------------------------------------------------------------------
# stock_phrase — owner ban (H4-P6): vague, "לא תמיד ברור למה מתכוונים".
# ---------------------------------------------------------------------------

STOCK_PHRASE_RE = re.compile(r"עוש(?:ים|ה|ות)\s+(?:כאן\s+)?את\s+(?:רוב\s+)?העבודה")


def rule_stock_phrase(text: str) -> dict | None:
    hits = STOCK_PHRASE_RE.findall(text)
    if not hits:
        return None
    return {"rule": "stock_phrase", "count": len(hits)}


def stock_phrase_hard_fires(text: str) -> bool:
    return STOCK_PHRASE_RE.search(text) is not None


# ---------------------------------------------------------------------------
# cross_field_value_repetition — owner ban (H4-P3). NOT a single-string rule:
# it needs every consumer field of one product at once.
# ---------------------------------------------------------------------------

# A nutrition figure = number + a mass/energy/percent unit. The unit is REQUIRED:
# a bare "100%" in "100% קמח חיטה" is a composition claim, not a nutrition value,
# and counting it inflated an early measurement of this rule from 34% to 57%.
#
# "מיליגרם" (sodium spelled in full) MUST precede "גרם" in the alternation, and
# the whole-word variants must be listed, or the engine matches "גרם" inside
# "מיליגרם" and captures the wrong token. This gap was live: the QA sign-off on
# the TASK-576 data-state drafts (2026-07-10) found 4 products repeating the
# sodium figure across insightLine+rowVerdict that this rule reported CLEAN,
# because the drafts wrote "660 מיליגרם" and the old pattern missed it entirely
# (and mis-captured the "ל-100 גרם" framing instead). Detector-blindness is the
# same failure class the whole gate program exists to kill — fixed + tested here.
NUTRITION_VALUE_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:מיליגרם|מיליגר['’]|גרם|גר['’]|מ\"ג|מ״ג|מג|קלוריות|קק\"ל|קק״ל)"
)

# Per-100g serving framing ("ל-100 גרם") is boilerplate every row shares — it is a
# UNIT, not a product-specific value, so its repetition across fields is never the
# H4-P3 defect. Strip it before scanning so it cannot false-positive.
_PER_100G_RE = re.compile(r"ל-?\s*100\s*גרם")


def _normalize_value(token: str) -> str:
    """Collapse spacing and unit spelling so '5 גרם' and '5גרם' are one value,
    and '660 מיליגרם' / '660 מ"ג' land on the same normalized key."""
    t = re.sub(r"\s+", "", token)
    t = (t.replace("מ״ג", 'מ"ג').replace("קק״ל", 'קק"ל').replace("גר’", "גר'")
          .replace("מיליגרם", 'מ"ג').replace("מיליגר'", 'מ"ג').replace("מיליגר’", 'מ"ג'))
    return t


def find_cross_field_value_repetition(fields: dict[str, str]) -> list[dict]:
    """Return one entry per nutrition figure that appears in >= 2 DISTINCT
    consumer fields of the same product.

    `fields` maps field name -> prose. Repetition WITHIN one field is a
    different defect (see rule_number_density) and is not reported here.
    """
    seen: dict[str, set[str]] = {}
    for fname, text in fields.items():
        if not isinstance(text, str) or not text.strip():
            continue
        text = _PER_100G_RE.sub(" ", text)  # drop the shared serving framing first
        for tok in NUTRITION_VALUE_RE.findall(text):
            seen.setdefault(_normalize_value(tok), set()).add(fname)
    return [
        {"rule": "cross_field_value_repetition", "value": val,
         "fields": sorted(where), "field_count": len(where)}
        for val, where in sorted(seen.items())
        if len(where) >= 2
    ]


# Ordered so deterministic rules surface first in reports.
RULES = [
    rule_sodium_term,
    rule_brand_spelling,
    rule_em_dash,
    rule_antithesis,
    rule_number_density,
    rule_grade_in_prose,
    rule_ingredient_count,
    rule_stock_phrase,
]
