# BSIP2 Sprint 1 — Production Release v1

**Task:** TASK-047  
**Owner:** Frontend Architect  
**Date:** 2026-05-31  
**Status:** RELEASED TO PRODUCTION

---

## 1. Release Summary

Sprint 1 approved signals have been merged into the production BSIP2 engine (`proto_v0/src/`). All five approved signals are live. EV-005 was revised with humectant-label detection prior to deployment (governance decision TASK-046B). Validation passed on both Snack Bars (53 products) and Hummus (69 products).

---

## 2. Final Signal Specifications

### EV-012 — Saturated-to-Unsaturated Fat Ratio

| Field | Value |
|-------|-------|
| Signal name | `fat_quality_v2` |
| Activation guard | `fat_g >= 8.0` |
| Below guard | v1 formula (absolute sat fat) unchanged |
| Above guard | piecewise linear map: unsat/sat ratio → score |
| Ratio anchors | 0.00→10, 0.25→25, 0.50→40, 1.00→55, 2.00→70, 3.50→83, 6.00→93 |
| Adjustments | seed oil −10, trans fat veto −20 / high −10 (both paths) |
| Implementation | `_score_fat_quality_sprint1()` in `score_engine.py` |

### EV-003 — Emulsifier Risk Differentiation

| Field | Value |
|-------|-------|
| Signal name | `mucus_thinning_emulsifier_load` |
| Tier 1: high-risk | CMC (E466), Polysorbate 80 (E433), Carrageenan (E407) → additive count +2 |
| Tier 2: neutral | Lecithin (soy/sunflower, E322) → additive count −1 if sole emulsifier |
| Effect | Changes `sprint1_additive_count` fed to `_score_additive_quality_sprint1()` |
| Implementation | `_detect_high_risk_emulsifier()`, `_detect_neutral_emulsifier()` in `signal_extractor.py` |

### EV-019 — Prebiotic Gum Exemption

| Field | Value |
|-------|-------|
| Signal name | `prebiotic_gum_exemption` |
| Scope | Gum arabic (E414), acacia gum, arabinogalactan |
| Effect | Stabilizer count −1 if gum arabic is sole stabilizer reason |
| Implementation | `_detect_prebiotic_gum()` in `signal_extractor.py` |

### EV-004 — Allulose Caloric/Glycemic Exemption

| Field | Value |
|-------|-------|
| Signal name | `allulose_adjusted_sugar_g` |
| Conservative adjustment | Sugar penalty reduced by 30% when allulose detected |
| Caloric adjustment | None (flag only — quantity not label-readable) |
| Implementation | `_score_glycemic_quality_sprint1()` in `score_engine.py` |

### EV-005 — Polyol Laxative Potential (Revised)

| Field | Value |
|-------|-------|
| Signal name | `polyol_laxative_potential` |
| Revision | Humectant refinement applied (TASK-046B) |
| **Humectant rule** | Polyol inside manufacturer-declared "חומרי הלחה" group → warning flag, **no score penalty** |
| Single standalone polyol | −4 pts |
| Multiple polyols (2+) | −10 pts |
| Keto/sugar-free + multiple | −15 pts |
| Applied | Post-cap (safety signal, not nutritional quality) |
| Detection | `HUMECTANT_GROUP_RE` regex in `signal_extractor.py`; `_extract_humectant_group_polyols()` |
| Scoring | `_compute_polyol_penalty()` uses `sprint1_penalty_polyol_count` (excludes humectant polyols) |

#### EV-005 Humectant Refinement Detail

A polyol within a "חומרי הלחה (גליצרול, סורביטול)" manufacturer declaration is a functional moisture-retention agent. All 7 affected snack bar products used sorbitol as a humectant, co-declared with glycerol. The HUMECTANT_GROUP_RE pattern captures the parenthetical group content and excludes matching polyols from the penalty count.

New L3 fields:
- `sprint1_humectant_polyols` — list of polyols excluded from penalty
- `sprint1_penalty_polyol_count` — count used for scoring (excludes humectants)
- `sprint1_penalty_polyols` — list of polyols that do attract penalty
- `sprint1_polyol_count` — total detected (audit trail)

---

## 3. Code Changes — Production Files

### `proto_v0/src/signal_extractor.py`

