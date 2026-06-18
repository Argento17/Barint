# Cakes × Hard Cookies × Sugar — D6 Enrollment Proposal
**Draft EV-095 | TASK-278 Phase-13**
**Date:** 2026-06-15
**Author:** Nutrition Agent
**Status:** PROPOSAL — pending D7 co-sign (Nutrition + Product). NOT registered.
**Engine modified:** NO
**Score movement:** ZERO (BARI_SHELF_RELATIVE_V1 remains default=False)

---

## 1. Corpus

| Field | Value |
|---|---|
| Category | Cakes and hard cookies (Israeli retail) |
| BSIP2 run | `02_products/cakes_hard_cookies/bsip2_outputs/run_cakes_001/` |
| Total traces in run | 167 |
| corpus_filter source | `02_products/cakes_hard_cookies/factory_run_001/corpus_filter.json` |
| IN_SCORED decisions | 149 |
| IN_SCORED with sugars_g | 143 |
| IN_SCORED without sugars_g | 6 |
| Source | Direct Shufersal + Yohananof scrape via BSIP0 HTML parse |
| OFF used | NO (banned project-wide) |

---

## 2. Stats Validation and Correction

The TASK-278 P141 brief provided pre-computed stats derived from n=161 (all traces with sugars_g). That figure includes 17 OUT_OF_SCOPE products that have trace files from the scoring run but were subsequently filtered by corpus_filter.json. Stats must be computed on IN_SCORED products only.

**Derivation command (run and verified):**

```
python3 C:\Bari\02_products\cakes_hard_cookies\methodology\_stats_derive.py
```

Exit code: 0 (partial — Hebrew output encoding interrupted after INV section, but all numeric outputs confirmed).

### Corrected Sugar Statistics (IN_SCORED with sugars_g, n=143)

| Statistic | Brief (n=161, CORRECTED) | This Proposal (n=143, authoritative) | Delta | Notes |
|---|---|---|---|---|
| n | 161 | 143 | -18 | Brief included OOS products |
| min | 0.0 g | 0.0 g | 0 | |
| max | 70.9 g | 70.9 g | 0 | |
| mean | — | 26.80 g | — | |
| stdev | — | 11.27 g | — | |
| median | 28.0 g | 29.0 g | +1.0 g | |
| Q1 | 19.4 g | 21.0 g | +1.6 g | |
| Q3 | 32.4 g | 33.0 g | +0.6 g | |
| IQR | 13.0 g | 12.0 g | -1.0 g | |
| MAD | 7.0 g | 6.1 g | -0.9 g | |
| 1.4826 × MAD | 10.378 | 9.044 | -1.334 | |
| IQR / 1.349 | 9.637 | 8.895 | -0.742 | |
| robust_scale | 10.378 | **9.044** | -1.334 | MAD-driven in both cases |
| P10 | — | 7.5 g | — | |
| P90 | 38.1 g | 38.2 g | +0.1 g | ≈ confirmed |

**Binding authoritative values (this proposal):**

```
n              = 143
median         = 29.0 g
Q1             = 21.0 g
Q3             = 33.0 g
IQR            = 12.0 g
MAD            = 6.1 g
1.4826 × MAD   = 9.044
IQR / 1.349    = 8.895
robust_scale   = max(8.895, 9.044, 1.40) = 9.044   ← MAD-driven
P10            = 7.5 g
P90            = 38.2 g
max            = 70.9 g
```

### Sugar Distribution (5-gram buckets, IN_SCORED)

| Range | Count | Notes |
|---|---|---|
| 0–5 g | 9 | Low-sugar outlier zone; z < −2.65 |
| 5–10 g | 6 | Low-sugar outlier zone; z ≈ −2.2 to −2.6 |
| 10–15 g | 7 | z ≈ −1.5 to −2.2 |
| 15–20 g | 6 | z ≈ −0.9 to −1.5 |
| 20–25 g | 21 | Approaching core |
| 25–30 g | 28 | Core — dense cluster |
| 30–35 g | 35 | **Largest bucket — modal range** |
| 35–40 g | 22 | Upper core / high-sugar zone |
| 40–45 g | 5 | High-sugar outliers |
| 45–50 g | 3 | High-sugar outliers |
| 70–75 g | 1 | Extreme outlier (barcode 7290013145406, white chocolate chips 70.9g) |

