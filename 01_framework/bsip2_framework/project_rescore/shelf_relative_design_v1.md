# Shelf-Relative Differentiator — Generalization Design v1
**Task:** TASK-278 — Project Rescore (Bari-wide program)
**Date:** 2026-06-14
**Author:** Nutrition Agent
**Status:** RETURNED — awaiting Product Agent D7 co-sign + owner philosophy calls
**Predecessor:** EV-056 (`BARI_SODIUM_SHELF_RELATIVE_V1`, sodium-only, brined dairy)

---

## Purpose and Scope

This document specifies the **design** of a category-agnostic, nutrient-agnostic generalization
of the EV-056 shelf-relative sodium surcharge mechanism into a parameterized capability that can
be applied across nutrients (sodium, sugar, sat_fat) and categories.

**What this design is NOT:**
- Not an implementation spec. No engine code is written or modified.
- Not a scoring decision. No published scores move.
- Not a philosophy ruling. The two owner-level philosophy forks are surfaced and designed around;
  they are not resolved here.

**What this design IS:**
- A parameterized function contract that makes the EV-056 pattern reusable.
- A new flag proposal (`BARI_SHELF_RELATIVE_V1`) with explicit backward-compat guarantees.
- A pending-decisions register for the C3 math consult and the owner's two forks.
- A no-regression plan mirroring the six-guard EV-055/056 pattern.
- A draft EV-084 registry entry.

---

## 1. Function Contract

### 1.1 The generalization intent

The EV-056 mechanism does two things that must be separated at design time:

**Layer A — Absolute backbone.** Graduated bands (`SODIUM_GENERAL_BANDS`) replace the hard
cliff (HIGH_SODIUM_700MG_PLUS). This layer uses only the product's own label value. It is already
live under `BARI_GRAD_SODIUM_V1` for endemic-sodium categories.

**Layer B — Shelf-relative differentiator (EV-056 today).** A surcharge keyed on the product's
*distance above the corpus median* — `max(0, value - shelf_median)` — bands into additional
penalty. This layer requires a corpus-level statistic (median + spread measure) computed before
the scoring loop runs.

The orchestrator's synthesis: both layers are required. The absolute backbone prevents
"best-of-a-bad-shelf" curve-grading immunity (which violates the Anti-Immunity Rule and the
"no snack bar reaches A" invariant). The relative differentiator restores within-shelf
resolution that the absolute backbone alone cannot provide when a category clusters at high
values.

### 1.2 Generalized `set_shelf_stats()` — replacing `set_shelf_sodium_stats()`

The current engine has one pair of module-level globals per nutrient (sodium). The generalization
uses a nutrient-keyed dict:

```python
# Module-level state — generalized shelf context (BARI_SHELF_RELATIVE_V1)
_SHELF_STATS: dict[str, dict] = {}
# Key: nutrient name ("sodium_mg" | "sugars_g" | "fat_saturated_g" | ...)
# Value: {"median": float, "scale": float, "scale_type": "stdev" | "mad" | "iqr"}

def set_shelf_stats(
    nutrient: str,          # canonical key matching normalized_nutrition_per_100g key
    median: float | None,
    scale: float | None,
    scale_type: str = "stdev",   # "stdev" | "mad" | "iqr"
) -> None:
    """Set corpus shelf statistics for a given nutrient. Called by the batch runner
    before the scoring loop. Multiple nutrients can be set independently."""
    global _SHELF_STATS
    if median is None or scale is None:
        _SHELF_STATS.pop(nutrient, None)
    else:
        _SHELF_STATS[nutrient] = {
            "median": float(median),
            "scale": float(scale),
            "scale_type": scale_type,
        }


def clear_shelf_stats(nutrient: str | None = None) -> None:
    """Clear stats for one nutrient, or all if nutrient is None."""
    global _SHELF_STATS
    if nutrient is None:
        _SHELF_STATS.clear()
    else:
        _SHELF_STATS.pop(nutrient, None)


def compute_shelf_stats(
    products: list,
    nutrient: str,
    scale_type: str = "stdev",
) -> tuple[float | None, float | None]:
    """Compute median and spread measure for a nutrient across a product corpus.
    Returns (median, scale) — scale semantics depend on scale_type.
    Reads only normalized_nutrition_per_100g[nutrient] — label-panel field only.
    OFF-BAN: no external source ever fed here."""
    values = [
        float(prod.get("normalized_nutrition_per_100g", {}).get(nutrient))
        for prod in products
        if prod.get("normalized_nutrition_per_100g", {}).get(nutrient) is not None
    ]
    if not values:
        return None, None
    values.sort()
    n = len(values)
    median = values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2.0
    if scale_type == "mad":
        deviations = sorted(abs(v - median) for v in values)
        scale = deviations[n // 2] if n % 2 else (deviations[n // 2 - 1] + deviations[n // 2]) / 2.0
    elif scale_type == "iqr":
        q1 = values[n // 4]
        q3 = values[(3 * n) // 4]
        scale = q3 - q1
    else:  # default: population stdev
        mean = sum(values) / n
        scale = (sum((x - mean) ** 2 for x in values) / n) ** 0.5
    return round(median, 2), round(scale, 2)
```

