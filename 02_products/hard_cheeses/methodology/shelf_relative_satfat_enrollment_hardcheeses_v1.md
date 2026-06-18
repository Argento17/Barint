# Shelf-Relative Sat_Fat Enrollment — Hard Cheeses Category
## D6 Design Proposal — Awaiting D7 Co-Sign (Nutrition Agent + Product Agent)

**EV Number:** EV-090 (draft — DO NOT register until D7 + orchestrator acceptance)
**Status:** D6 PROPOSAL — no engine edits, no score movement, no pilot wiring
**Author:** Nutrition Agent
**Date:** 2026-06-14
**Task:** TASK-278 Phase-8
**Authoritative corpus:** `run_hard_cheeses_001` (37 products, Shufersal+supplementary, 2026-06-08)
**Prior context:** Rollout spread analysis `rollout_spread_analysis_v1.md` (#2 ranked LAND candidate)
**Preceded by:** Phase-7 (cheese_spreads×sat_fat, EV-089)

---

## 1. Background and Authoritative Run

The rollout spread analysis ranked hard_cheeses×sat_fat as the **#2 LAND candidate** (composite=16.9,
score_stdev=17.35, 2.7% floored). Sugar was ruled out as the lever (near-zero IQR=1.0g); sat_fat is
the correct nutrient (IQR=8.0g across full corpus, scale=5.9).

### Authoritative Run

| Field | Value |
|---|---|
| Run ID | `run_hard_cheeses_001` |
| Path | `02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_001/` |
| Date generated | 2026-06-08 |
| Engine | proto_v0 / 0.4.1 + BARI_RECAL_P0=on |
| Source | Shufersal scrape + supplementary → BSIP1 run_hard_cheeses_001 |
| Total products | 37 |
| All with sat_fat data | 37 (100% coverage) |
| Products scored | 37 |

Source of fat_saturated_g: exclusively `L1_observed_signals.fat_saturated_g` in committed trace
files — direct product scrape. OFF is not used.

**Note on `run_hard_cheeses_yohananof_001`:** A second run exists (67 products, Yohananof storefront,
2026-06-08) with 37/67 products classified as `insufficient_data`. This run has a high misroute rate
(12/67 = 17.9%) and 55% insufficient-data rate. It is not used as the calibration corpus — `run_hard_cheeses_001` is authoritative for this D6 proposal, as it was the reference for the rollout spread analysis.

---

## 2. Critical Architectural Finding: Router Category Heterogeneity

### 2.1 The Problem

Unlike cheese_spreads (which is a unified `dairy_protein` shelf with subtype discrimination), the hard_cheeses
corpus has severe **router category heterogeneity**:

| Router category | Count | Products |
|---|---|---|
| `dairy_protein` | 25 | Correctly-routing yellow cheeses, yellow_light, bulgarians, tzfatit, processed |
| `dessert` | 11 | Misrouted yellow cheeses (עמק, גאודה, פרמזן) — router fires "מוס" signal |
| `whole_food_fat` | 1 | גבינה צפתית 28% — routed by fat content |

The 11 `dessert`-routed products are genuine hard cheeses (yellow blocks, parmesan) that the router
misclassifies. Their 39.0/D scores are an artifact of this misrouting (dessert calorie/sugar penalties
applied to cheese), NOT a reflection of sat_fat quality. A shelf-relative SR term applied only to
`dairy_protein` products would exclude these 11 misrouted products — which is actually correct behavior
(SR cannot fix a router error; it can only refine within correctly-routed products).

### 2.2 The `bsip_cheese_subpool` Field

The BSIP1 input files carry a `bsip_cheese_subpool` field that categorizes each product:

