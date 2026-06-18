# Shelf-Relative Sat_Fat Enrollment — Cheese Spreads Category
## D6 Design Proposal — Awaiting D7 Co-Sign (Nutrition Agent + Product Agent)

**EV Number:** EV-089 (draft)
**Status:** D6 PROPOSAL — no engine edits, no score movement, no pilot wiring
**Author:** Nutrition Agent
**Date:** 2026-06-14
**Task:** TASK-278 Phase-7
**Authoritative corpus:** `run_cheese_004` (59 products, 2026-06-02)
**Prior context:** Rollout spread analysis `rollout_spread_analysis_v1.md` (2026-06-14)
**Preceded by:** Phase-5 (cereals×sugar, EV-087) and Phase-6 (yogurt×sugar, EV-088)

---

## 1. Background

The rollout spread analysis ranked cheese_spreads×sat_fat as the #3 enrollment candidate:

| Metric | Value |
|---|---|
| Run | run_cheese_004 |
| n | 59 |
| Sat_fat IQR | 12.9g (spread_analysis used whole corpus) |
| Sat_fat robust_scale (whole corpus) | 9.5 |
| Score stdev | 14.47 |
| % Floored | 1.7% |
| Classification | LAND |

Sat_fat was confirmed as the right lever: sugar is sparse (34/59 non-null), sodium is secondary.
The score stdev of 14.47 and near-zero floor saturation indicate the mechanism will land.

