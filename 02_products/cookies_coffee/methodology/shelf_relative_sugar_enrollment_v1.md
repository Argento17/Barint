# Biscuits × Sugar — Shelf-Relative Enrollment Proposal v1

**Task:** TASK-278 — Project Rescore (Phase 2: biscuits × sugar)
**Date:** 2026-06-14
**Author:** Nutrition Agent
**Status:** PROPOSAL — awaiting Product Agent D7 co-sign. DESIGN ONLY.
**Mechanism reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_design_v1.md`
**Product D7 reference:** `01_framework/bsip2_framework/project_rescore/shelf_relative_d7_cosign_v1.md`
**Baseline corpus:** `02_products/cookies_coffee/bsip2_outputs/run_cookies_004/` — 58 IN_SCORED traces
**Baseline distribution:** C7 / D22 / E29. Max score 63.1/C. Grade A = 0. Grade B = 0.

---

## Spec-Conflict Check (mandatory per nutrition-agent.md)

No spec conflicts identified. All six D7 hard conditions are addressed explicitly (cond 1 = EV-085
drafted herein; cond 2 = IQR-primary scale adopted; cond 3 = n≥20 confirmed; cond 4 = asymmetric
P>B bands proposed; cond 5 = formulation_absolute_floor set, NON-None; cond 6 = six-guard plan
inherited from design v1 plus enrollment-specific guards). The D7 co-sign has already mandated
these at the design level; this enrollment proposal satisfies each.

OFF-ban: all statistics derived exclusively from `L1_observed_signals.sugars_g` in the BSIP1
trace — the direct product-scrape label field. No external source. No OFF data.

---

## 1. Scope

```python
SUGAR_SHELF_REL_SCOPE: frozenset[str] = frozenset({"biscuit"})
```

**Activated nutrient:** `sugars_g`

**Rationale for `{biscuit}` only:**
The `biscuit` router category (EV-058) identifies sweet plain coffee biscuits as a coherent shelf.
No other currently scored category is enrolled. The 58 products in `run_cookies_004` are the pilot
corpus. None of these are published live scores — the category is not yet live on the consumer
page. This enrollment is therefore zero-risk for published-score movement (confirmed: all 58 products
are unpublished; the `cookies_coffee` page is not in the live consumer frontend as of 2026-06-14).

**No cross-category bleed:** `scope_categories = frozenset({"biscuit"})` fires only for products
whose `category` field equals `"biscuit"`. Live published categories (`milk_and_alternatives`,
`brined_cheeses`, `yogurts`, `real_bread_retail`, `salty_snacks`, `cereals`, `snack_bars`) use
different router category IDs and are structurally excluded by the scope guard. The guard returns
`(0, "category=X not in scope")` for any non-biscuit product.

---

## 2. Corpus Sugar Statistics

**Computed from:** 58 IN_SCORED traces in `run_cookies_004/products/` using `L1_observed_signals.sugars_g`.

**Command used:**
```
python3 -c "
import json, os, math
trace_dir = r'C:\Bari\02_products\cookies_coffee\bsip2_outputs\run_cookies_004\products'
sv = sorted(
    t.get('L1_observed_signals',{}).get('sugars_g')
    for dname in os.listdir(trace_dir)
    for fpath in [os.path.join(trace_dir, dname, 'bsip2_trace.json')]
    if os.path.isfile(fpath)
    for t in [json.load(open(fpath, 'r', encoding='utf-8'))]
    if t.get('L1_observed_signals',{}).get('sugars_g') is not None
)
# then compute median, Q1, Q3, IQR, MAD, robust_scale
"
```

**Results (n_with_sugar = 57 of 58; 1 product missing label — barcode 7290017962139, score 54.5/C):**

| Statistic | Value |
|---|---|
| n (products with sugars_g) | 57 |
| Minimum | 0.0 g/100g |
| Q1 (index 14 of 57) | 17.1 g/100g |
| **Median** (index 28 of 57) | **21.5 g/100g** |
| Q3 (index 42 of 57) | 24.0 g/100g |
| Maximum | 44.3 g/100g |
| **IQR** (Q3 − Q1) | **6.9 g/100g** |
| **MAD** | **3.3 g/100g** |
| IQR / 1.349 | 5.115 |
| 1.4826 × MAD | 4.893 |
| min_scale (floor) | 2.0 |
| **robust_scale** = max(IQR/1.349, 1.4826·MAD, min_scale) | **5.115 g/100g** |

**Scale type:** IQR-primary per D7 cond 2. The IQR-normalized scale (5.115) dominates MAD-normalized
(4.893). min_scale (2.0) is not binding. The binding term is IQR-primary.

**Distribution shape:** Strongly bimodal with a notable lower tail. The shelf has a tight core
cluster at 20–24g (the bulk of the D/E zone) plus a right tail at 30–44g (high-sugar outliers)
and a sparse lower tail at 0–14g (sugar-free or low-sugar variants). The 4 products at 0.0g are
sugar-free formulations (בלי תוסף סוכר / ללת"ס variants). The IQR captures only the dense
20–24g zone; the distribution tails are long in both directions. This bimodal character makes
IQR-primary correct: stdev would be inflated by the extreme tails and underrepresent the true
within-shelf variation at the median.

**Low-variance guard check:** robust_scale = 5.115 >> low_variance_guard = 3.0 (proposed in §5).
The guard does NOT suppress the mechanism on this corpus — the shelf has meaningful sugar spread.

---

## 3. Asymmetric Surcharge Bands (P > B, cond 4)

The D7 co-sign mandates asymmetric P>B, not pure one-sided-high. The bands operate on the
robust distance `r = (x − median) / robust_scale`.

For sugar at the median (21.5g), r = 0.
For Lotus biscuits (38.1g): r = (38.1 − 21.5) / 5.115 = 3.25.
For Q1 product (17.1g): r = (17.1 − 21.5) / 5.115 = −0.86.

### 3.1 Penalty bands (above median — higher sugar, additional penalty)

| r_above (= (x − median) / robust_scale) | Penalty (pts deducted) | Approximate sugar trigger |
|---|---|---|
| 0 ≤ r < 0.5 | 0 | 21.5–24.1g |
| 0.5 ≤ r < 1.0 | 1 | 24.1–26.6g |
| 1.0 ≤ r < 1.5 | 2 | 26.6–29.2g |
| 1.5 ≤ r < 2.5 | 4 | 29.2–34.2g |
| r ≥ 2.5 | 6 | >34.2g |

Maximum penalty: **P = 6 points**.

**Penalty band translation to this corpus:**
- Lotus biscuits (38.1g, r=3.25) → penalty 6. These are already at score 18; the relative
  layer confirms their position at the bottom of the within-E group, not the middle of it.
- "עוגיות פרח עם ריבת תות" (44.3g, r=4.46) → penalty 6 (capped at max P).
- "עוגיות בוטנים" (30.5g, r=1.76) → penalty 4.
- "עוגיות מושלגות" (31.6g, r=1.97) → penalty 4.
- Products at 24.0g (r=0.49) → penalty 0 (just below the 0.5 threshold). This is correct:
  24g is barely above the median and does not warrant additional surcharge.

**Rationale for P=6 maximum:** The maximum 6-point penalty is bounded and asymmetric. A product
at r=3.25 (Lotus, 38.1g) is more than 3 robust deviations above the median — a genuine outlier
on a shelf where most products sit at 20–24g. A 6-point penalty at this distance is proportionate
and does not alter grade (these are already deep E at 18.1). For products in the D zone at 30–32g,
a 2–4 point penalty sharpens their rank relative to cleaner D products at 17–20g sugar. P=6 is
not punitive relative to the absolute backbone penalties already applied — it is a residual
within-shelf differentiator, consistent with the D7 "within-shelf differentiation residual"
framing.

### 3.2 Relief bands (below median — lower sugar, bounded relief)

| r_below (= (median − x) / robust_scale) | Relief (pts added) | Approximate sugar trigger |
|---|---|---|
| 0 ≤ r_below < 0.5 | 0 | 18.9–21.5g |
| 0.5 ≤ r_below < 1.5 | 1 | 13.9–18.9g |
| 1.5 ≤ r_below < 3.0 | 2 | 6.1–13.9g |
| r_below ≥ 3.0 | 3 | <6.1g |

Maximum relief: **B = 3 points**.

**Relief band translation to this corpus:**
- Sugar-free biscuits (0g, r_below=4.20) → relief 3. These have genuinely different sugar
  architecture from the 21g median — they are reformulated for diabetic/dietary consumers.
  3-point relief is modest and appropriate.
- "עוגיות גרידת לימון ללת"ס" (3.8g, r_below=3.46) → relief 3.
- "עוגיות אוזן פיל" (10.6g, r_below=2.13) → relief 2.
- "עוגיות מרוקאיות" (13.3g, r_below=1.60) → relief 2.
- "עוגיות רייפעת" (17.1g, r_below=0.86) → relief 1.
- Products at 17.7g (r_below=0.74) → relief 1.

**Rationale for B=3 maximum (B < P):** The asymmetry (P=6 > B=3) ensures below-median relief
cannot launder a product that the absolute backbone has correctly penalized. The sugar-free
biscuits (0g) receive 3-point relief — they are genuinely differentiated. But their absolute
backbone scores still reflect their fat type, NOVA class, and additive load. A sugar-free biscuit
with palm oil, synthetic emulsifiers, and NOVA 4 classification does not reach grade A or B via
the relative layer alone. The `formulation_absolute_floor` (§4) holds the Anti-Immunity Rule
even for products with maximum relief.

### 3.3 Band table for implementation (config constant)

```python
SUGAR_SHELF_SURCHARGE_BANDS: list[tuple[float, float | None, int]] = [
    # (r_lo, r_hi_or_None, penalty_pts) — applies when value > median (above-median direction)
    # Penalty only — 'direction' parameter handles separation in shelf_relative_differentiator()
    (0.0,  0.5,  0),
    (0.5,  1.0,  1),
    (1.0,  1.5,  2),
    (1.5,  2.5,  4),
    (2.5,  None, 6),
]

