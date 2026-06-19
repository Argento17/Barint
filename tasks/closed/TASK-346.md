---
id: TASK-346
title: Phase 2+3 WS-Frontend: re-skin shared expansion-section.tsx + AdditivePanel per spec
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: [TASK-344]
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified + committed. Re-skinned 4 files: expansion-section.tsx (5-section
  taxonomy), AdditivePanel.tsx (NewAdditivePanel sub-dropdown), view-models/index.ts (sourceLine,
  rank, categoryTotal, limitingFactors union), comparison-row.tsx (forwards rank/total). All 12
  polish refinements (R-01..R-12). INDEPENDENTLY VERIFIED: `npm run build` exit 0 (all routes incl.
  all /hashvaot pages); scope = only the 4 component/VM files (no JSON/scores — the additive_burden
  index change is parallel-chat, not this task); no red color; 5 verbatim labels present in order.
  Regression-safe: sections 2 (shelf-context) + 5-populated render only when VM fields exist, so
  existing pages silently omit until Data populates them. Additive shape normalized at runtime
  (name_he/function_he handled). not_done (= Data deps, TASK-347): rank/categoryTotal/sourceLine/
  magnitude not yet in JSON → those sub-sections hidden/0-width until remediation fills them. Milk
  fold = separate task. Applies to all 10 pages at once (shared component).
---

# TASK-346 — WS-Frontend re-skin shared dropdown

CLOSED + verified (build exit 0) + committed. Shows full data once TASK-347 populates rank/total/
magnitude/sourceLine. Milk-fold onto the shared component = separate follow-on.
