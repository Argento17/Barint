"""Hebrew naturalness pre-filter — translationese detector (offline, deterministic).

For: Content + Adversarial QA Agents. Project Tom's Voice (TASK-374), Phase 1.

The gap this fills
------------------
Every existing gate (hebrew_readability, hebrew_grammar_gate, HebEMO, Nakdan)
catches a *gross* failure — framework leakage, code tokens, agreement errors,
tone. NONE detects "translationese": grammatically-clean, leakage-clean Hebrew
that still reads translated/stilted. That is the defect the owner flagged
(`content_voice/tom_bari_voice/10_translationese_taxonomy.md`).

This module is the CHEAP first pass of the two-axis Naturalness Gate. It
deterministically flags the mechanical translationese tells T1–T7 from the
taxonomy. The nuanced half — F1 naturalness judgment + F2 stance/substance
("not neutral-bland") — is done by the LLM-judge described in
`content_voice/tom_bari_voice/11_naturalness_gate.md`, run on an INDEPENDENT lane
(the Adversarial QA Agent, which did not author the copy).

HONEST LIMITS (read before trusting a verdict)
----------------------------------------------
- This is a SIGNAL AMPLIFIER, not the arbiter. HIGH flags are reliable mechanical
  tells; MEDIUM flags are candidates for the LLM judge / human, not auto-fails.
- It cannot detect F2 (neutral-bland / "says nothing") — absence of stance is not
  a regex. It emits an F2 *risk signal* (hedge density + verdict-marker presence)
  for the judge to weigh; it never fails a line on F2 alone.
- Calibration guardrails baked in (owner ruling 2026-06-22): `אשר` is NOT a tell;
  an *earned* short fragment closer ("לייט זה לא.") is NOT a tell — only the
  comma/dash contrastive "X, לא Y" closer and the dangling-`גם` ending fire.

Interface
---------
    from integrations.clients.naturalness_gate import analyze, NaturalnessReport
    r = analyze("ממתק ממולא בטעם נוגט-דבש, לא טבלת קקאו.")
    r.is_clean        # False — T1 contrastive closer (HIGH)
    r.flags           # [NaturalnessFlag(...)]
    r.f2_signal       # {'hedge_ratio':..., 'has_verdict_marker':..., 'risk':...}
    r.to_dict()       # machine-readable

Runnable: `python -m integrations.clients.naturalness_gate` runs the acceptance
test (every owner-flagged line raises a HIGH flag; every owner gold line stays
HIGH-clean).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

CLIENT_VERSION = "1.0"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_SENT_SPLIT = re.compile(r"[.!?]+")


def _sentences(text: str) -> List[str]:
    # Neutralize the "(!)" marker so its "!" does not split sentences;
    # the emphasis count is read from the raw text, so no restore is needed.
    protected = text.replace("(!)", "")
    parts = [p.strip() for p in _SENT_SPLIT.split(protected)]
    return [p for p in parts if p]


def _last_sentence(text: str) -> str:
    s = _sentences(text)
    return s[-1] if s else text.strip()


# ---------------------------------------------------------------------------
# Tell patterns (taxonomy T1–T7). HIGH = reliable mechanical tell; MEDIUM = candidate.
# ---------------------------------------------------------------------------

# T1 — "X, לא Y" contrastive CLOSER (the #1 tell). Comma or em-dash + לא + short
# phrase as the final clause. Guard: bare "...זה לא." (no comma/dash) is an EARNED
# fragment per owner ruling and must NOT fire.
_T1_CLOSER = re.compile(r"[,—]\s*לא\s+\S+")

# T1 mid-text contrastive (weaker) — same shape anywhere. MEDIUM.
_T1_MID = re.compile(r"[,—]\s*לא\s+\S+\s+\S+")

# T1b — the "works as X; less so as Y" antithesis CLOSER (calque). Added after the
# independent judge caught it recurring 4× on the protein-bars shelf (NT-H1, TASK-374)
# where Layer-1 T1 missed it (semicolon/comma form, no bare "לא"). HIGH.
_T1B_CLOSER = re.compile(r"(עובד|נוח|מצוין|מתאים)\s+כ.{0,45}[;,]\s*(פחות|רחוק)\b")

# META — meta-narration opener ("let's call it what it is"). file 2 §5 bans warming-up
# / narrating intent. Caught by the judge (NT-H4, TASK-374). HIGH.
_META = re.compile(r"כדאי לקרוא לזה כמו שזה")

# BARE-CLOSER — a verdict that ends on a single bare evaluative word ("סביר.",
# "מהונדס.", "סבירה."). The "calque swapped for a sibling calque" failure (v2 judge):
# the X-not-Y closer was replaced by a one-word label that says nothing actionable
# (F2-empty + T3 staccato). HIGH. Guard: an earned multi-word fragment is fine.
_BARE_EVAL_WORDS = {"סביר", "סבירה", "מהונדס", "מהונדסת", "בינוני", "בינונית",
                    "חלש", "חלשה", "בעייתי", "בעייתית", "תעשייתי", "תעשייתית"}
_GRADE_TOKEN = re.compile(r"^[A-E]\s*[./]?\s*$")  # "C." grade leak as a whole closer

# SIBLING-CALQUE — "as his/her sibling" product-family reference (calque). MEDIUM.
_SIBLING_PHRASES = ["כמו אחיו", "כמו אחיה", "עוגייה אחות", "לאחותה", "לאחיו",
                    "אותה הנדסה כמו אח"]

# JARGON — phrases unclear to a "naked" shopper (owner 2026-06-22). MEDIUM.
# "מזון שלם" (whole food) reads as jargon — prefer "אוכל אמיתי" / "מזון אמיתי" /
# "חומרי גלם אמיתיים".
_JARGON_PHRASES = ["מזון שלם"]

# ADDITIVE-NAME-UNGLOSSED — a named technical additive must be glossed in plain
# language when it appears in consumer copy (owner 2026-06-22): e.g. "תוסף המזון
# מלטיטול" / "הממתיק מלטיטול", not a bare "מלטיטול". MEDIUM. Refines H4-3: when an
# additive name is MATERIAL to the finding it may be named, but always with a gloss.
_ADDITIVE_NAMES = ["מלטיטול", "גליצרול", "סורביטול", "אריתריטול", "קסיליטול",
                   "מלטודקסטרין", "סוכרלוז", "אספרטם", "אצסולפאם", "אצסולפיים"]
_GLOSS_TOKENS = ["ממתיק", "תוסף", "תוספי", "חומר משמר", "חומרי", "ממתיקים", "תחליף סוכר"]

# T2 — retired calque "X לא תמיד אומר Y" (repaired to "X הוא לא בהכרח Y"). HIGH.
_T2 = re.compile(r"לא\s+תמיד\s+אומר")
# Related variant on watch: "זה לא אומר" / "...לא אומר ש". MEDIUM.
_T2_VARIANT = re.compile(r"\bלא\s+אומר\b")

# T3 — dangling "גם" ending a sentence ("הסוכר גם."). HIGH.
_T3 = re.compile(r"\bגם\s*$")

# T4 — calqued metaphors (extensible phrase list). These are SPECIFIC known calques
# (not open-ended judgments) → HIGH. Expanded after the judge caught "נושא אותו" and
# "נזקף לטובתו" surviving a rewrite (NT-H2/NT-H3, TASK-374).
_T4_PHRASES = [
    "המחיר שלו ברור", "המחיר שלה ברור",
    "נושאים את החלבון", "נושא את החלבון", "נושאת את החלבון",
    "נושא אותו", "נושאת אותו", "נושאים אותו",
    "לזכותו", "לזכותה", "נזקף לטובתו", "נזקף לזכותו", "נזקף לטובתה",
    "עוצר אותו בציון", "עוצרים אותו בציון", "עוצרת אותה בציון",
    "מעמיד אותו ליד", "מעמידה אותה ליד",
    "מציב אותו ב", "מציב אותה ב", "מציבה אותה ב",
]

# T5 — passive nominalization. MEDIUM.
_T5_PATTERNS = [
    re.compile(r"שנעש(תה|ה)\s+היא"),     # "הבחירה שנעשתה היא"
    re.compile(r"ה\S+\s+שנעש(תה|ה)\b"),  # "הבחירה שנעשתה"
    re.compile(r"\bשמוסף\b"),             # should be "מוסף"
]

# T6 — untranslated English loanword. HIGH (list-based).
_T6_WORDS = ["מילק", "קלין", "נייצ'רל"]

# T7 — wrong-register words / calqued compressions. MEDIUM.
_T7_PHRASES = ["הפסד", "סיבים יפים", "בשם, "]
_T7_PATTERNS = [
    re.compile(r"\S+\s+בשם,\s*\d"),       # "דבש בשם, 4%..." compression
]

# F2 signal vocab
_HEDGES = ["יחסית", "קצת", "בדרך כלל", "לרוב", "סביר", "לא רע", "בערך",
           "נוטה", "עשוי", "אולי", "במידה מסוימת", "פחות או יותר"]
_VERDICT_MARKERS = ["מצוין", "ירוד", "גבוה מאוד", "הגבוה ביותר", "הנמוך ביותר",
                    "תעשייתי", "מהונדס", "מטעה", "מקרי בהחלט", "זהירות",
                    "הטוב ביותר", "הבעיה", "חזק", "עתיר"]


@dataclass
class NaturalnessFlag:
    tell: str          # e.g. "T1"
    severity: str      # "HIGH" | "MEDIUM"
    match: str         # the offending substring
    note: str          # what it is + the fix direction

    def to_dict(self):
        return {"tell": self.tell, "severity": self.severity,
                "match": self.match, "note": self.note}


@dataclass
class NaturalnessReport:
    text: str
    flags: List[NaturalnessFlag] = field(default_factory=list)
    f2_signal: dict = field(default_factory=dict)

    @property
    def is_clean(self) -> bool:
        """No HIGH mechanical tell. MEDIUM flags are candidates, not fails —
        they route to the LLM judge, mirroring hebrew_grammar_gate's policy."""
        return not any(f.severity == "HIGH" for f in self.flags)

    @property
    def high_flags(self) -> List[NaturalnessFlag]:
        return [f for f in self.flags if f.severity == "HIGH"]

    def to_dict(self):
        return {
            "client_version": CLIENT_VERSION,
            "is_clean": self.is_clean,
            "flags": [f.to_dict() for f in self.flags],
            "f2_signal": self.f2_signal,
        }


