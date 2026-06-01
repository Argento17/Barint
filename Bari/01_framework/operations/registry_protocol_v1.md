<!-- MOVED — canonical version now at C:\Bari\01_framework\operations\registry_protocol_v1.md
     (the real Agent OS that all agents load). This copy is NON-AUTHORITATIVE. Authoritative
     registry: C:\Bari\tasks\ — not the markdown task_registry_v1.md referenced below. (TASK-117) -->

# Registry Protocol — v1  (NON-AUTHORITATIVE COPY — see C:\Bari)

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31
**Scope:** All agent task work across Agent OS (Frontend, Content/CE, Data, Product, QA agents)
**Authority:** Governs how task state is reported and recorded in [`task_registry_v1.md`](./task_registry_v1.md). Role authority is defined by [`operating_model_v2.md`](./operating_model_v2.md).
**Created by:** TASK-114 (Product Agent)

---

## 1. Why this exists

Agents return deliverables but do not report structured state. The result is **dashboard drift**: tasks remain `IN_PROGRESS` after the work is done, and the Central Controller manually reconstructs what changed before it can update the registry.

This protocol removes the reconstruction step. **Every task return ends with a structured Registry Update block.** The Central Controller reads that block and records state — it never has to re-derive it.

**Single source of truth:** [`task_registry_v1.md`](./task_registry_v1.md) holds canonical task state. **Only the Central Controller writes CLOSED.** Agents *propose*; the Controller *commits*.

**Registry First:** any task-management request must consult the registry before answering or acting — the registry is authoritative, conversation history is not. See [`registry_first_rule_v1.md`](./registry_first_rule_v1.md).

---

## 2. Lifecycle states