| Subpool | n | Sat_fat range | Character |
|---|---|---|---|
| `yellow` | 15 | 17.5–19.5g | Full-fat hard yellow cheeses (עמק, גאודה, אמנטל, קולבי, גרוויר) |
| `yellow_light` | 4 | 5.0–10.0g | Reduced-fat yellow cheese variants (9%, 16%) |
| `hard_grating` | 3 | 18.0–21.0g | Grated/aged hard cheeses (פרמזן) |
| `bulgarian` | 7 | 2.5–10.5g | Bulgarian brined-type cheese |
| `tzfatit` | 4 | 3.0–18.0g | Tzfatit (צפתית) cheese |
| `processed` | 4 | 7.0–14.0g | Processed cheese slices/blocks |

**This field is available in BSIP1 inputs and flows through to scoring-time context** via the same
mechanism as `bsip_cheese_subpool` for brined cheeses (EV-055: `"bsip_cheese_subpool": "dairy_protein"`
category prior in router_v2.py lines 595–600). The field is NOT currently stored in BSIP2 trace JSON
(same situation as `category_subtype` in the cheese_spreads case) but IS accessible at scoring time.

### 2.3 Scope Guard Design

**Option A — True hard cheese scope: `yellow + yellow_light + hard_grating` (RECOMMENDED)**

Scope gate:
```python
category == "dairy_protein"
AND product.get("bsip_cheese_subpool") in HARD_CHEESE_YELLOW_SUBPOOLS
```
where:
```python
HARD_CHEESE_YELLOW_SUBPOOLS: frozenset = frozenset({"yellow", "yellow_light", "hard_grating"})
```

This covers n=22 products: the genuine hard yellow cheeses and their reduced-fat variants, plus
aged grating cheeses. It excludes bulgarians (brined-type, already partially handled by EV-055
sodium mechanism), tzfatit (heterogeneous sat_fat 3–18g), and processed cheese (structurally
different product class).

**Rationale:** The SR mechanism should compare products within a nutritionally coherent peer group.
Bulgarians and tzfatit at 3–10g sat_fat do not belong in the same calibration group as full-fat
28% yellow cheeses (17.5–19g sat_fat). Mixing them would produce a median that is not meaningful
for either group.

**Option B — Full corpus: all 37 products routing to dairy_protein**

No subpool guard. This was what the rollout_spread_analysis used (n=37, IQR=8g, scale=5.93).
Mixes fundamentally different cheese types but has better statistical properties.

**Decision for D7:** See §7 (D7 open questions). This is the most consequential scope call.

---

## 3. Corpus Statistics

All statistics are computed from BSIP1 `fat_saturated_g` values in the authoritative `run_hard_cheeses_001`
corpus. Source: direct product scrape → BSIP0 → BSIP1. No external source.

### 3.1 Scope A Statistics (Recommended: yellow + yellow_light + hard_grating, n=22)

| Statistic | Value |
|---|---|
| n (with non-null sat_fat) | 22 |
| n gate (≥20) | **PASS** |
| Min | 5.0g |
| Max | 21.0g |
| Median | 18.0g |
| Q1 | 17.5g |
| Q3 | 19.0g |
| IQR | 1.50g |
| MAD | 0.50g |
| IQR/1.349 | 1.1119 |
| 1.4826 × MAD | 0.7413 |
| min_scale_floor | 1.4 |
| **robust_scale = max(IQR/1.349, 1.4826×MAD, 1.4)** | **1.4000 (at floor, IQR-primary below floor)** |
| stdev | 4.83g |
| Near-median dead zone (\|z\|<0.3) | 31.8% (7/22 products at exactly 18.0g) |

**Scale concern (CRITICAL for D7):** The robust_scale=1.40 hits the minimum floor. This occurs
because the `yellow` cluster is extremely tight (15 of 22 products at 17.5–19.5g) while the
`yellow_light` outliers (5.0–10.0g) are far below. IQR/1.349=1.11 is below the minimum floor of
1.4. The floor prevents division-by-zero and unstable banding, but signals that the calibration is
dominated by the minimum guard rather than the empirical spread of the yellow cluster.

**Practical implication:** With robust_scale=1.4, the near-median dead zone (|z|<0.3) spans
17.58–18.42g. Products at 17.5g (Q1) are at z=-0.357 (barely outside the dead zone), getting
relief=1. Products at 19.0g (Q3) are at z=+0.714, getting penalty=1. Products at 5–10g
(yellow_light outliers) are at z values of -5.7 to -9.3 — maximum relief=3. The mechanism
primarily differentiates the outlier reduced-fat products from the tight full-fat cluster.

