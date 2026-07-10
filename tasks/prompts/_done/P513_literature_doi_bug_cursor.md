# P513 / Fix wrong-DOI bug in literature.py pubmed_fetch (route: C1-CURSOR)

**Repo:** `C:\Bari` (root). Work on the local tree; commit nothing (orchestrator controls commits). Do NOT touch `bari-web/`.

**Read first:** `C:\Bari\tasks\TASK-513.md` (the task + DoD).

## Objective
`pubmed_fetch()` in `C:\Bari\integrations\clients\literature.py` returns a `doi` field that is frequently
mismatched to an unrelated paper. During the 2026-07-05 GLP-1 evidence brief, 3 of 9 DOIs spot-checked resolved
via Crossref to unrelated papers (a 1998 UKPDS Lancet paper, a 2020 JMIR mHealth RCT, a 2012 J. Lipid Research
paper) — none matching the article title/journal in the same record. Root cause is almost certainly the XML parse
grabbing a DOI from a descendant `ReferenceList` / `CommentsCorrections` entry (a *cited* paper's DOI) rather than
the fetched article's own DOI.

## Deliverable
1. **Fix the parser** so the DOI is scoped to the fetched article only. The article's own DOI lives at
   `PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType="doi"]` and/or
   `PubmedArticle/MedlineCitation/Article/ELocationID[@EIdType="doi"]`. Ensure DOI extraction is bound to the
   article element and never descends into `ReferenceList`, `CommentsCorrectionsList`, or any cited-work subtree.
   Prefer `ArticleIdList/ArticleId[@IdType="doi"]`, fall back to `ELocationID[@EIdType="doi"]`, else `None`
   (NEVER a reference DOI). Apply the same scoping to any sibling id fields (pmcid etc.) if they share the bug.
2. **Add a deterministic regression test** (no network) under the repo's existing test location for
   `integrations/clients` — a saved EFetch XML fixture for one article that ALSO contains a `ReferenceList` with
   its own DOIs; assert `pubmed_fetch(...).doi` equals the ARTICLE's DOI, not any reference DOI, and that an
   article with no own-DOI returns `None` (not a borrowed reference DOI).
3. **Optional runtime cross-check (guarded, non-fatal):** if a lightweight assertion helper already exists, add
   an opt-in Crossref round-trip check (`doi → title` similarity) that only runs when explicitly enabled — do NOT
   add a network call to the default fetch path or the test suite.

## Boundaries / guards
- Change ONLY `integrations/clients/literature.py` + the new test (+ fixture file). No other modules, no scoring
  code, no frontend.
- **OFF ban:** irrelevant here (PubMed/Crossref only) — but do not add any new external data source beyond the
  already-configured PubMed/Crossref clients. No new paid services.
- Do not "fix" unrelated lints. Keep the diff minimal and reviewable.
- Run the new test and paste the actual runner output in the return.

## Return format
Return the machine-readable return contract (`01_framework/operations/return_contract_v1.md`): artifacts + sha256,
the exact test command + its real pass output, a before/after of the parse path (the XPath/element you changed),
and a note confirming the fixture contains reference DOIs that the parser now correctly ignores.
**Do not close — propose RETURNED.**
