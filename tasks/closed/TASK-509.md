---
id: TASK-509
title: Dormant category nutrition-config on bread/cheese/crackers/milk expansions (DEFAULT vs category scales)
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-04
closed_at: 2026-07-05
close_reason: >
  Analysis deliverable complete + orchestrator-verified (2026-07-05 unattended run). Memo:
  03_operations/reports/nutrition/task509_expansion_config_recommendation_v1.md (C0 PASS exit 0).
  Verdict: DEFAULT rendering is a latent display bug on all 4 pages, not intended behavior.
  Orchestrator independently confirmed the load-bearing claims against
  bari-web/src/components/shared/expansion-section.tsx: cheese protein.goodAbove=20 (line ~138) vs
  DEFAULT 8 (line ~194) → fresh-cheese protein flips green→grey; crackers config ABSENT from
  CATEGORY_NUTRITION; milk config servingLabel "ל-100 מ״ל" (line ~93) + no "milk-comparison" alias
  in CATEGORY_NUTRITION_ALIASES; all 4 comparison-page components pass category= zero times (grep -c = 0).
  Recommendation carries a within-lane tradeoff (activate configs) → spun off as TASK-511 (Nutrition+Product
  D7 co-sign on the NEW crackers config + Design render re-verify; own PR, never piggybacked). No published
  score affected — display/threshold only.
depends_on: []
blocks: []
category_id: null
summary: >
  TASK-507 QA discovered bread/cheese/crackers/milk comparison pages pass NO category to the product table, so their expansion nutrition bars use DEFAULT_NUTRITION scales/thresholds, NOT the category-specific configs already present in expansion-section.tsx (bread:106, cheese:137). Also milk config keyed 'milk' has no 'milk-comparison' alias, so it is unreachable (QA MEDIUM-4). Nutrition question: are the category-specific scales the correct intended behavior (making current DEFAULT a latent display bug), or is DEFAULT correct for these pages? If category scales SHOULD be active, that is an intended improvement needing Nutrition sign-off + Design re-verify as its OWN change, never via a nav PR. TASK-507 itself will decouple to PRESERVE current DEFAULT behavior (reversible, zero consumer change). Display/threshold question only — no published-score change.
---

# TASK-509 — Dormant category nutrition-config on bread/cheese/crackers/milk expansions (DEFAULT vs category scales)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
