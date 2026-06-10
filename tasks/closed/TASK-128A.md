---
id: TASK-128A
title: Author comparison_ui_reference_v2
owner: frontend-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Task resolved"
depends_on: [TASK-098, TASK-111, TASK-118, TASK-123]
blocks: []
category_id: null
summary: >
  Author the binding comparison_ui_reference_v2.md engineering reference (Phase-1 prerequisite gate for TASK-128). Converts the accepted v2 direction (TASK-098 spec) + roadmap (TASK-118) + sign-off (TASK-123, READY_WITH_MODIFICATIONS) into the authoritative implementation reference: row layout, metric block, confidence display, disclosure handling, expansion/responsive behavior, and explicit Phase 1 vs deferred scope.
---

# TASK-128A — Author comparison_ui_reference_v2

Sub-task of **TASK-128** (Comparison Platform v2 Completion). Satisfies the
prerequisite gate named in TASK-128: *"author+sign comparison_ui_reference_v2.md"*
(roadmap Blocker #2 / sign-off condition 3).

## Objective
Convert the accepted v2 direction into the single binding implementation reference
for TASK-128.

## Inputs consulted
- `handoff/comparison-v2-spec.md` — accepted v2 direction (**TASK-098**); changes #1–#9, data contract, layout rules.
- `handoff/comparison-v2-implementation-roadmap.md` — **TASK-118** (CLOSED); four-phase plan, VM deps, migration order, hummus pilot.
- `handoff/comparison-v2-signoff-package.md` — **TASK-123** (CLOSED); READY_WITH_MODIFICATIONS.
- **TASK-111** (CLOSED) — data readiness READY_WITH_MODIFICATIONS.
- `docs/comparison_ui_reference_v1.md` (frozen) and `src/lib/comparisons/comparison-product.ts` (current VM), to ground the data contract and file structure.

## Deliverable (artifact, website repo)
**`bari-web/docs/comparison_ui_reference_v2.md`** — binding engineering reference.
Defines (each FROZEN or explicitly phased): row layout + density model, metric block
(protein + additives at launch; `base_pct` deferred to Phase 3), confidence display
(promoted + accuracy gate + `full→verified` enum rename), disclosure handling,
expansion behavior, mobile behavior, desktop behavior (dense table + Phase-2 rail/
dividers/histogram), accessibility/RTL, migration + hummus pilot, open conditions,
QA acceptance assertions, and an explicit **Phase 1 vs Phase 0 / Phase 2 / deferred /
rejected** scope split.

## Status / sign-off
- Authoring half: **DONE** (frontend-agent, 2026-06-01).
- Sign half (design/product countersign + Controller acceptance) and open conditions
  (TASK-106 confirmation, hummus re-audit, QA re-baseline) remain before Phase-1 code.

## Registry note (surfaced, not silently resolved)
The `[registry-guard]` hook flagged **TASK-098** as referenced-but-unregistered.
TASK-098 is the *accepted v2 direction* already consumed by CLOSED tasks 118/123/126
and the live spec; it is a passing reference here, not work being opened, so it is
not re-registered (re-registering it under a new id would violate the Registry First
Rule — ids are never reused).
