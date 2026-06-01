# Bari Scoring System Verdict v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Final Verdict  
**Reviewer posture:** External scientific advisory board. Not defending the framework.

---

## Verdict

**MODERATE REVISION**

---

## Reasoning

### What the red team found

After auditing 18 snack products, three cross-category distributions, eleven distortion types, and all explanation patterns, the advisory board finds:

**The framework philosophy is defensible.**
Structural-first scoring (processing level, ingredient quality, additive load) is a legitimate approach to food quality assessment. It is not the only defensible approach, but it is a coherent one. The alternative — scoring primarily on macronutrient profile — would produce different results that are also defensible but not obviously more correct.

**The relative rankings within snacks are broadly correct.**
The ordering of snacks products (date bars at top, confectionery at bottom, processed protein bars in the middle) reflects real food quality differences. A consumer who follows these rankings will, on average, make better snack choices than one who ignores them. The system is not producing noise — it is producing signal.

**But four specific failures are serious enough to require revision.**

---

## The Four Specific Failures

### Failure 1: Zero nutritional data in snacks — the most urgent problem

All 18 snack products have null nutritional data AND null ingredient strings in the scoring system, despite BSIP0 capturing ingredients.html and nutrition.html for most products in `observations_bsip0/yohananof/`. The data exists. It was not ingested.

This means every snack score is a structural inference, not a nutritional fact. The system correctly labels most products as "partial" confidence, but snk-001, snk-002, snk-003, snk-005, snk-009, snk-010, snk-013, snk-015, snk-017, snk-018, snk-019 are labeled "verified" — which is incorrect. They have verified structural metadata but not verified nutritional content. The confidence labeling is misleading.

**This is not a scoring system flaw — it is a data pipeline flaw. It must be fixed before the snacks shelf is credible.**

### Failure 2: Mean convergence creates a credibility problem

Snacks (43.50) and maadanim (43.78) produce nearly identical average scores. This is defensible in theory — both categories are dominated by processed retail products — but not credible in practice. A date bar and a chocolate pudding existing in the same average quality band is not believable to a consumer or a journalist. This undermines confidence in the scoring engine's category sensitivity.

**The cause is the universal cap architecture creating mean convergence. The fix is category-specific caps.**

### Failure 3: False precision in the D-band

Eight products cluster in the 39–47 range (an 8-point spread). Within this band, micro-gaps of 1–2 points between near-identical products (snk-011/012 at 43/42; snk-009/010 at 47/45) appear as meaningful distinctions but are not. The system is producing scoring artifacts that will not survive scrutiny.

**The fix is a minimum sibling gap rule (≥5 points required between products with <2 structural differences).**

### Failure 4: The Date Sugar Halo is unhandled

The top of the snacks ranking is dominated by date bars (snk-001 at 70/B, snk-002 at 56/C, snk-015 at 55/C). Date bars receive their scores because they have minimal ingredient counts and whole-food bases. But dates are 60–70% simple sugars. A product that is primarily compressed dates has roughly the same glycemic impact as many products Bari penalizes for "high sugar" — but receives no sugar-related penalty because the sugar source is "natural."

The framework explicitly chooses not to penalize natural sugars at high concentrations. This is a philosophy choice, not a scoring error. But it must be disclosed explicitly: "Bari rewards structural simplicity. Products with high natural sugar concentrations (dates, honey) score well on structural grounds. If sugar intake is your concern, the sugar content of these products should inform your decision separately."

**Without this disclosure, the 70/B date bar is misleading to a consumer with diabetic concerns.**

---

## What Should Survive Unchanged

**The structural-first philosophy:** Processing level as the primary quality determinant is a coherent, defensible orientation for a consumer food intelligence tool. It correctly identifies the gap between marketing language and actual composition. It is the correct lens for a tool like Bari.

**The marketing divergence finding:** The fitness halo, the natural halo, the wellness halo — the current system's ability to identify when a product's marketing language contradicts its compositional reality is Bari's strongest capability. This should not change.

**The relative rankings:** Within each category, the ranking order is broadly correct. The products that should score higher do score higher. The ordering system works; the absolute calibration needs adjustment.