### 3.2 Alternative: Full Corpus Statistics (n=37, if D7 expands scope)

| Statistic | Value |
|---|---|
| n | 37 |
| Min | 2.5g |
| Max | 21.0g |
| Median | 17.5g |
| Q1 | 10.0g |
| Q3 | 18.0g |
| IQR | 8.00g |
| MAD | 3.50g |
| IQR/1.349 | 5.9303 |
| 1.4826 × MAD | 5.1891 |
| **robust_scale = max(...)** | **5.9303 (IQR-primary, well above floor)** |
| stdev | 5.62g |
| Near-median dead zone (\|z\|<0.3) | 45.9% (17/37) |

This is the distribution referenced in `rollout_spread_analysis_v1.md` (scale=5.9). It mixes
heterogeneous cheese types but has mechanically sound statistics. The median=17.5g is close to the
Israeli red-label sat_fat threshold of 15g/100g (scale separates products across a meaningful
nutritional range).

---

## 4. Band Design

Following Phase-7 pattern. Direction is `penalize_high` (asymmetric: above-median sat_fat → penalty,
below-median → relief).

| Parameter | Value | Rationale |
|---|---|---|
| P_max | 6 pts | Standard across all enrollments (EV-085/087/088/089) |
| B_max | 3 pts | Standard asymmetric P>B (C3 recommendation, D7 ratified) |
| Near-median z-threshold | 0.3 | Standard: \|z\|<0.3 → delta=0 |
| direction | asymmetric | Below-median reduced-fat products deserve relief; above-median full-fat products get penalty |
| normalize_distance | True | Bands in r-units (z-score normalized), consistent with all prior enrollments |

### 4.1 Band Tables (using Scope A, robust_scale=1.4)

**Surcharge bands** (r_above = (sat_fat − 18.0)/1.4, above-median only):

| r range | Penalty | Sat_fat threshold | Note |
|---|---|---|---|
| [0, 0.3) | 0 | 18.0–18.42g | Dead zone |
| [0.3, 0.5) | 0 | 18.42–18.70g | Near-median |
| [0.5, 1.0) | -1 | 18.70–19.40g | Mild penalty (most 19g products) |
| [1.0, 1.5) | -2 | 19.40–20.10g | Moderate penalty |
| [1.5, 2.5) | -4 | 20.10–21.50g | Strong penalty (parmesan 21g) |
| [2.5, ∞) | -6 | 21.50g+ | Max penalty |

**Relief bands** (r_below = (18.0 − sat_fat)/1.4, below-median only):

| r range | Relief | Sat_fat threshold | Note |
|---|---|---|---|
| [0, 0.3) | 0 | 17.58–18.0g | Dead zone |
| [0.3, 1.5) | +1 | 16.20–17.58g | Mild relief |
| [1.5, 3.0) | +2 | 13.80–16.20g | Moderate relief |
| [3.0, ∞) | +3 | <13.80g | Max relief (yellow_light at 5–10g) |

### 4.2 Band Tables (if D7 approves full corpus, robust_scale=5.93)

Thresholds shift substantially with the larger scale — these are informational for D7:

| r range above median (17.5g) | Penalty | Sat_fat approx |
|---|---|---|
| [0, 0.5) | 0 | 17.5–20.5g (dead + near-median) |
| [0.5, 1.0) | -1 | 20.5–23.5g |
| [1.0, 1.5) | -2 | 23.5–26.5g |
| [1.5, 2.5) | -4 | 26.5–32.3g |
| [2.5, ∞) | -6 | 32.3g+ |

With this calibration, essentially no product in the current corpus (max=21g) would receive more than
a -1 penalty — the scale is calibrated for a much wider spread than the actual corpus exhibits.

---

## 5. Floor Design and Anti-Immunity Proof