**Backward compat with EV-056:** `set_shelf_sodium_stats(median, stdev)` continues to exist
and internally calls `set_shelf_stats("sodium_mg", median, stdev, "stdev")`. The legacy function
is never removed — its callers (`batch_run_brined.py`) require no change when this flag is off.

### 1.3 Core differentiator function

```python
def shelf_relative_differentiator(
    value: float,                        # product's label value (e.g. sodium_mg)
    nutrient: str,                       # key matching _SHELF_STATS + nutrition panel
    scope_categories: frozenset[str],    # categories where this fires
    category: str,                       # product's routing category
    surcharge_bands: list[tuple],        # (lo, hi_or_None, penalty_points) on distance_above
    low_variance_guard: float,           # minimum scale value to allow surcharge (prevents punishing
                                         # tight shelves); maps to SODIUM_SHELF_STDEV_GUARD pattern
    min_n: int = 10,                     # minimum corpus size to compute; below this, suppressed
    direction: str = "one_sided_high",   # "one_sided_high" | "one_sided_low" | "two_sided"
    mapping: str = "banded",             # "banded" | "clamped_linear" | "tanh"
                                         # "banded" = EV-056 behavior (recommended default;
                                         # see section 3 for the pending C3 math call)
) -> tuple[int, str | None]:
    """Return (surcharge_penalty, diagnostic_note) for the shelf-relative layer.

    Returns (0, None) if:
      - category not in scope_categories
      - _SHELF_STATS[nutrient] not populated
      - scale < low_variance_guard (low-variance guard)
      - corpus size < min_n
      - value <= shelf_median (one_sided_high, no reward for being below median)

    The surcharge_penalty is ADDITIVE to the absolute backbone penalty and subject to the
    shared family budget (see section 1.4).

    OFF-BAN: reads only _SHELF_STATS populated from label-panel fields; no external source.
    """
    if category not in scope_categories:
        return 0, f"category={category} not in scope"
    stats = _SHELF_STATS.get(nutrient)
    if stats is None:
        return 0, f"{nutrient}: shelf stats not set"
    median = stats["median"]
    scale = stats["scale"]
    if scale < low_variance_guard:
        return 0, f"{nutrient}: scale={scale} < guard={low_variance_guard} — suppressed"

    if direction == "one_sided_high":
        distance = max(0.0, value - median)
    elif direction == "one_sided_low":
        distance = max(0.0, median - value)
    else:  # two_sided
        distance = abs(value - median)

    if mapping == "banded":
        penalty = _band_lookup(distance, surcharge_bands)
    elif mapping == "clamped_linear":
        # Pending C3 decision — placeholder; uses banded as safe fallback
        penalty = _band_lookup(distance, surcharge_bands)
    elif mapping == "tanh":
        # Pending C3 decision — placeholder; uses banded as safe fallback
        penalty = _band_lookup(distance, surcharge_bands)
    else:
        penalty = _band_lookup(distance, surcharge_bands)

    note = f"{nutrient}={value} dist_above_median={distance:.0f} band_penalty={penalty}"
    return penalty, note


def _band_lookup(distance: float, bands: list[tuple]) -> int:
    """(lo, hi_or_None, penalty) band lookup on distance. Same pattern as EV-056."""
    for lo, hi, pen in bands:
        if hi is None:
            if distance >= lo:
                return pen
        elif lo <= distance <= hi:
            return pen
    return 0
```

### 1.4 Blending with the absolute graduated backbone

The shelf-relative surcharge is **additive** to the absolute graduated backbone penalty, subject
to the nutrient's family budget:

```
total_penalty = clip(absolute_backbone_pen + shelf_relative_surcharge, 0, family_budget)
```

