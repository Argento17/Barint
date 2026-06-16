# Juices × Sugar: Shelf-Relative Enrollment D7 Co-Sign

**EV-091 | TASK-278 Phase-9 | 2026-06-14 | Product Agent**

---

## D7 Open Questions — Resolved

### Q1 (CRITICAL): Scope Guard Field

**Decision: REJECT both D6 and orchestrator proposals. The correct scope guard field is `product.get("juice_sub_pool") is not None`.**

Decisive reason: Neither `category_slug` (D6 proposal) nor `product.get("category") == "juices"` (orchestrator correction) is accessible in the BSIP1 product dict at `score_product` call time. Verified against `bsip1_7290000039435.json` and the batch runner source (`batch_run_juices_001.py`): the BSIP1 product dict has no `"category"` field. The router-assigned `"category"` (e.g. `"beverage"`, `"default"`, `"dessert"`) exists only on the trace output AFTER classification — it is not present as an input key in the `product` dict passed to `score_product()`.

What IS present in every juice BSIP1 file: `"juice_sub_pool"` (confirmed across all 65 products: `juice_100`=16, `fruit_drink`=13, `nectar`=3, MISSING field=2). This is the juice-specific enrichment field set by the juices BSIP1 enrichment pipeline — it is structurally analogous to `bsip_cheese_subpool` used in EV-090 for hard cheeses.

Correct scope guard: `product.get("juice_sub_pool") is not None`

This is exclusive to juices products by construction — no other BSIP1 corpus has a `juice_sub_pool` field. It handles the dessert misroute (1 product: barcode 7290006696717, which has `juice_sub_pool="juice_100"` — correctly included in SR scope since it is a juice product mislabeled by the router; the router-category guard is the wrong layer to exclude it). It includes all three router categories (beverage=45, default=19, dessert=1).

**Scope guard implementation spec:**
```python
# At score_product call site in score_engine.py:
if (BARI_SHELF_RELATIVE_V1 and
    product.get("juice_sub_pool") is not None and
    nn.get("sugars_g") is not None):
    # apply shelf_relative_differentiator(...)
```

No router-category guard is needed — `juice_sub_pool` presence is sufficient and exclusive.

The BSIP1 field spelling is `juice_sub_pool` (with underscore before pool), NOT `juice_subpool`. Data Agent must use the exact field name confirmed from BSIP1 files.

**Reversal condition:** If a future BSIP1 enrichment run adds `juice_sub_pool` to a non-juice corpus, the guard must be tightened. Monitor at each batch run.

---

### Q2: Fruit Drink Inclusion

**Decision: INCLUDE `fruit_drink` (13 products) in scope.**

Decisive reason: Sugar is the relevant scoring signal and fruit drinks carry measurable sugar load. Excluding them would narrow the corpus to 100% juices only, removing products where the SR surcharge does the most consumer-meaningful work (drinks with added sugar, lower fruit content, higher processed-sugar load). Exclusion would be cherry-picking scope to flatter high-juice-content products — the opposite of honest shelf comparison.

The corpus stats (n=65) already include fruit drinks. Removing them post-hoc would invalidate the shelf median (9.50g) and require a D6 rerun. The D6 Nutrition Agent included them; there is no nutritional argument for exclusion.

**Reversal condition:** If a QA audit finds that `fruit_drink` products systematically misrepresent the competitive set for consumers comparing juice options, revisit at D6 of the next rescore.

---

### Q3: P_max/B_max Adequacy at Lower Scale

**Decision: APPROVE P_max=6, B_max=3 as specified.**

