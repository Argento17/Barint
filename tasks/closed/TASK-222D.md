---
id: TASK-222D
title: "BSIP2 Phase 1 — matrix-integrity proxy design (DESIGN_ONLY)"
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
  Matrix-integrity v1 design accepted as conservative and label-observable. Approved
  design is limited to one binary signal: intact whole grain at ingredient[0], grain
  categories only, +3 max bonus on whole_food_integrity. Unobservable mechanisms
  rejected. No implementation authorized yet; defer scoring activation until category
  impact justifies it.
---

# TASK-222D — Matrix-Integrity Proxy Design

**Status:** DESIGN_ONLY — no scoring changes implemented
**Recommendation:** PROCEED TO IMPLEMENTATION (or defer to Phase 2)

## Design Summary

A narrow v1 matrix-integrity proxy consisting of exactly one binary observable signal:

| Parameter | Value |
|-----------|-------|
| Signal | `intact_whole_grain_detected` — ingredient[0] is a whole-grain form |
| Bonus | **+3** on `whole_food_integrity` dimension |
| Max | +3 (hard cap) |
| Categories | `bread`, `cereal`, `crispbread`, `cracker`, `snack_bar_granola` |
| Detection | Hebrew substring match against whole-grain markers (oat, whole wheat, spelt, rye, quinoa, etc.) |

## What was rejected

- Particle size, viscosity, chewing rate, gastric emptying (unobservable from labels)
- HP reconstruction triad, assembly drag, fortification classification (already captured by other dimensions; speculative)

## Artifacts

- `03_operations/bsip2/proto_v0/review/task_222d_design.md` — full design specification
