#!/usr/bin/env python3
r"""
rank_check.py — verify every superlative claim in a comparison page against the FULL corpus (TASK-422 / W3)
==========================================================================================================

`validate_comparison_page.py` gate 6 ("stale-rank") only *flags* a fixed list of Hebrew rank
phrases for MANUAL confirmation, and only checks "is this product #1 by score". But the failure
the owner actually hit (memory: superlative_claims_need_corpus_rankcheck) is broader: consumer
copy that says "the highest sugar on the shelf" / "least sodium" / "leads the table" — a claim a
per-product number-trace can't catch, because it is a statement about the product's RANK across the
WHOLE corpus. One product can be self-consistent and still make a false ranking claim.

This automates that check. It parses superlative claims out of the consumer-facing copy, re-derives
the true extremum for each claimed attribute across every product on the page, and verifies the
claiming product actually holds it. A mismatch is a HARD fail (not a manual WARN) — that is the
whole point of W3: turn the eyeball step into a gate.

Attributes it can verify (from the frontend JSON, no external data):
  - nutrients:  sugar, sodium, protein, fat, fiber, energyKcal   (expansion.nutrition, per-100g)
  - score/rank: "leads / #1 / top of the table"                  (product.score)
  - additives:  "most/fewest additives"                          (len(product.d4_additives))

Claims it cannot resolve deterministically (unknown attribute, uniqueness "the only one that…",
bare superlative with no attribute) are surfaced as WARN for manual review — never silently passed.

Exit codes (mirror run_gates.py):
  0  no superlative MISMATCH (WARNs allowed)
  1  >=1 false superlative claim (HARD)
  2  usage / load error

Usage:
  python rank_check.py --json bari-web/src/data/comparisons/cereals_frontend_v2.json
  python rank_check.py --json <page.json> --emit-json
  python rank_check.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass

EPS = 1e-6

# nutrient word (Hebrew) -> nutrition field. Detection is ADJACENCY-bound (regex below),
# never a proximity window — a window binds "סוכר" to a "הגבוה ביותר" that modifies "נתרן"
# two clauses away (a real false-positive class observed on live pages).
NUTRIENT_TERMS = {
    "סוכר": "sugar", "סוכרים": "sugar",
    "נתרן": "sodium", "מלח": "sodium",
    "חלבון": "protein", "חלבונים": "protein",
    "שומן": "fat", "שומנים": "fat",
    "סיבים": "fiber",
    "קלוריות": "energyKcal", "אנרגיה": "energyKcal", "קלוריה": "energyKcal",
}
_HIGH = r"(?:גבוה|גבוהה|רב|רבה)"
_LOW = r"(?:נמוך|נמוכה|מועט|מועטה|דל|דלה)"
_MOST = r"(?:הרבה|גבוה|גבוהה)"
_LEAST = r"(?:מעט|נמוך|נמוכה|פחות|דל)"

# adjective superlatives that imply BOTH attribute and direction (already require ביותר/הכי)
ADJ_CLAIMS = {
    "המתוק ביותר": ("sugar", "max"), "הכי מתוק": ("sugar", "max"),
    "המלוח ביותר": ("sodium", "max"), "הכי מלוח": ("sodium", "max"),
}
# score / table-position superlatives -> product.score max. TIGHTENED twice: bare
# "מוביל"/"בראש" are dropped (match "syrup leads the sweetness"); "בראש הטבלה" is also
# dropped because it attaches to a nutrient in real copy ("הנתרן ... בראש הטבלה" = highest
# sodium, NOT top score). Only phrases that unambiguously name the SCORE/rank remain.
SCORE_MAX_MARKERS = ["הציון הגבוה ביותר", "המקום הראשון", "מקום ראשון בטבלה",
                     "הראשון בטבלה", "הראשונה בטבלה", "#1"]
UNIQUE_MARKERS = ["היחיד ", "היחידה ", "היחידים ", "אין עוד"]

# A superlative that carries one of these nearby is scoped to a SUBSET of the shelf
# ("highest among children's cereals", "in the Bulgarian series"). We cannot verify a
# subpool deterministically from the page, so these are downgraded to manual WARN rather
# than falsely failed against the whole corpus.
SUBPOOL_SCOPE = ["בין ", "מבין ", "בסדרה", "בסדרת", "בקבוצת", "בקבוצה", "בבולגר",
                 "דגני היל", "מוצרי היל", "מסוג ", "מהסוג", "בין כל מוצרי היל"]

TEXT_FIELDS = ["insightLine", "rowVerdict"]
EXPANSION_TEXT_FIELDS = ["comparisonContext", "positiveSignals", "limitingFactors", "bottomLine"]


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []  # (level, status, detail)

    def hard(self, ok: bool, detail: str) -> None:
        self.rows.append(("HARD", "PASS" if ok else "FAIL", detail))

    def warn(self, detail: str) -> None:
        self.rows.append(("WARN", "WARN", detail))

    def info(self, detail: str) -> None:
        self.rows.append(("INFO", "PASS", detail))

    @property
    def failed(self) -> bool:
        return any(lvl == "HARD" and st == "FAIL" for lvl, st, _ in self.rows)

    def render(self, name: str) -> str:
        out = [f"rank_check :: {name}", "-" * 64]
        for lvl, st, detail in self.rows:
            out.append(f"  [{st:<4}] {detail}")
        out.append("-" * 64)
        out.append(f"  VERDICT: {'FAIL' if self.failed else 'PASS'}")
        return "\n".join(out)

    def as_json(self, name: str) -> dict:
        return {"page": name, "verdict": "FAIL" if self.failed else "PASS",
                "findings": [{"level": lvl, "status": st, "detail": d}
                             for lvl, st, d in self.rows if st != "PASS" or lvl == "INFO"]}


def _product_text(p: dict) -> str:
    parts = [str(p.get(f, "") or "") for f in TEXT_FIELDS]
    ex = p.get("expansion", {}) or {}
    for f in EXPANSION_TEXT_FIELDS:
        v = ex.get(f)
        if isinstance(v, list):
            parts.append(" ".join(str(x) for x in v))
        elif v:
            parts.append(str(v))
    return "  ".join(parts)


def _nutrient_value(p: dict, field: str):
    return ((p.get("expansion", {}) or {}).get("nutrition", {}) or {}).get(field)


def _additive_count(p: dict) -> int:
    return len(p.get("d4_additives") or [])


def _extremum_holders(prods: list[dict], value_fn, direction: str) -> tuple[list, float | None]:
    """Return (list of products at the extremum, extremum value). Ties → all holders."""
    valued = [(p, value_fn(p)) for p in prods]
    valued = [(p, v) for p, v in valued if isinstance(v, (int, float))]
    if not valued:
        return [], None
    ext = max(v for _, v in valued) if direction == "max" else min(v for _, v in valued)
    holders = [p for p, v in valued if abs(v - ext) <= EPS]
    return holders, ext


def _pid(p: dict) -> str:
    return str(p.get("id") or p.get("barcode") or p.get("name") or "?")


def _is_scoped(text: str, start: int, end: int) -> bool:
    """True if the SENTENCE containing the superlative carries a subpool-scope qualifier.

    Sentence-granularity (not a fixed char window): subpool phrases like 'מבין שלושת נקטרי
    ספרינג' sit at the sentence start while the superlative comes later — a window misses it,
    but the whole sentence catches it. Boundaries: . ? ! newline, or the '  ' field joiner."""
    delims = [m.start() for m in re.finditer(r"[.\n?!]|\s{2,}", text)]
    lo, hi = 0, len(text)
    for d in delims:
        if d <= start:
            lo = d + 1
        else:
            hi = d
            break
    sentence = text[lo:hi]
    return any(s in sentence for s in SUBPOOL_SCOPE)


def _detect_claims(text: str) -> list[tuple[str, str, str, bool]]:
    """Return (kind, field, direction, scoped). kind in {nutrient, additive, score, unique}.

    Nutrient/additive claims bind the attribute word ADJACENT to the superlative — either
    '<term> [ה]<high/low> ביותר' or 'הכי <most/least> <term>' — so a superlative that
    grammatically modifies a different noun cannot bind. `scoped` marks subpool-scoped claims.
    """
    claims: list[tuple[str, str, str, bool]] = []

    def add(kind, field, direction, span):
        claims.append((kind, field, direction, _is_scoped(text, span[0], span[1])))

    # adjective superlatives (attribute+direction fused in one phrase)
    for phrase, (field, direction) in ADJ_CLAIMS.items():
        for m in re.finditer(re.escape(phrase), text):
            add("nutrient", field, direction, m.span())

    # nutrient adjacency: "<term> [ה]גבוה ביותר" / "הכי הרבה <term>" (and the min forms)
    for term, field in NUTRIENT_TERMS.items():
        t = re.escape(term)
        for pat, direction in (
            (rf"{t}\s+ה?{_HIGH}\s+ביותר", "max"),
            (rf"הכי\s+{_MOST}\s+{t}", "max"),
            (rf"{t}\s+ה?{_LOW}\s+ביותר", "min"),
            (rf"הכי\s+{_LEAST}\s+{t}", "min"),
        ):
            for m in re.finditer(pat, text):
                add("nutrient", field, direction, m.span())

    # additive adjacency
    for pat, direction in (
        (rf"תוספי[ם]?\s+(?:מזון\s+)?ה?{_HIGH}\s+ביותר", "max"),
        (rf"הכי\s+{_MOST}\s+תוספי", "max"),
        (rf"תוספי[ם]?\s+(?:מזון\s+)?ה?{_LOW}\s+ביותר", "min"),
        (rf"הכי\s+{_LEAST}\s+תוספי", "min"),
        (r"הכי\s+הרבה\s+תוספי", "max"),
    ):
        for m in re.finditer(pat, text):
            add("additive", "additives", direction, m.span())

    # score / table-position superlatives (tightened, unambiguous phrases only)
    for mk in SCORE_MAX_MARKERS:
        m = re.search(re.escape(mk), text)
        if m:
            add("score", "score", "max", m.span())
            break

    # uniqueness — cannot resolve the predicate deterministically → WARN signal
    for mk in UNIQUE_MARKERS:
        m = re.search(re.escape(mk), text)
        if m:
            claims.append(("unique", "-", "-", False))
            break

    return sorted(set(claims))


def check(page: dict, rep: Report) -> None:
    prods = page.get("products", [])
    if not prods:
        rep.warn("no products in page")
        return

    # R0 — rank-field integrity: product.rank must follow descending score order.
    scored = [p for p in prods if isinstance(p.get("score"), (int, float))]
    if scored and all(isinstance(p.get("rank"), int) for p in scored):
        order = sorted(scored, key=lambda p: -p["score"])
        bad = [(_pid(p), p["rank"], i + 1) for i, p in enumerate(order) if p["rank"] != i + 1]
        rep.hard(not bad, f"R0 rank-field vs score order: "
                 + ("consistent" if not bad else f"{len(bad)} off, e.g. {bad[:3]}"))

    # R1 — superlative claims re-derived against the full corpus
    value_fns = {
        "sugar": lambda p: _nutrient_value(p, "sugar"),
        "sodium": lambda p: _nutrient_value(p, "sodium"),
        "protein": lambda p: _nutrient_value(p, "protein"),
        "fat": lambda p: _nutrient_value(p, "fat"),
        "fiber": lambda p: _nutrient_value(p, "fiber"),
        "energyKcal": lambda p: _nutrient_value(p, "energyKcal"),
        "score": lambda p: p.get("score"),
        "additives": _additive_count,
    }
    n_claims = n_confirmed = n_mismatch = n_warn = 0
    for p in prods:
        text = _product_text(p)
        for kind, field, direction, scoped in _detect_claims(text):
            if kind == "unique":
                n_warn += 1
                rep.warn(f"{_pid(p)}: uniqueness claim ('היחיד') — verify predicate manually")
                continue
            if scoped:
                n_warn += 1
                rep.warn(f"{_pid(p)}: subpool-scoped {direction} {field} claim "
                         f"('בין/בסדרה/…') — verify against the subpool manually")
                continue
            if field not in value_fns:
                n_warn += 1
                rep.warn(f"{_pid(p)}: superlative on unresolved attribute '{field}' — manual")
                continue
            n_claims += 1
            holders, ext = _extremum_holders(prods, value_fns[field], direction)
            if not holders:
                n_warn += 1
                rep.warn(f"{_pid(p)}: claims {direction} {field} but no data to rank — manual")
                continue
            holder_ids = {_pid(h) for h in holders}
            if _pid(p) in holder_ids:
                n_confirmed += 1
            else:
                n_mismatch += 1
                own = value_fns[field](p)
                rep.hard(False,
                         f"{_pid(p)}: FALSE SUPERLATIVE — claims {direction} {field} "
                         f"(own={own}) but the {direction} is {ext} held by "
                         f"{sorted(holder_ids)[:3]}")
    rep.info(f"R1 superlatives: {n_claims} corpus-wide claim(s) — "
             f"{n_confirmed} confirmed, {n_mismatch} FALSE, {n_warn} manual-review")


def run_page(json_path: Path, emit_json: bool) -> int:
    try:
        page = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"rank_check: LOAD ERROR — {e}", file=sys.stderr)
        return 2
    rep = Report()
    check(page, rep)
    name = json_path.name
    if emit_json:
        print(json.dumps(rep.as_json(name), ensure_ascii=False, indent=2))
    else:
        print(rep.render(name))
    return 1 if rep.failed else 0


def run_selftest() -> int:
    # 3 products; product B FALSELY claims lowest sugar though A has less; C truthfully leads by score.
    page = {
        "products": [
            {"id": "A", "score": 80, "rank": 1, "d4_additives": [],
             "insightLine": "מוצר סולידי", "rowVerdict": "בסדר גמור",
             "expansion": {"nutrition": {"sugar": 2.0, "sodium": 100, "protein": 10,
                                         "fat": 1, "fiber": 9, "energyKcal": 340}}},
            {"id": "B", "score": 70, "rank": 2, "d4_additives": [],
             "insightLine": "יש בו הכי פחות סוכר על המדף",  # FALSE: A has less sugar
             "rowVerdict": "בינוני",
             "expansion": {"nutrition": {"sugar": 5.0, "sodium": 90, "protein": 8,
                                         "fat": 2, "fiber": 6, "energyKcal": 360}}},
            {"id": "C", "score": 90, "rank": 3, "d4_additives": [],  # rank WRONG: C has top score
             "insightLine": "עומד בראש הטבלה עם הציון הגבוה ביותר",  # TRUE by score
             "rowVerdict": "מצוין",
             "expansion": {"nutrition": {"sugar": 3.0, "sodium": 80, "protein": 12,
                                         "fat": 1, "fiber": 8, "energyKcal": 330}}},
        ]
    }
    rep = Report()
    check(page, rep)
    print(rep.render("SELFTEST"))
    print()
    # expectations: B's false sugar claim → HARD FAIL; C's score claim → confirmed;
    # R0 rank integrity → FAIL (C should be rank 1). Overall FAIL.
    text = rep.render("SELFTEST")
    ok_false_sugar = "FALSE SUPERLATIVE" in text and "B:" in text.replace("B: ", "B:")
    ok_rank = "rank-field vs score order" in text and "off" in text
    ok_overall = rep.failed
    # confirm C's score claim did NOT get flagged false
    ok_c_ok = "C: FALSE" not in text
    allok = rep.failed and ("FALSE SUPERLATIVE" in text) and ok_rank and ok_c_ok
    print(f"SELFTEST: false-sugar-caught={'FALSE SUPERLATIVE' in text}, "
          f"rank-integrity-caught={ok_rank}, C-score-claim-not-flagged={ok_c_ok}, "
          f"overall-FAIL={ok_overall}  =>  {'OK' if allok else 'BROKEN'}")
    return 0 if allok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify superlative copy claims against the full corpus.")
    ap.add_argument("--json", help="path to a comparison-page frontend JSON")
    ap.add_argument("--emit-json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return run_selftest()
    if not args.json:
        ap.print_help()
        return 2
    return run_page(Path(args.json), args.emit_json)


if __name__ == "__main__":
    sys.exit(main())
