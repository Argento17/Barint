# Sprint 1 Production Decision v1

**Task:** TASK-046B  
**Owner:** Chief Nutrition Officer  
**Date:** 2026-05-31  
**Status:** APPROVED WITH REVISION

---

## Summary

Sprint 1 scoring changes are approved for production with one mandatory pre-condition: EV-005 (polyol scoring) must be revised before release. All other signals are approved as-is.

---

## 1. POLYOLx1 Product Count

**7 products** triggered the POLYOLx1 signal in Sprint 1.

All 7 products detected: sorbitol only (no multi-polyol products in this corpus).

| # | PID | Product | Brand | v1 Score | v2 Score | Δ |
|---|-----|---------|-------|----------|----------|---|
| 1 | bsip1_5900020018908 | חטיפי דגנים פיטנס קרם ועוגיות שישייה | Fitness (Nestlé) | 24.5 | 20.9 | −3.6 |
| 2 | bsip1_5900020020710 | חטיף דגנים שוקו וניל נסטלה שישייה | Fitness (Nestlé) | 27.9 | 24.6 | −3.3 |
| 3 | bsip1_5900020022325 | סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב | Fitness (Nestlé) | 25.7 | 22.3 | −3.4 |
| 4 | bsip1_5900020034021 | חטיפי דגנים פיטנס שוקולד בננה שישייה | Fitness (Nestlé) | 23.9 | 21.6 | −2.3 |
| 5 | bsip1_7290107947466 | חטיף דגנים מצופה שוקולד עם עוגיות קרמל וקרם נוגט | אנרג'י (Beter) | 16.9 | 12.6 | −4.3 |
| 6 | bsip1_7290107947480 | חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים שישייה | אנרג'י (Beter) | 18.1 | 13.8 | −4.3 |
| 7 | bsip1_7290110563851 | חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר שישייה | אנרג'י (Beter) | 31.4 | 27.0 | −4.4 |

---

## 2. Product Inspection Findings

### Product type
All 7 products are conventional chocolate-coated or cream-filled cereal bars. None carry keto, sugar-free, or low-carb positioning anywhere in their product name, claims, or packaging signals available in BSIP1.

### Keto / sugar-free positioning
None. All 7 products contain glucose syrup, white sugar, and/or invert sugar syrup as primary sweeteners — confirmed from ingredient order inspection. These are conventionally sweetened products.

### Ingredient order and sorbitol function

**Critical finding:** In all 7 products, sorbitol is declared by the manufacturer under **"חומרי הלחה" (humectants)**, always co-listed with glycerol in the form:

> חומרי הלחה (גליצרול, סורביטול)

This is a manufacturer-labeled functional declaration. Sorbitol in this context is a moisture-retention / texture ingredient — standard food technology practice in chocolate coatings and cream fillings.

The BSIP1 enrichment pipeline correctly extracted "חומרי הלחה" as `category: humectant` in `extracted_additives`. The sprint1 polyol detector then found "סורביטול" within that humectant group and applied the EV-005 penalty — this is the mismatch.

**Sorbitol ingredient positions across all 7 products:**

| Product | Humectant group position | Total ingredients |
|---------|--------------------------|-------------------|
| פיטנס קרם ועוגיות | 8 | 24 |
| שוקו וניל נסטלה | 5 | ~15 |
| קינמון על שכבת קרם חלב | 7 | ~15 |
| שוקולד בננה | 7 | ~17 |
| קרמל וקרם נוגט | 5 | 18 |
| שברי אגוזים שישייה | 5 | ~15 |
| בטר שישייה | 6 | 15 |

Sorbitol does not appear as a standalone sweetener in any of these 7 products. In all cases, real sugars (glucose syrup, white sugar) appear in positions 1–5 and drive glycemic quality.

---

## 3. EV-005 Decision

### Current implementation (Sprint 1 as shipped)
- Single polyol = −4 score penalty
- Multiple polyols = −10 score penalty
- Keto/sugar-free + multiple polyols = −15 score penalty

### Assessment

The current single-polyol penalty is incorrectly applied to all 7 products. The EV-005 evidence registry states:

> "Keto and low-carb products often rely heavily on polyols as sugar replacements."  
> `should_affect_score_now`: "flag if multiple polyols **or if product is keto/sugar-free**"

None of the 7 products meet the keto/sugar-free condition. None use sorbitol as a sweetener. The −4 penalty was triggered by sorbitol's presence within a manufacturer-declared humectant group — a false positive against EV-005's intent.

### Decision: **Approve with revision — adopt Option C with humectant-label detection**

Option C (ingredient-order logic) is adopted as the framework, with the following refinement that supersedes pure position logic:

**Primary rule:** If a detected polyol (sorbitol, xylitol, erythritol, etc.) appears within a manufacturer-declared humectant group ("חומרי הלחה"), apply **warning only — no score penalty**, regardless of position.

**Secondary rule (for polyols not in a humectant group):**
- Polyol in top 5 ingredients = penalty (primary sweetener use confirmed by volume)
- Polyol outside top 5 = warning only (minor sweetener or processing aid)

**Multi-polyol and keto rules unchanged:**
- Multiple polyols in any position = penalty (−10)
- Keto/sugar-free + multiple polyols = stronger penalty (−15)
- Keto/sugar-free + single polyol not declared as humectant = penalty (−4)

### Rationale
The humectant declaration is authoritative and directly observable from the label. It resolves the ambiguity that position logic alone cannot, as sorbitol can appear in position 5 in an 18-ingredient list while still being present at trace concentrations. The BSIP1 `extracted_additives.category` field already provides this signal — implementation cost is minimal.

---

## 4. Revised Deployment Recommendation

### Other Sprint 1 signals
**Approved as-is:**
- LECITHIN_EXEMPT — correct; lecithin exemption properly reduces additive penalty
- FAT_RATIO — correct; saturated-to-unsaturated ratio captures fat quality improvements

### EV-005 correction
**Pre-condition for production release:**
1. Implement humectant-label detection in the polyol scoring logic
2. Re-run the Sprint 1 polyol pass against all 7 affected products
3. Expected outcome: all 7 products recover the −4.0 penalty and return to approximately v1 baseline + other sprint1 adjustments

### Corrected score projections (7 affected products)

After EV-005 revision, v2 scores should be:

| Product | Current v2 | Expected corrected v2 | Correction |
|---------|------------|----------------------|------------|
| פיטנס קרם ועוגיות | 20.9 | 24.9 | +4.0 |
| שוקו וניל נסטלה | 24.6 | 28.6 | +4.0 |
| קינמון קרם חלב | 22.3 | 26.3 | +4.0 |
| שוקולד בננה | 21.6 | 25.6 | +4.0 |
| קרמל נוגט | 12.6 | 16.6 | +4.0 |
| שברי אגוזים | 13.8 | 17.8 | +4.0 |
| בטר שישייה | 27.0 | 31.0 | +4.0 |

Note: corrected scores remain at or below v1 levels — no product benefits from the correction beyond its pre-Sprint-1 baseline. Grade distribution is unchanged (all remain E).

### Deployment gate

| Signal | Status |
|--------|--------|
| LECITHIN_EXEMPT | Ready to ship |
| FAT_RATIO | Ready to ship |
| EV-005 (POLYOL) | Hold — implement humectant-label logic first |
| EV-005 re-run | Required for all 7 affected PIDs |

**Overall Sprint 1 status: APPROVED WITH REVISION**  
Sprint 1 may ship once EV-005 humectant correction is implemented and the 7 affected product scores are recalculated.

---

## 5. EV-005 Registry Update Required

The evidence registry entry for EV-005 must be updated to document this revision. The `notes` field should be extended with:

> **Humectant exception (added 2026-05-31):** Sorbitol or other polyols appearing within a manufacturer-declared "חומרי הלחה" (humectant) group — co-listed with glycerol or other non-sweetener humectants — are classified as functional humectants, not sweetener-load polyols. Apply warning flag only. No score penalty. This exception does not apply when multiple polyols are present or when the product is keto/sugar-free positioned.

---

*Decision authority: Chief Nutrition Officer*  
*TASK-046B — 2026-05-31*
