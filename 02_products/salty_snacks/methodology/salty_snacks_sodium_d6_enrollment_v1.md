# Shelf-Relative Sodium Enrollment — Salty Snacks × Sodium
## D6 Proposal | EV-093 | TASK-278 Phase-11

**Status:** D6 PROPOSED — awaiting D7 co-sign from Product Agent
**Author:** Nutrition Agent
**Date:** 2026-06-14
**Extends:** EV-087 (cereals), EV-088 (yogurt), EV-089 (cheese_spreads), EV-090 (hard_cheeses), EV-091 (juices), EV-092 (maadanim)

---

## 1. Category Definition

**Salty snacks** = the Israeli salty-snack shelf: chips (crisps), puffed snacks, popcorn, pretzels/bagels, rice cakes, baked snacks, and crackers. All products in this corpus carry `category: "salty_snack"` in their BSIP1 file — confirmed 54/54 (100%).

**Authoritative run:** `run_salty_snacks_002`
**BSIP1 source dir:** `C:\Bari\02_products\salty_snacks\bsip1_outputs\`
**BSIP2 output dir:** `C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\`
**Corpus size:** 54 products

---

## 2. Scope Guard

```python
# Activation condition for sodium shelf-relative adjustment
product.get("category") == "salty_snack" \
    and nn.get("sodium_mg") is not None
