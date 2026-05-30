# Future Scoring Architecture Options v1
**Date:** 2026-05-29  
**Status:** CE Advisory Board — Architecture Roadmap  
**Context:** Rebuilt knowing the framework is working. Options address real gaps, not disproven problems.

---

## Starting Position

The BSIP2 framework, as implemented, is producing defensible and category-discriminating results:
- Bread (72), maadanim (43.8), snacks (37.2) — three genuinely different means
- NOVA stratification within snacks: NOVA2=54.5, NOVA3=47.4, NOVA4=28.4
- Universal caps are not the primary constraint — the dimension engine does the work
- Category-specific calorie density tiers are already operational

The remaining problems are:
1. Explanation engine quality (22% strong)
2. Editorial transparency (displayed mean vs full corpus mean)
3. The clean-label/natural-sugar philosophy gap (date bars scoring above products with better macros)
4. Potential NOVA dominance at the expense of nutritional nuance within NOVA tiers

The architecture options below address these real problems.

---

## Option A: Evolutionary Improvement

**Philosophy:** Keep everything. Strengthen the nutritional discriminating power within NOVA tiers. Add display-layer transparency. Rebuild explanations.

### Changes

**A1. Intra-tier nutritional refinement**

The current system produces a 19-point gap between NOVA3 and NOVA4 means. But within NOVA4, products range from 13 to 47 — a 34-point spread. The engine does differentiate within tiers (by protein, sugar, additives, calorie density). But the discrimination could be sharper.

Specific changes:
- Add fiber quality scoring. Currently fiber contribution to glycemic_quality and satiety_support exists, but a product with chicory inulin (a common fiber-inflator in snack bars) should receive less credit than genuine oat fiber. Add a `has_chicory_inulin_fiber` flag to reduce fiber credit to 50%.
- Strengthen the protein source quality distinction. Protein from protein isolate (current penalty: -5 from protein_quality) vs protein from whole nuts (current: no explicit bonus). Add a +5 bonus for proteins sourced entirely from nuts/seeds without isolates.
- Sugar source discrimination within the 25g cap. Date sugar at 30g/100g and HFCS at 30g/100g currently receive the same cap trigger. Add a date_origin_sugar_relief: if product is NOVA2 and date-dominant, the HIGH_SUGAR_25G_PLUS cap is raised from 60 to 65. This addresses the date-bar/maadanim comparison without eliminating the penalty.

**A2. Category-specific grade thresholds**

Introduce grade boundary calibration per category:

| Grade | Universal | Snacks | Maadanim | Bread |
|---|---|---|---|---|
| B | 70 | 67 | 70 | 75 |
| C | 55 | 48 | 55 | 65 |
| D | 40 | 35 | 40 | 55 |

Under snacks-specific thresholds:
- snk-003 (53) moves from C to C (unchanged — above 48)
- snk-009 (47) moves from D to C (47 > 48? No, 47 < 48 → stays D)
- snk-016 (51) stays C (51 > 48)
- Several displayed D products near 48 move to C

Actually: C threshold at 48 means products scoring 48–67 are C. D threshold at 35 means 35–47 are D.
Under this: snk-017 (39→D), snk-020 (32→E), snk-019 (41→D), snk-018 (46→D), snk-009 (47→D)... Only products at 48+ would move to C.
This would move snk-016 (51), snk-003 (53) — but these are already C. The shift matters for the full corpus, where many 48–54 products currently labeled C would stay C, but products at 40–47 labeled D would have a lower D floor.

The more meaningful threshold change for snacks is **lowering D threshold from 40 to 35.** This means products scoring 35–39 (currently E) would display as D. This better reflects that a 37/D for a granola bar is genuinely D quality, not E.

**A3. Explanation engine rebuild**

The explanation audit identified 22% strong, 22% generic. The rebuild spec in `snacks_explanation_engine_review_v1.md` remains the correct scope. This is the highest-value change.

**A4. Editorial corpus display transparency**

Add a methodology stat: "ממוצע ציון קטגוריה מלאה: 37 (53 מוצרים). המוצגים נבחרו לייצג מגוון." This single number kills the false impression that displayed and category averages are the same.

### Advantages
- No disruption to existing scores
- Preserves 18 months of framework work
- Explanation rebuild is the highest ROI change
- Nutritional refinements add discriminating power where it's actually needed (within NOVA tiers)

### Weaknesses
- Does not address the fundamental structural-first philosophy
- Does not resolve the natural-sugar/added-sugar tension fully
- Grade threshold changes require consumer communication

### Complexity: Low
- A1 additions: 2–4 new flags in feature extraction, 3 rule modifications
- A2 thresholds: config file change + frontend display change
- A3 explanation rebuild: content sprint, no code change
- A4 transparency: one-line methodology addition

---

## Option B: Major Redesign — Composite Index with Explicit Dimensions

**Philosophy:** Stop presenting a single score. Present a composite of three explicit dimensions that the consumer can see and weigh according to their needs.

### Architecture

**Dimension 1: Structural Quality (0–100)**
What BSIP2 already measures: processing level, ingredient complexity, whole-food base, additive load. NOVA-primary.

**Dimension 2: Nutritional Value (0–100)**
A new sub-score, weighted differently:
- Protein per 100g (normalized to category expected range)
- Fiber per 100g (verified vs suspected)
- Sugar per 100g (natural-source credit, HFCS no credit)
- Caloric density (category-specific)
- Red label count

