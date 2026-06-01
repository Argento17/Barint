---
id: TASK-133
title: Implement approved BSIP2 Evidence-Watch 2026-06-01 revisions (F2, F1, F4)
owner: nutrition-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Objective: ship the owner-approved scoring revisions from the 2026-06-01 Evidence Watch evaluation (TASK-132) - F2 protein-bar matrix discount, F1 emulsifier identity tiering, F4 BHA named-additive penalty. F3 deferred. Sub-tasks A-D; taxonomy-first sequencing.
---

# TASK-133 — Implement approved BSIP2 Evidence-Watch 2026-06-01 revisions (F2, F1, F4)

Plan of record: [TASK-133_implementation_roadmap.md](../research/TASK-133_implementation_roadmap.md).
Origin: [TASK-132 evaluation](../research/BSIP2_Evidence_Watch_20260601_EVALUATION.md). F3 deferred.

## Return block — 2026-06-01 (proposed RETURNED → Controller to record CLOSED)

All sub-tasks complete; Phase E passed. Report: [TASK-133BCD_validation_report.md](../research/TASK-133BCD_validation_report.md).

- **133A** taxonomy — CLOSED.
- **133B** F2 protein-quality matrix discount + collagen — RETURNED. ×0.80 reconstructed / ×0.55
  collagen, quality-only, bar-format + primary-position gated (gaming-resistant).
- **133C** F1 emulsifier identity tiering — RETURNED. Identity wired via taxonomy; deltas neutral
  (sprint1 already realizes the directions); no new caps; flat `Emulsifiers: −6` spec retired.
- **133D** F4 BHA named penalty — RETURNED. FDA gate PASSED; BHA −5, BHT differentiated; dormant in current corpora.
- **Phase E** — DEC-004 DECIDED (magnitudes ratified); version `0.4.0`; specs synced (incl.
  weight re-sync DEC-004 G3, matrix-integrity Req 1 marked implemented); **frontend rescore
  verified as a no-op** (0 displayed-product changes on every live page).

Validation: golden 11 PASS / 1 pre-existing WARN / 0 FAIL (no golden score changed); cross-corpora
464 products → 4 changed, 0 grade-flips; live pages unaffected.

**Separate finding (not TASK-133):** pre-existing maadanim engine drift (85/90 displayed products
differ from the published build, incl. one latent C→D), unrelated to this revision — recommend
QA/Product open a dedicated triage task. Do **not** fold into a TASK-133 rescore.

Awaiting Central Controller to record CLOSED.