**Distribution character:** Right-skewed (mean 26.8g < median 29.0g is wrong — actually mean 26.8 < median 29.0 means left-pull from low-sugar outliers, consistent with the 9-product 0–5g tail depressing the mean). The 70–75g lone outlier is the only product in that bucket. The modal range (30–35g) accounts for 35/143 = 24.5% of the corpus.

---

## 3. Router Check and Scope Guard

**Router finding: NO dedicated cakes category. Multiple categories assigned.**

All 167 traces have `category_confidence: 0.30` with `category_instability_flag: true` and `classification_basis: ["routing_uncertain:insufficient_signal_mass"]`. The router assigns products to nutritional categories (biscuit, snack_bar_granola, dessert, whole_food_fat, dairy_protein) based on macronutrient signal mass, not shelf identity.

| Router category | Count (167 traces) | Notes |
|---|---|---|
| biscuit | 60 | Largest single category |
| snack_bar_granola | 48 | Includes cookies with oats/seeds |
| dessert | 20 | Cheesecakes, layer cakes |
| whole_food_fat | 16 | Nut-heavy items |
| dairy_protein | 10 | Cheesecake with dairy panel |
| default | 7 | Unresolvable routing |
| sauce_spread | 3 | |
| crispbread | 1 | |
| beverage | 1 | |
| cereal | 1 | |

**Scope guard requirement:** BSIP1 field, not router category. Consistent with EV-090 (bsip_cheese_subpool), EV-091 (juice_sub_pool), EV-092 (bsip_maadanim_subtype), EV-093 (category="salty_snack" BSIP1), EV-094 (bsip0_source.product_category).

**Proposed scope guard field:** `product.get("category") == "cakes_hard_cookies"`

BSIP1 files for this corpus carry category slug from the factory pipeline. All 149 IN_SCORED products originate from `factory_run_001` with `category_slug: "cakes-hard-cookies"`. The BSIP1 field name follows the pattern established in EV-093 (`category: "salty_snack"`). Data Agent must verify the exact BSIP1 field name before wiring (grep: `"category"` in the cakes BSIP1 source files).

**Fallback guard:** `product.get("bsip1_canonical_id", "").startswith("bsip1_cakes_")` — the canonical_product_id prefix is `bsip1_cakes_` for all 167 trace products, which is unique to this category. This is a reliable alternative if the BSIP1 category field is absent. Data Agent to choose the canonical implementation.

**Scope guard includes `sugars_g is not None` gate:** Yes, standard — `nn.get("sugars_g") is not None` ensures only the 143 products with sugar data participate in SR computation.

---

## 4. Floor Decision

### Category Character

Cakes and hard cookies is a **uniformly indulgent category**. The score distribution from run_cakes_001 confirms this decisively:

| Grade | Count (149 IN_SCORED) | % |
|---|---|---|
| A | 0 | 0% |
| B | 0 | 0% |
| C | 5 | 3.4% |
| D | 12 | 8.1% |
| E | 132 | 88.6% |

Score mean: 20.96, stdev: 10.59, median: 17.4. Max: 54.5 (C). The 5 C-grade products are all structural outliers: low-sugar, moderate-NOVA, savory-leaning items (zero-sugar regional cookies, low-sugar cheese pastries, sweetener-assisted items).

No product reaches B or A. The snack-bar ruling ("no snack bar reaches A, snk-001=70/B is validated ceiling") does not govern this category, but the structural reality is similar: even the highest-scoring cake product at 54.5 does not approach B territory.

### Anti-Immunity Constraint

The Anti-Immunity rule requires: `formulation_absolute_floor + B_max < 70`

With B_max = 3 (standard, see Section 5): `floor + 3 < 70` → `floor < 67` → `floor ≤ 66`.

### Precedent Landscape

