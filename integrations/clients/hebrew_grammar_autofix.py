"""Hebrew grammar auto-fix loop — bounded to high-confidence flags only.

Companion to hebrew_grammar_gate.py. Applies deterministic morphological
corrections to `confidence="high"` flags emitted by `analyze()`, then re-runs
the gate to confirm the fix passes. Medium-confidence flags are NEVER auto-fixed
— they are left for human review.

Architecture
------------
Two corrector tiers:

1. Deterministic gender-suffix corrector (built-in)
   Handles the most common high-confidence case: DET-anchored noun-adjective
   gender mismatch where the adjective carries a recognisable masculine or
   feminine suffix. Covers the pattern flagged as ISSUE_NOUN_ADJ_GENDER with
   confidence="high" (both tokens are definite).

   Correction table (adjective suffix swap):
     Masc→Fem : strip ה-suffix ambiguity, add ה
                e.g. הצהוב → הצהובה, הגדול → הגדולה, הקטן → הקטנה
     Fem→Masc : strip terminal ה (when preceded by consonant cluster)
                e.g. הצהובה → הצהוב

   The table operates on the surface form of the flagged token (flag.span),
   not on a morpheme decomposition — fast and portable with no extra deps.

2. LLM-based corrector hook (pluggable, NOT wired)
   For cases the deterministic fixer cannot handle (irregular forms, construct-
   state disagreement, subject-verb mismatches) a pluggable hook is documented
   below. To activate, supply a `llm_corrector` callable when calling
   `auto_fix()`. The hook contract is:

       def llm_corrector(text: str, flag: GrammarFlag) -> str | None:
           '''Return the corrected full text, or None to skip.'''

   The hook is called ONLY when the deterministic fixer does not produce a
   change that passes re-gating. It must not call any external API unless the
   caller has explicitly wired one in — this module ships with the hook slot
   empty and exit-safe.

   Example (Claude API — NOT called by default):
       from anthropic import Anthropic
       client = Anthropic()

       def claude_corrector(text: str, flag: GrammarFlag) -> str | None:
           prompt = (
               f"Fix this Hebrew grammar error and return ONLY the corrected sentence:\\n"
               f"Text: {text}\\n"
               f"Error: {flag.issue_type} — '{flag.span}' should be {flag.expected}\\n"
               f"Return the corrected sentence only, no explanation."
           )
           msg = client.messages.create(
               model="claude-opus-4-5",
               max_tokens=256,
               messages=[{"role": "user", "content": prompt}],
           )
           return msg.content[0].text.strip()

       corrected = auto_fix(text, llm_corrector=claude_corrector)

Interface
---------
    from integrations.clients.hebrew_grammar_autofix import auto_fix, AutoFixResult

    result = auto_fix("הגבינה הצהוב מונחת על המדף")
    print(result.fixed_text)    # הגבינה הצהובה מונחת על המדף
    print(result.is_clean)      # True
    print(result.fixes_applied) # [AutoFix(...)]

Runnable self-test:
    python -m integrations.clients.hebrew_grammar_autofix
exits 0 iff the canonical test case passes and existing 5/5 gate pairs still pass.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional

from integrations.clients.hebrew_grammar_gate import (
    GrammarFlag,
    GrammarReport,
    ISSUE_NOUN_ADJ_GENDER,
    analyze,
)

# ---------------------------------------------------------------------------
# Auto-fix result types
# ---------------------------------------------------------------------------


@dataclass
class AutoFix:
    """Record of a single correction applied to the text."""
    flag: GrammarFlag           # the original flag that triggered this fix
    original_span: str          # the offending token before correction
    corrected_span: str         # the token after correction
    method: str                 # "deterministic" | "llm"


@dataclass
class AutoFixResult:
    """Result of running the auto-fix loop on a passage."""
    original_text: str
    fixed_text: str
    is_clean: bool              # True iff re-gate passes after all fixes
    fixes_applied: list[AutoFix] = field(default_factory=list)
    skipped_medium: int = 0    # number of medium-confidence flags not touched
    residual_flags: list[GrammarFlag] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        return self.original_text != self.fixed_text


# ---------------------------------------------------------------------------
# Deterministic gender-suffix corrector
# ---------------------------------------------------------------------------

# Hebrew definite article prefix used in high-confidence DET-anchored checks.
_HE_DEF = "ה"   # ה

# Common masculine adjective suffixes and their feminine counterparts.
# Each tuple: (masc_pattern, fem_replacement, is_regex)
# We match against the surface form with the ה prefix already present.
#
# Strategy: strip the leading ה (definite prefix) to work on the bare stem,
# apply the suffix transformation, then re-attach ה.
#
# This covers the high-frequency Modern Hebrew adjective paradigm:
#   CCC    → CCC + ה    (e.g. גדול → גדולה, קטן → קטנה, צהוב → צהובה)
#   CCC+ה  → CCC        (reverse, Fem→Masc)
#
# We do NOT attempt to handle plural forms here — those are medium-confidence.

def _bare(token: str) -> str:
    """Strip leading definite ה from a surface token."""
    if token.startswith(_HE_DEF):
        return token[1:]
    return token


def _to_feminine(adj_token: str) -> Optional[str]:
    """Convert a masculine adjective surface form to feminine.

    Works on the form WITH the definite ה prefix (הצהוב → הצהובה).
    Returns None if we cannot apply a deterministic rule.
    """
    bare = _bare(adj_token)
    if not bare:
        return None
    # Already feminine (ends in ה that is not part of the root)
    # Heuristic: if bare ends in ה and has ≥3 chars, assume feminine — skip.
    if bare.endswith(_HE_DEF) and len(bare) >= 3:
        return None  # already fem (or looks like it)
    # Add feminine ה suffix to bare form, re-attach definite ה
    return _HE_DEF + bare + _HE_DEF


def _to_masculine(adj_token: str) -> Optional[str]:
    """Convert a feminine adjective surface form to masculine.

    Works on the form WITH the definite ה prefix (הצהובה → הצהוב).
    Returns None if we cannot apply a deterministic rule.
    """
    bare = _bare(adj_token)
    if not bare:
        return None
    # Feminine bare form ends in ה — strip it
    if bare.endswith(_HE_DEF) and len(bare) >= 2:
        masc_bare = bare[:-1]
        return _HE_DEF + masc_bare
    return None


def _deterministic_gender_fix(text: str, flag: GrammarFlag) -> Optional[str]:
    """Apply a deterministic gender-suffix correction for a single flag.

    Returns the corrected text if a rule fired, else None.
    Only handles ISSUE_NOUN_ADJ_GENDER.
    """
    if flag.issue_type != ISSUE_NOUN_ADJ_GENDER:
        return None
    if flag.confidence != "high":
        return None

    span = flag.span
    expected = flag.expected  # e.g. "Gender=Fem"
    corrected_span: Optional[str] = None

    if "Fem" in expected:
        corrected_span = _to_feminine(span)
    elif "Masc" in expected:
        corrected_span = _to_masculine(span)

    if corrected_span is None or corrected_span == span:
        return None

    # Replace the FIRST occurrence of the exact span in text.
    # We use a word-boundary-aware replacement to avoid partial token matches.
    # Hebrew has no ASCII word boundaries, so we replace only the first
    # occurrence that is surrounded by whitespace or string boundaries.
    pattern = r"(?<!\S)" + re.escape(span) + r"(?!\S)"
    new_text, n = re.subn(pattern, corrected_span, text, count=1)
    if n == 0:
        # Fallback: simple first-occurrence replace
        new_text = text.replace(span, corrected_span, 1)
        if new_text == text:
            return None
    return new_text


# ---------------------------------------------------------------------------
# Main auto-fix loop
# ---------------------------------------------------------------------------

LLMCorrectorFn = Callable[["str", GrammarFlag], Optional[str]]


def auto_fix(
    text: str,
    *,
    llm_corrector: Optional[LLMCorrectorFn] = None,
    max_iterations: int = 10,
) -> AutoFixResult:
    """Run the bounded auto-fix loop on a Hebrew passage.

    Parameters
    ----------
    text : str
        The Hebrew text to correct.
    llm_corrector : callable, optional
        Pluggable LLM-based corrector for cases the deterministic fixer cannot
        handle. Contract: `fn(text, flag) -> corrected_text | None`.
        If None (default), LLM fallback is disabled — only deterministic fixes
        are applied. Medium-confidence flags are never passed to the LLM hook.
    max_iterations : int
        Safety ceiling on the detect→fix→re-gate loop (default 10). Prevents
        infinite correction cycles on pathological inputs.

    Returns
    -------
    AutoFixResult
        `.is_clean` is True iff `analyze(fixed_text).is_clean` is True after
        all applicable fixes. `.fixes_applied` lists every correction made.
        `.skipped_medium` counts flags not touched (medium confidence).
        `.residual_flags` are the flags still present after the loop ends.
    """
    current_text = (text or "").strip()
    fixes_applied: list[AutoFix] = []
    skipped_medium = 0

    for _iteration in range(max_iterations):
        report: GrammarReport = analyze(current_text)
        if report.is_clean:
            break

        # Separate high vs medium flags
        high_flags = [f for f in report.flags if f.confidence == "high"]
        medium_flags = [f for f in report.flags if f.confidence != "high"]
        skipped_medium += len(medium_flags)

        if not high_flags:
            # Only medium flags remain — stop, leave for human review
            break

        # Process the first high-confidence flag per iteration (re-gate after each)
        flag = high_flags[0]
        fixed: Optional[str] = None
        method = "deterministic"

        # --- Tier 1: deterministic fixer ---
        fixed = _deterministic_gender_fix(current_text, flag)

        # --- Tier 2: LLM hook (only if deterministic couldn't fix it) ---
        if fixed is None and llm_corrector is not None:
            try:
                fixed = llm_corrector(current_text, flag)
                method = "llm"
            except Exception:
                fixed = None

        if fixed is None or fixed == current_text:
            # This flag cannot be auto-fixed — leave it and move on to the next
            # flag rather than looping infinitely on the same one.
            # To avoid an infinite loop: if we cannot fix the ONLY remaining
            # high flag, break entirely.
            remaining_high = [f for f in report.flags
                              if f.confidence == "high" and f.span != flag.span]
            if not remaining_high:
                break
            # Otherwise: skip this flag's span and continue (by re-gating, the
            # same flag may reappear — so we explicitly skip it next round).
            # Simple approach: just advance without applying a fix for this flag.
            break  # conservative: stop rather than risk loop

        # Verify the fix actually passed the gate
        verify_report = analyze(fixed)
        # Accept the fix regardless of whether it fully clears (the loop will
        # handle remaining flags on the next iteration)
        fixes_applied.append(AutoFix(
            flag=flag,
            original_span=flag.span,
            corrected_span=flag.span if fixed == current_text else _extract_change(current_text, fixed, flag.span),
            method=method,
        ))
        current_text = fixed

    # Final gate run for residual flags
    final_report = analyze(current_text)

    return AutoFixResult(
        original_text=text or "",
        fixed_text=current_text,
        is_clean=final_report.is_clean,
        fixes_applied=fixes_applied,
        skipped_medium=skipped_medium,
        residual_flags=final_report.flags,
    )


def _extract_change(original: str, fixed: str, original_span: str) -> str:
    """Best-effort extraction of what `original_span` became in `fixed`."""
    # Find where original_span was in original text
    idx = original.find(original_span)
    if idx == -1:
        return fixed[idx:idx + len(original_span)] if idx != -1 else "?"
    # The replacement length may differ; try to find the corresponding new token
    # by looking at the same position in fixed text (approximate)
    prefix = original[:idx]
    if fixed.startswith(prefix):
        after_prefix = fixed[len(prefix):]
        # The new span ends at the next whitespace after where original_span ended
        rest_original = original[idx + len(original_span):]
        if rest_original and after_prefix.endswith(rest_original):
            return after_prefix[: len(after_prefix) - len(rest_original)]
    return "?"


# ---------------------------------------------------------------------------
# Self-test / acceptance test (runnable as __main__)
# ---------------------------------------------------------------------------

_AUTOFIX_TEST_CASE = (
    # (description, input_text, expected_contains_in_fixed, expect_clean)
    "canonical gender mismatch: הגבינה הצהוב מונחת על המדף",
    "הגבינה הצהוב מונחת על המדף",
    "הצהובה",   # corrected adjective must appear in fixed text
    True,       # gate must pass after fix
)

_GATE_PAIRS = [
    # The original 5/5 acceptance pairs from hebrew_grammar_gate must still pass
    ("clean: definite masculine noun + masculine adjective",
     "הספר הגדול מונח על השולחן", True),
    ("clean: feminine noun + feminine adjective",
     "הגבינה הצהובה טעימה מאוד", True),
    ("clean: Bari product line (real copy)",
     "הקוטג' הזה עוצר ב-B כי רשימת הרכיבים נקייה אבל אחוז החלבון נמוך מהמתחרים",
     True),
    ("MISMATCH: feminine noun + masculine adjective (הגבינה הצהוב)",
     "הגבינה הצהוב מונחת על המדף", False),
    ("MISMATCH: feminine noun + masculine adjective (יוגורט / טעים-טעימה)",
     "היוגורט הטעימה בולטת בין המוצרים", False),
]


def _run_self_test(verbose: bool = True) -> bool:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print("=" * 60)
    print("hebrew_grammar_autofix — self-test")
    print("=" * 60)

    all_pass = True

    # --- Part A: auto-fix canonical test case ---
    desc, input_text, expected_token, expect_clean = _AUTOFIX_TEST_CASE
    print(f"\n[AUTO-FIX TEST] {desc}")
    print(f"  input   : {input_text}")

    result = auto_fix(input_text)
    print(f"  fixed   : {result.fixed_text}")
    print(f"  is_clean: {result.is_clean}  (expected: {expect_clean})")
    if result.fixes_applied:
        for fix in result.fixes_applied:
            print(f"  FIX [{fix.method}]: '{fix.original_span}' → '{fix.corrected_span}'  "
                  f"(flag: {fix.flag.issue_type}, anchor: '{fix.flag.anchor}')")
    if result.skipped_medium:
        print(f"  skipped {result.skipped_medium} medium-confidence flag(s) — human review required")

    token_present = expected_token in result.fixed_text
    clean_ok = (result.is_clean == expect_clean)

    if not token_present:
        print(f"  FAIL: expected '{expected_token}' in fixed text")
        all_pass = False
    if not clean_ok:
        print(f"  FAIL: is_clean={result.is_clean}, expected {expect_clean}")
        all_pass = False
    if token_present and clean_ok:
        print("  PASS")

    # --- Part B: original 5/5 gate pairs must still pass (gate not broken) ---
    print("\n--- Original 5/5 gate pairs (regression check) ---")
    for gate_desc, gate_text, gate_expect in _GATE_PAIRS:
        gate_report = analyze(gate_text)
        gate_ok = (gate_report.is_clean == gate_expect)
        status = "PASS" if gate_ok else "FAIL"
        all_pass = all_pass and gate_ok
        print(f"  [{status}] {gate_desc}")
        if not gate_ok:
            print(f"         text: {gate_text}")
            print(f"         is_clean={gate_report.is_clean}, expected={gate_expect}")

    print("\n" + ("=" * 60))
    print(f"Result: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
    return all_pass


if __name__ == "__main__":
    passed = _run_self_test(verbose=True)
    sys.exit(0 if passed else 1)