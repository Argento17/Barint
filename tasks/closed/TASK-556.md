---
id: TASK-556
title: board_check.py: read-only registry-to-DISPATCH_BOARD drift checker
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-10
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10. C1-CURSOR built tasks/board_check.py in scratch repo off registry
  copies; orchestrator code-reviewed (stdlib-only, read-only, path-relative, 5 checks, exit 0/1/2),
  patched utf-8-sig (BOM'd registry files false-flagged as missing delimiter — TASK-343 was healthy),
  landed and ran against the REAL registry. Tool immediately paid for itself — 143 findings: TASK-431
  unclosed frontmatter (repaired), TASK-462 ID COLLISION (two different closed tasks shared the id;
  Evidence-Watch repurpose renumbered → closed/TASK-558 after a second collision with the concurrent
  sweetener TASK-557 created this morning by another session), 15 CLOSED tasks unarchived (moved to
  closed/, status-verified each), 4 stale-active board headers (marked ✅), 4 recent ghost opens
  surfaced onto the board (550/552/553/557). Clean re-run: badfile 0, stale-active 0, unknown 0;
  remaining = 115 legacy ghosts (pre-compaction triage backlog, deliberate) + 3 RETURNED-in-closed
  (200/201/202, need reopen-or-close triage). --json interface verified parseable. One process burn
  logged: PowerShell regex rename mojibake'd the renumbered file (known Hebrew-shell gotcha) —
  recovered byte-exact from the scratch seed copy, redone with the Edit tool.
depends_on: []
blocks: []
category_id: null
summary: >
  From the CI/automation audit: new_task.py creates tasks but nothing reconciles the board; drift is detected by accident. Build a stdlib-only read-only checker (tasks/board_check.py) reporting GHOST open-tasks absent from board, STALE-ACTIVE board headers for CLOSED tasks, UNKNOWN board ids, BADFILE frontmatter, MISFILED closed-state files. Never writes the board (orchestrator-only writes). Lane: C1-CURSOR in scratch repo C:\bari_scratch_board off registry copies.
---

# TASK-556 — board_check.py: read-only registry-to-DISPATCH_BOARD drift checker

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
