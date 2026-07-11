---
id: TASK-631
title: task616_type_b comma-thousands audit: reconstruction producer bypasses the TASK-621 shared parser (corpus-wide)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: recurrence
lesson_outcome: regression_test
lesson_artifact: 03_operations/bsip0/manifest/canonicalize_task616_type_b.py
lesson_validator: python 03_operations/bsip0/manifest/canonicalize_task616_type_b.py --selftest
lesson_evidence: corpus audit re-derived 120 canonical records through the shared parser; 1 mismatch = already-fixed crackers 7290018790328 (1.2->1200.0); producer --selftest passes 1,200->1200/0,123->0.123/1.5->1.5; no served JSON touched.
close_reason: >
  VERIFIED + committed (4de34ed1). Corpus-wide re-derive-vs-stored audit: 120 canonical records checked
  (53 task616_type_b + 67 type_a), exactly 1 mismatch -- crackers 7290018790328 sodium 1.2 -> 1200.0
  (the comma-thousands signature), which TASK-629 had ALREADY caught and re-scored (50.3/C -> 35.0/D).
  So the bug was isolated to that single product corpus-wide; no NEW corruption. Root cause: the
  reconstruction producer (canonicalization_schema=task616_type_b_rows_reconstructed_from_nutrition_raw)
  did its OWN numeric parse, bypassing the TASK-621-hardened shared parser -- a DIFFERENT code path than
  the 7 siblings TASK-621 fixed. Producer hardened: new canonicalize_task616_type_b.py routes exclusively
  through parse_nutrition_rows -> bare_to_raw_keys -> parse_nutrition_numeric; --selftest proves
  1,200->1200, 0,123->0.123, 1.5->1.5. No served JSON / published score touched (the one score-affecting
  correction was already applied by 629). Audit report: 03_operations/bsip0/manifest/task631_type_b_comma_audit.json.
summary: >
  task616_type_b comma-thousands audit: reconstruction producer bypasses the TASK-621 shared parser (corpus-wide).
---

# TASK-631 — task616_type_b comma audit

Recurrence of the comma-thousands bug in a distinct producer. See close_reason. Producer now routes through the shared parser; --selftest is the regression guard.
