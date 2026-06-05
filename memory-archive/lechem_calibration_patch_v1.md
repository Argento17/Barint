---
name: lechem-calibration-patch-v1
description: "Bread Calibration Patch v1 — 10 score corrections, 7 grade changes B→C, root cause of scoring failure, output files"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af7e0b5-ff02-43a8-b8df-e8e443e61a10
---

Surgical post-scoring calibration applied to `lechem_frontend_v1.json` → `lechem_frontend_v2.json`.
No BSIP2 rerun. Synthesis-layer corrections only.

**Why:** BSIP2 bread scorer had no access to parsed ingredient data — only nutrition macros and product name.
Four failure modes identified:
1. Fiber from added inulin/isolated fiber scored identically to whole-grain fiber
2. White flour as primary base received no structural penalty
3. Fermentation credit from name detection (white-flour sourdough ≠ whole-grain sourdough)
4. Additive load (E-numbers, dual preservatives) had zero effect on score

**Result:** 74% B grade (60/81) → 65% B (53/81). C: 22% → 31%. No A or D regressions.

**10 corrections (5 types):**

| Barcode | Name | Before | After | Type |
|---------|------|--------|-------|------|
| 2079996 | לחם אחיד פרוס קל | 73/B | 66/B | fiber_laundering (added fiber 3rd ingredient) |
| 2079033 | לחם דגנים לייט | 74/B | 69/B | fiber_implausible (14.2g vs ~6g plausible) |
| 497044 | לחם ברמן אקטיב | 72/B | 68/B | inulin_augmentation (explicit 3% inulin) |
| 481180 | לחם מחמצת שאור | 71/B | 64/C | fermentation_authenticity (75% white flour, 2.5g fiber) |
| 497570 | לחם דגנים פלוס | 68/B | 62/C | fiber_laundering (12.7g vs ~4.5g plausible) |
| 7290018500316 | לחם כוסמין לבן | 68/B | 64/C | white_spelt_base (sifted spelt, 3.3g fiber) |
| 2079477 | לחם אחיד פרוס (אסם) | 67/B | 64/C | additive_accumulation (dual preservative, "שיא התוספות") |
| 4033736 | לחם עננים בסגנון בריוש | 66/B | 62/C | white_flour_base (100% white, sugar 2nd, 3 emulsifiers) |
| 7290018500231 | לחם אנג'ל WEEKEND | 65/B | 62/C | white_flour_base (white+sugar, enriched) |
| 7290017947105 | לחם בסגנון אמריקה | 65/B | 62/C | white_flour_base (white+sugar, enriched) |

**Output files:**
- `C:\Bari\02_products\bread_retail_003\lechem_frontend_v2.json` — canonical frontend JSON (use this, not v1)
- `C:\Bari\02_products\bread_retail_003\lechem_calibration_patch_v1.md` — full audit trail with rationales
- `C:\Bari\02_products\bread_retail_003\calibrate_lechem_scores.py` — repeatable patch script

**How to apply:** rebuild by running `calibrate_lechem_scores.py` (reads v1, writes v2).

**Insight line contradictions resolved:** all 7 grade-changed products now have scores that confirm rather than contradict their insight lines.

**Why:** Consumer trust logic — WEEKEND and America-style white breads no longer share a grade letter with 100% whole-grain clean-label products.

**How to apply:** Wire `lechem_frontend_v2.json` to frontend, not v1. The `_calibration` field in each patched product records the v1 score for audit purposes (strip before production if needed).
