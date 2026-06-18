---
id: TASK-285
title: NutriNet-Sante emulsifier evidence verification -> EV-061 proposal + EV-060 annotation + KB-003
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-15
depends_on: []
blocks: []
category_id: null
summary: >
  Verify 2024-25 NutriNet-Sante DOIs for E471/E472/E460-468 and confirm E471-specific isolation. If isolation holds, Nutrition drafts EV-061 proposing additive-library tier upgrade E471/E472 likely-neutral->contested (annotate-only W3, flag-OFF, 0 published score movement, Product D7 gate). Also annotate EV-060 source field with flax/coconut SCFA citations; add KB-003 (INFOGEST/phytate bioavailability) to nutrition reference KB. Origin: owner research-dump triage 2026-06-15, Nutrition Agent ruling.
---

# TASK-285 — NutriNet-Sante emulsifier evidence verification -> EV-061 proposal + EV-060 annotation + KB-003

## Origin
Owner research-dump triage 2026-06-15 → Nutrition Agent ruling: 6 of 7 dump items needed no engine work; the one
live thread was a flag-OFF, annotate-only additive-library tier question. **Zero published-score movement across
the entire task.**

## Dispatch chain (all orchestrator-verified against artifacts)
- **P145 → Research Agent — DOI verification.** VERDICT YES-ISOLATED. E471 isolated by name in Sellem et al.,
  *PLoS Medicine* 2024 (PMID 38349899, DOI 10.1371/journal.pmed.1004149): overall cancer HR 1.15 (1.04–1.27),
  breast 1.24 (1.03–1.51), prostate 1.46 (1.09–1.97) — **orchestrator re-verified all 3 HRs directly against the
  PubMed abstract.** CVD paper (BMJ 2023, PMID 37673430) isolates E472b/E472c + celluloses E460/E466. Evidence =
  Weak-to-Moderate (single cohort, zero independent replication, no EFSA post-2024 re-eval). The prior library note
  "could not isolate E471" was factually superseded. No OFF (literature/Crossref/EuropePMC/openFDA clients only).
- **P146 → Nutrition Agent — EV-060 annotation + KB-003.** EV-060 `corroborating_evidence` row (flax=mucilage
  caveat; keys/tiers/magnitude/activation byte-identical); KB-003 (INFOGEST/Caco-2 + phytate) created behind the KB
  firewall. 2 real DOIs (Minekus 2014, Gupta 2015), 2 marked "source pending", 0 fabricated.
- **P147 → Nutrition Agent — EV-061 drafted.** Registered with verified DOIs/PMIDs, exact HRs, ADDITIVE-SPECIFIC
  granularity, Weak-to-Moderate strength, should_affect_score_now=false, published_scores_moved=0; row-8 factual
  note corrected (tier value left pending D7).
- **P148 → Product Agent — D7 co-sign APPROVED.** E471→contested; E472b/c→new combined contested row; E460→contested
  WITH 24-month replication-revert condition; E472e/DATEM no-change; E466 corroborated/unchanged. All 5 tripwires
  checked → none fire (annotate-only display labels, 0 score weight per EV-043 §w3 / EV-059 §7.4) → in-lane call.
- **P149 → Data Agent — applied.** additive_tiered_library_v1.md: E471 row 8→contested; E466 row 17 +PMID 37673430;
  new rows 48 (E472b/c) + 49 (E460, with caveat); §8.4 distribution-delta note (EV-059 §7.3 not rewritten). EV-061
  registry governance → "D7 co-sign COMPLETE".

## close_reason
CLOSED 2026-06-15 by orchestrator after artifact verification of every claim:
- E471 row 8 = `**contested**` (additive_tiered_library_v1.md:64); E472e/DATEM row 9 still `likely-neutral`
  (untouched); E466 row 17 contested + PMID 37673430; new rows 48 (E472b/c) + 49 (E460 w/ 24-mo revert caveat).
- EV-061 registered with governance "D7 co-sign COMPLETE"; HRs orchestrator-verified against PubMed PMID 38349899.
- EV-060 corroborating row + KB-003 present; KB firewall language present; 0 fabricated DOIs.
- **Scope clean:** TASK-285 footprint = exactly 2 governance markdown files (library + registry). Engine files
  (score_engine/constants/signal_extractor) = 0 emulsifier/EV-061 content; comparison JSONs = 0 TASK-285 content
  (the 6 dirty JSONs are unrelated prior workstreams: granola, cookies-coffee #7, yogurts gates).
- **Zero published-score movement** — additive tiers are annotate-only display labels carrying no score weight; no
  flag activated; no engine edit.

## Notes
- HEAD moved mid-task 97a9213b → 4cf58ac0 = the OWNER's own TASK-278/284E go-live commit (rescore 6 cats, update
  comp JSONs, re-freeze milk; owner-authored 17:59). Separate owner-ratified workstream, not TASK-285. It absorbed
  P146's EV-060 row + the EV backlog into HEAD; EV-061 + library edits sit uncommitted on top, intact.
- EV-060 row + the EV-061/library edits remain **uncommitted** in the working tree (orchestrator does not commit
  without owner instruction). KB-003 is a new untracked file. Available to fold into the next commit when desired.
- **Forward maintenance item:** E460 `contested` tier reverts to `likely-neutral` absent independent replication
  by **2028-06** (per D7 condition).
- 6 of 7 dump items = no engine work (#3 already shipped as EV-060; #1/#7 covered by EV-008/009 + EV-001/003/045/051;
  #4/#5/#6 not label-parseable → KB reference only).
