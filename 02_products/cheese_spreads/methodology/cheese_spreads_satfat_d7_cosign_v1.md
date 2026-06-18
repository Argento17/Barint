# Cheese Spreads × Sat_Fat — Product Agent D7 Co-Sign (Phase 7 Enrollment)

**Task:** TASK-278 — Project Rescore (Phase 7: cheese_spreads × sat_fat enrollment)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Governance co-sign only. No engine code change. No pilot rescore. Zero score movement.
**Enrollment proposal (D6):** `02_products/cheese_spreads/methodology/shelf_relative_satfat_enrollment_cheesespreads_v1.md`
**Phase-1 D7 reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Phase-4 D7 reference:** `01_framework/bsip2_framework/project_rescore/cereals_d7_cosign_v1.md`
**Phase-6 D7 reference:** `02_products/yogurt_system/methodology/yogurt_sugar_d7_cosign_v1.md`
**EV registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-089 appended

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The D6 enrollment proposal is sound in architecture and scope design. The cream_cheese-only
calibration (n=24, MAD-primary scale=2.0756) correctly reflects the tight structural clustering
of this sub-category. The scope guard mirrors the yogurt precedent exactly. The Anti-Immunity
proof holds.

Five open questions from D6 are resolved below (Sections 1–5). All decisions are made and
binding. EV-089 is registered on this co-sign. The pilot acceptance gate (11 criteria) is
locked in Section 7.

The critical design acceptance: **gap-narrowing, not rank swap, is the correct and sufficient
pilot criterion for this enrollment.** With a tight corpus (IQR=2.60g) and backbone gaps driven
by multi-signal factors beyond sat_fat, the SR mechanism correctly produces partial corrections.
The gate is redesigned accordingly.

---

## Section 1 — D7-CS-01: Scale Adequacy and Scope Choice (Q1 CRITICAL)

### Decision: Option A — Proceed with cream_cheese-only scope (n=24, scale=2.0756)

**The ruling:** Cream_cheese-only calibration is adopted. The tight scale is accepted as
correct behavior, not a deficiency.

**Reasoning:**

Option B (whole-corpus calibration, n=57, scale=9.5626) is structurally wrong. The
whole-corpus scale is driven by cross-group structural differences: cottage cheese at ~3g
vs cream cheese at ~16g are not within-shelf variation to be corrected — they are different
product types in different eating contexts. Applying a whole-corpus median of 5.4g to a
cream_cheese product scoring 16g would generate z=+1.0 → a surcharge, which is incorrect:
16g is the GROUP MEDIAN for cream cheese. This confuses ecological comparison with
within-shelf SR. Option B is rejected.

Option C (defer) is not justified. n=24 passes the n≥20 guard. The mechanism fires on the
outlier products that matter most to consumers: the genuinely lower-fat cream cheese variants
(3–10g) and the maximum-fat products (18–22g). That these constitute a minority of the corpus
is honest — most cream cheese products are tightly clustered at 14–17g, and SR correctly
returns delta=0 for the near-median cluster.

Option D is functionally identical to Option A (delta=0 for the dead zone IS the intended
behavior of the banded mechanism). Option A is the correct framing.

**The tight scale is a correct finding, not a design failure.** The cream_cheese shelf is
genuinely homogeneous at the high end. SR distinguishes the outlier products that are actually
different — light cream cheese variants (7.8g, 3g), herb/flavored reduced-fat (12–14g),
and maximum-fat (18–22g). These are the products where SR adds consumer-visible signal.

**Pilot gate implication:** The gate tests for gap-narrowing and directional firing, not rank
swap. Named inversions show PARTIAL CORRECTIONS only. This is documented, honest, and
acceptable per the P116 precedent (yogurt gate revision accepted directional evidence without
requiring full swap).

**Reversal condition:** If the pilot shows that fewer than 5 cream_cheese products fire SR
with non-zero delta (i.e., the mechanism fires on fewer products than the outlier outlier
products predicted), reassess whether the corpus has sufficient outlier coverage.

---

## Section 2 — D7-CS-02: Scope Guard (Q2)

### Decision: CREAM_CHEESE_SPREAD_SUBTYPES = ("cream_cheese", "cheese_spread") — new constant

