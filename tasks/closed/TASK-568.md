---
id: TASK-568
title: Derived views: homepage carousel + featured duel generated from comparison JSON at build time
owner: frontend-agent
status: CLOSED
closed_at: 2026-07-10
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. Phase 1 scoping doc at 01_framework/frontend/derived_views_scoping_v1.md
  (6 cards audited; found insightLines/showInsights dead on ComparisonIntelligenceHero since
  2026-07-01, cutting scope). Phase 2 pilot: shared deriveComparisonCardStats module
  (bari-web/src/lib/derived/comparison-card-stats.ts) + npm run validate-card-stats parity
  fixture; 3 cards converted (cheese, protein-bars, granola). Orchestrator verification:
  branch task568-derived-cards @ 7c0740e9 pushed (confirmed ls-remote); validate_return.py
  --root C:/bari_wt_568 exit 0 re-run PASS; parity check re-run by orchestrator exit 0;
  cheese-card diff personally read - inline math replaced by shared module, Hebrew labels
  byte-identical, zero rendered-literal changes. Drift finding disclosed: protein 25-34
  vs actual 25-36 and granola 47 vs ~38 existed on the stale local branch but were already
  hand-fixed on origin/master, so the PR ships zero visible stat changes. Magnesium
  hardcoded updated-label has no derivable source - registered TASK-578 (data-agent).
  Agent build evidence: npm ci, tsc --noEmit 0, lint 0, next build 305 routes exit 0.
  PR pending owner merge. Remaining 13 cards = fan-out after pilot merges.

summary: >
  Owner-approved 2026-07-10. The ~16 hand-maintained featured-*-intelligence-card.tsx components carry scores/counts that silently drift from the served comparison JSON. Replace hand-maintained numbers with build-time derivation from the JSON (single StoryCard-style data shape). Approved copy strings remain inputs (two-gate governed) - only data fields derive. Needs design scoping before build; verify with a derived-vs-JSON parity check that becomes a CI fixture.
---

# TASK-568 — Derived views: homepage carousel + featured duel generated from comparison JSON at build time

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
