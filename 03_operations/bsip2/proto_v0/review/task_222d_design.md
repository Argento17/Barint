# TASK-222D — Matrix-Integrity Proxy Design (DESIGN_ONLY)

**Date:** 2026-06-09
**Status:** DESIGN_ONLY — no scoring changes implemented
**Part of:** TASK-222 (BSIP2 research-to-implementation)

---

## 1. Executive Summary

The existing `matrix_integrity.py` (v2, 1001 lines) is a rich standalone diagnostic module with 19 functions, ~31 trace fields, and HP triad detection. It is **NOT wired into the BSIP2 composite score** and should NOT be wired as-is — its HP reconstruction triad, assembly drag, and fortification-engineering parameters are too speculative for a live scoring path.

TASK-222D proposes a **narrow v1 proxy** of exactly one binary observable signal — intact whole-grain presence — as a small bonus on the existing `score_whole_food_integrity()` dimension.

**Recommendation: PROCEED TO IMPLEMENTATION** — the signal is fully observable, bounded (+3 max), grain-categories only, and zero regression risk.

---

## 2. Existing State: `score_whole_food_integrity()`

**File:** `score_engine.py:1486`

Current signature:
```python
def score_whole_food_integrity(nova_level: int, ing_count: int,
                               has_fermentation: bool = False) -> tuple[float, str]:
```

Current behavior:
- **Base:** `NOVA_WFI_SCORES[nova_level]` = {1:100, 2:85, 3:60, 4:30}
- **Complexity penalty:** `max(0, (ing_count - 8) * 2)` for >8 ingredients
- **Fermentation bonus:** +5 if live fermentation detected
- **Formula:** `min(100, max(0, base - complexity_pen + ferm_bonus))`

Called at `score_engine.py:2481`:
```python
wfi_score, wfi_note = score_whole_food_integrity(nova_level,
    l1.get("ingredient_count", 0), has_fermentation)
```

This dimension already has:
- A NOVA-derived base
- A fermentation bonus (precedent for signal-based bonuses on WFI)
- No intact-grain signal

---

## 3. Observable Signal Map

### Eligible for v1 Proxy

| Signal | Label Observable | Detection Method | False-Positive Risk |
|--------|-----------------|-----------------|---------------------|
| **Intact whole grain (position 1)** | YES — ingredient[0] text | Match against whole-grain Hebrew markers | Low — oat flakes, whole wheat flour, rolled oats are unambiguous |
| **Whole legume (position 1)** | YES — ingredient[0] text | Match against legume markers (chickpea, lentil, bean) | Low — "קמח חומוס" (chickpea flour) is mechanically degraded; should check for intact form vs flour |
| **Whole seed (position 1)** | YES — ingredient[0] text | Match against seed markers (sesame, flax, chia, sunflower) | Low — seeds in position 1 are unlikely to be refined |
| **Puree/paste (position 1)** | YES — ingredient[0] text | Match against "מחית", "רסק" | Medium — "רסק עגבניות" (tomato paste) in sauces is structurally disrupted but not ultra-processed |
| **Refined flour dominance (position 1)** | YES — ingredient[0] text | Match against "קמח חיטה", "קמח לבן" | Low — first ingredient white flour is a clear degradation signal |
| **Puffed/extruded base** | YES — ingredient[0] text or product name | "פופקורן", "תירס מוגש", "אוורירי" | Low — puffed grains are unambiguously restructured |
| **Bar-format** | YES — product name | Already classified by router_v2 as `snack_bar_granola` | Low — bar format is a structural clue |
| **Fermented intact matrix** | YES — product category | Already detected via existing fermentation markers | Already handled (+5 bonus exists) |

### REJECTED for v1 (Unobservable or Too Speculative)

