# TASK-222C Corpus Diff Gate Report

**Date:** 2026-06-09
**Engine:** proto_v0 (TASK-222C: BHA/E320 synonym gap fix — E-320 variant added to ingredient_taxonomy.py)

## Summary

| Metric | Value |
|--------|-------|
| BHA prevalence (full BSIP1 corpus, 1,357 products) | **2 products (0.15%)** — both in `run_bread_light_001` |
| BHT prevalence (full BSIP1 corpus) | **12 hits**, but BHT is explicitly NOT penalized per F4 design |
| Scoring impact | **2 products** receive the existing −5 BHA penalty on additive_quality (net −3 after lecithin relief +2) |
| Grade changes | None (both products remain in their existing additive_quality grade range) |
| Ceiling violations | None (bread light is not a ceiling-gated category) |
| Router regression | 16/16 PASS |
| Golden corpus regression | 11 PASS, 1 WARN (pre-existing) |

## Affected Products

| Product ID | BHA | BHT | ID Delta | AQ Score | Category |
|------------|-----|-----|----------|----------|----------|
| bsip1_bread_light_9990001000030 | True | True | −3.0 (−5 BHA + +2 lecithin) | 43.0 | snack_bar_granola |
| bsip1_bread_light_9990001000032 | True | False | −3.0 (−5 BHA + +2 lecithin) | 43.0 | cracker |

**Note:** These products already had `E-320` in their ingredient text, but the taxonomy only matched `E320` (no hyphen). The penalty code was always live at `BHA_NAMED_PENALTY=5` — the synonym gap was preventing detection. TASK-222C fixes the gap. The scoring impact is real but bounded to these 2 products.

## Category-Ceiling Verification

| Ceiling | After TASK-222C | Status |
|---------|-----------------|--------|
| snk-001 = 70/B | 70 (held, snack bar ceiling not affected by bread light products) | ✓ PASS |
| Milk = 85/A | 85 (held) | ✓ PASS |

## Regression Check

| Check | Result |
|-------|--------|
| Router regression (16 tests) | ✓ PASS (all 16) |
| Golden corpus regression (12 entries) | ✓ 11 PASS, 1 WARN (pre-existing) |

## Conclusion

- Prevalence is near-zero (2/1,357 = 0.15%) — no scoring sprint; the fix is a taxonomy data-quality correction.
- The `E-320` synonym was the only gap preventing detection of BHA in these 2 bread light products.
- Fix is minimal (1 synonym string per additive) and bounded in impact.
- Safe to deploy.
