# TASK-222E — Fiber Diversity Bonus Design (DESIGN_ONLY)

**Date:** 2026-06-09
**Status:** DESIGN_ONLY — no scoring changes implemented
**Part of:** TASK-222 (BSIP2 research-to-implementation)

---

## 1. Executive Summary

The BSIP2 scoring engine already uses `dietary_fiber_g` (from nutrition facts) in 5 separate scoring locations — `nutrient_density`, `glycemic_quality`, `satiety_support`, structural emptiness, and guardrail caps. However, it has **no awareness of fiber SOURCE or DIVERSITY**. A product with 5g fiber entirely from isolated inulin gets the same fiber score as 5g fiber from a blend of oat β-glucan + psyllium + inulin.

TASK-222E proposes a small quality bonus for products with ≥2 distinct named fiber sources, gated by NOVA proxy ≤ 3 (excludes ultra-processed fiber-gaming products).

**Recommendation: PROCEED TO IMPLEMENTATION** — signal is label-observable, bonus is bounded (+2 max), NOVA gate prevents gaming, and existing `bakery_semantics.py:ISOLATED_FIBER_TERMS` provides reusable marker set.

---

## 2. Existing State

### Fiber quantity flow (already in scoring)

| Location | Formula | Contribution |
|----------|---------|-------------|
| `score_nutrient_density()` | `0.65 × prot_score + 0.35 × fiber_score` | 15% of composite |
| `_score_glycemic_quality_sprint1()` | `+min(20, fiber × 2)` | Sub-dimension bonus |
| `score_satiety_support()` | `(prot×3 + fiber×5) / kcal × 400` | 6% of composite |
| `detect_structural_emptiness()` | `fiber < 1.5g` boolean | Gate condition |

### Fiber source awareness (exists but not in production)

| Resource | Content | Status |
|----------|---------|--------|
| `bakery_semantics.py:ISOLATED_FIBER_TERMS` (67–80) | 11 Hebrew fiber terms (inulin, psyllium, cellulose, β-glucan, guar, xanthan, pectin, polydextrose) | Used only by `classify_fiber_source_quality()` in bakery_semantics — NOT consumed by score_engine |
| `classify_fiber_source_quality()` (294–323) | Returns `structural | isolated | hybrid | minimal | unknown` | NOT called from scoring pipeline |
| `create_bread_light_corpus.py` enrichment | `has_prebiotic_fiber` boolean | Only in bread light enrichment, consumed by matrix_integrity.py only |
| `matrix_integrity.py` | `prebiotic_fiber` as additive category (22 engineering pts) | Standalone diagnostic only |

### Key gap
No signal for **fiber diversity** exists in the scoring pipeline. A product with 5g from four different named fiber sources scores identically to one with 5g from a single source.

---

## 3. Observable Signal Map

### Eligible for v1 Bonus

| Fiber Source | Hebrew Marker | Observable? | Notes |
|-------------|--------------|-------------|-------|
| Inulin / chicory | `אינולין`, `עולש` | YES | Clear ingredient text marker |
| FOS (fructooligosaccharides) | `FOS`, `פרוקטואליגוסכריד` | YES | Often labeled as FOS or full Hebrew name |
| β-glucan | `בטא-גלוקן` | YES | Labeled when explicitly added |
| Oat fiber | `סיבי שיבולת שועל` | YES | Distinct from whole oats |
| Psyllium | `ציליום`, `סיבי ציליום`, `אינדיאן` | YES | Common in bread/cereal |
| Cellulose | `תאית`, `סיבי תאית`, `E460`, `E-460` | YES | Distinguish from structural cellulose in whole plants |
| Acacia/gum arabic | `גומי ערבי`, `גומי אקאציה`, `E414` | YES | Already has sprint1 marker; existing `PREBIOTIC_GUM_PATTERNS` |
| Polydextrose | `פולידקסטרוז`, `E1200` | YES | Synthetic fiber |
| Pectin | `פקטין`, `E440` | YES | Functional additive + fiber |
| Guar gum | `גואר`, `E412` | YES | But primarily a thickener — double-counting risk |

### NOT Eligible (rejected for v1)

| Fiber Source | Reason |
|-------------|--------|
| General "dietary fiber" / "סיבים תזונתיים" | Too generic — could be anything; cannot verify diversity |
| Xanthan gum | Primarily an additive/thickener, not a fiber source in practice |
| Modified starch / resistant starch | Not labeled as a distinct fiber source; also counts as additive |
| "Whole grain" as fiber source | Already captured by intact-grain signal (TASK-222D); not a named fiber additive |

---

## 4. Proposed v1 Rule Table

