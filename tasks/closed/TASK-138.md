---
id: TASK-138
title: "Tri-category full-cycle BSIP0->BSIP2 assignment (Yogurts replace / Cereals greenfield / Cottage-White Cheese) — coordination + decision map"
owner: cc-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "Implementation roadmap has been created and executed in other tasks (e.g. TASK-142)"
depends_on: []
blocks: []
category_id: null
work_type: coordination
summary: >
  Product-Owner-assigned, CC-Agent-owned umbrella: run the full real Shufersal-sourced BSIP0->BSIP2 cycle
  for three categories in STRICT PARALLEL — Yogurts (replace live DEC-005 manual shelf via a calibrated
  engine), Cereals (clean greenfield), Cottage/White Cheese (governance-stress-test-first). CC owns registry
  accuracy + the live decision map + hand-off prompts; it does not score or code. Workstreams: TASK-139
  (dairy scoring calibration, shared by yogurt+cheese), TASK-140 (cereals), TASK-141 (cheese stress test),
  TASK-142 (cheese pipeline), TASK-143 (yogurt replace). Reports to Product Owner.
---

# TASK-138 — Tri-category full-cycle assignment (umbrella)

**Owner:** CC Agent · **Reports to:** Product Owner · **Assigned:** 2026-06-01

## Product Owner decisions (locked 2026-06-01)
1. **Yogurts** — full replace via the **calibrated** engine (do dairy calibration first, re-run, then retire DEC-005). Accepts a more truthful / less flattering shelf.
2. **Sequencing** — **strict parallel**: all workstreams kick off concurrently; dependent implementation steps gate internally.
3. **Cheese** — governance stress test must reach **B before any scrape**.
4. CC registers tasks + drafts hand-off prompts.

## Readiness asymmetry (why the three differ)
- **Yogurts** — data PROVEN (run_yogurt_003 Shufersal: 90% ingredient, 0% INSUFFICIENT). Blocked only by 3 engine calibration gaps + the dairy A-ceiling ruling. "Replace current data" = retire **DEC-005**.
- **Cereals** — governance DONE (cereals_gap_resolution_v1: B, Launch-Ready-with-Conditions). Data not started. Clean greenfield.
- **Cottage/White Cheese** — NO governance stress test yet; sub-pools (cottage/cream/labaneh/white-quark) + "light" threshold undefined. Governance precedes pipeline.

## Workstream map
```
TASK-139  Dairy Scoring Calibration (nutrition+data)  ─┬─ blocks 142 (cheese pipeline)
   139A  Dairy A-ceiling ruling          (nutrition)   └─ blocks 143 (yogurt replace)
   139B  Enricher culture-vocab fix       (data)        serves yogurt + cheese
   139C  Router yogurt-anchor fix         (data)
TASK-140  Cereals full-cycle BSIP0->BSIP2 (data)        independent — ship-first candidate
TASK-141  Cheese governance stress test   (product)     blocks 142
TASK-142  Cheese full-cycle BSIP0->BSIP2  (data)         depends 139,141
TASK-143  Yogurt re-run + DEC-005 retire  (data)         depends 139
```

## Per-category exit (evaluation panel — all four must clear)
1. **QA Agent** — hard-fail-free, BSIP2->BSIP0 traceability, baseline frozen, no stale data.
2. **Nutrition Agent** — scores coherent + truthful; sub-pool/ceiling rulings applied.
3. **Content + Design** — 15–20s mobile comprehension test passes.
4. **Product Agent -> Product Owner** — strategic go-live (DEC-005 retirement for yogurts).

## Frozen invariants to guard (CNO ruling)
Milk = run_004_recalibrated (top 85/A); no snack bar reaches A (snk-001 70/B ceiling); bread = real_bread_retail_003_v1. The enricher culture-vocab change (139B) must NOT move these — QA regression (golden corpus 12/12) guards it.

## CC deliverables
- Keep this map + the dashboard in sync with `C:\Bari\tasks\` (registry authoritative; never hand-edit command_center.json).
- Surface drift / blocked work + draft hand-off prompts for owning agents.
- Per OS rule, only the Central Controller records CLOSED; sub-task owners propose RETURNED/BLOCKED.
