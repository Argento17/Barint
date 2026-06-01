# BSIP2 Hummus — Post-Run Review

**Run:** run_hummus_001  
**Date:** 2026-05-31  
**Owner:** Frontend Architect  
**Category:** Hummus and Savory Dips (69 products — Shufersal corpus)  
**Framework reference:** `C:\Bari\03_operations\bsip2\hummus_review_framework_v1.md`  
**Run report:** `C:\Bari\02_products\hummus\reports\run_hummus_001_batch_summary.md`  
**BSIP2 version:** proto_v0 (unmodified)  
**Rules observed:** No score tuning. No BSIP2 logic changes. No BSIP1 record modification. No fat patching.

> **Known limitation:** fat_quality dimension may be unreliable for 58/69 products due to confirmed Shufersal fat-row scraping defect identified in TASK-039.

---

## Run Statistics

| Metric | Value |
|--------|-------|
| Products processed | 69 |
| Scored (sufficient data) | 67 |
| Insufficient data | 2 |
| Pipeline errors | 0 |
| Score mean | 65.1 |
| Score median | 64.5 |
| Score std dev | 9.5 |
| Score range | 42.8 – 85 |

---

## Section 1 — Does BSIP2 Generally Behave as Expected?

### Answer: Partially. The scoring pipeline ran cleanly, but a critical category routing error invalidates the calorie_density dimension for 44 of 69 products.

**What worked:**

- All 69 products processed without pipeline errors.
- NOVA inference behaved as expected: 59 products at NOVA 3, 6 at NOVA 1 (products with no ingredient data, correctly inferred as minimally processed), 4 at NOVA 2. Zero NOVA 4 — appropriate for this corpus; no ultra-processed formulations were detected.
- The SRC-04 structural emptiness gate handled the fat anomaly correctly: products with `fat_g < 0.5` returned `fat_quality = 50.0` (neutral), preventing the feared systematic inflation of fat_quality scores.
- Guardrail activity was coherent: the NOVA_PROXY_3_PROCESSED cap (68 ceiling) fired on 59 products, acting as the dominant structural constraint for the corpus. The sodium cap fired on 4 products, consistent with the 600mg+ sodium products identified in the framework.
- Additive penalties were moderate (`additive_quality` avg 72.1), not catastrophic — despite the raising_agent inflation concern (FM-2), the dimension did not score below 40 for any product.
- Grade A awarded only to NOVA 1 products with minimal data (floor-driven), which is mechanistically consistent. Grade D awarded to 5 low-complexity vegetable spreads.
- No trans fat vetoes, no structural emptiness gates firing (hummus products are calorie-dense).

**What did not work:**

The most significant deviation from expected behavior is **category router misfire**: 44 of 69 products were routed to the `dessert` category instead of `sauce_spread`. This is a confirmed routing error.

| Category | Count | Expected |
|----------|-------|---------|
| dessert | 44 | ~0 |
| default | 15 | ~0 |
| sauce_spread | 3 | ~69 |
| whole_food_fat | 7 | ~0 |

The `sauce_spread` calorie density table is the intended route for hummus products. The `dessert` table penalizes the 150–300 kcal range (normal for hummus) significantly more than `sauce_spread`:

| kcal/100g | sauce_spread score | dessert score | Difference |
|-----------|-------------------|---------------|------------|
| 150 | 90 | 85 | −5 |
| 250 | 75 | 70 | −5 |
| 300 | 75 | 55 | −20 |
| 380 | 60 | 40 | −20 |

Products scored with the dessert table at 200–300 kcal lost approximately 10–20 points on `calorie_density` (weight 15%) — a systematic underscoring of ~1.5–3.0 final score points per product. Across 44 products, this is a corpus-wide suppression of approximately 2–3 points on average.

