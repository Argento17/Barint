# Bari Weekly Cross-Routine Synthesis — Routine Spec v1

**Status:** CREATED & LIVE (owner-triggered 2026-06-23). **Registry:** TASK-382.
**Serves:** the owner directly — a weekly strategic digest across the three daily routines.

## Live routine (cloud)
- Routine ID: `trig_01Dw7DzbXJXuUKWWhyDDHbjE` · Manage: https://claude.ai/code/routines/trig_01Dw7DzbXJXuUKWWhyDDHbjE
- Cron `0 5 * * 0` UTC = **Sundays 08:00 Asia/Jerusalem** (IDT/UTC+3). First run: 2026-06-28.
- Model `claude-sonnet-4-6` · repo `Argento17/Barint` · tools: WebSearch, WebFetch, Read (read-only).
- Connector: **Gmail** (sends/drafts the report to tbarhaim@gmail.com).
- **DST:** when IL → UTC+2 (~late Oct), change cron to `0 6 * * 0`.
- Prompt is embedded **inline** in the cron (self-contained); this file is the versioned source-of-truth — keep them in sync via `RemoteTrigger` update.

## Why it re-derives (it does NOT read the dailies' run histories)
Verified 2026-06-23: Project Comp, BSIP2 Evidence Watch, and the Hebrew Health Scan all output to
**run history only** — they persist nothing to the repo (comp `daily_reports`/`comp_action_queue`,
`evidence_watch_log` all empty; no routine-authored commits). And a cloud agent **cannot** read another
routine's run history: it's behind claude.ai auth (WebFetch fails on authenticated URLs) and the routine
API exposes only list/get/create/run (`get` returns the routine *definition*, not run outputs).
So this synthesizer **derives the week's picture itself**: reads the durable repo state (file 9, KB,
evidence registry, comp source registry, tasks) + does a fresh themed web sweep, then synthesizes.

**Optional future upgrade (not built):** to make it *truly aggregate* the dailies, point all three at a
shared Notion log (they have the connector) and have this routine read that. Requires editing the two
existing routines — phase 2 only if the owner wants it.

## What it produces — the 4-bucket report (emailed weekly)
Per item: finding · source URL · tag [ACT / WATCH / DROP] · one-line why · suggested owner agent.
2–4 strongest items per bucket; empty bucket = "אין חדש / nothing new".
1. **Content Agent Hebrew skills** — register/voice lessons (emulate/avoid, fresh translationese tells) → content-agent (TASK-374).
2. **Category opportunities** — shelves/products to build next, competitor gaps → product-agent.
3. **Scoring/methodology scope** — candidate signals; ONLY label-derivable → EV-### candidate, else KB/decline; never a score move (EV+D7-gated, owner if published) → nutrition-agent + product-agent.
4. **Editorial/content opportunities** — caveats, comparison/blog topics, label-literacy, timely IL product-tests → content-agent + marketing-agent.

## Firewalls (same as the rest of the system)
Propose-only (no score move, no final copy, no repo writes, no task edits) · signal-not-evidence ·
no data inheritance (OFF banned) · label-derivability gate on bucket 3 · cite every source URL · no
hallucinated coverage · honest-thin over padded · consumer copy must go through the two-gate (never drafted here).
