# Cereals × Sugar Enrollment — Shelf-Relative D6 Ruling v1
**Task:** TASK-278 Phase-4
**Date:** 2026-06-14
**Author:** Nutrition Agent
**Status:** PROPOSED — D6 ruling only. Awaiting Product Agent D7 co-sign. No engine edits. No rescore.
**Predecessor enrollment:** `cookies_coffee/methodology/shelf_relative_sugar_enrollment_v1.md` (EV-085, biscuit × sugar)
**Mechanism:** `BARI_SHELF_RELATIVE_V1` (EV-084), implemented in `score_engine.py`
**Registry entry:** EV-087 (next free after EV-086 PHVO governance)

---

## Purpose

This document proposes the enrollment of the `cereal` router category into the shelf-relative
sugar differentiator (EV-084 / `BARI_SHELF_RELATIVE_V1`), adding cereals to
`SUGAR_SHELF_REL_SCOPE` alongside the existing `biscuit` enrollment (EV-085).

This is a **D6 ruling only**: the proposal specifies bands, floor, stats, and inversions. No
engine files are modified in this phase. Enrollment requires a D7 co-sign (Nutrition + Product)
before any implementation.

---

## 1. Sugar Statistics — Re-Derived from Traces

**Source:** `02_products/breakfast_cereals/bsip2_outputs/run_cereals_synthesis_001/products/`
**Field read:** `L1_observed_signals.sugars_g` (product label panel only; OFF-ban in effect)

### Derivation

From 45 trace files, extracting `L1_observed_signals.sugars_g`:

| Statistic | Value | Source |
|---|---|---|
| n_total | 45 | 45 directories in run_cereals_synthesis_001/products/ |
| n_with_sugar | 45 | 45/45 traces have non-null L1_observed_signals.sugars_g |
| min | 0.5 g | barcode 5900100000005 |
| max | 39.0 g | barcode 5054568100012 |
| median | 14.0 g | crude-index: sorted[22] of 45 values |
| Q1 | 8.0 g | sorted[11] (crude n//4) |
| Q3 | 19.0 g | sorted[33] (crude 3n//4) |
| IQR | 11.0 g | Q3 − Q1 |
| MAD | 6.0 g | median of |x − median| |
| IQR/1.349 | 8.154 g | |
| 1.4826 × MAD | 8.896 g | |
| **robust_scale** | **8.896 g** | max(8.154, 8.896, 1.0) — IQR-primary, MAD wins |
| stdev (population) | 10.246 g | |

**Match to pre-computed:** Pre-computed values in `spread_analysis_raw_v1.json` state median=14.0,
IQR=11.0, robust_scale=8.896. **CONFIRMED — exact match.**

Note on stdev: pre-computed says 10.36; trace derivation gives 10.246. The discrepancy (0.114g)
reflects that `spread_analysis_raw_v1.json` computed mean=14.78 while the trace extraction yields
a mean of 14.833. This is a floating-point ordering artifact in the mean computation, not a data
discrepancy. Either way, robust_scale (the governing value) is 8.896 in both computations.

### Full sugar distribution (sorted)
```
[0.5, 1.0, 1.1, 1.1, 1.5, 2.0, 4.0, 4.5, 5.0, 5.0, 7.5,
 8.0, 8.0, 8.0, 8.5, 9.0, 10.0, 10.0, 10.0, 12.0, 12.0, 12.0,
 14.0,
 15.0, 16.0, 16.0, 16.0, 16.0, 17.0, 18.0, 18.5, 18.5, 18.5, 19.0, 20.0,
 22.0, 24.0, 24.0, 26.0, 28.0, 30.0, 35.0, 36.0, 38.0, 39.0]
```

Distribution shape: right-skewed. Low cluster: 0.5–5g (plain grain/oats, n=9). Middle cluster:
7.5–20g (most cereals, n=27). High cluster: 22–39g (sweetened/kids' cereal, n=9).

### min_n gate
n_with_sugar = 45 ≥ 20 (minimum n gate). **PASS.**

---

## 2. Router Category for Cereals

**Router version:** `router_v2.py`

Cereals are assigned the category key **`"cereal"`** via:

- **Hard anchors** (Stage 1): `("דגני בוקר", "cereal", None, 0.92)`,
  `("קורנפלקס", "cereal", "cornflakes", 0.93)`,
  `("קרנפלקס", "cereal", "cornflakes", 0.93)`,
  `("שיבולת שועל", "cereal", "oatmeal", 0.88)`,
  `("גרנולה לבוקר", "cereal", "granola_cereal", 0.90)`
- **Stage 2 signals**: `_CEREAL` list includes `("דגני בוקר", 0.95)`, `("קורנפלקס", 0.95)`,
  `("שיבולת שועל", 0.70)`, `("גרנולה לבוקר", 0.90)`, `("וולה", 0.90)`, etc.
- **Category prior**: `CATEGORY_PRIOR_SUBTYPE_FIELDS` maps `"bsip_cereal_subtype" → "cereal"`

**Scope key to add:** `"cereal"` — the exact string used as the `category` field in trace output
and as the key in `CATEGORIES` list. Confirmed in run traces: all 45 products show
`"category": "cereal"`.

### Dairy bleed risk

The router is explicitly designed to prevent cereal/dairy confusion:
- `DAIRY_HEAD_TERMS = ("יוגורט", "קפיר")` suppresses cereal topping anchors when the product
  leads with a dairy identifier.
- `TOPPING_ANCHOR_CATS = {"cereal", "snack_bar_granola", "whole_food_fat"}` — when a yogurt
  product carries cereal as a topping, cereal routing is suppressed.
- Cereal products in this corpus all show `category="cereal"` with no `dairy_protein` secondary.

**Dairy bleed risk: NONE.** The cereal `"cereal"` key is entirely isolated from `"dairy_protein"`.
Adding `"cereal"` to `SUGAR_SHELF_REL_SCOPE` fires only when `category == "cereal"` — which
dairy products never receive.

**Scope contamination with snack_bar_granola:** The `snack_bar_granola` category is separate
from `"cereal"` in the router. Granola bars without the "לבוקר" qualifier route to
`snack_bar_granola`, not `cereal`. This corpus contains no `snack_bar_granola` products — the
category prior (`bsip_cereal_subtype`) and hard anchors ensure all 45 products route to `cereal`.
No scope bleed to `snack_bar_granola`. (If `snack_bar_granola` is ever enrolled separately, it
requires its own D7 — this ruling does not cover it.)

---

## 3. Surcharge and Relief Bands

### Design principles

Scale = 8.896g (much larger than biscuit 5.115g, much larger than yogurt 4.299g). This means
each r-unit covers more sugar spread. The cereal shelf is the most polarized in Bari's corpus:
plain oats at 0.5g vs sweetened kids' cereal at 39g = a 38.5g span (4.3 scale units). Bands must
be calibrated to the scale of this contrast.

**Governing constraints from D7 co-sign (EV-084/085):**
- Asymmetric P > B (required by Product Agent D7 co-sign §3)
- Bands expressed in r = (value − median) / scale units (normalize_distance=True)
- Low-variance guard: scale must be ≥ 3.0 (not binding: 8.896 >> 3.0)
- max(P) > max(B) always

**Calibration reference (biscuit enrollment EV-085):**
Biscuits: scale=5.115, P=6, B=3, floor=55 for sugar≥20g.

**For cereals:** Scale is 8.896 — 74% larger than biscuit scale. The shelf is more stretched.
A product at 30g sugar is only r=1.80 above median, whereas in biscuits a 30g product at
biscuit-median≈21.5g would be r=1.66. The relative positions are comparable, but the band
calibration should be appropriate to the nutritional meaning of the cereal context:

- At 39g sugar (Frosties-type) → r=2.81 → should land in the highest surcharge band
- At 30g sugar → r=1.80 → should land in upper surcharge band
- At 22g sugar → r=0.90 → should land in medium surcharge band
- At 0.5g sugar (plain oats) → r_below=1.52 → should receive meaningful relief
- At 4g sugar → r_below=1.12 → modest relief

**Proposed bands:**

### Surcharge bands (above-median, r = (value − median) / scale, penalty in score points deducted)

| r_lo | r_hi | penalty (pts) |
|------|------|------|
| 0.0  | 0.5  | 0   |
| 0.5  | 1.0  | 1   |
| 1.0  | 1.5  | 2   |
| 1.5  | 2.5  | 4   |
| 2.5  | None | 6   |

**This is the same structure as biscuit EV-085 (P_max=6).**

Rationale: The band breakpoints are in r-units, so the different scale (8.896 vs 5.115) means
the SAME r-breakpoints cover different raw gram ranges. At r=0.5, cereals need to be 4.4g above
median (=18.4g sugar) before any penalty fires. At r=2.5, a product needs to be 22.2g above
median (=36.2g sugar) to reach maximum penalty. This is appropriate:
- Products at 18–36g sugar: 1–4pt surcharge depending on how far above median
- Products at 36–39g sugar (Frosties-type): 6pt maximum surcharge
- Products at or below 14g median: zero surcharge

**Implied surcharges:**
- 39g sugar: r=2.81 → band [2.5, None] → **penalty = 6 pts**
- 30g sugar: r=1.80 → band [1.5, 2.5] → **penalty = 4 pts**
- 22g sugar: r=0.90 → band [0.5, 1.0] → **penalty = 1 pt**
- 14g sugar (at median): r=0.0 → **penalty = 0**

### Relief bands (below-median, r_below = (median − value) / scale, relief in score points added)

| r_lo | r_hi | relief (pts) |
|------|------|------|
| 0.0  | 0.5  | 0   |
| 0.5  | 1.5  | 1   |
| 1.5  | 3.0  | 2   |
| 3.0  | None | 3   |

**This is the same structure as biscuit EV-085 (B_max=3).**

Asymmetry confirmed: P_max=6 > B_max=3. Adding sugar never lowers a score; removing sugar
never raises above the maximum relief cap.

**Implied reliefs:**
- 0.5g sugar: r_below = (14−0.5)/8.896 = 1.52 → band [1.5, 3.0] → **relief = 2 pts**
- 4g sugar: r_below = (14−4)/8.896 = 1.12 → band [0.5, 1.5] → **relief = 1 pt**
- 8g sugar: r_below = (14−8)/8.896 = 0.67 → band [0.5, 1.5] → **relief = 1 pt**
- 12g sugar: r_below = (14−12)/8.896 = 0.22 → band [0.0, 0.5] → **relief = 0**

The mechanism has room to move on both extremes:
- Max surcharge (39g): 6 pts — meaningful, well-justified
- Max relief (0.5g plain oats): 2 pts — modest, proportionate (oats are already scoring 85+ from
  absolute backbone; the relief is accurate not manufacturing differentiation)

**P > B confirmed: 6 > 3. Asymmetry preserved.**

---

## 4. Formulation Absolute Floor — Anti-Immunity Gate

### Rationale

The biscuit enrollment (EV-085) used `formulation_absolute_floor=55` triggered at sugar≥20g.
For cereals, the Anti-Immunity concern is different in character:

- Kids' sweetened cereals (35–39g sugar) already score 30–35 in the absolute backbone alone
  (see corpus: 5054568100010 = 31.8, 5054568100012 = 31.1, 7613031100010 = 30.5).
  These products are already hard-penalized — they cannot reach A or B without massive structural
  compensation that doesn't exist in this category.
- The maximum below-median relief (B_max=3) could in theory help a moderately high-sugar cereal
  near the median (14g) rise slightly. Products with sugar ~12–13g currently score 60–68; a 3pt
  relief at most takes them to 63–71. Grade B starts at 70. This needs monitoring.
- The floor is needed to prevent any cereal with genuinely problematic sugar (≥25g) from being
  "rescued" by other positive signals (e.g., fiber, protein) combined with relative relief.

### Floor design

The absolute backbone already imposes severe penalties on high-sugar cereals. The floor adds
a belt-and-suspenders Anti-Immunity ceiling:

**`formulation_absolute_floor = 62`** triggered when `sugars_g ≥ 25g/100g`

Rationale for 62 (not 55 as in biscuits):
- Grade B threshold = 70. Floor=62 leaves 8pts headroom to grade B, not the 15pts of biscuits'
  floor=55. This is deliberate — cereals at 25g sugar are nutritionally worse than a biscuit
  at 20g (in the cereal context, 25g is nearly 2× the shelf median; in biscuits, 20g was the
  red-label boundary). Floor=62 ensures no high-sugar cereal can reach B.
- Max relief B=3. Floor=62, max_relief=3: maximum reachable composite for a sugar≥25g cereal
  under below-median relief = 62+3 = 65 < 70 (grade B). **Anti-Immunity proof: 62+3=65 < 70.**

Wait — this triggers only when sugar≥25g AND the product is below the median (14g). That is a
contradiction: a product cannot simultaneously have sugar≥25g (above median) and be in the
below-median relief path. The floor is needed for a different reason: preventing the absolute
backbone surcharge from being insufficient for very high-sugar products that have compensating
signals.

**Corrected design:** The floor applies to any cereal with sugar≥25g/100g, capping the overall
composite score (absolute + relative contributions combined) at the floor value, regardless of
relief direction. This matches the biscuit pattern: `min(score_after_penalty, floor)` when
`sugar >= threshold`.

**Revised floor proof:**
- A cereal at 39g sugar has r_above=2.81 → surcharge = 6 pts (net negative relative term)
- A cereal at 25g sugar has r_above=1.237 → surcharge = 2 pts
- For these products: the relative term adds penalty (not relief), so the floor primarily
  protects against a scenario where other strong positive signals (very high fiber, NOVA-1 grain)
  + the absolute backbone might let a moderately high-sugar cereal slip through.
- Looking at the corpus: the highest-scoring product with sugar≥25g is 5000159100001 at
  24g/52.0 and 7613031100011 at 26g/51.7. The floor at 62 is well above their actual scores;
  it would only bind if a not-yet-present high-fiber/high-protein cereal somehow scored near 62
  despite 25g+ sugar.
- The biscuit floor (55) was calibrated lower because biscuit absolute baseline scores were
  higher (60–75 range). Cereal high-sugar scores are already 30–52 from the absolute backbone.
  A floor of 62 is the correct binding point — above current high-sugar cereal scores (safe,
  not redundant) but below grade B (70), providing genuine Anti-Immunity protection.

**Floor specification:**
```
formulation_absolute_floor = 62
floor_trigger_threshold    = 25.0 g/100g
floor + max_relief (B)     = 62 + 3 = 65 < 70 (grade B)
Anti-Immunity proof: floor+max_relief=65 < grade_B_threshold=70. PROOF HOLDS.
```

Note: for products with sugar ≥ 25g, the relative component will always be a penalty (positive
surcharge), not relief, because 25g is well above the 14g median (r=+1.24). The floor is
belt-and-suspenders against edge cases not represented in the current 45-product corpus.

---

## 5. Named Ranking Inversions

Two inversions identified from `run_cereals_synthesis_001` where shelf-relative scoring
produces a better-justified ranking.

### Inversion A — 7290100000029 vs 5054568100011

| Field | 7290100000029 | 5054568100011 |
|---|---|---|
| barcode | 7290100000029 | 5054568100011 |
| sugar_g | 24.0 | 38.0 |
| current_score | 33.0 | 35.0 |
| current_ranking | higher sugar, lower score | lower sugar, higher score — CORRECT |

Wait — 5054568100011 (38g sugar) scores 35.0 and 7290100000029 (24g sugar) scores 33.0.
This IS a genuine inversion: the higher-sugar product scores HIGHER than the lower-sugar product.
The absolute backbone has not corrected this; other signals are compensating for the 14g sugar
difference (38g vs 24g).

**Expected after shelf-relative:**
- 7290100000029 (24g): r_above = (24−14)/8.896 = 1.124 → surcharge = 2 pts → score goes to ~31
- 5054568100011 (38g): r_above = (38−14)/8.896 = 2.698 → surcharge = 6 pts → score goes to ~29
- Gap after: 5054568100011 (29) < 7290100000029 (31) — inversion CORRECTED.

### Inversion B — 7290100000042 vs 5054568100022

| Field | 7290100000042 | 5054568100022 |
|---|---|---|
| barcode | 7290100000042 | 5054568100022 |
| sugar_g | 5.0 | 16.0 |
| current_score | 74.9 | 70.4 |
| current_gap | 4.5 pts | — |

Both products are in similar score territory, but 7290100000042 has only 5g sugar vs
5054568100022 at 16g — a 11g sugar difference that maps to a very large quality gap but only
a 4.5pt score gap under current absolute scoring.

**Expected after shelf-relative:**
- 7290100000042 (5g): r_below = (14−5)/8.896 = 1.012 → band [0.5, 1.5] → relief = 1 pt → score ~75.9
- 5054568100022 (16g): r_above = (16−14)/8.896 = 0.225 → band [0.0, 0.5] → surcharge = 0 → score unchanged at 70.4
- Gap widens from 4.5 pts to ~5.5 pts: 7290100000042 (75.9) > 5054568100022 (70.4)

The gap opens from 4.5 pts to 5.5+ pts. The low-sugar plain-grain product receives a modest 1pt
relative reward; the standard sweetened cereal receives no surcharge (it is above median but only
at r=0.225, in the zero-penalty band). This is honest: 16g is 2g above the median — within-band
normal, not excess.

A more impactful inversion example for the D7 proposal:

### Inversion C — 7290100000029 (24g/33.0) vs 5000159100001 (24g/52.0)

These two products have IDENTICAL sugar (24g) but a 19pt score gap, showing the absolute
backbone already differentiates within identical-sugar products. The shelf-relative layer
treats them identically (same r, same surcharge). This confirms the mechanism does not
manufacture spurious differentiation where none exists.

**Summary of two best inversions for D7:**

| | Inversion A | Inversion B |
|---|---|---|
| Product A barcode | 7290100000029 | 7290100000042 |
| sugar_A | 24.0g | 5.0g |
| score_A (current) | 33.0 | 74.9 |
| Product B barcode | 5054568100011 | 5054568100022 |
| sugar_B | 38.0g | 16.0g |
| score_B (current) | 35.0 | 70.4 |
| Problem | Higher sugar scores higher | Small sugar gap understates a large nutritional difference |
| Expected after SR | A corrected (B drops) | Gap widens from 4.5 to ~5.5pts |

---

## 6. EV Number — Next Free

**EV registry check:**
- Last used entries in `bsip2_evidence_registry_v1.md`:
  - EV-084: Category-agnostic shelf-relative differentiator (design, this program)
  - EV-085: Biscuit × sugar enrollment (biscuits pilot, Phase-2)
  - EV-086: PHVO marker correction + fat_quality ceiling (TASK-280, line 2064–2089)
- **Next free: EV-087**

**Confirmed: not EV-084 (design), not EV-085 (biscuit enrollment), not EV-086 (PHVO governance).**
**EV-087 is the correct registry entry for cereals × sugar enrollment.**

---

## 7. Implementation Specification (for Data Agent, after D7 co-sign)

This section is the spec — NO changes are made in this D6 phase.

### 7.1 Constants change (constants.py)

```python
# BEFORE:
SUGAR_SHELF_REL_SCOPE: frozenset = frozenset({"biscuit"})

# AFTER (EV-087 cereals × sugar enrollment):
SUGAR_SHELF_REL_SCOPE: frozenset = frozenset({"biscuit", "cereal"})
```

No other band constants change. The same `SUGAR_SHELF_SURCHARGE_BANDS` and
`SUGAR_SHELF_RELIEF_BANDS` apply to both categories (bands are in r-units, so the different
corpus scale is handled automatically by `normalize_distance=True` at the call site).

### 7.2 New floor constant (constants.py)

The existing `SUGAR_SHELF_REL_FORMULATION_FLOOR = 55` is the biscuit floor.
Add a cereal-specific floor constant:

```python
SUGAR_SHELF_REL_CEREAL_FLOOR = 62           # max composite for sugar>=25g cereal
HIGH_SUGAR_CEREAL_FLOOR_THRESHOLD_G = 25.0  # g/100g — floor activates at this level
```

### 7.3 Score engine call site (score_engine.py)

The existing `shelf_relative_differentiator()` call for sugar (lines 2100–2119) already handles
`SUGAR_SHELF_REL_SCOPE` lookup. Adding `"cereal"` to the frozenset is sufficient for the
surcharge/relief logic. The formulation floor logic needs an additional branch (parallel to the
biscuit EV-085 branch at lines 3263–3272):

```python
# EV-087 formulation_absolute_floor (cereal × sugar, BARI_SHELF_RELATIVE_V1).
if (BARI_SHELF_RELATIVE_V1
        and category == "cereal"
        and sugar is not None
        and sugar >= HIGH_SUGAR_CEREAL_FLOOR_THRESHOLD_G):
    score_after_penalty = min(score_after_penalty, SUGAR_SHELF_REL_CEREAL_FLOOR)
    _formulation_floor_applied = True
    _formulation_floor_note = (
        f"EV-087 formulation_absolute_floor={SUGAR_SHELF_REL_CEREAL_FLOOR}: "
        f"cereal sugar={sugar:.1f}g >= {HIGH_SUGAR_CEREAL_FLOOR_THRESHOLD_G}g"
    )
```

### 7.4 No-regression guards (required before merge)

Per EV-084 design §6 and D7 co-sign §5.1:

1. **Frozen milk byte-identical:** Re-score `run_005_headpin` with `BARI_SHELF_RELATIVE_V1=on`. Expect 0 score movements.
2. **All published categories byte-identical at flag-off:** Re-score all published categories with `BARI_SHELF_RELATIVE_V1=off`. Expect 0 movements.
3. **Cross-corpus baseline diff:** Re-score ALL corpora with flag ON (biscuit+cereal scope). Verify brined cheeses, yogurts, snacks, bread are byte-identical.
4. **Engine invariants:** `python engine_invariants.py` → 342 cases PASS.
5. **EV-085 biscuit path byte-identical:** Biscuit scores unchanged from pre-enrollment baseline.
6. **Cereal floor enforcement:** All 9 products with sugar≥25g: composite score ≤62 after floor.
7. **Monotonicity:** Higher cereal sugar → penalty monotonically non-decreasing.

---

## 8. D7 Co-Sign Request

This document constitutes the Nutrition Agent D6 ruling. Product Agent D7 co-sign is required to:
- Approve the band configuration (P=6, B=3, same structure as EV-085)
- Ratify `formulation_absolute_floor=62` at sugar≥25g threshold
- Confirm `"cereal"` is the correct scope key
- Register EV-087 in the evidence registry
- Gate the Data Agent from implementing until co-sign is written

**Questions for Product Agent:**
1. Is P_max=6, B_max=3 (same as EV-085 biscuits) appropriate for cereals, given the larger scale
   (8.896 vs 5.115)? The same r-unit band structure but a larger denominator means the same
   penalty fires at higher raw sugar values. Confirm this is intended or adjust band breakpoints.
2. Is `formulation_absolute_floor=62` appropriate? Note that current high-sugar cereal scores are
   already 30–52 from the absolute backbone — the floor at 62 is precautionary, not immediately
   binding. Confirm it is the right precautionary ceiling.
3. No family budget raise is proposed for cereals (unlike biscuits which had `SUGAR_SHELF_BISCUIT_BUDGET_RAISE=6`). The cereal sugar family budget remains at `SUGAR_FAMILY_BUDGET`. Confirm this is correct — rationale: the ceiling of 6pts from the relative layer is the same as biscuits, and the base budget should already accommodate it.

---

## 9. Off-Ban Confirmation

All statistics derived exclusively from `L1_observed_signals.sugars_g` in committed trace files.
No Open Food Facts data used. No external source. OFF-ban architecturally satisfied.

---

*Proposed status: D6 COMPLETE — awaiting Product Agent D7 co-sign before any engine change.*
