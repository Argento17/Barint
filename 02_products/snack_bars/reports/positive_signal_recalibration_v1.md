# Positive Signal Recalibration v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Alternative Calibration Design  
**Companion to:** `strength_recognition_review_v1.md`  
**Goal:** Strengthen reward signals for genuinely good products without weakening penalties for genuinely bad ones.

---

## Diagnosis Summary

The under-rewarding identified in the Strength Recognition Review traces to three specific mechanisms:

1. **Code bug:** `whole_food_bonus` key missing from config → positive bonus never fires
2. **Weight imbalance:** `whole_food_integrity` at 0.01 weight → dimension is irrelevant
3. **Cap over-suppression:** 1 red label cap at 55 double-penalizes the same signal; no relief for natural-source red labels

The dimension engine itself is not the problem. The penalty-reward balance across dimensions is approximately correct. These three targeted fixes address the complaint without requiring an architectural redesign.

---

## Fix 1: Bug Fix — Restore Whole-Food Positive Signal

**File:** `bsip2_dimensions.py`  
**Type:** Code correction — no config change required

### Current code (broken)

```python
# processing_quality section (line ~59)
if f.get("has_whole_food_marker"):
    pq += p["whole_food_bonus"]   # KeyError: key not in config

# whole_food_integrity section (line ~120)
if f.get("has_whole_food_marker"):
    wfi += p["whole_food_bonus"]  # KeyError: key not in config
```

### Corrected code

```python
# processing_quality section
if f.get("has_whole_food_marker"):
    pq += p.get("matrix_marker_bonus", 0)   # uses existing config key

# whole_food_integrity section
if f.get("has_whole_food_marker"):
    wfi += p.get("matrix_marker_bonus", 0)  # uses existing config key
```

### Also required: ensure `has_whole_food_marker` is produced by feature extraction

Check `bsip2_features.py` (or equivalent extractor): confirm that the `whole_food_positive` ingredient marker list in `bsip2_config.py` sets `has_whole_food_marker=True` when matched. If this flag is not set during extraction, the corrected code path remains unreachable.

### Effect

| Product type | processing_quality change | whole_food_integrity change | Weighted final score change |
|---|---|---|---|
| Date bar, nut bar, oat bar with oat as primary ingredient | +2.5 pts | +7 pts | +0.45 + 0.07 = **+0.52 pts** |
| NOVA4 engineered bar | 0 | 0 | 0 |
| Sourdough bread | +2.5 pts | +7 pts | **+0.52 pts** |

This is small in absolute terms but it makes the intended design actually work. Products that deserve the bonus will receive it.

---

## Fix 2: Weight Redistribution — Make Whole-Food Integrity Matter

**File:** `bsip2_config.py`  
**Type:** Configuration change — affects all categories

### Current weights

```python
"whole_food_integrity": 0.01,
"regulatory_quality":   0.04,
```

### Proposed weights

```python
"whole_food_integrity": 0.04,
"regulatory_quality":   0.01,
```

**Rationale:** `regulatory_quality` tracks Israeli red labels. Red labels are already captured by guardrail CAPS (`ISRAELI_RED_LABEL_1` cap at 55, `ISRAELI_RED_LABELS_2_PLUS` cap at 45) which are the actual operative mechanism. The dimension score penalty from `regulatory_quality` is -18 pts × 0.01 = -0.18 weighted points — effectively irrelevant. Reducing `regulatory_quality` weight from 0.04 to 0.01 costs 0.54 weighted points maximum. That value is transferred to `whole_food_integrity`, where it can reward genuinely whole-food products.

### Effect simulation

| Product | WFI score | Old weighted (×0.01) | New weighted (×0.04) | Score gain |
|---|---|---|---|---|
| Date bar (NOVA2, nuts, dates, ≤5 ingredients) | ~72 | 0.72 | 2.88 | **+2.16 pts** |
| Plain Greek yogurt (NOVA2, minimal ingredients) | ~65 | 0.65 | 2.60 | **+1.95 pts** |
| Sourdough bread (NOVA2, whole grain, ≤6 ingredients) | ~75 | 0.75 | 3.00 | **+2.25 pts** |
| NOVA4 cereal bar (many ingredients, coatings) | ~18 | 0.18 | 0.72 | +0.54 pts |
| NOVA4 Corny-type bar (extruded, coating, syrup) | ~10 | 0.10 | 0.40 | +0.30 pts |

