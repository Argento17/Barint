---
id: TASK-169C
title: P2/P3 frozen wave — milk run_004 recal re-approval + rescore (BARI_RECAL_P0)
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
close_reason: "Milk frozen wave complete + shipped live. Rescore run_milk_005_recal_p0 (BARI_RECAL_P0=on, config 832fdb55e03cae06) verified against artifacts: 85/A dairy ceiling HELD (0 products score >85, 0 A-crossings; טבעי 4% + עיזים 85/A->85/A), lactose-free leak closed (74.1->79.3/B, does not reach A), R7 culture-gate leaked the +8 to 0/20 milks, flag-OFF inert 20/20. The ONLY consumer-visible recal move = rice drink משקה אורז (8000215204219) D->C: a pure-recal delta (head_off==live==49.4, zero drift; driver = R3 leanness raising fat_quality 50->86, trace-confirmed). Owner chose to update plant-drink scores live. Shipped SURGICALLY to bari-web/src/data/milk-comparison.json — rice row only (49.4/D->52.3/C; grade_label->בינוני; fat_quality->86.0; whyRated 49->52 x2). Frontend score 52.3 = raw 55.31 minus the builder's ~3.0 calibration transform (reconciled, not invented). git diff = 6 lines, all in the rice entry; dairy + 16 other rows byte-identical. CC gate PASS: re-read live file = rice 52.3/C, dairy anchors untouched at 85/A; tsc 0 errors; next build clean (all routes incl /hashvaot/milk-comparison static); JSON valid. Other plant-drink recal deltas were sub-grade noise (<2pt) or HEAD-drift-contaminated -> deliberately NOT shipped (a whole-file rebuild would import dairy drift, unsafe). SEPARATE pre-existing QA item surfaced: HEAD reproduces only 13/20 published run_004 traces (engine drift since 2026-05-18, not a recal effect) -> needs a QA freshness task. Production deploy still needs cc-agent-v2->master merge (owner action)."
summary: >
  Frozen wave under TASK-169. P0 v1.1 model showed the recal leak CLOSED on fluid milk (lactose-free 87.3->79.3/B, 0 A-crossings, 85/A HELD) — expected to be a confirm-and-hold wave, not a promotion. Deliverable: rescore milk run_004 with BARI_RECAL_P0=on into a new run id, diff vs live, confirm no frozen-invariant breach, owner per-move sign-off, then reship milk frontend JSON (or formally confirm no change). Flag OFF = byte-identical rollback.
---

# TASK-169C — P2/P3 frozen wave — milk run_004 recal re-approval + rescore (BARI_RECAL_P0)

## Owner authorized start (2026-06-03)
Owner gave the per-move sign-off to **begin the rescore** (first frozen wave released). Unblocked → IN_PROGRESS. This authorizes the rescore + diff only; the **ship** decision (repoint live milk JSON, or formally confirm no change) is a second owner sign-off after the diff is presented.

## Scope / deliverable (Data Agent)
Rescore the frozen milk corpus (`run_004` / `run_004_recalibrated`) with `BARI_RECAL_P0=on` into a NEW run id; do NOT touch published dirs or live JSON. Produce:
1. **Before/after diff** of every milk product (live score/grade → recal score/grade), highlighting any grade move.
2. **Frozen-invariant check:** confirm the **85/A ceiling HELD** (top = whole/4%/goat) and enumerate any A-crossing or any product that breaches it. The P0 v1.1 model predicted 0 milk A-crossings and closed the lactose-free leak (87.3→79.3/B) — verify that holds on the real rescore.
3. **Rollback proof:** flag-OFF rescore == current published baseline (byte-identical), as in 169A/169B.
4. **Regression:** golden + router clean OFF and ON.
5. **Ship recommendation:** "no change → confirm-and-hold (no reship)" vs "N grade moves → list them for owner ship sign-off."

Governance: per `bari-bsip2-scoring-governance`. No live score ships from this task without the second owner sign-off. R-rules in play for milk = R1 (category-relative protein) + R3 (leanness) + R5 (sat-fat cap→penalty); R7 culture-gate must EXCLUDE plain milk (verify no +8 leaks to fluid milk).

## CLOSED (CC, 2026-06-03) — verified + shipped
Data Agent rescore (`run_milk_005_recal_p0`) returned a clean **confirm-and-hold on the invariant**: 85/A dairy ceiling held, lactose-free leak closed, R7 gate excluded all 20 milks, flag-OFF 20/20 byte-identical. Independently re-verified against the run artifacts before closing (see close_reason).

**Owner decision:** update the plant-drink scores live. The only consumer-visible recal move on the milk shelf is the rice drink **D→C** (pure recal, zero drift). Shipped surgically to `bari-web/src/data/milk-comparison.json` (rice row only; dairy + 16 rows byte-identical, 6-line diff). tsc/build/JSON all clean.

**Deliberately not shipped:** the other plant-drink recal nudges were either <2pt noise or HEAD-drift-contaminated; a whole-file rebuild would have imported pre-existing engine drift onto the frozen dairy rows, so only the one clean, drift-free row was changed.

**Follow-ups (not part of this wave):**
- **QA freshness item (new):** HEAD reproduces only 13/20 of the published `run_004` traces — engine drift since 2026-05-18, independent of recal. The legacy milk page is on May-18 scores. Recommend a QA task to quantify drift across the legacy pages and decide a clean re-baseline.
- **Production deploy:** still needs `cc-agent-v2 → master` merge (owner).
- **Next frozen wave:** snack-bars (169E) per the recommended order.
