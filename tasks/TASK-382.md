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

## NOT done (follow-ups)
- **Verify first run delivers email** (Gmail connector may only support drafting; prompt falls back to a
  draft addressed to the owner — confirm which happened after 2026-06-28 and adjust if needed).
- **Optional phase 2:** point the three dailies at a shared Notion log so this routine *aggregates* them
  instead of re-deriving (removes duplication; requires editing Comp + Evidence Watch). Only if owner wants it.
- Keep the inline cron prompt in sync with `synthesis_routine_v1.md`.
