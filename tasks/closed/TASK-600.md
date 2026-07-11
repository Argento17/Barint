---
id: TASK-600
title: Router v5.2: orchestrator default = Opus 4.8; SST (Fable/Sol) only via /stf
owner: data-agent
status: CLOSED
close_reason: >
  Router v5.2 live. Layer-0 invariant 10 added: orchestrator/main-loop default = claude-opus-4-8
  ALWAYS; SST (Fable/Sol) engages ONLY via STRATEGY-CONSULT (/stf), never ambient; Opus stays QA.
  STRATEGY-CONSULT Claude seat re-specced to claude-fable-5 EXPLICIT (Fable-pinned participant, not
  the now-Opus ambient session). Orchestrator verified: C0 PASS, selftests re-run green in lane
  worktree + merge worktree + local (table byte-match, route 15/15, telemetry), invariant-10 diff
  read. Speed-1 internal merge origin/master e100b686 -> 92cf5acb; local port done same cycle (both
  law files synced byte-exact, selftests green locally). Governance capture (orchestrator's hands):
  memory strategist_tier_sol_fable.md, /stf skill (two-seat model: Opus chairs, Fable subagent +
  Sol debate), CLAUDE.md model-routing section.
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  OWNER RULING 2026-07-11: default mode for the orchestrator is ALWAYS claude-opus-4-8. The SST strategist tier (Fable 5 + Sol 5.6) engages ONLY when the /stf (Strategy Task Force) skill is invoked. Router edits: (1) Layer-0 new invariant - orchestrator/main-loop default pin = claude-opus-4-8; SST models engage ONLY via the STRATEGY-CONSULT capability (the /stf skill), never as the ambient session; (2) Layer-2 STRATEGY-CONSULT row: Claude seat = claude-fable-5 EXPLICIT (obtained via a Fable-pinned participant, since the orchestrator is now Opus - update the old 'orchestrator session itself = Fable 5' note), GPT seat = gpt-5.6-sol read-only unchanged; (3) dispatch.py doc-mirror + any comment; all selftests green (table byte-match, route 15, telemetry). BUILD-LIGHT terra.
---

# TASK-600 — Router v5.2: orchestrator default = Opus 4.8; SST (Fable/Sol) only via /stf

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
