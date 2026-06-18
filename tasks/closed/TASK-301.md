---
id: TASK-301
title: QA data-sanity gate — block physically-impossible nutrition + nutrition-panel-as-ingredients from reaching a page
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-17
closed_at: 2026-06-17
close_reason: >
  C1-GROK (P159) added G8 DATA-SANITY to run_gates.py (sodium>5000 + absurd-value bounds per nutrient +
  nutrition-panel-as-ingredients token match); wired into the gate list (run_gates.py:1266) so generate_page +
  rescore_all self-gates now hard-fail on corrupt shelves. ORCHESTRATOR-VERIFIED INDEPENDENTLY: ran gate_data_sanity
  on all 9 staging pages -> granola=FAIL + hummus=FAIL (exactly the 2 shelves carrying the 6 known-bad records),
  other 7 shelves PASS (no false positives; snacks PASS = its RT-1 floor issue is methodology not data). Only run_gates.py
  touched (the parallel BSIP1 data edits in the git delta are TASK-300, disjoint files). Follow-up flagged: a BSIP1-ingest
  validator to catch corruption earlier. Uncommitted (batched with TASK-300 fix + re-run).
depends_on: [TASK-299]
blocks: []
category_id: null
summary: >
  Add deterministic data-sanity validation to the page gate (run_gates.py): sodium_mg>5000 per 100g = ERROR (and analogous absurd-value bounds per nutrient), and ingredient_text matching a nutrition-panel pattern (contains tokens like 'ערכים תזונתיים','קל','גרם חלבונים','מג נתרן') = ERROR. Must fail the gate (non-zero) so rescore_all/generate_page refuse to emit a corrupt shelf. Flag a BSIP1-ingest-level validator as follow-up.
---

# TASK-301 — QA data-sanity gate — block physically-impossible nutrition + nutrition-panel-as-ingredients from reaching a page

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
