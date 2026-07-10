---
id: TASK-555
title: guard-two-gate-commit.ps1: close the git -C commit bypass (regex + repo scoping)
owner: qa-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10, commit 774ef404 (task506). Trigger regex now matches commit as the
  git SUBCOMMAND after global options (-C/-c/--flags) — `git -C <path> commit` is gated (was a full
  bypass), filenames containing 'commit' (e.g. the hook's own name) no longer false-trigger (first
  broad-regex attempt blocked its own remediation commands; tightened). Staged-file check scopes to the
  -C target repo. Evidence: 9/9 payload-simulation battery (scratchpad test_guard_two_gate.ps1) incl.
  live BLOCK exit-2 on the real ungated staged yogurt JSON in C:\Bari and pass on clean worktree via -C
  scoping; plus a live-fire pass gating the hooks commit itself. Both guard scripts (two-gate + off-ban)
  now TRACKED (were untracked — enforcement existed only on this machine). Side note logged on board:
  the 2 staged yogurt JSONs (TASK-546 batch) had index blobs identical to HEAD; they are now unstaged —
  worktree R2 content untouched; re-stage + refresh markers through both gates before committing that
  batch (hook enforces). Memory two_gate_commit_hook_worktree_falseblock updated: git -C workaround
  retired, it is now a gated path.
depends_on: []
blocks: []
category_id: null
summary: >
  The two-gate commit hook's trigger regex (git\s+commit) misses 'git -C <path> commit' — the standard worktree commit pattern — so those commits bypass the sign-off guard entirely. Even when triggered, staged-file scoping uses payload cwd, not the -C target repo. Fix: broaden trigger to any git ... commit, parse -C <path> for repo scoping, add payload-simulation tests for block/pass/worktree cases. Orchestrator inline (hook untracked in worktree lanes; ~10-line scoped change + test harness).
---

# TASK-555 — guard-two-gate-commit.ps1: close the git -C commit bypass (regex + repo scoping)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
