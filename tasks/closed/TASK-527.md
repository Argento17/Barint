---
id: TASK-527
title: Investigate brined-cheeses 14 + milk 3 score==trace / ingredient-truncation mismatches on LIVE pages
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-08
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Diagnosis DoD met + orchestrator-verified 2026-07-09 (dispatched native-Sonnet Adversarial QA a0e1b21,
  READ-ONLY). Report: 03_operations/reports/qa/task527_live_mismatch_diagnosis_v1.md (sha256
  1f25d9450ab2b49b65089c7b5217beced88e247d4c0acb77c58f525f84569285). CLASSIFICATION (0 confirmed
  SCORE-AFFECTING): (1) BRINED 14 score-vs-trace mismatches = DISPLAY-ONLY — orchestrator independently
  confirmed the frontend _meta.reflow block documents TASK-438 with grade_movers exactly matching the 3
  grade changes (7290011499129 A->B, 7290108509106 A->B, 7290108509755 B->C); frontend JSON is post-reflow
  authoritative, the run_brined_005 traces are stale pre-reflow artifacts (delta -1.9..-2.2, single
  systematic adjustment). No ingredient truncations. (2) MILK 18/18 scores MATCH run_005_headpin
  (authoritative frozen baseline). 1 ingredient 'truncation' (7290019790259 trailing comma) = DISPLAY-ONLY
  scrape artifact (present identically in BSIP1 ingredients_raw; product is single-ingredient milk, complete).
  run_id traceability gap (task409_rederive_milk_20260626 has no trace dir) = DISPLAY-ONLY metadata.
  ROUTED FOLLOW-UPS: (a) M-003 rice drink 8000215204219 live=46.3/D vs owner-approved override 52.3/C
  (AUTHORITATIVE.md TASK-169C/180A) vs engine 49.4/D — orchestrator confirmed the live JSON shows 46.3/D,
  neither the override nor the engine value → override apparently lost in the task409 rebuild = TRIPWIRE-1,
  registered TASK-545 (BLOCKED, owner-gated, do NOT auto-fix). (b) 3 DISPLAY-ONLY hygiene items (brined
  stale-trace regen / milk trailing-comma BSIP1 hygiene / milk _meta.run_id alignment) → data-agent backlog,
  non-urgent. (c) 5 live banned-phrase copy rows (brined 4 = TASK-542; milk 1 NEW = 7290110325619) folded
  into the supervised copy-fix batch. Diagnosis changed nothing on disk beyond the report.
summary: >
  Surfaced incidentally by the validate_comparison_page.py --http instrument fix during TASK-515A: re-running the (now-fixed) go-live battery against LIVE brined_cheeses and milk pages found brined-cheeses has 14 score==trace mismatches and milk has 3 ingredient-truncation flags. Pre-existing, unrelated to yogurt or the instrument fix itself (confirmed the instrument fix only changed image-URL resolution, not score/ingredient logic). Need to determine: stale committed traces vs a real live-page drift. Not yet triaged for severity.
---

# TASK-527 — Investigate brined-cheeses 14 + milk 3 score==trace / ingredient-truncation mismatches on LIVE pages

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
