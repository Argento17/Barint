---
id: TASK-133A
title: Named-additive + ingredient-fragmentation taxonomy (matrix Req 1) - enabling infra
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
depends_on: []
blocks: []
category_id: null
summary: >
  Build the ingredient taxonomy with fragmentation level + named-additive identity metadata that matrix_integrity_framework.md Req 1 specifies. Enabling infra for F2/F1/F4: lets the scorer distinguish ingredient FORM (oats vs oat isolate; carrageenan/CMC vs lecithin; native vs modified starch) and named additives. Build once; F2/F1/F4 all ride on it.
---

# TASK-133A — Named-additive + ingredient-fragmentation taxonomy (matrix Req 1) - enabling infra

## Plan of record — Phase A (enabling gate)

Roadmap: [TASK-133_implementation_roadmap.md](../research/TASK-133_implementation_roadmap.md) §Phase A.

**Goal:** give the engine ingredient *identity* + *form*, not just class (matrix_integrity_framework Req 1).

- **Code:** new `ingredient_taxonomy.py` (name/synonyms → E-number, additive_class, fragmentation_level,
  is_named_concern); extend `extracted_additives` / `extracted_matrix_markers` extraction to emit
  identity. `matrix_integrity.py` already has the consumption hooks.
- **Must cover:** carrageenan (E407), CMC (E466), soy lecithin (E322), native vs. modified starch,
  BHA (E320), BHT; fragmentation levels intact / mechanical / fractional / reconstructed.
- **Constraints:** NOVA-independence (Req 2); primary-ingredient weighting (Req 3 — `_pos_weight` exists);
  gaming resistance (Req 5 — 5% whole-food garnish cannot claim the halo).
- **DoD:** resolves every additive referenced by 133B/C/D; extraction unit-tested on golden-product
  ingredient lists; `run_matrix_validation_v2.py` green. Size: L.
