---
id: TASK-383
title: Citation-integrity C0 verification gate (anti-fabrication) + full retroactive evidence sweep
owner: research-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-23
depends_on: []
blocks: []
category_id: null
summary: >
  Root cause: LLM agents hallucinate exact identifiers (PMIDs/DOIs) even when the underlying claim is real; citations rule required a source be NAMED, never that it RESOLVE+MATCH. Fix (deterministic, not instruction): verify_citations.py (C0) resolves every PMID/DOI in an evidence/copy artifact against PubMed/CrossRef and asserts real title/author/year match the claimed context; exit non-zero on any non-resolving/mismatched id. Wire as standing gate into two-gate/red-team + CI; orchestrator never marks evidence 'verified' until it passes. Full retroactive sweep across all governance files; every wrong cite routed to owning agent for verified replacement. Triggered 2026-06-23 by EV-104 fabricated cheese PMIDs (TASK-380) + registry sweep finding the Monteiro NOVA PMID 31122155 also wrong (resolves to an unrelated nursing case study).
---

# TASK-383 — Citation-integrity C0 verification gate (anti-fabrication) + full retroactive evidence sweep

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Progress log

### 2026-06-25 (orchestrate, unattended) — follow-up (b) DONE: heuristic hardened (author-surname + year cross-check)
- Dispatched native Research Agent (Sonnet). `verify_citations.py` hardened with `_parse_context_author_year` + `_author_year_corroborate` (author-surname + year corroboration that runs after the topic check), closing the F-10 same-domain-miss gap. +474 / −9 lines, **only `verify_citations.py` touched** (orchestrator-verified scope; no score/JSON/engine edits). Change is UNCOMMITTED in the working tree (3AM run — committing deferred to owner's supervised session).
- **Orchestrator independently verified:** `--selftest` 8/8 PASS (incl. live round-trip PMID 28615384 Thorning→Salas-Salvadó → MISMATCH, the exact F-10 case); full `--all` sweep = 55 checked / 51 PASS / **2 MISMATCH** / 0 FABRICATED / 2 UNRESOLVED-DOI.
- **NEW FINDING (the hardened gate's first catch — 2 genuine attribution errors the old same-domain-blind heuristic passed):**
  1. `01_framework/glass_box/diaas_source_table_v1.md:52` — PMID **37357639** attributed to "Nosworthy et al. (2023)" but resolves to Bailey/Fanelli/Stein 2023 (rapeseed heat-treatment). (Same PMID is used CORRECTLY for rapeseed claims elsewhere in the file — line 52 is the mis-attached one.)
  2. `bsip2_evidence_registry_v1.md:2430` — PMID **9771853** cited "Willett 1997" resolves to Judd et al. 1998 (margarine/butter). Board had flagged this borderline; now deterministically caught.
  - These are GOVERNANCE-doc attribution errors → **no published-score / consumer impact, no tripwire.** Correcting them = QUEUED for Research (find correct PMID for the Nosworthy/Willett claims, or fix attribution text).
- **Still open:** (a) wire `verify_citations.py` as a standing CI gate + D7 pre-condition; (c) re-ground the EV-024 fermented-dairy claim; (d-new) correct the 2 attribution errors above.
