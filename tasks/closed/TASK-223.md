---
id: TASK-223
title: ECS-v1 (emulsifier complexity score) — design + QA
status: CLOSED
owner: Nutrition Agent (Scoring Governance Lead)
created: 2026-06-10
closed: 2026-06-10
evidence_registry: EV-045
engine_component: bsip2 proto_v0
reconstructed: >
  RECONSTRUCTED 2026-06-10. The original tasks/closed/TASK-223.md (untracked, never committed)
  was accidentally overwritten during a parallel session's id-collision (a second task was drafted
  as 223 before checking tasks/closed/, then renumbered to TASK-226). This record is rebuilt
  faithfully from the surviving ECS-v1 artifacts and the TASK-224/225 cross-references; wording is
  reconstructed, not the byte-original. If the byte-original surfaces (e.g. from a machine backup),
  prefer it over this file.
produced_artifacts:
  - 01_framework/bsip2_framework/docs/scoring/emulsifier_complexity_spec_v1.md   # ECS-v1 design spec
  - 01_framework/bsip2_framework/validation/emulsifier_complexity_regression_v1.md  # 22-example regression set
preceded: [TASK-222A]   # F1 additive identity deltas
followed_by: [TASK-224, TASK-225]   # ECS-v1 implementation; concern-coordination review
---

## Scope

Design and QA the **Emulsifier Complexity Score (ECS-v1)** for the BSIP2 engine — a new
signal measuring the *aggregate burden* of texture-stabilizing additives, distinct from the
per-agent `ADDITIVE_IDENTITY_DELTAS` (F1 / TASK-222A) which penalise individual high-concern
emulsifiers by name. ECS-v1 captures what identity deltas miss: medium-concern agents
(mono/diglycerides, modified starches), low/contextual agents (guar/xanthan/acacia/locust-bean
gums, pectin, lecithin), and the compounding effect of multiple distinct agents acting together.

Naming locked to `emulsifier_complexity_score` (NOT `emulsifier_load_score`) — "load" is
reserved until serving-level concentration is label-observable on Israeli retail labels.

## Deliverables

- [x] `emulsifier_complexity_spec_v1.md` (Document ID ECS-v1, EV-045) — methodology spec: agent
      tiers, complexity aggregation, label-observability constraint, score bounds
- [x] `emulsifier_complexity_regression_v1.md` — 22 regression examples covering the agent tiers
      and multi-agent compounding
- [x] Evidence registered under EV-045 in the BSIP2 evidence registry
- [x] QA: design reviewed against label-observability rule and frozen-invariant safety (no change
      to published scores at design stage — implementation deferred to TASK-224)

## Standards compliance

- Label-observability: score uses only additives nameable from the ingredient list (no inferred
  concentration) — confirmed in spec §1.
- Frozen invariants: design stage is non-activating; activation + drift-check owned by TASK-224
  (which confirmed 22/22 regression + 6/6 integration pass, frozen invariants unaffected).
- Naming governance: `emulsifier_complexity_score` adopted; `_load_` deferred.

## Close

Design spec + regression set delivered and registered (EV-045); handed to TASK-224 for engine
implementation. Implementation report (`ecs_v1_implementation_report.md`) later confirmed PASS.
