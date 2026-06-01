# Tahini — Expected Corpus Size

**Task:** TASK-054  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Category:** Tahini

---

## Summary

| Scenario | Expected corpus | Gate status |
|----------|----------------|-------------|
| Conservative | 35–45 products | PASS (≥ 30) |
| Expected | 48–65 products | PASS comfortably |
| Optimistic (both retailers + organic section) | 65–80 products | PASS with margin |

**The 30-product gate will pass in all scenarios.**

The Tahini category is not at risk of corpus insufficiency. The main uncertainty is the yield from the Yohananof scrape and the organic section, not the core count.

---

## Section 1 — Discovery Estimates by Sub-Type

### 1.1 Raw Tahini (Ambient Shelf)

Israel has a well-developed tahini market. Major brands include: Achva (אחווה), Adam (אדם), Rena (רינה), Adina (עדינה), Baron (ברון), Har Bracha (הר ברכה), Shufersal private-label, Yohananof private-label, El Nakhleh (אל נח'ל), and imports from Jordan and Lebanon.

| Sub-type | Shufersal estimate | Yohananof estimate | Total |
|---|---|---|---|
| Standard hulled sesame tahini (major brands) | 12–18 | 5–8 | 17–26 |
| Whole sesame tahini ("כל שומשום") | 5–8 | 3–5 | 8–13 |
| Roasted tahini | 4–7 | 2–4 | 6–11 |
| Organic tahini | 5–9 | 4–7 | 9–16 |
| Flavored tahini (lemon, garlic) | 2–4 | 1–2 | 3–6 |
| Ethiopian / Humera sesame tahini | 2–4 | 1–3 | 3–7 |
| Shufersal/Yohananof private label | 2–3 | 1–2 | 3–5 |
| **Raw tahini subtotal** | **32–53** | **17–31** | **49–84** |

### 1.2 Ready-to-Eat Tahini Dip (Refrigerated Shelf)

Ready-to-eat tahini dip was deferred from the hummus corpus. It will be acquired here via targeted search queries, not shelf traversal (to avoid duplicating the hummus BSIP0 traversal).

| Sub-type | Shufersal estimate | Yohananof estimate | Total |
|---|---|---|---|
| Plain ready-to-eat tahini dip | 4–7 | 2–4 | 6–11 |
| Ready-to-eat with garlic/spices | 2–4 | 1–2 | 3–6 |
| Artisanal / branded dip preparations | 2–3 | 1–2 | 3–5 |
| **Tahini dip subtotal** | **8–14** | **4–8** | **12–22** |

### 1.3 Sweetened Tahini

| Sub-type | Shufersal estimate | Yohananof estimate | Total |
|---|---|---|---|
| Tahini with date paste | 2–4 | 1–3 | 3–7 |
| Tahini with honey | 2–3 | 1–2 | 3–5 |
| Tahini with carob | 1–2 | 0–1 | 1–3 |
| **Sweetened tahini subtotal** | **5–9** | **2–6** | **7–15** |

### 1.4 Grand Total — Approved Products (Before Cleanup)

| Scenario | Raw tahini | Tahini dip | Sweetened | **Total** |
|---|---|---|---|---|
| Conservative | 32 | 10 | 6 | **48** |
| Expected | 45 | 15 | 9 | **69** |
| Optimistic | 55 | 18 | 12 | **85** |

---

## Section 2 — Exclusion Estimates

Some products discovered during BSIP0 will be excluded in cleanup (Stage 6 of the factory workflow).

| Exclusion type | Expected count |
|---|---|
| Halva and halva spread | 5–10 |
| Chocolate-tahini spread | 3–6 |
| Sesame candy and confections | 3–6 |
| Sesame seeds (whole, not paste) | 3–5 |
| Sesame oil | 2–4 |
| Multi-packs and catering sizes | 2–4 |
| Duplicate with hummus corpus | 3–7 |
| Cooking sauces failing dilution test | 1–3 |
| Single-serving sachets | 1–2 |
| **Total expected exclusions** | **23–47** |

---

## Section 3 — Net Corpus After Cleanup

| Scenario | Gross discovery | Exclusions | Net corpus |
|---|---|---|---|
| Conservative | 48 | 13 | **35** |
| Expected | 69 | 21 | **48** |
| Optimistic | 85 | 28 | **57** |

**All three scenarios clear the 30-product gate with margin.**

Even the conservative scenario (35 products) exceeds the gate minimum. The expected scenario (48 products) provides a solid comparison corpus and is consistent with what the hummus category produced (69 products from a broader category).

---

## Section 4 — Sub-Type Coverage

The corpus must represent at least 3 sub-types for the comparison page to be meaningful:

| Sub-type | Expected count (mid-scenario) | Gate threshold |
|---|---|---|
| Raw tahini (hulled, whole, roasted, organic) | 30–40 | ≥ 10 |
| Ready-to-eat tahini dip | 10–15 | ≥ 5 |
| Sweetened tahini (date/honey) | 5–9 | ≥ 3 |

All three sub-types are expected to clear their minimum thresholds.

**If the ready-to-eat dip sub-type falls below 5 products:** Expand the Yohananof search query list and probe the refrigerated section directly. This is unlikely but possible if many dips were already captured in the hummus exclusion_log and the Shufersal refrigerated shelf was reorganized.

---

## Section 5 — Ingredient Coverage Expectations

Tahini is a category with excellent expected ingredient coverage because:

1. **Raw tahini:** Single-ingredient products (sesame) have the simplest possible label. Even if the scraper misses some label text, the product is identifiable. Expect > 95% coverage.

2. **Ready-to-eat dip:** More complex ingredient lists (3–7 ingredients). Expect ~85–90% coverage based on hummus experience with adjacent products.

3. **Sweetened tahini:** 2–4 ingredients typically. Expect > 90% coverage.

**Overall ingredient coverage estimate:** 90–95% — higher than hummus (94%) because the tahini category has fewer products with missing ingredient data (tahini has no private-label no-name products at the scale hummus had).

---

## Section 6 — Fat Data Quality Expectation

This is the most critical data quality dimension for this category.

**Raw tahini fat content:**
- Theoretical: 55–60g fat/100g (from sesame composition)
- Saturated: ~8g (15% of total fat)
- Expected `fat_g` in BSIP1: 50–62g (within label rounding tolerance)

**Shufersal fat-row defect risk:**
- The TASK-039 defect caused `fat_g = 0.5` (saturated fat captured instead of total fat) for 59/69 hummus products
- For tahini, if the same defect fires: `fat_g ≈ 8` (saturated fat sub-row captured instead of total fat)
- Unlike hummus (where 0.5g was obviously wrong), tahini at 8g fat might look plausible to a casual audit

**Caloric gap analysis (mandatory gate check):**
For raw tahini at 600 kcal, 20g protein, 20g carbs:
```
Implied fat = (600 − 20×4 − 20×4) / 9 = (600 − 80 − 80) / 9 = 48.9g
```
If `fat_g < 20g` for any raw tahini product → fat-row defect confirmed → BLOCK gate.

**Expected defect rate prediction:**
- If Shufersal fixes the fat-row parser before this run: 0% defect rate
- If defect persists: ~60–80% of Shufersal products will be affected (consistent with hummus rate)
- The defect is structural (same HTML parser, same nutrition panel format)

**Recommended action if defect is confirmed:**
1. Document in BSIP0 gate report
2. Compute `fat_g_implied_kcal_gap` for all affected products (per TASK-039 methodology)
3. Decide with CNO before BSIP1 whether to:
   a. Patch `fat_g` values (corrected run from gap analysis — more accurate fat_quality scores) OR
   b. Proceed with warning (fat_quality marked unreliable for affected products)

Option (a) is strongly preferred for Tahini because `fat_quality` is the **primary differentiating dimension** for this category (unlike hummus, where it was the least impactful dimension at 8% weight). Proceeding with corrupt fat data would make the tahini comparison less useful.

---

## Section 7 — BSIP2 Grade Distribution Forecast

Based on the category boundary and expected corpus composition:

| Grade | Score range | Expected count | Products |
|---|---|---|---|
| S (90–100) | 90–100 | 0 | None expected in this format |
| A (80–89) | 80–89 | 20–30 | Raw tahini (NOVA 1 floor dominates) |
| B (65–79) | 65–79 | 10–20 | Tahini dip (simple); sweetened tahini; flavored tahini |
| C (50–64) | 50–64 | 5–12 | Tahini dip with preservatives/stabilizers; diluted preparations |
| D (35–49) | 35–49 | 0–5 | Heavily reconstructed tahini sauce; very diluted products |
| E (0–34) | 0–34 | 0 | Not expected |
| insufficient_data | — | 2–5 | Products with missing nutrition labels |

**Key forecast notes:**

- **Grade A cluster will be large.** The NOVA 1 floor (85) protects all single-ingredient raw tahini products. With 30–40 raw tahini products in the corpus, the A-grade cluster will dominate. This is correct but may compress the visible comparison — users comparing A vs. A products get limited signal.
- **The meaningful differentiation is in the B/C range.** Ready-to-eat tahini dips and flavored variants will produce a spread of B–C scores that are useful for consumer comparison.
- **Fat quality calibration gap.** If the fat-row defect is patched before BSIP2, fat_quality will become the dominant driver for products that score below A. If not patched, all products will receive neutral fat_quality (50), and the differentiation will come from additive_quality and processing_quality only.

---

## Section 8 — Gate Risk Assessment

| Gate criterion | Risk | Assessment |
|---|---|---|
| Total products ≥ 30 | Low | Expected 48–57 net products; highly unlikely to fail |
| Nutrition coverage ≥ 85% | Low | Tahini labels are standardized; coverage will exceed 90% |
| Fat_g plausibility ≥ 90% of raw tahini products with fat_g > 40g | **Medium** | Depends on whether Shufersal fat-row defect persists; plan for defect and have correction protocol ready |
| Ingredient coverage ≥ 80% | Low | Expected 90%+ coverage |
| Sub-type coverage (≥ 3 types) | Low | Raw tahini, dip, sweetened all expected |
| Halva exclusion rate | Low | Hard-exclude terms will catch halva reliably |
| Hummus duplication | Low | Cross-check protocol documented; deduplication is straightforward |

**Overall gate risk: Low.** The fat_g plausibility check is the only non-trivial risk. Plan for it explicitly with the caloric gap analysis protocol.

---

*Expected Corpus Size — Tahini — TASK-054 — 2026-05-31*  
*Owner: Data Agent*  
*Expected net corpus: 48–57 products (35 minimum, 57 expected, 70+ possible)*
