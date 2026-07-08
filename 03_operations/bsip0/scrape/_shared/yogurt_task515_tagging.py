"""
TASK-515 yogurt subpool classifier — the SINGLE authority for spoonable/drinkable/
edge-case tagging across all three retailer scrapers (Shufersal, Victory, Yohananof).

Why this exists: the Shufersal boundary query "לבנה" (intended to find labneh)
mostly matched "גבינה לבנה" (white/farmer cheese — a DIFFERENT dairy product, not
yogurt) and one frozen-white-beans false positive ("שעועית לבנה"). This is the same
failure class the BSIP0 playbook's Stage-3 scope test exists to prevent (keyword
collision admits an adjacent category) — caught here before BSIP1, per the
missing_data_discard_rule / scope-authority discipline. True labneh in Israeli
retail is spelled "לאבנה" (with aleph); bare "לבנה" is far more often the feminine
adjective "white" attached to "גבינה" (cheese) or an unrelated noun.

Mid-run scope change (coordinator, 2026-07-05): drinkable yogurt is now a
FIRST-CLASS subpool (its own future comparison page), not a boundary maybe-exclude.
kefir and labneh remain true edge cases routed to a Nutrition/Product ruling.
Cottage cheese is out-of-scope entirely (dedicated corpus elsewhere) and is not
re-included here even if a query incidentally surfaces it.

Output per product: {"subpool": "spoonable"|"drinkable"|None,
                      "edge_case_flag": None|"kefir"|"labneh",
                      "out_of_scope_reason": None|"cheese_not_yogurt"|
                                              "commodity_not_dairy"|
                                              "cottage_excluded_dedicated_corpus"}
subpool is None only when out_of_scope_reason is set (product does not enter
either page's corpus at all).
"""
from __future__ import annotations

LABNEH_MARKERS = ["לאבנה", "labneh", "labne"]
# Bare "לבנה" is admitted as labneh ONLY with a corroborating labneh-context token
# (za'atar / olive oil topping is the classic Israeli labneh serving) and NOT if
# it co-occurs with cheese/commodity markers that mean something else entirely.
LABNEH_WEAK_MARKER = "לבנה"
LABNEH_CONTEXT_OK = ["זעתר", "שמן זית", "עיזים"]

CHEESE_NOT_YOGURT = ["גבינה לבנה", "גבינת לבנה", "גבינה", "גבינת", "סקי "]
COMMODITY_NOT_DAIRY = ["שעועית", "בין", "beans"]
COTTAGE_MARKERS = ["קוטג", "cottage"]

KEFIR_MARKERS = ["קפיר", "kefir"]

DRINKABLE_MARKERS = [
    "לשתייה", "לשתיה", "משקה יוגורט", "משקה אקטיביה", "אקטימל", "actimel",
    "דנאקטיב", "danactive", "לאסי", "lassi", "אירן", "ayran", "שייק", "shake",
    "שטוזים", "drink", "ציזיקי לשתיה",
]

SPOONABLE_POSITIVE = [
    "יוגורט", "yogurt", "yoghurt", "יווני", "greek", "סקיר", "skyr",
    "אקטיביה", "activia", "ביו", "bio", "מולר", "muller", "müller",
    "יופלה", "yoplait", "דנונה", "danone", "פרופ", "froop", "תנובה",
    "שטראוס", "פרו", "go ",
]


def classify(name_he: str) -> dict:
    nl = (name_he or "").strip()
    nll = nl.lower()

    # 1) Out-of-scope hard exclusions first (checked before any yogurt-ish marker,
    #    since these are adjacent categories that must never enter either subpool).
    if any(m in nl for m in COTTAGE_MARKERS) or any(m in nll for m in COTTAGE_MARKERS):
        return {"subpool": None, "edge_case_flag": None,
                "out_of_scope_reason": "cottage_excluded_dedicated_corpus"}

    if any(m in nl for m in COMMODITY_NOT_DAIRY):
        return {"subpool": None, "edge_case_flag": None,
                "out_of_scope_reason": "commodity_not_dairy"}

    # 2) Labneh (true edge case) — check the strong (unambiguous) spelling first.
    if any(m in nl or m in nll for m in LABNEH_MARKERS):
        return {"subpool": "spoonable", "edge_case_flag": "labneh", "out_of_scope_reason": None}

    if LABNEH_WEAK_MARKER in nl:
        if any(m in nl for m in CHEESE_NOT_YOGURT):
            # "גבינה לבנה" / "גבינת סקי" etc — white/soft CHEESE, not yogurt or labneh.
            return {"subpool": None, "edge_case_flag": None,
                     "out_of_scope_reason": "cheese_not_yogurt"}
        if any(m in nl for m in LABNEH_CONTEXT_OK):
            # "לבנה עם זעתר" style — no cheese marker, has labneh-serving context.
            return {"subpool": "spoonable", "edge_case_flag": "labneh", "out_of_scope_reason": None}
        # Bare "לבנה" with no corroborating context and no cheese marker either —
        # ambiguous; do not guess. Treat as out-of-scope rather than fabricate a tag.
        return {"subpool": None, "edge_case_flag": None,
                 "out_of_scope_reason": "cheese_not_yogurt"}

    # 3) Kefir (true edge case) — drinkable in practice but fermented-distinct;
    #    Nutrition/Product rules which subpool (or a third page) it belongs to.
    if any(m in nll for m in KEFIR_MARKERS):
        return {"subpool": "drinkable", "edge_case_flag": "kefir", "out_of_scope_reason": None}

    # 4) Drinkable — first-class subpool.
    if any(m in nl or m in nll for m in DRINKABLE_MARKERS):
        return {"subpool": "drinkable", "edge_case_flag": None, "out_of_scope_reason": None}

    # 5) Spoonable — default yogurt-shelf membership.
    if any(m in nl or m in nll for m in SPOONABLE_POSITIVE):
        return {"subpool": "spoonable", "edge_case_flag": None, "out_of_scope_reason": None}

    # No positive signal at all — should not normally reach here (upstream scrapers
    # already name-gated), but never silently admit; mark out-of-scope for review.
    return {"subpool": None, "edge_case_flag": None, "out_of_scope_reason": "no_positive_signal"}


def retag_records(records: list[dict], name_field: str = "name_he") -> tuple[list[dict], list[dict]]:
    """Split records into (kept, rejected) using classify(). Mutates each kept
    record in place, adding subpool/edge_case_flag keys. Rejected records keep
    their out_of_scope_reason for the run's audit trail — never silently dropped."""
    kept, rejected = [], []
    for rec in records:
        name = rec.get(name_field) or rec.get("name") or ""
        tag = classify(name)
        rec["subpool"] = tag["subpool"]
        rec["edge_case_flag"] = tag["edge_case_flag"]
        rec["out_of_scope_reason"] = tag["out_of_scope_reason"]
        if tag["subpool"] is None:
            rejected.append(rec)
        else:
            kept.append(rec)
    return kept, rejected
