# Red-Team Report — Granola (run_granola_task385_off)

**Task:** TASK-385 · **Date:** 2026-06-23 · **Run:** run_granola_task385_off · **Page:** /hashvaot/granola
**Verdict: FAIL (CHANGES_REQUESTED)** — go-live gate NOT clear; page is live with confirmed defects (owner-authorized fixes in progress).

This file is the canonical D10 artifact (was missing → RT-4). Findings below are **orchestrator-verified against the product labels/traces**, not raw agent prose.

## Track V (verification) — score side CLEAN
- score==trace: **22/22 PASS, 0 mismatch** (independently re-derived).
- OFF=0 (the `_meta.excluded_off_products` string is an exclusion audit record, not a data source).
- Nutrition completeness 22/22; prologue math (B4/C8/D8/E2, top 69.7/B, bottom 31.4/E, gap 38.3) PASS.

## CONFIRMED CONTENT DEFECTS (verified vs BSIP1 label) — CRITICAL
- **RT-1 / rank 5 (7290106773714):** "חמישה סוגי אגוזים" — label = 3 nuts (שקדים/קשיו/אגוזי לוז) + 2 SEEDS (חמנייה/דלעת). Fabricated category claim.
- **RT-2 / rank 6 (7290112498007):** "שמן קנולה" — label says only "שמן צמחי", never canola. **Fabricated ingredient** (carried v1 copy, never re-audited). Also "שני מקורות סוכר" undercounts (≥3).
- **RT-8 / rank 18 (7290011131968):** "ארבעה מקורות סוכר" — label lists FIVE (סוכר/סירופ תמרים/סוכר חום/סירופ גלוקוז/דבש).
- **RT-3 / metric:** headline metric = FIBER (granola-comparison-page.tsx:33) — owner-confirmed wrong (fiber is gameable via added chicory/inulin); creates fiber-vs-grade inversions. → change to sugar + protein.

## CONFIRMED CONTENT DEFECTS — HIGH/MEDIUM
- **C3-#3 / rank 19:** "25g = גבול הסף האדום הישראלי" — false; 25g is far above any threshold (regulatory ~10g; engine 17.5g).
- **RT-7:** 6 carried verdicts use the "יורדת ל-X כי" calque (ranks 9,11,12,14,16,17) — translationese.
- **RT-6 / C3:** a SUGAR metric bar will visibly contradict grades (13 cross-grade sugar inversions, e.g. [13] 9.3g=D below [11] 15.6g=C) unless cards show the non-sugar drivers.
- **RT-10/12/13:** sugar-source undercount (rank 6), ambiguous "מהנמוכים בקטגוריה" (rank 22).
- **RT-11:** rank 18 confidence_sub_reason "low_extraction" not supported by trace (confidence_score=90).
- **RT-5:** `_meta.pending_copy_count=7` stale (all 7 authored) — clear it.

## SCORING-COHERENCE QUESTIONS (→ Nutrition re-exam, may move grades)
Sugar cap @17.5g binary vs owner de-anchor directive; [19] 25g under-penalized (D, same band as 18g); NOVA proxy noise ([13] NOVA-4 @9.3g vs [19] NOVA-3 @25g).

## Root-cause
Orchestrator re-authored only the 7 grade-movers and did NOT re-audit the 15 CARRIED v1 verdicts against current data (→ canola fabrication). C3 consult was skipped. First QA pass missed both. Owner caught it on live review.

## Disposition (owner: "yes to all", 2026-06-23)
Hotfix the live fabrications now (Content) + Nutrition scoring re-exam + full 22-verdict re-audit (C3 in loop) + sugar+protein metric with explainers → C3 + red-team re-gate → re-deploy.