**The routing misfire mechanism:** The router in `router_v2.py` likely fires on the high carbohydrate and energy content of the hummus BSIP1 data (64.2g carbs, 380 kcal for a dry chickpea product; 11–20g carbs, 130–280 kcal for standard hummus spreads). Without the word-based savory routing signals — "חומוס", "טחינה" — or ingredient text to trigger the sauce_spread pathway, the router defaults to dessert based on macronutrient profile. This is a router calibration issue, not a scoring engine issue.

---

## Section 2 — Grade Distribution vs. Framework Expectation

| Grade | Observed | Expected (framework) | Deviation |
|-------|----------|----------------------|-----------|
| A (85–100) | 6 | 5–10 | Within range |
| B (70–84) | 25 | 20–28 | Within range |
| C (55–69) | 31 | 20–25 | Over by 6–11 |
| D (40–54) | 5 | 10–15 | Under by 5–10 |
| E (0–39) | 0 | 2–5 | Missing entirely |

The distribution is **compressed upward** relative to expectations:
- Too many products in C (31 vs. expected 20–25)
- Too few in D (5 vs. expected 10–15)
- None in E (0 vs. expected 2–5)

**Primary cause:** The NOVA_PROXY_3_PROCESSED cap (68) acts as a soft ceiling for the majority of the corpus. Products that should reach D or E via additive load and poor nutrition are capped at 68 before the processing cap brings them down further, but not below 40. The expected D–E products (heavily reconstructed hummus with gums, preservatives, multi-oil sources) scored C (55–65) rather than D–E because:

1. The additive_quality dimension penalizes 1–6 categories but does not push total scores below 55 for products with moderate nutrition
2. The sodium cap (4 products at >700mg) further suppressed scores, but still not into E territory
3. No products were detected as ultra-processed (NOVA 4), eliminating the primary route to E grades

**Secondary cause:** The dessert routing suppressed C–D products modestly, but also boosted a few of the bottom products past what they would score under correct `sauce_spread` routing (matbucha at 40–80 kcal would score 90 on sauce_spread calorie_density, likely lifting them into B from C).

---

## Section 3 — Top 10 Analysis vs. Expected Archetypes

### Actual top 10:

| Rank | Product | Score | Grade | NOVA | Category | Notes |
|------|---------|-------|-------|------|----------|-------|
| 1–6 | חומוס ענק/גדול/לבן/מוקפא/חומוס | 85 | A | 1 | dessert | Floor applied — no ingredient data |
| 7 | חומוס שלם יכין | 79.9 | B | 3 | sauce_spread | Dry chickpeas, no tahini |
| 8 | הקיסר חומוס ענק | 79.7 | B | 3 | dessert | Short ingredient list |
| 9 | סלט חומוס | 79.4 | B | 3 | dessert | Compact ingredients, high protein |
| 10 | חומוס עשיר ב40% טחינה | 72.8 | B | 3 | whole_food_fat | 40% tahini, correctly routed |

**Framework Archetype A (Traditional 3–6 ingredient hummus) — PARTIALLY MATCHED**

The 6 grade-A products are all Shufersal own-brand bulk hummus variants (חומוס ענק — "giant hummus," חומוס לבן ענק — "giant white hummus," frozen hummus). These scored 85 because:
- No ingredient data → NOVA 1 inferred → SRC-01 floor applied at 85
- This is a data artifact, not a genuine structural signal

A product with missing ingredient data reaching grade A via floor is **not the intended behavior for Archetype A**. The framework expected traditional 3–6 ingredient hummus with named tahini to reach A organically via high `additive_quality`, high `processing_quality`, and clean `whole_food_integrity`. Instead, the A grades went to no-data products via floor.

The genuinely high-quality traditional products — "מלך החומוס אבו מרוואן" (King of Hummus), "חומוס אבו גוש," "חומוס אסלי" — scored B (62–67), not A. The framework's Archetype A expectation was **not matched** for these named traditional products.

**Framework Archetype C (Simple eggplant spread) — NOT MATCHED**

