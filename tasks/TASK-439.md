---
id: TASK-439
title: Re-flow cakes to current engine (scattered drift, 3x D->E): rescore -> copy reconcile -> two gates -> deploy
owner: data-agent
status: CLOSED
closed_at: 2026-07-01
close_reason: DEPLOYED to origin/master 2cbfc91f. Cakes re-flow: 62 products (same set), 3 grade movers D->E on verified complete-data red-label/ultra-processed drivers, 27 within-grade updates. TWO-GATE CONTENT SIGN-OFF COMPLETE: Content authored+RT-fixed (RT-1 false shelf-ranking removed, RT-2 softened on low-NOVA-conf 5718021); Adversarial QA CLEAR-TO-DEPLOY (0 CRITICAL/0 open HIGH). C0: G4/G5/G6/G8 + rank R0/R1 PASS; G1/G3 pre-existing (identical on live). MEDIUM carried (RT-3 dup-pair, RT-4 leakage FP, RT-5 schema debt) non-blocking.
priority: HIGH
created_at: 2026-07-01
depends_on: [TASK-436]
blocks: []
category_id: null
summary: >
  cakes 26 movers, 3 grade moves D->E, scattered -6.5..+3.1. Confirm engine-legit, rescore via spine stages, reconcile Tom-voice copy for grade/rank breaks, two-gate sign-off + C0 gates, owner deploy.
---

# TASK-439 — Re-flow cakes to current engine (scattered drift, 3x D->E): rescore -> copy reconcile -> two gates -> deploy

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## STAGED (2026-07-01, orchestrator) — rescore + copy_stage done, BLOCKED on 2 forks
Ran canonical re-baseline (rescore_all --shelf cakes, staging-only): 18 score-moves, **3 grade moves D->E** (5718021, 7290016162264, 7290119045013). gate PASS, score==trace OK 0 mismatches. copy_stage author_set = **6/65 need copy** (3 grade-changed + 3 NEW-to-live products + 4 carried-score-moved). Staging: _rescore_staging/cakes/.
**FORK 1 (composition):** the re-baseline adds **3 products not on the live page** — that's a product-composition change, not a pure re-score. Keep same product set (exclude new) or expand? = Product call.
**Then:** Content authors the 6-product author_set -> Adversarial QA gate -> C0 gates -> owner deploy (tripwire #1).


## QA GATE (2026-07-01, Adversarial QA) — CONDITIONAL PASS, DEPLOY HELD on RT-1
Gate re-ran all checks independently. **0 CRITICAL.** G5 grade-integrity PASSES 62/62 (re-run with correct --run; my earlier run omitted --run = unverified). G4 OFF / G6 / G7 / G8 PASS. G1 schema + G3 scope FAIL but byte-identical on the untouched live page = pre-existing debt, not this re-flow's regression.
**HIGH RT-1 (BLOCKING):** all 3 newly-authored rowVerdicts claim "בתחתית/מהחלשים במדף עוגות הגבינה" (bottom/weakest of the cheese-cakes shelf) — FALSE. The 3 movers rank 2nd/3rd/4th of 9 cheese cakes; 5 others score LOWER (28,25,18.5,17.5,10). At ~32 they sit near the TOP of the E band on the full page. Superlative-rank-check failure. -> content fix required.
**HIGH RT-2:** cake_5718021 copy fully assertive ("מוצר תעשייתי לכל דבר") but its trace carries LOW_NOVA_CONFIDENCE (0.3); frontend shows uniform "verified" (trace confidence_band never reaches frontend = systemic/pre-existing display gap). Soften the over-assertion on THIS product; the display gap is a separate item.
**MEDIUM (non-blocking, pre-existing):** RT-3 identical nutrition pair 7290016162264/7290119045013 (possible corpus dup), RT-4 "20.6" hebrew-leakage false positive, RT-5 G1/G3 debt.
**Status: DEPLOY HELD.** Fix RT-1 (drop false shelf-ranking, keep the real red-label/additive E-driver) + RT-2 (soften assertion on 5718021) -> re-gate -> deploy.
