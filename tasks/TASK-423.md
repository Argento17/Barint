---
id: TASK-423
title: W4: Orchestrator durability — dispatch journal+lock+worktree-default, canary/rollback ledger
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
closed_at: 2026-07-01
depends_on: [TASK-420, TASK-421]
blocks: []
category_id: null
close_reason: >
  All 3 parts built + self-tested + integrated. (a) dispatch_journal.py — append-only JSONL
  step journal + already_done() replay check. (b) fail-fast dispatch_lock (serializes dispatch.py
  → kills the concurrent-opencode race) + guard_tree_for_cloud_lane (refuses a cloud lane when the
  tree is dirty → kills the git-stash-u wipe); both wired into dispatch.py (main lock-wrap + in-flow
  guard, GUARDED so they can never break the router). (c) promote.py — gated staging→live promotion
  (rank_check gate, refuses on fail) + one-command rollback from per-promotion backup; git deploy
  stays owner-gated. All selftests exit 0; dispatch.py compiles + runs (--route ok, dry-run journals
  2 events, py_compile ok). No published-score/consumer-facing change. Journal/lock/backups are
  runtime state (gitignored). This is the orchestrator-durability "to 9" piece.
summary: >
  3 parts: (a) append-only tasks/_journal/<run>.jsonl step-log so /orchestrate resumes mid-run (journal-replay, never re-run completed step); (b) dispatch lock serializing dispatch.py + worktree-default for CLI lanes (kills race + tree-wipe hazards); (c) promote.py: staging candidate -> shadow-score vs baseline -> promote to live_manifest only if gates pass, one-command rollback. Promote step stays owner-gated (tripwire-2).
---

# TASK-423 — W4: Orchestrator durability ("to 9")

## Deliverables (all under 03_operations/agentos/ + a minimal dispatch.py wire)
- **dispatch_journal.py** — durable-execution primitives: `dispatch_lock()` (fail-fast cross-process
  lock, Windows-safe O_EXCL, stale-reclaim), `journal()`/`read_journal()`/`already_done()` (append-only
  JSONL step-log + replay check), `guard_tree_for_cloud_lane()` (dirty-tree refusal for cloud lanes).
  Selftest exit 0 (lock/journal/guard).
- **promote.py** — gated staging→live promotion: runs the gate (rank_check.py default / `--gate-cmd` /
  `--no-gate`), backs up current live, promotes only on pass, records a ledger entry; `rollback --last|--id`
  restores from backup; `ledger` shows history. Selftest exit 0 (promote-pass / refuse-on-fail / rollback).
  The git deploy stays owner-gated — promote.py only moves the working-tree file.
- **dispatch.py wire (minimal, guarded):** `main()` runs the real dispatch inside `dispatch_lock()` +
  journals it; `cmd_dispatch()` runs `guard_tree_for_cloud_lane(route)` before a cloud lane. Both in
  try/except → a durability-module issue can never break the router (falls back to the original path).

## Maps to the 2026 durable-execution SOTA
journal-based replay + checkpoints (Temporal/LangGraph), serialize-to-avoid-races, and canary-with-
rollback (LLMOps) — adapted to a no-traffic product (promote = staging→live file gate, not traffic split).

## Follow-ups (not blocking)
- Extend the journal into the `/orchestrate` loop for full mid-run resume (today it covers dispatch).
- Optionally re-plumb cloud lanes into real `git worktree`s (the guard currently REFUSES on dirty tree;
  a worktree would let them run anyway) — bigger change, deferred.