No eggplant spread appeared in the top 10. The best eggplant spread scored 61.6 ("סלט חצילים על האש"). This is the opposite of the framework's prediction — FM-6 (eggplant/matbucha scoring high due to calorie density bonus) did **not** fire. Instead, matbucha and eggplant spreads clustered in the lower half (avg 56.8 and 57.4). This is explained by the routing error: these products routed to `default` instead of `sauce_spread`, denying them the calorie density bonus that would have lifted them.

**Framework Archetype D (Traditional matbucha) — NOT MATCHED**

Matbucha avg: 57.4. Framework expected high-B. Same routing cause.

**Verdict on top archetypes:** The top 10 matches the letter of expectation (6 grade-A, 4 high-B) but not the spirit. The A grades are floor-driven data artifacts, not earned quality signals.

---

## Section 4 — Bottom 10 Analysis vs. Expected Archetypes

### Actual bottom 10:

| Rank | Product | Score | Grade | Type | Notes |
|------|---------|-------|-------|------|-------|
| 1 | ממרח פלפלים קלויים | 42.8 | D | Pepper spread | Routing instability |
| 2 | ממרח פלפלים קלויים | 48.0 | D | Pepper spread | Whole_food_fat routing |
| 3 | מטבוחה אמיתית | 48.7 | D | Matbucha | Default routing |
| 4 | מטבוחה חריפה | 49.6 | D | Matbucha | Default routing |
| 5 | פלפל צ'ומה | 49.6 | D | Pepper spread | Default routing |
| 6–7 | מטבוחה פיקנטית / מטבוחה פיקנטי | 52.0 | C | Matbucha | Low satiety score |
| 8 | חציל על האש בטחינה | 52.2 | C | Eggplant+tahini | whole_food_fat, ADDITIVE_MARKERS_3_PLUS cap |
| 9 | סלט חציל בטעם כבד | 55.3 | C | Liver-flavor eggplant | dessert routing |
| 10 | סלט חציל פיקנטי | 56.4 | C | Eggplant | Default routing |

**Framework Archetype X (Industrially Reconstructed Hummus) — NOT IN BOTTOM 10**

No hummus spread appears in the bottom 10. The framework predicted heavily reconstructed hummus products (10–15 ingredients, multiple gums, preservatives) would anchor grades C–D. Instead, the bottom is entirely occupied by matbucha, pepper spreads, and eggplant products.

This is counterintuitive and likely reflects two interacting effects:
1. **Routing advantage for hummus:** Most hummus products routed to `dessert`, which gave moderate calorie_density scores (55–75 range). If they had routed to `sauce_spread`, their calorie_density would have been 75–90, actually helping them score higher. The mismatch accidentally partially compensates.
2. **Routing penalty for matbucha:** Matbucha products routed to `default`, which applies the generic calorie density table. At 60–100 kcal, the default table gives 80–90, but with NOVA 3 cap at 68 and additive penalties, these products still fall into D territory. Under `sauce_spread` routing, these products would score 90 on calorie_density and would likely reach B–C.

**FM-4 (Missing high-quality traditional products) — CONFIRMED ACTIVE**

Premium artisanal products scored B (62–67), not A:
- "מלך החומוס אבו מרוואן" (King of Hummus Abu Marwan): 62.2 C
- "חומוס אבו גוש": 66.9 B
- "חומוס אסלי": 67.6 B
- "חומוס אבו מרוואן 26% טחינה": 67.4 B

These products with declared tahini percentages (15–26%) and shorter ingredient lists should be in A territory per the framework. The NOVA 3 cap at 68 is the primary constraint — even a perfect traditional hummus with 5 ingredients scores at most 68 via the cap unless the floor overrides. FM-4 is active.

**FM-5 (Protein-enriched hummus scored too favorably) — NOT CONFIRMED**

"חומוס עשיר ב40% טחינה" (40% tahini enriched) scored 72.8 B — rank 10. This is NOT inflated relative to traditional hummus. In fact, it is within 5 points of other high-quality products. FM-5 did not fire — the protein_quality dimension does not appear to be rewarding this product disproportionately.

