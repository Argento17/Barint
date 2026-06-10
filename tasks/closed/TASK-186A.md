---
id: TASK-186A
title: Build the v2 Chief-of-Staff surface into the live dashboard (personal layer + portfolio demotion)
owner: cc-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-05
completed_at: 2026-06-05
close_reason: "parent TASK-186 closed"
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
summary: >
  Made the v2 surface real and previewable: killed the left-rail monitoring spine (render+CSS+voice timer); added GET /api/personal to serve.py (live, in-memory, NEVER persisted) importing google_workspace, with a LOCAL-TZ calendar fix; built the exception-gated top-to-bottom surface in command_center.html (prose brief, YOUR DECISION, INBOX-needs-you with draft-reply STUB button, TODAY/THIS WEEK, HANDLED-so-you-didnt-have-to absorption KPI, GOING WRONG/decide-or-kill); demoted the entire old task board into one collapsible BARI PORTFOLIO tile (reuses existing render, nothing deleted); backed up command_center.html to command_center_v1_backup.html. Privacy: no personal data in any git-tracked file (verified). Also fixed a connector bug: google_workspace _api_get now uses urlencode(doseq=True) so Gmail metadataHeaders populate (sender/subject were empty). Owner-gated go-live: previews first, NOT self-closed.
---

# TASK-186A — Build the v2 Chief-of-Staff surface into the live dashboard (personal layer + portfolio demotion)

## What
Made the v2 surface (`command_center_v2_operating_model.md`, Rev 1+2) **real and previewable**.
Until now only design + plumbing existed; Tom still saw the old board. This wave renders the
new Chief-of-Staff surface and demotes Bari to one portfolio tile.

## Built
- **Killed the monitoring spine** — removed `renderSpine`/`spineStats`/`spineVoiceLines`/
  `startSpineVoice`, all `.cc-spine*` CSS, the scan animation, the voice timer, and the
  page-wide aurora drift animation.
- **`GET /api/personal` in `serve.py`** — live, in-memory only, NEVER persisted. Imports
  `integrations.clients.google_workspace`; returns `status()`/`inbox_triage()`/local-tz
  `calendar_day()`. Not-linked → `{connected:false, hint}`; read error → honest message.
  `Cache-Control: no-store`.
- **Local-tz calendar fix** — `calendar_day()` bucketed "today" in UTC (read 0 events).
  Endpoint computes the day window in local time and passes it to `gw.list_events()`.
- **New surface in `command_center.html`** (exception-gated, top→bottom): prose brief ·
  YOUR DECISION (framed, registry) · INBOX — needs you (`/api/personal`, draft-reply
  **stub** button, read-only) · TODAY/THIS WEEK (local tz) · HANDLED SO YOU DIDN'T HAVE TO
  (absorption KPI) · GOING WRONG / DECIDE-OR-KILL · **BARI PORTFOLIO** (entire old board
  demoted into one collapsible tile, existing render reused, nothing deleted).
- **Backup** `command_center_v1_backup.html` for reversibility.
- **Connector bugfix** — `_api_get` now `urlencode(..., doseq=True)` so Gmail
  `metadataHeaders` populate (sender/subject were silently empty). Read-only, no posture
  change.

## Privacy (hard constraint, verified)
No personal inbox/calendar data is written to any git-tracked file. `git status` clean of
personal data; credential path (`~/.bari/google_token.json`) untouched.

## Preview
`cd C:\Bari\05_command_center && python serve.py` → http://localhost:8080/command_center.html

## roadmap_impact
`true` — reshapes Tom's primary instrument. **NOT self-closed** — go-live is owner-gated;
Tom previews first.

## Stubbed / degraded (honest)
- Draft-reply button is a disabled read-only stub (later wave).
- Inbox triage = `is:unread in:inbox` (includes some Updates-category mail); refine senders
  later. Personal hydration is sequential per-message and takes a few seconds to fill.

**Parent:** TASK-186. **Assigned:** cc-agent.
