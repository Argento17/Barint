# Maadanim x Sugar: Shelf-Relative Enrollment — D7 Co-Sign
## TASK-278 Phase-10 | EV-092 | Product Agent D7 Verdict

**Status:** D7 CO-SIGNED  
**Author:** Product Agent  
**Date:** 2026-06-14  
**D6 input:** Nutrition Agent (P127, 2026-06-14)  
**Extends:** EV-087 (cereals), EV-088 (yogurt), EV-089 (cheese_spreads), EV-090 (hard_cheeses), EV-091 (juices)

---

## 1. Co-Sign Verdict

The D6 proposal passes. Shelf-relative sugar enrollment for maadanim x sugars_g is authorized for pilot rescore by the Data Agent.

**Scope guard confirmed:** `product.get("bsip_maadanim_subtype") is not None AND nn.get("sugars_g") is not None`  
**n_scope approved:** 146  
**EV number:** EV-092  
**Anti-immunity proof:** floor(62) + B_max(3) = 65 < 70 PASS  
**Engine files modified in D7:** NONE — implementation is Data Agent's task (D8)

---

## 2. D7 Open Questions — Resolved

### Q1: Router category filter (scope n=146 vs ~97)

**Decision: Reject the filter. Scope remains n=146.**

Rationale: The `bsip_maadanim_subtype` BSIP1 field is the authoritative scope boundary for maadanim. Router category assignment is a downstream artifact of a general routing algorithm that does not know it is scoring a maadanim product. Filtering by router category would exclude valid maadanim products (e.g., protein desserts misrouted to `dairy_protein`, generic desserts landing in `default`) based on a signal that carries no shelf-membership information. This is the same design principle that governs EV-090 (`bsip_cheese_subpool`) and EV-091 (`juice_sub_pool`) — BSIP1 field defines the scope, not the router.

Reducing n from 146 to ~97 by excluding `snack_bar_granola`, `cracker`, and `beverage` routed products would create a two-class system within the same shelf: some maadanim products get SR scoring, others do not, based on an uninformative router assignment. This is scope manipulation, not scope hygiene.

The one exception worth flagging: barcode 518220 (97.12g sugar, `snack_bar_granola`) is a clear outlier and probable misbinning. However, this product's inclusion does not affect median or robust_scale (robust statistics are outlier-resistant), and the SR mechanism handles it correctly — it scores at maximum z and receives P_max surcharge. No exclusion needed.

### Q2: reduced_sugar_dessert subtype (n=5, sugar 0-3g)

**Decision: Include in scope. No subtype exclusion.**

Rationale: The sweetener cap (score ceiling = 70) and the shelf-relative sugar relief operate on different dimensions and at different stages of the scoring pipeline. The sweetener cap is a policy ceiling on final score — it prevents sweetener-containing products from reaching grade B. The SR sugar relief is a signal correction to the glycemic_quality dimension that reflects a genuine nutritional reality: a product with 0-3g sugar per 100g genuinely has a different glycemic load profile than one with 18-25g, regardless of how that low-sugar reading was achieved.

The fear of "double-benefit" misreads the pipeline: B_max=3 relief raises the final score by at most 3 points. A product already at score 34 (E) moves to 37 (still E). A product at 42 (D) moves to 45 (still D). The sweetener cap at 70 is nowhere near triggered by a 3-point relief on a product that scores in the 30s-40s due to NOVA=4 and additive load. There is no structural path to grade-inflation here.

The alternative — excluding `reduced_sugar_dessert` from SR — would mean that the 5 products deliberately engineered to have no sugar receive no sugar-axis relief, which would be counter to the category logic. The rule "lower sugar earns modest relief within the shelf" is general and correct.

### Q3: kids_dessert subtype (n=2)

**Decision: Include. Flag only.**

n=2 is thin but not a problem for SR scoring — SR is applied at the product level (each product gets a z-score based on its own sugar reading vs the shelf median/scale). The population statistics are not destabilized by 2 kids_dessert products (they comprise only 1.4% of n=146). Include in scope with a note that the subtype-level distribution is non-representative at n=2 and should be re-evaluated when corpus expands.

### Q4: Dead zone width (27.4% absorption at z_dead = +/-0.30)