def _f2(text: str) -> dict:
    sents = _sentences(text) or [text]
    hedges = sum(text.count(h) for h in _HEDGES)
    has_verdict = any(m in text for m in _VERDICT_MARKERS)
    ratio = round(hedges / max(len(sents), 1), 2)
    # Risk of neutral-bland: hedgey AND no clear verdict marker.
    risk = "high" if (not has_verdict and hedges >= 1) else (
        "medium" if not has_verdict else "low")
    return {"hedge_count": hedges, "hedge_ratio": ratio,
            "has_verdict_marker": has_verdict, "f2_risk": risk}


def analyze(text: str) -> NaturalnessReport:
    """Run the deterministic translationese pre-filter on one Hebrew string."""
    flags: List[NaturalnessFlag] = []
    last = _last_sentence(text)

    # T1 closer (HIGH) — only on the final sentence.
    m = _T1_CLOSER.search(last)
    if m:
        flags.append(NaturalnessFlag(
            "T1", "HIGH", m.group(0).strip(),
            "Contrastive 'X, לא Y' closer (calque). Resolve with "
            "'מדובר בסך הכל ב…', 'עדיין', or a plain positive — do not end on "
            "a bare 'X, לא Y'."))
    else:
        # T1 mid-text (MEDIUM) — elsewhere in the body.
        body = text[:text.rfind(last)] if last in text else text
        m2 = _T1_MID.search(body)
        if m2:
            flags.append(NaturalnessFlag(
                "T1", "MEDIUM", m2.group(0).strip(),
                "Possible 'X, לא Y' contrastive mid-text — judge whether it reads "
                "as a calque."))

    # T1b "works as X; less/far as Y" antithesis closer (HIGH) — on the final sentence.
    m = _T1B_CLOSER.search(last)
    if m:
        flags.append(NaturalnessFlag(
            "T1b", "HIGH", m.group(0).strip(),
            "'עובד/נוח כ-X; פחות/רחוק כ-Y' antithesis closer (calque of 'works as X; "
            "less so as Y'). Stop earlier or land on a flowing verdict; do not write "
            "the symmetrical antithesis."))

    # META meta-narration opener (HIGH)
    if _META.search(text):
        flags.append(NaturalnessFlag(
            "META", "HIGH", "כדאי לקרוא לזה כמו שזה",
            "Meta-narration opener ('let's call it what it is') — Tom does not warm up "
            "or narrate intent (file 2 §5). Start at the finding."))

    # Grade-token leak as the whole closer ("C.") (HIGH)
    if _GRADE_TOKEN.match(last):
        flags.append(NaturalnessFlag(
            "GRADE", "HIGH", last.strip(),
            "Grade/score token as the closing word — framework leakage + zero "
            "consumer value (the grade is already in the chip). Delete it."))
    # Bare-word evaluative closer ("סביר." / "מהונדס.") (HIGH)
    elif len(last.split()) == 1 and last.strip() in _BARE_EVAL_WORDS:
        flags.append(NaturalnessFlag(
            "BARE", "HIGH", last.strip(),
            "Bare one-word evaluative closer — says nothing actionable (F2-empty) and "
            "reuses across products. Name the mechanism or shelf position instead."))

    # Sibling-reference calque (MEDIUM)
    for p in _SIBLING_PHRASES:
        if p in text:
            flags.append(NaturalnessFlag(
                "T4s", "MEDIUM", p,
                "'as his/her sibling' family-reference calque — phrase it directly "
                "('מאותה משפחה', 'גרסה נוספת של…')."))
            break

    # T8 jargon unclear to a shopper (MEDIUM)
    for p in _JARGON_PHRASES:
        if p in text:
            flags.append(NaturalnessFlag(
                "T8", "MEDIUM", p,
                "Shopper-unclear jargon (owner 2026-06-22) — replace 'מזון שלם' with "
                "'אוכל אמיתי' / 'מזון אמיתי' / 'חומרי גלם אמיתיים'."))
            break

    # T9 ungloss'd technical additive name (MEDIUM)
    has_gloss = any(g in text for g in _GLOSS_TOKENS)
    if not has_gloss:
        for a in _ADDITIVE_NAMES:
            if a in text:
                flags.append(NaturalnessFlag(
                    "T9", "MEDIUM", a,
                    "Bare technical additive name — gloss it in plain language "
                    "(owner 2026-06-22): 'תוסף המזון " + a + "' / 'הממתיק " + a + "'."))
                break

    # T2 retired calque (HIGH)
    m = _T2.search(text)
    if m:
        flags.append(NaturalnessFlag(
            "T2", "HIGH", "לא תמיד אומר",
            "Retired calque 'X לא תמיד אומר Y'. Use 'X הוא לא בהכרח Y'."))
    elif _T2_VARIANT.search(text):
        flags.append(NaturalnessFlag(
            "T2", "MEDIUM", "לא אומר",
            "'לא אומר' variant on watch (calque of 'doesn't mean'). Judge it."))

    # T3 dangling גם (HIGH) — any sentence ending in גם
    for s in _sentences(text):
        if _T3.search(s):
            flags.append(NaturalnessFlag(
                "T3", "HIGH", s[-12:].strip(),
                "Sentence ends on dangling 'גם' (calque of trailing '…too.'). "
                "Rewrite as a full clause."))
            break

    # T4 calqued metaphors (HIGH — these are specific, known calques)
    for p in _T4_PHRASES:
        if p in text:
            flags.append(NaturalnessFlag(
                "T4", "HIGH", p,
                "Calqued metaphor — reads as an English figure of speech in Hebrew. "
                "Use plain Hebrew (e.g. 'מקורו מ…', 'היתרון שלו')."))
            break

    # T5 nominalization (MEDIUM)
    for pat in _T5_PATTERNS:
        m = pat.search(text)
        if m:
            flags.append(NaturalnessFlag(
                "T5", "MEDIUM", m.group(0),
                "Passive nominalization (e.g. 'הבחירה שנעשתה היא…'). Prefer an "
                "active verb ('בחרו להוסיף', 'סוכר מוסף')."))
            break

    # T6 loanword (HIGH)
    for w in _T6_WORDS:
        if re.search(r"\b" + re.escape(w) + r"\b", text):
            flags.append(NaturalnessFlag(
                "T6", "HIGH", w,
                "Untranslated English loanword. Use the Hebrew term "
                "(e.g. 'מילק' → 'שוקולד חלב')."))
            break

    # T7 wrong-register / compression (MEDIUM)
    hit_t7 = next((p for p in _T7_PHRASES if p in text), None)
    if not hit_t7:
        for pat in _T7_PATTERNS:
            m = pat.search(text)
            if m:
                hit_t7 = m.group(0)
                break
    if hit_t7:
        flags.append(NaturalnessFlag(
            "T7", "MEDIUM", hit_t7,
            "Wrong-register word or calqued compression — confirm against the "
            "natural-register vocabulary."))

    # "(!)" emphasis-move usage — seasoning, not default. MEDIUM if present.
    n_emph = text.count("(!)")
    if n_emph >= 1:
        flags.append(NaturalnessFlag(
            "EMPH", "MEDIUM" if n_emph == 1 else "HIGH", "(!)" * n_emph,
            "The '(!)' emphasis move is seasoning used sparingly and only when "
            "earned (file 2). Used " + str(n_emph) + "× — judge whether earned."))

    return NaturalnessReport(text=text, flags=flags, f2_signal=_f2(text))


