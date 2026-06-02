---
id: TASK-164
title: Investigate bread shufersal_3268429 whole-wheat-vs-refined + grade A/B contradiction
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-02
closed_at: 2026-06-02
closed_by: cc-agent
close_reason: "CC gate PASS — investigation delivered (no data changed; freeze respected). FINDING: the product IS genuinely whole-grain — BSIP0 raw scrape (real_bread_retail_003_v1...bsip0_raw.json) shows 'קמח חיטה מלא ... 100% מהקמח', extraction_confidence high. Engine authority (bsip2_shufersal_3268429.json) = 79.8/B with has_ingredients:true. ROOT CAUSE: the ingredient list failed to propagate from BSIP0 to the signal layer (limiting_factors_v1.json: 'אין רשימת רכיבים זמינה'), so signals defaulted to a false 'refined base / fiber unclear' reading -> wrong limitingFactors AND a stale live grade A. RECOMMENDATION (needs human, bread frozen): (1) reconcile grade A->B to match engine+curated; (2) re-propagate ingredients so the false refined-base/fiber signals recompute to whole-grain; (3) audit bread corpus for the same non-propagation pattern; interim: suppress the demonstrably-false limitingFactors for this id."
resolution: "OWNER RULED DE MINIMIS (2026-06-02) — not pursuing the grade A->B / signal reconciliation. Row copy made base-agnostic in TASK-168I (leads on undisputed protein 12.6 / fiber 6.4 / A standing, no base claim). Issue closed; do not resurface to the owner."
depends_on: []
blocks: []
category_id: bread
summary: >
  Lechem yarok mikemach male: name+insightLine say whole-grain, signal data says refined base; grade shows A (live) vs B (curated). Check the real source/provenance, recommend which is correct. Bread is a frozen invariant -> recommendation only, human decides grade.
---

# TASK-164 — Investigate bread shufersal_3268429 whole-wheat-vs-refined + grade A/B contradiction

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
