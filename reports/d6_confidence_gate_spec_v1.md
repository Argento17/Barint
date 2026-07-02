# D6 Ingredient-Confidence Gate — Formal Specification v1
**TASK-395C | D6 Proposal | Author: Nutrition Agent | 2026-06-26**
**Status: PROPOSED — awaiting Product Agent D7 co-sign**
**Moderate-tier ruling (2026-06-26, Nutrition Agent):** Option B selected — T-MOD composition scale = 1.0 (untouched, same as T-HIGH). Rationale: at least one stated percentage anchors the heavy hitter; remaining uncertainty is already captured by the orthogonal panel-completeness gate; applying 0.70 here would double-penalize. The §2.1 table and AC-5 have been corrected to match; AC-3/AC-6 are unchanged. Builder must set `_ING_CONF_COMPOSITION_SCALE["moderate"] = 1.0` and remove the provisional comment. Product Agent D7 confirm required on item 7.4.

---

## 0. Preamble and Framing

This spec formalizes the keystone gate of the TASK-395 de-chain roadmap. It
translates the owner's hard rule ("No confidence of ingredients and values is a
hard no-go — triggered by a cottage cheese promoted to grade S on zero readable
ingredients") into a precise, machine-enforced scoring constraint.

The gate has two distinct jobs that must not be conflated:

1. **The hard no-grade block** — a product with zero readable ingredient text can
   never display a letter grade, full stop.
2. **The composition weight scale** — a product with only order-level ingredient
   data (no stated percentages) receives a proportionally reduced contribution
   from composition-derived signals, with a hard grade ceiling preventing
   promotion to top tiers on the strength of ambiguous ingredient ordering alone.

The existing `compute_confidence()` mechanism (BSIP0 panel completeness → numeric
score → band → `confidence_ceiling`) is a separate, orthogonal gate addressing
*nutritional data* completeness. This new gate addresses *ingredient text*
completeness. They interact additively, never double-counting the same failure
mode. See §5 for the interaction model.

---

## 1. Confidence Tier Definitions

The gate operates on the four tiers emitted by `assess_ingredient_confidence()`
from `structured_ingredient_reader.py` (TASK-395). The function signature is:

```python
def assess_ingredient_confidence(
    text: str | None,
    parsed: list[StructuredIngredient] | None = None,
) -> str:  # "none" | "low" | "moderate" | "high"
```

### Corpus distribution (current supplement corpus, for calibration reference)
none=27, low=239, moderate=524, high=56 (total 846 scored products).

### Tier-to-behavior table

| Tier | `assess_ingredient_confidence()` return | What it means | Grade blocked? | Composition weight multiplier | Grade ceiling |
|---|---|---|---|---|---|
| **T-NONE** | `"none"` | No ingredient text present or unparseable (len<3 / marketing-bleed) | **YES — no grade, no score display** | 0.0 (composition signals zeroed) | N/A — grade withheld |
| **T-LOW** | `"low"` | Text present, no stated percentages, position-order only | No | **0.35** | **B (64.9)** |
| **T-MOD** | `"moderate"` | Some stated percentages (≥1 ingredient, stated_frac<0.40) | No | **1.0** | None (full grade range) |
| **T-HIGH** | `"high"` | Majority of records have stated/effective pct (stated_frac≥0.40) | No | **1.0** | None (full grade range) |

**Grade ceiling for T-LOW** is B (numeric ceiling: 64.9). Rationale: ingredient
position-order is genuine legal data under Israeli labeling law (heaviest-first
mandate). It is NOT fabrication. However, position-order alone cannot distinguish
"38% oats" from "47% oats" — the signal is coarse by an order of magnitude for
the scores it would otherwise generate. A T-LOW product that would score 80+
without the gate is most likely benefiting from a composition inference that the
label simply cannot support at that resolution. Capping at B (not A) is the
honest ceiling for order-only data. The empirical basis: the B2 knife-edge pair
(RP-08: 47% vs 39% oats, +0.5 margin) confirms that meaningful whole-food
separations can already be detected at T-LOW; the gate does not destroy the
signal — it only prevents it from promoting to S or A.

