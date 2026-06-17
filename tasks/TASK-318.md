---
id: TASK-318
title: Spine step 3 — automated copy stage (generalize copy-carryover + schema-strip + author-set detection into a reusable pipeline step)
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-17
depends_on: [TASK-316]
blocks: [TASK-319]
category_id: null
summary: >
  This week's publish carried copy + detected the author-set via TWO one-off scripts (_rescore_staging/copy_carryover.py TASK-305 +
  _rescore_staging/schema_strip.py TASK-307) hand-listed per shelf. Generalize them into ONE reusable, config-driven module so the
  spine does it automatically: given a freshly generated staging page + its live baseline (config.baseline_json), carry the live
  copy fields for grade-UNCHANGED products by barcode, leave PENDING_COPY + add to the author-set for grade-CHANGED/NEW products,
  strip staging-only fields to the live schema, and flag grade-unchanged-but-score-moved≥3pts. Emit the copy-applied page + an
  author_set.json manifest (barcodes needing fresh copy + fields + the grade move). Reuse the existing one-off logic as the source;
  make it parameterized (no per-shelf hand-listing). NO engine/scoring changes, NO bari-web edits, OFF-ban absolute. Test on one
  category end-to-end (generated staging + live baseline → carried copy + author-set). Route Data Agent (copy-pipeline reasoning).
---

# TASK-318 — Spine step 3: automated copy stage

See `tasks/prompts/P168_copy_stage.md`. With step 1 (render-contract) done, copy-carry is the last manual piece before the
orchestration can run a flag-flip to a near-complete page automatically (only genuinely-new copy needs an author pass).
