# Penalty Pressure Analysis — Current Scoring Architecture

**Status:** Recalibration evidence  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Sources:** constants.py, score_engine.py, run_003 traces, snack_bar latest_review  
**Companion:** distribution_analysis.md, recalibration_proposals.md

---

## Purpose

This document quantifies how much score compression each mechanism produces, and where that compression is disproportionate to the actual structural concern. The goal is not to identify penalties to remove — it is to identify penalties that fire with cliff-like behavior where smooth gradients are architecturally more honest.

All values are derived from actual scored products and the live constants in constants.py.

---

## Mechanism 1: NOVA Dimension Score Cliffs

### How NOVA affects dimension scores

NOVA feeds two dimensions directly:
- `processing_quality` (weight: 0.15): NOVA_PROCESSING_SCORES = {1:95, 2:80, 3:55, 4:25}
- `whole_food_integrity` (weight: 0.04): NOVA_WFI_SCORES = {1:100, 2:80, 3:50, 4:20}

### Dimension score drops at each NOVA transition

| Transition | processing_quality | WFI | Weighted impact |
|-----------|-------------------|-----|-----------------|
| NOVA 1 → 2 | 95 → 80 (−15) | 100 → 80 (−20) | −2.25 + −0.80 = **−3.05 pts** |
| NOVA 2 → 3 | 80 → 55 (−25) | 80 → 50 (−30) | −3.75 + −1.20 = **−4.95 pts** |
| NOVA 3 → 4 | 55 → 25 (−30) | 50 → 20 (−30) | −4.50 + −1.20 = **−5.70 pts** |

**Observation:** The drops are not uniform. NOVA 2→3 is a larger drop than NOVA 1→2, and NOVA 3→4 is the largest pure dimension drop. But the dimension drops alone are manageable — the real cliff comes from cap interaction (see Mechanism 2).

### The NOVA 3 → 4 cliff (combined effect)

| Source | Effect |
|--------|--------|
| Dimension score drop | −5.70 pts (processing_quality + WFI) |
| Cap change: NOVA3 cap 75 → NOVA4 cap 60 | −15 pts of ceiling headroom |
| **Total effective pressure** | **~−20.7 pts** |

A product crossing from NOVA 3 to NOVA 4 — even if all other signals are identical — experiences approximately **21 points of downward pressure** from NOVA reclassification alone. This is before any other concern signals fire.

**Why this is disproportionate:**  
NOVA 3→4 represents a real structural shift. But a 21-point combined penalty for a product that is barely NOVA 4 (e.g., one solvent extraction step or one processing-specific additive) vs. barely NOVA 3 is not proportional to the actual structural difference. The cliff creates false equivalence between:
- A barely-NOVA-4 product with minimal additives
- A heavily-NOVA-4 product with 5+ additive categories and engineering intent

Both receive the same NOVA4 cap at 60. The barely-NOVA-4 product may deserve 65–68; the heavily-NOVA-4 product may deserve 45. The current system conflates them.

---

## Mechanism 2: Processing Caps (PROCESSING_LOAD family)

### Cap table

| Rule | Condition | Cap value |
|------|-----------|-----------|
| NOVA_PROXY_3_PROCESSED | nova == 3 | 75 |
| NOVA_PROXY_4_ULTRA_PROCESSED | nova == 4 | 60 |
| ADDITIVE_MARKERS_3_PLUS | 3 ≤ additives < 5 | 65 |
| ADDITIVE_MARKERS_5_PLUS | additives ≥ 5 | 55 |

### Binding behavior

When a NOVA 4 product also has 3+ additive categories:
- NOVA4 cap: 60
- ADDITIVE_MARKERS_3_PLUS cap: 65
- Binding cap: **60** (the tighter cap wins)

When a NOVA 4 product has 5+ additive categories:
- NOVA4 cap: 60
- ADDITIVE_MARKERS_5_PLUS cap: 55
- Binding cap: **55**

