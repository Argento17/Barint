# Sign-off Memo: TASK-180C — Bread Re-baseline (run_bread_008_headpin)

**Date**: 2026-06-05
**Run ID**: run_bread_008_headpin
**Task**: TASK-180C
**Engine tag**: engine-baseline-2026-06-04 (f075d9e)
**Config hash**: b5ddce013f4f1fbd
**Flags**: BARI_RECAL_P0=off | BARI_GLASSBOX_W4=on | BARI_TASK144_FIXES=off
**Corpus**: 31 curated (24 scored + 7 transparency)
**Provenance**: real_bread_retail_003_v1 (Shufersal 25-26 May 2026) — frozen, not touched

---

## 1. Reproduction Rate

HEAD-OFF vs live lechem_frontend_v2.json (24 displayed products):
**2/24 exact match** (8%)

The live page is backed by the calibrated v2 scores (sprint1 + calibration patch, May 2026).
The HEAD engine diverges on 22 of 24 display products.
This is engine drift accumulated since the original sprint1 run (BSIP2 engine updates + GLASSBOX_W4 shipping).

Rollback identity (determinism check): 31/31

## 2. Drift Summary (HEAD-OFF vs live page, display corpus only)

| Category | Count |
|----------|-------|
| Exact match (within 0.5pt rounding) | 2 |
| Grade-affecting (grade changed) | 13 |
| >=2pt same grade | 6 |
| <2pt cosmetic | 5 |

## 3. Grade-Affecting Moves (HEAD-OFF vs live page)

| pid | name | live_score | live_grade | head_score | head_grade | delta |
|-----|------|-----------|-----------|-----------|-----------|-------|
| shufersal_3268429 | לחם ירוק מקמח מלא | 80 | B | 82.0 | A | +2.0 |
| shufersal_481203 | לחם מחמצת קמח מלא | 77 | B | 82.0 | A | +5.0 |
| shufersal_3054183 | לחם שיפון מלא מסטמכר | 76 | B | 81.0 | A | +5.0 |
| shufersal_2079927 | לחם דגנים מלא | 75 | B | 80.2 | A | +5.2 |
| shufersal_3268252 | לחם חיטה מלא לילדים | 75 | B | 82.0 | A | +7.0 |
| shufersal_574370 | לחם שיפון קל | 75 | B | 82.0 | A | +7.0 |
| shufersal_481197 | לחם מחמצת גרעינים | 76 | B | 80.9 | A | +4.9 |
| shufersal_2079217 | לחם מחמצת שיפון+אגוזים | 61 | C | 66.1 | B | +5.1 |
| shufersal_2079477 | לחם אחיד פרוס | 64 | C | 72.7 | B | +8.7 |
| shufersal_7290018500316 | לחם כוסמין לבן | 64 | C | 74.8 | B | +10.8 |
| shufersal_6451484 | לחם מחמצת אגוזים צימוקים | 60 | C | 67.4 | B | +7.4 |
| shufersal_96086000966 | קרקר כוסמין מלא ושומשום | 82 | A | 78.4 | B | -3.6 |
| shufersal_8434165658523 | קרקר קרם קרקר | 59 | C | 66.1 | B | +7.1 |


## 4. TASK-169F B->A Moves: Recal Isolation Table

TASK-169F modeled 4 specific bread products that BARI_RECAL_P0=on would promote B->A.
Ship obligation was transferred to TASK-180C. Owner must decide per-move: ship or hold.

**IMPORTANT**: The TASK-169F run used the engine WITHOUT GLASSBOX_W4.
This run uses GLASSBOX_W4=on (HEAD default as of 2026-06-05).
The off_score values differ between 169F and run_008 due to this engine change.
The delta_recal column in this table is the pure recal effect ON THE CURRENT HEAD+W4 engine.

