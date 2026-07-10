---
id: TASK-482
title: Milk gold-standard fixes: false 'complete data' confidence on 18/18 (nulls) + blog milk-analysis renders LEGACY scores (48.5/D) vs live comparison (51.7/C) cross-page contradiction (TASK-474 2x CRITICAL)
owner: data-agent
status: CLOSED
priority: CRITICAL
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: >
  SHIPPED LIVE. PR #61 merged → origin/master 4e46e6fa (verified cbf2a1f7 ancestor). RT-2 blog/comparison grade contradiction removed (legacy score/grade pulled to authoritative corpus, 15/18 were stale, 0/18 mismatch after; corpus authoritative scores 0-changed = NOT a score change). RT-1 false "complete data" fixed by backfilling fat/satFat/carbs/fiber verbatim from BSIP1 run_milk_002 (orchestrator + QA both matched values exactly, OFF-clean) + honest "partial"/ניתוח חלקי confidence matching 5 other categories byte-for-byte. Two-gate: Data author + Adversarial QA GO. Isolation 2 JSON files, 0 scoring, tsc 0. Worktree pruned. Systemic follow-up logged: generator NUTRITION_FIELD_MAP missing carbs/satFat blanks cheese/bread/cereals too (→ batch).
depends_on: []
blocks: []
category_id: null
summary: >
  Milk gold-standard fixes: false 'complete data' confidence on 18/18 (nulls) + blog milk-analysis renders LEGACY scores (48.5/D) vs live comparison (51.7/C) cross-page contradiction (TASK-474 2x CRITICAL)
---

# TASK-482 — Milk gold-standard fixes (TASK-474 batch 6, 2× CRITICAL, orchestrator-VERIFIED)

Source: TASK-474 milk red-team. Both CRITICALs verified against origin/master e615244a.

## Verified facts
- **RT-1 (false completeness):** all **18/18** milk products carry `confidence_tooltip_he` = "כל הנתונים התזונתיים ורשימת הרכיבים נסרקו ישירות מהמוצר" ("all data + ingredients scraped directly") AND `confidence_label_he` = "נתונים מלאים" (complete data) — while `fat`/`satFat`/`carbs`/`fiber` are NULL on 18/18 (sugar/sodium null on several). Example: "חלב מלא בטעם של פעם" has only energyKcal/protein/sodium; fat/satFat/carbs/sugar/fiber all null, yet labeled "complete data." False provenance/confidence claim on the gold-standard page. (Also: WHY is milk fat null across the board? likely a scrape/parse gap for milk nutrition — investigate; missing-data-discard says label it honestly, never fabricate.)
- **RT-2 (cross-page score/grade contradiction):** `milk-page-data.ts` exports TWO product sets from TWO sources — `milkProducts` (line 47) = LEGACY `@/data/milk-comparison.json` (bc 7290110325619 = **48.5/D**), and `milkVmProducts` (line 172) = uniform corpus `milk_frontend_v1.json` (same bc = **51.7/C**). File's own comment: "LEGACY consumers (blog, home-flagship, dimension-bars…)" use `milkProducts`. So **/blog/milk-analysis renders 48.5/D while /hashvaot/milk-comparison renders 51.7/C for the SAME barcode** — a live, grade-level (D vs C) contradiction. This is the TASK-468 stale-legacy-surface risk, NOT fully resolved. (bc 7290110324926: legacy 58.1/C vs live 56.9/C — same grade, minor.)
- **RT-3 downgraded (dead code, NOT live):** the ALMONDS-for-OAT mislabel in `milk-product-insights.ts` (bc 7290110325619) is real but `getProductInsight`/`buildConsumerExplanationView` have ZERO importers → not rendered. Still worth deleting to prevent future revival.
- **RT-4 HIGH:** "highest sugar on shelf" (7.6g, bc 5411188300328) true only among the 9/18 with non-null sugar → unqualified superlative on partial data. **RT-5 HIGH:** antithesis in `milk_frontend_v1.json` (9 comma-lo + 4 אלא) → milk was excluded from the copy overhaul by design → feeds the systemic phrasing sweep.
- **CLEAN (Track V):** 8/8 sampled scores match P478 engine trace exactly, rank/score monotonic, no dup barcodes, OFF-ban clean, 3 known-better nutrition pairs ranked correctly.