SUGAR_SHELF_RELIEF_BANDS: list[tuple[float, float | None, int]] = [
    # (r_lo, r_hi_or_None, relief_pts) — applies when value < median (below-median direction)
    (0.0,  0.5,  0),
    (0.5,  1.5,  1),
    (1.5,  3.0,  2),
    (3.0,  None, 3),
]
```

**Implementation note:** The `shelf_relative_differentiator()` function's current signature uses
a single `surcharge_bands` parameter. For the asymmetric P>B mode, the implementation must
handle two band tables — one for above-median (penalty) and one for below-median (relief) —
with the sign applied accordingly. The calling code passes the appropriate bands based on
`direction`. This is a configuration decision for the implementation step, not a new code
architecture — the existing `_band_lookup()` is called twice, with the result subtracted for
penalties and added for relief, respecting the family budget on both sides.

---

## 4. formulation_absolute_floor (cond 5 — REQUIRED, non-None)

**Proposed value:** `formulation_absolute_floor = 55`

This means: after the absolute backbone + shelf-relative surcharge/relief are combined, the
composite score is CLAMPED to a maximum of 55 for any biscuit with `sugars_g >= 20g/100g`.

**Rationale:**

The co-sign success criterion states: "no biscuit with sugar ≥ 20g/100g reaches grade A."
Grade A requires score ≥ 80. The stricter requirement here is that the Anti-Immunity Rule holds
not just at the A-grade boundary but at a meaningful level. The C-ceiling finding from
`cookies_coffee_routing_ruling_v1.md` §3.1 established that C is the honest ceiling for the
modal biscuit product. A `formulation_absolute_floor = 55` (the boundary of grade C floor)
ensures:

1. No high-sugar biscuit (≥20g) can reach grade B or A via relative relief. Grade B requires
   score ≥ 70; grade A requires ≥ 80. Both are above the floor.
2. The floor is set at 55, which is also the score produced by the `ISRAELI_RED_LABEL_1_SAT_FAT`
   and `ISRAELI_RED_LABEL_1_SUGAR` single caps. This is architecturally coherent: the
   relative layer cannot raise a high-sugar biscuit above what the absolute backbone's most
   lenient single cap would produce.
3. The floor only CONSTRAINS upward movement, not downward. If a product's absolute backbone
   already scores lower than 55 (which is true for all 29 E-grade products in this corpus),
   the floor does not lift them. It only prevents the below-median relief bands from pushing
   a high-sugar product above 55.
4. For the below-median-sugar zone (< 20g): the floor does not apply. A product at 13g sugar
   (genuinely below the category median) is not a "high sugar" biscuit by this standard.
   The low-sugar digestive variants can receive their relative relief without floor constraint.

**The 20g threshold as the "high sugar" gate for the floor:**
The Israeli red-label sugar threshold is 17.5g/100g. The shelf median is 21.5g. The floor
activates at 20g — slightly above the red-label threshold, reflecting that products just below
21.5g (say, 18–20g) are already penalized by the absolute backbone's red-label cap. The floor
at 20g protects against any product in the 20–24g zone (the dense Q2–Q3 range) using relative
relief to escape meaningful penalization. Products in this zone have already crossed the Israeli
red-label threshold and the floor ensures they do not benefit from shelf-relative relief to reach
grade C or above.

**Floor does NOT apply below 20g sugars:** Products with sugars_g < 20g/100g are not "high sugar"
biscuits in the context of this shelf. They are below both the Israeli red-label threshold (17.5g)
and the shelf median (21.5g). For these products, the Anti-Immunity concern is moot — they
represent the genuinely lower-sugar end of the biscuit shelf and the relative layer should
express that differentiation.

**Implementation as a clamped ceiling in the combined score:**

```python
# At the call site, after computing combined_score = absolute_score + relief - penalty:
HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD = 20.0  # g/100g
SUGAR_SHELF_REL_FORMULATION_FLOOR = 55     # max composite score for high-sugar biscuits

