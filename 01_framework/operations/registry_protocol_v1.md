# Registry Protocol — v1

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31 (relocated to the Agent OS under TASK-117; updated 2026-06-10 — CC layer removed)
**Scope:** All agent task work across Agent OS (Frontend, Content/CE, Data, Product, QA agents)
**Authority:** Governs how task state is reported and recorded in the authoritative registry.
**Related:** [`work_classification_v1.md`](./work_classification_v1.md) · [`registry_first_rule_v1.md`](./registry_first_rule_v1.md) · [`orchestration_model_v1.md`](./orchestration_model_v1.md)

---

## 0. Authoritative registry (single source of truth)

**`C:\Bari\tasks\` — one `TASK-NNN.md` file per task; state lives in the YAML frontmatter `status:` field.**

The registry is the single source of truth. (The former markdown registry at `C:\bari\bari-web\Bari\01_framework\operations\task_registry_v1.md` is a frozen, non-authoritative historical snapshot — do not edit or consult it for live state.)

This protocol applies only to **Registry Work** (see [`work_classification_v1.md`](./work_classification_v1.md)). Conversation Work never enters the registry.

---

## 1. Why this exists

Agents return deliverables but do not report structured state. The result is **dashboard drift**: tasks read `IN_PROGRESS` after the work is done, and the orchestrator manually reconstructs what changed. This protocol removes the reconstruction step: **every task return ends with a structured Registry Update block**, and the orchestrator records it. **Domain agents never write `CLOSED`** — they *propose*, the orchestrator *commits*. **Closing authority is the orchestrator (main chat)**, which records `CLOSED` only after verifying return-block claims against artifacts.

---

## 2. Lifecycle states (no new states; do not redesign)

| State | Meaning | Entered by | Terminal? |
|-------|---------|-----------|-----------|
| `IN_PROGRESS` | Agent actively working | Orchestrator (on assignment / on resume) | no |
| `BLOCKED` | Waiting on a named dependency | Orchestrator (from an agent's proposed `BLOCKED`) | no |
| `RETURNED` | Work delivered, awaiting review — **not complete** | Orchestrator (from an agent's proposed `RETURNED`) | no |
| `CHANGES_REQUESTED` | Returned for rework | Orchestrator (on rejection) | no |
| `CLOSED` | Explicitly accepted by the orchestrator | **Orchestrator only** (on acceptance) | **yes** |

```
   assign        propose RETURNED        accept (Orchestrator only)
  ───────► IN_PROGRESS ─────────────► RETURNED ──────────────────► CLOSED
              ▲   │                       │
    resume    │   │ propose BLOCKED       │ request changes
              │   ▼                       ▼
              │  BLOCKED            CHANGES_REQUESTED
              └───┴── resume → IN_PROGRESS ──┘
```

- An agent leaves `IN_PROGRESS` only by *proposing* `RETURNED` or `BLOCKED` in its return block. The orchestrator records it.
- `RETURNED → CLOSED` and `RETURNED → CHANGES_REQUESTED` are **orchestrator-only**.
- `CHANGES_REQUESTED → IN_PROGRESS` on resume; `BLOCKED → IN_PROGRESS` when the dependency clears.

---

## 3. Required agent return format (MANDATORY)

Every task return ends with this block, verbatim structure:

```
--- Registry Update (proposed) ---

Task: TASK-NNN

Proposed State:
- RETURNED
or
- BLOCKED

Deliverables Produced:
- item

Artifacts:
- file/path

Blockers:
- none
or
- blocker description

Recommended Next Action:
- Accept
or
- Changes Requested
or
- Open TASK-XXX
```

**Rules:** Agents may propose `RETURNED` or `BLOCKED`. Agents may **never** propose `CLOSED` / `ACCEPTED`. Only the orchestrator closes work.

---

## 4. How state is recorded (the orchestrator, in `C:\Bari\tasks\`)

State is recorded by editing the task file's frontmatter:

- **Accept / Close:** set `status: CLOSED`, `completed_at: YYYY-MM-DD`, and `close_reason: <one-line citing evidence>` in `tasks/TASK-NNN.md`. Move the file to `tasks/closed/TASK-NNN.md`.
- **Reject:** set `status: CHANGES_REQUESTED` (capture the reason in the body / return).
- **Return / Block (recording an agent proposal):** set `status: RETURNED` or `status: BLOCKED`.
- **Resume:** set `status: IN_PROGRESS`.

### Closing discipline

Before writing `CLOSED`, the orchestrator verifies the claims:

1. Re-read the DoD in the task file; list each exit criterion.
2. Check each claim against the artifact — quote file:line / the real number. If an artifact doesn't exist or contradicts the claim → `CHANGES_REQUESTED` with the gap.
3. Look for what the return did NOT say (silent side-effects). Surface them in `close_reason` or as a follow-up task.
4. High-stakes work (live score swap, frozen-invariant, governance) → get a second-agent review before closing.

### Orchestrator close block
```
--- Registry Update ---
Task: TASK-NNN
New State:
- CLOSED
Accepted Date:
- YYYY-MM-DD
Close Reason:
- <artifact checked: file:line / run output>
```

### Orchestrator rejection block
```
--- Registry Update ---
Task: TASK-NNN
New State:
- CHANGES_REQUESTED
Reason:
- explanation
```
On resume the state becomes `IN_PROGRESS`.

---

## 5. Task sections in the registry (state → section)

The registry renders state directly from the frontmatter:

| State | Section |
|-------|---------|
| `IN_PROGRESS` | Active Work |
| `RETURNED` | Awaiting Review |
| `BLOCKED` | Blockers |
| `CHANGES_REQUESTED` | Changes Requested |
| `CLOSED` | Archive (`tasks/closed/`) |

A done-but-unaccepted task reads `RETURNED`, not `IN_PROGRESS` — the specific drift this protocol eliminates.

---

## 6. Ownership

| Action | Owner |
|--------|-------|
| Classify the request (Conversation vs Registry Work) | Whoever receives it |
| Register `tasks/TASK-NNN.md` when Registry Work begins | Assigned agent / Orchestrator |
| Emit `Registry Update (proposed)` on every return | **Assigned agent** |
| Propose `RETURNED` / `BLOCKED` | Assigned agent |
| Record state in the registry frontmatter | **Orchestrator** |
| `CLOSED` / `ACCEPTED` transition | **Orchestrator (sole authority)** |

No agent self-closes its own work.

---

*Registry Protocol v1 — Bari Agent OS / 2026-05-31 · updated 2026-06-10*
