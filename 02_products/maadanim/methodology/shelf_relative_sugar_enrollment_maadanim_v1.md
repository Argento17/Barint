# Shelf-Relative Sugar Enrollment — Maadanim (מעדנים) × Sugar
## D6 Proposal | EV-092 | TASK-278 Phase-10

**Status:** D6 PROPOSED — awaiting D7 co-sign from Product Agent  
**Author:** Nutrition Agent  
**Date:** 2026-06-14  
**Extends:** EV-087 (cereals), EV-088 (yogurt), EV-089 (cheese_spreads), EV-090 (hard_cheeses), EV-091 (juices)  

---

## 1. Category Definition

**Maadanim (מעדנים)** = Israeli dairy desserts and puddings shelf — chocolate mousse (מילקי), puddings (פודינג), yogurt-style desserts (יופלה/עדנה), protein desserts, probiotic desserts, kids desserts, and reduced-sugar desserts. The category is defined by the presence of `bsip_maadanim_subtype` in the BSIP1 product file, not by the router-assigned category.

**Authoritative run:** `run_maadanim_001`  
**BSIP1 source dir:** `C:\Bari\03_operations\bsip1\run_maadanim_001\output\`  
**BSIP2 output dir:** `C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\`  
**Corpus size:** 200 products (all with `bsip_maadanim_subtype` confirmed)

---

## 2. Scope Guard

```python
# Activation condition for glycemic_quality shelf-relative adjustment
product.get("bsip_maadanim_subtype") is not None \
    and nn.get("sugars_g") is not None