The ADDITIVE_MARKERS_3_PLUS cap at 65 effectively **has no independent effect** when combined with NOVA 4, since the NOVA4 cap at 60 is always tighter. This means a NOVA 4 product with exactly 3 additives and a NOVA 4 product with 8 additives receive the same effective cap of 55 (from ADDITIVE_MARKERS_5_PLUS) — unless the 3-additive product escapes the 5+ threshold.

**The additive cap system produces meaningful differentiation within NOVA 3 (65 vs. 75) but no differentiation within NOVA 4 for 3–4 additive categories.** Products with 3 and 4 additive categories are both NOVA4-capped at 60.

### How often does the NOVA4 cap bind?

In the milk corpus (run_003), the NOVA4 cap at 60 fires on 4 products:
- Muller protein drink: weighted dim score 47.68 → cap 60 → cap does NOT bind (score already < 60)
- Alpro soy barista: similar non-binding scenario
- Alpro almond: cap 60 fires but score 43.4 < 60, not binding
- Go Milk: cap 55 fired (from additive escalation), score 39.5 < 55, not binding

**Key insight: In the milk corpus, the NOVA4 cap at 60 does not bind on any product** because the actual weighted dimension scores are already below 60. The cap's effect is primarily psychological — it prevents these products from ever recovering above 60 even with excellent nutrient profiles, but in this corpus, they don't have excellent nutrient profiles anyway.

In the snack bar corpus, the cap is more often binding. Specifically, the NOVA4 products with moderately good nutritional profiles (protein bars, date-based bars that are NOVA 4) might otherwise score 60–65 but are capped at 60.

---

## Mechanism 3: Additive Quality Dimension Collapse

### The additive_quality formula

```
additive_categories = count of distinct additive functional categories detected
base = max(0, 100 - additive_categories × 18)
sweetener_penalty = 15 if sweetener_detected else 0
additive_quality = max(0, base - sweetener_penalty)
```

**Weight of additive_quality: 0.10**

### Score table (no sweetener)

| Additive categories | additive_quality | Weighted contribution |
|--------------------|-----------------|-----------------------|
| 0 | 100 | 10.0 |
| 1 | 82 | 8.2 |
| 2 | 64 | 6.4 |
| 3 | 46 | 4.6 |
| 4 | 28 | 2.8 |
| 5 | 10 | 1.0 |
| 6+ | 0 | 0.0 |

### Score table (with sweetener, +15 penalty)

| Additive categories | additive_quality | Weighted contribution |
|--------------------|-----------------|-----------------------|
| 0 + sweetener | 85 | 8.5 |
| 1 + sweetener | 67 | 6.7 |
| 2 + sweetener | 49 | 4.9 |
| 3 + sweetener | 31 | 3.1 |
| 4 + sweetener | 13 | 1.3 |
| 5 + sweetener | 0 | 0.0 |

**The additive dimension swings 10 points in weighted score** (from 10.0 to 0.0). This is meaningful but not catastrophic on its own. The problem is additive pressure stacking with cap pressure.

### Compound additive effect (dimension + cap)

For a NOVA 4 product with 3 additive categories and sweetener:
- additive_quality = 31 → weighted contribution: 3.1 (vs. 10.0 clean) → **loss: 6.9 pts**
- processing_quality = 25 (vs. 95 clean) → weighted contribution: 3.75 (vs. 14.25) → **loss: 10.5 pts**
- WFI = 18 → weighted contribution: 0.72 (vs. 4.0) → **loss: 3.28 pts**
- Three structural dimensions together: **loss: 20.7 pts** from their clean-product equivalents

Plus:
- NOVA4 cap binds at 60 → prevents recovery
- SWEETENER_CAP at 70 → adds an independent ceiling

A product that is NOVA 4 with sweetener and 3 additive categories arrives with ~21 points of structural disadvantage from three dimensions alone, then runs into a 60-point ceiling that it likely doesn't reach anyway.

