---
id: TASK-310
title: Assemble — overlay-merge the 7 re-baselined staging pages into bari-web live JSONs (clean category scope), build + render-verify
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
depends_on: [TASK-308, TASK-309]
blocks: []
category_id: null
close_reason: >
  P163/Frontend Agent, orchestrator-verified against artifacts (agent's spot-checks UPGRADED to full checks). VERIFIED:
  FULL page-score==staging-score AND grade across ALL 7 pages, every product, 0 mismatches, 0 not-in-staging (cereals 20,
  cakes 65, cookies 119, granola 25, juices 21, brined 36, hummus 57). Clean-category-scope applied: granola muesli→granola
  7/7, hummus dips-only (7 dropped), cookies +1, juices +tomato & the 3 plant-milk/coffee dropped + added to juices config
  exclusions (now 11). Render fields PRESERVED via overlay-merge: hummus glassBox 57/57 + d3 57/57 + _product_type lenses
  intact (matbucha10/eggplant7/pepper5/hummus_spread33/masabacha2 → /vegetable-spreads safe), cakes novaGroup 65/65, juices
  kcalPer100ml 21/21. OFF=0 in ALL product objects (token hits are _meta text documenting the OFF exclusion — affirms the ban,
  not data). PENDING only cookies_coffee 392 (live-parity). All 7 sorted desc by score; _meta.product_count==array on all 7.
  Build exit 0, tsc 0 errors, 33/33 routes incl /hashvaot/vegetable-spreads. Milk untouched; no snack-bar A. Agent's flagged
  "out-of-spec hummus config +12" = MISREPORT (file is byte-identical to P161's 12-exclusion state; no actual change). NOTE for
  red-team: granola net-new 7290011131968 raw bsip2_trace=38.3 vs published 46.6 = by-design shelf-relative re-baseline; the
  authoritative score==trace reference is the staging rescored score (page==staging verified). Repo-side/reversible; NOT pushed.
summary: >
  Assemble the re-baseline into bari-web via in-place OVERLAY-MERGE (not file-swap): for products in both, keep the live
  product's render/display fields (glassBox, _product_type, novaGroup, sugarPer100ml, kcalPer100ml, _has_phvo, confidence_level,
  retailers/subPool, d3_processing_signal) and overlay ONLY the staging score/grade + live-schema copy fields. Apply owner's
  clean-category-scope ruling: keep granola muesli→granola swap (drop 7 muesli, add 7 granola) + hummus prepared-dips-only
  (drop 7 chickpea/empty), but DROP the 3 plant-milk/iced-coffee from juices (keep tomato juice) and add those 3 to the juices
  config exclusions. Build the 9 genuine net-new (granola 7, cookies 1, juices tomato 1) to the live schema, deriving render
  fields from their staging traces. Update _meta (counts/grade_distribution/run_id/generated). Sort products by score desc.
  tsc + npm run build green; verify all 7 /hashvaot routes + /vegetable-spreads (shares hummus JSON) render; score==trace, OFF=0.
  Repo-side + reversible (git); NO push/deploy. Then → red-team gate (TASK-311).
---

# TASK-310 — Assemble (overlay-merge) the 7 re-baselined pages into bari-web

See `tasks/prompts/P163_assemble_overlay_merge.md`. Owner ruling 2026-06-17: clean category scope (drop juices plant-milks/coffee).
