---
id: TASK-376
title: BSIP1 Victory mapper drops sugars_g -> null (inflated scores); add cross-retailer sugar regression guard
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-22
closed_at: 2026-06-22
depends_on: []
blocks: []
category_id: null
close_reason: >
  Fixed + orchestrator-verified. Root cause was NARROWER than the opening framing:
  not the Victory HTML parser, but a chocolate-specific builder script
  (02_products/chocolate/choc_task366b_write_final.py:125) that wrote the key
  "sugars_raw" (plural) where the canonical reader parse_nutrition_numeric reads
  "sugar_raw" (singular) -> sugars_g dropped to null. Fix: (1) root cause —
  renamed sugars_raw->sugar_raw in the builder; (2) defensive — bsip0_nutrition.py
  parse_nutrition_numeric now accepts both spellings (sugar_raw wins), preventing
  the whole class; (3) 2 regression tests added. VERIFIED by orchestrator: 33/33
  tests pass (ran it); builder fix present at :125; project-wide grep confirms NO
  other production builder emits "sugars_raw" (only the fix, the test, and the
  pre-existing _SUGAR_FIELD_VARIANTS coverage tuple) -> scope isolated, my
  "affects all Victory-sourced scoring across all categories" framing was an
  overstatement and the agent correctly narrowed it. Re-derived Lindt 70%
  sugars_g=30.0 (matches pass-1 Shufersal). NO published scores affected (Victory
  pass-2 was DATA_ONLY, never integrated; chocolate shipped on pass-1 Shufersal).
  FOLLOW-UP (logged, non-blocking): no dedicated "sugar null but carbs>X"
  plausibility guard — current filter_incomplete_nutrition (>=4/6) + nutrition_implausible
  both let a sugar-absent record through; a dedicated guard is a separate D6 proposal.
summary: >
  Victory/pass-2 BSIP1 canonical mapper silently nulls sugars_g, inflating scores (Lindt 70% bogus 61/C vs correct 28.7/E once raw label read; both retailers agree 30g). Surfaced in TASK-375 chocolate scrape. Affects any Victory-sourced scoring across all categories. Fix the mapper + add a regression test/plausibility guard.
---

# TASK-376 — BSIP1 Victory mapper drops sugars_g -> null (inflated scores); add cross-retailer sugar regression guard

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
