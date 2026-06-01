<!-- MOVED — canonical governance now lives in the Agent OS at C:\Bari\01_framework\operations\
     (see registry_protocol_v1.md §5 for state→section routing). This copy is NON-AUTHORITATIVE.
     The dashboard routing it describes is implemented in C:\Bari\05_command_center\generate_dashboard.py
     + command_center_v4.html. Authoritative registry: C:\Bari\tasks\. (TASK-117) -->

# Command Center — Registry Protocol v1 Support  (NON-AUTHORITATIVE COPY)

**Status:** Active
**Date:** 2026-05-31
**Scope:** Command Center dashboard behavior against Registry Protocol v1
**Source of truth:** [`registry_protocol_v1.md`](./registry_protocol_v1.md) (lifecycle) + [`task_registry_v1.md`](./task_registry_v1.md) (state data)
**Created by:** TASK-115 (Frontend Agent)
**Reference render:** [`/command-center/index.html`](../../../command-center/index.html)

> This is **not** a new lifecycle model and **not** a dashboard redesign. It maps the five states already defined in Registry Protocol v1 onto the existing Command Center concept ([`visual_wireframe_v1.md`](../frontend/visual_wireframe_v1.md) §5).

---

## 1. Supported lifecycle states

Exactly the five states from Registry Protocol v1 — no additions:

`IN_PROGRESS` · `BLOCKED` · `RETURNED` · `CHANGES_REQUESTED` · `CLOSED`

---

## 2. Section model (state → dashboard section)

| Operational section | Shows state | Rule |
|---------------------|-------------|------|
| **Active Work** | `IN_PROGRESS` | Only IN_PROGRESS. Nothing else. |
| **Awaiting Review** | `RETURNED` | Work delivered, pending Central Controller review. |
| **Blockers** | `BLOCKED` | Waiting on a named dependency. |
| **Changes Requested** | `CHANGES_REQUESTED` | Returned for rework. |
| *(Closed archive)* | `CLOSED` | **Excluded from all operational sections.** May appear only in a non-operational closed-count / archive view. |

Each task appears in **exactly one** section, determined solely by its current recorded state. A task with no recognized state is surfaced in an **Unrecognized** tray (never silently dropped).

---

## 3. Registry read contract

1. **Recorded state only.** Command Center renders the state the Central Controller has **recorded** in `task_registry_v1.md`. A `Proposed State` inside an agent's `Registry Update (proposed)` block is **not** a dashboard state until the Controller records it.
   - A return proposing `RETURNED` → renders as `RETURNED` **once the Controller records it**.
   - A return proposing `BLOCKED` → renders as `BLOCKED` **once the Controller records it**.
   - Only **Central Controller acceptance** moves a task to `CLOSED`.
2. **Where state is read from.**
   - **Active Tasks** entries: the `**Status:**` line under each `### TASK-NNN` heading.
   - **Recently Closed Tasks** table rows: treated as `CLOSED`.
3. **Status normalization.** The `**Status:**` value is matched case-insensitively to a lifecycle state. Trailing prose after the state is ignored (e.g. `RETURNED — awaiting Central Controller acceptance` → `RETURNED`).
4. **Legacy alias.** Pre-protocol entries labeled `ACTIVE` are read as `IN_PROGRESS` (the only legacy alias). New and migrated entries should use explicit lifecycle states.

---

## 4. Chip conventions

Extends the wireframe status chips ([`visual_wireframe_v1.md`](../frontend/visual_wireframe_v1.md) §5.2) — reuses existing colors, adds the two states the wireframe lacked. No restyling of existing chips.

| State | Color | Label | Source |
|-------|-------|-------|--------|
| `IN_PROGRESS` | `#CC785C` | ⬡ IN PROGRESS | wireframe (PIPELINE ACTIVE hue) |
| `BLOCKED` | `#DC2626` | ✗ BLOCKED | wireframe (unchanged) |
| `RETURNED` | `#2D3561` | ⊟ AWAITING REVIEW | wireframe (QA REVIEW hue) |
| `CHANGES_REQUESTED` | `#B45309` | ↺ CHANGES REQUESTED | new (amber, distinct from BLOCKED red) |
| `CLOSED` | `#059669` | ✓ CLOSED | wireframe (LIVE hue) |

---

## 5. Acceptance criteria

- Active Work lists **only** `IN_PROGRESS` tasks.
- Awaiting Review lists **only** `RETURNED` tasks.
- Blockers lists **only** `BLOCKED` tasks.
- Changes Requested lists **only** `CHANGES_REQUESTED` tasks.
- No `CLOSED` task appears in any operational section.
- A proposed state never changes the dashboard until the Controller records it.
- Changing a task's `**Status:**` in the registry and re-reading moves it between sections with no other edits.

---

## 6. Current registry projection (verification)

Applying §2–§3 to `task_registry_v1.md` as of 2026-05-31:

| Section | Tasks |
|---------|-------|
| Active Work (`IN_PROGRESS`) | TASK-100, TASK-101*, TASK-102 — read via legacy `ACTIVE` alias |
| Awaiting Review (`RETURNED`) | TASK-114 |
| Blockers (`BLOCKED`) | — |
| Changes Requested (`CHANGES_REQUESTED`) | — |
| Closed archive (`CLOSED`, non-operational) | TASK-086, 087A, 087B, 087C, 089, 089A, 090, 091, 094, 095 |

\* TASK-101's `**Status:**` is `ACTIVE`; its dependency on TASK-100 is noted in its Blockers field but it has not been **recorded** as `BLOCKED`, so it renders under Active Work. Re-recording its status to `BLOCKED` would move it to the Blockers section — illustrating that section membership follows recorded state, not prose.

---

*Command Center — Registry Protocol v1 Support / Bari / 2026-05-31*
