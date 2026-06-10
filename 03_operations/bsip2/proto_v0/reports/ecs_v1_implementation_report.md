# ECS-v1 Implementation Change Report

**Date:** 2026-06-10  
**Evidence registry:** EV-045  
**Engine tag:** (pending)  

---

## Summary

Emulsifier Complexity Score v1 (ECS-v1) implemented and integrated into the BSIP2 scoring engine. All 22 regression examples pass, all 6 integration tests pass, and score-drift analysis confirms frozen invariants are unaffected.

**Recommendation: PASS** — Implementation is correct, complete, and safe to activate.

---

## 1. Files Changed

| File | Lines changed | Change |
|------|--------------|--------|
| `ingredient_taxonomy.py` | +115 | Added 13 new Identity entries (4 medium + 8 low + modified_starch_stabilizer) |
| `signal_extractor.py` | +22 | Added `tax_emulsifier_medium`/`tax_emulsifier_low` signals, modified starch gate |
| `constants.py` | +17 | Added `EMULSIFIER_COMPLEXITY_CONSTANTS`, `EMULSIFIER_COMPLEXITY_FAMILY_BUDGET` |
| `score_engine.py` | +83 | Added `_emulsifier_complexity()` function, wired into Stage 7 penalty, added trace fields |

### 1.1 ingredient_taxonomy.py — New Identity entries

**Medium agents** (4): `mono_diglyceride` (E471), `datem` (E472e), `ssl` (E481), `pgpr` (E476)  
**Low agents** (8): `pectin` (E440), `gum_arabic` (E414), `guar_gum` (E412), `xanthan_gum` (E415), `locust_bean_gum` (E410), `agar` (E406), `gellan_gum` (E418), `sodium_alginate` (E401)  
**Gated medium**: `modified_starch_stabilizer` (E1400–E1450) — detected via structural path, counted only when position ≥ 4 or light/diet signal

### 1.2 signal_extractor.py — New L3 signals

- `tax_emulsifier_medium: list[str]` — mono/diglycerides, DATEM, SSL, PGPR, modified_starch_stabilizer
- `tax_emulsifier_low: list[str]` — lecithins, gums, pectin, agar, alginate, gellan
- Modified starch gate: position tracking + light/diet name signal

### 1.3 constants.py — Constants

```python
EMULSIFIER_COMPLEXITY_CONSTANTS = {
    "high_weight":          5,   # -5 per high-concern agent (CMC, P80)
    "medium_weight":        3,   # -3 per medium-concern agent
    "low_weight":           1,   # -1 per low-concern agent
    "complexity_moderate":  1,   # -1 for 2 distinct agents
    "complexity_high":      3,   # -3 for 3+ distinct agents
}
EMULSIFIER_COMPLEXITY_FAMILY_BUDGET = 8   # max total complexity penalty
```

### 1.4 score_engine.py — Scoring function

New function `_emulsifier_complexity(l3)` implements the ECS-v1 formula:

```
highest_penalty = max(penalty for each distinct agent by tier)
complexity_adj  = 0/0/1/3 for 0/1/2/3+ agents
total_penalty   = min(highest_penalty + complexity_adj, 8)
```

Applied at Stage 7 (post-cap penalty) alongside polyol penalty. Not a guardrail — does not interact with cap/penalty coordination.

---

## 2. Regression Results

### 2.1 All 22 spec examples — PASS (22/22)

| # | Scenario | Agents | Highest | Tier | Expected | Actual | Status |
|---|----------|--------|---------|------|----------|--------|--------|
| 1 | Plain almond butter | 0 | 0 | none | 0 | 0 | PASS |
| 2 | Peanut butter + lecithin | 1 low | −1 | simple | −1 | 1 | PASS |
| 3 | Hummus + guar + xanthan | 2 low | −1 | moderate | −2 | 2 | PASS |
| 4 | Plain Greek yogurt | 0 | 0 | none | 0 | 0 | PASS |
| 5 | Flavored yogurt + mod starch + pectin | 1 med + 1 low | −3 | moderate | −4 | 4 | PASS |
| 6 | Ice cream + CMC + carra + mono/di | 1 high + 2 med | −5 | high | −8 | 8 | PASS |
| 7 | Diet shake + CMC + lecithin + gum arabic | 1 high + 2 low | −5 | high | −8 | 8 | PASS |
| 8 | Whole milk | 0 | 0 | none | 0 | 0 | PASS |
| 9 | Plain bread | 0 | 0 | none | 0 | 0 | PASS |
| 10 | Bread light + E471 + E481 + E466 | 1 high + 2 med | −5 | high | −8 | 8 | PASS |
| 11 | Mayo + guar + xanthan | 2 low | −1 | moderate | −2 | 2 | PASS |
| 12 | Snack bar + lecithin + guar | 2 low | −1 | moderate | −2 | 2 | PASS |
| 13 | Snack bar + P80 + E471 + lecithin + xanthan | 1 high + 1 med + 2 low | −5 | high | −8 | 8 | PASS |
| 14 | Cream cheese + carra + LBG | 1 med + 1 low | −3 | moderate | −4 | 4 | PASS |
| 15 | Instant pudding + CMC + carra + guar + DATEM + mod starch | 1 high + 3 med + 1 low | −5 | high | −8 | 8 | PASS |
| 16 | Oat milk + CMC + gum arabic | 1 high + 1 low | −5 | moderate | −6 | 6 | PASS |
| 17 | Coconut milk + guar | 1 low | −1 | simple | −1 | 1 | PASS |
| 18 | Sugar-free gum + CMC + carra + gum arabic + lecithin | 1 high + 1 med + 2 low | −5 | high | −8 | 8 | PASS |
| 19 | Ketchup + xanthan | 1 low | −1 | simple | −1 | 1 | PASS |
| 20 | Plant yogurt + mod starch + pectin + guar + gellan | 1 med + 3 low | −3 | high | −6 | 6 | PASS |
| 21 | Bread + mod starch (pos 3, structural) | 0 (excluded) | 0 | none | 0 | 0 | PASS |
| 22 | Bread light + mod starch (pos 8) + E471 | 2 med | −3 | moderate | −4 | 4 | PASS |