**No ceiling for T-MOD**: once even a minority of stated percentages are present,
the parser can locate the heavy hitters with moderate precision. The remaining
uncertainty is absorbed by the existing panel-completeness confidence gate, which
already reduces scores for partial nutritional data. Applying a second ceiling
here would double-penalize.

---

## 2. Engine Enforcement — Exact Mechanism

### 2.1 Where in the pipeline

The gate fires in `score_product()` (both `proto_v0/src/score_engine.py` and
`sprint1/score_engine_v2.py` which imports from it). It operates at two points:

**Point A — T-NONE early exit (Stage 0.5, after out-of-scope, before confidence)**

Immediately after the out-of-scope check (Stage 0 in `score_product()`) and
before `compute_confidence()` runs:

```python
# TASK-395C — Ingredient-confidence gate (D6 spec, 2026-06-26)
# BARI_INGCONF_V1 env flag (default OFF → byte-identical to today)
BARI_INGCONF_V1 = os.environ.get("BARI_INGCONF_V1", "off").lower() == "on"

if BARI_INGCONF_V1:
    ing_text = (product.get("ingredients_text_he")
                or product.get("ingredients_raw") or None)
    ing_conf = assess_ingredient_confidence(ing_text)  # imported from structured_ingredient_reader
    product["_ing_conf"] = ing_conf  # store for downstream + trace

    if ing_conf == "none":
        return {
            "product_id": pid,
            "evaluation_status": eval_result["evaluation_status"],
            "ingredient_confidence": "none",
            "ingredient_confidence_gate": "withheld",
            "final_score_estimate": None,
            "grade_estimate": None,
            "data_sufficiency": "ingredient_data_absent",
            "ingconf_gate_note": "No readable ingredient text — grade withheld (TASK-395C D6 rule)",
        }
```

A `None` grade (not "E" and not "insufficient_data") is the correct signal for
"withheld for insufficient ingredient coverage." The distinction from the existing
`insufficient_data` path matters: `insufficient_data` is fired by missing
nutritional panel fields; `ingredient_data_absent` fires on zero ingredient text.
A product can have a complete nutritional panel and still be `ingredient_data_absent`
(e.g., a supplement with a readable panel but no ingredient list scrape).

**Point B — T-LOW ceiling and composition weight scale (after weighted_dim_score, before cap)**

After the 10-dimension weighted sum is computed (`weighted_dim_score`), but before
the guardrail caps are applied:

```python
if BARI_INGCONF_V1:
    ing_conf = product.get("_ing_conf", "high")  # fallback for flag-off path

    # Composition weight scale
    _ING_CONF_COMPOSITION_SCALE = {"none": 0.0, "low": 0.35, "moderate": 0.70, "high": 1.0}
    composition_scale = _ING_CONF_COMPOSITION_SCALE.get(ing_conf, 1.0)

    # The composition-linked dimension is whole_food_integrity (weight 0.04).
    # At T-HIGH (scale=1.0), contribution = wfi_score * 0.04 — unchanged.
    # At T-LOW (scale=0.35), contribution = wfi_score * 0.04 * 0.35 ≈ 0.014 of composite.
    # Rescale: pull the whole_food_integrity contribution toward neutral (50) by scale factor.
    if composition_scale < 1.0:
        wfi_original_contribution = dim_scores["whole_food_integrity"] * DIMENSION_WEIGHTS["whole_food_integrity"]
        wfi_scaled_contribution = (
            50.0 * DIMENSION_WEIGHTS["whole_food_integrity"]   # neutral anchor
            + (dim_scores["whole_food_integrity"] - 50.0)
              * DIMENSION_WEIGHTS["whole_food_integrity"]
              * composition_scale
        )
        weighted_dim_score = (weighted_dim_score
                              - wfi_original_contribution
                              + wfi_scaled_contribution)
        weighted_dim_score = round(weighted_dim_score, 2)

    # T-LOW grade ceiling
    _ING_CONF_GRADE_CEILING = {"low": 64.9}   # T-MOD/T-HIGH: no ceiling from this gate
    ingconf_ceiling = _ING_CONF_GRADE_CEILING.get(ing_conf)
```

