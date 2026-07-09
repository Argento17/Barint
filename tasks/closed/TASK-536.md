---
id: TASK-536
title: Template-fingerprint gate: baseline author_copy.py output must never ship as signed-off copy
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-08
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified 2026-07-09 (unattended run, branch task506). Template-fingerprint gate exists and
  works: 03_operations/spine/validate_copy_authored.py runs CHECK2 (sentence mass-templating), CHECK3
  (baseline author_copy.py fingerprint), CHECK4 (field-level mass-template). Controls reproduced live:
  negative fixtures FAIL exit 1 (baseline_fingerprint_negative + masshedge_negative); genuinely-authored
  round-2 yogurt PASS exit 0 (spoonable 78 / drinkable 20, all signals 0). Gate proves copy was AUTHORED
  not merely accurate — the exact 2026-07-08 failure mode. Also caught a real latent LIVE defect on
  brined_cheeses (4 rows narrate score mechanism) → TASK-542 scope expanded. Wired into
  validate_comparison_page.py as a hard gate (TASK-540). Overlaps/subsumed by the L2 layer verified under
  TASK-541.
summary: >
  Root cause of the 2026-07-08 yogurt copy rejection: author_copy.py baseline generator strings ('הגורם המגביל', 'תורם לתחושת שובע' templates) shipped verbatim in 98-product copy and passed both sign-off gates. Add a deterministic gate (validate_comparison_page.py or run_gates.py) that extracts author_copy.py's template phrases and FAILS any frontend JSON where copy fields match the baseline fingerprint. Gates must prove copy was actually authored, not just accurate.
---

# TASK-536 — Template-fingerprint gate: baseline author_copy.py output must never ship as signed-off copy

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
