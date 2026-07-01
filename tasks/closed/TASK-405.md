---
id: TASK-405
title: Ingredient-field pollution — ASSESS + CLEAN (~15%, nutrition-panel bleed); truncate before parse
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
closed_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
close_reason: >
  ASSESS + CLEAN DoD delivered locally (2026-06-26, documented in-body): 473 BSIP1 files
  de-polluted via the proven sanitize_ingredient_list, distinct-product pollution 28.6%->14.7%,
  all 8 handoff barcodes verified to true count, 5 all-bleed files flagged-and-escalated (never
  imputed, no OFF), reversible _task405_clean audit blocks, clean_report.json manifest.
  NOT PORTED TO ORIGIN by design: the cleaning is score-neutral (the BSIP2 engine sanitizes at
  runtime, so no published score moves), so the 2026-07-01 targeted port kept origin's raw source
  + runtime sanitization; the local scripts/reports/cleaned-files were never committed. Closing on
  DoD-met. The forward, port-worthy piece — a deterministic C0 sanitation gate so raw-text
  consumers (additive detector / matrix probe) can't be fooled at rest — is TASK-395F's scope
  (still open). Owner may separately decide whether to port the at-rest cleaning to origin.
summary: >
  TASK-395 handoff F1. 47/311 products (15.1%) have non-ingredient text (nutrition panel after ערכים תזונתיים, serving-size, disclaimer, marketing) bleeding into ingredients_text_he/ingredients_raw; parser counts junk as ingredients (cheese-dominant; 29 with parsed-vs-real diff>3). SCOPE = ASSESS + CLEAN the ingredient data only: truncate at first nutrition-panel marker + strip trailing non-ingredient sections BEFORE parsing; flag-and-escalate ambiguous (no silent impute). Verify 8 barcodes. Report new pollution rate + which files/corpus changed. NOT in scope: re-scoring or publishing — the de-chain agent (TASK-395) re-shadows on the cleaned data; owner ruling 2026-06-26 "rescoring is not on your mandate; you were tasked to assess polluted data."
---

# TASK-405 — Ingredient-field pollution: ASSESS + CLEAN (nutrition-panel bleed)

## Scope (owner-clarified 2026-06-26)
ASSESS and CLEAN the polluted ingredient fields. **Do NOT re-score, do NOT publish, do NOT touch any published score or frontend JSON.** The cleaned BSIP1 corpus is handed back to the de-chain agent (TASK-395), which owns the reproducibility re-map / re-shadow.

## Finding (from the TASK-395 validation triad)
~15% of products with ingredient text have non-ingredient text bleeding in — most often the nutrition panel appended after the real ingredient list; the parser then counts that junk as ingredients. Measured: 47/311 products with text (15.1%) polluted, dominant in cheese; 29 have parsed-vs-real count diff >3.