The `ingconf_ceiling` is then applied at the same point as the existing
`confidence_ceiling`:

```python
# Existing confidence ceiling (panel completeness)
ceiling = conf_result.get("confidence_ceiling")

# Ingredient-confidence ceiling (composition resolution)
if BARI_INGCONF_V1 and ingconf_ceiling is not None:
    ceiling = min(ceiling, ingconf_ceiling) if ceiling is not None else ingconf_ceiling
```

This ensures both ceilings are applied without conflict — the more binding one
governs, and neither is double-counted.

### 2.2 Why whole_food_integrity is the targeted dimension

`whole_food_integrity` (weight 0.04) is the score dimension most directly derived
from ingredient structure. It maps `nova_level` + `ingredient_count` +
`has_fermentation` to a score — and `nova_level` for complex products is
significantly informed by what the ingredient reader finds. Scaling this dimension
toward neutral at low confidence is the honest reduction: "we cannot read the
composition, so we cannot confidently claim high structural integrity."

The other 9 dimensions are anchored to the nutritional panel (kcal, protein,
fat, sodium, sugar, fiber, sat_fat) — these are derivable from the BSIP0 panel
independently of ingredient text quality. They are NOT scaled by this gate.

At T-HIGH (full weight, scale=1.0):
- `whole_food_integrity` at score 100 contributes: 100 × 0.04 = 4.0 pts to composite
- At score 30 (NOVA-4): 30 × 0.04 = 1.2 pts
- Range: ~2.8 pts — well under 1 grade band (15 pts), confirming the hard guarantee below

At T-LOW (scale=0.35):
- `whole_food_integrity` at score 100 contributes: (neutral pull) 50×0.04 + (100-50)×0.04×0.35 = 2.0+0.7 = 2.7 pts
- At score 30: 50×0.04 + (30-50)×0.04×0.35 = 2.0−0.28 = 1.72 pts
- Effective range: ~1.0 pt

The grade ceiling (64.9) is the binding constraint for T-LOW in any case where
the dimension alone cannot move more than ~1 grade. This is belt-and-suspenders.

### 2.3 What "held" output looks like

| State | `grade_estimate` | `final_score_estimate` | `data_sufficiency` | New field |
|---|---|---|---|---|
| Normal (T-MOD / T-HIGH) | A/B/C/D/E/S | numeric | sufficient | `ingredient_confidence: "moderate"` or `"high"` |
| T-LOW (ceiling applies) | B/C/D/E | ≤64.9 | sufficient | `ingredient_confidence: "low"`, `ingconf_ceiling_applied: true` |
| T-NONE (withheld) | `null` | `null` | `ingredient_data_absent` | `ingredient_confidence: "none"`, `ingredient_confidence_gate: "withheld"` |
| Existing insufficient_data (panel) | `"insufficient_data"` | numeric | insufficient | unchanged |

The frontend must treat `grade_estimate: null` with `ingredient_data_absent` as
"data unavailable" — not as E or as the existing insufficient_data path. This
is a new display state.

---

## 3. Interaction with Existing Ceilings

### 3.1 Panel-completeness confidence gate (existing)

`compute_confidence()` produces a numeric score (0-100) from panel field
coverage. When that score falls below thresholds:
- `confidence_score < 40` → `confidence_ceiling = CONFIDENCE_INSUFFICIENT_CEILING = 50`
- `confidence_score 40–59` → `confidence_ceiling = CONFIDENCE_LOW_CEILING = 75`
- `confidence_score ≥ 60` → no ceiling (None)

