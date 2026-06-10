# ADR-004 — Deprecate Command Center Operational Layer

**Status:** Decided  
**Date:** 2026-06-10  
**Authority:** Owner directive  
**Supersedes:** ADR-002 (CC closing authority), ADR-003 (extended close guard)

---

## Decision

The Command Center operational layer is deprecated. The CC Agent, the
`guard-roadmap-close.ps1` PreToolUse hook, and the `regen-dashboard-on-task-change.ps1`
PostToolUse hook are all retired.

The registry (`C:\Bari\tasks\`) remains the single source of truth for all task state.
Closing authority and verification discipline move directly to the orchestrator (main chat).

---

## Context

The Command Center was built to solve dashboard drift — tasks staying `IN_PROGRESS` after
work was done — and to enforce verification before closure. Over time it grew into a
mandatory routing layer: every deliverable had to pass through a separate CC Agent before
the orchestrator could close it. The `cc_reviewed` field became a hard block (enforced by
a PreToolUse hook) on HIGH-priority and `roadmap_impact` tasks.

The layer added coordination cost without proportional governance value:

- The CC Agent and the orchestrator were solving the same problem (verify and close) but
  the orchestrator was already equipped to do it directly.
- The PreToolUse hard-block on closes introduced friction for routine work and was often
  worked around by downgrading priority labels.
- Dashboard generation was triggered after every task write, adding latency and coupling
  the registry to a derived artifact on every edit.

---

## What changes

| Before | After |
|---|---|
| CC Agent verifies and closes | Orchestrator (main chat) verifies and closes directly |
| `cc_reviewed` required to close HIGH / roadmap_impact tasks | `close_reason` with cited evidence required to close any task |
| PreToolUse hook hard-blocks closes | No close guard hook; verification is a discipline, not a gate |
| PostToolUse hook regenerates dashboard on every task write | No auto-regen; run `generate_dashboard.py` manually when needed |
| `/cc` routes to CC Agent | `/cc` is a direct registry operation command |
| `/roadmap` routes through CC Agent reading lean JSON | `/roadmap` reads `tasks/TASK-*.md` directly |
| `roadmap_impact: true` triggers ROADMAP_REVIEW alert and CC nudge | `roadmap_impact: true` is informational only; orchestrator reviews as part of close |

---

## What is preserved

- **Registry as source of truth.** `C:\Bari\tasks\TASK-*.md` remains authoritative.
- **Task lifecycle states.** `IN_PROGRESS · BLOCKED · RETURNED · CHANGES_REQUESTED · CLOSED` — unchanged.
- **"Verify before closing" discipline.** The orchestrator reads each return-block claim against
  the actual artifact before writing `CLOSED`. The gate is not removed — it's just not enforced
  by a separate agent or hook.
- **Close-reason requirement.** All CLOSED tasks carry `close_reason` citing evidence.
- **Archive discipline.** CLOSED tasks move from `tasks/` to `tasks/closed/`.
- **Agent return format.** Domain agents still propose `RETURNED`/`BLOCKED`; never `CLOSED`.
- **Red-team gate for go-live tasks.** Still required; confirmed by the orchestrator before closing
  any `work_type: go_live` task.
- **Adversarial review for high-stakes work.** Still recommended; confirmed by the orchestrator.
- **5-part delegation spec.** Still the standard for agent hand-offs.
- **Autonomy default.** Still governs; 5 tripwires still reach the owner.

---

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Orchestrator skips verification and closes on prose | `close_reason` field required; this is now a registry discipline rather than a mechanical gate |
| Dashboard goes stale | Run `generate_dashboard.py` manually when a visual board is needed; the registry is always correct |
| Historical tasks with `cc_reviewed` fields become confusing | Those fields remain in closed-task frontmatter as historical record; they have no enforcement meaning going forward |

---

## Files changed

- `CLAUDE.md` — tasks & registry section + orchestration section + decision authority section
- `.claude/agents/cc-agent.md` — marked DEPRECATED v3.0
- `.claude/commands/cc.md` — rewritten as direct registry operation
- `.claude/commands/roadmap.md` — rewritten to read registry directly
- `.claude/settings.json` — removed `guard-roadmap-close.ps1` (PreToolUse) and `regen-dashboard-on-task-change.ps1` (PostToolUse)
- `01_framework/operations/orchestration_model_v1.md` — CC gate removed; verify-before-close is orchestrator responsibility
- `01_framework/operations/registry_protocol_v1.md` — closing authority updated to "orchestrator"
- `01_framework/operations/agent_router_v1.md` — cc-agent removed from routing table
- `01_framework/governance/decision_authority_matrix_v1.md` — CC removed from ownership tiers; v1.1