The family budget controls the maximum total penalty from both layers combined. EV-056 already
raised the sodium family budget for brined/endemic dairy from 8 to 16 (`SODIUM_FAMILY_BUDGET_BRINED`).
The same raise-per-category mechanism generalizes: when `BARI_SHELF_RELATIVE_V1` is on for a
category/nutrient pair, the config may specify an elevated family budget to prevent the combined
penalty from being artificially capped at the original single-layer budget.

**The family budget raise is itself a per-category D7 decision** — not hardcoded in this design.
The design provides the mechanism; the magnitude per category/nutrient comes at rollout.

**One-sided-high architecture:** For nutrients where "higher is worse" (sodium, sugar, sat_fat in
most contexts), the surcharge fires only when `value > median`. A product below the category median
receives no shelf-relative penalty and no shelf-relative reward. This preserves the absolute backbone
as the floor of differentiation. A product that is cleaner than the median is already rewarded by its
lower absolute penalty; the relative layer does not add a bonus on top (no reward for being the
"least bad" on a bad shelf).

---

## 2. Flag Design

### 2.1 Proposed flag: `BARI_SHELF_RELATIVE_V1`

```python
# TASK-278 / EV-084 — Category-agnostic shelf-relative differentiator.
# DEFAULT OFF → engine byte-identical to baseline when off.
# Activates only when BOTH:
#   (a) BARI_SHELF_RELATIVE_V1=on
#   (b) The underlying absolute-backbone flag for the nutrient is also on
#       (e.g. BARI_GRAD_SODIUM_V1 for sodium; analogous flags for sugar/sat_fat TBD).
# Reads _SHELF_STATS[nutrient] populated by set_shelf_stats() before the scoring loop.
# Per-category, per-nutrient surcharge bands are configuration inputs at rollout — no
# hardcoded activation scope in the flag declaration itself (unlike EV-056 which was
# sodium+dairy-only). Scope is controlled by the `scope_categories` parameter passed
# to shelf_relative_differentiator() at each call site.
# D7 co-sign: Nutrition Agent (this document) + Product Agent (pending).
# Owner go-live: required before any published category is rescored with this flag on.
BARI_SHELF_RELATIVE_V1 = os.environ.get("BARI_SHELF_RELATIVE_V1", "off").lower() == "on"
```

### 2.2 Relationship to existing flags

| Existing flag | Relationship to `BARI_SHELF_RELATIVE_V1` |
|---|---|
| `BARI_SODIUM_SHELF_RELATIVE_V1` (EV-056) | SUPERSEDED by `BARI_SHELF_RELATIVE_V1` for sodium in endemic dairy — but ONLY after the generalized mechanism is validated on the same corpus. Until then, EV-056 remains live and `BARI_SODIUM_SHELF_RELATIVE_V1` continues to control sodium/dairy. No removal without explicit backward-compat verification. |
| `BARI_GRAD_SODIUM_V1` (EV-055) | PREREQUISITE for the sodium relative layer — `BARI_SHELF_RELATIVE_V1` activates the sodium surcharge ONLY when `BARI_GRAD_SODIUM_V1` is also on. Same dependency chain as today. |
| `BARI_REDLABEL_V1` | INDEPENDENT — `BARI_SHELF_RELATIVE_V1` does not activate or depend on `BARI_REDLABEL_V1`. The bundled flag continues to enable EV-056's sodium/dairy path as before (backward compat). |
| `BARI_GRAD_SODIUM_V1` / `BARI_SODIUM_SHELF_RELATIVE_V1` together | When BOTH are on, the EV-056 sodium path continues to fire as today, UNCHANGED. `BARI_SHELF_RELATIVE_V1` is ADDITIVE new capability — it does not modify or replace the EV-056 call site until an explicit migration step is D7-approved. |

**Byte-identical guarantee when off:** When `BARI_SHELF_RELATIVE_V1=off` (the default), no code
path in the generalized function is reachable. The `shelf_relative_differentiator()` function
exists in the module but no call site invokes it unless the flag is on. The existing EV-056 path
(`_shelf_sodium_active` block in score_engine.py ~L2155) continues to operate exactly as today
under its own flags (`BARI_SODIUM_SHELF_RELATIVE_V1` + `BARI_GRAD_SODIUM_V1`). The new flag does
not touch that block.

### 2.3 Call-site architecture

At each nutrient's scoring block, a call to `shelf_relative_differentiator()` is added,
**gated by `BARI_SHELF_RELATIVE_V1`**:

```python
# Example: inside the sodium scoring block, after the absolute backbone penalty is computed:
if BARI_SHELF_RELATIVE_V1:
    _rel_pen, _rel_note = shelf_relative_differentiator(
        value=sodium,
        nutrient="sodium_mg",
        scope_categories=SODIUM_SHELF_REL_SCOPE,   # frozenset — per-category config
        category=category,
        surcharge_bands=SODIUM_SHELF_SURCHARGE_BANDS_V2,  # may reuse EV-056 values
        low_variance_guard=SODIUM_SHELF_STDEV_GUARD,
        direction="one_sided_high",
        mapping="banded",
    )
    if _rel_pen > 0:
        sodium_pens_fired.append(("SODIUM_SHELF_REL_V1", _rel_pen))
        # ... trace annotation ...
```

The per-category config constants (`SODIUM_SHELF_REL_SCOPE`, `SUGAR_SHELF_REL_SCOPE`, etc.) are
defined in `constants.py` and are the D7 inputs — the mechanism does not hardcode scope.

---

## 3. Scale Selection Recommendation

The design takes `scale_type` as a parameter. The recommendation for the default:

**Recommend: `stdev` (population standard deviation) as the default, with `min_n >= 10`.**

Rationale from EV-056 precedent: `SODIUM_SHELF_STDEV_GUARD = 150` mg is calibrated to population
stdev, which is what `compute_shelf_sodium_stats()` already computes. The brined-cheese corpus
(n~36–48) has adequate n for stdev to be stable. `stdev` is also the simplest for the C3
consult to evaluate mathematically.

**Open C3 question (section 5.1):** Whether MAD or IQR is more robust for smaller corpora (n < 20)
or skewed nutrient distributions (e.g. sugar in biscuits where most products cluster at 20–30g
but a few hit 50g+). The function signature accommodates any of the three — `scale_type` is a
parameter, not a constant.

---

## 4. Philosophy Fork Accommodation

The design explicitly accommodates BOTH branches of the two owner-level philosophy calls without
hardcoding either. This is the critical requirement from the TASK-278 brief: "design the mechanism
to accommodate EITHER branch."

### Fork 1 — Cross-category comparability

**The question:** Should the shelf-relative component produce scores that are comparable *across*
categories (e.g. can a biscuit with 25g sugar compare directly to a cereal with 25g sugar on
a normalized scale), or is Bari's scoring explicitly within-category-relative (a biscuit is
rated against biscuits, a cereal against cereals)?

**Branch A — Absolute backbone keeps numbers comparable:** The absolute graduated bands are
calibrated on a nutrient-wide absolute scale (same mg thresholds for all categories). The
shelf-relative layer is a within-category adjustment on top. The composite is still anchored to
the absolute scale, so cross-category comparison is preserved for the backbone signal. The
relative layer adds within-category resolution but is small enough (family-budget-constrained)
not to destroy comparability.

**Branch B — Explicitly category-relative scale:** The absolute backbone thresholds are
themselves calibrated per-category (analogous to `CALORIE_DENSITY_TABLES` which has a distinct
table per category). The relative layer operates on category-specific thresholds. Cross-category
comparisons are explicitly disclaimed at the UI layer (categories are compared within their own
shelf).

**Mechanism design to accommodate both:**
- Branch A: Reuse `SODIUM_GENERAL_BANDS` as-is for all categories. Category specificity comes
  only from the scope guard and the shelf-relative surcharge bands.
- Branch B: Add a `NUTRIENT_ABSOLUTE_BANDS_BY_CATEGORY` constant (dict of category → bands)
  used when `BARI_SHELF_RELATIVE_V1` is on. When the dict has no entry for a category, falls
  back to `SODIUM_GENERAL_BANDS`. No architecture change required — it is a constants lookup.

This fork resolves at D7 time by whether the per-category absolute bands are set or left as
the global fallback.

### Fork 2 — Endemic vs. formulation nutrients

**The question:** Should formulation nutrients (e.g. biscuit sugar — which the manufacturer
freely chooses and can reduce) receive the same shelf-relative treatment as structural/endemic
nutrients (e.g. brine-cheese sodium — which is a production artifact)?

The owner's initial directive pushes relative scoring INTO formulation nutrients (e.g. biscuit
sugar). The principle being challenged: does a relative layer give "the least-bad biscuit"
unwarranted immunity if all biscuits have high sugar?

