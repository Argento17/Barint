# BSIP2 Dimension Mapping — v1 to v2 Architecture

**Status:** Architecture specification  
**Version:** 2.0-draft  
**Date:** 2026-05-18  
**Companion:** layer_architecture.md

---

## Purpose

This document maps the ten analytical dimensions from the current BSIP2 scoring engine (proto_v0) to the four-layer architecture proposed in v2. It identifies:

1. Where each current dimension belongs in the new structure
2. Overlaps and redundancies between current dimensions
3. Hidden NOVA dependencies that inflate NOVA's effective weight
4. Collinearity risks and their mitigation
5. Signals that currently have no home and need new placement

---

## Current Dimension Inventory

The following ten dimensions are actively scored in BSIP2 proto_v0 with the weights shown:

| Dimension | Current Weight | Current Role |
|-----------|---------------|-------------|
| processing_quality | 15% | NOVA → score table lookup |
| nutrient_density | 15% | Protein + fiber breakpoint interpolation |
| calorie_density | 15% | kcal → category-specific table lookup |
| glycemic_quality | 12% | Sugar penalty + fiber bonus |
| protein_quality | 10% | Protein amount × source quality factor |
| additive_quality | 10% | Additive count × per-category deduction |
| satiety_support | 6% | (protein×3 + fiber×5) / kcal × 400 |
| fat_quality | 8% | Sat fat fraction + trans fat + seed oil |
| regulatory_quality | 5% | Israeli red label count |
| whole_food_integrity | 4% | NOVA base + ingredient count complexity |

---

## Dimension-to-Layer Mapping

### processing_quality → Layer 1 (Primary)

**Current behavior:** Direct table lookup on NOVA level: 1→95, 2→80, 3→55, 4→25.

**Layer assignment:** Layer 1 (Structural Integrity), primary signal.

**Notes:**  
This dimension is a near-direct mapping of NOVA. In the v2 architecture, NOVA remains a strong signal within Layer 1, but processing_quality as a standalone dimension is retired. Instead, Layer 1 computes a Structural Integrity Index from NOVA + reconstruction intensity + ingredient topology + additive architecture. The NOVA contribution within Layer 1 is calibrated differently — it no longer acts as a simple score lookup but as one factor among several.

**Transition:** processing_quality is absorbed into Layer 1. No separate dimension survives.

---

### whole_food_integrity → Layer 1 (Secondary, merge candidate)

**Current behavior:** NOVA base score (1→100, 2→80, 3→50, 4→20) minus ingredient count complexity penalty.

**Layer assignment:** Layer 1 (Structural Integrity), secondary signal.

**Collinearity with processing_quality:** CRITICAL  
Both dimensions draw directly from the NOVA level. processing_quality uses NOVA scores (95/80/55/25); whole_food_integrity uses a separate NOVA table (100/80/50/20). The correlation between these two dimensions is near-perfect for any given product. This represents **4% + 15% = 19% of total weight** measuring essentially the same thing — NOVA level.

**Transition:** whole_food_integrity is merged into Layer 1 and retired as a standalone dimension. Its insight — that ingredient count complexity also matters — is incorporated into the "ingredient topology" signal within Layer 1.

---

### additive_quality → Layer 1 (Secondary) + Layer 4 (Partial)

**Current behavior:** Per-additive-category deduction (18 pts each) + sweetener penalty (15 pts). Maximum floor at 0.

**Layer assignment:**  
- Structural dimension: additive count → Layer 1 (ingredient topology, additive architecture)
- Engineering-intent dimension: specific additive classes (flavor enhancers, artificial colors, sweeteners) → Layer 4 (Consumption Engineering)

**Notes:**  
The current dimension conflates two distinct concepts: (a) structural complexity from additive burden, and (b) the intent behind specific additive classes. A product with 3 stabilizers has structural complexity but no particular engineering intent. A product with a sweetener + artificial flavor + texture modifier is potentially engineered for consumption beyond satiety. These deserve different analytical homes.