This gate and the new ingredient-confidence gate address orthogonal axes:
- Panel completeness = "do we have all the nutritional numbers?"
- Ingredient confidence = "can we read the composition?"

They can fire together or independently. When both fire, the more binding ceiling
governs. There is no additive combination — both are independent score caps.

**Example**: A product with a partial nutritional panel (confidence_ceiling=75)
AND order-only ingredients (ingconf_ceiling=64.9). The binding ceiling is 64.9.
The product cannot score above B. This is correct: we know less about it on two
independent axes.

**Example**: A product with full panel data (no confidence ceiling) AND order-only
ingredients (ingconf_ceiling=64.9). The binding ceiling is 64.9. This is the
primary target case (supplements with clean panels but impenetrable ingredient
lists).

### 3.2 Trans-fat veto (existing)

The trans-fat veto returns grade E unconditionally before either ceiling applies.
The ingredient-confidence gate runs after the out-of-scope check but BEFORE the
trans-fat veto in the current pipeline ordering. This is intentional: a product
with zero readable ingredients AND trans fat still receives the trans-fat veto
(the veto fires on a nutritional panel signal, not on ingredient text). The veto
therefore takes precedence over the T-NONE withhold. Result: grade E (veto), not
null (withheld). This is the correct outcome — trans fat is a safety veto, not a
data-quality outcome.

Implementation note: in `score_engine_v2.py`, the trans-fat veto is inside
`evaluate_guardrails()` which runs AFTER the confidence computation. The T-NONE
early return described in §2.1 should be placed BEFORE `evaluate_guardrails()`.
However, to prevent the early return from suppressing a trans-fat veto, the
implementation should check trans-fat first:

```python
if BARI_INGCONF_V1:
    # T-NONE check — but only if trans-fat veto cannot apply
    # (trans_fat_veto reads from the panel, not ingredients)
    # Veto check is cheap: just read the l3 signal
    if ing_conf == "none" and not l3.get("has_trans_fat_veto_risk", False):
        return <withheld result>
    elif ing_conf == "none":
        # Let normal pipeline run; trans-fat veto will catch it via evaluate_guardrails
        pass
```

Alternatively, run the T-NONE check after `evaluate_guardrails()`. Either
approach is acceptable; the Data Agent implementation must verify the behavior
against a product with no ingredients AND a trans-fat signal.

### 3.3 Guardrail caps (binding_cap)

Guardrail caps (PHVO, sweetener, sodium, processing-load) are applied AFTER
the weighted dimension score and BEFORE floors. The ingredient-confidence ceiling
is applied AFTER floors, at the same point as the existing `confidence_ceiling`.
This ordering preserves the existing cap-then-floor-then-ceiling semantics:

```
weighted_dim_score
→ composition_scale adjustment (NEW, §2.1 Point B)
→ evaluate_guardrails() → binding_cap
→ scaled_penalty
→ polyol_penalty
→ apply_floors()
→ ingconf_ceiling AND confidence_ceiling (whichever more binding governs)
→ final_score
→ score_to_grade()
```

### 3.4 Inversion-invariant guardrail (TASK-395 de-chain safety net)

The de-chain roadmap's stated safety net is the inversion-invariant: adding sugar
or additives must never raise a score; removing data must never raise a score.
The ingredient-confidence gate reinforces the second arm of this invariant. A
product with T-NONE (no ingredient data) cannot score higher than a comparable
product with T-HIGH (full ingredient data), because T-NONE returns null — it
doesn't even participate in the ranked comparison.

For T-LOW vs T-HIGH: the T-LOW ceiling (B = 64.9) ensures a product with
order-only ingredients can never leapfrog a comparable product with stated
percentages that scores A or S. The invariant holds.

### 3.5 No interaction with BARI_GLASSBOX_D5D6 D6 gate

