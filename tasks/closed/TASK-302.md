---
id: TASK-302
title: RT-1 floor ruling — is whole_food_fat_nova1_2 floor appropriate lifting a 57 snack to the 70/B ceiling?
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Nutrition D6 ruling delivered + orchestrator-verified. VERDICT: NARROW-THE-FLOOR. Verified code WHOLE_FOOD_FAT_FLOOR=70
  (constants.py:841) vs SRC-v1 spec=65 (score_resolution_contract.md:91,483) — value/spec divergence (possible governance
  trail in recalibration_proposals.md / nutrition_rulings_registry, NOT the EV registry). Confirmed Anti-Immunity: floor
  lifts data-incomplete snack 7290011498870 (pre-floor 57.38, missing fiber+sodium) to the 70/B category ceiling. Proposed
  fix (D6 PROPOSAL, NOT applied): Part A restore floor 70->65; Part B data-completeness gate (no floor when key fields missing).
  Blast radius: 2 staging snack products; 109 butter + 9 non-butter ARCHIVED traces (butter WIPED = no live impact). Implementation
  = separate governed task: EV-### + Product D7 + owner (frozen-invariant-adjacent, snack ceiling). Ruling only; no engine edit.
depends_on: [TASK-299]
blocks: []
category_id: null
summary: >
  Nutrition D6 ruling (Product D7 co-sign) on Red-Team RT-1: snacks 7290011498870 computes 57.38 then the whole_food_fat_nova1_2 floor lifts it to exactly 70/B (category ceiling) on a 3-ingredient date+almond bar with missing fiber+sodium. Is the floor appropriate at this calorie density / data-completeness, or is it over-correcting (Anti-Immunity)? Ruling only — no engine edit; if it should change, that's a separate governed (EV+D7) engine task. Output: SOUND / NARROW-THE-FLOOR / other, with rationale.
---

# TASK-302 — RT-1 floor ruling — is whole_food_fat_nova1_2 floor appropriate lifting a 57 snack to the 70/B ceiling?

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