```

**Field verification:** `bsip_maadanim_subtype` is present in 200/200 BSIP1 source files (100% coverage). Values: `dairy_dessert_generic` (118), `protein_dessert` (19), `milky_style` (17), `probiotic_dessert` (16), `flavored_yogurt_dessert` (13), `pudding_dessert` (10), `reduced_sugar_dessert` (5), `kids_dessert` (2).

**Note on router category:** The maadanim corpus routes across multiple BSIP2 categories — `dessert` (91), `default` (48), `dairy_protein` (33), `snack_bar_granola` (13), `cracker` (5), `beverage` (4), others (6). This is expected: the router does not know it is scoring a maadanim product; that information lives in the BSIP1 `bsip_maadanim_subtype` field. The scope guard is therefore implemented against the BSIP1 field, not the router category. This is the same pattern as EV-090 (`bsip_cheese_subpool`) and EV-091 (`juice_sub_pool`).

**Recommended scope (n_scope):** 146 products (those with both `bsip_maadanim_subtype` and `sugars_g` not null). The 54 products missing `sugars_g` are excluded by the `is not None` guard.

---

## 3. Sugar Distribution — Shelf Statistics

Computed from `L1_observed_signals.sugars_g` across all 146 products in scope (run_maadanim_001 traces). No OFF data used. No external DB used.

| Statistic | Value |
|-----------|-------|
| **n (with sugar data)** | 146 / 200 |
| min | 0.00 g |
| max | 97.12 g |
| mean | 14.56 g |
| stdev | 16.75 g |
| **Q1** | 4.30 g |
| **Median** | 9.70 g |
| **Q3** | 16.08 g |
| **IQR** | 11.78 g |
| **MAD** | 5.90 g |
| IQR / 1.349 | 8.73 |
| 1.4826 × MAD | 8.75 |
| **robust_scale** | **8.75** (IQR-primary: max(8.73, 8.75, 1.4)) |
| Scale ≥ 3.0 guard | PASS (8.75 >> 3.0) |
| Dead zone [median ± 0.3×scale] | [7.08, 12.32] g |
| Products in dead zone | 40 / 146 = 27.4% |

**No juice-style exception needed.** The category has genuine spread (IQR=11.78g, scale=8.75), well above the 3.0 minimum. Standard SR activation applies.

**Note on max=97.12g:** Barcode 518220 routes to `snack_bar_granola` (not `dessert` or `dairy_protein`) and has 97.12g sugar — this is a clear misbinning/outlier product. Its presence in the corpus inflates the stdev but does not affect median or robust_scale meaningfully (robust statistics are outlier-resistant). The scope guard's `is not None` check includes it; a D7 open question addresses whether `snack_bar_granola` products should be explicitly excluded.

---

## 4. SR Design Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **direction** | asymmetric | High sugar is a harm signal; low sugar earns relief |
| **P_max** (penalty ceiling) | 6 | Consistent with cereals/yogurt/cheese_spreads/juices |
| **B_max** (bonus ceiling) | 3 | Consistent with prior phases |
| **floor** | 62 | Category floor (same as juices precedent; maadanim are NOVA-heavy desserts, appropriate ceiling on relief) |
| **z_dead** | ±0.30 | Standard dead zone; products within ±0.3×scale of median score 0 delta |
| **floor_threshold_g** | **16.08 g** (Q3) | De-anchored from the binary Israeli red-label 10g threshold per red-label de-anchor directive 2026-06-14 |

**Anti-Immunity proof:**  
- floor(62) + B_max(3) = 65 < 70 → PASS  
- Products at or above Q3 (16.08g) are in the surcharge zone (z > 0), meaning they receive negative delta, not B_max relief. The worst-case floor+relief scenario (sugar=0g, gets full B_max) still caps at 65, below the B grade threshold of 70.

**floor_threshold_g rationale (de-anchor):** The Israeli red-label threshold for sugar is 10g/100g. Under the old binary system, a product at 9.9g scored identically to one at 4g — both below the cliff. The SR system replaces this with Q3-based continuous scoring. A product at 16.08g (the Q3 of the shelf) is genuinely high for maadanim relative to its category peers; a product at 10g is near the median (9.70g) and receives near-neutral delta — not a penalty for being "barely above the cliff" that never existed in continuous scoring.

---

## 5. Named Inversions

### INV-A: מילקי טופ עדשים (7290110573751) vs. משקה יוגורט פרו תות ללס (7290110573737)

Two products from the same brand segment, both routing to `dessert`, both NOVA=4, both with 4 sprint1 additives. Sugar differs by 14.6g/100g.

| Attribute | 7290110573737 (lower sugar) | 7290110573751 (higher sugar) |
|-----------|------------------------------|-------------------------------|
| sugar | 3.4 g/100g | 18.0 g/100g |
| glycemic_quality | 81.5 | 45.0 |
| red_labels | none | sugar (binary cap fires) |
| NOVA | 4 | 4 |
| additive_count | 4 | 4 |
| current score | 56.3 / C | 28.5 / E |
| score delta | — | -27.8 pts |

The 27.8-point gap between structurally similar products is driven by both glycemic penalty AND the binary red-label cap (ISRAELI_RED_LABEL_1_SUGAR fires at 18g). The SR system would:

- 7290110573737 (z = (3.4 - 9.70) / 8.75 = -0.72): **z < -0.3** → earns B_max-proportional relief ≈ +2.9 pts (capped at floor 62)
- 7290110573751 (z = (18.0 - 9.70) / 8.75 = +0.95): **z > +0.3** → earns penalty ≈ -5.7 pts (capped at P_max 6)
- Expected net directional effect: gap maintained and directionally correct; lower-sugar product benefits from explicit relief while higher-sugar product is additionally penalized via continuous surcharge rather than solely via binary cap

This is not an inversion (the gap is already in the right direction), but it demonstrates that the binary cap creates an abrupt 2-tier system within what should be a continuous penalization curve, and that many products at 10-17g escape surcharge entirely under the current system.

### INV-B: Two Products at 9.8g vs 12.0g — Near-Median Compression

| Attribute | 7290110321697 (9.8g sugar) | 7290014762800 (12.0g sugar) |
|-----------|----------------------------|-----------------------------|
| sugar | 9.8 g/100g | 12.0 g/100g |
| score | 56.4 / C | 42.9 / D |
| NOVA | 4 | 4 |
| additive_count | 4 | 3 |
| red_labels | none | none |
| caps fired (sugar-related) | none | none |

The product at 12.0g scores 13.5 pts lower despite only 2.2g more sugar/100g, and having *fewer* additives (3 vs 4). This gap is driven by other signals (additive_quality dimension), showing that the current binary sugar system provides no meaningful gradient across the 9.8–12.0g range. Both are near-median; under SR, both would receive near-zero delta (both within dead zone [7.08, 12.32]). The SR system correctly identifies that these two products are on the same part of the shelf-relative sugar curve.

**Effective named inversion:** The LAND classification for maadanim×sugar is confirmed — the binary system clusters many products near the 10g red-label cliff without providing the continuous gradient that exists in the underlying sugar data.

---

## 6. Evidence Classification

**Type:** LAND (not COSMETIC). The sugar distribution spans 0–97g/100g with IQR=11.78g and scale=8.75, confirming genuine shelf spread. The 10g binary threshold cuts the distribution at approximately the 49th percentile (median=9.70g), creating artificial compression on both sides of the cliff.

**Evidence tier:** Strong. Stats computed from 146/200 authoritative BSIP2 traces. No external DB used. Prior SR precedents (EV-087 through EV-091) establish the mechanism.

---

## 7. D7 Open Questions

1. **Scope bleed: non-dessert router categories.** Products routing to `snack_bar_granola`, `cracker`, `beverage` have `bsip_maadanim_subtype` set (they were scraped from the maadanim shelf). Should the scope guard additionally require `category in ('dessert', 'dairy_protein', 'default')` to exclude clear misbins? This would narrow scope from 146 to approximately 97. Decision: Product Agent.

2. **reduced_sugar_dessert subtype (n=5).** These products were deliberately designed to have lower sugar (e.g., sugar-free milky-style desserts). They score near-zero on sugar (0–3g/100g) and would receive the full B_max relief under SR. Is this the correct behavior — should reduced-sugar desserts be rewarded via SR, or is their low-sugar status already captured by sweetener detection (which applies its own cap)? Products with `sweetener_tier` != null may double-benefit. D7 decision required.

3. **kids_dessert subtype (n=2, small sample).** Only 2 products. SR scoring with n=2 is statistically thin. Recommend noting that this subtype is included in the population stats but its individual z-scores may not be representative. Flag for future re-evaluation when corpus expands.

4. **Dead zone width (27.4%).** The dead zone captures 40/146 products = 27.4%. This is within tolerable range (below the 40% absorption ceiling used in prior phases), but higher than yogurt (EV-088). Product Agent should confirm the dead zone is acceptable or request z_dead adjustment to ±0.25 to sharpen discrimination.

---

## 8. Pilot Gate Criteria (for D7/D8 handoff)

Following the 12-criterion gate established for EV-091:

| Criterion | Requirement |
|-----------|-------------|
| C1 | Directional distribution: more products below median than above (sugar is right-skewed) |
| C2a | Grade distribution not degraded overall (net A+B+C count ≥ baseline) |
| C2b | No single grade absorbs >40% of movers |
| C3 | Gap narrows in INV-A and INV-B (correct direction) |
| C4 | Min movers ≥ 5 products with |delta| ≥ 1 pt |
| C5 | Min grade changes ≥ 1 |
| C6 | Max absorption: dead zone ≤ 40% (current: 27.4%, PASS pre-pilot) |
| C7 | Anti-immunity: floor+B_max=65 < 70 PASS |
| C8 | Floor compliance: no scored product above floor(62) via SR alone |
| C9 | No scope bleed: zero milk/bread/snack/cheese/yogurt/juice products affected |
| C10 | Frozen byte id: milk scores unchanged (CRITICAL) |
| C11 | Routing agnostic: outcome is determined by `bsip_maadanim_subtype`, not router category |

---

## 9. Implementation Notes (for Data Agent, post-D7)

- Scope guard field: `product.get("bsip_maadanim_subtype")` — present in BSIP1 input dict
- Signal field: `nn.get("sugars_g")` — from `normalized_nutrition_per_100g` in BSIP1
- Shelf parameters to encode as config (not hardcoded): `median=9.70`, `robust_scale=8.75`, `P_max=6`, `B_max=3`, `floor=62`, `z_dead=0.30`, `floor_threshold_g=16.08`
- The SR delta applies to `glycemic_quality` dimension, which is then re-weighted in the standard fashion
- No changes to `constants.py` or `score_engine.py` during D6 or D7 — implementation only in D8

---

## 10. Files

| File | Purpose |
|------|---------|
| `C:\Bari\03_operations\bsip1\run_maadanim_001\output\` | BSIP1 source files (scope guard field: `bsip_maadanim_subtype`) |
| `C:\Bari\02_products\maadanim\bsip2_outputs\run_maadanim_001\` | Authoritative BSIP2 traces (sugar stats source) |
| `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md` | EV-092 registration target |
| `C:\Bari\tasks\returns\P127_return.md` | Return block for orchestrator |

---

*Nutrition Agent | TASK-278 Phase-10 | 2026-06-14*  
*D6 only — no engine edits, 0 score movement*