### 5.1 Floor Rationale

Sat_fat is an endemic dairy nutrient (inherent in the product class). The floor prevents high-sat-fat
products from receiving SR relief via other scoring dimensions.

| Parameter | Value | Rationale |
|---|---|---|
| floor | 62 | Standard across all SR enrollments (cereals, yogurt, cheese_spreads) |
| floor_threshold_g | 19.0g | Q3 of Scope A — top quartile of the hard cheese corpus |

**Floor threshold rationale:** At 19.0g (Q3), z = (19.0−18.0)/1.4 = +0.714 — this product is
already in the penalty zone (r≥0.5 → penalty=1). The floor activates for the same products already
receiving a penalty, providing a belt-and-suspenders backstop for products with many additive or
structural relief signals. Products above 19.0g sat_fat (the top quartile) cannot be brought above
62 regardless of other signal relief.

### 5.2 Anti-Immunity Proof

`floor (62) + B_max (3) = 65 < 70` (grade B threshold) **PASS**

A product at or above the floor_threshold_g (19.0g sat_fat) is in the above-median zone — it cannot
receive B_max relief. Anti-Immunity is doubly protected: high-sat-fat products are penalized or neutral,
never relieved. The floor is a backstop for the residual path (a product below the floor threshold that
accumulates other relief signals).

---

## 6. Named Inversions

### Inversion 1 — Reduced-fat vs. full-fat yellow cheese

| | Product A | Product B |
|---|---|---|
| Barcode | `7290000062426` | `7290000062433` |
| Product name | עמק צהוב 9% מופחת שומן | עמק גאודה שנה 28% |
| sat_fat | 5.5g | 17.5g |
| Current score | 64.3 (C) | 77.6 (B) |
| z-value (Scope A, median=18.0g, scale=1.4) | z = (5.5−18.0)/1.4 = **−8.93 (BELOW median)** | z = (17.5−18.0)/1.4 = **−0.357 (BELOW median, near dead zone)** |
| SR delta | r_below = (18.0−5.5)/1.4 = 8.93 → band [3.0,∞) → **+3 (max relief)** | r_below = (18.0−17.5)/1.4 = 0.357 → band [0.3,1.5) → **+1 (mild relief)** |
| Predicted new score | 67.3 (C) | 78.6 (B) |
| Gap before SR | B scores 13.3pts MORE despite 12.0g MORE sat_fat |
| Gap after SR | 11.3pts (narrowed by 2.0pts) |

**Explicit median check:** A at 5.5g is **BELOW** median (18.0g). B at 17.5g is also **BELOW** median
(18.0g). Both receive relief — B gets +1, A gets +3. The gap narrows from 13.3 to 11.3pts. This is a
partial correction: A is rewarded more than B for having significantly less sat_fat.

**D7 note:** Both products are below the median (Scope A median=18.0g). This means the inversion is
partially corrected (A gains more relief than B) but neither product is penalized. To find a true
opposite-side inversion (one below, one above), Inversion 2 is needed.

### Inversion 2 — Reduced-fat vs. above-median grating cheese

| | Product A | Product B |
|---|---|---|
| Barcode | `7290000062426` | `8866972` |
| Product name | עמק צהוב 9% מופחת שומן | גבינה גרוויר 31% |
| sat_fat | 5.5g | 19.5g |
| Current score | 64.3 (C) | 69.9 (B) |
| z-value (Scope A, median=18.0g, scale=1.4) | z = (5.5−18.0)/1.4 = **−8.93 (BELOW median 18.0g)** | z = (19.5−18.0)/1.4 = **+1.071 (ABOVE median 18.0g)** |
| SR delta | r_below = 8.93 → band [3.0,∞) → **+3 (max relief)** | r_above = 1.071 → band [1.0,1.5) → **−2 (moderate penalty)** |
| Predicted new score | 67.3 (C) | 67.9 (B) |
| Gap before SR | B scores 5.6pts MORE despite 14.0g MORE sat_fat |
| Gap after SR | 0.6pts (nearly closed: narrowed by 5.0pts) |

