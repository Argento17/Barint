---
id: TASK-565
title: run_gates.py in CI -- BLOCKED: 14/16 live shelves fail the gate suite today
owner: qa-agent
status: BLOCKED
priority: HIGH
created_at: 2026-07-10
blocker: "Blocked by TASK-563 (pages not re-derivable from referenced traces -> G5) and TASK-564 (schema lag -> G1). Wiring run_gates now would red-X 14/16 shelves; mass-excepting them would make the gate meaningless."
depends_on: [TASK-563, TASK-564]
blocks: []
category_id: null
summary: >
  The audit called this do-first/low-effort. Probed before building (lesson from TASK-560): ran run_gates against every live shelf with re-anchored config paths. 2 PASS (crackers, granola) / 14 FAIL. Failing gates: G1 SCHEMA 11 shelves, G3 SCOPE 10, G5 GRADE-INTEGRITY 10. Real failures, not a harness artifact. G3 = scored barcodes absent from the page and unexplained in _meta exclusions (curation provenance not recorded). Additionally run_gates takes paths as CLI args, so a CI job needs a config-reading wrapper built on conformance.resolve_repo_path (TASK-560). Do NOT wire until 563/564 clear.
---

# TASK-565 — run_gates.py in CI -- BLOCKED: 14/16 live shelves fail the gate suite today

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