**Branch A — Formulation nutrients keep a stronger absolute anchor:** Sugar and sat_fat in
formulation categories retain the hard cliff (or at most a graduated absolute penalty) without
a shelf-relative surcharge. The Anti-Immunity Rule is implemented by NOT adding the relative
layer for these nutrients. A product that is "best of a bad shelf" is held by the absolute
backbone. The relative layer is reserved for endemic nutrients only.

**Branch B — Relative layer extends to formulation nutrients, with a hardened absolute floor:**
The shelf-relative surcharge is applied to sugar/sat_fat in formulation categories, but the
absolute backbone is calibrated to ensure no biscuit with 25g+ sugar reaches a grade above D
regardless of shelf median. The Anti-Immunity Rule is implemented via the absolute backbone
floor, not by excluding the relative layer. A biscuit at the low end of a high-sugar shelf
receives modest relative relief; the absolute floor prevents that relief from reaching A or B.

**Mechanism design to accommodate both:**
- A `formulation_absolute_floor: float | None` parameter on `shelf_relative_differentiator()`,
  or equivalently a `NUTRIENT_SHELF_ANTI_IMMUNITY_FLOOR` constant dict. When set for a
  nutrient/category pair, the composite score (after absolute + relative layers) is clamped
  to no higher than the floor, regardless of the relative surcharge direction.
- Branch A: set `formulation_absolute_floor = None` for endemic nutrients; hard-coded NO-FIRE
  for formulation nutrients at rollout by leaving them out of `scope_categories`.
- Branch B: set `formulation_absolute_floor` to e.g. 55 for biscuit/sugar (no biscuit with
  high sugar reaches C grade). The relative layer fires but the floor holds.

This is the owner's most important philosophy call. The mechanism allows it without a code
architecture change.

---

## 5. Pending Decisions

### 5.1 C3 Math Consult (P96, running concurrently)

These questions require mathematical analysis that Bari cannot resolve from corpus data alone.
C3 input is requested before implementation:

1. **Scale selection for small corpora.** At what minimum n does `stdev` become unstable
   relative to MAD or IQR? The brined-cheese corpus is n~36; a future cookie or biscuit
   corpus may be n~20–30. What is the crossover point? Recommendation requested: stdev vs
   MAD vs IQR and the minimum n floor per scale type.