**Dimension 3: Formulation Honesty (0–100)**
A new sub-score that directly captures the marketing divergence signal Bari does best:
- Claims alignment: does "high protein" claim match protein content?
- Name alignment: does "dates and hazelnuts" match proportion of those ingredients?
- Processing transparency: are additives disclosed or hidden behind E-numbers?
- Category fit: is this product genuinely a snack or a confectionery?

**Combined grade:** Composite_score = (Structural × 0.45) + (Nutritional × 0.35) + (Formulation_Honesty × 0.20)

**Consumer display:**
```
חטיפי דגנים פיטנס קלאסי
מבנה: 42    תזונה: 51    כנות: 38
ציון כולל: 45/D
```

### Why this is valuable

1. **The Formulation Honesty dimension is Bari's unique value.** No other food intelligence tool explicitly scores the gap between marketing and composition. This makes it explicit, consumer-visible, and commercially distinctive.

2. **The three-dimension display makes the score legible.** A consumer seeing 42/51/38 immediately understands: this product has mediocre structure, acceptable nutrition, but poor marketing honesty. The single score of 45/D doesn't communicate this.

3. **It separates the philosophical question from the scoring question.** A consumer who prioritizes structural simplicity weights Dimension 1. A consumer who prioritizes protein weights Dimension 2. Bari doesn't need to make this tradeoff for the consumer.

4. **Natural sugar is handled correctly.** In Structural Quality, a date bar with 4 ingredients scores very high. In Nutritional Value, a date bar with 60g/100g total sugar scores lower. The combined score reflects both realities, weighted by the consumer's priorities.

### Disadvantages
- Requires significant frontend redesign
- Three scores are harder to explain than one
- The Formulation Honesty dimension requires manual curation for each product (the "claim alignment" check is not fully automatable)
- Changes all existing scores — requires re-disclosure

### Complexity: High
- New Nutritional Value module (2–3 weeks development)
- Formulation Honesty module (partially manual curation, 4–6 weeks for existing categories)
- Frontend redesign (2–3 weeks)
- Consumer-facing explanation redesign (1–2 weeks)

---

## Option C: Clean-Sheet Rebuild — Category-Relative Quality Index

**Philosophy:** Abandon universal scoring. Each category defines what "good" and "bad" look like. Scores are relative to the category's achievable range.

### Architecture

**Step 1: Establish category quality anchors for each category**

| Category | Minimum achievable | Maximum achievable | Basis |
|---|---|---|---|
| Snacks | ~10 (confectionery wafer) | ~85 (hypothetical: 4-ingredient, fermented, whole-grain, low-sugar) | Category structure analysis |
| Maadanim | ~20 (heavily engineered pudding) | ~75 (plain fermented dairy, high protein, no additives) | Category structure analysis |
| Bread | ~40 (white refined commercial) | ~95 (whole-grain sourdough, no additives) | Category structure analysis |

**Step 2: Linear rescaling within category**

Any product score = 100 × (raw_score - category_min) / (category_max - category_min)

Result: Each category has its own 0–100 scale. A snack bar at 70 (raw) becomes approximately 71% of the way from the category floor to ceiling. A milky product at 27 (raw) becomes approximately 20% of the way.

**Step 3: Category-relative grade boundaries**

All categories would produce A/B/C/D/E grade distributions that reflect the category's internal range, not a universal standard.

### Why this fails

**Option C is rejected.** The reasons:

1. **It destroys Bari's absolute quality signal.** A milky cake scoring D/E is a genuine quality verdict: this product is bad by any nutritional standard. A snacks C grade in Option C would mean "better than average snacks" — but not necessarily good in any absolute sense. A consumer might confidently buy an "A-grade snack" that is still heavily processed.

2. **It creates perverse incentives for category-stuffing.** If adding more low-quality products to a category lowers the floor, the relative scores of existing products go up without them changing.

3. **It eliminates cross-category learning.** One of Bari's emerging capabilities is helping consumers understand that some product categories are systematically better than others (bread > dairy desserts > snack bars, on average). Option C hides this.

4. **It conflicts with the governance constitution.** The constitution establishes that Bari makes real quality judgments, not relative rankings. Category-relative scoring is a marketing tool, not an intelligence tool.

**Option C is not recommended at any scope.**

---

## Recommendation

**Implement Option A immediately.** The framework is working. The explanations are the weakest element (not the scores). The nutritional refinements (fiber quality, protein source) add discriminating power where it's actually needed.

**Evaluate Option B after Option A is complete.** The Formulation Honesty dimension is a genuinely valuable addition that aligns with Bari's editorial identity. It should be designed as a standalone extension to Option A's architecture — not a replacement. When ready, it can be introduced as a new visible dimension without changing the existing structural score.

**Do not implement Option C.** It contradicts the platform's core value proposition.

---

## Minimum Viable Option A (4-week scope)

If resource-constrained, the minimum viable Option A is three changes in order:

1. **Explanation engine rebuild** (week 1–2): Highest consumer impact. No code change. Purely content.
2. **Editorial transparency disclosure** (week 1): One sentence in methodology. Immediate credibility improvement.
3. **Date sugar awareness note** (week 2): One explanation addition per date bar product.

These three changes address the only two genuine quality problems (explanation weakness + editorial misrepresentation) without any scoring code changes, any re-scoring of existing products, or any frontend changes.
