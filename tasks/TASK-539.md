---
id: TASK-539
title: Router --repo/--cwd override so cloud C1 lanes (Grok/Cursor/Gemini) can target a clean worktree on a dirty tree
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  Owner 2026-07-08 'i dont see you using C1': cloud C1 CLI lanes are unusable whenever C:\Bari has uncommitted files (the W4 guard refuses their whole-tree git stash -u). Running the worktree's own dispatch.py does NOT help — guard_tree_for_cloud_lane(route, repo=REPO_ROOT) defaults to the hardcoded main root, not the caller's. Current workaround = drive grok.exe/cursor-agent directly in a clean worktree (loses router journaling). FIX: add dispatch.py --repo/--cwd that threads to BOTH the CLI subprocess cwd AND guard_tree_for_cloud_lane(route, repo=<worktree>), so 'python dispatch.py PNN --repo C:/bari_wt_c1' runs the lane against the clean worktree with full journaling. Memory: c1_cloud_lane_worktree_unblock.
---

# TASK-539 — Router --repo/--cwd override so cloud C1 lanes (Grok/Cursor/Gemini) can target a clean worktree on a dirty tree

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
