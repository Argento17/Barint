# Universal Caps Review v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Cap Architecture Challenge  
**Prior theory:** Universal caps at 68/55/60 force processed-food categories toward similar means.  
**Finding:** This theory is disproven by the data.

---

## The Cap Architecture

From `bsip2_guardrails.py` and `bsip2_config.py`:

| Rule | Type | Value | Family | Trigger |
|---|---|---|---|---|
| NOVA_PROXY_4_ULTRA_PROCESSED | cap | 60 | processing | nova_proxy == 4 |
| NOVA_PROXY_3_PROCESSED | cap | 75 | processing | nova_proxy == 3 |
| ISRAELI_RED_LABELS_2_PLUS | cap | 45 | regulatory | red_labels >= 2 |
| ISRAELI_RED_LABEL_1 | cap | 55 | regulatory | red_labels == 1 |
| SWEETENER_PRESENT | cap | 70 | additives | artificial sweetener present |
| ADDITIVE_MARKERS_5_PLUS | cap | 55 | additives | additive count >= 5 |
| ADDITIVE_MARKERS_3_PLUS | cap | 65 | additives | additive count 3–4 |
| HIGH_SUGAR_25G_PLUS | cap | 60 | sugar | sugars >= 25g/100g |
| HIGH_SODIUM_700MG_PLUS | cap | 60 | sodium | sodium >= 700mg |

