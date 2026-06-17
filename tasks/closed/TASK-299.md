---
id: TASK-299
title: Canonical re-baseline review gate — Nutrition methodology + Red-Team challenge of the 9-shelf delta report before owner deploy
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  Both reviews returned + orchestrator-verified against artifacts. CONVERGED VERDICT: deploy = NO-GO (3 CRITICAL,
  all orchestrator-confirmed). Nutrition = CONDITIONAL GO (8/9 sound, hard_cheeses hold for EV-099 D7 + 2 OFF) but
  MISSED the data-integrity defects on non-mover products. Red-Team caught + I verified: (RT-2 CRITICAL) 5 displayed
  granola products carry impossible sodium 6000-10000mg/100g in current BSIP1 — live page has sodium=None for them, so
  the re-baseline would REGRESS them B→C on corrupt data (verified: live grades B/B/B/C/C → rebaseline C/C/C/C/C);
  (RT-3 CRITICAL) hummus 7296073705505 scores A/80.9 conf=90 on an ingredient field that is the scraped nutrition-panel
  text (4 load_errors) — not on live page, re-baseline would INTRODUCE the bogus A; (RT-1 CRITICAL) snacks 7290011498870
  floored 57.38→70/B via whole_food_fat_nova1_2 (grade via floor not nutrition — Anti-Immunity Q). Frozen invariants HOLD
  (milk Δ0 180 checks, snacks no-A max 70/B, hummus 577480 C→E = valid RT-3-prior fix). 5 shelves CLEAN (cereals, juices,
  cakes, cookies_coffee, brined). Root cause of CRITICALs = corrupt/garbage BSIP1 SOURCE data the re-baseline exposed, NOT a
  trigger bug. Remediation routes: Data (fix granola sodium + hummus ingredient record), QA (add sodium>5000 sanity gate),
  Nutrition+Product (RT-1 floor ruling), then re-run trigger (~11s) + re-gate. HIGH/MED: RT-4 misleading explanation_drivers,
  RT-8 snacks 5 missing images, RT-11 35 new snack products need copy. Trigger itself = sound + committed (c3b1f42e0). No deploy.
depends_on: [TASK-298]
blocks: []
category_id: null
summary: >
  Two independent reviews of _rescore_staging/rebaseline_delta_report.md (128 score / 29 grade moves from the canonical re-baseline): Nutrition rules whether each move is methodologically sound / needs governance / is wrong + overall go/no-go; Red-Team adversarially challenges for invariant breaches, Anti-Immunity, clustering artifacts, indefensible scores (CRITICAL/HIGH/MED). Gates the owner-deploy of the re-scored staging pages. Read-only; no file production; no deploy.
---

# TASK-299 — Canonical re-baseline review gate — Nutrition methodology + Red-Team challenge of the 9-shelf delta report before owner deploy

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
