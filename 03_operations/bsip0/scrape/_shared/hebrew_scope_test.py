"""
BSIP0 Hebrew Scope Test — TASK-362 (owner-mandated; Orchestrator-defined).

WHY THIS EXISTS (the finding): the snacks corpus kept admitting the WRONG products
and dropping the RIGHT ones. Chocolate candy bars (Pesek Zman), salty snacks, and
raw oats leaked IN; real grain bars got dropped because curation pinned the display
set to hardcoded snk-NNN ids in a stale module. Both failures are the same root
cause: there was no single, explicit, Hebrew-language definition of what is IN the
category. Ad-hoc INCLUDE/EXCLUDE strings lived inside each scraper and each curation
script, drifting apart.

THE FIX: the Orchestrator (Opus) DEFINES the scope of each category ONCE, here, in
Hebrew, as a ScopeDefinition. Every stage — the scraper's filter, BSIP1 curation,
and the conformance gate — calls THIS test. Corpus membership has exactly one
authority. A product is IN the category iff this test says so; nothing is added or
dropped on an id technicality.

Contract: scope_test(name_he, ingredients_he, definition) -> ScopeResult
  verdict ∈ {IN_SCOPE, OUT_OF_SCOPE, AMBIGUOUS}
  - OUT_OF_SCOPE: hit a disqualifier (adjacent category) — never admit.
  - IN_SCOPE:     hit a required marker AND no disqualifier.
  - AMBIGUOUS:    no marker and no disqualifier — Orchestrator reviews; never silently admit.

This is a NECESSARY gate, not the whole of curation: it decides membership. Ranking,
dedup, and per-100g plausibility (plausibility_gate.py) are separate and still apply.
OFF is never a source here or anywhere.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Scope(str, Enum):
    IN_SCOPE = "IN_SCOPE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass
class ScopeDefinition:
    """Orchestrator-authored, per-category. All tokens are Hebrew (or brand latin)."""
    category: str
    # at least one REQUIRED marker must appear in name (or ingredients) to be in-scope.
    required_markers: list[str]
    # any DISQUALIFIER (adjacent category) forces OUT_OF_SCOPE even if a marker matched.
    disqualifiers: list[str]
    # conditional disqualifiers: (token, override_tokens). Disqualify if `token`
    # appears UNLESS one of `override_tokens` also appears. Encodes "גרנולה is OUT
    # (it has its own page) UNLESS it's a חטיף/בר form". A plain substring list
    # can't express this; this is how an adjacent category that shares a word with
    # us (loose granola vs granola BAR) is separated.
    conditional_disqualifiers: list[tuple[str, list[str]]] = field(default_factory=list)
    # optional: tokens that, in the NAME, strengthen in-scope (tie-breakers for AMBIGUOUS).
    supporting_markers: list[str] = field(default_factory=list)
    # where to look for required_markers: "name" | "name_or_ingredients"
    marker_source: str = "name_or_ingredients"
    notes: str = ""


@dataclass
class ScopeResult:
    verdict: Scope
    category: str
    matched_marker: str | None = None
    matched_disqualifier: str | None = None
    reason: str = ""


import re as _re

# Word-boundary matcher. Naive substring matching is unsafe for Hebrew: the matzo
# token 'מציות' is a substring of 'חומציות' (acidity regulator, in almost every
# ingredient list), which mass-rejected real protein bars. We require the token to
# sit at a word boundary — not preceded/followed by another letter or digit. \w in
# Python's Unicode regex includes Hebrew letters, so this works for both scripts.
def _has(text: str, tokens: list[str]) -> str | None:
    low = (text or "").lower()
    for t in tokens:
        tok = t.strip().lower()
        if not tok:
            continue
        if _re.search(r"(?<!\w)" + _re.escape(tok) + r"(?!\w)", low):
            return t
    return None


def scope_test(name_he: str, ingredients_he: str, definition: ScopeDefinition) -> ScopeResult:
    name = name_he or ""
    ingr = ingredients_he or ""
    hay_name = name
    hay_full = name + " || " + ingr

    # 1) disqualifier wins, always (adjacent category — e.g. chocolate candy, salty)
    dq = _has(hay_name, definition.disqualifiers) or _has(ingr, definition.disqualifiers)
    if dq:
        return ScopeResult(Scope.OUT_OF_SCOPE, definition.category, matched_disqualifier=dq,
                           reason=f"disqualifier '{dq}' (adjacent category)")

    # 1b) conditional disqualifiers: token present (in NAME) AND no override → OUT.
    for tok, overrides in definition.conditional_disqualifiers:
        if _has(hay_name, [tok]) and not _has(hay_name, overrides):
            return ScopeResult(Scope.OUT_OF_SCOPE, definition.category, matched_disqualifier=tok,
                               reason=f"conditional disqualifier '{tok}' without form-marker "
                                      f"({'/'.join(overrides)}) — adjacent category")

    # 2) required marker
    src = hay_full if definition.marker_source == "name_or_ingredients" else hay_name
    mk = _has(src, definition.required_markers)
    if mk:
        return ScopeResult(Scope.IN_SCOPE, definition.category, matched_marker=mk,
                           reason=f"required marker '{mk}'")

    # 3) supporting marker -> still ambiguous-leaning-in, but flagged for review
    sm = _has(hay_name, definition.supporting_markers)
    if sm:
        return ScopeResult(Scope.AMBIGUOUS, definition.category, matched_marker=sm,
                           reason=f"only supporting marker '{sm}', no required marker — review")

    return ScopeResult(Scope.AMBIGUOUS, definition.category,
                       reason="no required marker and no disqualifier — review")


# ── Canonical scope definitions (Orchestrator-authored). Add one per category. ──

BAR_SHELF = ScopeDefinition(
    category="bar_shelf",
    # a BAR in the snack/protein sense
    required_markers=[
        "חטיף", "חטיפי", "מאגדת", " bar", "בר חלבון", "בר דגנים", "בר אנרגיה",
        "חלבון", "פרוטאין", "protein", "גרנולה בר",
    ],
    # adjacent categories that must NEVER be admitted to the bar shelf
    disqualifiers=[
        # chocolate candy bars (owner: "Pesek Zman is a chocolate bar, not a snack bar")
        "פסק זמן", "קיט קט", "kitkat", "kit kat", "טוויקס", "twix", "מארס", "mars",
        "סניקרס", "snickers", "באונטי", "bounty", "מילקי", "milky", "כיף כף",
        "טבלת שוקולד", "שוקולד פרה", "פרה חלב", "לוקר", "loacker",
        # salty snacks
        "במבה", "ביסלי", "תפוצ'יפס", "צ'יפס", "chips", "פופקורן", "popcorn",
        "חטיף תירס", "דוריטוס", "doritos", "פרינגלס", "אפרופו",
        # crackers / wafers / cookies / rice cakes / candy
        "קרקר", "cracker", "ופל", "wafer", "עוגיו", "עוגית", "ביסקוויט",
        "פריכית", "פריכיות", "מציות", "rice cake", "קרמבו", "סוכריות",
        # drinks / dairy / baby / powders / spreads-in-a-jar
        "משקה", "drink", "שתיה", "יוגורט", "yogurt", "מעדן", "אבקת חלבון",
        "שייק", "shake", "דייסת תינוק", "מטרנה", "ממרח", "צנצנת",
        # raw commodity (not a bar)
        "שיבולת שועל 500", "קוואקר 500", "גריסים", "קמח שיבולת",
        # protein noodles / pasta — share 'חלבון' with protein bars but are NOT bars
        "נודלס", "noodle", "אטריות", "פסטה", "ספגטי",
    ],
    conditional_disqualifiers=[
        # loose granola has its OWN page — only a granola BAR/חטיף belongs here
        ("גרנולה", ["חטיף", "בר ", "בר-", "מאגדת"]),
        # loose muesli likewise
        ("מוזלי", ["חטיף", "בר ", "מאגדת"]),
    ],
    supporting_markers=["דגנים", "שיבולת שועל", "תמרים", "אנרגיה", "פיטנס", "fitness"],
    marker_source="name_or_ingredients",
    notes=("Bar shelf = snack bars + protein bars in ONE scope. The protein-vs-snack "
           "split is a SEPARATE step (plausibility_gate.classify_bar: protein>=20g/100g "
           "or name marks חלבון/פרוטאין). Owner: snacks category is ONLY snack bars."),
)

SCOPE_DEFINITIONS = {"bar_shelf": BAR_SHELF}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cases = [
        ("חטיף חלבון אגוזי לוז פנגיאה", "", Scope.IN_SCOPE),
        ("נייטשר וואלי חטיף שיבולת שועל עם דבש", "", Scope.IN_SCOPE),
        ("פסק זמן חטיף שוקולד", "", Scope.OUT_OF_SCOPE),     # chocolate candy (looks like חטיף!)
        ("ביסלי גריל", "", Scope.OUT_OF_SCOPE),               # salty
        ("שיבולת שועל קוואקר 500 גרם", "", Scope.OUT_OF_SCOPE),  # raw commodity
        ("עוגיות שוקולד צ'יפס", "", Scope.OUT_OF_SCOPE),       # cookies
        ("מאגדת דגנים מצופה שוקולד", "", Scope.IN_SCOPE),
        ("שוקולד מריר 70%", "סוכר, מסת קקאו", Scope.AMBIGUOUS),  # no marker, no DQ -> review
        ("נודלס חלבון בטעם בקר", "", Scope.OUT_OF_SCOPE),        # protein NOODLES, not a bar
        ("גרנולה פרוטאין שוקולד", "", Scope.OUT_OF_SCOPE),       # loose granola (own page)
        ("גרנולה 18% חלבון", "", Scope.OUT_OF_SCOPE),            # loose granola bag
        ("חטיף גרנולה דבש", "", Scope.IN_SCOPE),                 # granola BAR — belongs here
    ]
    ok = True
    for name, ingr, want in cases:
        r = scope_test(name, ingr, BAR_SHELF)
        flag = "OK " if r.verdict == want else "FAIL"
        if r.verdict != want:
            ok = False
        print(f"  [{flag}] {r.verdict.value:13} want {want.value:13} | {name[:34]:34} | {r.reason}")
    print("scope-test self-test", "PASS" if ok else "FAILED")
    assert ok
