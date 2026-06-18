# Hard Cheeses × Sat_Fat — Product Agent D7 Co-Sign (Phase 8 Enrollment)

**Task:** TASK-278 — Project Rescore (Phase 8: hard_cheeses × sat_fat enrollment)
**Date:** 2026-06-14
**Author:** Product Agent
**Verdict: CO-SIGN APPROVED WITH CONDITIONS**
**Scope:** Governance co-sign only. No engine code change. No pilot rescore. Zero score movement.
**Enrollment proposal (D6):** `02_products/hard_cheeses/methodology/shelf_relative_satfat_enrollment_hardcheeses_v1.md`
**Phase-7 D7 reference:** `02_products/cheese_spreads/methodology/cheese_spreads_satfat_d7_cosign_v1.md`
**EV registry:** `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` — EV-090 appended

---

## Verdict: CO-SIGN APPROVED WITH CONDITIONS

The D6 enrollment proposal is sound. Scope A (yellow+yellow_light+hard_grating, n=22) is the correct
calibration group. The tight scale (1.40, at floor) is accepted as an honest finding about the hard
yellow cheese shelf, not a calibration deficiency. The mechanism produces meaningful consumer-visible
corrections for 4 yellow_light outlier products that the absolute backbone currently underweights.
Anti-Immunity holds. Five D6 open questions are resolved below. EV-090 is registered on this co-sign.
The pilot acceptance gate (11 criteria, including 3 scope-bleed criteria) is locked in Section 7.

---

## Section 1 — Q1 (CRITICAL): Scope Choice

### Decision: Option A — Scope A (n=22, yellow+yellow_light+hard_grating, scale=1.40)

**The ruling:** Scope A is adopted. Option B (full corpus n=37, scale=5.93) is rejected.

**Reasoning:**

Option B's scale=5.93 is produced by mixing structurally different cheese types: bulgarians at 2.5g
sat_fat, tzfatit at 3–18g, processed cheese at 7–14g, and full-fat yellow at 17.5–19.5g. This is
cross-group ecological variation, not within-shelf quality variation. The SR mechanism is designed
to correct inversions within a coherent peer group — yellow cheese vs yellow cheese, not yellow cheese
vs bulgarian brined cheese. A median of 17.5g derived from mixing bulgarians and yellows does not
reflect the saturated fat expectation of any single product type on the shelf.

This is the same reasoning that Phase-7 applied when rejecting whole-corpus dairy_protein (n=57,
scale=9.56) in favor of cream_cheese-only (n=24, scale=2.076). The principle is identical: use
the coherent peer group, accept the tighter scale.

Option B also fails on consumer signal: with scale=5.93, the maximum penalty for a 21g parmesan
would be r_above=(21−17.5)/5.93=0.59 → band[0.5,1.0) → −1 pt. A mechanism that gives the
highest-sat-fat product in the corpus only 1 penalty point is miscalibrated. Scope A (scale=1.40)
gives that same parmesan r_above=(21−18.0)/1.4=2.14 → band[1.5,2.5) → −4 pts. That is the
proportionate signal.

**Reversal condition:** If the corpus expands to include more yellow_light variants (via router
correction bringing in dessert-misrouted products that are confirmed yellow or yellow_light), re-run
D6 stats. If the new n≥30 and IQR rises above 3g, revisit whether the scale floor is still binding.

---

## Section 2 — Q2 (CRITICAL): Scale Adequacy

### Decision: Option A — Enroll at scale=1.40 (at floor)

**The ruling:** Enrollment proceeds. The minimum-floor scale is accepted.

**Reasoning:**

The tight scale is a correct finding about the hard yellow cheese shelf, not a calibration error.
Of the n=22 scope products:
- 15 yellow-type products cluster at 17.5–19.5g sat_fat — this is genuine shelf homogeneity
- 4 yellow_light products sit at 5–10g sat_fat — genuine outliers the backbone underweights
- 3 hard_grating (parmesan-type) products sit at 18–21g — above median, penalty zone

The mechanism performs its primary job: the 4 yellow_light outlier products (currently scoring
lower than full-fat peers despite significantly better sat_fat profiles) receive +3 max relief.
This is a meaningful consumer-visible correction. A C→B grade change is within reach for at
least one product (7290000062426 at 64.3/C: +3 → 67.3/C, close to boundary). Even gap-narrowing
without grade change is a legitimate improvement in score accuracy.

