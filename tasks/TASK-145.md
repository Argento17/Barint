---
id: TASK-145
title: "Router: add cream-cheese/spread anchor (fixes run_cheese_001 QA-CHS-001 47.4% misroute) + regression-lock"
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "Router cream-cheese/spread anchor delivered, governed (EV-025) and regression-locked (router 15/15, frozen categories unmoved, determinism verified). It solved exactly the problem it was created for — run_cheese_001 misroute 47.4% -> run_cheese_002 1.8%, insufficient 5.3% -> 0%. Routing-only; no scoring rule. Closed (before TASK-142, per blocks: edge) on operator authorization following CC audit 2026-06-01."
depends_on: []
blocks: [TASK-142]
category_id: cheese_spreads
summary: >
  Scoped router engine change spun off from TASK-142 run_cheese_001 (QA-CHS-001). router_v2.py has a cottage
  hard anchor and Stage-2 dairy signals carry plain white cheese / labaneh, but has NO anchor for the
  cream-cheese/spread pool, so ALL 26 cream-cheese products (גבינת שמנת / ממרח גבינה / פילדלפיה / נפוליאון)
  misroute to default/whole_food_fat (47.4% total misroute, fails <5% gate; also causes 3 insufficient).
  Add specific cream-cheese hard anchors -> dairy_protein with נפוליאון cake exclusions; regression-lock
  (router corpus 12/12 + new cream-cheese entries; frozen milk/bread/snack/cereals/yogurt/maadanim unchanged).
  Governed under bari-bsip2-scoring-governance (evidence + label observability + rollback). Mirrors TASK-139C.
---

# TASK-145 — Router cream-cheese/spread anchor + regression-lock

Spun off from TASK-142 at the Product Owner's instruction (separate router task, not hand-tuned in the
data-pipeline run). Routing/identity change only — NO scoring weight/threshold/penalty change.

## Change
Add to `router_v2.py` HARD_ANCHORS (Dairy section), most-specific-first:
- `גבינת שמנת` -> dairy_protein / cream_cheese (0.93)
- `ממרח גבינה` -> dairy_protein / cheese_spread (0.92)
- `פילדלפיה` -> dairy_protein / cream_cheese (0.92)
- `נפוליאון` -> dairy_protein / cream_cheese (0.90), with ANCHOR_EXCLUSIONS = [עוגה, עוגת, פס, מאפה] (napoleon CAKE)

Bare `שמנת` deliberately NOT added (would catch sour/sweet/whipping cream — not cheese; those are
excluded at cheese curation, but the router is global). White cheese (גבינה לבנה) + labaneh already route
correctly via Stage-2 dairy signals — not touched (minimal-change / small regression surface).

## Governance (bari-bsip2-scoring-governance)
- Evidence: EV-024 (cream-cheese router misroute, run_cheese_001 QA-CHS-001).
- Label observability: reads canonical_name_he (100% Hebrew coverage on the cheese corpus).
- Scope: cheese-spreads (routing infra; collision-checked against maadanim/yogurt/milk — none).
- Rollback: git revert of the router_v2.py hunk; ROUTER_VERSION note.
- Accumulation: no existing cream-cheese anchor — not a duplicate.

## Exit / DoD
Router regression 12/12 PASS + new cream-cheese entries PASS; frozen categories unchanged; re-run cheese as
run_cheese_002 with misroute <5% and INSUFFICIENT 0% displayable. Then propose RETURNED (CC records CLOSED).

---

## Return block — proposed RETURNED (data-agent, 2026-06-01)

**Change shipped (routing/identity only — NO scoring weight/threshold/penalty/cap):** added 4 cream-cheese hard
anchors to `router_v2.py` (`גבינת שמנת`→cream_cheese, `ממרח גבינה`→cheese_spread, `פילדלפיה`→cream_cheese,
`נפוליאון`→cream_cheese) → `dairy_protein`, + a `נפוליאון` ANCHOR_EXCLUSIONS entry (`עוגה/עוגת/פס/מאפה/בצק`,
napoleon **cake**). Bare `שמנת` deliberately excluded (sour/sweet/whipping cream ≠ cheese).

**Governance (bari-bsip2-scoring-governance) — all 5 checks PASS:**
- Evidence: **EV-025** recorded in `bsip2_evidence_registry_v1.{json,md}`.
- Label observability: `canonical_name_he`, 100% coverage.
- Scope: cheese_spreads; collision-audited vs maadanim/yogurt/milk → **0 matches** (no frozen-category movement).
- Rollback: `git revert` of the HARD_ANCHORS hunk + `נפוליאון` exclusion + 3 regression entries.
- Accumulation: no prior cream-cheese anchor — not a duplicate.

**Regression-lock:** router regression **15/15 PASS** (12 frozen unchanged + 3 new: cream-cheese anchor,
cheese-spread anchor, napoleon-cake exclusion). Determinism verified (run_cheese_001 re-run on patched router
== run_cheese_002).

**Result (run_cheese_002):** misroute **47.4% → 1.8%** (PASS <5%); insufficient **5.3% → 0%** (PASS); all 26
cream-cheese SKUs now route to dairy_protein and score; 1 residual misroute (32% goat → snack_bar_granola, under
gate). A-ceiling correctly **withholds 6 macro-A white cheeses** (fail C3, no confirmed culture).

**Spillover surfaced for the CC (not actioned here):** while verifying, found that the displayed run_cheese_001
factory_run_001 artifacts describe the pre-fix diagnostic; the post-fix run is **run_cheese_002 / factory_run_002**
(QA PASS, frontend package 50/57 display-approved, NON-AUTHORITATIVE pending Nutrition sign-off). TASK-142's
misroute/insufficient DoD is now satisfied; only Nutrition/Product grade-publication sign-off remains for live.

**Proposing RETURNED.** Only the Central Controller records CLOSED.
