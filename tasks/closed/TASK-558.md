---
id: TASK-558
title: Repurpose BSIP2 Evidence Watch → Corroboration Ledger
renumbered_from: TASK-462 (2026-07-10, id collision — the 07-02 "CI green sweep" task is the canonical TASK-462; archive-board references to TASK-462 belong to it, not this task)
owner: orchestrator
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  Done + verified. RemoteTrigger update returned HTTP 200 with the new config confirmed
  on trig_01DCRbbmLuHtTV7S4Uhz3CfB: name="BSIP2 Corroboration Ledger", model=claude-sonnet-5,
  allowed_tools=[Bash,Read,Grep,WebSearch,WebFetch], Notion connector persisted
  (notion-create-pages + notion-fetch, data source 77bd20b8…), cron unchanged (0 5 * * *),
  next_run 2026-07-04T05:07Z. New prompt = tier-durability ledger (rotate roster, classify
  CORROBORATES/CONTRADICTS/REFINES, dedup+significance gate, Notion-only sink). Label-derivability
  firewall dropped; git-push/repo-write steps removed; PROPOSE-only + OFF-ban intact. Memory
  scheduled_routines_state updated. First live run 2026-07-04 05:00 UTC to be spot-checked.
depends_on: []
blocks: []
category_id: null
summary: >
  Repurposed dead cloud routine trig_01DCRbbmLuHtTV7S4Uhz3CfB from label-derivable new-findings hunt (firewall-starved, 0 registry entries ever traced to it, never-committed dedup log) to a tier-DURABILITY ledger: rotates the evidence-registry roster, classifies fresh literature as CORROBORATES/CONTRADICTS/REFINES vs existing verdicts, writes to Notion Bari Routine Log only. Label-derivability firewall dropped; PROPOSE-only + OFF-ban firewalls intact; model→sonnet-5.
---

# TASK-558 (né TASK-462) — Repurpose BSIP2 Evidence Watch → Corroboration Ledger

## Why

The routine ran daily since 2026-06-01 and was effectively a no-op. Root causes (evaluated
2026-07-03): (1) its **label-derivability firewall** rejects almost all fresh food science
(mechanistic / animal / regulatory / in-vitro is not readable off a Hebrew label) → honest
`NO ACTIONABLE FINDINGS` nearly every run; (2) **scoring never auto-codes**, so even a survivor
couldn't move anything without a separate owner TASK; (3) its dedup log dir
`03_operations/bsip2/evidence_watch_log/` **was never committed** (cloud agents can't push —
the same 403 that forced Hebrew Health Scan local and stranded Project Comp), so it could neither
dedupe across runs nor be read; (4) **redundant** with the owner-TASK evidence-registry flow that
does the real work. Grep confirmed **zero** of the ~40 registry EV-### entries trace to the watch —
every one cites a `TASK-XXX`.

## What changed

Repurposed to the one thing a cloud agent can actually do well: a **tier-durability ledger**.
Instead of hunting new label-derivable findings, it now checks whether Bari's *already-established*
evidence tiers are being corroborated, contradicted, or refined by fresh literature, and maintains
that as a running Notion ledger the Weekly Synthesis reads.

- Reads the evidence-registry roster from the repo checkout (confirmed present on origin/master).
- Deterministic `day-of-year mod 7` rotation → ~1/7 of the roster/day, whole roster/week, no memory.
- Classifies each fresh (last-30d) source: CORROBORATES / CONTRADICTS / REFINES / NEUTRAL.
- Dedup + significance gate (queries own last-60d Notion rows): logs only CONTRADICTS/REFINES,
  a stronger-grade corroboration, or a >90d durability re-confirm. Same-strength restatements dropped.
- Sink = Notion "Bari Routine Log" only (cloud can't commit — git steps removed).
- Firewalls intact: PROPOSE-only (a CONTRADICTS = flag for an owner-gated D6/D7 Nutrition TASK,
  moves nothing itself), OFF-ban, no dose/bioavailability inherited as a score input.

## Decision authority

No tripwire fired — reconfigures an existing minor routine that by design cannot change a published
score; fully reversible via another RemoteTrigger update. Acted autonomously on owner's direct
"repurpose it"; logged here + in memory `scheduled_routines_state`.

## Follow-up

Spot-check the first live run (2026-07-04 05:00 UTC) at claude.ai/code/routines and confirm at
least one sensible ledger row lands in the Notion "Bari Routine Log" (or a clean `NO LEDGER UPDATES`).
