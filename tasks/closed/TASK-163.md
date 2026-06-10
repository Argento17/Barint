---
id: TASK-163
title: Add missing-data disclosure to yogurts/maadanim/cheese comparison pages
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — verified disclosure added: yogurts 10/11, maadanim 69/84, cheese 49/51, wording byte-identical to the shipped hummus/snacks/bread template. Derived via the existing shared scripts/lib/derive-unknowns.mjs (scoped runner normalize-corpus-unknowns-task163.mjs to avoid a pre-existing bread-id collision bug). Additive only — before/after snapshot shows 0 score/grade/nutrition changes across 128 products; every unknowns line re-derived from genuinely-null fields (0 invented)."
follow_ups: "JUDGMENT FLAG (owner): fiber is null on nearly all dairy (yogurt/cheese/maadanim rarely print it), so the fiber disclosure fired on ~61 maadanim + ~49 cheese — technically true but possibly noise. Sugar disclosure is clearly useful. Option to suppress the fiber-specific disclosure for dairy categories = an editorial policy change to the shared deriver (affects all 6 categories) — surfaced to owner, not changed unilaterally."
depends_on: []
blocks: []
category_id: null
summary: >
  yogurts/maadanim/cheese have products with missing nutrition values (e.g. sugar/fiber not on label) but no on-page note saying the info was unavailable. hummus/snacks/bread already show this. Add the same transparency disclosure (unknowns field) to the 3 categories. Most acute: yogurts (10 products). No score change.
---

# TASK-163 — Add missing-data disclosure to yogurts/maadanim/cheese comparison pages

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