**"סלט חציל בטעם כבד" (liver-flavored eggplant) — FM PARTIAL**

Scored 55.3 C (rank 9 from bottom). The framework predicted this product should score poorly due to the `has_flavor_descriptor` signal. It did score near the bottom, but for routing reasons (dessert calorie table penalizes low-calorie eggplant), not because the flavor descriptor was specifically penalized. The mechanism that produced the low score was correct; the reason behind it was not the expected one.

---

## Section 5 — FM-1 through FM-6 Evaluation

| Failure Mode | Status | Observed Evidence |
|---|---|---|
| **FM-1** (Rewarding low-fat / low-tahini hummus) | **NOT FIRED** | The SRC-04 gate returned fat_quality=50.0 (neutral) for products with fat<0.5g. No inflation — neutral contribution only. |
| **FM-2** (Sodium bicarbonate additive inflation) | **MILD — not severe** | additive_quality avg 72.1. Products with 3+ additive categories received ADDITIVE_MARKERS_3_PLUS cap at 72, but most products with raising_agent signals scored 64–82 on additive_quality. Inflation is present but absorbed by other dimension constraints. |
| **FM-3** (Over-penalizing natural sesame fat) | **NOT APPLICABLE** | Fat data is corrupt for 58/69 products. The SE gate neutralized the dimension entirely. Cannot evaluate FM-3 until fat data is corrected. |
| **FM-4** (Missing high-quality traditional products) | **CONFIRMED** | Traditional hummus products with declared tahini (15–26%) scored B (62–68), not A. The NOVA 3 cap at 68 is the primary constraint; these products cannot reach A without the NOVA 1/2 floor. |
| **FM-5** (Protein-enriched hummus scored too favorably) | **NOT CONFIRMED** | The 40% tahini product scored 72.8 (rank 10), not inflated versus its ingredient complexity. protein_quality is not systematically inflating enriched products. |
| **FM-6** (Calorie density misfire on matbucha/eggplant) | **INVERTED** | Matbucha and eggplant did NOT score high — they scored low (avg 48–57). The routing error sent them to `default` category, denying them the calorie_density bonus. FM-6 would have fired under correct routing; it is masked by the routing error. |

**Additional failure mode not in framework:**

**FM-7 (Unobserved) — Category router misfire:** 44/69 products routed to `dessert`. This is the single highest-impact unobserved failure in this run. It systematically suppresses scores for products with high carbohydrate content and no disambiguating savory ingredient keywords. This is not a BSIP2 scoring error — it is a router calibration gap that must be resolved before the run is re-executed.

---

## Section 6 — Suspicious Outputs

The following outputs warrant investigation before any conclusions are drawn:

### S1 — NOVA 1 Floor Override (6 products, grade A = 85)

Products: חומוס ענק, חומוס לבן ענק שופרסל, חומוס גדול שופרסל, חומוס מוקפא, חומוס, חומוס ענק (7296073733331)

All have missing ingredient data (`ingredients_list = []`). The engine inferred NOVA 1 (no additive or processing signals) and the SRC-01 floor raised scores to 85. Weighted dimension scores before the floor: 72–85 (two products had high dimension scores organically; four had 72–78 before the floor).

**Why suspicious:** A score of 85 implies grade A quality, but these products have no structural evidence — no ingredient list, no additive check, no whole_food_integrity evidence beyond NOVA inference. The floor is technically correct per SRC-01 (NOVA 1 = unprocessed food, floor protects it from calibration gaps), but for missing-data products, it produces a score that should be flagged as data-quality-contingent, not genuine.

**Recommendation:** For these 6 products, mark the grade as "data_conditional" pending ingredient verification. The score of 85 should not be displayed to users.

### S2 — Dessert Category for Hummus (44 products)

All hummus, matbucha, and eggplant products should route to `sauce_spread`. The `dessert` routing penalizes these products on `calorie_density`. Products that should score 75–90 on calorie_density under sauce_spread scored 55–70 under dessert.

