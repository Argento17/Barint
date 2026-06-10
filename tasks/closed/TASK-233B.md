---
id: TASK-233B
title: "Shared frontend-packaging core — single grade/confidence/strip/emit (root cause #1 + confidence inflation)"
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-233]
blocks: []
roadmap_impact: true
work_type: pipeline-refactor
---

# TASK-233B — Shared packaging core

From the TASK-233 sweep, root cause #1: 10+ category generators hand-roll the same logic. Build
one shared module all generators import, owning the parts that keep drifting.

## Scope
- **One grade function** that derives the 5-grade from score, matching `corpus.ts`
  `frontendGradeFromScore` exactly, so on-disk grade == runtime grade (kills DA-009 drift, DA-002).
- **One confidence deriver** = `confidence_annotation.derive_from_trace`; **medium ≠ verified**
  (fixes DA-005). Delete inline `build_confidence`/`confidence_badge`/`confidence_label` funcs
  (DA-007). Fallback must NOT preserve `verified` without trace evidence (DA-013).
- **One canonical confidence tooltip set.** Frozen veg ships a non-canonical, stronger-claim
  variant — *"כל נתוני התזונה והרכיבים היו זמינים ממקור המזון הרשמי"* (53×, only category using it)
  — vs the canonical *"הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים"* used by every other
  category. Collapse to the canonical set.
- **Accuracy flag (route to Nutrition + Content):** the "official food source" (ממקור המזון הרשמי)
  wording overclaims — provenance is a Shufersal **retailer scrape** (per the file's own
  `_meta.provenance`), not an official source. Confirm correct wording before adopting.
- **One field-strip** (all `_`-prefixed + trace + non-VM keys) so internal fields never ship.
- **One VM emitter**; per-category scripts become thin config (selectors + cluster rules).
- Field-name alignment: generators must write `_aCappedToB` (not `_a_gate_capped`, DA-011).

## DoD
- [ ] Shared core module exists; ≥3 category generators migrated to it as proof
- [ ] frozen_vegetables re-derived: confidence honest (medium→partial), canonical tooltip, no contradiction with `unknowns`
- [ ] disk grade == runtime grade for all migrated categories (verified against the 233A gate)
- [ ] Nutrition co-sign on the confidence + tooltip wording; no published score values changed