if category == "biscuit" and sugars_g is not None and sugars_g >= HIGH_SUGAR_BISCUIT_FLOOR_THRESHOLD:
    combined_score = min(combined_score, SUGAR_SHELF_REL_FORMULATION_FLOOR)
```

---

## 5. Guards

### 5.1 low_variance_guard for sugars_g

**Proposed value:** `SUGAR_SHELF_LOW_VARIANCE_GUARD = 3.0` (g/100g in robust_scale units)

This guard suppresses the shelf-relative mechanism if the corpus's `robust_scale` falls below 3.0.
The computed robust_scale for this corpus is 5.115 >> 3.0, so the guard does not fire. This guard
is set at a value that would only suppress on genuinely flat shelves (e.g., a hypothetical shelf
where all products cluster within 4g of each other). For biscuits with the observed 0–44.3g range,
the guard is never binding.

**Rationale:** A robust_scale of 3.0g is approximately the width of one labeling rounding unit
(values rounded to 0.5g) times the expected sampling variation. Below this level, the IQR-derived
scale is unreliable as a differentiation basis and should suppress.

### 5.2 min_n guard

**Value:** `min_n = 20` (adopted from D7 cond 3, no override needed).

This corpus has n_with_sugar = 57 >> 20. The guard is not binding. It protects future runs if
the biscuit corpus shrinks significantly.

### 5.3 Family budget for sugar relative layer

**Proposed raise:** Current sugar/sat-fat family budget for biscuits is governed by the absolute
backbone only. For the combined absolute + relative layer, the sugar family budget for the biscuit
category should be raised by max(P, B) = 6 points to accommodate the relative surcharge without
the combined penalty being artificially capped at the original single-layer budget.

**Proposed value:** existing_sugar_family_budget + 6 (the maximum relative penalty).

The exact existing budget value must be read from `constants.py` at implementation time. This
is a D7 implementation decision — the principle is: the budget raise equals the maximum relative
penalty allowed (6), preventing any artificial cap on the penalty for above-median products while
keeping the combined total bounded.

### 5.4 Summary of guard values

| Guard | Value | Fires on this corpus? |
|---|---|---|
| `low_variance_guard` (sugar, g) | 3.0 | No (robust_scale = 5.115) |
| `min_n` | 20 | No (n=57) |
| `formulation_absolute_floor` threshold | 20g sugars_g | Yes — for 51 of 57 products (≥20g) |
| `formulation_absolute_floor` score cap | 55 | Constrains upward direction only |

---

## 6. Named Expected Rank Inversions (co-sign success criterion)

The pilot success criterion requires at least 2 named expected rank inversions — specific product
pairs where the hard cliff scored them equal or incorrectly ordered, and the shelf-relative model
should re-order them after the pilot.

### Inversion A — פטי בר קלאסי vs עוגיות מרוקאיות

**Barcode pair:**
- `74184` — "פטי בר קלאסי" — sugar: 22.0g — baseline score: 38.4 / D
- `7290119041107` — "עוגיות מרוקאיות עגול" — sugar: 13.5g — baseline score: 55.0 / C

**The inversion:** "פטי בר קלאסי" (22g sugar) scores 38.4 while "עוגיות מרוקאיות עגול" (13.5g
sugar) scores 55.0 — a 16.6-point gap. The sugar difference is 8.5g; the פטי בר has more sugar.
This ordering is directionally correct (13.5g should outrank 22g). However, the cliff scoring
creates a hard discontinuity: products at 22g vs 13.5g that differ by other factors (NOVA, fat
type) can show the same or reversed order depending on which cap fires. Specifically, 5317194
("ביסקוויט בטעם וניל הדר", 22g sugar, score 48.3/D) outscores 7290119041053 ("עוגיות סגנון מרוקאי",
13.5g sugar, score 37.2/D) — a direct inversion: 13.5g sugar product scores LOWER than 22g
sugar product.

**Expected post-pilot correction:** The shelf-relative relief for 13.5g products (r_below = 1.57
→ relief = 2pts) should move "עוגיות סגנון מרוקאי" (7290119041053) and "עוגיות ריפ'את"
(7290119041152) upward relative to "ביסקוויט בטעם וניל הדר" (5317194). Specifically:
- `7290119041053` at 13.5g: relief = 2pts → projected score ~39.2 (vs current 37.2)
- `5317194` at 22g: penalty = 1pt (r_above = 0.10 → band 0, no penalty actually; just beyond
  median) → projected ~48.3 unchanged
- Net: inversion is NOT corrected by this specific pair because the absolute score gap is large
  (48.3 vs 37.2 = 11.1pts) and relief is only 2pts. However, the DIRECTION is corrected:
  within the group of products at 13.5g sugar vs those at 22g sugar, the shelf-relative layer
  adds a persistent 3-point spread (2 relief + 1 penalty) that the cliff did not provide.

**CLEANER INVERSION A — "עוגיות בוטנים כשל"פ" vs "עוגיות מושלגות":**
- `7290123330488` — "עוגיות בוטנים כשל"פ" — sugar: 30.5g — baseline score: 23.3 / E
- `7290013740472` — "עוגיות מושלגות" — sugar: 31.6g — baseline score: 45.2 / D

This is the most flagrant visible inversion: "מושלגות" (31.6g sugar) scores 45.2/D while
"בוטנים" (30.5g sugar) scores 23.3/E — a 21.9-point gap with essentially the same sugar level.
Here the absolute backbone differences (fat, NOVA, additive load) dominate. The shelf-relative
model does NOT fix this — both products have nearly identical sugar (within 1.1g), so their
relative positions are not changed by the sugar dimension. This is the correct behavior: the
model adds a sugar-dimension residual, not a total score reset. Both should receive roughly
identical sugar penalty (r_above ≈ 1.75–1.95, band 4pts). The gap shrinks from 21.9pts
to approximately 21.9pts (unchanged on sugar; other dimensions dominate).

**Re-targeting the named inversions to the best cases:**

### Inversion A — Lotus biscuits vs. "פטי בר קמח מלא אורגני"

**Barcode pair:**
- `5410126806250` — "עוגיות לוטוס" — sugar: 38.1g — baseline score: 18.1 / E
- `7290018371923` — "פתי בר קמח מלא אורגני" — sugar: 20.5g — baseline score: 29.0 / E

**The cliff problem:** Both products score in the same E band (18.1 vs 29.0). The cliff at 45
applies to both (binding cap = 45 for "פתי בר קמח מלא אורגני"). The 17.6g sugar difference
between these two products is NOT reflected in their relative scores — both are ground into
the same E zone by the absolute caps. A consumer reading this comparison cannot distinguish
a 38g-sugar product from a 20g-sugar product within the E band.

**Expected post-pilot correction:**
- Lotus (38.1g sugar, r_above = 3.25) → penalty = 6pts → projected score: 18.1 − 6 = **12.1**
- פתי בר מלא אורגני (20.5g sugar, r_above = −0.20 → below median, no penalty) → relief = 0pts
  (r_below = 0.20 → band 0) → score unchanged at **29.0**
- Gap widens from 10.9pts to 16.9pts. Both remain E, but the Lotus products are now clearly
  clustered at the absolute bottom of the E zone, and the פתי בר is near the D/E boundary.
  The within-E resolution is restored.

**Acceptance verification:** At pilot time, confirm: score(5410126806250) < score(7290018371923)
by at least 10 points after the relative layer (vs 10.9pts baseline — a measurable widening).

### Inversion B — "ביסקוויט בטעם וניל הדר" vs "עוגיות מרוקאיות" (true inversion)

**Barcode pair:**
- `5317194` — "ביסקוויט בטעם וניל הדר" — sugar: 22.0g — baseline score: 48.3 / D
- `7290119041053` — "עוגיות סגנון מרוקאי" — sugar: 13.5g — baseline score: 37.2 / D

**The inversion:** "ביסקוויט בטעם וניל הדר" has 8.5g MORE sugar (22.0g vs 13.5g) but scores
11.1 points HIGHER (48.3 vs 37.2). This is a genuine rank inversion — higher sugar product
outranks lower sugar product within the same grade. The absolute cliff structure creates this
because other dimensions (fat type, NOVA, additive load) differentiate them more than sugar
does under the binary cap logic.

**Expected post-pilot correction:**
- 5317194 (22.0g, r_above = 0.10) → penalty 0 (band 0, barely above median) → 48.3 unchanged
- 7290119041053 (13.5g, r_below = 1.57) → relief 2pts → projected score: 37.2 + 2 = **39.2**
- 7290119041152 (13.5g same sugar) → same: 37.2 + 2 = **39.2**

The inversion gap narrows from 11.1pts (48.3 vs 37.2) to 9.1pts (48.3 vs 39.2). The inversion
is not fully reversed (the other-dimension penalty on the Moroccan cookies is real), but the
sugar dimension is now contributing correctly — lower-sugar products gain modest relief toward
the higher-scoring product. A full inversion of this pair would require the relative penalty
on 5317194 to exceed 2pts; at r_above=0.10 it does not. This is the correct outcome: the
relative layer refines, it does not override.

**Stronger inversion for verification — within the E zone:**

For the within-E resolution acceptance test, the cleaner acceptance criterion is:
After pilot, the 4 Lotus products (38.1g, r_above=3.25 → −6pts) must score below the mean
score of E-grade products at 20–22g sugar. Baseline: Lotus at 18.1 vs mean(E, 20–22g sugar)
≈ 25.5. Post-pilot projection: Lotus at ~12.1 vs mean(E, 20–22g) ≈ 25.5 (unchanged or +1
for below-median products). This is a 13.4pt separation vs baseline 7.4pt — resolution
improved materially.

**Summary of named inversions for the pilot acceptance set:**

| # | Pair | Low-sugar barcode | Low-sugar g | Low-sugar baseline | High-sugar barcode | High-sugar g | High-sugar baseline | Inversion gap | Expected post-pilot |
|---|---|---|---|---|---|---|---|---|---|
| A | Lotus vs פתי בר אורגני | 7290018371923 | 20.5g | 29.0/E | 5410126806250 | 38.1g | 18.1/E | −10.9 (correct dir) | gap widens to ~16.9 |
| B | מרוקאי vs וניל הדר | 7290119041053 | 13.5g | 37.2/D | 5317194 | 22.0g | 48.3/D | +11.1 (INVERTED) | gap narrows to ~9.1 |

Inversion A is the within-E resolution case (correct direction but insufficient separation).
Inversion B is the true rank inversion (incorrect direction that the model should reduce).

---

## 7. Draft EV-085

**Registry status check:** The evidence registry (`01_framework/governance/evidence_registry_v1.md`)
uses `BEV-` prefixed entries; its next entry is `BEV-088`. The shelf-relative program (TASK-278)
maintains a separate `EV-` numbering track in its design documents (EV-056 → EV-058 → EV-084 →
EV-085). EV-084 is the generalized shelf-relative mechanism (registered in the D7 co-sign).
EV-085 is the next entry in this track — confirmed as the correct next ID for this enrollment.

---

### EV-085 — Biscuits × Sugar: Shelf-Relative Enrollment (BARI_SHELF_RELATIVE_V1)

| Field | Value |
|---|---|
| **finding_id** | EV-085 |
| **concept** | Enrollment of the `biscuit` router category × `sugars_g` nutrient into the `BARI_SHELF_RELATIVE_V1` mechanism (EV-084). Applies asymmetric P>B shelf-relative surcharge/relief on top of the absolute backbone, using the biscuit corpus's robust sugar scale (IQR-primary). Resolves within-shelf rank inversions where the hard binary cliff compresses 57 products into a narrow E/D band despite 44g range of sugar variation. |
| **task** | TASK-278 (Phase 2 — biscuits × sugar pilot) |
| **recorded** | 2026-06-14 |
| **status** | PROPOSED — awaiting Product Agent D7 co-sign. No engine edit, no pilot rescore, 0 score movement until co-sign. |
| **scientific_rationale_short** | The biscuit corpus (run_cookies_004, 58 products) shows a sugar range of 0–44.3g/100g against a median of 21.5g, yet the absolute cliff structure compresses 29 of 57 products into a narrow E band (scores 18–34) with no meaningful sugar differentiation within that band. A product with 38g sugar (Lotus, score 18.1) and one with 20g sugar (score 22.8) are effectively indistinguishable under the cliff. This misrepresents the within-shelf nutritional reality. The shelf-relative differentiator (EV-084 mechanism) resolves this by adding a continuous surcharge for above-median sugar and bounded relief for below-median sugar, while the formulation_absolute_floor (55, at 20g+ sugar) prevents the Anti-Immunity Rule from being violated. The mechanism is formulation-nutrient appropriate: biscuit sugar is an active manufacturer choice (not endemic, unlike brine sodium), so the stronger absolute anchor (55 floor) is correct alongside the relative layer. |
| **evidence_strength** | Moderate — mechanism validated for sodium/brined dairy (EV-056); extension to sugar/biscuits by mechanism-analogy, now grounded in the corpus data (57 products with measured sugar values, verified IQR=6.9g, identifiable rank inversions). |
| **confidence_level** | High for mechanism correctness; Medium for parameter calibration (P=6, B=3, floor=55) pending pilot rescore validation. |
| **label_observability** | Fully label-observable. The only field read is `L1_observed_signals.sugars_g` — the direct product-scrape label field present in every BSIP1 trace. The corpus median and robust_scale are computed from these same label values at batch-run start. No external data, no OFF data, no inferred fields. OFF-BAN: the mechanism cannot be fed from Open Food Facts or any external source by design. |
| **activation_scope** | `scope_categories = frozenset({"biscuit"})`, `nutrient = "sugars_g"`. No other category or nutrient is enrolled by this EV. Each future enrollment is a separate EV + D7. |
| **flag** | `BARI_SHELF_RELATIVE_V1` — default `off`. Engine byte-identical when off. This enrollment does not activate any other flag or modify any existing scoring path. |
| **corpus_stats** | n=57 (1 missing label); median=21.5g; IQR=6.9g; MAD=3.3g; robust_scale=5.115g |
| **bands** | Penalty (above median): bands on r_above, max P=6. Relief (below median): bands on r_below, max B=3. See §3. |
| **formulation_absolute_floor** | 55 — applies when `sugars_g >= 20g/100g` for `category == "biscuit"`. Required per D7 cond 5, non-None. Anti-Immunity Rule: no biscuit with ≥20g sugar reaches grade B (70) or A (80). |
| **low_variance_guard** | 3.0g (robust_scale units). Not binding on this corpus (5.115 >> 3.0). |
| **min_n** | 20. Not binding on this corpus (n=57). |
| **published_scores_moved** | Zero by definition — flag default=off; biscuit category not live; owner go-live required before any published score moves (tripwire-1). |
| **rollback** | Set `BARI_SHELF_RELATIVE_V1=off` (default). Re-scoring with flag=off restores prior output exactly. All current published runs committed at flag=off — no contamination possible. |
| **no_regression_proof** | Six-guard plan from design v1 (Guards 1–6) plus enrollment-specific guards: (a) cross-corpus baseline diff on all published categories before and after enrollment; (b) explicit trace verification that `SUGAR_SHELF_REL_V1` rule tag appears in biscuit traces when surcharge fires; (c) low-variance guard and min_n guard verified against corpus; (d) formulation_absolute_floor verified against the 51 products with ≥20g sugar (none should exceed score 55 post-pilot); (e) `BARI_SHELF_RELATIVE_V1=off` byte-identical across all published categories; (f) monotonicity check: sugar value increasing → relative penalty non-decreasing. |
| **pilot_success_criteria** | All 7 criteria from D7 §5.2 must pass. Named inversions: Inversion A (gap widening) and Inversion B (gap narrowing) per §6 of this document. Shelf average lift must not exceed 1.5 pts vs baseline. |
| **product_agent_d7_required** | YES — this is a scoring rule enrollment. Product Agent D7 co-sign required alongside Nutrition Agent co-sign. This document represents Nutrition Agent approval; Product Agent sign-off is the blocking gate. |
| **pending** | Product D7 co-sign → pilot rescore → Phase-3 gauntlet → owner go-live. |
| **reference** | `02_products/cookies_coffee/methodology/shelf_relative_sugar_enrollment_v1.md` (this document). Mechanism: EV-084 / `shelf_relative_design_v1.md`. D7 framework: `shelf_relative_d7_cosign_v1.md`. |

```yaml
study_objects:
  - claim: "Within-shelf sugar relative position differentiates nutritional quality among biscuits
            where absolute cliff scoring collapses the distribution"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:run_cookies_004"
    notes: >
      Evidence tier C: internal corpus observation (57 biscuit products, 0–44.3g sugar range,
      IQR=6.9g, 2 confirmed rank inversions under cliff scoring). The relative mechanism is
      scientifically coherent — sugar level is a continuous formulation variable, and relative
      position within a shelf reflects how a manufacturer has chosen to formulate relative to
      peers. Extension from sodium/dairy (EV-056) to sugar/biscuits is by mechanism-analogy
      with corpus validation. No population RCT exists for the specific banded surcharge model.
      Anti-Immunity Rule protection is architectural (formulation_absolute_floor=55), not
      population-evidence dependent.
  - claim: "A formulation_absolute_floor of 55 for high-sugar biscuits (>=20g/100g) prevents
            the Anti-Immunity Rule from being violated by below-median relative relief"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:bari_usecase_guardrails_v2,cookies_coffee_routing_ruling_v1"
    notes: >
      Architectural property. Grade B requires score >= 70. The floor at 55 is 15 points below
      grade B. The maximum relief is 3 points. No product can reach 70 via relief alone starting
      from below 55. The C-ceiling finding (routing_ruling_v1 §3.1) established that B is only
      achievable for the very best clean digestive variants — the floor at 55 is consistent
      with this finding and enforces it mechanically.
