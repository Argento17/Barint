---
id: TASK-633
title: Author 10 grade-changed copy rows (629 re-score) — owner-released from freeze; Content + Adversarial QA two-gate
owner: content-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-629
lesson_trigger: none
close_reason: >
  VERIFIED + staged, committed 369e990a. The two-gate operated exactly as designed and closed pre-ship.
  Content (fable) authored 10 Hebrew rows (6 bread + 4 crackers) for the 629 grade changes; Adversarial QA
  (opus) red-teamed against ingredients_raw/d4_additives/expansion.nutrition and flagged 3 defensibility
  holes on first pass -- a false purity claim (3268429 'only flour' erased the soy flour), an unsupported
  saturated-fat claim (7290011489595 has no sat-fat field, only generic vegetable fat), and a partial-list
  enumeration (8434165658523 said 'short list' of 6 while the real list is 8). Content revised the 3 (+ an
  optional keto softening) and self-caught a new X-not-Y antithesis it introduced; the re-gate returned
  SIGN-OFF, all 10 clean, 0 new defects. Orchestrator staged the 10 signed-off insightLine/rowVerdict pairs
  into bread_frontend_v4.json + crackers_frontend_v1.json; semantic diff confirms ONLY those 20 fields on
  the 10 barcodes changed, 0 PENDING_COPY remain, no cited nutrient values. These overclaim classes are the
  already-codified [[cleanliness_claims_need_full_additive_list]] and [[false_inference_hides_in_bridges]]
  memories -- no new lesson. Consumer deploy = owner merge (two-speed). Data-hygiene note routed to Data:
  8434165658523 ingredients_raw says E223 while d4_additives says E224 (copy uses generic 'סולפיט', unaffected).
summary: >
  Author + two-gate the 10 grade-changed copy rows from the 629 re-score; owner-released from the freeze.
---

# TASK-633 — 10 grade-changed copy rows (two-gate)

Content authored + Adversarial QA SIGN-OFF; 10 rows staged. Two-gate caught+resolved 3 overclaims pre-ship. See close_reason.
