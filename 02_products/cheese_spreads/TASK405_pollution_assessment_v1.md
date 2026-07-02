# TASK-405 — Ingredient-pollution ASSESSMENT (orchestrator, read-only)
**Date:** 2026-06-26 · **Scope:** assess polluted ingredient data (owner: "you were tasked to assess polluted data"; re-scoring NOT in scope).
**Status:** ASSESSMENT of the 8 handoff barcodes done; full-corpus clean deferred to the Data Agent (Anthropic session limit hit mid-run, resets ~1pm Amsterdam; it wrote 0 files — tree clean).

## What the 8 TASK-395 barcodes actually show (cheese_spreads, run_cheese_002 traces)
The nutrition-panel bleed is REAL and present in every one. BUT an existing sanitizer
(`ingredient_sanitization`, tagged **"TASK-144 Fix1/EV-024: non-ingredient OCR/nutrition/disclaimer
bleed removed before NOVA count inference"**) already strips it for the NOVA count — and it strips
at the WRONG BOUNDARY for the dominant pattern.

| barcode | raw_count | sanitized count | TRUE count | sanitizer action | correct? |
|---|---|---|---|---|---|
| 7290014758681 (קוטג' 1%) | 6 | **2** (חלב, מלח) | **3** (חלב, מלח, תוסף תזונה: סידן) | DROPPED whole final chunk | ❌ over-truncates |
| 4127077 | 6 | 2 | 3 | DROPPED whole final chunk | ❌ |
| 4127329 | 6 | 2 | 3 | DROPPED whole final chunk | ❌ |
| 4127336 | 6 | 2 | 3 | DROPPED whole final chunk | ❌ |
| 41445 | 6 | 2 | 3 | DROPPED whole final chunk | ❌ |
| 41452 | 6 | 2 | 3 | DROPPED whole final chunk | ❌ |
| 2824183 | 8 | 5 | 5 | TRUNCATED at marker (kept מייצב) | ✅ |
| 2824640 | 8 | 5 | 5 | TRUNCATED at marker (kept מייצב) | ✅ |

## Root cause (precise)
The OCR concatenates the last real ingredient, the allergen declaration, and the nutrition panel
into ONE comma-chunk with no delimiter, e.g.:
`"תוסף תזונה: סידן (טריקלציום פוספט) מכיל חלב עלול להכיל חלב ערכים תזונתיים 100 גרם 62 קל ..."`
- When a delimiter (".") precedes the panel (2824183/640), the sanitizer's split isolates the real
  ingredient and TRUNCATES correctly → keeps it.
- When there is NO delimiter (the 6 cottage-type), the sanitizer can't isolate the real additive and
  **DROPS the entire chunk**, losing the legitimate `תוסף תזונה: סידן` → undercount 3→2.

## Why this matters / direction (NOT a rush — diagnose before changing derived counts)
- The de-chain's prescribed fix is correct and BETTER than the status quo: **truncate at the
  `ערכים תזונתיים` (/ `ערך תזונתי` / `ל-100 גרם`) marker** and also strip the allergen run
  (`מכיל חלב` / `עלול להכיל`), rather than dropping the whole chunk. This RECOVERS `תוסף תזונה: סידן`
  for the 6 cottage-type products (and the same class corpus-wide), yielding the true count.
- Direction of the count error here is UNDER-count (2 vs 3) → makes these products look marginally
  "cleaner" than they are. Whether any published score moves depends on whether the engine consumes
  the sanitized `ingredient_count` (2) vs `ingredient_count_raw` (6) — a reproducibility question for
  TASK-406, NOT resolved here.
- The RAW `ingredients_text_he` string still carries the full bleed and feeds OTHER consumers
  (additive detector, matrix probe — see `03_operations/bsip2/proto_v0/reports/ingredient_reading_diagnosis_v1.md`,
  2026-06-25). That is the broader exposure beyond the NOVA count.

## Handoff to the Data Agent (when the lane resets) — the clean pass
1. Fix the sanitizer boundary: split/truncate at the nutrition-panel marker first, THEN strip the
   allergen run, preserving any real leading additive in the chunk. Re-derive counts corpus-wide.
2. Re-measure the pollution rate vs the 47/311 (15.1%) baseline using the de-chain's definition (it
   reported the cottage as "parses as 6" → it measured `ingredient_count_raw`, so reconcile which
   field/run the 47/311 came from).
3. Flag-and-escalate any chunk where the real-vs-panel boundary is ambiguous; never impute; never OFF.
4. List every file/corpus changed for the de-chain reproducibility re-map.
