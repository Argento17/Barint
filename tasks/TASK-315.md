---
id: TASK-315
title: Port frontend for cakes / cookies-coffee / brined onto Barint deploy repo → PR (the 3 pages PR #7 couldn't carry)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-314]
blocks: []
category_id: null
close_reason: >
  Frontend Agent ported the 3 pages onto Barint → PR #8 (https://github.com/Argento17/Barint/pull/8). Orchestrator-verified
  against the pushed branch: exactly 17 files, ALL ADDITIONS (no collateral changes to origin/master's frontend → bounded port,
  shared deps corpus/registry/view-models reused). cakes RT-6 fix confirmed _meta-ONLY (schema cookies-coffee-v1→cakes-hard-cookies-v1,
  version v2→v1; products/scores untouched). The 3 data JSONs = the TASK-310-verified set (cookies/brined sha256 byte-identical;
  cakes = verified + meta-only fix) → score==data + OFF=0 carry over. Agent reported tsc 0 + npm run build 0 (51 pages, all 4 routes
  in output); Vercel preview on PR #8 is the authoritative build gate. NOT merged/deployed (owner-gated).
  REMAINING (escalated to TASK-314, NOT a quick add): the /hashvaot INDEX is hand-built with a bespoke FeaturedXIntelligenceCard per
  category + still lists monorepo-wiped categories (butter/maadanim/cheese/bread) → linking the 3 new pages = bespoke card work
  entangled with the broader index/divergence reconciliation; sequences after merge; governed by the stock-theme-image rule.
summary: >
  PR #7 (Argento17/Barint) landed the 4 route-ready re-baseline pages. The other 3 (cakes, cookies-coffee, brined-cheeses)
  have NO routes/loaders/components on Barint `master`, so their verified pages can't render there. Port the bounded
  dependency closure from the monorepo line (task-275-engine-fixes-abc) onto a Barint-master-based branch: 3 route page.tsx,
  3 lib/comparisons/*-page-data loaders, 3 components/comparisons/*-comparison-page components, lib/seo/faq-schema.ts + the
  FAQ schema JSONs, the 3 verified data JSONs, and any minimal shared-lib delta needed (e.g. view-models 8-line diff).
  Shared deps (corpus.ts, registry/types.ts, view-models) ALREADY EXIST on master and are near-identical → port should not
  cascade into the broader 112-file divergence. Build (tsc + npm run build) against master's frontend; resolve missing imports
  minimally by porting from task-275; verify the 3 routes render + score==staging. Push branch to origin (Barint), open PR
  (base master). Vercel preview = build check. NEVER merge/deploy (owner-gated). If the dependency closure cascades and can't
  build cleanly, STOP and report the blocker list — do not force. Also fix RT-6 (cakes _meta.schema wrong category/version)
  while porting cakes.
---

# TASK-315 — Port the 3 missing-route pages onto the Barint deploy repo

Sibling of PR #7 (which carried the 4 route-ready pages). See DISPATCH_BOARD + [[deploy_topology_main_vs_monorepo]].
