---
id: TASK-473
title: Social content: 10 FB/IG posts (concrete Bari use cases)
owner: marketing-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-03
depends_on: []
blocks: []
category_id: null
summary: >
  Author 10 distinct FB+IG social posts grounded in REAL live-category Bari data (>=5 concrete product/comparison), owner honesty hard-rules (no bad/dangerous/medical/invent, don't-tell-what-to-buy, label-relative language), exact A-I format + table. Then Adversarial QA/Red-Team gate on hard-rules + no-invention + rank-checks. Natural Israeli Hebrew.
---

# TASK-473 — Social content: 10 FB/IG posts (concrete Bari use cases)

## Status — 2026-07-03: red-team GO_WITH_FIXES, fix round in flight
- **Chain:** P492 Marketing Agent authored 10 posts (6 concrete, grounded in real category JSONs, A–I + table + grounding ledger; NOT authored inline by orchestrator per content-signoff rule) → P493 Adversarial QA/Red-Team gate (verified every superlative/count against FULL category JSONs, not samples).
- **Gate result:** GO_WITH_FIXES. 9/10 clean. Highest-risk claims VERIFIED true (Post 10 סלט חומוס 18.2g = genuine category-max protein; Post 8 "only one B of 32" correct; Post 7 sodium 231mg = true category min; Post 1 Vitabix 10g = true category-max fiber — several claims were UNDERstated, good author discipline). Findings: RT-1 CRITICAL Post 8 invented count (13/32 "≈half" → true 12/32, 37.5%); RT-2 HIGH Post 7 bare raw mean 52.8 exposure (no grade wrapper, no Exception Registry entry); RT-3 HIGH Post 7 scare-quoted "רע" adjacent to named bottom product; RT-4 MED Post 9 uncited fruit-snack generalization; RT-5 MED Post 4 full-body re-scan.
- **Fix round:** SendMessage → Marketing Agent (a6e183c56e953a059) to correct posts 7/8/9 (+confirm 4), copy-only, data-true. Then red-team re-confirm touched posts → present to owner.
- **Canva:** connector LIVE, Bari brand kit (kAHOOLmPnYE) + existing Bari social designs present (mascot brand covers + a 4-page IG carousel "מוצרי סופרמרקט — השוואות רב-פרמטריות"). On copy approval → assemble post visuals in Canva off brand kit, RTL-checked, export FB/IG.
- **Note:** dovetails owner marketing weeks (Item 8) — these are the finding-posts.
