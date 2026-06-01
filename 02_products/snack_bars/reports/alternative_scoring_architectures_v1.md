# Alternative Scoring Architectures v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Architecture Options for Consideration

---

## Context

This document presents three architectural alternatives to Bari's current BSIP2 scoring system. All three assume that:
- The current system has produced defensible relative rankings within categories
- The absolute scores lack cross-category comparability
- The mean convergence between categories is a credibility risk
- The explanation layer is currently too generic

The three options are not mutually exclusive in all aspects — elements from each can be combined.

---

## Option A: Evolutionary Improvement

**Philosophy:** Keep the four-layer structural-first framework. Fix the specific calibration failures without changing the architecture. Add category-specific parameters where universal ones fail.

### What changes

**1. Category-specific cap values**

Replace universal caps with category-specific variants:

| Cap Type | Current (Universal) | Snacks | Maadanim | Bread |
|---|---|---|---|---|
| Max processing cap | 68 | 65 | 70 | 75 |
| High sugar cap | 55 | 60 (natural sugar exception) | 50 | 70 (no sugar in bread) |
| 5+ additives cap | 60 | 58 | 55 | 65 |

*Natural sugar exception in snacks*: date/nut/fruit-based products with no added sweetener receive a partial sugar cap exemption (cap raised to 60).

**2. Category-specific grade boundaries**

| Grade | Current (Universal) | Snacks | Maadanim |
|---|---|---|---|
| A | 80+ | 75+ | 70+ |
| B | 70–79 | 65–74 | 60–69 |
| C | 55–69 | 52–64 | 45–59 |
| D | 35–54 | 35–51 | 28–44 |
| E | <35 | <35 | <28 |

This produces different grade distributions per category without changing the underlying scoring formula.

**3. Confidence floor**

Products with partial confidence receive a maximum achievable score:
- Full confidence: uncapped
- Partial confidence: max score = 60 (currently: partial products can reach any score)
- Insufficient: score = null

**4. Minimum sibling gap enforcement**

Products with ingredient count difference ≤1 and same structural base and same cluster must have a minimum 5-point score gap or be collapsed to the same score. Eliminates the 1–2 point noise gaps between near-identical products.

**5. Nutritional data requirement for verified confidence**

A product can only receive "verified" confidence label if nutrition data has been parsed. Currently snk-001 receives "verified" confidence with null nutrition. This is contradictory.

### Advantages
- Preserves 2+ years of architectural and editorial work
- All existing scores are valid relative rankings — only absolute values shift
- Can be implemented category-by-category without a full rebuild
- Minimal disruption to existing frontend

### Weaknesses
- Does not solve the fundamental problem: a high-sugar date bar can still score 70/B
- Cap adjustments are somewhat arbitrary — what is the principled basis for "snacks max processing = 65" vs 68?
- Does not add a nutritional dimension — still structurally primary
- The explanation engine remains a separate problem

### Complexity
Medium. Requires BSIP2 category parameter configuration file, re-scoring all existing products, and recalibration of grade boundaries. No architectural changes.

### Impact on existing categories
Bread scores would shift slightly (calibration already done). Maadanim and snacks scores would shift materially — some products change grade. This requires a re-disclosure communication to users.

---

## Option B: Major Redesign — Dual Score System

**Philosophy:** Separate structural quality from nutritional value. Display both. Let the consumer choose which matters more for their decision.

### Architecture

**Score A: Structural Index (0–100)**
What the current BSIP2 system already measures:
- Processing level (NOVA proxy)
- Ingredient count and quality
- Structural base classification
- Additive load
- Sweetener pattern

**Score B: Nutritional Value Index (0–100)**
What BSIP2 currently cannot measure without nutritional data:
- Protein per 100g (relative to category)
- Sugar per 100g (penalized for refined, partially penalized for natural)
- Fiber per 100g (positive)
- Fat quality (saturated vs unsaturated ratio)
- Caloric density (contextual — different implications for snacks vs dairy)
- Sodium (penalized at high levels)

**Combined Grade:** Weighted combination with category-specific weights
- Snacks: Structural 60% + Nutritional 40%
- Maadanim: Structural 50% + Nutritional 50%
- Bread: Structural 70% + Nutritional 30%

**Consumer Display:**
```
חטיף תמרים במילוי חמאת שקדים
מבנה: 85/100    תזונה: ─── (לא נמדד)
ציון כולל: 70/B
```

### Why this is better

1. **Honest about what is being measured.** Structural quality and nutritional quality are two different things. The current system conflates them.

2. **Enables snack-specific insight.** "This bar is structurally clean (85/100) but we don't have its nutritional profile" is more honest than "70/B" with no disclosure.

3. **Creates a natural data collection incentive.** Categories without nutritional data get lower combined scores (structural + null nutrition = incomplete), which creates pressure to collect the data.