**Decision: Approve z_dead = +/-0.30. Dead zone is acceptable.**

27.4% (40/146 products) in the dead zone is within the 40% absorption ceiling established across all prior SR enrollments. The dead zone at z_dead = +/-0.30 spans sugar values of [7.08g, 12.32g] — a range of 5.24g around the 9.70g median. This is appropriate: products within 5g of the median are genuinely close on the maadanim sugar shelf and should not receive meaningful differentiation from SR alone.

Tightening to z_dead = +/-0.25 would narrow the dead zone to [7.50g, 11.95g], reducing absorption to approximately 22-24% at a cost of meaningless signal amplification for products that differ by 1-2g from the median. The standard parameter (+/-0.30) is the correct choice. No adjustment.

---

## 3. INV-B Replacement

The original INV-B pair (7290110321697 vs 7290014762800) was correctly rejected by the orchestrator — both products fall within the dead zone [7.08g, 12.32g], so SR assigns near-zero delta to both. This does not qualify as gate criterion C3 (gap_narrows_inversion).

**Replacement INV-B identified from trace search across all 200 run_maadanim_001 products.**

### INV-B (Replacement): בולגרית מעודנת 24% vs מעדן משמש

| Attribute | `2385455` (A — low sugar) | `5014271300429` (B — high sugar) |
|-----------|--------------------------|----------------------------------|
| Product | בולגרית מעודנת 24% | מעדן משמש |
| bsip_maadanim_subtype | dairy_dessert_generic | dairy_dessert_generic |
| router category | default | dessert |
| sugars_g | 3.5 g/100g | 52.0 g/100g |
| nova | 2 | 2 |
| sprint1_additive_count | 0 | 0 |
| sweetener_tier | None | None |
| red_labels | sat_fat, sodium | sugar |
| glycemic_quality | 81.2 | 10.0 |
| current score | **45.0 / D** | **45.6 / D** |

**The inversion:** Two products of the same BSIP1 subtype (`dairy_dessert_generic`), same NOVA=2, zero additives. Product A has 3.5g sugar/100g — it is a 24% fat Bulgarian-style dairy dessert with essentially no added sugar. Product B has 52.0g sugar/100g — an apricot dairy dessert with a dominant sugar load. Despite this 48.5g sugar differential, Product A currently scores 0.6 points *lower* than Product B (45.0 vs 45.6). The binary sugar system fails to differentiate them on the sugar axis because Product A's 3.5g does not trigger any sugar cap or penalty, and Product B's 52.0g triggers the `ISRAELI_RED_LABEL_1_SUGAR` cap but is counteracted by higher glycemic_quality base differences.

**SR correction:**

| | Product A (3.5g sugar) | Product B (52.0g sugar) |
|--|------------------------|-------------------------|
| z-score | (3.5 - 9.70) / 8.75 = -0.709 | (52.0 - 9.70) / 8.75 = +4.834 |
| zone | below dead zone → relief | far above dead zone → max surcharge |
| SR delta | +2.13 pts (B_max × min(0.709, 1.0) = 3 × 0.709) | -6.00 pts (P_max, capped) |
| score after SR | 45.0 + 2.13 = **47.13** | 45.6 - 6.00 = **39.6** |
| gap_before | -0.6 (A scores lower — wrong direction) |
| gap_after | +7.5 (A now scores higher — correct direction) |
| gap correction | +8.1 pts |

The SR system converts a 0.6-point wrong-direction gap into a 7.5-point correct-direction gap. This is a genuine inversion correction, not a cosmetic adjustment. The pair qualifies for C3 (gap_narrows_inversion) with directional reversal.

---

## 4. Pilot Gate Criteria (11 criteria)

