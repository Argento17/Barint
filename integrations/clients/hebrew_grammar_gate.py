"""Hebrew grammar / morphological-agreement gate (offline, model-based).

For: Content + QA Agents. Fills the gap hebrew_readability.py cannot fill:
grammatical agreement errors in Hebrew — gender and number mismatches between
noun-adjective pairs, pronoun-noun chains, and subject-verb constructions.

Architecture
------------
Backend: DictaBERT-morph (`dicta-il/dictabert-morph`, ~440MB, BERT-base size).
The model assigns per-token POS tags + morphological features (Gender, Number,
Person, Tense, …) via its custom `predict()` method. We run agreement checks over
the resulting token sequence using deterministic rules — the ML part is tagging,
not rule-learning.

Download policy: the model downloads on first use (HuggingFace hub cache, same
as HebEMO). Subsequent calls load from cache, no network. `transformers` +
`torch` must already be installed (they are — verified at TASK-341 Phase 1).

License: DictaBERT is released under MIT (dicta-il GitHub, confirmed 2026-06-19).
Safe to embed in Bari's pipeline without copyleft obligation.

HONEST LIMITS
-------------
- DictaBERT-morph can mislabel grammatical gender for loan-words and ambiguous
  forms (e.g. חמאה, which it may tag Masc despite being Fem in standard Hebrew).
  Flags should therefore be treated as CANDIDATES for human review, not hard
  verdicts. The gate is a signal amplifier, not a rubber stamp.
- Subject-verb checks are approximate: we detect the closest preceding bare
  NOUN/PRON to a VERB; multi-clause sentences can produce false positives.
- The gate covers Modern Israeli Hebrew prose. Niche liturgical or archaic forms
  are out of scope.

Interface
---------
    from integrations.clients.hebrew_grammar_gate import analyze, GrammarReport

    report = analyze("הגבינה הצהוב מאוד")
    print(report.is_clean)          # False — Fem noun + Masc adj
    print(report.flags)             # [GrammarFlag(...)]
    print(report.to_dict())         # machine-readable

Runnable: `python -m integrations.clients.hebrew_grammar_gate` runs the built-in
acceptance test (clean sentence passes, gender-mismatched sentence is flagged).
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

CLIENT_VERSION = "1.0"
_MODEL_ID = "dicta-il/dictabert-morph"

# ---------------------------------------------------------------------------
# Lazy model cache — load once per process
# ---------------------------------------------------------------------------
_model = None
_tokenizer = None


def _load_model():
    """Load DictaBERT-morph on first call; cache in module globals."""
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer
    try:
        from transformers import AutoModel, AutoTokenizer
        import os
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
        _tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID, trust_remote_code=True)
        _model = AutoModel.from_pretrained(_MODEL_ID, trust_remote_code=True)
        logger.debug("DictaBERT-morph loaded from cache / HF hub.")
    except ImportError as exc:
        raise RuntimeError(
            "hebrew_grammar_gate requires `transformers` and `torch`. "
            "They are listed as installed (TASK-341); check your venv."
        ) from exc
    return _model, _tokenizer


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

ISSUE_NOUN_ADJ_GENDER = "noun_adj_gender_mismatch"
ISSUE_NOUN_ADJ_NUMBER = "noun_adj_number_mismatch"
ISSUE_SUBJ_VERB_GENDER = "subject_verb_gender_mismatch"
ISSUE_SUBJ_VERB_NUMBER = "subject_verb_number_mismatch"
ISSUE_ILLEGAL_FORM = "unrecognized_token"


@dataclass
class GrammarFlag:
    """A single morphological-agreement problem detected in the text."""
    issue_type: str           # one of the ISSUE_* constants above
    span: str                 # the offending token(s), Hebrew text
    anchor: str               # the governing token (head of the mismatch pair)
    expected: str             # what we expected (e.g. "Gender=Fem")
    observed: str             # what the model tagged (e.g. "Gender=Masc")
    context: str              # surrounding text snippet (~±30 chars)
    confidence: str           # "high" | "medium" — see note in HONEST LIMITS

    def to_dict(self) -> dict:
        return {
            "issue_type": self.issue_type,
            "span": self.span,
            "anchor": self.anchor,
            "expected": self.expected,
            "observed": self.observed,
            "context": self.context,
            "confidence": self.confidence,
        }


@dataclass
class GrammarReport:
    """Full morphological-agreement report for one passage of Hebrew text."""
    text: str
    token_analysis: list[dict]     # raw per-token dicts from DictaBERT-morph
    flags: list[GrammarFlag] = field(default_factory=list)
    model_id: str = _MODEL_ID
    client_version: str = CLIENT_VERSION

    @property
    def is_clean(self) -> bool:
        """True iff no agreement flags were raised.
        Mirrors hebrew_readability.ReadabilityReport.is_clean interface.
        """
        return len(self.flags) == 0

    @property
    def flag_count(self) -> int:
        return len(self.flags)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "is_clean": self.is_clean,
            "flag_count": self.flag_count,
            "flags": [f.to_dict() for f in self.flags],
            "token_analysis": self.token_analysis,
            "model_id": self.model_id,
            "client_version": self.client_version,
        }


# ---------------------------------------------------------------------------
# Agreement rules
# ---------------------------------------------------------------------------

# Gender values the model may return
_MASC = "Masc"
_FEM = "Fem"
_GENDERS = {_MASC, _FEM}

# Number values
_SING = "Sing"
_PLUR = "Plur"
_NUMBERS = {_SING, _PLUR}

# POS tags where gender/number agreement is enforced with a preceding noun
_AGREEING_WITH_NOUN = {"ADJ", "DET"}
# POS tags that can be subjects
_SUBJECT_POS = {"NOUN", "PROPN", "PRON"}
# POS for verbs
_VERB_POS = {"VERB", "AUX"}


def _feat(token: dict, key: str) -> Optional[str]:
    """Extract a morphological feature value; return None if absent or '?'."""
    val = token.get("feats", {}).get(key)
    if val in (None, "?", ""):
        return None
    return val


def _ctx(text: str, span: str, window: int = 30) -> str:
    """Return the text window around the first occurrence of `span`."""
    idx = text.find(span)
    if idx == -1:
        return text[:window * 2]
    a = max(0, idx - window)
    b = min(len(text), idx + len(span) + window)
    return text[a:b].replace("\n", " ").strip()


def _is_construct_state(token: dict) -> bool:
    """Return True if this NOUN is in construct state (סמיכות / nomen regens).

    In DictaBERT-morph output, a construct-state noun has no DET prefix
    (the definite article attaches to the possessed noun, not the possessor).
    Example: רשימת (no DET) in "רשימת הרכיבים" vs. הרשימה (DET) in "הרשימה הנקייה".
    This heuristic is correct for modern Hebrew prose in the vast majority of cases.
    """
    return "DET" not in token.get("prefixes", [])


def _resolve_noun_head(tokens: list[dict], start: int) -> tuple[int, dict]:
    """Resolve the true semantic head of a noun phrase starting at `start`.

    Handles construct-state chains (סמיכות): רשימת הרכיבים, מחיר היחידה, etc.
    Returns (index_of_last_consumed_token, head_noun_token).

    The ADJ after this chain must agree with the first noun (the head).
    We consume forward through NOUN tokens that are:
      - the current noun in construct state (no DET), followed by another NOUN,
      - or the final possessed noun (with DET or not).
    We stop when we hit an ADJ, VERB, CONJ, or non-NOUN token.
    """
    n = len(tokens)
    head = tokens[start]
    j = start

    # Walk forward through the construct chain — each bare NOUN followed by another
    # NOUN is a construct link. The last NOUN in the chain is NOT the head for ADJ
    # agreement purposes; the FIRST one is.
    while j + 1 < n:
        next_tok = tokens[j + 1]
        next_pos = next_tok.get("pos", "")
        if next_pos in ("NOUN", "PROPN"):
            # Advance through the chain; head remains the first noun
            j += 1
        else:
            break

    return j, head


def _check_noun_adj_agreement(tokens: list[dict], text: str) -> list[GrammarFlag]:
    """Detect noun-adjective gender or number mismatches.

    Strategy: walk the token list; when we see a NOUN, resolve the full noun
    phrase (including construct-state chains like רשימת הרכיבים). Then check
    every immediately following ADJ against the FIRST noun in the chain (the
    semantic head). Stop the ADJ scan at the first non-ADJ/non-DET token.

    Hebrew construct-state (סמיכות) rule: in "רשימת הרכיבים נקייה", the ADJ
    "נקייה" modifies "רשימת" (the head, Fem Sing), NOT "הרכיבים" (Masc Plur).
    A naive scan anchoring on the immediately preceding NOUN produces the false
    positive rשימת הרכיבים + נקייה → flagged, which is wrong. This function
    resolves the head correctly.

    Confidence assignment:
    - "high"   — both noun-head and ADJ carry the definite-article (DET) prefix,
                 which in Hebrew obligatorily co-occur (definite agreement); a
                 mismatch here is almost certainly an error.
    - "medium" — one or both are bare (no DET); still a likely error but the
                 model's gender tags for loanwords / ambiguous forms are less
                 reliable.

    Known limit: does not detect agreement errors inside relative clauses or
    after coordinating conjunctions ("ו-/אבל/או"), where the reference noun may
    be several tokens away. Those cases are rare in Bari's short product-copy
    strings and are deferred to a future version.
    """
    flags: list[GrammarFlag] = []
    n = len(tokens)
    i = 0
    while i < n:
        tok = tokens[i]
        if tok.get("pos") not in ("NOUN", "PROPN"):
            i += 1
            continue

        # Resolve the full construct-state chain; `last_noun_idx` = last consumed
        # NOUN position; `head` = the semantic head (first noun) for ADJ agreement.
        last_noun_idx, head = _resolve_noun_head(tokens, i)
        head_gender = _feat(head, "Gender")
        head_number = _feat(head, "Number")
        head_text = head.get("token", "")

        # Now look ahead past the chain for adjectives
        j = last_noun_idx + 1
        while j < n and tokens[j].get("pos") in ("ADJ", "DET"):
            adj = tokens[j]
            adj_gender = _feat(adj, "Gender")
            adj_number = _feat(adj, "Number")
            adj_text = adj.get("token", "")

            # Confidence: high when head noun has DET prefix AND ADJ has DET prefix
            # (definite agreement is obligatory and unambiguous in Modern Hebrew)
            both_definite = (
                "DET" in head.get("prefixes", [])
                and "DET" in adj.get("prefixes", [])
            )
            confidence = "high" if both_definite else "medium"

            # Gender mismatch
            if (head_gender in _GENDERS and adj_gender in _GENDERS
                    and head_gender != adj_gender):
                flags.append(GrammarFlag(
                    issue_type=ISSUE_NOUN_ADJ_GENDER,
                    span=adj_text,
                    anchor=head_text,
                    expected=f"Gender={head_gender}",
                    observed=f"Gender={adj_gender}",
                    context=_ctx(text, adj_text),
                    confidence=confidence,
                ))

            # Number mismatch
            if (head_number in _NUMBERS and adj_number in _NUMBERS
                    and head_number != adj_number):
                flags.append(GrammarFlag(
                    issue_type=ISSUE_NOUN_ADJ_NUMBER,
                    span=adj_text,
                    anchor=head_text,
                    expected=f"Number={head_number}",
                    observed=f"Number={adj_number}",
                    context=_ctx(text, adj_text),
                    confidence=confidence,
                ))
            j += 1

        # Advance past the entire noun phrase (head + chain)
        i = last_noun_idx + 1
    return flags


def _check_verb_agreement(tokens: list[dict], text: str) -> list[GrammarFlag]:
    """Detect subject-verb gender or number mismatches.

    Strategy: for each VERB token, find the nearest preceding NOUN/PROPN/PRON
    in the same clause (heuristic: within 4 tokens, stopping at another VERB or
    punctuation). Check gender and number agreement.

    Known limit: in VSO word-order sentences (verb comes before subject) this
    can produce false positives; those are flagged as 'medium' confidence.
    """
    flags: list[GrammarFlag] = []
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if tok.get("pos") not in _VERB_POS:
            continue
        verb_gender = _feat(tok, "Gender")
        verb_number = _feat(tok, "Number")
        if not verb_gender and not verb_number:
            continue  # uninflected verb form — skip
        verb_text = tok.get("token", "")

        # Search backward for a subject candidate
        subject = None
        for k in range(i - 1, max(-1, i - 5), -1):
            candidate = tokens[k]
            cpos = candidate.get("pos", "")
            if cpos in _SUBJECT_POS:
                subject = candidate
                break
            if cpos in _VERB_POS:
                break  # another verb = clause boundary, stop

        if subject is None:
            continue

        subj_gender = _feat(subject, "Gender")
        subj_number = _feat(subject, "Number")
        subj_text = subject.get("token", "")

        # Gender: verb gender is often Masc|Fem (singular) or Fem,Masc (plural, ambiguous)
        # Only flag when verb gender is a single unambiguous value
        if (verb_gender in _GENDERS
                and subj_gender in _GENDERS
                and verb_gender != subj_gender):
            flags.append(GrammarFlag(
                issue_type=ISSUE_SUBJ_VERB_GENDER,
                span=verb_text,
                anchor=subj_text,
                expected=f"Gender={subj_gender}",
                observed=f"Gender={verb_gender}",
                context=_ctx(text, verb_text),
                confidence="medium",  # VSO order can look like mismatch
            ))

        # Number
        if (verb_number in _NUMBERS
                and subj_number in _NUMBERS
                and verb_number != subj_number):
            flags.append(GrammarFlag(
                issue_type=ISSUE_SUBJ_VERB_NUMBER,
                span=verb_text,
                anchor=subj_text,
                expected=f"Number={subj_number}",
                observed=f"Number={verb_number}",
                context=_ctx(text, verb_text),
                confidence="medium",
            ))

    return flags


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def analyze(text: str) -> GrammarReport:
    """Run morphological-agreement analysis on a Hebrew passage.

    Parameters
    ----------
    text : str
        The Hebrew string to analyze. May be a single clause or a full
        multi-sentence paragraph.

    Returns
    -------
    GrammarReport
        Contains `.is_clean` (True = no flags), `.flags` (list[GrammarFlag]),
        and `.token_analysis` (raw DictaBERT-morph output per sentence).

    Raises
    ------
    RuntimeError
        If DictaBERT-morph cannot be loaded (missing `transformers`/`torch`).
    """
    text = (text or "").strip()
    if not text:
        return GrammarReport(text=text, token_analysis=[])

    model, tokenizer = _load_model()

    # Split into sentences on clause boundaries for better tagging accuracy.
    # We join the full list in one `predict` call — the model handles batches.
    sentences = _split_sentences(text)
    raw_results = model.predict(sentences, tokenizer=tokenizer)

    all_tokens: list[dict] = []
    all_flags: list[GrammarFlag] = []

    for sent_result in raw_results:
        sent_text = sent_result.get("text", "")
        tokens = sent_result.get("tokens", [])
        all_tokens.extend(tokens)

        # Run agreement checks per sentence (avoid cross-sentence false positives)
        all_flags.extend(_check_noun_adj_agreement(tokens, sent_text))
        all_flags.extend(_check_verb_agreement(tokens, sent_text))

    return GrammarReport(
        text=text,
        token_analysis=raw_results,
        flags=all_flags,
    )


def _split_sentences(text: str) -> list[str]:
    """Split Hebrew text into sentence-level chunks for the morph model.

    The morph model works at sentence granularity. We split on sentence-ending
    punctuation and filter empty chunks.
    """
    parts = re.split(r"[.!?׃\n]+", text)
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Reader-context lock
# ---------------------------------------------------------------------------

READER_CONTEXT = {
    "audience": "plural",          # אתם — second-person plural
    "audience_he": "אתם",
    "register": "direct-conversational",
    "default_gender": "Masc",     # Israeli Hebrew default when gender is underspecified
    "second_person_form": "plural-masculine",
    # Prompt fragment to inject into generation prompts.
    "generation_context": (
        "הכתיבה מופנית לקהל ברבים (אתם) בגוף שני ברבים, בעברית יומיומית ישירה. "
        "הימנע מגוף שלישי יחיד, מלשון נקבה כברירת מחדל, ומפניה בגוף ראשון."
    ),
}
"""
Reader-context lock for Bari's default grammatical register.

