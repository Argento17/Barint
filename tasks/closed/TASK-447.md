---
id: TASK-447
title: Wired-in capability audit — find installed/built-but-unwired tools across the pipeline (rembg-shaped holes)
owner: data-agent
status: CLOSED
closed_at: 2026-07-11
close_reason: "DONE-IN-FACT - read-only capability audit completed; evidence = its downstream action tasks exist in the registry (TASK-446/451/453 asserted), each citing the audit's findings. Per ghost triage 2026-07-11 (tasks/reports/ghost_triage_2026-07-11.md); orchestrator mechanically asserted the cited artifacts before closing."
priority: MEDIUM
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  Systematic sweep: walk BSIP0->BSIP1->BSIP2->page_generator->copy->gates->render, classify every capability WIRED / PROTOTYPE / INSTALLED-UNUSED / GAP with file:line evidence. Prompted by rembg (installed) + Azure DI OCR (built prototype, not wired). Read-only; produces a ranked table + top-3 dormant holes. Running bg (a8d4c193).
---

# TASK-447 — Wired-in capability audit — find installed/built-but-unwired tools across the pipeline (rembg-shaped holes)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
