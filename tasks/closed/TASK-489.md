---
id: TASK-489
title: Cross-page brand completeness — audit all live comparison pages (re-audit on origin/master), classify each gap fillable-vs-source-empty, backfill from scrape
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "BOTH PHASES DONE. Phase-1 audit answered owner 'verify all brands': 13/16 pages fully branded; cheese live=v5 47/47 (v4/v5 worry moot). Phase-2 SHIPPED LIVE PR #76 (merged; origin/master 26e57834; 24 hard_cheeses brands live). 24 fillable carried from canonical bsip1_task412 (all shufersal), 7 yohananof source-empty left null. Barcode-keyed: only brand changed on 31, #69 carbs/satFat preserved. bread(18)/crackers(17)/hummus(57) = genuine SOURCE-EMPTY, honest-null (no OFF/fabrication). Hummus name-token extraction = owner left blank (orch rec)."
depends_on: []
blocks: []
category_id: null
summary: >
  Owner (2026-07-03): "verify that all brands appear in all comparison pages." Orchestrator LOCAL-tree audit
  found gaps (crackers 2/19 [→ TASK-486: source-empty, not fillable], hard_cheeses_v4 0/31, bread_v4 5/23,
  hummus_v5 29/57) — but that audit was run on the DIVERGED local tree and is unreliable for any file that
  differs on origin/master (e.g. live cheese = v5 not v4). PHASE 1 = re-audit brand coverage on the ACTUAL
  live files (origin/master + the real page-data import graph) for ALL comparison pages, and classify each
  missing brand as FILLABLE-from-scrape vs SOURCE-EMPTY (like crackers, where the retailer scrape's brand
  field was empty for all 19 — a genuine unknown, not a pipeline loss). PHASE 2 = backfill the fillable ones
  from the direct scrape only (OFF BANNED; source-empty stays null per missing_data_discard_rule).
---

# TASK-489 — cross-page brand completeness (owner "verify all brands appear")

## PHASE 1 — AUDIT (read-only, do this first; do NOT edit yet)
For EVERY live comparison page, using origin/master + the real import in bari-web/src/lib/comparisons/
*-page-data.ts (do NOT trust the local working tree — it is diverged; confirm the live file per import):
1. Count brand present vs null per file (live file only).
2. For each null-brand product, determine from the committed BSIP0/BSIP1 scrape + corpus whether a brand is
   RECOVERABLE (present in the scrape's brand/manufacturer field or unambiguously in the product name via the
   existing brand_extractor whitelist) or SOURCE-EMPTY (scrape carried no brand — like crackers TASK-486).
3. Return a per-file table: live file, N, brand present, fillable count, source-empty count, with evidence.
This directly answers the owner's "verify all brands" question with a definitive per-page picture.

## PHASE 2 — BACKFILL (after Phase 1 returns + orchestrator reviews)
- Backfill ONLY the FILLABLE brands, from the direct scrape / corpus. **OFF (Open Food Facts) BANNED any
  field/any fallback forever. Tzameret directional-only.** Source-empty stays null (no fabrication, no
  over-sourcing — missing_data_discard_rule).
- ⚠️ FILE-OVERLAP: hard_cheeses_v4 + bread_v4 are also touched by TASK-487v2 (PR #69, carbs/satFat). Do the
  backfill for those two OFF PR #69's merge (or its branch) to avoid a conflict; hummus_v5 + any others are
  independent and can go off origin/master. Orchestrator will sequence Phase 2 dispatch after #69 lands.
- Consumer-facing (brand shows on cards/rows) → owner PR (tripwire-2). Zero score/grade/rank change.

## Guards
- Base off origin/master (NOT local HEAD — F1 divergence bit twice already this batch). OFF ban absolute.
- Phase 1 is READ-ONLY (no edits). Recommend, don't fabricate.

## Return (Phase 1): per-file audit table + fillable-vs-source-empty classification + Return Contract JSON.
Propose RETURNED. Do not write CLOSED.

## PHASE 1 RETURNED (Data, read-only, origin/master @29795088) + orchestrator-reviewed
- **16 comparison pages, 580 products: 459 brand present, 121 missing.** 13/16 pages fully branded. cheese live = v5 (47/47 clean) — the owner's v4/v5 divergence worry is a non-issue. magnesium 18/18 (hardcoded inline).
- **3 pages with gaps, classified from the committed direct scrape (no OFF, no Tzameret, no il_prices):**
  - **hard_cheeses_v4 0/31 → 24 FILLABLE + 7 source-empty.** PIPELINE BUG not source-empty: 24/31 barcodes HAVE a real brand in the proven canonical source `02_products/hard_cheeses/bsip1_task412` (TASK-429 byte-reproduces the file) — the frontend builder just never carried `brand` over. 7/31 (yohananof-sourced) genuinely null at source. → **worth a Phase-2 field-carry backfill (24), zero score risk.**
  - **bread_v4 18/23 missing → ALL source-empty** (Shufersal scrape brand="" at BSIP0, byte-verified). Leave null.
  - **crackers 17/19 → source-empty** (confirms TASK-486). Leave null.
  - **hummus_v5 57/57 → source-empty at every layer** (BSIP0 shufersal + BSIP1 canonical all brand=""). JUDGMENT-CALL flagged (NOT auto-applied): product NAMES carry apparent brand/line tokens (אבו גוש/אחלה/צבר/יום יום) that a brand_extractor.py whitelist extension could surface like bread/crackers' KRIT/Osem — but that's a scoring-adjacent precision call (misattribution risk) for Nutrition/Product, not an audit auto-fill.
- **PHASE 2 (queued):** hard_cheeses 24-brand field-carry backfill ONLY, off PR #69's branch/merge (hard_cheeses_v4 file overlap w/ TASK-487v2). Others leave honest-null (missing_data_discard_rule). Hummus name-token extraction = owner/Nutrition decision, held.

## PHASE 2 DISPATCH (2026-07-03, owner "continue with the hard cheese") — #69 MERGED (origin/master 32198372), overlap cleared
- Data Agent off origin/master 32198372 (now carries #69 carbs/satFat on hard_cheeses_v4). Carry `brand` for the 24 FILLABLE barcodes from committed canonical `02_products/hard_cheeses/bsip1_task412`; leave the 7 yohananof source-empty null. OFF banned. Preserve carbs/satFat/scores/copy byte-identical (only add brand). Consumer-facing (brand on cards) → owner PR. Hummus HELD (owner left blank per orch rec).
- **RETURNED + orchestrator-VERIFIED:** 24 filled (all shufersal canonical brand) + 7 null (yohananof source-empty) = exact _meta retailer_breakdown match. Barcode-keyed vs origin/master (3-dot, merge-base 32198372): ONLY `brand` changed on all 31 (0 non-brand change); carbs/satFat from #69 preserved 29/31; tsc 0; branch touches only hard_cheeses_frontend_v4.json.
- **🚀 PR #76 OPENED** https://github.com/Argento17/Barint/pull/76 (brand on cards = consumer-facing = owner merge, tripwire-2). On merge → CLOSE TASK-489 (both phases done). bread/crackers/hummus stay honest-null (source-empty). Prune C:\Bari\bari_wt_t489.