**Key property:** The bottom products gain minimal score (+0.30–0.54 pts) because their WFI scores are already very low. The top products gain +2–2.25 pts. This correctly widens the quality gap.

### Governance alignment

This change does not alter any penalty. It does not make bad products look better. It makes the whole-food integrity signal visible at the score level for the first time. The governance constitution requires that Bari's scores reflect genuine quality differences; a 2-point score change for date bars vs. NOVA4 bars is consistent with this.

---

## Fix 3: Regulatory Cap Relief for Natural-Source Red Labels

**File:** `bsip2_guardrails.py`  
**Type:** New conditional relief rule — most targeted change

### The problem

The `ISRAELI_RED_LABEL_1` guardrail caps any product with 1 Israeli red label at 55. This cap does not distinguish between:

- Red label for saturated fat from **natural dairy fat** (Greek yogurt, labane, cheese) — inherent to whole-food composition
- Red label for saturated fat from **hydrogenated palm oil** — a manufacturing choice
- Red label for added sugar — a manufacturing choice

For a plain Greek yogurt with 5g sat fat per 100g (triggering a red label at the threshold), the 55 cap suppresses a natural food property. For a pastry with 5g hydrogenated fat, the cap is appropriate.

### Proposed rule: Natural Saturated Fat Relief

**Condition:** Product has exactly 1 red label AND the red label type is saturated fat AND the product is NOVA2 AND `has_nut_or_seed_marker` OR inferred_category is `dairy_protein`.

**Effect:** Raise the effective cap from 55 → 63 for qualifying products only.

**Implementation sketch (bsip2_guardrails.py):**

```python
# After ISRAELI_RED_LABEL_1 cap is applied:
if (
    red_label_count == 1
    and red_label_type == "saturated_fat"
    and nova_proxy <= 2
    and (features.get("has_nut_or_seed_marker") or inferred_category == "dairy_protein")
):
    # Natural sat fat relief: raise cap from 55 to 63
    final_score = min(natural_score, 63)
```

### Effect simulation

| Product | Natural score | Current capped score | Relief score | Comment |
|---|---|---|---|---|
| Plain Greek yogurt, 1 sat-fat red label, NOVA2 | 83 | 55 | **63** | Natural dairy fat — relief applies |
| Labane 9%, 1 sat-fat red label, NOVA2 | 80 | 55 | **63** | Natural dairy fat — relief applies |
| Nut bar, 1 sat-fat red label, NOVA2, nut-dominant | 72 | 55 | **63** | Natural nut fat — relief applies |
| Protein yogurt with hydrogenated fat, 1 red label | 70 | 55 | 55 | Hydrogenated fat — NO relief |
| Protein yogurt, NOVA3, 1 sat-fat red label | 77 | 55 | 55 | NOVA3 — NO relief (cap appropriate) |
| Pastry, 1 sat-fat red label, NOVA4 | 48 | 48 | 48 | Score below cap — cap not binding |

### Governance alignment

This relief does not override the MoH label. The red label is still present on the product. The score still reflects that the product carries a regulatory warning. The difference is that the cap is relaxed from 55 to 63 for products where the red label is inherent to the food's natural composition — not a manufacturing decision. A plain Greek yogurt still scores C/D range in most cases; it simply isn't suppressed all the way to 55 by a natural-composition property.

---

## Combined Effect on Benchmark Products

Assuming all three fixes are implemented:

| Product | Current score | After Fix 1 | After Fix 2 | After Fix 3 | Net change |
|---|---|---|---|---|---|
| Date bar (snk-001, NOVA2, 70) | 70 | +0.52 | +2.16 | 0 | **+2.68 → 73** |
| Plain Greek yogurt, NOVA2, no red labels | ~84 | +0.52 | +1.95 | 0 | **+2.47 → ~87** |
| Greek yogurt, NOVA2, 1 sat-fat red label | 55 (capped) | +0.52 | +1.95 | +8 (relief) | **+10.47 → ~65** |
| NOVA3 protein yogurt, no red labels | ~77 | 0 | +1.5 | 0 | **+1.5 → ~79** |
| NOVA3 protein yogurt, 1 sat-fat red label | 55 (capped) | 0 | 0 | 0 | **0 → 55** (cap appropriate) |
| NOVA4 cereal bar (Corny-type) | ~13 | 0 | +0.30 | 0 | **+0.30 → 13** |
| NOVA4 bar with modest profile (Fitness) | ~46 | 0 | +0.54 | 0 | **+0.54 → 47** |

### Critical property confirmed

The bottom products (NOVA4, heavily processed) gain less than 1 point. The top products (NOVA2, genuinely whole-food) gain 2–3 points under fixes 1+2, and up to 10 points under fix 3 for the specifically suppressed case. The quality gap widens, not narrows.

---

## What This Does NOT Address

These three fixes do not change:

1. **The NOVA4 penalty structure** — NOVA4 products remain low-scoring. This is correct.
2. **The grade band thresholds** — A still starts at 85, C at 55. Separate calibration (Option A2 from `future_scoring_architecture_options_v1.md`).
3. **The date bar sugar halo** — A date bar at 73 (post-fix) still has 60g+ natural sugar. The explanation disclosure remains the right mechanism.
4. **Products with 2+ red labels** — The `ISRAELI_RED_LABELS_2_PLUS` cap at 45 is unchanged.
5. **NOVA3 products with 1 red label** — These receive no relief from Fix 3. A NOVA3 protein yogurt with a red label is appropriately capped at 55.

---

## Implementation Priority

| Fix | Effort | Score impact | Risk | Priority |
|---|---|---|---|---|
| Fix 1 (bug fix) | 30 minutes — 2 line changes + feature extraction verification | Small (+0.52 pts for whole-food products) | Very low | **IMMEDIATE — this is a correctness fix** |
| Fix 2 (weight redistribution) | 2 line changes in config | Moderate (+2 pts for top products) | Low — no architectural change | **SHORT-TERM — next calibration sprint** |
| Fix 3 (natural sat fat relief) | New conditional in guardrails (~10 lines) + requires red_label_type field in features | Large (+8 pts for specifically suppressed products) | Medium — requires red_label_type to be tracked | **EVALUATE — needs data pipeline verification** |

---

## Alternative Calibration: Strength Accumulation Layer (Option for Post-Fix Evaluation)

If the three fixes above are insufficient to address the product owner's concern, the next architectural option is a **strength recognition multiplier** — a post-calculation bonus layer that rewards products demonstrating exceptional performance across multiple quality dimensions simultaneously.

**Design:**

If a product's dimension profile shows:
- processing_quality ≥ 85 (genuinely clean processing)
- protein_quality ≥ 65 (meaningful protein)
- glycemic_quality ≥ 70 (controlled sugar)

Then apply a `multi_dimension_excellence_bonus`: +4 points to final score (before grade assignment).

This bonus would only apply to products already in the 65–82 range — it cannot push a mediocre product into B territory. It rewards products that are genuinely strong across the three most consequential quality pillars.

**Effect:** A plain Greek yogurt (NOVA2, high protein, low sugar, clean processing) currently scoring 83 would reach 87 (A-grade). A NOVA3 protein yogurt scoring 77 would reach 81. NOVA4 bars, which cannot simultaneously achieve high processing_quality and high glycemic_quality, are not affected.

**Governance consideration:** This introduces a non-linear reward that favors certain product profiles. Before implementing, the CE board should verify it does not systematically advantage any single manufacturer or create gaming incentives for product reformulation toward exactly-three-dimension optimization.

**Recommendation:** Implement fixes 1–3 first. Evaluate the strength accumulation layer after observing the fix effects on real product scores.