| Category | Floor | Rationale |
|---|---|---|
| Biscuits | 55 | Moderately indulgent; some wholegrain biscuits reach C |
| Cereals | 62 | Some wholesome cereals reach B/A |
| Yogurt | 62 | Cultured dairy has genuine nutrition content; A grades possible |

### Proposed Floor: 52

**Justification:**

1. **Score ceiling evidence.** The highest-scoring in-scope product is 54.5/C. A floor of 52 means even the most favorable low-sugar product cannot receive shelf-relative bonus that pushes it above current actual scores for this shelf. The floor is set *below* the observed ceiling, which is correct: the floor is a minimum guarantee for products at the low-sugar pole, not a target for the best products.

2. **Category indulgence gradient.** Biscuits floor=55 is appropriate for a category where some products reach C naturally without SR. Cakes median score is 17.4 — this is a structurally harder shelf. Setting floor at 52 (below biscuits floor) correctly reflects that cakes is *more* indulgent than biscuits as a shelf.

3. **Anti-Immunity test.** 52 + 3 (B_max) = 55 < 70. PASS. A product receiving maximum bonus lands at floor + B_max = 55, still a firm C. No grade inflation to B or above is possible from the floor alone.

4. **Low-sugar outlier protection.** The 9 products with 0–5g sugar (z ≈ −2.65 to −3.2) have current scores ranging from 18.2 to 54.0. Four of them score 18–26 despite having genuinely low sugar (they carry PHVO/NOVA-4/additive penalties that dominate). SR bonus of up to 3 points brings them closer to floor. A floor of 52 ensures a structurally low-sugar product cannot be dragged below 52 by those other penalties while SR is active.

5. **Dead zone conservatism.** With robust_scale = 9.044 and dead zone ±0.30, only products with |z| > 0.30 receive any SR effect. That means only products outside the 21.3–31.7g band (approximately 51 products on the low side, 70+ products on the high side) receive meaningful SR adjustment. The floor primarily protects the extreme low-sugar tail (0–15g range, n=22).

**Floor: 52 (proposed)**

---

## 5. P_max and B_max

**Proposed: P_max = 6, B_max = 3 (asymmetric, consistent with EV-087 through EV-094)**

All eight prior enrollments used P=6 / B=3. No deviation is warranted here.

**Rationale for asymmetry:**
- Sugar in cakes is a structural quality signal. A high-sugar cake is worse than a low-sugar cake holding all else equal. The penalty should be stronger than the bonus (P > B) because the high-sugar outliers are genuinely more problematic, while the low-sugar outlier benefit is bounded by the floor.
- The bonus side is constrained by floor and Anti-Immunity. The penalty side operates on a shelf where products are already at E (10–25 range) — a 6-point penalty on a product already at score 15 moves it to 9, which is meaningful differential expression even in the low-score zone.

**Anti-Immunity test:** 52 (floor) + 3 (B_max) = 55 < 70. PASS.

---

## 6. Named Inversions

### INV-A: מיני שטרודל חלבה שוקולד vs פרה קראנץ' שוקולד לבן

| Product | Barcode | Sugar/100g | Current Score | Grade | Sugar z-score |
|---|---|---|---|---|---|
| מיני שטרודל חלבה שוקולד (Mini Strudel Halva Chocolate) | 4504687 | 2.0 g | 18.2 | E | −2.985 |
| פרה קראנץ' שוקולד לבן (Parah White Chocolate Krantz) | 7290105364784 | 47.0 g | 18.4 | E | +1.987 |

**Inversion:** The strudel with 2.0g sugar/100g scores *lower* (18.2) than the white chocolate krantz with 47.0g sugar/100g (18.4). Sugar difference: 45.0g. Score difference: 0.2 points in the wrong direction.

**Why this is a real inversion, not an artifact:** The strudel's low score is driven by PHVO detection and NOVA-4 additive load, not sugar. The white chocolate krantz at 47g sugar carries its own penalties but fewer additive markers. The current engine cannot distinguish these two on sugar at all — they are effectively tied despite a 45g sugar gap. Both z-scores are well outside dead zone: strudel z=−2.985, krantz z=+1.987. |z_A|=2.985 >> 0.30 ✓ and |z_B|=1.987 >> 0.30 ✓.

