---
id: TASK-169F
title: P2/P3 frozen wave — bread retail_003 harness-wiring + R3/R5 re-model + sign-off
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
completed_at: 2026-06-04
cc_reviewed: 2026-06-04
blocker: null
depends_on: []
blocks: [TASK-180C]
category_id: null
close_reason: >
  CC close-readiness gate PASS (2026-06-04, claims verified against artifacts:
  result JSON confirms exactly 4 grade-affecting B->A moves matching the owner memo,
  R5 inert, OFF/stored 6/24 drift-separated, golden 11P/1W/0F + router 13/13, bread
  frontend JSON git-confirmed untouched). The MODEL deliverable is complete and accepted.
  Owner reviewed the 4 frozen B->A moves on 2026-06-04 and chose the re-baseline path:
  the SHIP (P3) is NOT done here — it is sequenced into the bread re-baseline wave
  (TASK-180C) so the 4 recal-intended moves ship together with the pre-existing-drift
  resolution and a single owner per-move sign-off, rather than silently absorbing ~8
  drift-A's. 169F's modeling obligation is fully discharged; its ship-obligation transfers
  to TASK-180C. Report: 03_operations/reports/recal/TASK-169F_bread_recal_remodel_2026-06-04.md.
return_reason: >
  MODEL delivered (NOT LIVE). retail_003 wired into the BARI_RECAL_P0 harness by reusing
  batch_run_bread_retail_003 as a module (OFF/ON toggle, full synthesis+ceiling pipeline).
  OFF safety contract PASS (flag inertness; every R3/R5 branch is `if RECAL_P0_ON`). Real
  R3/R5 before/after over all 31 curated: R5 INERT (sat_fat=None for 31/31 -> 0 sat-fat red
  labels); R3 lifts fat_quality 50->80-92 but the moderate-band 82 ceiling bounds it -- net
  4 grade-affecting B->A, 10 cosmetic <2pt, 17 no-move, none reaches S. R1/R2/R4/R6 confirmed
  not materially applicable (R4 0/31 NOVA moves, R2 bread excluded from fiber-N/A, R6
  sauce_spread-only). Golden 11P/1W/0F flag-insensitive; router 13/13 PASS OFF+ON. DRIFT
  SEPARATED: OFF reproduces only 6/24 published scores -- the 18/24 gap is pre-existing HEAD
  drift (TASK-178), cancels in the OFF->ON delta, reported as head_drift not recal. Owner
  sign-off memo lists exactly 4 frozen B->A moves needing per-move P2 approval; recommends
  sequencing any bread reship AFTER TASK-178 sets the engine baseline (HEAD already shows
  11 A vs published 3 A from drift alone). Latent moderate-band grade-ceiling inconsistency
  (score_ceiling=82 but grade_ceiling=B) flagged for Nutrition/QA, pre-existing not recal.
  Report: 03_operations/reports/recal/TASK-169F_bread_recal_remodel_2026-06-04.md. Artifacts:
  02_products/bread_retail_003/_model_task169f/. EV-031/EV-032 bread-confirmation entry added
  to the evidence registry. NO live bread score/grade/frontend JSON touched (P3 gated on
  owner P2 sign-off). Proposing RETURNED for CC close-readiness gate + owner P2 decision.
summary: >
  Frozen wave under TASK-169 — only one with prerequisite engineering. bread retail_003 uses a bespoke loader, NOT wired into the recal harness, so its blast radius (R3 leanness + R5 sat-fat cap->penalty only) was estimated, not modeled. Deliverable: (1) wire retail_003 into the BARI_RECAL_P0 harness, (2) real R3/R5 before/after diff + golden/router regression, (3) owner per-move sign-off (provenance real_bread_retail_003_v1 is a frozen invariant), (4) rescore + reship bread frontend JSON only if approved. Sequence last.
---

# TASK-169F — P2/P3 frozen wave — bread retail_003 harness-wiring + R3/R5 re-model + sign-off

## Release (owner, 2026-06-04)
Owner released the bread wave ("launch both"). BLOCKED → IN_PROGRESS. The prerequisite
engineering (harness-wiring) is now the active first step. **No frozen bread score ships
without explicit owner per-move sign-off (P2)** — provenance `real_bread_retail_003_v1`
is a frozen invariant. This wave produces the model + recommendation; the owner gate is
the last step before any rescore/reship (P3).

## Scope (the only recal change vectors that touch bread)
- **R3 — leanness reward** (`fat_quality` now credits genuinely lean products instead of a
  neutral 50 floor).
- **R5 — sat-fat red-label cap → graded penalty** (the cliff becomes a slope).
- R1/R2/R4/R6 do not materially apply to the bread corpus (no dairy protein curve, no
  fiber-free-dairy blend, NOVA/veg-spread rules out of scope) — confirm, don't assume.

## Deliverable
1. Wire `real_bread_retail_003_v1` (bespoke loader) into the `BARI_RECAL_P0` harness so its
   blast radius is **modeled, not estimated**. OFF = byte-identical (verify).
2. Real R3/R5 **before/after diff** over the 31 curated bread products — per-product, with
   each delta classified **grade-affecting vs <2pt cosmetic**.
3. Golden-corpus + router regression delta — must stay green except the intended R3/R5 diffs.
4. A short **owner sign-off memo**: the exact list of frozen bread moves that need approval,
   each with old→new grade + the one-line reason.
5. Do **NOT** rescore/reship the bread frontend JSON yet — that is P3, gated on owner approval.

## Cross-link
TASK-178 (qa-agent) is auditing HEAD-vs-published drift for legacy pages incl. bread. Consume
its bread-drift slice so the R3/R5 re-model separates **recal-intended** moves from
**pre-existing engine drift** — do not attribute drift deltas to the recal.

## Return
Propose **RETURNED** with the before/after table + regression result + the owner sign-off memo,
for the CC close-readiness gate, then the owner P2 decision.
