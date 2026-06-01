---
id: TASK-126
title: Validate Bari Strategic Objectives
owner: CommandCenter
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Accepted with minor amendments (Controller). Direction + P1-P5 structure + Wave 2 gated-4 + Launch Definition (DEC-003) ratified; amendments A (milk LEGACY at launch, committed post-launch) and B (Launch Success Indicators) incorporated. Launch-critical trio opened active (TASK-128/129/130); per ratified roadmap section 9 (WIP capacity 3), P4/P5 reserved as TASK-131/132 and open when a slot frees."
depends_on: []
blocks: [TASK-128, TASK-129, TASK-130]
category_id: null
summary: >
  Central Controller strategic review: validate/challenge the 5 proposed Bari objectives (Comparison Platform V1, BSIP0-2 Evolution, Intelligence Articles, Comparison Wave 2, Hummus Production Verdict); challenge sequencing; identify missing/overlapping objectives; recommend final priority order, success criteria, and an approved objective roadmap on the highest-value path to launch. Deliverable: bari_objective_roadmap_v1.md.
---

# TASK-126 — Validate Bari Strategic Objectives

Central Controller strategic review of the five proposed Bari objectives.
Deliverable: **`C:\Bari\bari_objective_roadmap_v1.md`** (validation + recommended roadmap).

Inputs consulted: registry `C:\Bari\tasks\`, DEC-002 (hummus GO_LIVE_APPROVED),
TASK-098 (accepted v2 direction), TASK-118 (v2 roadmap), TASK-111 (data readiness
READY_WITH_MODIFICATIONS), TASK-123 (v2 sign-off), `category_scaling_readiness_v1.md`,
and live dashboard category states.

## Recommendation (summary)
- **O1 Comparison Platform V1 → REFRAME + KEEP (P1):** re-label to *v2 completion of the
  existing fleet* — V1 is frozen; v2 is the accepted direction (TASK-098). Surfaces the
  `comparison_ui_reference_v2.md` sign-off + QA re-baseline as explicit prerequisite gates;
  absorbs the live v2-pilot exit verdict on hummus.
- **O2 BSIP0–BSIP2 Evolution → SPLIT:** keep the launch-gating *calibration + confidence*
  slice (P2, freeze scores per category); **defer** BSIP2 next-gen + future-category readiness
  to post-launch (it has its own roadmaps).
- **O3 Intelligence Articles → KEEP, RESEQUENCE (P4):** downstream of P1+P2; pilot 1 article
  off a score-frozen category, then scale to 3.
- **O4 Comparison Wave 2 → DEFER + REDUCE (P5):** gated behind P1 (v2 ref) and the new P3
  hardening per `category_scaling_readiness_v1` (system NOT ready for Category #5); cut 4 → 2
  (cereals + tahini, already QUEUED/staged, born on v2).
- **O5 Hummus Production Verdict → REMOVE:** redundant — DEC-002 already GO_LIVE_APPROVED + LIVE;
  fold the only live part (v2-pilot exit gate) into P1.
- **MISSING → ADD P3 Operating-Model Hardening:** automated corpus validation, category-module
  contract, route/status governance, deprecation policy. Justified: already specified by
  `category_scaling_readiness_v1` (naming required work, not inventing scope).

Recommended order: **PREREQ (v2 ref + QA re-baseline + hummus confidence re-audit) → P1 v2
completion → P2 calibration/freeze → P3 hardening (parallel) → P4 articles → P5 Wave 2 →
deferred BSIP2 next-gen.** Full success criteria, risks, and the one-screen sequence are in
the deliverable.

## Registry note (surfaced, not silently resolved)
This work was invoked as "TASK-124", but `TASK-124` is already registered and CLOSED
("Add one-click task action buttons to Command Center", frontend-agent). Per
`registry_first_rule_v1`, ids are never reused; the registry wins on conflict. Re-registered
here at the next free id **TASK-126** (TASK-125 also taken).

## Feedback round 1 (Controller, 2026-06-01)
Direction approved; O5 removal + P1/P2/P3 structure ratified. Return items addressed:
1. **Wave 2 challenge — accepted.** Flat 4→2 withdrawn; target stays **4** as an instrumented,
   gated cohort (1→2→gate G-W2A→3→4; "repeatability proven" at Cat 3). Honest cause: the
   original cut was sequencing/capacity-driven, mis-expressed as scope. Full answer in
   `bari_objective_roadmap_v1.md` §8.
2. **Launch Definition v1** proposed → `C:\Bari\launch_definition_v1.md` (recommend ratify as DEC-003).
3. **Registry structure for P1–P5** → `bari_objective_roadmap_v1.md` §9 (objective tasks + lettered
   sub-tasks, dependency edges, capacity-3 staggering).
Infra fix (item 5) implemented under **TASK-127** (interpreter pinned to `C:\Bari\.venv`).

## Disposition: CLOSED — Accepted with minor amendments (Controller, 2026-06-01)
Roadmap direction, P1–P5 structure, Wave 2 gated-4, and Launch Definition v1 (→ **DEC-003**, DECIDED)
ratified. Two amendments incorporated: **A** milk launches LEGACY-labelled with a committed
post-launch gen0→gen1→v2 migration (not optional; P1 §128E); **B** Launch Success Indicators
(market-facing readiness) added to `launch_definition_v1.md` §6.5.

Execution on ratification:
- DEC-003 recorded in `decisions/decisions.json`.
- Launch-critical trio opened **IN_PROGRESS** (= task_capacity 3): **TASK-128** (P1, CRITICAL),
  **TASK-129** (P2, HIGH), **TASK-130** (P3, HIGH).
- **P4/P5 reserved as TASK-131/TASK-132**, not yet opened — per ratified roadmap §9 they open as the
  trio retires (P4 when 128+129 deliver; P5 when 128+130 deliver), so the WIP limit of 3 holds and the
  board stays GREEN. (Opening them now would count as active and breach capacity.)