Penalty families also have cap floors:
- processing: floor 55 (caps can't go below 55 within family)
- additives: floor 55
- sugar: floor 45
- hyper_palatability: floor 50

---

## Testing the Theory: Are Caps Forcing Mean Convergence?

**For caps to force mean convergence between categories, they would need to be BINDING — i.e., they would need to be the constraint that determines the final score. If natural dimension scoring already produces scores below the cap level, the caps are irrelevant.**

### Snacks corpus cap binding test

From the BSIP2 synthesis data (53 products):

| NOVA class | N | Max score | Relevant cap | Cap binding? |
|---|---|---|---|---|
| NOVA 2 | 7 | 70.0 | 75 (NOVA3, not applicable) | N/A |
| NOVA 3 | 15 | 62.2 | 75 | **No** (62.2 < 75) |
| NOVA 4 | 31 | 47.4 | 60 | **No** (47.4 < 60) |

**The NOVA4 cap at 60 is not binding for any of the 31 NOVA4 snack products.** The maximum NOVA4 score (47.4) is 12.6 points below the cap. The cap would need to be reduced to 47 before it becomes binding.

**The NOVA3 cap at 75 is not binding for any of the 15 NOVA3 snack products.** The maximum NOVA3 score (62.2) is 12.8 points below the cap.

Products scoring above 60: only 2 of 53 (3.8%) — both are NOVA2 or NOVA3 products, and their scores (62.2 and 70.0) are below the relevant cap values.

**Conclusion: The universal cap architecture is not compressing the snacks distribution.** The caps are acting as safety nets that are rarely triggered, not as mean-anchoring constraints.

---

## Why Scores Are Low Without Cap Intervention

The scoring engine produces naturally low scores for processed snack bars because the DIMENSION CALCULATIONS themselves penalize these products heavily. The caps are redundant constraints for snacks — the multi-dimensional scoring gets there first.

### Decomposition of a typical NOVA4 snack bar (estimated)

Using the dimension weights and parameters from `bsip2_config.py` and `bsip2_dimensions.py`:

| Dimension | Weight | Typical Score | Contribution | Why |
|---|---|---|---|---|
| processing_quality | 0.18 | ~48 | 8.6 | -24 (NOVA4), -8 (glucose syrup), -6 (flavouring), -6 (emulsifier) |
| nutrient_density | 0.16 | ~38 | 6.1 | High sugar penalty overwhelms low protein benefit |
| calorie_density_quality | 0.12 | ~40 | 4.8 | snack_bar_granola tier: 430kcal → score 40 |
| glycemic_quality | 0.11 | ~48 | 5.3 | Sugar 28g: -(28-5)×1.4 = -32 penalty off base 80 |
| hyper_palatability | 0.10 | ~72 | 7.2 | One HP combo triggered |
| protein_quality | 0.09 | ~53 | 4.8 | Low protein (4g) gives moderate score |
| additive_quality | 0.07 | ~30 | 2.1 | 5 markers × 12 = 60 penalty off base 90 |
| satiety_support | 0.06 | ~48 | 2.9 | Low protein + fiber, high sugar |
| fat_quality | 0.06 | ~62 | 3.7 | Seed oil present: -8 |
| regulatory_quality | 0.04 | ~100 | 4.0 | Assuming no red labels |
| whole_food_integrity | 0.01 | ~22 | 0.2 | NOVA4 + syrup + coating penalties |
| **BASE TOTAL** | 1.00 | | **~49.7** | |

A typical NOVA4 snack bar naturally scores ~50 from dimension calculation alone — BEFORE any cap is applied. With additional penalties (multiple HP combos, more additives, sugar above threshold), scores fall further into the 25–45 range. The 60 cap is irrelevant.

### What would make the cap binding?

The NOVA4 cap at 60 would only become binding if:
- A NOVA4 product had high protein (>12g, boosting nutrient_density and protein_quality)
- AND low sugar (<10g, removing glycemic penalties)
- AND few additives (only 1–2 markers, high additive_quality)
- AND no HP combos triggered

This is theoretically possible (e.g., a high-protein, low-sugar NOVA4 bar with minimal additives) but does not exist in the yochananof snack corpus.

---

## Does the Cap Architecture Produce Cross-Category Compression?

**Test: Maadanim**

Maadanim products score between 27 and 70. Their constraint pattern differs from snacks:
- Many maadanim products carry Israeli red labels (2+ labels → cap at 45)
- The 2-red-label cap IS binding for some maadanim products (milky-type products below 45)
- NOVA4 cap at 60: likely binding for some highly processed dairy desserts

For maadanim, the cap architecture IS doing meaningful work — the regulatory cap at 45 for 2+ red labels is the primary constraint for the worst products. For snacks, no equivalent cap bites.

**This means the cap architecture actually creates asymmetric behavior:** Caps compress maadanim's top from further downward but don't touch snacks' already-low natural scores.

**The cap architecture is NOT creating a shared mean between categories. It is functioning as intended: a safety net for specific regulatory violations.**

---

## The Real Effect of Universal Caps

The caps serve a different function than previously theorized:

1. **NOVA caps are not mean-compressors.** They are upper bounds that prevent a future product with very good nutritional data but poor processing from receiving an inflated score. They don't touch the current corpus.

2. **Regulatory caps (Israeli red labels) DO bite for some products.** Any product with 2+ red labels is capped at 45, regardless of other qualities. This is correct and intentional — the MoH warning system should translate to score boundaries.

3. **Additive caps are redundant for the worst products.** A product with 5+ additive markers already scores ~30 on additive_quality (base 90 - 5×12 = 30). The cap at 55 doesn't touch products that naturally score below 50.

4. **Family floors prevent over-penalization.** The processing family floor at 55 ensures that even a NOVA4 product can't be pushed below 55 from processing-related rules alone. This is anti-pile-on protection.

---

## Should Category-Specific Caps Be Introduced?

**Verdict: Lower priority than previously assessed.**

Category-specific caps would change score distributions only if:
1. The universal caps are currently binding, OR
2. Category-specific rules are needed to prevent misclassification

For snacks: Caps are not binding. Category-specific caps would have no effect on current scores.

The only area where category-specific parameters would help:
- The calorie density tier is already category-specific (`snack_bar_granola` vs `dairy_protein` vs `whole_food_fat`) — this is already implemented.
- Grade boundaries (A/B/C/D/E thresholds) are universal. Making them category-specific would have the largest effect on consumer-facing grade display without requiring scoring changes.

**The most actionable change is category-specific grade thresholds, not category-specific caps.**

For example:
- Snacks C threshold: currently 55 (same as all categories). With typical NOVA3 snacks scoring 47–62, this means most decent-quality granola bars are D. A snacks-specific C threshold of 48 would correctly classify good oat-based bars as C rather than D.
- Maadanim C threshold: could remain 55, since dairy products with protein and low processing can legitimately achieve C+.

---

## Summary

| Claim | Status |
|---|---|
| "Caps force snacks and maadanim toward similar means" | **DISPROVEN** |
| "NOVA4 cap at 60 is binding for snack products" | **DISPROVEN** (max NOVA4 = 47.4) |
| "Universal caps create cross-category convergence" | **DISPROVEN** |
| "Caps are functioning as safety nets, not mean anchors" | **CONFIRMED** |
| "Category-specific caps would significantly change snack rankings" | **UNLIKELY** — caps not binding |
| "Category-specific grade thresholds would improve display" | **CONFIRMED — highest-value change** |
