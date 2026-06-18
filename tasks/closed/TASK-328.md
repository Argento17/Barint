---
id: TASK-328
title: Parser identity additions: E903/E492/E553b/E525/E327 (no-score, identity table only)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
depends_on: []
blocks: []
category_id: null
close_reason: >
  P208 (C1-GROK) verified by orchestrator. 6 identities added to ingredient_taxonomy.py ONLY (+72; git
  diff --stat confirms no other src file). All 6 resolve correctly (E903 carnauba/glazing_benign, E492
  sorbitan/emulsifier_low_structural, E553b talc/anti_caking_benign, E525 KOH/acidity_regulator_benign,
  E327 calcium_lactate, E326 potassium_lactate) and E327≠E326 distinct (verified live). ZERO scoring delta
  PROVEN structurally: (1) grep = 0 references to the 5 new class strings in score_engine/constants/
  signal_extractor; (2) the consumer at signal_extractor.py:966-973 matches additive_class by exact ==, so
  emulsifier_low_structural ≠ emulsifier_low never enters any tax_emulsifier_* list → no F1/ECS delta. Holds
  for ALL products, not one sample. Selftest ALL PASS exit 0 (earlier crash = cp1252 console encoding only).
  additive_marker_count is pattern-driven, untouched. OFF-ban honored. No flag, no spine needed (display-only
  enrichment); no deploy. Return contract present.
summary: >
  Add named-additive identities to ingredient_taxonomy.py ONLY (resolution/explanation layer): E903 carnauba, E492 sorbitan tristearate, E553b talc, E525 potassium hydroxide, E327 calcium lactate (with E327!=E326 potassium lactate fix) + Hebrew aliases. NO signal_extractor category patterns (those move additive_count = score = spine). Score-neutral; verify scoring diff EMPTY.
---

# TASK-328 — Parser identity additions: E903/E492/E553b/E525/E327 (no-score, identity table only)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
