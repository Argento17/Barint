---
id: TASK-272
title: Missing-data secondary-retailer rule (Yohananof/Victory else remove) + apply to brined 15
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
closed_at: 2026-06-13
depends_on: []
blocks: []
category_id: null
close_reason: >
  Owner SIMPLIFIED the rule mid-flight (2026-06-13): "I don't want it to take so much resources. You don't find it one shot, you discard the products." The Data agent had started building an elaborate Yohananof/Victory + BSIP1/BSIP2 re-score pipeline (only 1 of ~12 products recoverable) — exactly the resource sink to avoid; stopped it (TaskStop). Applied the simplified rule directly: discarded the 12 brined products with NO ingredient list from brined_cheeses_frontend_v2.json (verified by orchestrator: 48→36, parse OK, no hardcoded refs to removed ids in lib/components/app, grade dist 9A/20B/5C/2D). Rule codified in memory missing_data_discard_rule.md. No re-scoring, no OFF. Removed ids: bc-019/020/021/022/023/026/033/034/040/042/045/046.
summary: >
  Owner directive 2026-06-13: never score-punish a product for a primary-scrape data gap. SIMPLIFIED to: one-shot recovery at most, else DISCARD (no elaborate re-sourcing). Applied to brined: 12 ingredient-less products removed → 36 remain.
---

# TASK-272 — Missing-data: discard products without one-shot data (simplified per owner)

Discarded 12 ingredient-less brined products (48→36). Rule (one-shot-else-discard, never punish, never over-invest) codified in memory `missing_data_discard_rule.md`. Corpus locked at 36, dist 9A/20B/5C/2D.