The 15/22 yellow cluster products getting delta=0 or ±1 is not a failure — it is correct behavior.
These products are genuinely similar in sat_fat (17.5–19.5g range, IQR=1.5g). SR producing small
deltas for homogeneous products is the mechanism working as designed.

Option B (defer for router fix) is not justified. The router fix timeline is unknown. The 11
misrouted products are already excluded from the SR scope by the `bsip_cheese_subpool` guard — SR
does not interact with them. Deferring a mechanism that correctly fires for 22 products because 11
other products have a router error unrelated to SR is not a proportionate response.

Option C (full corpus scale) is rejected — see Section 1.

**Acknowledged limitation:** robust_scale=1.40 is not organically derived from the empirical spread
(IQR/1.349=1.11 < floor). The floor is doing the calibration work. This means the band thresholds
are set by the minimum guard rather than the data. The pilot gate must confirm that the mechanism
fires correctly and that the near-median dead zone (31.8% of scope products) behaves as expected.
If the pilot shows fewer than 5 scope products with clean_delta≠0, revisit this decision.

**Reversal condition:** If pilot C4 fails (fewer than 5 movers), defer and wait for corpus expansion
from router correction. If pilot C5 fails (0 grade changes), assess whether the investment is worth
the implementation cost for gap-narrowing only.

---

## Section 3 — Q3: Router Correction Sequencing

### Decision: Proceed — SR enrollment does not gate on router fix

**The ruling:** Enrollment proceeds for dairy_protein-routed products. Router correction is tracked
as a separate task.

**Reasoning:**

The `bsip_cheese_subpool` scope guard correctly excludes the 11 dessert-misrouted products from SR
firing. The SR mechanism for the 22 correctly-routed scope products does not interact with the 11
misrouted products in any way — it cannot worsen their already-artifact D scores, and it cannot
correct their routing error. These are genuinely independent concerns.

Blocking enrollment until the router is fixed would impose an unknown delay on a mechanism that
has already been validated within its correct scope. The correct action is to proceed and track
router correction separately.

**For Data Agent:** The router correction for hard cheeses (11 products misrouted to `dessert` —
genuine yellow cheeses including עמק, גאודה, פרמזן variants) is a separate task. The misrouting
occurs because the router fires a "מוס" signal that overrides the hard cheese anchors. This fix
belongs in a separate TASK and should not be part of the Phase-8 wire+pilot implementation.

---

## Section 4 — Q4: Floor Threshold

### Decision: floor_threshold_g = 19.0g (Q3-based) — CONFIRMED

**The ruling:** Q3=19.0g is adopted. The Israeli red-label threshold (15.0g) is explicitly rejected.

**Reasoning:**

The red-label de-anchor directive (owner standing directive 2026-06-14) explicitly moves away from
binary regulatory threshold anchoring. Using the Israeli 15g red-label threshold would floor
approximately 59% of the scope corpus (products at 15–21g) — converting the floor into a de facto
score ceiling that undermines the backbone scoring for the majority of the scope. This is the same
overbuilding failure that Phase-7 rejected when 15g would have floored 67% of cream_cheese products.

At Q3=19.0g, only the top quartile (~14% of scope = approximately 3 hard_grating/parmesan products
at 19–21g) triggers the floor. These are the products with sat_fat meaningfully above the shelf Q3.
The floor is a guard against boundary failures, not a mass override.

**Anti-Immunity proof:** At 19.0g (z=(19.0−18.0)/1.4=+0.714), these products are already in the
penalty zone (r≥0.5 → penalty=1). They are above the median → they cannot receive B_max relief
under SR → the floor+B_max scenario (62+3=65<70) is structurally impossible for the cohort the
floor protects. Anti-Immunity is doubly protected.

**Reversal condition:** If pilot shows any scope product above 19g reaching score above 62 at flag-on
via accumulated relief from other signal paths (which should be impossible structurally), lower
threshold to 17.5g (Q1).

---

## Section 5 — Q5: FAT_QUALITY_FAMILY_BUDGET Raise

### Decision: NO budget raise — FAT_QUALITY_FAMILY_BUDGET remains at 8

**The ruling:** No raise. Cereals/yogurt/cheese_spreads no-raise precedent holds.

**Evidence from trace (bc=7290000062426, score=64.3/C — primary SR beneficiary, yellow_light 9%):**

