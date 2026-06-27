---
id: TASK-409
title: Clean+traceable corpus: re-derive live categories on clean corpus, persist provenance, two-gate copy on grade-movers, validate, stage deploy
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
closed_at: 2026-06-27
close_reason: >
  DEPLOYED to origin/master via 97400f8d5 (integrate; chain 1440468ba → 120ff8f0c →
  ebc447dab → 3a833c564 → 5f2e611db → 338668d50 → 8e2edc45c). Clean+traceable
  re-derive across 12 categories: 7 served frontends changed, cleaned bsip1 corpus +
  provenance persisted, engine untouched, OFF=0. 13 grade-movers (all upgrades incl
  bread A→S) through Content+Adversarial-QA two-gate (0 CRIT/HIGH/MED), 5 empty-ingredient
  cheese discards (53→48). Combined regression with TASK-410 PASSED before the owner-authorized
  train-run deploy. Open SUB-ITEMS handed off (NOT blockers on this task): snacks re-derive
  → shipped separately as TASK-413 (origin/master 8761cf863); hard_cheeses governed sat-fat
  port → TASK-412 (owner decision pending, tripwire-1). Score moves owner-authorized
  (tripwire-1 lifted for corpus traceability program).
depends_on: []
blocks: []
category_id: null
summary: >
  Steps 2-5 of the corpus traceability program. Owner authorized all score movements (tripwire-1 lifted). Commit TASK-405 clean, re-derive each live category on the corrected+clean corpus so published==reproduce by construction, two-gate copy only on grade-movers, validate score==trace+OFF=0, stage for deploy. Step 1 (binding/harness fixes for snacks+hard_cheeses) handed to de-chain chat. protein_bars rebind included.
---

# TASK-409 — Clean+traceable corpus: re-derive live categories on clean corpus, persist provenance, two-gate copy on grade-movers, validate, stage deploy

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
