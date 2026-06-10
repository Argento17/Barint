---
id: TASK-222E
title: "BSIP2 Phase 1 — fiber diversity bonus design (DESIGN_ONLY)"
owner: orchestrator
status: CLOSED
priority: LOW
created_at: 2026-06-09
closed_at: 2026-06-09
depends_on: [TASK-222]
blocks: []
roadmap_impact: false
cc_reviewed: true
work_type: design
close_reason: >
  Fiber diversity design accepted conceptually, with NOVA <=3 gate approved.
  Implementation is not yet authorized. Before scoring activation, split the
  signal into natural matrix fiber diversity versus isolated added-fiber
  diversity, and prevent isolated fibers from receiving the same benefit as
  whole-food fiber sources.
---

# TASK-222E — Fiber Diversity Bonus Design

**Status:** DESIGN_ONLY — no scoring changes implemented
**Recommendation:** PROCEED TO IMPLEMENTATION

## Design Summary

A small quality bonus for products with ≥2 distinct named fiber sources:

| Parameter | Value |
|-----------|-------|
| Signal | `distinct_fiber_source_count ≥ 2` |
| Bonus | **+2** on `nutrient_density` dimension |
| Gate | `nova_proxy ≤ 3` (NOVA 4 excluded) |
| Detection | Full ingredient text scan against 9 fiber categories |
| Marker source | Extends `bakery_semantics.py:ISOLATED_FIBER_TERMS` |

## What was rejected

- Single-source fiber bonuses (too easy to game with one isolated fiber)
- NOVA 4 eligibility (ultra-processed fiber-gaming must be excluded)
- Generic "dietary fiber" / "סיבים תזונתיים" as a marker (too ambiguous)
- Medical/physiological claims linkage (microbiome, digestion, cholesterol)

## Artifacts

- `03_operations/bsip2/proto_v0/review/task_222e_design.md` — full design specification
