"""
Hebrew-aware text matching with negation handling.
"""
import re
from typing import List
from bsip2_config import HEBREW_NEGATION_PREFIXES, ENGLISH_NEGATION_PREFIXES

HEBREW_PREFIX_LETTERS = "בהלמשו"


def normalize(text: str) -> str:
    if not text:
        return ""
    t = text.replace("\u200f", " ").replace("\u200e", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _has_hebrew(s: str) -> bool:
    return any("\u0590" <= ch <= "\u05FF" for ch in s)


# Characters that act as word boundaries in Hebrew/English mixed text
_BOUNDARY_CHARS = set(" ,;.-()[]{}\t\n\"'")


def _is_boundary(text: str, pos: int) -> bool:
    """A position is a word boundary if it's at the start/end or next to a boundary char."""
    if pos < 0 or pos >= len(text):
        return True
    return text[pos] in _BOUNDARY_CHARS


def _find_term(text: str, term: str) -> List[int]:
    """Find all start positions where `term` occurs as a whole word."""
    matches = []
    text_lower = text.lower() if not _has_hebrew(term) else text
    term_lower = term.lower() if not _has_hebrew(term) else term

    start = 0
    while True:
        idx = text_lower.find(term_lower, start)
        if idx == -1:
            # Try with optional Hebrew prefix letter
            if _has_hebrew(term):
                for prefix in HEBREW_PREFIX_LETTERS:
                    prefixed = prefix + term_lower
                    pidx = text_lower.find(prefixed, start)
                    if pidx != -1:
                        if _is_boundary(text, pidx - 1) and _is_boundary(text, pidx + len(prefixed)):
                            matches.append(pidx)
            break

        # Check word boundaries
        before_ok = _is_boundary(text, idx - 1)
        after_ok = _is_boundary(text, idx + len(term_lower))
        if before_ok and after_ok:
            matches.append(idx)
        start = idx + 1

    return matches


def _is_negated(text: str, match_start: int) -> bool:
    """
    Check if a match is preceded by a negation phrase WITHIN THE SAME CLAUSE.
    A clause ends at ',' ';' '.' or paragraph break.
    """
    # Walk backwards from match_start, but stop at a clause separator
    window_start = max(0, match_start - 25)
    window = text[window_start:match_start]

    # Find the last clause separator in the window
    last_sep = max(window.rfind(","), window.rfind(";"), window.rfind("."))
    if last_sep != -1:
        # Only consider the part AFTER the last separator
        window = window[last_sep + 1:]

    window_lower = window.lower()
    for neg in HEBREW_NEGATION_PREFIXES + ENGLISH_NEGATION_PREFIXES:
        if neg.lower() in window_lower:
            return True
    return False


def contains_term(text: str, term: str) -> bool:
    if not text or not term:
        return False
    text_norm = normalize(text)
    positions = _find_term(text_norm, term)
    for pos in positions:
        if not _is_negated(text_norm, pos):
            return True
    return False


def contains_any(text: str, terms: List[str]) -> bool:
    return any(contains_term(text, t) for t in terms)


def count_terms(text: str, terms: List[str]) -> int:
    return sum(1 for t in terms if contains_term(text, t))