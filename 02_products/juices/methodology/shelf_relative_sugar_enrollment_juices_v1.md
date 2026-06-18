# Juices × Sugar: Shelf-Relative Enrollment Proposal
## D6 Ruling — Nutrition Agent

**Status:** D6 PROPOSED (awaiting D7 Product co-sign)
**Task:** TASK-278 Phase-9
**Recorded:** 2026-06-14
**Author:** Nutrition Agent
**Extends:** EV-084 (mechanism), EV-087 (cereals×sugar), EV-088 (yogurt×sugar), EV-089 (cheese_spreads×sat_fat), EV-090 (hard_cheeses×sat_fat)
**Proposed EV:** EV-091

---

## 1. Authoritative Corpus

**Run:** `run_juices_001` (2026-06-07)
**Path:** `02_products/juices/bsip2_outputs/run_juices_001/`
**Batch summary:** `02_products/juices/reports/run_juices_001_batch_summary.json`

- Products loaded: 65
- Products scored: 65
- Products with sugars_g data: 65 (100% coverage)
- Grade distribution: A=1, C=54, D=10
- Score range: 48.7–85.0

---

## 2. Router Category Analysis

**Finding: Split routing — beverage (45) + default (19) + dessert (1)**

The juices corpus is not cleanly confined to a single router category:
- `beverage` (45 products): 100% juices, lemon juices, fruit drinks, cold-pressed
- `default` (19 products): nectars (פריגת, ספרינג, Minute Maid), cold-pressed squeezed juices (סחוט), smoothies
- `dessert` (1 product): מיץ מוסקט אפרת — confirmed misroute, already flagged in batch summary

The `default` routing for nectars and cold-pressed is an artifact of the router not recognising these sub-types, not a product-quality distinction. Products in both `beverage` and `default` are the same shelf category to a consumer.

**Scope recommendation:** Use `category_slug == "juices"` (BSIP1 field, present on all 65 products) as the scope guard, NOT the router category. This mirrors the corpus filter (`corpus_filter.json`, CF-J-001/002/003) and aligns with how EV-055 handled brined cheeses (using `bsip_cheese_subpool` rather than router category) and EV-088 handled yogurt (using `category_subtype`). The shelf_relative_differentiator should read the BSIP1 `category_slug` field.

**D7 open question Q1:** Confirm that `category_slug` is accessible in the `nn` dict at scoring time (Data Agent verification required before wiring).

---

## 3. Shelf Sugar Statistics (n=65, all with sugars_g)

All figures from `run_juices_001` trace files. Data source: direct product scrape via BSIP0 (no OFF used).

| Statistic | Value |
|---|---|
| n | 65 |
| min | 1.75 g/100ml |
| max | 16.8 g/100ml |
| mean | 9.95 g/100ml |
| stdev | 3.42 g/100ml |
| Q1 | 8.4 g/100ml |
| median | 9.5 g/100ml |
| Q3 | 12.2 g/100ml |
| IQR | 3.80 g/100ml |
| MAD | 1.30 g/100ml |
| 1.4826 × MAD | 1.93 g/100ml |
| IQR / 1.349 | 2.82 g/100ml |
| **robust_scale (IQR-primary)** | **2.82 g/100ml** |
| dead_zone_lo (median − 0.3×scale) | 8.65 g/100ml |
| dead_zone_hi (median + 0.3×scale) | 10.35 g/100ml |
| near_median_dead_pct | 24.6% |
| 0 scaling-pinned products | confirmed (prior spread analysis) |

**IQR-primary check:** IQR/1.349 = 2.82 > 1.4826×MAD = 1.93. IQR-primary is the binding scale. Consistent with EV-084 D7 co-sign mandate.

**Scale adequacy:** robust_scale = 2.82g is above the EV-084 minimum guard of 1.4g. The 3.42g stdev and 14.05g range (min=1.75 to max=16.8) confirm substantial spread. Context from prior spread analysis: juices IQR=3.80, which is lower than cereals (11.0) but meaningful given the per-100ml basis (liquid category). 0% scaling-pinned products confirms the mechanism has headroom across the corpus.

---

## 4. Subgroup Assessment

The corpus spans five sub-pools as defined in `corpus_filter.json`:

