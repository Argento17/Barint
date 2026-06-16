---
id: TASK-233F
title: "Full migration of the remaining 10 category generators to the shared packaging core"
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-06-10
depends_on: [TASK-233B]
blocks: []
roadmap_impact: false
work_type: pipeline-refactor
---

# TASK-233F — Finish migrating generators to `frontend_core.py`

TASK-233B built the shared core and proved it on frozen_vegetables + salty_snacks_v4. The
remaining live-category generators still hand-roll grade/confidence/strip/image/copy and rely on
the runtime corpus.ts gate (TASK-233A) + `run_confidence_annotation_pass.py` as a backstop. This
task migrates them at the source so the backstop becomes belt-and-suspenders, not load-bearing.

## Scope
- Migrate generators for: bread, cereals, granola, hummus, juices, maadanim, olive_oil,
  hard_cheeses, snacks, butter (and complete the yogurt_cheese re-run, which 233B deferred to
  avoid regressing hand-patched `_cluster` — re-establish those clusters first).
- Each migration: grade via `grade_from_score`, confidence via `derive_from_trace`, canonical
  tooltip, `strip_non_vm_fields`, `select_image_url`.
- **Forward-fix from TASK-233C:** route per-product copy through the editorial banned-term /
  anti-redundancy filter at the generator write path, so future regenerations cannot re-introduce
  `NN/X` literals or rescore narration.
- Each re-run must report grade/confidence/score deltas and pass the validation gate (TASK-233A);
  no scoring methodology change.

## ⚠️ Nutrition pre-migration caveat (EV-027 — from the TASK-233B co-sign, MUST honor)
The "unknowns → partial" confidence rule is correct for frozen vegetables (its gaps are real label
omissions) but **must NOT be applied as a blanket rule** to categories where a "missing" nutrient is
structurally N/A. The deriver's `_missing_field_set` treats any null in SECONDARY_FIELDS
(`dietary_fiber_g, sugars_g, fat_saturated_g, sodium_mg`) as missing → demotes to partial.
- **Must-fix before migrating dairy / milk / plain yogurt / butter:** fiber is not applicable to
  dairy (EV-027). A null fiber there is N/A, not a gap — a complete whole-milk/natural-yogurt panel
  would be wrongly downgraded to partial. Either pre-populate fiber as 0/N-A in the trace or add a
  per-structural-class exemption in `_missing_field_set`. **Do not let a blanket rule ship over EV-027.**
- **Watch-list (verify per category):** `sugars_g` on savory/sodium-free items; `fat_saturated_g`
  on genuinely fat-free products — distinguish "blank because zero/N-A" from "blank because the
  label omitted a real value."

## ⚠️ LIVE defects found in the 2026-06-10 post-implementation verification (fix these FIRST)
1. **snacks confidence inflation — LIVE, consumer-visible.** `snacks_frontend_v2.json` ships 4
   products as `confidence: verified` ("based on full data") while their `unknowns` says the entire
   nutrition panel (energy/protein/sugar/fat/fiber/sodium) was unavailable: **snk-003, snk-007,
   snk-009, snk-020.** Root cause = DA-013: `confidence_annotation.annotate_fallback` preserves the
   generator's inflated `verified` when a product does not join a trace. snacks IS in the
   annotation-pass LIVE_FILES yet these survived → the fallback must re-derive, not trust. Same bug
   class as frozen-veg, still live on snacks. **Highest priority.**
2. **On-disk grade drift (not consumer-visible — runtime corrects it):** granola 1, hummus 3,
   maadanim 2. Confirms these generators are unmigrated; fixed when they adopt `frontend_core`.
3. **Stale annotation-pass config:** `run_confidence_annotation_pass.py` LIVE_FILES lists
   `salty_snacks_v3` + `olive_oil_v1` (both NOT shipped) and omits the live `salty_snacks_v4`.
4. **Dead-but-leaky files in the shipped data dir (not imported, but landmines):**
   `olive_oil_frontend_v1.json` (11 NN/X + 11 banned terms + leak keys), `crackers_staged_v1.json`,
   `salty_snacks_frontend_v2.json`, `salty_snacks_frontend_v3.json`. Delete or move out of
   `src/data/comparisons/` so a future wire-up or bulk pass cannot ship them.

## DoD
- [ ] All remaining generators call `frontend_core.py`; no bespoke grade/confidence/strip/image fns left
- [ ] Copy write-path runs the banned-term + anti-redundancy filter
- [ ] yogurt_cheese full re-run completed without `_cluster`/lens regression
- [ ] **EV-027 caveat honored** — no dairy/butter/yogurt product downgraded to partial for a
      structurally-N/A nutrient (Nutrition confirms before those categories ship)
- [ ] All deltas reported; validation gate green; no methodology change
