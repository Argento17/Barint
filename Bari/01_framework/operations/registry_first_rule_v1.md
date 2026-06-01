<!-- MOVED — canonical version now at C:\Bari\01_framework\operations\registry_first_rule_v1.md
     (the real Agent OS that all agents load). This copy is NON-AUTHORITATIVE. Authoritative
     registry: C:\Bari\tasks\ — not the markdown task_registry_v1.md referenced below. (TASK-117) -->

# Registry First Rule — v1  (NON-AUTHORITATIVE COPY — see C:\Bari)

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31
**Scope:** All agents and the Central Controller, for any task-management request
**Builds on:** [`registry_protocol_v1.md`](./registry_protocol_v1.md) (lifecycle) · [`command_center_registry_support_v1.md`](./command_center_registry_support_v1.md) (dashboard)
**Authoritative store:** [`task_registry_v1.md`](./task_registry_v1.md)
**Created by:** TASK-116 (Product Agent)

> This rule adds **no new lifecycle states** and **does not redesign the registry**. It governs *where an agent gets the answer* before acting on a task-management request.

---

## 1. The governance gap

TASK-114 defined the lifecycle and return protocol; TASK-115 made the dashboard read the registry. One gap remains: an agent can still answer a task-management request from **conversation memory** ("I closed that earlier", "it was returned") instead of the registry. Conversation history is lossy, per-session, and not shared across agents — answering from it reintroduces the drift the protocol exists to remove.

---

## 2. The rule

**Any request involving a task identity must begin by consulting the registry.** Trigger forms include:

- `TASK-XXX` (any reference)
- `Status TASK-XXX`
- `Close TASK-XXX`
- `Accept TASK-XXX`
- `Reject TASK-XXX` / Changes Requested
- `Block TASK-XXX`
- `Resume TASK-XXX`
- `Reopen TASK-XXX`

**The registry is authoritative. Conversation history is not authoritative.**
Conversation may *prompt* a request; it never *substitutes* for the recorded state. If the registry and the conversation disagree, the registry wins and the discrepancy is surfaced, not silently resolved.

---

## 3. Operating sequence (every task-management request)

```
1. CONSULT  — read task_registry_v1.md; locate the TASK-XXX entry and its recorded state.
2. VERIFY   — confirm the requester's authority for the action (see §4) and that the
              recorded state permits the transition (per registry_protocol_v1.md).
3. ACT      — perform only what the recorded state + authority allow.
4. RECORD   — write the resulting state change to the registry (Central Controller only),
              or, for an agent, emit the Registry Update (proposed) block.
```

If the task is **not in the registry**, say so ("TASK-XXX is not registered") — do not reconstruct its state from memory.

---

## 4. Expected behavior by operation

### 4.1 Task lookup / status request — `Status TASK-XXX`
- **Consult first.** Answer with the **recorded** state and its dashboard section (Active Work / Awaiting Review / Blockers / Changes Requested / Closed).
- If absent → "not registered." Never infer status from chat.
- Any agent may perform a lookup (read-only).

### 4.2 Task closure — `Close TASK-XXX`
- Consult first. **Central Controller only** records `CLOSED`.
- An agent receiving a close request must decline to record it and instead propose `RETURNED` (agents never close their own work — Registry Protocol v1).
- Controller verifies the recorded state is `RETURNED` before closing. If it is not (e.g. still `IN_PROGRESS`), do **not** close on a memory claim that "it was returned" — surface the gap and obtain a return first.

### 4.3 Task acceptance — `Accept TASK-XXX`
- Consult first. **Central Controller only.**
- Precondition: recorded state is `RETURNED`. On accept → record the acceptance block (`CLOSED` + accepted date) and move Active → Closed table.
- If the registry shows the task is not `RETURNED`, acceptance is invalid regardless of what the conversation asserts.

### 4.4 Task rejection — `Reject TASK-XXX` / request changes
- Consult first. **Central Controller only.**
- Precondition: recorded state is `RETURNED`. On reject → record `CHANGES_REQUESTED` + reason. When work resumes the state becomes `IN_PROGRESS`.

### 4.5 Block / Resume / Reopen
- **Block** — consult first; an agent proposes `BLOCKED` (with the named dependency) in its return; the Controller records it.
- **Resume** — consult first; from `CHANGES_REQUESTED` or `BLOCKED`, the Controller records `IN_PROGRESS`.
- **Reopen** — `CLOSED` is terminal; only the Central Controller reopens, recording the new state with a note. Consult the registry to confirm the task is actually `CLOSED` first.

---

## 5. Examples

### 5.1 Status request — correct
> **Request:** "What's the status of TASK-100?"
> **Agent:** *Reads `task_registry_v1.md`.* "Recorded state: `IN_PROGRESS` (Active Work). Agent: Frontend Agent."

### 5.2 Status request — violation
> **Request:** "What's the status of TASK-100?"
> **Agent (wrong):** "I think we finished that earlier, so it's done."
> ✗ Answered from memory, not the registry. The registry shows `IN_PROGRESS`.

### 5.3 Closure — authority + precondition
> **Request:** "Close TASK-114."
> **Controller:** *Consults registry → TASK-114 is `RETURNED`.* Records `CLOSED` + accepted date; moves Active → Closed.
> **If an agent receives this:** "I can't close work — proposing `RETURNED`; closure is the Central Controller's action."

### 5.4 Acceptance — registry overrides conversation
> **Request:** "Accept TASK-102, we discussed it's done."
> **Controller:** *Consults registry → TASK-102 is `IN_PROGRESS`, no return on record.* "TASK-102 is not `RETURNED` in the registry — there's no recorded return to accept. Need the assigned agent's `RETURNED` proposal first."

### 5.5 Rejection
> **Request:** "Reject TASK-101 — copy leaks weight vocabulary."
> **Controller:** *Consults registry → `RETURNED`.* Records `CHANGES_REQUESTED` with that reason. On resume → `IN_PROGRESS`.

### 5.6 Unknown task
> **Request:** "Status TASK-130?"
> **Agent:** *Consults registry → not found.* "TASK-130 is not registered."

---

## 6. Enforcement

- Answering a task-management request **without** consulting the registry is a protocol violation, even if the answer happens to be correct.
- When conversation and registry conflict, the **registry is authoritative**; the agent reports the conflict rather than acting on memory.
- This rule is referenced from Agent OS guidance (`AGENTS.md`), the operating model (`operating_model_v2.md` §7), and Registry Protocol v1 so it loads into every agent's context.

---

*Registry First Rule v1 — Bari / 2026-05-31*
