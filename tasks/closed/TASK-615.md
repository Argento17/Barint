---
id: TASK-615
title: Integrate batch-4/5 captures into canonical manifest format (bespoke shape not scanned)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
close_reason: >
  Canonicalization DELIVERED (data-agent, commit 5302d5a8) + orchestrator-verified. Agent found TWO
  non-canonical schemas (Type A captured-wrapper with rows = rename; Type B flat nutrition_raw =
  rows reconstructed from the canonical Hebrew label vocab, cross-verified vs 69 existing captures).
  VERIFIED by orchestrator: (1) tripwire-1 CLEAN (commit touched 0 served comparison JSON); (2) census
  re-run 567→**693/710** covered (target ~687; +6 incidental bread_v3); (3) registry_ops.py --check +
  --selftest PASS, barcode_status verified 442→535 (+93), pending 116→23, malformed 129 unchanged;
  (4) Type-B fidelity SPOT-CHECK on crackers = 8/8 rows correctly paired (energy 418→אנרגיה/kcal,
  sodium 397→נתרן/mg, sat-fat 1.6→מתוכם שומן רווי/g …) values verbatim, units right. Honest deviations
  accepted: 1 empty cookies capture discarded (missing-data rule, cookies 111 vs ~112), 1 hard_cheese
  PLU-vs-GTIN exposed to served GTIN. Baseline is now INTEGRATED (not just retained). Lesson codified
  (memory scrape_capture_canonical_format + 6b). NOTE: this is the CANONICALIZATION task — the id was
  mislabeled "TASK-616" in the dispatch prompt/early board; TASK-616 is the separate yogurt-config task.
depends_on: []
blocks: []
category_id: null
origin_task: TASK-602
lesson_trigger: failure
lesson_outcome: implementation_task
lesson_generated_task_id: TASK-617
lesson_evidence: "census 567 to 693 (commit 5302d5a8); non-canonical captures invisible to build_manifest"
lesson_signature: bsip0_capture_noncanonical_not_scanned
lesson_related: [TASK-602, TASK-617]
summary: >
  TASK-602 batch-4/5 retained raw captures (captured.nutrition_raw_keys + full_page_text_hebrew_source) but in a bespoke LIST shape lacking the nutrition_raw_source.rows dict that build_manifest.py scans for -> ~120 captures on disk but INVISIBLE to the manifest (coverage stuck 567/710, should be ~687). Data is present, not lost. Fix = canonicalization transform: map each batch-4/5 item into the canonical nutrition_raw_source:{rows:[...]}+gtin schema (use a batch-3 capture the manifest already references as the golden format), write manifest-scannable files, rebuild manifest+census (prove coverage jump), recompile registry. LESSON (6b): scrape dispatches MUST require the canonical retention helper + acceptance test = manifest coverage rises, not just files-written.
---

# TASK-615 — Integrate batch-4/5 captures into canonical manifest format (bespoke shape not scanned)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