- `concern_family_coordination.fat_quality.binding_cap = null`
- `concern_family_coordination.fat_quality.coordinated_penalty = 0.0`
- `fat_quality` dimension score = 39.9 (flowing through dimension weight, not through `_coordinate_family()`)
- No fat_pens_fired entries that would consume FAT_QUALITY_FAMILY_BUDGET

With FAT_QUALITY_FAMILY_BUDGET=8 and current coordinated_penalty=0.0 for this product, adding
SR relief of +3pts (as a negative fat_pens entry) has full headroom. No absorption will occur.
The budget is non-binding.

Note: `hp.coordinated_penalty=6.0` IS binding for this product, but hp is the `HP_FAMILY_BUDGET`,
not `FAT_QUALITY_FAMILY_BUDGET`. No interaction with the sat_fat SR term.

**Reversal condition:** If pilot shows SR fires but effective clean_delta < nominal delta for the
primary beneficiaries (suggesting absorption), check fat_pens_fired composition at flag-on and raise
by max(P_max, B_max)=6 if budget saturation is confirmed.

---

## Section 6 — D6 Ratification

### Elements confirmed

**1. Scope guard field — bsip_cheese_subpool confirmed**

The scope guard uses `bsip_cheese_subpool` (BSIP1 input field), not `category_subtype`. This is a
different mechanism from yogurt (uses `category_subtype`) and cheese_spreads (uses `category_subtype`).
It is the same mechanism as brined cheeses (EV-055). Data Agent must confirm the field is accessible
at scoring time in the `nn` dict (see Section 9 implementation note).

**2. Router category — dairy_protein (for scope products)**

22/22 scope products route to `dairy_protein`. The 11 dessert-misrouted products are excluded
by the subpool guard. Confirmed from run_hard_cheeses_001 traces.

**3. Stats confirmed — IQR-primary at floor, scale=1.40**

n=22, median=18.0g, Q1=17.5g, Q3=19.0g, IQR=1.50g, MAD=0.50g, IQR/1.349=1.11,
1.4826×MAD=0.741, robust_scale=max(1.11, 0.741, 1.4)=1.40 (at minimum floor). Confirmed.

**4. Asymmetric P>B confirmed**

P_max=6 > B_max=3. Mandatory design per Phase-1 D7. Ratified.

**5. Floor=62 / threshold=19.0g / Anti-Immunity confirmed** (Section 4 above)

**6. Named inversions confirmed — gap-narrowing is the correct and honest expectation**

Both named inversions use the same barcode_A (7290000062426 = yellow_light 9%, עמק). This is
structurally sound — there is one genuine yellow_light outlier in the corpus, and both inversions
correctly demonstrate how it moves relative to (a) a near-median yellow product (INV-1) and
(b) an above-median grating product (INV-2). Both pairs show directional gap-narrowing.

The pilot C3 criterion tests gap-narrowing, not rank swap. This is the correct design — the
backbone gap in INV-1 (13.3pts) is driven by multi-signal factors beyond sat_fat; SR cannot
and should not eliminate a 13.3pt gap with a 3pt maximum relief.

- INV-1 expected: gap 13.3 → 11.3 (narrows by 2.0pts)
- INV-2 expected: gap 5.6 → 0.6 (narrows by 5.0pts; near-closure)

Both inversions use only BSIP1 trace data. No OFF.

---

## Section 7 — Pilot Acceptance Gate (11 Criteria — Locked)

All criteria must pass before Phase-8 wire+pilot results are accepted. Any hard fail = stop.
C11 is documentation-only (non-blocking).

**Key design difference from cereals/yogurt/cheese_spreads:** This enrollment adds a THIRD call
site in dairy_protein (after yogurt EV-088 and cheese_spreads EV-089). C10b and C10c are NEW
criteria specific to Phase-8, verifying that the hard_cheese SR branch does not bleed into the
other two existing dairy_protein call sites.