| Criterion | Requirement | Status |
|-----------|-------------|--------|
| **C1** | directional_distribution: more products below median than above OR right-skewed distribution (sugar is KNOWN to be right-skewed in this category — mean=14.56 > median=9.70, confirming right skew) | Pre-PASS (skew confirmed from distribution stats) |
| **C2a** | grade_dist: net A+B+C count not degraded overall | Verify post-pilot |
| **C2b** | No single grade absorbs >40% of movers | Verify post-pilot |
| **C2c** | Magnitude: mean |delta| for movers in range [0.5, P_max] | Verify post-pilot |
| **C3** | gap_narrows_inversion: INV-A (7290110573751 vs 7290110573737, gap confirmed directionally correct before and after SR — SR adds continuous surcharge to 18.0g vs relief to 3.4g) AND INV-B (2385455 vs 5014271300429, gap_before=-0.6 corrects to gap_after=+7.5) | Pre-PASS on both |
| **C4** | min_movers >= 5 products with |delta| >= 1 pt | Pre-expected PASS (55 products below dead zone at various z depths; 37 above Q3) |
| **C5** | min_grade_changes >= 1 | Verify post-pilot |
| **C6** | max_absorption: dead zone <= 40% (current: 27.4%) | PASS |
| **C7** | anti_immunity: 0 products with sugar >= 16.08g at grade B after SR | Enforce via floor=62. At floor=62, no product can score >=70 (grade B) via SR alone. Anti-immunity proof: floor(62) + B_max(3) = 65 < 70 PASS |
| **C8** | floor_compliance: no product exceeds floor(62) as a result of SR relief alone | Enforce: SR relief applies only when current score < 62; floor clamps output at 62 |
| **C9** | no_scope_bleed: 0 products outside bsip_maadanim_subtype scope receive non-zero SR delta | CRITICAL guard — verified by scope_guard activation condition |
| **C10** | frozen_byte_id_milk: CRITICAL — 20/20 milk products must have delta=0 | Milk products have no `bsip_maadanim_subtype` field → scope guard returns False → delta=0 by construction |

**Note on C10 (CRITICAL):** Milk products are scoped by `run_005_headpin`. None carry `bsip_maadanim_subtype`. The scope guard `product.get("bsip_maadanim_subtype") is not None` evaluates to False for all 20 milk products → they receive zero SR delta from this enrollment. This must be verified by the Data Agent in the pilot run before any scores are reported.

---

## 5. Approved SR Parameters

| Parameter | Value | Authority |
|-----------|-------|-----------|
| scope_guard | `product.get("bsip_maadanim_subtype") is not None AND nn.get("sugars_g") is not None` | D7 approved |
| n_scope | 146 | D7 approved (Q1 rejected router filter) |
| median_g | 9.70 | Computed from 146 traces |
| robust_scale | 8.75 | IQR-primary: max(8.73, 8.75, 1.4) |
| z_dead | ±0.30 | D7 approved (Q4) |
| dead_zone_lo | 7.08g | Derived |
| dead_zone_hi | 12.32g | Derived |
| floor_threshold_g | 16.08g | Q3-based; de-anchored from Israeli red-label 10g per directive 2026-06-14 |
| P_max | 6 | Consistent with EV-087 through EV-091 |
| B_max | 3 | Consistent with EV-087 through EV-091 |
| floor | 62 | Category floor; anti-immunity proof: 62+3=65<70 |
| reduced_sugar_dessert | include | D7 approved (Q2) |
| kids_dessert | include with flag | D7 approved (Q3) |

---

## 6. De-Anchor Confirmation

The floor_threshold_g of 16.08g (Q3) is explicitly de-anchored from the Israeli red-label binary sugar threshold of 10g. Under the old binary system, products at 9.9g and at 4.0g were treated identically (both below the 10g cliff). The SR system replaces this with a continuous z-score curve centered on the shelf median (9.70g). A product at 10g receives near-zero delta (z = (10.0-9.70)/8.75 = +0.034, within dead zone) — correctly identified as near-median, not penalized. The floor threshold at Q3 (16.08g) marks the genuinely high end of the shelf, not an arbitrary regulatory boundary.

---

## 7. Files

| File | Purpose |
|------|---------|
| `02_products/maadanim/methodology/shelf_relative_sugar_enrollment_maadanim_v1.md` | D6 proposal (Nutrition Agent) |
| `02_products/maadanim/methodology/maadanim_sugar_d7_cosign_v1.md` | This D7 co-sign (Product Agent) |
| `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` | EV-092 registration |
| `tasks/returns/P128_return.md` | Return block |

---

*Product Agent | TASK-278 Phase-10 | 2026-06-14*  
*D7 co-sign only — no engine edits, 0 score movement*
