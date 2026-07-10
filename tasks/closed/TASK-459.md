---
id: TASK-459
title: Local-to-origin reconciliation: end the brain/live divergence (P0-1 of launch report, owner mandate)
owner: data-agent
status: CLOSED
close_reason: >
  Orchestrator-verified against the tree (2026-07-02): 6 commits on feature/homepage-mascots
  (f801db5a..7807d16a — governance/registry/tools/design groups + 23MB junk purge + .gitignore
  hardening, verified via git log + porcelain); worktree C:\bari_wt_t459 branch
  reconcile/task459-brain-to-master carries exactly 1 commit (a365a656, 52-file registry
  reconcile, verified via git log origin/master..HEAD); commit classification verified — 0
  cherry-picks needed (3 patch-id duplicates, 4 superseded by origin 48811ebb curated port,
  9 board-narration, 1 frontend duplicate, 1 HOLD = 889-file WIP snapshot 6871d374); junk
  files confirmed gone from disk. C0 validate_return.py = PASS exit 0 (re-run independently
  by orchestrator). HOLD items open: WIP snapshot 6871d374 decision; sibling-agent logo churn;
  tmp_strip.txt. Deliverable branch awaits owner PR (tripwire #2).
priority: CRITICAL
created_at: 2026-07-02
depends_on: []
blocks: []
category_id: null
summary: >
  Inventory + classify the 18 local-only vs 18 origin-only commits and the ~50 dirty main-tree files; commit real uncommitted work durably on feature/homepage-mascots; port intended non-catalog local-only work to a branch off origin/master (catalog rides TASK-458); reconcile the forked task registry; classify+clean scratch junk. No pushes to live master; PR branch for owner merge.
---

# TASK-459 — Local-to-origin reconciliation: end the brain/live divergence (P0-1 of launch report, owner mandate)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
