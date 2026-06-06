"""Hebrew readability + framework-leakage analyzer (fully offline, no network).

For: Content + QA Agents. Two jobs the project had no instrument for:

  1. READABILITY — an offline heuristic profile of a Hebrew passage: sentence length,
     word length, long-word density (a rare-word proxy), and function-word ratio. The
     Content Agent's editorial standard prizes short, concrete consumer copy; this turns
     "feels heavy" into measurable signals (e.g. avg sentence > 22 words, long-word ratio
     high) so a draft can be tightened against numbers.

  2. FRAMEWORK-LEAKAGE SCAN — the hard QA gate. The editorial contract forbids Tier-4
     internals from ever reaching consumer copy: NOVA, cap, floor, BSIP, dimension/
     penalty/weight names, raw confidence numbers, English words bleeding into Hebrew,
     and "score 68.2 / grade B" mechanics. This scans a string for every such leak and
     returns located hits — a deterministic check the QA Agent can run on any insightLine
     / rowVerdict / explanation before it ships.
     (Grounded in: bari_explanation_framework_v1 §"forbidden", bsip2_to_web_translation_
     contract_v1 Tier-4 table, score_presentation_v1.)

HONEST LIMIT: the readability score is a transparent heuristic, NOT a validated Hebrew
readability index (no Hebrew analogue of Flesch-Kincaid is calibrated here). Use it to
*compare* drafts and flag outliers, not as an absolute grade. The leakage scan, by
contrast, is a precise allow/deny check and is safe to gate on.

No network, no deps — pure stdlib. Importable, and runnable for a self-test.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

CLIENT_VERSION = "1.0"

# Hebrew standalone function words (prefix particles ב/ל/מ/ה/ו/ש/כ are handled separately).
_FUNCTION_WORDS = {
    "של", "את", "על", "עם", "אל", "מן", "כי", "גם", "כל", "זה", "זו", "זאת",
    "הוא", "היא", "הם", "הן", "אני", "אתה", "אנחנו", "אבל", "או", "אם", "לא",
    "כמו", "יותר", "פחות", "רק", "כבר", "עוד", "אך", "אשר", "כאשר", "בין",
    "אחרי", "לפני", "תחת", "מעל", "בלי", "יש", "אין", "היה", "הייתה", "להיות",
}

# Tier-4 framework terms that must never appear in consumer copy (mixed he/en).
_LEAK_TERMS = [
    # English internals
    "nova", "bsip", "cap", "floor", "penalty", "penalties", "dimension",
    "dimension_scores", "caps_applied", "penalties_applied", "floors_applied",
    "nova_proxy", "confidence_score", "confidence_band", "weighted_dimension_score",
    "binding_cap", "structural_emptiness", "weight", "weights", "archetype", "router",
    "engine", "algorithm",
    # Hebrew framework jargon
    "אלגוריתם", "מנוע הניקוד", "דימנשן", "נובה", "פרוקסי",
]

# words that signal a *recommendation* (Bari describes, never prescribes)
_RECOMMENDATION_TERMS = [
    "מומלץ", "כדאי לקנות", "עדיף לקנות", "אל תקנו", "הימנעו", "בריא יותר",
    "הבחירה הנכונה", "אסור לאכול", "צריך לאכול",
]

_LATIN_RUN = re.compile(r"[A-Za-z]{2,}")
# a numeric score/grade mechanic: "68.2", "72/B", "ניקוד 80"
_SCORE_NUM = re.compile(r"\b\d{1,3}(?:\.\d+)?\s*/\s*[A-Eא-ה]\b|\b\d{2,3}\.\d+\b")
_SENT_SPLIT = re.compile(r"[.!?׃\n]+")
_HEB_WORD = re.compile(r"[֐-׿]+")
_TOKEN = re.compile(r"[A-Za-z֐-׿']+")


@dataclass
class Leak:
    kind: str          # "framework" | "english" | "recommendation" | "score_mechanic"
    term: str
    context: str       # ~surrounding snippet


@dataclass
class ReadabilityReport:
    word_count: int
    sentence_count: int
    avg_sentence_len_words: float
    avg_word_len_chars: float
    long_word_ratio: float          # share of Hebrew words >= 8 chars (rare-word proxy)
    function_word_ratio: float       # share of tokens that are function words
    leaks: list[Leak] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        """True iff no framework/score/recommendation leak — the shippability gate.
        (English leaks alone don't block: a brand name may be Latin.)"""
        return not any(l.kind in ("framework", "score_mechanic", "recommendation")
                       for l in self.leaks)

    @property
    def readability_score(self) -> float:
        """Transparent 0-100 heuristic (higher = simpler/cleaner). NOT a validated index."""
        s = 100.0
        if self.avg_sentence_len_words > 18:
            s -= min(30, (self.avg_sentence_len_words - 18) * 2.5)
        if self.long_word_ratio > 0.18:
            s -= min(20, (self.long_word_ratio - 0.18) * 100)
        if self.avg_word_len_chars > 6.0:
            s -= min(15, (self.avg_word_len_chars - 6.0) * 6)
        s -= 8 * sum(1 for l in self.leaks if l.kind != "english")
        return round(max(0.0, s), 1)


def _scan_leaks(text: str) -> list[Leak]:
    leaks: list[Leak] = []
    low = text.lower()
    for term in _LEAK_TERMS:
        idx = low.find(term.lower())
        if idx != -1:
            # word-boundary-ish guard for short English tokens to cut false hits
            if term.isascii() and len(term) <= 4:
                if not re.search(rf"(?<![a-z]){re.escape(term)}(?![a-z])", low):
                    continue
            leaks.append(Leak("framework", term, _ctx(text, idx)))
    for term in _RECOMMENDATION_TERMS:
        idx = text.find(term)
        if idx != -1:
            leaks.append(Leak("recommendation", term, _ctx(text, idx)))
    for m in _SCORE_NUM.finditer(text):
        leaks.append(Leak("score_mechanic", m.group(0), _ctx(text, m.start())))
    for m in _LATIN_RUN.finditer(text):
        # skip if it was already caught as a framework term
        if any(l.term.lower() == m.group(0).lower() and l.kind == "framework" for l in leaks):
            continue
        leaks.append(Leak("english", m.group(0), _ctx(text, m.start())))
    return leaks


def _ctx(text: str, idx: int, span: int = 24) -> str:
    a = max(0, idx - span)
    b = min(len(text), idx + span)
    return text[a:b].replace("\n", " ").strip()


def analyze(text: str) -> ReadabilityReport:
    """Profile a Hebrew passage and scan it for framework leakage."""
    text = text or ""
    sentences = [s for s in _SENT_SPLIT.split(text) if s.strip()]
    tokens = _TOKEN.findall(text)
    heb_words = _HEB_WORD.findall(text)
    word_count = len(tokens)
    sent_count = max(1, len(sentences))
    avg_sent = round(word_count / sent_count, 1)
    avg_wlen = round(sum(len(w) for w in heb_words) / max(1, len(heb_words)), 1)
    long_words = sum(1 for w in heb_words if len(w) >= 8)
    long_ratio = round(long_words / max(1, len(heb_words)), 3)
    fn = sum(1 for t in tokens if t in _FUNCTION_WORDS)
    fn_ratio = round(fn / max(1, word_count), 3)

    leaks = _scan_leaks(text)
    flags: list[str] = []
    if avg_sent > 22:
        flags.append(f"long sentences (avg {avg_sent} words/sentence)")
    if long_ratio > 0.22:
        flags.append(f"dense vocabulary ({long_ratio:.0%} long words)")
    for l in leaks:
        if l.kind == "framework":
            flags.append(f"FRAMEWORK LEAK: '{l.term}' (…{l.context}…)")
        elif l.kind == "score_mechanic":
            flags.append(f"SCORE MECHANIC exposed: '{l.term}'")
        elif l.kind == "recommendation":
            flags.append(f"RECOMMENDATION language: '{l.term}'")
    return ReadabilityReport(
        word_count=word_count,
        sentence_count=len(sentences),
        avg_sentence_len_words=avg_sent,
        avg_word_len_chars=avg_wlen,
        long_word_ratio=long_ratio,
        function_word_ratio=fn_ratio,
        leaks=leaks,
        flags=flags,
    )


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    samples = {
        "clean consumer line":
            "הקוטג' הזה עוצר ב-B כי רשימת הרכיבים נקייה אבל אחוז החלבון נמוך מהמתחרים.",
        "leaky (framework + score)":
            "המוצר קיבל ניקוד 68.2 כי ה-NOVA cap הופעל על ה-dimension של processing.",
        "recommendation + english":
            "מומלץ לקנות את ה-Milky כי הוא הבריא יותר על המדף.",
    }
    for name, txt in samples.items():
        r = analyze(txt)
        print(f"== {name} ==")
        print(f"  words={r.word_count} sent={r.sentence_count} avg_sent={r.avg_sentence_len_words} "
              f"avg_wlen={r.avg_word_len_chars} long={r.long_word_ratio} fn={r.function_word_ratio}")
        print(f"  readability_score={r.readability_score} is_clean={r.is_clean}")
        for f in r.flags:
            print(f"    - {f}")