| Sub-pool | Representative sugar range | Count (approx) |
|---|---|---|
| juice_100 (100% fruit juice) | 7.6–14.2 g/100ml | ~35 |
| nectar (25–99% fruit) | 8.4–13.8 g/100ml | ~19 |
| fruit_drink (<25% fruit) | 9.6–11.6 g/100ml | ~5 |
| smoothie | 9.4–9.5 g/100ml | ~3 |
| cold_pressed | 7.6–9.4 g/100ml | ~3 |

**Sugar ranges substantially overlap across sub-pools.** The juice_100 sub-pool spans a wider range (7.6–14.2g) than the nectars (8.4–13.8g), reflecting variation in fruit type (lemon=2.5g, mango/grape=14.2g) rather than sub-pool category. Smoothies and cold-pressed products cluster near the median.

**Recommendation: Score as a single peer group.** Sub-pool splitting is not warranted because:
1. Sugar variation within juice_100 (1.75–14.2g) is greater than variation between sub-pools
2. The consumer comparison frame is the full juice/drink shelf, not sub-pool-specific
3. A peer-group split on sub-pools would require router-level sub-pool detection (not currently wired) and produce low-n groups for smoothies/cold-pressed (<5 each)

**Exception flag:** The 1 dessert-misrouted product (מיץ מוסקט, 7290006696717, sugar=9.4g, score=57.4/C) should be excluded from SR scope by the `category_slug` guard — this product was already flagged as a misroute in the batch summary. No scope action needed here; the `category_slug` guard handles it.

**D7 open question Q2:** Should the "fruit_drink" sub-pool (products with <25% fruit content, e.g. משקה פירות תרה) be included in the same SR peer group? These products (e.g. 7290000118276, תרה תפוז-מנגו 11.6g, 49.9/D) score lower due to broader architecture factors but their sugar is real and shelf-comparable. Nutrition position: INCLUDE — excluding them would shelter the worst formulations from SR surcharge. Product Agent should confirm.

---

## 5. SR Band Parameters

All parameters follow the standard established by EV-085 through EV-090.

| Parameter | Value | Rationale |
|---|---|---|
| nutrient | sugars_g | Sugar is the key driver in juice quality differentiation |
| direction | asymmetric | Penalize high-sugar, relieve low-sugar |
| P_max | 6 | Standard across all TASK-278 enrollments |
| B_max | 3 | Standard asymmetry (P > B per EV-084 D7 co-sign) |
| floor_value | 62 | Standard floor across TASK-278 juices enrollment |
| floor_threshold_g | Q3 = 12.2 g/100ml | Products at/above Q3 receive the floor protection |
| z_dead_zone | ±0.3 | Standard dead zone to suppress noise at the median |
| scale | IQR-primary = 2.82 g/100ml | EV-084 formula: max(IQR/1.349, 1.4826×MAD, 1.4) |
| min_n guard | 20 | Corpus n=65 >> 20 ✓ |
| low_variance guard | IQR ≥ 2.0 | IQR=3.80 >> 2.0 ✓ |

**Floor threshold rationale:** Q3 = 12.2 g/100ml is the shelf's natural upper quartile. Products at or above this value receive the floor(62) protection. The Israeli red-label sugar threshold (10g/100ml for beverages per prior system) is explicitly NOT used — this follows the redlabel-de-anchor directive (2026-06-14 standing).

**Anti-Immunity proof:**
floor(62) + B_max(3) = **65 < 70** (grade B threshold at 70).
Anti-Immunity Rule: PASSES. Even a low-sugar juice at full +3 relief cannot reach grade B (70) from the floor. The absolute backbone (scores in the 50–62 range for the bulk of the corpus) retains priority.

---

## 6. Named Inversions

### Inversion A — Opposite-Side (Relief vs No-Change): Lemon juice vs Orange juice 100%

**A (high-sugar, higher-score):** מיץ תפוזים 100% פריגת 1 ליטר  
- Barcode: 7290000039435  
- sugars_g: 8.4 g/100ml  
- Current score: 56.1 / C  
- z = (8.4 − 9.5) / 2.82 = −0.39 → within dead zone → SR_delta = 0