| # | Criterion | Name | Pass Condition | Class |
|---|---|---|---|---|
| C1 | directional_distribution | SR direction purity | Mean delta for above-median scope products (sat_fat > 18.0g, non-null) is ≤ 0 AND mean delta for below-median scope products (sat_fat < 18.0g, non-null) is ≥ 0. Tests that SR fires in the correct direction across the scope — penalties for high-sat-fat, relief for low-sat-fat. | Hard |
| C2 | grade_dist_and_magnitude | Grade distribution + magnitude | (A) 0 HARD_CHEESE_YELLOW_SUBPOOLS products with sat_fat ≥ 19.0g reach grade B (score ≥ 70) at flag-on. (B) ≥ 1 scope product with sat_fat ≤ 10g holds grade C or better (score ≥ 52) at flag-on (confirms yellow_light outliers receive SR relief without net penalty). (C) Mean |clean_delta| ≥ 0.5 among SR-firing scope products. All three sub-conditions must hold. | Hard |
| C3 | gap_narrows_inversion | Named inversion gap-narrowing | For BOTH named inversion pairs, gap at flag-on < gap at flag-off: (INV-1) |(7290000062426 flag_on) − (7290000062433 flag_on)| < |(7290000062426 flag_off) − (7290000062433 flag_off)| (expect: 11.3 < 13.3); (INV-2) |(7290000062426 flag_on) − (8866972 flag_on)| < |(7290000062426 flag_off) − (8866972 flag_off)| (expect: 0.6 < 5.6). Direction confirmed: lower-sat-fat product moves toward higher-sat-fat product. Both pairs must show gap reduction. | Hard |
| C4 | min_movers | Minimum movers | ≥ 5 HARD_CHEESE_YELLOW_SUBPOOLS scope products with clean_delta ≠ 0 (SR fired). 4 yellow_light products (5–10g) are predicted at +3 max relief; several yellow products near 18.5–20g are predicted at ±1/±2. 5 movers = minimum above-noise threshold. | Hard |
| C5 | min_grade_changes | Minimum grade changes | ≥ 1 HARD_CHEESE_YELLOW_SUBPOOLS product with grade change at flag-on vs flag-off. Given +3 relief available for bc=7290000062426 (64.3/C → 67.3/C) and +3 for other yellow_light products, a grade change is expected if the engine fires correctly. If no grade change occurs, document and assess whether the investment is justified for gap-narrowing only. | Hard |
| C6 | max_absorption | Absorption rate | ≤ 40% of SR-firing scope products show clean_delta = 0 despite SR term being non-zero before final application. FAT_QUALITY_FAMILY_BUDGET is confirmed non-binding (Q5). > 40% = budget or floor constraint issue — halt and investigate. | Hard |
| C7 | anti_immunity | Anti-Immunity hold | 0 HARD_CHEESE_YELLOW_SUBPOOLS products with sat_fat ≥ 19.0g reach grade B (score ≥ 70) at flag-on. Full scope check. | Hard |
| C8 | floor_compliance | Floor compliance | All HARD_CHEESE_YELLOW_SUBPOOLS products with sat_fat ≥ 19.0g: flag-on score ≤ 62. Full scope check, not spot-check. | Hard |
| C9 | no_scope_bleed | Scope isolation — non-hard-cheese | 0 non-HARD_CHEESE_YELLOW_SUBPOOLS dairy_protein products (yogurt, milk, cottage, white cheese, brined cheese, bulgarian, tzfatit, processed) with non-zero clean_delta from the hard_cheese SR branch. Any delta in non-scope dairy_protein products = scope enforcement failure. | Hard |
| C10 | frozen_byte_id_milk | Frozen milk byte-identity | All milk run_005_headpin products (20 products) show clean_delta = 0.0 at flag-on. Milk scores are a FROZEN INVARIANT (TASK-180A, engine-baseline-2026-06-04). Any milk score movement = immediate pilot FAIL regardless of other criteria. | Hard — CRITICAL |
| C10b | cheese_spread_byte_id | Cheese spreads scope isolation | All CREAM_CHEESE_SPREAD_SUBTYPES products show clean_delta = 0.0 from the hard_cheese SR branch specifically. Hard cheeses and cheese spreads both share the dairy_protein router category. The HARD_CHEESE_YELLOW_SUBPOOLS guard (using `bsip_cheese_subpool`) and the CREAM_CHEESE_SPREAD_SUBTYPES guard (using `category_subtype`) must be mutually exclusive. Any cheese_spread gaining or losing points from the hard_cheese sat_fat branch = scope enforcement failure. | Hard — NEW |
| C10c | yogurt_byte_id | Yogurt scope isolation | All CULTURED_YOGURT_SUBTYPES products show clean_delta = 0.0 from the hard_cheese SR branch specifically. Yogurt SR (EV-088, SUGAR_SHELF_REL_V1 via sugars_g) is a separate call site. The hard_cheese sat_fat SR branch must not fire on yogurt products. Any yogurt product gaining or losing points from the hard_cheese sat_fat branch = scope enforcement failure. | Hard — NEW |
| C11 | flag_off_drift | Flag-off documentation | Flag-off scores for all 22 scope products match run_hard_cheeses_001 committed baseline within ±5 pts. Engine drift from TASK-275 fixes is acceptable if documented; threshold: ≤5 mismatches out of 22 is informational. Documentation-only — non-blocking for gate pass. | Docs only |