**Mechanism:** The router appears to lack keyword anchors for savory spread classification. Products with no ingredient text and high carbs route to `dessert` by default.

**Impact on scores:** Approximately −2 to −3 final score points on average for 44 products. The effect is meaningful but not catastrophic because the NOVA 3 cap (68) is the dominant constraint for most products — calorie_density is partially capped anyway.

### S3 — "מלך החומוס אבו מרוואן" scored C (62.2)

Product: "King of Hummus Abu Marwan" — a premium artisanal brand. Scored C, which would display to users as below-average. The product has a declared ingredient list that includes chickpeas, tahini, and minimal additives. This is a classic Archetype A candidate that scored C due to:
- NOVA 3 inferred (has acidity regulators → not NOVA 1/2)
- NOVA 3 cap of 68 applies
- Dessert routing suppresses calorie_density
- Penalty applied for ingredient count / additive markers

This output is counterintuitive for users who recognize this brand as a quality product.

### S4 — Two products scored 50 (insufficient_data)

Products: bsip1_7296073733317 and bsip1_7296073733348. Both received `grade = insufficient_data`. These products lack sufficient nutrition data for confident scoring. The 50-point display score is a placeholder. These should be excluded from any grade comparisons.

### S5 — Nutrient density avg = 27.5 (very low)

The `nutrient_density` dimension averaged 27.5 across the corpus — the lowest of all dimensions. This reflects the protein/fiber breakpoint calibration: 7–9g protein (normal for hummus) scores ~30–40 on protein density, not 60+. The dimension rewards high-protein categories (dairy, legume concentrates) more than hummus's natural protein contribution. This is a calibration issue for category-level expectation, not a data error.

---

## Section 7 — Did the Fat Anomaly Materially Distort Results?

### Answer: Less than feared. The impact was effectively neutralized by the SRC-04 gate.

**Finding:** The engine's existing rule — `if fat_g < 0.5: return 50.0 (neutral)` — acted as a de facto corrective mechanism for the fat anomaly. Products with `fat_g = 0.5` (the corrupt value from the scraper) triggered this gate and received `fat_quality = 50.0` instead of either:
- An inflated score (as FM-1 predicted) — this did NOT happen
- A penalized score (from incorrect saturated fat fraction) — this also did NOT happen

**Quantitative impact:**

| Scenario | fat_quality score | Contribution to final (weight=8%) |
|----------|------------------|------------------------------------|
| Actual (corrupt → neutral gate) | 50.0 | 4.0 |
| If corrected for tahini fat (genuine unsaturated) | ~70–80 | 5.6–6.4 |
| If FM-1 had fired (low fat rewarded) | ~85–95 | 6.8–7.6 |

The actual neutral contribution (4.0) is close to what a corrected run would produce (5.6–6.4). The fat anomaly cost ~1–2 final score points for products that should have scored well on fat_quality. This is not material.

**The 5 products with correct fat data** (NONE severity) scored normally on fat_quality. The dimension did not malfunction for these products.

**Conclusion on fat anomaly:** The fat anomaly did not materially distort grade distributions or comparisons. The SRC-04 gate provided an accidental but effective workaround. The TASK-039 decision to proceed with warning was validated — the warning was appropriate, and the run is still interpretable.

The fat anomaly should still be corrected before any re-run, because:
1. Products with declared tahini percentages (15–40%) should show fat_quality scores that reflect their actual quality
2. The current neutral 50 understates the quality advantage of tahini-based fat versus reconstructed oils
3. Comparative analysis across categories will be misleading if hummus products always show neutral fat_quality while other categories show genuine fat_quality variance

---

## Section 8 — Is BSIP2 Ready for Wave 2 Categories?

### Answer: Conditionally yes — with one blocking issue and two advisories.

**Blocking issue — Category router:**

