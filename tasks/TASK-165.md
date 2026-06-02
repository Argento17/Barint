---
id: TASK-165
title: Vegetable-spreads: give the protein bar a proper scale so bars aren't flat
owner: frontend-agent
status: CLOSED
priority: LOW
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — verified VEGETABLE_SPREADS_METRIC_SPECS=[VEG_PROTEIN_METRIC] in veg page. New VEG_PROTEIN_METRIC spec (scaleMax 7, good 3, poor 1, aria per-100g) tuned to the measured 0.7-6.3g range so bars discriminate instead of collapsing on the 0-20 hummus scale. PROTEIN_METRIC + DAIRY_PROTEIN_METRIC untouched (other categories unaffected). Display-only, no scores. tsc/build/corpus-validate exit 0."
depends_on: []
blocks: []
category_id: null
summary: >
  Veg-spreads reuse hummus PROTEIN_METRIC (scale 0-20) but their protein is 0.7-6.3g, so every bar looks tiny/flat. Add a veg-tuned protein spec (lower scaleMax, per-100g aria already correct). Display-only.
---

# TASK-165 — Vegetable-spreads: give the protein bar a proper scale so bars aren't flat

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
