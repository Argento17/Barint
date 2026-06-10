---
id: TASK-139A
title: "Nutrition: dairy A-ceiling ruling (does plain live-culture dairy reach A, or is B the truthful ceiling?)"
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
depends_on: []
blocks: [TASK-142, TASK-143]
category_id: null
summary: >
  Philosophy ruling that gates both yogurt replacement and cheese scoring. run_yogurt_003 produced 0 grade-A
  on real ingredients (median 57, ceiling 78/B) — the engine reads added sugar / modified starch / stabilizers
  in 60% of SKUs as NOVA 4. Decide whether plain, additive-free, live-culture dairy (yogurt + white cheese)
  should be able to reach grade A, or whether B is the truthful category ceiling. Mirror the milk A-ceiling
  precedent (whole/4%/goat = 85/A) and the snack-bar B-ceiling precedent. Evidence-registered; Product co-signs.
---

# TASK-139A — Dairy A-ceiling ruling

## Question
Is mainstream Israeli yogurt/white-cheese's **true ceiling B** (engine's current read), or should **plain,
additive-free, live-culture** dairy reach **A**? This is a Nutrition philosophy call with published-grade
consequences — it sets whether the replaced yogurt shelf and the new cheese shelf can show an A at all.

## Inputs
- run_yogurt_003 distribution: 0 A · B17 · C46 · D24 · E1; ceiling 78/B; median 57.
- Milk precedent (frozen): whole/4%/goat dairy = 85/A — dairy CAN reach A when the matrix is clean.
- Snack-bar precedent (frozen): B is a legitimate validated category ceiling (snk-001 = 70/B).

## Deliverable
`02_products/yogurt_system/reports/dairy_a_ceiling_ruling_139A.md` — ruling + rationale + the exact
condition under which dairy reaches A (e.g. additive-free + live culture credited + no added sugar),
registered to the BSIP2 evidence registry. Flag the published-grade consequence for Product.

## State
**CLOSED — Product co-signed 2026-06-01.** Ruling `RULING-DAIRY-A-01` is now governing.
The co-sign activation precondition is **satisfied**. Two preconditions remain and are inherited by
TASK-139B (they gated *publishing grades*, not the ruling itself):
1. **Gap 2 culture-vocab coverage** must be restored before C3 can evaluate (EV-015 fix).
2. **A-threshold reconciliation (80 vs 85)** must be resolved before 139B publishes any yogurt grade.

Blocks/gates 139B/C re-score interpretation, 142, 143 — these now read the post-culture-fix
distribution against the governing C1–C6 condition.

## Delivered (2026-06-01, nutrition-agent)
Ruling `RULING-DAIRY-A-01` written to `02_products/yogurt_system/reports/dairy_a_ceiling_ruling_139A.md`.

**Ruling:** A IS reachable by plain, additive-free, live-culture dairy (yogurt + white cheese) — dairy
inherits the frozen **milk** precedent (clean dairy matrix + fermentation positive earns A), not the
snack-bar B-ceiling. **B is the truthful ceiling for the sweetened/stabilized mainstream (~60% of the
shelf), not for the category.** run_yogurt_003's "0 A" is mostly the EV-015 culture-detection bug, not
a philosophy signal — fixing it yields ~2–5 *earned* A's (not the manual shelf's 5×A-by-format).

**Exact A-condition (C1–C6):** no added sugar · no engineered additives · live culture confirmed AND
credited · intact dairy matrix (reconstituted base excluded) · correct dairy routing · verified
confidence. Earned by score; no grant, no floor, no format credit.

**Registered:** EV-021 in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.{md,json}`
(composes EV-014/015/018/019 + milk precedent; no new scoring rule).

**Product co-sign items:** (1) published-grade consequence — yogurt A-count 5→~2–5, median 72→~61–63;
(2) ⚠️ reconcile the A-threshold (`scoring.md` says 85; milk run_004 used 80) BEFORE 139B publishes grades.

**Activation preconditions (governance):** Product co-sign + Gap 2 culture-vocab coverage restoration +
A-threshold reconciliation. Only the Central Controller records CLOSED.
