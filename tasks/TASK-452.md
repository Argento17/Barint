---
id: TASK-452
title: Restore + reactivate verify_citations.py C0 gate (source lost; only stale .pyc remains — fabrication check is dead)
owner: data-agent
status: CLOSED
close_reason: >
  Gate restored + reactivated + committed. Recovered c90d49ef source, reconciled vs newer
  .pyc (author-year corroboration), implemented the --json stdin contract validate_return.py:301
  calls, fixed the case-sensitive stop-word bug. Verified: C6 flips WARN→hard-FAIL on a
  fabricated citation, PASS on a real one; --all 33/43 PASS, 0 fabricated. Committed e4cd6d30
  on the live branch (feature/homepage-mascots) to keep the gate ON. Follow-ups (non-blocking):
  (1) 'IJE' journal-abbrev stopword gap — 2 false MISMATCH in --all mode only, C6 path safe;
  (2) 4 real citation defects → TASK-454 triage; (3) consolidate to master (see risk note).
priority: HIGH
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-451 scoping found the citation-fabrication gate is HALF-DEAD: validate_return.py:301 (C6) hands off to 03_operations/validators/verify_citations.py, but the SOURCE is absent from master AND HEAD (only committed once at c90d49ef 2026-06-23 on an unmerged branch; a Jun-25 .pyc exists suggesting newer lost edits). So vc.exists()=False and C6 degrades to PMID/DOI FORMAT-check + WARN only — agent-invented citations are shape-checked, never resolved against PubMed/Crossref. verify_citations already imports literature.pubmed_fetch + crossref.get_doi. RESTORE the c90d49ef source, reconcile vs the .pyc, BEHAVIORALLY TEST (real PMID->PASS, fake->FABRICATED, retracted DOI, exit 0/1/2), confirm the validate_return.py:301 handoff goes live, and check no false-positives on existing shipped citations before activation. Score-neutral (reject-only) but gate-behavior-affecting. Ties TASK-451 #1 + the TASK-447 'gates exist but not enforced' theme.
---

# TASK-452 — Restore + reactivate verify_citations.py C0 gate (source lost; only stale .pyc remains — fabrication check is dead)

## RESOLUTION (2026-07-02) — restored, fixed, committed LIVE (e4cd6d30)
See close_reason. Gate is on: `validate_return.py:301` C6 handoff now resolves PMIDs/DOIs against PubMed/Crossref and hard-fails fabrications (was format-check + WARN for weeks).

## ⚠️ TOPOLOGY RISK (→ owner, root-cause of how this gate was lost)
verify_citations was originally lost **because it was committed only to an unmerged branch (c90d49ef)** — master never got it. I've now committed the restored gate to the current live branch (`feature/homepage-mascots`) to keep it ON, but **if that branch also never merges to master, we repeat the exact failure.** The session's gate fixes are now scattered: OFF neutralize + off_sweep on branch `task448/off-ban-neutralize-callers` (NOT in the homepage-mascots working tree → the off_sweep fix isn't even live on the current branch), verify_citations on `feature/homepage-mascots`. **The live Agent-OS line is unconfirmed** ([[deploy_topology_main_vs_monorepo]], [[local_origin_brain_divergence]]). NEEDS an owner decision: consolidate all gate/governance fixes onto master (or the confirmed live line) and merge, so nothing lives on a branch that can vanish.

## FOLLOW-UPS
- 'IJE' journal-abbrev stopword gap (2 false MISMATCH, --all mode only; C6 single-contract path unaffected). Better fix than whack-a-mole: don't treat ALL-CAPS tokens as surnames (surnames are Titlecase) — a gate-logic decision, fold into TASK-453.
- 4 real citation defects → TASK-454 triage (PMID 31122155 / D6 BARI_HC_NOVA1_V1 routed to Nutrition).

<!-- Live view: tasks/DISPATCH_BOARD.md. -->
<!-- opened with new_task.py -->