4. **Breaks the mean convergence.** Nutritional profiles of snacks and dairy desserts differ materially. Adding a nutritional dimension would produce different means.

### Disadvantages
- Requires full nutritional data collection before the nutritional score is meaningful
- More complex consumer-facing display
- Current snacks corpus (all null nutrition) would display only Structural Index, making 18 products incompletely scored until data is collected
- Grade boundaries need recalibration for the combined score

### Complexity
High. Requires BSIP2 architecture change, nutritional data ingestion pipeline (BSIP0 already captured the HTML files), new scoring module, frontend changes to display dual scores.

### Impact on existing categories
Bread: minimal (small nutritional correction). Maadanim: moderate (nutritional scores already computable from existing data — could be activated quickly). Snacks: no change until nutritional data is parsed.

---

## Option C: Clean-Sheet Rebuild — Within-Category Percentile System

**Philosophy:** Abandon absolute scores entirely. Score products relative to their category peers. Display percentile rank, not absolute number.

### Architecture

**Step 1: Establish category anchors**
For each category, identify 3–5 anchor products:
- Best achievable (the product closest to "ideal" in category)
- Category median (typical Israeli retail product in this category)
- Worst present (category floor)

**Step 2: Score relative to anchors**
Every product receives a score that is relative to the category anchors, not to a universal scale. A date bar at 70/100 means "this is 70% of the way from the category floor to the category ceiling" — not "this product is 70/100 in absolute quality."

**Step 3: Display percentile rank, not score**
Instead of "70/B," display:
```
מדרגה #1 מתוך 18 חטיפים
טווח: שיא קטגוריה
```

Or, with a simplified grade:
```
A — שיא (top 10% of snacks)
B — מעל ממוצע (top 25%)
C — ממוצע (25th–75th percentile)
D — מתחת לממוצע (bottom 25%)
E — תחתית (bottom 10%)
```

**Step 4: Separate comparison from ranking**
The comparison page shows relative positions within the category. An "export to compare across categories" function is explicitly labeled as cross-category only, with explicit disclaimers.

### Why this solves the core problem

- **Zero cross-category comparability confusion.** A snacks A is the best snack. A maadanim A is the best dairy dessert. No numeric comparison is possible.
- **Category mean is always 50th percentile by definition.** No calibration needed.
- **Every category automatically has the same grade distribution.** 10% A, 15% B, 50% C, 15% D, 10% E regardless of absolute quality.
- **Eliminates the 70 ceiling problem.** The #1 product in any category always gets the top grade, regardless of absolute score.

### Disadvantages
- **Loss of absolute quality information.** A consumer who wants to know "is any snack actually good in absolute terms?" cannot get this from percentiles.
- **Category inflation risk.** The best milky (currently 27/E) would receive a high percentile rank within the milky-type sub-category — which is misleading.
- **Loses the "Bari grade is a real judgment" identity.** If every category has 10% A-grade products regardless of quality, the grade is a marketing tool, not a quality signal.
- **Breaking change.** All existing scores and grades change. Users who have made decisions based on existing scores are invalidated.
- **Category inflation within Bari's editorial identity** — this is antithetical to the governance constitution's claim that Bari makes real quality judgments.

### Complexity
Very high. Complete architectural rebuild. New scoring philosophy. New frontend. New explanation system. Existing corpus invalidated.

### Impact on existing categories
Full rebuild required. All existing categories start over.

---

## Head-to-Head Comparison

| Criterion | Option A (Evolutionary) | Option B (Dual Score) | Option C (Percentile) |
|---|---|---|---|
| Solves mean convergence | Partially (by shifting caps) | Yes (different nutritional profiles) | Yes (by definition) |
| Preserves existing scores | Mostly | Partially | No |
| Handles null nutrition honestly | No | Yes | N/A |
| Requires nutritional data | No | Yes (for full function) | No |
| Consumer clarity | Good | Medium (two numbers) | High (simple ranking) |
| Bari identity integrity | High | High | Low |
| Implementation complexity | Medium | High | Very High |
| Category-specific reality | Partial | Full | Full (by definition) |
| Absolute quality signal | Yes | Yes | No |
| Cross-category consistency | No | Partial | No |
| Time to implement | 2–4 weeks | 2–3 months | 3–6 months |

---

## CE Recommendation: Option A + Selected Elements from Option B

**Primary recommendation:** Implement Option A immediately (category-specific caps, confidence floors, sibling gap enforcement). This stops the bleeding within the current architecture.

**Secondary recommendation:** Implement Option B's dual-score display for categories where nutritional data exists (Maadanim first, then Snacks once BSIP0 data is parsed). This adds the analytical dimension without requiring a full rebuild.

**Do not implement Option C.** The percentile approach abandons Bari's core value proposition — that the grades are real quality judgments, not relative rankings. Within-category percentiles would make every category look equally distributed regardless of actual quality. This is dishonest in a different way than the current problem.
