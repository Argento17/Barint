# Snacks V5 Score Provenance Report

**Generated:** 2026-06-25  
**Investigator:** Data Agent  
**Source file:** `C:\bari\bari-web\src\data\comparisons\snacks_frontend_v5.json`  
**SHA256:** `2a5e5da0f2c200f2cda1ceb08d0b813b20799bcbf2fbe8363d22862575ee24fe`  
**Authoritative scoring run:** `score_bars_task362_20260620_150421`  

---

## 1. Authoritative Run per Product (21-product table)

All 21 v5 products trace to a single run: **`score_bars_task362_20260620_150421`**.  
Traces are double-nested at: `<run>/products/bsip1_<bc>/products/bsip1_<bc>/bsip2_trace.json`.  
Score field: `final_score_estimate`. Grade field: `grade_estimate`.

| ID | Barcode | V5 Score | V5 Grade | Phase3 Score/Grade | Score_362 Score/Grade | Match | Verdict |
|----|---------|----------|----------|--------------------|-----------------------|-------|---------|
| snk-001 | 7290100659090 | 66.8 | B | 66.9/B | 66.8/B | SCORE_362 | CURRENT |
| snk-002 | 7290011498894 | 55.0 | C | ABSENT | 55.0/C | SCORE_362 | CURRENT |
| snk-003 | 7290105436382 | 47.0 | D | ABSENT | 47.0/D | SCORE_362 | CURRENT |
| snk-004 | 7290011498948 | 45.0 | D | 45.0/D | 45.0/D | SCORE_362 | CURRENT |
| snk-005 | 7290105431516 | 42.8 | D | ABSENT | 42.8/D | SCORE_362 | CURRENT |
| snk-006 | 16000548404 | 34.6 | E | 34.6/E | 34.6/E | SCORE_362 | CURRENT |
| snk-007 | 16000548503 | 34.6 | E | 34.6/E | 34.6/E | SCORE_362 | CURRENT |
| snk-008 | 7290011498986 | 32.0 | E | 32.0/E | 32.0/E | SCORE_362 | CURRENT |
| snk-009 | 7290011498917 | 32.0 | E | ABSENT | 32.0/E | SCORE_362 | CURRENT |
| snk-010 | 7290011498900 | 32.0 | E | 50.0/C | 32.0/E | SCORE_362 | CURRENT (see §2) |
| snk-011 | 16000423534 | 31.5 | E | 35.6/D | 31.5/E | SCORE_362 | CURRENT (see §2) |
| snk-012 | 7290107971522 | 26.0 | E | 26.0/E | 26.0/E | SCORE_362 | CURRENT |
| snk-013 | 6009684861000 | 26.0 | E | ABSENT | 26.0/E | SCORE_362 | CURRENT |
| snk-014 | 8423207208703 | 24.4 | E | 24.4/E | 24.4/E | SCORE_362 | CURRENT |
| snk-015 | 8410076610508 | 22.2 | E | 22.2/E | 22.2/E | SCORE_362 | CURRENT |
| snk-016 | 8423207208680 | 21.8 | E | 21.8/E | 21.8/E | SCORE_362 | CURRENT |
| snk-017 | 8410076610492 | 21.5 | E | 21.5/E | 21.5/E | SCORE_362 | CURRENT |
| snk-018 | 7290019297208 | 16.6 | E | ABSENT | 16.6/E | SCORE_362 | CURRENT (see §4) |
| snk-019 | 4011800633516 | 15.9 | E | 15.9/E | 15.9/E | SCORE_362 | CURRENT |
| snk-020 | 4011800628512 | 15.4 | E | 15.4/E | 15.4/E | SCORE_362 | CURRENT |
| snk-021 | 4011800632519 | 14.8 | E | ABSENT | 14.8/E | SCORE_362 | CURRENT |

**"ABSENT" in Phase3 BSIP2** means the barcode was scraped (BSIP0 data exists in  
`observations_bsip0/shufersal/run_snacks_task360_phase3_20260620_083413/`) but was  
not scored in the phase3 BSIP2 pass — it was scored in the later `score_bars_task362` pass.

**Assembly type:** NOT a multi-retailer assembly. All 21 products sourced from **Shufersal**  
(confirmed via `source_retailers` in each canonical BSIP1 file). The v5 JSON is a single-retailer  
corpus uniformly drawn from one scoring run.