---

## Mechanism 4: Cross-Family Cap Stacking

### The stacking problem

Each concern family (SUGAR_LOAD, PROCESSING_LOAD, CALORIE_LOAD, SODIUM_LOAD, FAT_QUALITY) produces an independent binding cap. The **overall binding cap is the minimum across all families plus SWEETENER_CAP**.

### Worst-case example: heavily loaded snack bar

A heavily sweetened, calorie-dense, NOVA 4 snack bar with 2 Israeli red labels:

| Cap source | Cap value |
|-----------|-----------|
| NOVA_PROXY_4_ULTRA_PROCESSED | 60 |
| ADDITIVE_MARKERS_3_PLUS | 65 |
| HIGH_SUGAR_25G_PLUS | 60 |
| SNACK_BAR_RED_SUGAR_LABEL | 55 |
| ISRAELI_RED_LABEL_1_SUGAR | 55 |
| ISRAELI_RED_LABELS_2_PLUS | 45 |
| SNACK_BAR_HIGH_CAL | 70 |
| SNACK_BAR_HIGH_CAL_SUGAR | 60 |
| ISRAELI_RED_LABEL_1_SAT_FAT | 55 |
| **Binding cap (minimum)** | **45** |

The product is capped at 45 before any penalties. If penalties then remove an additional 15–25 points (possible under SRC-05 with a 45-point pre-penalty score), the final score reaches 20–30.

This is realistic: the lowest snack bar in the corpus scores 12.4. Several score in the 15–20 range. The heavy cap stacking is the primary driver, not the dimension scores.

**Is this wrong?**  
Not entirely. Products with 2+ Israeli red labels, NOVA 4, 5+ additive categories, and high sugar genuinely deserve severe structural penalties. The concern is not that these products score 20 — it is that the **resolution between 20 and 35 is lost**. All heavily stacked products collapse into a narrow 12–30 range with minimal differentiation.

### Stack frequency in snack bar corpus

| Binding cap level | Product count | % |
|------------------|--------------|---|
| ≥ 70 (no significant cap) | 0 | 0% |
| 60–69 | 8 | 16% |
| 55–59 | 12 | 24% |
| 45–54 | 16 | 33% |
| below 45 | 13 | 27% |

**60% of snack bars have a binding cap at 55 or lower.** Only 16% have no meaningful cap applied (≥70). This means cap architecture — not dimension scoring — drives the majority of final scores in this category.

---

## Mechanism 5: The Structural Emptiness Gate (SE)

The SE gate fires when: `kcal < threshold AND protein < 3g AND fiber < 1.5g AND fat < 2g AND (sweetener OR additives≥2)`.

When SE fires, calorie_density is capped at 50 and fat_quality returns neutral 50.

**SE effect in the milk corpus (run_003):**  
After Fix F2 (SE_BEVERAGE_KCAL reduced from 20 to 10), **zero products** in the milk corpus triggered SE. The gate no longer fires on plain plant milks at 15 kcal/100ml.

**SE design concern:**  
The SE gate's threshold conditions — particularly `protein < 3g` — are calibrated for foods, not beverages. A product with 1g protein/100ml is actually reasonable for a plain plant drink, but the 3g threshold makes the gate borderline for these products. The fix (lowering the kcal threshold to 10) correctly addressed this, but the gate retains some sensitivity to low-calorie beverages.

The SE gate produces a discrete 0/1 output — either it fires or it doesn't. When it fires, it applies a fixed penalty regardless of how close to the threshold the product is. This is a cliff: a product at kcal=9 (no SE) vs. kcal=11 (SE fires) receives dramatically different treatment despite a 2-kcal difference.

---

## Mechanism 6: The SRC-05 Relative Penalty Factor

When total coordinated penalties are applied, SRC-05 scales them to prevent over-penalization:

```python
penalty_factor = 0.45 if score_after_cap < 30 else 0.50
max_relative_pen = score_after_cap × penalty_factor
if total_pen > max_relative_pen:
    scaled_penalty = max_relative_pen
```