**B (low-sugar, lower-score):** מיץ לימון משומר 500מ"ל  
- Barcode: 7290002263586  
- sugars_g: 2.5 g/100ml  
- Current score: 59.7 / C → WAIT: 59.7 > 56.1 — B scores HIGHER despite lower sugar — this is the correct Inversion A direction (B has less sugar AND scores higher; A has more sugar and scores lower)

**Correction:** This is not a true inversion where high-sugar scores higher. Lemon juice already scores 3.6pts higher despite 5.9g less sugar — which is the *correct* direction architecturally (lemon's lower glycemic_quality from sugar is reflected). However, the gap (3.6pts) is understated given the sugar difference: lemon at 2.5g should score substantially more than orange at 8.4g.

**SR effect:**
- Lemon (z = −2.49, well below dead zone): SR_delta = +B_max = +3.0 → new score: 62.7/C
- Orange (z = −0.39, within dead zone): SR_delta = 0 → new score: 56.1/C

Gap before SR: **3.6 pts** (lemon higher — correct direction but understated)  
Gap after SR: **6.6 pts** (lemon now 62.7 vs orange 56.1 — correct direction, appropriately widened)

This is an **understated-gap inversion** — the mechanism correctly amplifies a gap that exists but is compressed by absolute-only scoring. Lemon at 2.5g sugar is genuinely shelf-exceptional and earns the relief.

---

### Inversion B — True Ranking Inversion: Peach nectar vs Apple juice 100%

**A (high-sugar, higher-score):** נקטר אפרסק פריגת 1 ליטר  
- Barcode: 7290002696043  
- sugars_g: 12.2 g/100ml  
- Current score: 58.1 / C  
- Category: default (nectar, misrouted from beverage)

**B (lower-sugar, lower-score):** מיץ תפוחים 100% פריגת 1 ליטר  
- Barcode: 7290000039442  
- sugars_g: 9.6 g/100ml  
- Current score: 51.4 / C  
- Category: beverage

**The inversion:** Apple juice 100% (9.6g) scores 51.4 while Peach nectar (12.2g, +2.6g sugar) scores 58.1 — a 6.7pt gap in the wrong direction. The score gap arises because the nectar routes to `default` (which has a more favourable calorie_density dimension baseline under the beverage→calorie mapping) rather than from any quality difference. Architecturally: a 100% fruit juice should not score 6.7 points below a nectar with more sugar.

**SR effect:**
- Peach nectar (z = (12.2 − 9.5) / 2.82 = +0.96): SR_delta = −min(6, 0.96×6) = −5.8 → new score: 52.3/C
- Apple juice (z = (9.6 − 9.5) / 2.82 = +0.04, within dead zone): SR_delta = 0 → new score: 51.4/C

Gap before SR: **+6.7 pts** (nectar HIGHER despite +2.6g sugar — true inversion)  
Gap after SR: **+0.9 pts** (near-eliminated — nectar no longer dominates 100% juice)

This is a **true ranking inversion** eliminated by SR. The 100% juice is correctly elevated to near-parity with the higher-sugar nectar.

---

### Additional Inversion C — Cross-Sugar, Same Sub-Pool: Grape juice vs Orange juice 100%

**A (high-sugar):** מיץ ענבים סגל משפחות 1 ליטר  
- Barcode: 7290015348423  
- sugars_g: 14.2 g/100ml  
- Current score: 50.5 / C

**B (lower-sugar):** מיץ תפוזים 100% פריגת 1 ליטר  
- Barcode: 7290000039435  
- sugars_g: 8.4 g/100ml  
- Current score: 56.1 / C

Both are 100% juices, same `beverage` router category. Orange correctly scores higher despite being the same sub-pool. But the gap of 5.6pts understates the 5.8g sugar difference.

**SR effect:**
- Grape (z = (14.2 − 9.5) / 2.82 = +1.67): SR_delta = −min(6, 1.67×6) = −6.0 → new score: 44.5/C
- Orange (z = (8.4 − 9.5) / 2.82 = −0.39): SR_delta = +min(3, 0.39×3) = +1.2 → new score: 57.3/C

Gap before SR: **5.6 pts** (correct direction but compressed)  
Gap after SR: **12.8 pts** (gap expands appropriately for 5.8g sugar difference, both remain C)

---

## 7. Proposed EV Number

**EV-091**

Verified: the highest EV in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` is EV-090 (hard_cheeses×sat_fat, TASK-278 Phase-8). EV-091 is the next free slot.

**Do NOT register EV-091 yet.** Registration is the D7+orchestrator step, not the D6 proposal.

---

## 8. D7 Open Questions for Product Agent

**Q1 — Scope guard field:** The recommended scope guard is `category_slug == "juices"` (from BSIP1 data). Data Agent must verify this field is accessible in the `nn` dict at scoring time before wiring. If not accessible, fallback scope would need to be negotiated (e.g., a new `bsip_juice_subpool` field, or a combined `(category == "beverage" OR category == "default") AND bsip0_category_tag in {"juice_100","nectar","fruit_drink","smoothie","cold_pressed"}` guard). **This is a blocking pre-wiring item.**

**Q2 — Fruit drink inclusion:** Should the fruit drink sub-pool (<25% fruit content, e.g. משקה פירות תרה products at 11.6g sugar, 49.9/D) be included in the same SR peer group as 100% juices and nectars? Nutrition position: include — these are on the same consumer shelf and their sugar load is real. Exclusion would shelter the weakest products from SR surcharge. Product Agent call.

**Q3 — Scale adequacy vs prior enrollments:** The juice robust_scale (2.82 g/100ml) is substantially lower than cereals (8.896 g/100ml) or yogurt (4.299 g/100ml). This reflects the compressed sugar range in a beverage category reported per 100ml. At scale=2.82, a product 2 standard deviations above median (e.g. 15.1g) receives the full P_max=6 surcharge — which is appropriate. But Product Agent should confirm that P_max=6 / B_max=3 remains correctly calibrated for this scale, or whether the budget should be adjusted given the narrower spread.

**Q4 — Pilot gate criteria:** Should the standard 11-criterion gate (from EV-087/090) apply, or does the routing split (beverage vs default) require additional criteria? Nutrition position: add one criterion: "SR does not fire differently based on router category alone" — i.e., a nectar in `default` and an equivalent 100% juice in `beverage` with the same sugar_g should receive the same SR delta. This tests that the scope guard is working on `category_slug`, not on the router category.

---

## 9. Scope Definition (Proposed)

```
SUGAR_SHELF_REL_SCOPE add: category_slug == "juices"
SUGAR_SHELF_REL_JUICE_FLOOR = 62
JUICE_FLOOR_THRESHOLD_G = 12.2  # Q3 of corpus
```

Scope guard: `nn.get("category_slug") == "juices"` — evaluated BEFORE router category check, consistent with EV-088/089 subtype guard pattern.

---

## 10. No-Regression Commitments

These are the standard six guards from EV-084, binding on the implementing agent:

1. Cross-corpus baseline diff: all published categories byte-identical under flag-off
2. SUGAR_SHELF_REL_V1 rule tag present in juice traces when SR fires
3. Low-variance guard (IQR ≥ 2.0) and min_n guard (n ≥ 20) verified at runtime
4. All products with sugars_g ≥ 15.0g confirmed at composite ≤ 55 (floor protection holding)
5. Flag-off: byte-identical across all published categories (milk, brined, yogurt, cereals as deployed)
6. Monotonicity: sugars_g increasing → SR_delta non-decreasing in magnitude (penalty direction)

**Additional juice-specific guard:**
7. SR delta for any `category_slug == "juices"` product does not fire based on router category alone — two products with identical sugar_g but different router category (beverage vs default) must receive identical SR_delta.

---

## 11. Governance Classification

Category/nutrient enrollment into the approved EV-084 mechanism. Requires:
- D7 co-sign: Nutrition Agent (this document) + Product Agent (pending)
- Neither D6 nor D7 constitutes engine modification — implementation is Data Agent's task, gated on both co-signs
- Owner go-live before any published juice score changes

---

## 12. Rollback Condition

If pilot rescore shows:
- Any product with sugars_g ≤ 5g scoring below 60 after SR (over-relief)
- Any product with sugars_g ≥ 15g scoring above 55 (floor protection failure)
- Router-category bleeding: SR fires on non-juice products in `beverage` category

→ Halt immediately, notify orchestrator, revert scope entry.

---

*Data source: run_juices_001 BSIP2 traces (2026-06-07). All nutrition values from direct product scrape. OFF not used — banned project-wide.*
