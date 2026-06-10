---
id: TASK-169E
title: P2/P3 frozen wave — snack bars recal confirm (snk-001 70/B hold)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
cc_reviewed: 2026-06-03
depends_on: []
blocks: []
category_id: null
close_reason: "Snack-bars frozen wave: CONFIRM-AND-HOLD, nothing shipped. Rescore run_snackbars_006_recal_p0 (BARI_RECAL_P0=on, config 4e286ef740765a33, corpus n=53) independently verified against run_record + on/off artifacts: frozen invariant HELD — snk-001 (bsip1_7290011498870) = 70/B both OFF and ON; 0 products >=80, 0 grade A (no bar reaches A). recal_grade_moves = 0 (independently recomputed OFF->ON = 0); 14 sub-grade score nudges only (R3/R5, max +3.4 within-grade). Rollback flag-OFF 53/53 byte-identical; golden 0 FAIL/1 WARN (flag-insensitive), router all PASS, OFF+ON. Matches P0 v1.1 prediction exactly (14 score / 0 grade / snk-001 70B / 0 A). No reship, no second owner sign-off needed (nothing to ship); live snacks_frontend_v2.json untouched. Drift lens (TASK-178): flag-OFF == live sprint1 production baseline 51/53 (the 2 deltas are sprint1's post-engine additive_correction -1 layer, NOT engine drift, both stay D) -> live snack page is NOT stale. The superseded proto_v0 2026-05-17 traces reproduce only 5/53 but predate the live RC-01/sprint1 baseline (snk-001 was 65/C there) -> stale, do not cite as baseline (noted for TASK-178)."
summary: >
  Frozen wave under TASK-169 — expected fast. P0 v1.1 showed 0 changes on snack bars (snk-001 = 70/B HELD, B-ceiling intact). Deliverable: rescore snack bars with BARI_RECAL_P0=on into a new run id, confirm 0 grade moves vs live, owner confirm-and-hold sign-off, no reship expected. If any move appears, escalate before shipping. Flag OFF = byte-identical rollback.
---

# TASK-169E — P2/P3 frozen wave — snack bars recal confirm (snk-001 70/B hold)

## Owner authorized start (2026-06-03)
Owner released the snack-bars wave (2nd in the recommended order, after milk 169C closed). Unblocked → IN_PROGRESS. P0 v1.1 predicted **0 changes** on snack bars (snk-001 70/B HELD). This authorizes the rescore + confirm; if any grade moves, escalate before shipping.

## Scope / deliverable (Data Agent)
Rescore the frozen snack-bars corpus with `BARI_RECAL_P0=on` into a NEW run id (published dirs + live JSON untouched). Produce:
1. **Before/after diff** of every snack bar (live → recal), flag any grade move.
2. **Frozen-invariant check:** confirm **snk-001 = 70/B HELD** and that **no bar reaches A** (category ceiling).
3. **Rollback:** flag-OFF rescore == published baseline (byte-identical) — report N/N.
4. **Regression:** golden + router clean OFF and ON.
5. **Recommendation:** "0 moves → confirm-and-hold, no reship" (expected) vs "N moves → list for owner sign-off."

Governance per `bari-bsip2-scoring-governance`. No live score ships without a second owner sign-off. Watch for the same HEAD-vs-published drift TASK-169C found (TASK-178) — separate recal effect from drift before recommending any ship.

## CLOSED (CC, 2026-06-03) — confirm-and-hold, nothing shipped
Rescore `run_snackbars_006_recal_p0` returned exactly the P0 v1.1 prediction and was independently verified against the artifacts: **snk-001 70/B HELD, 0 A, 0 grade moves, rollback 53/53**. Recal only produces 14 within-grade sub-point nudges. No reship, live JSON untouched. Drift lens: live snack page is NOT stale (flag-OFF == sprint1 production, the 2 deltas are a post-engine correction layer, not drift). The proto_v0 2026-05-17 traces are superseded/stale — noted for **TASK-178**.

**Frozen waves remaining under parent 169:** 169D yogurt (the real owner decision — 14A/3S top-trim), 169F bread (needs harness-wiring first). Next per recommended order = **yogurt (169D)**.