**Explicit median check:** A at 5.5g is **BELOW** median (18.0g). B at 19.5g is **ABOVE** median
(18.0g). This is a genuine opposite-side inversion. A gets relief (+3), B gets penalty (−2). The
sat_fat gap correction is effective: 5.6pts → 0.6pts.

**CRITICAL CHECK PASSED:** Both products are on **opposite sides** of the median:
- A (5.5g sat_fat) is BELOW median 18.0g → receives relief (+3)
- B (19.5g sat_fat) is ABOVE median 18.0g → receives penalty (−2)
- SR moves them toward parity. Grade change: A stays C (67.3), B stays B (67.9) — nearly tied.

---

## 7. Scope Guard Implementation Specification

**Recommended implementation (for Data Agent, post-D7):**

```python
# In score_engine.py, after EV-089 cheese_spread sat_fat block (line ~2549):
# Hard cheese sat_fat shelf-relative (EV-090, TASK-278 Phase-8).
# Scope guard: category=="dairy_protein" AND bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS.
# Uses same asymmetric bands as cheese_spreads / yogurt / cereals.
# Shelf stats (fat_saturated_g) must be set by batch caller: median=18.0, scale=1.4, n=22.
_hc_satfat_g = nn.get("fat_saturated_g")
_sr_hc_satfat = 0
_sr_hc_satfat_note = None
_hc_subpool = product.get("bsip_cheese_subpool", "")
if (BARI_SHELF_RELATIVE_V1
        and category == "dairy_protein"
        and _hc_subpool in HARD_CHEESE_YELLOW_SUBPOOLS
        and _hc_satfat_g is not None):
    _sr_hc_satfat, _sr_hc_satfat_note = shelf_relative_differentiator(
        value=float(_hc_satfat_g),
        nutrient="fat_saturated_g",
        scope_categories=frozenset({"dairy_protein"}),  # gate-only; FATSAT_SHELF_REL_SCOPE untouched
        category=category,
        surcharge_bands=SUGAR_SHELF_SURCHARGE_BANDS,    # same P_max=6 bands as prior enrollments
        low_variance_guard=FATSAT_SHELF_SCALE_GUARD,
        direction="asymmetric",
        mapping="banded",
        relief_bands=SUGAR_SHELF_RELIEF_BANDS,
        normalize_distance=True,
    )
    if _sr_hc_satfat != 0:
        check_penalty("FATSAT_HARDCHEESE_SHELF_REL_V1", True, _sr_hc_satfat, fat_pens_fired,
                      _sr_hc_satfat_note or "")
```

**No engine edits in this D6 doc.** This is the implementation spec for post-D7 Data Agent work.

**New constant required in constants.py:**
```python
# EV-090 hard_cheeses×sat_fat shelf-relative scope guard (TASK-278 Phase-8)
HARD_CHEESE_YELLOW_SUBPOOLS: frozenset = frozenset({"yellow", "yellow_light", "hard_grating"})
FATSAT_SHELF_REL_HARDCHEESE_MEDIAN = 18.0
FATSAT_SHELF_REL_HARDCHEESE_IQR = 1.50
FATSAT_SHELF_REL_HARDCHEESE_SCALE = 1.4000      # IQR-primary at floor
FATSAT_SHELF_REL_HARDCHEESE_FLOOR = 62
FATSAT_SHELF_REL_HARDCHEESE_FLOOR_THRESHOLD_G = 19.0
FATSAT_SHELF_REL_HARDCHEESE_P_MAX = 6
FATSAT_SHELF_REL_HARDCHEESE_B_MAX = 3
```

---

## 8. D7 Open Questions

These require Product Agent decision before pilot wiring. Listed in priority order:

### Q1 — Scope guard type: subpool-level vs. full dairy_protein (CRITICAL)

The most consequential call. Two options:

**Option A (recommended):** `category == "dairy_protein" AND bsip_cheese_subpool in {"yellow", "yellow_light", "hard_grating"}` — calibrates within the true hard yellow cheese group (n=22). Robust_scale hits the minimum floor (1.4) because the yellow cluster is tight; the mechanism primarily differentiates the reduced-fat outliers from the full-fat cluster.

