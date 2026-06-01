# Registry Protocol — v1

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31 (relocated to the Agent OS under TASK-117)
**Scope:** All agent task work across Agent OS (Frontend, Content/CE, Data, Product, QA agents)
**Authority:** Governs how task state is reported and recorded in the authoritative registry.
**Related:** [`work_classification_v1.md`](./work_classification_v1.md) · [`registry_first_rule_v1.md`](./registry_first_rule_v1.md) · [`operating_model_v2.md`](./operating_model_v2.md)

---

## 0. Authoritative registry (single source of truth)

**`C:\Bari\tasks\` — one `TASK-NNN.md` file per task; state lives in the YAML frontmatter `status:` field.**

`generate_dashboard.py` reads these files → `command_center.json` → the dashboard. There is exactly one registry. (The former markdown registry at `C:\bari\bari-web\Bari\01_framework\operations\task_registry_v1.md` is a frozen, non-authoritative historical snapshot — do not edit or consult it for live state.)

This protocol applies only to **Registry Work** (see [`work_classification_v1.md`](./work_classification_v1.md)). Conversation Work never enters the registry.

---

## 1. Why this exists

Agents return deliverables but do not report structured state. The result is **dashboard drift**: tasks read `IN_PROGRESS` after the work is done, and the Central Controller manually reconstructs what changed. This protocol removes the reconstruction step: **every task return ends with a structured Registry Update block**, and the Controller records it. **Only the Central Controller writes `CLOSED`.** Agents *propose*; the Controller *commits*.

---

## 2. Lifecycle states (no new states; do not redesign)

| State | Meaning | Entered by | Terminal? |
|-------|---------|-----------|-----------|
| `IN_PROGRESS` | Agent actively working | Controller (on assignment / on resume) | no |
| `BLOCKED` | Waiting on a named dependency | Controller (from an agent's proposed `BLOCKED`) | no |
| `RETURNED` | Work delivered, awaiting review — **not complete** | Controller (from an agent's proposed `RETURNED`) | no |
| `CHANGES_REQUESTED` | Returned for rework | Controller (on rejection) | no |
| `CLOSED` | Explicitly accepted by the Central Controller | **Controller only** (on acceptance) | **yes** |

```
   assign        propose RETURNED        accept (Controller only)
  ───────► IN_PROGRESS ─────────────► RETURNED ──────────────────► CLOSED
              ▲   │                       │
    resume    │   │ propose BLOCKED       │ request changes
              │   ▼                       ▼
              │  BLOCKED            CHANGES_REQUESTED
              └───┴── resume → IN_PROGRESS ──┘
```

- An agent leaves `IN_PROGRESS` only by *proposing* `RETURNED` or `BLOCKED` in its return block. The Controller records it.
- `RETURNED → CLOSED` and `RETURNED → CHANGES_REQUESTED` are **Controller-only**.
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

**Rules:** Agents may propose `RETURNED` or `BLOCKED`. Agents may **never** propose `CLOSED` / `ACCEPTED`. Only the Central Controller closes work.

---

## 4. How state is recorded (the Controller, in `C:\Bari\tasks\`)

State is recorded by editing the task file's frontmatter, then regenerating the dashboard:

- **Accept:** set `status: CLOSED` and `completed_at: YYYY-MM-DD` in `tasks/TASK-NNN.md`.
- **Reject:** set `status: CHANGES_REQUESTED` (capture the reason in the body / return).
- **Return / Block (recording an agent proposal):** set `status: RETURNED` or `status: BLOCKED`.
- **Resume:** set `status: IN_PROGRESS`.

Then run `python generate_dashboard.py` (in `05_command_center`) so the dashboard reflects the change. The dashboard is **derived** — never hand-edit `command_center.json`.

### Controller acceptance block
```
--- Registry Update ---
Task: TASK-NNN
New State:
- CLOSED
Accepted Date:
- YYYY-MM-DD
Notes:
- optional
```

### Controller rejection block
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

## 5. Command Center behavior (state → section)

The dashboard renders state directly from the registry frontmatter:

| State | Section |
|-------|---------|
| `IN_PROGRESS` | Active Work |
| `RETURNED` | Awaiting Review |
| `BLOCKED` | Blockers |
| `CHANGES_REQUESTED` | Changes Requested |
| `CLOSED` | excluded from operational sections (closed/history only) |

A done-but-unaccepted task reads `RETURNED`, not `IN_PROGRESS` — the specific drift this protocol eliminates.

---

## 6. Ownership

| Action | Owner |
|--------|-------|
| Classify the request (Conversation vs Registry Work) | Whoever receives it |
| Register `tasks/TASK-NNN.md` when Registry Work begins | Assigned agent / Controller |
| Emit `Registry Update (proposed)` on every return | **Assigned agent** |
| Propose `RETURNED` / `BLOCKED` | Assigned agent |
| Record state in the registry frontmatter | **Central Controller** |
| `CLOSED` / `ACCEPTED` transition | **Central Controller (sole authority)** |

No agent self-closes its own work.

---

*Registry Protocol v1 — Bari Agent OS / 2026-05-31*
