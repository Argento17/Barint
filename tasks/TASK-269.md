---
id: TASK-269
title: Spine Stage 9: red_team_gate — adversarial review is the terminal gate before any run is owner-ready
owner: red-team-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-13
depends_on: [TASK-268]
blocks: []
category_id: null
summary: >
  Owner directive 2026-06-13: red-team is the FINAL item of every shelf run, auto-run (without being asked), right after Stage 8 render_local_page. A rendered page is NEVER 'done' until adversarially torn apart. Add Stage 9 red_team_gate to 03_operations/spine/pipeline_e2e.py — HYBRID: (a) DETERMINISTIC auto-checks that hard-fail the stage — every product image URL resolves (no dead hosts), every dropdown/expansion complete (no null/empty panels), npm run build passes, displayed score==run trace, OFF=0; (b) AGENT-IN-LOOP red-team seam (like Stage 6 author_copy) — adversarial content coherence/strength + fabrication/honesty check → CRITICAL/HIGH/MEDIUM. Run is owner-ready ONLY when Stage 9 has zero CRITICAL. Brined-cheese red_team_brined_page_v1 is the prototype. Deploy stays separate owner-gated step.
---

# TASK-269 — Spine Stage 9: red_team_gate — adversarial review is the terminal gate before any run is owner-ready

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
