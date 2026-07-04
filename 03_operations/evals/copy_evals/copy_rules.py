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


# Ordered so deterministic rules surface first in reports.
RULES = [
    rule_sodium_term,
    rule_brand_spelling,
    rule_em_dash,
    rule_antithesis,
    rule_number_density,
]