The Glass Box D6 gate (`BARI_GLASSBOX_D5D6`) operates on the nutritional panel
transparency (D5 bands: full, minor, partial, severe) and emits `d6_gate_state`
(unconstrained / demote / withhold). The ingredient-confidence gate operates on
ingredient text readability. They are independent:
- A product can have a fully transparent panel (Glass Box: unconstrained) but
  zero ingredient text (new gate: withheld).
- A product can have opaque panel gaps (Glass Box: demote) with full percentage
  data in its ingredient list (new gate: T-HIGH, no ceiling).

Neither gate should call the other's functions or read the other's outputs.

---

## 4. The B2 Ranking-Formula Issue

### What the Red-Team CRITICAL C-2 actually found

The matrix signal probe v5.1 report (`analysis/matrix_signal_probe_v5_1_report.txt`,
run 2026-06-26) documents the following:

- B2 gate (ordinal ranking on 20 T3 pairs): **20/20 PASS at v5.1 (100%)**
- 1 knife-edge pair (RP-08): margin = +0.5 pts (oats 47% > oats 39%)
- The report does NOT show 25% mis-ordering. The ~25% figure cited in the TASK-395C
  delegation likely refers to an earlier probe version or a different corpus slice.

The actual finding: the formula correctly separates all 20 T3 pairs at v5.1, but
RP-08's margin is dangerously thin (+0.5 pts). A minor label-scrape variance,
rounding change, or signal extractor update could flip it. This is a *fragility*
finding, not a mis-ordering finding.

### Recommendation

**Scope as a separate sub-task (TASK-395D): B2 knife-edge robustness.**

Rationale for separating:

1. The D6 confidence gate (TASK-395C) does not fix knife-edge margins — it
   constrains the grade ceiling for T-LOW products and withholds T-NONE products.
   RP-08 is two T3 products that presumably have readable ingredient text; the
   gate does not touch them.

2. The formula fix for knife-edge robustness requires re-running the full B2
   matrix with modified parameters, which is a Data Agent / TASK-395A/B scope.
   The structured reader fix in TASK-395A (dedup comparator: stated_pct must beat
   position-weight) may partially address this, since RP-08's thin margin involves
   a case where a small stated_pct difference (47% vs 39% oats) may be competing
   with position-weight inference.

3. A B2 formula change that intentionally widens the 38%–47% separation band
   touches the DIMENSION_WEIGHTS or the `_ratio_to_grain_score()` mapping —
   these require a separate D6 proposal and D7 co-sign, as they affect all
   scoring categories that use the matrix signal.

**Proposed TASK-395D scope:**
- Analyze whether the TASK-395A dedup fix (stated_pct beats position-weight)
  naturally widens RP-08's margin
- If not: propose a calibration adjustment to the effective_pct weighting formula
  that increases separation in the 0.35–0.50 grain_whole_ew band
- D6 + D7 co-sign required before activation
- Target: RP-08 margin ≥ 3.0 pts after TASK-395A fix

---

## 5. Machine-Checkable Acceptance Criteria

The following assertions are runnable against the scored supplement corpus (or
any scored category corpus) once `BARI_INGCONF_V1=on`:

### AC-1: Hard no-grade rule (T-NONE)
```python
for product in scored_corpus:
    if product.get("ingredient_confidence") == "none":
        assert product["grade_estimate"] is None, (
            f"AC-1 FAIL: {product['product_id']} has ing_conf=none "
            f"but grade={product['grade_estimate']}"
        )
        assert product["final_score_estimate"] is None, (
            f"AC-1 FAIL: {product['product_id']} has ing_conf=none "
            f"but score={product['final_score_estimate']}"
        )
        assert product["data_sufficiency"] == "ingredient_data_absent", (
            f"AC-1 FAIL: {product['product_id']} wrong data_sufficiency"
        )
```