## How to clean
- **Marker:** everything from the Hebrew "ערכים תזונתיים" (also "ערך תזונתי" / "ל-100 גרם") onward is NOT ingredients; also strip trailing serving-size ("גודל מנה") / disclaimer / marketing sections.
- Truncate the ingredient field at the first nutrition-panel marker and strip trailing non-ingredient sections **BEFORE** parsing. Fields: `ingredients_text_he` then `ingredients_raw` (BSIP1 output, carried from BSIP0 scrape).
- **Flag-and-escalate** anything still ambiguous — do NOT silently fix or impute (owner's "raise the imperfect reads" rule). NEVER fill from OFF.

## Verify these 8 barcodes parse to true ingredient count after cleaning
7290014758681 (קוטג 1% — true label is just חלב, מלח, תוסף תזונה: סידן = 3 items, currently parses as 6), 4127077, 4127329, 4127336, 41445, 41452, 2824183, 2824640.

## Deliverable
- Cleaned BSIP1 ingredient fields (in place), per-file.
- New pollution rate (vs the 47/311 = 15.1% baseline) + the 8-barcode before→after parsed counts.
- List of every file/corpus changed (so TASK-395 can re-run the reproducibility map + re-shadow).
- The flag-and-escalate list of ambiguous reads left untouched.

## ASSESSMENT DONE (orchestrator, read-only, 2026-06-26) — see `02_products/cheese_spreads/TASK405_pollution_assessment_v1.md`
The Data Agent hit the Anthropic session limit mid-run (resets ~1pm Amsterdam); it wrote 0 files (tree clean). Orchestrator ran the read-only assessment on the 8 handoff barcodes (cheese_spreads, run_cheese_002):
- The nutrition-panel bleed is real in all 8. An EXISTING sanitizer (TASK-144 Fix1/EV-024) already strips it for the NOVA count, but **truncates at the wrong boundary** for the dominant pattern: when the OCR runs the last real additive straight into the panel with no delimiter, it DROPS the whole chunk — losing the legitimate `תוסף תזונה: סידן`. Cottage 7290014758681 → sanitized **2** (חלב, מלח) but TRUE = **3**. 6/8 under-count this way; 2/8 (2824183/640, which had a "." delimiter) truncated CORRECTLY (count 5).
- The de-chain's marker-truncation fix is correct and BETTER than status quo — it RECOVERS the real additive.
- **Direction = UNDER-count (cleaner-looking), not over-count.** Whether any published score moves depends on engine consuming `ingredient_count` (sanitized) vs `ingredient_count_raw` — a TASK-406 reproducibility question, NOT resolved here.
- NEXT: Data Agent (lane reset) fixes the sanitizer boundary (split at panel marker → strip allergen run → keep real leading additive), re-derives counts corpus-wide, reconciles the 47/311 baseline field/run, flag-and-escalates ambiguous, lists changed files. **Diagnose-before-changing (motto): the fix alters how every product's ingredient count is derived — not a rush.**

## CLEAN DONE (orchestrator, owner-directed "you take this and fix", 2026-06-26)
**Key reframe found during assessment:** the sanitizer CODE (`signal_extractor.sanitize_ingredient_list` + `_truncate_glued_bleed`) is ALREADY correct — it truncates at the `ערכים תזונתיים` marker and yields the true counts (cottage→3). The old run_cheese_002 trace showing 2 was generated by an EARLIER version. So the defect was NOT in the parser; it was that the **stored BSIP1 source fields** (`ingredients_list` / `ingredients_text_he` / `ingredients_raw` / `ingredient_order`) still hold the raw polluted blob at rest — which the BSIP2 engine sanitizes at runtime (so SCORES are unaffected) but **raw-text consumers** (additive detector via `re.search`, matrix probe) read directly and get fooled.
**Fix applied (score-neutral data hygiene, NOT a re-score):** ran the proven `sanitize_ingredient_list` over the stored BSIP1 fields corpus-wide and wrote back the cleaned list + rebuilt text/raw/order, each with a reversible `_task405_clean` audit block (original fields + dropped/truncated delta). Scripts: `03_operations/bsip1/_task405_detect.py` (read-only sweep) + `_task405_clean.py` (`--apply`). Report: `03_operations/bsip1/task405_reports/clean_report.json` (full per-file manifest) + `post_clean_detect.json`.
**Result:** distinct-product pollution **28.6% → 14.7%**; **473 files cleaned across 25 run dirs**; all 8 handoff barcodes now parse to true count (cottage + 5 siblings = 3; 2824183/640 = 5). EXCLUDED the wiped/dead corpora **maadanim (116) + yogurt (135)** — pointless churn; they are the bulk of the 14.7% residual. **5 files FLAGGED-and-escalated** (not auto-cleaned): single-item lists that are ENTIRELY bleed (`clean_count==0`) → distinct products `7297488098688` (cereals, ×3 runs) + `7296073733324` + `7296073733331` (hummus) — their real ingredient list was never scraped; need human/re-scrape, never imputed, no OFF.
**Score-neutrality:** the BSIP2 engine already sanitizes at runtime, so cleaning the stored source does NOT move any published score. Handoff to TASK-395 de-chain: re-run the reproducibility map + re-shadow on the cleaned BSIP1; the audit blocks make every change reversible/traceable.