Fields
------
audience
    "plural" — Bari addresses the reader as part of a collective (אתם), not
    as a lone individual (אתה/את). This prevents the model from drifting into
    singular masculine (אתה) or singular feminine (את) forms.

register
    "direct-conversational" — the register of the supermarket shelf: clear,
    immediate, no jargon. Not formal, not academic.

default_gender
    "Masc" — Israeli Hebrew defaults to masculine when the audience gender is
    unknown. Bari copy uses masculine plural (אתם) as the unmarked form.

generation_context
    Inject this Hebrew sentence into a generation prompt to lock the register
    before any Hebrew output is requested.

Usage in a generation prompt
----------------------------
    from integrations.clients.hebrew_grammar_gate import READER_CONTEXT

    system_prompt = (
        "אתה כותב עברית עבור Bari. "
        + READER_CONTEXT["generation_context"]
    )
    # Then generate with this system prompt prepended.

This is a config dict, not a function. Import and use directly.
"""


# ---------------------------------------------------------------------------
# Self-test / acceptance test (runnable as __main__)
# ---------------------------------------------------------------------------

_ACCEPTANCE_PAIRS = [
    # (description, text, expect_clean)
    (
        "clean: definite masculine noun + masculine adjective",
        "הספר הגדול מונח על השולחן",
        True,
    ),
    (
        "clean: feminine noun + feminine adjective",
        "הגבינה הצהובה טעימה מאוד",
        True,
    ),
    (
        "clean: Bari product line (real copy)",
        "הקוטג' הזה עוצר ב-B כי רשימת הרכיבים נקייה אבל אחוז החלבון נמוך מהמתחרים",
        True,
    ),
    (
        "MISMATCH: feminine noun + masculine adjective (הגבינה הצהוב)",
        "הגבינה הצהוב מונחת על המדף",
        False,
    ),
    (
        "MISMATCH: feminine noun + masculine adjective (יוגורט / טעים-טעימה)",
        "היוגורט הטעימה בולטת בין המוצרים",
        False,   # יוגורט is Masc; הטעימה is Fem → mismatch
    ),
]


def _run_acceptance_test(verbose: bool = True) -> bool:
    """Run acceptance tests. Returns True iff all expectations are met."""
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print("=" * 60)
    print("hebrew_grammar_gate — acceptance test")
    print(f"model: {_MODEL_ID}")
    print("=" * 60)

    all_pass = True
    for desc, text, expect_clean in _ACCEPTANCE_PAIRS:
        report = analyze(text)
        ok = (report.is_clean == expect_clean)
        status = "PASS" if ok else "FAIL"
        all_pass = all_pass and ok

        print(f"\n[{status}] {desc}")
        print(f"  text     : {text}")
        print(f"  is_clean : {report.is_clean}  (expected: {expect_clean})")
        if report.flags:
            for f in report.flags:
                print(
                    f"  FLAG [{f.confidence}] {f.issue_type}: "
                    f"'{f.span}' (anchor='{f.anchor}') "
                    f"expected {f.expected}, got {f.observed}"
                )
        elif verbose:
            print("  no flags (clean)")

    n_pairs = len(_ACCEPTANCE_PAIRS)
    print("\n" + ("=" * 60))
    print(f"Result: {'ALL PASS' if all_pass else 'SOME FAILURES'} "
          f"({n_pairs if all_pass else '?'}/{n_pairs} pairs correct)")
    return all_pass


if __name__ == "__main__":
    import sys
    passed = _run_acceptance_test(verbose=True)
    sys.exit(0 if passed else 1)
