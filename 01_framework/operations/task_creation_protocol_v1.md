# Task Creation Protocol — v1

**Status:** Active — **MANDATORY**
**Date:** 2026-05-31
**Scope:** All agents and the Central Controller, at the moment Registry Work is opened
**Created by:** TASK-122 (Product Agent)
**Related:** [`work_classification_v1.md`](./work_classification_v1.md) · [`registry_first_rule_v1.md`](./registry_first_rule_v1.md) · [`registry_protocol_v1.md`](./registry_protocol_v1.md)

> This is the **entry gate** to the task lifecycle. It governs the moment a task is *opened*, completing the lifecycle that [`registry_protocol_v1.md`](./registry_protocol_v1.md) starts from *reporting* and *closing*. It adds **no new lifecycle states**, does **not** redesign the registry, and **automates nothing** — creating a task file is a manual, deliberate act.

---

## 0. Where tasks live

**`C:\Bari\tasks\TASK-NNN.md` — one file per task; state lives in the YAML frontmatter `status:` field.** The Command Center is *derived* from these files (`generate_dashboard.py` → `command_center.json` → `command_center_v4.html`). A task with **no file does not exist** to the system — no dashboard row, no lifecycle, no review. This is the failure this protocol prevents: TASK-120 and TASK-121 produced returns but were never opened as files, so they were invisible regardless of their proposed state.

---

## 1. The rule

**A task is registered at the instant it is opened — before substantive work begins.** Not at return time, not when the first deliverable lands. The registry file is the *act* of opening, not a record of it after the fact.

If Registry Work has begun and no `TASK-NNN.md` exists, the protocol has already been violated.

---

## 2. Who creates `TASK-NNN.md`  (Q1)

| Role | Responsibility |
|------|----------------|
| **Central Controller** | **Numbering authority.** Allocates the next sequential `TASK-NNN` (ids are sequential and never reused — there is no automation to allocate or de-duplicate them). Creates the file for any task it assigns or mints (the normal path). |
| **Assigned agent** | Creates the file for **self-initiated Registry Work** — when an agent recognizes mid-conversation that a request meets a Registry Work trigger (§6) — using the id the Controller allocates, before starting work. |

**The opener creates the file.** In practice that is the Controller for assigned/minted tasks (the dominant case, and the one that failed for TASK-120/121), and the assigned agent for self-initiated Registry Work. Either way the file exists before the work does. Numbering stays with the Controller so two openers never claim the same id.

---

## 3. At what moment is it created  (Q2)

**At the moment of opening** — defined as the first of these to occur:

- the Central Controller **assigns or mints** a `TASK-XXX`, or
- an agent **classifies an incoming request as Registry Work** (§6) and is about to begin it.

The file is created **before** any substantive work, with `status: IN_PROGRESS` (work starting now). The only other valid opening state is `status: BLOCKED`, used when the task opens already waiting on a *named, recorded* dependency — capture it in the `blocker:` field and `depends_on:`.

A task is **never** opened directly at `RETURNED`, `CHANGES_REQUESTED`, or `CLOSED` in the normal flow — those are lifecycle outcomes the Controller records later (per [`registry_protocol_v1.md`](./registry_protocol_v1.md) §4). *Exception — retroactive remediation:* when work was delivered before any file existed (the TASK-120 case), the Controller creates the file at the state that reflects reality and notes that it is a retroactive registration.

---

## 4. Minimum required fields  (Q3)

### Hard requirement (or the task is invisible / flagged)
`generate_dashboard.py` will only render a row if the file has a **valid YAML frontmatter block** (`---` … `---`) containing an **`id`**. A file with no frontmatter, malformed YAML, or no `id` is surfaced as `REGISTRY_UNPARSEABLE` and never reaches a section. So the one non-negotiable is: **a parseable frontmatter block with `id`.**

### Minimum fields for a correct, non-misleading task row
Beyond the hard requirement, an opened task must set these so its dashboard row is accurate rather than defaulted:

```yaml
---
id: TASK-NNN                 # REQUIRED — must match the filename
title: <one-line title>      # REQUIRED — human-readable
owner: <agent>               # REQUIRED — e.g. frontend-agent, content-agent, data-agent, product-agent
status: IN_PROGRESS          # REQUIRED at open — IN_PROGRESS (or BLOCKED if opening blocked)
priority: HIGH | MEDIUM | LOW # REQUIRED — defaults to MEDIUM if omitted; set it explicitly
created_at: YYYY-MM-DD       # REQUIRED — the open date
depends_on: []               # list of TASK ids this waits on (default empty)
blocks: []                   # list of TASK ids waiting on this (default empty)
category_id: null            # comparison category id, or null
summary: >                   # 1–3 lines: what the task delivers
  <what this task delivers and why>
---

# TASK-NNN — <Title>

<Short body: context / scope / the deliverable.>
```