2. **Mapping shape.** The banded mapping (EV-056's current approach) creates discontinuities
   at band boundaries (a product at 199mg above median and one at 200mg above median receive
   different penalties). Is a clamped-linear or tanh mapping preferable for continuity, and
   does it materially change outcomes at realistic corpus distributions? Recommendation
   requested: banded vs linear vs tanh and the conditions under which each is preferred.

3. **Family budget calibration.** The EV-056 raise from 8 to 16 for brined dairy was
   calibrated empirically. For sugar in biscuits or sat_fat in a formulation category, what
   is the principled way to set the combined family budget so the absolute + relative penalty
   is not double-penalizing? Specifically: is there a compositional rule (e.g. budget =
   max_absolute_band_pen + max_relative_band_pen) that prevents over-penalization without
   needing per-category empirical tuning?

4. **Two-sided application.** For some nutrients (e.g. fiber, where more is better), a
   one-sided-low version is needed (penalize products far below the median). Does the
   mathematics change substantially for two-sided vs one-sided? Specifically: does the
   distance measure need to be normalized by the scale (z-score style) rather than absolute
   distance when applying the same band thresholds in both directions?

### 5.2 Owner Philosophy Calls (tripwire-1 and tripwire-5)

These are OWNER-LEVEL decisions. Neither Nutrition Agent nor Product Agent resolves them.
They must be called before D7 parameter selection at rollout:

**Call A — Cross-category comparability (Fork 1 above):**
> Does Bari publish category-relative scores (biscuits are only compared to biscuits, with
> category-relative thresholds) or absolute scores (all food is scored on one absolute scale
> with shelf-relative adjustment as a within-category refiner)?

This determines whether `NUTRIENT_ABSOLUTE_BANDS_BY_CATEGORY` is populated or global bands
are used universally. If category-relative: the UI layer must disclaim cross-category
comparisons. If absolute: the current band structure is reused and cross-category comparison
is preserved (with the caveat that a biscuit at 50 and a cereal at 50 mean different things
nutritionally — Bari already addresses this through dimension weighting, not absolute-scale
redefinition).

**Call B — Endemic vs. formulation nutrients (Fork 2 above):**
> Does the shelf-relative layer extend to formulation nutrients (sugar in biscuits,
> sat_fat in processed spreads), and if so, what is the absolute floor that prevents
> the Anti-Immunity Rule from being violated?

This is the most consequential philosophy call in the program. If the answer is "formulation
nutrients get relative treatment with an absolute floor," the absolute floor value for each
category/nutrient pair is a specific number that must be owner-approved before D7 can finalize
parameters.

---

## 6. No-Regression Plan

Mirrors the EV-055/056 six-guard pattern. These guards are REQUIRED before any engine merge:

### Guard 1 — Frozen milk byte-identical (tripwire-1)
**Command:** Re-score `run_005_headpin` with `BARI_SHELF_RELATIVE_V1=on`, all other flags as
per the run's environment.
**Expected:** All 20 products byte-identical. milk_scores_moved = 0.
**Basis:** Milk sodium is 40–60mg. Even if sodium shelf stats for dairy_protein are set,
the absolute backbone already produces 0 penalty for these products. The relative surcharge
(`max(0, 40-median)` where median is likely 300–1000mg for any brined cheese corpus) = 0.
**Failure condition:** Any milk score moves → HALT, investigate scope leak.

### Guard 2 — All published categories byte-identical under flag OFF
**Command:** Re-score all 7+ published categories with `BARI_SHELF_RELATIVE_V1=off` (the
default). Compare byte-for-byte against committed baseline traces.
**Expected:** 0 score movements across all published categories.
**Basis:** The flag is default-off. No call site executes when flag is off.
**Failure condition:** Any published score moves under flag-off → flag declaration has a syntax
error or a call site is not properly guarded.

### Guard 3 — Engine invariants suite
**Command:** `python C:\Bari\03_operations\bsip2\proto_v0\tests\engine_invariants.py`
**Expected:** All 342 cases pass.
**Failure condition:** Any case fails → do not merge.

### Guard 4 — EV-056 sodium path byte-identical under combined flags
**Command:** Re-score the brined-cheese corpus with `BARI_GRAD_SODIUM_V1=on` +
`BARI_SODIUM_SHELF_RELATIVE_V1=on` + `BARI_SHELF_RELATIVE_V1=off`.
**Expected:** Results byte-identical to the committed brined-cheese baseline. The new general
flag being off must not interfere with the existing EV-056 path.
**Basis:** The EV-056 path is in a separate code block (`_shelf_sodium_active`) that is not
touched by the new flag's call sites.
**Failure condition:** Any brined product changes score → new code has an unintended side effect
on the existing path.

### Guard 5 — Monotonicity invariant for the new mechanism
**Command:** Construct a synthetic product suite where nutrient value increases monotonically
from 0 to max. Verify that `shelf_relative_differentiator()` output is monotonically
non-decreasing (higher value = higher or equal penalty).
**Expected:** For `one_sided_high` direction with banded mapping, penalty is monotonically
non-decreasing. For a given median, a product at value=X+1 never has lower relative penalty
than value=X.
**Failure condition:** Any inversion → band table is mis-ordered or the distance computation
has a sign error.

### Guard 6 — Non-scope categories fire = zero
**Command:** Re-score cereals, snack-bars, and bread corpora with `BARI_SHELF_RELATIVE_V1=on`
but with `scope_categories` set to an empty frozenset (the initial state before any category
is enrolled). Verify that all products receive 0 relative surcharge.
**Expected:** No category not in `scope_categories` receives any relative penalty.
**Basis:** The scope guard in `shelf_relative_differentiator()` returns (0, ...) for any
category not in the set. An empty set fires on nothing.
**Failure condition:** Any product in an un-enrolled category receives a non-zero surcharge →
scope guard is broken.

### Additional guard for each category enrolled at rollout

When any future category/nutrient pair is enrolled (i.e., added to `scope_categories` under
`BARI_SHELF_RELATIVE_V1`), the following are added to the guard set for that enrollment:

- Cross-corpus baseline diff on ALL published categories (the requirement from return_contract_v1.md
  §8: "scope/keyword/routing/flag changes require a full cross-corpus baseline diff — from the
  first one").
- Explicit verification that the enrolled category's trace shows the `NUTRIENT_SHELF_REL_V1`
  rule tag when the surcharge fires.
- Verify the low-variance guard fires correctly on small corpora (n < `min_n`).

---

## 7. Draft EV-084 Registry Entry

```
### EV-084 — Category-Agnostic Shelf-Relative Nutrient Differentiator (`BARI_SHELF_RELATIVE_V1`)
```

| Field | Value |
|---|---|
| **finding_id** | EV-084 |
| **concept** | Generalized shelf-relative nutrient surcharge: parameterized extension of EV-056 (sodium/dairy) to any nutrient and any category. Shelf median + spread measure computed from the corpus at batch-run start; distance-above-median banded into additional penalty on top of the absolute graduated backbone. |
| **task** | TASK-278 — Project Rescore (Bari-wide program); design phase only |
| **recorded** | 2026-06-14 |
| **status** | DESIGN — not implemented. D7 co-sign pending (Product Agent). Owner philosophy calls pending (Calls A + B in §5.2). |
| **scientific_rationale_short** | The EV-056 sodium/dairy mechanism proved that within-shelf relative position is nutritionally meaningful — a product 600mg above the shelf median is a materially different nutritional proposition from one at or below median, even if both exceed the same absolute band. This principle extends to other nutrients (sugar in confectionery, sat_fat in spreads) where absolute thresholds alone cannot distinguish reformulation effort within a category. The relative layer adds within-category resolution without replacing the absolute backbone (which holds the Anti-Immunity Rule). For endemic nutrients (sodium in brined cheese), the relative layer has empirical support from the 42/48 brined-cheese corpus pin (EV-055/056). For formulation nutrients, the case is philosophical: the owner must decide whether "best-of-a-bad-shelf" deserves relative scoring with an absolute floor, or whether the hard absolute backbone is the correct deterrent (Fork 2, §5.2 of design). Evidence strength for the generalized extension: Moderate — mechanism established for sodium/dairy; extension to other nutrients is by analogy + will require per-category empirical validation. |
| **evidence_strength** | Moderate — sodium/dairy mechanism empirically confirmed (EV-055/056); extension to other nutrients by mechanism-analogy pending per-category validation at rollout |
| **confidence_level** | High for mechanism design; Low for per-category parameter values until rollout calibration |
| **BSIP2_relevance** | Direct — this is the core mechanism for TASK-278 Project Rescore |
| **label_observability** | Fully label-observable. The differentiator reads only `normalized_nutrition_per_100g[nutrient]` — the same nutrition panel field already present in every BSIP1 trace. The corpus median/scale is computed from those same label fields across the run corpus. No external data, no OFF data, no inferred fields. OFF-BAN: the mechanism cannot be fed from Open Food Facts or any external source by design — it reads only BSIP1 nutrition panel fields. |
| **implementation_complexity** | Low-Medium — generalized `set_shelf_stats()` / `compute_shelf_stats()` / `shelf_relative_differentiator()` functions; call-site additions per nutrient/flag guard; backward-compat with EV-056 path preserved without modification to existing code |
| **recommended_action** | implement_after_D7_cosign_and_owner_philosophy_calls |
| **activation_scope** | Configured at rollout via `scope_categories` frozenset per nutrient. Initially empty (no category enrolled). Each category enrollment is a separate D7 decision. The mechanism is category-agnostic; the policy of which categories use it is D7-governed. |
| **flag** | `BARI_SHELF_RELATIVE_V1` — default `off`. Engine byte-identical when off. Does NOT activate or modify the existing EV-056 path (controlled by `BARI_SODIUM_SHELF_RELATIVE_V1`). Both flags can coexist; EV-056 is the backward-compat predecessor for sodium/dairy. |
| **published_scores_moved** | Zero by definition — flag default=off; owner go-live required before any published category is rescored with flag on (tripwire-1). |
| **rollback** | Set `BARI_SHELF_RELATIVE_V1=off` (default). All published runs committed at flag=off. Re-scoring with flag=off restores prior output exactly. The flag is a feature gate; no data is modified by enabling/disabling it. |
| **no_regression_proof** | Six-guard plan in §6 of this design document. Guards 1–6 must pass before merge. Guard 1 (frozen milk byte-identical) and Guard 2 (all published categories byte-identical at flag-off) are the mandatory preconditions. |
| **pending_decisions** | (C3) Scale selection (stdev vs MAD vs IQR); mapping shape (banded vs linear vs tanh); family budget calibration rule; two-sided normalization. (Owner Call A) Cross-category comparability. (Owner Call B) Endemic vs. formulation nutrient policy + absolute floor per nutrient/category. No D7 parameter finalization until these are resolved. |
| **governance_classification** | New scoring capability (not a new scoring rule per se — a parameterized extension of an existing approved mechanism). Requires D7 co-sign: Nutrition Agent (this document) + Product Agent (pending). Owner go-live before any published category is rescored. |
| **reference** | `01_framework/bsip2_framework/project_rescore/shelf_relative_design_v1.md` (this document). Predecessor: EV-056 (`02_products/brined_cheeses/methodology/graduated_sodium_d7_design_v1.md`). |
| **reversal_condition** | If empirical rollout calibration shows the relative layer produces score inversions (a product with lower absolute nutrient load scoring worse than a higher-load product due to median shift across run versions), revert to absolute-backbone-only for that nutrient/category and log as a calibration failure in the evidence registry. |

```yaml
study_objects:
  - claim: "Within-shelf relative nutrient position is a meaningful differentiator beyond
            absolute level alone, for nutrients where category clustering makes absolute
            thresholds insufficient to distinguish quality within the shelf"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:EV-055,EV-056"
    notes: >
      Evidence tier C: internal corpus observation (42/48 brined-cheese pin under absolute
      bands alone — EV-055; resolved by EV-056 relative layer). The mechanism is sound
      (within-category relative position is used in FSA traffic-light, HFSS, and academic
      nutrient profiling work). No population RCT exists for the specific banded surcharge
      model. The extension to non-sodium nutrients is by mechanism-analogy only; per-category
      corpus validation is required at rollout before each enrollment is D7-approved.
  - claim: "A shelf-relative differentiator on top of an absolute backbone preserves
            the Anti-Immunity Rule: a product cannot escape absolute penalties by being
            the lowest on a high shelf"
    dose_realistic: true
    population_direct: false
    rob_grade: low
    evidence_tier: C
    source_doi: "internal:bari_usecase_guardrails_v2"
    notes: >
      Architectural property, not a population claim. The one-sided-high design ensures
      no relative surcharge fires below the median — there is no "below-median reward"
      that could lift a score above what the absolute backbone permits. The Anti-Immunity
      Rule is protected by design, not by a separate cap.
```

---

## 8. Spec-Conflict Notes

Per the Spec-Conflict Duty (nutrition-agent.md mandatory 2026-06-12), the following potential
conflicts are flagged:

1. **EV-056 path independence.** The brief specifies the generalized mechanism "generalizes/
   replaces" the EV-056 sodium block. This design does NOT replace EV-056 — it creates a
   parallel capability that coexists with EV-056. Replacement of EV-056 by the generalized
   mechanism is a future migration step, to be D7-approved after the generalized mechanism is
   validated on the brined-cheese corpus. Silent replacement before validation would be the
   RC1/RC3 failure class (executing a spec without flagging that the spec's "replaces" claim
   is premature). The design specifies coexistence; replacement is flagged as a separate
   future step.

2. **"Activation scope" per brief vs. per design.** The brief asks for `scope_categories` as a
   function parameter. The existing `REDLABEL_ENDEMIC_SATFAT_CATEGORIES` frozenset is the natural
   initial value for sodium. The design keeps this as a config constant (`SODIUM_SHELF_REL_SCOPE`)
   distinct from the function signature — so the function is fully general (category-agnostic at
   the code level) while the configuration is category-specific (policy-controlled). This is more
   correct than hardcoding the endemic set into the function signature, and allows scope expansion
   without code changes.

3. **Family budget raise.** The design flags that the family budget raise (`SODIUM_FAMILY_BUDGET_BRINED = 16`
   for EV-056) is itself a D7 decision at rollout, not a design-time constant. The brief does not
   address this explicitly. Flagging it here so Product Agent is aware: each category/nutrient
   enrollment requires a budget raise decision.

---

## Summary of Deliverables

| Deliverable | Status |
|---|---|
| Function contract for `shelf_relative_differentiator()` | Complete — §1.3 |
| Generalized `set_shelf_stats()` / `compute_shelf_stats()` | Complete — §1.2 |
| Flag proposal `BARI_SHELF_RELATIVE_V1` | Complete — §2.1 |
| Backward-compat with `BARI_SODIUM_SHELF_RELATIVE_V1` / EV-056 | Specified — §2.2 |
| Philosophy fork accommodation (Cross-category + Endemic/Formulation) | Complete — §4 |
| Pending decisions register (C3 + Owner) | Complete — §5 |
| No-regression six-guard plan | Complete — §6 |
| Draft EV-084 registry entry | Complete — §7 |
| Spec-conflict notes | Complete — §8 |

---

*Proposed status: RETURNED — awaiting Product Agent D7 co-sign, C3 math consult (P96), and
owner philosophy calls A + B before any parameter finalization or implementation proceeds.*
