---
id: TASK-315
title: Port frontend for cakes / cookies-coffee / brined onto Barint deploy repo → PR (the 3 pages PR #7 couldn't carry)
owner: frontend-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-314]
blocks: []
category_id: null
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
