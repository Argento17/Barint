---
id: TASK-382
title: Weekly Cross-Routine Synthesis — emailed 4-bucket owner report across the daily routines
owner: orchestrator
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-23
depends_on: [TASK-381]
blocks: []
category_id: null
summary: >
  A weekly cloud routine that synthesizes the discourse/evidence/voice picture across the three daily
  routines (Project Comp, BSIP2 Evidence Watch, Hebrew Health Scan) into one owner-facing report in 4
  buckets - (1) Content Agent Hebrew skills, (2) Category opportunities, (3) Scoring/methodology scope,
  (4) Editorial/content opportunities - each item tagged ACT/WATCH/DROP with source URL + owner agent,
  and EMAILS it to the owner. Owner-initiated 2026-06-23 (email + weekly).
---

# TASK-382 — Weekly Cross-Routine Synthesis (emailed 4-bucket owner report)

**Spec:** `01_framework/operations/cross_routine_synthesis/synthesis_routine_v1.md`.
**Memory:** [[scheduled_routines_state]].

## Owner direction (2026-06-23)
- Want a regular check across Project Comp + the other two routines, producing a report on what to do in
  4 buckets: Content Agent Hebrew skills · Category opportunities · Scoring/methodology scope · Editorial/content.
- Delivery: **email** (Gmail). Cadence: **weekly**.

## Key finding that shaped the design (verified 2026-06-23)
- The three daily routines persist **nothing** to the repo (comp daily_reports / comp_action_queue /
  evidence_watch_log all empty; 0 routine-authored commits) — they output to **run history only**.
- A cloud agent **cannot** read another routine's run history (claude.ai auth + the routine API has no
  run-output export; `get` returns only the definition).
- => A true auto-aggregator is not buildable now. The routine therefore **re-derives**: reads durable
  repo state (file 9, KB, evidence registry, comp registry, tasks) + a fresh themed weekly web sweep.

## LIVE (created 2026-06-23)
- Routine `trig_01Dw7DzbXJXuUKWWhyDDHbjE`, cron `0 5 * * 0` UTC = Sundays 08:00 IL; first run 2026-06-28.
  Manage: https://claude.ai/code/routines/trig_01Dw7DzbXJXuUKWWhyDDHbjE
- Inline self-contained prompt; read-only tools + Gmail connector (send-or-draft to tbarhaim@gmail.com).

## Phase 2 — Notion Log BUILT (2026-06-23, owner: "Notion Log is amazing!")
- Shared Notion DB **"Bari Routine Log"** created under the "Bari" page: db `fb50a533316440c4a571f9bb32206e48`,
  data source `collection://77bd20b8-fd7f-4486-b477-475a387f6b5e`. Schema: Finding/Date/Routine/Bucket/Tag/
  Detail/Source URL/Owner/Status. Seed row written (write verified).
- All 3 dailies wired to APPEND (Notion connector + `notion-create-pages` + logging step), firewalls intact:
  - Hebrew Health Scan `trig_01CkS9V6cacHDY3WCToqrK9i` (Lane A→Content-Hebrew, Lane B→Scoring/etc.)
  - Project Comp `trig_0171rxWLPZrTBfUjquGVA2vJ` (Assignment-Queue actionables P0-P2)
  - BSIP2 Evidence Watch `trig_01DCRbbmLuHtTV7S4Uhz3CfB` (findings→Scoring/methodology; Notion = reliable sink vs its 403ing git push)
- Weekly Synthesis `trig_01Dw7DzbXJXuUKWWhyDDHbjE` rewired: READS the log (last 7 days, Notion query/fetch),
  aggregates by Bucket, emails; re-derive demoted to a gap-fill. Notion + Gmail connectors attached.

## NOT done (follow-ups)
- **Verify first weekly run (2026-06-28):** (a) email delivered vs draft-only (Gmail connector); (b) the
  Notion query/read worked (plan may gate `notion-query-data-sources` → fallback is fetch+filter). Adjust if needed.
- **Verify the dailies actually write Notion rows** — check the DB after the next daily runs (HHS already
  ran 08:32 IL today BEFORE the Notion wiring; first Notion write expected next run).
- Keep each inline cron prompt in sync with its spec doc.
