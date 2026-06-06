# ADR-003 — Extended close guard: HIGH priority + go-live tasks hard-blocked without CC verification

**Status:** Accepted  
**Date:** 2026-06-04  
**Deciders:** CC Agent (autonomous, no tripwire fired)  
**Supersedes:** none (extends existing guard-roadmap-close.ps1)

---

## Context

The existing `guard-roadmap-close.ps1` PreToolUse hook hard-blocked closing a task with `roadmap_impact: true` and no `cc_reviewed` date. This closed the enforcement gap for explicitly flagged tasks.

The remaining gap: tasks without `roadmap_impact: true` — including HIGH priority single-category deliverables, score swaps, and frontend go-lives — could be closed without any CC verification. A task being HIGH priority and not roadmap-impacting is the normal case for most tracked work. The gate was therefore advisory for the majority of tasks that most need verification.

Additionally, there was no machine enforcement of the red-team requirement for go-live tasks.

---

## Decision

Extend the guard to three hard blocks and two advisory warnings:

**Hard blocks (exit 2 — denies close):**
1. `roadmap_impact: true` + no `cc_reviewed` — existing
2. `priority: HIGH` + no `cc_reviewed` — new: closes the primary enforcement gap
3. `work_type: go_live|launch` + no `red_team_cleared` — new: enforces red-team gate

**Advisory warnings (exit 0 — allows write but model sees the message):**
4. No `close_reason` on any CLOSED task
5. No `cc_reviewed` on any other CLOSED task (soft nudge for Conversation Work boundaries)

---

## Reasoning chain

1. **Constraint:** `SubagentStop` cannot spawn agents — the gate must be a PreToolUse hook on the write, not a hook reaction to the agent's return.
2. **Option A — status quo:** Only roadmap_impact tasks are hard-blocked. Most HIGH priority closes go unverified.
3. **Option B — hard-block all closes without cc_reviewed:** Correct in principle but breaks Conversation Work (minor admin tasks, typo fixes) that get CLOSED without a full CC gate. Excessive friction.
4. **Option C — hard-block HIGH + go-live only; advisory others (this ruling):** HIGH priority is already the proxy the system uses for "this matters enough to track carefully." If a task is HIGH and the agent claims it's done, CC should verify. Go-live is an irreversible consumer-facing action — always needs the red-team gate. Everything else gets an advisory.
5. **Tiebreaker:** Option C adds meaningful protection where risk is highest (HIGH priority deliverables) while avoiding false friction on low-stakes closes (CLOSED status on a clarification task).

---

## Consequences

**Positive:**
- HIGH priority score swaps, frontend ships, content launches now require CC verification before close — not just roadmap-flagged ones.
- Go-live tasks are machine-blocked without `red_team_cleared` — the red-team gate is now enforced, not just documented.
- Advisory nudges build the habit of `close_reason` and `cc_reviewed` for lower-stakes tasks without blocking them.

**Negative / trade-offs:**
- A trivial task inadvertently marked HIGH will block until either CC verifies or priority is downgraded. Mitigation: the block message explicitly says to downgrade priority if this is the case.
- `red_team_cleared` is a new frontmatter field — not yet present on legacy task files. Only gates tasks with `work_type: go_live`, which is a forward-looking convention.

**Follow-up required:**
- [ ] Add `red_team_cleared:` to the task template / new_task.py for go-live tasks
- [ ] Update cc-agent.md to note HIGH priority tasks now require cc_reviewed before close
- [ ] Run validate_agents.py to confirm schema still clean after guard change

---

## Tripwire evaluation

| Tripwire | Fired? | Note |
|---|---|---|
| 1. Frozen invariant / published scores | No | Guard change does not touch scores |
| 2. Irreversible AND consumer-facing | No | Internal tooling change |
| 3. Starts or kills a major program | No | |
| 4. External commitment / spend / legal | No | |
| 5. Redefines strategy / target user | No | |

---

## Reversibility

- **Door type:** two-way
- **Rollback path:** Revert guard-roadmap-close.ps1 to v1 content (git history).

---

## Related

- `.claude/hooks/guard-roadmap-close.ps1` — implementation
- ADR-002 — CC closing authority (this extends it)
- `.claude/agents/red-team-agent.md` — red_team_cleared gate definition
- `.claude/agents/qa-agent.md` — Hard Rule 9 (QA side of the same requirement)
