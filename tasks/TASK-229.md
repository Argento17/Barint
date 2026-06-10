---
id: TASK-229
title: "Score-0 floor artifact — engine returns exactly 0/E for products lacking positive-driver signals (surfaced by salty-snacks v4 rebuild)"
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-228]
blocks: []
roadmap_impact: true
work_type: scoring-review
d7_cosign_required: true
tripwire: "#1 — touches scoring philosophy / score floor. Requires owner sign-off before any engine change ships."
---

# TASK-229 — Score-0 floor artifact

## Context

The real salty-snacks rebuild (TASK-228) surfaced 2 products that score **exactly 0/E** in the
current engine (`engine-baseline-2026-06-04` family, `BARI_RECAL_P0=on`):

1. **פיטנס קרקר דק סלק** — score **0/E**, confidence `verified`, NOVA 3.
   Nutrition (per 100g): energy 458, protein **12.1g**, fat 15.8, carbs 64.2, **fiber 6.5g**,
   sodium 400, sugar 8.8, sat-fat 1.9. Its own `positiveSignals` list "6.5g fiber" and "12.1g protein."
   **A decent-macro health cracker scoring an absolute 0/E is indefensible — almost certainly an
   engine floor artifact**, not a real verdict. Plausible real grade ≈ C.
2. **אפרופו קרמל** — score **0/E**, confidence `partial`, NOVA 2. 35g sugar, 31.5g fat, 13g sat-fat.
   Direction (E) is plausible, but the **literal 0** is the same floor artifact (a sugary/fatty
   snack should land low D/E, not a mathematical zero).

## Hypothesis

The engine produces a 0 when a product has no positive-driver signals to accumulate from (or the
recalibration floor clamps to 0), rather than computing a defensible low-but-nonzero score. This
makes any product without matched positive drivers collapse to 0/E regardless of decent macros.

## Scope (Nutrition Agent)

1. Read the score floor / aggregation in `03_operations/bsip2/proto_v0/src/score_engine.py`. Identify
   where/why a 0 is emitted. Determine if it's a missing-positive-driver path or a clamp.
2. Diagnose whether this is isolated to these 2 products or a general edge (scan all categories for
   any displayed score == 0).
3. Recommend the single best fix (do NOT implement an engine change without owner sign-off — tripwire #1):
   e.g. a defensible minimum-floor computation, or proper crediting of fiber/protein positive signals
   for the beet cracker. Confirm the fix does not move any other published score.
4. After owner sign-off: implement, rescore salty-snacks v4 (regenerate the affected entries only),
   confirm beet cracker lands at a defensible grade and Apropo lands D/E (not 0).

## Interim display guard (decide with orchestrator)

Until fixed, the live salty-snacks shelf should not show an obviously-wrong 0/E. Options: withhold
the 2 score-0 products from display (mark insufficient), or hold the v4 commit. Orchestrator to pick.

## Acceptance criteria

- [ ] Root cause of score==0 identified in `score_engine.py`
- [ ] Cross-category scan: any other displayed score==0?
- [ ] Recommended fix with no-collateral-score-move confirmation; owner sign-off obtained
- [ ] Beet cracker rescored to a defensible grade; Apropo D/E not 0; salty-snacks v4 updated
- [ ] D7 co-sign (Nutrition + Product) recorded
