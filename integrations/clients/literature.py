"""Scientific-literature client — PubMed E-utilities + Europe PMC.

For: Research Agent. Turns its source hierarchy (Cochrane > RCTs > EFSA/WHO) from
manual browsing into queryable evidence. Returns structured records the agent can
tier (Strong/Moderate/Weak/Insufficient/Contested) — the client never assigns a tier
itself; tiering is the agent's judgement.

Four complementary backends (all free, no key required):
  * PubMed E-utilities (NCBI) — authoritative index, abstracts via efetch.
  * Europe PMC          — full-text links, citation counts, open-access flags.
  * OpenAlex            — full scholarly graph; broad coverage + citation counts.
  * ClinicalTrials.gov  — the trial registry (ongoing + completed), not just papers.

NCBI allows ~3 req/s without a key, ~10 with one — set NCBI_API_KEY to raise the limit.

Docs: https://www.ncbi.nlm.nih.gov/books/NBK25500/
      https://europepmc.org/RestfulWebService
      https://docs.openalex.org/  ·  https://clinicaltrials.gov/data-api/api
"""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from .http import get, get_json

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
OPENALEX = "https://api.openalex.org"
CLINICALTRIALS = "https://clinicaltrials.gov/api/v2"


@dataclass
class Paper:
    source: str                 # "pubmed" | "europepmc"
    id: str                     # PMID or Europe PMC id
    title: str
    journal: str | None = None
    year: str | None = None
    doi: str | None = None
    abstract: str | None = None
    authors: list[str] = field(default_factory=list)
    cited_by: int | None = None
    is_open_access: bool | None = None
    pub_types: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        if self.source == "pubmed":
            return f"https://pubmed.ncbi.nlm.nih.gov/{self.id}/"
        return f"https://europepmc.org/article/MED/{self.id}"


def _ncbi_params(extra: dict) -> dict:
    p = {"db": "pubmed", "retmode": "json", **extra}
    key = os.environ.get("NCBI_API_KEY")
    if key:
        p["api_key"] = key
    return p


def pubmed_search(query: str, retmax: int = 10) -> list[str]:
    """Return a list of PMIDs for a query (newest/most-relevant first)."""
    data = get_json(
        f"{EUTILS}/esearch.fcgi",
        params=_ncbi_params({"term": query, "retmax": retmax, "sort": "relevance"}),
    )
    return data.get("esearchresult", {}).get("idlist", [])


def pubmed_fetch(pmids: list[str]) -> list[Paper]:
    """Fetch full records (with abstracts) for PMIDs via efetch XML."""
    if not pmids:
        return []
    raw = get(
        f"{EUTILS}/efetch.fcgi",
        params=_ncbi_params({"id": ",".join(pmids), "retmode": "xml"}),
        headers={"Accept": "application/xml"},
    )
    root = ET.fromstring(raw)
    papers: list[Paper] = []
    for art in root.findall(".//PubmedArticle"):
        medline = art.find(".//MedlineCitation")
        if medline is None:
            continue
        pmid = (medline.findtext("PMID") or "").strip()
        art_el = medline.find("Article")
        if art_el is None:
            continue
        title = (art_el.findtext("ArticleTitle") or "").strip()
        journal = art_el.findtext(".//Journal/Title")
        year = art_el.findtext(".//JournalIssue/PubDate/Year") or \
            art_el.findtext(".//JournalIssue/PubDate/MedlineDate")
        abstract = " ".join(
            (t.text or "") for t in art_el.findall(".//Abstract/AbstractText")
        ).strip() or None
        authors = []
        for a in art_el.findall(".//AuthorList/Author"):
            last, fore = a.findtext("LastName"), a.findtext("ForeName")
            if last:
                authors.append(f"{fore} {last}".strip() if fore else last)
        doi = None
        for idn in art.findall(".//ArticleIdList/ArticleId"):
            if idn.get("IdType") == "doi":
                doi = (idn.text or "").strip()
        pub_types = [pt.text for pt in art_el.findall(".//PublicationType") if pt.text]
        papers.append(Paper(
            source="pubmed", id=pmid, title=title, journal=journal, year=year,
            doi=doi, abstract=abstract, authors=authors, pub_types=pub_types,
        ))
    return papers


def pubmed(query: str, retmax: int = 8) -> list[Paper]:
    """Convenience: search + fetch in one call."""
    return pubmed_fetch(pubmed_search(query, retmax=retmax))


