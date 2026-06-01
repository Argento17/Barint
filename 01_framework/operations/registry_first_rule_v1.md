# Registry First Rule — v1

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31 (relocated to the Agent OS under TASK-117)
**Scope:** All agents and the Central Controller, for any task-management request
**Authoritative registry:** `C:\Bari\tasks\` (one `TASK-NNN.md` per task; state in YAML frontmatter)
**Related:** [`work_classification_v1.md`](./work_classification_v1.md) · [`registry_protocol_v1.md`](./registry_protocol_v1.md)

> Adds **no new lifecycle states** and does **not** redesign the registry. It governs *where an agent gets the answer* before acting on a task-management request.

---

## 1. The rule

**Any request involving a task identity must begin by consulting the registry.** Trigger forms:

`TASK-XXX` (any reference) · `Status TASK-XXX` · `Close TASK-XXX` · `Accept TASK-XXX` · `Reject TASK-XXX` · `Block TASK-XXX` · `Resume TASK-XXX` · `Reopen TASK-XXX`

**The registry (`C:\Bari\tasks\`) is authoritative. Conversation history is not.**
Conversation may *prompt* a request; it never *substitutes* for the recorded state. If the registry and the conversation disagree, the registry wins and the discrepancy is surfaced, not silently resolved.

(Requests with no task identity are usually **Conversation Work** — handle them inline; see [`work_classification_v1.md`](./work_classification_v1.md).)

---

## 2. Operating sequence (every task-management request)

```
1. CONSULT — read C:\Bari\tasks\TASK-XXX.md; locate the `status:` frontmatter (recorded state).
2. VERIFY  — confirm the requester's authority (§3) and that the recorded state permits
             the transition (per registry_protocol_v1.md).
3. ACT     — perform only what the recorded state + authority allow.
4. RECORD  — Controller edits the frontmatter + re-runs generate_dashboard.py; an agent
             instead emits the Registry Update (proposed) block.
```

If `C:\Bari\tasks\TASK-XXX.md` does not exist → say "TASK-XXX is not registered." Never reconstruct state from memory.

---

## 3. Expected behavior by operation

- **Lookup / `Status`** — Consult first; answer with the recorded state and its dashboard section. Absent → "not registered." Any agent may look up (read-only).
- **Close** — Consult first. **Central Controller only.** An agent receiving a close request declines and proposes `RETURNED`. The Controller verifies the recorded state is `RETURNED` before closing; if it is not, surface the gap rather than closing on a memory claim.
- **Accept** — Controller only. Precondition: recorded `RETURNED` → set `status: CLOSED` + `completed_at`. If not `RETURNED` in the registry, acceptance is invalid regardless of what the conversation asserts.
- **Reject** — Controller only. Precondition: recorded `RETURNED` → set `status: CHANGES_REQUESTED` + reason. On resume → `IN_PROGRESS`.
- **Block / Resume / Reopen** — Consult first. Agent proposes `BLOCKED`; Controller records. Resume from `CHANGES_REQUESTED`/`BLOCKED` → `IN_PROGRESS`. `CLOSED` is terminal; only the Controller reopens, after confirming the file is actually `CLOSED`.

---

## 4. Examples

- **Correct status:** *Reads `tasks/TASK-115.md`.* "Recorded state: `IN_PROGRESS` (Active Work)." 
- **Violation:** "I think we finished that earlier, so it's done." ✗ answered from memory, not the file.
- **Close (new chat):** "Close TASK-114." → *Consult `tasks/TASK-114.md` → `CLOSED`.* "TASK-114 is already `CLOSED` (accepted 2026-05-31) — no action needed." (The registry decides validity, not the conversation.)
- **Accept overridden by registry:** "Accept TASK-102, we said it's done." → *Consult → `CLOSED` already, or not `RETURNED`* → respond from the recorded state, not the claim.
- **Unknown:** "Status TASK-130?" → *not found* → "TASK-130 is not registered."

---

## 5. Notes

- Answering a task-management request **without** consulting the registry is a protocol violation, even if the answer happens to be correct.
- The registry is the single source of truth; a state asserted in chat or a handoff doc is not binding until the Controller records it in `C:\Bari\tasks\`.
- This is a lightweight, convention-based rule — there is no CI/enforcement gate. Agents and the Controller follow it because the operating model requires it.

---

*Registry First Rule v1 — Bari Agent OS / 2026-05-31*
