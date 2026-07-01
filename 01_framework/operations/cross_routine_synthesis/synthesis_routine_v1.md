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

## How it aggregates — the shared Notion Log (phase 2, BUILT 2026-06-23)
Background: the three dailies output to **run history only** and a cloud agent **cannot** read another
routine's run history (claude.ai auth + the API exposes no run-output export). So run-history can't be
auto-aggregated. **Solution (owner-approved):** a shared **Notion database, "Bari Routine Log"**, that
all three dailies now append to, and this synthesizer reads.
- Notion DB: `fb50a533316440c4a571f9bb32206e48` · data source `collection://77bd20b8-fd7f-4486-b477-475a387f6b5e` · under the "Bari" Notion page.
- Schema: Finding · Date · Routine · Bucket (the 4 owner buckets + Context/other) · Tag (ACT/WATCH/DROP) · Detail · Source URL · Owner · Status (New/Reviewed/Actioned/Dropped — for human triage).
- The three dailies each got a Notion connector (`notion-create-pages`) + a logging step; they append one row per finding (same firewalls — no copied phrasing, no inherited data). This synthesizer reads the last 7 days (Notion query, or fetch+filter), groups by Bucket, and emails the 4-bucket report. A light **gap-fill web sweep** remains as a secondary supplement only.

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
