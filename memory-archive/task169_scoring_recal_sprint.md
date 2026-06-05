---
name: task169_scoring_recal_sprint
description: "TASK-169 scoring recalibration sprint — CLOSED 2026-06-04, all 6 waves done. cheese/hummus/milk/yogurt LIVE; snack held; bread modeled (169F) → ship handed to the legacy re-baseline TASK-180C. See [[milk_rebaseline_run005_task180a]]"
metadata: 
  node_type: memory
  type: project
  originSessionId: d06dc8ca-7b83-4ae4-8449-075d271292ac
---

TASK-169 (owner-opened 2026-06-02): vast scoring recalibration sprint. Trigger = owner rejected
cheese/hummus/salad score compression. Diagnosis traced it to a supplement-calibrated protein
curve (10g→50, 20g→85 used in nutrient_density+protein_quality = 25% of score) + 6 other shared-engine
defects (R1–R7, full table in tasks/TASK-169.md). Owner decisions: (1) rework the SHARED math
(re-opens frozen milk/bread/snack/yogurt), (2) protein = category-relative (lean high-protein product
can reach top-of-shelf), (3) keep the live-cultures +8 bonus but GATE it to genuinely cultured foods
(exclude plain milk AND plain cottage), (4) open to frozen ceilings rising — review real numbers.

**State (2026-06-03): P1 cheese+hummus SHIPPED + owner-approved LIVE; TASK-169B CLOSED.**
- Cheese page → `cheese_frontend_v2.json` (run_cheese_004), hummus + vegetable-spreads → `hummus_frontend_v4.json`
  (run_hummus_003), both BARI_RECAL_P0=on. 47 grade promotions, 12 new A's (cottage 1% 90/A leads; 2 capped
  9% cottages 81/B via EV-021 Amendment A1 sat-fat gate). Verdicts verified grade-consistent (0 contradictions).
- **Caught late by a grade-drift audit:** the ship was committed (8af14a2) + Product-D7-co-signed 2026-06-02 but
  the registry stayed IN_PROGRESS and the JSON `_meta` still said `staged_not_live: true` → audit flagged
  "unapproved scores live." Reconciled on owner approval: flags flipped to live, 169B closed, dashboard drift→0.
  Lesson: reconcile registry + `_meta` flags at ship time, not after.
- Sat-fat now SURFACED in cheese + yogurt nutrition tables (TASK-168J, 2026-06-03): added `satFat` to BariNutritionVM
  + a 'שומן רווי' row; values verbatim from traces. Resolves the TASK-168H open governance item.
