---
id: TASK-522
title: Analytics measurement fix package: internal-traffic filtering, @vercel/analytics beforeSend, outbound-click event, UTM convention
owner: frontend-agent
status: CLOSED
close_reason: >
  Verified in worktree C:\bari_wt_t522 off origin/master: build PASS (exit 0, full route
  generation), diff = exactly 7 files / +201-7 with no consumer-visible strings; beforeSend
  logic + internal-traffic flag + GA4 traffic_type + outbound_click confirmed at file level
  by the orchestrator (this file, Delivery log). Branch frontend/task522-analytics-measurement
  pushed to origin @ 0ac57c20; PR opened by owner (gh absent) — deploy = owner merge, per
  standing rule. Remaining GA4 Admin-UI steps are owner-side (checklist in this file).
priority: HIGH
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Close the GA4-vs-Vercel measurement gap actionably: add @vercel/analytics with beforeSend (drop /admin + internal-flagged clients), tag internal traffic in GA4 (traffic_type=internal for localhost/preview + persistent owner flag), add outbound_click event on dormant buyUrl, category param on comparison page_views, UTM convention doc for social posts, and a 5-min owner GA4-UI checklist (retention 14mo, GSC link, key event, filter activation).
---

# TASK-522 — Analytics measurement fix package: internal-traffic filtering, @vercel/analytics beforeSend, outbound-click event, UTM convention

## Context
Owner request 2026-07-08 after a traffic report showed GA4 (strict consent-gated, ~18 users/28d)
vs Vercel Web Analytics (cookieless auto-injection, ~318 visitors/7d) — GA4 sees ~5% of real
traffic and both layers count owner/agent/dev traffic. Consent posture (PPA Feb-2026 strict
opt-in) is deliberate and NOT changed by this task.

## Delivery log
- Frontend Agent built the package in the local tree (return: 6/6 deliverables, build PASS
  301/301). Orchestrator verification found the local branch (task506) had DIVERGED from
  origin/master — origin already ships `@vercel/analytics` mounted plainly in layout.tsx
  (PR-merged earlier) and the TASK-471 product-page-link code. The local build was therefore
  NOT committable as-is.
- Orchestrator ported the TASK-522-only change set onto origin/master in worktree
  `C:\bari_wt_t522`, branch `frontend/task522-analytics-measurement`:
  - `bari-web/src/lib/internal-traffic.ts` (new) — localhost/127.0.0.1/*.vercel.app auto-internal
    + persistent `?bari_internal=1|0` localStorage flag.
  - `bari-web/src/components/shared/vercel-analytics.tsx` (new) — wraps `<Analytics/>` with
    `beforeSend` dropping `/admin` paths + internal clients. No `track()` (Pro-only; Hobby plan).
  - `bari-web/src/app/layout.tsx` — plain `<Analytics/>` → `<VercelAnalytics/>`.
  - `bari-web/src/components/shared/ga4-script.tsx` — `traffic_type: 'internal'` config param
    for internal clients (GA4 Admin data filter to be activated by owner).
  - `bari-web/src/lib/analytics.ts` — `outbound_click` event added to BariEventName.
  - `bari-web/src/components/inventory/product-table.tsx` — BuyAffordance fires
    `outbound_click` {barcode, category} on buyUrl click (both desktop + mobile call sites).
  - `01_framework/operations/utm_convention_v1.md` (new) — social UTM convention + deep-link
    rule; orchestrator corrected two agent errors: dead `/hashvaot/yogurt` example route
    (checked against LOCAL tree, not origin) and a false claim that Vercel lacks UTM reporting.

## Owner GA4-UI checklist (5 min, code cannot do these)
1. Admin → Data settings → Data retention → 14 months (default is 2!).
2. Admin → Data streams → configure internal-traffic rule is NOT needed (we send
   `traffic_type=internal` directly) — but Admin → Data settings → Data filters →
   activate the `Internal Traffic` filter (it ships in "testing" state).
3. Admin → Product links → Search Console → link the bari.digital GSC property.
4. Admin → Events → mark `newsletter_signup` (and later `outbound_click`) as key events.
5. Visit bari.digital once with `?bari_internal=1` on every device/browser the owner uses.

## DoD
- [x] beforeSend drops /admin + internal (code)
- [x] GA4 traffic_type param (code)
- [x] outbound_click wired through fireEvent only
- [x] UTM convention doc with live-route examples
- [x] Worktree build passes (exit 0, all routes)
- [x] Branch pushed @ 0ac57c20; PR URL handed to owner (owner merges consumer-facing deploys):
      https://github.com/Argento17/Barint/pull/new/frontend/task522-analytics-measurement
