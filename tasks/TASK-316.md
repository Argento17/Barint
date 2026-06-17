---
id: TASK-316
title: Spine step 1 — close the generator render-contract gap (generate_page emits the FULL frontend render contract → drop-in output)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: []
blocks: [TASK-317]
category_id: null
summary: >
  The #1 prerequisite for the score-switch spine. Today generate_page.py emits scoring + copy fields but NOT the full
  frontend RENDER contract — the display fields (glassBox, _product_type, novaGroup, sugarPer100ml/kcalPer100ml, _has_phvo,
  confidence_level, retailers/subPool, d3_processing_signal, d4_additives) come from the BESPOKE per-category builders
  (03_operations/bsip2/proto_v0/src/build_*_frontend*.py, batch_run_hummus_001.py). That gap forced an overlay-merge for this
  week's publish (TASK-310) and blocks a true "flip a switch" flow. Port that render-field logic into generate_page's
  config-driven extension mechanism (build_product + get_extension_field_value + extension_fields config), so the generic
  generator's output is DROP-IN for each category (an overlay-merge becomes a no-op). Scope to the 7 re-baselined categories
  first (cereals, cakes, cookies_coffee, granola, juices, brined_cheeses, hummus). HARD: additive OUTPUT fields only — ZERO
  change to score/grade (scores stay = trace.final_score_estimate); NO scoring/engine edits; OFF-ban absolute (derive only from
  direct-scrape corpus/trace, null if absent, never fabricate). Acceptance: re-run rescore_all per category → staging render
  fields MATCH the live page's render schema for unchanged products (drop-in parity), verified field-by-field. Staging-only.
---

# TASK-316 — Spine step 1: close the generator render-contract gap

See `tasks/prompts/P166_render_contract_gap.md`. Foundational for the spine ([[generator_render_contract_gap]]); blocks the
orchestration steps (a flag-flip can only auto-produce a deploy-ready page once generate_page output is drop-in).