| Parameter | Reason for Rejection |
|-----------|---------------------|
| Particle size | Not on any label |
| Viscosity | Not on any label |
| Chewing rate | Requires clinical study |
| Gastric emptying | Requires clinical study |
| Cellular integrity | Not inferable from label — even "intact grain" is a proxy for this |
| HP reconstruction triad (sweetener+flavor+emulsifier) | Already captured by additive_quality + NOVA proxy — would double-count |
| Assembly complexity drag | Partly captured by ingredient_count complexity penalty already in WFI |
| Fortification type (restoration vs wellness) | Speculative — "restoration" vs "engineering" requires knowing manufacturer intent |
| Protein engineering intensity | Already captured by `score_protein_quality()` |
| Sweetener stacking | Already captured by `sugar_quality` and sweetener caps |

---

## 4. Proposed v1 Rule Table

### Single Rule: Intact-Grain Bonus

| Parameter | Value |
|-----------|-------|
| **Signal** | `intact_whole_grain_detected` (boolean) |
| **Detection** | Product category is grain-based AND ingredient[0] matches whole-grain marker set |
| **Bonus** | **+3** on `whole_food_integrity` (stacked on existing base + complexity_pen + ferm_bonus) |
| **Max** | +3 (hard cap — no stacking with other WFI bonuses; see Double-Counting) |
| **Dimension** | `whole_food_integrity` (not additive_quality, not protein_quality) |
| **Categories eligible** | `bread`, `cereal`, `crispbread`, `cracker`, `snack_bar_granola` (granola/muesli subtypes only) |
| **Categories excluded** | All dairy (milk, yogurt, cheese), beverages, plant milks, whole_food_fat, sauces, spreads |
| **Hedge** | If ingredient[0] matches BOTH a whole-grain marker AND a refined-flour marker (e.g., "קמח חיטה מלא" = whole wheat flour), the whole-grain signal wins (conservative benefit-of-doubt) |

### Whole-Grain Marker Set (Proposed)

```
WHOLE_GRAIN_MARKERS = [
    "שיבולת שועל",      # oats (flakes or whole)
    "קמח שיבולת שועל",  # oat flour (still whole grain if not refined)
    "קמח חיטה מלא",     # whole wheat flour
    "קמח כוסמין",       # spelt flour
    "קמח שיפון",        # rye flour
    "קמח כוסמת",       # buckwheat flour
    "שיפון",           # rye grain
    "כוסמין",          # spelt grain
    "כוסמת",           # buckwheat groats
    "קוואקר",          # oatmeal
    "גריסים",          # groats/pearl barley
    "שעורה",           # barley
    "פתיתי שיבולת שועל", # rolled oat flakes
    "פתיתי כוסמין",    # spelt flakes
    "אורז מלא",        # brown rice
    "קינואה",          # quinoa
    "דוחן",            # millet
    "אמרנט",           # amaranth
]
```

### Refined-Flour Marker Set (for exclusion hedge, not for separate penalty)

```
REFINED_FLOUR_MARKERS = [
    "קמח חיטה",        # wheat flour (not "מלא" = whole)
    "קמח לבן",          # white flour
    "קמח תופח",         # self-rising flour
    "קמח מאפה",         # pastry flour
    "קמח לחם",          # bread flour
]
```

---

## 5. Scoring Behavior (Proposed Code Change)

### Modified function signature
```python
def score_whole_food_integrity(nova_level: int, ing_count: int,
                               has_fermentation: bool = False,
                               intact_grain_bonus: int = 0) -> tuple[float, str]:
```

### Modified formula
```python
base = NOVA_WFI_SCORES.get(nova_level, 50)
complexity_pen = max(0, (ing_count - 8) * 2) if ing_count > 8 else 0
ferm_bonus = 5 if has_fermentation else 0
intact_bonus = min(3, intact_grain_bonus)  # hard cap
score = round(min(100, max(0, base - complexity_pen + ferm_bonus + intact_bonus)), 1)
```

### Call site modification
```python
l3_intact = 3 if l3.get("intact_whole_grain_detected") else 0
wfi_score, wfi_note = score_whole_food_integrity(nova_level,
    l1.get("ingredient_count", 0), has_fermentation, l3_intact)
```

