---
id: TASK-331
title: G2 COVERAGE blocker — staged cereals/hummus fail v3 milk-depth content reqs (PENDING_COPY)
owner: product-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-18
depends_on: [TASK-330]
blocks: []
category_id: null
blocker: Owner decision needed — corrected diagnosis (see summary); orig sugar-null scope was an orchestrator misread of INFO lines.
summary: >
  CORRECTION (2026-06-18): the original sugar-null framing was WRONG — sugar coverage (19/20, 55/57) is a g.info
  line, NOT a fail. The REAL G2 fail is: staged cereals/hummus pages carry schema_version=v3 (the milk-depth
  content model), which HARD-requires consumerExplanation.whyRated + bestUseCases per product — and those are all
  PENDING_COPY (unauthored). FAIL lines: 'v3 consumerExplanation.whyRated: 20/20 (57/57) PENDING_COPY' +
  'v3 bestUseCases: 20/20 (57/57) PENDING_COPY'. This is a CONTENT/schema-assignment question, not a missing-data
  nulls policy. Options: (A) author the v3 milk-depth content for these shelves (Content/Sonnet, heavy); (B) these
  categories should NOT be schema-v3 milk-depth — fix the schema_version assignment so they use the standard schema
  (milk is the content gold standard, not cereals/hummus — [[owner_milk_page_content_gold_standard]]); (C) make v3
  milk-depth content non-hard-fail (warn) for non-milk categories. Owner ruling needed before dispatch. The prior
  'allow documented nulls' ruling addressed the wrong problem.
---

# TASK-331 — G2 COVERAGE: allow documented nutrition nulls (sugar) to PASS instead of requiring 100%

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