**The ruling:** A new named constant `CREAM_CHEESE_SPREAD_SUBTYPES` is required. Hardcoding
the tuple directly is not acceptable — it is less observable and breaks the CULTURED_YOGURT_SUBTYPES
naming pattern that makes scope guards auditable in constants.py.

**Scope guard:**
```python
category == "dairy_protein" AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES
```

where `constants.py` adds:
```python
CREAM_CHEESE_SPREAD_SUBTYPES: tuple = ("cream_cheese", "cheese_spread")
```

**Why a named constant, not an inline tuple:** The yogurt precedent uses `CULTURED_YOGURT_SUBTYPES`
(a named constant in constants.py), not an inline tuple in score_engine.py. Consistency is
mandatory for auditability. A future D7 auditor can grep constants.py and find every SR scope
guard by name. An inline tuple in score_engine.py is invisible in a grep audit.

**Why not add to FATSAT_SHELF_REL_SCOPE:** The existing `FATSAT_SHELF_REL_SCOPE` (currently
`frozenset()`) is a category-level scope, not a subtype-level scope. Adding `"dairy_protein"`
to it would fire for ALL dairy_protein products — cottage, white cheese, milk in mixed runs,
yogurt. The correct pattern is a separate code branch in score_engine.py gated on both
`category == "dairy_protein"` AND `category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES`, parallel
to the yogurt×sugar branch (lines 2125–2148 of the yogurt implementation). FATSAT_SHELF_REL_SCOPE
remains `frozenset()`.

**Interaction with CULTURED_YOGURT_SUBTYPES:** The two constants are mutually exclusive by
subtype value. No cream_cheese or cheese_spread product has a yogurt subtype. No yogurt product
has a cream_cheese or cheese_spread subtype. The scope guards cannot bleed into each other.
This is confirmed by the router_v2.py HARD_ANCHORS logic — each subtype is assigned by distinct
Hebrew anchor terms. C10b in the pilot gate tests this explicitly.

**Reversal condition:** If a router update reassigns any cream_cheese product to a different
subtype, update the constant and re-run D7.

---

## Section 3 — D7-CS-03: Floor Threshold (Q3)

### Decision: floor_threshold_g = 16.5g — CONFIRMED

**The ruling:** The Q3-based threshold (16.5g) is adopted. The Israeli red-label threshold
(15.0g) is not adopted as the floor trigger.

**Reasoning:**

The floor's purpose in this enrollment is Anti-Immunity: preventing a high-sat-fat cream
cheese product from reaching grade B (score ≥ 70) through SR relief or other scoring
gains. High-sat-fat products are in the surcharge zone (above median at 16.05g), so they
receive penalties under SR, not relief. The Anti-Immunity scenario (floor + B_max) requires
a product to simultaneously be above the floor threshold AND receive B_max relief — which
is structurally impossible for products above the median.

The floor is therefore a belt-and-suspenders guard for edge cases: future products, backbone
drift, or SR relief from other family paths. The question is where to set the trigger.

**Why 16.5g, not 15.0g:**

At 15.0g (the Israeli red-label threshold), approximately 67% of the cream_cheese corpus
(~16/24 products) would be floored at 62. This means 16 products cannot score above 62
regardless of their backbone signals. The floor is designed as a guard against boundary
failures, not a mass override. Flooring 2/3 of the corpus is overbuilding — it converts
the floor into a de facto score ceiling for the category, which competes with and undermines
the backbone scoring.

At 16.5g (Q3 + 0.45g), only the top quartile (~6 products) triggers the floor. These are
products with sat_fat meaningfully above the shelf Q3 — genuinely high-fat outliers within
an already-high-fat sub-category. This is the correct precision.

**Red-label vs Q3 framing:** The red-label de-anchor directive (owner standing 2026-06-14)
explicitly moves away from binary regulatory threshold anchoring. Using Q3 of the actual
corpus as the floor trigger is the correct shelf-relative calibration approach.

**Anti-immunity proof holds at 16.5g:** Products at 16.5g+ are above the median (16.05g)
→ in the surcharge zone → cannot receive B_max relief → floor+B_max scenario is structurally
impossible. Belt-and-suspenders still holds because: floor(62) + B_max(3) = 65 < 70. PASS.

