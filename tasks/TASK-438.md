---
id: TASK-438
title: Root-cause brined_cheeses drift (GOLDEN page): 14/36 don't reproduce, 3 grade moves down — engine drift vs stale invocation? then refresh w/ fiber-gate bundled
owner: nutrition-agent
status: BLOCKED
blocker: owner go/no-go for brined_cheeses golden-page re-flow (tripwire #1 + factory content gates); cakes/cookies_coffee root-cause queued
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-436]
blocks: []
category_id: null
summary: >
  brined_cheeses (the golden reference page) shows 14 drifters vs published, 3 grade moves (2x A->B, 1x B->C), all downward, none clean-stamped. Determine mechanism per mover (TASK-429-style: does config reproduce published; if not why); classify engine-drift vs invocation-gap vs data. If a clean refresh is warranted, prep movement table + fiber-gate bundled, owner go/no-go before deploy (tripwire #1).
---

# TASK-438 — Root-cause brined_cheeses drift (GOLDEN page): 14/36 don't reproduce, 3 grade moves down — engine drift vs stale invocation? then refresh w/ fiber-gate bundled

<!-- opened with new_task.py; fill in context / scope / the deliverable -->


## RESOLUTION (2026-07-01, orchestrator — root-cause DELIVERED + VERIFIED)
Ran forensics directly (deterministic; Data Agent lane hallucinates on measurement work). brined_cheeses drift is FULLY root-caused and NOT ambiguous:

**Mechanism (verified end-to-end):** the published golden page (`run_brined_005`, 2026-06-15) scored 14 brined cheeses as **NOVA-1**. After publication, the **EV-099 NOVA-1 gate (TASK-288, "blessed engine" commit f1d1275e)** tightened NOVA-1 qualification, so fermented brined cheeses now correctly proxy **NOVA-2**. NOVA-1->2 drops `processing_quality` 95->85 (NOVA_PROCESSING_SCORES, weight 0.15 = -1.5) and `whole_food_integrity` 100->90 (weight 0.04 = -0.4) = the uniform **-1.9/-2.1**. Confirmed by (a) dimension diff of mover 7290108509106 (only processing_q 95->85 + WFI 100->90 changed; all 8 other dims byte-identical), (b) published trace shows nova_level=1 / processing_q=95 for that product, (c) removing the config's 2 extra flags (SHELF_RELATIVE_V1/FAT_TECH_V1) did NOT change the drift = not an invocation gap, (d) exactly the 14 run_005 NOVA-1 products moved; the 22 already-NOVA-2/3 are byte-identical.

**NOT an invocation gap (unlike HC/TASK-429), NOT data (0 clean-stamped) — genuine, INTENTIONAL, owner-blessed engine evolution the golden page predates.**

**Full re-flow (current engine + fiber-gate bundled — fiber is inert for brined):** 36 products, 14 movers (all -2.1), **3 grade moves down** (7290108509106 A->B, 7290011499129 A->B, 7290108509755 B->C). #1 product (85.4) stays A. Table: `03_operations/page_generator/reports/brined_cheeses_reflow_table_v1.json`.

**RECOMMENDATION: SHIP the re-flow** — the blessed engine is the source of truth; holding NOVA-1 scores on cheeses the engine now classifies NOVA-2 = shipping stale numbers on the GOLDEN reference page. BUT this is tripwire #1 (published consumer-facing scores on the golden page) and 2 products drop A->B, so it MUST go through the factory (rescore -> copy reconciliation for any grade/rank claims that break -> two-gate content sign-off -> C0 gates -> deploy), NOT an inline number swap (orchestrator must not author/ship content inline). **Owner go/no-go required to authorize the re-flow.**

**Other 3 queued categories characterized (shape only, not yet root-caused):**
- cakes: SCATTERED drift (-6.5..-5.3..+3.1), 3x D->E, up to -6.5 — multi-cause, biggest open, needs own investigation.
- cookies_coffee: mostly tiny (<=1.6) + one +7.3 UPWARD grade correction (7290119043149 D->C). Low-stakes.
- juices: already ruled (EV-045 backlogged, TASK-437); residual mixed, 1 product.

**Status -> BLOCKED on owner go/no-go for the brined golden-page re-flow (tripwire #1); cakes/cookies_coffee root-cause queued.**
