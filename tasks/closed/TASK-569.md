---
id: TASK-569
title: Generate page JSON schema from BariProductVM (kill schema lag class)
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-10
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. Dedicated ComparisonPageContract TS type (raw served-JSON shape,
  distinct from BariProductVM) + ts-json-schema-generator/ajv (MIT devDeps only) wired as
  generate-page-schema / diff-page-schema / validate-page-schema npm scripts. Orchestrator
  re-ran: 18/18 shelves PASS against the generated schema; validate_return.py --root
  C:/bari_wt_569 PASS; branch task569-vm-schema @ b382d9a6 confirmed pushed. Live schema NOT
  swapped (per spec: generate->diff->propose). 42 categorized diffs delivered in the return.
  Key finding INDEPENDENTLY CONFIRMED by orchestrator: hand schema types
  limitingFactors[].magnitude as string while chocolate_bars/chocolate_tablets/snacks emit
  ints - G1's checker validates property presence not value types, which is why gates never
  caught it. Adoption + diff review + magnitude fix + regen-diff CI step registered as
  TASK-581. PR pending owner merge.

summary: >
  Owner-approved 2026-07-10. page_output_schema_v1.json is hand-maintained and lagged an owner-approved copy change (TASK-564 false alarms). Generate the schema from the TS view-model at build time (free OSS tooling only), diff against current schema, adopt after review. TASK-564's manual fix lands first; this prevents recurrence.
---

# TASK-569 — Generate page JSON schema from BariProductVM (kill schema lag class)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
