---
id: TASK-169
title: Scoring recalibration sprint — category-relative whole-food rubric (protein curve, fiber-blend, leanness, NOVA proxy, red-label cliff, category-fit)
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-02
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
summary: >
  Owner-opened vast scoring sprint. Diagnosis (2026-06-02) traced cheese/hummus/salad score compression to 7 shared-engine root causes: supplement-calibrated protein curve, 35% fiber-blend on fiber-free dairy (EV-027 gated off for cheese), fat_quality that never rewards leanness, NOVA proxy over-classifying cultured/fortified dairy + jarred spreads as processed (+false consumer label), red-label sat-fat cap acting as a cliff, one universal rubric applied to category-inappropriate veg spreads, and a white-cheese ranking inversion. Owner directive: rework the SHARED math (re-opens frozen milk/bread/snack) + make protein category-relative so a lean high-protein product (cottage 1%) can reach top-of-shelf. Governed: evidence-registry ref + rollback + frozen-category blast-radius + owner sign-off per change.
---

# TASK-169 — Scoring recalibration sprint — category-relative whole-food rubric (protein curve, fiber-blend, leanness, NOVA proxy, red-label cliff, category-fit)

## Trigger & owner directive (2026-06-02)

Owner reviewed the live cheese / hummus / savory-spread shelves and rejected the score
spread: hummus compressed in the 60s; cottage 1% (best protein-to-calorie on the shelf)
only 75/B and ranked *below* a garlic white cheese; a 16% napoleon spread scoring near a
lean cottage; cottage 9% collapsed to the level of a 25g-fat cream cheese; veg "salads"
bottoming out. Owner decisions:
- **Scope = rework the SHARED scoring math** (not cheese-only). This re-opens the frozen
  invariants (milk run_004, bread retail_003, snack bars snk-001) — each frozen move needs
  owner re-approval before it ships.
- **Protein = category-relative**: a lean, high-protein product must be able to reach
  top-of-shelf within its category (cottage 1% target ≈ 90/A), rather than being held down
  by an absolute curve calibrated for 20–25g supplement protein.

## Diagnosis (engine-traced, run_cheese_003 / run_hummus_002 / run_maadanim_001)

The compression is **one mis-calibrated whole-food rubric** surfacing as 7 defects. All
line/curve references are `03_operations/bsip2/proto_v0/src/score_engine.py` + `constants.py`.

| # | Root cause | Evidence (live) | Shelves |
|---|---|---|---|
| **R1** | Protein curve calibrated for supplements: `(10g→50, 15g→70, 20g→85, 25g→95)` used in BOTH nutrient_density (15%) + protein_quality (10%) = 25% of score. Whole-food ceilings (dairy 11.5g, hummus 8g) can't reach the top and barely differentiate (9g→45 vs 11.5g→56). | cottage 1% pq=56; white 9g pq=45; hummus 5–8g pq=28–42 | all |
| **R2** | `nutrient_density` blends 35% fiber even for structurally fiber-free dairy → cottage 11.5g protein (56) × 0.65 + 0×0.35 = **36.4**. EV-027 fix exists but is gated OFF for cheese (`TASK144_FIXES_ON`, maadanim-only). | cottage1% nutrient=36.4 | cheese, dairy |
| **R3** | `fat_quality` punishes fat but never rewards leanness; <0.5g fat or missing sat-fat → neutral 50. Lean products get no credit. | cottage1% fat_quality neutral path | all |
| **R4** | NOVA proxy over-classifies cultured/fortified dairy + jarred spreads as NOVA 3 "processed" → processing_quality 65, wfi 60, cap 87 + false consumer line "מבנה רכיבים מעובד — תוספות מעבר לבסיס החלבי" (L8 fallback, build_cheese_signals.py:166). Cottage was NOVA 2 in run_001 → regression. | cottage1% nova=3; hummus NOVA dist 3:59 / 1:6 / 2:4 | cheese, hummus |
| **R5** | Red-label sat-fat **cap** (`ISRAELI_RED_LABEL_1_SAT_FAT`→55) is a cliff: a 1.6g satfat difference flips a 16-pt swing; once it fires it flattens protein quality (10.5g cottage 9% == 4.3g/25g-fat napoleon == 52). | cottage 9% 52/C vs napoleon 16% 68/B | cheese |
| **R6** | One universal rubric on category-inappropriate foods: veg spreads (matbucha/pepper/eggplant, 1–2g protein) judged on a 31%-protein-weighted rubric → structural floor 42–62. | matbucha 48.7/D, pepper-spread 42.8/D | salads/spreads |
| **R7** | Ranking inversion: garlic white cheese final 76.9 > sum-of-its-dimensions (≈68.9), while cottage final matches its dims exactly (74.9). A ~8-pt term lifts the nutritionally-inferior product to #1. Needs run-down. | white+garlic vs cottage1% | cheese |

## Phased plan (each phase gates on the prior; governance per bari-bsip2-scoring-governance)

- **P0 — Recalibration design + blast-radius model** (nutrition + data, NO live change).
  Propose the category-relative protein scale, R2/R3 fixes, R4 NOVA refinement, R5 cap→penalty,
  R6 category-fit rule. Model before/after for cheese/hummus/salads AND the frozen corpora
  (milk run_004, bread retail_003, snack bars, yogurt). Output: design doc + diff table +
  golden-corpus regression delta. **Owner approves before any engine edit.** ← current next step.