**Reversal condition:** If pilot shows products in the 15–16.5g zone systematically exceeding
score 62 via SR relief (which should be impossible given they're near-median surcharge
candidates), lower threshold to 15.0g.

---

## Section 4 — D7-CS-04: Budget Raise (Q4)

### Decision: NO budget raise — FAT_QUALITY_FAMILY_BUDGET remains at 8

**The ruling:** No raise. Follow cereals/yogurt no-raise precedent.

**Evidence from trace (bc=7622201521493, score=52.3, sat_fat=7.8g — the primary beneficiary
of SR relief at +3pts):**

- `concern_family_coordination.fat_quality.coordinated_penalty = 0.0`
- `concern_family_coordination.fat_quality.binding_cap = null`
- `fat_pens_fired` in the trace: SEED_OIL_PRESENT = false (not fired), SATFAT_SHELF_REL_V1 = not yet enrolled
- The sat_fat signal in this product flows through the `fat_quality` dimension score (31.2), not through fat_pens_fired
- The only penalty in the fat family that would fire at SR enrollment is FATSAT_SHELF_REL_V1 (+3 relief = −3 penalty in the budget framework)

With FAT_QUALITY_FAMILY_BUDGET=8 and current fat_pens_fired=0 for this product, adding
SR relief of 3pts (as a negative penalty = positive relief) has full headroom (0 < 8).
No absorption will occur. The budget is non-binding.

**The sat_fat dimension penalty (red_label → −10pts in fat_quality dimension score 31.2)
does not consume FAT_QUALITY_FAMILY_BUDGET.** It flows through the dimension weight
calculation, not through `_coordinate_family()`. Only rules passed to `fat_pens_fired` go
through the budget gate.

**HP_FAT_SODIUM_COMBO in this product fires at 3.0pts** but it is in the `hp` family budget
(`HP_FAMILY_BUDGET`), not FAT_QUALITY_FAMILY_BUDGET. No interaction.

The biscuit precedent (EV-085 raised budget) does not apply here — that raise was triggered
by the HP_SUGAR accumulation pattern specific to biscuits, which is absent in cream cheese.

**Reversal condition:** If the pilot shows absorption (SR fires but effective delta < nominal
delta for high-headroom products), check fat_pens_fired composition at flag-on and raise
by max(P_max, B_max)=6 if budget saturation is confirmed.

---

## Section 5 — D7-CS-05: BSIP1 Pilot Source (Q5)

### Decision: Use run_cheese_003 BSIP1 + current HEAD engine (re-score, not replay run_cheese_004)

**The ruling:** The pilot (P119) scores from BSIP1 files in `03_operations/bsip1/run_cheese_003/output/`
using the current HEAD engine (branch task-275-engine-fixes-abc). It does NOT use run_cheese_004
bsip2_trace.json files as a replay source.

**Reasoning:**

The bsip2_trace files from run_cheese_004 were generated with engine 0.4.1 + BARI_RECAL_P0=on
(2026-06-02). The current engine (task-275-engine-fixes-abc branch) includes TASK-275 fixes.
Using the old traces as a comparison baseline would replicate the cereals P108 harness defect
(stale baseline contamination from engine drift). The clean pilot pattern established in P112
(cereals) and P115 (yogurt) is: run both flag-on and flag-off from the same BSIP1 source
against the SAME current-HEAD engine. This produces a clean differential.

**Confirmed path:** `03_operations/bsip1/run_cheese_003/output/` contains BSIP1 files for
all cheese_spreads products including bc=7622201521493 (confirmed: file
`bsip1_7622201521493.json` exists). The run_cheese_004 bsip2_trace.json `input_reference`
confirms the same BSIP1 source path. The pilot script scores these 59 (or 57 with sat_fat)
products twice: flag_off (BARI_SHELF_RELATIVE_V1=False) and flag_on (BARI_SHELF_RELATIVE_V1=True,
cream_cheese scope wired). Clean delta = flag_on − flag_off.

**No BSIP0 → replay_parse re-run required.** BSIP1 files are the correct and sufficient
input for the BSIP2 scoring engine. The pilot output directory should be named
`run_cheese_005_satfat_pilot` or similar to distinguish from the committed run_cheese_004.

