---
id: TASK-611
title: PD-3: internal Page-1 product-inspection view
owner: frontend-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-11
close_reason: >
  PD-3 internal inspection view DELIVERED (frontend-agent, commits c543ff15 + fixup ab5bfd84) +
  orchestrator-verified. Routes /internal/dossier (corpus list) + /internal/dossier/[pid] (Page-1),
  8 components, dossier data lib + sync-dossiers.mjs (687 dossiers/18 shelves → gitignored cache).
  VERIFIED: both commits are PD-3-only (17 files, all bari-web/internal + dossier), ZERO served-
  comparison/score/bsip2 files (tripwire-1 clean), robots.ts disallows /internal/, noindex layout.
  Agent real-DOM verified (Playwright): 687 rows, "calc failed" filter = 77 (matches manifest
  calculation.fail=77), per-product renders identity/4-check-panel/evidence-cells/publication_record
  (calc-FAIL shown beside served score), and assessment (10 bars) vs data_quality (3 bars) as DISJOINT
  toggles — never blended into one number (memo R-C upheld). tsc+eslint+build clean. NOT pushed (deploy
  = owner-gated; internal noindex tool). Radar shipped as plain bars (memo's explicit >1-day fallback);
  Page-2/image-confidence deferred per §5. Commit-slip self-caught+fixed (git commit -- pathspec swept
  an ambient .gitignore line; fixup ab5bfd84 isolated it — instance of the known dirty-tree hazard).
  **PD MVP COMPLETE (PD-1 registry + PD-2 compiler/join + PD-3 view); only the committed dossier
  baseline remains, blocked on the parser fix.**
depends_on: [TASK-610]
blocks: []
category_id: null
origin_task: TASK-608
lesson_trigger: none
summary: >
  Internal-only inspection route (no two-gate yet): identity+barcode status, Layer-4 check panel, per-field evidence cells, score-as-copied. Radar simplest honest form (single 2D polygon, hard-toggled assessment/data_quality layers) or plain bars if polygon >1 day. Foundation for the future consumer scanner-result page (two-gate applies then). Deferred: page 2 as designed UI, radar polish/blend, scanner UI, image confidence.
---

# TASK-611 — PD-3: internal Page-1 product-inspection view

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
