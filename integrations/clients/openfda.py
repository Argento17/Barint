"""openFDA — food enforcement (recalls) + adverse-event signal (US FDA).

For: Red-Team + Research + Nutrition Agents. Two free, no-auth endpoints that add a
real-world *harm signal* the composition databases can't carry:

  * /food/enforcement   FDA food & dietary-supplement recall/enforcement reports —
                        contamination, undeclared allergens, adulteration, mislabeling.
                        Searchable by product, firm, or reason.
  * /food/event         CAERS adverse-event reports for foods & supplements (consumer /
                        clinician reported symptoms tied to a product or substance).

These are US signals — directly relevant for imported products and for any *substance*
(an additive, a supplement active) regardless of market. The Red-Team Agent uses them to
challenge a clean score ("E-number X is class-approved, but FDA logged N adverse events");
the client surfaces counts + records, it draws no conclusion and does NOT stamp provenance.

HONEST LIMIT: US jurisdiction. Absence of a US recall is NOT evidence of Israeli safety,
and CAERS is a passive voluntary-report system (no incidence/denominator) — counts signal
attention, not proven causation. Treat as a lead, not a verdict.

Free, no key (240 req/min, 1000/day unauthenticated). Set OPENFDA_API_KEY to raise limits.
Docs: https://open.fda.gov/apis/food/
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"
API = "https://api.fda.gov"


def _params(extra: dict) -> dict:
    key = os.environ.get("OPENFDA_API_KEY")
    return {**extra, **({"api_key": key} if key else {})}


@dataclass
class Recall:
    recall_number: str | None
    status: str | None = None
    classification: str | None = None       # Class I / II / III (I = most serious)
    product_description: str | None = None
    reason: str | None = None
    recalling_firm: str | None = None
    distribution_pattern: str | None = None
    recall_date: str | None = None
    country: str | None = None


@dataclass
class AdverseEventSummary:
    term: str
    total_reports: int
    top_reactions: list[tuple[str, int]] = field(default_factory=list)


def enforcement(search_term: str, field: str = "product_description", limit: int = 10) -> list[Recall]:
    """Search food/supplement recall & enforcement reports. Matches `search_term` in one
    field (default product_description; pass field='reason_for_recall' to search reasons,
    or 'recalling_firm' for a firm). openFDA's `+`-joined multi-field OR does not survive
    url-encoding, so the client scopes to one field per call by design."""
    try:
        data = get_json(
            f"{API}/food/enforcement.json",
            params=_params({"search": f"{field}:{search_term}", "limit": limit}),
        )
    except HttpError as e:
        if e.status == 404:   # openFDA returns 404 for "no matches"
            return []
        raise
    out: list[Recall] = []
    for r in data.get("results", []):
        out.append(Recall(
            recall_number=r.get("recall_number"),
            status=r.get("status"),
            classification=r.get("classification"),
            product_description=(r.get("product_description") or "")[:160],
            reason=(r.get("reason_for_recall") or "")[:200],
            recalling_firm=r.get("recalling_firm"),
            distribution_pattern=(r.get("distribution_pattern") or "")[:120],
            recall_date=r.get("recall_initiation_date"),
            country=r.get("country"),
        ))
    return out


def adverse_events(term: str, field: str = "products.name_brand",
                   limit_reactions: int = 8) -> AdverseEventSummary:
    """Count CAERS adverse-event reports mentioning a product/substance, with the most
    common reported reactions. total_reports is the true report count from the API meta;
    top_reactions is a frequency count of reported symptoms. total_reports=0 means none
    on record (NOT 'safe' — CAERS is passive voluntary reporting)."""
    try:
        meta = get_json(
            f"{API}/food/event.json",
            params=_params({"search": f"{field}:{term}", "limit": 1}),
        )
    except HttpError as e:
        if e.status == 404:
            return AdverseEventSummary(term=term, total_reports=0)
        raise
    total = int(meta.get("meta", {}).get("results", {}).get("total", 0) or 0)
    top: list[tuple[str, int]] = []
    try:
        data = get_json(
            f"{API}/food/event.json",
            params=_params({"search": f"{field}:{term}",
                            "count": "reactions.exact", "limit": limit_reactions}),
        )
        top = [(r.get("term"), r.get("count")) for r in data.get("results", []) if r.get("term")]
    except HttpError as e:
        if e.status != 404:
            raise
    return AdverseEventSummary(term=term, total_reports=total, top_reactions=top)


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("== enforcement: tahini ==")
    for r in enforcement("tahini", limit=3):
        print(f"  [{r.classification}] {r.recall_date} {r.recalling_firm}: {(r.reason or '')[:70]}")
    print("== adverse events: spirulina ==")
    s = adverse_events("spirulina")
    print(f"  total_reports={s.total_reports} top={s.top_reactions[:4]}")
