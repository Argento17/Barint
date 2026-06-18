---
id: TASK-325
title: Additive burden aggregate INDEX method (rollup of EV-002/003/019 from traces), representation-only NO new penalty
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  P176/C1-GROK delivered + ORCHESTRATOR-VERIFIED. method_additive_burden.py (standalone) rolls EXISTING
  trace signals EV-002 (tax_named_concern_additives), EV-003 (sprint1_high_risk/neutral_emulsifier_found),
  EV-019 (sprint1_prebiotic_gum_found) into one burden index/band. Counts reconciled independently: 935
  traces processed / 37 index_null (OFF-sourced excluded) / 898 computed; bands HIGH 40 + MED 280 + LOW 4
  + NONE 574 = 898. Criterion (d) FAITHFUL-ROLLUP VERIFIED against the real trace for barcode 2472148
  (cakes): trace tax_named_concern_additives=['carrageenan','cmc','soy_lecithin'], high_risk=['E466','E407'],
  neutral=['E322'] match the index payload exactly; index 13.0 = 3x3 + 2x2 (no re-derivation). SCOPE GUARD
  VERIFIED: git diff on score_engine/constants/configs/bari-web = EMPTY. Inert ADDITIVE_BURDEN_* weights;
  no penalty, no score feedback.
  ⚠️ ORCHESTRATOR FINDING for the later D6/D7 step (return did not surface it): the weighting DOUBLE-COUNTS
  emulsifiers that are also at-risk additives — CMC/E466 and carrageenan/E407 score once as EV-002 at-risk
  (x3) AND again as EV-003 high-risk emulsifier (x2). Harmless for a representation-only index, but if this
  ever informs display/activation the double-weight must be reconciled. Activation out of scope.
  Not committed, not pushed.
depends_on: [TASK-322]
blocks: []
category_id: null
summary: >
  Build a standalone method that rolls the existing per-signal additive findings (EV-002 at-risk count, EV-003 emulsifier tier, EV-019 prebiotic exemption) read from BSIP2 traces into a single displayable 'additive burden' aggregate index. Representation/explanation only: introduces no new penalty, moves no published score, edits no live scoring path.
---

# TASK-325 — Additive burden aggregate INDEX method (rollup of EV-002/003/019 from traces), representation-only NO new penalty

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
