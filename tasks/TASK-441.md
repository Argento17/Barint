---
id: TASK-441
title: Re-flow juices to current engine (6 movers, 1x D->E grapefruit)
owner: data-agent
status: CLOSED
closed_at: 2026-07-01
close_reason: Owner 'go ahead all the way' on recommended defaults. Juice default = LEAVE AS-PUBLISHED: its only grade move (grapefruit 7290019056737 D->E) is the EV-045 count-surcharge over-penalty ruled indefensible + BACKLOGGED (TASK-437). Re-flowing would ship a known defect, so no re-flow; juices stays at published v3. Becomes a real re-flow only if EV-045 refine is un-backlogged + built (Product co-sign). No score changed, nothing deployed.
priority: MEDIUM
created_at: 2026-07-01
depends_on: [TASK-436, TASK-437]
blocks: []
category_id: null
summary: >
  juices residual drift; grapefruit D->E is EV-045 count-surcharge (backlogged as a defect per TASK-437). Decide: re-flow current engine as-is, or hold grapefruit pending EV-045 refine. Rescore -> copy reconcile -> gates.
---

# TASK-441 — Re-flow juices to current engine (6 movers, 1x D->E grapefruit)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## STAGED (2026-07-01, orchestrator) — CONFLICT surfaced
rescore_all --shelf juices: 5 score-moves, **1 grade move 7290019056737 D->E** — and that grapefruit D->E IS the EV-045 count-surcharge defect TASK-437 ruled an OVER-PENALTY (BACKLOGGED by owner 2026-07-01). **Re-flowing juices as-is would SHIP a grade drop Nutrition already ruled indefensible.** Autonomous resolution: HOLD the grapefruit at D (do not ship the defect) -> juices then has 0 legit grade moves + only sub-point drift = a near-no-op re-flow not worth publishing until EV-045 refine is un-backlogged. **So juices "fix" = un-backlog + build BARI_ECS_TIER_GATED_COMPLEXITY_V1 (Product co-sign), OR leave juices as-published.** = owner call.
