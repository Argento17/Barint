"""Crossref — DOI metadata, reference counts, and retraction signal.

For: Research + Red-Team Agents. The DOI registry of record. Given a DOI (from any other
backend — Europe PMC, OpenAlex, Semantic Scholar, bioRxiv), Crossref returns authoritative
bibliographic metadata plus two signals that matter for evidence quality:

  * is_referenced_by_count   how many works cite this DOI (Crossref's own count)
  * references_count         how many references the work itself carries (a thin reference
                             list on a "review" is a red flag the Red-Team Agent can use)
  * update_to / retraction   `update-to` relations expose corrections, retractions, and
                             expressions-of-concern — the single most important integrity
                             signal when leaning on a paper.

EVIDENCE/IDENTITY client — informs tiering and integrity checks; assigns no tier and does
NOT stamp provenance. Free, no key. Crossref asks for a contact in the User-Agent for the
polite pool, which `http.USER_AGENT` already provides.

Docs: https://api.crossref.org/swagger-ui/index.html
"""
from __future__ import annotations

import urllib.parse
from dataclasses import dataclass, field

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"
API = "https://api.crossref.org"


@dataclass
class CrossrefWork:
    doi: str
    title: str | None = None
    type: str | None = None                 # journal-article | posted-content | review ...
    container: str | None = None            # journal / venue title
    year: int | None = None
    publisher: str | None = None
    cited_by_count: int | None = None       # is-referenced-by-count
    references_count: int | None = None
    is_retracted: bool = False
    update_types: list[str] = field(default_factory=list)  # e.g. ['retraction','correction']
    found: bool = True

    @property
    def url(self) -> str:
        return f"https://doi.org/{self.doi}"


_RETRACTION_FLAGS = {"retraction", "withdrawal", "removal", "expression of concern"}


def get_doi(doi: str) -> CrossrefWork:
    """Fetch authoritative metadata + integrity signal for a DOI. found=False on miss."""
    enc = urllib.parse.quote(doi, safe="")
    try:
        data = get_json(f"{API}/works/{enc}")
    except HttpError as e:
        if e.status == 404:
            return CrossrefWork(doi=doi, found=False)
        raise
    return _to_work(data.get("message", {}), doi)


def search(query: str, rows: int = 10) -> list[CrossrefWork]:
    """Bibliographic search across Crossref (relevance ordered)."""
    data = get_json(f"{API}/works", params={"query": query, "rows": rows})
    items = data.get("message", {}).get("items", [])
    return [_to_work(it, it.get("DOI", "")) for it in items]


def _to_work(m: dict, doi: str) -> CrossrefWork:
    title = (m.get("title") or [None])
    container = (m.get("container-title") or [None])
    year = None
    for k in ("published", "published-print", "published-online", "issued"):
        parts = (m.get(k) or {}).get("date-parts")
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    updates = m.get("update-to") or []
    update_types = [u.get("type") for u in updates if u.get("type")]
    update_labels = " ".join((u.get("label") or "") for u in updates).lower()
    is_retracted = (
        m.get("type") == "retraction"
        or any(t and t.lower() in {"retraction", "withdrawal"} for t in update_types)
        or any(flag in update_labels for flag in _RETRACTION_FLAGS)
    )
    return CrossrefWork(
        doi=doi,
        title=title[0] if title and title[0] else None,
        type=m.get("type"),
        container=container[0] if container and container[0] else None,
        year=year,
        publisher=m.get("publisher"),
        cited_by_count=m.get("is-referenced-by-count"),
        references_count=m.get("references-count"),
        is_retracted=is_retracted,
        update_types=update_types,
    )


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("== get_doi ==")
    w = get_doi("10.1186/s12970-017-0173-z")
    print(f"  found={w.found} {w.type} {w.year} cited_by={w.cited_by_count} "
          f"refs={w.references_count} retracted={w.is_retracted}")
    print(f"  {(w.title or '')[:70]}")
    print("== search ==")
    for w in search("creatine cognition meta-analysis", rows=3):
        print(f"  {w.year} [{w.type}] cited_by={w.cited_by_count}: {(w.title or '')[:55]}")
