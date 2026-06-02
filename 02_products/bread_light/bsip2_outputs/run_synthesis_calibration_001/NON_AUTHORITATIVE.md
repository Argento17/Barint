# run_synthesis_calibration_001 — NON-AUTHORITATIVE / EXPERIMENTAL

**Status:** NON-AUTHORITATIVE — experimental synthesis run. NOT a launch source.
**Marked by:** TASK-129C (nutrition-agent)
**Date:** 2026-06-01
**Controller decision:** 2026-06-01 — `bread_retail_003` (`real_bread_retail_003_v1`) is the sole authoritative bread launch corpus.

## What this run is

A score-synthesis / calibration experiment over **32 synthetic bread products** (`bsip1_bread_light_99900010000xx`), with full BSIP2 traces. It was used to develop the post-score synthesis layer (GSS / fiber / fermentation / engineering nuance) — see memory `bsip2_synthesis_calibration_v1`. The products are **synthetic, not real retail items**.

## Why it is not authoritative

- The launch shelf must be a real, representative retail corpus. This run is synthetic.
- The authoritative bread launch corpus is **`real_bread_retail_003_v1`** only:
  - Authoritative marker: `C:\Bari\02_products\bread_retail_003\bsip2\AUTHORITATIVE.md`
  - Freeze report: `C:\Bari\03_operations\bsip2\run_bread_retail_003\baseline_freeze_report.md`
  - Displayed corpus: `C:\Bari\bari-web\src\data\comparisons\bread_frontend_v2.json` (24 rows, `source_run_id: real_bread_retail_003_v1`)

## Prohibition

This directory must not be read by the frontend packaging pipeline or treated as a launch/display source. The full traces here may be referenced for synthesis-layer methodology only. Do not surface any score, grade, or product from this run to users.
