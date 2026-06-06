"""bioRxiv / medRxiv — preprint evidence (Cold Spring Harbor API).

For: Research + Red-Team + Nutrition Agents. Surfaces the *not-yet-peer-reviewed* edge of
the literature — new nutrition/supplement findings that PubMed won't index until a journal
accepts them. This is the leading indicator the peer-reviewed backends miss.

DELIBERATELY LOW-TRUST: a preprint is the weakest evidence tier by construction. The
client tags every record `peer_reviewed=False` and exposes `published_doi` when the
preprint has since appeared in a journal (so the agent can upgrade to the version of
record). It informs the Research Agent's tiering; it never assigns a tier, and — as an
evidence client — it does NOT stamp provenance.

Two endpoints used:
  * /details/{server}/{DOI}            fetch one preprint by DOI
  * /details/{server}/{from}/{to}      browse a date window (the API has no full-text
                                       keyword search; callers filter the window
                                       client-side). The `published` field flips to the
                                       journal DOI once the preprint is peer-reviewed.

Free, no key. Docs: https://api.biorxiv.org/
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

from .http import HttpError, get_json

CLIENT_VERSION = "1.0"
API = "https://api.biorxiv.org"


@dataclass
class Preprint:
    doi: str
    title: str
    server: str                       # "biorxiv" | "medrxiv"
    date: str | None = None
    version: str | None = None
    category: str | None = None
    authors: str | None = None
    abstract: str | None = None
    published_doi: str | None = None  # set once a journal publishes it (version of record)
    peer_reviewed: bool = False       # always False here — it's a preprint server

    @property
    def url(self) -> str:
        return f"https://www.{self.server}.org/content/{self.doi}"

    @property
    def is_published(self) -> bool:
        return bool(self.published_doi and self.published_doi.lower() != "na")


def get_preprint(doi: str, server: str = "biorxiv") -> Preprint | None:
    """Fetch one preprint by DOI. Returns None on miss."""
    try:
        data = get_json(f"{API}/details/{server}/{doi}")
    except HttpError as e:
        if e.status == 404:
            return None
        raise
    coll = data.get("collection") or []
    if not coll:
        return None
    rec = coll[-1]  # last = newest version
    return _to_preprint(rec, server)


def recent(server: str = "biorxiv", count: int = 30, days: int = 30,
           category: str | None = None) -> list[Preprint]:
    """Preprints from the last `days` on a server (newest first). Optionally filter by
    category (e.g. 'nutrition'). The date-window endpoint pages 100 at a time; we walk
    cursors until we have `count` (post-filter) or the window is exhausted."""
    today = datetime.now(timezone.utc).date()
    frm = (today - timedelta(days=days)).isoformat()
    to = today.isoformat()
    out: list[Preprint] = []
    cursor = 0
    cat_l = category.lower() if category else None
    for _ in range(20):  # hard cap: 20 pages * 100 = 2000 scanned
        data = get_json(f"{API}/details/{server}/{frm}/{to}/{cursor}")
        coll = data.get("collection") or []
        if not coll:
            break
        for rec in reversed(coll):              # within a page, newest last -> reverse
            p = _to_preprint(rec, server)
            if cat_l and (p.category or "").lower() != cat_l:
                continue
            out.append(p)
        total = int((data.get("messages") or [{}])[0].get("total") or 0)
        cursor += len(coll)
        if cursor >= total or len(out) >= count:
            break
    # newest-first across the whole window
    out.sort(key=lambda p: p.date or "", reverse=True)
    return out[:count]


def search(term: str, server: str = "biorxiv", days: int = 30, scan: int = 200) -> list[Preprint]:
    """Keyword filter over a recent date window (the API has no native text search).
    Best-effort leading-indicator scan, not an exhaustive corpus query."""
    term_l = term.lower()
    hits: list[Preprint] = []
    for p in recent(server=server, count=scan, days=days):
        hay = f"{p.title} {p.abstract or ''} {p.category or ''}".lower()
        if term_l in hay:
            hits.append(p)
    return hits


def _to_preprint(rec: dict, server: str) -> Preprint:
    return Preprint(
        doi=rec.get("doi") or "",
        title=(rec.get("title") or "").strip(),
        server=server,
        date=rec.get("date"),
        version=str(rec.get("version")) if rec.get("version") is not None else None,
        category=rec.get("category"),
        authors=rec.get("authors"),
        abstract=(rec.get("abstract") or "").strip() or None,
        published_doi=rec.get("published") if rec.get("published") not in (None, "NA") else None,
    )


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("== recent biorxiv ==")
    for p in recent(count=3):
        print(f"  {p.date} [{p.category}] published={p.is_published}: {p.title[:60]}")
    print("== get_preprint by DOI ==")
    p = get_preprint("10.1101/2020.09.09.289074")
    if p:
        print(f"  {p.title[:60]} v{p.version} published_doi={p.published_doi}")
    else:
        print("  (no match — DOI window may have rolled)")