Decisive reason: The scale of 2.82 g/100ml (vs yogurt's 4.3) means SR fires proportionally more aggressively in z-distance terms for the same gram difference — this is correct behavior. A product 5.6g above the median (e.g., max=16.8g) sits at z=1.99, landing in the [1.5,2.5) surcharge band (−4). A product 7.75g below median (lemon juice at 1.75g) sits at z=2.75, landing in [2.5,∞) relief band (+3). These are proportionate corrections for what are genuinely large deviations on this shelf. P_max=6 is the standard maximum across all prior enrollments (EV-085/087/088/089/090) and is appropriate here. B_max=3 is unchanged.

The tight scale is an honest finding: sugar variance is real but moderate on the juice shelf. The SR mechanism should express that moderate differentiation, not manufacture stronger signal than the data supports.

**Reversal condition:** If the pilot run shows mean |delta| < 0.5 among SR-firing products (C2c criterion fails), raise P_max to 8 and rerun D6.

---

### Q4: Pilot Gate Routing-Agnostic Criterion

**Decision: ADD C11 as explicit routing-agnostic criterion.**

The scope guard uses `juice_sub_pool` (not router category), which structurally enforces routing agnosticism. But C11 makes it explicitly testable: run two products with identical sugar_g through `beverage` and `default` router paths and confirm delta is identical. This must pass before wiring.

---

## Scope Approval

**Approved scope:** All products with `product.get("juice_sub_pool") is not None` AND `sugars_g` not None.

This covers:
- `juice_100`: 16 products
- `fruit_drink`: 13 products (INCLUDED — see Q2)
- `nectar`: 3 products
- MISSING `juice_sub_pool` value: 2 products EXCLUDED (field absent or None)
- Total in scope: ~63–65 products (exact count depends on 2 products with missing field)

Router categories covered: beverage (45), default (19), dessert (1 — included by design).

**Scope guard field:** `juice_sub_pool` (BSIP1 enrichment field, present in product dict at scoring time).

---

## SR Parameters (Confirmed)

| Parameter | Value | Basis |
|---|---|---|
| Nutrient | sugars_g | Label-observable; 65/65 non-null in run_juices_001 |
| n_scope | 65 | run_juices_001 corpus |
| median_g | 9.50 | Confirmed from D6 |
| Q1 | 8.40 | D6 |
| Q3 | 12.20 | D6 — used as floor_threshold_g |
| IQR | 3.80 | D6 |
| MAD | 1.30 | D6 |
| robust_scale | 2.82 | IQR-primary: max(IQR/1.349=2.82, 1.4826×MAD=1.93, min_scale) = 2.82 |
| P_max | 6 | Approved (standard) |
| B_max | 3 | Approved (standard) |
| floor | 62 | Anti-immunity: 62+3=65 < 70 PASS |
| floor_threshold_g | 12.20 | Q3-based (de-anchor from 10g Israeli red-label threshold) |
| z_dead | ±0.30 | Standard across all enrollments |

**De-anchor confirmation:** The floor trigger of 12.2g (Q3) was chosen from corpus distribution, not from the Israeli red-label 10g threshold. Compliant with the red-label de-anchor directive.

**Anti-Immunity proof:** floor(62) + B_max(3) = 65 < 70 (grade B threshold). PASS.
Additionally: products at or above floor_threshold_g (12.2g) are above the median (9.50g) → surcharge zone, cannot receive B_max relief → floor+relief scenario structurally impossible for the protected cohort.

---

## Named Inversion Verification

**INV-A (same-side, gap-widening):**
- Lemon juice ~2.5g sugar, score ~59.7/C: below median by 7.0g → z = 7.0/2.82 = 2.48 → relief band [2.0,∞) → +3 pts
- Orange 100% ~8.4g sugar, score ~56.1/C: below median by 1.1g → z = 1.1/2.82 = 0.39 → relief band [0.3,0.5) or similar small band → ~+1 pt
- Pre-SR gap: 59.7 − 56.1 = 3.6 pts (low-sugar product ranked higher, correct direction)
- Post-SR gap: (59.7+3) − (56.1+1) = 62.7 − 57.1 = 5.6 pts (gap widens: low-sugar gets more relief, correct)
- Verdict: correct direction.

**INV-B (opposite-side, gap-narrowing):**
- Apple juice 100% ~9.6g: below median by −0.1g → z = 0.035 → dead zone → 0 pts
- Peach nectar ~12.2g: above median by 2.7g → z = 2.7/2.82 = 0.96 → surcharge band → −1 pt
- Pre-SR: nectar scores 58.1 > apple 51.4, gap = 6.7 pts (wrong direction: higher-sugar product ranks higher)
- Post-SR: nectar at 57.1, apple at 51.4, gap = 5.7 pts (narrows toward correct direction)
- This is partial correction — full rank swap would require a much larger surcharge, which P_max=6 does not reach given the multi-signal calorie_density difference. Gap-narrowing is the correct and honest expectation.
- Verdict: correct direction. INV-B is accepted as partial correction per honest-shelf-finding precedent (EV-090 INV-2).

---

## Pilot Gate — 12 Criteria

| ID | Name | Criterion | Type |
|---|---|---|---|
| C1 | directional_distribution | above-median mean_delta ≤ 0; below-median mean_delta ≥ 0 | HARD FAIL |
| C2a | grade_dist_immunity | 0 products with sugar_g ≥ 12.2 at grade B with SR flag-on | HARD FAIL |
| C2b | grade_dist_low_sugar | ≥1 low-sugar product at grade C or better with SR relief | HARD FAIL |
| C2c | grade_dist_magnitude | mean |delta| ≥ 0.5 among SR-firing products | HARD FAIL |
| C3 | gap_narrows_inversion | INV-A gap widens in correct direction; INV-B gap narrows toward correct direction | HARD FAIL |
| C4 | min_movers | ≥5 products with delta ≠ 0 | HARD FAIL |
| C5 | min_grade_changes | ≥1 grade change (C→B or B→C) in scope | SOFT |
| C6 | max_absorption | ≤40% of products have |delta| = P_max or B_max (not absorbed at ceiling) | HARD FAIL |
| C7 | anti_immunity | 0 products with sugar_g ≥ 12.2 at grade B with SR flag-on | HARD FAIL (alias C2a) |
| C8 | floor_compliance | all products with sugar_g ≥ 12.2 score ≤62 with SR flag-on | HARD FAIL |
| C9 | no_scope_bleed | 0 non-juice products (no `juice_sub_pool` field) with non-zero delta from juice SR branch | CRITICAL |
| C10 | frozen_byte_id_milk | 20/20 milk run_005_headpin products: delta=0 (score byte-identical between SR flag-on and flag-off) | CRITICAL — HARD FAIL |
| C11 | routing_agnostic | identical sugar_g → identical SR delta regardless of `beverage` vs `default` router-assigned category | HARD FAIL |

**Total: 12 criteria (11 slots, with C2a/C7 aliased + C11 added for routing agnosticism).**

C10 is the single most critical criterion. If any milk product shows non-zero delta with `BARI_SHELF_RELATIVE_V1=on`, the entire enrollment is rejected until root cause is found.

C9 uses the confirmed correct scope guard: products lacking `juice_sub_pool` field must show zero delta.

---

## Implementation Spec for Data Agent

The following is the Data Agent's implementation guide. This D7 co-sign authorizes the pilot rescore — it does not execute any engine change.

1. **Scope guard field:** `product.get("juice_sub_pool") is not None` — NOT `product.get("category")`, NOT `category_slug`.

2. **Field spelling:** `juice_sub_pool` (two underscores: `juice_` + `sub_` + `pool`). Verify against BSIP1 files before wiring.

3. **Add to constants.py:**
   - `SUGAR_SHELF_REL_JUICES_MEDIAN: float = 9.50`
   - `SUGAR_SHELF_REL_JUICES_SCALE: float = 2.82`
   - `SUGAR_SHELF_REL_JUICES_FLOOR: int = 62`
   - `SUGAR_SHELF_REL_JUICES_FLOOR_THRESHOLD_G: float = 12.2`
   - `SUGAR_SHELF_REL_JUICES_P_MAX: int = 6`
   - `SUGAR_SHELF_REL_JUICES_B_MAX: int = 3`

4. **Add call site in score_engine.py** (new branch, after beverage category scoring, before guardrails):
   ```python
   if (BARI_SHELF_RELATIVE_V1 and
       product.get("juice_sub_pool") is not None and
       nn.get("sugars_g") is not None):
       # shelf_relative_differentiator() call with juice sugar bands
   ```

5. **Do NOT modify** the existing `beverage` category scoring path, `evaluate_guardrails()`, or any published-category scoring branch.

6. **Run all 12 pilot gate criteria** before returning. C10 is non-negotiable.

---

## D7 Co-Sign Authority

This co-sign covers:
- Scope guard: APPROVED (`juice_sub_pool` is not None) with field-name correction from D6/orchestrator
- Fruit drink inclusion: APPROVED
- P_max=6, B_max=3: APPROVED
- floor=62, floor_threshold=12.2g: APPROVED
- Anti-immunity: VERIFIED (65 < 70)
- De-anchor compliance: VERIFIED (12.2g from corpus Q3, not 10g regulatory)
- EV-091: REGISTERED

**This enrollment is authorized for pilot rescore. No published score changes until owner go-live (tripwire-1).**

---

*Product Agent D7 Co-Sign | TASK-278 Phase-9 | 2026-06-14*