## Deliverable (Data + Content, two-gate; gold standard = extra care)
1. **RT-2:** make the blog milk-analysis render the SAME live scores as the comparison page (repoint `milkProducts`-consuming surfaces to the corpus set, or reconcile the legacy `milk-comparison.json` to live). Verify NO live surface shows a different score/grade for any barcode. This is the priority — it's a visible grade contradiction.
2. **RT-1:** make the milk confidence label/tooltip HONEST — either the fields get populated from a real source (investigate the null-fat scrape gap; NEVER OFF, NEVER fabricate) or the label reflects partial data. Owner honesty doctrine: "unknown is acceptable; overclaiming is not."
3. RT-4 superlative → qualify or drop. RT-3 dead code → delete. RT-5 antithesis → fold into the phrasing sweep.
4. Any consumer score/label/copy change → two-gate + owner PR (tripwire-2).

## DISPATCHED (owner 2026-07-03: "change the milk, don't wait for me... it is like any other category" — milk gold-standard status RETIRED, see memory owner_milk_page_content_gold_standard). Data Agent, worktree C:\bari_wt_t482, branch fix/task482-milk commit cbf2a1f7.

## Fix RETURNED + orchestrator-VERIFIED
- **RT-2:** root cause = legacy `milk-comparison.json` score/grade drifted from corpus on **15/18** (not 1). Fixer patched legacy score/grade/grade_label to match the authoritative corpus. **Orchestrator-verified:** legacy==corpus **0/18 mismatches**; corpus score/grade **0 lines changed** vs origin (authoritative scores untouched — NOT a score change; aligning a stale surface to the already-live value). Also auto-fixes home-flagship-analysis.tsx (same milkProducts source).
- **RT-1:** root cause = milk frontend JSON hand-extracted at TASK-321D from a legacy schema that never carried fat/carbs; generator `NUTRITION_FIELD_MAP` (generate_page.py:309) ALSO missing carbs/satFat keys. Real fat/satFat/carbs/fiber ARE in BSIP1 run_milk_002. Fixer backfilled verbatim from BSIP1 (18 fat, 18 carbs, 12 satFat, 7 fiber; satFat/fiber genuinely null on the rest). **Orchestrator-verified:** spot-check bc 7290110325619 corpus fat/satFat/carbs/fiber = 3/0.3/5/1.5 == BSIP1 normalized_nutrition_per_100g EXACTLY; BSIP1 OFF-clean. Scoring unaffected (score_engine reads BSIP1 directly, not the frontend map). Confidence relabeled to standard `partial`/"ניתוח חלקי" for 15, kept `verified`/"נתונים מלאים" for 3 genuinely-complete. Isolation: 2 JSON files, 0 .ts, tsc exit 0.
- **→ Adversarial QA gate DISPATCHED** (a0fb057f, bg): 18-barcode legacy==corpus, ≥6-barcode nutrition-vs-BSIP1, confidence-pattern byte-match vs other cats, copy-vs-new-data contradiction hunt, corpus-score-untouched. On GO → push → owner PR (tripwire-2).

## Adversarial QA gate = GO (both gates satisfied). Independently reproduced: legacy==corpus 0/18, corpus score/grade 0 changed vs master, direction verified (legacy→corpus x15 never reverse), 7-barcode BSIP1 nutrition match exact, OFF-clean (8 grep hits = BARI_*_V1 flags, false positives), partial tooltip byte-identical to cheese/bread/cookies/hummus/juices, 0 copy contradictions vs newly-shown numbers, 2 JSON files only. QA out-of-scope note: "verified/complete" label wording differs ACROSS categories pre-existing (cheese "נתונים מאומתים", bread "מבוסס על נתונים מלאים", milk "נתונים מלאים") → Content standardization backlog, not a blocker.
## SHIPPED → PR #61: https://github.com/Argento17/Barint/pull/61 (owner merge = tripwire-2). CLOSE on merge; prune worktree C:\bari_wt_t482.

## SYSTEMIC follow-up (out of scope, do NOT block): generator `NUTRITION_FIELD_MAP` (generate_page.py:309) omits `carbs`/`satFat` → those display null 100% on cheese/bread/cereals too, despite BSIP1 having the data. Display-only (scoring unaffected). → generator-hardening backlog (relates TASK-479); a cross-category nutrition-backfill pass would fix all at once.
