---
id: TASK-513
title: Fix wrong-DOI bug in literature.py pubmed_fetch (citation-integrity)
owner: data-agent
status: CLOSED
close_reason: >
  VERIFIED by orchestrator (2026-07-05). Root cause = recursive `.//ArticleIdList/ArticleId` in pubmed_fetch()
  descended into PubmedData/ReferenceList and last-match-wins returned a CITED paper's DOI. Fix (P513, C1-Sonnet):
  new `_article_doi()` helper reads direct-child `PubmedData/ArticleIdList/ArticleId[@IdType="doi"]` (confirmed
  non-recursive at literature.py:84), falls back to `ELocationID[@EIdType="doi"]` (:91), else None — never descends
  into ReferenceList. Independently verified: ran `pytest integrations/clients/tests/test_literature.py` myself →
  6/6 PASS (incl. article-gets-own-DOI-not-reference, no-own-DOI→None-not-borrowed, ELocationID fallback). Scope
  clean: `git diff --stat` = literature.py only (28+/4−) + 2 new files (test + no-network fixture); no other tracked
  file touched, nothing committed. C1-CURSOR route refused first (dirty-tree wipe hazard) → rerouted to shared-tree
  Sonnet, scoped touch-only. Restores C0 citation-gate integrity.
priority: HIGH
created_at: 2026-07-05
closed_at: 2026-07-05
depends_on: []
blocks: []
category_id: null
summary: >
  pubmed_fetch() returns a mismatched DOI (parses a reference/ELocationID DOI, not the article's own). 3/9 DOIs spot-checked in the GLP-1 brief resolved to unrelated papers. Threatens the C0 citation gate. Fix parser to ArticleId[@IdType='doi'], add Crossref cross-check + regression test. Found 2026-07-05 GLP-1 assessment.
---

# TASK-513 — Fix wrong-DOI bug in literature.py pubmed_fetch (citation-integrity)

Fixed at `integrations/clients/literature.py` (`_article_doi()` helper, :72–92). Regression test +
no-network fixture at `integrations/clients/tests/`. 6/6 pass (orchestrator-verified). Local tree only —
not committed (ambient dirty tree; commit batched with a supervised push, like TASK-508/510).