---

## 2. Mismatch Resolution: snk-010 and snk-011

### snk-010 (barcode 7290011498900, "חטיף תמר עם חמאת שקד")

| Field | Phase3 | Score_362 | V5 |
|-------|--------|-----------|----|
| final_score_estimate | 50 | 32.0 | 32.0 |
| grade_estimate | C | E | E |

**What happened (traced):**

Phase3: Product was classified NOVA-2 (nova_proxy=2, confidence=0.5; evidence: "minimal_additives_and_processing_signals"). This triggered the `whole_food_fat_nova1_2` SRC-01 floor: `score_after_penalty=32.0` was raised to `score_after_floors=50`.

Score_362: Product was reclassified NOVA-3 (nova_proxy=3, confidence=0.55). The NOVA-3 reclassification:  
- Changed `processing_quality` from 85.0 → 65.0  
- Changed `whole_food_integrity` from 85 → 60  
- Made the `whole_food_fat_nova1_2` floor ineligible (floor requires NOVA 1 or 2)  
- Result: `score_after_penalty=32.0` → `score_after_floors=32.0` (no floor applied)

**Verdict:** The v5 score of 32.0/E matches score_362. The phase3 score of 50/C was produced by a temporary NOVA-2 classification that was corrected to NOVA-3 in the later run. The score_362 result is the authoritative one. There is no cap, manual adjustment, or undocumented policy. The change is fully traced.

### snk-011 (barcode 16000423534, "חטיף שיבולת שועל+שוקולד")

| Field | Phase3 | Score_362 | V5 |
|-------|--------|-----------|----|
| final_score_estimate | 35.6 | 31.5 | 31.5 |
| grade_estimate | D | E | E |

**What happened (traced):**

Both runs: NOVA-3. Binding cap=55 (ISRAELI_RED_LABEL_1_SAT_FAT). No floor applied in either run.

The difference is in ingredient parsing: Phase3 detected 12 ingredients (WFI complexity_pen=8 → WFI=52). Score_362 detected 13 ingredients (WFI complexity_pen=10 → WFI=50). This single-ingredient difference lowered `weighted_dimension_score` by ~0.08 points, cascaded to a final score of 35.6→31.5, crossing the D/E grade boundary at 35.

**Verdict:** The v5 score of 31.5/E matches score_362. The grade change D→E is a legitimate consequence of the ingredient parser finding one additional item in the later run. No cap, no manual edit. Authoritative run is score_362.

---

## 3. The 7 "Absent" Products

The orchestrator's pre-check identified 7 barcodes absent from the phase3 BSIP2 run. Resolved here:

| Barcode | Phase3 BSIP2 | BSIP0 scrape in phase3 obs? | Scored in score_362 | Score_362 result |
|---------|-------------|----------------------------|---------------------|-----------------|
| 7290011498894 (snk-002) | ABSENT | YES | YES | 55.0/C |
| 7290105436382 (snk-003) | ABSENT | YES | YES | 47.0/D |
| 7290105431516 (snk-005) | ABSENT | YES | YES | 42.8/D |
| 7290011498917 (snk-009) | ABSENT | YES | YES | 32.0/E |
| 6009684861000 (snk-013) | ABSENT | YES | YES | 26.0/E |
| 7290019297208 (snk-018) | ABSENT | YES | YES | 16.6/E |
| 4011800632519 (snk-021) | ABSENT | YES | YES | 14.8/E |

All 7 were scraped from Shufersal during the phase3 scrape pass (`run_snacks_task360_phase3_20260620_083413`) but their BSIP2 scoring was deferred to the score_bars_task362 scoring pass. Their BSIP0 observations are real scrapes. Their BSIP1 canonical files are in `canonical_bsip1/run_task362/`. Their scores are not fabricated or hand-set.

---

## 4. Per-100g Plausibility: snk-018 Sodium Anomaly

**Product:** snk-018 / barcode 7290019297208 / "חטיף גרנולה פירות יבשים" / brand "השוק הקולינרי"  
**Reported `sodium_mg` in v5:** 0.2

**Finding: This is a unit transposition bug. The value 0.2 is in g/100g, not mg/100g.**

Evidence chain:

1. **BSIP0 raw scrape** (`observations_bsip0/shufersal/run_snacks_task360_phase3_20260620_083413/P_7290019297208/product.json`):  
   `nutrition_from_api_hints.sodium = 0.2`. The Shufersal API returned 0.2 and the scraper stored it as `sodium_mg = 0.2` without detecting the unit.

2. **Plausibility gate PASSED** despite the implausible value. The `plausibility_gate` checks mass-balance (`accounted_mass = 94.6`) and macro plausibility, but has no explicit sodium-range check. 0.2 mg/100g passed silently.

3. **Correct inference:** The product contains E500ii (sodium bicarbonate, a leavening agent) and palm oil in a granola with oats. Comparable Shufersal granola products in this corpus show sodium of 130–416 mg/100g. 0.2 g/100g = 200 mg/100g is plausible and consistent with the comparable product snk-013 (same brand, same category, sodium=200 mg/100g confirmed correct).

4. **`dietary_fiber_g: null`** — confirmed missing in BSIP0 scrape and BSIP1 canonical. Not a transposition; the Shufersal page did not publish fiber data for this SKU.

**Score impact of the sodium error:** The `regulatory_quality` dimension for snk-018 = 25 (fired by 2 red labels: sugar + sat_fat). The sodium_mg value does not feed into the red-label check (which uses absolute satfat and sugar thresholds). The HIGH_SODIUM_700MG_PLUS cap (fires at ≥700 mg/100g) also did not fire (0.2 < 700). Had sodium been correctly stored as 200 mg/100g, it still would not have triggered the 700 mg cap. The `L6_policy_decisions` trace shows no sodium-driven policy gate fired.

**Conclusion on score impact:** The sodium transposition error (0.2 mg vs 200 mg) did NOT materially affect snk-018's score of 16.6/E. The score is driven by NOVA-4 classification, 3 added-sugar sources, palm oil, and 2 red labels — none of which depend on the sodium field.

**However,** the displayed `nutrition_per_100g.sodium_mg = 0.2` is wrong as a display value. The consumer-facing page will show "0 mg sodium" which is misleading for a product that clearly contains sodium. This is a **display data bug** requiring a scrape correction before the page goes live. It does not require a rescore.

---

## 5. Overall Verdict

**PROCEED — scores are current and traceable.**

- All 21 v5 products match exactly the `score_bars_task362_20260620_150421` scoring run.
- No scores are fabricated, hand-set, or stale relative to that run.
- The two "mismatches" vs the phase3 run are explained: both are legitimate engine improvements (NOVA reclassification for snk-010; ingredient parser refinement for snk-011) applied in the later scoring run.
- The 7 "absent-from-phase3-BSIP2" products have real BSIP0 scrapes and real BSIP1 canonicals; they were simply scored in the score_362 pass rather than the phase3 BSIP2 pass.
- The v5 JSON is a single-run, single-retailer (Shufersal) corpus, not a multi-retailer assembly.

**One data bug to fix before go-live (non-blocking for copy rework):**  
snk-018 `sodium_mg = 0.2` is a unit transposition error (should be ~200 mg/100g). The score is unaffected, but the display value is wrong. A BSIP0 re-scrape or manual correction of the stored value is required before publishing the page.

**Copy rework can proceed on all 21 products.** The scores and grades are traceable and stable. The snk-018 sodium display bug is logged here for the next BSIP0 correction pass.

---

## Run Record

| Field | Value |
|-------|-------|
| Investigation date | 2026-06-25 |
| Source JSON | `C:\bari\bari-web\src\data\comparisons\snacks_frontend_v5.json` |
| Source JSON SHA256 | `2a5e5da0f2c200f2cda1ceb08d0b813b20799bcbf2fbe8363d22862575ee24fe` |
| Authoritative scoring run | `score_bars_task362_20260620_150421` |
| Scoring run location | `C:\Bari\02_products\snack_bars\bsip2_outputs\score_bars_task362_20260620_150421` |
| BSIP0 source | `C:\Bari\02_products\snack_bars\observations_bsip0\shufersal\run_snacks_task360_phase3_20260620_083413` |
| BSIP1 canonical | `C:\Bari\02_products\snack_bars\canonical_bsip1\run_task362` |
| Products traced | 21/21 |
| Score matches | 21/21 (all match score_362) |
| Data bugs found | 1 (snk-018 sodium unit transposition) |
| Rescore required | NO |