### Named Inversions for C3

**INV-1 (same-side gap-narrowing — both below median):**

| Field | Product A (lower sat_fat) | Product B (higher sat_fat) |
|---|---|---|
| Barcode | 7290000062426 | 7290000062433 |
| Product name | עמק צהוב 9% מופחת שומן | עמק גאודה שנה 28% |
| sat_fat_g | 5.5g | 17.5g |
| Median side | BELOW median (18.0g) | BELOW median (18.0g) |
| Expected z | z=−8.93 → r_below=8.93 → band[3.0,∞) → **+3** | z=−0.357 → r_below=0.357 → band[0.3,1.5) → **+1** |
| Expected flag-on score | ~67.3 (C) | ~78.6 (B) |
| Gap at flag-off | 13.3 pts |
| Gap at flag-on | ~11.3 pts |
| C3 pass condition | 11.3 < 13.3 PASS (gap narrows by 2.0pts) |

**INV-2 (opposite-side — A below median, B above median):**

| Field | Product A (lower sat_fat) | Product B (higher sat_fat) |
|---|---|---|
| Barcode | 7290000062426 | 8866972 |
| Product name | עמק צהוב 9% מופחת שומן | גבינה גרוויר 31% |
| sat_fat_g | 5.5g | 19.5g |
| Median side | BELOW median (18.0g) | ABOVE median (18.0g) |
| Expected z | z=−8.93 → r_below=8.93 → band[3.0,∞) → **+3** | z=+1.071 → r_above=1.071 → band[1.0,1.5) → **−2** |
| Expected flag-on score | ~67.3 (C) | ~67.9 (B) |
| Gap at flag-off | 5.6 pts |
| Gap at flag-on | ~0.6 pts |
| C3 pass condition | 0.6 < 5.6 PASS (gap narrows by 5.0pts; near-closure) |

---

## Section 8 — Hard Conditions (All Blocking)

**Carried from Phase-1 D7 co-sign (EV-084) and Phase-7 (EV-089):**

1. EV-084 registered — done at Phase-1 co-sign.
2. Stats formula: `robust_scale = max(IQR/1.349, 1.4826×MAD, 1.4)` — minimum floor 1.4 (raised from 1.0 at Phase-7; confirm engine uses 1.4 as floor, not 1.0).
3. n≥20 guard: PASS (n=22).
4. Asymmetric P>B: P_max=6, B_max=3. Confirmed.
5. `formulation_absolute_floor` non-None: floor=62, threshold=19.0g. Confirmed.
6. Six-guard no-regression plan executes before merge. Guard-1 (milk byte-identical to run_005_headpin) = pilot gate C10 (CRITICAL). Guard-2 (all published categories byte-identical at flag-off) = mandatory.

**Hard_cheeses-enrollment specific (added here):**

7. **Scope guard trace verification:** In the pilot output, at least 4 HARD_CHEESE_YELLOW_SUBPOOLS
   products must show the SR rule tag (`FATSAT_HARDCHEESE_SHELF_REL_V1` or equivalent) firing in
   their BSIP2 trace. Tagless score movement is not auditable and is a gate fail.
8. **bsip_cheese_subpool field accessibility:** Before wiring, Data Agent must confirm `bsip_cheese_subpool`
   is available in the `nn` dict at scoring time (see Section 9). If not accessible, add it to the
   BSIP1→scoring context pass-through before any pilot run.
9. **Three-way dairy_protein isolation check (C10/C10b/C10c):** Explicitly run one milk product
   (e.g., 7290000051352 from run_005_headpin), one yogurt product, and one cream_cheese product
   through the engine with BARI_SHELF_RELATIVE_V1=True. Confirm the HARD_CHEESE_YELLOW_SUBPOOLS-gated
   SR branch does not fire (tag absent, delta=0 from that branch) for all three.
