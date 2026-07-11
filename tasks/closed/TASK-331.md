---
id: TASK-331
title: v3 schema-assignment — cereals/hummus (and bread/cheese) gated on un-rendered milk-depth fields
owner: product-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "SUPERSEDED - TASK-564/569/574/581 schema overhaul (board-verified closes) removed the v3 deep-dive fields from production; scope obsolete. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: MEDIUM
created_at: 2026-06-18
depends_on: [TASK-330]
blocks: []
category_id: null
blocker: >
  Owner/Product decision needed — RE-SCOPED 2026-06-18 after the parallel-chat spine red-team landed+pushed
  (origin/master 6ceccabeb) AND a verified render-contract finding. Two upstream facts now collapse the original
  options: (1) RT-2 made run_gates' PENDING_COPY gate UNIVERSAL (fails for ALL schemas, not just v3) — so "assign
  v3 so G2 catches it" is moot; the gate catches PENDING regardless. (2) The v3 deep-dive fields
  (consumerExplanation.whyRated / bestUseCases / consumerTakeaway) are rendered by NO component — verified:
  buildConsumerExplanationView + ConsumerExplanationView in src/lib/comparisons/consumer-explanation-view.ts are
  exported but imported/called by nobody; no component in src/components or src/app references the fields. They are
  a dead data layer (the [[generator_render_contract_gap]]). => Option (A) "author v3 content for cereals/hummus"
  is DEAD = writing copy into a void. This is the same block hitting bread_frontend_v3.json + cheese_frontend_v4.json
  (parallel chat is handling those two files — DO NOT touch them).
summary: >
  RE-SCOPED 2026-06-18. The G2 fail on staged cereals/hummus is: schema_version=v3 (set globally at
  generate_page.py:61 SCHEMA_VERSION="v3") HARD-requires consumerExplanation.whyRated + bestUseCases per product,
  all PENDING_COPY. Row-level verdict coverage already passes (every product has insightLine or rowVerdict); the
  ONLY remaining fails are the v3 deep fields. With option (A) dead (fields render nowhere), the live fork is:
  (B) RECOMMENDED — make schema_version per-category (config-driven, not the generate_page.py:61 global) so only
      milk (the content gold standard, [[owner_milk_page_content_gold_standard]]) declares v3 milk-depth; cereals/
      hummus declare the standard schema and pass G2 without authoring dead copy. Reversible, config-level.
  (C) gate-side — stop hard-failing the v3 deep fields until a component renders them (warn-only). This is the
      parallel chat's run_gates.py domain (they own it post-RT-2) and a broader architecture call.
  CROSS-CUTTING DECISION for owner/Product (bigger than cereals/hummus): should the v3 deep-dive fields be GATED
  AT ALL while no component consumes them? Resolving the render-contract gap (wire the view OR drop the gate) is
  the real root cause and affects bread/cheese/cereals/hummus alike. TASK-331 itself recommends (B) for the two
  staged shelves; the render-contract call routes up. Implementation of (B) touches generate_page.py (NOT a
  forbidden spine file) but is entangled with the parallel chat's bread_v3/cheese_v4 work — coordinate before
  dispatch.
---

# TASK-331 — G2 COVERAGE: allow documented nutrition nulls (sugar) to PASS instead of requiring 100%

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