Notes:
- `completed_at` is **not** set at open — the Controller adds it only on `CLOSED`.
- `blocker:` (free text) is set only when `status: BLOCKED`.
- The `# TASK-NNN — Title` body header and a short body are convention (human-facing); the dashboard reads only the frontmatter.

---

## 5. How the dashboard sees newly opened tasks  (Q4)

**It does not see them automatically — the dashboard is derived, not live.** Creating the file makes the task *eligible*; it appears only after a regeneration:

1. The opener creates `C:\Bari\tasks\TASK-NNN.md` (§§2–4).
2. The **Central Controller** runs `python generate_dashboard.py` (in `05_command_center\`). This rebuilds `command_center.json`; a new `IN_PROGRESS` task renders under **Active Work** (a `BLOCKED` one under **Blockers**), per [`registry_protocol_v1.md`](./registry_protocol_v1.md) §5.
3. **Never hand-edit `command_center.json`** — it is regenerated output.

Until step 2 runs, the new file is invisible on the served dashboard, and `check_drift.py` will raise `SNAPSHOT_DRIFT` (a registry source file is newer than the served JSON). Regeneration remains a **deliberate manual action** — this protocol defines the step; it does not wire a hook, watcher, or schedule to perform it.

---

## 6. Registry Work vs Conversation Work at creation time  (Q5)

Classification is the gate **in front of** creation — apply [`work_classification_v1.md`](./work_classification_v1.md) **before** minting an id. Only Registry Work gets a file.

A request is **Registry Work** (→ create a file) if **any** hold:
- it is multi-step or spans more than one work session;
- it produces a deliverable that will be **reviewed / accepted** (`RETURNED → CLOSED`);
- another task or agent **depends on** its outcome;
- it changes shipped product, scoring, governance, or the dashboard itself;
- the Central Controller **explicitly assigns it a `TASK-XXX`** (assignment is itself sufficient).

Otherwise it is **Conversation Work** — handle it inline: **no id, no file, no dashboard entry.**

```
Incoming request
   │
   ├─ Conversation Work? (quick advice, clarification, prompt/copy tweak, one-off, light review)
   │      → answer inline. Do NOT create a file.
   │
   └─ Registry Work? (any trigger above, incl. an explicit TASK-XXX assignment)
          → Controller allocates the next TASK-NNN
          → opener creates tasks/TASK-NNN.md at IN_PROGRESS (§§2–4)
          → Controller regenerates the dashboard (§5)
```

When genuinely unsure, default to **Conversation Work** — do not create tasks "just in case." Promote to Registry Work only when a trigger is actually met. The cost of a missing file (invisible work — the TASK-120 failure) and the cost of a needless file (registry/dashboard clutter) are both real; classification decides correctly between them.

---

## 7. Worked example

Controller assigns a vegetable-spreads content review:

1. Controller classifies it as Registry Work (reviewed deliverable, depends on TASK-100/101) and allocates **TASK-120**.
2. Controller (the opener) creates `C:\Bari\tasks\TASK-120.md`:
   ```yaml
   ---
   id: TASK-120
   title: Review vegetable-spreads comparison experience; enrichment roadmap
   owner: content-agent
   status: IN_PROGRESS
   priority: MEDIUM
   created_at: 2026-05-31
   depends_on: [TASK-100, TASK-101]
   blocks: []
   category_id: null
   summary: >
     Evaluate the vegetable-spreads comparison page (category explanation,
     methodology, insight quality, consumer usefulness) and recommend an
     enrichment roadmap. Advisory; no copy changes.
   ---

   # TASK-120 — Vegetable Spreads Content Review
   ```
3. Controller runs `generate_dashboard.py` → TASK-120 shows under **Active Work** before the Content Agent starts.
4. On return, the Content Agent emits its `Registry Update (proposed)` block; the Controller records `RETURNED` and regenerates (that path is [`registry_protocol_v1.md`](./registry_protocol_v1.md), not this one).

Had step 2 happened at assignment, TASK-120 would have been visible throughout — the gap TASK-121 traced.

---

## 8. What this protocol prevents

- **Invisible work** — a returned/in-progress task with no registry file (TASK-120, TASK-121).
- **Deferred registration** — "I'll add the file when I return" leaves the dashboard blind during the work.
- **Id collisions / reuse** — centralized numbering keeps ids sequential and unique.
- **Phantom deliverables** — artifacts referencing a `TASK-NNN` that has no file (`PHANTOM_TASK` drift) become the exception, not the norm.

This protocol is convention-based, like the rest of the Agent OS: there is no CI gate. Agents and the Controller follow it because opening without registering is what makes work disappear.

---

*Task Creation Protocol v1 — Bari Agent OS / 2026-05-31*