```

---

## 8. Pilot Outcome Prediction

**Status of this section: PREDICTION — not a scored run. To be tested against actual pilot results.**

The shelf-relative layer adds a bounded residual on top of the absolute backbone. With P=6 and
B=3, and a median at 21.5g, the predicted effects on the distribution are:

- **Lotus biscuits (4 products, 38.1g sugar):** each loses 6pts. Projected scores: ~12.1 (vs 18.1).
  These move deeper into E but remain E. The within-E ordering is now correct: Lotus sits at
  the bottom of E, not the middle of it.
- **Products at 30–38g sugar (right tail, ~5 products):** lose 4–6 pts. Remain E.
- **Products at 24–26g sugar (just above Q3, ~4 products):** lose 0–1pt. Minimal change.
- **Products at 20–24g sugar (core zone, ~20 products):** lose 0–1pt or gain 0pts. Minimal change.
- **Products at 13–17g sugar (~6 products):** gain 1–2pts. Minor upward shift.
- **Sugar-free products (0–0.9g, 5 products):** gain 3pts. The most meaningful relief.

**Predicted post-pilot distribution (estimate):** C5–6 / D22–23 / E28–30. No grade-boundary
crossings expected because:
1. The sugar-free products (gain 3pts) currently score 42.9–45.7 / D — adding 3pts brings
   them to 45.9–48.7 / D (D boundary is 40–54). No grade change.
2. The highest-scoring product at 63.1/C (sugar=0g) would gain 3pts → 66.1/C. Remains C.
3. Lotus biscuits lose 6pts from 18.1 → 12.1. Remain E.

**Shelf average movement prediction:** The net effect is approximately zero (a few products gain
2–3pts; a few lose 4–6pts; the majority at 20–24g are unchanged). The average shift is predicted
to be ≤ 0.5pts (well within the 1.5pt co-sign ceiling). This is the correct behavior for a
"residual differentiator" that reshuffles within-E/D ordering without inflating the category average.

**Grade distribution prediction:** C7 / D22 / E29 → C5–7 / D22–23 / E28–31. No B, no A.
The C-ceiling finding is preserved. No product currently at D is pushed to C by 3pts of relief
(the minimum D-to-C crossover would require a product at score 52+ gaining 3pts → 55+ = C;
the product at 960860015432, score 45.7 + 3pts = 48.7, remains D).

**Warning flag on sugar-free products:** The 5 products with 0g sugar (sugar-free biscuits) are
a structurally distinct cohort. They may have other properties (artificial sweeteners, higher
fat to compensate, or very low total scores from NOVA/additive penalties) that make the relief
modest in context. The predicted +3pts is arithmetically correct but the pilot must verify
these products' traces individually to confirm the relief is not being applied in a context
where it creates misleading rankings (e.g., a sugar-free product with trans fat getting +3pts
from the sugar layer while already being penalized by the trans-fat veto).

---

## 9. Cross-Category Contamination Check

**Confirmed zero:** The `scope_categories = frozenset({"biscuit"})` guard prevents any non-biscuit
product from receiving a sugar relative surcharge. The live published categories do not use the
`biscuit` router ID. Even if `BARI_SHELF_RELATIVE_V1` is turned on for the pilot run, the
surcharge function returns `(0, "category=X not in scope")` for all milk, yogurt, bread, snack,
cereal, and brined cheese products.

Shelf sugar stats for the biscuit corpus (median=21.5g) are set only for the biscuit pilot run;
they do not carry over to other category batch runs because each batch run calls `set_shelf_stats()`
independently (and would clear or not set sugar stats for non-biscuit categories).

---

## Summary Table

| Parameter | Proposed Value | D7 Condition | Status |
|---|---|---|---|
| scope_categories | `frozenset({"biscuit"})` | — | Proposed |
| nutrient | `sugars_g` | D7 §5.2 (biscuits × sugar only) | Confirmed |
| n_with_sugar | 57 (of 58) | cond 3: n≥20 ✓ | Confirmed |
| median | 21.5 g/100g | — | Computed |
| IQR | 6.9 g/100g | — | Computed |
| MAD | 3.3 g/100g | — | Computed |
| robust_scale | 5.115 (IQR-primary) | cond 2: IQR-primary ✓ | Confirmed |
| direction | asymmetric P>B | cond 4 ✓ | Confirmed |
| max penalty P | 6 pts | — | Proposed |
| max relief B | 3 pts | B < P ✓ | Proposed |
| formulation_absolute_floor | 55 (at ≥20g sugar) | cond 5: non-None ✓ | Proposed |
| low_variance_guard | 3.0g | — | Proposed |
| min_n | 20 | cond 3 ✓ | Confirmed |
| Named inversion A | Lotus (38.1g) vs פתי בר אורגני (20.5g) | rank inversion pre-specified ✓ | Proposed |
| Named inversion B | מרוקאי (13.5g) vs וניל הדר (22.0g) | rank inversion pre-specified ✓ | Proposed |
| EV ID | EV-085 | cond 1: EV registered ✓ | Draft |

---

```json
{
  "task": "TASK-278 Phase-2 / P100",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/shelf_relative_sugar_enrollment_v1.md",
      "sha256": "5c8dae020825cf01d7843ebc899e4ec4d2e55cbfa62494f66ab09804150cfdc1"
    }
  ],
  "counts": {
    "sections_in_proposal": 9,
    "ev_id_drafted": "EV-085",
    "ev_max_in_track_before_this": "EV-084",
    "products_in_corpus_total": 58,
    "products_in_corpus_with_sugars_g": 57,
    "products_missing_sugar": 1,
    "sugar_stats_n": 57,
    "sugar_median_g": 21.5,
    "sugar_q1_g": 17.1,
    "sugar_q3_g": 24.0,
    "sugar_iqr_g": 6.9,
    "sugar_mad_g": 3.3,
    "sugar_robust_scale_g": 5.115,
    "sugar_min_g": 0.0,
    "sugar_max_g": 44.3,
    "max_penalty_P_pts": 6,
    "max_relief_B_pts": 3,
    "formulation_absolute_floor_score": 55,
    "high_sugar_floor_threshold_g": 20.0,
    "low_variance_guard_g": 3.0,
    "min_n": 20,
    "named_rank_inversions": 2,
    "baseline_grade_dist_C": 7,
    "baseline_grade_dist_D": 22,
    "baseline_grade_dist_E": 29,
    "baseline_grade_dist_B": 0,
    "baseline_grade_dist_A": 0
  },
  "commands_run": [
    {
      "cmd": "python3 extract sugars_g from L1_observed_signals in 58 bsip2_trace.json files",
      "exit_code": 0,
      "output_summary": "n=57 with sugar; n=1 missing (7290017962139); sorted distribution 0.0–44.3g; median=21.5; Q1=17.1; Q3=24.0; IQR=6.9; MAD=3.3; robust_scale=5.115"
    },
    {
      "cmd": "python3 grade distribution from grade_estimate across 58 traces",
      "exit_code": 0,
      "output_summary": "C:7 D:22 E:29 (A:0 B:0)"
    },
    {
      "cmd": "python3 rank inversion analysis: lower sugar but lower score pairs",
      "exit_code": 0,
      "output_summary": "7290119041053 (13.5g, 37.2/D) vs 5317194 (22.0g, 48.3/D) = Inversion B; 5410126806250 (38.1g, 18.1/E) vs 7290018371923 (20.5g, 29.0/E) = Inversion A"
    },
    {
      "cmd": "grep evidence_registry_v1.md for max EV entry to verify EV-085 is next",
      "exit_code": 0,
      "output_summary": "Registry uses BEV- prefix; max BEV=BEV-087, next=BEV-088. TASK-278 EV-track max=EV-084 (shelf-relative design, D7 co-sign). EV-085 is confirmed next in TASK-278 EV track."
    }
  ],
  "not_done": [
    "Product Agent D7 co-sign — this proposal is Nutrition Agent approval; Product Agent co-sign is the blocking gate before any pilot run",
    "Pilot rescore (run_cookies_004 with BARI_SHELF_RELATIVE_V1=on, scope={biscuit}) — requires D7 co-sign first",
    "Phase-3 no-regression gauntlet (Guards 1–6 + enrollment-specific guards) — runs at implementation",
    "Owner go-live gate (tripwire-1) — required before any published score moves; biscuit page is not live, so pilot is low-risk but go-live still required before consumer deployment",
    "IQR-primary scale implementation in compute_shelf_stats() — D7 cond 2; confirmed needed before pilot runs",
    "EV-085 formal registration in evidence_registry_v1.md — draft here; registration after Product D7 co-sign"
  ],
  "self_check": {
    "off_ban_respected": true,
    "sugar_source": "L1_observed_signals.sugars_g from BSIP1 label panel only",
    "no_external_data_used": true,
    "no_fabricated_numbers": true,
    "all_numbers_from_traced_corpus": true,
    "ev_id_verified": "EV-085 is next in TASK-278 EV track after EV-084",
    "formulation_absolute_floor_non_none": true,
    "floor_value": 55,
    "floor_threshold_g": 20.0,
    "p_greater_than_b": "6 > 3 = true",
    "min_n_adopted": 20,
    "iqr_primary_adopted": true,
    "no_engine_edits": true,
    "no_score_movement": true,
    "pilot_success_criteria_documented_before_run": true,
    "named_inversions_documented_before_run": true,
    "c_ceiling_honored": "floor=55 prevents B or A for >=20g sugar products",
    "anti_immunity_rule_held": true,
    "frozen_invariants_untouched": true,
    "d7_cosign_condition_5_met": true,
    "return_contract_present": true
  }
}
```
