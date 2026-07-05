"""Regression test for TASK-513 — pubmed_fetch() wrong-DOI bug.

Root cause: the original parser searched ``.//ArticleIdList/ArticleId`` from the
PubmedArticle root, which also matches the nested ArticleIdList inside
PubmedData/ReferenceList/Reference (a CITED paper's own ids) and silently returned
that reference's DOI instead of the fetched article's own DOI. 3 of 9 DOIs in the
2026-07-05 GLP-1 evidence brief resolved via Crossref to unrelated papers as a
result.

This test is fully offline: it monkeypatches literature.get() to return a saved
EFetch XML fixture (no network, no NCBI key needed) and asserts:
  1. an article whose own DOI is in PubmedData/ArticleIdList gets THAT doi, never
     one of its ReferenceList's cited-paper DOIs;
  2. an article with no doi anywhere returns None, even though its own reference
     list contains a (different, unrelated) doi;
  3. an article with no PubmedData/ArticleIdList doi but an ELocationID doi on the
     Article element itself gets that doi via the documented fallback path.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from integrations.clients import literature  # noqa: E402

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "pubmed_efetch_with_references.xml"

# DOIs that live only inside a ReferenceList (cited works) — must NEVER be returned
# as the fetched article's own doi.
REFERENCE_ONLY_DOIS = {
    "10.1016/S0140-6736(98)07019-6",  # cited under PMID 11111111's ReferenceList
    "10.2196/99999",                   # cited under PMID 11111111's ReferenceList
    "10.1000/borrowed-reference-doi",  # cited under PMID 22222222's ReferenceList
}


@pytest.fixture
def fixture_papers(monkeypatch):
    raw = FIXTURE.read_bytes()

    def _fake_get(*args, **kwargs):
        return raw

    monkeypatch.setattr(literature, "get", _fake_get)
    return {p.id: p for p in literature.pubmed_fetch(["11111111", "22222222", "33333333"])}


def test_no_network_call(monkeypatch):
    """Sanity check: pubmed_fetch must not attempt a real request in this test module."""

    def _boom(*args, **kwargs):
        raise AssertionError("pubmed_fetch made a real network call — test is not offline")

    monkeypatch.setattr(literature, "get", _boom)
    with pytest.raises(AssertionError):
        literature.pubmed_fetch(["11111111"])


def test_article_gets_its_own_doi_not_a_reference_doi(fixture_papers):
    paper = fixture_papers["11111111"]
    assert paper.doi == "10.1016/j.article-a.2024.00111"
    assert paper.doi not in REFERENCE_ONLY_DOIS


def test_article_with_no_own_doi_returns_none_not_a_borrowed_reference_doi(fixture_papers):
    paper = fixture_papers["22222222"]
    assert paper.doi is None
    # Explicitly guard against the historical bug: the reference doi must not leak in.
    assert paper.doi != "10.1000/borrowed-reference-doi"


def test_article_doi_falls_back_to_elocation_id(fixture_papers):
    paper = fixture_papers["33333333"]
    assert paper.doi == "10.2337/article-c.2023.00333"


def test_all_three_articles_parsed(fixture_papers):
    assert set(fixture_papers) == {"11111111", "22222222", "33333333"}


def test_article_doi_helper_ignores_reference_list_directly():
    """Exercise _article_doi() directly against the raw XML nodes (belt-and-braces:
    covers the helper even if pubmed_fetch's plumbing around it changes later)."""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(FIXTURE.read_bytes())
    articles = {
        (a.findtext(".//PMID") or "").strip(): a
        for a in root.findall(".//PubmedArticle")
    }

    art_a = articles["11111111"]
    art_el_a = art_a.find(".//MedlineCitation/Article")
    assert literature._article_doi(art_a, art_el_a) == "10.1016/j.article-a.2024.00111"

    art_b = articles["22222222"]
    art_el_b = art_b.find(".//MedlineCitation/Article")
    assert literature._article_doi(art_b, art_el_b) is None