**The four-layer architecture:** Structural/Nutritional/Metabolic/Engineering is a sound design. The issue is that two of the four layers (Nutritional and Metabolic) are not active for snacks due to missing data.

---

## What Must Change

**1. Nutritional data ingestion for snacks (URGENT)**  
Parse the BSIP0 HTML files for the 18 displayed products. This is not an architectural change — it is a data pipeline completion task. The data exists in `observations_bsip0/yohananof/[barcode]/nutrition.html` and `ingredients.html`. Once parsed, approximately 30–40% of scores will shift (within ±8 points) as the nutritional layer activates.

**2. Category-specific caps (MODERATE URGENCY)**  
Replace universal caps (68, 55, 60) with category-specific variants. Snacks should have a natural-sugar exception for date-based products. This breaks the mean convergence without requiring a full rebuild.

**3. Confidence labeling correction (URGENT)**  
Products labeled "verified" without nutritional data should be relabeled "partial" until nutritional data is confirmed. The misleading confidence labels are a governance violation.

**4. Minimum sibling gap enforcement (LOW URGENCY)**  
Products with <2 structural differences cannot be scored within 1–2 points of each other. Either assign the same score or enforce a 5-point minimum gap with a documented mechanism.

**5. Date Sugar Halo disclosure (MODERATE URGENCY)**  
Add a methodology disclosure: "ציוני Bari מתגמלים בסיס מרכיבים נקי. מוצרי תמרים ודבש מקבלים ציון גבוה על בסיס פשטות הרכב — לא על בסיס תכולת סוכר כוללת."

---

## What Should NOT Change

- Do not introduce percentile-based scoring (Option C). Bari's identity is absolute quality judgment.
- Do not penalize natural sugars equally to refined sugars at equivalent concentrations. The structural distinction between dates and HFCS is real and matters. The current philosophy is correct — but needs disclosure.
- Do not rebuild the entire system before completing the nutritional data pipeline. Option A fixes are the right scope.
- Do not stop publishing snacks scores. The current rankings are directionally correct and are better than nothing. Add the data gap disclosure and continue.

---

## Verdict Summary

| Component | Verdict |
|---|---|
| Core philosophy (structural-first) | KEEP |
| Four-layer architecture | KEEP |
| Marketing divergence detection | KEEP |
| Relative rankings within category | KEEP (minor adjustments after data ingestion) |
| Universal caps | MODIFY → category-specific |
| Confidence labeling | FIX (snacks verified → partial until nutrition confirmed) |
| Grade boundaries | MODIFY → category-specific thresholds |
| Explanation engine | REBUILD (separate sprint, see explanation engine review) |
| Nutritional data ingestion | COMPLETE (urgent data pipeline work, not scoring work) |
| Date Sugar Halo handling | DISCLOSE (add methodology note, do not change scores) |
| Sibling gap precision | FIX (minimum 5-point gap rule) |

**Overall system verdict: MODERATE REVISION.**

The system is not broken. It is producing real signal. But it has four specific failures — two urgent (data pipeline, confidence labels) and two moderate (universal caps, date sugar disclosure) — that must be addressed before the snacks comparison is fully credible and before further category rollout.

The scoring philosophy should remain unchanged. The calibration should be improved. The explanation engine needs a full rebuild as a separate sprint.

---

## Sequencing

**Immediate (this week):**
1. Fix confidence labels: relabel 11 "verified" snack products to "partial" until nutrition.html is parsed
2. Parse BSIP0 HTML files for top-10 most impactful snack products (start with snk-001, snk-005, snk-009, snk-013 — the ones where nutritional data would most change the story)
3. Add date sugar disclosure to snacks methodology

**Short-term (2–4 weeks):**
4. Implement category-specific caps (snacks first, maadanim second)
5. Implement category-specific grade boundaries
6. Add minimum sibling gap rule
7. Complete nutritional data ingestion for all 18 displayed snacks

**Medium-term (4–8 weeks):**
8. Rebuild explanation engine per `snacks_explanation_engine_review_v1.md`
9. Recalibrate all 18 snack scores after nutritional data ingestion
10. Re-publish snacks shelf with updated scores and updated explanations

**Do not start new category rollout (milk, yogurt) until nutritional data pipeline is confirmed working for snacks.**
