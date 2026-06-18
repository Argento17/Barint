---
id: TASK-270
title: Generator confidence: archetype-aware required-fields (fiber-null not a gap for dairy)
owner: data-agent
status: BLOCKED
priority: MEDIUM
created_at: 2026-06-13
blocker: "Deferred by owner 2026-06-13 (chose page-first over all-categories). Ruling ready: 02_products/brined_cheeses/reports/confidence_archetype_ruling_v1.md. Fix generate_page.py build_confidence_fields() lines ~234-237 (core_nutrition_fields hardcodes dietary_fiber_g) via ARCHETYPE_EXPECTED_NULL map + per-category archetype config. MANDATORY cross-corpus confidence baseline diff before ship (rule 8); generic-archetype categories must show ZERO change; salty-snacks fiber-null is a REAL gap (must not move)."
depends_on: []
blocks: []
category_id: null
summary: >
  Systematic version of brined RT-H1. Confidence logic must recognize structurally-absent fields per archetype (fiber for dairy/meat/fat) so it stops false-flagging complete products as partial. Brined page already fixed locally (P54); this generalizes it to the factory.
---

# TASK-270 — Generator confidence: archetype-aware required-fields (fiber-null not a gap for dairy)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