---

## Section 6 — D6 Ratification

### Elements confirmed

**1. Scope guard — CREAM_CHEESE_SPREAD_SUBTYPES confirmed** (Section 2 above)

**2. Router category — dairy_protein confirmed**

All cheese_spreads products route to `dairy_protein`. The two misroutes (snack_bar_granola +
default) noted in D6 are excluded. Confirmed from run_cheese_004 traces.

**3. Stats confirmed — MAD-primary, scale=2.0756**

n=24, median=16.05g, IQR=2.60g, MAD=1.40g. Scale formula: `max(IQR/1.349, 1.4826×MAD, 1.0)`
= max(1.9274, 2.0756, 1.0) = 2.0756 (MAD-primary). Low-variance guard: 2.0756 ≥ 0.5 PASS.

**4. Asymmetric P>B confirmed**

P_max=6 > B_max=3 is the mandatory design per Phase-1 D7. Ratified.

**5. Floor=62 / threshold=16.5g / Anti-Immunity confirmed** (Section 3 above)

**6. Named inversions confirmed — partial corrections are the honest expectation**

Both inversions from D6 are confirmed as structurally real. The partial-correction label is
accurate and correct. This is NOT a D6 sign error (unlike yogurt C3 where both products were
above median). In cream_cheese:

- Inversion 1 (bc=4129118, 14.0g, 56.4pts vs bc=7290116935409, 16.2g, 62.3pts): A has 2.2g
  less sat_fat but scores 5.9pts lower. Backbone gap is driven by multi-signal factors (additive
  quality, NOVA). SR gives A z=−0.988 → near-median band [0.5,1.5) → +1 relief; B z=+0.072,
  |z|<0.3 → delta=0. Gap narrows from 5.9 to 4.9pts. Structurally real, directionally correct.

- Inversion 2-revised (bc=7622201521493, 7.8g, 52.3pts vs bc=4129101, 15.0g, 55.6pts): A has
  7.2g less sat_fat but scores 3.3pts lower. SR gives A z=−3.975 → band [3.0,∞) → +3 max
  relief; B z=−0.506 → band [0.5,1.5) → +1 relief. Gap narrows from 3.3 to 1.3pts. Not a full
  rank swap (gap still positive), but a meaningful partial correction. Directionally correct.

Both inversions qualify as named inversions for the pilot gate (gap-narrowing criterion).

---

## Section 7 — Pilot Acceptance Gate (11 Criteria — Locked)

All criteria must pass before Phase-7 wire+pilot results are accepted. Any hard fail = stop.
C11 is documentation-only (not a blocker).

**Key design difference from cereals/yogurt:** Named inversions show gap-NARROWING, not rank
swap. C3 tests for directional correction and gap reduction, not full reversal.