### Signal extraction (new field in signal_extractor.py L3)
```python
# TASK-222D — intact whole grain detection (matrix-integrity proxy v1)
# Checks if position-1 ingredient is a whole-grain form.
intact_whole_grain_detected = False
ing_order = product.get("ingredient_order") or []
if ing_order and isinstance(ing_order[0], dict):
    first_ing = ing_order[0].get("text", "")
    if any(m in first_ing for m in WHOLE_GRAIN_MARKERS):
        intact_whole_grain_detected = True
```

---

## 6. Double-Counting Risk Analysis

| Rule | Same Signal? | Dimension | Risk |
|------|-------------|-----------|------|
| NOVA proxy (NOVA 1 ↔ whole food) | No — NOVA classifies by additive/ingredient count, not grain form | Separate dimension (NOVA is a gate, not a WFI score) | Low — NOVA 1 gives WFI base=100, which already reflects whole-food status. But a NOVA-4 product with intact grain (e.g., puffed whole-grain cereal) would get NOVA 4 base=30 + intact bonus +3 = 33, which is correct (the grain is intact but the product is ultra-processed) |
| Fermentation bonus (+5) | No — live fermentation is different from intact grain | Same dimension (WFI) | Low — both bonuses on same dimension are intentional; a fermented whole-grain bread SHOULD get both |
| Fiber in nutrient_density | No — fiber grams from nutrition facts, not ingredient text | Separate dimension | **None** — whole-grain products deserve both WFI bonus AND fiber credit |
| Protein quality (TASK-222B) | No — reconstructed protein is a different signal | Separate dimension | **None** |
| Additive quality (TASK-222A/F4) | No — additive markers are a different signal | Separate dimension | **None** |
| Existing matrix_integrity.py (standalone) | Yes — `_MECHANICAL_TRANSFORM_PATTERNS` has "שיבולת שועל" at 6pts | Not wired into composite | **Critical if matrix_integrity is ever wired in** — the same "intact oat flakes" signal would fire in both the proxy (+3 on WFI) AND in matrix_integrity's degradation score. Future wiring must EXCLUDE this signal from matrix_integrity or remove the proxy. Same pattern as PROTEIN_QUALITY_MATRIX_DISCOUNT coordination note. |

**Key coordination note (must be documented in constants.py if implemented):**
> This proxy is the SOLE owner of the intact-grain bonus in the LIVE score path. matrix_integrity.py's raw_form_degradation currently includes intact-grain forms (rolled oats=20pts degradation) but is NOT wired into the composite. If matrix_integrity is ever composited in, it must EXCLUDE intact-grain forms from its degradation calculation to avoid double-counting with this proxy.

---

## 7. Regression-Risk Analysis

### Snack bars (53 products)
- **Grain-based subcategories**: granola/muesli bars are eligible (since routed as `snack_bar_granola`)
- **Expected impact**: Granola/muesli bars with "שיבולת שועל" (oat flakes) or "פתיתי שיבולת שועל" as first ingredient get +3 on WFI
- **Ceiling**: snk-001 = 70/B holds — the bonus is small (+3 WFI) and the date-bar ceiling product (no grain) is unaffected
- **Risk**: Very low — snack bars are the most heterogeneous subcategory; some granola bars will get the bonus, others won't

### Bread / bread light (32+ products)
- **Expected impact**: Many bread products have whole-grain first ingredient → +3 WFI bonus. Bread light is mostly refined-flour base → no change for most products
- **Risk**: Very low — whole-grain bread SHOULD score higher on WFI

### Cereals (multi-run, ~50+ products)
- **Expected impact**: Products with "שיבולת שועל" or "פתיתי שיבולת שועל" or "סובין" (bran) as first ingredient get +3
- **Risk**: Low — some puffed-whole-grain cereals may get the intact-grain bonus despite being puffed. This is a known edge case (intact grain form ≠ intact cellular structure after puffing). Acceptable for v1 — puffing is not detectable from ingredient text alone

### Juices (1 run)
- **Excluded** — not a grain-based category
- **Risk**: None

### Yogurts (86 products)
- **Excluded** — not a grain-based category
- **Risk**: None

### Plant milks (within milk run)
- **Excluded** — not a grain-based category
- **Risk**: None