Added after vocabulary section:
- `HIGH_RISK_EMULSIFIER_PATTERNS`, `NEUTRAL_EMULSIFIER_PATTERNS`, `PREBIOTIC_GUM_PATTERNS`
- `ALLULOSE_PATTERNS`, `POLYOL_TYPE_MAP`
- `NON_LECITHIN_EMULSIFIER_RE`, `HUMECTANT_GROUP_RE`

Added detection functions:
- `_detect_high_risk_emulsifier()`, `_detect_neutral_emulsifier()`, `_detect_prebiotic_gum()`
- `_detect_allulose()`, `_count_polyol_types()`, `_extract_humectant_group_polyols()`

Updated `extract_signals()` L3 output with 15 new sprint1 fields.

### `proto_v0/src/score_engine.py`

Added sprint1 constants:
- `_FAT_RATIO_GUARD = 8.0`, `_POLYOL_PENALTY_SINGLE/MULTI/KETO`, `_ALLULOSE_SUGAR_REDUCE`

Added scoring functions:
- `_fat_ratio_to_score()` — piecewise linear fat ratio mapper
- `_score_fat_quality_sprint1()` — EV-012 production scorer
- `_score_glycemic_quality_sprint1()` — EV-004 production scorer
- `_score_additive_quality_sprint1()` — EV-003/019 production scorer
- `_compute_polyol_penalty()` — EV-005 production penalty with humectant exclusion

Updated `score_product()`:
- Dimension scoring calls replaced with sprint1 versions
- Stage 7 now applies polyol penalty post-cap
- Return dict gains `polyol_penalty` and `polyol_penalty_note` fields

### Sprint1 overlay files (sprint1/)

- `signal_extractor_v2.py` — updated with same humectant detection logic
- `score_engine_v2.py` — updated to use `sprint1_penalty_polyol_count`
- Both remain functional for reference and audit comparison

---

## 4. Validation Summary

### Snack Bars (53 products)

| Metric | Value |
|--------|-------|
| Products processed | 53 |
| Scored (sufficient data) | 48 |
| Insufficient data | 5 |
| Pipeline errors | 0 |
| EV-005 polyols detected | 7 products |
| EV-005 humectant-exempt | 7 products |
| EV-005 penalty applied | **0 products** |

**Grade distribution (48 scored):**

| Grade | Count |
|-------|-------|
| B | 2 |
| C | 11 |
| D | 13 |
| E | 22 |

**EV-005 humectant-exempt products (sorbitol, no penalty):**

| Product | Sorbitol group position | v1 score | Production score |
|---------|------------------------|----------|-----------------|
| חטיפי דגנים פיטנס קרם ועוגיות שישייה | 8/24 | 24.5 | 24.9 |
| חטיף דגנים שוקו וניל נסטלה שישייה | 5/15 | 27.9 | 28.6 |
| סיני מיניס חטיף בטעם קינמון על שכבת קרם חלב | 7/15 | 25.7 | 26.3 |
| חטיפי דגנים פיטנס שוקולד בננה שישייה | 7/17 | 23.9 | 25.6 |
| חטיף דגנים מצופה שוקולד עם עוגיות קרמל נוגט | 5/18 | 16.9 | 16.6* |
| חטיף דגנים מצופה שוקולד חלב עם שברי אגוזים | 5/15 | 18.1 | 17.8* |
| חטיף דגנים עם שברי אגוזים ושוקולד חלב בטר | 6/15 | 31.4 | 31.0* |

*Minor difference from v1 baseline reflects EV-012 fat ratio adjustment applied simultaneously.

**Observation:** All 7 products recover the −4 polyol penalty from the interim Sprint 1 run (TASK-046B). No grade migrations from the EV-005 fix. All remain E grade. EV-012 (fat ratio) introduces minor additional movement.

### Hummus (69 products)

| Metric | Value |
|--------|-------|
| Products processed | 69 |
| Scored (sufficient data) | 67 |
| Insufficient data | 2 |
| Pipeline errors | 0 |
| EV-005 polyols detected | **0 products** |
| EV-005 penalty applied | **0 products** |

**Grade distribution (67 scored):**

| Grade | Count |
|-------|-------|
| A | 8 |
| B | 31 |
| C | 22 |
| D | 6 |

**EV-003/019 emulsifier signals in hummus:** preserved from previous run_hummus_001 baseline; no high-risk emulsifiers detected in this corpus. Lecithin exemptions apply where relevant.

