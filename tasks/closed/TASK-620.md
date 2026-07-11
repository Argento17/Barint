---
id: TASK-620
title: PD-3.1: human-readable Overview tab for /internal/dossier (English, reuse VerdictRow, 3-tab)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
lesson_trigger: correction
lesson_outcome: not_applicable
lesson_evidence: "Process lesson (already codified elsewhere, not re-litigated here): the orchestrator KILLED this build mid-flight to retroactively satisfy the BUILD->Codex routing rule, but the killed Claude build was actually COMPLETE and better-integrated (used the live loader.ts); the Codex re-dispatch then collided on a stale worktree base. Lesson = don't kill near-complete work to satisfy a routing rule after the fact; probe/route correctly UP FRONT. Fully captured in memory router_no_single_vendor_probe_lanes + orchestrate.md lane-preflight rule + the 2026-07-11 telemetry audit. No new artifact needed for THIS task."
close_reason: "VERIFIED + owner-approved. Render-verified in real DOM (localhost:3000/internal/dossier/bari_02b825a4420f905ff2b9214b, HTTP 200): Overview default tab shows all spec sections — header (name/brand/category/pkg/manufacturer/barcode-status/published-score), Bari verdict = the REAL ComparisonRow with real rowVerdict text + an 'Estimated' badge correctly NOT styled as Verified + plain-English non-reproducibility caveat, THREE separate cards (Product assessment / Data quality / Publication integrity — not blended), 2D product-profile bars (assessment-only, 'never blended'), deterministic Strengths/Concerns bullets from assessment axes, 'Checks needing attention' (Barcode WARN) with '3 other checks passed' collapsed. tsc --noEmit exit 0 on the clean tree. Evidence + Technical-audit tabs wired in [pid]/page.tsx + compile. Owner viewed and approved ('I see it. that's fine'). Implementation kept = the committed Claude build (complete, integrated); redundant Codex worktree discarded."
summary: >
  Add Overview (default) + Evidence + Technical-audit tabs to the internal dossier detail page. Reuse public VerdictRow (or thin adapter) for the one-line verdict; 3 separate cards (assessment/data-quality/publication-integrity, never blended); 2D product-profile visual; human insights + attention-checks. English. Compiled PD outputs only, no scoring/compiler change.
---

# TASK-620 — PD-3.1: human-readable Overview tab for /internal/dossier (English, reuse VerdictRow, 3-tab)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