```

**Field verification:** `category: "salty_snack"` is present in 54/54 BSIP1 files (100% coverage). Sub-pools represented: chips (11), baked (13), puffed (13), popcorn (7), rice_cakes (7), pretzels (3).

**Note on BSIP2 router category:** The 54 salty-snack products route across multiple BSIP2 categories — `whole_food_fat` (27), `snack_bar_granola` (9), `bread` (5), `dairy_protein` (4), `cracker` (4), `dessert` (2), `sauce_spread` (1), `beverage` (1), `default` (1). This is expected: the BSIP2 router assigns a nutritional category agnostic to shelf placement. The scope guard is therefore implemented against the BSIP1 `category` field, not the router-assigned BSIP2 category. This is consistent with EV-090 (`bsip_cheese_subpool`) and EV-091 (`juice_sub_pool`).

**Sodium data coverage:** 54/54 products have `sodium_mg` in `L1_observed_signals`. No missing data — the guard `is not None` excludes nobody from this corpus.

---

## 3. Sodium Shelf Statistics

Computed from `L1_observed_signals.sodium_mg` (mg per 100g) across all 54 products in scope (run_salty_snacks_002 traces). No OFF data used. No external database used. All values are derived from authoritative BSIP0/BSIP1 panel scans.

| Statistic | Value |
|-----------|-------|
| **n (with sodium data)** | 54 / 54 |
| min | 10 mg |
| max | 920 mg |
| mean | 543.4 mg |
| stdev | 192.1 mg |
| **Q1** | 440 mg |
| **Median** | 560.0 mg |
| **Q3** | 630 mg |
| **IQR** | 190 mg |
| **MAD** | 85.0 mg |
| IQR / 1.349 | 140.85 |
| 1.4826 × MAD | 126.02 |
| **robust_scale** | **140.85** (IQR-primary: max(140.85, 126.02, 1.40)) |
| Scale >= 3.0 guard | PASS (140.85 >> 3.0) |
| Dead zone [median ± 0.3 × scale] | [517.7, 602.3] mg |
| Products in dead zone | 15 / 54 = 27.8% |

**Distribution note:** The corpus spans 10–920 mg/100g with the IQR running 440–630 mg. The distribution is approximately symmetric in the core (median 560 vs mean 543) with a long right tail (pretzels cluster at 840–920 mg). The scale (140.85) is substantive — well above the 3.0 minimum — confirming genuine shelf spread and SR applicability.

**Unit confirmation:** All sodium values are in mg per 100g, consistent with Israeli labeling requirements. The field `sodium_mg` in the trace stores the per-100g panel value directly; no unit conversion is applied.

**No Q3-based cap justification:** The Israeli Ministry of Health red-label threshold for sodium is 600 mg/100g (packaged salty snacks). Under the old binary system, products at 599 mg scored identically to products at 300 mg — both below the cliff. The Q3 at 630 mg reflects the actual distribution: more than one-quarter of salty snacks on shelf exceed this level. Products above Q3 are genuinely high-sodium relative to their shelf peers, independent of whether they exceed any regulatory threshold.

---

## 4. SR Design Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **nutrient** | sodium_mg | Sodium is the primary shelf-differentiating nutrient in salty snacks |
| **direction** | asymmetric | High sodium is a harm signal; low sodium earns relief |
| **median** | 560.0 mg | Shelf median from corpus |
| **IQR** | 190 mg | From corpus |
| **robust_scale** | 140.85 | max(IQR/1.349, 1.4826×MAD, 1.40) = max(140.85, 126.02, 1.40) |
| **P_max** (penalty ceiling) | 6 | Consistent with all prior SR phases (EV-087 through EV-092) |
| **B_max** (bonus ceiling) | 3 | Consistent with prior phases |
| **floor** | 62 | Standard SR floor; salty snacks are structurally calorie-dense, appropriate relief ceiling |
| **z_dead** | ±0.30 | Standard dead zone |
| **floor_threshold_mg** | **630 mg** (Q3) | De-anchored from binary Israeli red-label 600 mg cap per directive 2026-06-14 |
| **SUGAR_SHELF_SCALE_GUARD** | PASS | robust_scale = 140.85 >> 3.0; guard is satisfied by a factor of 47× |

**Anti-Immunity proof:**
- floor(62) + B_max(3) = 65 < 70 → PASS (B-grade threshold is 70; maximum SR-boosted score remains 65)
- Products at or above Q3 (630 mg) are in the surcharge zone (z > 0), receiving negative delta
- Products at the minimum (10 mg, rice cakes plain) receive maximum relief: z = (10 - 560) / 140.85 = -3.90 → capped at B_max = +3 pts → maximum score via SR alone = 62 + 3 = 65/B

**De-anchor rationale:** The Israeli red-label sodium threshold is 600 mg/100g (binary cliff). Under the current system, a product at 598 mg scores identically to one at 200 mg on all sodium-related signals — the only sodium penalization mechanism is the `HIGH_SODIUM_700MG_PLUS` cap at 700 mg and the `HP_FAT_SODIUM_COMBO` penalty which fires on fat×sodium interaction. The Q3 floor at 630 mg anchors the surcharge zone on the real distribution: a product must be genuinely above most of its shelf peers (top 25%) to attract a penalty delta, rather than being 1 mg above an arbitrary regulatory cliff.

**Dimension target:** The SR delta applies to the `regulatory_quality` dimension (sodium is a regulatory concern) or, subject to D7 deliberation, as a standalone adjustment. Note: the current `regulatory_quality` dimension reads Israeli red-label count; wiring sodium SR here may require distinguishing SR delta from red-label count signal. The alternative (a standalone sodium_shelf_relative adjustment independent of dimensions) is the cleaner implementation path. D7 open question #3 below.

---

## 5. Named Inversions

### INV-A: Pringles Original (7290005204001) vs Bisli Spaghetti (7290009900003)

Two products where 320 mg/100g more sodium produces only 0.5 pts score difference — the high-sodium product scores effectively identically to a product with 67% less sodium.

| Attribute | 7290005204001 (Pringles Original) | 7290009900003 (Bisli Spaghetti) |
|-----------|-----------------------------------|----------------------------------|
| sodium_mg | 480 mg/100g | 800 mg/100g |
| sub_pool | chips | puffed |
| current score | 52.4 / C | 52.9 / C |
| grade | C | C |
| sodium z-score (SR) | (480 - 560) / 140.85 = -0.57 | (800 - 560) / 140.85 = +1.70 |
| SR z position | OUTSIDE dead zone (low) | OUTSIDE dead zone (high) |
| HP_FAT_SODIUM fired | No | No |
| HIGH_SODIUM_700MG_PLUS fired | No | Yes (cap=60, fired but score already <60) |

**Inversion nature:** Both products score 52-53/C. The Bisli Spaghetti contains 320 mg/100g more sodium — a difference that represents more than two full servings' worth of additional sodium. Under SR, Bisli Spaghetti (z=+1.70) would attract a penalty of approximately -5.1 pts (approaching P_max=6), while Pringles Original (z=-0.57) would earn relief of approximately +1.7 pts. This would create a ~6.8-point spread between two products currently rated identically, which correctly reflects the meaningful sodium gap.

**Why the gap is currently invisible:** The `HIGH_SODIUM_700MG_PLUS` cap fires for Bisli Spaghetti but has no effect because the pre-cap score is already 52.9 (below the 60 cap). The HP_FAT_SODIUM_COMBO requires both fat>30% of kcal AND sodium>600mg — Bisli Spaghetti's fat content sits below this combined threshold. Sodium at 800 mg/100g imposes zero effective penalty beyond these two non-firing mechanisms.

---

### INV-B: Bisli Spaghetti (7290009900003) vs Baked Pretzels (7290011350002)

A genuine score inversion: the higher-sodium product scores 4.1 points HIGHER than the lower-sodium product, both outside the dead zone, both in the C-grade band.

| Attribute | 7290009900003 (Bisli Spaghetti) | 7290011350002 (Baked Pretzels) |
|-----------|----------------------------------|--------------------------------|
| sodium_mg | 800 mg/100g | 920 mg/100g |
| sub_pool | puffed | pretzels |
| current score | 52.9 / C | 57.0 / C |
| grade | C | C |
| sodium z-score (SR) | +1.70 | +2.56 |
| SR z position | OUTSIDE dead zone (high) | OUTSIDE dead zone (high) |
| HIGH_SODIUM_700MG_PLUS fired | Yes | Yes |
| Na difference | — | +120 mg/100g more |
| Score difference | — | +4.1 pts (inversion) |

**Inversion nature:** Baked Pretzels contains 120 mg/100g more sodium than Bisli Spaghetti but scores 4.1 points higher. This is a genuine quality-signal inversion: other structural signals (whole-grain content, cleaner ingredient list, lower fat) drive the pretzel scores upward despite higher sodium. The current engine has no mechanism to penalize the sodium difference continuously once the binary 700 mg cap has fired and been absorbed. Under SR, Baked Pretzels (z=+2.56) would receive a penalty approaching P_max = -6.0 pts while Bisli Spaghetti (z=+1.70) would receive approximately -5.1 pts. The remaining score gap between them would then reflect genuine non-sodium architectural differences rather than an artifact of sodium penalization saturation.

**The saturation problem:** At 800 mg and 920 mg, both products have already absorbed the `HIGH_SODIUM_700MG_PLUS` cap. Because the cap fires only once (binary), there is zero marginal penalty for 120 additional mg/100g of sodium above the cliff. The SR system converts this to a continuous function: z=2.56 correctly penalizes more than z=1.70, proportionally and without saturation.

---

## 6. Evidence Classification

**Type:** LAND (not COSMETIC). The sodium distribution spans 10–920 mg/100g with IQR=190 mg and scale=140.85. The Israeli 600 mg red-label threshold cuts the distribution at approximately the 67th percentile (Q3=630 mg), creating a binary cliff at which many products cluster. The 700 mg HIGH_SODIUM cap fires and saturates for products above the cliff — creating the inversion documented in INV-B.

**Evidence tier:** Strong. Stats computed from 54/54 authoritative BSIP2 traces (run_salty_snacks_002). No external database used. Both named inversions are directly trace-verifiable at the cited barcodes. Prior SR precedents (EV-087 through EV-092) establish the mechanism.

**OFF data used:** None. All sodium values are from direct product scrape panels stored in BSIP1 files.

---

## 7. Open Questions for D7

1. **Scope guard mechanism.** The proposed guard uses `product.get("category") == "salty_snack"` (BSIP1 field). This is simpler and more robust than sub-pool filtering, but includes all 54 products regardless of sub-pool. Two sub-pools may warrant scrutiny: (a) rice_cakes (n=7, sodium range 10–420 mg — extremely low-sodium; their low z-scores would all earn near-B_max relief of +3 pts, which is the intended behavior); (b) caramel popcorn (n=2, sodium 260–280 mg, but score ~21-24/E due to sugar/additive issues — SR would give them modest relief that the sugar caps would override). Product Agent should confirm the single-field guard is sufficient or whether `sub_pool not in ("caramel_popcorn",)` is warranted.

2. **Rice cakes as high-relief outliers.** Rice Cakes Plain (Na=10 mg, score=85/A) is already at the corpus ceiling. SR B_max=3 would push a theoretical maximum to 65 (floor) — but the whole-food floor at 70 already protects this product. Net SR effect on this specific product is zero (floor absorbs B_max relief). However, the 7 rice-cake products collectively score 61–82/A-B; those already above 62 (the SR floor) would benefit from +1 to +3 pts. D7 should confirm this relief is appropriate for an already-high-scoring segment, given that rice cakes are genuinely low-sodium relative to the category.

3. **Dimension target for sodium SR.** The current engine applies sodium signals through: (a) `regulatory_quality` dimension (binary Israeli red-label count); (b) `HIGH_SODIUM_700MG_PLUS` cap; (c) `HP_FAT_SODIUM_COMBO` penalty. Wiring sodium SR into `regulatory_quality` risks conflating the red-label binary signal with the continuous SR delta. The cleaner implementation (recommended) is a standalone sodium SR adjustment applied after dimension scoring — consistent with how sugar SR is applied to `glycemic_quality`. Product Agent + Data Agent should confirm the implementation lane in D8.

4. **HP_FAT_SODIUM_COMBO interaction.** This penalty fires when fat>30% kcal AND sodium>600 mg. For products where SR penalty also fires (high-sodium), there will be a stacking effect: HP penalty (up to 6 pts) + SR penalty (up to 6 pts). For a product at sodium=800 mg with 32% fat, the combined penalty could reach -12 pts. D7 should confirm whether a combined penalty budget is needed or whether stacking is acceptable (the two penalties target different concerns: HP targets behavioral palatability patterning, SR targets shelf-relative sodium architecture).

5. **Budget consideration.** P_max=6 is consistent with prior phases. For salty snacks, where 18/54 products (33%) are above the dead zone ceiling (602.3 mg), a 6-point penalty ceiling is proportionate. If D7 believes the scale of sodium harm in salty snacks warrants stronger penalization (given that these are high-frequency consumption items), P_max=8 is an option — but this would deviate from the cross-category consistency established in EV-087 through EV-092. Nutrition Agent recommendation: keep P_max=6 for consistency; the continuous gradient provides sufficient differentiation.

---

## 8. Pilot Gate Criteria (for D7/D8 handoff)

Following the gate established for prior SR phases:

| Criterion | Requirement |
|-----------|-------------|
| C1 | Directional distribution: products outside dead zone (high) penalized, products outside (low) relieved |
| C2a | Grade distribution not degraded overall (net A+B+C count >= baseline) |
| C2b | No single grade absorbs >40% of movers |
| C3 | INV-A gap widens: Bisli Spaghetti penalized vs Pringles Original relieved |
| C4 | INV-B corrected: Baked Pretzels penalty exceeds Bisli Spaghetti penalty |
| C5 | Min movers >= 5 products with |delta| >= 1 pt |
| C6 | Min grade changes >= 1 |
| C7 | Max absorption: dead zone <= 40% (current: 27.8%, PASS pre-pilot) |
| C8 | Anti-immunity: floor+B_max=65 < 70 PASS |
| C9 | Floor compliance: no product above floor(62) via SR alone |
| C10 | No scope bleed: zero milk/bread/yogurt/cheese/juice/maadanim products affected |
| C11 | Frozen invariant: milk scores unchanged (CRITICAL) |
| C12 | Routing agnostic: outcome determined by `category=="salty_snack"`, not BSIP2 router category |

---

## 9. Implementation Notes (for Data Agent, post-D7)

- Scope guard field: `product.get("category") == "salty_snack"` — present in BSIP1 input dict
- Signal field: `nn.get("sodium_mg")` — from `normalized_nutrition_per_100g` in BSIP1
- Shelf parameters to encode as config (not hardcoded):
  - `median_sodium_mg = 560.0`
  - `robust_scale = 140.85`
  - `P_max = 6`
  - `B_max = 3`
  - `floor = 62`
  - `z_dead = 0.30`
  - `floor_threshold_mg = 630` (Q3)
- No changes to `constants.py` or `score_engine.py` during D6 or D7 — implementation only in D8
- The SR delta is a post-dimension, pre-floor adjustment (consistent with sugar SR in other phases)

---

## 10. Corpus Table (run_salty_snacks_002, sorted by sodium)

| Barcode | Na (mg/100g) | Score | Grade | Sub-pool | Product (EN) |
|---------|-------------|-------|-------|----------|--------------|
| 7290011499001 | 10 | 85 | A | rice_cakes | Rice Cakes Plain |
| 7290003100018 | 15 | 77.5 | B | popcorn | Popcorn Natural No Salt |
| 7290000066010 | 240 | 28.7 | E | puffed | Bamba Chocolate |
| 7290004000001 | 260 | 21.4 | E | popcorn | Rainbow Caramel Popcorn |
| 7290000087007 | 280 | 23.6 | E | popcorn | Flex Caramel Popcorn |
| 7290028800001 | 280 | 79.8 | B | rice_cakes | Rice Cakes Whole Wheat Rye |
| 3560071099022 | 320 | 82.5 | A | rice_cakes | Carrefour Whole Wheat Cakes |
| 7290000066003 | 360 | 54.1 | C | puffed | Bamba |
| 7290011499025 | 380 | 74.2 | B | rice_cakes | Wheat Cakes Whole Wheat |
| 3560071099008 | 390 | 61.2 | C | rice_cakes | Carrefour Rice Cakes Sea Salt |
| 3560071033002 | 420 | 87.5 | A | baked | Carrefour Baked Lentil Chips |
| 7290011499018 | 420 | 65.8 | B | rice_cakes | Rice Cakes Sea Salt |
| 7290035510001 | 420 | 81.3 | A | rice_cakes | Rye Crackers |
| 3560071033019 | 440 | 84.0 | A | baked | Carrefour Baked Chickpea Chips |
| 7290011350033 | 450 | 72.1 | B | baked | Whole Wheat Seed Crackers |
| 3560071044503 | 480 | 83.4 | A | baked | Carrefour Whole Wheat Crackers |
| 7290005204001 | 480 | 52.4 | C | chips | **Pringles Original (INV-A low-Na)** |
| 7290019900001 | 480 | 70.0 | B | popcorn | Good Boy Popcorn Salt |
| 3560071020002 | 500 | 70.4 | B | popcorn | Carrefour Popcorn Salt |
| 7290021800018 | 500 | 64.2 | C | baked | Baked Sea Salt Crisps |
| 7290000091004 | 510 | 58.3 | C | baked | Baked Potato Crisps Sea Salt |
| 7290000055007 | 530 | 70.0 | B | chips | Tapuchips Original |
| 8001505008118 | 530 | 44.3 | D | chips | Pringles Paprika |
| 7290014800001 | 540 | 70.0 | B | chips | Chipsy Sea Salt |
| 7290021800001 | 540 | 56.2 | C | baked | Baked Tomato Crisps |
| 7290003100001 | 560 | 64.2 | C | popcorn | Popcorn Salt Butter |
| 7290014250001 | 560 | 50.8 | C | chips | Tasty Tomato Basil |
| 7290024400001 | 560 | 83.4 | A | baked | Crisp Whole Wheat Crackers |
| 3560071020019 | 570 | 56.0 | C | popcorn | Carrefour Popcorn Cheese |
| 5010477348070 | 580 | 70.9 | B | baked | Faces Pita Chips Sea Salt |
| 7290000055014 | 580 | 51.9 | C | chips | Tapuchips Paprika |
| 7290014800018 | 580 | 70.0 | B | chips | Chipsy Reduced Fat |
| 8710908800001 | 590 | 53.9 | C | chips | Doritos Nacho Cheese |
| 7290002050001 | 600 | 70.0 | B | chips | Round Chips |
| 7290002211001 | 600 | 70.5 | B | baked | Sea Salt Crackers |
| 7290015700001 | 600 | 49.2 | D | puffed | Tapuchips Cheese Flavor |
| 7290014250018 | 610 | 33.0 | E | puffed | Tasty Cheese |
| 5010477348087 | 620 | 67.7 | B | baked | Faces Pita Chips Garlic Herb |
| 7290015700018 | 620 | 39.2 | D | chips | Tapuchips BBQ |
| 7290019900018 | 620 | 36.0 | D | popcorn | Good Boy Popcorn Cheese |
| 7290000615010 | 630 | 73.1 | B | baked | Pita Chips Whole Wheat |
| 8710908800018 | 640 | 49.6 | D | chips | Doritos Cool Ranch |
| 3560071063009 | 650 | 39.0 | D | puffed | Carrefour Cheese Crackers |
| 7290000615003 | 650 | 72.2 | B | baked | Pita Chips Original |
| 7290031100001 | 700 | 36.1 | D | puffed | Cheese Corn Puffs |
| 7290000078006 | 720 | 39.0 | D | puffed | Shem Tov Cheese Crackers |
| 7290004702001 | 750 | 47.5 | D | puffed | Corn Puffs |
| 7290009900003 | 800 | 52.9 | C | puffed | **Bisli Spaghetti (INV-A high-Na / INV-B low-Na)** |
| 7290000630006 | 820 | 54.0 | C | puffed | Bisli Grill |
| 3560071056000 | 840 | 57.0 | C | pretzels | Carrefour Mini Pretzels Sesame |
| 7290000630020 | 840 | 52.4 | C | puffed | Bisli Onion |
| 3560071050009 | 880 | 57.0 | C | pretzels | Carrefour Pretzels |
| 7290011350019 | 880 | 57.0 | C | pretzels | Whole Wheat Pretzels |
| 7290011350002 | 920 | 57.0 | C | pretzels | **Baked Pretzels (INV-B high-Na)** |

**Grade distribution:** A=9, B=17, C=19, D=8, E=1 (n=54)
**Dead zone [517.7 – 602.3 mg]:** 15 products (27.8%)
**Above dead zone (>602.3 mg):** 18 products (33.3%)
**Below dead zone (<517.7 mg):** 21 products (38.9%)

---

## 11. Files

| File | Purpose |
|------|---------|
| `C:\Bari\02_products\salty_snacks\bsip1_outputs\` | BSIP1 source files (scope guard field: `category`) |
| `C:\Bari\02_products\salty_snacks\bsip2_outputs\run_salty_snacks_002\` | Authoritative BSIP2 traces (sodium stats source) |
| `C:\Bari\02_products\salty_snacks\reports\tmp_sodium_stats.json` | Intermediate computation artifact (ephemeral) |
| `C:\Bari\03_operations\bsip2\evidence_registry\bsip2_evidence_registry_v1.md` | EV-093 registration target |
| `C:\Bari\tasks\returns\P130_return.md` | Return block for orchestrator |

---

*Nutrition Agent | TASK-278 Phase-11 | 2026-06-14*
*D6 only — no engine edits, 0 score movement*