**Option B:** `category == "dairy_protein"` with no subpool guard — uses full corpus stats (n=37, scale=5.93). Mixes bulgarians/tzfatit/processed but has mechanically sound statistics and was the basis for the LAND classification.

**Nutrition Agent recommendation: Option A** — the calibration should reflect the peer group (yellow cheese vs yellow cheese), not a cross-type comparison. The bulgarians and tzfatit have fundamentally different sat_fat profiles and NOVA classifications; mixing them would produce a median that is not nutritionally meaningful for yellow cheese comparison. The scale issue (hitting floor) is a limitation that D7 must accept or propose addressing via Option B.

### Q2 — Scale adequacy at minimum floor (CRITICAL)

Scope A yields robust_scale=1.40 (at the minimum floor). Is this sufficient to justify enrollment?

The practical effect: the dead zone spans 17.58–18.42g — products in the dense yellow cluster (15 products at 17.5–19.5g) will mostly receive delta=0 to delta=±1. The mechanism primarily differentiates the 4 yellow_light products (5–10g sat_fat, getting +3 relief) from the tight yellow cluster.

**Product Agent must assess:** Is +3 relief for reduced-fat variants (5–10g sat_fat) a meaningful differentiation worth the implementation cost? Or does the mechanism simply confirm a distinction that the absolute backbone already captures?

### Q3 — What to do with misrouted hard cheeses (11 `dessert`-routed products)

11/37 products (29.7%) in the corpus route to `dessert` — these are genuine hard cheeses (עמק, גאודה, פרמזן) that score D because of misrouting, not sat_fat quality. SR cannot address misrouting errors.

**Product Agent must decide:** Is the router misrouting issue a blocker for this enrollment (correct the router first), or does the enrollment proceed for the correctly-routed dairy_protein products, with router fixes tracked separately?

### Q4 — Floor threshold (19.0g) confirmation

19.0g was chosen as Q3 of Scope A. The Israeli red-label sat_fat threshold is 15.0g/100g. Should the floor activate at:
- Q3=19.0g (statistical approach, as recommended)
- 15.0g (regulatory threshold: any sat_fat red-label product is floored at 62)

The Anti-Immunity proof holds either way: `62+3=65<70`. At 15.0g: more products floored (all products above red-label threshold). At 19.0g: only the top quartile floored. If the redlabel-de-anchor directive (standing owner directive 2026-06-14) applies, the regulatory floor at 15.0g should be deprioritized and Q3=19.0g is correct.

### Q5 — Budget raise: FAT_QUALITY_FAMILY_BUDGET

Prior enrollments (cereals, yogurt, cheese_spreads) did NOT raise the fat family budget. For hard cheeses, sat_fat is the dominant fat signal. Does FAT_QUALITY_FAMILY_BUDGET need adjustment to prevent the SR term (max P=6) from being absorbed into the existing fat family budget cap?

Check at pilot: verify that the SR penalty+absolute backbone combined does not exceed the budget cap for high-sat-fat products.

---

## 9. Draft EV-090

