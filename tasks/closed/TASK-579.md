---
id: TASK-579
title: Fan out derived card stats to all remaining featured intelligence cards
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-10
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. 17/19 featured cards now derive from deriveComparisonCardStats
  (3 pilot + 14 fan-out); 2 honest exclusions (magnesium = TASK-578 no generated source;
  bread-lite = scan-funnel stats on a different product type, forcing would redefine meanings).
  Consumer-visible changes: NONE - orchestrator spot-verified: milk meta product_count=18 =
  len(products)=18, scored 18/18, so all relocated milk stats render identically; chocolate-
  tablets ceiling "B" literal matches derived ceilingGrade; cocoa% left as literal with inline
  note (no source field - correct non-forcing). Orchestrator re-ran: parity fixture exit 0
  (17/17), validate_return.py --root C:/bari_wt_568 PASS, branch task579-cards-fanout @
  2dcecb0d confirmed pushed (stacked on pilot, not rebased). CI: validate-card-stats step
  added to barint_ci frontend job with documented Node 20->24 bump (native TS stripping
  required; single-job scope; orchestrator read the workflow diff). Pilot manifest bug found
  and fixed: cheese parity pointed at orphaned v4 while page imports v5 (values identical
  today, reference wrong - caught by validate-corpus orphan check). Agent evidence: tsc 0,
  lint 0, next build exit 0. PR pending owner merge (merge pilot 568 first or together).

summary: >
  Owner go-ahead 2026-07-10 after TASK-568 pilot (cheese/protein-bars/granola). Convert every remaining featured-*-intelligence-card.tsx to deriveComparisonCardStats, extend the validate-card-stats parity fixture to all converted cards, and wire it into barint_ci frontend job (prove green first). Zero copy changes; every hardcoded-vs-derived drift disclosed as consumer-visible. Stacked on branch task568-derived-cards until the pilot PR merges. Magnesium excluded (TASK-578, no derivable date source).
---

# TASK-579 — Fan out derived card stats to all remaining featured intelligence cards

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