- **P1 — Engine changes behind a flag** (data). Implement P0-approved changes gated by an env
  flag (rollback = unset). Golden + router regression must stay green except intended diffs.
- **P2 — Frozen-category re-approval** (product + owner). Present milk/bread/snack/yogurt deltas;
  owner signs off (or vetoes) each frozen move. Update frozen-invariant rulings as needed.
- **P3 — Rescore + reship** (data + frontend). Rescore all affected categories; rebuild frontend
  JSON; QA stale-data + insight-line truthfulness; fix the false "processed" labels (R4) and any
  insight lines invalidated by new scores.
- **P4 — Close-readiness gate** (CC). Verify each claim against artifacts before CLOSED.

## Governance scaffolding (must be satisfied before P1 merges)
- **Evidence registry:** each of R1–R6 needs an EV-### entry (signal + source + date) before its
  rule changes. R1 (category-relative protein) + R3 (leanness) are new evidence; R2 (EV-027) +
  R4 (EV-024/026) extend existing entries.
- **Label observability:** R5 reads sat-fat red label, R4 reads NOVA proxy — confirm coverage.
- **Activation scope:** owner approved CROSS-CATEGORY. Frozen categories still need per-move sign-off (P2).
- **Rollback:** env-flag gating (precedent: BARI_TASK144_FIXES). Document previous state per change.
- **Rule-accumulation:** R2/R3 modify existing dimension fns; do NOT add shadow rules.

## Sub-tasks
- TASK-169A — P0 recalibration design + blast-radius model (nutrition + data) — **CLOSED 2026-06-03** (model consumed by shipped P1).
- TASK-169B — P1 engine behind flag + rescore/reship CHEESE + HUMMUS (data) — **CLOSED 2026-06-03** (live, owner-approved).
- TASK-169C — P2/P3 frozen wave: milk run_004 re-approval + rescore (data) — **BLOCKED** on owner per-move sign-off. Expected confirm-and-hold (v1.1 leak closed).
- TASK-169D — P2/P3 frozen wave: yogurt R1-anchor top-trim decision + rescore (data) — **BLOCKED** on owner decision (14A/3S distribution). Highest-judgment wave.
- TASK-169E — P2/P3 frozen wave: snack bars confirm (snk-001 70/B hold) (data) — **BLOCKED** on owner per-move sign-off. Expected 0 moves.
- TASK-169F — P2/P3 frozen wave: bread retail_003 harness-wiring + R3/R5 re-model + sign-off (data) — **BLOCKED** on prerequisite harness-wiring, then owner gate. Sequence last.
- Recommended execution order: **milk → snack-bars → yogurt → bread** (rising risk; bread's harness prereq last). P4 = CC close-readiness gate on each wave, then close parent.

## Out of scope / guardrails
- No live score ships until P0 design is owner-approved.
- "best ≠ excellent" framing stays; only the numbers move (per frozen-invariant doctrine).
- Do not invent product/nutrition data; all recalibration validated against existing traces.

## Status note (CC, 2026-06-03) — P1 wave owner-approved live; parent stays open
- **TASK-169B (P1 — cheese + hummus) CLOSED 2026-06-03.** Owner gave the final human sign-off
  that was its last gate; recal grades are approved live on the cheese, hummus and
  vegetable-spreads pages (47 grade promotions incl. 12 new A's; cottage 1% 90/A leads). Live
  files verified against the recal engine runs + verdicts grade-consistent (see 169B close_reason).
- **Why this surfaced late:** the P1 ship was committed (8af14a2) and Product-co-signed on
  2026-06-02 but never reconciled — registry stayed IN_PROGRESS and the JSON `_meta` still said
  `staged_not_live: true`, so a grade-drift audit (2026-06-03) flagged unapproved scores live.
  Reconciled on owner approval; flags flipped to `live`.
- **Parent remains IN_PROGRESS.** Open: the frozen-category waves (P2/P3) — milk run_004,
  yogurt top-trim via R1 anchor, snack bars — each still needs its own owner per-move sign-off
  before rescore/reship. Not started.
- Production deploy of the shipped P1 wave still needs branch merge `cc-agent-v2 -> master` (owner).

## Status note (CC, 2026-06-03) — P0 closed, frozen waves opened (all blocked on owner)
- **TASK-169A (P0) CLOSED.** Its design + v1.1 blast-radius model were owner-validated by the shipped P1; closing it resolved registry drift (output already built on while the row read IN_PROGRESS).
- **Frozen waves opened as discrete sub-tasks** (169C milk · 169D yogurt · 169E snack-bars · 169F bread), each **BLOCKED** so they don't read as fake active WIP — they cannot begin until the owner gives the per-move sign-off the frozen-invariant doctrine requires (bread also needs harness-wiring first). The deferred items 169A had been carrying (yogurt distribution, bread harness/re-model, aged-cheese router reconciliation) moved onto these waves, not back onto 169A.
- **Next owner action:** decide the first frozen wave to release. Recommended start = **milk (169C)** — lowest risk, v1.1 model showed the leak already closed, likely confirm-and-hold.