**Collinearity with processing_quality / whole_food_integrity:**  
High NOVA correlates with high additive count, so all three dimensions (processing_quality, whole_food_integrity, additive_quality) tend to fire together. Combined, they represent 29% of nominal weight but >40% of effective influence on NOVA 4 products.

**Transition:** additive_quality is split. The structural component enters Layer 1. The engineering-intent component enters Layer 4. The current dimension is retired.

---

### nutrient_density → Layer 2 (Primary)

**Current behavior:** Protein + fiber breakpoint interpolation, weighted 65/35.

**Layer assignment:** Layer 2 (Nutritional Contribution), primary signal.

**Notes:**  
This dimension is well-placed conceptually. It belongs in Layer 2 as the primary nutritional contribution signal. In the v2 architecture, it is augmented by fortification skepticism (synthetic nutrients count for less) and protein realism (declared protein is credible-checked against ingredient list).

**Collinearity with protein_quality and satiety_support:**  
nutrient_density includes protein (65% weight), protein_quality also evaluates protein (with source adjustment), and satiety_support is heavily protein-driven. These three dimensions together represent 15% + 10% + 6% = 31% of weight with substantial protein signal overlap.

**Transition:** nutrient_density moves to Layer 2 as its primary nutrient contribution signal. The protein component is harmonized with protein_quality to prevent triple-counting.

---

### protein_quality → Layer 2 (Secondary, partial merge)

**Current behavior:** Protein quantity × source quality factor (whole_food: 1.0, mixed: 0.85, isolate: 0.70, unknown: 0.80).

**Layer assignment:** Layer 2 (Nutritional Contribution), secondary signal.

**Redundancy with nutrient_density:**  
Both evaluate protein quantity. nutrient_density uses protein on the 65% weight component; protein_quality re-evaluates protein with source adjustment. For a product with 15g whole-food protein, both dimensions score well for the same reason. This is collinear.

**What protein_quality adds uniquely:** The source quality factor. Isolate protein is credited at 70%, which nutrient_density does not capture. This is the unique contribution.

**Transition:** In Layer 2, protein_quality's unique value (source quality) is preserved as a modifier on the protein contribution signal. As a standalone equally-weighted dimension, it is retired. The protein evaluation in Layer 2 applies source quality intrinsically.

---

### satiety_support → Layer 3 (Primary)

**Current behavior:** (protein×3 + fiber×5) / max(50, kcal) × 400.

**Layer assignment:** Layer 3 (Metabolic Stability), primary signal.

**Notes:**  
The concept is right: this dimension tries to assess satiety potential. But the current formula has a problem: the kcal floor of 50 artificially inflates scores for very-low-calorie products. A product at 15 kcal with 0.5g protein and 0.3g fiber gets satiety_support ≈ 24, which is low — but if we divide by the actual 15 kcal rather than the floored 50, the score appears better than it should for a product with virtually no satiety contribution.

**Redundancy with nutrient_density:** Both depend heavily on protein and fiber. The signal overlap is significant. The key distinction: satiety_support is context-weighted by calorie content; nutrient_density is not. This distinction is worth preserving.

**Transition:** satiety_support moves to Layer 3 as a core signal. The kcal floor behavior is reviewed. The protein/fiber overlap with nutrient_density is addressed by Layer 2 and Layer 3 operating at different granularity (Layer 2: what is present; Layer 3: how it behaves metabolically).

---

### calorie_density → Layer 3 (Primary) + Layer 2 (Context)

**Current behavior:** Category-specific lookup table mapping kcal to a score (lower kcal = higher score for most categories).

**Layer assignment:**  
- Metabolic Stability dimension: Layer 3 (calorie context, digestion dynamics)
- Nutritional contribution context: Layer 2 (calorie proportionality check)

