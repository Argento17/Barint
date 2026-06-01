# Score Impact Assessment v1

**Date:** 2026-05-29  
**Scope:** What changes if nutrition and ingredient data are restored to the snacks shelf  
**Constraint:** Assessment only — no score or explanation modifications

---

## Executive summary

| Scenario | Score change? | Explanation change? | User impact |
|----------|---------------|---------------------|-------------|
| **A. Frontend hydration only** (BSIP1 → JSON, no rescoring) | **None** | **None** (by rule) | Expansion panel shows nutrition + ingredients |
| **B. BSIP1 parse fixes + BSIP2 re-run** | **Possible ±1–8 pts** on subset | CE would need new pass | Rank order may shift slightly |
| **C. Full CE rescoring initiative** | **Material** (~30–40% products per CE estimate) | Required | Category credibility review |

**Key finding:** Current scores **already incorporated** BSIP1 nutrition and ingredients via BSIP2. The shelf nulls are a **display gap**, not evidence that scores were computed without nutritional evidence.

---

## Evidence: scoring already used nutrition

BSIP2 trace for snk-001 (`bsip1_7290011498870`):

| Signal | Value used |
|--------|------------|
| energy_kcal | 92.0 |
| sugars_g | 15.5 |
| protein_g | 1.6 |
| ingredient_count | 3 |
| final_score_estimate | 70 (= shelf score) |

Active dimension notes:
- `calorie_density`: kcal=92.0 → score 90
- `glycemic_quality`: sugar_penalty(38.8) → 51.2
- `nutrient_density`: protein=1.6g, fiber=0g → 5.2
- `satiety_support`: (protein×3)/kcal → 20.9

All 18 products: shelf score matches `final_score_estimate` within rounding.

---

## Scenario A — Restore data to frontend only

### Scoring engine

| Component | Impact |
|-----------|--------|
| BSIP2 batch scores | **No change** — not re-run |
| `snacks_frontend_v2.json` score/grade | **No change** |
| `snack-page-data.ts` engine fixtures | **No change** |

### Explanations (current corpus)

| Field | Impact |
|-------|--------|
| `insightLine` | **No change** (audit rule) |
| `bottomLine` | **No change** |
| `positiveSignals` / `limitingFactors` | **No change** |
| Editorial references to "4 רכיבים" etc. | **No change** — structural copy remains valid |

### UI / consumer experience

| Surface | Improvement |
|---------|-------------|
| Expansion nutrition grid | **New evidence visible** — kcal, protein, sugar, fat, sodium |
| Ingredient list | **New evidence visible** — full Hebrew label text |
| Confidence badge | Should move to `partial` until relabel policy applied |
| Methodology trust | Users can verify structural claims against label data |

### Scoring engine parts that **do not** gain new evidence in Scenario A

The engine already had this evidence in BSIP2. Hydration does not activate dormant code paths — it exposes what was already used.

---

## Scenario B — Parse correction + selective rescoring

Products where BSIP1 values may be wrong:

| Product | Issue | Dimension at risk | Direction if fixed |
|---------|-------|-------------------|-------------------|
| snk-001 | 92 kcal/100g likely wrong basis | `calorie_density`, `glycemic_quality`, `satiety_support` | **Down** if true kcal ~350–400 |
| snk-019 | BSIP0 folder 89 kcal vs audit listing | Low — BSIP1/BSIP2 aligned at 89 | Minimal |
| snk-020 | Truncated ingredients in BSIP0 | `additive_quality`, NOVA proxy | Unlikely if BSIP1 string complete |

**If snk-001 kcal corrected to ~380/100g (date-bar plausible):**
- `calorie_density` dimension drops sharply (currently 90 at 92 kcal)
- `glycemic_quality` may shift (sugar ratio unchanged but thresholds may differ)
- Top-of-shelf 70/B **questionable** — CE advisory flagged Date Sugar Halo separately

**Products likely stable after re-run (16/18):** Parsed `usable_raw`, BSIP0/BSIP1/BSIP2 consistent.

---

## Scenario C — Full nutritional layer recalibration (CE moderate revision)

From CE `bari_scoring_verdict_v1.md`:

> Once parsed, approximately 30–40% of scores will shift (within ±8 points) as the nutritional layer activates.

**Audit refinement:** Nutritional layer is **already active** in BSIP2. CE estimate applies if:
- Parse errors fixed
- Category-specific caps introduced
- Minimum sibling gap enforced

### Engine layers — evidence status today

| BSIP2 layer | Active for snacks? | Evidence source |
|-------------|-------------------|-----------------|
| L1 Observed (nutrition, ingredients) | **Yes** | BSIP1 |
| L2 Derived (sugar/carb ratio, fat % kcal) | **Yes** | L1 |
| L3 Inferred (sweeteners, additives, seed oils) | **Yes** | Ingredient text |
| L4 Interpreted concerns / caps | **Yes** | Combined |
| L5 Behavioral hypotheses | Partial | Population-level, not product-specific |
| L6 Policy (NOVA floors, sweetener caps) | **Yes** | Structural |

### Parts of explanations that would improve (future CE pass, not Scenario A)

| Pattern | Example | Requires |
|---------|---------|----------|
| Quantified limiting factors | "35.5g sugar/100g" on snk-020 | Copy rewrite + hydrated data |
| Calorie-source disambiguation | Date-bar kcal vs structural simplicity | CE editorial |
| Sibling comparisons with numbers | "14 נקודות פחות" already present | Partially exists |
| Date Sugar Halo disclosure | Methodology note | CE policy, not data restore |

### Parts of current scores that become questionable

| Score region | Concern | Root cause |
|--------------|---------|------------|
| snk-001 @ 70/B | Date bar ceiling with possible kcal parse error | Low reported kcal inflates calorie_density |
| snk-015 @ 55/C vs snk-001 @ 70/B | 405 kcal vs 92 kcal same category | Inconsistent retailer label basis |
| D-band micro-gaps (39–47) | 1–2 pt gaps snk-009/010, snk-011/012 | Structural scoring precision artifact (CE Failure 3) |
| Category mean ~43.5 | Converges with maadanim | Universal caps (CE Failure 2) — not nutrition-null issue |

---

## Impact matrix

| Action | Scores | Rank order | Explanations | Trust |
|--------|--------|------------|--------------|-------|
| Hydrate frontend from BSIP1 | — | — | — (frozen) | ↑↑ |
| Fix snk-001 kcal + rescore | snk-001 ↓ likely | Possible | CE pass needed | ↑ |
| Relabel verified → partial | — | — | — | ↑ |
| Category-specific caps | Many | Yes | CE pass needed | ↑ |
| Sibling gap rule | D-band | Yes | CE pass needed | ↑ |

---

## Recommendation sequence

1. **Scenario A first** — zero score risk, maximum transparency gain  
2. **Confidence relabel** — parallel governance fix  
3. **snk-001 kcal CE review** — before any rescore  
4. **Scenario C elements** — separate CE sprint; not blocked on frontend hydration

---

## Conclusion

Restoring nutrition and ingredients to the shelf **does not require rescoring** and **does not change current scores** if done as a corpus hydration pass. The scoring engine already operated on BSIP1 nutritional evidence; the gap is user-visible transparency and confidence labeling.

Scores become **questionable** primarily where **data quality** (snk-001 kcal) or **CE policy** (date sugar halo, universal caps, false precision) intersect — not because nutrition was absent from BSIP2.

**Before any scoring-system redesign:** complete Scenario A + confidence fix. That establishes an honest baseline where users see the same facts the engine already used.