### Food categories NOT YET scored
- Products in unscored categories (e.g., bread light routed as cracker/snack_bar_granola) are already captured above
- No new categories need analysis

---

## 8. Consumer-Copy Restrictions

| Allowed | Prohibited |
|---------|------------|
| "מבנה מזון שלם יותר" (more intact food structure) | "לא מעלה סוכר בדם" (does not spike blood sugar) |
| "צורת מוצר מובנית פחות" (more disrupted product form) | "משביע יותר" (more satiating) |
| "דגן מלא" (whole grain) | "פוגע במטבוליזם" (damages metabolism) |
| "קמח מלא" (whole flour) | טוען רפואי מכל סוג (any medical claim) |
| "שיבולת שועל מלאה" (whole oats) | "בריא יותר" (healthier — comparative claim without evidence) |

**Hard rule:** No mention of glucose, insulin, glycemic index, satiety, gut health, permeability, or metabolic function. The proxy is about food STRUCTURE, not physiological effect.

---

## 9. Implementation/No-Implementation Decision

**RECOMMENDATION: PROCEED TO IMPLEMENTATION**

| Criteria | Assessment |
|----------|-----------|
| Signal observability | Fully observable from ingredient[0] text |
| Detection complexity | Single Hebrew substring match — ~15 lines total |
| False-positive risk | Very low — whole-grain markers are unambiguous |
| Scoring impact | Bounded (+3 max, grain categories only) |
| Double-counting risk | None today; documented coordination note for future |
| Regression risk | Near-zero — only bonus (positive deltas) for a subset of grain products |
| Consumer-copy clarity | Clear — structural framing, no medical claims |
| Business value | Moderate — closes a known gap where granola/muesli products with intact oat flakes got the same WFI score as refined-flour products |

**However:** If the Phase 1 backlog priority is tight, TASK-222D can wait — the proxy is additive only (no negative deltas), so delaying it does not produce incorrect scores. Existing products that SHOULD get the intact-grain bonus simply don't get it yet.

**Suggestion:** Deploy as a single-sprint implementation (~2 hrs) after higher-priority work, or defer to Phase 2.

---

## 10. Artifacts Created

| Artifact | Purpose |
|----------|---------|
| This document | Design specification for CC review |
| `review/task_222d_design.md` | DESIGN_ONLY review artifact |
| (Future) `constants.py` | `WHOLE_GRAIN_MARKERS`, `MAX_INTACT_GRAIN_BONUS`, `INTACT_GRAIN_CATEGORIES` |
| (Future) `signal_extractor.py` | L3 field `intact_whole_grain_detected` |
| (Future) `score_engine.py` | Modified `score_whole_food_integrity()` |
| (Future) `evidence_registry_v1.md` | BEV-088 (TASK-222D) |
| (Future) corpus diff gate | Grain-category run: before vs after |

---

## 11. Registry Update

```yaml
TASK-222D: Design Review — RETURNED for CC review
status: RETURNED
return_reason: >
  Design complete. Proposes a single binary signal (intact whole-grain in ingredient[0])
  as a +3 bonus on whole_food_integrity for grain-based categories. Signal is fully
  observable, bounded, and zero-regression-risk. All unobservable parameters explicitly
  rejected. Double-counting risk is zero today (matrix_integrity.py not wired into
  composite) with a documented coordination note for future wiring. Recommend PROCEED
  TO IMPLEMENTATION if Phase 1 bandwidth permits, or defer to Phase 2.
rejected_parameters:
  - particle size
  - viscosity
  - chewing rate
  - gastric emptying
  - cellular integrity (unless directly inferable)
  - HP reconstruction triad
  - assembly complexity drag
  - fortification type classification
  - protein engineering intensity
  - sweetener stacking
consumer_copy_approved:
  - "מבנה מזון שלם יותר" (more intact food structure)
  - "צורת מוצר מובנית פחות" (more disrupted product form)
  - "דגן מלא" (whole grain)
prohibited_copy:
  - any glucose/insulin/glycemic claim
  - any satiety/medical claim
  - any metabolic-damage language
```
