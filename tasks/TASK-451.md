---
id: TASK-451
title: Wire dormant evidence clients (PubChem/DSLD/USDA/literature/openFDA/...) into citation + Red-Team + additive gates
owner: research-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-447 found ~10 authoritative external clients built + self-test-green but wired into ZERO production stages (literature, pubchem, dsld, usda_fdc, food_additives, semantic_scholar, crossref, biorxiv, openfda, tzameret). Largest dormant already-paid-for capability — meant to back Red-Team/citation gates + additive-identity. Step 1 = scoping/design pass (Plan agent, read-only): map each client -> gate/stage, how it composes with existing verify_citations.py (C0) + citation_fabrication_gate, effort, recommended first 2-3 to wire. Then execute per plan. NOTE: tzameret DIRECTIONAL-ONLY (never authoritative).
---

# TASK-451 — Wire dormant evidence clients (PubChem/DSLD/USDA/literature/openFDA/...) into citation + Red-Team + additive gates

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
