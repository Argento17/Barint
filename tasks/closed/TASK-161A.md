---
id: TASK-161A
title: Headline metric per comparison category (bread protein-vs-fiber; snacks has no protein)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — metric decisions verified vs live JSON + VM contract. protein bar for cheese/yogurts/vegetable-spreads/bread (protein present on all rows; PROTEIN_METRIC wired). snacks = NO metric bar (all 6 nutrition fields null on all 18 rows — a bar would be fabricated; rowReason-only is honest). milk left as-is. Two refinements carved off as follow-ups (NOT blockers), folded into 161C as notes: (1) bread fiber is the better headline but fiber_g is not wired — ship protein now, switch later; (2) cheese/yogurts protein bars sit low on the hummus-tuned scale (max 20) — want a dairy-style preset to discriminate."
depends_on: []
blocks: []
category_id: null
summary: >
  Decide the front-of-row metric bar for each category to match hummus's protein headline: confirm protein for cheese/yogurts/veg-spreads/milk; rule bread (protein vs fiber); resolve snacks (protein=0 in data -> alternative metric or no bar).
---

# TASK-161A — Headline metric per comparison category (bread protein-vs-fiber; snacks has no protein)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
