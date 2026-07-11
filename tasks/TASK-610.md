---
id: TASK-610
title: PD-2: build_dossiers.py compiler v1 + committed baseline + --check CI gate
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: [TASK-609]
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
summary: >
  One shelf-agnostic compiler regenerates per-product dossiers wholesale (Layers 1+2 provenance cells from 601 manifest/replay + L3 three disjoint namespaces assessment/data_quality/publication_record, read-only stamped, honest derivation labels + L4 four checks: barcode/source-traceability/calculation/publishability importing existing gate logic). OFF-source cell = build fail; missing = NULL, no imputation path; cross-namespace metric read = build fail; no overall_score. Committed dossier_baseline.jsonl + --check next to replay gate. BLOCKER: committed baseline waits on the BSIP0 parser fix (other session) + replay re-baseline; pre-fix projection allowed only uncommitted, parser_version-stamped.
---

# TASK-610 — PD-2: build_dossiers.py compiler v1 + committed baseline + --check CI gate

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