| # | Criterion | Name | Pass Condition | Class |
|---|---|---|---|---|
| C1 | directional_distribution | SR direction purity | Mean delta for above-median cream_cheese products (sat_fat > 16.05g, non-null) is ≤ 0 AND mean delta for below-median cream_cheese products (sat_fat < 16.05g, non-null) is ≥ 0. Tests that SR fires in the correct direction across the corpus — penalties for high-sat-fat, relief for low-sat-fat — without requiring individual rank swaps. | Hard |
| C2 | grade_dist_and_magnitude | Grade distribution + magnitude evidence | (A) 0 cream_cheese products with sat_fat ≥ 18g reach grade B (score ≥ 70) at flag-on. (B) ≥ 1 cream_cheese product with sat_fat ≤ 10g holds grade C or better (score ≥ 52) at flag-on (confirms low-fat outliers receive relief and are not net-penalized). (C) Mean \|clean_delta\| ≥ 0.5 among SR-firing cream_cheese products (mechanism fires with substance). All three sub-conditions must hold. | Hard |
| C3 | gap_narrows_inversion | Named inversion gap-narrowing | For BOTH named inversion pairs, the gap at flag-on is smaller than the gap at flag-off (gap-narrowing, not rank swap): (Inv-1) \|(4129118 flag_on) − (7290116935409 flag_on)\| < \|(4129118 flag_off) − (7290116935409 flag_off)\|; (Inv-2-revised) \|(7622201521493 flag_on) − (4129101 flag_on)\| < \|(7622201521493 flag_off) − (4129101 flag_off)\|. Direction confirmed correct: lower-sat-fat product moves toward or past the higher-sat-fat product. Both pairs must show gap reduction. | Hard |
| C4 | min_movers | Minimum movers | ≥ 5 cream_cheese-subtype products with clean_delta ≠ 0 (SR fired). Corpus n=24 with sat_fat; outlier products (3–10g below-median, ≥18g above-median) are predicted to fire. 5 movers = the minimum above-noise threshold for a tight-distribution corpus. | Hard |
| C5 | min_grade_changes | Minimum grade changes | ≥ 1 cream_cheese-subtype product with grade change at flag-on vs flag-off. Given the +3 relief available for bc=7622201521493 (52.3→55.3), a grade change is expected if the engine correctly fires SR on this product. | Hard |
| C6 | max_absorption | Absorption rate | ≤ 40% of SR-firing cream_cheese products show clean_delta = 0 despite SR term being non-zero before final application. FAT_QUALITY_FAMILY_BUDGET is non-binding (confirmed from trace), so absorption should be low. > 40% = budget or floor constraint issue — halt and investigate. | Hard |
| C7 | anti_immunity | Anti-Immunity hold | 0 cream_cheese products with sat_fat ≥ 16.5g reach grade B (score ≥ 70) at flag-on. Full corpus check. | Hard |
| C8 | floor_compliance | Floor compliance | All cream_cheese products with sat_fat ≥ 16.5g: flag-on score ≤ 62. Full corpus check, not spot-check. | Hard |
| C9 | no_scope_bleed | Scope isolation | 0 non-cream_cheese dairy_protein products (yogurt, milk, cottage, white cheese, hard cheese, brined cheese) with non-zero clean_delta. Scope bleed could go in both directions: yogurt (CULTURED_YOGURT_SUBTYPES) and milk (dairy_protein but not cream_cheese). Any delta in non-cream_cheese dairy_protein products = scope enforcement failure. | Hard |
| C10 | frozen_byte_id_milk | Frozen milk byte-identity | All milk run_005_headpin products (20 products) have clean_delta = 0.0 at flag-on. Milk scores are a FROZEN INVARIANT. Any milk score movement at flag-on = immediate pilot FAIL regardless of other criteria. The milk scope bleed risk is the same here as for yogurt×sugar — both share dairy_protein router. This is the primary safety gate. | Hard — CRITICAL |
| C10b | yogurt_byte_id | Yogurt scope isolation | All CULTURED_YOGURT_SUBTYPES products included in the pilot run show clean_delta = 0.0 at flag-on from the CREAM_CHEESE_SPREAD_SUBTYPES branch specifically. This is a new criterion: the cheese_spread call site must NOT fire on yogurt products even though both share dairy_protein. If yogurt SR (SUGAR_SHELF_REL_V1) also fires for these products, verify that the clean_delta for the cheese_spread call site (FATSAT_SHELF_REL_V1 branch) specifically is 0. Any yogurt product gaining or losing points from the cream_cheese sat_fat branch = scope enforcement failure. | Hard |
| C11 | flag_off_drift | Flag-off documentation | Flag-off scores for all 57 sat_fat-present cheese_spreads products match run_cheese_004 committed baseline within ±5 pts (engine drift from TASK-275 fixes is acceptable if documented; threshold: ≤10 mismatches out of 57 is informational). Documentation-only — non-blocking for gate pass. Documents engine drift for the record. | Docs only |

### Named Inversions for C3

**Inversion 1 (gap-narrowing):**

| Field | Product A (lower sat_fat) | Product B (higher sat_fat) |
|---|---|---|
| Barcode | 4129118 | 7290116935409 |
| sat_fat_g | 14.0g | 16.2g |
| Current score (flag_off) | 56.4 / C | 62.3 / C |
| Expected z | −0.988 → band[0.5,1.5) → +1 relief | +0.072 → \|z\|<0.3 → delta=0 |
| Expected flag-on score | ~57.4 | ~62.3 |
| C3 pass condition | Gap at flag-on < gap at flag-off: \|57.4−62.3\| = 4.9 < 5.9 PASS (gap narrows from 5.9 to ~4.9) |