| Parameter | Value |
|-----------|-------|
| **Signal** | `distinct_named_fiber_sources ≥ 2` (integer count of matched fiber terms) |
| **Detection** | Scan full ingredient text (not just position 1) for named fiber markers |
| **Bonus** | **+2** on `nutrient_density` dimension |
| **Gate** | `nova_proxy ≤ 3` only. NOVA 4 products are excluded from the bonus regardless of fiber count |
| **Count rule** | Count is the number of **distinct categories** matched, not raw marker occurrences. E.g., `אינולין` appearing twice still counts as 1. |
| **Threshold** | ≥2 distinct sources → +2 bonus. 1 source → 0 bonus. |
| **Dimension** | `nutrient_density` (applied after the protein-fiber blend score, before the fortification discount) |
| **Categories eligible** | **All categories** (the NOVA gate is the primary scope control, not category restriction) |
| **Categories excluded** | (none beyond NOVA gate) |

### Fiber Marker Set (Proposed)

Reuses and extends `bakery_semantics.py:ISOLATED_FIBER_TERMS`:

```
FIBER_DIVERSITY_MARKERS = {
    "inulin":        ["אינולין", "סיבי עולש", "שורש עולש"],
    "fos":           ["FOS", "פרוקטואליגוסכריד"],
    "beta_glucan":   ["בטא-גלוקן", "בטא גלוקן", "betaglucan"],
    "oat_fiber":     ["סיבי שיבולת שועל"],
    "psyllium":      ["ציליום", "סיבי ציליום", "אינדיאן", "psyllium"],
    "cellulose":     ["תאית", "סיבי תאית", "E460", "E-460"],
    "acacia_gum":    ["גומי ערבי", "גומי אקאציה", "E414", "E-414"],
    "polydextrose":  ["פולידקסטרוז", "E1200", "E-1200"],
    "pectin":        ["פקטין", "E440", "E-440"],
}
```

Each product gets a count of how many distinct categories are matched. If `nova_proxy ≤ 3` AND count ≥ 2, bonus = +2.

### Scoring Behavior (Proposed)

#### Modified function: `score_nutrient_density()`
```python
# Current formula:
raw = 0.65 * prot_score + 0.35 * fiber_score
if has_fortification:
    raw *= 0.80

# Proposed addition:
fiber_diversity_bonus = 2 if (nova_proxy <= 3 and distinct_fiber_sources >= 2) else 0
score = raw + fiber_diversity_bonus
```

#### New L3 field in `signal_extractor.py`:
```python
# TASK-222E — distinct named fiber source count (for fiber diversity bonus)
distinct_fiber_sources = set()
for fiber_cat, markers in FIBER_DIVERSITY_MARKERS.items():
    if any(m in full_text for m in markers):
        distinct_fiber_sources.add(fiber_cat)
```

---

## 5. Double-Counting Risk Analysis

| Existing Rule | Signal Overlap | Risk Assessment |
|---------------|---------------|-----------------|
| `score_nutrient_density()` — `fiber_score` from grams | **Same dimension (nutrient_density)** but different signal: quantity vs diversity | **Low** — quantity and diversity are independent. A product with 5g from 1 source gets the same fiber gram score as 5g from 3 sources; the diversity bonus only rewards the latter. |
| `_score_glycemic_quality_sprint1()` — `fiber_bonus = min(20, fiber × 2)` | No — uses grams only, separate dimension | **None** |
| `score_satiety_support()` — `fiber × 5.0` | No — uses grams only, separate dimension | **None** |
| NOVA proxy — additive classification | **NOVA gate** is the INVERSE: NOVA ≤ 3 allows the bonus, NOVA 4 excludes it | **None** — correct gating |
| Additive quality — inulin/psyllium may be counted as additives | Yes — inulin and psyllium could appear in `additive_marker_count` | **Low** — additive quality penalizes additive BURDEN; fiber diversity rewards source VARIETY. These are different dimensions and different signals. A product with fiber diversity gets a +2 on nutrient_density but also gets the normal additive-quality treatment for any additives. The bonus does not cancel the additive penalty — they're independent. |
| TASK-222D — intact-grain bonus | No — intact grain is a separate signal on WFI dimension | **None** |
| `matrix_integrity.py` — `prebiotic_fiber` as engineering signal | No — not wired into composite | **None today** (but flagged for future coordination) |

**Key coordination note (must be documented if implemented):**
> This fiber-diversity bonus is the SOLE owner of the named-fiber-source quality signal. matrix_integrity.py's `prebiotic_fiber` engineering signal (22 pts) consumes the same ingredient presence but is NOT wired into the composite. If matrix_integrity's engineering intensity is ever composited in, it must EXCLUDE the prebiotic-fiber category from its calculation to avoid double-counting with this bonus.

---

## 6. Regression-Risk Analysis

### Snack bars (53 products)
- Some granola/protein bars list inulin or psyllium → may trigger ≥2 sources
- **NOVA proxy**: Most snack bars are NOVA 4 (ultra-processed) → excluded by the gate
- **Risk**: Very low — the NOVA gate naturally limits this to less-processed bars

