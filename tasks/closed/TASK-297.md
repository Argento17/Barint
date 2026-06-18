---
id: TASK-297
title: Clean-baseline wipe — remove butter/cheese-spreads/salty-snacks/bread/yogurts (page+route only) + delete stale dup frontend versions
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  Frontend Agent (C1) wiped 5 categories page+route-only; orchestrator INDEPENDENTLY verified (not on the
  agent's word): re-ran `npx tsc --noEmit` = exit 0 and `npm run build` = exit 0 myself. Build route manifest
  shows exactly the 13 kept /hashvaot routes (breakfast-cereals, brined-cheeses, cakes, cakes-hard-cookies,
  cookies-coffee, granola, hard-cheeses, hummus, juices, milk-comparison, snack-bars, snacks, vegetable-spreads)
  with butter/cheese/salty-snacks/bread/bread-comparison/yogurts ABSENT. grep for wiped-category frontend refs in
  bari-web/src = 0 live (only inert string inside archive/yogurts_frontend_v2.json). All 9 kept comparison JSONs
  present; all wiped JSONs gone. Agent deleted 75 files / edited 6 (routes, comparison JSONs, SEO faq, blog
  routes+content, page-data libs, shelf-filters, registry entries, landing index, sitemap, home category list) +
  stale dups brined_v1/cookies_coffee_v1; build-green proves no over-deletion broke a kept import. Scope honored:
  nothing outside bari-web/ touched (raw scrape/corpus/BSIP retained). No commit, no deploy (owner-gated).
depends_on: [TASK-296]
blocks: []
category_id: null
summary: >
  Owner-mandated clean-up (2026-06-16): wipe 5 non-conforming categories from the website (page + route only; raw scrape/corpus/BSIP data stays in repo). bread frozen-invariant override RATIFIED by owner. Remove frontend JSON + /hashvaot route(s) + SEO FAQ schema + blog content + page-data lib + shelf-filters + landing-index entry + sitemap/robots refs for each. Also delete stale duplicate frontend versions (brined v1, cookies_coffee v1). npm run build + tsc must pass. NO deploy (owner-gated).
---

# TASK-297 — Clean-baseline wipe — remove butter/cheese-spreads/salty-snacks/bread/yogurts (page+route only) + delete stale dup frontend versions

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