10. **Null-sat_fat pass-through:** Any scope products with null fat_saturated_g must appear in pilot
    output with delta=0 and no FATSAT_HARDCHEESE_SHELF_REL_V1 trace tag.
11. **EV-085/087/088/089 paths byte-identical:** Adding the hard_cheese sat_fat SR branch must not
    move any biscuit, cereal, yogurt, or cream_cheese product's score. Confirm from pilot traces.

---

## Section 9 — Implementation Note for Data Agent

**Scope guard implementation (new pattern — differs from yogurt and cheese_spreads):**

The hard_cheese SR scope guard uses `bsip_cheese_subpool` (a BSIP1 input field), NOT `category_subtype`
(a router-assigned field). This is a critical difference from the yogurt (EV-088) and cheese_spreads
(EV-089) patterns, both of which use `category_subtype`.

**Required constants in constants.py:**
```python
# EV-090: hard_cheeses × sat_fat shelf-relative scope guard (TASK-278 Phase-8)
HARD_CHEESE_YELLOW_SUBPOOLS: frozenset = frozenset({"yellow", "yellow_light", "hard_grating"})
FATSAT_SHELF_REL_HARDCHEESE_MEDIAN: float = 18.0
FATSAT_SHELF_REL_HARDCHEESE_IQR: float = 1.50
FATSAT_SHELF_REL_HARDCHEESE_SCALE: float = 1.4000      # IQR-primary at minimum floor (1.4)
FATSAT_SHELF_REL_HARDCHEESE_FLOOR: int = 62
FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G: float = 19.0
FATSAT_SHELF_REL_HARDCHEESE_P_MAX: int = 6
FATSAT_SHELF_REL_HARDCHEESE_B_MAX: int = 3
```

**Scope guard expression in score_engine.py:**
```python
category == "dairy_protein"
AND nn.get("bsip_cheese_subpool") in HARD_CHEESE_YELLOW_SUBPOOLS
AND fat_saturated_g is not None
```

**CRITICAL pre-implementation check:** Verify that `bsip_cheese_subpool` is accessible at
scoring time via `nn.get("bsip_cheese_subpool")`. If the field is NOT in the `nn` dict (the BSIP1
dict passed to the scoring function), it must be added to the context pass-through before wiring.
Check by reading how `bsip_cheese_subpool` flows from BSIP1 input → the `product` or `nn` dict
in score_engine.py. The D6 doc (Section 7) suggests using `product.get("bsip_cheese_subpool", "")`
in the implementation spec — confirm which dict is the correct access point.

**Placement in score_engine.py:** Add after the EV-089 cheese_spread sat_fat block (approximately
line 2549, or wherever EV-089 is wired). This is the THIRD call site in dairy_protein (after
EV-088 yogurt×sugar and EV-089 cheese_spread×sat_fat).

**FATSAT_SHELF_REL_SCOPE remains `frozenset()`** — no changes to the scope-based path.

---

## Section 10 — Anti-Immunity Proof (Final)

floor = **62**
B_max = **3**
floor + B_max = **65 < 70** (grade B threshold) **PASS**

Additional structural protection: products at or above floor_threshold_g (19.0g sat_fat) are
above the median (18.0g) → they are in the surcharge zone → they cannot receive B_max relief.
The floor+B_max scenario is structurally impossible for the cohort the floor protects.
Anti-Immunity is doubly protected.

---

## Section 11 — Tripwire Assessment

**No tripwire fires on this co-sign.**

- Frozen invariants: not touched. Milk run_005_headpin scores are unchanged. Pilot gate C10
  enforces this at implementation time. Flag default=off. Zero score movement at co-sign.
- Consumer-facing / irreversible: not applicable. Hard_cheeses pilot is internal.
  Owner go-live gate (tripwire-1) is required before any published score movement.
- Major program start/kill: this is Phase 8 of an already-approved program (TASK-278; D7 Phase-1
  co-signed 2026-06-14).
- External commitment/spend/legal: none.
- Strategy redefinition: not applicable.

**Owner escalation: NOT required.** This co-sign is within the D7 lane.

---

## Section 12 — Final Parameters (Locked)