### AC-2: T-LOW grade ceiling
```python
for product in scored_corpus:
    if product.get("ingredient_confidence") == "low":
        grade = product.get("grade_estimate")
        assert grade not in ("S", "A"), (
            f"AC-2 FAIL: {product['product_id']} has ing_conf=low "
            f"but grade={grade} (must be B or below)"
        )
        score = product.get("final_score_estimate")
        if score is not None:
            assert score <= 64.9, (
                f"AC-2 FAIL: {product['product_id']} has ing_conf=low "
                f"but score={score} (must be ≤64.9)"
            )
```

### AC-3: T-MOD / T-HIGH unconstrained (by THIS gate)
```python
for product in scored_corpus:
    if product.get("ingredient_confidence") in ("moderate", "high"):
        # Ensure the ingconf gate did not apply a ceiling for these tiers
        assert not product.get("ingconf_ceiling_applied", False), (
            f"AC-3 FAIL: {product['product_id']} has ing_conf=moderate/high "
            f"but ingconf_ceiling_applied=True"
        )
```

### AC-4: T-NONE products not present in any ranked comparison output
```python
for product in scored_corpus:
    if product.get("ingredient_confidence") == "none":
        assert product.get("grade_estimate") is None, "AC-4 see AC-1"
        # These products must be excluded from the frontend ranked display
        # (enforcement is at the frontend contract layer, not the score engine)
```

### AC-5: Inversion invariant preserved (composition resolution cannot raise a score)
```python
# For a given product, score with T-HIGH must be >= score with T-LOW >= score with T-NONE(null)
# This is verified structurally: T-NONE → null; T-LOW → ceiling 64.9; T-HIGH → no ceiling.
# The scale multiplier (0.35 for T-LOW vs 1.0 for T-HIGH) applied to wfi_contribution
# can only reduce or preserve the weighted_dim_score, never increase it.
# Formal check: verify composition_scale is in [0, 1] for all tiers.
for tier, scale in [("none", 0.0), ("low", 0.35), ("moderate", 1.0), ("high", 1.0)]:
    assert 0.0 <= scale <= 1.0
```

### AC-6: Existing paths byte-identical when flag OFF
```python
# Run the same corpus with BARI_INGCONF_V1=off and =on;
# for any product with ing_conf in ("moderate", "high"):
# score and grade must be identical between the two runs.
# (T-NONE and T-LOW products will differ — that is the intended change.)
```

### AC-7: Corpus count check
```python
# Report: how many products are T-NONE / T-LOW / T-MOD / T-HIGH
# and how many grades were withheld vs ceiling-applied.
# Expected (supplement corpus baseline): none~27, low~239, moderate~524, high~56
# Any significant deviation from these counts is a reader regression, not a gate issue.
```

### AC-8: Trans-fat veto still fires on T-NONE products with trans-fat risk
```python
for product in scored_corpus:
    if (product.get("ingredient_confidence") == "none"
        and l3.get("trans_fat_status") in ("veto", "high_concern")):
        # Either trans_fat_veto=True result, or grade=null (withheld before veto check)
        # Both are acceptable depending on implementation order (see §3.2)
        result = score_product(product, ...)
        assert (result.get("trans_fat_veto_applied") is True
                or result.get("grade_estimate") is None), (
            f"AC-8 FAIL: trans-fat veto path broken for T-NONE product"
        )
```

---

## 6. Rollout Flag

The gate is gated behind `BARI_INGCONF_V1` (env flag, default OFF), following
the established pattern for all score-affecting changes in this codebase. The
flag must be activated in:
- `batch_run_*.py` scripts for each category run that uses the structured reader
- The score-switch spine (`spine_flip.py`)
- Any other runner that calls `score_product()`

When `BARI_INGCONF_V1=off` (default), the engine is byte-identical to the
pre-gate baseline for all products. All existing baselines remain valid until
the flag is activated for a category run.

---

## 7. What Requires Product Agent D7 Co-Sign

The following decisions require Product Agent D7 co-sign before any code
implementation or category re-run under this flag:

| Item | Decision | Nutrition position | Why D7 needed |
|---|---|---|---|
| 7.1 | T-LOW grade ceiling: B (64.9) vs A (79.9) | B — position-order is too coarse for A-range | Affects live supplement scores; ~239 products potentially capped |
| 7.2 | T-NONE behavior: grade=null vs grade="E" | null (withheld, not punished) — zero data is not a failing grade, it's a missing grade | Consumer-facing display state; "E" for no-data is misleading |
| 7.3 | `data_sufficiency` label for T-NONE: `ingredient_data_absent` | Yes — distinct from `insufficient_data` (which is panel-completeness) | Frontend display contract change |
| 7.4 | Composition scale values (0.35 for low; 1.0 for moderate and high) | Ruled by Nutrition Agent 2026-06-26: moderate=1.0 (not 0.70); rationale in §1 and §2.2 | Confirms ruling; builder must update `_ING_CONF_COMPOSITION_SCALE` accordingly |
| 7.5 | B2 knife-edge as TASK-395D (separate sub-task, not part of this gate) | Scope separation is correct | Sub-task creates its own D6/D7 requirement |

D7 items 7.1 and 7.2 are the most consequential. Either partner can block. If
Product Agent sets a different T-LOW ceiling (e.g., A instead of B), this spec
must be updated and re-versioned before implementation.

---

## 8. What Is NOT In This Spec

- Any change to `compute_confidence()` or `CONFIDENCE_INSUFFICIENT_CEILING` /
  `CONFIDENCE_LOW_CEILING` — those are untouched.
- Any change to DIMENSION_WEIGHTS — the 0.04 weight for `whole_food_integrity`
  is not modified; only the contribution is scaled toward neutral at T-LOW.
- Any change to the B2 matrix ranking formula — deferred to TASK-395D.
- Any macro→composition estimation — retired per the forum decision (circular at
  r=0.811, information-theoretically blind at 8% macro-twins).
- Any change to the NOVA proxy or ingredient classifiers — out of scope.

---

## Appendix A: Calibration Arithmetic

At T-LOW (scale=0.35), maximum score impact from the composition weight adjustment:

```
wfi_score range: 30 (NOVA-4) to 100 (NOVA-1, single ingredient)
dimension weight: 0.04

At T-HIGH: contribution range = 30×0.04 to 100×0.04 = 1.2 to 4.0 pts
At T-LOW:
  min: 50×0.04 + (30-50)×0.04×0.35 = 2.0 − 0.28 = 1.72 pts
  max: 50×0.04 + (100-50)×0.04×0.35 = 2.0 + 0.70 = 2.70 pts

Max score REDUCTION from T-HIGH to T-LOW (for a NOVA-1 product):
  T-HIGH max: 4.0 pts
  T-LOW max: 2.70 pts
  Delta: −1.30 pts

Max score INCREASE from T-HIGH to T-LOW (for a NOVA-4 product — reduces penalty):
  T-HIGH: 1.2 pts
  T-LOW: 1.72 pts
  Delta: +0.52 pts (a NOVA-4 product is slightly less penalized at T-LOW)
```

The ±1.3 pt range is well within 1 grade band (B→C = 15 pts, C→D = 15 pts).
The composition weight adjustment alone cannot change a grade. The T-LOW ceiling
(64.9) is the operative constraint for any product that would otherwise score A
or S; the weight adjustment is a secondary honest-signal reduction.

---

## Appendix B: Evidence Basis

- Owner hard rule (2026-06-26): "No confidence of ingredients and values is a
  hard no-go." Triggered by cottage cheese promoted to S on zero readable
  ingredients.
- Owner de-chain directive (2026-06-24, TASK-395): remove hard chains; keep
  only safety vetoes + inversion-invariant guardrail.
- Macro-inference retirement: forum consensus (macro→composition is circular at
  r=0.811, 8% macro-twins make it information-theoretically blind). Reference:
  `reports/macro_inference_retirement_v1.md` (not yet committed to master — in
  the worktree from TASK-395 predecessor work; reference confirmed by the forum
  report per the delegation brief).