```
EV-090 — Hard Cheeses × Sat_Fat: Shelf-Relative Enrollment (D6 proposal)
--------------------------------------------------------------------------
finding_id: EV-090
task: TASK-278 Phase-8
recorded: 2026-06-14
extends: EV-084 (shelf-relative design), EV-089 (cheese_spreads×sat_fat precedent)
layer: Shelf-relative differentiator enrollment — scoped to
       category=="dairy_protein" AND bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS.
       No router edit. FATSAT_SHELF_REL_SCOPE remains frozenset().
concept: D6 proposal to enroll hard yellow cheese products into BARI_SHELF_RELATIVE_V1
         on the fat_saturated_g nutrient. Addresses within-shelf sat_fat inversions in
         the hard yellow cheese group where reduced-fat variants (9%, 16% fat) sit at
         5–10g sat_fat while full-fat aged cheeses (28–32% fat) cluster at 17.5–19.5g.
         The absolute backbone does not differentiate within the full-fat cluster (where
         all products receive the same sat_fat red-label penalty); SR provides modest
         additional resolution for the reduced-fat outliers.
scope_guard: category=="dairy_protein" AND bsip_cheese_subpool in HARD_CHEESE_YELLOW_SUBPOOLS
             where HARD_CHEESE_YELLOW_SUBPOOLS = frozenset({"yellow", "yellow_light", "hard_grating"})
corpus: run_hard_cheeses_001 (2026-06-08), yellow+yellow_light+hard_grating subpools only
corpus_stats: n=22, median=18.0g, Q1=17.5g, Q3=19.0g, IQR=1.50g, MAD=0.50g,
              robust_scale=1.40 (at min_scale_floor; IQR/1.349=1.11 < floor),
              min=5.0g, max=21.0g, stdev=4.83g
P_max: 6 pts
B_max: 3 pts
near_median_z_threshold: 0.3
floor: 62 (formulation_absolute_floor)
floor_threshold_g: 19.0g (Q3-based)
anti_immunity_proof: 62+3=65<70 PASS
d7_open_questions: 5 (see §8 above)
status: D6 PROPOSAL — awaiting Product Agent D7 co-sign
d6_author: Nutrition Agent (2026-06-14, TASK-278 Phase-8, P121)
file: 02_products/hard_cheeses/methodology/shelf_relative_satfat_enrollment_hardcheeses_v1.md
```

---

## 10. Spec-Conflict Flags

### SC-1: Scope guard mechanism differs from cheese_spreads

The cheese_spreads EV-089 used `category_subtype` (a router-assigned field). Hard cheeses do not have
a dedicated router subtype ("hard_cheese" exists in router HARD_ANCHORS but only fires for "גאודה",
"אמנטל", "גרנה פדנו" — NOT for "עמק", "קולבי", "מונסטר", etc.). Instead, `bsip_cheese_subpool`
from the BSIP1 input is the correct discriminator. This is the same mechanism used for brined cheeses
(EV-055: `bsip_cheese_subpool` via category prior in router_v2.py). Flagged for Data Agent awareness
at implementation time — the subpool field must be accessible at scoring time.

### SC-2: Rollout spread analysis scope vs. this proposal

The rollout spread analysis used the full 37-product corpus (Option C: all subpools, n=37, scale=5.9).
This D6 proposal recommends the narrower Scope A (n=22, scale=1.4). This is a scope reduction from
the analysis reference. The correct approach is the coherent peer group (Scope A), but the analysis
calibration (Scope C) has better mechanical properties. This conflict is surfaced as Q1 and Q2 for
D7 to resolve.

### SC-3: 11/37 products in `dessert` category are out of scope

These misrouted products score D due to router error, not sat_fat quality. The SR mechanism cannot
and should not attempt to correct this. Flagged for Product Agent: router correction for hard cheeses
(dedicated `hard_cheese` category or improved anchors for "עמק", "פרמזן", "קולבי") is a prerequisite
for a comprehensive category rollout. This D6 proposes SR only for correctly-routed products.

---

## 11. Compliance

- Engine files modified: **0** (constants.py unchanged, score_engine.py unchanged)
- Score movement: **0** (FATSAT_SHELF_REL_SCOPE remains frozenset())
- Published scores changed: **0**
- OFF used: **No** (all stats from L1_observed_signals in committed trace files)
- Data source: `02_products/hard_cheeses/bsip2_outputs/run_hard_cheeses_001/` trace files
- Source authority: direct product scrape → BSIP0 → BSIP1 run_hard_cheeses_001 → BSIP2 run_hard_cheeses_001

---

*Document: `02_products/hard_cheeses/methodology/shelf_relative_satfat_enrollment_hardcheeses_v1.md`*
*D6 PROPOSAL only. No enrollment until D7 co-sign from both Nutrition Agent and Product Agent.*
*Generated: 2026-06-14*
