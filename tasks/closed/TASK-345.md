---
id: TASK-345
title: Phase 2+3 WS-Data: parsing-coverage audit of ingredients/nutrition/additives across all 10 live pages
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified. 02_products/_parsing_audit/dropdown_data_coverage_v1.md — 407 products
  / 10 pages audited, counts reconcile (20+25+21+57+28+36+65+119+18+18=407). Independently
  confirmed the decision-critical claims: OFF product-level = 0 (the 2 hits are
  _meta.excluded_off_products = OFF-ban compliance records, not display data); cereals sugar=None;
  rank/categoryTotal absent on products; juices d4_additives=0 (absent) vs cakes=66 (present);
  milk dataset = milk_frontend_v1.json. Real gaps cataloged: 5 malformed ingredients (4 cereals +
  1 granola, Shufersal disclaimer appended), 3 cereal ingredient-nulls, systematic sugar-null
  (cereals 20/granola 25/hard_cheeses 26), sodium-null (milk 18/juices 15), d4_additives field
  absent (milk 18 + juices 21), rank/categoryTotal absent (0/407), additive key mismatch
  (data name_he/function_he vs spec name/function → Frontend maps). → remediation TASK-347.
---

# TASK-345 — WS-Data parsing-coverage audit

CLOSED. Report → dropdown_data_coverage_v1.md. Fixes → TASK-347. Frontend (TASK-346) must map
additive keys name_he/function_he → name/function and handle absent d4_additives as [].