### Bread / bread light (32+ products)
- Some whole-grain breads add psyllium + oat fiber + inulin → may trigger the bonus
- Most bread light products are NOVA 3 → eligible, but many have only 0–1 named fiber sources
- **Risk**: Low — the bonus is small (+2) and limited to products with genuine fiber diversity

### Cereals (50+ products)
- Many cereals list inulin + oat fiber + cellulose → could trigger bonus
- **Key concern**: Some heavily fortified NOVA 4 cereals may list 3+ fiber sources. These are excluded by the NOVA ≤ 3 gate, which is the intended behavior.
- **Risk**: Low — the NOVA gate is the correct defense

### Yogurts (86 products)
- Some "high-fiber" yogurts add inulin. But yogurt category has `FIBER_NOT_APPLICABLE` status, and fiber there is typically a single source (inulin only).
- **Risk**: Very low — 1 source (inulin) doesn't trigger ≥2 threshold. Even if it did, the bonus is +2 on a dimension that's protein-only for yogurt (fiber-not-applicable path).

### Plant milks (milk run)
- Some oat milks list β-glucan + inulin → could trigger bonus. Most are NOVA 3–4.
- **Risk**: Very low — oat base β-glucan is structural (not isolated), so it wouldn't match the marker set. Added β-glucan would.

### Juices
- Some juices add pectin or inulin for fiber claims. Usually single source.
- **Risk**: Very low — 1 source threshold not met.

---

## 7. Consumer-Copy Restrictions

| Allowed | Prohibited |
|---------|------------|
| "מגוון מקורות סיבים" (diverse fiber sources) | "מוריד כולסטרול" (lowers cholesterol) |
| "סיבים מ-2+ מקורות" (fiber from 2+ sources) | "משפר עיכול" (improves digestion) |
| "סיבים תזונתיים מגוונים" (diverse dietary fiber) | טוען רפואי מכל סוג (any medical claim) |
| "מכיל סיבי אינולין ופסיליום" (contains inulin and psyllium fiber) | "בריא יותר" (healthier — comparative without evidence) |

**Hard rule:** No mention of microbiome, gut health, digestion, cholesterol, glycemic response, or satiety. The bonus is about fiber SOURCE DIVERSITY as a quality signal, not a physiological claim.

---

## 8. Implementation/No-Implementation Decision

**RECOMMENDATION: PROCEED TO IMPLEMENTATION**

| Criteria | Assessment |
|----------|-----------|
| Signal observability | Fully observable — ingredient text match against 9 fiber categories |
| Detection complexity | Simple — ~20 lines in signal_extractor + ~5 lines in score_engine |
| False-positive risk | Low — markers are specific named fibers; "סיבים תזונתיים" generic excluded |
| Scoring impact | Bounded (+2 max) — small additive bonus on a 15%-weighted dimension |
| NOVA gate | Strong defense against gaming — NOVA 4 products excluded |
| Double-counting risk | Low today; coordination note for future matrix_integrity wiring |
| Regression risk | Near-zero — only positive deltas for a subset of products |
| Consumer-copy clarity | Clear — source diversity framing, no medical claims |
| Leverage of existing code | `ISOLATED_FIBER_TERMS` in `bakery_semantics.py` provides ~50% of needed markers |

---

## 9. Artifacts

| Artifact | Purpose |
|----------|---------|
| This document | Design specification for CC review |
| `review/task_222e_design.md` | DESIGN_ONLY review artifact |
| (Future) `constants.py` | `FIBER_DIVERSITY_MARKERS`, `FIBER_DIVERSITY_BONUS`, `FIBER_DIVERSITY_MIN_SOURCES` |
| (Future) `signal_extractor.py` | L3 field `distinct_fiber_source_count` |
| (Future) `score_engine.py` | Modified `score_nutrient_density()` — adds `fiber_diversity_bonus` param |
| (Future) `evidence_registry_v1.md` | BEV-089 (TASK-222E) |

---

## 10. Registry Update

```yaml
TASK-222E: Design Review — RETURNED for CC review
status: RETURNED
return_reason: >
  Design complete. Proposes a binary fiber-diversity bonus: +2 on nutrient_density
  when >=2 distinct named fiber sources detected in ingredient text, gated by
  NOVA proxy <= 3. Nine fiber marker categories defined (inulin, FOS, beta-glucan,
  oat fiber, psyllium, cellulose, acacia gum, polydextrose, pectin). Reuses and
  extends bakery_semantics.py ISOLATED_FIBER_TERMS. Double-counting risk is low
  (same dimension but different signal — quantity vs diversity). NOVA 4 gate
  prevents ultra-processed gaming. Recommend PROCEED TO IMPLEMENTATION.
```