- Corpus distribution: none=27, low=239, moderate=524, high=56 (from the
  delegation brief, citing agent aae66f48e330c2e8c from the TASK-395 forum).
- B2 knife-edge finding: `03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v5_1_report.txt`,
  RP-08 (margin=+0.5), run 2026-06-26T05:13:14.
- Evidence quality: Moderate. The gate design is sound in principle; the exact
  scale multipliers (0.35/0.70) are proposed calibration values, not lab-derived
  optima. They can be adjusted at D7 without changing the gate architecture.

---

```json
{
  "return_contract": {
    "task": "TASK-395C",
    "status": "RETURNED",
    "lane": "Nutrition/D6",
    "summary": "Formal D6 spec for the ingredient-confidence gate. Four-tier table (none/low/moderate/high), exact engine mechanism (two insertion points in score_product(), BARI_INGCONF_V1 flag), interaction model with existing ceilings, B2 knife-edge scoped to separate TASK-395D, eight machine-checkable acceptance criteria.",
    "artifacts": [
      {
        "path": "C:/Bari/reports/d6_confidence_gate_spec_v1.md",
        "sha256": "not-computed — single write, no prior version"
      }
    ],
    "counts": {
      "tiers_defined": 4,
      "acceptance_criteria": 8,
      "d7_items_requiring_cosign": 5,
      "dimensions_affected": 1,
      "dimensions_total": 10,
      "products_impacted_T_NONE": 27,
      "products_impacted_T_LOW": 239,
      "products_unaffected_T_MOD_HIGH": 580
    },
    "commands_run": [],
    "key_decisions": [
      "T-NONE → grade withheld (null), not E — zero ingredient data is a missing-grade, not a failing grade",
      "T-LOW ceiling = B (64.9) — position-order too coarse for A/S promotion; order IS real legal data, just insufficient resolution",
      "T-MOD / T-HIGH → no ceiling from this gate; existing panel-completeness ceiling remains orthogonal",
      "Composition weight scale: only whole_food_integrity (dim weight 0.04) is pulled toward neutral — nutrition panel dimensions untouched",
      "B2 knife-edge (RP-08 margin +0.5) scoped to separate TASK-395D — not a mis-ordering, a fragility finding; TASK-395A dedup fix may resolve it",
      "Interaction with trans-fat veto: veto takes precedence; implementation must verify T-NONE does not suppress a trans-fat veto"
    ],
    "d7_cosign_required": {
      "Product_Agent": true,
      "items": [
        "7.1: T-LOW ceiling (B vs A)",
        "7.2: T-NONE behavior (null vs E)",
        "7.3: data_sufficiency label (ingredient_data_absent)",
        "7.4: composition scale values (0.35/0.70/1.0)",
        "7.5: B2 knife-edge as TASK-395D scope separation"
      ]
    },
    "not_done": [
      "Product Agent D7 co-sign — required before any code implementation",
      "Engine implementation (Data Agent, post D7)",
      "Corpus re-run under BARI_INGCONF_V1=on (post D7 + implementation)",
      "Adversarial QA gate on re-scored corpus (AC-1 through AC-8)",
      "TASK-395D: B2 knife-edge formula robustness (separate sub-task)",
      "Frontend display contract for grade=null / ingredient_data_absent state"
    ],
    "acceptance_test_result": "CANNOT RUN — engine not yet modified (spec only; BARI_INGCONF_V1 does not exist yet). AC-1 through AC-8 are the verification harness to run post-implementation.",
    "confidence": "Moderate — gate architecture is grounded in real engine code (score_engine.py, structured_ingredient_reader.py read directly); scale multipliers are calibration proposals, not optima; B2 mis-ordering claim in the brief did not match the v5.1 probe report (20/20 pass, 1 knife-edge), reported accurately."
  }
}
```