**Inversion 2-revised (gap-narrowing):**

| Field | Product A (lower sat_fat) | Product B (higher sat_fat) |
|---|---|---|
| Barcode | 7622201521493 | 4129101 |
| sat_fat_g | 7.8g | 15.0g |
| Current score (flag_off) | 52.3 / C | 55.6 / C |
| Expected z | −3.975 → band[3.0,∞) → +3 max relief | −0.506 → band[0.5,1.5) → +1 relief |
| Expected flag-on score | ~55.3 | ~56.6 |
| C3 pass condition | Gap at flag-on < gap at flag-off: \|55.3−56.6\| = 1.3 < 3.3 PASS (gap narrows from 3.3 to ~1.3) |

---

## Section 8 — Hard Conditions (All Blocking)

**Carried from Phase-1 D7 co-sign (EV-084):**

1. EV-084 registered — done at Phase-1 co-sign (line 1881, confirmed in registry).
2. `compute_shelf_stats()` MAD-primary confirmed for this enrollment. Stats: median=16.05g,
   MAD=1.40g, robust_scale=2.0756. The engine must use: `max(IQR/1.349, 1.4826×MAD, 1.0)`.
3. n≥20 guard: PASS (n=24).
4. Asymmetric P>B: P=6, B=3. Confirmed.
5. `formulation_absolute_floor` non-None: floor=62, threshold=16.5g. Confirmed.
6. Six-guard no-regression plan executes before merge. Guard-1 (milk byte-identical to
   run_005_headpin) = pilot gate C10 (CRITICAL). Guard-2 (all published categories byte-identical
   at flag-off) = mandatory.

**Cheese_spreads-enrollment specific (added here):**

7. **Scope guard trace verification:** In the pilot output, at least 4 cream_cheese-subtype
   products must show the SR rule tag (`FATSAT_SHELF_REL_V1` or equivalent) firing in their
   BSIP2 trace. Tagless score movement is not auditable and is a gate fail.
8. **Non-cream_cheese dairy_protein verification (C9/C10b extension):** Explicitly run one
   milk product (e.g., 7290000051352 from run_005_headpin), one yogurt product, and one cottage
   cheese product through the engine with BARI_SHELF_RELATIVE_V1=True. Confirm the
   CREAM_CHEESE_SPREAD_SUBTYPES-gated SR branch does not fire (tag absent, delta=0 from that
   branch) for all three.
9. **Null-sat_fat pass-through:** The 2 cream_cheese products with null fat_saturated_g must
   appear in pilot output with delta=0 and no FATSAT_SHELF_REL_V1 trace tag.
10. **EV-085 (biscuit), EV-087 (cereal), EV-088 (yogurt) paths byte-identical:** Adding the
    cream_cheese sat_fat SR branch must not move any biscuit, cereal, or yogurt product's score.
    Confirm from pilot traces (non-cream_cheese movers = 0, consistent with C9).

---

## Section 9 — Anti-Immunity Proof (Final)

floor = **62**
B_max = **3**
floor + B_max = **65 < 70** (grade B threshold) **PASS**

Additional structural protection: products at or above floor_threshold_g (16.5g sat_fat) are
above the median (16.05g) → they are in the surcharge zone, not the relief zone → they cannot
receive B_max relief. The floor+B_max scenario is structurally impossible for the cohort the
floor protects. Anti-Immunity is doubly protected.

---

## Section 10 — Tripwire Assessment

**No tripwire fires on this co-sign.**

- Frozen invariants: not touched. Milk run_005_headpin scores are unchanged. The pilot gate
  C10 enforces this at implementation time. Flag default=off. Zero score movement.
- Consumer-facing / irreversible: not applicable. The cheese_spreads category pilot is internal.
  Owner go-live gate (tripwire-1) is required before any published movement.
- Major program start/kill: this is Phase 7 of an already-approved program (TASK-278, D7
  Phase-1 co-signed 2026-06-14).
- External commitment/spend/legal: none.
- Strategy redefinition: not applicable.

**Owner escalation: NOT required.** This co-sign is within the D7 lane.

