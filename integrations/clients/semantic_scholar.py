"""Semantic Scholar — citation-weighted evidence signal (Allen Institute Graph API).

For: Research + Red-Team + Nutrition Agents. PubMed/Europe PMC tell you a paper exists;
Semantic Scholar tells you how much the field *leaned on it*. It adds three signals the
NCBI/EBI backends don't carry well:

  * tldr                       a one-sentence machine summary of the paper's claim
  * influentialCitationCount   citations where this work materially shaped the citing one
                               (a sharper signal than raw count for "did this stick?")
  * citationCount + year       lets the agent compute citation *velocity* (cites/year)

This is an EVIDENCE/IDENTITY client — it informs the Research Agent's manual tiering
(Strong/Moderate/Weak/Contested); it does NOT assign a tier and does NOT stamp
provenance (nothing here is a candidate scoring input).

Free Graph API, no key required (~100 req/5min unauthenticated). Set
SEMANTIC_SCHOLAR_API_KEY to raise the limit.

Docs: https://api.semanticscholar.org/api-docs/graph
"""
from __future__ import annotations

import os
import urllib.parse
from dataclasses import dataclass, field

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"
API = "https://api.semanticscholar.org/graph/v1"

_FIELDS = ("title,year,venue,externalIds,citationCount,influentialCitationCount,"
           "isOpenAccess,tldr,authors")


def _headers() -> dict[str, str]:
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    return {"x-api-key": key} if key else {}


@dataclass
class Work:
    paper_id: str
    title: str
    year: int | None = None
    venue: str | None = None
    doi: str | None = None
    pmid: str | None = None
    citation_count: int | None = None
    influential_citation_count: int | None = None
    is_open_access: bool | None = None
    tldr: str | None = None
    authors: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"https://www.semanticscholar.org/paper/{self.paper_id}"

    @property
    def citation_velocity(self) -> float | None:
        """Citations per year since publication — a recency-normalised impact signal."""
        if self.citation_count is None or not self.year:
            return None
        from datetime import datetime
        span = max(1, datetime.now().year - self.year + 1)
        return round(self.citation_count / span, 1)


def _to_work(p: dict) -> Work:
    ext = p.get("externalIds") or {}
    tldr = (p.get("tldr") or {}).get("text") if p.get("tldr") else None
    return Work(
        paper_id=p.get("paperId") or "",
        title=(p.get("title") or "").strip(),
        year=p.get("year"),
        venue=p.get("venue") or None,
        doi=ext.get("DOI"),
        pmid=ext.get("PubMed"),
        citation_count=p.get("citationCount"),
        influential_citation_count=p.get("influentialCitationCount"),
        is_open_access=p.get("isOpenAccess"),
        tldr=tldr,
        authors=[a.get("name") for a in (p.get("authors") or []) if a.get("name")][:8],
    )


def search(query: str, limit: int = 10) -> list[Work]:
    """Relevance search across the Semantic Scholar corpus."""
    data = get_json(
        f"{API}/paper/search",
        params={"query": query, "limit": limit, "fields": _FIELDS},
        headers=_headers(),
    )
    return [_to_work(p) for p in data.get("data", [])]


def get_paper(id_: str) -> Work | None:
    """Fetch one paper by S2 id, DOI ('DOI:10.x/y'), or PMID ('PMID:12345').
    Returns None on miss (no such paper)."""
    enc = urllib.parse.quote(id_, safe=":")
    try:
        data = get_json(f"{API}/paper/{enc}", params={"fields": _FIELDS},
                        headers=_headers())
    except HttpError as e:
        if e.status in (404, 400):
            return None
        raise
    return _to_work(data)


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("== search: creatine cognition ==")
    for w in search("creatine supplementation cognition", limit=3):
        print(f"  {w.year} cites={w.citation_count} infl={w.influential_citation_count} "
              f"vel={w.citation_velocity}: {w.title[:60]}")
        if w.tldr:
            print(f"     tldr: {w.tldr[:90]}")
    print("== get_paper by DOI ==")
    w = get_paper("DOI:10.1186/s12970-017-0173-z")
    if w:
        print(f"  {w.title[:70]} cites={w.citation_count} infl={w.influential_citation_count}")
