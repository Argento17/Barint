#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wording_check.py — shared lexical unsafe-wording checker (D3b)
TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1

Precise, no-LLM scan used by both the schema-validation and pairwise gates.
- ABSOLUTE banned phrases  -> violation on any occurrence.
- NEEDS_REFERENCE phrases   -> violation ONLY if no digit within ref_window chars
                              after the phrase (the compliant form pairs it with a number).
- framework_terms (Latin)   -> word-boundary, case-insensitive.
- apology_markers (Hebrew)  -> substring.
Returns a list of (phrase, kind) violations.
"""
import re
from pathlib import Path
import yaml

_LEX = None


def load_lexicon(path=None):
    global _LEX
    if _LEX is None:
        p = Path(path) if path else (Path(__file__).resolve().parent / "config" / "unsafe_wording_lexicon_v1.yaml")
        _LEX = yaml.safe_load(p.read_text(encoding="utf-8"))
    return _LEX


def scan_text(text, lex=None):
    if not isinstance(text, str) or not text:
        return []
    lex = lex or load_lexicon()
    out = []
    window = int(lex.get("ref_window", 20))

    for phrase in lex.get("banned_phrases_absolute", []):
        if phrase in text:
            out.append((phrase, "absolute"))

    for phrase in lex.get("banned_phrases_needs_reference", []):
        start = 0
        while True:
            i = text.find(phrase, start)
            if i < 0:
                break
            after = text[i + len(phrase): i + len(phrase) + window]
            if not re.search(r"\d", after):
                out.append((phrase, "needs_reference_unreferenced"))
            start = i + len(phrase)

    for term in lex.get("framework_terms", []):
        if re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.IGNORECASE):
            out.append((term, "framework_term"))

    for marker in lex.get("apology_markers", []):
        if marker in text:
            out.append((marker, "apology"))

    return out
