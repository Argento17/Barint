```yaml
id: TASK-224
title: Implement ECS-v1 emulsifier_complexity_score into BSIP2 engine
status: CLOSED
created: 2026-06-10
closed: 2026-06-10
evidence_registry: EV-045
engine_component: bsip2 proto_v0
```

## DoD

1. [x] **Taxonomy extended**: 13 new Identity entries added to `ingredient_taxonomy.py` (4 medium + 8 low + modified_starch_stabilizer)
2. [x] **Signal extraction**: `tax_emulsifier_medium`/`tax_emulsifier_low` signals + modified starch position/light-diet gate in `signal_extractor.py`
3. [x] **Constants defined**: `EMULSIFIER_COMPLEXITY_CONSTANTS` + `EMULSIFIER_COMPLEXITY_FAMILY_BUDGET` in `constants.py`
4. [x] **Engine function added**: `_emulsifier_complexity()` in `score_engine.py` with correct formula and budget clamp
5. [x] **Score synthesis wired**: ECS penalty applied at Stage 7 alongside polyol penalty; result dict includes trace fields
6. [x] **22 regression examples PASS**: All spec examples match expected outputs exactly
7. [x] **6 integration tests PASS**: additive_quality independence, frozen invariants, carrageenan reclassification, budget cap, Stage 7 wiring
8. [x] **Score-drift analysis**: Frozen invariants (milk 85/A, snack bar ceiling, bread retail) unchanged; negative-only drift for products with agents
9. [x] **Implementation report**: `reports/ecs_v1_implementation_report.md` with PASS recommendation

## Changes

| File | Change |
|------|--------|
| `ingredient_taxonomy.py` | +115 lines: 13 new Identity entries |
| `signal_extractor.py` | +22 lines: new L3 signals + modified starch gate |
| `constants.py` | +17 lines: EMULSIFIER_COMPLEXITY block |
| `score_engine.py` | +83 lines: _emulsifier_complexity() + wiring |
| `run_ecs_regression.py` | NEW: 22-example regression harness |
| `run_ecs_integration.py` | NEW: 6 integration tests |
| `reports/ecs_v1_implementation_report.md` | NEW: implementation change report |

## Close reason

ECS-v1 implemented in ingredient_taxonomy.py, signal_extractor.py, constants.py, and score_engine.py.

- All 22 emulsifier_complexity regression examples pass.
- All 6 integration tests pass.
- Formula matches approved spec: final penalty = highest individual emulsifier penalty + complexity adjustment, capped at 8 points.
- No cap floor 55 is used.
- Modified starch gate uses ingredient position and light/diet signals.
- ECS is traceable through emulsifier_complexity_penalty, emulsifier_complexity_penalty_note, and emulsifier_complexity_detail.
- Frozen invariants remain unaffected.
- Score drift is zero for clean products and negative only for products with relevant emulsifier/stabilizer agents.

**Recommendation: PASS** — closed by owner.

### Archive note

ECS-v1 is a label-detectable emulsifier complexity proxy, not a true additive dose or exposure model. Do not describe it as "load," "dose," "unsafe," or "toxic."

### Follow-up backlog

Create a concern coordination review for additive_quality + ECS + fragmentation to ensure combined penalties remain proportionate across highly engineered products.

## Ancestry

Preceded by TASK-223 (ECS-v1 design + QA), TASK-222A (F1 identity deltas), EV-045 (evidence registration).
