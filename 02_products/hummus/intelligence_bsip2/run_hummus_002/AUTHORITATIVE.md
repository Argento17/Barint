# run_hummus_002 — AUTHORITATIVE BASELINE

**Status:** FROZEN — authoritative baseline for Hummus BSIP2  
**Frozen by:** TASK-045  
**Date:** 2026-05-31  
**Freeze report:** `C:\Bari\03_operations\bsip2\run_hummus_002\baseline_freeze_report.md`  
**Corpus:** 69 products — Shufersal hummus and savory dips  
**Router version:** router_v2 with savory-spread anchors (TASK-044)

## Known Limitations (must accompany any display)

1. `fat_quality` dimension unreliable for 58/69 products — Shufersal fat-row scraping defect (TASK-039)
2. 2 products carry `insufficient_data` grade (bsip1_7296073733317, bsip1_7296073733348) — no nutrition panel; display score placeholder only
3. 2 products routed to `default` — ambiguous product names without savory keyword anchors; scores are valid but category label is imprecise

## Do Not Modify

This directory is frozen. Do not re-run, overwrite, or patch any traces.  
All future re-runs (including post-fat-fix re-runs) must write to `run_hummus_003` or later.
