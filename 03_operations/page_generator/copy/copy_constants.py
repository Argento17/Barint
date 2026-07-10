#!/usr/bin/env python3
"""copy_constants.py — single source of truth for consumer-copy enforcement (P541).

Banned phrases, prose field registry, sentence-repeat threshold, and robust
harvesters for author_copy.py template fingerprints. stdlib only.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Banned consumer phrases — substring match, zero tolerance at validation time
# and generation time (enforce_clean in author_copy.py).
# ---------------------------------------------------------------------------

BANNED_CONSUMER_PHRASES: list[str] = [
    # Data-state / confidence narration
    "צילום תווית",
    "חוסר ודאות",
    "מאומת במלואו",
    "נשארת זהירה",
    "נשארים זהירים",
    "משאירה מקום לספק",
    "הנתונים כאן זמינים",
    "הערכה זהירה",
    "טקסט העמוד",
    "לא מאומת",
    "בגדר הערכה",
    "רמת ביטחון",
    "מהימנות הנתונים",
    # Score-mechanism narration
    "מגביל את הציון",
    "קובע את הציון",
    "הגורם המגביל",
    "מוריד את הציון",
    "משפיעים על הציון",
    "ממתן את הציון",
    "עוצר ב-",
    "הציון נשאר",
    "הציון יורד",
    "מעצב את הציון",
    # Historical baseline templates
    "תורם לתחושת שובע",
    "הציון מבטא הערכה",
    # H3-R2 (owner ruling, 2026-07-10, TASK-550): inverted-valence Hebrew —
    # "קל" reads positive/diet-adjacent while the intended meaning is
    # nutritionally poor. Wrong Hebrew, wrong valence, banned outright.
    # Owner's approved replacement construction: "בתור מקור לארוחת בוקר,
    # אתם לא מקבלים כאן הרבה ערכים תזונתיים." — say it directly, second
    # person, no euphemism.
    "קל מבחינה תזונתית",
    "קל יחסית מבחינה תזונתית",
    "קלה מבחינה תזונתית",
    "קלה יחסית מבחינה תזונתית",
]

# ---------------------------------------------------------------------------
# Banned consumer PATTERNS — regex families, zero tolerance (CHECK 6).
#
# Why families and not more literal strings: on 2026-07-10 the hard_cheeses_v4
# shelf passed CHECK 1 with banned=0 while shipping "רשימת הרכיבים לא הגיעה
# מהסריקה, כך שהציון מבוסס על הנתונים התזונתיים בלבד", "אי-אפשר לאמת" and
# "מגביל את האמינות". The list above bans "לא מאומת" — the copy wrote "לא אומת".
# It bans "מגביל את הציון" — the copy wrote "מגביל את האמינות". A literal-string
# list only ever bans the phrasings the engine already happened to emit; the next
# paraphrase walks straight through. These patterns ban the ACT (narrating where
# the data came from, whether it was verified, how confident the score is), which
# is what the owner actually ruled against.
#
# Owner ruling: consumer copy NEVER narrates data-state. Unknown is acceptable;
# saying "we couldn't scrape it" to a shopper is not. If a field is unknown the
# page shows "data could not be retrieved" as UI state — the PROSE stays silent.
# ---------------------------------------------------------------------------

BANNED_CONSUMER_PATTERNS: list[tuple[str, str]] = [
    # (name, regex) — matched with re.search against each consumer prose field.
    ("scrape_narration",
     r"מהסריקה|לא\s+נסרק|(?:רשימת\s+ה?רכיבים|הנתונים|נתוני\s+\S+)\s+לא\s+הגיע\w*"),
    ("score_basis_narration",
     r"הציון\s+מבוסס\s+על|מבוסס\s+על\s+הנתונים\s+התזונתיים\s+בלבד"),
    ("verification_narration",
     r"אי-?\s*אפשר\s+לאמת|לא\s+ניתן\s+לאמת|לא\s+אומת\b|לא\s+מאומת|טרם\s+אומת"),
    ("confidence_narration",
     r"מגביל\s+את\s+ה?(?:אמינות|מהימנות|ודאות)|רמת\s+ה?(?:אמינות|מהימנות)|"
     r"אמינות\s+הנתונים|מהימנות\s+הנתונים"),
    # "בהיעדר סוכר מוסף" is legitimate; only the DATA-absence framing is banned,
    # so the pattern requires a data noun after the preposition. "עדר" (herd) is
    # the misspelling of "היעדר" found live in cheese_v4 — banned in both spellings.
    ("data_absence_narration",
     r"ב?ה?יעדר\s+נתונ\w*|\bעדר\s+נתונ\w*|חסרים\s+נתונ\w*|נתונים\s+חסרים|"
     r"נתונים\s+לא\s+זמינים"),
]


def get_banned_patterns() -> list[tuple[str, str]]:
    """Return the canonical (name, regex) banned-pattern families."""
    return list(BANNED_CONSUMER_PATTERNS)


# An identical sentence in MORE THAN this many products' free-prose copy = mass-templating.
SENTENCE_REPEAT_THRESHOLD = 10

# Canonical consumer-prose field paths (barcode prefix omitted).
#
# Coverage rule (TASK-576): exactly the AUTHORED editorial prose the site renders
# to a consumer — no more, no less. Each path is justified by a file:line citation
# in the React component that renders it (paths under bari-web/src/components/):
#   insightLine ................................ shared/comparison-row.tsx L282
#   rowVerdict ................................. shared/comparison-row.tsx L277 (+ expansion-section.tsx L1208)
#   consumerTakeaway ........................... shared/deep-dive-section.tsx TakeawayLine L175
#   expansion.comparisonContext ................ shared/expansion-section.tsx ShelfContextSection L721
#   expansion.positiveSignals[] ................ shared/expansion-section.tsx AssessmentSection L515
#   expansion.limitingFactors[] ................ shared/expansion-section.tsx AssessmentSection L580 (str or {text} item)
#   expansion.consumerExplanation.whyRated ..... shared/deep-dive-section.tsx L111
#   expansion.consumerExplanation.takeaway ..... shared/deep-dive-section.tsx TakeawayLine L282/175
#   expansion.consumerExplanation.context ...... shared/deep-dive-section.tsx L141
#   expansion.consumerExplanation.good[] ....... shared/deep-dive-section.tsx BulletList L126
#   expansion.consumerExplanation.watchOut[] ... shared/deep-dive-section.tsx BulletList L132
#   bariInterpretation[].interpretation ........ shared/deep-dive-section.tsx PillarRow L205
#
# Deliberately EXCLUDED (rendered, but structured UI-STATE / raw DATA, not authored
# prose — the owner ruling permits UI state to name data-state; only PROSE stays
# silent). Adding these would false-positive on legitimate UI affordances:
#   expansion.confidenceLabel .................. confidence UI chip (expansion-section.tsx L1137)
#   expansion.servingNote ...................... serving-size unit label (expansion-section.tsx L1238)
#   expansion.sourceLine ....................... mono source citation (expansion-section.tsx L1031)
#   expansion.ingredients ...................... raw scraped ingredient list, not authored (expansion-section.tsx L874)
#   expansion.nutrition ........................ numeric data, not prose
#   expansion.unknowns[] / .caveats[] .......... legacy glass-box data-state DISCLOSURE lists,
#                                                rendered under "מה שלא ניתן לאמת" — the UI-state
#                                                channel itself (expansion-section.tsx L1309/L1317)
#   expansion.bottomLine ....................... NOT rendered by any component (dead JSON key)
CONSUMER_PROSE_FIELDS: list[str] = [
    "insightLine",
    "rowVerdict",
    "consumerTakeaway",
    "expansion.comparisonContext",
    "expansion.positiveSignals[]",
    "expansion.limitingFactors[]",
    "expansion.consumerExplanation.whyRated",
    "expansion.consumerExplanation.takeaway",
    "expansion.consumerExplanation.context",
    "expansion.consumerExplanation.good[]",
    "expansion.consumerExplanation.watchOut[]",
    "bariInterpretation[].interpretation",
]

# Scalar free-prose fields for sentence-level repetition (CHECK 2).
# Excludes bariInterpretation (systematic dimension bank) and good[]/watchOut[]
# list slots (tier-cluster bullets may legitimately repeat — same scope as CHECK 4).
SENTENCE_REPEAT_FIELDS: frozenset[str] = frozenset({
    "insightLine",
    "rowVerdict",
    "consumerTakeaway",
    "expansion.consumerExplanation.whyRated",
    "expansion.consumerExplanation.takeaway",
    "expansion.consumerExplanation.context",
})

_AUTHOR_COPY_PATH = Path(__file__).resolve().parent / "author_copy.py"

# Candidate module-level constants to harvest for fingerprint sync (TASK-540 crash fix:
# never assume a name exists).
_FINGERPRINT_CONSTANT_NAMES: tuple[str, ...] = (
    "_STORY_DESC",
    "_DIM_INTERPRETATION_BASELINE",
    "_DIM_INTERPRETATION_PHRASES",
    "_STRENGTH_PHRASE",
    "_GRADE_LABEL",
)

# Hand-listed inline literals from author_copy.py (not stored as module constants).
_INLINE_AUTHOR_FINGERPRINTS: tuple[str, ...] = (
    "מוצר עם מאפייני עיבוד מורכבים — העיבוד הוא הנקודה הבולטת בהרכב",
    "ריכוז קלורי גבוה יחסית לקטגוריה",
    "תכולת סוכר גבוהה יחסית למדף",
    "מכיל ממתיק מוסף",
    "ערכים תזונתיים מתונים ביחס לקטגוריה",
    "תחושת שובע נמוכה יחסית — צפיפות תזונתית מוגבלת",
    "רשימת רכיבים ארוכה יחסית — מוצר עם רכיבים מרובים",
    "שמן צמחי מעובד ברשימת הרכיבים",
    "ללא תוספי מזון מזוהים — רשימת רכיבים נקייה",
    "מאפיינים תזונתיים לבחינה ביחס למדף",
    "מדורג ביחס לשאר מוצרי הקטגוריה לפי הרכב וערכים תזונתיים.",
    "מידת העיבוד של המוצר בולטת — פרמטרים הקשורים לתהליך הייצור ניכרים בהרכב.",
    "הצפיפות הקלורית גבוהה ביחס לקטגוריה.",
    "תכולת הסוכרים גבוהה ביחס למוצרים אחרים ברשימה.",
    "המוצר מכיל ממתיק מוסף ברשימת הרכיבים.",
    "הצפיפות התזונתית מתונה ביחס לאפשרויות האחרות.",
    "רשימת הרכיבים ארוכה יחסית — מספר רכיבים מרובה לעומת מוצרים פשוטים יותר.",
    "ללא תוספי מזון מזוהים — הרכב הרכיבים יחסית נקי.",
    "הציון מבוסס על שקלול כלל הפרמטרים הרלוונטיים לקטגוריה.",
    "מוצר שמתאפיין ביתרונות ברורים ביחס לחלק מהמתחרים.",
    "מוצר עם נקודות חוזק לצד גורמים הראויים לבחינה.",
    "ניתן למצוא אפשרויות עם פרופיל תזונתי עדיף ברשימה.",
    "ישנן אפשרויות עם פרופיל תזונתי טוב יותר זמינות ברשימה.",
    "יש לשקול את הנתונים ביחס לצרכים האישיים.",
    "מאפיינים תזונתיים לבחינה",
    "ללא תוספי מזון מזוהים ברשימת הרכיבים",
    "רמת עיבוד גבוהה יחסית לקטגוריה",
    "הציון מבטא מוצר שרמת עיבודו היא הגורם המרכזי בהערכה הכוללת.",
    "הציון מבטא מוצר עם צפיפות קלורית גבוהה ביחס לקטגוריה.",
    "הציון מבטא מוצר עם תכולת סוכרים גבוהה ביחס למדף.",
    "הציון מבטא מוצר המכיל ממתיק מוסף.",
    "הציון מבטא מוצר עם צפיפות תזונתית מתונה.",
    "הציון מבטא מוצר ללא תוספי מזון מזוהים ברשימת הרכיבים.",
    "מדורג לפי שקלול הרכב המוצר ביחס לקטגוריה.",
    "המוצר מתאפיין בפרמטרים ייחודיים לו ביחס לשאר הרשימה.",
    "נתון לא זמין",
)

# Distinctive _STORY_DESC keys safe for substring scan (short generic descriptors excluded).
_DISTINCTIVE_STORY_KEYS: frozenset[str] = frozenset({
    "processing_is_the_ceiling",
    "distance_from_whole_food",
    "heavy_processing_additives",
    "cap_bound",
    "unknown",
})

# ---------------------------------------------------------------------------
# Recite-vs-insight WARN check (TASK-546 prevention item #1).
#
# A consumer prose line that (a) contains >= RECITE_MIN_CHIP_TOKENS chip-value
# tokens (numbers tied to גרם / % / מ"ג / קלוריות / "ל-100 גרם" / a spelled-out
# or digit ingredient count) AND (b) contains NONE of RECITE_VERDICT_MARKERS is
# a data-dump: it just reads back the row's own chips with no verdict. This is
# a WARN/flag-for-author-review signal, not a hard fail (validate_copy_authored.py
# CHECK 5) — near-zero false positives, tuned against the 12 pre-fix yogurt
# rowVerdicts (must all be flagged) vs. the 67 owner-approved yogurt
# rowVerdict/insightLine/consumerTakeaway lines (target: 0 false positives,
# achieved 8/201 — see _fixtures/recite_negative.txt and the validator's
# --selftest for the confusion-matrix proof).
# ---------------------------------------------------------------------------

RECITE_MIN_CHIP_TOKENS: int = 2

# Fields eligible for the recite-vs-insight scan (short field name, no barcode prefix).
RECITE_CHECK_FIELDS: frozenset[str] = frozenset({
    "rowVerdict",
    "insightLine",
    "consumerTakeaway",
})

# Spelled-out Hebrew ingredient counts ("שני/שלושה/... רכיבים"). Multi-word
# numbers ("אחד עשר" etc.) are listed before their single-word prefixes so the
# regex alternation (first-match-wins per position) doesn't truncate them.
_SPELLED_INGREDIENT_COUNTS: str = (
    "שנים עשר|שלושה עשר|ארבעה עשר|חמישה עשר|שישה עשר|אחד עשר|"
    "שני|שתי|שלושה|שלוש|ארבעה|ארבע|חמישה|חמש|שישה|שש|שבעה|שבע|"
    "שמונה|תשעה|תשע|עשרה|עשר"
)

# Chip-value token patterns (raw regex strings — validator compiles them).
# A "chip token" is a number the row's own UI chips already show elsewhere
# (grams, percent, mg, calories, per-100g framing, or an ingredient count) —
# reciting >=2 of these with no judgment word is the data-dump defect.
RECITE_CHIP_TOKEN_PATTERNS: list[str] = [
    r"ל-?100\s*גרם",
    r"\d+(?:\.\d+)?\s*%",
    r'\d+(?:\.\d+)?\s*(?:מ"ג|מ״ג|מג)',
    r"\d+(?:\.\d+)?\s*גרם",
    r"\d+(?:\.\d+)?\s*קלוריות",
    r"\d+\s*רכיבים",
    rf"(?:{_SPELLED_INGREDIENT_COUNTS})\s*רכיבים",
]

# Verdict-marker lexicon — words/phrases that signal a judgment, comparison,
# tradeoff, causal explanation, or use-case framing rather than a plain list.
# Seeded from the owner-validated GOOD yogurt copy and tuned against the 12
# pre-fix NEGATIVE rowVerdicts (zero of these markers appear in any of the 12 —
# do not add a marker without re-running the validator's --selftest first).
RECITE_VERDICT_MARKERS: list[str] = [
    "אבל", "יחסית", "צנוע", "צנועה", "נוטה", "דוחף", "דוחפת", "מתפקד",
    "קינוח", "מקור", "בזכות", "מספיק", "למרות", "פונקציונלית",
    "בטווח הרגיל", "הטווח הרגיל", "על חשבון", "אמיתי", "אמיתית", "אמיתיים",
    "כמעט סמלית", "מעבר ל", "גבוה", "גבוהה", "נמוך", "נמוכה",
    "קרוב ל", "כדי ל", "בעוד", "לעומת", "יותר מ", "פחות מ",
    "עדיין", "במקום", "בלי", "מול", "אפס",
    "מתחת", "פשוט", "מייצר", "יוצר",
    "מינימלי", "תרגיל שיווקי",
]


def get_banned_phrases() -> list[str]:
    """Return the canonical banned-phrase list."""
    return list(BANNED_CONSUMER_PHRASES)


def _flatten_strings(obj) -> list[str]:
    """Recursively collect str leaves from dicts/lists."""
    out: list[str] = []
    if isinstance(obj, str) and obj.strip():
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(_flatten_strings(v))
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out.extend(_flatten_strings(v))
    return out


def _load_author_copy_module():
    spec = importlib.util.spec_from_file_location("author_copy", _AUTHOR_COPY_PATH)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_author_copy_fingerprints() -> list[str]:
    """
    Harvest baseline scaffold phrases from author_copy.py constants.
    Never raises — missing constant names are skipped (TASK-540).

    Only distinctive _STORY_DESC tags and legacy baseline banks are harvested.
    _DIM_INTERPRETATION_PHRASES is the production dimension panel bank and is
    intentionally excluded from substring fingerprints (would false-positive on
    legitimately authored pages).
    """
    phrases: list[str] = []
    mod = _load_author_copy_module()
    if mod is not None:
        story_desc = getattr(mod, "_STORY_DESC", None)
        if isinstance(story_desc, dict):
            for k in _DISTINCTIVE_STORY_KEYS:
                if k in story_desc and isinstance(story_desc[k], str):
                    phrases.append(story_desc[k])
        # Legacy baseline-only banks (absent in TASK-538+ author_copy — skip silently).
        for legacy_name in ("_DIM_INTERPRETATION_BASELINE", "_STRENGTH_PHRASE"):
            val = getattr(mod, legacy_name, None)
            if val is not None:
                phrases.extend(_flatten_strings(val))

    phrases.extend(_INLINE_AUTHOR_FINGERPRINTS)
    return sorted({p for p in phrases if p}, key=len, reverse=True)


def get_recite_verdict_markers() -> list[str]:
    """Return the canonical verdict-marker lexicon (recite-vs-insight WARN check)."""
    return list(RECITE_VERDICT_MARKERS)


def get_recite_chip_token_patterns() -> list[str]:
    """Return the canonical chip-value regex pattern strings (uncompiled)."""
    return list(RECITE_CHIP_TOKEN_PATTERNS)