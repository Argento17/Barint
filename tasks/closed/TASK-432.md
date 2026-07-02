---
id: TASK-432
title: Juices/fiber classifier: does stabilizer pectin/gum (E412/E414) wrongly earn a functional-fiber bonus in zero-fiber juices? (from TASK-430)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Juices/fiber classifier: does stabilizer pectin/gum (E412/E414) wrongly earn a functional-fiber bonus in zero-fiber juices? (from TASK-430)
---

# TASK-432 — Juices/fiber classifier: does stabilizer pectin/gum (E412/E414) wrongly earn a functional-fiber bonus in zero-fiber juices? (from TASK-430)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Update 2026-07-01 (orchestrator) — RULED (P278, Nutrition) + orchestrator-VERIFIED → BLOCKED on activation path
**Ruling: YES, false positive** — trace E412/E414/E440 in zero-declared-fiber products (dietary_fiber_g=None)
should not earn the EV-006 functional-fiber bonus (evidence tier Moderate; exact threshold is a regulatory
proxy — Research Agent lit-work for full D6 rigor). Verified: 7290019056737 = zero declared fiber + gum/pectin
present = the exact trigger.
**Mechanism CORRECTED (resolves the P276/orchestrator caveat):** the fiber bonus RAISES the score (+0.36); the
net DOWNWARD juice drift (36.0→32.3, D→E) is a SEPARATE already-live mechanism — `_emulsifier_complexity()`
(ECS-v1/EV-045) −4 penalty for "3+ distinct low-risk stabilizers" (both from commit 117e7021, 2026-06-10,
post the 2026-06-07 juice baseline). `BARI_FIBER_FERMENT_V1` is NOT the cause (toggled → zero effect). Task's
example 7290019056720 doesn't actually drift (no gum); the real drifters are 4 other barcodes.
**Fix built + gated + VERIFIED byte-identical-off:** `BARI_FIBER_TRACE_GATE_V1` (default off; HC harness 31/31;
0/28 juice mismatches) on branch `p278/juices-fiber-ruling` (commit 78d61c18, NOT on master). Self-caught a QA
false-positive (whole-text scan suppressed genuine fiber-fortified products) → fixed to term-local proximity.
**All-category shadow:** activation moves 15 products across 5 cats (cakes/cookies ×8, hummus ×3, milk ×2,
chocolate ×1, cookies_coffee ×1). Two hummus near the C/D=50 boundary = UNRECONCILED (needs canonical re-flow).
**BLOCKED on the activation path (tripwire):** (1) Product D7 co-sign on the gate mechanism; (2) resolve the
hummus C/D discrepancy via canonical re-flow; (3) owner sign-off on the multi-category movement. NOTE: this
fix alone does NOT restore juices to published — the juice drop is mostly EV-045 (a separate scoring question:
is a −4 penalty for 3+ trace stabilizers correct?). Recommend: activate juices first (cleanest), then decide
the other 4 + the EV-045 question separately.

## Update 2026-07-01 (orchestrator) — CO-SIGNED + hummus-reconciled + LANDED → CLOSED
Owner "go ahead" → drove the fiber-gate to publish-ready and landed it:
- **Product D7 CO-SIGN** (P280 cosign): sound rule (closes internal inconsistency vs EV-003/019; asymmetric
  downside; sub-noise; reversible default-off); Product verified the code scope itself. Condition: hummus held
  until reconciled → now reconciled.
- **Hummus reconciliation** (P280, verified): real canonical re-flow — **0 grade moves** across 57 published
  hummus; the 2 boundary products stay C (51.3→50.9, 51.4→51.0); only 3/69 carry trace-fiber, all −0.4;
  66/69 byte-identical off↔on. (Surfaced a pre-existing NOVA-band drifter 7290106577480 +4.8, unrelated to
  TASK-432, = the known TASK-429 hummus 56/57 residual — flagged for Nutrition, not fixed here.)
- **LANDED on master + origin (a5c6feeb..78d61c18):** `BARI_FIBER_TRACE_GATE_V1` in the canonical engine,
  DEFAULT-OFF (byte-identical verified on merged engine: HC harness 31/31 drift 0). Zero live-score impact.
**Activation reality (honest):** turning it ON to change LIVE scores = re-flowing each affected category to the
current engine, which ALSO pulls in that category's OTHER accumulated drift (hummus +4.8 NOVA-band; juices the
EV-045 −4). So it is NOT a standalone flag-flip — it folds into the per-category refresh program (same class as
the TASK-418 refresh that already did HC/cheese/cereals). The corrected engine is now canonical; each category
inherits the fix on its next refresh, owner-gated per category. CLOSED (rule + fix + co-sign + landing done).
**SEPARATE follow-up (NOT this task):** the EV-045 emulsifier −4 penalty for 3+ trace stabilizers is the real
driver of the juice D→E drop — its own Nutrition scoring question if/when juices is refreshed.