The router misclassified 44/69 hummus products as `dessert`. This is not acceptable for a production scoring run or for any category where the router lacks sufficient keyword anchors. Before Wave 2:

1. **Fix:** Add explicit keyword anchors for savory spread categories in `router_v2.py`. Keywords like "חומוס," "טחינה," "מטבוחה," "חציל," "פלפל ממרח" should trigger `sauce_spread` or a dedicated `savory_spread` archetype.
2. **Verify:** Re-run the hummus corpus after router fix and confirm routing distribution approaches 65+/69 to `sauce_spread`.
3. **Do not deploy scores to users** from run_hummus_001 with the dessert-routing error unresolved.

**Advisory 1 — NOVA 1 floor on missing-data products:**

Six products scored grade A via SRC-01 floor. These products have no ingredient data. The floor is working as designed, but the output is misleading. Consider adding a flag to grade A products where the floor was the primary driver of the score and data is insufficient — to prevent these from displaying as genuine quality endorsements.

**Advisory 2 — Nutrient density calibration for legumes:**

The `nutrient_density` and `protein_quality` dimensions score hummus low (avg 27.5 and 35.3). This is because the protein breakpoints were calibrated for high-protein categories. A hummus product with 8g protein and 5g fiber — genuinely good nutritional density for a spread — scores ~35 on nutrient_density. The framework notes this as a calibration concern, not an error. CNO ruling recommended before deploying hummus scores.

**Wave 2 readiness for other categories:**

BSIP2 proto_v0 is mechanistically sound:
- Signal extraction: working correctly
- NOVA inference: appropriate
- Guardrail application: logical and traceable
- Confidence scoring: appropriate (confidence reductions for missing data correctly applied)
- Dimension scoring: functioning, pending category-specific calibration
- Floor/cap hierarchy: operating correctly

The hummus run confirmed the engine works end-to-end without crashes, data errors, or logic failures. The issues found are calibration and routing issues — both fixable without changes to the core scoring contract.

---

## Section 9 — Recommended Actions Before Re-Run or Wave 2

| Priority | Action | Owner | Blocker? |
|----------|--------|-------|----------|
| **P0** | Fix router_v2.py: add sauce_spread/savory_spread keyword anchors for Hebrew savory spread terms | Backend/Router | Yes — blocks re-run |
| **P1** | Re-run hummus_001 after router fix to establish corrected baseline | Frontend Architect | Yes — required before publishing scores |
| **P1** | Correct fat_g values per TASK-039 before re-run (or accept neutral fat_quality for this corpus) | QA | Advisory |
| **P2** | Flag NOVA 1 floor-driven grade A products as "data_conditional" in grade output | Backend | No |
| **P2** | CNO ruling on nutrient_density breakpoints for legume-based spreads | CNO | Before user-facing scores |
| **P3** | Evaluate whether raising_agent category should be excluded or down-weighted in sauce_spread archetype | CNO | No |

---

## Summary

| Question | Answer |
|----------|--------|
| Does BSIP2 generally behave as expected? | Partially. Scoring pipeline is functional. Category routing misfired on 44/69 products, which is the primary distortion in this run. |
| Which outputs appear suspicious? | All 44 products routed to `dessert`; the 6 grade-A products with missing data that scored via floor; "מלך החומוס" at C; 2 insufficient_data products at score 50. |
| Did the fat anomaly materially distort results? | No. The SRC-04 neutral gate effectively contained the anomaly. Impact was ~1–2 points per product at most. The decision to run with warning (TASK-039) was correct. |
| Is BSIP2 ready for Wave 2? | Conditionally yes, pending router fix. The core engine is sound. The routing layer requires calibration before hummus scores are valid or before Wave 2 categories with similar routing ambiguity are processed. |

---

*Post-run review — run_hummus_001 — 2026-05-31*  
*Owner: Frontend Architect*  
*Framework reference: hummus_review_framework_v1.md (TASK-038)*  
*BSIP2 proto_v0 — Observe reality before scoring adjustments. This document records what was found.*