### 2.2 Integration tests — PASS (6/6)

1. **additive_quality independence**: F1 identity deltas (−6) fire on additive_quality; ECS (−8) fires separately on emulsifier_complexity signal
2. **Stage 7 penalty application**: ECS penalty correctly subtracted: 70.0 − 8.0 = 62.0
3. **Frozen invariant — milk**: Whole milk has zero ECS penalty → unchanged 85/A
4. **Complex snack bar**: 4 agents → ECS=8 (family budget cap)
5. **Low-only moderate**: 2 low agents → ECS=2
6. **Carrageenan reclassification**: Carrageenan correctly treated as medium for ECS (not high)

---

## 3. Score-Drift Analysis

### 3.1 Frozen invariants — UNCHANGED

| Invariant | ECS-v1 Impact | Reasoning |
|-----------|---------------|-----------|
| Milk scores (85/A) | **0 drift** | No emulsifiers → penalty = 0 |
| Snack bar ceiling (70/B, snk-001) | **0 or negative drift** | ECS can only lower score, making breakthrough HARDER |
| Bread retail corpus | **0 drift for clean bread** | No emulsifiers → penalty = 0 |
| No snack bar reaches A | **Reinforced** | Any ECS penalty makes A harder to reach |

### 3.2 Category impact assessment

| Category | Typical agents | ECS range | Scoring impact |
|----------|---------------|-----------|----------------|
| Plant-based dairy | CMC, carrageenan, gum arabic, guar | −1 to −8 | New penalty for multi-agent products |
| Sauces/dressings | Guar, xanthan, lecithin | −1 to −2 | Modest for 1–2 gum products |
| Processed meats | Carrageenan, modified starch | −3 to −6 | Already penalised via fragmentation |
| Protein bars | Lecithin, mono/diglycerides, gums | −1 to −5 | New penalty for engineered bars |
| Desserts | CMC, carrageenan, guar, DATEM, mod starch | −1 to −8 | Highest impact category |
| Kids' foods | Various stabilisers | −1 to −6 | Variable |
| Light/diet breads | E471, E481, CMC, mod starch | −4 to −8 | Engineered breads now captured |

### 3.3 Double-counting verification

| Pair | Dimension 1 | Dimension 2 | Overlap? |
|------|-------------|-------------|----------|
| F1 identity deltas vs ECS | additive_quality (−3 each CMC/carra/P80) | emulsifier_complexity (−5/−3/−1) | **None** — different dimensions |
| additive_marker_count vs ECS | All additive categories | Emulsifier/stabiliser only | **None** — different scope |
| modified_starch fragmentation vs ECS | Processing quality (reconstructed) | Emulsifier complexity | **None** — different signals |

---

## 4. Trace Fields Added

The result dict now contains these new keys (always present):

| Key | Type | Description |
|-----|------|-------------|
| `emulsifier_complexity_penalty` | float | Total ECS-v1 penalty (0–8) |
| `emulsifier_complexity_penalty_note` | str\|None | Human-readable trace (when penalty > 0) |
| `emulsifier_complexity_detail` | dict\|None | Breakdown: agents, tier, adjustments |

L3 signals:
- `tax_emulsifier_medium: list[str]`
- `tax_emulsifier_low: list[str]`

---

## 5. Known Limitations

1. **No multi-family coordination**: ECS penalty is applied as a direct Stage 7 subtraction, not through `_coordinate_family`. The 8-pt budget is enforced internally. If multi-family penalty scaling is needed (e.g., ECS penalty competes with HP penalties for budget), the guardrail system needs extension.
2. **Old traces lack ECS signals**: The new `tax_emulsifier_medium`/`tax_emulsifier_low` signals are only emitted by the updated signal extractor. Pre-ECS traces will not show these fields and will compute ECS penalty = 0 on re-run.
3. **Modified starch gate requires product name**: The light/diet signal depends on `product.get("canonical_name_he")` being populated at signal extraction time.

---

## 6. Recommendation

**PASS** — Ship ECS-v1.

The implementation is:
- **Correct**: All 22 regression examples match spec exactly
- **Independent**: Separate dimension from F1 identity deltas (no double-counting)
- **Safe**: Frozen invariants unaffected; score drift is always negative for products with agents
- **Traceable**: Full breakdown emitted in trace dict
- **Bounded**: Maximum 8-pt penalty via family budget
- **Backward-compatible**: Products with no emulsifier/stabiliser agents get score = same as before
