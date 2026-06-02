# Cottage / White Cheese — Post-Fix Run Findings (run_cheese_002)

**Tasks:** TASK-142 (cycle) + **TASK-145** (router cream-cheese anchor) · **Date:** 2026-06-01
**Engine:** proto_v0 / 0.4.0 + TASK-145 cream-cheese router anchor (**EV-025**, routing-only)
**Supersedes:** run_cheese_001 (pre-fix diagnostic; misroute 47.4%, QA-CHS-001)
**Verdict:** **DoD MET** on data/routing/QA gates; frontend package launch-candidate, NON-AUTHORITATIVE pending Nutrition sign-off.

---

## What changed (TASK-145, governed under bari-bsip2-scoring-governance)

Added four specific cream-cheese hard anchors to `router_v2.py` → `dairy_protein` (`גבינת שמנת`, `ממרח גבינה`, `פילדלפיה`, `נפוליאון`), with a `נפוליאון` cake-exclusion (`עוגה/עוגת/פס/מאפה/בצק`). **Routing/identity only — no scoring weight/threshold/penalty/cap.** Bare `שמנת` deliberately excluded (sour/sweet/whipping cream are not cheese).

**Governance checklist (all PASS):** evidence **EV-025** (JSON+MD); label observability = `canonical_name_he` (100%); scope = cheese-spreads, collision-audited vs maadanim/yogurt/milk (0 matches); rollback = git revert hunk; no rule duplication (no prior cream-cheese anchor). Mirrors TASK-139C.

**Regression-lock:** router regression **15/15 PASS** (12 frozen + 3 new: cream-cheese anchor, cheese-spread anchor, napoleon-cake exclusion). Determinism confirmed: re-running batch_run_cheese_001 on the patched router == run_cheese_002.

## Result (run_cheese_002, same 57 BSIP1 corpus)

| Metric | run_cheese_001 (pre-fix) | run_cheese_002 (post-fix) |
|---|---|---|
| Misroute | 47.4% (27/57) | **1.8% (1/57)** ✅ |
| Insufficient (displayable) | 5.3% (3/57) | **0% (0/57)** ✅ |
| Grades | B36/C16/A1/D1* | A6/B23/C27/D1 |
| Cream pool routing | all 26 misroute | all 26 → dairy_protein ✅ |
| Display-approved | 29/57 | **50/57** |

\* run_001 traces carried stale NOVA for some correctly-routed products (pre-curation-rebuild); the misroute finding (47.4%) was correct and is what TASK-145 fixed.

**Residual misroute (1):** גבינת עזים 32% שומן (32% goat) → snack_bar_granola. 1.8% < 5% gate; low priority.

**Per pool (correctly routed):** cottage 11 (all B, median 76.6) · white-cheese/quark 17 (B7/A6/C4, median 73.8) · labaneh 3 (B2/C1, median 74.8) · cream-cheese-spread 26 (C22/B3/D1, median 60.7 — high fat + stabilizers, plausible).

## A-ceiling working as designed

6 white-cheese SKUs reach **85/A on raw macros** (גבינה לבנה 5%/9%, טבורוג 5%) but **all fail the dairy A-ceiling C1–C6** — binding on **C3** (no confirmed/credited live culture in the scraped panel). Per EV-021/RULING-DAIRY-A-01 these A grades are **WITHHELD**. This is the conservative dairy ceiling functioning correctly: plain white cheese without declared live cultures does not publish at A.

## Status

All **data + routing + QA gates PASS**. The only remaining gate to live promotion is **Nutrition/Product grade-publication sign-off** (the 6 withheld A's + the correctly-routed grades). Frontend package `factory_run_002/frontend_package.json` (50/57 display-approved, 2 Sec 6.4 disclosures in clean RTL Hebrew) is the launch-candidate, held NON-AUTHORITATIVE pending that sign-off. run_cheese_001 / factory_run_001 are retained as the pre-fix diagnostic record (why TASK-145 existed).
