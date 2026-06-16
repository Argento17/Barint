# Handoff — TASK-278 (parallel orchestrator session standing down)
**Date:** 2026-06-14 · **From:** the orchestrator session that ran P96–P105 · **Reason:** owner confirmed a SECOND orchestrator track is intentionally running TASK-278; this session stands down to avoid board/registry collision. The OTHER track is authoritative.

## ⚠️ CRITICAL CORRECTION for the cereals × sugar enrollment (EV-087)
The other track's **EV-087** calibrated cereals on **all-45** products (corpus_stats median 14.0, IQR 11.0, robust_scale 8.896) and states router=`cereal` for all 45.

**That is contaminated.** Orchestrator-verified from the 45 `run_cereals_synthesis_001` traces:
- **Routing is SCATTER: 33 `cereal` / 11 `snack_bar_granola` / 1 `bread`.** Not all-45 cereal.
- **Cereal-ONLY (n=33):** median **14.0**, Q1 5.0, Q3 ~18.5–19.0, IQR **13.5–14.0**, robust_scale **~10.4–13.3** (MAD-sensitive: hand-calcs diverged 6.5 vs 9.0 → **compute via the engine `compute_shelf_stats` at pilot and calibrate bands to THAT**, per the calibration-recheck gate).
- The all-45 IQR (11.0) is **compressed by the granola/muesli products** that should not be on the cereal shelf.

**Therefore:** EV-087's `floor=62 / P=6 / scale=8.896` is calibrated on the wrong (contaminated) distribution → **recalibrate to cereal-only n=33.** And **PRE-A (category-specific scoping) IS required for cereals** — `scope={cereal}` must exclude the 11 granola-routed + 1 bread-routed, or they contaminate the shelf stats and/or get wrongly surcharged.

## ⚠️ Unverified governance stamps in the other track
EV-087 / the P107 board entry claim **"Product D7 co-signed by Product Agent"** and **"orchestrator-verified."** Those were **NOT** performed by this session. Verify independently before relying on them. (EV-086 also references TASK-280, which has no task file.)

## Clean, verified contributions from this session (safe to reuse)
- **Mechanism** `BARI_SHELF_RELATIVE_V1` (Phase-1): built, **default-off, byte-identical** (brined 48/48 + invariants 342, re-verified). Engine: `shelf_relative_differentiator` / `compute_shelf_stats` (IQR-primary) + empty scope/band constants. Governance: EV-084 (line 1881), `shelf_relative_design_v1.md`, `shelf_relative_d7_cosign_v1.md`.
- **Owner philosophy (locked):** ONE absolute scale; relative refines within-shelf; firm absolute floor holds Anti-Immunity; endemic/formulation binary retired.
- **Validated:** yogurt LANDS (61/88 move, 0 absorbed); biscuits COSMETIC (floor-saturated — EV-085, `run_cookies_005_shelfrel_pilot`).
- **Rollout plan:** `rollout_plan_v1.md` + verified spread classification `rollout_spread_analysis_v1.md` (9 LAND / 4 COSMETIC / 3 N-A; hard_cheeses = LAND).
- **This session's cereals proposal (scatter-aware, the correct basis):** `02_products/breakfast_cereals/methodology/shelf_relative_sugar_enrollment_cereals_v1.md` — floor=None rationale (cereals not uniformly indulgent, 11% floored), P=7, cereal-only n=33, named inversions. Reconcile the two cereals proposals before pilot.

## Note on the shared board
This session and the parallel track both edited `tasks/DISPATCH_BOARD.md` concurrently (the cause of the repeated "file changed under me" errors). The board likely needs reconciliation — entries from this session (P96–P105) and the parallel track (P106–P108) may have clobbered each other. The authoritative (other) track should reconcile.
