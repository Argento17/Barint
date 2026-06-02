# bread_retail_003 / bsip2 — AUTHORITATIVE LAUNCH CORPUS

**Status:** FROZEN — authoritative launch corpus for Bread (לחם) BSIP2
**Frozen by:** TASK-129C (nutrition-agent)
**Date:** 2026-06-01
**Controller decision:** 2026-06-01 — `bread_retail_003` declared authoritative (TASK-129-A confidence re-audit, §3 P0 #4, §7)
**source_run_id:** `real_bread_retail_003_v1`
**Freeze report:** `C:\Bari\03_operations\bsip2\run_bread_retail_003\baseline_freeze_report.md`
**CLAUDE.md frozen invariant:** matches `real_bread_retail_003_v1` (Shufersal, 25–26 May 2026)

## Provenance chain

| Stage | Count | Artifact |
|-------|-------|----------|
| Scraped (representative Shufersal shelf) | 256 | `02_products/bread_retail_003/bsip2/bsip2_shufersal_*.json` |
| Scored / coherent | 81 | `02_products/bread_retail_003/lechem_frontend_v2.json` (calibrated, Bread Calibration Patch v1) |
| Displayed (curated launch set) | 24 | `bari-web/src/data/comparisons/bread_frontend_v2.json` (`_meta.source_run_id: real_bread_retail_003_v1`) |

The 24 displayed rows = the curated launch shelf. 7 additional transparency rows exist in the wider curation (31 curated total per CLAUDE.md invariant) but are not in the scored display set. This directory holds the slim BSIP2 export traces (256) that the frontend pipeline draws from.

## Known Limitations (must accompany any display)

1. **All 24 displayed rows are `partial` confidence (0 `verified`).** The slim retail export schema carries nutrition panels but only 9 of 24 rows carry a real ingredient list; the rest have `ingredients: null`. This is disclosed in-UI as `נתונים חלקיים` and is an accepted partial-confidence shelf, not a defect. Root re-scrape with ingredient lists folds into a future `run_bread_retail_004`.
2. **`energyKcal`, `sugar`, `fat` are `null` across all 24 displayed rows** — the retail export captured protein/fiber/sodium only. Scores are valid (structural + fiber + sodium + fermentation signals); do not display kcal/sugar/fat dimension breakdowns as actionable data.
3. **Fiber-source nuance (shufersal_7290016245325, לחם טחינה פרוס, 82/A):** the 18.5g fiber originates from tahini, not whole-grain matrix. Insight line discloses this; do not present its fiber as grain-structure evidence.
4. **Fermentation claim vs. ingredient gap:** several "מחמצת" (sourdough)-named rows show industrial yeast in the ingredient list where one is available. Disclosed per-row in `insightLine` and `limitingFactors`.

## Do Not Modify

This directory is frozen. Do not re-run, overwrite, or patch any traces.
All future re-runs (post ingredient/kcal re-scrape) must write to `run_bread_retail_004` or later. The displayed scores are versioned under the already-frozen bread framing ("best ≠ excellent") — framing unchanged, numbers frozen.