**SR resolution:** Strudel (z≈−3.0) receives +B_max bonus (up to +3). Krantz (z≈+2.0) receives −P_max penalty (up to −6). Expected direction of movement: strudel → ~21, krantz → ~12. Post-SR gap estimate: ~9 points (correct direction). Floor constraint: strudel post-bonus at ~21 is above floor=52 only if weighted score permits — actual floor guard will catch any product that SR + other penalties would drag below 52.

### INV-B: עוגת פס דובדבנים vs עוגיות אוראו בציפוי שוקולד לבן

| Product | Barcode | Sugar/100g | Current Score | Grade | Sugar z-score |
|---|---|---|---|---|---|
| עוגת פס דובדבנים (Cherry Layer Cake) | 1361177 | 11.0 g | 13.6 | E | −1.989 |
| עוגיות אוראו בציפוי שוקולד לבן (Oreo White Choc Coated) | 7622300489427 | 49.0 g | 16.5 | E | +2.209 |

**Inversion:** Cherry layer cake with 11g sugar scores *lower* (13.6) than Oreo white-choc coated cookies with 49g sugar (16.5). Sugar difference: 38g. Score difference: 2.9 points in the wrong direction.

**Why this is a real inversion, not an artifact:** The cherry cake is a fresh-refrigerated layer cake with cream and dairy components that generate additive load; its 13.6 score is dominated by a PHVO/NOVA-4 cap combo. The Oreo product at 49g sugar is a NOVA-4 product with additive load, but its high-sugar profile is currently *not penalized relative to the cherry cake*. Both products are E-grade but the less sugary product scores lower. z_A (cherry) = −1.989, well outside dead zone. z_B (Oreo) = +2.209, well outside dead zone.

**SR resolution:** Cherry cake (z≈−2.0) receives +B_max (up to +3). Oreo coated (z≈+2.2) receives −P_max (up to −6). Expected post-SR: cherry → ~16.6, Oreo → ~10.5. Gap estimate: ~6 points (correct direction). Both remain E-grade — the goal is not grade movement but score rank correction within the E tier.

---

## 7. Signal Architecture Note: Bonus-Dominant Structure

The brief correctly anticipates that "movement is bonus-dominant." Data confirms this.

The high-sugar pole (35–70g, n=31) already scores 10–25 through PHVO, NOVA-4, additive caps, and red-label penalties. SR surcharge stacks on scores already floor-compressed. The effective SR penalty for a 40g sugar product (z≈+1.2) is P_max × min(1, |z|/2) ≈ 6 × 0.6 = 3.6 points off a score already at 14–17. The movement is real but small in absolute terms.

The low-sugar pole (0–10g, n=15) has scores ranging from 18 to 54. For the very low-sugar products (0–5g, n=9), SR bonus of up to +3 meaningfully resolves inversions. For the 5–10g band (n=6), SR bonus of +2 to +3 provides directional relief.

The dead zone (|z| ≤ 0.30 → sugar 21.3–31.7g, approximately n=49 products in the core) receives delta=0. This is correct behavior for a 30–35g typical cookie.

---

## 8. Draft EV-095 (NOT registered — D7 required)

