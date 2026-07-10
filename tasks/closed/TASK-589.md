---
id: TASK-589
title: Router telemetry: entry rows + tokens/duration in router_v5_log
owner: frontend-agent
status: CLOSED
close_reason: >
  BUILD-LIGHT (Codex gpt-5.6-terra) delivered in worktree; orchestrator verified: C0 PASS (sha256
  match), all three selftests independently re-run green in the worktree AND again in the Speed-1
  merge worktree (--selftest-table byte-match, --selftest-route 14/14, new --selftest-telemetry:
  start row / end duration+tokens / pre-run-crash entry row), diff scan telemetry-only (122+/17-,
  MODEL_BINDING read not modified). Lane obeyed the new sandbox-git rule: clean tree, no fallback
  git-dir. Speed-1 internal merge pushed: origin/master 841d0c83 -> 9f793f5b.
priority: LOW
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Audit 2026-07-10 findings E4+E5: dispatch.py telemetry writes one row only at lane COMPLETION and captures no tokens/duration/tool-calls (both TASK-588 lane attempts show UNKNOWN consumption; the attempt-1 driver crash left no row at all). Extend _log_telemetry: write a row at dispatch ENTRY (ts, task, capability, model, attempt) and enrich the completion row with duration_s and token usage parsed from codex exec output. BUILD-LIGHT (gpt-5.6-terra). Keep selftests green (--selftest-table byte-match unaffected - telemetry is not in the law tables).
---

# TASK-589 — Router telemetry: entry rows + tokens/duration in router_v5_log

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