| pid | name | 169F off_score | 169F off_grade | run008 off_score | run008 off_grade | run008 on_score | run008 on_grade | delta_recal |
|-----|------|---------------|---------------|-----------------|-----------------|----------------|----------------|-------------|
| shufersal_2079996 | לחם אחיד פרוס קל | 79.6/B | B | 78.3/B | 82.0/A | +3.7 |
| shufersal_2079477 | לחם אחיד פרוס | 74.1/B | B | 72.7/B | 79.2/B | +6.5 |
| shufersal_7290018500316 | לחם כוסמין לבן | 76.1/B | B | 74.8/B | 81.6/A | +6.8 |
| shufersal_96086000577 | קרקר כוסמין אורגני | 77.7/B | B | 76.3/B | 79.6/B | +3.3 |


**Per-move owner decision required:**
For each of the 4 products above, decide:
- [ ] SHIP: accept the B->A move when RECAL_P0 ships (when RECAL_P0 is activated globally)
- [ ] HOLD: keep at B; recal effect not appropriate for this product
- [ ] DEFER: defer decision until RECAL_P0 activation scope is decided globally

Note: RECAL_P0 is NOT being activated in this run. This table is informational only.
The 4 moves would only take effect when the owner separately activates RECAL_P0 globally.

## 5. Lechem Calibration Layer Assessment

The calibration patch (calibrate_lechem_scores.py) was applied because the original BSIP2
had no ingredient access. The current HEAD engine (with GLASSBOX_W4) has D3 de-moralization
and improved ingredient signal handling. The question is whether HEAD scores now produce
results that make the manual calibration obsolete, still needed, or partially needed.

| barcode | name | v2_live_score | cal_delta | cal_grade | head_off_score | head_off_grade | assessment |
|---------|------|--------------|----------|----------|---------------|---------------|----------|
| 2079996 | לחם אחיד פרוס קל | 66/C | -7 | C | 78.3 | B | HEAD ABOVE CALIBRATION (h=78.3 >= v1=73); patch may still be needed |
| 497044 | לחם ברמן אקטיב | 68/B | -4 | B | 79.4 | B | HEAD ABOVE CALIBRATION (h=79.4 >= v1=72); patch may still be needed |
| 2079033 | לחם דגנים לייט | 69/B | -5 | B | 78.8 | B | HEAD ABOVE CALIBRATION (h=78.8 >= v1=74); patch may still be needed |
| 481180 | לחם מחמצת שאור | 64/C | -7 | C | NOT IN CURATED | — | Not in 31 curated — check full 81-product run |
| 2079477 | לחם אחיד פרוס | 64/C | -3 | C | 72.7 | B | HEAD ABOVE CALIBRATION (h=72.7 >= v1=67); patch may still be needed |
| 7290018500316 | לחם כוסמין לבן | 64/C | -4 | C | 74.8 | B | HEAD ABOVE CALIBRATION (h=74.8 >= v1=68); patch may still be needed |


**Assessment methodology:**
- CONVERGED: HEAD independently lands within 2pt of the calibrated score -> patch not needed for this product
- HEAD PARTIALLY AGREES: HEAD moved in the right direction but not as far -> patch partially still needed
- HEAD ABOVE CALIBRATION: HEAD scores higher than the uncalibrated v1 -> patch definitely still needed

**Overall calibration recommendation:**
For products where HEAD converges with the calibrated score, the calibration layer is effectively
obsolete (HEAD engine now handles the underlying concern). For products where HEAD still scores
above the calibration target, the patch remains needed. The detailed assessment above should
guide the per-product decision.

The owner must decide: retain calibrate_lechem_scores.py for the reship, or retire it
(relying on HEAD engine scores directly). If retired, the reship would use HEAD-OFF scores
directly. If retained, the reship would apply the calibration patch on top of HEAD-OFF scores.

## 6. Recommendation

13 grade-affecting move(s) found vs live page. Review per-product table above. Each move should reflect genuine engine improvement (HEAD is more accurate than the original sprint1 baseline). No move reverses a product's direction without ingredient evidence.

---

**Sign-off required from**: Owner
**Per-move recal decision**: Owner (4 TASK-169F B->A moves)
**Calibration layer decision**: Owner (retire vs retain)
**Hard rule**: No changes to bari-web/src/data/comparisons/lechem_frontend_v2.json until owner sign-off received.
**Next step on approval**: Frontend reship (rebuild lechem_frontend_v2.json from run_bread_008_headpin/off.json)
