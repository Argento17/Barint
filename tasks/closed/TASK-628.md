---
id: TASK-628
title: Capture->PID matcher fix: attach the 24 cookies_coffee ambiguous captures + fix cross-category GTIN collision
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-626
lesson_trigger: none
close_reason: "VERIFIED (static + rebuild) + merged. Capture-matcher now category-aware + dedup + category_mismatch_capture guard (cross-category GTIN collision -> not_retrieved). source_traceability improved 580->599 pass. No score change. Codex-built, Opus-verified."
summary: >
  24 cookies_coffee low-evidence products have a real capture that the barcode->PID matcher failed to attach; plus a cross-category GTIN collision (milk barcode -> capture tagged bread) where the compiler marks status=retrieved with null values (overstates completeness). Fix the matcher/join in the PD compiler so these attach correctly; evidenceCompleteness rises for the 24. No score change.
---

# TASK-628 — Capture->PID matcher fix: attach the 24 cookies_coffee ambiguous captures + fix cross-category GTIN collision

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