| Parameter | Value | Source |
|---|---|---|
| Nutrient | fat_saturated_g | D6 confirmed |
| Router category | dairy_protein (scope products only) | D6 confirmed |
| Scope guard field | `bsip_cheese_subpool` (BSIP1 input — NOT category_subtype) | D7 Q1 decision |
| Scope guard constant | `HARD_CHEESE_YELLOW_SUBPOOLS = frozenset({"yellow", "yellow_light", "hard_grating"})` | D7 Q1 decision |
| Scope guard expression | `category == "dairy_protein" AND nn.get("bsip_cheese_subpool") in HARD_CHEESE_YELLOW_SUBPOOLS` | D7 Q1 decision |
| n (calibration corpus) | 22 | D6, Scope A only |
| Median | 18.0g | D6 confirmed |
| Scale | 1.4000 (IQR-primary at minimum floor) | D6 confirmed |
| P_max | 6 pts | Standard (EV-084/085/087/088/089) |
| B_max | 3 pts | Standard asymmetric P>B |
| z_threshold | 0.3 | Standard (consistent with all prior enrollments) |
| Floor | 62 | Standard (consistent with cereals/yogurt/cheese_spreads) |
| Floor_threshold_g | 19.0g | D7 Q4 decision (Q3-based) |
| Budget raise | None | D7 Q5 decision (trace confirmed non-binding) |
| Anti-immunity proof | floor(62) + B_max(3) = 65 < 70 PASS | Verified above |
| EV reference | EV-090 | Registered on this co-sign |

---

## Decision Log

| Item | Options considered | Choice | Decisive reason | Reversal condition |
|---|---|---|---|---|
| Q1 — Scope choice | (A) Scope A n=22 scale=1.4; (B) Full corpus n=37 scale=5.93 | (A) Scope A | Full corpus scale driven by cross-group ecological variation (bulgarians at 2.5g vs yellow at 19g), not within-shelf quality variation — same reasoning as Phase-7 rejection of whole-corpus dairy_protein; Option B also produces proportionately weak penalties for the highest-sat-fat products | Reassess if corpus expands to n≥30 with IQR > 3g after router correction |
| Q2 — Scale adequacy | (A) Enroll at scale=1.40; (B) Defer pending router fix; (C) Use full corpus scale | (A) Enroll | 4 yellow_light outliers get genuine +3 relief (consumer-visible correction); Phase-7 precedent accepted tight scale as correct behavior for homogeneous shelf; router fix timeline unknown and orthogonal to SR scope; n=22 passes n≥20 guard | Defer if pilot C4 fails (<5 movers); reassess if pilot C5 fails (0 grade changes) |
| Q3 — Router sequencing | Proceed vs block until router fixed | Proceed | Subpool guard already correctly excludes 11 misrouted products; SR cannot interact with router errors; blocking imposes unknown delay for an orthogonal fix | None — independent concerns |
| Q4 — Floor threshold | (a) 19.0g (Q3-based); (b) 15.0g (Israeli red-label); (c) 21.0g (corpus max−1) | (a) 19.0g | Red-label de-anchor directive; 15g would floor 59% of scope (overbuilding); 21g is so conservative it provides no belt-and-suspenders protection; Q3-based is shelf-calibrated consistent with Phase-7 | Lower if pilot shows 15–19g products systematically exceed score 62 via other signal relief |
| Q5 — Budget raise | No raise vs raise to 14 | No raise | Trace bc=7290000062426 confirms fat_quality.binding_cap=null, coordinated_penalty=0.0; FAT_QUALITY_FAMILY_BUDGET non-binding; cereals/yogurt/cheese_spreads no-raise precedent holds | Raise by 6 if pilot shows absorption for SR-firing products |
| Pilot C3 design | Gap-narrowing vs rank swap vs directional | Gap-narrowing (both pairs) | Named inversions explicitly labelled as partial corrections in D6; full rank swap impossible for INV-1 (backbone gap=13.3pts > max SR range=5pts); near-closure on INV-2 is sufficient | Require full rank swap if a future corpus revision produces a genuine opposite-side pair with backbone gap < 4pts |

---

## EV-090 Registration

EV-090 is registered in `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`
as part of this co-sign. The full entry is appended to the registry by this document.

The D7 decisions above (scope guard = HARD_CHEESE_YELLOW_SUBPOOLS, field = bsip_cheese_subpool,
scale=1.40, floor=62, threshold=19.0g, no budget raise) are the binding parameters for the
implementation in the next phase (wire+pilot rescore by Data Agent).