**Effect:** A product at score 60 can absorb at most 30 points of penalty. A product at score 30 can absorb at most 13.5 points of penalty.

**Observed effect in corpus:** SRC-05 scaling rarely fires. Most products in the corpus accumulate 0–12 total coordinated penalty before the budget applies. The relative penalty factor is a safety valve, not a primary driver.

The more significant effect is the **absolute floor at 10** — no non-veto product scores below 10. This creates a soft bottom for the distribution.

---

## Mechanism 7: The Nutrient Density Problem in Beverages

### The formula

```
nutrient_density = 0.65 × prot_score(protein_g) + 0.35 × fiber_score(fiber_g)
```

Protein breakpoints: 0g→0, 3g→15, 6g→30, 10g→50, 15g→70, 20g→85, 25g→95

**Weight of nutrient_density: 0.15**

### Effect on whole milk

Whole milk has 3.3g protein, 0g fiber (missing):
- prot_score(3.3) ≈ 16.5
- fiber_score(0) = 0
- nutrient_density = 10.7

Weighted contribution: 10.7 × 0.15 = **1.6 points** (maximum possible: 14.25)

Whole milk's nutrient_density contributes only **1.6/14.25 = 11%** of its potential weight. The formula is calibrated for dense solid foods where protein needs to exceed 10g to be considered meaningful. For beverages, 3.3g protein per 100ml is actually strong, but the formula doesn't account for this.

**Combined with protein_quality (weight 0.10):** whole milk's protein at 3.3g (whole_food source) scores 16.5 → weighted contribution 1.65. The two protein-related dimensions (25% of the total weight) contribute 3.25 points total — 13% of their maximum potential (25 points).

Without the NOVA1 floor, whole milk would score **69.54**, landing in C (current threshold: C = 55–69). This is wrong. Whole milk is not a C-tier product by any credible structural analysis. The nutrient density formula's calibration for solid food density is the primary reason.

---

## Summary: Pressure Quantification by Source

| Pressure source | Typical impact | Severity |
|----------------|----------------|----------|
| NOVA 3→4 dimension cliff | −5.70 pts (dimension) | Moderate |
| NOVA 4 cap: 60 (vs. NOVA 3: 75) | −15 pts ceiling headroom | High |
| Combined NOVA 3→4 | **~−21 pts total** | Very high |
| Additive quality collapse (0→5 cats) | −10 pts weighted dim | Moderate |
| Additive cap escalation (no cap→55) | −5 to −15 pts ceiling | High |
| Cross-family cap stacking (worst case) | binding cap = 45 | Very high |
| SE gate (when firing) | calorie_density fixed at 50 | Situational |
| Nutrient density formula vs. beverages | ~−12 pts for milk (protein mis-calibration) | High for beverages |
| SRC-05 relative penalty | 0–12 pts typical | Low–moderate |

**The dominant sources of excessive compression are:**
1. The NOVA 3→4 combined cliff (~21 pts combined cap + dimension)
2. Cross-family cap stacking to 45 or lower
3. The beverage/dairy protein density formula miscalibration

These three sources account for most of the gap between where products naturally fall and where they structurally belong.

---

## What the Analysis Does NOT Conclude

This analysis does NOT conclude:
- That NOVA 4 products deserve higher scores
- That heavy additive stacking should be penalized less
- That Israeli red label caps are too harsh

It concludes:
- The **transition between NOVA levels** should be smoother (fewer cliff effects)
- **Cap stacking resolution** should improve (products at 2 caps vs. 8 caps should land further apart)
- The **nutrient density formula** needs beverage-appropriate calibration (or a category-specific modifier)
- The **grade thresholds** should reflect the actual distribution, not an aspirational ideal

Bari's conviction is preserved. Its calibration is improved.

---

*Next: See `recalibration_proposals.md` for specific proposed constant changes.*