---

## Section 11 — Final Parameters (Locked)

| Parameter | Value | Source |
|---|---|---|
| Nutrient | fat_saturated_g | D6 confirmed |
| Router category | dairy_protein | D6 confirmed |
| Scope guard constant | `CREAM_CHEESE_SPREAD_SUBTYPES = ("cream_cheese", "cheese_spread")` | D7 Q2 decision |
| Scope guard expression | `category == "dairy_protein" AND cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES` | D7 Q2 decision |
| n (calibration corpus) | 24 | D6, cream_cheese scope only |
| Median | 16.05g | D6 confirmed |
| Scale | 2.0756 (MAD-primary) | D6 confirmed |
| P_max | 6 pts | Standard (EV-084/085/087/088) |
| B_max | 3 pts | Standard asymmetric P>B |
| z_threshold | 0.3 | Standard (consistent with yogurt, cereals) |
| Floor | 62 | Standard (consistent with cereals/yogurt) |
| Floor_threshold_g | 16.5g | D7 Q3 decision |
| Budget raise | None | D7 Q4 decision |
| Pilot BSIP1 source | `03_operations/bsip1/run_cheese_003/output/` | D7 Q5 decision |
| Anti-immunity proof | floor(62) + B_max(3) = 65 < 70 PASS | Verified above |
| EV reference | EV-089 | Registered on this co-sign |

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Q1 — Scale and scope | (A) cream_cheese-only n=24 scale=2.076; (B) whole-corpus n=57 scale=9.563; (C) defer; (D) same as A | (A) cream_cheese-only | Whole-corpus calibration structurally wrong — cross-group ecological variation is not SR signal; tight scale for cream_cheese is a correct finding; n=24 passes n≥20 guard | Reassess if pilot shows <5 movers (insufficient outlier coverage) |
| Q2 — Scope guard | Named constant CREAM_CHEESE_SPREAD_SUBTYPES vs inline tuple | Named constant | Auditable; consistent with CULTURED_YOGURT_SUBTYPES pattern; grep-discoverable in constants.py | None — named constant is always correct here |
| Q3 — Floor threshold | (a) 16.5g (Q3-based); (b) 15.0g (Israeli red-label) | (a) 16.5g | 15.0g would floor 67% of corpus — overbuilding; red-label de-anchor directive moves away from binary regulatory anchor; Q3-based is shelf-calibrated; anti-immunity holds at both | Lower to 15.0g if pilot shows 15–16.5g products exceed score 62 via SR relief |
| Q4 — Budget raise | No raise vs raise to 14 | No raise | Trace confirms FAT_QUALITY_FAMILY_BUDGET=8 entirely unused for primary beneficiary (bc=7622201521493): fat_pens_fired=0, coordinated_penalty=0; sat_fat dimension penalty flows through dimension score, not through _coordinate_family; cereals/yogurt no-raise precedent holds | Raise if pilot shows absorption for fat-family SR products |
| Q5 — Pilot BSIP1 source | run_cheese_003 BSIP1 + current HEAD vs run_cheese_004 bsip2 traces as baseline | run_cheese_003 BSIP1 + current HEAD engine | Clean flag-on vs flag-off differential pattern established in P112/P115; stale baseline contamination avoided; run_cheese_003/output confirmed to contain all required BSIP1 files | None — current HEAD + BSIP1 is always the correct pilot pattern |
| Pilot C3 design | Gap-narrowing vs rank swap vs directional distribution | Gap-narrowing (both pairs) | Named inversions explicitly labelled "partial corrections" in D6; full rank swap structurally impossible at current parameters (backbone gaps > max SR range); yogurt P116 established that directional evidence without full swap is acceptable | Require full rank swap if a future corpus revision produces a genuine below/above-median pair with backbone gap < 3pts |

---

## EV-089 Registration

EV-089 is registered in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
as part of this co-sign. The full entry is appended to the registry by this document.

The D7 decisions above (scope guard = CREAM_CHEESE_SPREAD_SUBTYPES, scale=2.0756, floor=62,
threshold=16.5g, no budget raise) are the binding parameters for the implementation in the
next phase (P119 wire+pilot rescore by Data Agent).
