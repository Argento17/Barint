---
id: TASK-615
title: Integrate batch-4/5 captures into canonical manifest format (bespoke shape not scanned)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-602
lesson_trigger: failure
summary: >
  TASK-602 batch-4/5 retained raw captures (captured.nutrition_raw_keys + full_page_text_hebrew_source) but in a bespoke LIST shape lacking the nutrition_raw_source.rows dict that build_manifest.py scans for -> ~120 captures on disk but INVISIBLE to the manifest (coverage stuck 567/710, should be ~687). Data is present, not lost. Fix = canonicalization transform: map each batch-4/5 item into the canonical nutrition_raw_source:{rows:[...]}+gtin schema (use a batch-3 capture the manifest already references as the golden format), write manifest-scannable files, rebuild manifest+census (prove coverage jump), recompile registry. LESSON (6b): scrape dispatches MUST require the canonical retention helper + acceptance test = manifest coverage rises, not just files-written.
---

# TASK-615 — Integrate batch-4/5 captures into canonical manifest format (bespoke shape not scanned)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
