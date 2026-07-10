---
id: TASK-494
title: Blog template WCAG-AA contrast fix (meta + eyebrow text, all blog components)
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-03
closed_at: 2026-07-05
depends_on: []
close_reason: >
  Blog-template contrast fixed + orchestrator-verified after one CHANGES_REQUESTED round (2026-07-05
  unattended run). Colors: meta #7A817C→#5C635E (6.17:1), eyebrow #7A9450→#4A5E26 (7.19:1 solid / 4.96:1
  at /85) — all ≥WCAG-AA on white and #F7F7F2. Canonical token file src/lib/design/blog-tokens.ts added.
  First commit 3198c557 was color-correct but introduced a UTF-8 BOM on all 46 files (30 on the "use client"
  line — Next.js client-directive risk that tsc/lint miss); orchestrator caught it (46/46 BOM confirmed) and
  sent back. Fix commit e4434a0b re-saved all files UTF-8-no-BOM. FINAL VERIFICATION: C0 validate_return
  PASS; 0/46 files start with EF BB BF; 0 old hexes remain in blog scope; "use client" clean at byte 0;
  all 47 changed files strictly blog-scoped (no frozen/comparison/out-of-scope file touched); tsc 0, lint 0.
  Branch fix/task494-blog-contrast @ e4434a0b (worktree C:\bari_wt_t494) — NOT pushed; push+PR queued for
  supervised morning. Non-blog #7A817C occurrences (~50 in 22 files) intentionally out of scope.
blocks: []
category_id: null
summary: >
  Design critic (TASK-492A) found meta text #7A817C (3.99:1) + eyebrow #7A9450 (3.16-3.40:1) below WCAG-AA 4.5:1. Pre-existing debt inherited from the food-dyes template across ~14 blog components. Fix template-wide (darken to >=4.5:1, ideally via CSS tokens) so no single page diverges from the frozen reference. axe/test:a11y gate flags it.
---

# TASK-494 — Blog template WCAG-AA contrast fix (meta + eyebrow text, all blog components)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
