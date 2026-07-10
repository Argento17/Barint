---
id: TASK-436
title: Per-category refresh program: pre-deploy movement census (published vs current-master engine, incl. fiber-gate ON delta)
owner: data-agent
status: CLOSED
closed_at: 2026-07-01
close_reason: Census delivered + orchestrator-verified (ran harness directly after Data Agent hallucinated). OWNER RULED 2026-07-01: fiber-gate BUNDLES into next refresh (grade-neutral, no standalone activation); per-category root-cause program APPROVED, serial, starting brined_cheeses -> TASK-438. protein_bars flagged baseline-not-pinned. Report per_category_movement_census_v1.md.
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-418, TASK-429, TASK-432]
blocks: []
category_id: null
summary: >
  Score-neutral analysis: for every live category, movement table published->current engine (OFF baseline) + isolated fiber-gate-ON delta, each mover classified DATA-CLEAN/ENGINE/FIBER-GATE, per-category refresh verdict. Deploy is owner-gated per category (tripwire #1). Dispatched to Data Agent in isolated worktree.
---

# TASK-436 — Per-category refresh program: pre-deploy movement census (published vs current-master engine, incl. fiber-gate ON delta)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->


## RESOLUTION (2026-07-01, orchestrator — census delivered deterministically)
Dispatched Data Agent(s) mis-delegated (hallucinated "now running in background" loop, worktree never created, 0 real work — same P275 pattern; chain stopped via TaskStop). Orchestrator ran the census DIRECTLY with the proven `provenance/_reproduce_diag.py` harness (score-neutral, writes only diag JSON) against master 78d61c18, two passes (fiber OFF / ON).

**Deliverable:** `03_operations/page_generator/reports/per_category_movement_census_v1.md` (sha256[:16]=914e3591c8639691) + `provenance/_census_fiber_OFF.json` / `_census_fiber_ON.json`.

**Findings (verified — orchestrator ran the harness):**
- **Fiber-gate activation is grade-neutral:** 0 new grade moves in any of 16 categories, ON vs OFF; ≤0.4pt nudges only. The fiber-gate is a correctness fix, NOT a score-mover.
- **4 categories reproduce published 100%** (cereals, chocolate_bars, chocolate_tablets, snacks).
- **Needs per-category owner ruling (genuine drift):** brined_cheeses (14 drift, 3 grade A→B/B→C, incl. the GOLDEN page), cakes (26 drift, 3 grade D→E), cookies_coffee (9 drift, 1 grade D→C up), juices (6 drift, 1 grade D→E = EV-045 / TASK-437).
- **BASELINE-NOT-PINNED (movement unverifiable, flagged not asserted):** protein_bars (adhoc corpus → all 32 → insufficient_data50; published came from a different invocation — needs its own TASK-429-style pin first); hard_cheeses (loader drops bsip1_enriched; already refreshed+pinned).

**Status → BLOCKED on owner per-category refresh ruling.** The census (magnitude) is done; each actual re-flow deploy is tripwire #1. Next mechanistic step per flagged category = root-cause each mover (engine change vs invocation gap) before a go/no-go — not yet done here.