def europepmc(query: str, page_size: int = 10) -> list[Paper]:
    """Search Europe PMC — adds citation counts + open-access flags."""
    data = get_json(
        f"{EUROPEPMC}/search",
        params={"query": query, "format": "json", "pageSize": page_size,
                "resultType": "core"},
    )
    out: list[Paper] = []
    for r in data.get("resultList", {}).get("result", []):
        out.append(Paper(
            source="europepmc",
            id=str(r.get("id") or r.get("pmid") or ""),
            title=(r.get("title") or "").strip(),
            journal=r.get("journalTitle"),
            year=str(r.get("pubYear")) if r.get("pubYear") else None,
            doi=r.get("doi"),
            abstract=r.get("abstractText"),
            cited_by=r.get("citedByCount"),
            is_open_access=(r.get("isOpenAccess") == "Y"),
            pub_types=[r["pubTypeList"]["pubType"]] if isinstance(
                r.get("pubTypeList", {}).get("pubType"), str) else
            (r.get("pubTypeList", {}).get("pubType", []) if r.get("pubTypeList") else []),
        ))
    return out


def openalex(query: str, per_page: int = 10) -> list[Paper]:
    """Search OpenAlex — broad scholarly graph with citation counts + OA flags."""
    data = get_json(
        f"{OPENALEX}/works",
        params={"search": query, "per-page": per_page,
                "select": "id,title,publication_year,doi,cited_by_count,"
                          "open_access,primary_location,type"},
    )
    out: list[Paper] = []
    for w in data.get("results", []):
        loc = w.get("primary_location") or {}
        src = (loc.get("source") or {}).get("display_name")
        out.append(Paper(
            source="openalex",
            id=(w.get("id") or "").rsplit("/", 1)[-1],
            title=w.get("title") or "",
            journal=src,
            year=str(w["publication_year"]) if w.get("publication_year") else None,
            doi=(w.get("doi") or "").replace("https://doi.org/", "") or None,
            cited_by=w.get("cited_by_count"),
            is_open_access=(w.get("open_access") or {}).get("is_oa"),
            pub_types=[w["type"]] if w.get("type") else [],
        ))
    return out


@dataclass
class Trial:
    nct_id: str
    title: str
    status: str | None = None
    phase: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    interventions: list[str] = field(default_factory=list)
    enrollment: int | None = None

    @property
    def url(self) -> str:
        return f"https://clinicaltrials.gov/study/{self.nct_id}"


def clinicaltrials(query: str, page_size: int = 10) -> list[Trial]:
    """Search ClinicalTrials.gov — registered trials (design, phase, status, enrollment).
    Complements published literature: shows what is being / has been tested, including
    null and unpublished results the paper record misses."""
    data = get_json(
        f"{CLINICALTRIALS}/studies",
        params={"query.term": query, "pageSize": page_size},
    )
    out: list[Trial] = []
    for s in data.get("studies", []):
        ps = s.get("protocolSection", {})
        ident = ps.get("identificationModule", {})
        status = ps.get("statusModule", {})
        design = ps.get("designModule", {})
        arms = ps.get("armsInterventionsModule", {})
        cond = ps.get("conditionsModule", {})
        out.append(Trial(
            nct_id=ident.get("nctId", ""),
            title=ident.get("briefTitle", ""),
            status=status.get("overallStatus"),
            phase=design.get("phases", []),
            conditions=cond.get("conditions", []),
            interventions=[i.get("name") for i in arms.get("interventions", [])
                           if i.get("name")],
            enrollment=(design.get("enrollmentInfo") or {}).get("count"),
        ))
    return out


if __name__ == "__main__":
    print("== PubMed ==")
    for p in pubmed("creatine supplementation muscle strength systematic review", retmax=3):
        print(f"  PMID {p.id} ({p.year}) {p.journal}: {p.title[:70]}")
        print(f"     types={p.pub_types} abstract={'yes' if p.abstract else 'no'}")
    print("== Europe PMC ==")
    for p in europepmc("vitamin D deficiency meta-analysis", page_size=3):
        print(f"  {p.id} ({p.year}) cited_by={p.cited_by} OA={p.is_open_access}: {p.title[:60]}")
    print("== OpenAlex ==")
    for p in openalex("magnesium glycinate sleep", per_page=3):
        print(f"  {p.id} ({p.year}) cited_by={p.cited_by} {p.journal}: {p.title[:55]}")
    print("== ClinicalTrials.gov ==")
    for t in clinicaltrials("creatine cognition", page_size=3):
        print(f"  {t.nct_id} [{t.status}] phase={t.phase} n={t.enrollment}: {t.title[:50]}")