**Critical architectural finding from this D6 analysis:** The "cheese_spreads" category is not
a homogeneous shelf. The corpus includes:
- **Cream cheese spreads** (גבינת שמנת, פילדלפיה, נפוליאון): sat_fat 3–22g, median ~16g
- **Cottage cheese** (קוטג'): sat_fat 1.8–7.8g, median ~3g
- **White cheese / quark** (גבינה לבנה, טבורוג, גבינה 5–9%): sat_fat 0.6–5.4g, median ~3g

These are structurally distinct products with fundamentally different sat_fat distributions.
Enrolling `dairy_protein` wholesale (as the yogurt pilot did as a diagnostic shortcut) would
mix cream-cheese calibration (median ~16g) with cottage calibration (median ~3g), producing
nonsensical cross-group SR adjustments. The scope must be product-group specific.

---

## 2. Authoritative Corpus

| Field | Value |
|---|---|
| Run ID | `run_cheese_004` |
| Date generated | 2026-06-02 |
| Engine | proto_v0 / 0.4.1 + BARI_RECAL_P0=on |
| Source | Shufersal scrape → BSIP1 run_cheese_003 |
| Total products | 59 |
| Scored products | 54 |
| Insufficient data | 5 |
| Products with non-null fat_saturated_g | 57 |
| Null sat_fat | 2 |
| Coverage | 96.6% |
| Router category (dominant) | `dairy_protein` |
| Non-dairy_protein routes | 2 misroutes (snack_bar_granola + default) — excluded |

Source of fat_saturated_g: exclusively `L1_observed_signals.fat_saturated_g` in committed
trace files — direct product scrape, no external source. OFF is not used.

---

## 3. Scope Guard Design

### 3.1 The Core Problem

All cheese_spreads products route to `"dairy_protein"` — the same composite router category
as yogurt and milk. Unlike yogurt (which has `category_subtype` values like `"yogurt"`,
`"greek_yogurt"`, etc.), the cheese_spreads corpus includes multiple distinct product types:

| Product type | Router subtype | n | Sat_fat range |
|---|---|---|---|
| Cream cheese / spreads | `"cream_cheese"` | ~26 | 3–22g |
| Cottage cheese | `"cottage"` | ~10 | 1.8–7.8g |
| White cheese / quark | `None` (Stage 2 routing) | ~23 | 0.6–22g |

The router's `HARD_ANCHORS` list in `router_v2.py` emits `category_subtype="cream_cheese"` for
products matched by `"גבינת שמנת"`, `"פילדלפיה"`, `"נפוליאון"` anchors, and `"cheese_spread"`
for `"ממרח גבינה"`. This is the discriminator available at scoring time.

**Note:** Traces from `run_cheese_004` do NOT store `category_subtype` in the JSON (the
`trace_writer.py` does not persist this field). However, at scoring time, `score_product()`
receives `cat_result` from `classify_category()` which includes the subtype — exactly as in
the yogurt implementation at `score_engine.py:2132`. The subtype is runtime-available even
though traces don't store it.

### 3.2 Discriminator Options

**(A) Router `category_subtype` field (cream_cheese/cheese_spread) — RECOMMENDED**

Scope gate:
```python
category == "dairy_protein" AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES
```
where:
```python
CREAM_CHEESE_SPREAD_SUBTYPES = ("cream_cheese", "cheese_spread")
```

This mirrors the yogurt precedent exactly. No router changes. Uses the subtype already emitted
at scoring time. Excludes cottage (subtype="cottage") and white cheese (subtype=None).

Corpus for stat computation: cream_cheese subtype products only.

**(B) Dairy_protein wholesale (diagnostic shortcut)**

Gate: `category == "dairy_protein"` with whole-corpus stats (median=5.4g, scale=9.5626).
This applies a single calibration across cream cheese + cottage + white cheese. Produces
relief awards for cottage (3g sat_fat) using a median calibrated for cream cheese. Structurally
incorrect for a heterogeneous category.

**Decision: Option A is correct.** The scope guard must restrict to cream_cheese subtypes.
This is the same reasoning that motivated CULTURED_YOGURT_SUBTYPES for yogurt.

---

## 4. Corpus Statistics — Cream Cheese Scope

All statistics computed from `run_cheese_004` traces, restricted to products where the
router assigns `category_subtype in ("cream_cheese", "cheese_spread")` at scoring time.
Source: `L1_observed_signals.fat_saturated_g` only.

| Statistic | Value |
|---|---|
| n (cream_cheese subtype with non-null sat_fat) | 24 |
| n gate (≥20) | **PASS** |
| Median | 16.05g |
| Q1 | 14.15g |
| Q3 | 16.75g |
| IQR | 2.60g |
| MAD | 1.40g |
| IQR/1.349 | 1.9274 |
| 1.4826 × MAD | 2.0756 |
| robust_scale = max(IQR/1.349, 1.4826×MAD, 1.0) | **2.0756** (MAD-primary) |
| Min | 3.0g |
| Max | 20.0g |
| Coverage | 24/26 cream_cheese products = 92.3% |

**Key observation:** The corpus is highly clustered. Most cream cheese products sit at
14–17g sat_fat (near the Israeli red-label threshold of 15g), while a minority of lower-fat
or plant-based variants sit at 3–10g. The robust_scale of 2.0756 reflects this tight clustering
near the high end, with a few outlier lower-fat products at large z-distances below the median.

**Low-variance guard check:** robust_scale=2.0756 ≥ FATSAT_SHELF_SCALE_GUARD=0.5 PASS.

**D7 flag — scale concern:** The small robust_scale (2.0756) means a product must be at
least 2.1g below/above the median to enter the first non-zero band (z≥0.5 at 1.04g distance).
The SR term will fire for outlier products (low-fat at 3–10g, max-fat at 20g) but produce
delta=0 for the large mid-cluster. Product Agent must assess whether this adjustment range
is meaningful enough to justify enrollment.

---

## 5. Scope Guard Design (Final)

**Recommended guard:**
```python
category == "dairy_protein" AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES
```

**Why not a simple `category in FATSAT_SHELF_REL_SCOPE` add:**
The existing `shelf_relative_differentiator()` checks `category not in scope_categories` at
line 285. Adding `"dairy_protein"` to `FATSAT_SHELF_REL_SCOPE` would fire for ALL
dairy_protein products — cottage, white cheese, yogurt, milk (on runs that include them).
This would be wrong. The correct implementation follows the yogurt×sugar precedent (score_engine
lines 2125–2148): a separate code branch gated on both `category` and `category_subtype`.

**Implementation spec (for Data Agent, post-D7):**
```python
# In evaluate_guardrails(), after the existing FATSAT SR block (line 2500-2514):
# Add a parallel branch for cream cheese sat_fat SR:
if (BARI_SHELF_RELATIVE_V1
        and category == "dairy_protein"
        and cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES
        and nn.get("fat_saturated_g") is not None):
    _cream_sat_rel_pen, _cream_sat_rel_note = shelf_relative_differentiator(
        value=float(nn.get("fat_saturated_g")),
        nutrient="fat_saturated_g",
        scope_categories=frozenset({"dairy_protein"}),  # gate-only; global scope untouched
        category=category,
        surcharge_bands=FATSAT_SHELF_SURCHARGE_BANDS,
        low_variance_guard=FATSAT_SHELF_SCALE_GUARD,
        direction="asymmetric",
        mapping="banded",
        relief_bands=FATSAT_SHELF_RELIEF_BANDS,
        normalize_distance=True,
    )
    if _cream_sat_rel_pen != 0:
        check_penalty("FATSAT_SHELF_REL_V1", True, _cream_sat_rel_pen, fat_pens_fired, ...)
```

**No router changes.** FATSAT_SHELF_REL_SCOPE remains empty (unchanged). A new constant
`CREAM_CHEESE_SPREAD_SUBTYPES` is added to constants.py.

---

## 6. Band Design

Following D7 co-sign spec (shelf_relative_d7_cosign_v1.md) standard parameters:

| Parameter | Value | Rationale |
|---|---|---|
| P_max | 6 pts | Standard across all enrollments (EV-085/087/088) |
| B_max | 3 pts | Standard asymmetric P>B (C3 recommendation, D7 ratified) |
| Near-median z-threshold | 0.3 | Standard threshold: \|z\|<0.3 → delta=0 |
| direction | asymmetric | Sat_fat is endemic but graduated — below-median deserves relief |
| normalize_distance | True | Bands in r-units, consistent with EV-087/088 |

**Surcharge bands** (r-units, r=(sat_fat−16.05)/2.0756):
| r range | Penalty |
|---|---|
| [0, 0.5) | 0 |
| [0.5, 1.0) | 1 |
| [1.0, 1.5) | 2 |
| [1.5, 2.5) | 4 |
| [2.5, ∞) | 6 |

**Relief bands** (r_below = (16.05−sat_fat)/2.0756):
| r range | Relief |
|---|---|
| [0, 0.5) | 0 |
| [0.5, 1.5) | 1 |
| [1.5, 3.0) | 2 |
| [3.0, ∞) | 3 |

**Floor design:**

Sat_fat is an endemic dairy nutrient. The concern is high-fat cream cheese receiving too much
SR relief from other signals. A formulation_absolute_floor prevents the Anti-Immunity failure.

| Parameter | Value | Rationale |
|---|---|---|
| floor | 62 | Same as cereals/yogurt (grade C ceiling; standard floor) |
| floor_threshold_g | 16.5g | Activates at Q3+0.45g — captures the top quartile of high-sat-fat products |

**Floor_threshold rationale:** At 16.5g, z = (16.5−16.05)/2.0756 = +0.217, which is in the
near-median dead zone (z<0.5 → penalty=0). The floor therefore catches products that sit in
the very-near-above-median zone where no SR penalty fires but the absolute sat_fat is
high. Products at 17g+ (z≥+0.458) are already in the penalty zone; floor provides a safety
backstop. Products at 14.15–16.5g (Q1–floor_threshold) are in the SR-neutral zone (|z|<0.3)
and the floor does not activate.

---

## 7. Anti-Immunity Proof

floor (62) + B_max (3) = **65 < 70** (grade B threshold) **PASS**

A cream cheese product at or above the floor_threshold_g (16.5g sat_fat) is in the above-
median zone — it cannot receive relief (B_max). Anti-Immunity is doubly protected: high-sat-fat
products are penalized or neutral, never relieved. The floor is a backstop for the residual
scoring paths (e.g. a product with many additive penalties that drops below the floor threshold
via backbone and then gets modest SR relief — the floor caps at 62).

---

## 8. Named Inversions

Two clean inversions from cream_cheese subtype products in run_cheese_004:

### Inversion 1

| | Product A | Product B |
|---|---|---|
| Barcode | `4129118` | `7290116935409` |
| sat_fat_g | 14.0g | 16.2g |
| Current score | 56.4 (C) | 62.3 (C) |
| z-value | −0.988 | +0.072 |
| SR delta | +1 (below-median relief) | 0 (near-median, \|z\|<0.5→0) |
| Predicted new score | 57.4 (C) | 62.3 (C) |
| Inversion correction | A currently scores 5.9pts LOWER than B despite 2.2g less sat_fat. SR gives A +1 relief. Gap narrows from 5.9 to 4.9pts. Partial correction. |

**Note:** The gap narrows but is not fully reversed because both products are near the median.
The large baseline score gap (5.9pts) is driven by other signals (processing quality, additives).
SR provides the sat_fat-relative correction within what the mechanism can do.

### Inversion 2

| | Product A | Product B |
|---|---|---|
| Barcode | `7622201521493` | `7290014759084` |
| sat_fat_g | 7.8g | 9.6g |
| Current score | 52.3 (C) | 66.4 (B) |
| z-value | −3.975 | −3.108 |
| SR delta | +3 (max relief) | +3 (max relief) |
| Predicted new score | 55.3 (C) | 69.4 (B) |
| Inversion situation | A scores 14.1pts lower than B despite 1.8g less sat_fat. Both receive max relief (+3) — same delta, gap unchanged at 14.1pts after SR. The backbone-driven gap is not an SR-addressable inversion. |

**Note on Inversion 2:** Both products are well below the median and both receive the same
maximum relief. The gap between them is not sat_fat-driven and SR cannot correct it. This
exposes the enrollment's limitation: with median=16.05g and most products at 14–17g, the
SR mechanism primarily acts on outlier products (3–10g below-median, 18–22g above-median),
not on the dense near-median cluster.

**Better named inversion (Inversion 2-revised):**

| | Product A | Product B |
|---|---|---|
| Barcode | `7622201521493` | `4129101` |
| sat_fat_g | 7.8g | 15.0g |
| Current score | 52.3 (C) | 55.6 (C) |
| z-value | −3.975 | −0.506 |
| SR delta | +3 (max relief, z>3.0) | +1 (near-median, z=0.506→band[0.5,1.5)=1 relief) |
| Predicted new score | 55.3 (C) | 56.6 (C) |
| Gap: before SR | B scores 3.3pts higher despite 7.2g more sat_fat |
| Gap: after SR | Narrows from 3.3 to 1.3pts. Direction maintained (A still below B) but approaching parity |

This is the cleaner inversion: A has meaningfully less sat_fat and gets more relief than B,
partially correcting the inversion caused by other scoring signals.

---

## 9. D7 Open Questions

These require Product Agent decision before pilot wiring:

1. **Scale adequacy (CRITICAL):** The cream_cheese-only robust_scale=2.0756 reflects a
   corpus that clusters tightly at 14–17g sat_fat. With a near-median z-threshold of 0.3,
   the dead zone is |sat_fat−16.05| < 0.62g. Most products (those at 15.0–17.0g) get
   delta=0. SR primarily fires on the outlier low-fat products (3–10g, getting +3) and
   the high-fat products above 18g (getting −2 to −4). Product Agent must confirm this
   pattern is worth the implementation cost, or propose an adjusted z-threshold.

2. **Alternative scope option — full dairy_protein enrollment:** If Product Agent believes
   the right unit of analysis is the entire cheese_spreads shelf (including cottage and white
   cheese), the correct corpus for stat computation is all 57 products (median=5.4g, IQR=12.9,
   scale=9.5626). This would calibrate correctly within the whole category but raises the
   philosophical question of whether SR should operate across structurally different product
   types. This is a product call, not a nutrition call.

3. **Floor_threshold_g confirmation:** 16.5g was chosen as Q3+0.45g. The actual Israeli
   red-label threshold for sat_fat is 15.0g/100g. Should the floor activate at the regulatory
   threshold (15.0g) rather than Q3+margin? If the floor activates at 15.0g (the red-label
   line), the Anti-Immunity proof still holds: 62+3=65<70. But more products would be floored.

4. **Budget raise:** Unlike biscuits (EV-085 raised the budget by max(P,B)=6), cereals and
   yogurt did NOT raise the budget. Should cream cheese follow the no-raise pattern (consistent
   with cereals/yogurt), or does the FAT_QUALITY_FAMILY_BUDGET need adjustment given sat_fat
   is already the dominant signal in the fat family for cream cheeses?

5. **Pilot scope for gate:** What is the right comparison baseline for the pilot — run_cheese_004
   current scores, or a re-run with the current engine (TASK-275 fixes applied)? The engine
   has changed since run_cheese_004 (branch task-275-engine-fixes-abc is current). A clean
   pilot should use the current HEAD engine for both flag-on and flag-off.

---

## 10. Draft EV-089

```
EV-089 — Cheese Spreads × Sat_Fat: Shelf-Relative Enrollment (D6 proposal)
-----------------------------------------------------------------------
finding_id: EV-089
task: TASK-278 Phase-7
recorded: 2026-06-14
extends: EV-084 (shelf-relative design), EV-088 (yogurt×sugar precedent)
layer: Shelf-relative differentiator enrollment — scoped to
       category=="dairy_protein" AND category_subtype in CREAM_CHEESE_SPREAD_SUBTYPES.
       No router edit. FATSAT_SHELF_REL_SCOPE remains empty.
concept: D6 proposal to enroll cream_cheese spread products into BARI_SHELF_RELATIVE_V1
         on the fat_saturated_g nutrient. Addresses within-shelf sat_fat inversions in
         the cream cheese sub-category where 14-17g is the norm and outlier products
         (3-10g light/plant-based, 18-22g maximum fat) are not distinguished by the
         absolute backbone alone.
scope_guard: category=="dairy_protein" AND cat_subtype in CREAM_CHEESE_SPREAD_SUBTYPES
             where CREAM_CHEESE_SPREAD_SUBTYPES = ("cream_cheese", "cheese_spread")
corpus: run_cheese_004 (2026-06-02), cream_cheese subtype products only
corpus_stats: n=24, median=16.05g, Q1=14.15g, Q3=16.75g, IQR=2.60g, MAD=1.40g,
              robust_scale=2.0756 (MAD-primary: 1.4826×1.40=2.0756 > IQR/1.349=1.9274),
              min=3.0g, max=20.0g
P_max: 6 pts
B_max: 3 pts
near_median_z_threshold: 0.3
floor: 62 (formulation_absolute_floor)
floor_threshold_g: 16.5g
anti_immunity_proof: 62+3=65<70 PASS
d7_open_questions: 5 (see enrollment doc §9)
status: D6 PROPOSAL — awaiting Product Agent D7 co-sign
d6_author: Nutrition Agent (2026-06-14, TASK-278 Phase-7, P117)
file: 02_products/cheese_spreads/methodology/shelf_relative_satfat_enrollment_cheesespreads_v1.md
```

---

## 11. Spec-Conflict Flags

No spec conflicts detected. The D7 co-sign spec parameters are applied as specified:
- P_max=6, B_max=3: standard
- near-median z-threshold=0.3: standard
- Anti-Immunity: floor+B_max<70: confirmed

The scope guard cannot be `category in FATSAT_SHELF_REL_SCOPE` (which would require adding
`"dairy_protein"` and would bleed into yogurt/milk). The yogurt precedent (separate code path
with subtype guard) is the correct architecture — flagged here as a spec-compliant implementation
requirement for Data Agent.

---

## 12. Compliance

- Engine files modified: **0** (constants.py unchanged, score_engine.py unchanged)
- Score movement: **0** (FATSAT_SHELF_REL_SCOPE remains empty)
- Published scores changed: **0**
- OFF used: **No** (all stats from L1_observed_signals in committed trace files)
- Data source: `02_products/cheese_spreads/bsip2_outputs/run_cheese_004/` trace files
- Source authority: direct product scrape → BSIP0 → BSIP1 run_cheese_003 → BSIP2 run_cheese_004

---

*Document: `02_products/cheese_spreads/methodology/shelf_relative_satfat_enrollment_cheesespreads_v1.md`*
*D6 PROPOSAL only. No enrollment until D7 co-sign from both Nutrition Agent and Product Agent.*
*Generated: 2026-06-14*
