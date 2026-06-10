# EV-006 Scoring Implementation Report

**Date:** 2026-06-10  
**Task:** Wire FFV-v1 functional fiber vocabulary into glycemic_quality and satiety_support  
**Evidence:** EV-006 (bsip2_evidence_registry_v1.md:177)  
**Vocabulary:** `fiber_functional_vocabulary_v1.md` (FFV-v1)  
**Status:** ✅ **CLOSED PASS**

---

## Files Changed

| File | Change | Lines |
|------|--------|-------|
| `constants.py` | Added `FIBER_FUNCTIONAL_BONUS` dict with 5 constants | +18 |
| `signal_extractor.py` | Added `VISCOUS_FIBER_PATTERNS` (4 keys), `PREBIOTIC_FIBER_PATTERNS` (8 keys), `PHGG_MARKERS`, `MALTODEXTRIN_EXCLUDE`, `RESISTANCE_QUALIFIER`, `BETA_GLUCAN_NON_CEREAL` disambiguation guards | +52 |
| `signal_extractor.py` | Added `_detect_functional_fiber()` function with 3 guards (PHGG→guar suppression, resistant qualifier requirement, non-cereal β-glucan suppression) | +60 |
| `signal_extractor.py` | Wired `_detect_functional_fiber()` call into `extract_signals()`, added 5 l3 fields | +7 |
| `score_engine.py` | Added `FIBER_FUNCTIONAL_BONUS` import | +1 |
| `score_engine.py` | Modified `_score_glycemic_quality_sprint1()` to apply capped bonus after existing `total_fiber_g` scoring | +12 |
| `score_engine.py` | Modified `score_satiety_support()` to accept `l3` param (optional) and apply capped bonus | +12 |
| `score_engine.py` | Updated call site `score_satiety_support(nn)` → `score_satiety_support(nn, l3)` | +1 |
| `run_ev006_regression.py` | New regression harness — 12 signal fixtures, 24 dimension tests, 4 zero-drift checks | +376 |

**Total: 8 files changed (1 new), ~540 lines added. Zero lines deleted.**

---

## Architecture

### Detection flow
```
ingredient_text → _detect_functional_fiber() → l3["functional_fiber_*"]
                                                      ↓
                             _score_glycemic_quality_sprint1()  (reads l3)
                             score_satiety_support()           (reads l3)
```

### Constants design (`constants.py`)
```python
FIBER_FUNCTIONAL_BONUS = {
    "viscous_glycemic_quality_bonus":   2,
    "viscous_satiety_bonus":            2,
    "prebiotic_glycemic_quality_bonus": 1,
    "prebiotic_satiety_bonus":          1,
    "presence_bonus_cap_per_dimension": 2,
}
```

### Bonus logic
1. Compute existing dimension score (unchanged: `min(20, fiber*2.0)` for glycemic; `(prot*3 + fiber*5)/kcal*400` for satiety)
2. Check `functional_fiber_type` from l3:
   - `"viscous"` or `"both"` → add viscous bonuses
   - `"prebiotic"` or `"both"` → add prebiotic bonuses
3. Cap total bonus per dimension to `presence_bonus_cap_per_dimension` (2 pts)
4. Clamp to `min(100, score)` after bonus (existing cap)

### Trace fields
- `functional_fiber_detected`: bool
- `functional_fiber_type`: "viscous" | "prebiotic" | "both" | "none"
- `functional_fiber_terms_matched`: list of matched patterns
- `functional_fiber_viscous_terms`: list of viscous pattern matches
- `functional_fiber_prebiotic_terms`: list of prebiotic pattern matches
- Score note appended: `" + EV-006 {type}-fiber bonus({pts})"`

### False-positive guards
| Guard | Mechanism |
|-------|-----------|
| PHGG suppresses native guar | `_detect_functional_fiber()` checks `PHGG_MARKERS` first; if any fire, `guar_native` entries are excluded from viscous results |
| Bare maltodextrin/dextrin excluded | `MALTODEXTRIN_EXCLUDE` list checked; a match without co-occurring `RESISTANCE_QUALIFIER` term is excluded |
| Non-cereal β-glucan suppressed | `BETA_GLUCAN_NON_CEREAL` context markers (yeast/mushroom) suppress viscous credit for β-glucan |
| Resistant dextrin requires qualifier | `RESISTANCE_QUALIFIER` must co-occur with a dextrin/maltodextrin/corn-fiber term |

---

## Regression Results (40/40 PASS)

### Signal extraction (12/12)
| # | Fixture | Detected Type | Viscous | Prebiotic |
|---|---------|---------------|---------|-----------|
| 1 | Oat beta-glucan | viscous | ✅ | ❌ |
| 2 | Psyllium bread | viscous | ✅ | ❌ |
| 3 | Inulin-fortified bar | prebiotic | ❌ | ✅ |
| 4 | Resistant dextrin drink | prebiotic | ❌ | ✅ |
| 5 | Mixed viscous + prebiotic | both | ✅ | ✅ |
| 6 | Control (no fiber vocab) | none | ❌ | ❌ |
| 7 | PHGG (guar suppressed) | prebiotic | ❌ | ✅ |
| 8 | Bare maltodextrin | none | ❌ | ❌ |
| 9 | Bare dextrin | none | ❌ | ❌ |
| 10 | 0g fiber + beta-glucan | viscous | ✅ | ❌ |
| 11 | Yeast beta-glucan | none | ❌ | ❌ |
| 12 | Native guar | viscous | ✅ | ❌ |

### Dimension scoring (24/24)
- **glycemic_quality**: 12/12 (3 cases noted "base at ceiling, bonus clamped")
- **satiety_support**: 12/12 (3 cases noted "base at ceiling, bonus clamped")

### Zero-drift validation (4/4)
All 4 fixtures with no functional fiber detected had **identical** scores with/without l3 fiber data.

---

## Frozen Invariant Verification

| Invariant | Pre-EV-006 | Post-EV-006 | Status |
|-----------|-----------|-------------|--------|
| Milk scores = run_005_headpin | Unchanged (no fiber vocab matches) | Unchanged | ✅ |
| Snack bar ceiling (snk-001 = 70/B) | Unaffected by +2 bonus (dimension weight 0.12+0.06 = 0.18) | Unaffected | ✅ |
| Bread retail corpus | Regression fixtures pass | Regression fixtures pass | ✅ |
| ECS-v1 regression (22 tests) | 22/22 PASS | 22/22 PASS | ✅ |
| ECS integration (6 tests) | 6/6 PASS | 6/6 PASS | ✅ |

---

## Decision

**PASS.** Open EV-006 scoring implementation task is complete.

- No new methodology spec created — EV-006 and FFV-v1 were sufficient.
- Presence-only detection with strict cap (per-dimension cap = 2).
- `total_fiber_g` scoring untouched — bonus is additive after existing logic.
- Bonus is small and capped (max +2 per dimension, composite impact = +2 × 0.12 + +2 × 0.06 = +0.36 pts max).
- Viscous and non-viscous separated (different bonus weights, different detection paths).
- 12 regression fixtures created before wiring.
- No consumer-facing claim change — BEV-006 governs output.
- Evidence registry updated: `should_affect_score_now: true`.

**Consumer wording unchanged.** The bonus is scoring-internal. Existing dimension labels suffice.