**EV-005 result:** Zero polyols detected in the hummus corpus. Expected — hummus, tahini, and savory dip formulations do not use polyol sweeteners or humectants at detectable levels.

---

## 5. Score Movement Summary (Snack Bars vs v1 baseline)

| Signal | Products affected | Avg score change |
|--------|------------------|-----------------|
| EV-012 fat ratio | 48 (all scored) | +0.1 to −0.3 (fat profile dependent) |
| EV-003 lecithin exempt | ~20 products | +1.8 (additive count −1) |
| EV-005 humectant fix | 7 products | +4.0 recovery vs interim run |
| EV-004 allulose | 0 products | n/a (no allulose in corpus) |
| EV-019 gum exempt | varies | marginal |

No grade-boundary crossings introduced by Sprint 1 in either corpus.

---

## 6. Known Limitations

| # | Limitation | Scope | Mitigation |
|---|-----------|-------|------------|
| L-001 | Hummus category routing returns `cat=None` | Hummus corpus only | Pre-existing gap; hummus router not in v2 router. Scores computed without category context — conservative path. Does not affect snack bar corpus. |
| L-002 | Hummus BSIP1 schema is pre-enrichment-v1 | Hummus corpus only | Missing `conflicts_summary`, `missing_fields` fields trigger validation warnings. Non-fatal — pipeline degrades gracefully. |
| L-003 | EV-005 humectant detection uses text pattern only | All categories | `HUMECTANT_GROUP_RE` catches all confirmed cases. Polyols not co-listed in "חומרי הלחה" groups correctly receive penalty. |
| L-004 | fat_quality unreliable for ~58/69 hummus products | Hummus corpus only | Shufersal fat-row scraping defect (TASK-039). fat_quality dimension scores are inflated. All other dimensions are correct. |
| L-005 | EV-004 allulose: quantity not adjustable | All categories | Presence-only detection — 30% conservative reduction applied. No products in either corpus triggered this in Sprint 1. |
| L-006 | EV-012 fat ratio guard (8g) | All categories | Products with fat < 8g use v1 formula. This is intentional — ratio logic is unreliable at very low fat quantities. |

---

## 7. Rollback Procedure

The sprint1 functions use naming conventions that allow selective rollback without touching the rest of the engine.

**Full rollback (revert to v1 behavior):**
1. In `score_engine.py`, revert `score_product()` to call:
   - `score_glycemic_quality()` instead of `_score_glycemic_quality_sprint1()`
   - `score_additive_quality()` instead of `_score_additive_quality_sprint1()`
   - `score_fat_quality()` instead of `_score_fat_quality_sprint1()`
   - Remove polyol penalty from Stage 7
2. The sprint1 functions (`_score_fat_quality_sprint1`, etc.) can remain in the file or be removed — they do not execute unless called.

**Signal-level rollback (per signal):**
- EV-012: restore `score_fat_quality()` call in `score_product()`
- EV-003/019: restore `score_additive_quality()` call
- EV-004: restore `score_glycemic_quality()` call
- EV-005: remove `_compute_polyol_penalty()` call from Stage 7

**No data migration required.** The sprint1 L3 fields are additive to v1 output; removing the scoring calls restores v1 scores without any BSIP1 data changes.

---

## 8. Production Artifacts

| File | Description |
|------|-------------|
| `proto_v0/src/signal_extractor.py` | Production signal extractor (Sprint 1 merged) |
| `proto_v0/src/score_engine.py` | Production score engine (Sprint 1 merged) |
| `sprint1/signal_extractor_v2.py` | Sprint 1 overlay (reference, humectant fix applied) |
| `sprint1/score_engine_v2.py` | Sprint 1 overlay (reference, humectant fix applied) |
| `sprint1/run_production_snack_bars.py` | Production validation runner — snack bars |
| `sprint1/run_production_hummus.py` | Production validation runner — hummus |
| `sprint1/outputs/production_snack_bars.json` | Full snack bars validation results |
| `sprint1/outputs/production_snack_bars_summary.md` | Snack bars summary report |
| `sprint1/outputs/production_hummus.json` | Full hummus validation results |
| `sprint1/outputs/production_hummus_summary.md` | Hummus summary report |
| `sprint1/production_decision_v1.md` | Governance decision (TASK-046B) |

---

*TASK-047 — Production Release v1*  
*Frontend Architect + Chief Nutrition Officer — 2026-05-31*