| State | Meaning | Entered by | Terminal? |
|-------|---------|-----------|-----------|
| `IN_PROGRESS` | Agent actively working | Controller (on assignment / on resume) | no |
| `BLOCKED` | Waiting on a named dependency | Controller (from an agent's proposed `BLOCKED`) | no |
| `RETURNED` | Work delivered, awaiting review | Controller (from an agent's proposed `RETURNED`) | no |
| `CHANGES_REQUESTED` | Returned for rework | Controller (on rejection) | no |
| `CLOSED` | Accepted and complete | **Controller only** (on acceptance) | **yes** |

### Transitions

```
                 ┌─────────────────────────────────────────────┐
                 │                                             │
   assign        ▼            propose RETURNED      accept     │
  ───────►  IN_PROGRESS ──────────────────────►  RETURNED ───────────►  CLOSED
                 ▲   │                               │  (Controller only)
       resume    │   │ propose BLOCKED               │
                 │   ▼                               │ request changes
                 │  BLOCKED                          ▼
                 │   │ dependency cleared      CHANGES_REQUESTED
                 │   │ (Controller)                  │
                 └───┴───────────────────────────────┘
                          resume → IN_PROGRESS
```

- An agent may move a task **out of** `IN_PROGRESS` only by *proposing* `RETURNED` or `BLOCKED` in its return block. The Controller records it.
- `RETURNED` → `CLOSED` and `RETURNED` → `CHANGES_REQUESTED` are **Controller-only**.
- `CHANGES_REQUESTED` → `IN_PROGRESS` happens **when work resumes** (Controller re-assigns / agent picks it back up).
- `BLOCKED` → `IN_PROGRESS` when the dependency clears.

---

## 3. Required agent return format (MANDATORY)

Every task return — from every agent — **must end** with this block, verbatim structure:

```
--- Registry Update (proposed) ---

Task: TASK-NNN

Proposed State:
- RETURNED
or
- BLOCKED

Deliverables Produced:
- item
- item
- item

Artifacts:
- file/path
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

### Rules

- Agents **may propose**: `RETURNED`, `BLOCKED`.
- Agents **may NEVER propose**: `CLOSED`, `ACCEPTED`.
- **Only the Central Controller can close work.**
- `Artifacts` lists concrete paths/links (files written, docs produced). If the deliverable is the return itself (advisory/analysis), state that explicitly.
- `Recommended Next Action` is advisory input to the Controller, not a state change.

---

## 4. Central Controller acceptance format

When the Central Controller accepts work:

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

On `CLOSED`, the Controller moves the task from **Active** to the **Recently Closed** table in [`task_registry_v1.md`](./task_registry_v1.md) with the accepted date.

---

## 5. Central Controller rejection format

When the Central Controller requests changes:

```
--- Registry Update ---

Task: TASK-NNN

New State:
- CHANGES_REQUESTED

Reason:
- explanation
```

When work resumes, state becomes:

```
- IN_PROGRESS
```

---

## 6. Command Center behavior (state legend)

The dashboard renders task state directly from the registry:

| State | Dashboard meaning |
|-------|-------------------|
| `IN_PROGRESS` | Agent actively working |
| `BLOCKED` | Waiting on dependency |
| `RETURNED` | Work delivered, awaiting review |
| `CHANGES_REQUESTED` | Returned for rework |
| `CLOSED` | Accepted and complete |

A task that is done-but-unaccepted now reads `RETURNED`, not `IN_PROGRESS` — which is the specific drift this protocol eliminates.

---

## 7. Ownership

| Action | Owner |
|--------|-------|
| Emit `Registry Update (proposed)` block on every return | **Assigned agent** |
| Propose `RETURNED` / `BLOCKED` | Assigned agent |
| Record state in the registry | **Central Controller** |
| `CLOSED` / `ACCEPTED` transition | **Central Controller (sole authority)** |
| `CHANGES_REQUESTED` transition | Central Controller |
| Move Active → Closed table | Central Controller |

Consistent with `operating_model_v2.md`: closure aligns with publication/acceptance authority — no agent self-closes its own work.

---

## 8. Examples

### 8.1 Agent return — RETURNED, recommend Accept

```
--- Registry Update (proposed) ---

Task: TASK-100

Proposed State:
- RETURNED

Deliverables Produced:
- New route /hashvaot/vegetable-spreads
- Registry entry in src/lib/comparisons/registry/categories/vegetable-spreads.ts
- Corpus scoped to vegetable-family subtypes only
- Page wired to ComparisonShelfPage template

Artifacts:
- src/app/hashvaot/vegetable-spreads/page.tsx
- src/lib/comparisons/registry/categories/vegetable-spreads.ts
- src/lib/comparisons/vegetable-spreads-comparison-page-data.ts

Blockers:
- none

Recommended Next Action:
- Accept
```

### 8.2 Agent return — BLOCKED on a dependency

```
--- Registry Update (proposed) ---

Task: TASK-101

Proposed State:
- BLOCKED

Deliverables Produced:
- Draft category eyebrow + headline (Hebrew)
- Draft methodologyLines copy

Artifacts:
- handoff/vegetable-spreads-copy-draft.md

Blockers:
- Hero stats (productCount, scoredCount, averageScore) cannot be finalized until TASK-100 confirms the final corpus definition.

Recommended Next Action:
- Open TASK-XXX
```

### 8.3 Agent return — RETURNED with a follow-up recommendation

```
--- Registry Update (proposed) ---

Task: TASK-111

Proposed State:
- RETURNED

Deliverables Produced:
- Field inventory for Comparison UI Reference v2
- Readiness assessment (exists / derivable / new pipeline / category-specific)
- Blocker list

Artifacts:
- This return (advisory; no files modified)

Blockers:
- none

Recommended Next Action:
- Open TASK-XXX  (fund base_pct main-ingredient extraction)
```

### 8.4 Controller acceptance

```
--- Registry Update ---

Task: TASK-100

New State:
- CLOSED

Accepted Date:
- 2026-05-31

Notes:
- Route live; corpus scoped correctly. Moved Active → Closed.
```

### 8.5 Controller rejection

```
--- Registry Update ---

Task: TASK-101

New State:
- CHANGES_REQUESTED

Reason:
- methodologyLines surface EXCEPTION-002 weight vocabulary; ontology-leakage policy requires consumer-safe phrasing. Re-author without internal weight language.
```

Then, when the Content Agent resumes:

```
New State:
- IN_PROGRESS
```

---

## 9. Enforcement

- A return **without** a `Registry Update (proposed)` block is **non-compliant** and is treated by the Controller as still `IN_PROGRESS` (no state change recorded).
- An agent proposing `CLOSED` or `ACCEPTED` is a protocol violation; the Controller disregards the proposed state and records `RETURNED` if deliverables are present.
- The registry is the single source of truth; a state asserted anywhere else (chat, handoff doc) is not binding until the Controller records it in [`task_registry_v1.md`](./task_registry_v1.md).

---

*Registry Protocol v1 — Bari / 2026-05-31*