# ---------------------------------------------------------------------------
# Acceptance test — calibrated on the owner's real examples (TASK-374, Phase 0).
# ---------------------------------------------------------------------------
def _selftest() -> int:
    # Owner-FLAGGED lines: each must raise at least one HIGH flag.
    bad = [
        "ממתק ממולא בטעם נוגט-דבש, לא טבלת קקאו.",      # T1 closer (#27)
        "מוצר סביר, לא חזק.",                            # T1 closer (protein)
        "זה הטוב במדף מהונדס, לא מזון חזק.",             # T1 closer (protein)
        "זו התמונה הכוללת — לא רכיב אחד.",          # T1 closer dash (#5)
        "הפקאן שם. הסוכר גם.",                           # T3 dangling גם (#1)
        "נקי לא תמיד אומר חזק.",                         # T2 (#2)
        "מתאים למי שמחפש מילק עם מינימום סוכר.",         # T6 loanword (#9)
        # New tells caught by the independent judge on the protein-bars refine (TASK-374):
        "עובד כמקור חלבון וסיבים מרוכז, פחות כנשנוש עשוי ממאכל אמיתי.",  # T1b (NT-H1)
        "מצוין כתוסף חלבון נוח; פחות כמזון אמיתי.",      # T1b (NT-H1)
        "החלבון נושא אותו, השאר ציפוי תעשייתי.",         # T4 metaphor (NT-H2)
        "החלבון בא מבוטנים קלויים אמיתיים, וזה נזקף לטובתו.",  # T4 metaphor (NT-H3)
        "כדאי לקרוא לזה כמו שזה: יש כאן הרבה סוכר.",     # META opener (NT-H4)
        # v2 judge: calque swapped for bare-word closer / grade-token leak:
        "המספרים סבירים אבל ההרכב מהונדס לעומק. סביר.",   # BARE one-word closer
        "רשימה ארוכה וחלבון מבודד מכמה מקורות. מהונדס.",  # BARE one-word closer
        "עוגייה שמרכזת את הכל, חלבון מכמה מקורות מבודדים. C.",  # GRADE token leak
    ]
    # Owner GOLD lines: none may raise a HIGH flag.
    good = [
        "זו כנראה העוגה הטובה ביותר שראינו בקטגוריה הזאת, ולא מפתיע שזו עוגת גבינה.",
        "לייט זה לא.",                                   # earned fragment — guard
        "יחד עם זאת היצרן השתמש בממתיקים ותוסף מתחלב, כך שזה מוצר מהונדס יותר משוקולד מריר קלאסי.",
        "כל קשר בין עוגת בריוש לעוגה זו מקרי בהחלט.",
        "סוכר הוא הרכיב הראשון במוצר ויש בו גם דבש.",     # גם mid-sentence — guard
        "מוצר נקי הוא לא בהכרח מוצר חזק תזונתית.",        # repaired T2 form — guard
    ]
    failures = []
    for t in bad:
        r = analyze(t)
        if r.is_clean:
            failures.append(("BAD-NOT-FLAGGED", t))
    for t in good:
        r = analyze(t)
        if not r.is_clean:
            failures.append(("GOOD-WRONGLY-FLAGGED", t,
                             [f.to_dict() for f in r.high_flags]))

    # F2 "calm-trap" signal test (owner ruling: 'calm' over-corrects to mush).
    # Layer 1 never FAILS on F2 (that is the LLM judge's call) but its f2_signal must
    # separate a clear verdict (low risk) from hedge-only neutral copy (high risk).
    bland = "המוצר הזה סביר יחסית. יש בו קצת חלבון וגם קצת סוכר, פחות או יותר כמו אחרים."
    verdicty = "החלבון כאן מהגבוהים במדף, אבל המתיקות תעשייתית — מבנה של ממתק."
    if analyze(bland).f2_signal["f2_risk"] != "high":
        failures.append(("F2-CALM-TRAP-NOT-HIGH", bland, analyze(bland).f2_signal))
    if analyze(verdicty).f2_signal["f2_risk"] != "low":
        failures.append(("F2-VERDICT-NOT-LOW", verdicty, analyze(verdicty).f2_signal))

    if failures:
        print("NATURALNESS GATE SELFTEST: FAIL")
        for f in failures:
            print("  ", f)
        return 1
    print("NATURALNESS GATE SELFTEST: PASS")
    print(f"  {len(bad)} flagged lines all raised HIGH; "
          f"{len(good)} gold lines all HIGH-clean; "
          f"F2 calm-trap + verdict signals correct.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(_selftest())
