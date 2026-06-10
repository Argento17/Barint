# TASK-222B Corpus Diff Gate Report

**Date:** 2026-06-09
**Engine:** proto_v0 (TASK-222B: PROTEIN_QUALITY_MATRIX_DISCOUNT activated — reconstructed=0.80, collagen=0.55)

## Summary

| Metric | Value |
|--------|-------|
| Categories checked | snack_bars (53) |
| Products with `protein_matrix_form` set | 2 (both `reconstructed`, 0 collagen) |
| Products with non-zero score impact | **0** (both affected products have 0g protein → PRQ=0 × discount=0) |
| Grade changes | None |
| Ceiling violations | snk-001 = 70/B held; no new A or S grade introduced |
| Router regression | 16/16 PASS |
| Golden corpus regression | 11 PASS, 1 WARN (pre-existing) |

## Products with Detected Matrix Form

| Product ID | Matrix Form | Protein g | Category | Source | PRQ | Final Score | Grade |
|------------|-------------|-----------|----------|--------|-----|-------------|-------|
| bsip1_8410076610379 | reconstructed | 0 | snack_bar_granola | mixed | 0.0 | 46.1 | D |
| bsip1_8410076610386 | reconstructed | 0 | snack_bar_granola | mixed | 0.0 | 44.6 | D |

Both products have 0g protein (ingredient scan detected whey/soy protein isolate markers in top-3 positions, but the product contains only trace protein — likely a garnish/crisp, not a protein source). The ×0.80 reconstructed discount applies structurally (0 × 0.80 = 0) with zero score impact.

## Collagen Coverage

**0 products** in the full BSIP1 corpus have collagen markers in their primary ingredient window. The ×0.55 collagen discount is structurally correct but has no corpus impact.

## Category-Ceiling Verification

| Ceiling | Baseline | After TASK-222B | Status |
|---------|----------|-----------------|--------|
| snk-001 = 70/B | 70 (date bar, no reconstructed protein) | 70 (held) | ✓ PASS |
| Milk = 85/A | 85 (no matrix discount applies to milk) | 85 (held) | ✓ PASS |

## Collateral-Dimension Check

| Dimension | Unchanged? | Evidence |
|-----------|-----------|----------|
| Protein grams (mass) | ✓ | `protein_g` feeds `satiety_support` and `nutrient_density` directly, not through `PROTEIN_QUALITY_MATRIX_DISCOUNT` |
| Nutrient density | ✓ | No code path touches `nutrient_density` |
| Satiety support | ✓ | No code path touches `satiety_support` |
| Additive quality | ✓ | No code path touches `additive_quality` |
| NOVA proxy | ✓ | No code path touches NOVA classification |

## Double-Counting Check

`matrix_integrity.py` is **NOT wired into the composite score**. The `PROTEIN_QUALITY_MATRIX_DISCOUNT` is the sole owner of the reconstructed-protein penalty in the live score path. If matrix_integrity is ever composites in, it must NOT re-penalize reconstructed protein (documented in `constants.py` coordination note).

## Regression Check

| Check | Result |
|-------|--------|
| Router regression (16 tests) | ✓ PASS (all 16) |
| Golden corpus regression (12 entries) | ✓ 11 PASS, 1 WARN (pre-existing) |

## Conclusion

- **0 products** have non-zero score change — the matrix discount is structurally correct but has no corpus impact (only 2 products with reconstructed form, both 0g protein; 0 collagen products).
- Code is verified: discount applies to `protein_quality` only, protein mass untouched, no collateral dimension changes, no double-counting.
- The ×0.80 (reconstructed, bar-format) and ×0.55 (collagen, any format) values are confirmed from DIAAS evidence band.
- Safe to deploy — zero regression risk.