- **Production deploy still pending branch merge `cc-agent-v2 -> master` (owner action).**
- **2026-06-03 governance pass:** 169A (P0) CLOSED (model consumed by shipped P1; was registry drift). Frozen waves opened as discrete BLOCKED sub-tasks: **169C milk · 169D yogurt · 169E snack-bars · 169F bread** (bread also needs harness-wiring first). Recommended order milk→snack→yogurt→bread.
- **169C milk wave SHIPPED LIVE + CLOSED 2026-06-03.** Rescore `run_milk_005_recal_p0`: 85/A dairy ceiling HELD (0 A-crossings), lactose-free leak closed (→79.3/B), R7 gate excluded all 20 milks, flag-OFF 20/20. Only consumer-visible move = rice drink `משקה אורז` 8000215204219 **D→C** (pure recal, zero drift; R3 leanness fat_quality 50→86). Owner authorized; shipped surgically to `bari-web/src/data/milk-comparison.json` (rice row only, dairy byte-identical, 6-line diff). KEY: milk frontend score = raw trace minus ~**3.0 calibration transform** (build_milk_comparison_data.py); milk page renders curated insights (milk-product-insights.ts) that OVERRIDE the JSON consumerExplanation; dimensions/bariInterpretation panel NOT rendered on the unified page.
- **NEW QA freshness item:** HEAD reproduces only **13/20** published run_004 milk traces (engine drift since 2026-05-18, NOT a recal effect) — legacy pages on stale scores; needs a QA re-baseline task. Whole-file rebuilds are unsafe until resolved (would import drift onto frozen rows).
- **169E snack-bars wave CLOSED 2026-06-03 — confirm-and-hold, nothing shipped.** Rescore `run_snackbars_006_recal_p0` matched the P0 v1.1 prediction exactly: snk-001 70/B HELD, 0 A, 0 grade moves (14 within-grade nudges), rollback 53/53. Live `snacks_frontend_v2.json` untouched; live snack page NOT stale (flag-OFF == sprint1 production 51/53; the 2 deltas are a post-engine additive_correction layer, not drift). proto_v0 2026-05-17 traces are superseded (5/53) — noted for TASK-178.
- **TASK-178 (qa-agent, IN_PROGRESS):** legacy-page score freshness audit — HEAD reproduces only 13/20 published milk run_004 traces (engine drift since freeze). Quantify per legacy category + propose clean re-baseline before any full rebuild.
- **DEPLOYED 2026-06-03:** `cc-agent-v2 → master` fast-forwarded + pushed (origin/master @ 0b70bb7). The milk rice D→C + all 169 governance/registry is now on production master. (cheese/hummus P1 was already on master from the prior 8af14a2 ship.)
- **169D yogurt wave SHIPPED LIVE + CLOSED 2026-06-03 (deployed to master @ f075d9e).** Owner chose **cap-at-A (no S)**. Recal lifts yogurt 0A/0S → would-be 11A/3S; capped via **EV-034** (`BARI_RECAL_P0_YOGURT_TRIM`, +8 A-ceiling 89.9) → live page = **6 A / 3 B / 1 C / 1 D, 0 S** (was 0 A). Nutrition endorsed + Product D7 co-signed. Reship was SURGICAL (score/grade overwrite only — **macros preserved from run_004 because the run_003 yogurt corpus still carries the EV-029 fat-overwrite**; do NOT regen yogurt macros until EV-029 fixed in corpus). Content rewrote the inverted premise (top was 'best=B'; now top 89/A). **QA gotcha worth remembering: a capped 89.9 rounds to 90 (the S threshold) via ScoreChip Math.round → floor capped displays to 89 so they can't read as S.** Two corpus data bugs fixed: 190g-protein SKU→12.5 (OFF-sourced) + bio-naturel false +8 (marketing-prose 'דבש' bleed). Yogurt page was stale (HEAD reproduced only 23/86 published run_004) → this was a stale→fresh re-baseline.
- **TASK-169 CLOSED 2026-06-04 — all 6 waves done.** 169F bread (CLOSED 2026-06-04): the bespoke retail_003 loader WAS wired into the recal harness; real R3/R5 model = **R5 inert** (sat_fat=None 31/31), **R3 leanness only → 4 grade-affecting B→A**, none reaches S, R1/R2/R4/R6 confirmed N/A. The bread SHIP was NOT done under 169F — per owner decision it's sequenced into the legacy re-baseline **TASK-180C** so the 4 recal moves ship together with the pre-existing-drift fix (one owner sign-off), not on top of ~8 phantom drift-A's.
- **TASK-178 CLOSED 2026-06-04** (was the "QA freshness item" above): the legacy drift is real and worst on BREAD (165/256, 83 upward grade drifts), not milk. Root cause = unflagged v2 grade recal in constants.py folded in after the May freezes; git init 2026-06-01 so no git-pinned legacy engine state. Spawned **TASK-180** (re-baseline program): pin HEAD (git tag `engine-baseline-2026-06-04`) → milk→snack→bread. **Milk wave (180A) DONE & LIVE on `run_005_headpin`** (rice override preserved). Snack (180B) + bread (180C) pending. Full detail: [[milk_rebaseline_run005_task180a]].

**(superseded) P0 state:** design + blast-radius model DONE and clean —
- Design spec: `01_framework/bsip2_framework/recalibration_p0_design_v1.md` (v1.1 revision section is current).
- Model: `02_products/_recal_p0_model/TASK-169A_blast_radius_model_v1.1.md` + `*_v1.1.json`.
- All changes gated behind env flag **`BARI_RECAL_P0`** (default OFF). Flag OFF = byte-identical to engine
  0.4.1 (verified 59/59 on run_cheese_003). This is the rollback. Golden+router regressions clean OFF & ON.
- Results (flag ON): cottage 1% 75→90/A (target hit), cottage 9% 52→81/A (red-label cliff fixed),
  white+garlic inversion resolved (cottage ranks above), cheese 1→13 A / still 0 S, hummus 37 C→15 (→35 B/9 A),
  veg salads judged on veg-fit not protein. FROZEN: milk 85/A HELD, snk-001 70/B HELD; yogurt = NEW 14 A / 3 S
  (high-protein yogurts) — the live P2 owner decision.

**Open before P1 (real implementation + reship):** owner sign-off on yogurt A/S distribution; decide whether
flavored white cheese reaching A via declared-culture +8 is desired (Nutrition flag); author evidence-registry
entries EV-029–032 (+EV-024/027 extensions); **Product Agent D7 co-sign required before any P1 engine edit ships**;
bread retail_003 not yet wired into harness (bespoke loader, small R3+R5 radius) — re-model in P1 before bread sign-off.
Router note: live router emits no `milk_dairy`/`yogurt` category (all dairy → `dairy_protein`); cultured-gate
implemented via name markers + yogurt subtype — reconcile in P1. See [[cc_v3_1_upgrade]] for registry conventions.