**Notes:**  
The current calorie_density dimension creates the most dangerous failure mode in the system: low calories score well, regardless of what (or what isn't) in the product. A diet soda and a bowl of plain oats can score identically on this dimension. The SE (Structural Emptiness) gate exists to partially mitigate this, but it is a late-stage patch rather than a structural solution.

In the v2 architecture, calorie density is evaluated differently in Layers 2 and 3:
- **Layer 2**: "Are the calories proportional to the nutrition delivered?" A product at 30 kcal with 0g protein and 0g fiber scores poorly in Layer 2's calorie context — the calories deliver nothing.
- **Layer 3**: "What does this calorie density imply for metabolic stability?" A high-calorie dense product that also has strong satiety support (Layer 3) and good nutrition (Layer 2) behaves very differently from a high-calorie dense product without those properties.

**Transition:** calorie_density as a standalone dimension is retired. Its concept is split between Layer 2 (calorie proportionality) and Layer 3 (calorie density context). The category-specific tables are preserved as calibration inputs to these layers.

---

### glycemic_quality → Layer 3 (Primary)

**Current behavior:** 90 − sugar_penalty + fiber_bonus + whole_grain_bonus, with sweetener annotation.

**Layer assignment:** Layer 3 (Metabolic Stability), primary signal.

**Notes:**  
This is the most purely Layer 3 dimension in the current system. It is well-placed. The current formula is a reasonable proxy for glycemic behavior, though it has known limitations (doesn't distinguish fructose from glucose, doesn't account for physical form, doesn't account for co-ingestion with fat/protein).

**Transition:** glycemic_quality moves to Layer 3 with minimal structural change. The formula is a valid starting point for the glycemic plausibility signal.

---

### fat_quality → Layer 2 (Partial) + Layer 3 (Partial)

**Current behavior:** Saturated fat fraction + trans fat status + seed oil penalty.

**Layer assignment:**  
- Nutritional contribution component: Layer 2 (fat profile as nutrition signal)
- Metabolic context component: Layer 3 (fat's role in glycemic moderation, satiety)

**Notes:**  
Fat quality currently evaluates the fat profile from a health risk perspective (saturated fat ratio, trans fat, seed oil). In the v2 architecture, fat evaluation serves two purposes: (a) whether the fat profile is nutritionally coherent (Layer 2), and (b) whether fat interacts with other macros in metabolically meaningful ways (Layer 3).

The current penalty for seed oils may carry implicit ideological weight. In v2, the fat evaluation is explicitly limited to what nutritional science can credibly claim, separated from cultural preferences.

**Transition:** fat_quality is split between Layer 2 (fat composition quality) and Layer 3 (fat-carb interaction as metabolic moderator). The trans fat veto remains a standalone safety mechanism outside the layer system.

---

### regulatory_quality → Cross-layer (Meta)

**Current behavior:** Israeli red label count (0 labels: 95, 1 label: 60, 2+ labels: 25).

**Layer assignment:** Cross-layer regulatory signal — applied as a cap modifier, not absorbed into any single layer.

**Notes:**  
Regulatory quality is categorically different from the other dimensions. It is not an analytical judgment — it is a regulatory fact. A product has or does not have a red label. In v2, regulatory status is treated as a **meta-signal** that modifies the orchestration output rather than contributing to any specific layer.

A product with 2+ red labels should face score restrictions regardless of how well it scores on Layer 2 or Layer 3. This is a policy commitment, not an analytical finding.

**Transition:** regulatory_quality is removed from the dimension layer. It becomes a first-class meta-signal that feeds directly into the orchestration resolution layer, with explicit separation from the interpretive intelligence.

---

## Summary Mapping Table

| Current Dimension | Weight | → Layer 1 | → Layer 2 | → Layer 3 | → Layer 4 | → Meta |
|-------------------|--------|-----------|-----------|-----------|-----------|--------|
| processing_quality | 15% | Primary ✓ | | | | |
| whole_food_integrity | 4% | Merge into L1 | | | | |
| additive_quality | 10% | Structural part | | | Engineering part | |
| nutrient_density | 15% | | Primary ✓ | | | |
| protein_quality | 10% | | Modifier (source) | | | |
| calorie_density | 15% | | Proportionality | Primary ✓ | | |
| glycemic_quality | 12% | | | Primary ✓ | | |
| satiety_support | 6% | | | Primary ✓ | | |
| fat_quality | 8% | | Partial | Partial | | |
| regulatory_quality | 5% | | | | | Primary ✓ |

---

## Collinearity Analysis

### Critical collinearity cluster: NOVA-dependent trio

**Dimensions:** processing_quality + whole_food_integrity + additive_quality  
**Nominal weight:** 15% + 4% + 10% = 29%  
**Effective correlation:** Near-perfect on NOVA 4 products (all three score poorly)  
**Impact:** NOVA effectively controls ~35–40% of the final score, not the nominal 15%

**Mitigation in v2:** All three are absorbed into Layer 1. The Layer 1 output is one voice in the orchestration, not three.

---

### Moderate collinearity cluster: Protein signal triple

**Dimensions:** nutrient_density (65% protein weighted) + protein_quality + satiety_support (protein × 3)  
**Nominal weight:** 15% + 10% + 6% = 31%  
**Effective correlation:** High for protein-rich products; moderate for others  
**Impact:** High-protein products receive triple credit. Low-protein products receive triple penalty.

**Mitigation in v2:** Layer 2 evaluates protein once (with source quality built in). Layer 3 evaluates satiety as a composite signal that includes protein but is not dominated by it.

---

### Low-level collinearity: Glycemic / Satiety interaction

**Dimensions:** glycemic_quality + satiety_support  
**Shared signal:** fiber (appears in both)  
**Impact:** High-fiber products receive double credit through these two dimensions.

**Mitigation in v2:** Layer 3 evaluates glycemic behavior and satiety as interrelated metabolic signals, coordinated within the same layer rather than independently weighted.

---

## Hidden NOVA Dependencies

Beyond the explicit NOVA-dependent trio, the following mechanisms carry hidden NOVA influence:

| Mechanism | How NOVA enters | Hidden weight |
|-----------|----------------|---------------|
| NOVA_PROXY_4 cap (60) | NOVA 4 → hard score ceiling | Blocks all layers from contributing above 60 |
| HP nova_weight gate | NOVA 1-2: HP fires at 0%; NOVA 3: 50%; NOVA 4: 100% | Amplifies HP penalties for NOVA 4 |
| Category confidence modulation | Lower confidence → relaxed thresholds | NOVA uncertainty feeds confidence |
| Sweetener cap | Sweeteners often → NOVA 4; cap at 70 | Double-penalizes NOVA 4 with sweeteners |

**In v2:** The NOVA cap is replaced by Layer 1's orchestration influence. Layer 1's Structural Integrity Index, when low, sets a ceiling — but this ceiling is computed from the full structural signal set, not from NOVA alone.

---

## Signals Currently Without a Home

The following concepts appear in framework documents but have no formal home in the current dimension scoring:

| Signal | Current status | v2 Home |
|--------|---------------|---------|
| Fermentation credit | Mentioned in beneficial_processing.md; not scored | Layer 1 (beneficial processing credit) |
| Ingredient fragmentation spectrum | In ingredient_fragmentation_concept.md; not scored | Layer 1 (reconstruction intensity) |
| Fortification skepticism | In positive_architecture_framework.md; not scored | Layer 2 (modifier on nutrient credit) |
| Liquid calorie effect | Partially via category tables; not explicit | Layer 3 (liquid calorie delivery signal) |
| Reward stacking | In hyper-palatability concept; limited in HP rules | Layer 4 (reward stacking index) |
| Matrix coherence | In matrix_integrity_framework.md; not scored | Layer 1 (matrix coherence signal) |
| Protein realism | In positive_architecture_framework.md; not scored | Layer 2 (protein realism check) |

---

*Next: See `orchestration_v2.md` for how the four layer outputs are coordinated into a final assessment.*
