---
id: TASK-581
title: Adopt the generated page schema as the contract (review 42 diffs, fix magnitude typing, sync ops copy)
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-10
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. 42 diffs adjudicated grounded in live data (37 generated-wins;
  2 real contract bugs fixed incl. reversing TASK-569's own positiveSignals call - present
  681/681 so required; 3 comment corrections). Single source of truth adopted: TS contract ->
  generated schema -> ops copy synced verbatim with GENERATED header (sync-ops-schema /
  verify-schema-sync); orchestrator re-ran diff-page-schema = 0/0/0/0 across all four diff
  categories. ROOT-CAUSE FIX independently read by orchestrator: run_gates.py validator had
  zero anyOf/oneOf support (typed unions fell through unchecked - exactly how the magnitude
  int/string bug shipped); fix adds branch matching, G1 18/18 non-regression (orchestrator
  re-ran 3 shelves PASS in worktree), corrupted-magnitude tamper now fails. NEW CI
  page_schema_gate.yml: changed-comparison-JSON ajv gate (18/18 simulated) + schema-lag
  regen-diff gate (proven no-op green). Factory skill Stage 13 checklist added (C7 CRITICAL
  adjudicated - orchestrator read the diff: schema-valid / no leaked raw fields per TASK-574 /
  sha256 sign-off per TASK-567; sign-off authorship stays orchestrator-only). Owner directive
  satisfied: a future non-conforming shelf goes RED in CI and is blocked at factory checklist.
  Branch task581-schema-adoption @ ba89c2a6 pushed; PR pending owner merge. Return C0: all
  families PASS except expected C7 (task-mandated skill edit, resolved by human read).

summary: >
  Follow-up to TASK-569. The generated schema (bari-web/schema/page-output-schema.generated.json) passes 18/18 shelves; the hand-maintained page_output_schema_v1.json has 42 categorized differences and types limitingFactors[].magnitude as string while chocolate_bars/chocolate_tablets/snacks emit numbers (G1's checker validates property presence, not value types, so it never caught this). Work: review the 42-diff list in TASK-569_return, decide field-by-field which side is right, fix the hand schema or the contract type accordingly, add a CI step that regenerates and diffs so lag can never return, and define the sync between bari-web/schema and 03_operations/page_generator/contract.
---

# TASK-581 — Adopt the generated page schema as the contract (review 42 diffs, fix magnitude typing, sync ops copy)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