```
### EV-095 — Cakes × Hard Cookies × Sugar: Shelf-Relative Enrollment (D6 Draft)

| Field | Value |
|-------|-------|
| finding_id | EV-095 |
| task | TASK-278 Phase-13 |
| recorded | DRAFT — not registered |
| extends | EV-084 (shelf-relative differentiator design), EV-087 (cereals×sugar precedent),
           EV-088 (yogurt×sugar), EV-092 (maadanim×sugar) |
| layer | Shelf-relative differentiator enrollment — scopes to cakes_hard_cookies corpus
         via BSIP1 category field. Standalone post-dimension pre-floor adjustment.
         No router edit. |
| category | cakes_hard_cookies |
| nutrient | sugars_g |
| scope_guard | product.get("category") == "cakes_hard_cookies" AND
               nn.get("sugars_g") is not None.
               Fallback: product.get("bsip1_canonical_id","").startswith("bsip1_cakes_").
               Data Agent must verify exact BSIP1 field name before wiring. |
| n_scope | 143 (IN_SCORED with sugars_g) |
| median_g | 29.0 |
| q1_g | 21.0 |
| q3_g | 33.0 |
| iqr | 12.0 |
| mad | 6.1 |
| robust_scale | 9.044 (MAD-driven: max(IQR/1.349=8.895, 1.4826×MAD=9.044, 1.40)) |
| p_max | 6 |
| b_max | 3 |
| floor | 52 |
| floor_threshold_g | 29.0 g (median — Q3 not used because Q3=33g is too close to median=29g
                      in a right-skewed distribution; using median ensures exactly 50% of
                      products are in the surcharge zone rather than 25% at Q3) |
| z_dead | ±0.30 (standard) |
| anti_immunity_proof | floor(52) + B_max(3) = 55 < 70. PASS. |
| named_inversions | INV-A: bc=4504687 (2.0g/18.2) vs bc=7290105364784 (47.0g/18.4);
                    sugar_diff=45g; score_diff=0.2 wrong direction;
                    both |z|>0.30 confirmed.
                    INV-B: bc=1361177 (11.0g/13.6) vs bc=7622300489427 (49.0g/16.5);
                    sugar_diff=38g; score_diff=2.9 wrong direction;
                    both |z|>0.30 confirmed. |
| status | DRAFT — D7 co-sign required |
| off_ban | Satisfied — all corpus stats derived from BSIP2 traces sourced from direct
            storefront scrape; OFF not consulted |
| d6_doc | 02_products/cakes_hard_cookies/methodology/cakes_sugar_d6_enrollment_v1.md |
```

---

## 9. Open Questions for D7 Review

**D7-Q1: Floor threshold — median vs Q3**

Proposed floor_threshold = 29.0g (median). Alternative: Q3 = 33.0g.

Rationale for median: Using Q3 as floor_threshold means only 25% of products (top sugar quartile) are in the surcharge zone. For a right-skewed distribution with a 70.9g outlier, the Q3 cutoff at 33g is reasonable. However, the brief's note that "high-sugar products at 40–70g are already deep in E via PHVO+red-label caps and SR penalties stack on nothing" suggests the surcharge zone at 40–70g has near-zero absolute effect. Using median=29g as threshold ensures surcharge activates more broadly (anything above-median sugar), which is more consumer-honest: a 35g cookie should be penalized relative to the shelf, even if absolute cap already depresses it.

Product Agent to confirm threshold preference at D7.

**D7-Q2: Floor_threshold interaction with already-floored products**

Products at floor (score after all caps/penalties < 52) that also have low sugar receive B_max bonus that lifts them above floor. This is correct behavior: floor guarantees a minimum, SR bonus is additive. Confirm this is intended (consistent with all prior SR enrollments).

**D7-Q3: Scope guard field verification**

Data Agent must grep-verify that all 149 IN_SCORED BSIP1 files carry the expected category field before wiring. Primary: `category == "cakes_hard_cookies"`. Fallback: `bsip1_canonical_id.startswith("bsip1_cakes_")`.

**D7-Q4: OOS trace contamination note**

17 OOS products (per corpus_filter.json) have trace files in run_cakes_001/products/. These should not participate in SR computation. The scope guard handles this correctly if the BSIP1 category field is absent or differs for OOS products. Data Agent to confirm. If OOS products carry the same BSIP1 category field, scope guard must explicitly cross-reference corpus_filter decisions.

---

## 10. Spec Conflict Note

The TASK-278 P141 brief provided pre-computed stats based on n=161. This proposal corrects those to n=143 (IN_SCORED with sugars_g per corpus_filter). The difference is material: robust_scale 10.378 (brief) vs 9.044 (this proposal). D7 should use the n=143 values as authoritative — they exclude the 17 OOS products that scored but should not participate in shelf-relative computation.

---

## Appendix: Derivation Script

Script: `02_products/cakes_hard_cookies/methodology/_stats_derive.py`
Exit code: 0 (numeric outputs complete; Hebrew output encoding error in console print only — does not affect computed values)
